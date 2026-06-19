#!/usr/bin/env python3
"""Render UTP/FISC academic review Markdown to PDF.

Design rules:
- UTP logo top-left, FISC logo top-right on every page.
- Academic flat style, no cover page.
- Header/footer repeated with version/date/page.
- Verdict section renders as compact full-width status strip:
  - APROBADO = green
  - CAMBIOS SUGERIDOS = amber
  - DESAPROBADO = red
"""
from __future__ import annotations

import argparse
import datetime as _dt
import html
import re
import unicodedata
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    Flowable,
    PageBreak,
)

ACCENT = colors.HexColor("#0B4D8B")
ACCENT_DARK = colors.HexColor("#17324D")
GREEN = colors.HexColor("#0E7A4F")
GREEN_BG = colors.HexColor("#E8F7EF")
GREEN_BG_2 = colors.HexColor("#D7FBE8")
GREEN_HI = colors.HexColor("#BFF3D5")
GREEN_LINE = colors.HexColor("#55C98A")
TEXT = colors.HexColor("#1F2933")
MUTED = colors.HexColor("#5B6670")
LINE = colors.HexColor("#D7DEE6")
SOFT = colors.HexColor("#F5F8FB")
YELLOW = colors.HexColor("#B45309")
YELLOW_BG = colors.HexColor("#FFF7D6")
YELLOW_BG_2 = colors.HexColor("#FFE8A3")
YELLOW_HI = colors.HexColor("#FFD777")
YELLOW_LINE = colors.HexColor("#F59E0B")
RED = colors.HexColor("#B42318")
RED_BG = colors.HexColor("#FEECEC")
RED_LINE = colors.HexColor("#E35D5B")
DANGER = colors.HexColor("#B42318")


def parse_frontmatter(text: str) -> Tuple[Dict[str, str], str]:
    if text.startswith("---"):
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
        if m:
            raw = m.group(1)
            body = text[m.end():]
            if yaml:
                data = yaml.safe_load(raw) or {}
            else:
                data = {}
                for line in raw.splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        data[k.strip()] = v.strip().strip('"').strip("'")
            return {str(k): "" if v is None else str(v) for k, v in data.items()}, body
    return {}, text


