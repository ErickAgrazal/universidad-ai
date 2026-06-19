#!/usr/bin/env python3
"""Auto-grade PollClass lab submissions against the rubric.

Reads a student folder, finds the pollclass project, extracts grading signals,
applies the rubric, writes GRADING.md, and returns a score (0-100).

Rubric (5 criteria, 20pts each):
1. Funcionalidad completa (PRD compliance, profesor/estudiante views, polls, votes)
2. Interfaz responsive (Tailwind, mobile-friendly)
3. Validación de votos (one vote per student per poll)
4. Documentación del proyecto (README quality, screenshots, agentic evidence)
5. Despliegue exitoso (ngrok setup)
"""
import json
import os
import re
import sys
from pathlib import Path

from alt_repo import discover_and_clone


IMG_EXT = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
CODE_EXT = {'.js', '.jsx', '.ts', '.tsx'}
# Top-level GitHub repo names that suggest a student kept the PollClass app
# in a separate repo (instead of the course repo). Order = preference rank.
ALT_REPO_KEYWORDS = ('pollclass', 'pollify', 'encuesta-clase', 'poll-class')


def find_project_root(repo: Path) -> Path | None:
    """Find the pollclass project root - directory with package.json near a 'pollclass'-named ancestor or sibling.

    Strongly prefers paths containing pollclass/lab5/asignacion5 keywords. Ignores templates,
    presentations, and other unrelated React projects.
    """
    POSITIVE = ('pollclass', 'pollify', 'asignacion5', 'asignacion_5', 'asignacion-5',
                'lab5', 'laboratorio5', 'laboratorio 5', 'laboratorio-5',
                'lab_5', 'lab 5')
    EXCLUDE = ('tema_asignado', 'tema-asignado', 'template', 'plantilla', 'presentacion',
               'presentación', 'investigacion', 'investigación', 'informe',
               'parcial1', 'parcial2', 'parcial', 'parciales',
               'proyecto1', 'proyecto2', 'proyectos/',
               'lab1', 'lab2', 'lab3', 'lab4', 'lab6', 'lab7',
               'laboratorio1', 'laboratorio2', 'laboratorio3', 'laboratorio4',
               'laboratorio-1', 'laboratorio-2', 'laboratorio-3', 'laboratorio-4',
               'laboratorio6', 'laboratorio 6', 'laboratorio-6', 'laboratorio7',
               'playwright',  # lab 6 is playwright
               'asignacion1', 'asignacion2', 'asignacion3', 'asignacion4', 'asignacion6')

    candidates = []
    for pj in repo.rglob('package.json'):
        if 'node_modules' in pj.parts or '.git' in pj.parts:
            continue
        # Only consider path *inside* the student repo, not parents
        rel = pj.relative_to(repo)
        # `_alt-repo/` is provenance from a prior auto-recovery run — not part
        # of the student's original submission. analyze_repo() recurses into it
        # explicitly. The check uses RELATIVE parts so that when we recurse
        # INTO `_alt-repo` itself, its own contents aren't skipped.
        if '_alt-repo' in rel.parts:
            continue
        rel_lower = str(rel).lower()
        # Check package.json name field for pollclass/poll keyword (strongest signal)
        pkg_name = ''
        try:
            pkg_data = json.loads(pj.read_text(errors='ignore'))
            pkg_name = pkg_data.get('name', '').lower()
        except Exception:
            pass
        name_match = any(k in pkg_name for k in ('pollclass', 'pollify', 'poll-', 'poll_', 'encuesta'))
        # Hard exclude (only if name doesn't directly identify it)
        if any(x in rel_lower for x in EXCLUDE) and not name_match:
            if not any(p in rel_lower for p in ('pollclass', 'pollify')):
                continue
        score = 0
        for kw in POSITIVE:
            if kw in rel_lower:
                score += 20
        if name_match:
            score += 50  # package.json name is the strongest signal
        # Penalize 'test', 'tests', 'e2e' folders/names (separate test repos)
        if 'test' in pkg_name or 'tests' in rel_lower or '-tests/' in rel_lower or '/e2e/' in rel_lower:
            score -= 30
        # Penalty for being in a 'client' or 'server' subdir vs root
        last_parts = [p.lower() for p in pj.parts[-3:]]
        if 'client' in last_parts or 'server' in last_parts or 'backend' in last_parts or 'frontend' in last_parts:
            score -= 2
        score -= len(rel.parts)  # prefer shallower in lab tree
        candidates.append((score, pj))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    best_pj = candidates[0][1]
    parent = best_pj.parent
    parent_name = parent.name.lower()
    # If best is .../X/client (or server/backend/frontend)/package.json,
    # use X as project root (the lab dir), regardless of whether X has its own package.json.
    if parent_name in ('client', 'server', 'backend', 'frontend', 'web', 'api',
                       'e2e', 'tests', 'mobile', 'app', 'apps', 'src'):
        return parent.parent
    return parent


