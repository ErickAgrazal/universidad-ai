# Workspace docente — Universidad (multi-año)

Contexto y operación de este directorio para Codex. Léelo antes de actuar.

## ¿Qué es esto?

Workspace de gestión docente universitaria, organizado por año. No es código de aplicación: sirve para **calificar asignaciones, crear nuevas (Teams/Forms), generar materiales (PDFs) y mantener trazabilidad** de lo entregado por los estudiantes.

**No todos los semestres tienen la misma asignatura.** Este archivo solo contiene lo genérico/transversal; la asignatura, secciones, convenciones y estado de cada semestre viven en el `AGENTS.md` (y `CLAUDE.md`) de su carpeta `SEM*`.

## Estructura

```
universidad/
├── AGENTS.md / CLAUDE.md          ← contexto genérico (este nivel, multi-año)
├── 2024/  2025/                   ← años anteriores (archivo)
└── 2026/
    ├── $CODEX_HOME/               ← automations de Codex del año
    ├── SEMI/                      ← primer semestre 2026 (asignatura actual: DS_IX)
    │   ├── AGENTS.md / CLAUDE.md  ← contexto ESPECÍFICO del semestre/asignatura — leerlo al trabajar aquí
    │   ├── MEMORY.md              ← memoria operativa del curso del semestre
    │   ├── submissions/           ← una carpeta por asignación (asignacion-NN-*/)
    │   ├── materials/  scripts/  pdf-qa/  portafolio_docente/
    │   ├── grades/                ← exports de Teams + precalificaciones
    │   └── debug-dumps/           ← dumps de Playwright (descartables)
    └── (SEMII/ — desde agosto 2026)
```

> **Replicación**: año nuevo → `universidad/<año>/`; semestre nuevo → `<año>/SEM<I|II>/` con sus propios `AGENTS.md`/`CLAUDE.md` + `MEMORY.md` describiendo la asignatura de ese semestre y la misma estructura interna.

## Skills relevantes (invocar primero, no reinventar)

| Skill | Cuándo | Qué hace |
|---|---|---|
| `grade-teams-lab` | "califica asignación N", "grade los repos" | Descubre repos GitHub de estudiantes, clona, aplica rúbrica heurística, llena Teams via Playwright |
| `create-teams-assignment` | "crea la asignación X", "agrega un parcial" | Crea asignaciones en Teams con título, instrucciones, rúbrica ponderada, fechas; soporta Forms quiz (`lib/create_quiz.js`) asociado a la clase |
| `gsd:*` | Workflows estructurados multi-fase | Solo si el usuario lo invoca explícitamente |

Los skills específicos de una asignatura (p. ej. generación de capítulos PDF) se documentan en el `AGENTS.md` del semestre correspondiente.

### Para crear quizzes Forms (importante)

El Forms quiz **DEBE** abrirse desde Teams → Create → New quiz → **Add quiz**. Abrir `forms.office.com` directamente crea un quiz huérfano que no se puede reasociar. Corrección explícita del usuario (2026-05-18): *"El forms tienes que abrirlo desde la creación de la asignación en teams, para que se asocie"*.

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

## Dumps de depuración

Los `*.md`/`*.png`/`*.yml` que genera Playwright durante sesiones van en `SEM*/debug-dumps/`, NO sueltos en la raíz ni en el año. No son documentación. Se pueden borrar sin pérdida una vez la sesión termina.

## Cosas que NO hacer

- No abrir `forms.office.com` directamente para editar un quiz de Teams (se vuelve huérfano).
- No usar `git add -A` aquí — el directorio acumula screenshots de Playwright que no deben commitearse.
- No re-correr `grade-teams-lab` sin revisar primero el FINAL_GRADES.md de la asignación: las notas ya pueden estar en Teams.
- No confiar en transcripciones Whisper para detectar grupos — siempre cruzar con las fuentes escritas (PDFs) del semestre.