def norm_text(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(ch for ch in s if not unicodedata.combining(ch))


def md_inline(s: str) -> str:
    s = html.escape(s.strip())
    s = re.sub(r"`([^`]+)`", r"<font face='Courier'>\1</font>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", s)
    s = s.replace("  ", "&nbsp;&nbsp;")
    return s


def split_table_row(line: str) -> List[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def is_table_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.match(r"^:?-{3,}:?$", c.strip()) for c in cells)


def make_styles():
    base = getSampleStyleSheet()
    styles = {}
    styles["body"] = ParagraphStyle(
        "body", parent=base["BodyText"], fontName="Helvetica", fontSize=9.4,
        leading=13.2, textColor=TEXT, spaceAfter=6
    )
    styles["small"] = ParagraphStyle(
        "small", parent=styles["body"], fontSize=8.2, leading=10.5, textColor=MUTED
    )
    styles["h1"] = ParagraphStyle(
        "h1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=16,
        leading=20, textColor=ACCENT_DARK, spaceBefore=6, spaceAfter=10
    )
    styles["h2"] = ParagraphStyle(
        "h2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=12.4,
        leading=16, textColor=ACCENT, spaceBefore=12, spaceAfter=6
    )
    styles["h3"] = ParagraphStyle(
        "h3", parent=base["Heading3"], fontName="Helvetica-Bold", fontSize=10.6,
        leading=14, textColor=ACCENT_DARK, spaceBefore=8, spaceAfter=4
    )
    styles["bullet"] = ParagraphStyle(
        "bullet", parent=styles["body"], leftIndent=14, firstLineIndent=-8, bulletIndent=0,
        spaceAfter=3
    )
    styles["number"] = ParagraphStyle(
        "number", parent=styles["body"], leftIndent=16, firstLineIndent=-12,
        spaceAfter=3
    )
    styles["number_heading"] = ParagraphStyle(
        "number_heading", parent=styles["body"], fontName="Helvetica-Bold", fontSize=10.4,
        leading=13.8, textColor=ACCENT_DARK, leftIndent=16, firstLineIndent=-12,
        spaceBefore=5, spaceAfter=4
    )
    styles["meta"] = ParagraphStyle(
        "meta", parent=styles["small"], fontSize=8.4, leading=10.8, spaceAfter=0
    )
    styles["title"] = ParagraphStyle(
        "title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=15.5,
        leading=18, textColor=ACCENT_DARK, alignment=TA_CENTER, spaceAfter=2
    )
    styles["summary_title"] = ParagraphStyle(
        "summary_title", parent=styles["body"], fontName="Helvetica-Bold", fontSize=9.2,
        leading=11.5, textColor=ACCENT_DARK, spaceBefore=0, spaceAfter=4
    )
    styles["subtitle"] = ParagraphStyle(
        "subtitle", parent=styles["small"], alignment=TA_CENTER, fontSize=8.5,
        leading=10.5, textColor=MUTED
    )
    styles["cell"] = ParagraphStyle(
        "cell", parent=styles["small"], fontSize=7.8, leading=9.4, textColor=TEXT
    )
    styles["cell_header"] = ParagraphStyle(
        "cell_header", parent=styles["cell"], fontName="Helvetica-Bold", textColor=colors.white
    )
    styles["verdict_label"] = ParagraphStyle(
        "verdict_label", parent=styles["body"], fontName="Helvetica-Bold", fontSize=12.2,
        leading=14.6, spaceAfter=0
    )
    styles["verdict_detail"] = ParagraphStyle(
        "verdict_detail", parent=styles["body"], fontSize=8.7, leading=11.0,
        textColor=TEXT, spaceAfter=0
    )
    return styles


def logo_path(skill_root: Path, name: str) -> Path | None:
    candidates = [
        skill_root / "assets" / name,
        Path.cwd() / "assets" / name,
        Path.cwd() / name,
    ]
    for p in candidates:
        if p.exists() and p.stat().st_size > 0:
            return p
    return None


def normalize_verdict_status(raw_status: str = "", detail: str = "") -> str:
    """Return 'approved', 'suggested', or 'rejected'. Defaults to rejected if uncertain."""
    raw = norm_text((raw_status or "").strip()).replace("-", "_").replace(" ", "_")
    if raw in {"approved", "aprobado", "aprobada", "ready", "listo", "lista", "listo_para_enviar", "apto", "apto_para_envio", "ok"}:
        return "approved"
    if raw in {"suggested", "cambios_sugeridos", "cambio_sugerido", "sugeridos", "sugerido", "observaciones", "ajustes_menores"}:
        return "suggested"
    if raw in {"rejected", "desaprobado", "desaprobada", "no_aprobado", "no_aprobada", "changes_required", "cambios_requeridos", "cambio_requerido", "requiere_cambios", "requiere_cambio", "no_listo"}:
        return "rejected"

    text = norm_text(f"{raw_status} {detail}")
    rejected_markers = [
        "desaprobado", "desaprobada", "no aprobado", "no aprobada",
        "riesgo de devolucion", "no listo", "no esta listo", "devolucion",
        "critico", "critica", "falta", "ausente", "debe corregir", "correcciones criticas",
        "cambios requeridos", "requiere cambios",
    ]
    suggested_markers = [
        "cambios sugeridos", "cambio sugerido", "observaciones", "correcciones menores",
        "ajustes menores", "cambios muy ligeros", "solo cambios ligeros", "aprobable con correcciones",
    ]
    approved_markers = [
        "aprobado", "aprobada", "listo para enviar", "lista para enviar",
        "apto para envio", "apto para enviar", "sin cambios", "sin correcciones",
    ]
    if any(m in text for m in rejected_markers):
        return "rejected"
    if any(m in text for m in suggested_markers):
        return "suggested"
    if any(m in text for m in approved_markers):
        return "approved"
    return "rejected"


def verdict_display(status: str):
    """Return display label + colors for compact summary table."""
    if status == "approved":
        return "APROBADO", GREEN, GREEN_BG, GREEN_LINE
    if status == "suggested":
        return "SOLICITUD DE REVISIÓN", YELLOW, YELLOW_BG, YELLOW_LINE
    return "SOLICITUD DE REVISIÓN", RED, RED_BG, RED_LINE


class VerdictCard(Flowable):
    """Compact full-width verdict strip. Direct, no ornamental clutter."""

    def __init__(self, detail: str, status: str, styles, width: float = 6.22 * inch):
        super().__init__()
        self.detail = detail.strip()
        self.status = status
        self.styles = styles
        self.req_width = width
        self.width = width
        self.height = 54
        self.detail_para = None

    def wrap(self, availWidth, availHeight):
        self.width = min(self.req_width, availWidth)
        text_w = self.width - 2.15 * inch
        fallback = {
            "approved": "Documento listo para enviar.",
            "suggested": "Documento usable, pero conviene aplicar ajustes antes de enviar.",
            "rejected": "No enviar todavía. Corregir puntos marcados abajo.",
        }.get(self.status, "No enviar todavía. Corregir puntos marcados abajo.")
        detail = self.detail or fallback
        self.detail_para = Paragraph(md_inline(detail), self.styles["verdict_detail"])
        _, detail_h = self.detail_para.wrap(text_w, max(20, availHeight))
        self.height = max(50, detail_h + 27)
        return self.width, self.height

    def _draw_gradient(self, canvas, w, h, radius, c1, c2):
        path = canvas.beginPath()
        path.roundRect(0, 0, w, h, radius)
        canvas.saveState()
        canvas.clipPath(path, stroke=0, fill=0)
        canvas.linearGradient(0, h, w, 0, (c1, c2), extend=True)
        canvas.restoreState()

    def draw(self):
        canvas = self.canv
        w, h = self.width, self.height
        if self.status == "approved":
            label, icon, strong, bg, border = "APROBADO", "✓", GREEN, GREEN_BG, GREEN_LINE
            label_hex = "#0E7A4F"
        elif self.status == "suggested":
            label, icon, strong, bg, border = "CAMBIOS SUGERIDOS", "•", YELLOW, YELLOW_BG, YELLOW_LINE
            label_hex = "#92400E"
        else:
            label, icon, strong, bg, border = "DESAPROBADO", "!", RED, RED_BG, RED_LINE
            label_hex = "#B42318"

        canvas.saveState()
        radius = 10
        self._draw_gradient(canvas, w, h, radius, bg, colors.white)
        canvas.setStrokeColor(border)
        canvas.setLineWidth(0.95)
        canvas.roundRect(0, 0, w, h, radius, stroke=1, fill=0)

        # Integrated left status rail.
        canvas.setFillColor(strong)
        rail_w = 0.11 * inch
        canvas.roundRect(0, 0, rail_w, h, radius, stroke=0, fill=1)

        # Small aligned icon.
        ix = 0.30 * inch
        iy = h / 2
        box = 0.25 * inch
        canvas.setFillColor(strong)
        canvas.roundRect(ix, iy - box / 2, box, box, 5, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 10.5)
        canvas.drawCentredString(ix + box / 2, iy - 3.4, icon)

        tx = 0.68 * inch
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica-Bold", 6.3)
        canvas.drawString(tx, h - 0.19 * inch, "ESTADO")
        title = Paragraph(f"<font color='{label_hex}'><b>{label}</b></font>", self.styles["verdict_label"])
        title.wrap(2.05 * inch, 0.28 * inch)
        title.drawOn(canvas, tx, h - 0.45 * inch)

        if self.detail_para:
            self.detail_para.drawOn(canvas, 2.55 * inch, 0.16 * inch)

        canvas.restoreState()


def verdict_card(detail: str, status: str, styles) -> VerdictCard:
    return VerdictCard(detail, status, styles)


class UTPDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, meta: Dict[str, str], skill_root: Path, page_size=letter, utp_logo_override: str | None = None, fisc_logo_override: str | None = None):
        self.meta = meta
        self.skill_root = skill_root
        self.page_size = page_size
        self.utp_logo = Path(utp_logo_override).expanduser().resolve() if utp_logo_override else logo_path(skill_root, "utp-logo.png")
        self.fisc_logo = Path(fisc_logo_override).expanduser().resolve() if fisc_logo_override else logo_path(skill_root, "fisc-logo.png")
        margin_x = 0.62 * inch
        top_margin = 1.18 * inch
        bottom_margin = 0.58 * inch
        super().__init__(
            filename,
            pagesize=page_size,
            leftMargin=margin_x,
            rightMargin=margin_x,
            topMargin=top_margin,
            bottomMargin=bottom_margin,
        )
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="normal",
            showBoundary=0,
        )
        self.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=self.draw_header_footer)])

    def draw_header_footer(self, canvas, doc):
        w, h = self.page_size
        canvas.saveState()

        y_top = h - 0.24 * inch
        logo_h = 0.55 * inch
        logo_w = 0.72 * inch

        if self.utp_logo:
            canvas.drawImage(str(self.utp_logo), self.leftMargin, h - 0.78 * inch, width=logo_w, height=logo_h, preserveAspectRatio=True, mask="auto")
        else:
            canvas.setFillColor(DANGER)
            canvas.setFont("Helvetica-Bold", 7)
            canvas.drawString(self.leftMargin, h - 0.55 * inch, "Falta logo UTP")

        if self.fisc_logo:
            canvas.drawImage(str(self.fisc_logo), w - self.rightMargin - logo_w, h - 0.78 * inch, width=logo_w, height=logo_h, preserveAspectRatio=True, mask="auto")
        else:
            canvas.setFillColor(DANGER)
            canvas.setFont("Helvetica-Bold", 7)
            canvas.drawRightString(w - self.rightMargin, h - 0.55 * inch, "Falta logo FISC")

        title = self.meta.get("title", "Revisión académica UTP/FISC")
        dtype = self.meta.get("document_type", "Documento académico")
        student = self.meta.get("student", "")
        subtitle = f"{dtype}" + (f" · {student}" if student else "")

        canvas.setFillColor(ACCENT_DARK)
        canvas.setFont("Helvetica-Bold", 9.5)
        canvas.drawCentredString(w / 2, y_top - 0.12 * inch, title[:92])
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7.3)
        canvas.drawCentredString(w / 2, y_top - 0.29 * inch, subtitle[:100])

        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.6)
        canvas.line(self.leftMargin, h - 0.91 * inch, w - self.rightMargin, h - 0.91 * inch)

        version = self.meta.get("version", "v1.0")
        date = self.meta.get("date", _dt.date.today().isoformat())
        confidentiality = self.meta.get("confidentiality", "Uso académico interno")
        footer = f"{confidentiality} · {version} · {date}"
        canvas.setStrokeColor(LINE)
        canvas.line(self.leftMargin, 0.42 * inch, w - self.rightMargin, 0.42 * inch)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7.2)
        canvas.drawString(self.leftMargin, 0.25 * inch, footer[:120])
        canvas.drawRightString(w - self.rightMargin, 0.25 * inch, f"Página {doc.page}")
        canvas.restoreState()


