"""Genera los PDFs de los capítulos 2-8 del curso con el motor visual estándar.

- El contenido de cada capítulo vive en scripts/chapters_ext/cap02..cap08 (variable CHAPTER por módulo).
- Soporta el bloque ("code", "...") para fragmentos de código.
- Las tablas aceptan fracciones de ancho ([0.3, 0.7]) o usan defaults por número de columnas.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    ListFlowable,
    ListItem,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

from diagrams import DIAGRAMS

ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "materials" / "modulos"
EXT_DIR = Path(__file__).resolve().parent / "chapters_ext"

PAGE_W, PAGE_H = letter
LEFT = RIGHT = 0.78 * inch
TOP = 0.72 * inch
BOTTOM = 0.72 * inch
CONTENT_W = PAGE_W - LEFT - RIGHT

BLUE = colors.HexColor("#174A7C")
BLUE_DARK = colors.HexColor("#0E2E4F")
BLUE_LIGHT = colors.HexColor("#EAF2FA")
GRAY = colors.HexColor("#5C6773")
INK = colors.HexColor("#1F2933")


def clean(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )


class ChapterTemplate(BaseDocTemplate):
    def __init__(self, filename: str, meta: dict):
        super().__init__(
            filename,
            pagesize=letter,
            leftMargin=LEFT,
            rightMargin=RIGHT,
            topMargin=TOP,
            bottomMargin=BOTTOM,
            title=meta["title"],
        )
        self.meta = meta
        frame = Frame(LEFT, BOTTOM, CONTENT_W, PAGE_H - TOP - BOTTOM, id="normal")
        self.addPageTemplates(
            [
                PageTemplate(id="cover", frames=[frame], onPage=cover_page),
                PageTemplate(id="body", frames=[frame], onPage=body_page),
            ]
        )

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            if flowable.style.name == "H1":
                text = flowable.getPlainText()
                self.notify("TOCEntry", (0, text, self.page))
                self.canv.bookmarkPage(text)
                self.canv.addOutlineEntry(text, text, level=0, closed=False)


def cover_page(canvas, doc: ChapterTemplate):
    meta = doc.meta
    canvas.saveState()
    canvas.setFillColor(BLUE_DARK)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(LEFT, PAGE_H - 0.7 * inch, "UNIVERSIDAD TECNOLÓGICA DE PANAMÁ")
    canvas.setFont("Helvetica", 9)
    canvas.drawString(LEFT, PAGE_H - 0.9 * inch, "Facultad de Ingeniería de Sistemas Computacionales")
    canvas.setStrokeColor(colors.HexColor("#9CC8E8"))
    canvas.setLineWidth(1.2)
    canvas.line(LEFT, PAGE_H - 1.1 * inch, PAGE_W - RIGHT, PAGE_H - 1.1 * inch)

    canvas.setFont("Helvetica-Bold", 30)
    canvas.drawString(LEFT, PAGE_H - 2.1 * inch, meta["chapter_label"])
    canvas.setFont("Helvetica-Bold", 22)
    y = PAGE_H - 2.55 * inch
    for line in meta["cover_title_lines"]:
        canvas.drawString(LEFT, y, line)
        y -= 0.35 * inch

    canvas.setFillColor(colors.HexColor("#D7EAF7"))
    canvas.setFont("Helvetica", 12.5)
    canvas.drawString(LEFT, PAGE_H - 3.75 * inch, f"Desarrollo de Software IX · Código 1493 · {meta['module_label']}")

    canvas.setFillColor(colors.HexColor("#FFFFFF"))
    canvas.setStrokeColor(colors.HexColor("#5EA2D1"))
    canvas.roundRect(LEFT, 1.35 * inch, CONTENT_W, 1.85 * inch, 10, stroke=1, fill=0)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(LEFT + 0.28 * inch, 2.75 * inch, "Propósito del capítulo")
    canvas.setFont("Helvetica", 10.5)
    y = 2.48 * inch
    for line in meta["purpose_lines"]:
        canvas.drawString(LEFT + 0.28 * inch, y, line)
        y -= 0.22 * inch
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#D7EAF7"))
    canvas.drawString(LEFT, 0.74 * inch, "Material de apoyo docente · DES__SOFT_IX · 2026")
    canvas.restoreState()


def body_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D3DCE6"))
    canvas.setLineWidth(0.6)
    canvas.line(LEFT, PAGE_H - 0.48 * inch, PAGE_W - RIGHT, PAGE_H - 0.48 * inch)
    canvas.setFillColor(GRAY)
    canvas.setFont("Helvetica", 8.5)
    canvas.drawString(LEFT, PAGE_H - 0.36 * inch, f"Desarrollo de Software IX · {doc.meta['chapter_label']}")
    canvas.drawRightString(PAGE_W - RIGHT, 0.38 * inch, f"Página {doc.page}")
    canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Lead", parent=styles["BodyText"], fontName="Helvetica", fontSize=11.5, leading=16, textColor=INK, spaceAfter=10))
styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.15, leading=14.2, textColor=INK, spaceAfter=8))
styles.add(ParagraphStyle(name="H1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=BLUE, spaceBefore=16, spaceAfter=9))
styles.add(ParagraphStyle(name="H1NoTOC", parent=styles["H1"]))
styles.add(ParagraphStyle(name="H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13.2, leading=16, textColor=BLUE_DARK, spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name="CalloutTitle", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=10.2, leading=13, textColor=BLUE_DARK, spaceAfter=3))
styles.add(ParagraphStyle(name="CalloutBody", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.4, leading=12.2, textColor=INK, spaceAfter=0))
styles.add(ParagraphStyle(name="TableHead", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=colors.white, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="TableCell", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.25, leading=10.7, textColor=INK, spaceAfter=0))
styles.add(ParagraphStyle(name="Check", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.2, leading=11.8, textColor=INK, leftIndent=14, firstLineIndent=-10, spaceAfter=4))
styles.add(ParagraphStyle(name="CodeBlock", parent=styles["BodyText"], fontName="Courier", fontSize=8.6, leading=11.4, textColor=INK, backColor=colors.HexColor("#F4F6F8"), borderPadding=6, spaceAfter=8))


def p(text: str, style: str = "Body") -> Paragraph:
    return Paragraph(clean(text), styles[style])


def code(text: str) -> KeepTogether:
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>").replace(" ", "&nbsp;")
    return KeepTogether([Paragraph(escaped, styles["CodeBlock"])])


def bullet(items):
    return ListFlowable([ListItem(p(str(i)), leftIndent=12) for i in items], bulletType="bullet", start="circle", leftIndent=18, bulletFontName="Helvetica", bulletFontSize=8)


def numbered(items):
    return ListFlowable([ListItem(p(str(i)), leftIndent=14) for i in items], bulletType="1", leftIndent=18, bulletFontName="Helvetica-Bold")


def callout(title, body):
    t = Table([[p(title, "CalloutTitle")], [p(body, "CalloutBody")]], colWidths=[CONTENT_W - 8])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLUE_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#B7CCE0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


DEFAULT_FRACTIONS = {
    2: [0.32, 0.68],
    3: [0.26, 0.37, 0.37],
    4: [0.19, 0.30, 0.26, 0.25],
    5: [0.2, 0.2, 0.2, 0.2, 0.2],
}


def resolve_widths(data, spec):
    ncols = len(data[0])
    fractions = None
    if isinstance(spec, (list, tuple)) and len(spec) == ncols and all(isinstance(x, (int, float)) for x in spec):
        total = sum(spec)
        if 0.95 <= total <= 1.05:
            fractions = [x / total for x in spec]
    if fractions is None:
        fractions = DEFAULT_FRACTIONS.get(ncols, [1.0 / ncols] * ncols)
    return [f * CONTENT_W for f in fractions]


def make_table(data, widths):
    converted = []
    for r, row in enumerate(data):
        style = "TableHead" if r == 0 else "TableCell"
        converted.append([p(str(cell), style) for cell in row])
    t = Table(converted, colWidths=widths, repeatRows=1)
    commands = [
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#B8C2CC")),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D3DCE6")),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ]
    for idx in range(1, len(data)):
        if idx % 2 == 0:
            commands.append(("BACKGROUND", (0, idx), (-1, idx), colors.HexColor("#FAFBFC")))
    t.setStyle(TableStyle(commands))
    return t


def checklist(items):
    return [Paragraph("□ " + clean(str(i)), styles["Check"]) for i in items]


def add_block(story, block):
    kind = block[0]
    if kind == "h1":
        story.append(p(block[1], "H1"))
    elif kind == "h2":
        story.append(p(block[1], "H2"))
    elif kind == "p":
        story.append(p(block[1], "Body"))
    elif kind == "lead":
        story.append(p(block[1], "Lead"))
    elif kind in ("bullets", "bullet"):
        story.append(bullet(block[1]))
    elif kind in ("numbers", "number", "numbered"):
        story.append(numbered(block[1]))
    elif kind == "callout":
        story.append(callout(block[1], block[2]))
        story.append(Spacer(1, 8))
    elif kind == "table":
        spec = block[2] if len(block) > 2 else None
        story.append(make_table(block[1], resolve_widths(block[1], spec)))
        story.append(Spacer(1, 8))
    elif kind == "code":
        story.append(code(block[1]))
    elif kind == "diagram":
        story.append(KeepTogether([DIAGRAMS[block[1]]()]))
        story.append(Spacer(1, 8))
    elif kind == "checklist":
        story.extend(checklist(block[1]))
    elif kind in ("space", "spacer"):
        story.append(Spacer(1, block[1] if len(block) > 1 else 8))
    elif kind == "pagebreak":
        story.append(PageBreak())
    else:
        raise ValueError(f"Unknown block kind: {kind!r}")


def build_story(chapter):
    story = [NextPageTemplate("body"), PageBreak()]
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle(fontName="Helvetica-Bold", fontSize=10, name="TOCHeading1", leftIndent=0, firstLineIndent=0, spaceBefore=5, leading=12)]
    story += [p("Tabla de contenido", "H1NoTOC"), toc, PageBreak()]
    for block in chapter["blocks"]:
        add_block(story, block)
    return story


def load_chapter(path: Path) -> dict:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CHAPTER


def main():
    for path in sorted(EXT_DIR.glob("cap0*.py")):
        chapter = load_chapter(path)
        out = OUT_ROOT / chapter["module_dir"] / chapter["filename"]
        out.parent.mkdir(parents=True, exist_ok=True)
        doc = ChapterTemplate(str(out), chapter)
        doc.multiBuild(build_story(chapter))
        print(f"OK {len(chapter['blocks']):>3} bloques -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
