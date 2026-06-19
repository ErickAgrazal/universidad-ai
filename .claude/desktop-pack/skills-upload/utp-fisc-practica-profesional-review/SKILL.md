---
name: utp-fisc-practica-profesional-review
description: Review a UTP FISC práctica profesional anteproyecto against faculty expectations and produce concise student feedback, including WhatsApp-ready messages.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [UTP, FISC, anteproyecto, práctica profesional, academic-review, PDF]
---

# UTP FISC práctica profesional anteproyecto review

Use this when a user wants to know whether a student's práctica profesional anteproyecto matches what FISC expects, especially from a PDF.

## Sources to ground against
Prefer official or near-official FISC/UTP materials. In this workflow, the most useful anchors were:
- FISC Reglamento para la inscripción, asesoría y sustentación de los trabajos de graduación
- FIE/FIM practice guides only as secondary cross-checks when FISC material is incomplete
- The student's submitted PDF itself

## Core FISC expectations to check
For práctica profesional in FISC, verify the anteproyecto includes:
1. Página de presentación
2. Registro oficial del trabajo de graduación
3. Introducción
4. Índice
5. Objetivo general y específicos
6. Plan de contenido
7. Bibliografía
8. Cronograma de actividades
9. Herramientas de software y hardware
10. Créditos académicos oficiales
11. Constancia de matrícula y, when requested, seguro estudiantil vigente
12. Información del programa de práctica profesional

Also verify práctica-profesional-specific content:
- Carta de aceptación de la empresa or equivalent formal company acceptance
- Nombre y ubicación de la empresa
- Explicación de producción/servicios/operación
- Área donde hará la práctica
- Puesto o rol a ocupar
- Supervisor asignado por la empresa
- Cargo y título del supervisor
- Descripción de actividades y grado de participación del estudiante

## FISC formatting expectations
Check for these even if only visually or by extracted text:
- Arial 12
- Interlineado 1.5
- Márgenes de 1 pulgada
- Tamaño carta
- Numeración inferior central

If formatting cannot be proven from extracted text, say so explicitly and limit claims to what is visible.

## Practical review workflow
1. Read the PDF directly with Claude Code's **Read tool** (it ingests text and renders scanned pages for vision; use the `pages` parameter for critical pages).
   - As a bulk-text fallback, run `pdftotext "file.pdf" -` in the terminal.
   - Do not trust extracted text alone: visually confirm signatures, stamps, the company acceptance letter, and Gantt shading that plain text omits.
2. Compare the document against the FISC checklist.
3. Separate findings into:
   - Present / acceptable
   - Missing
   - Weak / should improve
   - Inconsistencies
4. Look for common failure modes:
   - Missing signed official registration form
   - Non-official credits instead of official credits
   - Transcript-looking annexes that visually resemble portal exports or uncertified copies rather than official records
   - Index/table of contents errors like “Error! Marcador no definido.”
   - Company info present but no formal acceptance letter
   - Student request letter mistaken for company acceptance letter
   - Missing supervisor name, title, or cargo
   - Tools listed without justification
   - Introduction too descriptive but weak on problem, improvement, scope, methodology, technique
   - Technology stack inconsistencies across sections
   - Objectives not measurable enough
   - Bibliography count OK but formatting sloppy
   - Constancia, seguro, or annex evidence present but not clearly legible/current
   - Dates inconsistent across cover letters/anexos
5. Produce a short verdict:
   - “Encaja”
   - “Encaja con ajustes”
   - “No lo presentaría todavía así”
6. Then produce a WhatsApp-ready message in Spanish:
   - Formal but not overly stiff
   - Concrete, numbered or clearly grouped
   - No academic jargon overload
   - End with a positive next-step statement

## Recommended response structure
1. Short verdict
2. What is good
3. What is missing / needs correction
4. WhatsApp-ready copy

For Erick's deliverable: after the audit, generate the institutional PDF with `utp-fisc-review-pdf` (use `document_type: "Anteproyecto"` and `modality: "Práctica Profesional"`), then provide the WhatsApp-ready copy as a separate copy-paste block.

## Good phrasing for final student feedback
Use language like:
- “Va bien encaminado, pero antes de presentarlo…”
- “Lo principal sería…”
- “Conviene dejar más explícito…”
- “Revisar la coherencia…”
- “Si haces estos ajustes, quedará mucho mejor preparado para presentarlo en FISC.”

## Important nuance
Do not say a requirement is satisfied just because a checklist page appears in the PDF. Confirm whether the actual supporting document exists in the body/anexos. For example:
- A “Formulario de verificación” page is not the same as an attached signed “Registro oficial”.
- A student request letter is not the same as a company acceptance letter.
- A transcript-looking page may still be non-official if it visually lacks official certification cues.

## Example verdict pattern
- Good base and generally aligned with FISC
- Not ready to submit yet
- Main blockers: missing official registration form, non-official credits, TOC error, weak company acceptance evidence, supervisor data incomplete, tools unmotivated, intro/objectives consistency issues

## Output style notes
- Keep the explanatory audit concise and operational.
- When the user asks for a message to forward, write it in copy-pasteable Spanish for WhatsApp.
- Avoid markdown-heavy formatting if the destination is chat/mobile.