def meta_block(meta: Dict[str, str], styles) -> Table:
    rows = []
    fields = [
        ("Estudiante", meta.get("student", "")),
        ("Documento", meta.get("document_type", "")),
        ("Modalidad", meta.get("modality", "")),
        ("Carrera", meta.get("career", "")),
        ("Proyecto", meta.get("project", "")),
        ("Revisor", meta.get("reviewer", "Erick Vicente Agrazal Lopez")),
    ]
    for k, v in fields:
        if v:
            rows.append([
                Paragraph(f"<b>{md_inline(k)}</b>", styles["meta"]),
                Paragraph(md_inline(v), styles["meta"]),
            ])
    if not rows:
        return Table([[""]])
    tbl = Table(rows, colWidths=[1.12 * inch, 5.05 * inch], hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#E6ECF2")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return tbl


def review_summary_table(meta: Dict[str, str], styles) -> Table:
    """Small top table with thesis/document, submitter, version, and status."""
    status = normalize_verdict_status(meta.get("verdict_status", ""), meta.get("verdict_detail", ""))
    label, strong, fill, border = verdict_display(status)
    doc_name = (
        meta.get("thesis_document")
        or meta.get("source_document")
        or meta.get("document_name")
        or meta.get("project")
        or meta.get("title", "Documento revisado")
    )
    delivered_by = meta.get("submitted_by") or meta.get("student", "")
    version = meta.get("version", "v1.0")
    header_style = styles["cell_header"]
    value_style = styles["cell"]
    status_style = ParagraphStyle(
        "status_value", parent=styles["cell"], fontName="Helvetica-Bold", fontSize=6.7,
        leading=8.2, textColor=strong, alignment=TA_CENTER
    )
    data = [
        [
            Paragraph("Documento / tesis", header_style),
            Paragraph("Entregado por", header_style),
            Paragraph("Versión", header_style),
            Paragraph("Estado", header_style),
        ],
        [
            Paragraph(md_inline(doc_name), value_style),
            Paragraph(md_inline(delivered_by), value_style),
            Paragraph(md_inline(version), value_style),
            Paragraph(md_inline(label), status_style),
        ],
    ]
    tbl = Table(data, colWidths=[3.95 * inch, 1.10 * inch, 0.55 * inch, 1.66 * inch], hAlign="LEFT", repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT_DARK),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return tbl


def render_table(lines: List[str], styles) -> Table:
    rows = []
    for ln in lines:
        if is_table_separator(ln):
            continue
        rows.append(split_table_row(ln))
    if not rows:
        return Table([[""]])
    max_cols = max(len(r) for r in rows)
    for r in rows:
        while len(r) < max_cols:
            r.append("")
    data = []
    for ri, row in enumerate(rows):
        sty = styles["cell_header"] if ri == 0 else styles["cell"]
        data.append([Paragraph(md_inline(c), sty) for c in row])
    usable = 6.22 * inch
    if max_cols == 3:
        colw = [1.28 * inch, 0.92 * inch, usable - 2.20 * inch]
    elif max_cols == 2:
        colw = [1.65 * inch, usable - 1.65 * inch]
    else:
        colw = [usable / max_cols] * max_cols
    tbl = Table(data, colWidths=colw, hAlign="LEFT", repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAFCFE")]),
    ]))
    return tbl


