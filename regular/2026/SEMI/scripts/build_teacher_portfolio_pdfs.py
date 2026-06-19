# -*- coding: utf-8 -*-
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
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


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "materials" / "portafolio_docente"
CSV_PATH = (
    ROOT
    / "submissions"
    / "notas_actuales_2026-05-24-eric-marin-michael-portela"
    / "notas_hasta_ahora_2026-05-24_eric-marin-michael-portela.csv"
)

PAGE_W, PAGE_H = letter
LEFT = RIGHT = 0.72 * inch
TOP = 0.72 * inch
BOTTOM = 0.72 * inch
CONTENT_W = PAGE_W - LEFT - RIGHT

NAVY = colors.HexColor("#0E2E4F")
BLUE = colors.HexColor("#174A7C")
BLUE_2 = colors.HexColor("#2F6F9F")
BLUE_LIGHT = colors.HexColor("#EAF2FA")
INK = colors.HexColor("#1F2933")
GRAY = colors.HexColor("#5C6773")
GRAY_LIGHT = colors.HexColor("#F5F7FA")
GREEN_LIGHT = colors.HexColor("#EAF7EF")
GOLD_LIGHT = colors.HexColor("#FFF6DC")
RED_LIGHT = colors.HexColor("#FDECEC")


def esc(text: object) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverKicker", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=colors.white, spaceAfter=6))
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=25, leading=30, textColor=colors.white, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="CoverSubtitle", parent=styles["BodyText"], fontName="Helvetica", fontSize=11.5, leading=15, textColor=colors.HexColor("#DDEBF7")))
styles.add(ParagraphStyle(name="H1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=BLUE, spaceBefore=14, spaceAfter=8))
styles.add(ParagraphStyle(name="H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12.5, leading=15.5, textColor=NAVY, spaceBefore=10, spaceAfter=5))
styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.7, leading=13.4, textColor=INK, spaceAfter=7))
styles.add(ParagraphStyle(name="Lead", parent=styles["Body"], fontSize=11.0, leading=15.0, spaceAfter=10))
styles.add(ParagraphStyle(name="Small", parent=styles["Body"], fontSize=8.2, leading=10.5, textColor=GRAY, spaceAfter=4))
styles.add(ParagraphStyle(name="TableHead", parent=styles["Body"], fontName="Helvetica-Bold", fontSize=7.8, leading=9.7, textColor=colors.white, alignment=TA_LEFT, spaceAfter=0))
styles.add(ParagraphStyle(name="TableCell", parent=styles["Body"], fontSize=7.6, leading=9.7, spaceAfter=0))
styles.add(ParagraphStyle(name="CalloutTitle", parent=styles["Body"], fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=NAVY, spaceAfter=2))
styles.add(ParagraphStyle(name="CalloutBody", parent=styles["Body"], fontSize=8.8, leading=11.4, spaceAfter=0))
styles.add(ParagraphStyle(name="CenterSmall", parent=styles["Small"], alignment=TA_CENTER))


class PortfolioDoc(BaseDocTemplate):
    def __init__(self, filename: Path, title: str, code: str):
        super().__init__(
            str(filename),
            pagesize=letter,
            leftMargin=LEFT,
            rightMargin=RIGHT,
            topMargin=TOP,
            bottomMargin=BOTTOM,
            title=title,
            author="Erick Agrazal",
            subject="Portafolio docente Desarrollo de Software IX",
        )
        self.doc_title = title
        self.doc_code = code
        frame = Frame(LEFT, BOTTOM, CONTENT_W, PAGE_H - TOP - BOTTOM, id="normal")
        self.addPageTemplates(
            [
                PageTemplate(id="cover", frames=[frame], onPage=self.cover_page),
                PageTemplate(id="body", frames=[frame], onPage=self.body_page),
            ]
        )

    def cover_page(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 10)
        canvas.drawString(LEFT, PAGE_H - 0.66 * inch, "UNIVERSIDAD TECNOLÓGICA DE PANAMÁ")
        canvas.setFont("Helvetica", 9)
        canvas.drawString(LEFT, PAGE_H - 0.86 * inch, "Facultad de Ingeniería de Sistemas Computacionales · Departamento de Programación de Computadoras")
        canvas.setStrokeColor(colors.HexColor("#9CC8E8"))
        canvas.line(LEFT, PAGE_H - 1.08 * inch, PAGE_W - RIGHT, PAGE_H - 1.08 * inch)

        y = PAGE_H - 1.72 * inch
        canvas.setFont("Helvetica-Bold", 13)
        canvas.drawString(LEFT, y, self.doc_code)
        y -= 0.44 * inch
        canvas.setFont("Helvetica-Bold", 25)
        for line in split_title(self.doc_title, 32):
            canvas.drawString(LEFT, y, line)
            y -= 0.36 * inch

        canvas.setFillColor(colors.HexColor("#DDEBF7"))
        canvas.setFont("Helvetica", 11)
        canvas.drawString(LEFT, y - 0.12 * inch, "Portafolio docente · Desarrollo de Software IX · Código 1493 · I Semestre 2026")

        canvas.setStrokeColor(colors.HexColor("#5EA2D1"))
        canvas.roundRect(LEFT, 1.18 * inch, CONTENT_W, 1.62 * inch, 9, stroke=1, fill=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 10.5)
        canvas.drawString(LEFT + 0.25 * inch, 2.43 * inch, "Contenido")
        canvas.setFont("Helvetica", 9.7)
        for idx, line in enumerate(
            [
                "Curso DES__SOFT_IX: 11 asignaciones (A1-A11), 9 capítulos teóricos, guía de estudio y 2 módulos extra.",
                "Precalificación mid-term cargada en matrícula (corte 24-may-2026); semestral y portafolio pendientes.",
                "Documento generado desde el workspace del curso. Actualizado al 12 de junio de 2026.",
            ]
        ):
            canvas.drawString(LEFT + 0.25 * inch, 2.18 * inch - idx * 0.22 * inch, line)
        canvas.setFillColor(colors.HexColor("#DDEBF7"))
        canvas.setFont("Helvetica", 8.6)
        canvas.drawString(LEFT, 0.62 * inch, "DES__SOFT_IX_1GS241_2026 · DES__SOFT_IX_1GS242_2026")
        canvas.restoreState()

    def body_page(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D3DCE6"))
        canvas.line(LEFT, PAGE_H - 0.48 * inch, PAGE_W - RIGHT, PAGE_H - 0.48 * inch)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(GRAY)
        canvas.drawString(LEFT, PAGE_H - 0.36 * inch, f"Portafolio docente DS IX · {self.doc_code}")
        canvas.drawRightString(PAGE_W - RIGHT, 0.36 * inch, f"Página {doc.page}")
        canvas.restoreState()


def split_title(title: str, max_len: int) -> list[str]:
    words = title.split()
    lines: list[str] = []
    cur: list[str] = []
    for word in words:
        if len(" ".join(cur + [word])) > max_len and cur:
            lines.append(" ".join(cur))
            cur = [word]
        else:
            cur.append(word)
    if cur:
        lines.append(" ".join(cur))
    return lines


def p(text: object, style: str = "Body") -> Paragraph:
    return Paragraph(esc(text), styles[style])


def h1(text: str) -> Paragraph:
    return p(text, "H1")


def h2(text: str) -> Paragraph:
    return p(text, "H2")


def bullets(items: list[str]) -> ListFlowable:
    return ListFlowable(
        [ListItem(p(item), leftIndent=12) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=16,
        bulletFontName="Helvetica",
        bulletFontSize=7,
    )


def table(data: list[list[object]], widths: list[float], header: bool = True) -> Table:
    converted = []
    for r, row in enumerate(data):
        style = "TableHead" if header and r == 0 else "TableCell"
        converted.append([p(cell, style) for cell in row])
    t = Table(converted, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("BOX", (0, 0), (-1, -1), 0.45, colors.HexColor("#B8C2CC")),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D3DCE6")),
        ("LEFTPADDING", (0, 0), (-1, -1), 5.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5.5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    if header:
        commands.append(("BACKGROUND", (0, 0), (-1, 0), BLUE))
    start = 1 if header else 0
    for i in range(start, len(data)):
        if i % 2 == 0:
            commands.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#FAFBFC")))
    t.setStyle(TableStyle(commands))
    return t


def callout(title: str, body: str, fill=BLUE_LIGHT) -> Table:
    t = Table([[p(title, "CalloutTitle")], [p(body, "CalloutBody")]], colWidths=[CONTENT_W])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), fill),
                ("BOX", (0, 0), (-1, -1), 0.65, colors.HexColor("#B7CCE0")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


def add(story: list, *items):
    for item in items:
        story.append(item)
        if isinstance(item, Table):
            story.append(Spacer(1, 7))


def read_grade_rows() -> list[dict[str, str]]:
    with CSV_PATH.open(newline="") as f:
        return list(csv.DictReader(f))


def grade_summary() -> dict[str, dict]:
    rows = read_grade_rows()
    out = {}
    for section in sorted({r["section"] for r in rows}):
        sec_rows = [r for r in rows if r["section"] == section]
        numeric = [int(r["precalificacion"]) for r in sec_rows if r["precalificacion"]]
        categories = {}
        for col in ["parciales", "proyectos_investigaciones", "laboratorios", "asistencia"]:
            vals = [float(r[col]) for r in sec_rows if r[col]]
            categories[col] = (round(mean(vals), 2), round(min(vals), 2), round(max(vals), 2)) if vals else None
        bins = Counter()
        for val in numeric:
            if val >= 90:
                bins["90-100"] += 1
            elif val >= 80:
                bins["80-89"] += 1
            elif val >= 70:
                bins["70-79"] += 1
            elif val >= 60:
                bins["60-69"] += 1
            else:
                bins["<60"] += 1
        out[section] = {
            "n": len(sec_rows),
            "numeric": len(numeric),
            "avg": round(mean(numeric), 2) if numeric else None,
            "min": min(numeric) if numeric else None,
            "max": max(numeric) if numeric else None,
            "categories": categories,
            "bins": bins,
            "missing": [r for r in sec_rows if not r["precalificacion"]],
        }
    return out


ASSIGNMENTS = [
    ["A1", "Creación de repositorio GitHub", "Laboratorio", "Checklist de README, foto, datos personales, materia e intención del curso.", "Módulo II: entorno, GitHub y prácticas de trabajo"],
    ["A2", "Investigación: Desarrollo Agéntico", "Proyecto / investigación", "Investigación individual sobre agentes de desarrollo, comparación de herramientas, capturas y evidencia Git.", "Módulo I-II: investigación tecnológica, herramientas y ciclo de desarrollo"],
    ["A3", "Presentación grupal: tema asignado", "Proyecto / investigación", "Presentación audiovisual con dominio del tema, participación, ejemplos, habilidades y tiempo.", "Módulos I-II: comunicación técnica y análisis de tecnologías"],
    ["A4", "Informe escrito grupal", "Proyecto / investigación", "Informe académico con profundidad, APA, conclusiones, ejemplos visuales y estructura.", "Módulos I-II: documentación técnica y análisis de herramientas"],
    ["A5", "PollClass: Desarrollo Agéntico Full Stack", "Laboratorio", "Aplicación full stack con rol docente/estudiante, votos, tiempo real, documentación y despliegue.", "Módulo III: integración frontend-backend y desarrollo de producto"],
    ["A6", "Suite Playwright para validar A5", "Laboratorio", "Pruebas E2E con flujos críticos, assertions, caso negativo y bitácora de validación.", "Módulo III: calidad, verificación y pruebas"],
    ["A7", "Parcial #2: MVP Startup Full Stack", "Parcial", "Evaluación práctica de producto full stack y defensa de decisiones técnicas.", "Módulos II-III: arquitectura, implementación y entrega funcional"],
    ["A8", "Parcial teórico", "Parcial", "Prueba Forms con preguntas objetivas y preguntas abiertas.", "Módulos I-III: fundamentos conceptuales y juicio técnico"],
    ["A9", "Proyecto individual: Pokemon Battle Rooms", "Proyecto / investigación", "Proyecto full stack individual con MongoDB, Hono/Bun, TanStack, salas, batalla y pruebas.", "Módulo III: implementación integral, APIs, persistencia, seguridad y UI"],
    ["A10", "Proyecto individual: Juego de Damas con IA A*", "Proyecto / investigación", "Juego de damas (una de 5 variantes) vs computadora: A* obligatorio en microservicio Bun, login, ranking, pago en modo prueba y tests.", "Módulo III + Módulo I U3: algoritmos, microservicios, seguridad, pasarela de pago y pruebas"],
    ["A11", "Parcial #3: React y Hono", "Parcial", "Forms con 20 preguntas objetivas (15 React 19, 5 Hono) y 2 de desarrollo tipo escenario; 80 pts, 30 min.", "Módulo III U1/U3: frontend declarativo moderno y backend sobre Web Standards"],
]

ASSIGNMENT_RESULTS = [
    ["A1", "Repositorio GitHub", "Ambos salones", "Checklist administrativo usado como laboratorio; verificación de repo, README, identidad, foto e intención del curso.", "Base para repos posteriores y uso de Git."],
    ["A2", "Investigación Desarrollo Agéntico", "69 notas capturadas", "Promedios aproximados: 1GS241 ~83, 1GS242 ~78. Se revisaron PRs, Markdown, capturas y commits.", "Introdujo herramientas de desarrollo asistido y reflexión técnica actualizada."],
    ["A3", "Presentación grupal", "69 notas capturadas", "1GS241 avg 82.6; 1GS242 avg 77.1. Se cruzaron videos, READMEs, repos y evidencia grupal.", "Evaluó comunicación técnica, dominio y colaboración."],
    ["A4", "Informe escrito grupal", "69 notas capturadas", "1GS241 avg 87.7; 1GS242 avg 81.8. Se detectaron grupos por Integrantes, PDFs y READMEs.", "Evaluó investigación académica, APA, estructura y conclusiones."],
    ["A5", "PollClass", "Notas revisadas", "Laboratorio full stack con varias correcciones por branches, repos alternos e invitaciones aceptadas.", "Evidencia de construcción de producto y uso de agentes."],
    ["A6", "Playwright", "Notas revisadas", "Suite E2E evaluada por flujos críticos, assertions, caso negativo y bitácora.", "Evidencia de calidad y validación automatizada."],
    ["A7", "Parcial #2 MVP Startup", "Capturado", "Parcial práctico ingresado manualmente y usado en la categoría de parciales.", "Integra arquitectura, MVP y decisiones técnicas."],
    ["A8", "Parcial teórico", "Calificado", "Preguntas abiertas calificadas manualmente y revisión de respuestas conceptuales.", "Evidencia conceptual de fundamentos Full Stack."],
    ["A9", "Pokemon Battle Rooms", "Finalizado y devuelto", "Proyecto individual calificado con base en persistencia, salas, motor de batalla, interfaz, documentación y reproducibilidad. Devuelto 36/36 en ambas secciones.", "Proyecto integrador individual de backend, frontend, DB, salas, reglas de dominio y pruebas."],
    ["A10", "Juego de Damas con IA A*", "Publicada 11-jun; due 12-jun 11:59 PM (cierre 13-jun)", "100 pts sin rúbrica Teams (puntos por criterio en instrucciones); el criterio de mayor peso (25 pts) es el microservicio Bun con A* puro. Pendiente de calificación.", "Integra algoritmos de búsqueda, arquitectura de microservicios, pagos en modo prueba y testing."],
    ["A11", "Parcial #3: React y Hono", "Programado: 1GS241 lun 15-jun 7:30 PM; 1GS242 mar 16-jun 7:30 PM", "Quiz Forms asociado por sección: 20 MC (3 pts c/u) + 2 desarrollo (10 pts c/u) = 80 pts, timer de 30 min. Guía de estudio publicada en Class Materials.", "Tercer parcial del curso; evalúa React 19 y Hono con preguntas de criterio técnico."],
]

PLANNED_ACTIVITIES = [
    ["A11 Parcial #3: React y Hono", "Parcial (ya programado)", "Forms con 20 MC + 2 desarrollo (80 pts, 30 min). 1GS241: lun 15-jun 7:30 PM; 1GS242: mar 16-jun 7:30 PM. Guía de estudio publicada.", "Comprobar comprensión conceptual de React 19 y Hono posterior a los proyectos integradores."],
    ["Refactor técnico de proyecto existente", "Laboratorio aplicado", "Mejora puntual sobre un proyecto ya desarrollado: separación de lógica, modelos, handlers, validaciones, manejo de errores o estado React.", "Evitar repetir laboratorios básicos y evidenciar madurez técnica sobre código real."],
    ["QA sobre proyecto existente", "Laboratorio aplicado", "Validación de flujos críticos, caso negativo, evidencia de ejecución y corrección de hallazgos sobre el propio proyecto.", "Conectar pruebas con producto real y no con un laboratorio aislado."],
    ["Plan de evolución a MVP", "Proyecto / preparación", "Diagnóstico del POC del parcial #2, backlog, alcance MVP, riesgos, arquitectura propuesta y demo actual.", "Preparar el semestral con decisiones concretas y alcance realista."],
    ["Semestral: POC a MVP de comercio electrónico", "Semestral", "Mejora sustancial del comercio electrónico del parcial #2 para llevarlo de POC a MVP funcional, demostrable y estable.", "Cerrar el curso con un producto integrado que combine frontend, backend, datos, calidad y documentación."],
]

COMPLIANCE_MATRIX = [
    ["Elemento mínimo", "Evidencia producida", "Dónde se conserva", "Estado"],
    ["Programa de la asignatura", "Programa oficial y resumen estructurado del programa 1493.", "materials/1493 DS_IX Programa de Asignatura.pdf; COURSE_PROGRAM_DS_IX.md; PDF 01.", "Completo"],
    ["Planificación semestral", "Módulos, cronograma operativo, mapa de evaluación y acciones pendientes.", "PDF 01; MEMORY.md.", "Completo a la fecha"],
    ["Material didáctico", "9 capítulos por módulos (versiones extendidas de 10-14 págs, 12-jun), guía de estudio del Parcial #3 y 2 módulos extra, publicados en Teams.", "materials/modulos/; PDF 02.", "Completo"],
    ["Pruebas parciales", "Parcial práctico A7 y teórico A8 aplicados con política de corrección; A11 (Parcial #3) programado 15/16-jun con quiz Forms y JSON fuente.", "Teams Assignments; submissions/asignacion-08-* y asignacion-11-*.", "Completo a la fecha"],
    ["Proyectos / asignaciones", "A2, A3, A4, A9 calificados con rúbricas, resultados y feedback; A10 publicada (due 12-jun).", "submissions/asignacion-02-* a asignacion-11-*; PDF 04.", "Completo a la fecha"],
    ["Laboratorios / prácticas", "A1, A5 y A6 con criterios y evidencia de repos.", "submissions/asignacion-01-*, asignacion-05-*, asignacion-06-*.", "Completo"],
    ["Registro de calificaciones", "CSV/XLSX consolidado, precalificación y carga en matrícula.", "submissions/notas_actuales_*; submissions/matricula_midterm_*; PDF 05.", "Completo a la fecha"],
    ["Asistencia", "Asistencia completa usada en precalificación; soporte institucional disponible en matrícula.", "PDF 06; sistema matrícula UTP.", "Parcial"],
    ["Mejora continua", "Revisión de evidencias, actualización de repositorios, devolución de notas y ajustes documentados.", "submissions/revisiones/; MEMORY.md; PDF 06.", "Completo a la fecha"],
]

SECTION_CONTEXT = [
    ["Sección", "Teams", "Codhora matrícula", "Uso en portafolio"],
    ["1GS241", "DES__SOFT_IX_1GS241_2026", "5208", "Grupo 1 del curso; materiales y asignaciones paralelas a 1GS242."],
    ["1GS242", "DES__SOFT_IX_1GS242_2026", "5214", "Grupo 2 del curso; mismas evidencias docentes con registro de notas independiente."],
]


MATERIALS = [
    ["Programa oficial", "PROGRAMA_DE_ASIGNATURA.pdf", "Class Materials raíz", "Programa oficial 1493 Desarrollo de Software IX."],
    ["Módulo I", "CAPITULO_01_FORMULACION_PROYECTOS_FULL_STACK.pdf", "MODULO_01_FORMULACION_PROYECTOS", "Formulación de proyectos Full Stack."],
    ["Módulo II", "CAPITULO_02_ARQUITECTURA_FULL_STACK_Y_CICLO_DE_DESARROLLO.pdf", "MODULO_02_FUNDAMENTOS_TECNOLOGICOS", "Arquitectura Full Stack y ciclo de desarrollo."],
    ["Módulo II", "CAPITULO_03_ENTORNO_HERRAMIENTAS_Y_CONFIGURACION_FULL_STACK.pdf", "MODULO_02_FUNDAMENTOS_TECNOLOGICOS", "Entorno, herramientas y configuración."],
    ["Módulo III", "CAPITULO_04_BACKEND_NODE_EXPRESS_APIS_REST.pdf", "MODULO_03_DESARROLLO_IMPLEMENTACION", "Backend Node, Express y APIs REST."],
    ["Módulo III", "CAPITULO_05_SEGURIDAD_APIS_AUTENTICACION_JWT.pdf", "MODULO_03_DESARROLLO_IMPLEMENTACION", "Seguridad, cifrado y autenticación JWT."],
    ["Módulo III", "CAPITULO_06_MONGODB_MONGOOSE_CRUD.pdf", "MODULO_03_DESARROLLO_IMPLEMENTACION", "MongoDB, Mongoose y CRUD."],
    ["Módulo III", "CAPITULO_07_REACT_COMPONENTES_HOOKS_FORMULARIOS.pdf", "MODULO_03_DESARROLLO_IMPLEMENTACION", "React, componentes, hooks y formularios."],
    ["Módulo III", "CAPITULO_08_INTEGRACION_FRONTEND_BACKEND_PRUEBAS.pdf", "MODULO_03_DESARROLLO_IMPLEMENTACION", "Integración frontend-backend y pruebas."],
    ["Módulo III", "CAPITULO_09_INTEGRACIONES_EXTERNAS_PAGOS_E_IA.pdf", "MODULO_03_DESARROLLO_IMPLEMENTACION", "Servicios de terceros, pasarelas de pago y consumo de modelos de IA (completa Módulo I U3)."],
    ["Módulo III", "GUIA_ESTUDIO_PARCIAL_3_REACT_19_Y_HONO.pdf", "MODULO_03_DESARROLLO_IMPLEMENTACION", "Material teórico de React 19 y Hono; preparación del Parcial #3."],
    ["Módulo extra", "MODULO_EXTRA_AGENTES_CLAUDE_CODE_OPENCODE_CODEX_MAYO_2026.pdf", "modulo extra", "Agentes de desarrollo, skills, rules, MCPs y plugins."],
    ["Módulo extra", "MODULO_EXTRA_GIT_BUENAS_PRACTICAS_DESARROLLO_AGENTICO_MAYO_2026.pdf", "modulo extra", "Git y buenas prácticas en desarrollo agéntico."],
]


def doc_index() -> list:
    story = [NextPageTemplate("body"), PageBreak()]
    add(
        story,
        h1("Propósito y alcance"),
        p("Este índice organiza el portafolio docente del curso Desarrollo de Software IX para el I semestre 2026. El expediente reúne el programa de asignatura, la planificación semestral, los materiales didácticos, las evaluaciones, las asignaciones, los laboratorios, el registro de calificaciones y la asistencia."),
        h1("Documentos del portafolio"),
        table(
            [
                ["PDF", "Contenido", "Uso en revisión"],
                ["00 Índice y contexto", "Mapa del portafolio, secciones del curso y ubicación de evidencias.", "Ubicar rápidamente cada parte del expediente."],
                ["01 Programa y planificación", "Datos oficiales, competencias, resultados, módulos, cronograma y alineación.", "Verificar correspondencia con programa 1493."],
                ["02 Materiales didácticos", "Capítulos y módulos subidos a Teams, recursos extra y cobertura teórica.", "Evidenciar apoyo docente y cobertura de contenidos."],
                ["03 Evaluación y rúbricas", "Ponderaciones, clasificación de asignaciones y criterios de corrección.", "Consultar cómo se evaluó cada componente."],
                ["04 Asignaciones y actividades", "Evidencia de A1-A11, finalidad pedagógica y relación con módulos.", "Demostrar aprendizaje basado en proyectos y laboratorios."],
                ["05 Calificaciones y precalificación", "Resumen estadístico, registro de notas y carga de mid-term.", "Evidenciar seguimiento académico."],
                ["06 Asistencia, seguimiento y mejora", "Asistencia, devoluciones, revisiones de evidencias y mejora continua.", "Documentar gestión del curso y acciones correctivas."],
                ["07 Anexos institucionales", "Referencias institucionales y checklist de cierre.", "Conservar base normativa y pendientes del curso."],
            ],
            [1.55 * inch, 3.2 * inch, 1.95 * inch],
        ),
        h1("Ubicación operativa"),
        table(
            [
                ["Elemento", "Ubicación"],
                ["Workspace local", str(ROOT)],
                ["Materiales PDF", "materials/modulos/ y materials/portafolio_docente/"],
                ["Evidencias de asignaciones", "submissions/asignacion-01-* hasta submissions/asignacion-11-*"],
                ["Notas consolidadas", "submissions/notas_actuales_2026-05-24-eric-marin-michael-portela/"],
                ["Salón Teams 1", "DES__SOFT_IX_1GS241_2026"],
                ["Salón Teams 2", "DES__SOFT_IX_1GS242_2026"],
            ],
            [1.8 * inch, 4.9 * inch],
        ),
        h1("Secciones del curso"),
        table(SECTION_CONTEXT, [0.85 * inch, 2.45 * inch, 1.15 * inch, 2.25 * inch]),
        h1("Contenido del portafolio"),
        table(COMPLIANCE_MATRIX, [1.25 * inch, 2.0 * inch, 2.45 * inch, 1.0 * inch]),
    )
    return story


def doc_program() -> list:
    story = [NextPageTemplate("body"), PageBreak()]
    add(
        story,
        h1("Datos generales de la asignatura"),
        table(
            [
                ["Campo", "Descripción"],
                ["Universidad", "Universidad Tecnológica de Panamá"],
                ["Facultad", "Facultad de Ingeniería de Sistemas Computacionales"],
                ["Departamento", "Programación de Computadoras"],
                ["Asignatura", "Desarrollo de Software IX"],
                ["Código", "1493"],
                ["Créditos y horas", "4 créditos; 2 horas de teoría y 4 horas de laboratorio por semana"],
                ["Requisito", "Haber aprobado tercer año"],
                ["Documento fuente", "1493 DS_IX Programa de Asignatura.pdf; creado/modificado el 16 de marzo de 2026"],
            ],
            [1.8 * inch, 4.9 * inch],
        ),
        h1("Descripción académica"),
        p("El curso consolida fundamentos previos de programación y orienta al estudiante hacia el diseño e implementación de soluciones Full Stack. La experiencia formativa integra arquitectura cliente-servidor, backend, frontend, base de datos, calidad, seguridad y toma de decisiones técnicas frente a necesidades organizacionales reales."),
        h1("Competencia específica y resultado de aprendizaje"),
        table(
            [
                ["Tipo", "Declaración"],
                ["Competencia específica", "Desarrollar soluciones de software bajo enfoque Full Stack mediante integración de arquitecturas cliente-servidor, servicios backend, interfaces frontend y bases de datos, aplicando ingeniería de software, calidad y seguridad."],
                ["Resultado de aprendizaje", "Integrar componentes frontend, backend y bases de datos en una aplicación web funcional utilizando frameworks de desarrollo y buenas prácticas de calidad y seguridad."],
            ],
            [1.65 * inch, 5.05 * inch],
        ),
        h1("Módulos oficiales y planificación docente"),
        table(
            [
                ["Módulo", "Duración", "Contenidos principales", "Evidencia del curso"],
                ["I. Formulación de Proyectos Full Stack", "2 semanas", "Problema, objetivos, alcance, requerimientos, arquitectura, desarrollo y pruebas.", "A2, A3, A4; Capítulo 1; análisis de herramientas y formulación."],
                ["II. Fundamentos Tecnológicos y Entorno", "3 semanas", "Arquitectura Full Stack, frameworks, stacks, Node.js, npm, Express, React, MongoDB.", "A1, A2-A4, A7; capítulos 2-3; módulo extra de agentes y Git."],
                ["III. Desarrollo e Implementación", "11 semanas", "Backend/API, rutas REST, middlewares, errores, documentación, seguridad JWT, MongoDB/Mongoose/CRUD, React, hooks, integración, pruebas e integraciones externas.", "A5, A6, A8, A9, A10, A11; capítulos 4-9 y guía React 19/Hono; proyectos PollClass, Pokemon y Damas."],
            ],
            [1.35 * inch, 0.85 * inch, 2.65 * inch, 1.85 * inch],
        ),
        h1("Cronograma académico interpretado"),
        table(
            [
                ["Semana / fase", "Enfoque", "Actividad o evidencia esperada"],
                ["Semanas 1-2", "Formulación, problema, alcance, requerimientos y arquitectura.", "A1, A2, A3/A4 iniciales; Capítulo 1."],
                ["Semanas 3-5", "Arquitectura Full Stack, herramientas, entorno y desarrollo agéntico.", "Capítulos 2-3; módulo extra de agentes y Git; preparación de laboratorios."],
                ["Semanas 6-8", "Backend, producto mínimo, pruebas y parcial teórico/práctico.", "A5 PollClass, A6 Playwright, A7, A8 y precalificación."],
                ["Semanas 9-13", "Persistencia, seguridad, React, integración y proyecto integrador.", "Capítulos 4-8; A9 Pokemon Battle Rooms."],
                ["Semanas 14-16", "Cierre: proyecto algorítmico, parcial teórico #3 y semestral.", "A10 Damas con IA A* (due 12-jun); A11 Parcial #3 React y Hono (15/16-jun); plan de MVP y evolución del comercio electrónico del parcial #2."],
            ],
            [1.2 * inch, 2.95 * inch, 2.55 * inch],
        ),
        h1("Planificación de cierre"),
        table(
            [["Actividad", "Categoría", "Descripción", "Propósito"]] + PLANNED_ACTIVITIES,
            [1.25 * inch, 1.05 * inch, 2.65 * inch, 1.75 * inch],
        ),
        h1("Metodología aplicada"),
        bullets(
            [
                "Aprendizaje basado en problemas y proyectos, con evidencias incrementales desde investigación hasta implementación.",
                "Estudios de caso y demostraciones: agentes de desarrollo, Git, PollClass, APIs, MongoDB, React y Pokemon Battle Rooms.",
                "Trabajo individual y colaborativo: investigaciones, presentaciones, informes grupales y proyectos individuales.",
                "Evaluación formativa y sumativa: rúbricas, retroalimentación en Teams, revisión de evidencias y precalificación institucional.",
            ]
        ),
    )
    return story


def doc_materials() -> list:
    story = [NextPageTemplate("body"), PageBreak()]
    add(
        story,
        h1("Materiales publicados en Teams"),
        p("Los materiales teóricos fueron generados como PDFs docentes y publicados en Class Materials de ambos salones. La estructura respeta los módulos oficiales del programa y añade dos módulos extra por pertinencia tecnológica del año 2026. El 12 de junio los capítulos 2-8 se reemplazaron por versiones extendidas (de 5-6 a 10-14 páginas, con más teoría, código ilustrativo y casos guía), se añadió el capítulo 9 de integraciones externas — que completa los temas de pasarela de pago y consumo de IA del Módulo I — y la guía de estudio de React 19 y Hono."),
        table(
            [["Bloque", "Archivo", "Carpeta Teams", "Propósito"]] + MATERIALS,
            [0.9 * inch, 2.25 * inch, 1.65 * inch, 1.9 * inch],
        ),
        h1("Cobertura frente al programa"),
        table(
            [
                ["Resultado / contenido", "Material de apoyo", "Tipo de evidencia"],
                ["Formulación de proyecto y arquitectura", "Capítulo 1", "Guía conceptual, actividades, checklist y rúbrica."],
                ["Arquitectura y entorno Full Stack", "Capítulos 2 y 3", "Explicación de stacks, herramientas y configuración."],
                ["Backend, APIs y seguridad", "Capítulos 4 y 5", "Diseño de servicios, rutas, middlewares, errores, JWT y cifrado."],
                ["Persistencia", "Capítulo 6", "MongoDB, Mongoose, modelos, CRUD y buenas prácticas."],
                ["Frontend", "Capítulo 7", "React, componentes, hooks, formularios y validación."],
                ["Integración y pruebas", "Capítulo 8", "Consumo de APIs, QA, Playwright y validación de integración."],
                ["Integraciones externas (Módulo I U3)", "Capítulo 9", "Servicios de terceros, pasarelas de pago, webhooks e idempotencia, y consumo de modelos de IA."],
                ["Frontend y backend modernos", "Guía React 19 y Hono", "React 19 (use, Actions, useOptimistic, Compiler) y Hono sobre Web Standards; soporte del Parcial #3."],
                ["Actualización profesional", "Módulos extra", "Agentes, MCPs/plugins, skills/rules y Git en entornos agénticos."],
            ],
            [1.7 * inch, 1.6 * inch, 3.4 * inch],
        ),
        h1("Criterios de calidad del material"),
        bullets(
            [
                "Los documentos se generaron con formato docente uniforme: portada, contenido conceptual, tablas, actividades, checklist y síntesis.",
                "Se verificó visualmente el renderizado de los PDFs con páginas de QA para evitar tablas cortadas o texto no extraíble.",
                "El contenido conecta teoría con práctica Full Stack: frontend, backend, base de datos, seguridad, integración y pruebas.",
                "Los módulos extra reflejan herramientas y prácticas actualizadas a mayo de 2026, útiles para desarrollo production-ready.",
            ]
        ),
        h1("Control documental de materiales"),
        table(
            [
                ["Control", "Aplicación"],
                ["Formato", "PDF tamaño carta, texto extraíble, portada institucional, tablas y actividades."],
                ["Publicación", "Subido a Class Materials de ambos salones con los mismos nombres de archivo."],
                ["Revisión visual", "Renderizado a PNG y revisión de hojas de contacto para detectar cortes de tablas o páginas dañadas."],
                ["Actualización", "Los módulos extra tienen corte explícito a mayo 2026 por depender de herramientas en evolución."],
                ["Uso docente", "Sirven como soporte de teoría, lectura previa, referencia de laboratorio y documentación para estudiantes."],
            ],
            [1.55 * inch, 5.15 * inch],
        ),
    )
    return story


def doc_eval() -> list:
    story = [NextPageTemplate("body"), PageBreak()]
    add(
        story,
        h1("Modelo de evaluación del curso"),
        table(
            [
                ["Componente", "Peso", "Asignaciones asociadas", "Estado a la fecha"],
                ["Parciales", "30%", "A7, A8, A11", "A7 y A8 capturados; A11 programado 15/16-jun (Forms, 80 pts)."],
                ["Proyectos / investigaciones", "15%", "A2, A3, A4, A9, A10", "A9 incorporado; A10 publicada con due 12-jun, pendiente de calificar."],
                ["Laboratorios", "15%", "A1, A5, A6", "Clasificación corregida: A1 es laboratorio."],
                ["Portafolio", "5%", "Pendiente", "Sin asignación cargada todavía."],
                ["Semestral", "30%", "Pendiente", "A realizar en cierre del curso."],
                ["Asistencia", "5%", "Registro institucional", "100 para todos en cálculo actual."],
            ],
            [1.55 * inch, 0.7 * inch, 2.35 * inch, 2.1 * inch],
        ),
        h1("Mapa de rúbricas y criterios"),
        table(
            [["Asignación", "Criterios principales", "Forma de evidencia"]]
            + [
                ["A2", "Definición, comparación, capturas, Markdown, Copilot, explicación de agentes, commit CLI.", "README / PR / repositorio."],
                ["A3", "Dominio, participación, ejemplos, habilidad de presentación, gestión del tiempo.", "Video, README, evidencias grupales."],
                ["A4", "Profundidad, conclusiones, APA, ejemplos visuales, estructura.", "PDF o Markdown con integrantes y bibliografía."],
                ["A5", "Funcionalidad, responsive, validación de votos, documentación y despliegue.", "Aplicación PollClass y README."],
                ["A6", "Cobertura, assertions, caso negativo y bitácora.", "Suite Playwright y evidencia de validación."],
                ["A8", "Selección múltiple parcial y preguntas abiertas con criterio estricto.", "Forms, revisión manual de abiertas."],
                ["A9", "Datos/persistencia, salas, motor de batalla, UI, documentación/Docker/demo.", "Repo Pokemon Battle Rooms."],
                ["A10", "Motor de damas (20), microservicio Bun con A* puro (25), login/ranking (15), pago en modo prueba (15), tests (10), documentación/Docker/demo (15).", "Repo del juego; puntos por criterio en las instrucciones (sin rúbrica Teams)."],
                ["A11", "MC: 3 pts solo si perfecta, 1 pt con al menos una correcta, 0 sin ninguna. Desarrollo: hasta 10 pts con criterio estricto.", "Forms por sección; quiz.json local como fuente auditable."],
            ],
            [0.75 * inch, 4.0 * inch, 1.95 * inch],
        ),
        h1("Control de justicia en la evaluación"),
        bullets(
            [
                "Se hicieron segundas pasadas para notas bajas cuando existía riesgo de evidencia enterrada en carpetas del repositorio.",
                "Se actualizaron repositorios locales antes de revisar entregas basadas en código, evitando usar copias desactualizadas.",
                "Se documentaron cambios relevantes en las calificaciones dentro de los registros del curso.",
                "Las recalificaciones se registraron en archivos de revisión dentro de submissions/revisiones/.",
            ]
        ),
        h1("Evidencias de evaluación generadas"),
        table(
            [
                ["Tipo de evidencia", "Descripción"],
                ["Rúbricas Markdown", "Criterios por asignación conservados localmente para consulta y actualización."],
                ["Comentarios Teams", "Retroalimentación registrada en asignaciones calificadas."],
                ["Parcial A8", "Registro local de preguntas, resultados y revisión manual."],
                ["Seguimiento A9", "Registro acumulado del proyecto Pokemon con calificaciones, observaciones y devoluciones."],
                ["Revisiones", "Archivos fechados en submissions/revisiones para seguimiento de evidencias y calificaciones."],
            ],
            [1.6 * inch, 5.1 * inch],
        ),
    )
    return story


def doc_assignments() -> list:
    story = [NextPageTemplate("body"), PageBreak()]
    add(
        story,
        h1("Asignaciones ejecutadas hasta la fecha"),
        table(
            [["ID", "Actividad", "Categoría", "Evidencia / producto", "Alineación con el programa"]] + ASSIGNMENTS,
            [0.45 * inch, 1.55 * inch, 1.0 * inch, 2.15 * inch, 1.55 * inch],
        ),
        h1("Secuencia pedagógica"),
        table(
            [
                ["Fase", "Estrategia", "Evidencias"],
                ["Inicio", "Configurar identidad técnica y repositorio; introducir investigación tecnológica.", "A1 y A2."],
                ["Exploración", "Comunicar hallazgos y documentar temas técnicos con APA y ejemplos.", "A3 y A4."],
                ["Construcción", "Desarrollar producto Full Stack con apoyo de agentes y despliegue.", "A5 PollClass."],
                ["Calidad", "Validar funcionalidad mediante pruebas E2E y bitácora de agente.", "A6 Playwright."],
                ["Síntesis intermedia", "Evaluar práctica y teoría en arquitectura, herramientas e implementación.", "A7 y A8."],
                ["Integración avanzada", "Resolver un proyecto individual completo con datos externos, persistencia, backend, frontend y motor de dominio.", "A9 Pokemon Battle Rooms."],
                ["Cierre algorítmico y teórico", "Exigir un algoritmo clásico (A*) aislado en un microservicio, con pagos y tests; cerrar la teoría con el tercer parcial.", "A10 Damas con IA A* y A11 Parcial #3."],
            ],
            [1.2 * inch, 3.0 * inch, 2.5 * inch],
        ),
        h1("Evidencias de publicación y devolución"),
        bullets(
            [
                "Las asignaciones se gestionaron en Teams para ambos salones, con revisiones, feedback y devolución.",
                "A8 fue corregida y revisada en sus componentes teóricos y de desarrollo.",
                "A9 fue corregida para permitir puntuación real de 100 puntos tras detectar una rúbrica Teams sin puntos.",
                "Todas las entregas recalculadas y pendientes fueron devueltas en Teams antes de la precalificación.",
            ]
        ),
        h1("Resultados y observaciones por asignación"),
        table(
            [["ID", "Actividad", "Estado", "Observación de evaluación", "Valor académico"]] + ASSIGNMENT_RESULTS,
            [0.42 * inch, 1.35 * inch, 1.0 * inch, 2.55 * inch, 1.38 * inch],
        ),
        h1("Actividades planificadas"),
        p("Las siguientes actividades no repiten laboratorios básicos de React, MongoDB o Hono/Bun, porque esos contenidos ya se trabajaron de forma integrada en los proyectos. El cierre se orienta a comprensión teórica, mejora de código real, validación y evolución del comercio electrónico del parcial #2."),
        table(
            [["Actividad", "Categoría", "Enfoque", "Evidencia esperada"]] + [
                ["A11 Parcial #3 (programado 15/16-jun)", "Parcial", "React 19 y Hono desde preguntas conceptuales y escenarios de criterio técnico.", "Resultado Forms, respuestas de desarrollo y quiz.json auditable."],
                ["Refactor técnico", "Laboratorio aplicado", "Mejora de arquitectura interna sobre proyecto existente.", "Commits, breve justificación y evidencia antes/después."],
                ["QA aplicado", "Laboratorio aplicado", "Pruebas o validaciones sobre flujos reales del proyecto.", "Ejecución, hallazgos y correcciones."],
                ["Plan MVP", "Proyecto / preparación", "Backlog y alcance para convertir el comercio electrónico del parcial #2 en MVP.", "Documento breve, demo actual y plan de trabajo."],
                ["Semestral", "Semestral", "Evolución sustancial del POC de comercio electrónico.", "MVP funcional, demo, documentación y repositorio actualizado."],
            ],
            [1.25 * inch, 1.05 * inch, 2.55 * inch, 1.85 * inch],
        ),
        h1("Ubicación de evidencias locales"),
        table(
            [
                ["Evidencia", "Archivo / carpeta"],
                ["Rúbricas", "submissions/asignacion-02-* a submissions/asignacion-11-*/RUBRIC.md"],
                ["Resultados finales", "FINAL_GRADES.md, GRADING_RESULTS.md y GRADE_PROGRESS.md"],
                ["Revisiones de evidencias", "submissions/revisiones/"],
                ["Notas actuales", "submissions/notas_actuales_2026-05-24-eric-marin-michael-portela/"],
                ["Precalificación matrícula", "submissions/matricula_midterm_2026-05-24-eric-marin-michael-portela/"],
            ],
            [2.0 * inch, 4.7 * inch],
        ),
    )
    return story


def doc_grades() -> list:
    summary = grade_summary()
    story = [NextPageTemplate("body"), PageBreak()]
    rows = [["Grupo", "Estudiantes", "Con nota", "Promedio", "Mín", "Máx"]]
    for sec, data in summary.items():
        rows.append([sec, data["n"], data["numeric"], data["avg"], data["min"], data["max"]])
    add(story, h1("Resumen de precalificación mid-term"), table(rows, [1.0 * inch, 1.1 * inch, 1.0 * inch, 1.1 * inch, 0.8 * inch, 0.8 * inch]))
    add(
        story,
        p("La nota mid-term se calculó con los componentes ya ejecutados y con asistencia completa. Semestral y portafolio no fueron incluidos porque aún no tienen calificación. Fórmula usada: ((Parciales*30) + (Proyectos/Investigaciones*15) + (Laboratorios*15) + (Asistencia*5)) / 65."),
        h1("Promedios por categoría"),
    )
    cat_rows = [["Grupo", "Categoría", "Promedio", "Mín", "Máx"]]
    labels = {
        "parciales": "Parciales",
        "proyectos_investigaciones": "Proyectos / investigaciones",
        "laboratorios": "Laboratorios",
        "asistencia": "Asistencia",
    }
    for sec, data in summary.items():
        for key, label in labels.items():
            avg, mn, mx = data["categories"][key]
            cat_rows.append([sec, label, avg, mn, mx])
    add(story, table(cat_rows, [0.8 * inch, 2.1 * inch, 1.0 * inch, 0.9 * inch, 0.9 * inch]))
    add(story, h1("Distribución de precalificaciones"))
    dist = [["Grupo", "90-100", "80-89", "70-79", "60-69", "<60"]]
    for sec, data in summary.items():
        dist.append([sec, data["bins"]["90-100"], data["bins"]["80-89"], data["bins"]["70-79"], data["bins"]["60-69"], data["bins"]["<60"]])
    add(story, table(dist, [0.95 * inch, 0.95 * inch, 0.95 * inch, 0.95 * inch, 0.95 * inch, 0.95 * inch]))
    add(
        story,
        h1("Carga institucional en matrícula"),
        bullets(
            [
                "1GS241 / codhora 5208: 36 precalificaciones cargadas y registradas en matrícula.",
                "1GS242 / codhora 5214: precalificaciones registradas en matrícula.",
                "Los archivos de carga quedaron en submissions/matricula_midterm_2026-05-24-eric-marin-michael-portela/.",
            ]
        ),
        h1("Archivos de respaldo"),
        table(
            [
                ["Archivo", "Descripción"],
                ["notas_hasta_ahora_2026-05-24_eric-marin-michael-portela.xlsx", "Consolidado Excel con notas por categoría, raw y precalificación."],
                ["matricula_midterm_upload.csv", "Tabla preparada para cargar a matrícula."],
                ["matricula_midterm_exceptions.csv", "Control interno de excepciones de carga."],
                ["README.md de notas actuales", "Resumen de cambios Eric Marin y Michael Portela."],
            ],
            [2.8 * inch, 3.9 * inch],
        ),
        h1("Interpretación académica"),
        bullets(
            [
                "Las medias de ambos grupos son cercanas, con diferencias moderadas por la distribución de desempeño en proyectos y laboratorios.",
                "La categoría de proyectos/investigaciones refleja tanto investigación formal como implementación integradora; por eso A9 movió significativamente casos individuales.",
                "La precalificación no representa nota final: faltan A10 (due 12-jun), A11 Parcial #3 (15/16-jun), portafolio y semestral.",
                "Los valores registrados en Teams se conservaron como fuente oficial del consolidado.",
            ]
        ),
    )
    return story


def doc_followup() -> list:
    story = [NextPageTemplate("body"), PageBreak()]
    add(
        story,
        h1("Asistencia y participación"),
        p("Para el cálculo actual, la asistencia estudiantil fue tratada como completa para todos los estudiantes, con valor 100 en el componente de asistencia. El registro formal puede respaldarse con la plataforma institucional o con los reportes de Teams."),
        table(
            [
                ["Elemento", "Evidencia / decisión"],
                ["Asistencia estudiantil", "100 para todos en el cálculo de precalificación."],
                ["Asistencia docente", "Sistema matrícula UTP, módulo Asistencia / Justificar Asistencia, con credenciales resguardadas fuera del repositorio."],
                ["Publicación de materiales", "Class Materials en ambos salones Teams."],
                ["Devoluciones de notas", "Teams Assignments, con revisión y Return de tareas recalculadas."],
            ],
            [2.0 * inch, 4.7 * inch],
        ),
        h1("Seguimiento académico"),
        bullets(
            [
                "Se revisaron evidencias individuales y grupales en repositorios, ramas y carpetas alternativas.",
                "Se aplicó la regla de actualizar repos locales antes de recalificar para evitar evaluaciones con copias antiguas.",
                "Se mantuvo consistencia entre criterios de entrega, evidencia disponible y calificación registrada.",
                "Se documentó retroalimentación en Teams para orientar el cierre de cada actividad.",
            ]
        ),
        h1("Mejora continua"),
        table(
            [
                ["Hallazgo", "Acción correctiva"],
                ["Rúbrica sin puntos en A9", "Se retiró la rúbrica No points y se configuró nota real de 100 pts."],
                ["A8 parcial teórico", "Se revisaron manualmente los componentes que requerían juicio docente."],
                ["Repos locales desactualizados", "Se estableció regla de fetch/pull antes de recalificar."],
                ["Evidencia enterrada en subcarpetas", "Se ajustó revisión para buscar en Laboratorios/Tareas/Proyectos y no solo en la raíz."],
                ["Material teórico disperso", "Se crearon carpetas por módulo y PDFs teóricos completos en ambos salones."],
            ],
            [2.15 * inch, 4.55 * inch],
        ),
        h1("Bitácora de decisiones docentes recientes"),
        table(
            [
                ["Fecha", "Decisión / acción"],
                ["2026-05-22", "Se revisó A8 y se completó la calificación de preguntas abiertas y conceptuales."],
                ["2026-05-22", "Se corrigió A9 en Teams para permitir calificación real sobre 100 puntos."],
                ["2026-05-23", "Se estableció pull/fetch obligatorio antes de recalificar repos locales."],
                ["2026-05-23", "Se publicaron los módulos teóricos y extras en ambos salones Teams."],
                ["2026-05-24", "Se actualizaron evidencias pendientes y se registraron precalificaciones en matrícula."],
                ["2026-06-10/11", "Se creó y programó A11 Parcial #3 (React y Hono) en ambas secciones, con quiz.json auditable; reprogramado a 15/16-jun por decisión docente. Se publicó A10 Damas con IA A* con due 12-jun."],
                ["2026-06-11/12", "Se publicó la guía de estudio del Parcial #3, se extendieron los capítulos 2-8 (10-14 págs), se añadió el capítulo 9 de integraciones externas y se reemplazó todo en Class Materials de ambos salones."],
            ],
            [1.1 * inch, 5.6 * inch],
        ),
        h1("Acciones pendientes para cierre del curso"),
        bullets(
            [
                "Aplicar y calificar A11 Parcial #3 (programado: 15-jun 1GS241, 16-jun 1GS242) con la política de MC 3/1/0 y desarrollo con criterio estricto.",
                "Calificar A10 Damas con IA A* tras el cierre del 13-jun, verificando A* puro en el microservicio Bun como criterio de mayor peso.",
                "Publicar una actividad de preparación del semestral: diagnóstico y plan de evolución del POC a MVP.",
                "Planificar y publicar el semestral como mejora sustancial del comercio electrónico del parcial #2.",
                "Actualizar este portafolio con nota final, semestral, asistencia definitiva y cierre de contenidos.",
                "Exportar o conservar evidencias finales de Teams antes de cualquier cierre o cambio de plataforma.",
            ]
        ),
    )
    return story


def doc_annexes() -> list:
    story = [NextPageTemplate("body"), PageBreak()]
    add(
        story,
        h1("Referencias institucionales"),
        table(
            [
                ["Fuente", "Aporte al portafolio", "URL / referencia"],
                ["Estatuto Universitario UTP", "Marco normativo general de la Universidad.", "https://utp.ac.pa/estatuto-universitario"],
                ["Calidad de la Docencia UTP", "Fundamento de evaluación docente desde estudiantes, jefes y autoevaluación.", "https://utp.ac.pa/calidad-de-la-docencia"],
                ["Vicerrectoría Académica", "Funciones de coordinación, supervisión, evaluación y calidad académica.", "https://utp.ac.pa/vicerrectoria-academica"],
                ["Procedimiento de portafolios UTP", "Elementos mínimos del portafolio docente y formatos digitales permitidos.", "RIDDA2 UTP, propuesta de procedimiento para portafolios."],
                ["Evaluación externa ACAAI", "Portafolio docente obligatorio, supervisado por coordinadores y jefes de departamento.", "Inf_Evaluacion_Externa_-_2012.pdf"],
                ["Autoestudio FISC", "Incluye planificación del programa semestral dentro del portafolio docente FISC.", "Inf_Acreditacion_Lic_ingenieria_sistemas_y_computacion.pdf"],
            ],
            [1.55 * inch, 2.5 * inch, 2.65 * inch],
        ),
        h1("Checklist de portafolio docente"),
        table(
            [
                ["Requisito", "Evidencia en este portafolio", "Estado"],
                ["Programa de asignatura", "materials/1493 DS_IX Programa de Asignatura.pdf y PDF 01.", "Completo"],
                ["Planificación semestral", "PDF 01, mapa por módulos y acciones pendientes.", "Completo a la fecha"],
                ["Copias de pruebas parciales", "A7 y A8 en Teams; A8 y A11 con JSON local auditable y política de corrección.", "Completo a la fecha"],
                ["Registro de calificaciones", "PDF 05, XLSX/CSV consolidados y matrícula mid-term.", "Completo a la fecha"],
                ["Proyectos/asignaciones", "PDF 04, rúbricas y evidencias A1-A11.", "Completo a la fecha"],
                ["Guías de laboratorio/prácticas", "A5 PollClass, A6 Playwright, capítulos técnicos y rúbricas.", "Completo a la fecha"],
                ["Lista de asistencia", "PDF 06; asistencia completa en cálculo actual.", "Parcial"],
                ["Material didáctico", "PDF 02 y Class Materials por módulos.", "Completo a la fecha"],
            ],
            [1.8 * inch, 3.45 * inch, 1.45 * inch],
        ),
        h1("Cierre documental recomendado"),
        bullets(
            [
                "Al finalizar el semestre, regenerar este portafolio con semestral y nota final.",
                "Agregar evidencia exportada de asistencia definitiva y de la evaluación docente si el sistema la emite.",
                "Conservar los PDFs fuente y los CSV/XLSX de notas en una carpeta de solo lectura o en OneDrive institucional.",
                "Mantener una copia de los materiales de Teams por si cambia el acceso de los salones.",
            ]
        ),
    )
    return story


DOCS = [
    ("00_INDICE_CONTEXTO_PORTAFOLIO_DOCENTE_DSIX.pdf", "Índice y contexto del portafolio docente", "PDF 00", doc_index),
    ("01_PROGRAMA_PLANIFICACION_DOCENTE_DSIX.pdf", "Programa y planificación docente", "PDF 01", doc_program),
    ("02_MATERIALES_DIDACTICOS_RECURSOS_DSIX.pdf", "Materiales didácticos y recursos", "PDF 02", doc_materials),
    ("03_EVALUACION_RUBRICAS_CRITERIOS_DSIX.pdf", "Evaluación, rúbricas y criterios", "PDF 03", doc_eval),
    ("04_EVIDENCIAS_ASIGNACIONES_ACTIVIDADES_DSIX.pdf", "Evidencias de asignaciones y actividades", "PDF 04", doc_assignments),
    ("05_REGISTRO_CALIFICACIONES_PRECALIFICACION_DSIX.pdf", "Registro de calificaciones y precalificación", "PDF 05", doc_grades),
    ("06_ASISTENCIA_SEGUIMIENTO_MEJORA_DSIX.pdf", "Asistencia, seguimiento y mejora continua", "PDF 06", doc_followup),
    ("07_ANEXOS_INSTITUCIONALES_DSIX.pdf", "Anexos institucionales", "PDF 07", doc_annexes),
]


def build_pdf(filename: str, title: str, code: str, story_fn) -> Path:
    path = OUT_DIR / filename
    doc = PortfolioDoc(path, title, code)
    story = story_fn()
    doc.build(story)
    return path


def write_readme(paths: list[Path]):
    readme = OUT_DIR / "README.md"
    lines = [
        "# Portafolio docente - Desarrollo de Software IX",
        "",
        "Portafolio del I semestre 2026, basado en el programa oficial 1493, los materiales publicados en Teams (9 capítulos extendidos, guía de estudio y 2 módulos extra), las asignaciones A1-A11 y la precalificación mid-term del 24 de mayo de 2026. Última actualización: 12 de junio de 2026.",
        "",
        "## PDFs generados",
        "",
    ]
    for path in paths:
        lines.append(f"- `{path.name}`")
    lines += [
        "",
        "## Fuentes internas principales",
        "",
        "- `COURSE_PROGRAM_DS_IX.md`",
        "- `MEMORY.md`",
        "- `materials/modulos/`",
        "- `submissions/asignacion-*`",
        "- `submissions/notas_actuales_2026-05-24-eric-marin-michael-portela/`",
        "",
        "## Nota",
        "",
        "Estos PDFs organizan las evidencias principales del curso y se apoyan en los registros originales de Teams y del workspace local.",
    ]
    readme.write_text("\n".join(lines), encoding="utf-8")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    paths = [build_pdf(*spec) for spec in DOCS]
    write_readme(paths)
    # PDF combinado con las 8 secciones en orden
    from pypdf import PdfWriter

    writer = PdfWriter()
    for path in paths:
        writer.append(str(path))
    combined = OUT_DIR / "PORTAFOLIO_DOCENTE_DSIX_COMPLETO_2026.pdf"
    with combined.open("wb") as f:
        writer.write(f)
    paths.append(combined)
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
