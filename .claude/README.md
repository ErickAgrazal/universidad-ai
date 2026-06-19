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