def build_story(body: str, meta: Dict[str, str], styles) -> List:
    story: List = []
    if str(meta.get("show_body_title", "false")).lower() in {"1", "true", "yes", "si", "sí"}:
        story.append(Paragraph(md_inline(meta.get("title", "Revisión académica UTP/FISC")), styles["title"]))
        subtitle_bits = [meta.get("document_type", ""), meta.get("student", ""), meta.get("version", "v1.0")]
        story.append(Paragraph(md_inline(" · ".join([b for b in subtitle_bits if b])), styles["subtitle"]))
        story.append(Spacer(1, 8))
    else:
        story.append(Spacer(1, 3))
    show_summary_table = str(meta.get("show_summary_table", "true")).lower() not in {"0", "false", "no"}
    if show_summary_table:
        story.append(Paragraph("Resumen de revisión", styles["summary_title"]))
        story.append(review_summary_table(meta, styles))
        story.append(Spacer(1, 10))
    elif str(meta.get("show_metadata", "false")).lower() in {"1", "true", "yes", "si", "sí"}:
        story.append(meta_block(meta, styles))
        story.append(Spacer(1, 10))

    body_has_verdict = bool(re.search(r"^##\s+Veredicto\b", body, re.I | re.M))
    if (not show_summary_table) and (not body_has_verdict) and (meta.get("verdict_status") or meta.get("verdict") or meta.get("verdict_detail")):
        detail = meta.get("verdict_detail") or meta.get("verdict") or ""
        status = normalize_verdict_status(meta.get("verdict_status", ""), detail)
        story.append(verdict_card(detail, status, styles))
        story.append(Spacer(1, 10))

    lines = body.splitlines()
    i = 0
    para_buf: List[str] = []

    def flush_para():
        nonlocal para_buf
        if para_buf:
            txt = " ".join(x.strip() for x in para_buf if x.strip())
            if txt:
                story.append(Paragraph(md_inline(txt), styles["body"]))
            para_buf = []

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        if not stripped:
            flush_para()
            story.append(Spacer(1, 2))
            i += 1
            continue

        if stripped in {"<!-- pagebreak -->", "\\f"}:
            flush_para()
            story.append(PageBreak())
            i += 1
            continue

        if stripped.startswith("```"):
            flush_para()
            fence = stripped[3:].strip()
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1
            if fence == "signoff":
                story.append(HRFlowable(width="100%", thickness=0.5, color=LINE, spaceBefore=8, spaceAfter=8))
                story.append(Paragraph("Revisión preparada por", styles["h3"]))
                story.append(Paragraph(md_inline(meta.get("reviewer", "Erick Vicente Agrazal Lopez")), styles["body"]))
            else:
                story.append(Paragraph("<font face='Courier'>" + html.escape("\n".join(block)).replace("\n", "<br/>") + "</font>", styles["small"]))
            continue

        if stripped.startswith("# "):
            flush_para()
            title_text = stripped[2:].strip()
            if title_text.lower() != meta.get("title", "").lower():
                story.append(Paragraph(md_inline(title_text), styles["h1"]))
            i += 1
            continue

        if stripped.startswith("## ") and norm_text(stripped[3:]).startswith("veredicto"):
            flush_para()
            i += 1
            block: List[str] = []
            while i < len(lines) and not re.match(r"^#{1,3}\s+", lines[i].strip()):
                if lines[i].strip():
                    block.append(lines[i].strip())
                i += 1
            if not show_summary_table:
                detail = " ".join(block).strip() or meta.get("verdict_detail", "") or meta.get("verdict", "")
                status = normalize_verdict_status(meta.get("verdict_status", ""), detail)
                story.append(verdict_card(detail, status, styles))
                story.append(Spacer(1, 10))
            continue

        if stripped.startswith("## "):
            flush_para()
            story.append(Paragraph(md_inline(stripped[3:]), styles["h2"]))
            i += 1
            continue
        if stripped.startswith("### "):
            flush_para()
            story.append(Paragraph(md_inline(stripped[4:]), styles["h3"]))
            i += 1
            continue

        if stripped == "---":
            flush_para()
            story.append(HRFlowable(width="100%", thickness=0.6, color=LINE, spaceBefore=6, spaceAfter=8))
            i += 1
            continue

        if stripped.startswith("|") and "|" in stripped[1:]:
            flush_para()
            tbl_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tbl_lines.append(lines[i].strip())
                i += 1
            story.append(render_table(tbl_lines, styles))
            story.append(Spacer(1, 8))
            continue

        m_bullet = re.match(r"^[-*]\s+(.*)", stripped)
        if m_bullet:
            flush_para()
            story.append(Paragraph("• " + md_inline(m_bullet.group(1)), styles["bullet"]))
            i += 1
            continue

        m_num = re.match(r"^(\d+)\.\s+(.*)", stripped)
        if m_num:
            flush_para()
            story.append(Paragraph(f"{m_num.group(1)}. " + md_inline(m_num.group(2)), styles["number_heading"]))
            i += 1
            continue

        m_field = re.match(r"^(Problema|Riesgo|Correcci[oó]n|Texto sugerido|Documento revisado|Prioridad):\s*(.*)", stripped, re.I)
        if m_field:
            flush_para()
            label, rest = m_field.group(1), m_field.group(2)
            story.append(Paragraph(f"<b>{md_inline(label)}:</b> {md_inline(rest)}", styles["body"]))
            i += 1
            continue

        para_buf.append(line)
        i += 1

    flush_para()
    return story


