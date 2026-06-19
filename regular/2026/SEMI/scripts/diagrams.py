"""Diagramas vectoriales para los PDFs del curso (paleta institucional).

Cada función devuelve un Drawing de ReportLab listo para insertarse en un
story. Registro central: DIAGRAMS["nombre"]() → Drawing.
"""
from __future__ import annotations

import math

from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib import colors

BLUE = colors.HexColor("#174A7C")
BLUE_DARK = colors.HexColor("#0E2E4F")
BLUE_LIGHT = colors.HexColor("#EAF2FA")
BLUE_MID = colors.HexColor("#5EA2D1")
GRAY = colors.HexColor("#5C6773")
GRAY_LIGHT = colors.HexColor("#F4F6F8")
INK = colors.HexColor("#1F2933")
GREEN = colors.HexColor("#2E7D5B")
GREEN_LIGHT = colors.HexColor("#EAF7EF")
GOLD_LIGHT = colors.HexColor("#FFF6DC")

W = 460  # ancho estándar de los diagramas


def box(d, x, y, w, h, lines, fill=BLUE_LIGHT, stroke=BLUE, size=8.2, text=INK, bold_first=True):
    d.add(Rect(x, y, w, h, rx=5, ry=5, fillColor=fill, strokeColor=stroke, strokeWidth=1))
    n = len(lines)
    line_h = size + 2.6
    total = n * line_h
    ty = y + h / 2 + total / 2 - size
    for i, ln in enumerate(lines):
        font = "Helvetica-Bold" if (i == 0 and bold_first) else "Helvetica"
        d.add(String(x + w / 2, ty, ln, fontName=font, fontSize=size, fillColor=text, textAnchor="middle"))
        ty -= line_h


def label(d, x, y, text, size=7.4, color=GRAY, anchor="middle", bold=False):
    d.add(String(x, y, text, fontName="Helvetica-Bold" if bold else "Helvetica", fontSize=size, fillColor=color, textAnchor=anchor))


def arrow(d, x1, y1, x2, y2, color=GRAY, width=1.1, dashed=False, both=False):
    ln = Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=width)
    if dashed:
        ln.strokeDashArray = [3, 2]
    d.add(ln)
    ang = math.atan2(y2 - y1, x2 - x1)
    for (tx, ty, a) in ([(x2, y2, ang)] + ([(x1, y1, ang + math.pi)] if both else [])):
        s = 5.2
        p1 = (tx, ty)
        p2 = (tx - s * math.cos(a - 0.42), ty - s * math.sin(a - 0.42))
        p3 = (tx - s * math.cos(a + 0.42), ty - s * math.sin(a + 0.42))
        d.add(Polygon([*p1, *p2, *p3], fillColor=color, strokeColor=color, strokeWidth=0.4))


def dot(d, x, y, r=4.6, fill=BLUE, stroke=BLUE_DARK):
    from reportlab.graphics.shapes import Circle

    d.add(Circle(x, y, r, fillColor=fill, strokeColor=stroke, strokeWidth=1))


# ── MCP ──────────────────────────────────────────────────────────────────────

