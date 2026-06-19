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
OUT_DIR = ROOT / "materials" / "modulos" / "MODULO_EXTRA_AGENTES_DESARROLLO_IA"
OUT = OUT_DIR / "MODULO_EXTRA_AGENTES_CLAUDE_CODE_OPENCODE_CODEX_MAYO_2026.pdf"

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
GREEN_LIGHT = colors.HexColor("#EAF7EF")
GOLD_LIGHT = colors.HexColor("#FFF7E0")
RED_LIGHT = colors.HexColor("#FCEBEB")


def clean(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )


class ChapterTemplate(BaseDocTemplate):
    def __init__(self, filename: str):
        meta = {
            "title": "Modulo Extra - Agentes de desarrollo con IA",
            "chapter_label": "Modulo Extra",
        }
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
        if isinstance(flowable, Paragraph) and flowable.style.name == "H1":
            text = flowable.getPlainText()
            self.notify("TOCEntry", (0, text, self.page))
            self.canv.bookmarkPage(text)
            self.canv.addOutlineEntry(text, text, level=0, closed=False)


def cover_page(canvas, doc: ChapterTemplate):
    canvas.saveState()
    canvas.setFillColor(BLUE_DARK)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(LEFT, PAGE_H - 0.7 * inch, "UNIVERSIDAD TECNOLOGICA DE PANAMA")
    canvas.setFont("Helvetica", 9)
    canvas.drawString(LEFT, PAGE_H - 0.9 * inch, "Facultad de Ingenieria de Sistemas Computacionales")
    canvas.setStrokeColor(colors.HexColor("#9CC8E8"))
    canvas.setLineWidth(1.2)
    canvas.line(LEFT, PAGE_H - 1.1 * inch, PAGE_W - RIGHT, PAGE_H - 1.1 * inch)

    canvas.setFont("Helvetica-Bold", 30)
    canvas.drawString(LEFT, PAGE_H - 2.1 * inch, "Modulo Extra")
    canvas.setFont("Helvetica-Bold", 22)
    canvas.drawString(LEFT, PAGE_H - 2.55 * inch, "Agentes de desarrollo")
    canvas.drawString(LEFT, PAGE_H - 2.9 * inch, "con IA en 2026")
    canvas.setFillColor(colors.HexColor("#D7EAF7"))
    canvas.setFont("Helvetica", 12.5)
    canvas.drawString(LEFT, PAGE_H - 3.45 * inch, "Claude Code · OpenCode · Codex · MCP · Skills · Rules · Plugins")
    canvas.drawString(LEFT, PAGE_H - 3.7 * inch, "Desarrollo de Software IX · Codigo 1493 · Actualizado a mayo de 2026")

    canvas.setFillColor(colors.HexColor("#FFFFFF"))
    canvas.setStrokeColor(colors.HexColor("#5EA2D1"))
    canvas.roundRect(LEFT, 1.35 * inch, CONTENT_W, 1.85 * inch, 10, stroke=1, fill=0)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(LEFT + 0.28 * inch, 2.75 * inch, "Proposito del modulo")
    canvas.setFont("Helvetica", 10.5)
    lines = [
        "Orientar al estudiante para trabajar con agentes de desarrollo de forma profesional:",
        "configurar instrucciones, skills, subagentes, reglas, MCPs y plugins; mantener control",
        "humano; y exigir verificaciones que acerquen el resultado a production ready.",
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
    canvas.drawString(LEFT, PAGE_H - 0.36 * inch, "Desarrollo de Software IX · Modulo Extra")
    canvas.drawRightString(PAGE_W - RIGHT, 0.38 * inch, f"Pagina {doc.page}")
    canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Lead", parent=styles["BodyText"], fontName="Helvetica", fontSize=11.4, leading=16, textColor=INK, spaceAfter=10))
styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.0, leading=14.1, textColor=INK, spaceAfter=8))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.4, leading=10.8, textColor=GRAY, spaceAfter=5))
styles.add(ParagraphStyle(name="H1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=17.5, leading=21.5, textColor=BLUE, spaceBefore=16, spaceAfter=9))
styles.add(ParagraphStyle(name="H1NoTOC", parent=styles["H1"]))
styles.add(ParagraphStyle(name="H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13.0, leading=16, textColor=BLUE_DARK, spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name="CalloutTitle", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=10.0, leading=13, textColor=BLUE_DARK, spaceAfter=3))
styles.add(ParagraphStyle(name="CalloutBody", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.2, leading=12.2, textColor=INK, spaceAfter=0))
styles.add(ParagraphStyle(name="TableHead", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=8.0, leading=10.2, textColor=colors.white, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="TableCell", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.9, leading=10.4, textColor=INK, spaceAfter=0))
styles.add(ParagraphStyle(name="CodeBlock", parent=styles["BodyText"], fontName="Courier", fontSize=7.4, leading=9.2, textColor=INK, spaceAfter=0))
styles.add(ParagraphStyle(name="Check", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.0, leading=11.8, textColor=INK, leftIndent=14, firstLineIndent=-10, spaceAfter=4))


def p(text: str, style: str = "Body") -> Paragraph:
    return Paragraph(clean(text), styles[style])


def h1(text: str):
    return p(text, "H1")


def h2(text: str):
    return p(text, "H2")


def bullet(items: list[str]) -> ListFlowable:
    return ListFlowable(
        [ListItem(p(item), leftIndent=12) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=18,
        bulletFontName="Helvetica",
        bulletFontSize=8,
    )


def numbered(items: list[str]) -> ListFlowable:
    return ListFlowable(
        [ListItem(p(item), leftIndent=14) for item in items],
        bulletType="1",
        leftIndent=18,
        bulletFontName="Helvetica-Bold",
    )


def callout(title: str, body: str, fill=BLUE_LIGHT):
    t = Table([[p(title, "CalloutTitle")], [p(body, "CalloutBody")]], colWidths=[CONTENT_W - 8])
    t.setStyle(
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
    return t


def make_table(data, widths, header=True):
    converted = []
    for r, row in enumerate(data):
        style = "TableHead" if header and r == 0 else "TableCell"
        converted.append([p(str(cell), style) for cell in row])
    t = Table(converted, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#B8C2CC")),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D3DCE6")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    if header:
        commands += [("BACKGROUND", (0, 0), (-1, 0), BLUE), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)]
    for idx in range(1 if header else 0, len(data)):
        if idx % 2 == 0:
            commands.append(("BACKGROUND", (0, idx), (-1, idx), colors.HexColor("#FAFBFC")))
    t.setStyle(TableStyle(commands))
    return t


def codeblock(text: str):
    rows = [[Paragraph(clean(line) or "&nbsp;", styles["CodeBlock"])] for line in text.strip("\n").splitlines()]
    t = Table(rows, colWidths=[CONTENT_W - 10])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F7F9FB")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D3DCE6")),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def checklist(items: list[str]):
    return [Paragraph("□ " + clean(item), styles["Check"]) for item in items]


def build_story():
    story = [NextPageTemplate("body"), PageBreak()]
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle(fontName="Helvetica-Bold", fontSize=10, name="TOCHeading1", leftIndent=0, firstLineIndent=0, spaceBefore=5, leading=12)]
    story += [p("Tabla de contenido", "H1NoTOC"), toc, PageBreak()]

    W3 = [1.45 * inch, 2.45 * inch, 2.45 * inch]
    W4 = [1.25 * inch, 1.75 * inch, 1.75 * inch, 1.6 * inch]
    W5 = [1.15 * inch, 1.25 * inch, 1.45 * inch, 1.35 * inch, 1.35 * inch]

    story += [
        h1("1. Panorama actualizado a mayo de 2026"),
        p("Los agentes de desarrollo ya no son solo asistentes que completan codigo. En 2026 se usan como sistemas de trabajo capaces de leer repositorios, ejecutar comandos, abrir navegadores, revisar pull requests, consultar documentacion viva, operar herramientas externas y delegar tareas a subagentes. La diferencia entre un uso casual y un uso profesional esta en la configuracion: instrucciones claras, permisos acotados, skills verificables, MCPs con alcance limitado y ciclos de validacion antes de aceptar cambios."),
        callout("Idea central", "El agente acelera el trabajo, pero no reemplaza la responsabilidad tecnica. El equipo sigue definiendo arquitectura, criterios de aceptacion, controles de seguridad y pruebas. Un resultado agentico solo debe considerarse listo cuando pasa las mismas verificaciones que un cambio humano.", BLUE_LIGHT),
        make_table(
            [
                ["Capa", "Funcion", "Riesgo si se ignora"],
                ["Instrucciones/rules", "Definen como se trabaja en el repositorio.", "El agente inventa comandos, estilos o convenciones."],
                ["Skills", "Guardan procedimientos y conocimiento reutilizable.", "Cada tarea se redescubre desde cero."],
                ["Agentes/subagentes", "Aislan roles: plan, build, review, debug, docs.", "Una sola conversacion acumula demasiado contexto."],
                ["MCP/plugins", "Conectan herramientas externas y eventos.", "El agente queda ciego o recibe demasiadas capacidades."],
                ["Permisos/hooks", "Controlan acciones peligrosas y automatizan guardrails.", "Se ejecutan comandos o cambios sin control suficiente."],
            ],
            W3,
        ),
        h1("2. Tres herramientas representativas"),
        p("Claude Code, OpenCode y Codex comparten el mismo patron general: un modelo con herramientas, memoria/instrucciones, permisos, extensiones y capacidad de ejecutar trabajo en un workspace. Sus nombres cambian, pero las decisiones de ingenieria son transferibles."),
        make_table(
            [
                ["Herramienta", "Fortaleza practica", "Configuracion clave", "Uso recomendado en clase"],
                ["Claude Code", "Ecosistema maduro de skills, subagentes, hooks, MCP y plugins.", "CLAUDE.md/rules, .claude/skills, agents, .mcp.json, permisos.", "Comparar enfoques, crear skills, usar subagentes de investigacion/revision."],
                ["OpenCode", "Configuracion abierta en opencode.json, AGENTS.md, permisos y agentes en Markdown.", "permission, agent, mcp, plugin, instructions, lsp, formatter.", "Practicar configuracion explicita y control de permisos por agente."],
                ["Codex", "Integracion con AGENTS.md, skills, plugins, app/CLI, navegador, automatizaciones y workflows.", "AGENTS.md por jerarquia, skills, plugins, MCP, worktrees, automations.", "Aplicar flujos completos: issue -> cambio -> pruebas -> PR -> verificacion."],
            ],
            W4,
        ),
        callout("Regla de lectura", "No memorice comandos especificos como si fueran permanentes. Estas herramientas cambian rapido. Aprenda el modelo mental: instrucciones persistentes, workflows reutilizables, herramientas externas, permisos y verificacion.", GRAY_LIGHT),
        h1("3. AGENTS.md, CLAUDE.md y reglas"),
        p("Las reglas son el contrato de trabajo del repositorio. Deben responder preguntas que el agente no puede inferir con seguridad: como ejecutar el proyecto, que comandos verifican cambios, que carpetas son sensibles, como se nombran modulos, que patrones estan prohibidos y cuando pedir confirmacion."),
        make_table(
            [
                ["Tipo", "Cuándo usarlo", "Contenido sugerido"],
                ["AGENTS.md", "Estandar portable entre herramientas como Codex y OpenCode.", "Setup, comandos, convenciones, estructura, criterios de PR, restricciones."],
                ["CLAUDE.md", "Contexto especifico de Claude Code.", "Preferencias del equipo, comandos, arquitectura, reglas que siempre deben cargar."],
                ["Rules por rutas", "Cuando una parte del repo necesita reglas distintas.", "Reglas para frontend, backend, infra, pagos, auth o migraciones."],
                ["Override", "Cuando se requiere una excepcion temporal o local.", "Cambios de comportamiento acotados y faciles de remover."],
            ],
            W3,
        ),
        h2("Plantilla minima de AGENTS.md para un proyecto Full Stack"),
        codeblock(
            """
# AGENTS.md

## Contexto del proyecto
Aplicacion Full Stack con React, Express, MongoDB y autenticacion JWT.

## Comandos obligatorios
- Backend: npm run lint && npm test
- Frontend: npm run lint && npm run build
- E2E: npm run test:e2e cuando cambien flujos de usuario

## Reglas de seguridad
- No leer ni imprimir .env, tokens, cookies o credenciales.
- No cambiar esquemas de base de datos sin documentar migracion.
- Pedir confirmacion antes de instalar dependencias de produccion.

## Criterios de entrega
- Explicar archivos cambiados, riesgos y pruebas ejecutadas.
- No marcar la tarea lista si no se verifico el flujo principal.
"""
        ),
        h1("4. Skills: workflows reutilizables"),
        p("Una skill es una unidad de conocimiento operativo. Debe activarse cuando el usuario pide una tarea repetible: revisar un PR, generar una guia, auditar seguridad, preparar deploy, crear un informe o verificar una app. La skill no debe ser un documento gigante que siempre carga; debe apuntar a archivos de soporte, ejemplos o scripts que se usan solo cuando hacen falta."),
        make_table(
            [
                ["Elemento", "Buena practica", "Error comun"],
                ["description", "Primera frase clara: que hace y cuando usarla.", "Descripcion vaga que se solapa con otras skills."],
                ["SKILL.md", "Instrucciones breves, ordenadas y accionables.", "Meter toda la documentacion en el archivo principal."],
                ["support files", "Referencias, ejemplos, plantillas y scripts separados.", "Obligar al modelo a cargar informacion que no necesita."],
                ["scripts", "Automatizar validaciones repetibles.", "Hacer que el agente copie comandos a mano cada vez."],
                ["permisos", "Preaprobar solo herramientas necesarias.", "Dar acceso amplio por comodidad."],
            ],
            W3,
        ),
        callout("Criterio de calidad para skills", "Una skill es buena si otro estudiante puede instalarla, leer el SKILL.md en menos de dos minutos, entender cuando usarla y obtener un resultado consistente sin que el agente tenga que adivinar.", GREEN_LIGHT),
        h2("Plantilla breve de skill"),
        codeblock(
            """
---
name: review-fullstack-pr
description: Revisa cambios Full Stack antes de abrir PR. Usar cuando el usuario pida revisar diff, validar riesgos o preparar PR.
---

## Objetivo
Revisar cambios de frontend, backend, base de datos y seguridad.

## Flujo
1. Leer git diff y archivos modificados.
2. Identificar riesgos: auth, validacion, errores, datos, UX.
3. Ejecutar pruebas/lint si el entorno lo permite.
4. Entregar hallazgos con severidad, archivo y accion recomendada.

## Recursos
- rubric.md: criterios de revision.
- scripts/check.sh: verificacion automatizada del proyecto.
"""
        ),
        h1("5. Agentes y subagentes"),
        p("Los subagentes permiten dividir trabajo por rol y contexto. Son utiles para investigar grandes areas, revisar seguridad, ejecutar pruebas ruidosas, comparar alternativas o escribir documentacion sin llenar la conversacion principal. No deben usarse para todo: una correccion pequeña suele ser mas rapida en la conversacion principal."),
        make_table(
            [
                ["Agente", "Herramientas", "Permisos", "Salida esperada"],
                ["plan", "Read, grep, docs", "sin edits", "Plan de implementacion y riesgos."],
                ["build", "read, edit, bash controlado", "edits permitidos, bash ask", "Cambio implementado y pruebas."],
                ["review", "read, grep, test logs", "sin edits", "Hallazgos ordenados por severidad."],
                ["security", "read, grep, deps, docs", "sin edits, sin secretos", "Riesgos de auth, datos, config y dependencias."],
                ["docs", "read, edit docs", "sin bash", "README, guia o changelog actualizado."],
            ],
            W4,
        ),
        p("En Claude Code, los subagentes pueden restringir herramientas y scoped MCP servers; OpenCode permite crear agentes con permisos seleccionados; Codex usa subagentes/workflows y skills para conservar procedimientos. La practica comun es la misma: roles pequenos, permisos minimos y una salida verificable."),
        h1("6. MCP y plugins: conectar sin perder control"),
        p("MCP conecta agentes con herramientas externas: GitHub, navegadores, documentacion, errores de produccion, bases de datos, tickets, correo o sistemas internos. Plugins empaquetan capacidades: skills, agentes, hooks, MCPs y herramientas. La ventaja es enorme, pero tambien lo es el riesgo de contexto, permisos y acciones no deseadas."),
        callout("Principio de minimo contexto", "No conecte todos los MCPs por defecto. Active los necesarios para la tarea, use nombres descriptivos y prefiera descubrimiento progresivo de herramientas cuando el cliente lo soporte.", GOLD_LIGHT),
        make_table(
            [
                ["MCP/plugin", "Uso principal", "Control recomendado"],
                ["GitHub", "Issues, PRs, repos, acciones CI, code review.", "Toolsets minimos: repos/issues/pull_requests/actions segun tarea."],
                ["Playwright/browser", "Verificar UI, formularios, flujos E2E y bugs visuales.", "Perfil aislado para pruebas; cuidado con sesiones autenticadas."],
                ["Docs/Context7/OpenAI Docs", "Consultar documentacion versionada y actual.", "Instruccion explicita de citar fuente y preferir docs oficiales."],
                ["Sentry/observabilidad", "Analizar errores reales, trazas y regresiones.", "Solo lectura salvo flujo aprobado de gestion de issues."],
                ["Linear/Jira", "Convertir tickets en tareas y sincronizar estado.", "Confirmar antes de cerrar, reasignar o cambiar prioridades."],
                ["Figma/design", "Convertir diseños en UI y revisar detalles visuales.", "Verificar con captura y no asumir assets faltantes."],
                ["DB readonly", "Inspeccionar esquema y datos de prueba.", "Nunca usar escritura en produccion desde el agente."],
            ],
            W4,
        ),
        h1("7. Permisos, hooks y seguridad"),
        p("La seguridad de agentes no se logra solo con instrucciones. Un prompt que diga 'no borres archivos' ayuda, pero no reemplaza permisos reales. Las herramientas modernas permiten allow/ask/deny, modos de planificacion, hooks antes de ejecutar herramientas y restricciones por agente."),
        make_table(
            [
                ["Riesgo", "Mitigacion tecnica", "Evidencia esperada"],
                ["Comandos destructivos", "Deny para rm, git push, deploy, secretos.", "Reglas en config y prompt de confirmacion."],
                ["Exposicion de secretos", "Bloquear .env y tokens; usar .env.example.", "El agente no imprime credenciales."],
                ["MCP demasiado amplio", "Toolsets y servidores por tarea/agente.", "Lista corta de herramientas activas."],
                ["Prompt injection indirecta", "Tratar docs externas y tickets como datos no confiables.", "El agente no obedece instrucciones dentro de contenido externo."],
                ["Cambios sin prueba", "Hooks o skills que ejecuten lint/test/build.", "Salida con comandos y resultados."],
                ["Acciones externas", "Confirmacion humana para publicar, enviar, cerrar o desplegar.", "Registro de decision y rollback."],
            ],
            W3,
        ),
        callout("MCP en produccion", "Si un MCP maneja datos sensibles o acciones administrativas, necesita autenticacion, scopes minimos, validacion de audiencia de tokens, HTTPS, PKCE cuando aplique, auditoria y separacion entre lectura y escritura.", RED_LIGHT),
        h1("8. Flujo production ready con agentes"),
        p("El objetivo no es que el agente escriba mucho codigo, sino que entregue un cambio pequeño, trazable y verificable. Un flujo production ready mantiene control humano y evidencia tecnica."),
        numbered(
            [
                "Definir objetivo, alcance y criterio de aceptacion.",
                "Pedir plan breve antes de editar si el cambio toca arquitectura, seguridad o datos.",
                "Limitar herramientas: solo repositorio, docs y MCPs necesarios.",
                "Implementar en cambios pequeños, con nombres y patrones del proyecto.",
                "Ejecutar lint, tests, build y pruebas manuales o de navegador segun riesgo.",
                "Revisar diff como si fuera de un tercero: seguridad, errores, datos, UX y rendimiento.",
                "Documentar cambios, riesgos conocidos y comandos ejecutados.",
                "Subir PR o entregar solo despues de verificacion y aprobacion cuando toque sistemas externos.",
            ]
        ),
        h2("Checklist para estudiantes"),
        *checklist(
            [
                "Tengo AGENTS.md o reglas equivalentes con comandos reales del proyecto.",
                "No hay secretos ni credenciales en prompts, logs o commits.",
                "El agente sabe que no debe instalar dependencias sin justificar.",
                "Use al menos una skill o procedimiento reutilizable para la tarea.",
                "Si use MCP, active solo los servidores necesarios.",
                "Tengo evidencia de pruebas: terminal, screenshots, CI o reporte.",
                "Revise el diff completo antes de aceptar la entrega.",
            ]
        ),
        h1("9. Caso guia: proyecto MERN con agente"),
        p("Suponga un proyecto de reservas con React, Express, MongoDB y JWT. El equipo quiere agregar 'cancelar reserva'. Un flujo correcto con agentes no empieza escribiendo codigo al azar; empieza por contrato, permisos y pruebas."),
        make_table(
            [
                ["Paso", "Agente/capa", "Resultado"],
                ["Analisis", "plan/research", "Identifica modelo Reserva, rutas y pantallas afectadas."],
                ["Contrato", "main/build", "Define PATCH /api/reservas/:id/cancel con estados permitidos."],
                ["Backend", "build", "Valida usuario, estado, persistencia y errores 401/403/409."],
                ["Frontend", "build", "Boton cancelar, confirmacion, estado de carga y error."],
                ["Pruebas", "test/browser", "API con caso feliz y prohibido; UI verifica flujo."],
                ["Revision", "review/security", "Confirma que no se cancela reserva ajena ni finalizada."],
            ],
            W3,
        ),
        h1("10. Fuentes oficiales consultadas"),
        p("Este modulo fue preparado el 23 de mayo de 2026 con documentacion oficial y primaria. Las herramientas cambian con frecuencia; antes de usar comandos exactos en un proyecto real, revisar la documentacion vigente."),
        make_table(
            [
                ["Tema", "Fuente"],
                ["Claude Code skills", "https://docs.claude.com/en/docs/claude-code/skills"],
                ["Claude Code extension model", "https://code.claude.com/docs/en/features-overview"],
                ["Claude Code subagents", "https://code.claude.com/docs/en/sub-agents"],
                ["Claude Code plugins/permissions/MCP", "https://code.claude.com/docs/en/plugins · /permissions · /mcp"],
                ["OpenCode agents/rules/permissions/MCP/plugins", "https://opencode.ai/docs/agents · /rules · /permissions · /mcp-servers · /plugins"],
                ["Codex AGENTS.md y casos de uso", "https://developers.openai.com/codex/guides/agents-md · /codex/use-cases"],
                ["OpenAI Docs MCP", "https://developers.openai.com/learn/docs-mcp"],
                ["MCP specification and security", "https://modelcontextprotocol.io/specification/2025-06-18/basic/transports · /authorization · /security_best_practices"],
                ["MCP client best practices", "https://modelcontextprotocol.io/docs/develop/clients/client-best-practices"],
                ["Playwright MCP", "https://playwright.dev/docs/getting-started-mcp"],
                ["GitHub MCP server", "https://github.com/github/github-mcp-server"],
            ],
            [1.75 * inch, 4.75 * inch],
        ),
        h1("11. Cierre"),
        p("Trabajar con agentes exige criterio de ingenieria: dividir responsabilidades, configurar contexto, restringir permisos, conectar herramientas con intencion y verificar resultados. En un curso Full Stack, estas practicas no son un accesorio; son una forma moderna de construir, revisar y mantener software con mayor trazabilidad."),
    ]

    return story


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = ChapterTemplate(str(OUT))
    doc.multiBuild(build_story())
    print(OUT)


if __name__ == "__main__":
    main()
