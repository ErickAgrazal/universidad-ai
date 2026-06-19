"""Shared helper to write per-student GRADING.md and produce feedback text.

Used by all grader templates so Phase 5.5 can write specific feedback
(based on missing rubric items) instead of generic banded templates.

Each grader passes a `findings` dict:
  {
    "score": int,
    "rubric": [
      {"criterion": "Funcionalidad", "level": 4, "max": 4, "weight_pct": 20, "note": "Excelente"},
      ...
    ],
    "signals": {...arbitrary key/value...},
    "missing": ["criterio X (level 1)", ...],   # criteria that scored low
    "recovered_from": None | "branch:laboratorios" | "alt_folder:informe-copilot",
  }
"""
from __future__ import annotations
from pathlib import Path
import json


LEVEL_LABELS = {4: "Excelente", 3: "Bueno", 2: "Normal", 1: "Deficiente", 0: "No detectado"}


def _level_label(level: int) -> str:
    return LEVEL_LABELS.get(level, "?")


def write_grading_md(student_dir: Path, assignment_slug: str, findings: dict) -> Path:
    """Write GRADING-<slug>.md inside the student's cloned repo dir.

    Returns the path written.
    """
    name = student_dir.name
    score = findings["score"]
    recovered = findings.get("recovered_from")

    lines = [
        f"# Calificación — {name} — {assignment_slug}",
        "",
        f"**Score total: {score}/100**",
        "",
    ]
    if recovered:
        lines += [f"> Auto-recuperado desde: `{recovered}`", ""]

    # Signals block
    signals = findings.get("signals") or {}
    if signals:
        lines += ["## Signals detectados", ""]
        for k, v in signals.items():
            lines.append(f"- {k}: {v}")
        lines.append("")

    # Rubric block
    rubric = findings.get("rubric") or []
    if rubric:
        lines += [
            "## Calificación por criterio",
            "",
            "| Criterio | Nivel | Puntos | Peso | Nota |",
            "|---|---|---|---|---|",
        ]
        for r in rubric:
            lvl = r.get("level", 0)
            mx = r.get("max", 4)
            lines.append(
                f"| {r['criterion']} | {_level_label(lvl)} | {lvl}/{mx} | {r.get('weight_pct', '')}% | {r.get('note', '')} |"
            )
        lines += [f"| **TOTAL** | | | | **{score}/100** |", ""]

    # Missing items (drives Phase 5.5 feedback)
    missing = findings.get("missing") or []
    if missing:
        lines += ["## Áreas a mejorar (drive el feedback de Teams)", ""]
        for m in missing:
            lines.append(f"- {m}")
        lines.append("")

    out = student_dir / f"GRADING-{assignment_slug}.md"
    out.write_text("\n".join(lines))
    return out


def build_feedback_text(findings: dict, assignment_topic: str = "") -> str:
    """Build per-student feedback text from findings.

    Falls back to banded templates if `missing` is empty.
    Prepends recovery note if findings.recovered_from is set.
    """
    score = findings["score"]
    missing = findings.get("missing") or []
    recovered = findings.get("recovered_from")
    prefix = ""
    if recovered:
        prefix = (
            f"Investigación recuperada de `{recovered}` (recordar entregar en `main` o "
            f"como PR según la consigna). "
        )

    # Specific feedback when we know what failed
    if missing and score > 0:
        items = "; ".join(missing[:3])
        return f"{prefix}Áreas para mejorar la nota: {items}."

    # Banded fallback
    if score == 0:
        return (
            "No recibí entrega para esta asignación. Si tienes el material, "
            "envíamelo (DM/correo) y reabro la nota."
        )
    if 1 <= score <= 30:
        topic = f" ({assignment_topic})" if assignment_topic else ""
        return (
            f"{prefix}La entrega no corresponde al tema solicitado{topic}. "
            "Revisa el enunciado y entrega el documento correcto para reconsiderar la nota."
        )
    if 31 <= score <= 60:
        return (
            f"{prefix}Entrega parcial. Faltan varios criterios del rubric. "
            "Revisa la rúbrica completa para los próximos labs."
        )
    if 61 <= score <= 79:
        return (
            f"{prefix}Buen contenido pero le faltan elementos del rubric. "
            "Amplía con más evidencia (capturas/ejemplos) y revisa los criterios faltantes."
        )
    if 80 <= score <= 86:
        return (
            f"{prefix}Investigación sólida. Para nota máxima: agrega más evidencia "
            "y profundiza en las áreas evaluadas como 'Normal'."
        )
    if 87 <= score <= 89:
        return (
            f"{prefix}Muy cerca de excelente. Detalles puntuales para llegar a 100: "
            "afina los criterios que quedaron en 'Bueno' en vez de 'Excelente'."
        )
    return ""  # 90+ skips feedback per skill policy


def update_index(submissions_dir: Path, assignment_slug: str, student_scores: dict):
    """Write submissions/<slug>/INDEX.json — list of all students with their score.

    Useful for Phase 5.5 to iterate <90 students and for AUDIT.json downstream.
    """
    target = submissions_dir / assignment_slug
    target.mkdir(parents=True, exist_ok=True)
    (target / "INDEX.json").write_text(json.dumps(student_scores, indent=2))
