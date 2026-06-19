# Diseño: Revisión de Trabajos de Graduación UTP/FISC en Claude Code

Fecha: 2026-06-16
Estado: aprobado en brainstorming, pendiente revisión del spec
Autor: Erick (con Claude)

## Objetivo

Portar a este workspace `universidad` el flujo de revisión académica que existía en
hermes (`~/.hermes`) para evaluar **anteproyectos**, **prácticas profesionales** y
**documentos finales** de Trabajo de Graduación UTP/FISC, usando Claude Code en lugar
de hermes (que actualmente consume tokens de forma ineficiente). Mantener fidelidad al
contenido normativo de hermes y aprovechar las ventajas de Claude Code (lectura nativa
de PDF con visión).

## Fuente (hermes) que se porta

- `~/.hermes/profiles/hermesgeneralist/skills/academic/utp-fisc-anteproyecto-review/`
  (SKILL.md + `references/calificacion-anteproyectos-ejemplos.md`) — la skill profunda,
  reglamento FISC 2018, checklist de 12 puntos, rúbrica /100, calibración de notas.
- `~/.hermes/profiles/g2stash/skills/productivity/utp-fisc-practica-profesional-anteproyecto-review/SKILL.md`
  — variante de práctica profesional + mensaje WhatsApp para el estudiante.
- `~/.hermes/profiles/hermesgeneralist/skills/academic/utp-fisc-final-doc-review/`
  — revisión del documento/informe final.
- `~/.hermes/profiles/hermesgeneralist/skills/academic/utp-fisc-review-pdf/`
  (SKILL.md + `scripts/render_utp_fisc_review_pdf.py` + `templates/review-template.md`
  + `assets/{utp-logo.png,fisc-logo.png}`) — genera el PDF institucional.

## Skills resultantes (4)

| Skill (nuevo nombre) | Propósito | Entregable |
|---|---|---|
| `utp-fisc-anteproyecto-review` | Revisión profunda de anteproyectos (teórico / teórico-práctico / práctica profesional): checklist FISC de 12 puntos, coherencia académica, alcance técnico, rúbrica /100 con calibración | PDF + resumen en chat |
| `utp-fisc-practica-profesional-review` | Chequeo enfocado en práctica profesional (carta de aceptación, supervisor, actividades) + mensaje WhatsApp listo para enviar al estudiante | PDF + mensaje WhatsApp |
| `utp-fisc-final-doc-review` | Revisión del informe/documento final de graduación | PDF + resumen |
| `utp-fisc-review-pdf` | Renderiza el PDF institucional (logo UTP izq., logo FISC der., tabla de estado compacta, correcciones, checklist de cumplimiento) | PDF |

Las tres skills de revisión invocan a `utp-fisc-review-pdf` para el entregable, igual
que en hermes.

## Adaptación clave: extracción de PDF

Hermes dependía de una skill `ocr-and-documents` (PyMuPDF render + OCR). **Claude Code
lee PDFs de forma nativa** con la herramienta Read (texto + render visual de páginas
escaneadas para visión). Por lo tanto, en cada SKILL.md se reescribe el paso de
extracción a:

- Usar la herramienta **Read sobre el PDF** directamente, con el parámetro `pages` para
  inspeccionar visualmente las páginas críticas: registro oficial del tema,
  cronograma/Gantt, créditos académicos, constancia de matrícula/seguro, carta de
  aceptación de empresa, información de práctica, bibliografía y checklist final.
- `pdftotext` (disponible en `/opt/homebrew/bin/pdftotext`) como respaldo para volcado
  masivo de texto.

Esto elimina la dependencia de OCR y mejora justamente las verificaciones visuales que
la skill de hermes valora (sombreado del Gantt, firmas, sellos, casillas marcadas).
Todas las referencias a `ocr-and-documents` en el texto portado se reemplazan por esto.

## Estructura de carpetas (final)

