"""Alt-repo discovery: when a student's course repo doesn't contain the lab,
look at their OTHER public GitHub repos for a name match (e.g. PollClass-FSDSN).

This implements SKILL.md Phase 4.5 step 4 as actual code rather than a narrative
instruction the agent might skip.
"""
import json
import re
import subprocess
from pathlib import Path


def get_repo_owner(repo: Path) -> str | None:
    """Extract GitHub owner from the cloned repo's origin remote."""
    config = repo / '.git' / 'config'
    if not config.exists():
        return None
    try:
        text = config.read_text(errors='ignore')
    except Exception:
        return None
    m = re.search(
        r'(?:git@github\.com:|https?://github\.com/)([^/\s]+)/[^/\s]+?(?:\.git)?\s*$',
        text, re.MULTILINE)
    return m.group(1) if m else None


def list_user_repos(owner: str, timeout: int = 30) -> list[dict]:
    """List public repos for `owner` via gh CLI. Returns minimal repo objects."""
    try:
        out = subprocess.run(
            ['gh', 'api', f'users/{owner}/repos', '--paginate',
             '--jq', '.[] | {name, full_name, html_url, updated_at}'],
            capture_output=True, text=True, timeout=timeout)
    except Exception:
        return []
    if out.returncode != 0:
        return []
    repos = []
    for line in out.stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            repos.append(json.loads(line))
        except Exception:
            continue
    return repos


def find_candidates(owner: str, keywords: tuple[str, ...]) -> list[dict]:
    """Return repos whose name contains any keyword (case-insensitive).

    Sorted by preference: keyword hit > recency.
    """
    repos = list_user_repos(owner)
    out = []
    for r in repos:
        name_lower = r.get('name', '').lower()
        hits = [k for k in keywords if k in name_lower]
        if hits:
            r['_keyword_hits'] = hits
            out.append(r)
    # Prefer names with the more-specific keywords first (e.g. 'pollclass' > 'poll')
    keyword_rank = {k: i for i, k in enumerate(keywords)}
    out.sort(key=lambda r: (
        min(keyword_rank.get(k, 99) for k in r['_keyword_hits']),
        -_to_epoch(r.get('updated_at', '')),
    ))
    return out


def _to_epoch(iso: str) -> int:
    """ISO8601 → epoch seconds. Returns 0 on parse failure."""
    if not iso:
        return 0
    try:
        from datetime import datetime
        return int(datetime.fromisoformat(iso.replace('Z', '+00:00')).timestamp())
    except Exception:
        return 0


def clone_alt_repo(student_dir: Path, full_name: str, timeout: int = 60) -> Path | None:
    """Shallow-clone `full_name` into `student_dir/_alt-repo/`. Idempotent."""
    target = student_dir / '_alt-repo'
    if (target / '.git').exists():
        return target
    if target.exists():
        return None  # exists but not a repo — refuse to overwrite
    try:
        result = subprocess.run(
            ['gh', 'repo', 'clone', full_name, str(target), '--', '--depth=1'],
            capture_output=True, text=True, timeout=timeout)
    except Exception:
        return None
    return target if result.returncode == 0 and (target / '.git').exists() else None


def discover_and_clone(student_dir: Path, keywords: tuple[str, ...]) -> dict:
    """One-shot: find candidates for `student_dir`'s GitHub owner and clone the best.

    Returns: {
      'owner': str|None,
      'candidates': list[dict],     # all matching repos (for surfacing in GRADING.md)
      'used': str|None,             # full_name of cloned repo
      'path': Path|None,            # clone path if successful
    }
    """
    result = {'owner': None, 'candidates': [], 'used': None, 'path': None}
    owner = get_repo_owner(student_dir)
    if not owner:
        return result
    result['owner'] = owner
    candidates = find_candidates(owner, keywords)
    result['candidates'] = candidates
    if not candidates:
        return result
    best = candidates[0]
    path = clone_alt_repo(student_dir, best['full_name'])
    if path:
        result['used'] = best['full_name']
        result['path'] = path
    return result
