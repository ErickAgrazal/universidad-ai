---
description: Revisar el Trabajo de Graduación UTP/FISC más reciente en graduacion/ (o el del estudiante indicado) y generar el PDF institucional (+ WhatsApp si es práctica)
argument-hint: "[estudiante opcional]"
---

Revisa un Trabajo de Graduación UTP/FISC y entrega el PDF institucional de comentarios.

Argumento (opcional): `$ARGUMENTS` = nombre o slug del estudiante. Si está vacío, usar el documento entregado más reciente.

## Pasos

1. **Ubicar el documento** bajo `/Users/ea/Projects/universidad/graduacion/`:
   - Usar el año más reciente (carpeta con el número mayor).
   - Documento candidato = PDF con `mtime` más nuevo, **excluyendo** los `revision-*.pdf` ya generados.
   - Si `$ARGUMENTS` tiene valor, primero filtrar a la carpeta/estudiante cuyo slug (`apellido-nombre`) haga match.
   - Si el PDF está suelto en `graduacion/<año>/` (no dentro de una carpeta de estudiante), crear `graduacion/<año>/<apellido-nombre>/` y mover el PDF allí con un nombre limpio (`anteproyecto-vN.pdf` o `informe-final-vN.pdf`, deduciendo de su nombre).

2. **Determinar tipo/modalidad** leyendo portada + índice del PDF (usar la herramienta Read; para páginas escaneadas, renderizar con `pdftoppm -png -r 120 -f P -l P archivo.pdf /tmp/...` y leer el PNG):
   - **Anteproyecto** (Teórico / Teórico-Práctico / **Práctica Profesional**) → invocar la skill `utp-fisc-anteproyecto-review`.
   - **Informe / documento final / tesina** → invocar la skill `utp-fisc-final-doc-review`.

3. **Ejecutar la revisión** siguiendo la skill: aplicar checklist FISC, revisar coherencia y alcance, y **verificar evidencia visual** (firmas, sellos, sombreado del Gantt, casillas marcadas) antes de marcar cualquier ítem como cumplido. No inflar la nota.

4. **Generar entregables** en la carpeta del estudiante (bumpear `vN` si ya existe una revisión previa):
   - `revision-<tipo>-vN.md` (fuente, con el frontmatter de `utp-fisc-review-pdf`).
   - `revision-<tipo>-vN.pdf` — PDF institucional vía:
     `"/Users/ea/Projects/universidad/.claude/skills/utp-fisc-review-pdf/.venv/bin/python3" "/Users/ea/Projects/universidad/.claude/skills/utp-fisc-review-pdf/scripts/render_utp_fisc_review_pdf.py" <md> <pdf>`
   - Si es **práctica profesional**, además `whatsapp-<tipo>-vN.txt` (mensaje copy-paste para el estudiante).

5. **En el chat**: veredicto + nota /100 + 3-5 correcciones priorizadas + rutas de los entregables, y ofrecer el PDF.

Responder en español. Si solo se recibió un fragmento o falta contexto, decirlo explícitamente.