def main() -> int:
    ap = argparse.ArgumentParser(description="Render UTP/FISC review Markdown to PDF")
    ap.add_argument("source_md")
    ap.add_argument("output_pdf")
    ap.add_argument("--utp-logo", default=None)
    ap.add_argument("--fisc-logo", default=None)
    args = ap.parse_args()

    src = Path(args.source_md).expanduser().resolve()
    out = Path(args.output_pdf).expanduser().resolve()
    skill_root = Path(__file__).resolve().parents[1]

    if args.utp_logo and not Path(args.utp_logo).expanduser().exists():
        raise SystemExit(f"UTP logo not found: {args.utp_logo}")
    if args.fisc_logo and not Path(args.fisc_logo).expanduser().exists():
        raise SystemExit(f"FISC logo not found: {args.fisc_logo}")
    if not src.exists():
        raise SystemExit(f"source not found: {src}")

    text = src.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    meta.setdefault("reviewer", "Erick Vicente Agrazal Lopez")
    meta.setdefault("version", "v1.0")
    meta.setdefault("date", _dt.date.today().isoformat())
    meta.setdefault("confidentiality", "Uso académico interno")
    meta.setdefault("title", "Revisión académica UTP/FISC")

    page_size = A4 if meta.get("page_size", "letter").lower() == "a4" else letter
    styles = make_styles()
    story = build_story(body, meta, styles)

    out.parent.mkdir(parents=True, exist_ok=True)
    doc = UTPDocTemplate(str(out), meta=meta, skill_root=skill_root, page_size=page_size, utp_logo_override=args.utp_logo, fisc_logo_override=args.fisc_logo)
    doc.build(story)

    if not out.exists() or out.stat().st_size <= 0:
        raise SystemExit("PDF render failed: output missing or empty")
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
