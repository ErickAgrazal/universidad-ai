#!/usr/bin/env python3
"""Auto-grade Asignación 6: Playwright test suite for PollClass.

Adapted from grade_template.py. Reuses project root detection but targets the
laboratorio 6 (Playwright tests) instead of PollClass app.

Rubric criteria (4 × 25%):
1. Cobertura de flujos críticos: count of distinct test() blocks (3+=4, 2=3, 1=2, 0=1)
2. Assertions verificables: count of expect() calls, weighted (rich=4, some=3, navigation-only=2, none=1)
3. Caso negativo: detect error/fail/negative tests
4. Bitácora: README or BITACORA file documenting agent interactions
"""
import json
import re
import sys
from pathlib import Path

from alt_repo import discover_and_clone


CODE_EXT = {'.js', '.ts', '.jsx', '.tsx'}
# Repo-name keywords that suggest a separate Playwright test repo (or the
# PollClass repo, since A6 tests usually live inside the PollClass project).
ALT_REPO_KEYWORDS = ('playwright', 'pollclass', 'pollify', 'e2e-tests', 'pollclass-tests')


def find_playwright_root(repo: Path) -> Path | None:
    """Find the Playwright test project root.

    Strategy:
    - Look for playwright.config.* files
    - Prefer paths with 'lab6', 'laboratorio-6', 'pollclass-playwright', 'playwright'
    - Exclude lab1-5 unless they have playwright config too
    """
    POSITIVE = ('lab6', 'laboratorio6', 'laboratorio-6', 'laboratorio 6',
                'lab_6', 'lab 6', 'pollclass-playwright', 'playwright',
                'asignacion6', 'asignacion-6', 'asignacion_6', 'tests')
    # Don't exclude lab5/pollclass because Playwright tests OFTEN live inside the
    # PollClass project (e.g. pollclass/tests/, pollclass/e2e/)
    EXCLUDE = ('tema_asignado', 'template', 'plantilla', 'presentacion',
               'parcial1', 'parcial2', 'investigacion', 'informe')

    candidates = []
    # First pass: playwright.config files. Skip `_alt-repo/` — that's provenance
    # metadata; analyze_repo() recurses into it explicitly when needed. The
    # check uses path-relative-to-repo so recursion INTO _alt-repo still works.
    for cfg in repo.rglob('playwright.config*'):
        if 'node_modules' in cfg.parts or '.git' in cfg.parts:
            continue
        if '_alt-repo' in cfg.relative_to(repo).parts:
            continue
        candidates.append((100, cfg.parent))

    # Second pass: package.json with playwright in deps OR a 'tests'/'e2e' folder with .spec files
    for pj in repo.rglob('package.json'):
        if 'node_modules' in pj.parts or '.git' in pj.parts:
            continue
        if '_alt-repo' in pj.relative_to(repo).parts:
            continue
        rel_lower = str(pj.relative_to(repo)).lower()
        if any(x in rel_lower for x in EXCLUDE):
            continue
        try:
            pkg = json.loads(pj.read_text(errors='ignore'))
            deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
            has_playwright = any('playwright' in d.lower() for d in deps)
            pkg_name = pkg.get('name', '').lower()
            score = 0
            if has_playwright:
                score += 50
            for kw in POSITIVE:
                if kw in rel_lower or kw in pkg_name:
                    score += 20
            score -= len(pj.parts)
            if score > 0:
                candidates.append((score, pj.parent))
        except Exception:
            continue

    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


