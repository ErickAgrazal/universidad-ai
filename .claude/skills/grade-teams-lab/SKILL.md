---
name: grade-teams-lab
description: Bulk-grade a Microsoft Teams Assignments lab where students submit GitHub repos. Discovers student repos (gh search + invitations + collaborator list), clones them organized, applies the assignment rubric heuristically against the code, and bulk-fills grades into Teams' grade table via Playwright. Use when the user asks to grade a Teams course assignment with code submissions (e.g. "grade asignación 5", "califica los repos de PollClass", "help me grade my class").
---

# Grade a Teams Lab with Code Submissions

End-to-end workflow for grading a Microsoft Teams Assignment where students submit GitHub repository links. Built from the PollClass grading session (Asignación 5, May 2026).

## When to invoke

- User asks to grade a Teams assignment with code/repo deliverables
- User mentions "califica/grade Asignación X" or "PollClass" or similar lab name
- User opens Teams in browser and references the assignment

## Prerequisites

- `gh` CLI authenticated as the teacher account
- Playwright MCP server available (`mcp__playwright__*`)
- User is signed into Teams in the browser

## Autonomy contract

**The skill is autonomous end-to-end up to (but not including) clicking `Return`.** The user clicks Return — nothing else. Specifically:

| Step | Who does it |
|---|---|
| Identify the assignment | agent |
| Extract rubric + instructions | agent |
| Discover all repos (search + invitations + collaborator list) | agent |
| Clone every repo | agent |
| Auto-recover (branches, submodules, alternate names) for low scores | agent |
| Decide score per student (using rubric + recovered evidence) | agent |
| Enter every score into the Teams grade table textboxes | agent |
| Write per-student feedback for everyone scoring < 90 (banded templates) | agent |
| Surface BLOCKED/UNCLEAR cases with annotated reasons | agent |
| Click "Return" | **user** (always) |

The agent does NOT pause mid-workflow to ask the user about individual students. It collects all `BLOCKED`/`UNCLEAR` cases and presents them ONCE at the end, with proposed defaults. If the user doesn't override, defaults apply.

## Phase 0 — Gather policies (ask ONCE, then run autonomous)

Before starting, the agent asks the user the policy questions that will come up. Ask in ONE batch — don't drip-feed:

