#!/usr/bin/env python3
"""Auto-grade Asignación 2: Investigación: Desarrollo Agéntico.

Submission: PR merged into student's portfolio repo. Content lives at
"I. investigaciones/agentic_development/" (or similar variants).

Rubric (7 criteria × ~14.28%):
1. Definición de desarrollo
2. Comparación entre herramientas
3. Capturas de pantalla
4. README.md renderizable
5. Uso de Copilot
6. Explicación de agentes
7. Commit con git/gh CLI
"""
import json
import re
import subprocess
import sys
from pathlib import Path


IMG_EXT = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}


def find_investigacion_root(repo: Path) -> Path | None:
    """Find the agentic-development research dir."""
    candidates = []
    for p in repo.rglob('*'):
        if not p.is_dir(): continue
        if '.git' in p.parts or 'node_modules' in p.parts: continue
        nm = p.name.lower()
        full = str(p.relative_to(repo)).lower()
        score = 0
        if 'agentic_development' in nm or 'agentic-development' in nm or 'agentic development' in nm: score += 50
        if 'investiga' in nm or 'investiga' in full: score += 20
        if 'research' in nm or 'desarrollo' in nm: score += 10
        if score > 0:
            score -= len(p.relative_to(repo).parts)
            candidates.append((score, p))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


def analyze_repo(repo: Path) -> dict:
    sig = {
        'has_research': False,
        'project_root': None,
        'readme_lines': 0,
        'readme_has_markdown_table': False,
        'readme_mentions_2026': False,
        'tool_mentions': {},
        'has_comparison_table': False,
        'screenshots_count': 0,
        'agent_screenshots': 0,
        'mentions_copilot': False,
        'mentions_opencode_or_cursor_or_claude': False,
        'has_agent_explanation': False,
        'gh_cli_commits': 0,
        'merge_commits': 0,
    }
    root = find_investigacion_root(repo)
    if root is None:
        return sig
    sig['has_research'] = True
    sig['project_root'] = str(root.relative_to(repo))

    # README
    readme = None
    for c in [root / 'README.md', root / 'readme.md']:
        if c.exists():
            readme = c
            break
    if readme is None:
        # try any .md file
        mds = list(root.glob('*.md'))
        if mds:
            readme = mds[0]
    if readme:
        text = readme.read_text(errors='ignore')
        text_lower = text.lower()
        sig['readme_lines'] = len(text.splitlines())
        sig['readme_has_markdown_table'] = bool(re.search(r'\|.*\|.*\|', text)) and bool(re.search(r'\|[\s-]+\|', text))
        sig['readme_mentions_2026'] = '2026' in text
        # Tool mentions
        tools = ['copilot', 'opencode', 'claude', 'cursor', 'cline', 'aider', 'pi.ai', 'gemini', 'chatgpt']
        for t in tools:
            count = len(re.findall(t, text_lower))
            if count:
                sig['tool_mentions'][t] = count
        sig['has_comparison_table'] = sig['readme_has_markdown_table'] and len(sig['tool_mentions']) >= 2
        sig['mentions_copilot'] = 'copilot' in sig['tool_mentions']
        sig['mentions_opencode_or_cursor_or_claude'] = any(t in sig['tool_mentions'] for t in ['opencode', 'cursor', 'claude'])
        # Agent explanation: look for "agente" definition or section
        sig['has_agent_explanation'] = bool(re.search(r'(qué\s+es\s+un\s+agente|agente.*ia|agentic\s+development|definici[oó]n.*agente)', text_lower))

    # Screenshots in root directory
    image_files = list(root.rglob('*'))
    for img in image_files:
        if not img.is_file() or img.suffix.lower() not in IMG_EXT: continue
        sig['screenshots_count'] += 1
        name = img.name.lower()
        if any(t in name for t in ['copilot', 'opencode', 'claude', 'cursor', 'cline', 'pi', 'agent']):
            sig['agent_screenshots'] += 1

    # Git history: gh CLI commits + merge commits
    try:
        r = subprocess.run(['git', '-C', str(repo), 'log', '--all', '--pretty=%h|%s|%an'],
                          capture_output=True, text=True, timeout=10)
        for line in r.stdout.splitlines():
            parts = line.split('|', 2)
            if len(parts) < 2: continue
            msg = parts[1].lower()
            if 'merge' in msg:
                sig['merge_commits'] += 1
            # Hard to detect "gh CLI" use from commit alone; check for typical gh-PR-merge style
            if 'merge pull request' in msg or '(pr #' in msg or ' #' in msg:
                sig['gh_cli_commits'] += 1
    except Exception:
        pass

    return sig


