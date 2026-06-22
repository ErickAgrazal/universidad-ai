#!/usr/bin/env python3
"""
build_assignments_pdf.py — Renderiza ASSIGNMENTS.md (catálogo de asignaciones)
a un PDF versionado.

Uso (desde cualquier cwd):
    uv run --with markdown --with xhtml2pdf --with pillow \
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
REPO_ROOT = ROOT.parents[2]                          # .../universidad
SRC = ROOT / "ASSIGNMENTS.md"
OUT_DIR = ROOT / "materials" / "assignments_pdf"
FONT_DIR = OUT_DIR / "_fonts"
ASSETS_DIR = OUT_DIR / "_assets"
VERSIONS_LOG = OUT_DIR / "VERSIONS.md"

# Logos institucionales oficiales (reutilizados del skill utp-fisc-review-pdf)
LOGO_UTP = REPO_ROOT / ".claude/skills/utp-fisc-review-pdf/assets/utp-logo.png"
LOGO_FISC = REPO_ROOT / ".claude/skills/utp-fisc-review-pdf/assets/fisc-logo.png"

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


def prepare_logos():
    """Genera versiones redimensionadas (RGBA) de los logos UTP/FISC."""
    from PIL import Image  # noqa: PLC0415

    if not LOGO_UTP.is_file() or not LOGO_FISC.is_file():
        sys.exit(
            "No se encontraron los logos UTP/FISC en "
            ".claude/skills/utp-fisc-review-pdf/assets/ (utp-logo.png, fisc-logo.png)."
        )
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    specs = [
        ("utp_cover", LOGO_UTP, 360),
        ("fisc_cover", LOGO_FISC, 360),
        ("utp_head", LOGO_UTP, 150),
        ("fisc_head", LOGO_FISC, 150),
    ]
    out = {}
    for key, src, h in specs:
        im = Image.open(src).convert("RGBA")
        w = max(1, round(im.width * h / im.height))
        im = im.resize((w, h), Image.LANCZOS)
        dst = ASSETS_DIR / f"{key}.png"
        im.save(dst)
        out[key] = dst.as_posix()
    # aspect ratios (ancho/alto) del original, para no deformar al fijar tamaño
    with Image.open(LOGO_UTP) as u:
        out["utp_ar"] = u.width / u.height
    with Image.open(LOGO_FISC) as fi:
        out["fisc_ar"] = fi.width / fi.height
    return out


def next_version():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    mx = 0
    for p in OUT_DIR.glob("ASSIGNMENTS_v*.pdf"):
        m = re.match(r"ASSIGNMENTS_v(\d+)_", p.name)
        if m:
            mx = max(mx, int(m.group(1)))
    return mx + 1


CSS_TMPL = """
/* Portada: SIN encabezado institucional (solo el lockup grande de logos) */
@page cover {{ size: a4 landscape; margin: 1.3cm 1.3cm 1.35cm 1.3cm;
  @frame footer {{ -pdf-frame-content: footerContent; bottom: 0.55cm; margin-left: 1.3cm; margin-right: 1.3cm; height: 0.6cm; }} }}
/* Páginas de contenido: encabezado (membrete) + footer (área de contenido derivada del margen) */
@page main {{ size: a4 landscape; margin: 2.4cm 1.3cm 1.35cm 1.3cm;
  @frame header {{ -pdf-frame-content: headerContent; top: 0.4cm; margin-left: 1.3cm; margin-right: 1.3cm; height: 1.7cm; }}
  @frame footer {{ -pdf-frame-content: footerContent; bottom: 0.55cm; margin-left: 1.3cm; margin-right: 1.3cm; height: 0.6cm; }} }}
