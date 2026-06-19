# Workspace docente — Universidad (multi-año)

Contexto y operación de este directorio para Claude. Léelo antes de actuar.

## ¿Qué es esto?

Workspace de gestión docente universitaria, organizado por año. No es código de aplicación: sirve para **calificar asignaciones, crear nuevas (Teams/Forms), generar materiales (PDFs) y mantener trazabilidad** de lo entregado por los estudiantes.

**No todos los semestres tienen la misma asignatura.** Este archivo solo contiene lo genérico/transversal; la asignatura, secciones, convenciones y estado de cada semestre viven en el `CLAUDE.md` de su carpeta `SEM*`.

## Estructura

```
universidad/
├── CLAUDE.md / AGENTS.md          ← contexto genérico (este nivel, multi-año)
├── .claude/                       ← skills de graduación (anteproyecto/práctica/informe) + venv del PDF; ver .claude/README.md
├── regular/                       ← DOCENCIA por año (calificar asignaciones, Teams/Forms)
│   ├── 2024/  2025/               ← años anteriores (archivo)
│   └── 2026/
│       ├── $CODEX_HOME/           ← automations de Codex del año
│       ├── SEMI/                  ← primer semestre 2026 (asignatura actual: DS_IX)
│       │   ├── CLAUDE.md          ← contexto ESPECÍFICO del semestre/asignatura — leerlo al trabajar aquí
│       │   ├── MEMORY.md          ← memoria operativa del curso del semestre
│       │   ├── submissions/       ← una carpeta por asignación (asignacion-NN-*/)
│       │   ├── materials/  scripts/  pdf-qa/  portafolio_docente/
│       │   ├── grades/            ← exports de Teams + precalificaciones
│       │   └── debug-dumps/       ← dumps de Playwright (descartables)
│       └── (SEMII/ — desde agosto 2026)
└── graduacion/                    ← TRABAJOS DE GRADUACIÓN UTP/FISC (no es docencia por semestre)
    └── 2026/                      ← anteproyectos / prácticas / informes finales por estudiante
```

> **Replicación**: año nuevo → `universidad/regular/<año>/`; semestre nuevo → `regular/<año>/SEM<I|II>/` con su propio `CLAUDE.md` + `MEMORY.md` describiendo la asignatura de ese semestre y la misma estructura interna (submissions, materials, grades, debug-dumps…). Trabajos de graduación → `universidad/graduacion/<año>/`.

## Skills relevantes (invocar primero, no reinventar)

| Skill | Cuándo | Qué hace |
|---|---|---|
| `grade-teams-lab` | "califica asignación N", "grade los repos" | Descubre repos GitHub de estudiantes, clona, aplica rúbrica heurística, llena Teams via Playwright |
| `create-teams-assignment` | "crea la asignación X", "agrega un parcial" | Crea asignaciones en Teams con título, instrucciones, rúbrica ponderada, fechas; soporta Forms quiz (`lib/create_quiz.js`) asociado a la clase |
| `utp-fisc-anteproyecto-review` / `utp-fisc-practica-profesional-review` / `utp-fisc-final-doc-review` | "revisa el anteproyecto / práctica / informe final de X" | Revisa Trabajos de Graduación UTP/FISC (reglamento FISC 2018, checklist 12 puntos, rúbrica /100); entregable = PDF institucional vía `utp-fisc-review-pdf` (+ mensaje WhatsApp en práctica). Trabajan sobre `graduacion/<año>/` |
| `utp-fisc-review-pdf` | (lo invocan las skills de revisión) | Renderiza el PDF académico con logos UTP/FISC. Tiene `.venv` propio (reportlab+PyYAML) en `.claude/skills/utp-fisc-review-pdf/` |
| `gsd:*` | Workflows estructurados multi-fase | Solo si el usuario lo invoca explícitamente |

### Para crear quizzes Forms (importante)