def mcp_arquitectura():
    d = Drawing(W, 168)
    # Host
    d.add(Rect(0, 22, 158, 124, rx=6, ry=6, fillColor=GRAY_LIGHT, strokeColor=BLUE_DARK, strokeWidth=1.2))
    label(d, 79, 131, "HOST", size=8.6, color=BLUE_DARK, bold=True)
    label(d, 79, 120, "Claude Code · ChatGPT", size=7.2)
    box(d, 12, 78, 134, 30, ["Modelo (LLM)", "decide qué tool usar"])
    box(d, 12, 34, 134, 30, ["Cliente MCP", "mantiene la conexión"])
    arrow(d, 79, 78, 79, 64, both=True, color=BLUE)
    # Servidor MCP
    box(d, 208, 50, 124, 72, ["Servidor MCP", "mcp-tienda", "tools · resources", "valida con Zod"], fill=BLUE_LIGHT)
    # Backend propio
    box(d, 372, 50, 88, 72, ["Tu backend", "API Hono/", "Express", "+ MongoDB"], fill=GREEN_LIGHT, stroke=GREEN)
    # Conexiones
    arrow(d, 158, 86, 208, 86, both=True, color=BLUE_DARK, width=1.3)
    label(d, 183, 96, "JSON-RPC", size=7.2, color=BLUE_DARK, bold=True)
    label(d, 183, 72, "stdio / HTTP", size=7.0)
    arrow(d, 332, 86, 372, 86, both=True, color=GREEN, width=1.3)
    label(d, 352, 96, "HTTP", size=7.2, color=GREEN, bold=True)
    label(d, 230, 8, "El modelo nunca toca la base de datos: pide; el servidor decide y responde.", size=7.4, color=GRAY)
    return d


def mcp_flujo_tool():
    d = Drawing(W, 118)
    steps = [
        ("Usuario", "pide en lenguaje", "natural"),
        ("LLM", "elige la tool por", "su descripción"),
        ("Cliente MCP", "envía la", "invocación"),
        ("Servidor MCP", "valida (Zod)", "y ejecuta"),
        ("API · DB", "del comercio", "electrónico"),
    ]
    bw, bh, gap = 82, 44, 12
    x = 0
    for i, (t, s1, s2) in enumerate(steps):
        box(d, x, 56, bw, bh, [t, s1, s2], size=7.2)
        if i < len(steps) - 1:
            arrow(d, x + bw, 78, x + bw + gap, 78, color=BLUE_DARK)
        x += bw + gap
    # retorno
    arrow(d, 4 * (bw + gap) + bw / 2, 56, bw + bw / 2, 36, color=GREEN, width=1.2)
    d.add(Line(4 * (bw + gap) + bw / 2, 56, 4 * (bw + gap) + bw / 2, 36, strokeColor=GREEN, strokeWidth=1.2))
    d.add(Line(bw + bw / 2, 36, 4 * (bw + gap) + bw / 2, 36, strokeColor=GREEN, strokeWidth=1.2))
    arrow(d, bw + bw / 2 + 14, 36, bw + bw / 2, 36, color=GREEN, width=1.2)
    label(d, W / 2, 24, "el resultado vuelve al contexto del modelo, que razona y responde", size=7.4, color=GREEN)
    return d


# ── Git ──────────────────────────────────────────────────────────────────────

def git_areas():
    d = Drawing(W, 128)
    areas = [
        ("Directorio de", "trabajo", "archivos editados"),
        ("Staging", "(index)", "cambios marcados"),
        ("Repositorio", "local", "historial de commits"),
        ("Remoto", "(GitHub)", "colaboración / PRs"),
    ]
    cmds = ["git add", "git commit", "git push"]
    bw, bh, gap = 88, 50, 34
    x = 0
    for i, lines in enumerate(areas):
        fill = BLUE_LIGHT if i < 3 else GREEN_LIGHT
        stroke = BLUE if i < 3 else GREEN
        box(d, x, 56, bw, bh, list(lines), fill=fill, stroke=stroke, size=7.4)
        if i < 3:
            arrow(d, x + bw + 2, 81, x + bw + gap - 2, 81, color=BLUE_DARK)
            label(d, x + bw + gap / 2, 112, cmds[i], size=7.0, color=BLUE_DARK, bold=True)
        x += bw + gap
    # retornos
    x_remote = 3 * (bw + gap) + bw / 2
    x_work = bw / 2
    d.add(Line(x_remote, 56, x_remote, 34, strokeColor=GRAY, strokeWidth=1))
    d.add(Line(x_work + 60, 34, x_remote, 34, strokeColor=GRAY, strokeWidth=1))
    arrow(d, x_work + 74, 34, x_work + 60, 34, color=GRAY)
    label(d, W / 2, 22, "git pull / git fetch — siempre antes de trabajar (y antes de recalificar repos)", size=7.2)
    return d


