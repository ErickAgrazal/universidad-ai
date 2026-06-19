from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
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


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "materials" / "capitulos" / "capitulo-01-formulacion-proyectos-full-stack.pdf"

PAGE_W, PAGE_H = letter
LEFT = RIGHT = 0.78 * inch
TOP = 0.72 * inch
BOTTOM = 0.72 * inch
CONTENT_W = PAGE_W - LEFT - RIGHT

BLUE = colors.HexColor("#174A7C")
BLUE_DARK = colors.HexColor("#0E2E4F")
BLUE_LIGHT = colors.HexColor("#EAF2FA")
GRAY = colors.HexColor("#5C6773")
GRAY_LIGHT = colors.HexColor("#F4F6F8")
INK = colors.HexColor("#1F2933")
GREEN = colors.HexColor("#2E7D5B")
GOLD = colors.HexColor("#8A6400")
RED = colors.HexColor("#9B1C1C")


def clean(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )


class CourseDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs):
        super().__init__(
            filename,
            pagesize=letter,
            leftMargin=LEFT,
            rightMargin=RIGHT,
            topMargin=TOP,
            bottomMargin=BOTTOM,
            **kwargs,
        )
        frame = Frame(LEFT, BOTTOM, CONTENT_W, PAGE_H - TOP - BOTTOM, id="normal")
        self.addPageTemplates(
            [
                PageTemplate(id="cover", frames=[frame], onPage=cover_page),
                PageTemplate(id="body", frames=[frame], onPage=body_page),
            ]
        )

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            style_name = flowable.style.name
            text = flowable.getPlainText()
            if style_name == "H1":
                self.notify("TOCEntry", (0, text, self.page))
                self.canv.bookmarkPage(text)
                self.canv.addOutlineEntry(text, text, level=0, closed=False)


def cover_page(canvas, doc):
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

    canvas.setFont("Helvetica-Bold", 32)
    canvas.drawString(LEFT, PAGE_H - 2.25 * inch, "Capítulo 1")
    canvas.setFont("Helvetica-Bold", 24)
    canvas.drawString(LEFT, PAGE_H - 2.7 * inch, "Formulación de Proyectos")
    canvas.drawString(LEFT, PAGE_H - 3.08 * inch, "Full Stack")

    canvas.setFillColor(colors.HexColor("#D7EAF7"))
    canvas.setFont("Helvetica", 13)
    canvas.drawString(
        LEFT,
        PAGE_H - 3.65 * inch,
        "Desarrollo de Software IX · Código 1493 · Primer módulo del curso",
    )

    canvas.setFillColor(colors.HexColor("#FFFFFF"))
    canvas.setStrokeColor(colors.HexColor("#5EA2D1"))
    canvas.roundRect(LEFT, 1.35 * inch, CONTENT_W, 1.85 * inch, 10, stroke=1, fill=0)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(LEFT + 0.28 * inch, 2.75 * inch, "Propósito del capítulo")
    canvas.setFont("Helvetica", 10.5)
    lines = [
        "Guiar al estudiante desde una idea inicial hasta una propuesta técnica coherente,",
        "con objetivos, alcance, requerimientos, arquitectura, plan de desarrollo y criterios",
        "de prueba para una aplicación web Full Stack.",
    ]
    y = 2.48 * inch
    for line in lines:
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
    canvas.drawString(LEFT, PAGE_H - 0.36 * inch, "Desarrollo de Software IX · Capítulo 1")
    canvas.drawRightString(PAGE_W - RIGHT, 0.38 * inch, f"Página {doc.page}")
    canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="Lead",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=11.5,
        leading=16,
        textColor=INK,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.2,
        leading=14.2,
        textColor=INK,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="Small",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.7,
        leading=11,
        textColor=GRAY,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="H1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=BLUE,
        spaceBefore=16,
        spaceAfter=9,
    )
)
styles.add(
    ParagraphStyle(
        name="H1NoTOC",
        parent=styles["H1"],
    )
)
styles.add(
    ParagraphStyle(
        name="H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13.2,
        leading=16,
        textColor=BLUE_DARK,
        spaceBefore=10,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="H3",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11.2,
        leading=14,
        textColor=INK,
        spaceBefore=8,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="CalloutTitle",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=10.2,
        leading=13,
        textColor=BLUE_DARK,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="CalloutBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=12.3,
        textColor=INK,
        spaceAfter=0,
    )
)
styles.add(
    ParagraphStyle(
        name="TableHead",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=10.5,
        textColor=colors.white,
        alignment=TA_LEFT,
    )
)
styles.add(
    ParagraphStyle(
        name="TableCell",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.4,
        leading=10.8,
        textColor=INK,
        spaceAfter=0,
    )
)
styles.add(
    ParagraphStyle(
        name="Check",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.4,
        leading=12,
        textColor=INK,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4,
    )
)


def p(text: str, style: str = "Body") -> Paragraph:
    return Paragraph(clean(text), styles[style])