def collect_files(root: Path, exts=None, max_files=2000):
    """Walk repo files (excluding node_modules/.git)."""
    out = []
    for p in root.rglob('*'):
        if not p.is_file():
            continue
        parts = p.parts
        if 'node_modules' in parts or '.git' in parts:
            continue
        if exts and p.suffix.lower() not in exts:
            continue
        out.append(p)
        if len(out) >= max_files:
            break
    return out


def grep_files(files, patterns):
    """Return dict pattern -> count of matching files."""
    out = {p: 0 for p in patterns}
    compiled = {p: re.compile(p, re.IGNORECASE | re.MULTILINE) for p in patterns}
    for f in files:
        try:
            text = f.read_text(errors='ignore')
        except Exception:
            continue
        for p, c in compiled.items():
            if c.search(text):
                out[p] += 1
    return out


def read_package_json(root: Path) -> dict:
    """Merge all package.json deps across the project."""
    all_deps = {}
    scripts = {}
    for pj in root.rglob('package.json'):
        if 'node_modules' in pj.parts:
            continue
        try:
            d = json.loads(pj.read_text(errors='ignore'))
        except Exception:
            continue
        all_deps.update(d.get('dependencies', {}))
        all_deps.update(d.get('devDependencies', {}))
        scripts.update(d.get('scripts', {}))
    return {'deps': all_deps, 'scripts': scripts}


