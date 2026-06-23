# SEMI 2026 — Desarrollo de Software IX (DS_IX)

Contexto específico de este semestre/asignatura. El contexto genérico del workspace está en `universidad/CLAUDE.md`.

## Asignatura y secciones

Curso **DES__SOFT_IX** (código 1493, FISC — UTP), dictado a dos secciones paralelas:

- **1GS241** (clase 1) — `DES__SOFT_IX_1GS241_2026` en Teams
- **1GS242** (clase 2) — `DES__SOFT_IX_1GS242_2026` en Teams

Las clases en Teams usan `DES__SOFT_IX_1GS<sección>_2026` (con doble underscore). Programa de la asignatura: `COURSE_PROGRAM_DS_IX.md` (resumen del PDF oficial en `materials/`). Ponderación real del curso registrada en `MEMORY.md`: Parciales 30%, Proyectos/Investigaciones 15%, Laboratorios 15%, Portafolio 5%, Semestral 30%, Asistencia 5%.

## Estructura de esta carpeta

```
SEMI/
├── CLAUDE.md                  ← este archivo
├── MEMORY.md                  ← memoria operativa del curso (decisiones, sesiones)
├── COURSE_PROGRAM_DS_IX.md
├── submissions/
│   ├── asignacion-01-github-repo/        ← A1
│   ├── asignacion-02-investigacion/      ← A2
│   ├── asignacion-03-presentacion-grupal/← A3 (videos)
│   ├── asignacion-04-informe-grupal/     ← A4 (PDFs/MDs; FINAL_GRADES.md + RUBRIC.md)
│   ├── asignacion-05-pollclass/          ← A5 (grupo-1/ = 241, grupo-2/ = 242)
│   ├── asignacion-06-playwright/         ← A6
│   ├── asignacion-08-parcial-teorico/    ← A8 (class1_quiz.json / class2_quiz.json)
│   └── asignacion-11-parcial-react-hono/ ← A11 (quiz.json compartido por ambas clases)
├── materials/                 ← capítulos, módulos, portafolio docente, PDF del programa
├── scripts/                   ← build_*.py que generan los PDFs de materials/ (ROOT = SEMI/)
│   ├── build_module_pdfs_v2.py   ← builder de capítulos 2-9 (versión extendida 10-14 págs, 2026-06-12). Con el Cap. 9 (integraciones: terceros/pagos/IA) el temario oficial queda 100% cubierto.
│   ├── chapters_ext/cap0N.py     ← contenido por capítulo (dict CHAPTER, DSL de bloques; editar aquí y re-correr el builder)
│   ├── diagrams.py               ← librería de diagramas vectoriales (paleta del curso). En capítulos: bloque ("diagram", "nombre"); en scripts standalone: DIAGRAMS["nombre"](). 15 diagramas en 11 documentos (2026-06-12).
│   ├── build_guia_parcial3_react_hono.py / build_modulo_extra_mcp.py / build_modulo_extra_*_pdf.py  ← documentos standalone (guía y módulos extra)
│   └── build_teacher_portfolio_pdfs.py  ← portafolio docente (8 secciones + combinado; correr con uv --with reportlab --with pypdf; actualizado 2026-06-12)
├── pdf-qa/                    ← QA visual de los PDFs generados
├── portafolio_docente/
├── grades/                    ← exports .xlsx de Teams + precalificaciones (csv/md/json)
└── debug-dumps/               ← screenshots y dumps de Playwright (descartables)
```

> **Convención de carpetas grupo**: `grupo-1` = clase **241**, `grupo-2` = clase **242**. Cuenta esto cada vez — es contraintuitivo.

## Convenciones de calificación (este curso)

