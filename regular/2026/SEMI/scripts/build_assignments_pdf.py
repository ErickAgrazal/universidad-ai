#!/usr/bin/env python3
"""
build_assignments_pdf.py — Renderiza ASSIGNMENTS.md (catálogo de asignaciones)
a un PDF versionado.

Uso (desde cualquier cwd):
    uv run --with markdown --with xhtml2pdf \
        regular/2026/SEMI/scripts/build_assignments_pdf.py --note "agregada A13"

- Fuente:  SEMI/ASSIGNMENTS.md
- Salida:  SEMI/materials/assignments_pdf/ASSIGNMENTS_v{NNN}_{YYYY-MM-DD}.pdf
           + copia ASSIGNMENTS_latest.pdf
- Versionado: numera automáticamente (vNNN = max existente + 1). Cada corrida
  genera un PDF nuevo (no sobrescribe los anteriores) y registra la versión en
  materials/assignments_pdf/VERSIONS.md (este sí se versiona en git; los PDF no).

REGLA OPERATIVA: cada vez que se agregue una asignación o se modifique alguna
(instrucciones/rúbrica/fechas), primero actualizar ASSIGNMENTS.md y luego
re-correr este script para emitir una nueva versión del PDF.
"""
import argparse
import datetime as _dt
import re
import shutil
import sys
from pathlib import Path

import markdown  # type: ignore
from xhtml2pdf import pisa  # type: ignore

ROOT = Path(__file__).resolve().parents[1]          # .../SEMI
SRC = ROOT / "ASSIGNMENTS.md"
OUT_DIR = ROOT / "materials" / "assignments_pdf"
FONT_DIR = OUT_DIR / "_fonts"
VERSIONS_LOG = OUT_DIR / "VERSIONS.md"

# Fuentes Unicode candidatas (macOS). Primera que exista gana.
FONT_CANDIDATES_REGULAR = [
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]
FONT_CANDIDATES_BOLD = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
]


def _first_existing(paths):
    for p in paths:
        if Path(p).is_file():
            return Path(p)
    return None


def prepare_fonts():
    """Copia las fuentes a nombres sin espacios para que @font-face no falle."""
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    reg = _first_existing(FONT_CANDIDATES_REGULAR)
    if reg is None:
        sys.exit("No se encontró una fuente Unicode (Arial Unicode/Arial).")
    bold = _first_existing(FONT_CANDIDATES_BOLD) or reg
    reg_dst = FONT_DIR / "uni.ttf"
    bold_dst = FONT_DIR / "uni-bold.ttf"
    shutil.copyfile(reg, reg_dst)
    shutil.copyfile(bold, bold_dst)
    return reg_dst, bold_dst


def next_version():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    mx = 0
    for p in OUT_DIR.glob("ASSIGNMENTS_v*.pdf"):
        m = re.match(r"ASSIGNMENTS_v(\d+)_", p.name)
        if m:
            mx = max(mx, int(m.group(1)))
    return mx + 1


