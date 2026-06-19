---
name: utp-fisc-review-pdf
description: "Generar PDFs académicos de revisión para anteproyectos e informes finales UTP/FISC, con encabezado institucional: logo UTP arriba izquierda y logo FISC arriba derecha."
version: 1.4.2
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [UTP, FISC, PDF, revision-academica, anteproyecto, informe-final, trabajo-de-graduacion, Panama]
    related_skills: [utp-fisc-anteproyecto-review, utp-fisc-final-doc-review]
---

# UTP/FISC review PDF

## Cuándo usar

Usar cuando Erick pida crear, convertir, renderizar o entregar en PDF una revisión académica para:

- Anteproyecto de Trabajo de Graduación UTP/FISC.
- Informe/documento final de Trabajo de Graduación UTP/FISC.
- Retroalimentación para estudiantes UTP/FISC después de usar `utp-fisc-anteproyecto-review` o `utp-fisc-final-doc-review`.

No usar `client-pdf-docs` para estas revisiones universitarias. Esa habilidad queda para propuestas/clientes. Esta habilidad es específica para documentos académicos UTP/FISC.

## Identidad visual obligatoria

Todo PDF generado con esta habilidad debe usar:

- Papel carta por defecto.
- Sin portada formal, salvo que Erick la pida explícitamente.
- Encabezado repetido en cada página.
- Logo UTP arriba izquierda.
- Logo Facultad de Ingeniería de Sistemas Computacionales arriba derecha.
- Título/contexto centrado entre logos.
- Estilo plano, limpio y académico; sin sombra gris, halo, degradados pesados ni decoración de propuesta comercial.
- Footer con versión, fecha, tipo de revisión y número de página.
- Arriba del contenido, mostrar título breve `Resumen de revisión` y tabla compacta de ancho completo con: documento/tesis, entregado por, versión y estado.
- No mostrar cuadro grande de aprobación/desaprobación por defecto.
- Estado va dentro de la tabla como texto pequeño con color; no colorear toda la celda como bloque grande:
  - `APROBADO`: verde.
  - `SOLICITUD DE REVISIÓN`: amarillo o rojo según severidad (`cambios_sugeridos` o `desaprobado`).
- Después de la tabla, ir directo a `Correcciones a realizar`.
- En `Correcciones a realizar`, los puntos principales numerados deben salir en negrita y un poco más grandes; las viñetas internas quedan como acciones específicas para el estudiante.
- Al final, incluir tabla de cumplimiento/faltantes del documento.

Assets esperados:

- `assets/utp-logo.png`
- `assets/fisc-logo.png`

Si faltan assets, pedirlos o extraerlos del documento recibido si vienen embebidos. No inventar logos.

## Flujo recomendado

1. Revisar documento fuente con skill académico correspondiente:
   - `utp-fisc-anteproyecto-review` para anteproyectos.
   - `utp-fisc-final-doc-review` para documentos finales.
2. Preparar contenido en Markdown usando `templates/review-template.md` como base.
3. Incluir veredicto compacto, correcciones a realizar y tabla final de cumplimiento/faltantes. Evitar vueltas largas.
4. Renderizar con:

```bash
"$SKILL_ROOT/.venv/bin/python3" "$SKILL_ROOT/scripts/render_utp_fisc_review_pdf.py" revision.md revision.pdf
```

5. Verificar:
   - PDF existe y tiene tamaño > 0.
   - Logos aparecen en encabezado.
   - Paginación aparece.
   - Veredicto y secciones clave aparecen.
   - No hay placeholders visibles.

## Frontmatter soportado

Campos recomendados:

```yaml
title: "Revisión de Anteproyecto UTP/FISC"
student: "Nombre del estudiante"
submitted_by: "Nombre del estudiante"
document_type: "Anteproyecto"
modality: "Práctica Profesional"
career: "Licenciatura en Desarrollo y Gestión de Software"
thesis_document: "Título del documento/tesis"
source_document: "archivo_recibido.docx"
project: "Título del proyecto"
reviewer: "Erick Vicente Agrazal Lopez"
verdict_status: "desaprobado" # aprobado | cambios_sugeridos | desaprobado
verdict_detail: "No enviar todavía. Corregir puntos marcados abajo."
version: "v1.0"
date: "YYYY-MM-DD"
confidentiality: "Uso académico interno"
page_size: "letter"
show_summary_table: true
show_metadata: false
show_body_title: false
```

Defaults:

- `reviewer`: Erick Vicente Agrazal Lopez
- `verdict_status`: `desaprobado` si hay duda
- `version`: v1.0
- `date`: fecha actual
- `confidentiality`: Uso académico interno
- `page_size`: letter

## Regla de estado

El estado se muestra dentro de la tabla inicial, no como tarjeta grande.

- `APROBADO` (`verdict_status: aprobado`): listo para enviar.
- `SOLICITUD DE REVISIÓN` (`verdict_status: cambios_sugeridos`): ajustes ligeros o mejoras no bloqueantes; color amarillo.
- `SOLICITUD DE REVISIÓN` (`verdict_status: desaprobado`): no enviar todavía; faltan correcciones importantes; color rojo.

Si `verdict_status` no está claro, asumir `desaprobado`. La sección `## Veredicto` se omite visualmente cuando `show_summary_table: true` porque el estado ya aparece en la tabla inicial.

## Estructura recomendada del PDF

1. Encabezado institucional con logos y título.
2. Tabla inicial compacta con documento/tesis, entregado por, versión y estado.
3. Correcciones a realizar, priorizadas y directas.
4. Tabla final de cumplimiento/faltantes.