1. **Parsear PDFs primero** para identificar grupos antes de calificar A3 (video). El campo `Integrantes:` del PDF es la señal más confiable; Whisper a veces deforma nombres en transcripciones.
2. **Grupos heredan entre asignaciones**: si un estudiante aparece en un grupo en A4, su nota de A3 debería reflejar pertenencia al grupo (no "no encontrado").
3. **Scoring per-criterio para informes**: páginas, citas APA (regex `\([0-9]{4}\)`), número de "Conclusión", presencia de "Bibliografía". Diferencia 85 de 92 de 100 sin re-leer cada PDF.
4. **Buscar en `Laboratorios/Tareas/`** cuando un informe parece vago — a veces el README real está enterrado en una sub-carpeta temática.

## Estado actual (al 2026-06-11)

> **Catálogo de asignaciones**: `ASSIGNMENTS.md` (en esta carpeta) es el índice único con metadata + instrucciones/contenido + rúbrica de cada asignación (A1–A14). La fuente de verdad de lo que ven los estudiantes sigue siendo Teams.
>
> **REGLA (siempre)**: cada vez que se **agregue una asignación o se modifique algo** de una (instrucciones, rúbrica, fechas, estado), (1) actualizar `ASSIGNMENTS.md` y (2) **emitir una nueva versión del PDF** corriendo:
> `uv run --with markdown --with xhtml2pdf --with pillow regular/2026/SEMI/scripts/build_assignments_pdf.py --note "<qué cambió>"`
> El script numera solo (vNNN), no sobrescribe versiones previas, actualiza `ASSIGNMENTS_latest.pdf` y registra la emisión en `materials/assignments_pdf/VERSIONS.md`. Los PDF están gitignored (binarios); se versionan `ASSIGNMENTS.md`, el script y `VERSIONS.md`.