def bullet(items: list[str]) -> ListFlowable:
    return ListFlowable(
        [ListItem(p(item, "Body"), leftIndent=12) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=18,
        bulletFontName="Helvetica",
        bulletFontSize=8,
    )


def numbered(items: list[str]) -> ListFlowable:
    return ListFlowable(
        [ListItem(p(item, "Body"), leftIndent=14) for item in items],
        bulletType="1",
        leftIndent=18,
        bulletFontName="Helvetica-Bold",
    )


def callout(title: str, body: str, fill=BLUE_LIGHT):
    data = [[p(title, "CalloutTitle")], [p(body, "CalloutBody")]]
    table = Table(data, colWidths=[CONTENT_W - 8])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), fill),
                ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#B7CCE0")),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def table(data, widths, header=True):
    converted = []
    for r, row in enumerate(data):
        style = "TableHead" if header and r == 0 else "TableCell"
        converted.append([p(str(cell), style) for cell in row])
    t = Table(converted, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#B8C2CC")),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D3DCE6")),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    if header:
        commands.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ]
        )
    for idx in range(1 if header else 0, len(data)):
        if idx % 2 == 0:
            commands.append(("BACKGROUND", (0, idx), (-1, idx), colors.HexColor("#FAFBFC")))
    t.setStyle(TableStyle(commands))
    return t


def checklist(items: list[str]):
    flow = []
    for item in items:
        flow.append(Paragraph("□ " + clean(item), styles["Check"]))
    return flow


def section(title: str):
    return [p(title, "H1")]


def subsection(title: str):
    return [p(title, "H2")]