def git_ramas():
    d = Drawing(W, 138)
    y_main, y_feat = 42, 96
    label(d, 6, y_main + 12, "main", size=8, color=BLUE_DARK, anchor="start", bold=True)
    label(d, 6, y_feat + 12, "feature/checkout-stripe", size=8, color=GREEN, anchor="start", bold=True)
    d.add(Line(20, y_main, 440, y_main, strokeColor=BLUE_DARK, strokeWidth=1.6))
    xs_main = [50, 120, 330, 410]
    for x in xs_main:
        dot(d, x, y_main)
    # rama
    d.add(Line(120, y_main, 175, y_feat, strokeColor=GREEN, strokeWidth=1.4))
    d.add(Line(175, y_feat, 270, y_feat, strokeColor=GREEN, strokeWidth=1.4))
    d.add(Line(270, y_feat, 330, y_main, strokeColor=GREEN, strokeWidth=1.4))
    for x in (175, 225, 270):
        dot(d, x, y_feat, fill=GREEN_LIGHT, stroke=GREEN)
    label(d, 120, y_main - 16, "se ramifica", size=7.0)
    label(d, 222, y_feat + 13, "commits pequeños y auditables", size=7.0, color=GREEN)
    label(d, 330, y_main - 16, "merge vía Pull Request", size=7.0, color=BLUE_DARK, bold=True)
    label(d, 330, y_main - 26, "(revisión + CI antes de entrar a main)", size=6.8)
    label(d, 410, y_main + 13, "main siempre desplegable", size=7.0, color=BLUE_DARK)
    return d


# ── React ────────────────────────────────────────────────────────────────────

def react_flujo():
    d = Drawing(W, 168)
    # ciclo: Estado (izq) → arriba Render → DOM (der) → abajo Evento → Estado
    box(d, 6, 64, 104, 40, ["Estado", "(useState)"], size=8.2)
    box(d, 178, 118, 124, 40, ["Render", "UI = f(estado)"], size=8.2)
    box(d, 352, 64, 102, 40, ["DOM real"], size=8.2)
    box(d, 178, 8, 124, 40, ["Evento", "onClick → manejador"], size=7.6)
    arrow(d, 110, 96, 178, 132, color=BLUE_DARK, width=1.2)
    label(d, 124, 134, "re-render", size=7.0, color=BLUE_DARK)
    arrow(d, 302, 132, 352, 98, color=BLUE_DARK, width=1.2)
    label(d, 345, 134, "reconciliación:", size=7.0, color=BLUE_DARK)
    label(d, 349, 124, "cambios mínimos", size=7.0, color=BLUE_DARK)
    arrow(d, 352, 70, 302, 34, color=GRAY, width=1.2)
    label(d, 345, 36, "interacción del usuario", size=7.0)
    arrow(d, 178, 34, 110, 70, color=GREEN, width=1.2)
    label(d, 120, 36, "setState(...)", size=7.0, color=GREEN, bold=True)
    label(d, 124, 26, "programa re-render", size=6.8, color=GREEN)
    return d


def react_reconciliacion():
    d = Drawing(W, 120)
    box(d, 0, 62, 92, 44, ["Cambio de", "estado"], size=7.8)
    box(d, 118, 62, 100, 44, ["Nuevo árbol", "de elementos", "(Virtual DOM)"], size=7.4)
    box(d, 244, 62, 96, 44, ["Diff vs árbol", "anterior", "(reconciliación)"], size=7.4)
    box(d, 366, 62, 94, 44, ["Operaciones", "mínimas sobre", "el DOM real"], size=7.4)
    arrow(d, 92, 84, 118, 84, color=BLUE_DARK)
    arrow(d, 218, 84, 244, 84, color=BLUE_DARK)
    arrow(d, 340, 84, 366, 84, color=BLUE_DARK)
    d.add(Rect(60, 8, 340, 32, rx=5, ry=5, fillColor=GOLD_LIGHT, strokeColor=GRAY, strokeWidth=0.8))
    label(d, 230, 27, "En listas, la prop key es la identidad estable que el diff usa para saber", size=7.2, color=INK)
    label(d, 230, 16, "si un elemento se movió, se agregó o se eliminó.", size=7.2, color=INK)
    return d


