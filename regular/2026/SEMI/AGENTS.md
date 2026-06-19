# SEMI 2026 — Desarrollo de Software IX (DS_IX) — contexto para Codex

Contexto específico de este semestre/asignatura. El contexto genérico del workspace está en `universidad/AGENTS.md`. La estructura de esta carpeta, las convenciones de calificación y el estado actual de asignaciones están en `CLAUDE.md` (esta misma carpeta) — aplican igual para Codex. La memoria operativa del curso está en `MEMORY.md`.

## Asignatura y secciones

Curso **DES__SOFT_IX** (código 1493, FISC — UTP), dos secciones paralelas:

- **1GS241** (clase 1) — `DES__SOFT_IX_1GS241_2026` en Teams
- **1GS242** (clase 2) — `DES__SOFT_IX_1GS242_2026` en Teams (doble underscore)

> **Convención de carpetas grupo**: `grupo-1` = clase **241**, `grupo-2` = clase **242**. Contraintuitivo — verificar cada vez.

## Skill específico del curso: capítulos/materiales PDF

Usar primero el skill `dsix-chapter-pdf` en `/Users/ea/.codex/skills/dsix-chapter-pdf`.

- El skill contiene el programa oficial en `references/course-program-dsix.md`.
- El patrón visual y de contenido aprendido del capítulo 1 está en `references/chapter-pattern.md`.
- La plantilla ReportLab reutilizable está en `scripts/build_chapter_pdf_template.py`.
- Flujo esperado: generar PDF local en `materials/capitulos/`, renderizar páginas para QA visual, entregar el PDF para revisión y **no subirlo a Teams** hasta que el usuario lo confirme.

## Políticas de calificación confirmadas por el usuario

### A8 — Parcial Teórico (aplica a parciales teóricos en general)

- Preguntas de escoger varias/mejor respuesta: **3 pts solo si está perfecta**; **1 pt si marcó al menos una opción correcta/buena**, aunque haya omitido otras correctas o marcado una mala; **0 pts solo si no tiene ninguna buena**.
- Preguntas abiertas: analizar contenido y asignar hasta 10 pts con criterio estricto. Solo respuestas realmente completas merecen 10. Si escribieron algo razonable, evitar bajar de 5 salvo respuestas vacías, irrelevantes o muy malas.
- Caso de referencia: pregunta TanStack donde el estudiante marcó Query/Router y una mala, pero omitió Table → **1/3**, no 0.

### A9 — Proyecto individual: Pokemon Battle Rooms

- No volver a adjuntar una rúbrica Teams sin puntos (modo "No points" bloquea la nota con `Points are disabled for the selected rubric`). Usar la rúbrica del enunciado como guía manual, o crear una rúbrica puntuable que sume 100 pts verificada antes de publicar.
