# Desktop pack — Revisión UTP/FISC en Claude Desktop / claude.ai

Dos formas de usar las revisiones de Trabajos de Graduación fuera de Claude Code.
Recuerda: en Desktop **adjuntas el PDF en el chat** (no hay acceso a tu disco), y la
fuente de verdad de las skills sigue siendo `universidad/.claude/skills/` en el Mac.

---

## Opción 1 — Proyecto de Claude Desktop (lo más simple)

Entrega revisión en **markdown** + mensaje WhatsApp. No genera el PDF con logos.

1. Claude Desktop → **Projects** → New project (ej. "Revisión Graduación UTP/FISC").
2. **Custom instructions:** pega TODO el contenido de `INSTRUCCIONES-PROYECTO.md`.
3. **Project knowledge:** sube los 3 archivos de `conocimiento/`:
   - `fisc-anteproyecto.md`
   - `fisc-informe-final.md`
   - `fisc-calibracion-notas.md`
4. Uso: en un chat del proyecto, **adjunta el PDF** del estudiante y escribe
   "revisa este anteproyecto" (o "califica"). Obtienes veredicto, nota /100,
   correcciones, checklist FISC y, si es práctica, el mensaje de WhatsApp.
5. Si quieres el **PDF institucional con logos**, copia el markdown y córrelo por la
   skill `utp-fisc-review-pdf` en Claude Code (Mac), o usa la Opción 2.

---

## Opción 2 — Subir como Skills de Anthropic

Solo si tu plan muestra **Skills** en claude.ai/Desktop (Settings → Capabilities/Skills).
Estas corren en el sandbox de código de Claude, así que **sí** pueden generar el PDF
institucional (instalan `reportlab` solas).

Archivos en `skills-upload/` (un `.zip` por skill, con paths relativos y sin el venv del Mac):
- `utp-fisc-anteproyecto-review.zip`
- `utp-fisc-practica-profesional-review.zip`
- `utp-fisc-final-doc-review.zip`
- `utp-fisc-review-pdf.zip`  ← el que rinde el PDF con logos UTP/FISC

Pasos:
1. claude.ai/Desktop → Skills → **Upload skill** → sube cada `.zip`.
2. En un chat, **adjunta el PDF** y pide la revisión; Claude invoca la skill.
3. Para el PDF con logos, el sandbox corre
   `pip install -r requirements.txt && python3 scripts/render_utp_fisc_review_pdf.py rev.md rev.pdf`
   y te da el PDF descargable.

Notas:
- Subes **una sola vez**; luego usas las skills en cualquier chat.
- Si Skills **no** aparece en tu plan, usa la Opción 1.
- `pdftotext`/`textutil` pueden no existir en el sandbox; no importa, Claude lee el PDF
  adjunto directamente.

---

## Mantener sincronizado

Si editas las skills en `universidad/.claude/skills/` (la fuente de verdad), vuelve a
generar este pack: re-copia `conocimiento/` y re-arma los `.zip` de `skills-upload/`.