def analyze_repo(repo: Path, allow_alt_repo: bool = True) -> dict:
    """Extract grading signals from a student repo.

    If the conventional course repo doesn't contain a pollclass project AND
    `allow_alt_repo` is True, queries the student's other public GitHub repos
    for a keyword match (Phase 4.5 step 4 of the skill). If found, clones to
    `<repo>/_alt-repo/` and re-runs analysis against that.
    """
    sig = {
        'has_project': False,
        'project_root': None,
        'stack': {'react': False, 'vite': False, 'bun': False, 'mongoose': False, 'mongodb': False, 'tailwind': False},
        'bun_lock': False,
        'readme_lines': 0,
        'readme_path': None,
        'images': 0,
        'pollclass_images': 0,  # images inside the pollclass project
        'code_files': 0,
        'has_vote_validation': False,
        'vote_signal_files': 0,
        'has_setinterval': False,
        'has_websocket': False,
        'has_polling': False,
        'profesor_view': False,
        'estudiante_view': False,
        'mongodb_models': 0,
        'tailwind_config': False,
        'ngrok_mentions': 0,
        'agentic_evidence': 0,
        'opencode_screenshot': False,
        'has_charts': False,
        'alt_repo_used': None,        # full_name of cloned alt repo, if any
        'alt_repo_candidates': [],    # surfaced in GRADING.md even when none cloned successfully
    }
    root = find_project_root(repo)
    if root is None and allow_alt_repo:
        alt = discover_and_clone(repo, ALT_REPO_KEYWORDS)
        sig['alt_repo_candidates'] = [
            {'full_name': c['full_name'], 'url': c.get('html_url'), 'updated_at': c.get('updated_at')}
            for c in alt['candidates']
        ]
        if alt['path']:
            alt_root = find_project_root(alt['path'])
            if alt_root is not None:
                sig['alt_repo_used'] = alt['used']
                repo = alt['path']
                root = alt_root
    if root is None:
        return sig
    sig['has_project'] = True
    sig['project_root'] = str(root.relative_to(repo))

    pkg = read_package_json(root)
    deps_lower = ' '.join(pkg['deps'].keys()).lower()
    sig['stack']['react'] = 'react' in deps_lower
    sig['stack']['vite'] = 'vite' in deps_lower
    sig['stack']['bun'] = 'bun' in deps_lower or any('@types/bun' in d for d in pkg['deps'])
    sig['stack']['mongoose'] = 'mongoose' in deps_lower
    sig['stack']['mongodb'] = 'mongodb' in deps_lower
    sig['stack']['tailwind'] = 'tailwind' in deps_lower

    # Charts
    sig['has_charts'] = any(k in deps_lower for k in ['chart', 'recharts', 'd3', 'apexchart', 'victory'])

    # bun.lock presence (either at project root or repo root)
    for p in [root / 'bun.lock', root / 'bun.lockb', repo / 'bun.lock', repo / 'bun.lockb']:
        if p.exists():
            sig['bun_lock'] = True
            break

    # README — find top-level README in project or repo, or in lab dir
    readmes = []
    for r in repo.rglob('README.md'):
        if 'node_modules' in r.parts:
            continue
        # Prefer README in project root or one level up
        depth = len(r.relative_to(repo).parts)
        in_proj = str(r).startswith(str(root))
        score = (10 if in_proj else 0) - depth
        readmes.append((score, r))
    readmes.sort(reverse=True)
    if readmes:
        best = readmes[0][1]
        try:
            content = best.read_text(errors='ignore')
            sig['readme_lines'] = len(content.splitlines())
            sig['readme_path'] = str(best.relative_to(repo))
            # Check screenshots referenced in README
            if any(kw in content.lower() for kw in ['screenshot', 'captura', '![', 'imagen', 'opencode']):
                sig['readme_has_images'] = True
        except Exception:
            pass

    # Image files in pollclass project
    for img in root.rglob('*'):
        if img.is_file() and img.suffix.lower() in IMG_EXT and 'node_modules' not in img.parts:
            sig['pollclass_images'] += 1
    # Total images in repo
    for img in repo.rglob('*'):
        if img.is_file() and img.suffix.lower() in IMG_EXT and 'node_modules' not in img.parts and '.git' not in img.parts:
            sig['images'] += 1

    # Code analysis
    code_files = collect_files(root, exts=CODE_EXT)
    sig['code_files'] = len(code_files)

    patterns = {
        'vote_unique': r'(unique\s*:\s*true|hasVoted|alreadyVoted|voted.*before|userId.*poll|voterId|findOne.*vote.*user|voto.*unico|one.*vote)',
        'set_interval': r'setInterval\s*\(',
        'websocket': r'(WebSocket|socket\.io|ws://|new\s+WebSocket)',
        'mongoose_model': r'mongoose\.(model|Schema)|new\s+Schema|MongoClient|db\.collection|getCollection',
        'tailwind_class': r'className\s*=\s*"[^"]*(flex|grid|p-\d|m-\d|w-\d|md:|sm:|lg:)',
        'profesor': r'(profesor|teacher|professor|/teacher|/profesor)',
        'estudiante': r'(estudiante|student|/student|/estudiante|join.*code)',
        'chart': r'(Chart|recharts|<Bar|<Pie|<Line|chart\.js)',
    }
    matches = grep_files(code_files, list(patterns.values()))
    sig['vote_signal_files'] = matches[patterns['vote_unique']]
    sig['has_vote_validation'] = sig['vote_signal_files'] > 0
    sig['has_setinterval'] = matches[patterns['set_interval']] > 0
    sig['has_websocket'] = matches[patterns['websocket']] > 0
    sig['has_polling'] = sig['has_setinterval'] and not sig['has_websocket']
    sig['mongodb_models'] = matches[patterns['mongoose_model']]
    sig['profesor_view'] = matches[patterns['profesor']] > 0
    sig['estudiante_view'] = matches[patterns['estudiante']] > 0
    sig['tailwind_class_files'] = matches[patterns['tailwind_class']]
    sig['has_charts'] = sig['has_charts'] or matches[patterns['chart']] > 0

    # Tailwind config
    for cfgname in ['tailwind.config.js', 'tailwind.config.ts', 'tailwind.config.cjs', 'tailwind.config.mjs']:
        for cfg in [root / cfgname]:
            if cfg.exists():
                sig['tailwind_config'] = True
                break
        # Also check nested client dir
        for cfg in (root / 'client').rglob(cfgname) if (root / 'client').exists() else []:
            if 'node_modules' not in cfg.parts:
                sig['tailwind_config'] = True
                break

    # ngrok mentions
    for f in collect_files(repo, exts={'.md', '.txt', '.json', '.yaml', '.yml', '.env', '.sh', '.js', '.ts'}):
        try:
            if 'ngrok' in f.read_text(errors='ignore').lower():
                sig['ngrok_mentions'] += 1
        except Exception:
            pass

    # Agentic evidence in markdown
    for f in repo.rglob('*.md'):
        if 'node_modules' in f.parts:
            continue
        try:
            text = f.read_text(errors='ignore').lower()
            if any(kw in text for kw in ['opencode', 'copilot', 'claude', 'cursor', 'agente', 'agéntico', 'agentico']):
                sig['agentic_evidence'] += 1
        except Exception:
            pass

    # OpenCode screenshot? check image filenames
    for img in repo.rglob('*'):
        if img.is_file() and img.suffix.lower() in IMG_EXT:
            name = img.name.lower()
            if any(kw in name for kw in ['opencode', 'copilot', 'claude', 'agentic', 'agente', 'historial']):
                sig['opencode_screenshot'] = True
                break

    return sig


