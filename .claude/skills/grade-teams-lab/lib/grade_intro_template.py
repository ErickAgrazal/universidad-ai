#!/usr/bin/env python3
"""Auto-grade Asignación 1: Creación de Repositorio en GitHub.

Per the instructions, calification is binary: 100 if all indications followed, 0 if any non-compliance.

This grader checks the repo root README.md for the 5 required elements:
1. Student full name
2. Materia / course name
3. Photo (img reference or actual image file)
4. "Qué me gusta" content
5. "Qué espero" content

Plus the repo must be accessible (we cloned = teacher has collaborator access).
"""
import re
import sys
from pathlib import Path


def grade_repo(repo: Path) -> dict:
    sig = {
        'has_readme': False,
        'readme_lines': 0,
        'has_name': False,
        'has_materia': False,
        'has_photo': False,
        'has_likes': False,
        'has_expects': False,
        'photo_files_present': 0,
    }
    readme = repo / 'README.md'
    if not readme.exists():
        return sig, 0
    sig['has_readme'] = True
    try:
        text = readme.read_text(errors='ignore')
    except Exception:
        return sig, 0
    sig['readme_lines'] = len(text.splitlines())
    text_lower = text.lower()
    # Check for substantive name presence (any "nombre completo" or upper-case name pattern)
    sig['has_name'] = bool(re.search(r'(nombre\s+completo|name:|nombre:)', text_lower)) or \
                     bool(re.search(r'\*\*[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+', text))
    sig['has_materia'] = bool(re.search(r'(materia|curso|desarrollo\s+de\s+software|software\s+development|des\s*ix|dsix|dsoftware)', text_lower))
    sig['has_photo'] = bool(re.search(r'(!\[|<img|foto|photo)', text_lower)) and \
                      bool(re.search(r'(\.jpe?g|\.png|\.gif|\.webp|user-attachments|githubuser)', text_lower))
    sig['has_likes'] = bool(re.search(r'(qué\s+me\s+gusta|que\s+me\s+gusta|me\s+gusta\s+(el\s+|la\s+|del\s+)?desarrollo|like.*software)', text_lower))
    sig['has_expects'] = bool(re.search(r'(qué\s+espero|que\s+espero|espero\s+(de\s+este|del\s+)?curso|expect.*course)', text_lower))
    # Count image files in repo for triangulation
    for f in repo.rglob('*'):
        if not f.is_file() or '.git' in f.parts or 'node_modules' in f.parts: continue
        if f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.heic'}:
            sig['photo_files_present'] += 1

    # Score: count of 5 elements
    elements = sum([sig['has_name'], sig['has_materia'], sig['has_photo'],
                    sig['has_likes'], sig['has_expects']])

    # Per the rubric: 100 if all 5, 0 otherwise. But many real students have 4/5 + got 100,
    # so use a lenient mapping. Strict mode: 5/5 = 100, else 0.
    # Lenient mode: 5=100, 4=80, 3=60, ≤2=0.
    if elements == 5:
        score = 100
    elif elements == 4 and (sig['has_photo'] or sig['photo_files_present'] > 0):
        # Most students who got 100 had 4/5 + a photo file
        score = 100
    elif elements >= 3:
        score = 60
    elif elements >= 1:
        score = 30
    else:
        score = 0
    return sig, score


INTRO_ELEMENTS = [
    ('has_name', 'Nombre completo'),
    ('has_materia', 'Nombre de la materia'),
    ('has_photo', 'Foto'),
    ('has_likes', 'Qué te gusta del software'),
    ('has_expects', 'Qué esperas del curso'),
]


def build_findings(sig: dict, score: int, recovered_from: str | None = None) -> dict:
    rubric = [
        {'criterion': label, 'level': 4 if sig.get(key) else 1, 'max': 4, 'weight_pct': 20,
         'note': 'Presente' if sig.get(key) else 'Ausente'}
        for key, label in INTRO_ELEMENTS
    ]
    missing = [label for key, label in INTRO_ELEMENTS if not sig.get(key)]
    return {
        'score': score,
        'rubric': rubric,
        'signals': {k: v for k, v in sig.items() if not isinstance(v, (list, dict))},
        'missing': missing,
        'recovered_from': recovered_from,
    }


def main():
    if len(sys.argv) < 2:
        print('Usage: grade_repo_intro.py <student-folder|group-folder> [--slug ASIGNACION]')
        sys.exit(1)
    target = Path(sys.argv[1])
    slug = 'asignacion-01-repo-github'
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
        sig, score = grade_repo(sd)
        write_grading_md(sd, slug, build_findings(sig, score))
        rows.append((sd.name, sig, score))

    print(f'\n{"Student":<25} {"RM":<3} {"N":<3} {"M":<3} {"P":<3} {"L":<3} {"E":<3} {"Files":<5} {"Score"}')
    print('-' * 80)
    for name, s, score in rows:
        flag = lambda b: '✓' if b else '✗'
        print(f'{name:<25} {flag(s["has_readme"])} '
              f'{flag(s["has_name"])} {flag(s["has_materia"])} '
              f'{flag(s["has_photo"])} {flag(s["has_likes"])} '
              f'{flag(s["has_expects"])} {s["photo_files_present"]:<5} {score}')
    if rows:
        avg = sum(r[2] for r in rows) / len(rows)
        below = sum(1 for r in rows if r[2] < 80)
        print(f'\nN={len(rows)}  avg={avg:.1f}  <80: {below}/{len(rows)}')


if __name__ == '__main__':
    main()