def grade(sig: dict) -> dict:
    if not sig['has_research']:
        return {'definicion': 1, 'comparacion': 1, 'capturas': 1, 'readme': 1,
                'copilot': 1, 'agentes': 1, 'gh_cli': 1, 'total': 25}

    # 1. Definición de desarrollo
    if sig['readme_lines'] >= 50 and sig['readme_mentions_2026']:
        definicion = 4
    elif sig['readme_lines'] >= 30:
        definicion = 3
    elif sig['readme_lines'] >= 15:
        definicion = 2
    else:
        definicion = 1

    # 2. Comparación entre herramientas
    if sig['has_comparison_table'] and len(sig['tool_mentions']) >= 3:
        comparacion = 4
    elif sig['has_comparison_table']:
        comparacion = 3
    elif len(sig['tool_mentions']) >= 2:
        comparacion = 2
    else:
        comparacion = 1

    # 3. Capturas de pantalla
    if sig['agent_screenshots'] >= 3:
        capturas = 4
    elif sig['agent_screenshots'] >= 2 or sig['screenshots_count'] >= 4:
        capturas = 3
    elif sig['screenshots_count'] >= 1:
        capturas = 2
    else:
        capturas = 1

    # 4. README.md renderizable
    if sig['readme_lines'] >= 50:
        readme = 4
    elif sig['readme_lines'] >= 20:
        readme = 3
    elif sig['readme_lines'] >= 5:
        readme = 2
    else:
        readme = 1

    # 5. Uso de Copilot
    if sig['mentions_copilot'] and sig['agent_screenshots'] >= 1:
        copilot = 4
    elif sig['mentions_copilot']:
        copilot = 3
    elif sig['readme_lines'] >= 30:
        copilot = 2
    else:
        copilot = 1

    # 6. Explicación de agentes
    if sig['has_agent_explanation'] and sig['readme_lines'] >= 50:
        agentes = 4
    elif sig['has_agent_explanation']:
        agentes = 3
    elif sig['mentions_opencode_or_cursor_or_claude']:
        agentes = 2
    else:
        agentes = 1

    # 7. Commit con git/gh CLI
    if sig['gh_cli_commits'] >= 2 or sig['merge_commits'] >= 1:
        gh_cli = 4
    elif sig['gh_cli_commits'] >= 1:
        gh_cli = 3
    elif sig['merge_commits'] >= 0:  # at least has git history
        gh_cli = 2
    else:
        gh_cli = 1

    raw = definicion + comparacion + capturas + readme + copilot + agentes + gh_cli
    # 28 raw max → 100. Each pt ≈ 3.57
    total = round(raw * 100 / 28)
    return {'definicion': definicion, 'comparacion': comparacion, 'capturas': capturas,
            'readme': readme, 'copilot': copilot, 'agentes': agentes, 'gh_cli': gh_cli,
            'total': total}


CRITERIA = [
    ('definicion', 'Definición de desarrollo agéntico', 14.28),
    ('comparacion', 'Comparación entre herramientas', 14.28),
    ('capturas', 'Capturas de pantalla / evidencia', 14.28),
    ('readme', 'README estructurado', 14.28),
    ('copilot', 'Uso de Copilot', 14.28),
    ('agentes', 'Explicación de agentes', 14.28),
    ('gh_cli', 'Commit con git/gh CLI', 14.28),
]


def build_findings(sig: dict, scores: dict, recovered_from: str | None = None) -> dict:
    """Convert grader outputs to the standard `findings` dict consumed by
    lib/grading_md.write_grading_md / build_feedback_text."""
    rubric = [{
        'criterion': label,
        'level': scores[key],
        'max': 4,
        'weight_pct': round(weight, 1),
        'note': {4: 'Excelente', 3: 'Bueno', 2: 'Normal', 1: 'Deficiente'}.get(scores[key], '?'),
    } for key, label, weight in CRITERIA]
    missing = [r['criterion'] for r in rubric if r['level'] <= 2]
    return {
        'score': scores['total'],
        'rubric': rubric,
        'signals': {k: v for k, v in sig.items() if not isinstance(v, (list, dict)) or len(str(v)) < 200},
        'missing': missing,
        'recovered_from': recovered_from,
    }


def main():
    if len(sys.argv) < 2:
        print('Usage: grade_investigacion.py <student-or-group-folder> [--slug ASIGNACION]')
        sys.exit(1)
    target = Path(sys.argv[1])
    slug = 'asignacion-02-investigacion'
    if '--slug' in sys.argv:
        slug = sys.argv[sys.argv.index('--slug') + 1]
    if (target / '.git').exists():
        dirs = [target]
    else:
        dirs = [d for d in target.iterdir() if d.is_dir() and (d / '.git').exists()]

    try:
        from grading_md import write_grading_md
    except ImportError:
        sys.path.insert(0, str(Path(__file__).parent))
        from grading_md import write_grading_md

    rows = []
    for sd in sorted(dirs):
        sig = analyze_repo(sd)
        scores = grade(sig)
        findings = build_findings(sig, scores)
        write_grading_md(sd, slug, findings)
        rows.append((sd.name, sig, scores))

    print(f'\n{"Student":<25} {"Def":<4} {"Cmp":<4} {"Cap":<4} {"RM":<4} {"Cpi":<4} {"Ag":<4} {"GHC":<4} {"TOT"}')
    print('-' * 75)
    for name, sig, s in rows:
        print(f'{name:<25} {s["definicion"]:<4} {s["comparacion"]:<4} {s["capturas"]:<4} {s["readme"]:<4} '
              f'{s["copilot"]:<4} {s["agentes"]:<4} {s["gh_cli"]:<4} {s["total"]}/100')
    if rows:
        avg = sum(r[2]['total'] for r in rows) / len(rows)
        below = sum(1 for r in rows if r[2]['total'] < 80)
        print(f'\nN={len(rows)}  avg={avg:.1f}  <80: {below}/{len(rows)}')


if __name__ == '__main__':
    main()