- **A1–A6**: calificadas en ambas clases (excepto retornos manuales pendientes que hace el usuario).
- **A7 (`7. Parcial #2: MVP de Aplicación Startup Full Stack en Grupo`)**: notas manuales del usuario ingresadas en Teams. En 241 queda 1 entrega en "Ready to grade".
- **A8 (`8. Parcial Teórico`)** = Parcial #1 teórico: 20 MC + 2 desarrollo = 80 pts, 20 min. Aplicado May 20 (241) y May 21 (242).
- **A9 (`9. Proyecto individual: Pokemon Battle Rooms`)**: calificada y devuelta (May 22, 36/36 ambas clases).
- **A10 (`10. Proyecto individual: Juego de Damas con IA A*`)**: publicada en ambas clases el 2026-06-11. Due **Vie Jun 12** 11:59 PM (sin cambios), cierre (late) extendido a **Dom Jun 21** 11:59 PM en ambas clases el 2026-06-19 (solo se movió la fecha de cierre, no la de entrega), 100 pts. Mismo stack que A9 + microservicio Bun con A* puro (criterio de mayor peso, 25 pts), login/ranking, pago en modo prueba, tests. Sin rúbrica Teams (lección A9); puntos por criterio en las instrucciones. Fuente: `submissions/asignacion-10-damas-astar/`.
- **A12 (`12. Laboratorio: Servidor MCP local con GitHub Copilot en VS Code`)**: laboratorio publicado en ambas clases el 2026-06-19, 100 pts, rúbrica Teams 5×20%. Construir un FastMCP `server.py` (3 tools base) + `.vscode/mcp.json` (stdio) + ejecución desde Copilot en modo Agent + 4 retos + evidencias en repo GitHub. Due **241: Mié Jun 24 11:00 PM**, **242: Jue Jun 25 11:00 PM**. Fuente: `submissions/asignacion-12-laboratorio-mcp/assignment.json` (origen: `regular/2026/Laboratorio_MCP_1.docx`).
- **A13 (`13. Diseño: Historias de Usuario MVP — Production-Ready y MCP`)**: asignación GRUPAL de diseño (fase previa al proyecto MCP), publicada con rúbrica Teams 5×20% en ambas clases el 2026-06-21. Entregable: UN PDF por grupo (mismos grupos del MVP/A7) con historias de usuario: (1) inventario del MVP ya implementado, (2) ≥30 historias nuevas para production-ready, (3) ≥15 del total expuestas vía MCP bajo auth (importables en Claude Code/Codex). Después: reunión presencial por grupo para decidir qué implementar. Due **241: Lun Jun 22 11:59 PM**, **242: Mar Jun 23 11:59 PM**. Fuente: `submissions/asignacion-13-historias-usuario-mcp/assignment.json`. Título acortado a 61 chars por el límite de 70 de Teams.
- **A14 / A15 — Avances semanales del Semestral** (grupales, mismos grupos del MVP/A7, 100 pts c/u, rúbrica Teams 5×20% "Rúbrica - Avance del Semestral"): checkpoints de implementación del proyecto semestral. **Programados (Schedule) en ambas clases el 2026-06-22**. A14 (Avance 1: tablero GitHub Projects + despliegue remoto gratuito + primeros tickets→PRs + harness Playwright) libera **Lun 29 jun 7:00 AM**, due **241 Mié 1 jul / 242 Jue 2 jul**. A15 (Avance 2: MCP integrado + QA + pruebas Playwright E2E sobre TODAS las funcionalidades + despliegue actualizado + borrador pitch) libera **Lun 6 jul 7:00 AM**, due **241 Mié 8 jul / 242 Jue 9 jul**. Fuentes: `submissions/asignacion-14-avance1-semestral/`, `asignacion-15-avance2-semestral/`.
- **A16 — Proyecto Semestral (sustentación)**: PUBLICADA (Assign) en ambas clases el 2026-06-23, rúbrica Teams de 3 criterios (50/40/10), 100 pts (`submissions/asignacion-16-semestral-final/`). Implementación de las historias de A13 (+ comentarios) sobre React 19 + Bun/Hono + MongoDB + servidor MCP. Sustentación EN CLASE: **241 Jue 23 jul / 242 Vie 24 jul** (2da semana de exámenes), todo el grupo presenta. Nota (sobre 100, confirmada): **Funcionalidad 50% + Preguntas (hasta 5) 40% + Presentación 5 min 10%** (el semestral vale 30% del curso). El concepto previo de "build servidor MCP" queda absorbido aquí (MCP es parte del stack del semestral).
- **Calendario UTP (I Semestre 2026, calendario oficial 2026-2027)**: terminación de clases **Sáb 11 jul 2026**; exámenes **Lun 13 – Sáb 25 jul**; entrega de calificaciones **20 jul – 1 ago**. II Semestre (SEMII) inicia **Lun 17 ago 2026**.
- **A11 (`11. Parcial #3: React y Hono`)**: quizzes Forms creados y programados (2026-06-10; renumerado de 9→11 porque el 9 ya estaba usado). Es el tercer parcial (#1 = A8, #2 = A7 MVP). Fuente: `submissions/asignacion-11-parcial-react-hono/quiz.json` (mismo contenido ambas clases):
  - Clase 1 (1GS241): Lun **Jun 15** 7:30 PM, due 8:10 PM (el original de Jun 10 fue borrado y recreado)
  - Clase 2 (1GS242): Mar **Jun 16** 7:30 PM, due 8:10 PM (movido desde Jun 11)
  - Cada uno: 20 MC (3 pts c/u — 15 React 19, 5 Hono) + 2 desarrollo (10 pts c/u) = 80 pts, 30 min timer.
  - Los drafts huérfanos "7. Entrega de parcial #2" y "Untitled assignment" en 241 fueron descartados el 2026-06-11.
  - Guía de estudio publicada (2026-06-11) en Class Materials/MODULO_03 de ambos salones: `materials/modulos/MODULO_03_DESARROLLO_IMPLEMENTACION/GUIA_ESTUDIO_PARCIAL_3_REACT_19_Y_HONO.pdf` (generada con `scripts/build_guia_parcial3_react_hono.py`). Cubre el gap: el Cap. 7 solo trae React clásico y no existía material de Hono.
