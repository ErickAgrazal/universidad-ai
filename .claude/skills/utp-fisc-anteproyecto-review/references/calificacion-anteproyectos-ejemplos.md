# Calibración de calificaciones para anteproyectos UTP/FISC

Usar como referencia rápida cuando Erick pida “califica”, “nuevamente” o “revisa esta versión nueva”. No copiar narrativas de sesión; usar para calibrar severidad y evitar inflar notas.

## Rúbrica práctica sobre 100

- Cumplimiento estructural FISC: 25 pts.
- Contenido académico y coherencia: 25 pts.
- Alcance técnico y metodología: 25 pts.
- Presentación, anexos y referencias: 25 pts.

Rangos útiles:
- 70-74: base viable, pero no listo; faltan varios bloques o anexos claves.
- 75-84: aprobable con correcciones fuertes; contenido encaminado, pero hay bloqueos administrativos, bibliografía débil, cronograma deficiente o alcance ambiguo.
- 85-89: aprobable con correcciones administrativas/puntuales; contenido ya defendible, pero faltan firmas/Vo.Bo./checklist marcado o limpieza final.
- 90+: listo o casi listo; no debe tener bloqueos administrativos ni placeholders visibles.

## Ejemplos de calibración observados

### Uriel Reyna v2 — 78/100

Subió respecto al borrador inicial porque ya incluía formulario, metodología, carta/constancia/créditos visibles y bibliografía. Se mantuvo debajo de 80 por:
- tabla de estudiante/firma y Vo.Bo. vacíos;
- placeholder `X` en objetivo específico;
- bibliografía con cantidad pero calidad irregular;
- herramientas poco justificadas;
- alcance de Claude/automatización todavía ambiguo;
- checklist final sin marcar.

Lección: un documento con anexos visibles pero campos oficiales vacíos no pasa de “aprobable con correcciones fuertes”.

### Justin Barrios v3 — 84/100

Mejoró mucho por alcance técnico claro: distingue plataforma propia, Layrz, ThingsBoard, API, frontend, autenticación, QA, exclusiones y objetivos medibles. Se mantuvo en 84 por:
- “Registro Oficial del Tema” era tabla propia, no formulario oficial FISC;
- firmas/Vo.Bo. incompletos;
- fecha imposible de práctica;
- falta checklist final;
- cronograma era planificación por semanas, no Gantt visual;
- bibliografía necesitaba más actualidad.

Lección: buen contenido técnico no compensa bloqueo administrativo del formulario oficial.

### Uriel Reyna v3 — 85/100

Ya defendible: corrigió placeholder, justificó herramientas, agregó Gantt visual marcado, créditos oficiales, constancia, carta firmada y mejor delimitación de Claude. Se quedó en 85 por:
- formulario oficial presente, pero tabla de estudiante/firma/Vo.Bo. vacíos;
- checklist final sin marcar/revisado/fecha;
- nombre del asesor con puntuación/nombre formal inconsistente;
- bibliografía de 11 fuentes pero APA irregular y fuentes comerciales/blogs;
- sección 8.2 duplicada y anexos redundantes.

Lección: si el contenido está defendible y el Gantt/anexos existen, pero solo quedan firmas/checklist/bibliografía/formato, calibrar alrededor de 85-89, no 90+.

## Pitfalls de revisión

- No confiar solo en texto extraído: los anexos escaneados pueden verse completos en imagen aunque PyMuPDF extraiga casi nada.
- Si el cronograma visual tiene sombreado/color por mes, marcarlo como cumple con ajuste menor, no como vacío.
- Si el checklist final aparece pero todas las casillas están vacías, marcar `Parcial`, no `Cumple`.
- Si el formulario oficial aparece pero la tabla de estudiante/firma/Vo.Bo. está vacía, marcar `Parcial crítico`.
- Si la bibliografía tiene 10+ fuentes pero incluye muchas fuentes institucionales/comerciales/blogs y APA irregular, marcar `Parcial`: cantidad no equivale a calidad.
- Para práctica profesional, carta firmada cuenta como avance; aun así verificar si menciona supervisor, actividades, duración, horario/ubicación y si sello/membrete son legibles.
