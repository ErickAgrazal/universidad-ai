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


from diagrams import DIAGRAMS

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "materials" / "modulos" / "MODULO_EXTRA_AGENTES_DESARROLLO_IA"
OUT = OUT_DIR / "MODULO_EXTRA_GIT_BUENAS_PRACTICAS_DESARROLLO_AGENTICO_MAYO_2026.pdf"

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
            "title": "Modulo Extra - Git en desarrollo agentico",
            "chapter_label": "Modulo Extra Git",
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
    canvas.drawString(LEFT, PAGE_H - 2.55 * inch, "Git y buenas practicas")
    canvas.drawString(LEFT, PAGE_H - 2.9 * inch, "en desarrollo agentico")
    canvas.setFillColor(colors.HexColor("#D7EAF7"))
    canvas.setFont("Helvetica", 12.5)
    canvas.drawString(LEFT, PAGE_H - 3.45 * inch, "Branches · Commits · Worktrees · PRs · CI · CODEOWNERS · Seguridad")
    canvas.drawString(LEFT, PAGE_H - 3.7 * inch, "Desarrollo de Software IX · Codigo 1493 · Actualizado a mayo de 2026")

    canvas.setFillColor(colors.HexColor("#FFFFFF"))
    canvas.setStrokeColor(colors.HexColor("#5EA2D1"))
    canvas.roundRect(LEFT, 1.35 * inch, CONTENT_W, 1.85 * inch, 10, stroke=1, fill=0)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(LEFT + 0.28 * inch, 2.75 * inch, "Proposito del modulo")
    canvas.setFont("Helvetica", 10.5)
    lines = [
        "Explicar como usar Git con rigor cuando humanos y agentes de IA modifican el",
        "mismo repositorio: ramas pequenas, commits auditables, worktrees aislados, PRs",
        "con revision humana, CI obligatorio y reglas que evitan cambios destructivos.",
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
    canvas.drawString(LEFT, PAGE_H - 0.36 * inch, "Desarrollo de Software IX · Modulo Extra Git")
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

    story += [
        h1("1. Por que Git cambia en un ambiente agentico"),
        p("Git ya era el registro de decisiones del equipo. En desarrollo agentico se vuelve aun mas importante porque el repositorio puede recibir cambios de humanos, agentes locales, agentes remotos, automatizaciones, bots de dependencias y CI. Si Git se usa mal, el agente acelera el desorden: commits gigantes, ramas ambiguas, cambios sin revision, conflictos repetidos y secretos expuestos."),
        callout("Idea central", "El agente puede escribir codigo, pero Git debe conservar la trazabilidad. Cada cambio debe responder: que se hizo, por que se hizo, quien lo reviso, que pruebas pasaron y como revertirlo.", BLUE_LIGHT),
        make_table(
            [
                ["Practica", "Uso tradicional", "Uso agentico"],
                ["Ramas", "Aislar features.", "Aislar tareas humanas, sesiones de agente y experimentos."],
                ["Commits", "Guardar puntos de avance.", "Crear evidencia revisable, con cambios pequenos y coherentes."],
                ["Worktrees", "Trabajar varias ramas a la vez.", "Ejecutar varios agentes sin pisar archivos ni servidores."],
                ["Pull requests", "Revisar antes de mezclar.", "Frontera obligatoria entre codigo generado y main."],
                ["CI", "Detectar regresiones.", "Validar que el agente no produjo solo una solucion superficial."],
            ],
            W3,
        ),
        h1("2. Modelo mental: area de trabajo, index e historial"),
        p("Git separa tres momentos: archivos modificados en el working tree, seleccion de cambios en el index/staging area y commits en el historial. El agente debe trabajar dentro de ese modelo. Antes de editar debe mirar el estado; antes de commitear debe revisar diff; antes de subir debe ejecutar pruebas."),
        DIAGRAMS["git_areas"](),
        make_table(
            [
                ["Comando", "Pregunta que responde", "Uso con agente"],
                ["git status", "Que cambio y que falta registrar.", "Primera y ultima accion de una sesion."],
                ["git diff", "Que cambio sin stage.", "Revisar linea por linea antes de aceptar."],
                ["git diff --staged", "Que entrara al commit.", "Evitar mezclar cambios no relacionados."],
                ["git log --oneline --graph", "Como llegamos aqui.", "Orientar al agente antes de rebase o merge."],
                ["git restore", "Como descartar un cambio puntual.", "Usar con precision; no destruir trabajo ajeno."],
            ],
            W3,
        ),
        callout("Regla operativa", "El agente nunca debe asumir que el working tree esta limpio. Si hay cambios existentes, debe identificarlos y trabajar con ellos sin revertirlos, salvo instruccion explicita.", GOLD_LIGHT),
        h1("3. Ramas pequenas y nombres utiles"),
        p("Una rama representa una intencion. En trabajo agentico conviene que cada rama sea pequena y facil de revisar. Un agente no deberia acumular un redisenio, una migracion, cambios de estilo, pruebas y documentacion no relacionada en la misma rama."),
        DIAGRAMS["git_ramas"](),
        make_table(
            [
                ["Tipo de rama", "Ejemplo", "Cuando usarla"],
                ["feature", "feature/reservas-cancelacion", "Nueva capacidad de usuario."],
                ["fix", "fix/login-token-expirado", "Correccion de bug reproducible."],
                ["chore", "chore/actualizar-deps-test", "Mantenimiento sin cambio funcional directo."],
                ["docs", "docs/guia-api-reservas", "Documentacion o material docente."],
                ["agent", "agent/issue-42-validacion", "Trabajo aislado de un agente o experimento."],
            ],
            W3,
        ),
        h2("Reglas para ramas en agentes"),
        bullet(
            [
                "Una rama por objetivo verificable.",
                "No trabajar en main directamente.",
                "Sincronizar con la rama base antes de iniciar trabajo largo.",
                "Eliminar ramas remotas cerradas si el flujo del equipo lo permite.",
                "Usar worktrees para trabajo paralelo en lugar de cambiar de rama sobre archivos sucios.",
            ]
        ),
        h1("4. Commits auditables"),
        p("Un commit debe contar una decision tecnica. En un entorno con agentes, los commits pequenos permiten detectar exactamente donde se introdujo un error. El historial no debe convertirse en un volcado de cambios generados."),
        make_table(
            [
                ["Buena practica", "Ejemplo", "Motivo"],
                ["Mensaje imperativo", "fix(auth): validate expired JWT", "Explica la accion aplicada."],
                ["Scope claro", "feat(reservas): add cancellation endpoint", "Ubica el area afectada."],
                ["Un tema por commit", "modelo + ruta + prueba del mismo caso", "Facilita revertir y revisar."],
                ["No commitear ruido", "sin logs, screenshots temporales o build outputs", "Evita ensuciar el historial."],
                ["Firmar/verificar si aplica", "commit signing en repos sensibles", "Aumenta confianza de autoria."],
            ],
            W3,
        ),
        h2("Plantilla de commit para cambios con agente"),
        codeblock(
            """
tipo(scope): resumen breve

Contexto:
- Problema o ticket relacionado.

Cambio:
- Backend: ...
- Frontend: ...
- Tests: ...

Verificacion:
- npm test
- npm run build
- flujo manual revisado
"""
        ),
        h1("5. Worktrees: aislamiento para agentes paralelos"),
        p("Git worktree permite tener varios directorios de trabajo conectados al mismo repositorio. La documentacion oficial de Git lo describe como multiples working trees asociados a un repositorio. En mayo de 2026, Git 2.54 mantiene este mecanismo como una herramienta clave para trabajar varias ramas a la vez. Claude Code tambien documenta worktrees para correr sesiones paralelas sin que los cambios colisionen."),
        make_table(
            [
                ["Escenario", "Sin worktree", "Con worktree"],
                ["Dos agentes editan el repo", "Se pisan archivos o ramas.", "Cada agente usa su rama/directorio."],
                ["Bugfix urgente", "Hay que stash o interrumpir feature.", "Se abre worktree limpio para fix."],
                ["Review de PR", "Se cambia de rama y se ensucia entorno.", "Se revisa en directorio aislado."],
                ["Experimento", "Riesgo de mezclar cambios.", "Se descarta worktree si no sirve."],
            ],
            W3,
        ),
        h2("Comandos base"),
        codeblock(
            """
# Crear rama aislada para un agente
git fetch origin
git worktree add ../repo-agent-issue-42 -b agent/issue-42 origin/main

# Ver worktrees activos
git worktree list

# Eliminar cuando este limpio y cerrado
git worktree remove ../repo-agent-issue-42
git branch -d agent/issue-42
"""
        ),
        callout("Cuidado practico", "Los worktrees comparten el repositorio Git, pero no comparten necesariamente dependencias, variables locales ni servidores. En proyectos web, asigne puertos distintos por worktree para evitar choques entre agentes.", GRAY_LIGHT),
        h1("6. Pull requests como frontera de calidad"),
        p("El pull request es donde el codigo agentico deja de ser una propuesta local y se convierte en candidato a integrarse. El PR debe incluir contexto, cambios, pruebas y riesgos. La revision humana no es opcional cuando el agente toca autenticacion, base de datos, pagos, despliegue, permisos o datos sensibles."),
        make_table(
            [
                ["Seccion de PR", "Debe incluir", "Senal de alerta"],
                ["Resumen", "Problema y solucion en 3-5 lineas.", "Resumen generico sin relacion al ticket."],
                ["Cambios", "Archivos/capas principales.", "Lista enorme sin criterio."],
                ["Pruebas", "Comandos ejecutados y resultado.", "No se ejecutaron pruebas."],
                ["Riesgos", "Migraciones, auth, datos, UX, compatibilidad.", "Dice 'sin riesgos' por defecto."],
                ["Capturas", "UI antes/despues si aplica.", "Cambio visual sin evidencia."],
            ],
            W3,
        ),
        h2("Plantilla de PR para agente"),
        codeblock(
            """
## Contexto
Issue/tarea:

## Cambios principales
- Backend:
- Frontend:
- Datos/config:

## Verificacion
- [ ] lint
- [ ] tests
- [ ] build
- [ ] prueba manual o navegador

## Riesgos y rollback
- Riesgo:
- Como revertir:

## Uso de agente
Herramienta/agente usado:
Revision humana pendiente:
"""
        ),
        h1("7. Branch protection, CODEOWNERS y CI"),
        p("En GitHub, las ramas protegidas y los rulesets permiten exigir revisiones, estados de CI, restricciones de push y otras reglas antes de mezclar a main. CODEOWNERS asigna responsabilidad sobre carpetas o archivos y puede requerir aprobacion de quienes conocen esa parte. En repos con agentes, estas reglas son guardrails de produccion."),
        make_table(
            [
                ["Control", "Configuracion recomendada", "Por que importa con agentes"],
                ["Protected branch", "No push directo a main; PR requerido.", "Impide que el agente salte la revision."],
                ["Required checks", "lint, test, build, e2e critico.", "Detecta codigo que solo parece correcto."],
                ["CODEOWNERS", "Auth, DB, infra y workflows con propietarios.", "Cambios sensibles pasan por experto."],
                ["Dismiss stale approvals", "Revisiones caducan si cambian commits.", "Evita aprobar codigo que luego fue modificado."],
                ["Actions permissions", "Token minimo y secretos protegidos.", "Reduce impacto de PRs maliciosos o inseguros."],
            ],
            W3,
        ),
        callout("Regla de seguridad", "Un agente puede proponer cambios en workflows CI/CD, pero no deberia aprobarlos ni desplegarlos sin revision humana. Cambios en .github/workflows, scripts de deploy o permisos requieren doble cuidado.", RED_LIGHT),
        h1("8. Conflictos, rebase y merge"),
        p("Los conflictos aumentan cuando varios agentes trabajan en paralelo. La solucion no es ocultarlos, sino reducir el tamano de ramas y sincronizar frecuentemente. Rebase puede limpiar historial local; merge puede conservar historia compartida. La decision depende del flujo del equipo."),
        make_table(
            [
                ["Operacion", "Uso", "Precaucion"],
                ["git fetch", "Traer cambios sin mezclar.", "Preferible antes de decidir merge/rebase."],
                ["git merge origin/main", "Integrar base preservando merge commit.", "Revisar conflictos con pruebas completas."],
                ["git rebase origin/main", "Reaplicar commits sobre base actual.", "No reescribir ramas compartidas sin acuerdo."],
                ["git cherry-pick", "Traer commit puntual.", "Evitar duplicar cambios si luego se mergea rama original."],
                ["git revert", "Deshacer en historial publico.", "Mejor que reset en ramas compartidas."],
            ],
            W3,
        ),
        h2("Protocolo de conflicto con agente"),
        numbered(
            [
                "Detener cambios nuevos hasta entender el conflicto.",
                "Leer ambos lados y la intencion del PR/base.",
                "Resolver minimo necesario; no reescribir logica no relacionada.",
                "Ejecutar pruebas afectadas.",
                "Explicar en el PR que se resolvio y por que.",
            ]
        ),
        h1("9. Reglas para AGENTS.md en Git"),
        p("El repositorio debe explicar al agente como usar Git. Estas reglas evitan accidentes frecuentes: revertir trabajo ajeno, commitear secretos, usar git add -A sin revisar, hacer push directo o mezclar cambios no relacionados."),
        codeblock(
            """
## Git rules for agents

- Always run `git status` before editing and before final response.
- Never run `git reset --hard`, `git clean -fd`, or checkout files unless explicitly asked.
- Do not use `git add -A`; stage only files relevant to the task.
- Do not commit generated logs, screenshots, build output, .env files, or secrets.
- Prefer one branch per task; use worktrees for parallel agent sessions.
- Before opening PR, run lint/test/build required by this repo.
- PR description must include: summary, tests, risks, rollback, agent/tool used.
- Do not push to main. Do not deploy without human confirmation.
"""
        ),
        callout("Buen habito", "Si el agente encuentra cambios que no hizo, debe mencionarlos y evitar tocarlos. Esa regla protege trabajo humano y otros agentes.", GREEN_LIGHT),
        h1("10. Caso guia: cancelar reserva en MERN"),
        p("Un equipo usa React, Express, MongoDB y JWT. Se pide agregar cancelacion de reserva con agente. Git debe ordenar el trabajo para que la revision sea simple."),
        make_table(
            [
                ["Paso", "Git", "Evidencia"],
                ["Preparar", "git fetch; git worktree add ../reserva-cancel -b agent/reserva-cancel origin/main", "Directorio aislado."],
                ["Implementar", "Commits pequenos: backend, frontend, tests.", "Diff revisable por capa."],
                ["Verificar", "npm test; npm run build; prueba manual.", "Resultados en PR."],
                ["Abrir PR", "Descripcion con riesgo auth/datos.", "Revisor sabe que mirar."],
                ["Revisar", "CODEOWNERS para backend/auth.", "Aprobacion humana antes de merge."],
                ["Cerrar", "Eliminar worktree y rama si el PR se mergea.", "Workspace limpio."],
            ],
            W3,
        ),
        h1("11. Checklist production ready"),
        *checklist(
            [
                "La rama tiene un objetivo claro y pequeno.",
                "El agente no trabajo sobre main.",
                "No hay secretos, .env ni archivos generados innecesarios.",
                "El diff fue revisado completo antes del commit/PR.",
                "Los commits tienen mensajes utiles y cambios coherentes.",
                "Se ejecutaron pruebas relevantes y build.",
                "El PR explica riesgos, rollback y uso de agente.",
                "Cambios sensibles tienen reviewer/CODEOWNER.",
                "La rama base esta actualizada o el conflicto fue resuelto con pruebas.",
                "El worktree o rama temporal se limpio al terminar.",
            ]
        ),
        h1("12. Fuentes oficiales consultadas"),
        p("Material preparado el 23 de mayo de 2026. Para comandos exactos y opciones nuevas, verificar la documentacion vigente del proveedor antes de aplicarlo en repositorios reales."),
        make_table(
            [
                ["Tema", "Fuente"],
                ["Git worktree 2.54", "https://git-scm.com/docs/git-worktree"],
                ["Git contributing workflows", "https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project"],
                ["GitHub protected branches", "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches"],
                ["GitHub CODEOWNERS", "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners"],
                ["GitHub Actions secure use", "https://docs.github.com/en/actions/reference/security/secure-use"],
                ["Claude Code worktrees", "https://code.claude.com/docs/en/worktrees"],
                ["Codex AGENTS.md", "https://developers.openai.com/codex/guides/agents-md"],
                ["OpenCode rules", "https://opencode.ai/docs/rules/"],
            ],
            [1.75 * inch, 4.75 * inch],
        ),
        h1("13. Cierre"),
        p("Git es la capa de control que convierte trabajo agentico en ingenieria revisable. La velocidad del agente solo es valiosa si el historial queda limpio, las ramas son comprensibles, los PRs tienen evidencia, CI bloquea regresiones y las personas conservan la decision final sobre cambios sensibles."),
    ]
    return story


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = ChapterTemplate(str(OUT))
    doc.multiBuild(build_story())
    print(OUT)


if __name__ == "__main__":
    main()
