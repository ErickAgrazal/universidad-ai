#!/usr/bin/env python3
"""Convert Teams student name "LASTNAME, FIRSTNAME" → folder slug "LASTNAME_FIRSTNAME".

Handles:
- Accents: BAZÁN, CÉSAR → BAZAN_CESAR
- No comma: CARLOS JAEN → CARLOS_JAEN (kept as-is)
- Mixed case: Martinez, Angel → MARTINEZ_ANGEL
- Trailing dot: CACERES, JORGE. → CACERES_JORGE

Usage:
    from teams_to_folder import teams_to_folder
    teams_to_folder("RODRÍGUEZ, ANGÉLICA")  # → "RODRIGUEZ_ANGELICA"
"""
import unicodedata


def teams_to_folder(name: str) -> str:
    nfkd = unicodedata.normalize('NFKD', name)
    s = ''.join(c for c in nfkd if not unicodedata.combining(c))
    s = s.upper().strip().rstrip('.')
    if ',' in s:
        last, first = [p.strip() for p in s.split(',', 1)]
        return f'{last}_{first}'.replace(' ', '_')
    return s.replace(' ', '_')


if __name__ == '__main__':
    import sys
    for line in sys.stdin:
        print(teams_to_folder(line.strip()))
