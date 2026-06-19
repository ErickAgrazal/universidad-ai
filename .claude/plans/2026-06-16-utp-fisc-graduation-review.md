# UTP/FISC Graduation-Work Review — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port hermes' UTP/FISC academic-review skills into the `universidad` workspace as 4 Claude Code skills (anteproyecto, práctica profesional, informe final, PDF renderer), then restructure the workspace into `regular/` + `graduacion/`.

**Architecture:** Skills live in `universidad/.claude/skills/` (source of truth) and are symlinked into `~/.claude/skills/` so Claude Code auto-invokes them. The hermes OCR pipeline is replaced by Claude Code's native PDF Read + `pdftotext`. The PDF renderer keeps its reportlab/pyyaml engine inside a self-contained `.venv`. The folder restructure (and Claude-state migration) runs LAST to avoid stranding the live session.

**Tech Stack:** Markdown skills (Claude Code SKILL format), Python 3 + reportlab + PyYAML (PDF render), bash (symlinks, restructure), macOS `pdftotext`/`textutil`.

**Note on git:** `universidad` is NOT a git repo (and per `universidad/CLAUDE.md`, no `git add -A` here). So this plan has NO commit steps — verification is by inspecting files, resolving symlinks, and rendering a sample PDF.

**Source paths (hermes, read-only):**
- Anteproyecto: `~/.hermes/profiles/hermesgeneralist/skills/academic/utp-fisc-anteproyecto-review/`
- Práctica: `~/.hermes/profiles/g2stash/skills/productivity/utp-fisc-practica-profesional-anteproyecto-review/`
- Final doc: `~/.hermes/profiles/hermesgeneralist/skills/academic/utp-fisc-final-doc-review/`
- PDF: `~/.hermes/profiles/hermesgeneralist/skills/academic/utp-fisc-review-pdf/`

---

## Task 1: Scaffold the `.claude` skills tree

**Files:**
- Create dirs: `universidad/.claude/skills/`, `universidad/graduacion/2026/`

- [ ] **Step 1: Create the directory skeleton**

```bash
mkdir -p /Users/ea/Projects/universidad/.claude/skills
mkdir -p /Users/ea/Projects/universidad/graduacion/2026
```

- [ ] **Step 2: Verify**

```bash
ls -la /Users/ea/Projects/universidad/.claude /Users/ea/Projects/universidad/graduacion/2026
```
Expected: both directories exist; `.claude/` already contains `specs/` and `plans/`.

---

## Task 2: Port `utp-fisc-anteproyecto-review`

**Files:**
- Create: `universidad/.claude/skills/utp-fisc-anteproyecto-review/SKILL.md`
- Create: `universidad/.claude/skills/utp-fisc-anteproyecto-review/references/calificacion-anteproyectos-ejemplos.md`

- [ ] **Step 1: Copy the skill verbatim**

```bash
cp -R ~/.hermes/profiles/hermesgeneralist/skills/academic/utp-fisc-anteproyecto-review \
      /Users/ea/Projects/universidad/.claude/skills/utp-fisc-anteproyecto-review
```

- [ ] **Step 2: Drop the OCR dependency from frontmatter**

Edit `SKILL.md`. Replace:
```
    related_skills: [ocr-and-documents]
```
with:
```
    related_skills: [utp-fisc-review-pdf]
```

- [ ] **Step 3: Replace the OCR extraction mechanism (keep the visual-inspection guidance)**

Edit `SKILL.md`. In step 2 of "Procedimiento de revisión", replace exactly:
```
2. Si archivo es PDF/DOCX/imagen, cargar `ocr-and-documents` y extraer texto. Para PDF local, preferir PyMuPDF/pypdf; para escaneado usar OCR si necesario. Para DOCX, además de extraer texto con `python-docx`, revisar señales de formato académico: márgenes por sección, tamaño carta, numeración/pies de página, estilos aplicados como encabezado vs párrafo normal, tablas, imágenes embebidas, placeholders visibles como “Aquí inserta…”, y datos sensibles de portada como ortografía del asesor/estudiante.
```
with:
```
2. Si el archivo es PDF/DOCX/imagen, **leerlo directamente con la herramienta Read de Claude Code** (ingiere texto y renderiza páginas escaneadas para visión; usar el parámetro `pages` para páginas críticas). Como respaldo de texto masivo, usar `pdftotext "archivo.pdf" -` en la terminal; para DOCX usar `textutil -convert txt "archivo.docx" -stdout` (macOS). En DOCX revisar señales de formato académico: márgenes por sección, tamaño carta, numeración/pies de página, estilos aplicados como encabezado vs párrafo normal, tablas, imágenes embebidas, placeholders visibles como “Aquí inserta…”, y datos sensibles de portada como ortografía del asesor/estudiante.
```
Leave the remaining sub-bullets of step 2 (the visual-inspection guidance about PDFs exported from Word, Gantt shading, scanned annexes, contact sheets, DOCX tables, BIBLIOGRAFÍA, etc.) UNCHANGED — they describe exactly the visual checks Read enables.