1. **"Sin URL = 0"** — confirmed? (Y/n, default Y)
2. **Off-topic submission** (student turned in wrong project) — score 0, 25 (rubric floor), or 65 (partial credit)? Default: 25 for consistency
3. **Late penalty** — apply or not? Default: no (rubric doesn't include it)
4. **Cross-class students** (in both class teams) — same score in both? Default: yes
5. **Branch with PollClass but Teams marks "Not turned in"** — credit or not? Default: credit (work was done, Teams flag is unreliable)

If the user says "use defaults" or doesn't customize, the agent locks those in and runs autonomously until the final Return.

## Workflow (6 phases + roster reconciliation)

### Phase 1 — Extract assignment context

If the user did NOT name a specific assignment, auto-pick: navigate to the class's Assignments tab, select `Past due`, and choose the **oldest unreturned** listitem. See `lib/teams_helpers.js → autoPickNextAssignment(page)`. Confirm the pick to the user in one sentence and proceed without further prompting.

Once the assignment is open, pull three pieces:

1. **Roster of "Turned in" students** from the grade table (`To return (N)` tab). Each row in Teams uses `LASTNAME, FIRSTNAME` format (with comma) — note ALL names exactly, including 36th-student "off-screen" cases that only show after scrolling.

2. **Rubric**. Click any student row → "Open pop up rubric grader". The popup dialog enumerates criteria with weights and point levels. Save to `submissions/<assignment-slug>/RUBRIC.md`. If the assignment has no rubric attached (Teams sometimes hides the button — see gotcha #10), fall back to parsing the instructions text into per-element compliance checks.

3. **Instructions**. Click "Take action in student view" (impersonate) → grab the `Instructions` heading content and `Requisitos`/`Entrega` lists. Save to `submissions/<assignment-slug>/INSTRUCTIONS.md`.

### Phase 2.0 — Capture submission URLs from Teams (do this FIRST for code labs)

For code-lab assignments (A5/A6/anything where the student attaches a GitHub URL), **read what the student actually submitted before guessing**. The convention-based discovery in Phase 2 (gh search by `2026-1GS24X-<lastname>-<firstname>`) is a fallback, not the primary signal. Students routinely submit a separate project repo (e.g. `1ZH13/PollClass-FSDSN`) while their conventionally-named course repo only contains earlier assignments.

```js
// In the grade view of the assignment:
const submissions = await captureSubmissionUrls(page);
// → [{ name: "BAZÁN, CÉSAR", urls: ["https://github.com/1ZH13/PollClass-FSDSN"] }, ...]
```

See `lib/teams_helpers.js → captureSubmissionUrls(page, opts)`. Write the output to `submissions/<slug>/SUBMISSION_URLS.json` so re-runs don't re-navigate. Treat the URL list as the **primary** repo source for Phase 3 clones; only fall back to Phase 2's discovery channels for students whose Teams entry has no URL.

This step was added after the PollClass session where BAZAN_CESAR was scored 25 because his course repo had no app — his actual PollClass code lived in `1ZH13/PollClass-FSDSN`, which he had pasted in Teams but the skill never read.

### Phase 2 — Discover student repos (4 sources, fallback when Phase 2.0 finds nothing)

**Single `gh search repos` is NOT enough.** Students use inconsistent naming. Combine all four:

```bash
# 1. ALWAYS run these 4 in order. The agent does this autonomously, not the user.

# 1a. Accept ALL pending invitations matching the term/class (do this FIRST so
#     step 1c sees everything)
gh api --paginate /user/repository_invitations \
  --jq '.[] | select(.repository.full_name | test("2026|1GS24|PollClass")) | .id' \
  | xargs -I{} gh api -X PATCH "/user/repository_invitations/{}"

# 1b. Search by the obvious class pattern
gh search repos "1GS241" --limit 100 --json fullName > class1.txt
gh search repos "1GS242" --limit 100 --json fullName > class2.txt

# 1c. List ALL repos accessible as collaborator (catches alternate naming
#     like "2026-241-X" without "GS", and any other variations)
gh api --paginate user/repos --jq '.[] | select(.full_name | test("2026|1GS24")) | .full_name'

# 1d. ONLY if a student isn't found by 1b+1c, fall back to Teams:
#     In Teams grade view, click student row → Open options for resource → Open online.
#     The new tab URL exposes the repo path. Use this for the residual <5% of cases.
```

In the PollClass session, the four sources combined found **63 repos**; `gh search` alone found only 57. The missing 6 used naming `2026-241-{lastname}` (without "GS") and only appeared via #3.

### Phase 2.5 — Check for follow-up labs (NEW after dry-run)

If the assignment is "Lab N" where N > 1, **first check if the previous lab's repos exist locally**. Many students extend the same repo with `laboratorios/lab-N/` for each lab. In that case:

```bash
# Before re-cloning, point the new grader at the EXISTING submissions dir
python3 grade_<assignment>.py /path/to/submissions/asignacion-0{N-1}-<slug>/grupo-1
```

Save the new GRADING-<assignment>.md files alongside the old GRADING.md files in each student dir. Only do fresh clones for students who don't already have a clone (e.g. new students enrolled mid-semester).

### Phase 3 — Clone in organized structure

```
submissions/<assignment-slug>/
├── RUBRIC.md
├── INSTRUCTIONS.md
├── FINAL_GRADES.md
├── grupo-1/
│   ├── ACOSTA_REY/        # repo cloned here
│   ├── BARRERA_ROY/
│   └── ...
└── grupo-2/
```

Folder naming: convert Teams `LASTNAME, FIRSTNAME` → `LASTNAME_FIRSTNAME` (strip accents, uppercase). The Python helper in this skill's `lib/` does this.

```bash
gh repo clone <owner>/<repo> grupo-X/LASTNAME_FIRSTNAME -- --depth=1
```

### Phase 4 — Heuristic grading (per repo)

Use the template grader at `lib/grade_template.py`. It extracts signals per repo:

- **Stack detection**: walk `package.json` merging all deps; flag React/Vite/Bun/Mongoose/Tailwind etc.
- **Project root detection** (HARDEST PART — see Gotchas)
- **Code analysis** via grep: setInterval (polling), WebSocket (forbidden), mongoose models, vote-uniqueness patterns
- **README quality**: line count + image references
- **Screenshots**: count of image files in project directory
- **Deployment evidence**: grep for "ngrok"
- **Agentic process**: grep for "opencode/copilot/claude/cursor" mentions in markdown

Then map signals to rubric criteria (1-4 points each) and compute total /100.

### Phase 4.5 — Auto-recovery for low scores (AGENT, not user)

**The agent must auto-retry before reporting any score <80 to the user.** Don't ask the human to do work the prompt can drive. For every student with score <80 from Phase 4, the agent runs this recovery loop:

```
for student in students_below_80:
    1. List all remote branches: gh api repos/<owner>/<repo>/branches
    2. For each non-main branch:
        a. git fetch origin <branch>
        b. git checkout <branch> (or temp worktree)
        c. Re-run grader on the checked-out tree
        d. If new score > old score: KEEP the new score, note the branch
        e. git checkout main (restore)

    3. If repo has .gitmodules:
        a. For each submodule URL, gh api repos/<url-derived> to check 200/404
        b. If 200: gh repo clone into the submodule path, re-grade
        c. If 404: mark as "submodule broken — student error"

    4. Check the student's OTHER repos via gh api users/<owner>/repos
        Look for repos with the target keyword (pollclass, playwright, etc.)
        If found, clone separately and re-grade.
        Implemented in `lib/alt_repo.py` and called automatically from
        `grade_template.py` / `grade_playwright_template.py` when
        `find_project_root()` returns None — the alt repo is cloned to
        `<student_dir>/_alt-repo/` and grading recurses into it. Provenance
        ("Recuperado del repo alterno X") is surfaced in GRADING.md.

    5. Check pending invitations: gh api /user/repository_invitations
        If new invitation visible: accept (PATCH) and clone

    6. For naming variations, search:
        gh search repos "<lastname>" --limit 5
        + gh api search/repositories?q=user:<owner>+<keyword>
```

Only after this loop is exhausted does the agent surface the student to the user with a clear annotation:

- `RECOVERED: 95 (from branch=laboratorios)` — fixed automatically
- `BLOCKED: submodule 404 / repo deleted` — needs user decision
- `UNCLEAR: stack present but content off-topic` — needs user judgment
- `NO_SUBMISSION: not in collaborator list, no repo found` — defaults to 0 per policy

The output of Phase 4 + 4.5 is a single table with status column per student, not raw scores. The user only intervenes on `BLOCKED` / `UNCLEAR` rows.

### Phase 4 — hybrid path for written reports (PDF/DOCX/MD)

When the assignment is a written report (no repo — students upload .docx/.pdf/.md directly to Teams), the heuristic-only path is wrong because the rubric judges things like "profundidad del análisis" and "originalidad de conclusiones" that no regex can score. The hybrid path:

**Phase 2-equivalent — Acquire submissions**:

For informe-style assignments, the acquisition priority is: **(1) cloned repos from prior assignments**, **(2) OneDrive sync**, **(3) SharePoint bulk-download**, **(4) per-student manual**.

| Source | Mechanism | Notes |
|---|---|---|
| **Cloned repos** | Most students reuse the same GitHub repo across assignments. A4 informes typically sit in `investigaciones/<topic>/`, `Investigaciones/<topic>/Informe/`, `<topic>_grupal/informe/`, `Trabajos_grupales/`, AND `Laboratorios/Laboratorio <topic>/` (technical-topic informes hide here — see gotcha) — alongside the A3 presentation folder | **Preferred — zero downloads.** Run `find <repos> -maxdepth 6 \( -iname "*.pdf" -o -iname "informe*" -o -iname "Informe*" -o -iname "*.docx" \)`. For technical topics, ALSO run `find <repos> -maxdepth 5 -path "*Laboratori*" -name "README.md" -exec grep -l -iE "Integrantes" {} \;` |
| **OneDrive sync folder** | If the teacher has OneDrive Files-on-Demand or has synced the class folder, submissions live in `~/Library/CloudStorage/OneDrive-*/<class>/<assignment>/Submissions/` | Zero clicks once synced |
| **Bulk download via SharePoint** | Each Teams assignment has a backing SharePoint document library. Open `class team → Files → Submissions → <assignment>` → Select all → Download as ZIP | One click; move ZIP contents to `submissions/<slug>/raw/` |
| **Per-student manual download** | In speed-grader, "Download as .docx" button per submission | Last resort. ~30+ clicks |

The agent runs the cloned-repo find FIRST. Only falls back to OneDrive/SharePoint when a student's repo lacks the informe artifact.

**Phase 3-equivalent — Extract + structural signals** (Python):

```bash
python3 ~/.claude/skills/grade-teams-lab/lib/grade_informe_template.py \
  submissions/asignacion-04-informe-grupal/raw/
```

This walks `raw/`, extracts text from each `.docx`/`.pdf`/`.md`, computes structural signals (sections present, word count, image count, APA inline citation count, references count, personal-conclusion markers), and writes one `.txt` (extracted text) + one `.json` (signals) per submission to `submissions/<slug>/extracted/`.

**Phase 4-LLM — Agent reads + judges**:

For each `.txt` in `extracted/`, the agent reads the extracted text and applies the 4 LLM-judged criteria (Profundidad, Conclusiones personales, Formato APA correcto, Ejemplos visuales relevance). Output is a `llm_scores` dict with level 1-4 per criterion + brief justification per criterion. The agent then calls:

```python
from grade_informe_template import build_findings
from grading_md import write_grading_md
findings = build_findings(signals, llm_scores, recovered_from=None)
write_grading_md(student_dir, "asignacion-04-informe-grupal", findings)
```

`build_findings` combines: structural levels (estructura, structural floor for APA & visuales) with LLM-judged levels, then computes the weighted total (each criterion 20%, each level worth 5pts) and surfaces `missing` for Phase 5.5 feedback.

**Group identification by PDF "Integrantes:" header — the highest-confidence group signal** (more reliable than video transcripts, READMEs, or filename authorship):

```bash
# Per-PDF: extract first 60 lines, look for the Integrantes block
for pdf in submissions/<slug>/raw/**/*.pdf; do
  echo "=== $(basename "$pdf") ==="
  pdftotext -layout "$pdf" - 2>/dev/null | head -60 | grep -iE "integrantes|autor|cédula" -A 6
done
```

A typical informe header looks like:
```
                        Integrantes:
                García, Eliel, 8-990-1192
                Rodríguez, Angélica, 2-751-41
```

Confidence ranking (highest → lowest):
1. **PDF Integrantes header** — explicit, formal, no name-mangling
2. **PDF authorship in filename** — `Diseno-Arquitectura-FullStack_Valdespino_TenSu_Bazán.pdf` directly names members
3. **README "Integrantes:" markdown** — same content, plain text, easy to grep
4. **Video transcript opening line** — Whisper mangles Spanish names ("Miguel García" was actually "Eliel García")
5. **Frame visual ID** — limited samples, can miss off-camera members
6. **File MD5 dedup** — confirms same group but doesn't name members

Always parse PDFs first for group rosters. The Integrantes signal also reveals **A3 groups that were unclear at A3 time** — recommend running A4 PDF parsing BEFORE finalizing A3 scores when grading both in the same session.

**Per-criterion structural scoring for informes** (deterministic, no LLM needed for the level-1-4 floor):

```bash
# Single PDF → 4 numbers that drive 4 of the 5 criteria
pdf="<path>"
pages=$(pdfinfo "$pdf" | grep "^Pages:" | awk '{print $2}')                       # → Estructura
apa=$(pdftotext "$pdf" - | grep -cE "\([0-9]{4}\)|, [0-9]{4}\.")                  # → APA correcto
concl=$(pdftotext "$pdf" - | grep -ciE "conclusi[oó]n|reflexi[oó]n")              # → Conclusiones personales
bib=$(pdftotext "$pdf" - | grep -ciE "bibliograf[ií]a|referencias")               # → Estructura corroboration
```

Empirical thresholds (from A4 class 1 calibration, N=14 group PDFs):

| Bucket | Pages | APA inline | Conclusiones | Bib? | Score band |
|---|---|---|---|---|---|
| Exemplary | ≥20 | ≥10 | ≥5 | yes | 100 |
| Excellent | 15-25 | 6-10 | 3-6 | yes | 92-95 |
| Good | 10-16 | 3-6 | 2-4 | yes | 88-92 |
| Adequate | 10-15 | 0-3 | 1-2 | yes | 85-88 |
| Weak | <10 | 0 | 0-1 | maybe | 80-85 |
| Individual when group expected | any | any | any | any | -5 to -10 from band |

These thresholds calibrated against the rubric: APA criterion needs ≥5 inline citations for level 4 ("Excelente"); Conclusiones personales needs N≥group_size conclusiones for level 4 (each integrant has their own). Pages alone is a weak proxy for Profundidad — pair with manual content check for top scores.

**Group submissions**: When N students share one file, group their cloned folders under `submissions/<slug>/raw/GROUP_<topic>/` with a `MEMBERS.txt` listing folder names. The grader writes one `findings` for the group, then the Phase 5 fill loop expands it to each member when matching against the Teams roster.

**Cross-assignment group inheritance**: when grading multiple assignments in the same period (e.g. A3 + A4 of the same semester), parse A4 PDFs FIRST to build the canonical group→members map. Then back-propagate to A3 — students who scored 0 or 75 on A3 due to "no evidence found" often turn out to be in a group identified only via the A4 PDF. Real example from A4 class 1 grading: FERREIRA was A3=75 → A4 PDF identified him in Pasarelas group → his A3 score should retroactively be 95 (group inheritance). Similar for ATHANASIADIS, GARCIA_JACK (CopilotKit), RUIZ_ERIC (Stitch).

### Phase 4 — hybrid path for video presentations (.mp4)

Video grading uses the same hybrid pattern as written reports, but the extraction toolchain is heavier and downloads go through SharePoint Stream (not Office viewer).

**Phase 2-equivalent — Acquire videos**:

The acquisition order is: **(1) check already-cloned repos first**, **(2) Teams SharePoint Stream**, **(3) YouTube/external URLs**.

**(1) Cloned repo audit** (cheapest, fastest). If the student's repo was cloned for a previous assignment (A2/A5/etc.), the A3 video may already be on disk in a different folder than the Teams submission link. Run:

```bash
A5=submissions/asignacion-05-pollclass/grupo-1
for s in "$A5"/*/; do
  found=$(find "$s" -maxdepth 5 -iname "*.mp4" 2>/dev/null | grep -v node_modules | head -1)
  [ -n "$found" ] && echo "$(basename $s): $found"
done
```

Many students submit to Teams a link to their A2 investigation folder, but the actual A3 video sits in `presentacion_grupal/video.mp4`, `tareas/Charla_*/`, `tema_asignado_*/`, `Plantilla_repo_github/Presentacion_grupal/`, etc. Audit ALL cloned repos before assuming a "wrong link" submission means no A3 work was done.

**Watch for Git LFS pointers** (small files <1KB that look like MP4 by name). Detect via `file <path>` — LFS pointers show as ASCII text starting with `version https://git-lfs.github.com/spec/v1`. Install + pull: `brew install git-lfs && git lfs install && cd <repo> && git lfs pull`.

**Group identification by file MD5**: if 2-3 students each cloned the same video to their repos, `md5 */presentation.mp4` will match — confirms they're in the same group. Group inheritance: transcribe once, assign the same score to all matched students.

**Group identification by README "Integrantes:" — the most reliable signal when no video is accessible** (and the dominant pattern for many groups):

```bash
# Find every README/MD that lists Integrantes — gives N→1 group→members mapping
find submissions/asignacion-05-pollclass -name "*.md" -not -path "*/.git/*" -not -path "*node_modules*" \
  -exec grep -l -iE "Integrantes" {} \;
# Then extract names per file: grep -A 8 -iE "integrantes" <file>
```

Typical pattern: a README inside `Investigaciones/<topic>/`, `presentacion_grupal/`, `Trabajos_grupales/`, etc. with markdown like:
```
**Integrantes del grupo:**
- Eliab Mena
- Luisa Guerra
```

This is **higher confidence than transcript opening lines** (Whisper mangles Spanish names) and **higher confidence than frame visual ID** (only 1-3 frames sampled). Always grep for `Integrantes` across every cloned repo first; the resulting member list drives group inheritance for any student in the same Teams class.

**Folder-name conventions to look for** when scanning repos for A3 artifacts:
- `presentacion_grupal/`, `Presentacion/`, `presentaciones/`
- `Trabajos_grupales/`, `Trabajo_Grupal/`, `<N>.Presentacion_Grupal/`
- `tareas/Charla_*/`, `Asignaciones/presentacion grupal/`
- `tema_asignado*/`, `Plantilla_<topic>/`
- `resumenpresentacion-grupo*/`
- Topic-keyworded folders: `Stitch/`, `TanStack/`, `medinet-project/`, `OpenRouter/`, `agentic_development/4.Presentacion_Grupal/`
- **`Laboratorios/Laboratorio <topic>/`** ⚠️ — A4 informes for technical topics (Backend Architecture, Frontend Template, Deployment, etc.) often live HERE, not in `investigaciones/`. Real example: IZARRA+GONZ_FAB+PORTELA's 607-line Backend Architecture informe was in `Laboratorios/Laboratorio Arquitectura Backend/` while their other folders only had A2 content. Skipping this folder would have under-graded 3 students by ~20 points.

**(2) Teams SharePoint Stream** (when no repo video exists):

Teams embeds video submissions in a SharePoint Stream player. The video plays from a `blob:` URL via Media Source Extensions — **cannot be downloaded directly from the embedded player**. But each video has a `uniqueId` (GUID) embedded in the streamembed.aspx URL, and SharePoint exposes a `download.aspx?UniqueId=<guid>` endpoint that returns the raw MP4 when called with authenticated cookies.

Procedure (one video at a time, looping over the class roster):

1. Open the student's speed-grader → locate the video resource → click it once (triggers the SharePoint embed iframe to load).
2. Find the SharePoint frame: `page.frames().find(f => f.url().includes('streamembed.aspx'))` and parse `uniqueId=([0-9a-f-]+)` out of its URL.
3. Extract SharePoint cookies from `page.context().cookies()`, filter to `*.sharepoint.com`, write to a Netscape-format cookies file at `/tmp/sp_cookies.txt`.
4. Construct the download URL: `https://<tenant>.sharepoint.com/sites/<site>/_layouts/15/download.aspx?UniqueId=<guid>` and fetch with `curl -L --cookie /tmp/sp_cookies.txt -o presentation.mp4 <url>`.
5. Validate: `file presentation.mp4` should report `ISO Media, MP4 Base Media`. Content-Length is the file size; 100-200 MB is typical for 10-min HD presentations.

The cookies last ~1 hour. If a download fails with HTTP 401/403, re-extract cookies from the active Playwright context.

**Phase 3-equivalent — Extract signals + transcribe** (Python, ~80s per 10-min video on CPU):

```bash
~/.claude/skills/grade-teams-lab/.venv/bin/python \
  ~/.claude/skills/grade-teams-lab/lib/grade_presentacion_template.py \
  submissions/asignacion-03-presentacion-grupal/raw/<GROUP>/
```

This runs `ffprobe` for duration, `ffmpeg` to extract 16-kHz mono WAV for Whisper, samples 6 evenly-spaced frames as JPEGs, then runs `faster-whisper` (`small` model, Spanish) to produce `transcript.json` + `transcript.txt` + `turns.json` + `STRUCTURAL.json`.

Outputs per submission folder:
- `audio.wav` (~17 MB for 10 min) — reusable for re-transcription with bigger model if needed
- `frames/frame_01.jpg` … `frame_06.jpg` — sampled slides for visual judgment
- `transcript.txt` / `transcript.json` — Whisper output (Spanish)
- `turns.json` — heuristic speaker-change segments (pause threshold 4s — short pauses are normal speech, longer gaps usually indicate handoffs)
- `STRUCTURAL.json` — duration, language confidence, turn count, time-criterion level pre-computed

**Phase 4-LLM — Agent reads + judges**:

The agent reads `transcript.txt` for content judgments and reads 2-4 sampled frames as images to verify:
- **Dominio** — does the transcript demonstrate accurate technical depth? Are concepts explained vs name-dropped?
- **Participación** — do frames show all integrants on camera? Does the transcript contain explicit handoffs ("ahora le paso la palabra a…", "X va a hablar sobre…")? `turns.json` count >1 is a positive signal but visual evidence in frames is stronger.
- **Ejemplos prácticos** — frames showing code, diagrams, demos, screen-share? Transcript referencing specific tools/commands/URLs?
- **Habilidad de presentación** — does transcript show natural Spanish with hesitations/paraphrasing ("entonces", "este"), or does it match slide text verbatim (= reading)?

Then call `build_findings(signals, llm_scores)` from `grade_presentacion_template.py` and `write_grading_md` from `grading_md.py`.

**Gestión del tiempo is automatic** — the agent doesn't judge it; `score_time(duration_sec)` already returns the level + a one-line note.

**Group submissions**: A3-style videos are inherently group work — one video per group, N students share the score. The roster mapping uses the speed-grader's "student detail view" — clicking any group member's row shows the same video. The skill captures `uniqueId` once per submission and maps it to every group-member folder for downstream Phase 5 fill.

**Score ceiling when no video is accessible (README/PDF only)**:

When a group has a clear README + content evidence but no accessible video (the most common pattern in non-CS-savvy classes), the rubric ceiling is **90, not 100**. Reasoning: 2 of 5 criteria require observing the presenter directly:
- **Habilidad de presentación** — cannot verify natural delivery vs reading slides without audio/video → cap at level 3 "Bueno"
- **Participación equitativa** — cannot verify each member spoke equally without the recording → cap at level 3 "Bueno" (the README names the integrants, but "named in README" ≠ "spoke equitably in the recording")

Other 3 criteria (Dominio, Ejemplos, Tiempo) can reach level 4 from written evidence alone (Tiempo defaults to "Bueno" with a 3 unless we have audio length to verify Excelente). Resulting cap: 3+3+4+4+3 = 17/20 = 85, or 3+3+4+4+4=90 if the time is explicitly documented in the README. Practical rule: **score 90 for confirmed-group + good README, score 85 if README is thin or individual-only**.

**Short-video preview detection** (< 5 min but README implies a longer presentation):

If a found video is <5 min AND the same folder/repo has a substantive README implying a full presentation was given (rubric topics covered in writing), the video is likely a preview/intro clip and the full recording lives elsewhere (Loom, Google Drive, OneDrive, YouTube). Search the README for external links (`grep -iE "youtu|drive\.google|loom\.com|onedrive|youtube" <README>`) before applying the time-deficient penalty. If a longer recording link is found, try `yt-dlp` against it. If nothing recovered, score the time criterion at level 1 (correct rubric outcome) BUT flag in feedback "video parece preview de X seg, README implica presentación completa — comparte el video completo para reabrir la nota".

In the original PollClass session this loop, if it had existed, would have caught:
- GONZALEZ_FABIANA's `laboratorios` branch (recovered → 95)
- The 6 students with `2026-241-X` naming (caught via step 4 + step 5)
- TENSU_ERIEL's hidden submission (caught via step 5)
- Adrian_Wong's broken submodule (correctly flagged as `BLOCKED` rather than silently scoring 25)

That would have eliminated ~9 of the 10 manual corrections we did, leaving only the genuine `UNCLEAR` cases (DELGADO submitting wrong project) for human decision. (BAZAN was originally on this list as "no-submission" but turned out to have his PollClass app in a separate repo `1ZH13/PollClass-FSDSN` — see Phase 2.0; the alt-repo recovery in `lib/alt_repo.py` now catches this case automatically.)

### Phase 4.75 — Roster reconciliation (pre-Phase 5 sanity check)

Before touching any textbox, diff the grade map against the actual Teams class roster. The grader produces a folder-name keyed map (`LASTNAME_FIRSTNAME`); Teams uses aria-label format (`LASTNAME, FIRSTNAME`). Mismatches happen for three reasons and each requires different handling:

| Mismatch | Cause | Action |
|---|---|---|
| `in_map_not_in_teams` | Cross-class artifact — same student-id appears in both class teams (graded in class 1, also listed in `grade_map[grupo-2]`), but Teams class 2 roster doesn't have them | **Silently skip** in Phase 5/5.5 — don't error out |
| `in_teams_not_in_map` | Student enrolled in Teams but never appeared in any of the 4 discovery sources (no repo invite, no shared collaborator list, no public repo matching the term) | **Surface to user**: "X students enrolled in Teams but had no discoverable repo — default 0?" |
| Folder name encoding drift | Teams uses accents/mixed case; grader strips to ASCII upper-case | Normalization handled in `lib/teams_helpers.js → reconcileRoster()` |

Use `lib/teams_helpers.js → reconcileRoster(page, gradeMap)`. It returns `{ teams_roster, matched, in_map_not_in_teams, in_teams_not_in_map }`. The agent acts on `matched[]` for Phase 5 and surfaces `in_teams_not_in_map[]` once before continuing.

### Phase 5 — Bulk-enter grades in Teams

The Teams grade table has an inline `Grade, out of 100 for <NAME>` textbox per student row. The path:

1. Open class team → Assignments → click the specific assignment
2. The grade table renders ~22 rows at a time (virtualized scroll)
3. Fill ALL textboxes in ONE call via `mcp__playwright__browser_run_code_unsafe`

**Preferred pattern — bulk fill in a single tool call** (avoids the snapshot+fill ping-pong and the per-snapshot 50-70KB token bloat that overflows context):

```js
async (page) => {
  const frame = page.locator('iframe').first().contentFrame();
  // 1. Scroll to top so virtualization renders the first batch
  await frame.locator('body').evaluate(() => {
    const ss = Array.from(document.querySelectorAll('*')).filter(e => {
      const s = getComputedStyle(e);
      return (s.overflowY === 'auto' || s.overflowY === 'scroll') && e.scrollHeight > e.clientHeight;
    });
    for (const s of ss) s.scrollTop = 0;
  });
  // 2. Enumerate every grade textbox aria-label (Teams uses exact "LASTNAME, FIRSTNAME" — note accents/case)
  // 3. Fill with scrollIntoViewIfNeeded so virtualized rows render before fill
  const fills = [ ["ACOSTA, REY", 90], ["APARICIO, ANA", 0], /* ... */ ];
  for (const [name, val] of fills) {
    const tb = frame.locator(`input[aria-label="Grade, out of 100 for ${name}"]`);
    await tb.scrollIntoViewIfNeeded({ timeout: 3000 });
    await tb.fill(String(val));
  }
  // 4. Verify: scroll back to top, then walk down collecting every textbox value
  // (returns empty[] if any student is unfilled)
}
```

**Why this beats `browser_type` snap+fill**: `browser_type` requires a fresh ref each call (refs invalidate per fill), and each snapshot is 50-70KB. For 33-36 students that's >2MB of snapshot output per class. `browser_run_code_unsafe` runs Playwright in-process — frame.contentFrame() bypasses the cross-origin block, and all fills + verification happen in ONE tool call.

**Cross-origin caveat**: `mcp__playwright__browser_evaluate` (page-level JS) CANNOT reach the Teams iframe document (cross-origin SecurityError). `browser_run_code_unsafe` CAN, because it uses Playwright's frame locator, not raw `iframe.contentDocument`.

**Discover the exact aria-labels first** (Teams uses `LASTNAME, FIRSTNAME` for most, but quirks exist: `CARLOS JAEN` no comma; `Martinez, Angel` title-case; `BAZÁN, CÉSAR` with accents; `Cisneros, Axel` mixed-case). Enumerate before mapping:

```js
const labels = await frame.locator('input[aria-label*="Grade, out of 100"]').evaluateAll(els =>
  els.map(e => e.getAttribute('aria-label').replace('Grade, out of 100 for ', '')));
```

The textbox accepts integers 0-100. Just `.fill(score)` overwrites.

### Phase 5.5 — Bulk-enter feedback for students scoring < 90

Students scoring < 90 get individualized text feedback alongside their grade. Students scoring 90+ are skipped — "Bueno" is already a strong rubric tier and per-student notes there are noise.

**Banded feedback templates** (the agent generates these, then writes them to Teams in the same loop):

| Score band | Reason | Template (Spanish, ~1 sentence + concrete next step) |
|---|---|---|
| 0 | NO_SUBMISSION | "No recibí entrega para esta asignación. Si tienes el material, envíamelo (DM/correo) y reabro la nota." |
| 25 | OFF_TOPIC | "La entrega no corresponde al tema solicitado (`<topic>`). Por favor lee el enunciado y entrega el documento correcto para reconsiderar la nota." |
| 26–60 | INCOMPLETE | "Entrega parcial. Faltan varios criterios: `<top 2-3 missing rubric items>`. Revisa la rúbrica para próximos labs." |
| 61–79 | PARTIAL | "Buen contenido pero le faltan elementos del rubric: `<missing items>`." |
| 80–86 | SOLID | "Investigación sólida. Para nota máxima: `<top 1-2 improvements>`." |
| 87–89 | NEAR_EXCELLENT | "Muy cerca de excelente. Para llegar a 100 te faltó: `<specific gap>`." |
| any band, recovered via Phase 4.5 | RECOVERED | Prepend: "Investigación recuperada de `<branch / alt folder>` (recordar entregar en `main` o como PR según la consigna). " Then the band template. |

**Mechanism — same `browser_run_code_unsafe` pattern**:

```js
async (page) => {
  const frame = page.locator('iframe').first().contentFrame();
  const feedbacks = [ ["LASTNAME, FIRSTNAME", "feedback text"], /* ... */ ];

  // Scroll to top first
  await frame.locator('body').evaluate(() => { /* scroll all scrollables to 0 */ });

  for (const [name, text] of feedbacks) {
    // Progressive scroll until row is visible (toggle button enters the virtualized window)
    let found = false;
    for (let s = 0; s < 25 && !found; s++) {
      found = await frame.locator(`button[aria-label^="Toggle feedback for ${name},"]`).first().isVisible().catch(() => false);
      if (!found) await frame.locator('body').evaluate(() => { /* scroll each scrollable +200 */ });
      await page.waitForTimeout(250);
    }
    if (!found) continue; // student not in this class (cross-class artifact)

    const toggle = frame.locator(`button[aria-label^="Toggle feedback for ${name},"]`).first();
    await toggle.scrollIntoViewIfNeeded({ timeout: 5000 });
    await toggle.click();              // expands the inline editor
    await page.waitForTimeout(450);

    // Find THIS student's editor by walking DOM up from the toggle
    const editorHandle = await toggle.evaluateHandle(btn => {
      let n = btn;
      for (let d = 0; d < 15; d++) {
        n = n.parentElement;
        if (!n) return null;
        const ed = n.querySelector('div[aria-label="Feedback"]');
        if (ed && ed.offsetParent !== null) return ed;
      }
      return null;
    });
    const editor = editorHandle.asElement();
    if (!editor) continue;
    await editor.click();
    await page.keyboard.press('Meta+A');
    await page.keyboard.press('Delete');
    await page.keyboard.type(text, { delay: 3 });
  }
}
```

**Critical gotchas**:

- **Editor identification by DOM walk, NOT by `Feedback` selector alone**: opening one toggle reveals an editor; opening a second leaves the first one open too. Multiple `div[aria-label="Feedback"]` elements exist simultaneously. Walk up from the *toggle button* to a common ancestor, then find the editor inside that ancestor — that pairs each editor with its student row.
- **Virtualization moves rows as editors expand**: each opened editor adds vertical space, pushing later rows off-screen. The progressive-scroll loop must handle this (don't assume one initial `scrollTop = 0` is enough).
- **Editor is a contenteditable div, not a textarea**: use `page.keyboard.type(text)` after focusing. `Meta+A` then `Delete` clears any prior content.
- **`browser_evaluate` cannot reach this editor either** (cross-origin iframe). Use `browser_run_code_unsafe` only.
- **Cross-class roster artifacts**: a student listed in `grade_map[grupo-2]` but absent from the Teams class 2 grade table is a discovery-phase artifact (they were graded in class 1 by the same person-id). The scroll loop's `if (!found) continue` skip handles this — don't error out.
- **Recovery-flagged students get a prefix**: BEITIA_BETHEL (laboratorios branch), MARTINEZ_ANGEL (copilot/investigacion-agente-desarrollo), RUIZ_ERIC (investigacion), DELBIONDO/JIMENEZ (group-informe repurposed) — all started <80, got auto-recovered, and the feedback should *acknowledge* the recovery + suggest entregar en `main`/PR next time.

### Phase 6 — Self-verify, write AUDIT.json, then hand off to user for Return

The agent verifies its OWN work — no human review required at this stage. Verification runs in the SAME `browser_run_code_unsafe` call as Phase 5:

1. After all fills, scroll the table back to top
2. Loop ~12 times: read every `input[aria-label*="Grade, out of 100"]` into a Map, scroll down 400px
3. Map = source of truth (deduped across virtualization passes). Filter `value === ''` → empties list
4. If `empty.length > 0` or any `error` from the fill loop: retry only those students; otherwise verification passes
5. Total students matched: assert `Map.size === expected_roster_size` (33 or 36 for these classes)

**Audit log** — Phase 6 also captures an offline record. Use `lib/teams_helpers.js → captureAuditSnapshot(page)` to read every `(name, score, has_feedback)` triple from Teams, then write:

```
submissions/<assignment-slug>/AUDIT.json
{
  "timestamp": "2026-05-17T22:30:00-05:00",
  "assignment": "2. Investigación: Desarrollo Agéntico",
  "classes": {
    "1GS241": [{ "name": "ACOSTA, REY", "score": "90", "has_feedback": false }, ...],
    "1GS242": [...]
  },
  "summary": { "total": 69, "filled": 69, "feedbacks_given": 20 }
}
```

This survives Teams sync issues, lets the user spot-check post-hoc, and feeds future re-grade runs without re-cloning.
5. Build the handoff report:

```
✅ <N> grades entered and verified in Teams (group 1)
✅ <N> grades entered and verified in Teams (group 2)

🟢 Auto-graded: <N> students (avg X)
🟡 Auto-recovered after low-score retry: <N> (e.g. branch swap, submodule clone)
🔴 BLOCKED — needs your input: <N>
   - <student> — <reason> — proposed: <score> (override?)
🟦 NO_SUBMISSION — defaulted to 0 per policy: <N>

NEXT STEP (you): Open class 1 grade table → Select all → Return.
Then class 2 → Select all → Return.
```

The agent stops here. Never clicks Return — that is the user's explicit action.

## Gotchas (learned the hard way)

| Gotcha | Symptom | Fix |
|---|---|---|
| Students name repos `2026-241-X` instead of `2026-1GS241-X` | `gh search` returns 57 not 63 | Use `user/repos` collaborator list (source #3) |
| PollClass lives in non-main branch (e.g. `laboratorios`) | Score=25 but code exists | After clone, `git ls-remote --heads`; check each non-main branch for the target project |
| Submodule with broken URL (`adr-wong/PollClass` → 404) | `.gitmodules` present but folder empty | Verify submodule URL responds; if 404, treat as no-submission |
| Student submitted off-topic project (e.g. their e-commerce final instead of the lab) | Auto-grader gives ~65 because stack matches but content doesn't | Add `is_pollclass` check: no views + no models + no validation → cap criteria at 1 (Deficiente) |
| Project detection picks wrong dir (e.g. `tema_asignado/template`) | High stack score but Func=1, no validation | EXCLUDE list of common wrong-dir names (templates, presentations, parciales, otros labs). Boost paths where `package.json` has `name` field matching the target. Penalize being inside `client/server/test/e2e` subdirs unless parent has package.json |
| `client/package.json` not committed | Stack score low even though .jsx files use React | Walk `.jsx` files for `import * from 'react'` as fallback signal. Or scan `tailwind.config.js` at project root |
| Cross-origin iframe blocks page-level JS injection | `mcp__playwright__browser_evaluate` throws SecurityError on `iframe.contentDocument` | Use `mcp__playwright__browser_run_code_unsafe` instead — Playwright's `frame.contentFrame()` traverses the boundary even when raw DOM access cannot |
| The grade table is virtualized (only ~22 rows render) | Some textbox `aria-label` selectors miss off-screen rows | Inside the `run_code_unsafe` loop, call `tb.scrollIntoViewIfNeeded()` BEFORE each `tb.fill()`. For verification, scroll-down-and-collect into a Map (deduplicates re-rendered rows) — virtualization recycles DOM nodes but aria-label is stable |
| Snapshot tool output exceeds 60KB token limit | `browser_snapshot` errors with "Output too large" after several fills | Switch from `browser_type` (needs fresh ref per fill → forces snapshot) to `browser_run_code_unsafe` (one tool call, no intermediate snapshots) |
| Teams aria-label formatting is inconsistent | `Grade, out of 100 for ACOSTA, REY` vs `Grade, out of 100 for CARLOS JAEN` (no comma) vs `Martinez, Angel` (title-case) vs `BAZÁN, CÉSAR` (accents) | ALWAYS enumerate via `evaluateAll` first to capture exact aria-label strings, then build the fills array from those — never assume a uniform `LASTNAME, FIRSTNAME` format |
| Written report submissions can't be programmatically downloaded via the Teams web UI | The speed-grader embeds Office Web Apps in a nested iframe; the `Turned in` link navigates but doesn't expose a raw-file URL Playwright can fetch | Check the teacher's OneDrive sync folder first (`~/Library/CloudStorage/OneDrive-*/<class>/<assignment>/Submissions/`). If absent, do a one-time SharePoint bulk-download: `team → Files → Submissions → <assignment>` → Select all → Download ZIP. Move ZIP contents to `submissions/<slug>/raw/`. The skill grader operates on local files after that. |
| Video submissions stream via blob: URL (MediaSource Extensions) — cannot be downloaded from the player | The Teams speed-grader embeds `streamembed.aspx` which loads the video as fragmented MP4 segments via MSE | Extract `uniqueId=([0-9a-f-]+)` from the streamembed URL via `page.frames().find(f => f.url().includes('streamembed.aspx')).url()`. Then call `https://<tenant>.sharepoint.com/sites/<site>/_layouts/15/download.aspx?UniqueId=<guid>` with cookies extracted from `page.context().cookies()` (write Netscape-format to `/tmp/sp_cookies.txt`, fetch via `curl -L --cookie /tmp/sp_cookies.txt`). Returns the raw MP4 (typically 75-110 MB for 8-10 min HD). |
| A3-style assignments have heterogeneous artifacts: direct MP4 (minority), SharePoint personal-share link (counts as same-group inheritance), GitHub repo links (often wrong artifact pointing to A2 investigación), PPT-only, "Link" text buttons | Each student row contains 1-N attachments visible only after navigating to their speed-grader URL `/classes/<cid>/assignment-review/<aid>/submissions/<sid>` | Iterate the roster, navigate each submission URL via `iframe.contentWindow.location.href = url`, enumerate `button[aria-label*="View and grade work of"]` to capture all attachment titles. Then classify per row: direct MP4 (full LLM eval), other artifact (heuristic scoring with feedback noting what couldn't be verified). |
| Group videos: one student uploads, partners marked "Viewed" (no upload) but DID present | Teams treats each student independently; group members who didn't click Turn-in look like no-submissions but appear in the video | Identify groups by (a) transcript opening lines ("mi grupo conformado por X y Y", "mi compañero Z y mi persona"), (b) frame inspection (multiple presenters visible), (c) topic/title text match. Credit the same score to all confirmed group members — never auto-zero a "Viewed" student until checking video evidence. |
| Teams submission link points to "wrong" artifact, but the cloned repo has the right one in a different folder | A student submits a GitHub URL to their A2 investigation folder, but their A3 video/PPT lives in `presentacion_grupal/`, `tema_asignado/`, `tareas/Charla_*/`, or similar elsewhere in the same repo | **Always audit the cloned repo** (from any prior assignment that cloned the same student's repo — A2/A5/etc.) before scoring on Teams artifact alone. Run `find <repo> -maxdepth 5 \( -iname "*.mp4" -o -iname "*.pptx" -o -iname "*presentacion*" -o -iname "*charla*" -o -iname "*tema_asign*" \)`. Found videos can be processed directly (no Teams download needed). |
| Large videos stored via Git LFS or stub-replaced | A `.mp4` file in the repo is suspiciously small (50-150 bytes) — either a Git LFS pointer (`version https://git-lfs.github.com/spec/v1`) or a manually-truncated stub | Detect via `file` (LFS pointer is detected as ASCII text) or by checking file size <1KB. For LFS pointers: `brew install git-lfs && git lfs install && cd <repo> && git lfs pull`. For stubs (real `ftyp` header but truncated body): cannot recover — note as "video unviewable, scored on artifact presence alone". |
| Videos may also be hosted on YouTube/Vimeo (not in Teams or repo) | Student left a `VIDEO_EXPLICACION.md` with a URL, often citing GitHub-size limits as the reason | Try `yt-dlp '<url>'` with the active browser cookies (`--cookies-from-browser chrome` etc.). Private videos return HTTP 403 — cannot grade Dominio/Habilidad/Participación, but documented effort + slide PDF + explanation deserves credit (~80, not 0). |
| Informes/READMEs sometimes embed external video links (OneDrive personal share, Loom, Drive) | Look inside `Informe_escrito_grupal/README.md` or the PDF for lines like "Video ubicado en: https://1drv.ms/..." — students reference the actual full-quality video there rather than uploading to Teams | Grep informe content for `https?://` URLs and inspect each. For OneDrive `1drv.ms` shares: open the URL in Playwright (`page.goto`), find the `Download` button (`button[aria-label="Download"]`), click it — Playwright emits a `download` event you can `saveAs(path)`. This works without authentication for public shares. Real example: GitHub Template group's actual 17:23 video lived in a 1drv.ms link inside their informe README, not in the Teams meeting recording I'd been processing. Updating their grade from 65 → 85 after finding it. |
| When re-grading an already-Returned assignment, edits to grade + feedback are kept locally but require a fresh Return to push them to students | Teams shows the updated grade in the Returned tab grid but doesn't notify students until you re-Return | After bulk-editing grades/feedback in the Returned view, the assignment shows in "To return" again with the changed-rows count. User clicks Return on those rows. The agent's edits are persistent regardless. |
| Group identification by file MD5 / shared filename | Two or three students each upload the same group video to their own repos — same file size + same duration + same MD5 confirms they're the same group | After downloading all candidate videos, run `md5 */presentation.mp4` and `ffprobe -show_entries format=duration` per file. Identical → de-dup the transcription work (do it once per unique MD5) and assign the resulting score to every student sharing that MD5. Also infers groups via PDF authorship (filename like `Diseno_Author1_Author2_Author3.pdf`). |
| README "Integrantes:" is the most reliable group signal | For non-video presentations (PDF/README only), it's the only reliable group source. For videos, it's more reliable than transcript opening (Whisper mangles Spanish names) or frame visual ID (limited samples). | `find <repos> -name "*.md" -exec grep -l -iE "Integrantes" {} \;` then `grep -A 8 -iE "integrantes" <file>`. Build the group→members map BEFORE attempting any video processing. Group inheritance flows from this map. |
| For presentation-style assignments (A3): cloned repo is more authoritative than the Teams submission link | Students often submit a GitHub URL to their A2 investigation folder, not the A3 presentation. The repo's `presentacion_grupal/`, `Trabajos_grupales/`, `tema_asignado_*/` folders are where A3 evidence actually lives. | For A3-style assignments, reverse the normal Phase 2 priority: audit cloned repos FIRST for any A3 artifact folder, ONLY use the Teams submission link as fallback. Opposite of the A5/A6 lab pattern where Teams is authoritative. |
| Score ceiling for "README/PDF only" group submissions: 90, never 100 | The rubric has criteria (Habilidad de presentación, Participación equitativa) that require observing the actual recording. Without video, those cap at level 3 ("Bueno"). | Hard rule: if no accessible video → max score 90 (3+3+4+4+4 weighted). If only an individual README (no group named) → max 85. Feedback should say "Para nota máxima: subir el video al repo o a Teams" explicitly so the student understands the gap. |
| Short videos (<5 min) when README implies a full presentation | Student uploaded an intro/preview clip; the actual 8-12 min recording lives on Loom/Drive/YouTube/OneDrive | Before scoring time-deficient at level 1: `grep -iE "youtu\|drive\.google\|loom\.com\|onedrive\|youtube" <README>` for an external video link. If found, try `yt-dlp <url>`. If empty/private, score time level 1 BUT flag explicitly in feedback that the clip looks like a preview, not a final reason for the grade. |
| PDF "Integrantes:" header is the HIGHEST-confidence group signal | Higher than README (writers paraphrase), higher than video transcript opening (Whisper mangles names), higher than filename (truncated/encoded). When grading a written-report assignment that's part of a multi-assignment series, parse PDFs FIRST to build the group→members map | `pdftotext -layout <pdf> \| head -60 \| grep -iE "integrantes" -A 6`. Confidence ranking documented in Phase 4 informes section. |
| A3 video group affiliations are often unclear; A4 PDFs resolve them | Whisper-mangled names, off-camera members, and topic-matching ambiguity make A3 group identification imperfect. The corresponding A4 informe PDF has a formal Integrantes block that's authoritative | When grading A3 and A4 of the same semester, ALWAYS process A4 PDFs first. Use the resulting group map to back-fill A3 scores: students with A3=0 or A3=75 who appear in an A4 PDF Integrantes block should inherit their group's A3 score retroactively. |
| Per-criterion structural scoring for PDFs is calibratable | The 5-criterion informe rubric maps cleanly to 4 measurable signals: pdfinfo pages → Estructura, regex `\([0-9]{4}\)` → APA, `grep conclusi[oó]n -c` → Conclusiones, `grep bibliograf` → Bib presence | See Phase 4 informes "Per-criterion structural scoring" table — calibrated against N=14 group PDFs from A4 class 1 grading. 4 numbers per PDF differentiate the 80/85/90/92/95/100 bands. |
| Technical-topic informes live in `Laboratorios/Laboratorio <topic>/`, not `investigaciones/` | When the assignment topic is technical (Backend Architecture, Frontend Template, Deployment, Database, DevOps), students treat it as part of their "lab work" and put the writeup in a Laboratorios subfolder. The first repo-audit pass (`find -iname "informe*"` in investigaciones/Trabajos) misses these | Add `Laboratorios/Laboratorio*/README.md` to the audit pattern. Pattern: `find <repo> -maxdepth 5 -name "README.md" -path "*Laboratori*" -exec grep -l -iE "Integrantes" {} \;` — surfaces these hidden group informes. Real impact: 3 students rescued from "75 (no evidence)" to "95 (full group informe)" in A4 class 2. |
| LLM-judged criteria need traceable rationale | If the agent silently picks level 3 for "Profundidad" the teacher can't audit | Every LLM judgment must write a one-sentence justification per criterion into `GRADING-<slug>.md` (under each rubric row). `build_findings` already includes the `note` field; agent fills it during Phase 4-LLM |
| Teams "Not turned in" can be wrong | Students with real repos shown as not-turned-in | Don't auto-zero "Not turned in" students; clone and grade them anyway, then ask the user whether to credit |
| Follow-up labs reuse the same repo | When grading "Lab N" after already grading "Lab N-1", many students put Lab N inside their existing repo at `laboratorios/lab-N/` — no new clone needed | Before re-cloning, run the grader against already-cloned submissions/ dirs from the previous assignment. Only clone fresh for students whose repo isn't already present |
| Score 25 is ambiguous | Could mean "submitted off-topic" OR "auto-grader failed to detect work" | Tag low-score students as either `AUTO_DEFICIENTE` (rubric floor, all 1s for legit reasons) or `DETECTION_UNCERTAIN` (worth manual re-check). Surface both groups separately to the user — never bulk-enter `DETECTION_UNCERTAIN` as 25 |
| Tests detected only by filename pattern | Files like `tests/poll-vote.ts` without `.spec.` extension aren't counted | Detect test files by import (`import { test, expect } from '@playwright/test'`) not just by name suffix |
| Bitácora often inline in README | Grader expects a separate BITACORA.md but most students put the agent log inside the lab's README.md | Score Bitácora using README content + agent keywords, not just file existence |
| Assignment has no attached Rubric in Teams | "Open pop up rubric grader" button missing — only Feedback + Points + Return shown | Read criteria from the assignment Instructions text instead. Build a per-element compliance grader (one boolean per requirement). Report each element separately so the teacher sees WHICH requirement each non-100 student missed |
| Group work repurposed as individual deliverable | A2 (individual research) submitted as group informe with folder named `Presentacion-Informe sobre CopilotKit` or `informe-copilotCLI.md` instead of `investigacion/agentic_development/`. Grader returns 25 (no folder found) even though content fully satisfies rubric | Phase 4.5 auto-recovery: after branch check, also search ALL `.md` files in repo for ones >50 lines containing target keywords (`copilot`, `agentic`, `agente`, `cursor`, `claude`). If found, score that markdown as the A2 deliverable. Note in handoff report: "RECOVERED FROM: alternate folder X" so teacher can verify whether group→individual repurposing is acceptable per their policy |

## Scoring policy decisions (asked once in Phase 0, then locked)

These are surfaced ONCE at the start of the workflow (Phase 0) — not during grading. After the user answers, agent runs autonomously.

1. **"Sin URL = 0"** — if no accessible repo after all 4 discovery sources + auto-recovery, score is 0. (Default Y.)
2. **Off-topic submission**: student turned in but wrong project. Default: 25 (rubric floor, consistent with no-PollClass cases).
3. **Late submission penalty**: default no (rubric doesn't include it).
4. **Students in both class teams**: grade once, enter the same score in both. (Default yes.)
5. **Branch with the work but Teams marks "Not turned in"**: credit it (default yes — the work was done; Teams flag can be wrong if student forgot to click Turn-in).

## Helper files in this skill

- `lib/grade_template.py` — Heuristic grader for **app-style labs** (PollClass and similar). Adapt the `find_project_root()` keywords (POSITIVE/EXCLUDE), per-criterion scoring rules, and rubric mapping. Calls `write_grading_md` for per-student records.
- `lib/grade_playwright_template.py` — Variant for **test-suite labs**: counts test() blocks, expect() calls, detects negative cases, looks at bitácora. Exposes `build_findings(sig, scores)` for feedback generation.
- `lib/grade_intro_template.py` — Variant for **administrative assignments without rubric** (e.g. "create a portfolio repo"): per-element compliance check. Exposes `build_findings`.
- `lib/grade_investigacion_template.py` — Variant for **research/markdown labs with PR submission**: scans README for markdown tables, tool mentions, screenshots, git history for PR/merge commits. Exposes `build_findings`.
- `lib/grade_informe_template.py` — Variant for **written reports** (PDF/DOCX/MD). Hybrid: Python extracts text + structural signals; the agent (LLM) reads the extracted text and judges the cualitative criteria. See "Phase 4 — hybrid path for written reports" below.
- `lib/grade_presentacion_template.py` — Variant for **video presentations** (.mp4). Hybrid: `ffprobe` for duration (Gestión del tiempo is fully structural — 8-12 min ⇒ Excelente, etc.), `ffmpeg` for audio extraction + frame sampling, `faster-whisper` (small model, Spanish) for transcription. Agent reads the transcript + sampled frames as images to judge Dominio/Participación/Ejemplos/Habilidad. See "Phase 4 — hybrid path for video presentations" below. Requires: `ffmpeg`, `ffprobe`, `pip install faster-whisper` in the skill's venv (`.venv/`).
- `lib/grading_md.py` — **Shared** writer for per-student `GRADING-<slug>.md` and `build_feedback_text(findings)` (drives Phase 5.5). Every grader template emits its `findings` through this so the feedback Teams sees is specific (top 3 missing rubric items) instead of banded.
- `lib/teams_helpers.js` — Playwright snippets pasted into `browser_run_code_unsafe`: `autoPickNextAssignment` (Phase 1), `reconcileRoster` (Phase 4.75), `captureAuditSnapshot` (Phase 6 AUDIT.json).
- `lib/teams_to_folder.py` — Convert Teams `LASTNAME, FIRSTNAME` to folder slug `LASTNAME_FIRSTNAME`.

## Closing checklist (agent verifies before handoff)

The agent runs this checklist itself, not the user:

- [ ] All graded students have a non-blank score in Teams grade table (verified via fresh snapshot)
- [ ] Students with 0 have a documented `BLOCKED` or `NO_SUBMISSION` annotation
- [ ] `FINAL_GRADES.md` written with score breakdown grouped by status (Auto / Recovered / Blocked / No_submission)
- [ ] Per-student `GRADING.md` exists explaining the score
- [ ] Average score is sanity-checked. If avg <80 OR more than 20% of students <80, the agent re-runs auto-recovery (Phase 4.5) — never delivers a low average without first investigating its own detection
- [ ] BLOCKED/UNCLEAR list ≤ 5% of total students (if higher, agent does another auto-recovery pass before reporting)
- [ ] Every student with score < 90 has feedback written in Teams (Phase 5.5). The agent re-enumerates `Toggle feedback for ... Feedback given` aria-labels after Phase 5.5 — any "Feedback not given" remaining for a <90 student is a gap to retry
- [ ] Roster reconciliation (Phase 4.75) ran: `in_teams_not_in_map` was either resolved or surfaced to the user before Phase 5
- [ ] Per-student `GRADING-<slug>.md` exists for every cloned repo — drives the specific Phase 5.5 feedback
- [ ] `AUDIT.json` written to `submissions/<slug>/AUDIT.json` with timestamp + per-class breakdown
- [ ] Agent reports to user once, with the proposed BLOCKED resolutions
- [ ] Agent does NOT click Return — that is the user's explicit final action