@font-face {{ font-family: "AUni"; src: url("{reg}"); }}
@font-face {{ font-family: "AUni"; src: url("{bold}"); font-weight: bold; }}
body {{ font-family: "AUni"; font-size: 8.6pt; line-height: 1.35; color: #1a1a1a; }}
h1 {{ font-size: 19pt; color: #0b3d66; margin: 0 0 4pt 0; }}
h2 {{ font-size: 13pt; color: #0b3d66; page-break-before: always; border-bottom: 1.2pt solid #0b3d66; padding-bottom: 2pt; margin: 0 0 6pt 0; -pdf-outline: true; -pdf-outline-level: 0; -pdf-outline-open: false; }}
h2.first {{ page-break-before: avoid; }}
h3 {{ font-size: 10.5pt; color: #16608a; margin: 9pt 0 3pt 0; -pdf-outline: true; -pdf-outline-level: 1; -pdf-outline-open: false; }}
a {{ color: #0b3d66; text-decoration: none; }}
/* Portada */
.cover {{ }}
.cover-band {{ background: #0b3d66; color: #ffffff; padding: 34pt 30pt; margin-top: 60pt; }}
.cover-band h1 {{ color: #ffffff; font-size: 30pt; margin: 0; }}
.cover-band .sub {{ color: #cfe0ef; font-size: 13pt; margin-top: 8pt; }}
.cover-meta {{ margin: 26pt 30pt 0 30pt; font-size: 11pt; color: #1a1a1a; }}
.cover-meta .v {{ color: #137333; font-weight: bold; }}
.cover-toc {{ margin: 18pt 30pt 0 30pt; font-size: 9pt; color: #555; }}
.cover-logos {{ text-align: center; margin: 6pt 0 14pt 0; }}
/* Encabezado institucional (letterhead) repetido en cada página */
.plain {{ width: 100%; }}
.plain td {{ border: none; background: none; padding: 1pt 0; vertical-align: middle; }}
.hdr-center {{ text-align: center; font-size: 7.6pt; color: #0b3d66; line-height: 1.25; }}
.hdr-center b {{ font-size: 8pt; }}
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

    # Anclas/ids en cada sección "## A{N}" -> navegación (bookmarks) + índice clicable
    def _slug(num):
        return "sec-a" + num.replace(".", "_")

    def _h2_anchor(m):
        num = m.group(1)
        inner = m.group(0)[len("<h2>"):-len("</h2>")]
        sid = _slug(num)
        return f'<a name="{sid}"></a><h2 id="{sid}">{inner}</h2>'

    html_body = re.sub(r"<h2>A(\d+(?:\.\d+)?)\b[^<]*</h2>", _h2_anchor, html_body)

    # Índice: 1ª celda (A1, A11.1, ...) -> enlace clicable a su sección
    html_body = re.sub(
        r"<td>(A(\d+(?:\.\d+)?))</td>",
        lambda m: f'<td><a href="#{_slug(m.group(2))}">{m.group(1)}</a></td>',
        html_body,
    )

    # Extraer H1 + blockquote inicial para la portada y quitarlos del cuerpo
    cover_title = "Catálogo de Asignaciones — SEMI 2026 (DS_IX)"
    m_h1 = re.search(r"<h1>(.*?)</h1>", html_body, re.S)
    if m_h1:
        cover_title = re.sub(r"<[^>]+>", "", m_h1.group(1)).strip()
    html_body = re.sub(r"^\s*<h1>.*?</h1>\s*", "", html_body, count=1, flags=re.S)
    html_body = re.sub(
        r"^\s*<blockquote>.*?</blockquote>\s*", "", html_body, count=1, flags=re.S
    )
    # primer h2 (Índice) sin salto de página previo (va tras la portada)
    html_body = html_body.replace("<h2>", '<h2 class="first">', 1)

    css = CSS_TMPL.format(reg=reg_dst.as_posix(), bold=bold_dst.as_posix())
    ver = next_version()
    today = _dt.date.today().isoformat()
    stamp = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    logos = prepare_logos()
    footer = (
        f'<div id="footerContent" style="font-size:7pt;color:#888;">'
        f'Catálogo de Asignaciones — SEMI 2026 (DS_IX) · v{ver:03d} · {today} · '
        f'<pdf:pagenumber> / <pdf:pagecount></div>'
    )
    uh_w, fh_w = 26 * logos["utp_ar"], 26 * logos["fisc_ar"]
    uc_w, fc_w = 96 * logos["utp_ar"], 96 * logos["fisc_ar"]
    header = (
        '<div id="headerContent"><table class="plain"><tr>'
        f'<td style="width:90pt;"><img src="{logos["utp_head"]}" '
        f'style="width:{uh_w:.1f}pt; height:26pt;" /></td>'
        '<td class="hdr-center"><b>Universidad Tecnológica de Panamá</b><br/>'
        "Facultad de Ingeniería de Sistemas Computacionales (FISC) · DES__SOFT_IX</td>"
        f'<td style="width:90pt; text-align:right;"><img src="{logos["fisc_head"]}" '
        f'style="width:{fh_w:.1f}pt; height:26pt;" /></td>'
        "</tr></table></div>"
    )
    cover = (
        '<div class="cover">'
        '<div class="cover-logos">'
        f'<img src="{logos["utp_cover"]}" style="width:{uc_w:.1f}pt; height:96pt;" />'
        f'<img src="{logos["fisc_cover"]}" '
        f'style="width:{fc_w:.1f}pt; height:96pt; margin-left:60pt;" />'
        "</div>"
        '<div class="cover-band">'
        f"<h1>{cover_title}</h1>"
        '<div class="sub">Curso DES__SOFT_IX · 1GS241 + 1GS242</div>'
        "</div>"
        '<div class="cover-meta">'
        f'Versión <span class="v">v{ver:03d}</span> · {today}<br/>'
        "Catálogo de las asignaciones colocadas a los estudiantes — metadata, "
        "instrucciones/contenido y rúbricas (A1–A16).<br/>"
        "Fuente de verdad de lo que ven los estudiantes: Microsoft Teams."
        "</div>"
        '<div class="cover-toc">Generado desde ASSIGNMENTS.md con '
        "scripts/build_assignments_pdf.py — navegación por marcadores (bookmarks) "
        "e índice clicable (toca el código AN en la tabla).</div>"
        "</div>"
    )
    # La portada usa la plantilla @page cover (sin header); tras ella se cambia
    # a @page main (con membrete) para todo el resto del documento.
    html = (
        f'<html><head><meta charset="utf-8"><style>{css}</style></head>'
        f"<body>{footer}{header}{cover}"
        '<pdf:nexttemplate name="main" /><pdf:nextpage />'
        f"{html_body}</body></html>"
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