- [ ] **Step 4: Verify no dangling OCR references remain**

```bash
grep -rn "ocr-and-documents\|PyMuPDF\|pypdf" /Users/ea/Projects/universidad/.claude/skills/utp-fisc-anteproyecto-review/SKILL.md
```
Expected: no output (the references file may still mention PyMuPDF in pitfalls — that's fine, see Step 5).

- [ ] **Step 5: Verify the references file copied**

```bash
ls -la /Users/ea/Projects/universidad/.claude/skills/utp-fisc-anteproyecto-review/references/calificacion-anteproyectos-ejemplos.md
```
Expected: file exists. (Its "Pitfalls" section mentions PyMuPDF as a caution — leave it; it's calibration context, not a mechanism instruction.)

---

## Task 3: Port `utp-fisc-practica-profesional-review`

**Files:**
- Create: `universidad/.claude/skills/utp-fisc-practica-profesional-review/SKILL.md`

- [ ] **Step 1: Copy and rename the skill**

```bash
cp -R /Users/ea/.hermes/profiles/g2stash/skills/productivity/utp-fisc-practica-profesional-anteproyecto-review \
      /Users/ea/Projects/universidad/.claude/skills/utp-fisc-practica-profesional-review
```

- [ ] **Step 2: Update the skill `name` to match its folder**

Edit `SKILL.md` frontmatter. Replace:
```
name: utp-fisc-practica-profesional-anteproyecto-review
```
with:
```
name: utp-fisc-practica-profesional-review
```

- [ ] **Step 3: Anchor the extraction step to Claude Code's Read tool**

Edit `SKILL.md`. In "Practical review workflow", replace exactly:
```
1. Extract text from the PDF.
   - Use lightweight PDF extraction first.
   - If scanned pages are image-only, render target pages and inspect with vision.
```
with:
```
1. Read the PDF directly with Claude Code's **Read tool** (it ingests text and renders scanned pages for vision; use the `pages` parameter for critical pages).
   - As a bulk-text fallback, run `pdftotext "file.pdf" -` in the terminal.
   - Do not trust extracted text alone: visually confirm signatures, stamps, the company acceptance letter, and Gantt shading that plain text omits.
```

- [ ] **Step 4: Add a pointer to the PDF deliverable skill**

Edit `SKILL.md`. At the end of "Recommended response structure", after the line `4. WhatsApp-ready copy`, append:
```

For Erick's deliverable: after the audit, generate the institutional PDF with `utp-fisc-review-pdf` (use `document_type: "Anteproyecto"` and `modality: "Práctica Profesional"`), then provide the WhatsApp-ready copy as a separate copy-paste block.
```

- [ ] **Step 5: Verify**

```bash
grep -n "name: utp-fisc-practica-profesional-review" /Users/ea/Projects/universidad/.claude/skills/utp-fisc-practica-profesional-review/SKILL.md
grep -n "Read tool\|utp-fisc-review-pdf" /Users/ea/Projects/universidad/.claude/skills/utp-fisc-practica-profesional-review/SKILL.md
```
Expected: name line matches; both extraction + PDF references present.

---

## Task 4: Port `utp-fisc-final-doc-review`

**Files:**
- Create: `universidad/.claude/skills/utp-fisc-final-doc-review/SKILL.md`

- [ ] **Step 1: Copy the skill verbatim**

```bash
cp -R /Users/ea/.hermes/profiles/hermesgeneralist/skills/academic/utp-fisc-final-doc-review \
      /Users/ea/Projects/universidad/.claude/skills/utp-fisc-final-doc-review
```

- [ ] **Step 2: Drop the OCR dependency from frontmatter**

Edit `SKILL.md`. Replace:
```
    related_skills: [ocr-and-documents]
```
with:
```
    related_skills: [utp-fisc-review-pdf]
```

- [ ] **Step 3: Replace the OCR extraction mechanism (step 2)**

Edit `SKILL.md`. In "Procedimiento de revisión", replace exactly:
```
2. Si archivo es PDF/DOCX/imagen, cargar `ocr-and-documents` y extraer texto. Para PDF local, usar PyMuPDF/pypdf; para escaneado, OCR.
```
with:
```
2. Si el archivo es PDF/DOCX/imagen, **leerlo con la herramienta Read de Claude Code** (texto + visión de páginas escaneadas; parámetro `pages` para páginas clave). Respaldo de texto masivo: `pdftotext "archivo.pdf" -`; para DOCX `textutil -convert txt "archivo.docx" -stdout` (macOS).
```

- [ ] **Step 4: Adapt the DOCX/structure-inspection mechanic in step 3**

Edit `SKILL.md`. In step 3, replace the clause:
```
Para PDFs largos, inspeccionar páginas por palabras clave (`RESUMEN`, `ÍNDICE`, `CAPÍTULO`, `CONCLUSIONES`, `REFERENCIAS`, `ANEXOS`) y muestras de fuentes/tamaños/papel con PyMuPDF. Para DOCX, además de texto con `python-docx`, inspeccionar señales estructurales:
```
with:
```
Para PDFs largos, inspeccionar páginas por palabras clave (`RESUMEN`, `ÍNDICE`, `CAPÍTULO`, `CONCLUSIONES`, `REFERENCIAS`, `ANEXOS`) leyendo esos rangos con la herramienta Read. Para DOCX, además del texto convertido con `textutil`, inspeccionar señales estructurales:
```
Leave the rest of step 3 (the list of structural signals — `docProps/app.xml`, márgenes, estilos, etc.) UNCHANGED.

- [ ] **Step 5: Verify no dangling OCR/PyMuPDF references remain**

```bash
grep -n "ocr-and-documents\|PyMuPDF\|pypdf\|python-docx" /Users/ea/Projects/universidad/.claude/skills/utp-fisc-final-doc-review/SKILL.md
```
Expected: no output.

---

## Task 5: Port `utp-fisc-review-pdf` + self-contained venv

**Files:**
- Create: `universidad/.claude/skills/utp-fisc-review-pdf/` (SKILL.md, scripts/, templates/, assets/)
- Create: `universidad/.claude/skills/utp-fisc-review-pdf/requirements.txt`
- Create: `universidad/.claude/skills/utp-fisc-review-pdf/.venv/`

- [ ] **Step 1: Copy the skill (script + templates + logo assets) verbatim**

```bash
cp -R /Users/ea/.hermes/profiles/hermesgeneralist/skills/academic/utp-fisc-review-pdf \
      /Users/ea/Projects/universidad/.claude/skills/utp-fisc-review-pdf
ls /Users/ea/Projects/universidad/.claude/skills/utp-fisc-review-pdf/assets
```
Expected assets: `utp-logo.png`, `fisc-logo.png`. (The script resolves `assets/` relative to its own dir via `Path(__file__).resolve().parents[1]`, so copying the tree intact keeps logo resolution working.)

- [ ] **Step 2: Drop the OCR dependency from frontmatter**

Edit `SKILL.md`. Replace:
```
    related_skills: [utp-fisc-anteproyecto-review, utp-fisc-final-doc-review, ocr-and-documents]
```
with:
```
    related_skills: [utp-fisc-anteproyecto-review, utp-fisc-final-doc-review]
```

- [ ] **Step 3: Write `requirements.txt`**

Create `universidad/.claude/skills/utp-fisc-review-pdf/requirements.txt`:
```
reportlab
PyYAML
```

- [ ] **Step 4: Create the venv and install deps**

```bash
cd /Users/ea/Projects/universidad/.claude/skills/utp-fisc-review-pdf
python3 -m venv .venv
.venv/bin/python3 -m pip install --upgrade pip
.venv/bin/python3 -m pip install -r requirements.txt
```

- [ ] **Step 5: Verify deps import**

```bash
/Users/ea/Projects/universidad/.claude/skills/utp-fisc-review-pdf/.venv/bin/python3 -c "import reportlab, yaml; print('deps OK')"
```
Expected: `deps OK`

- [ ] **Step 6: Update SKILL.md invocation to use the venv**

Edit `SKILL.md`. Replace the render command:
```
python3 "$SKILL_ROOT/scripts/render_utp_fisc_review_pdf.py" revision.md revision.pdf
```
with:
```
"$SKILL_ROOT/.venv/bin/python3" "$SKILL_ROOT/scripts/render_utp_fisc_review_pdf.py" revision.md revision.pdf
```

---

## Task 6: Verify the PDF pipeline end-to-end (the one real "test")

**Files:**
- Temp: `/tmp/utp-pdf-smoketest.pdf`

- [ ] **Step 1: Render a real hermes sample review through the new venv**

```bash
cd /Users/ea/Projects/universidad/.claude/skills/utp-fisc-review-pdf
.venv/bin/python3 scripts/render_utp_fisc_review_pdf.py \
  ~/.hermes/profiles/hermesgeneralist/output/utp_reviews/revision_anteproyecto_luisa_guerra_v1.md \
  /tmp/utp-pdf-smoketest.pdf
```
Expected: command exits 0, no traceback.

- [ ] **Step 2: Confirm the PDF exists, is non-empty, and is multi-page with logos**

```bash
ls -la /tmp/utp-pdf-smoketest.pdf
pdftotext /tmp/utp-pdf-smoketest.pdf - | head -40
```
Expected: file size > 0; extracted text shows "Resumen de revisión", "Veredicto"/"Correcciones a realizar", and the student/verdict content. (If `pdftotext` shows pages and headings, the pipeline works; logos are drawn on canvas and won't appear in text — spot-check visually with the Read tool if desired.)

- [ ] **Step 3: (Optional) Visually confirm logos render**

Read `/tmp/utp-pdf-smoketest.pdf` with the Read tool (page 1) and confirm UTP logo top-left, FISC logo top-right, compact status table near the top.

- [ ] **Step 4: Clean up**

```bash
rm -f /tmp/utp-pdf-smoketest.pdf
```

---

## Task 7: Symlink the 4 skills into `~/.claude/skills/` and confirm discovery

**Files:**
- Create symlinks: `~/.claude/skills/utp-fisc-{anteproyecto-review,practica-profesional-review,final-doc-review,review-pdf}`

- [ ] **Step 1: Create the 4 symlinks (source of truth stays under universidad)**

```bash
SRC=/Users/ea/Projects/universidad/.claude/skills
DST=/Users/ea/.claude/skills
for s in utp-fisc-anteproyecto-review utp-fisc-practica-profesional-review utp-fisc-final-doc-review utp-fisc-review-pdf; do
  ln -snf "$SRC/$s" "$DST/$s"
done
```

- [ ] **Step 2: Verify all 4 symlinks resolve to the universidad source**

```bash
ls -la /Users/ea/.claude/skills | grep utp-fisc
for s in utp-fisc-anteproyecto-review utp-fisc-practica-profesional-review utp-fisc-final-doc-review utp-fisc-review-pdf; do
  test -f "/Users/ea/.claude/skills/$s/SKILL.md" && echo "$s SKILL.md reachable" || echo "$s BROKEN"
done
```
Expected: 4 symlinks shown pointing into `universidad/.claude/skills/`; all 4 print "reachable".

- [ ] **Step 3: Confirm each SKILL.md frontmatter `name` matches its directory**

```bash
for s in utp-fisc-anteproyecto-review utp-fisc-practica-profesional-review utp-fisc-final-doc-review utp-fisc-review-pdf; do
  echo -n "$s -> "; grep -m1 '^name:' "/Users/ea/.claude/skills/$s/SKILL.md"
done
```
Expected: each `name:` equals its folder name. (Skills are discovered on next session start; note that to the user.)

---

## Task 8: Write `graduacion/2026/README.md` (submission convention)

**Files:**
- Create: `universidad/graduacion/2026/README.md`

- [ ] **Step 1: Write the README**

Create `universidad/graduacion/2026/README.md`:
```markdown
# Trabajos de Graduación — 2026

Carpeta para revisar **anteproyectos**, **prácticas profesionales** e **informes finales**
de Trabajo de Graduación UTP/FISC. No es docencia por semestre; es asesoría/revisión.

## Convención

Una carpeta por estudiante (o por documento):

    graduacion/2026/<apellido-nombre>/
        <documento-original>.pdf        ← lo que entrega el estudiante
        revision-<tipo>-vN.md           ← revisión en markdown (fuente del PDF)
        revision-<tipo>-vN.pdf          ← PDF institucional generado
        whatsapp-<tipo>-vN.txt          ← mensaje copy-paste para el estudiante (si aplica)

`<tipo>` ∈ {anteproyecto, practica, informe-final}. Versionar (`v1`, `v2`, …) al recibir
nuevas entregas para comparar avance.

## Cómo revisar

1. Coloca el PDF del estudiante en su carpeta.
2. Pide a Claude: "revisa el anteproyecto de <estudiante>" (o práctica / informe final).
   Se dispara la skill correspondiente (`utp-fisc-anteproyecto-review`,
   `utp-fisc-practica-profesional-review`, `utp-fisc-final-doc-review`).
3. El entregable es un **PDF institucional** (logos UTP/FISC) vía `utp-fisc-review-pdf`,
   más un mensaje WhatsApp cuando se pida.
```

- [ ] **Step 2: Verify**

```bash
ls -la /Users/ea/Projects/universidad/graduacion/2026/README.md
```
Expected: file exists.

---

## Task 9: Write `universidad/.claude/README.md` (explains the folder + symlinks)

**Files:**
- Create: `universidad/.claude/README.md`

- [ ] **Step 1: Write the README**

Create `universidad/.claude/README.md`:
```markdown
# universidad/.claude — skills y contexto del workspace

Fuente de verdad de las skills de Claude Code para **todo lo universitario**
(trabajos de graduación: anteproyectos, prácticas profesionales, tesis/informes finales).

## skills/

| Skill | Para qué |
|---|---|
| `utp-fisc-anteproyecto-review` | Revisión profunda de anteproyectos (teórico/teórico-práctico/práctica), checklist FISC 12 puntos, rúbrica /100 |
| `utp-fisc-practica-profesional-review` | Chequeo de práctica profesional + mensaje WhatsApp al estudiante |
| `utp-fisc-final-doc-review` | Revisión del informe/documento final + rúbricas de sustentación |
| `utp-fisc-review-pdf` | Render del PDF institucional (logos UTP/FISC). Tiene `.venv` propio (reportlab + PyYAML) |

## Descubrimiento (symlinks)

Claude Code descubre skills en `~/.claude/skills/`. Por eso cada skill de aquí está
**symlinkeada** allá. Para re-crear los enlaces:

    SRC=/Users/ea/Projects/universidad/.claude/skills
    DST=/Users/ea/.claude/skills
    for s in utp-fisc-anteproyecto-review utp-fisc-practica-profesional-review utp-fisc-final-doc-review utp-fisc-review-pdf; do
      ln -snf "$SRC/$s" "$DST/$s"
    done

Editar las skills aquí (no en `~/.claude/skills/`, que solo son enlaces).

## Recrear el venv del PDF

    cd skills/utp-fisc-review-pdf && python3 -m venv .venv && .venv/bin/python3 -m pip install -r requirements.txt

## specs/ y plans/

Diseño e implementación de esta porción (brainstorming → spec → plan).
```

- [ ] **Step 2: Verify**

```bash
ls -la /Users/ea/Projects/universidad/.claude/README.md
```
Expected: file exists.

---

## Task 10: Restructure workspace into `regular/` + migrate Claude state (RUN LAST)

> This task moves the current working directory (`2026/`). Do it only after Tasks 1–9 are verified. All commands use ABSOLUTE paths and start from a path that survives the move.

**Files:**
- Move: `universidad/{2024,2025,2026}` → `universidad/regular/{2024,2025,2026}`
- Copy: Claude memory for the moved 2026 project key
- Modify: `universidad/CLAUDE.md`, teaching skills' hardcoded paths

- [ ] **Step 1: Find hardcoded `universidad/<year>` paths BEFORE moving**

```bash
grep -rln "universidad/2026\|universidad/2025\|universidad/2024\|universidad-2026\|universidad-2025\|universidad-2024" \
  /Users/ea/.claude/skills/grade-teams-lab \
  /Users/ea/.claude/skills/create-teams-assignment \
  /Users/ea/Projects/universidad/CLAUDE.md \
  /Users/ea/Projects/universidad/AGENTS.md 2>/dev/null
```
Record the matching files; they get updated in Step 6. (`AGENTS.md` may not exist — that's fine.)

- [ ] **Step 2: List existing Claude project dirs for these years (to migrate memory)**

```bash
ls -d /Users/ea/.claude/projects/-Users-ea-Projects-universidad-2026 \
      /Users/ea/.claude/projects/-Users-ea-Projects-universidad-2025 \
      /Users/ea/.claude/projects/-Users-ea-Projects-universidad-2024 2>/dev/null
```
Record which exist (likely only `…-2026`).

- [ ] **Step 3: Create `regular/` and move the year folders (2024, 2025 first)**

```bash
mkdir -p /Users/ea/Projects/universidad/regular
mv /Users/ea/Projects/universidad/2024 /Users/ea/Projects/universidad/regular/2024 2>/dev/null
mv /Users/ea/Projects/universidad/2025 /Users/ea/Projects/universidad/regular/2025 2>/dev/null
```

- [ ] **Step 4: Move 2026 LAST (this invalidates the shell cwd)**

```bash
mv /Users/ea/Projects/universidad/2026 /Users/ea/Projects/universidad/regular/2026
cd /Users/ea/Projects/universidad
pwd && ls regular
```
Expected: `pwd` shows `/Users/ea/Projects/universidad`; `regular/` lists 2024, 2025, 2026. (The first `cd` re-anchors the shell since `…/universidad/2026` no longer exists.)

- [ ] **Step 5: Migrate Claude memory to the new project key (non-destructive)**

For each project dir found in Step 2 (replace `<key>` per year), copy its `memory/` into the new `regular`-keyed dir so future sessions launched from the new path retain memory. Old dirs keep history intact.

```bash
OLD=/Users/ea/.claude/projects/-Users-ea-Projects-universidad-2026
NEW=/Users/ea/.claude/projects/-Users-ea-Projects-universidad-regular-2026
mkdir -p "$NEW"
[ -d "$OLD/memory" ] && cp -R "$OLD/memory" "$NEW/memory" && echo "memory migrated" || echo "no memory/ to migrate"
ls -la "$NEW/memory" 2>/dev/null | head
```
Expected: `MEMORY.md` and the memory `.md` files present under the new key. (Repeat for 2024/2025 only if Step 2 found them.)

- [ ] **Step 6: Update hardcoded paths found in Step 1**

For each file recorded in Step 1, replace `universidad/2026` → `universidad/regular/2026` (and same for 2024/2025) using the Edit tool, matching exact surrounding context. Re-verify:

```bash
grep -rn "Projects/universidad/2026\|Projects/universidad/2025\|Projects/universidad/2024" \
  /Users/ea/.claude/skills/grade-teams-lab \
  /Users/ea/.claude/skills/create-teams-assignment \
  /Users/ea/Projects/universidad/CLAUDE.md 2>/dev/null
```
Expected: no output (all updated to `regular/`).

- [ ] **Step 7: Update `universidad/CLAUDE.md` structure + add graduation section**

Edit `universidad/CLAUDE.md`:
1. In the "## Estructura" tree, nest the year folders under `regular/` and add `.claude/` and `graduacion/` siblings:
```
universidad/
├── CLAUDE.md / AGENTS.md          ← contexto genérico (este nivel, multi-año)
├── .claude/                       ← skills de graduación (anteproyecto/práctica/informe) + venv del PDF
├── regular/                       ← docencia por año (calificar asignaciones, Teams/Forms)
│   ├── 2024/  2025/               ← años anteriores (archivo)
│   └── 2026/
│       ├── $CODEX_HOME/
│       └── SEMI/                  ← primer semestre 2026 (DS_IX)
└── graduacion/                    ← trabajos de graduación UTP/FISC
    └── 2026/                      ← anteproyectos / prácticas / informes finales por estudiante
```
2. Add a row to the "## Skills relevantes" table:
```
| `utp-fisc-anteproyecto-review` / `utp-fisc-practica-profesional-review` / `utp-fisc-final-doc-review` | "revisa el anteproyecto/práctica/informe de X" | Revisa Trabajos de Graduación FISC (checklist 2018, rúbrica), genera PDF institucional vía `utp-fisc-review-pdf` |
```
3. Update any inline prose that says `2026/SEMI` or `<año>/SEM<I|II>` to `regular/2026/SEMI` / `regular/<año>/SEM<I|II>`.

- [ ] **Step 8: Spot-check the SEMI context files for absolute paths**

```bash
grep -rn "Projects/universidad/2026" \
  /Users/ea/Projects/universidad/regular/2026/SEMI/CLAUDE.md \
  /Users/ea/Projects/universidad/regular/2026/SEMI/MEMORY.md 2>/dev/null
```
Expected: no output (these use relative paths). If any match, update to `regular/2026`.

---

## Task 11: Final verification pass

- [ ] **Step 1: All 4 skills present, named, and symlinked**

```bash
for s in utp-fisc-anteproyecto-review utp-fisc-practica-profesional-review utp-fisc-final-doc-review utp-fisc-review-pdf; do
  src="/Users/ea/Projects/universidad/.claude/skills/$s/SKILL.md"
  link="/Users/ea/.claude/skills/$s/SKILL.md"
  test -f "$src" && test -f "$link" && echo "$s OK" || echo "$s FAIL"
done
```
Expected: 4 lines, all `OK`.

- [ ] **Step 2: No dangling OCR mechanism references across the ported skills**

```bash
grep -rln "ocr-and-documents" /Users/ea/Projects/universidad/.claude/skills/ || echo "clean"
```
Expected: `clean`.

- [ ] **Step 3: Workspace restructure intact**

```bash
ls -d /Users/ea/Projects/universidad/regular/2024 \
      /Users/ea/Projects/universidad/regular/2025 \
      /Users/ea/Projects/universidad/regular/2026 \
      /Users/ea/Projects/universidad/graduacion/2026 \
      /Users/ea/Projects/universidad/.claude/skills 2>&1
test ! -e /Users/ea/Projects/universidad/2026 && echo "old 2026 path gone (good)"
```
Expected: all listed paths exist; old top-level `2026/` is gone.

- [ ] **Step 4: PDF venv still works post-restructure**

```bash
/Users/ea/Projects/universidad/.claude/skills/utp-fisc-review-pdf/.venv/bin/python3 -c "import reportlab, yaml; print('pdf venv OK')"
```
Expected: `pdf venv OK`. (Venv uses absolute interpreter path; the move within `.claude` doesn't affect it since `.claude` didn't move.)

- [ ] **Step 5: Tell the user a session restart is needed for skill discovery**

The 4 skills are symlinked into `~/.claude/skills/` but Claude Code loads the skill list at session start. Note to the user: start a new session (from `universidad/regular/2026` or `universidad/`) to pick up the new skills and the migrated memory dir.

---

## Self-Review

- **Spec coverage:** 4 skills ported (Tasks 2–5) ✓; native PDF/`pdftotext` extraction replacing OCR (Tasks 2–5 edits) ✓; PDF+WhatsApp deliverable (Task 3 WhatsApp, Task 5/6 PDF) ✓; `.claude/skills` source-of-truth + symlink discovery (Tasks 7,9) ✓; `graduacion/2026` submissions area (Task 8) ✓; `regular/` restructure + Claude-state migration + path-ref fixes done LAST (Task 10) ✓; verification incl. sample render (Tasks 6,11) ✓.
- **Placeholder scan:** No TBD/TODO; every edit has exact old/new strings; every command has expected output.
- **Naming consistency:** Folder `utp-fisc-practica-profesional-review` matches the `name:` set in Task 3 Step 2 and the symlink/verify lists in Tasks 7 & 11. Render invocation uses `.venv/bin/python3` consistently (Tasks 5,6,11).
- **Known nuance:** Task 10 moves the live cwd; mitigated by ordering 2026 last + immediate `cd` to the surviving `universidad/` root. Memory migration is copy (non-destructive), so the live session's transcript dir is untouched.
