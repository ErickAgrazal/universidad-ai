# Helper scripts for grade-teams-lab

## `grade_template.py`

Heuristic grader for Teams lab submissions. Built originally for PollClass (Asignación 5, 2026-1GS24*) — adapt for each new assignment by editing:

- `POSITIVE` keywords in `find_project_root()`: paths/folder names that signal the right project (e.g. `pollclass`, `lab5`, `laboratorio-5`)
- `EXCLUDE` keywords: paths to ignore (other labs, templates, parciales, investigations, presentations)
- The `analyze_repo()` patterns dict: extend `vote_unique` / `set_interval` / etc. patterns for the new assignment's required features
- The `grade()` function: remap signals to your rubric's criteria and thresholds

Run on a single student or a whole group:

```bash
python3 grade_template.py submissions/<assignment>/grupo-1/ACOSTA_REY
python3 grade_template.py submissions/<assignment>/grupo-1   # whole group
```

Output: writes `GRADING.md` inside each student folder + summary table to stdout.

## `teams_to_folder.py`

Normalize a Teams student name to a folder slug. Use when building the clone manifest.

```bash
echo "RODRÍGUEZ, ANGÉLICA" | python3 teams_to_folder.py
# → RODRIGUEZ_ANGELICA
```

## Adapting for a new assignment

Order of operations:
1. Copy `grade_template.py` into the new project as `grade_<assignment>.py`
2. Read the rubric in Teams → write down each criterion's weights and level descriptions
3. Update `POSITIVE`/`EXCLUDE` for the assignment's directory naming conventions
4. Update `analyze_repo()` patterns for the required features (e.g. for a chat app: WebSocket+message persistence; for a CRUD app: REST endpoints)
5. Rewrite the `grade()` function rules — map signals to your specific criteria
6. Run on 3-5 known-good repos first to calibrate
7. Run on all, manually verify all scores <80 before bulk-entering to Teams