```
universidad/
├── CLAUDE.md                     ← actualizado: rutas regular/2026/SEMI, +sección graduación
├── .claude/
│   ├── README.md                 ← qué es esto + mecanismo de symlinks
│   ├── specs/                    ← este documento
│   └── skills/
│       ├── utp-fisc-anteproyecto-review/      (SKILL.md, references/calificacion-…md)
│       ├── utp-fisc-practica-profesional-review/  (SKILL.md)
│       ├── utp-fisc-final-doc-review/         (SKILL.md)
│       └── utp-fisc-review-pdf/   (SKILL.md, scripts/, templates/, assets/, .venv/, requirements.txt)
├── regular/
│   └── 2024/  2025/  2026/        ← carpetas de docencia por año (movidas)
└── graduacion/
    └── 2026/                      ← PDFs entregados + revisiones generadas, por estudiante
        └── README.md             ← convención de nombres
```

`universidad/.claude/skills/` es la fuente de verdad organizada. Cada skill se
**symlinkea dentro de `~/.claude/skills/`** (donde ya viven `grade-teams-lab` y
`create-teams-assignment`, probadamente auto-invocables por Claude Code). Así quedan
agrupadas bajo el workspace y a la vez son descubribles. Son 4 symlinks.

## Dependencias del PDF

El renderer (`render_utp_fisc_review_pdf.py`) importa `reportlab` y `yaml` (PyYAML),
que **no están instalados** en este sistema. Plan:

- Crear un **`.venv`** local dentro de `utp-fisc-review-pdf/`, e instalar ahí
  `reportlab` + `pyyaml` (con `requirements.txt`).
- SKILL.md invoca `"$SKILL_ROOT/.venv/bin/python3" "$SKILL_ROOT/scripts/render_utp_fisc_review_pdf.py" rev.md rev.pdf`
  para ser autocontenido y no tocar el python del sistema.
- Logos: copiar `assets/{utp-logo.png,fisc-logo.png}` desde hermes.

## Reestructuración del workspace + migración de estado

Mover `2024/2025/2026` dentro de `regular/` tiene efectos colaterales porque Claude Code
indexa estado por ruta. Se ejecuta **al final del setup** (para no dejar la sesión
huérfana a mitad de trabajo). Pasos:

1. Crear `universidad/regular/` y mover `2024/`, `2025/`, `2026/` adentro.
2. Migrar el dir de proyecto/memoria de Claude:
   `~/.claude/projects/-Users-ea-Projects-universidad-2026/` →
   `~/.claude/projects/-Users-ea-Projects-universidad-regular-2026/`
   (preserva `MEMORY.md` y memorias acumuladas).
3. `grep` de rutas `universidad/2026`, `universidad/2025`, `universidad/2024` en:
   - `~/.claude/skills/grade-teams-lab/`, `~/.claude/skills/create-teams-assignment/`
   - `universidad/CLAUDE.md`, `universidad/regular/2026/SEMI/CLAUDE.md` y `MEMORY.md`
   - referencias a `$CODEX_HOME` dentro de `2026/`
   y actualizar cada una a la nueva ruta.
4. Actualizar el diagrama de estructura y el texto de `universidad/CLAUDE.md` para
   reflejar `regular/<año>/SEM*` y añadir una breve sección sobre `graduacion/` y las
   nuevas skills.

Riesgo conocido: el cwd actual de la sesión es `universidad/2026`; tras el movimiento la
ruta deja de existir. Por eso el move es el último paso y se hace con rutas absolutas.

## Verificación (antes de declarar "listo")

1. Los 4 symlinks en `~/.claude/skills/` resuelven y las skills aparecen listadas.
2. Render de prueba: pasar el sample de hermes
   `revision_anteproyecto_luisa_guerra_v1.md` por el `.venv` nuevo y confirmar que el
   PDF sale con logos (UTP izq., FISC der.), paginación, tabla de estado y secciones.
3. Tras la reestructuración: `MEMORY.md` accesible desde la nueva ruta de proyecto;
   `grep` no deja rutas `universidad/2026` colgando en skills/CLAUDE.md.

## Fuera de alcance (YAGNI)

- No se porta `ocr-and-documents` (reemplazado por Read nativo).
- No se automatiza descubrimiento de entregas (los PDFs los coloca Erick en
  `graduacion/2026/`).
- No se integra Teams/Forms aquí (esto es revisión de documentos, no asignaciones).
- El repo `universidad` no es git, así que no hay commit del spec (solo se guarda en
  disco).