def build_story():
    story = []
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            fontName="Helvetica-Bold",
            fontSize=10,
            name="TOCHeading1",
            leftIndent=0,
            firstLineIndent=0,
            spaceBefore=5,
            leading=12,
        ),
        ParagraphStyle(
            fontName="Helvetica",
            fontSize=9,
            name="TOCHeading2",
            leftIndent=18,
            firstLineIndent=0,
            leading=11,
            textColor=GRAY,
        ),
    ]
    story += [p("Tabla de contenido", "H1NoTOC"), toc, PageBreak()]

    story += section("1. Panorama del capítulo")
    story.append(
        p(
            "Este capítulo traduce la primera parte del programa oficial de Desarrollo de Software IX en una guía práctica para formular proyectos Full Stack. Antes de escribir código, el estudiante debe aprender a convertir una necesidad difusa en una propuesta técnica verificable: problema, objetivos, alcance, requerimientos, arquitectura, plan de desarrollo y pruebas.",
            "Lead",
        )
    )
    story.append(
        callout(
            "Idea central",
            "Un proyecto Full Stack no comienza con React, Express o MongoDB. Comienza con una decisión de diseño: qué problema se resolverá, para quién, con qué límites y bajo qué evidencia se podrá decir que la solución funciona.",
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        p(
            "En el contexto del curso, formular un proyecto no significa redactar una propuesta decorativa. Significa construir el mapa que guiará el trabajo técnico durante el semestre. Una formulación débil produce repositorios confusos, APIs improvisadas, interfaces sin propósito y bases de datos que no responden a la necesidad real. Una formulación sólida permite evaluar decisiones, distribuir responsabilidades y defender técnicamente la solución.",
        )
    )

    story += subsection("Resultado esperado")
    story.append(
        p(
            "Al finalizar este capítulo, el estudiante debe poder presentar una propuesta de proyecto Full Stack que incluya un problema claramente delimitado, objetivos evaluables, requerimientos funcionales y no funcionales, arquitectura inicial, diseño preliminar de API y base de datos, boceto de interfaz, plan de desarrollo y plan básico de pruebas.",
        )
    )
    story.append(
        table(
            [
                ["Elemento", "Pregunta que debe responder", "Evidencia mínima"],
                ["Problema", "¿Qué situación concreta se quiere mejorar?", "Descripción del contexto, usuarios afectados y consecuencias actuales."],
                ["Objetivo", "¿Qué cambio observable busca el proyecto?", "Objetivo general y objetivos específicos medibles."],
                ["Alcance", "¿Qué entra y qué queda fuera?", "Límites explícitos, entregables y supuestos."],
                ["Requerimientos", "¿Qué debe hacer y bajo qué restricciones?", "Lista funcional/no funcional priorizada."],
                ["Arquitectura", "¿Cómo se integran frontend, backend y datos?", "Diagrama o descripción de componentes y flujo."],
                ["Pruebas", "¿Cómo se validará que funciona?", "Casos de prueba e indicadores de aceptación."],
            ],
            [1.25 * inch, 2.35 * inch, 2.65 * inch],
        )
    )

    story += section("2. Del problema a la oportunidad técnica")
    story.append(
        p(
            "La primera tarea de un equipo Full Stack es comprender el problema antes de proponer una pantalla, una ruta de API o una colección en la base de datos. Muchos proyectos fallan porque confunden síntomas con problemas. Por ejemplo, “la empresa necesita una app” no es un problema; es una posible solución. Un problema mejor formulado sería: “el registro manual de solicitudes retrasa la atención, duplica datos y dificulta conocer el estado de cada caso”.",
        )
    )
    story.append(
        p(
            "La formulación del problema debe ubicar al lector en un contexto específico: quiénes participan, qué proceso actual existe, qué falla, qué impacto genera y por qué una solución digital puede aportar valor. La descripción debe ser suficientemente concreta para justificar decisiones posteriores de arquitectura y suficientemente limitada para que el proyecto sea viable dentro del semestre.",
        )
    )

    story += subsection("2.1 Señales de un buen problema")
    story.append(
        bullet(
            [
                "Tiene usuarios o actores identificables, no solo una idea abstracta.",
                "Describe una situación actual con consecuencias observables: tiempo perdido, errores, falta de trazabilidad, baja disponibilidad, mala experiencia o alto costo operativo.",
                "Permite imaginar criterios de éxito: reducción de pasos, mejor control, reportes, disponibilidad, seguridad, integración o automatización.",
                "No presupone una tecnología desde la primera línea. La tecnología se justifica después.",
                "Puede ser abordado mediante una aplicación Full Stack dentro de las restricciones del curso.",
            ]
        )
    )
    story += subsection("2.2 Técnica de redacción")
    story.append(
        p(
            "Una estructura útil para redactar el problema es: contexto + proceso actual + dificultad + consecuencia + oportunidad. Esta forma evita frases genéricas y obliga a conectar la necesidad con el diseño posterior.",
        )
    )
    story.append(
        callout(
            "Plantilla de problema",
            "En [contexto/organización], [usuarios] actualmente realizan [proceso] mediante [método actual]. Esto provoca [dificultad observable], lo cual genera [consecuencia]. Se requiere una solución que permita [cambio esperado] mediante [capacidades generales, sin entrar aún en implementación].",
            fill=GRAY_LIGHT,
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        table(
            [
                ["Versión débil", "Versión mejorada"],
                ["Queremos hacer un sistema para reservas.", "En laboratorios universitarios, la reserva de equipos se coordina por mensajes dispersos. Esto causa choques de horario, falta de historial y baja visibilidad de disponibilidad. Se requiere una plataforma que centralice reservas, estados y notificaciones."],
                ["La tienda necesita una página web.", "Una tienda local registra pedidos por chat y hojas separadas, lo que dificulta confirmar inventario, calcular totales y dar seguimiento. Se requiere una aplicación que integre catálogo, carrito, pedidos y administración básica."],
                ["Haremos una app con IA.", "El equipo académico revisa manualmente entregas extensas y no cuenta con un primer filtro de similitud, estructura o completitud. Se requiere una herramienta que apoye la revisión inicial y organice evidencias para evaluación humana."],
            ],
            [2.0 * inch, 4.3 * inch],
        )
    )

    story += section("3. Objetivos del proyecto")
    story.append(
        p(
            "Los objetivos convierten el problema en una dirección de trabajo. El objetivo general expresa el cambio principal que se quiere lograr; los objetivos específicos descomponen ese cambio en resultados más concretos. En un proyecto Full Stack, los objetivos deben conectar necesidades de usuario con componentes técnicos: interfaz, API, persistencia, seguridad e integración.",
        )
    )
    story.append(
        p(
            "Un error común es escribir objetivos como tareas aisladas: “crear una base de datos”, “hacer un login”, “usar React”. Esas frases describen acciones técnicas, pero no explican el valor del proyecto. Un objetivo más útil indica qué se logra con la acción: “permitir que usuarios autenticados consulten el estado de sus solicitudes en tiempo real mediante una interfaz web conectada a servicios backend”.",
        )
    )
    story += subsection("3.1 Objetivo general")
    story.append(
        p(
            "El objetivo general debe ser una oración clara que responda qué solución se construirá, para quién y con qué propósito. Puede mencionar el enfoque Full Stack, pero no debe convertirse en una lista de tecnologías.",
        )
    )
    story.append(
        callout(
            "Plantilla de objetivo general",
            "Diseñar e implementar una aplicación web Full Stack para [usuarios/contexto] que permita [capacidad principal] con el fin de [beneficio o cambio esperado].",
            fill=BLUE_LIGHT,
        )
    )
    story += subsection("3.2 Objetivos específicos")
    story.append(
        p(
            "Los objetivos específicos deben ser verificables. Una buena regla es redactar entre cuatro y seis objetivos: uno de análisis, uno de arquitectura, uno de backend, uno de frontend, uno de persistencia/seguridad y uno de pruebas o despliegue cuando aplique.",
        )
    )
    story.append(
        table(
            [
                ["Tipo", "Objetivo específico posible", "Evidencia"],
                ["Análisis", "Identificar requerimientos funcionales y no funcionales del proceso seleccionado.", "Matriz de requerimientos priorizada."],
                ["Arquitectura", "Diseñar la estructura cliente-servidor y el flujo de datos de la solución.", "Diagrama de arquitectura y explicación de componentes."],
                ["Backend", "Implementar servicios REST para gestionar las entidades principales del sistema.", "Rutas, controladores, validaciones y documentación API."],
                ["Frontend", "Construir interfaces web que permitan ejecutar los flujos principales del usuario.", "Pantallas funcionales, formularios y consumo de API."],
                ["Datos", "Modelar y persistir información usando una base de datos acorde al dominio.", "Modelo de datos, colecciones/tablas y operaciones CRUD."],
                ["Calidad", "Validar integración, usabilidad básica y manejo de errores.", "Casos de prueba, resultados y correcciones."],
            ],
            [1.05 * inch, 3.35 * inch, 1.9 * inch],
        )
    )

    story += section("4. Alcance del proyecto")
    story.append(
        p(
            "El alcance delimita el proyecto. Indica qué se entregará, qué funcionalidades son obligatorias, cuáles son deseables y qué elementos quedan fuera. Esta sección es crítica porque protege al equipo de prometer más de lo que puede construir y ayuda al profesor a evaluar coherencia entre propuesta, avance y entrega final.",
        )
    )
    story.append(
        p(
            "En Desarrollo de Software IX, el alcance debe ser compatible con un proyecto de aprendizaje: suficientemente amplio para integrar frontend, backend y datos; suficientemente acotado para que el equipo pueda completarlo con calidad. Un alcance sano evita sistemas gigantescos como “un ERP completo” o “una red social total” y prefiere un flujo central completo con extensiones secundarias.",
        )
    )
    story += subsection("4.1 Dentro y fuera del alcance")
    story.append(
        table(
            [
                ["Categoría", "Dentro del alcance", "Fuera del alcance"],
                ["Usuarios", "Roles esenciales para el flujo principal.", "Roles administrativos complejos sin uso real en el MVP."],
                ["Funcionalidades", "CRUD principal, autenticación si aplica, reportes básicos y validaciones.", "Automatizaciones avanzadas, analítica compleja o integraciones no críticas."],
                ["Integraciones", "Una integración externa bien justificada, como pasarela simulada o API pública.", "Dependencias externas que bloquean el proyecto si no se obtiene acceso."],
                ["Datos", "Modelo de datos necesario para la operación del MVP.", "Históricos masivos, migraciones reales o inteligencia de negocio completa."],
                ["Seguridad", "Cifrado de contraseñas, JWT, validación y control básico de acceso.", "Auditorías completas, cumplimiento regulatorio avanzado o pentesting formal."],
            ],
            [1.15 * inch, 2.65 * inch, 2.55 * inch],
        )
    )
    story += subsection("4.2 MVP como herramienta de alcance")
    story.append(
        p(
            "El Producto Mínimo Viable o MVP es una versión mínima pero funcional de la solución. No es una maqueta incompleta ni un prototipo visual sin backend. En este curso, un MVP debe permitir que el usuario complete al menos un flujo de valor de inicio a fin: ingresar, crear o consultar datos, ejecutar una acción y observar un resultado persistido o procesado.",
        )
    )
    story.append(
        callout(
            "Regla práctica del MVP Full Stack",
            "Si se apaga el backend o se elimina la base de datos y la aplicación sigue pareciendo funcionar, probablemente no es un MVP Full Stack real. El flujo principal debe depender de la integración entre capas.",
            fill=colors.HexColor("#FFF7E0"),
        )
    )

    story += section("5. Análisis de requerimientos")
    story.append(
        p(
            "Los requerimientos describen lo que el sistema debe hacer y las condiciones bajo las cuales debe operar. Son el puente entre el problema y la arquitectura. Sin requerimientos, el diseño se vuelve una colección de gustos técnicos; con requerimientos claros, cada tecnología y cada componente puede justificarse.",
        )
    )
    story += subsection("5.1 Requerimientos funcionales")
    story.append(
        p(
            "Los requerimientos funcionales especifican comportamientos del sistema. Normalmente se redactan desde la perspectiva del usuario o del sistema: registrar, consultar, actualizar, eliminar, autenticar, notificar, generar, validar, filtrar, exportar o integrar.",
        )
    )
    story.append(
        table(
            [
                ["ID", "Requerimiento funcional", "Prioridad", "Criterio de aceptación"],
                ["RF-01", "El sistema debe permitir registrar usuarios con datos mínimos y validación de correo.", "Alta", "No se puede crear un usuario sin correo válido ni contraseña segura."],
                ["RF-02", "El usuario autenticado debe crear una solicitud con categoría, descripción y evidencia opcional.", "Alta", "La solicitud queda persistida y visible en su historial."],
                ["RF-03", "El administrador debe cambiar el estado de una solicitud.", "Media", "El cambio actualiza la base de datos y se refleja en la vista del usuario."],
                ["RF-04", "El sistema debe permitir filtrar solicitudes por estado y fecha.", "Media", "La lista responde al filtro sin recargar manualmente datos inconsistentes."],
            ],
            [0.65 * inch, 3.0 * inch, 0.85 * inch, 1.8 * inch],
        )
    )
    story += subsection("5.2 Requerimientos no funcionales")
    story.append(
        p(
            "Los requerimientos no funcionales describen atributos de calidad: seguridad, rendimiento, disponibilidad, usabilidad, mantenibilidad, escalabilidad, accesibilidad, compatibilidad y trazabilidad. En proyectos académicos suelen descuidarse, pero son esenciales para demostrar criterio de ingeniería.",
        )
    )
    story.append(
        table(
            [
                ["Categoría", "Ejemplo de requerimiento no funcional", "Cómo se evidencia"],
                ["Seguridad", "Las contraseñas deben almacenarse cifradas y las rutas privadas deben requerir token válido.", "Uso de bcrypt/JWT o mecanismo equivalente; pruebas de acceso no autorizado."],
                ["Usabilidad", "El usuario debe completar el flujo principal sin instrucciones externas.", "Interfaz con navegación clara, mensajes de error y estados visibles."],
                ["Rendimiento", "Las consultas principales deben responder en un tiempo razonable para el conjunto de datos esperado.", "Pruebas con datos semilla y mediciones básicas."],
                ["Mantenibilidad", "El backend debe separar rutas, controladores, modelos y servicios.", "Estructura de carpetas y nombres consistentes."],
                ["Confiabilidad", "El sistema debe manejar errores de validación y errores del servidor sin romper la interfaz.", "Respuestas HTTP apropiadas y mensajes de UI controlados."],
            ],
            [1.15 * inch, 3.25 * inch, 1.95 * inch],
        )
    )

    story += section("6. Diseño de la arquitectura Full Stack")
    story.append(
        p(
            "La arquitectura describe cómo se organiza la solución. En este curso, la arquitectura mínima suele incluir una aplicación frontend, un servidor backend, una base de datos y posibles servicios externos. La arquitectura no es solo un dibujo: es una explicación de responsabilidades, comunicación, datos, seguridad y decisiones de tecnología.",
        )
    )
    story.append(
        table(
            [
                ["Capa", "Responsabilidad", "Decisiones típicas"],
                ["Frontend", "Presentar interfaz, capturar acciones del usuario, validar datos básicos y consumir APIs.", "React, componentes, rutas, manejo de estado, formularios, estilos."],
                ["Backend", "Exponer servicios, aplicar reglas de negocio, autenticar, validar, coordinar persistencia e integraciones.", "Node.js, Express, REST, middlewares, controladores, JWT."],
                ["Base de datos", "Persistir entidades del dominio y permitir consultas coherentes.", "MongoDB, Mongoose, modelos, índices, relaciones por referencia o embebidas."],
                ["Servicios externos", "Ampliar capacidades con pagos, IA, correo, mapas u otras APIs.", "API keys, manejo de errores, límites, simulación si no hay acceso real."],
            ],
            [1.05 * inch, 3.15 * inch, 2.15 * inch],
        )
    )
    story += subsection("6.1 Flujo cliente-servidor")
    story.append(
        p(
            "El flujo básico inicia cuando el usuario interactúa con una pantalla. El frontend envía una solicitud HTTP al backend. El backend valida la solicitud, ejecuta reglas de negocio, consulta o modifica la base de datos y devuelve una respuesta. El frontend interpreta esa respuesta y actualiza la interfaz. Este ciclo debe estar claro desde la formulación porque afecta requerimientos, rutas, modelos y pruebas.",
        )
    )
    story.append(
        callout(
            "Descripción textual de arquitectura",
            "Usuario → Interfaz React → Servicio HTTP del frontend → API Express → Middleware de autenticación/validación → Controlador → Modelo Mongoose → MongoDB → Respuesta JSON → Actualización de UI.",
            fill=GRAY_LIGHT,
        )
    )
    story += subsection("6.2 Diseño preliminar de API")
    story.append(
        p(
            "Diseñar la API antes de implementarla evita improvisación. La API define recursos, rutas, métodos HTTP, entradas, salidas y errores. Para un MVP, no se necesita una documentación extensa tipo OpenAPI completa, pero sí una tabla clara de endpoints principales.",
        )
    )
    story.append(
        table(
            [
                ["Método", "Ruta", "Uso", "Entrada", "Respuesta esperada"],
                ["POST", "/api/auth/login", "Autenticar usuario.", "correo, contraseña", "token, datos básicos del usuario"],
                ["GET", "/api/solicitudes", "Listar solicitudes visibles.", "token, filtros opcionales", "arreglo de solicitudes"],
                ["POST", "/api/solicitudes", "Crear solicitud.", "categoría, descripción", "solicitud creada"],
                ["PUT", "/api/solicitudes/:id/estado", "Cambiar estado.", "nuevo estado", "solicitud actualizada"],
                ["DELETE", "/api/solicitudes/:id", "Eliminar o cancelar solicitud.", "id", "confirmación o estado final"],
            ],
            [0.78 * inch, 1.45 * inch, 1.48 * inch, 1.28 * inch, 1.36 * inch],
        )
    )
    story += subsection("6.3 Diseño preliminar de base de datos")
    story.append(
        p(
            "El diseño de datos debe partir de entidades del dominio, no de pantallas. Una entidad representa algo que el sistema necesita recordar: usuario, solicitud, reserva, producto, pedido, pago, comentario, archivo o notificación. En MongoDB, el equipo debe decidir qué datos se embeben, qué datos se referencian y qué validaciones se aplican con Mongoose.",
        )
    )
    story.append(
        table(
            [
                ["Entidad", "Campos esenciales", "Relaciones o notas"],
                ["Usuario", "nombre, correo, hashPassword, rol, estado", "Puede crear solicitudes; puede administrar según rol."],
                ["Solicitud", "titulo, descripcion, categoria, estado, prioridad, creador, fechas", "Referencia al usuario creador; historial opcional."],
                ["Comentario", "solicitudId, autor, texto, fecha", "Puede embebirse en solicitud si el volumen es bajo."],
                ["Evidencia", "solicitudId, nombreArchivo, url, tipo", "Puede almacenarse como metadato si el archivo vive en otro servicio."],
            ],
            [1.05 * inch, 3.0 * inch, 2.25 * inch],
        )
    )

    story += section("7. Diseño de interfaz frontend")
    story.append(
        p(
            "El diseño de interfaz en este capítulo no exige una maqueta perfecta, pero sí una definición clara de pantallas y flujos. La interfaz debe reflejar las tareas del usuario, no solo la estructura de la base de datos. Cada pantalla debe tener un propósito, datos requeridos, acciones disponibles y estados de error o carga.",
        )
    )
    story.append(
        table(
            [
                ["Pantalla", "Propósito", "Elementos mínimos"],
                ["Inicio / dashboard", "Orientar al usuario y mostrar información relevante.", "Resumen, accesos principales, estado de sesión."],
                ["Listado", "Consultar registros y aplicar filtros.", "Tabla o tarjetas, filtros, búsqueda, paginación si aplica."],
                ["Formulario", "Crear o editar información.", "Campos validados, mensajes de error, acciones guardar/cancelar."],
                ["Detalle", "Ver información completa y acciones contextuales.", "Datos principales, historial, cambios de estado."],
                ["Autenticación", "Controlar acceso a funciones privadas.", "Login, registro si aplica, recuperación opcional."],
            ],
            [1.35 * inch, 2.3 * inch, 2.7 * inch],
        )
    )
    story.append(
        p(
            "Una buena práctica es construir un mapa de navegación antes de programar. Este mapa debe indicar qué rutas existen, qué rol puede acceder a cada una y qué datos consume. En React, esto se traduce en rutas, componentes, hooks y servicios de API.",
        )
    )

    story += section("8. Desarrollo y pruebas")
    story.append(
        p(
            "La última unidad del módulo conecta formulación con ejecución. El equipo debe proponer cómo desarrollará y verificará la solución. Aunque el desarrollo completo ocurra en módulos posteriores, desde el inicio deben existir criterios de calidad: qué se probará, qué se considerará terminado y cómo se manejarán errores.",
        )
    )
    story += subsection("8.1 Plan mínimo de desarrollo")
    story.append(
        numbered(
            [
                "Preparar repositorio, estructura de carpetas, convenciones de ramas y archivo README.",
                "Configurar backend con Node.js, Express, variables de entorno y conexión a base de datos.",
                "Definir modelos principales y datos semilla.",
                "Implementar endpoints del flujo principal con validación y manejo de errores.",
                "Configurar frontend con React, rutas, layout base y servicios HTTP.",
                "Conectar pantallas al backend y validar flujo completo.",
                "Agregar seguridad mínima, documentación y pruebas de aceptación.",
            ]
        )
    )
    story += subsection("8.2 Pruebas que deben planificarse")
    story.append(
        table(
            [
                ["Tipo de prueba", "Pregunta", "Ejemplo"],
                ["Funcional", "¿El flujo cumple el requerimiento?", "Crear solicitud y verla en el listado."],
                ["Integración", "¿Frontend, backend y base de datos se comunican correctamente?", "Formulario React envía POST y MongoDB persiste."],
                ["Validación", "¿El sistema rechaza datos inválidos?", "Correo inválido o campos obligatorios vacíos."],
                ["Seguridad básica", "¿Las rutas privadas bloquean usuarios no autenticados?", "GET privado sin token responde 401."],
                ["Usabilidad", "¿El usuario entiende qué hacer y qué ocurrió?", "Mensajes de error, confirmaciones y estados de carga."],
            ],
            [1.25 * inch, 2.55 * inch, 2.5 * inch],
        )
    )
    story.append(
        callout(
            "Criterio de cierre del módulo",
            "Un proyecto está bien formulado cuando otra persona puede leer la propuesta y entender qué se construirá, por qué, para quién, qué incluye, qué no incluye, cómo se conectan sus capas y cómo se validará.",
            fill=BLUE_LIGHT,
        )
    )

    story += section("9. Caso guía: sistema de reservas de laboratorio")
    story.append(
        p(
            "Para ilustrar el proceso, se presenta un caso guía breve. No es un proyecto obligatorio, sino un ejemplo de cómo aplicar los elementos del capítulo.",
        )
    )
    story += subsection("9.1 Problema")
    story.append(
        p(
            "En una facultad universitaria, la reserva de laboratorios y equipos se coordina mediante mensajes, hojas compartidas y confirmaciones manuales. Esto provoca choques de horario, poca visibilidad de disponibilidad y dificultad para auditar quién solicitó un recurso. Se requiere una aplicación web que centralice reservas, disponibilidad y aprobación básica.",
        )
    )
    story += subsection("9.2 Objetivo y alcance")
    story.append(
        p(
            "Objetivo general: diseñar e implementar una aplicación web Full Stack para gestionar reservas de laboratorios, permitiendo que estudiantes o docentes soliciten espacios y que un administrador apruebe, rechace o consulte solicitudes.",
        )
    )
    story.append(
        table(
            [
                ["Incluye", "No incluye en el MVP"],
                ["Registro/autenticación básica de usuarios.", "Integración real con cerraduras inteligentes o sensores físicos."],
                ["Calendario o listado de disponibilidad.", "Optimización automática de horarios."],
                ["Solicitud, aprobación y rechazo de reservas.", "Facturación, pagos o reservas multi-campus complejas."],
                ["Panel administrativo y estados.", "Aplicación móvil nativa."],
            ],
            [3.1 * inch, 3.1 * inch],
        )
    )
    story += subsection("9.3 Arquitectura inicial")
    story.append(
        p(
            "Frontend React con rutas para login, dashboard, calendario/listado, formulario de reserva y panel administrativo. Backend Express con rutas REST para autenticación, laboratorios y reservas. Base de datos MongoDB con colecciones de usuarios, laboratorios y reservas. Seguridad básica con hash de contraseñas y JWT para rutas privadas.",
        )
    )
    story.append(
        table(
            [
                ["Recurso", "Endpoints mínimos"],
                ["auth", "POST /api/auth/register, POST /api/auth/login, GET /api/auth/me"],
                ["laboratorios", "GET /api/laboratorios, POST /api/laboratorios"],
                ["reservas", "GET /api/reservas, POST /api/reservas, PUT /api/reservas/:id/estado"],
            ],
            [1.2 * inch, 5.1 * inch],
        )
    )

    story += section("10. Plantilla de entrega para el estudiante")
    story.append(
        p(
            "La siguiente plantilla puede usarse como estructura mínima para la primera entrega de formulación. Cada sección debe completarse con información concreta del proyecto seleccionado.",
        )
    )
    story += checklist(
        [
            "Título del proyecto y nombre de integrantes.",
            "Descripción del contexto y problema.",
            "Usuarios o actores principales.",
            "Objetivo general.",
            "Cuatro a seis objetivos específicos.",
            "Alcance: dentro, fuera, supuestos y restricciones.",
            "Requerimientos funcionales priorizados.",
            "Requerimientos no funcionales priorizados.",
            "Arquitectura propuesta: frontend, backend, base de datos e integraciones.",
            "Tabla preliminar de endpoints.",
            "Modelo preliminar de datos.",
            "Pantallas principales o mapa de navegación.",
            "Plan de desarrollo por hitos.",
            "Plan básico de pruebas y criterios de aceptación.",
        ]
    )
    story.append(Spacer(1, 6))
    story.append(
        callout(
            "Recomendación de formato",
            "La entrega debe ser clara y auditable. Evitar párrafos genéricos, capturas sin explicación o listas de tecnologías sin justificación. Cada decisión técnica debe poder conectarse con un requerimiento o una restricción.",
            fill=GRAY_LIGHT,
        )
    )

    story += section("11. Actividades sugeridas")
    story += subsection("Actividad 1: diagnóstico de problema")
    story.append(
        p(
            "Seleccione un proceso real o plausible que pueda mejorarse con una aplicación web. Redacte tres versiones del problema: una versión inicial, una versión corregida y una versión final usando la plantilla de contexto, proceso, dificultad, consecuencia y oportunidad.",
        )
    )
    story += subsection("Actividad 2: matriz de requerimientos")
    story.append(
        p(
            "Construya una matriz con al menos ocho requerimientos funcionales y cinco no funcionales. Cada requerimiento debe tener prioridad, criterio de aceptación y componente relacionado.",
        )
    )
    story += subsection("Actividad 3: arquitectura defendible")
    story.append(
        p(
            "Dibuje o describa la arquitectura inicial. Luego justifique por qué cada capa existe, qué datos maneja y qué errores debe controlar. La explicación debe incluir al menos un flujo completo de usuario desde la interfaz hasta la base de datos.",
        )
    )
    story += subsection("Actividad 4: revisión entre pares")
    story.append(
        p(
            "Intercambie la propuesta con otro equipo y responda: ¿el problema está claro?, ¿el alcance es viable?, ¿los requerimientos son verificables?, ¿la arquitectura conecta con los requerimientos?, ¿hay riesgos técnicos no reconocidos?",
        )
    )

    story += section("12. Rúbrica sugerida para evaluar la formulación")
    story.append(
        table(
            [
                ["Criterio", "Excelente", "Satisfactorio", "Insuficiente"],
                ["Problema y contexto", "Problema específico, evidencia clara y usuarios definidos.", "Problema entendible pero con contexto parcial.", "Problema genérico o confundido con la solución."],
                ["Objetivos y alcance", "Objetivos medibles y alcance viable con exclusiones claras.", "Objetivos adecuados pero con límites incompletos.", "Objetivos vagos o alcance sobredimensionado."],
                ["Requerimientos", "Funcionales y no funcionales priorizados con criterios de aceptación.", "Lista básica con algunos criterios verificables.", "Requerimientos ambiguos, incompletos o no priorizados."],
                ["Arquitectura", "Capas, datos, API e integraciones coherentes y justificadas.", "Arquitectura general entendible con algunas omisiones.", "Tecnologías listadas sin relación clara con el problema."],
                ["Pruebas y calidad", "Plan de validación conectado con requerimientos y riesgos.", "Pruebas básicas del flujo principal.", "No hay criterios claros para validar la solución."],
            ],
            [1.25 * inch, 1.95 * inch, 1.65 * inch, 1.55 * inch],
        )
    )

    story += section("13. Cierre del capítulo")
    story.append(
        p(
            "La formulación de proyectos Full Stack es una práctica de ingeniería. Obliga a pensar antes de programar, a justificar tecnologías, a reconocer límites y a definir cómo se validará la solución. En los siguientes módulos, las decisiones tomadas aquí se convertirán en configuración del entorno, servicios backend, modelos de datos, interfaces React, seguridad e integración.",
        )
    )
    story.append(
        p(
            "El estudiante que domina este primer capítulo no solo puede proponer una aplicación; puede explicar por qué esa aplicación debe existir, qué problema resuelve, cómo se estructura y cómo se sabrá que cumple su propósito.",
        )
    )
    story.append(
        callout(
            "Pregunta final de reflexión",
            "Si otro equipo recibiera su documento de formulación, ¿podría construir el mismo MVP sin pedir explicaciones adicionales? Si la respuesta es no, la formulación todavía necesita precisión.",
            fill=colors.HexColor("#EAF7EF"),
        )
    )

    story.append(PageBreak())
    story += section("Anexo A. Formato resumido de propuesta")
    story.append(
        table(
            [
                ["Campo", "Contenido esperado"],
                ["Título", "Nombre breve y claro del proyecto."],
                ["Problema", "Contexto, usuarios, proceso actual, dificultad y consecuencia."],
                ["Objetivo general", "Solución Full Stack y beneficio principal."],
                ["Objetivos específicos", "Resultados verificables de análisis, arquitectura, backend, frontend, datos y pruebas."],
                ["Alcance", "Incluye, excluye, supuestos y restricciones."],
                ["Requerimientos", "Funcionales y no funcionales con prioridad y criterio de aceptación."],
                ["Arquitectura", "Capas, tecnologías, flujo de datos, seguridad e integraciones."],
                ["API", "Tabla de endpoints mínimos."],
                ["Datos", "Entidades principales y relaciones."],
                ["Interfaz", "Pantallas y rutas principales."],
                ["Pruebas", "Casos de aceptación para el flujo principal."],
            ],
            [1.55 * inch, 4.75 * inch],
        )
    )
    story += section("Anexo B. Glosario básico")
    story.append(
        table(
            [
                ["Término", "Definición operativa"],
                ["Full Stack", "Enfoque de desarrollo que integra interfaz, lógica del servidor y persistencia de datos."],
                ["MVP", "Versión mínima funcional que permite validar el flujo central de valor."],
                ["API REST", "Conjunto de endpoints HTTP para consultar o modificar recursos."],
                ["Middleware", "Función intermedia que procesa solicitudes antes de llegar al controlador."],
                ["JWT", "Token usado para representar una sesión o identidad en rutas protegidas."],
                ["CRUD", "Operaciones de crear, leer, actualizar y eliminar información."],
                ["Requerimiento no funcional", "Condición de calidad o restricción bajo la cual debe operar el sistema."],
            ],
            [1.6 * inch, 4.7 * inch],
        )
    )
    return story


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = CourseDocTemplate(str(OUT), title="Capítulo 1 - Formulación de Proyectos Full Stack")
    story = build_story()
    doc.multiBuild(story)
    print(OUT)


if __name__ == "__main__":
    main()