def grade(sig: dict) -> dict:
    """Apply rubric to signals, return per-criterion points (1-4) and total /100."""
    if not sig['has_project']:
        return {
            'funcionalidad': 1, 'interfaz': 1, 'validacion': 1, 'documentacion': 1, 'despliegue': 1,
            'total': 25, 'notes': 'No project found - student turned in something but no pollclass app detected'
        }

    # 1. Funcionalidad completa
    stack_ok = sum([sig['stack']['react'], sig['stack']['vite'],
                    sig['stack']['mongoose'] or sig['stack']['mongodb'],
                    sig['stack']['tailwind']])
    # Profesor + Estudiante views + DB models + polling
    has_views = sig['profesor_view'] and sig['estudiante_view']
    has_models = sig['mongodb_models'] >= 1
    has_realtime = sig['has_polling'] or sig['has_setinterval']

    # Detect if this is actually PollClass (vs. some unrelated project)
    is_pollclass = has_views or has_models or sig['has_vote_validation']

    if (stack_ok >= 3 and has_views and has_models and has_realtime
            and sig['has_vote_validation'] and not sig['has_websocket']):
        func = 4  # Excelente
    elif stack_ok >= 3 and has_views and has_models and (has_realtime or sig['has_vote_validation']):
        func = 3  # Bueno
    elif sig['code_files'] >= 10 and (has_views or has_models):
        func = 2  # Normal
    else:
        func = 1  # Deficiente

    # 2. Interfaz responsive
    tw_classes = sig.get('tailwind_class_files', 0)
    if (sig['stack']['tailwind'] and tw_classes >= 3) or (tw_classes >= 5 and sig['tailwind_config']):
        interfaz = 4
    elif sig['stack']['tailwind'] or tw_classes >= 3:
        interfaz = 3
    elif tw_classes >= 1:
        interfaz = 2
    else:
        interfaz = 1
    # Cap interfaz if the project isn't PollClass at all
    if not is_pollclass:
        interfaz = min(interfaz, 1)

    # 3. Validación de votos
    if sig['has_vote_validation'] and sig['vote_signal_files'] >= 2:
        validacion = 4
    elif sig['has_vote_validation']:
        validacion = 3
    elif sig['mongodb_models'] >= 1:  # has DB structure but unclear validation
        validacion = 2
    else:
        validacion = 1

    # 4. Documentación
    score_doc = 0
    if sig['readme_lines'] >= 50: score_doc += 1
    if sig['readme_lines'] >= 100: score_doc += 1
    if sig['pollclass_images'] >= 3 or sig['images'] >= 3: score_doc += 1
    if sig['agentic_evidence'] >= 1 or sig['opencode_screenshot']: score_doc += 1
    doc = max(1, score_doc)

    # 5. Despliegue (ngrok)
    if sig['ngrok_mentions'] >= 2:
        despliegue = 4
    elif sig['ngrok_mentions'] == 1:
        despliegue = 3
    elif any('deploy' in s.lower() or 'serve' in s.lower() or 'host' in s.lower()
             for s in [str(sig['readme_path'] or '')]):
        despliegue = 2
    else:
        despliegue = 2  # default to Normal if ngrok not explicitly evident - apps were deployed in class

    total = (func + interfaz + validacion + doc + despliegue) * 5
    return {
        'funcionalidad': func,
        'interfaz': interfaz,
        'validacion': validacion,
        'documentacion': doc,
        'despliegue': despliegue,
        'total': total,
    }


def grade_label(p):
    return {4: 'Excelente', 3: 'Bueno', 2: 'Normal', 1: 'Deficiente'}.get(p, '?')


def _format_alt_repo_block(sig: dict, scores: dict) -> str:
    """Build the alt-repo provenance block for GRADING.md.

    Three cases:
      - Recovered (alt repo found and used): note which one was scored.
      - Candidates available but none yielded a project: list them so a human
        can verify (e.g. an alt repo that's also off-topic).
      - No candidates: stay silent.
    """
    used = sig.get('alt_repo_used')
    candidates = sig.get('alt_repo_candidates') or []
    if used:
        return (
            f"\n> Calificación recuperada del repo alterno **{used}** "
            f"(el repo del curso no contenía la app PollClass).\n"
        )
    if scores['total'] == 25 and candidates:
        lines = ["\n## Posibles repos alternos (revisar manualmente)\n",
                 "El repo del curso no contiene la app. Estos repos públicos del usuario "
                 "matchean keywords del lab:\n"]
        for c in candidates:
            updated = (c.get('updated_at') or '')[:10]
            lines.append(f"- [`{c['full_name']}`]({c.get('url')}) — actualizado {updated}")
        lines.append("")
        return "\n".join(lines)
    return ""