# ── Express / Hono ───────────────────────────────────────────────────────────

def express_middlewares():
    d = Drawing(W, 142)
    box(d, 0, 84, 74, 40, ["Request", "HTTP"], size=7.8)
    box(d, 102, 84, 86, 40, ["Middleware", "logger"], size=7.6)
    box(d, 216, 84, 86, 40, ["Middleware", "auth / JWT"], size=7.6)
    box(d, 330, 84, 60, 40, ["Handler", "de la ruta"], size=7.6)
    box(d, 414, 84, 46, 40, ["Resp.", "JSON"], size=7.6, fill=GREEN_LIGHT, stroke=GREEN)
    for x1, x2 in [(74, 102), (188, 216), (302, 330), (390, 414)]:
        arrow(d, x1, 104, x2, 104, color=BLUE_DARK)
    label(d, 95, 114, "next()", size=6.6, color=BLUE_DARK)
    label(d, 209, 114, "next()", size=6.6, color=BLUE_DARK)
    box(d, 156, 8, 150, 34, ["Manejador de errores", "(centralizado)"], size=7.4, fill=GOLD_LIGHT, stroke=GRAY)
    for x in (145, 259, 360):
        arrow(d, x, 84, max(170, min(x, 292)), 42, color=GRAY, dashed=True, width=0.9)
    label(d, 380, 52, "throw / error", size=6.8)
    label(d, 230, 64, "la cadena de responsabilidad: cada eslabón decide si continúa", size=7.2, color=GRAY)
    return d


def hono_vs_express():
    d = Drawing(W, 168)
    label(d, 4, 148, "Express (API propia de Node.js)", size=8.4, color=BLUE_DARK, anchor="start", bold=True)
    box(d, 0, 96, 96, 38, ["req · res", "dos objetos", "mutables"], size=7.4)
    box(d, 128, 96, 130, 38, ["(req, res, next)", "los middlewares y el", "handler MUTAN res"], size=7.2)
    box(d, 290, 96, 110, 38, ["res.json(...)", "responde como", "efecto secundario"], size=7.2)
    arrow(d, 96, 115, 128, 115, color=BLUE_DARK)
    arrow(d, 258, 115, 290, 115, color=BLUE_DARK)
    label(d, 430, 115, "solo", size=7.0)
    label(d, 430, 106, "Node.js", size=7.0, bold=True)

    label(d, 4, 72, "Hono (Web Standards)", size=8.4, color=GREEN, anchor="start", bold=True)
    box(d, 0, 18, 96, 38, ["Request", "estándar de la", "plataforma web"], size=7.2, fill=GREEN_LIGHT, stroke=GREEN)
    box(d, 128, 18, 130, 38, ["Context (c)", "una sola interfaz:", "c.req · c.json()"], size=7.2, fill=GREEN_LIGHT, stroke=GREEN)
    box(d, 290, 18, 110, 38, ["return Response", "la respuesta es el", "valor de RETORNO"], size=7.2, fill=GREEN_LIGHT, stroke=GREEN)
    arrow(d, 96, 37, 128, 37, color=GREEN)
    arrow(d, 258, 37, 290, 37, color=GREEN)
    label(d, 430, 41, "cualquier", size=7.0)
    label(d, 430, 32, "runtime", size=7.0, bold=True)
    return d