El Forms quiz **DEBE** abrirse desde Teams → Create → New quiz → **Add quiz**. Abrir `forms.office.com` directamente crea un quiz huérfano que no se puede reasociar. Corrección explícita del usuario (2026-05-18): *"El forms tienes que abrirlo desde la creación de la asignación en teams, para que se asocie"*.

Detalles del editor Forms en `~/.claude/skills/create-teams-assignment/SKILL.md` sección **"Forms quiz assignments"**.

## Convenciones genéricas de creación de asignaciones

1. **JSON como source-of-truth** (quiz/rubric data) antes de correr Playwright. Permite auditar, re-correr, hacer diff. Guardarlo en la carpeta de la asignación bajo `SEM*/submissions/`.
2. **Preguntas de desarrollo = UN concepto cada una**, no 3-en-1. Corrección del usuario: *"parecen 3 preguntas en 1. Debería ser solo 1."*
3. **MC distribuidas entre todos los temas** evaluables (no concentradas en uno). Documentar en `_topics_covered`.
4. **Timer**: para quiz de N minutos, `dueTime = postTime + (N+10) min`. 10 min de buffer de llegada.
5. Asignaciones se nombran `<N>. <Título>` — verificar en Teams qué números ya están usados antes de numerar.

## Operación con Playwright Teams

- Usar `mcp__playwright__browser_run_code_unsafe` para flujos complejos con frames anidados (Teams → assignments iframe → Forms iframe).
- Selectors clave:
  - Top-level: `page.locator('iframe').first().contentFrame()` → app de assignments
  - Forms: `page.frames().find(f => f.url().includes('forms.office.com'))`
- Una pregunta del quiz solo expone sus textboxes cuando está enfocada; las demás colapsan a `button[aria-label^="N. Question title ..."]`.
- "Done" (top-right en Teams iframe) asocia el quiz a la asignación. "Close" es el botón de retorno cuando re-editas un quiz adjunto.

## Control de versiones

Este workspace está en el repo **privado** `git@github.com:ErickAgrazal/universidad-ai.git` (rama `main`). Es privado a propósito: incluye reportes con nombres+notas de estudiantes (FINAL_GRADES, GRADING_RESULTS, `revisiones/`, precalificaciones). **Si alguna vez se vuelve público, purgar esos reportes del historial primero.**

- **Se versiona** (por allowlist): contexto (CLAUDE/AGENTS/MEMORY/programa), `.claude/skills` + comandos, `SEM*/scripts`, `SEM*/materials`, definiciones de asignaciones (RUBRIC/INSTRUCTIONS/quiz/assignment.json) y reportes md/csv seleccionados.
- **Se ignora** (`.gitignore`): repos clonados de estudiantes, videos/binarios, `node_modules`/`.venv`/`__pycache__`, `debug-dumps`/`pdf-qa`, `/2026/`, `/graduacion/`, y PII cruda (`notas_actuales_*`, `matricula_midterm_*`, `*_rosters.json`, `feedback_*.json`, `.xlsx` de Teams).
- **Nunca `git add -A`** (arrastra los 133 `.git` anidados de clones y la PII cruda). Añadir por allowlist explícita de archivos.

## Dumps de depuración

Los `*.md`/`*.png`/`*.yml` que genera Playwright durante sesiones (screenshots, snapshots de listas, vistas de estudiantes) van en `SEM*/debug-dumps/`, NO sueltos en la raíz ni en el año. No son documentación. Se pueden borrar sin pérdida una vez la sesión termina. (Están en `.gitignore`.)

## Cosas que NO hacer

- No abrir `forms.office.com` directamente para editar un quiz de Teams (se vuelve huérfano).
- No usar `git add -A` aquí — el directorio acumula repos clonados de estudiantes, PII cruda y screenshots de Playwright. Añadir por allowlist explícita (ver "Control de versiones").
- No re-correr `grade-teams-lab` sin revisar primero el FINAL_GRADES.md de la asignación: las notas ya pueden estar en Teams.
- No confiar en transcripciones Whisper para detectar grupos — siempre cruzar con las fuentes escritas (PDFs) del semestre.