def write_grading_md(student_dir: Path, sig: dict, scores: dict):
    name = student_dir.name
    alt_block = _format_alt_repo_block(sig, scores)
    md = f"""# Calificación — {name}

**Score total: {scores['total']}/100**
{alt_block}
## Signals detectados

- Proyecto encontrado: {sig['has_project']} ({sig.get('project_root', '—')})
- Stack: React={sig['stack']['react']}, Vite={sig['stack']['vite']}, Bun={sig['stack']['bun']}, MongoDB/Mongoose={sig['stack']['mongoose'] or sig['stack']['mongodb']}, Tailwind={sig['stack']['tailwind']}
- bun.lock: {sig['bun_lock']}
- Vista profesor detectada: {sig['profesor_view']}
- Vista estudiante detectada: {sig['estudiante_view']}
- Modelos MongoDB: {sig['mongodb_models']} archivo(s)
- Validación de voto (señales): {sig['vote_signal_files']} archivo(s)
- setInterval (polling): {sig['has_setinterval']}
- WebSocket: {sig['has_websocket']}
- Tailwind config: {sig['tailwind_config']}, archivos con clases tailwind: {sig.get('tailwind_class_files', 0)}
- Charts: {sig['has_charts']}
- Capturas (en pollclass): {sig['pollclass_images']} / total repo: {sig['images']}
- README: {sig['readme_lines']} líneas ({sig['readme_path']})
- ngrok menciones: {sig['ngrok_mentions']}
- Evidencia agéntica (md): {sig['agentic_evidence']}; screenshot OpenCode: {sig['opencode_screenshot']}
- Archivos de código: {sig['code_files']}

## Calificación por criterio

| Criterio | Nivel | Puntos | Aporte /100 |
|---|---|---|---|
| Funcionalidad completa | {grade_label(scores['funcionalidad'])} | {scores['funcionalidad']}/4 | {scores['funcionalidad']*5} |
| Interfaz responsive | {grade_label(scores['interfaz'])} | {scores['interfaz']}/4 | {scores['interfaz']*5} |
| Validación de votos | {grade_label(scores['validacion'])} | {scores['validacion']}/4 | {scores['validacion']*5} |
| Documentación | {grade_label(scores['documentacion'])} | {scores['documentacion']}/4 | {scores['documentacion']*5} |
| Despliegue | {grade_label(scores['despliegue'])} | {scores['despliegue']}/4 | {scores['despliegue']*5} |
| **TOTAL** | | | **{scores['total']}/100** |

"""
    (student_dir / 'GRADING.md').write_text(md)


def main():
    if len(sys.argv) < 2:
        print('Usage: grade_pollclass.py <student-folder|group-folder>')
        sys.exit(1)
    target = Path(sys.argv[1])
    student_dirs = []
    if (target / '.git').exists():
        # Target IS a student repo. The presence of a nested `_alt-repo/.git`
        # from a prior recovery run must not flip us into group-mode.
        student_dirs = [target]
    elif any(target.rglob('package.json')):
        nested = [c for c in target.glob('*/.git') if c.parent.name != '_alt-repo']
        student_dirs = list(target.iterdir()) if nested else [target]
    if not student_dirs:
        student_dirs = [d for d in target.iterdir()
                        if d.is_dir() and (d / '.git').exists() and d.name != '_alt-repo']

    rows = []
    for sd in sorted(student_dirs):
        if not sd.is_dir():
            continue
        sig = analyze_repo(sd)
        scores = grade(sig)
        write_grading_md(sd, sig, scores)
        rows.append((sd.name, scores))

    print(f'\n{"Student":<25} {"Func":<5} {"Resp":<5} {"Vot":<5} {"Doc":<5} {"Depl":<5} {"TOTAL"}')
    print('-' * 70)
    for name, s in rows:
        print(f'{name:<25} {s["funcionalidad"]:<5} {s["interfaz"]:<5} {s["validacion"]:<5} {s["documentacion"]:<5} {s["despliegue"]:<5} {s["total"]}/100')
    if rows:
        avg = sum(s['total'] for _, s in rows) / len(rows)
        below80 = sum(1 for _, s in rows if s['total'] < 80)
        print(f'\nN={len(rows)}  avg={avg:.1f}  below 80: {below80}/{len(rows)}')


if __name__ == '__main__':
    main()