La tabla de metadatos completa no se muestra por defecto; solo usar `show_metadata: true` cuando Erick pida más contexto administrativo. El título grande del cuerpo tampoco se muestra por defecto; el encabezado con logos ya identifica el documento. Usar `show_body_title: true` solo si Erick quiere formato más formal.

No incluir secciones largas de fortalezas, comentarios por sección o próximos pasos salvo que Erick lo pida. Ir directo a qué corregir.

## Estilo de contenido

- Español académico, claro y directo.
- Máximo una nota breve positiva si aporta contexto; no hacer sección larga de fortalezas por defecto.
- No prometer aprobación; usar `APROBADO`, `CAMBIOS SUGERIDOS` o `DESAPROBADO` como estado de revisión.
- Si Erick pide calificar, incluir en el PDF una calificación explícita sobre 100 y una rúbrica compacta por bloques; mantener el estado institucional como `APROBADO` o `SOLICITUD DE REVISIÓN` en la tabla inicial. No usar una tarjeta grande de nota.
- Separar problemas administrativos de problemas de contenido.
- En anteproyectos, revisar alcance, metodología, objetivos, bibliografía, cronograma y documentos administrativos.
- Si la fuente es PDF, basar la tabla de cumplimiento en extracción de texto + revisión visual de páginas críticas; las evidencias escaneadas (créditos, recibos, cartas firmadas) pueden no aparecer como texto pero sí contar como anexos visibles.
- En informes finales, revisar coherencia entre objetivos, metodología, resultados, conclusiones, referencias y anexos.
- Si hay IA, IoT, web, móvil o terceros como Layrz, exigir delimitación técnica: qué construye el estudiante, qué integra, qué configura, qué queda fuera y cómo se valida.

## Comandos útiles

Skill root (fuente de verdad en el workspace `universidad`; `~/.claude/skills/utp-fisc-review-pdf` es un symlink a esta ruta):

```bash
SKILL_ROOT="/Users/ea/Projects/universidad/.claude/skills/utp-fisc-review-pdf"
```

Render (usa el `.venv` propio de la skill: reportlab + PyYAML):

```bash
"$SKILL_ROOT/.venv/bin/python3" "$SKILL_ROOT/scripts/render_utp_fisc_review_pdf.py" ./revision.md ./revision.pdf
```

Si el `.venv` no existe (p. ej. clon nuevo), recrearlo una vez:

```bash
cd "$SKILL_ROOT" && python3 -m venv .venv && .venv/bin/python3 -m pip install -r requirements.txt
```

## QA antes de entregar

No entregar PDF hasta confirmar:

- Renderer exit code 0.
- PDF existe y no está vacío.
- Logos UTP/FISC presentes o, si faltan, fue marcado explícitamente.
- Encabezado y footer aparecen en páginas.
- Título breve `Resumen de revisión` aparece sobre la tabla inicial.
- Tabla inicial aparece full-width con documento/tesis, entregado por, versión y estado.
- Estado aparece pequeño dentro de la tabla: `APROBADO` o `SOLICITUD DE REVISIÓN`, con texto de color; no como recuadro grande.
- Correcciones a realizar aparecen inmediatamente después de la tabla inicial.
- Puntos principales numerados aparecen en negrita y ligeramente más grandes que las viñetas internas.
- Tabla final de cumplimiento/faltantes aparece.
- No hay placeholders como `[pendiente]`, `TODO` o “Aquí inserta”. Al verificar esto por texto extraído, buscar `TODO` con límites de palabra o mayúsculas exactas; no usar una búsqueda simple de `todo` en minúsculas porque da falsos positivos en palabras españolas como “metodología” o “todo/ todos” usados naturalmente.
- Nombre estudiante y tipo de documento correctos.
- Versión visible correcta.

QA visual recomendado antes de enviar (renderizar la página 1 a PNG y leerla con la herramienta Read):

```bash
pdftoppm -png -f 1 -singlefile -r 160 revision.pdf /tmp/revision_page1
# verificación de texto/placeholders sin binarios extra:
pdftotext revision.pdf - | grep -nE '\bTODO\b|\[pendiente\]|Aquí inserta' || echo "sin placeholders"
```

Luego leer `/tmp/revision_page1.png` con la herramienta Read y confirmar especialmente:
- no hay título duplicado en cuerpo si el encabezado ya identifica el documento;
- no aparece tarjeta/cuadro grande de estado;
- el estado está contenido en la tabla inicial como texto pequeño de color;
- la tabla ocupa casi todo el ancho útil;
- las correcciones principales 1, 2, 3... destacan más que sus viñetas internas;
- no hay secciones huérfanas al final de página. Si ocurre, insertar `<!-- pagebreak -->` antes del punto que quedó cortado.

## Pitfalls

- Esta habilidad no es para propuestas comerciales.
- No usar cover page por defecto.
- No usar estilo con sombras/halos.
- No mezclar criterios de anteproyecto y final sin indicar el tipo de documento.
- No inventar información administrativa ausente; marcarla como ausente/no visible.
- If se actualiza una revisión, bump versión visible antes de renderizar.
- Renderer soporta `<!-- pagebreak -->` para evitar títulos/correcciones huérfanas al final de página.
- Evitar backticks para frases largas extraídas del documento del estudiante (fechas, nombres, oraciones completas). El renderer las muestra en monoespaciado y puede crear espaciado visual raro en Telegram/PDF. Usar comillas normales para citas largas y reservar backticks para placeholders cortos, comandos, nombres de campos o errores puntuales como `X`, `TODO`, `Vo.Bo.`.