def analyze_repo(repo: Path, allow_alt_repo: bool = True) -> dict:
    sig = {
        'has_tests': False,
        'project_root': None,
        'playwright_config': False,
        'spec_files': 0,
        'test_blocks': 0,
        'expect_calls': 0,
        'expect_per_test': 0.0,
        'has_negative_case': False,
        'negative_indicators': 0,
        'has_bitacora': False,
        'bitacora_lines': 0,
        'bitacora_mentions_agent': False,
        'critical_flows_estimated': 0,
        'has_visit_only': False,  # only goto() with no expect — bad
        'alt_repo_used': None,
        'alt_repo_candidates': [],
    }
    root = find_playwright_root(repo)
    if root is None and allow_alt_repo:
        alt = discover_and_clone(repo, ALT_REPO_KEYWORDS)
        sig['alt_repo_candidates'] = [
            {'full_name': c['full_name'], 'url': c.get('html_url'), 'updated_at': c.get('updated_at')}
            for c in alt['candidates']
        ]
        if alt['path']:
            alt_root = find_playwright_root(alt['path'])
            if alt_root is not None:
                sig['alt_repo_used'] = alt['used']
                repo = alt['path']
                root = alt_root
    if root is None:
        return sig
    sig['has_tests'] = True
    sig['project_root'] = str(root.relative_to(repo))

    # Playwright config present?
    for f in root.iterdir() if root.exists() else []:
        if f.name.lower().startswith('playwright.config'):
            sig['playwright_config'] = True
            break

    # Walk spec files
    test_files = []
    for f in root.rglob('*'):
        if not f.is_file() or 'node_modules' in f.parts or '.git' in f.parts:
            continue
        name = f.name.lower()
        if f.suffix.lower() in CODE_EXT and ('.spec.' in name or '.test.' in name or name.startswith('test')):
            test_files.append(f)
        elif f.suffix.lower() in CODE_EXT and any(p.name.lower() in ('tests', 'e2e', '__tests__') for p in f.parents):
            test_files.append(f)
    sig['spec_files'] = len(test_files)

    # Count test() blocks and expect() calls
    total_tests = 0
    total_expects = 0
    negative_count = 0
    visit_only_files = 0
    for f in test_files:
        try:
            text = f.read_text(errors='ignore')
        except Exception:
            continue
        # test() and test.describe() blocks
        tests_here = len(re.findall(r'\b(test|it)\s*\(\s*[\'"]', text))
        expects_here = len(re.findall(r'\bexpect\s*\(', text))
        # Negative case indicators
        if re.search(r'(should\s+not|must\s+not|cannot|negative|invalid|error|fail|forbid|denied|unauthor|reject|duplicate.*vote|already.*vot|alreadyVoted|voto.*duplic)', text, re.IGNORECASE):
            negative_count += 1
        if tests_here > 0 and expects_here == 0:
            visit_only_files += 1
        total_tests += tests_here
        total_expects += expects_here

    sig['test_blocks'] = total_tests
    sig['expect_calls'] = total_expects
    sig['expect_per_test'] = total_expects / max(1, total_tests)
    sig['negative_indicators'] = negative_count
    sig['has_negative_case'] = negative_count > 0
    sig['has_visit_only'] = visit_only_files >= sig['spec_files'] // 2 and sig['spec_files'] > 0

    # Critical flow estimation: roughly tests / 2 (assumes each flow has multiple expects/steps)
    sig['critical_flows_estimated'] = min(total_tests, 10)

    # Bitácora / README de la suite
    bitacora_candidates = []
    for r in repo.rglob('*'):
        if not r.is_file() or 'node_modules' in r.parts or '.git' in r.parts: continue
        if r.suffix.lower() != '.md': continue
        nm = r.name.lower()
        if any(kw in nm for kw in ('bitacora', 'bitácora', 'log', 'changelog', 'context', 'handoff', 'historial')) or nm == 'readme.md':
            # Prefer ones inside playwright project root
            in_root = str(r).startswith(str(root))
            bitacora_candidates.append((1 if in_root else 0, r))
    bitacora_candidates.sort(reverse=True)
    if bitacora_candidates:
        path = bitacora_candidates[0][1]
        try:
            text = path.read_text(errors='ignore')
            sig['bitacora_lines'] = len(text.splitlines())
            sig['has_bitacora'] = sig['bitacora_lines'] >= 10
            if any(kw in text.lower() for kw in ['opencode', 'copilot', 'claude', 'cursor', 'agente', 'agéntico', 'agentico', 'playwright']):
                sig['bitacora_mentions_agent'] = True
        except Exception:
            pass

    return sig


def grade(sig: dict) -> dict:
    if not sig['has_tests']:
        return {'cobertura': 1, 'assertions': 1, 'negativo': 1, 'bitacora': 1, 'total': 25}

    # 1. Cobertura de flujos críticos — by # of test blocks
    tb = sig['test_blocks']
    if tb >= 6:
        cobertura = 4
    elif tb >= 4:
        cobertura = 3
    elif tb >= 1:
        cobertura = 2
    else:
        cobertura = 1

    # 2. Assertions verificables
    ept = sig['expect_per_test']
    if ept >= 2.5:
        assertions = 4  # rich assertions
    elif ept >= 1.0:
        assertions = 3
    elif ept >= 0.3:
        assertions = 2  # superficial
    else:
        assertions = 1

    # 3. Caso negativo
    if sig['negative_indicators'] >= 2:
        negativo = 4
    elif sig['negative_indicators'] == 1:
        negativo = 3
    elif sig['spec_files'] >= 2:
        negativo = 2  # might exist but pattern not detected
    else:
        negativo = 1

    # 4. Bitácora
    if sig['bitacora_lines'] >= 100 and sig['bitacora_mentions_agent']:
        bitacora = 4
    elif sig['bitacora_lines'] >= 50:
        bitacora = 3
    elif sig['bitacora_lines'] >= 15:
        bitacora = 2
    else:
        bitacora = 1

    # Total: each criterion is 25 pts max, so multiply pts by 6.25
    total = round((cobertura + assertions + negativo + bitacora) * 6.25)
    return {'cobertura': cobertura, 'assertions': assertions,
            'negativo': negativo, 'bitacora': bitacora, 'total': total}


def grade_label(p):
    return {4: 'Excelente', 3: 'Bueno', 2: 'Normal', 1: 'Deficiente'}.get(p, '?')


