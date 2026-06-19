"""Módulo extra: construcción de servidores MCP para proyectos propios.

Base documental del próximo proyecto del curso: exponer el comercio
electrónico del Parcial #2 como servidor MCP e integrarlo en Claude Code
y ChatGPT. Corte de actualidad: junio 2026.
"""
from __future__ import annotations

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

from diagrams import DIAGRAMS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "materials" / "modulos" / "MODULO_EXTRA_AGENTES_DESARROLLO_IA" / "MODULO_EXTRA_MCP_PROYECTOS_JUNIO_2026.pdf"

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

    canvas.setFont("Helvetica-Bold", 26)
    canvas.drawString(LEFT, PAGE_H - 2.1 * inch, "Módulo extra")
    canvas.setFont("Helvetica-Bold", 21)
    canvas.drawString(LEFT, PAGE_H - 2.55 * inch, "Servidores MCP para tus proyectos:")
    canvas.drawString(LEFT, PAGE_H - 2.9 * inch, "construcción e integración con")
    canvas.drawString(LEFT, PAGE_H - 3.25 * inch, "Claude Code y ChatGPT")

    canvas.setFillColor(colors.HexColor("#D7EAF7"))
    canvas.setFont("Helvetica", 12.5)
    canvas.drawString(
        LEFT,
        PAGE_H - 3.8 * inch,
        "Desarrollo de Software IX · Código 1493 · Actualizado a junio 2026",
    )

    canvas.setFillColor(colors.HexColor("#FFFFFF"))
    canvas.setStrokeColor(colors.HexColor("#5EA2D1"))
    canvas.roundRect(LEFT, 1.35 * inch, CONTENT_W, 1.85 * inch, 10, stroke=1, fill=0)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(LEFT + 0.28 * inch, 2.75 * inch, "Propósito del módulo")
    canvas.setFont("Helvetica", 10.5)
    lines = [
        "Explicar el Model Context Protocol y guiar la construcción de un servidor MCP",
        "sobre un proyecto propio — el comercio electrónico del Parcial #2 — y su",
        "integración en Claude Code y ChatGPT. Este material es la base del próximo proyecto.",
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
    canvas.drawString(LEFT, PAGE_H - 0.36 * inch, "Desarrollo de Software IX · Módulo extra MCP")
    canvas.drawRightString(PAGE_W - RIGHT, 0.38 * inch, f"Página {doc.page}")
    canvas.restoreState()


class GuideDoc(BaseDocTemplate):
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


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Lead", parent=styles["BodyText"], fontName="Helvetica", fontSize=11.5, leading=16, textColor=INK, spaceAfter=10))
styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.2, leading=14.2, textColor=INK, spaceAfter=8))
styles.add(ParagraphStyle(name="H1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=BLUE, spaceBefore=16, spaceAfter=9))
styles.add(ParagraphStyle(name="H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13.2, leading=16, textColor=BLUE_DARK, spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name="CalloutTitle", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=10.2, leading=13, textColor=BLUE_DARK, spaceAfter=3))
styles.add(ParagraphStyle(name="CalloutBody", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.3, textColor=INK, spaceAfter=0))
styles.add(ParagraphStyle(name="TableHead", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=colors.white, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="TableCell", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.4, leading=10.8, textColor=INK, spaceAfter=0))
styles.add(ParagraphStyle(name="CodeBlock", parent=styles["BodyText"], fontName="Courier", fontSize=8.4, leading=11.2, textColor=INK, backColor=colors.HexColor("#F4F6F8"), borderPadding=6, spaceAfter=8))


def p(text: str, style: str = "Body") -> Paragraph:
    return Paragraph(clean(text), styles[style])


def code(text: str) -> KeepTogether:
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>").replace(" ", "&nbsp;")
    return KeepTogether([Paragraph(escaped, styles["CodeBlock"])])


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


def callout(title: str, body: str):
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


def table(data, fractions):
    widths = [f * CONTENT_W for f in fractions]
    converted = []
    for r, row in enumerate(data):
        style = "TableHead" if r == 0 else "TableCell"
        converted.append([p(str(cell), style) for cell in row])
    t = Table(converted, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#B8C2CC")),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D3DCE6")),
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def build_story():
    story = [NextPageTemplate("body"), PageBreak()]

    story.append(p("1. Panorama: por qué existe MCP", "H1"))
    story.append(p(
        "En el módulo extra de agentes vimos cómo Claude Code, Codex y otros agentes ayudan a "
        "construir software. Este módulo invierte la pregunta: ¿cómo logramos que esos agentes "
        "puedan operar NUESTRO software? La respuesta de la industria es el Model Context Protocol "
        "(MCP), un protocolo abierto publicado por Anthropic en noviembre de 2024 y adoptado desde "
        "2025 por OpenAI, Google y el resto del ecosistema. MCP estandariza cómo una aplicación de "
        "IA descubre y usa capacidades externas: datos, herramientas y acciones.", "Lead"))
    story.append(p(
        "Antes de MCP, conectar un asistente con un sistema externo exigía una integración a la "
        "medida por cada par asistente-sistema: N asistentes por M sistemas = N×M integraciones. "
        "MCP reduce el problema a N+M: cada asistente implementa el protocolo una vez como cliente, "
        "cada sistema lo implementa una vez como servidor, y cualquier combinación funciona. Es la "
        "misma jugada que estandarizó los puertos de hardware — por eso se le apoda el "
        "\"USB-C de las aplicaciones de IA\".", "Body"))
    story.append(callout(
        "El proyecto que sigue",
        "Este material es la base del próximo proyecto del curso: construir un servidor MCP sobre el "
        "comercio electrónico que desarrollaste en el Parcial #2, e integrarlo en Claude Code y "
        "ChatGPT, de modo que un agente pueda consultar tu catálogo, revisar órdenes y operar tu "
        "tienda conversando. El enunciado formal se publicará en Teams."))

    story.append(p("2. Arquitectura del protocolo", "H1"))
    story.append(p("2.1 Host, cliente y servidor", "H2"))
    story.append(p(
        "MCP define tres roles. El HOST es la aplicación de IA con la que interactúa el usuario "
        "(Claude Code, ChatGPT, un IDE). Dentro del host vive un CLIENTE MCP que mantiene la "
        "conexión. Del otro lado está el SERVIDOR MCP: un programa — frecuentemente pequeño — que "
        "expone capacidades de un sistema concreto. El modelo de lenguaje nunca toca tu base de "
        "datos: pide al host ejecutar una herramienta, el cliente la invoca en el servidor, y el "
        "servidor decide qué hacer y qué responder. La comunicación usa JSON-RPC 2.0.", "Body"))
    story.append(KeepTogether([DIAGRAMS["mcp_arquitectura"]()]))
    story.append(Spacer(1, 8))
    story.append(p("2.2 Las tres primitivas", "H2"))
    story.append(table([
        ["Primitiva", "Qué es", "Ejemplo en el comercio electrónico"],
        ["Tools", "Acciones que el MODELO decide invocar: funciones con nombre, descripción y esquema de entrada.", "buscar_productos, crear_orden, estado_orden, resumen_ventas."],
        ["Resources", "Datos de solo lectura que la APLICACIÓN puede adjuntar como contexto.", "El catálogo en JSON, la política de envíos, el esquema de la base."],
        ["Prompts", "Plantillas reutilizables que el USUARIO invoca explícitamente.", "\"Analiza las ventas de la semana y sugiere promociones\"."],
    ], [0.16, 0.42, 0.42]))
    story.append(p(
        "La distinción importa para el diseño: una herramienta es algo que el modelo puede decidir "
        "ejecutar por su cuenta dentro de una conversación; un recurso es contexto que se aporta; "
        "un prompt es un atajo de usuario. La mayor parte del valor de un MCP de proyecto está en "
        "las tools bien diseñadas.", "Body"))
    story.append(KeepTogether([DIAGRAMS["mcp_flujo_tool"]()]))
    story.append(Spacer(1, 8))
    story.append(p("2.3 Transportes: stdio y HTTP", "H2"))
    story.append(table([
        ["Transporte", "Cómo corre el servidor", "Cuándo usarlo"],
        ["stdio", "El host lanza el servidor como proceso local y conversan por entrada/salida estándar.", "Desarrollo local y Claude Code: simple, sin red, sin autenticación adicional."],
        ["Streamable HTTP", "El servidor corre como servicio web (propio o en la nube) y los clientes se conectan por HTTPS.", "Integraciones remotas: ChatGPT solo acepta servidores remotos; permite compartir un MCP entre varios usuarios."],
    ], [0.18, 0.42, 0.40]))

    story.append(p("3. Diseñar el MCP de tu proyecto", "H1"))
    story.append(p(
        "Antes del código viene una decisión de diseño: ¿qué operaciones del comercio electrónico "
        "merecen ser herramientas? La tentación es exponer la API completa; el buen diseño expone "
        "un conjunto pequeño de operaciones con INTENCIÓN clara, porque el modelo elige qué "
        "herramienta usar leyendo sus nombres y descripciones — una herramienta ambigua se usa mal "
        "o no se usa.", "Body"))
    story.append(bullet([
        "Nombra por intención del dominio, no por endpoint: buscar_productos mejor que get_api_products_v1.",
        "Describe para el modelo: la descripción debe decir qué hace, qué espera y qué devuelve. Es documentación que un LLM va a leer literalmente.",
        "Esquemas estrictos: cada parámetro con tipo y validación (Zod). El modelo comete menos errores cuando el contrato es preciso.",
        "Separa lectura de escritura: consultar el catálogo es inocuo; crear órdenes o cambiar precios merece confirmación o quedar fuera de la primera versión.",
        "Respuestas compactas y útiles: el resultado vuelve al contexto del modelo; una lista de 500 productos completos desborda — devuelve los 10 más relevantes con los campos que importan.",
    ]))
    story.append(callout(
        "Reutiliza tu backend",
        "El servidor MCP no reemplaza tu API REST: la consume. Cada tool llama a los endpoints (o "
        "servicios) que ya construiste con Hono/Express y MongoDB. Así la lógica de negocio sigue "
        "viviendo en un solo lugar y el MCP es una capa delgada de traducción — el mismo principio "
        "de adaptadores del Capítulo 9."))

    story.append(p("4. Construir el servidor con el SDK de TypeScript", "H1"))
    story.append(p("4.1 Proyecto y dependencias", "H2"))
    story.append(code(
        "bun init mcp-tienda\n"
        "bun add @modelcontextprotocol/sdk zod"))
    story.append(p("4.2 Servidor con una tool de lectura", "H2"))
    story.append(code(
        "// src/index.ts\n"
        "import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'\n"
        "import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'\n"
        "import { z } from 'zod'\n\n"
        "const server = new McpServer({ name: 'mcp-tienda', version: '1.0.0' })\n\n"
        "server.registerTool(\n"
        "  'buscar_productos',\n"
        "  {\n"
        "    title: 'Buscar productos',\n"
        "    description: 'Busca productos del catálogo por texto y precio máximo. ' +\n"
        "                 'Devuelve hasta 10 resultados con id, nombre, precio y stock.',\n"
        "    inputSchema: {\n"
        "      consulta: z.string().describe('Texto a buscar en nombre y descripción'),\n"
        "      precioMax: z.number().optional().describe('Precio máximo en USD'),\n"
        "    },\n"
        "  },\n"
        "  async ({ consulta, precioMax }) => {\n"
        "    const url = new URL(`${process.env.TIENDA_API}/api/products`)\n"
        "    url.searchParams.set('q', consulta)\n"
        "    if (precioMax) url.searchParams.set('maxPrice', String(precioMax))\n"
        "    const res = await fetch(url)\n"
        "    const productos = await res.json()\n"
        "    return {\n"
        "      content: [{ type: 'text', text: JSON.stringify(productos.slice(0, 10)) }],\n"
        "    }\n"
        "  }\n"
        ")\n\n"
        "await server.connect(new StdioServerTransport())"))
    story.append(p(
        "El patrón se repite para cada herramienta: registerTool recibe el nombre, los metadatos "
        "(título, descripción y esquema Zod de entrada) y el manejador async que ejecuta la "
        "operación — aquí, llamando a la API del proyecto — y devuelve contenido. Una tool de "
        "escritura como crear_orden sigue la misma forma, validando con Zod los items y devolviendo "
        "el identificador y total de la orden creada.", "Body"))
    story.append(p("4.3 Probar con el Inspector", "H2"))
    story.append(p(
        "Antes de conectar ningún asistente, el MCP Inspector — la herramienta oficial de "
        "depuración — permite lanzar el servidor, listar sus tools, invocarlas a mano y ver las "
        "respuestas crudas:", "Body"))
    story.append(code("npx @modelcontextprotocol/inspector bun src/index.ts"))
    story.append(p(
        "El flujo de prueba mínimo: verificar que las tools aparecen con sus descripciones, invocar "
        "cada una con entradas válidas e inválidas (el esquema debe rechazar las inválidas), y "
        "confirmar que las respuestas son compactas y correctas contra la base real del proyecto.", "Body"))

    story.append(p("5. Integración en Claude Code", "H1"))
    story.append(p(
        "Claude Code consume servidores MCP locales por stdio. Hay dos formas de registrarlo. La "
        "rápida, desde la terminal:", "Body"))
    story.append(code(
        "claude mcp add tienda -e TIENDA_API=http://localhost:3000 -- bun src/index.ts"))
    story.append(p(
        "La recomendada para el proyecto: un archivo .mcp.json en la raíz del repositorio, que se "
        "versiona en Git y hace que cualquier integrante del equipo (y el profesor al clonar) tenga "
        "el servidor disponible automáticamente:", "Body"))
    story.append(code(
        "// .mcp.json (raíz del repo)\n"
        "{\n"
        "  \"mcpServers\": {\n"
        "    \"tienda\": {\n"
        "      \"command\": \"bun\",\n"
        "      \"args\": [\"mcp/src/index.ts\"],\n"
        "      \"env\": { \"TIENDA_API\": \"http://localhost:3000\" }\n"
        "    }\n"
        "  }\n"
        "}"))
    story.append(p(
        "Dentro de Claude Code, el comando /mcp muestra los servidores conectados y sus "
        "herramientas. A partir de ahí, la conversación opera la tienda: \"¿qué productos tienen "
        "stock bajo 5?\", \"crea una orden de prueba con dos unidades del producto X\", \"resume "
        "las ventas de esta semana\" — el agente elige las tools, las invoca y razona sobre los "
        "resultados.", "Body"))

    story.append(p("6. Integración en ChatGPT", "H1"))
    story.append(p(
        "ChatGPT integra MCP a través de sus apps/connectors (los connectors fueron renombrados a "
        "apps en diciembre de 2025). A diferencia de Claude Code, ChatGPT NO lanza procesos "
        "locales: exige un servidor MCP REMOTO accesible por HTTPS con transporte Streamable HTTP. "
        "El camino:", "Body"))
    story.append(numbered([
        "Adaptar el servidor al transporte HTTP (el SDK trae StreamableHTTPServerTransport; el servidor pasa a ser una app web que puede convivir con tu API Hono).",
        "Desplegarlo con HTTPS público (el mismo proveedor donde vive tu API, o un túnel de desarrollo para demos).",
        "En ChatGPT: Settings → Apps & Connectors → activar Developer mode (disponible en planes Pro/Plus y Enterprise/Edu según la organización) → Create app/connector con la URL del servidor.",
        "Probar en una conversación habilitando la app: ChatGPT lista las tools del servidor y las invoca igual que Claude.",
    ]))
    story.append(callout(
        "Si tu plan de ChatGPT no permite connectors de desarrollador",
        "La integración con ChatGPT puede demostrarse con una cuenta del equipo que tenga Developer "
        "mode, o sustituirse en la demo por el MCP Inspector apuntando al servidor remoto — lo que "
        "evalúa el proyecto es que el servidor hable MCP por HTTP correctamente, no la suscripción."))
    story.append(p(
        "Un mismo código de servidor puede soportar ambos transportes: stdio para el trabajo local "
        "con Claude Code y HTTP para la integración remota — el núcleo (las tools) no cambia, solo "
        "la capa de conexión.", "Body"))

    story.append(p("7. Seguridad del servidor MCP", "H1"))
    story.append(bullet([
        "El servidor corre con TUS credenciales: el modelo no ve la llave de la base ni los secretos, pero todo lo que una tool permita, el modelo lo puede hacer. El control de daños se diseña en las tools, no en el prompt.",
        "Tools de escritura con freno: montos máximos, estados permitidos, modo prueba de la pasarela. Una tool crear_orden jamás debe poder cobrar una tarjeta real en la demo.",
        "Un servidor remoto sin autenticación es una API pública: protege el endpoint HTTP (token Bearer u OAuth) igual que protegiste las rutas privadas con JWT en el Capítulo 5.",
        "Valida las entradas con los esquemas Zod y trata las salidas hacia el modelo como datos, no como instrucciones: contenido malicioso en una descripción de producto podría intentar manipular al agente (inyección de prompt).",
        "Principio de mínima exposición: empieza con tools de lectura; agrega escritura solo donde el proyecto lo justifique y documenta cada una en el README.",
    ]))

    story.append(p("8. Lo que se espera del próximo proyecto", "H1"))
    story.append(p(
        "Como base de preparación — el enunciado formal con fechas, puntos y rúbrica se publicará "
        "en Teams — el proyecto consistirá en llevar tu comercio electrónico del Parcial #2 a la "
        "era agéntica:", "Body"))
    story.append(table([
        ["Componente", "Expectativa"],
        ["Servidor MCP", "Construido con @modelcontextprotocol/sdk + Zod sobre TU comercio electrónico, consumiendo tu API existente (no lógica duplicada)."],
        ["Tools", "Un conjunto pequeño y bien descrito que cubra lectura (catálogo, órdenes, métricas) y al menos una operación de escritura controlada."],
        ["Pruebas", "Evidencia con MCP Inspector: tools listadas, invocaciones válidas e inválidas."],
        ["Integración Claude Code", ".mcp.json versionado en el repo y demo conversacional operando la tienda."],
        ["Integración ChatGPT", "Servidor con transporte HTTP desplegado y conectado como app/connector (o demo equivalente vía Inspector remoto)."],
        ["Documentación", "README: arquitectura, tools con sus contratos, cómo correr local y remoto, y decisiones de seguridad."],
    ], [0.26, 0.74]))

    story.append(p("9. Actividades sugeridas", "H1"))
    story.append(bullet([
        "Levanta tu comercio electrónico del Parcial #2 y lista en papel las 5 operaciones más valiosas para un agente; clasifícalas en lectura/escritura.",
        "Implementa buscar_productos y pruébala en el Inspector con entradas válidas e inválidas.",
        "Conecta el servidor a Claude Code con .mcp.json y pide en conversación un análisis del catálogo que requiera 2 tools encadenadas.",
        "Adapta el servidor a Streamable HTTP y conéctalo (a ChatGPT con Developer mode, o al Inspector por URL).",
        "Escribe la sección de seguridad del README: qué expusiste, qué no, y por qué.",
    ]))

    story.append(p("10. Cierre y referencias", "H1"))
    story.append(p(
        "MCP cierra el arco del curso: construiste una aplicación Full Stack (frontend, backend, "
        "datos, pagos), aprendiste a desarrollarla con agentes, y ahora la conviertes en algo que "
        "los agentes pueden operar. Esa es la forma 2026 de \"integrar un sistema\": no solo "
        "exponer una API para otros programas, sino un contrato que las IAs entienden.", "Body"))
    story.append(Spacer(1, 6))
    story.append(p(
        "Referencias: modelcontextprotocol.io (especificación y SDKs) · github.com/modelcontextprotocol/typescript-sdk · "
        "docs de Claude Code (sección MCP) · developers.openai.com (Apps SDK y connectors MCP) · "
        "Capítulo 9 (integraciones externas) y módulo extra de agentes de este curso. "
        "Corte de actualidad: junio 2026 — el ecosistema MCP evoluciona rápido; verificar las docs oficiales al implementar.", "Body"))
    return story


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = GuideDoc(str(OUT))
    doc.build(build_story())
    print(f"OK -> {OUT}")


if __name__ == "__main__":
    main()