def hono_runtimes():
    d = Drawing(W, 128)
    box(d, 115, 84, 230, 36, ["Mismo código Hono", "(construido solo sobre Web Standards)"], size=7.8, fill=GREEN_LIGHT, stroke=GREEN)
    targets = [
        ("Node.js", "servidor clásico", 0),
        ("Bun", "desarrollo local", 122),
        ("Deno", "runtime seguro", 244),
        ("Cloudflare Workers", "edge global", 352),
    ]
    for name, sub, x in targets:
        w = 108 if x == 352 else 102
        box(d, x, 14, w, 36, [name, sub], size=7.4)
        arrow(d, 230, 84, x + w / 2, 50, color=GREEN, width=1.0)
    return d


# ── Full Stack / entorno ─────────────────────────────────────────────────────

def fullstack_capas():
    d = Drawing(W, 164)
    box(d, 0, 92, 122, 52, ["Frontend", "React (SPA)", "interacción y estados"], size=7.6)
    box(d, 170, 92, 130, 52, ["Backend / API", "Express · Hono", "reglas, validación,", "seguridad"], size=7.2)
    box(d, 348, 92, 112, 52, ["MongoDB", "persistencia y", "consultas"], size=7.6)
    arrow(d, 122, 118, 170, 118, both=True, color=BLUE_DARK, width=1.3)
    label(d, 146, 130, "HTTP · JSON", size=7.0, color=BLUE_DARK, bold=True)
    arrow(d, 300, 118, 348, 118, both=True, color=BLUE_DARK, width=1.3)
    label(d, 324, 130, "Mongoose", size=7.0, color=BLUE_DARK, bold=True)
    box(d, 170, 22, 130, 40, ["Servicios externos", "pagos · IA · correo"], size=7.2, fill=GOLD_LIGHT, stroke=GRAY)
    arrow(d, 235, 92, 235, 62, both=True, color=GRAY, dashed=True)
    label(d, 230, 6, "el navegador NUNCA habla directo con la base ni con los secretos", size=7.0)
    return d


def docker_compose():
    d = Drawing(W, 152)
    d.add(Rect(120, 14, 340, 116, rx=7, ry=7, fillColor=GRAY_LIGHT, strokeColor=BLUE_DARK, strokeWidth=1.2))
    label(d, 290, 118, "docker-compose.yml — define servicios y red interna", size=7.6, color=BLUE_DARK, bold=True)
    box(d, 140, 56, 130, 50, ["Contenedor app", "Node / Bun", "API + frontend"], size=7.4)
    box(d, 308, 56, 130, 50, ["Contenedor mongo", "MongoDB", "volumen = persistencia"], size=7.2)
    arrow(d, 270, 81, 308, 81, both=True, color=BLUE_DARK, width=1.2)
    label(d, 289, 92, "red interna", size=6.8, color=BLUE_DARK)
    label(d, 289, 40, "mismo entorno en cada máquina del equipo: 'funciona en la mía' deja de existir", size=7.0)
    box(d, 0, 56, 84, 50, ["Navegador", "(host)", "localhost"], size=7.4, fill=GREEN_LIGHT, stroke=GREEN)
    arrow(d, 84, 81, 140, 81, color=GREEN, width=1.2)
    label(d, 112, 92, "puertos", size=6.8, color=GREEN)
    return d


# ── JWT / pruebas / Mongo / pagos ────────────────────────────────────────────