def _format_alt_repo_block(sig: dict, scores: dict) -> str:
    """Surface alt-repo provenance in GRADING-A6.md (see grade_template.py for rationale)."""
    used = sig.get('alt_repo_used')
    candidates = sig.get('alt_repo_candidates') or []
    if used:
        return (
            f"\n> Calificación recuperada del repo alterno **{used}** "
            f"(el repo del curso no contenía tests de Playwright).\n"
        )
    if scores['total'] <= 25 and candidates:
        lines = ["\n## Posibles repos alternos (revisar manualmente)\n",
                 "El repo del curso no contiene tests. Estos repos públicos del usuario "
                 "matchean keywords del lab:\n"]
        for c in candidates:
            updated = (c.get('updated_at') or '')[:10]
            lines.append(f"- [`{c['full_name']}`]({c.get('url')}) — actualizado {updated}")
        lines.append("")
        return "\n".join(lines)
    return ""


def write_md(student_dir: Path, sig: dict, scores: dict):
    alt_block = _format_alt_repo_block(sig, scores)
    md = f"""# Calificación A6 — {student_dir.name}

**Score: {scores['total']}/100**
{alt_block}
## Signals

- Proyecto de tests encontrado: {sig['has_tests']} ({sig.get('project_root', '—')})
- playwright.config: {sig['playwright_config']}
- Archivos .spec/.test: {sig['spec_files']}
- Bloques test()/it(): {sig['test_blocks']}
- expect() calls: {sig['expect_calls']}
- expects por test (promedio): {sig['expect_per_test']:.2f}
- Caso negativo detectado: {sig['has_negative_case']} ({sig['negative_indicators']} archivos con indicadores)
- Solo navegación, sin assertions: {sig['has_visit_only']}
- Bitácora: {sig['bitacora_lines']} líneas, menciona agente: {sig['bitacora_mentions_agent']}

## Calificación por criterio

| Criterio | Nivel | Puntos | Aporte /100 |
|---|---|---|---|
| Cobertura flujos críticos | {grade_label(scores['cobertura'])} | {scores['cobertura']}/4 | {round(scores['cobertura']*6.25)} |
| Assertions verificables | {grade_label(scores['assertions'])} | {scores['assertions']}/4 | {round(scores['assertions']*6.25)} |
| Caso negativo | {grade_label(scores['negativo'])} | {scores['negativo']}/4 | {round(scores['negativo']*6.25)} |
| Bitácora | {grade_label(scores['bitacora'])} | {scores['bitacora']}/4 | {round(scores['bitacora']*6.25)} |
| **TOTAL** | | | **{scores['total']}/100** |
"""
    (student_dir / 'GRADING-A6.md').write_text(md)


CRITERIA = [
    ('cobertura', 'Cobertura flujos críticos', 25),
    ('assertions', 'Assertions verificables', 25),
    ('negativo', 'Caso negativo', 25),
    ('bitacora', 'Bitácora con uso de agente', 25),
]


def build_findings(sig: dict, scores: dict, recovered_from: str | None = None) -> dict:
    """Standard `findings` dict consumed by lib/grading_md.build_feedback_text."""
    rubric = [{
        'criterion': label,
        'level': scores[key],
        'max': 4,
        'weight_pct': weight,
        'note': {4: 'Excelente', 3: 'Bueno', 2: 'Normal', 1: 'Deficiente'}.get(scores[key], '?'),
    } for key, label, weight in CRITERIA]
    missing = [r['criterion'] for r in rubric if r['level'] <= 2]
    return {
        'score': scores['total'],
        'rubric': rubric,
        'signals': {k: v for k, v in sig.items() if not isinstance(v, (list, dict))},
        'missing': missing,
        'recovered_from': recovered_from,
    }


def main():
    if len(sys.argv) < 2:
        print('Usage: grade_playwright.py <student-or-group-folder>')
        sys.exit(1)
    target = Path(sys.argv[1])
    student_dirs = []
    if (target / '.git').exists():
        student_dirs = [target]
    else:
        student_dirs = [d for d in target.iterdir()
                        if d.is_dir() and (d / '.git').exists() and d.name != '_alt-repo']

    rows = []
    for sd in sorted(student_dirs):
        sig = analyze_repo(sd)
        scores = grade(sig)
        write_md(sd, sig, scores)
        rows.append((sd.name, scores))

    print(f'\n{"Student":<25} {"Cobr":<5} {"Asrt":<5} {"Neg":<5} {"Bit":<5} {"TOTAL"}')
    print('-' * 60)
    for name, s in rows:
        print(f'{name:<25} {s["cobertura"]:<5} {s["assertions"]:<5} {s["negativo"]:<5} {s["bitacora"]:<5} {s["total"]}/100')
    if rows:
        avg = sum(s['total'] for _, s in rows) / len(rows)
        below80 = sum(1 for _, s in rows if s['total'] < 80)
        print(f'\nN={len(rows)}  avg={avg:.1f}  below 80: {below80}/{len(rows)}')


if __name__ == '__main__':
    main()