CSS_TMPL = """
@page {{ size: a4 landscape; margin: 1.4cm 1.3cm; @frame footer {{ -pdf-frame-content: footerContent; bottom: 0.6cm; margin-left: 1.3cm; margin-right: 1.3cm; height: 0.6cm; }} }}
@font-face {{ font-family: "AUni"; src: url("{reg}"); }}
@font-face {{ font-family: "AUni"; src: url("{bold}"); font-weight: bold; }}
body {{ font-family: "AUni"; font-size: 8.6pt; line-height: 1.35; color: #1a1a1a; }}
h1 {{ font-size: 19pt; color: #0b3d66; margin: 0 0 4pt 0; }}
h2 {{ font-size: 13pt; color: #0b3d66; page-break-before: always; border-bottom: 1.2pt solid #0b3d66; padding-bottom: 2pt; margin: 0 0 6pt 0; }}
h2.first {{ page-break-before: avoid; }}
h3 {{ font-size: 10.5pt; color: #16608a; margin: 9pt 0 3pt 0; }}
p {{ margin: 3pt 0; }}
ul, ol {{ margin: 3pt 0 3pt 14pt; }}
li {{ margin: 1.5pt 0; }}
blockquote {{ background: #eef4fa; border-left: 3pt solid #16608a; margin: 4pt 0; padding: 3pt 7pt; color: #324; }}
code {{ font-family: "Courier"; background: #f0f0f0; font-size: 8pt; }}
pre {{ background: #f5f5f5; padding: 5pt; font-size: 7.6pt; }}
table {{ width: 100%; border-collapse: collapse; margin: 5pt 0; }}
th {{ background: #0b3d66; color: #ffffff; font-weight: bold; font-size: 7.8pt; padding: 4pt; border: 0.5pt solid #0b3d66; text-align: left; vertical-align: top; }}
td {{ font-size: 7.8pt; padding: 4pt; border: 0.5pt solid #b9c6d2; vertical-align: top; }}
tr:nth-child(even) td {{ background: #f4f8fb; }}
.chk {{ color: #137333; font-family: "AUni"; font-size: 9.5pt; }}
"""


def render():
    if not SRC.is_file():
        sys.exit(f"No existe la fuente {SRC}")
    reg_dst, bold_dst = prepare_fonts()
    md_text = SRC.read_text(encoding="utf-8")

    html_body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists", "attr_list"],
    )
    # marca de respuesta correcta: emoji ✅ -> check verde con glifo Unicode estándar
    html_body = html_body.replace("✅", '<span class="chk">✓</span>')
    # primer h2 (Índice) sin salto de página previo
    html_body = html_body.replace("<h2>", '<h2 class="first">', 1)

    css = CSS_TMPL.format(reg=reg_dst.as_posix(), bold=bold_dst.as_posix())
    ver = next_version()
    today = _dt.date.today().isoformat()
    stamp = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    footer = (
        f'<div id="footerContent" style="font-size:7pt;color:#888;">'
        f'Catálogo de Asignaciones — SEMI 2026 (DS_IX) · v{ver:03d} · {today} · '
        f'<pdf:pagenumber> / <pdf:pagecount></div>'
    )
    html = (
        f'<html><head><meta charset="utf-8"><style>{css}</style></head>'
        f"<body>{footer}{html_body}</body></html>"
    )

    out_pdf = OUT_DIR / f"ASSIGNMENTS_v{ver:03d}_{today}.pdf"
    with open(out_pdf, "wb") as fh:
        result = pisa.CreatePDF(html, dest=fh, encoding="utf-8")
    if result.err:
        sys.exit(f"Error de xhtml2pdf al renderizar ({result.err} errores).")

    latest = OUT_DIR / "ASSIGNMENTS_latest.pdf"
    shutil.copyfile(out_pdf, latest)

    note = ARGS.note or "(sin nota)"
    line = f"- v{ver:03d} — {stamp} — {out_pdf.name} — {note}\n"
    if not VERSIONS_LOG.exists():
        VERSIONS_LOG.write_text(
            "# Versiones del PDF del catálogo de asignaciones\n\n"
            "Cada línea = una emisión del PDF (`ASSIGNMENTS_vNNN_fecha.pdf`). "
            "Los PDF en esta carpeta están gitignored (binarios); este registro y "
            "`scripts/build_assignments_pdf.py` sí se versionan. Regenerar con:\n"
            "`uv run --with markdown --with xhtml2pdf "
            "regular/2026/SEMI/scripts/build_assignments_pdf.py --note \"...\"`\n\n",
            encoding="utf-8",
        )
    with open(VERSIONS_LOG, "a", encoding="utf-8") as fh:
        fh.write(line)

    size_kb = out_pdf.stat().st_size / 1024
    print(f"OK  v{ver:03d}  {out_pdf}  ({size_kb:.0f} KB)")
    print(f"    latest -> {latest}")
    print(f"    log    -> {VERSIONS_LOG}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--note", default="", help="Nota de la versión (qué cambió)")
    ARGS = ap.parse_args()
    render()