def jwt_flujo():
    d = Drawing(W, 178)
    label(d, 4, 160, "1) Autenticación (una vez)", size=8.4, color=BLUE_DARK, anchor="start", bold=True)
    box(d, 0, 104, 96, 44, ["Cliente", "envía email +", "contraseña"], size=7.2)
    box(d, 128, 104, 122, 44, ["POST /login", "compara contra el", "hash (bcrypt)"], size=7.2)
    box(d, 282, 104, 90, 44, ["Firma el JWT", "con el secreto", "del servidor"], size=7.2)
    box(d, 396, 104, 64, 44, ["Cliente", "guarda el", "token"], size=7.2, fill=GREEN_LIGHT, stroke=GREEN)
    arrow(d, 96, 126, 128, 126, color=BLUE_DARK)
    arrow(d, 250, 126, 282, 126, color=BLUE_DARK)
    arrow(d, 372, 126, 396, 126, color=GREEN)

    label(d, 4, 84, "2) Acceso (en cada petición)", size=8.4, color=GREEN, anchor="start", bold=True)
    box(d, 0, 26, 130, 44, ["GET /privado", "Authorization:", "Bearer <token>"], size=7.2, fill=GREEN_LIGHT, stroke=GREEN)
    box(d, 162, 26, 138, 44, ["Middleware", "verifica firma y exp;", "sin consultar sesión"], size=7.2, fill=GREEN_LIGHT, stroke=GREEN)
    box(d, 332, 26, 128, 44, ["Handler", "usa los claims", "(sub, rol) y responde"], size=7.2, fill=GREEN_LIGHT, stroke=GREEN)
    arrow(d, 130, 48, 162, 48, color=GREEN)
    arrow(d, 300, 48, 332, 48, color=GREEN)
    label(d, 230, 8, "firma inválida o token vencido → 401 sin tocar el handler", size=7.0)
    return d


def mongo_embeber_referenciar():
    d = Drawing(W, 168)
    label(d, 4, 150, "Embeber: el todo y sus partes viajan juntos", size=8.2, color=BLUE_DARK, anchor="start", bold=True)
    d.add(Rect(0, 86, 218, 56, rx=6, ry=6, fillColor=BLUE_LIGHT, strokeColor=BLUE, strokeWidth=1))
    label(d, 109, 128, "orden { cliente, fecha, total,", size=7.6, color=INK, bold=True)
    d.add(Rect(14, 92, 190, 26, rx=4, ry=4, fillColor=colors.white, strokeColor=BLUE_MID, strokeWidth=0.9))
    label(d, 109, 102, "items: [ {producto, precio, cant}, … ]  }", size=7.4, color=INK)
    label(d, 109, 72, "una sola lectura · atomicidad por documento", size=7.0, color=BLUE_DARK)

    label(d, 250, 150, "Referenciar: cada entidad vive aparte", size=8.2, color=GREEN, anchor="start", bold=True)
    box(d, 246, 92, 96, 46, ["orden", "{ productoId,", "cantidad }"], size=7.2, fill=GREEN_LIGHT, stroke=GREEN)
    box(d, 384, 92, 76, 46, ["producto", "{ _id, nombre,", "precio, stock }"], size=7.0, fill=GREEN_LIGHT, stroke=GREEN)
    arrow(d, 342, 115, 384, 115, color=GREEN, width=1.2)
    label(d, 363, 126, "referencia", size=6.8, color=GREEN)
    label(d, 353, 72, "sin duplicación · el stock se actualiza en un solo lugar", size=7.0, color=GREEN)
    label(d, 230, 18, "Criterio: lo que se lee junto y pertenece al padre se embebe; lo compartido y cambiante se referencia.", size=7.2, color=GRAY)
    return d


def piramide_pruebas():
    d = Drawing(W, 178)
    cx, base_y, top_y = 230, 22, 162
    half_base = 150
    def x_at(y, side):
        f = (y - base_y) / (top_y - base_y)
        return cx + side * half_base * (1 - 0.62 * f)
    bands = [(22, 68, "Unitarias", "motor de reglas, utilidades", BLUE_LIGHT),
             (68, 114, "Integración / API", "rutas con supertest, datos semilla", colors.HexColor("#D9E8F5")),
             (114, 162, "E2E (Playwright)", "flujos reales en el navegador", colors.HexColor("#BCD7EC"))]
    for y0, y1, t, s, fill in bands:
        pts = [x_at(y0, -1), y0, x_at(y0, 1), y0, x_at(y1, 1), y1, x_at(y1, -1), y1]
        d.add(Polygon(pts, fillColor=fill, strokeColor=BLUE_DARK, strokeWidth=0.9))
        ymid = (y0 + y1) / 2
        label(d, cx, ymid + 2, t, size=8.2, color=BLUE_DARK, bold=True)
        label(d, cx, ymid - 9, s, size=6.8, color=INK)
    label(d, 40, 150, "pocas ·", size=7.2, color=GRAY, anchor="start")
    label(d, 40, 140, "lentas ·", size=7.2, color=GRAY, anchor="start")
    label(d, 40, 130, "máxima confianza", size=7.2, color=GRAY, anchor="start")
    label(d, 40, 44, "muchas ·", size=7.2, color=GRAY, anchor="start")
    label(d, 40, 34, "rápidas · baratas", size=7.2, color=GRAY, anchor="start")
    arrow(d, 416, 34, 416, 150, color=GRAY, width=1.0)
    label(d, 428, 90, "costo", size=7.0, color=GRAY, anchor="start")
    return d


def pago_webhook():
    d = Drawing(W, 186)
    box(d, 0, 122, 120, 50, ["Navegador", "del cliente"], size=7.8)
    box(d, 340, 122, 120, 50, ["Pasarela", "(Stripe, modo prueba)"], size=7.4, fill=GOLD_LIGHT, stroke=GRAY)
    box(d, 170, 14, 120, 50, ["Tu backend", "API + MongoDB"], size=7.6, fill=GREEN_LIGHT, stroke=GREEN)
    # 1: cliente → backend
    arrow(d, 50, 122, 195, 64, color=BLUE_DARK, width=1.1)
    label(d, 86, 92, "1. iniciar compra", size=7.0, color=BLUE_DARK, bold=True)
    # 2: backend → pasarela
    arrow(d, 268, 64, 388, 122, color=BLUE_DARK, width=1.1)
    label(d, 366, 88, "2. crear sesión", size=7.0, color=BLUE_DARK, bold=True)
    label(d, 370, 78, "(con idempotencia)", size=6.6, color=BLUE_DARK)
    # 3: cliente → pasarela (tarjeta directa)
    arrow(d, 120, 152, 340, 152, color=GRAY, width=1.2)
    label(d, 230, 162, "3. paga EN el checkout — la tarjeta nunca toca tu servidor", size=7.0, bold=True)
    # 4: pasarela → cliente redirect (dashed)
    arrow(d, 340, 134, 120, 134, color=GRAY, width=0.9, dashed=True)
    label(d, 230, 124, "4. redirect de éxito (cosmético: NO entregar aquí)", size=6.8)
    # 5: pasarela → backend webhook
    arrow(d, 388, 122, 268, 50, color=GREEN, width=1.4)
    label(d, 358, 56, "5. webhook firmado", size=7.2, color=GREEN, bold=True)
    label(d, 358, 46, "verificar firma + evento único", size=6.6, color=GREEN)
    label(d, 230, 2, "6. solo tras el webhook verificado: acreditar la compra en la base", size=7.2, color=GREEN, bold=True)
    return d


DIAGRAMS = {
    "fullstack_capas": fullstack_capas,
    "docker_compose": docker_compose,
    "jwt_flujo": jwt_flujo,
    "mongo_embeber_referenciar": mongo_embeber_referenciar,
    "piramide_pruebas": piramide_pruebas,
    "pago_webhook": pago_webhook,
    "mcp_arquitectura": mcp_arquitectura,
    "mcp_flujo_tool": mcp_flujo_tool,
    "git_areas": git_areas,
    "git_ramas": git_ramas,
    "react_flujo": react_flujo,
    "react_reconciliacion": react_reconciliacion,
    "express_middlewares": express_middlewares,
    "hono_vs_express": hono_vs_express,
    "hono_runtimes": hono_runtimes,
}
