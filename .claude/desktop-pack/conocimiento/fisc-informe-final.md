---
name: utp-fisc-final-doc-review
description: Revisar informes finales de Trabajo de Graduación UTP/FISC en español, verificando estructura, formato, mínimo de páginas, rúbricas de evaluación y requisitos de sustentación según reglamento FISC 2018.
version: 1.0.1
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [UTP, FISC, informe-final, trabajo-de-graduacion, tesis, sustentacion, revision-academica, Panama]
    related_skills: [utp-fisc-review-pdf]
---

# UTP/FISC final document review

## Cuándo usar

Usar cuando Erick pida revisar, auditar, corregir, comentar o preparar el informe final de Trabajo de Graduación UTP/FISC, incluyendo tesis teórica, tesis teórico-práctica o práctica profesional.

## Estilo para Erick

- Responder en español.
- Empezar con elogio breve y específico.
- Luego correcciones concretas, académicas y priorizadas.
- Separar problemas de contenido, formato, evaluación y entrega administrativa.
- Cuidar especialmente coherencia entre objetivos, metodología, desarrollo, pruebas/resultados, conclusiones y recomendaciones.
- Si Erick adjunta un PDF/DOCX de tesina/informe final y pide “revisa”, “revísalo” o equivalente, entregar la revisión completa **en markdown** (veredicto, riesgos priorizados, checklist FISC, rúbrica estimada, correcciones por capítulo, siguiente paso). En este entorno no se genera el PDF institucional; si Erick lo quiere con logos UTP/FISC, debe correr la skill `utp-fisc-review-pdf` en Claude Code (Mac) sobre este markdown.
- Si el trabajo mezcla plataforma propia, Layrz, IoT, web, móvil o IA, exigir delimitar qué fue construido por el estudiante, qué fue integrado/configurado, qué evidencia demuestra aporte propio y qué queda fuera.

## Base normativa resumida

Fuente: Reglamento FISC 2018 para inscripción, asesoría y sustentación de Trabajos de Graduación; anexos de portada/lomo, estructura final y rúbricas de evaluación.

## Estructura obligatoria del informe final

Debe contener:
1. Página de título: portada, primera hoja y lomo según Anexo 5.
2. Resumen de 250 a 500 palabras.
   - Teórico / Teórico-Práctico: tema, objetivos, metodología usada, resultados generales y palabras clave.
   - Práctica Profesional: resumen de práctica, actividades desarrolladas y aportes realizados.
3. Dedicatoria.
4. Agradecimientos.
5. Índice general automático, con niveles jerárquicos.
6. Índice de figuras si aplica.
7. Índice de tablas/cuadros/gráficas si aplica.
8. Introducción: idea general del tema y secciones que componen el documento.
9. Cuerpo del trabajo: desarrollo completo y documentación respectiva, dividido lógicamente en capítulos/secciones.
10. Conclusiones: afines al trabajo y objetivos, enumeradas en orden lógico.
11. Recomendaciones: sugerencias relacionadas al trabajo realizado.
12. Referencias bibliográficas: APA o IEEE, generadas automáticamente, en orden alfabético de autor cuando aplique.
13. Anexos: documentos complementarios; deben respetar márgenes y numeración.

## Formato obligatorio

- Papel carta 8.5 x 11.
- Márgenes: derecho, superior e inferior 1.0 pulgada; izquierdo 1.5 pulgadas.
- Fuente Arial 12 en todo el documento.
- Interlineado 1.5.
- Numeración en centro del margen inferior.
- Carátula y páginas de título de capítulo cuentan, pero no muestran número.
- Páginas preliminares desde carátula hasta introducción usan romanos en minúscula: ii, iii, etc.
- Desde cuerpo del documento, numeración ordinal: 1, 2, 3...
- Figuras: número y título debajo.
- Tablas/cuadros/gráficas: número y título arriba.
- Si figura/tabla/gráfico viene de publicación, incluir referencia debajo.

## Extensión y entrega

- Mínimo 75 páginas para documento final.
- Para cómputo de páginas se excluyen: hoja de presentación, resumen, dedicatoria, agradecimiento, índices, introducción, referencias bibliográficas y anexos.
- Redacción final debe ser revisada y certificada por persona con dominio del español.
- Para solicitar sustentación se entrega al Decanato, con al menos 10 días hábiles previos a fecha solicitada:
  - un original y dos copias del informe final sin empastar
  - certificación de revisión de redacción
  - copia digital en formato de procesador de texto
  - formulario de solicitud de sustentación
- Nota de plazo: Art. 56 exige mínimo 10 días hábiles; el Anexo 4/formulario menciona 8 días hábiles. Recomendar cumplir 10 días y avisar la discrepancia si el estudiante usa el formulario.
- Después de aprobación final: un ejemplar impreso en papel bond, dos CD rotulados con informe y presentación, empastado en percalina verde FISC con letras doradas según formato.

## Plan de contenido esperado por modalidad

En todos los planes de contenido del Anexo 2, verificar secuencia común antes de capítulos propios: dedicatoria, agradecimiento, índice general, índice de tablas y figuras opcional, introducción y resumen/abstract.

### Teórico-Práctico

Revisar que cuerpo incluya, como mínimo:
- Antecedentes del proyecto: problemática, objetivo general/específicos, estructura
- Concepción del proyecto: metodología de trabajo y análisis
- Diseño del proyecto: diseño del software/sistema
- Desarrollo del proyecto: codificación, implementación, etapas de desarrollo y construcción
- Pruebas y validación: pruebas y validación de resultados
- Conclusiones
- Recomendaciones
- Referencias y bibliografía APA o IEEE
- Anexos si aplica

### Teórico

Revisar que cuerpo incluya:
- Identificación del proyecto: descripción, antecedentes/estado del arte, justificación, preguntas, objetivos, hipótesis si aplica
- Metodología: enfoque, procedimientos, instrumentos, estrategias, recursos, análisis e interpretación
- Desarrollo de investigación
- Resultados y discusión
- Conclusiones
- Recomendaciones
- Referencias y bibliografía APA o IEEE
- Anexos si aplica

### Práctica Profesional

Revisar que cuerpo incluya:
- Antecedentes de empresa: misión, visión, objetivos, políticas, organigrama, funciones, productos/servicios, áreas
- Descripción del proyecto: objetivos, justificación, problemática
- Actividades realizadas en empresa
- Resultados obtenidos
- Conclusiones con cursos/aspectos de carrera aplicados y lecciones aprendidas
- Recomendaciones, incluyendo recomendaciones para la carrera
- Referencias y bibliografía APA o IEEE
- Anexos si aplica

## Rúbricas de evaluación

### Trabajo Teórico: informe escrito 70%, presentación oral 30%

Informe escrito:
- Descripción del problema 0-5
- Antecedentes 0-5
- Justificación 0-5
- Preguntas de investigación y/o hipótesis 0-5
- Estado del arte / fundamentación teórica 0-5
- Objetivo general y específicos 0-5
- Metodología 0-10
- Resultados obtenidos 0-10
- Discusión: interpretación, conclusiones, perspectivas/trabajos futuros 0-10
- Calidad de referencias 0-5
- Formato: redacción, ortografía, diseño, gráficos, tablas 0-5

Presentación oral:
- Dominio del tema 0-10
- Material audiovisual 0-5
- Preguntas y respuestas 0-10
- Expresión oral 0-5

### Trabajo Teórico-Práctico: informe escrito 70%, presentación oral 30%

Informe escrito:
- Antecedentes: problema, objetivos, estructura 0-5
- Análisis/diseño del proyecto y metodología 0-15
- Desarrollo: codificación, implementación, instalación 0-20
- Pruebas y validación 0-15
- Consideraciones finales: conclusiones, recomendaciones, trabajos futuros 0-10
- Formato: redacción, ortografía, diseño, gráficos, tablas 0-5

Presentación oral:
- Dominio del tema 0-10
- Material audiovisual 0-5
- Preguntas y respuestas 0-10
- Expresión oral 0-5

### Práctica Profesional: evaluación mensual 35%, informe final 35%, presentación oral 30%

Informe escrito:
- Antecedentes: empresa, servicios/operación, proyecto, objetivos, puesto 0-5
- Actividades realizadas y grado de participación 0-10
- Aplicación de conocimientos, cursos/aspectos de carrera, resultados 0-10
- Conclusiones y recomendaciones 0-5
- Formato: redacción, ortografía, diseño, gráficos, tablas 0-5

Presentación oral:
- Dominio del tema 0-10
- Material audiovisual 0-5
- Preguntas y respuestas 0-10
- Expresión oral 0-5

## Procedimiento de revisión

1. Identificar modalidad, carrera, título, estudiante(s), asesor, fecha y versión.
2. El usuario **adjunta el PDF/DOCX en el chat**; léelo directamente del adjunto (texto y páginas escaneadas). No hay acceso al disco local ni ejecución de scripts. Si algo no se puede verificar solo con el adjunto, decirlo.
3. Extraer no solo texto completo: guardar también snippets de portada/preliminares, índice, inicio de capítulos, pruebas/resultados, conclusiones/recomendaciones, referencias y anexos. Para PDFs largos, inspeccionar páginas por palabras clave (`RESUMEN`, `ÍNDICE`, `CAPÍTULO`, `CONCLUSIONES`, `REFERENCIAS`, `ANEXOS`) leyendo esos rangos con la herramienta Read. Para DOCX, además del texto convertido con `textutil`, inspeccionar señales estructurales: `docProps/app.xml` (`Pages`, `Words`, `Paragraphs`, `Lines`), secciones/márgenes/tamaño de papel, estilos usados, fuentes/tamaños directos, índices de figuras/tablas y pies de figura. Esto permite detectar problemas FISC como margen izquierdo 1.0" vs 1.5", índices sin actualizar y numeración de figuras inconsistente.
4. Si se puede, calcular páginas computables y advertir si no llega a 75 excluyendo preliminares, introducción, referencias bibliográficas y anexos. En DOCX con `Pages` totales cerca de 75-85, tratarlo como riesgo si el cuerpo útil inicia después de preliminares y termina antes de bibliografía; pedir conteo desde primer capítulo hasta antes de referencias/anexos y recomendar ampliar contenido sustantivo/anexos técnicos, no relleno. En PDFs finales, estimar desde el índice y numeración visible: cuerpo útil desde primer capítulo hasta antes de referencias/anexos; indicar “cumple con margen justo” si queda cerca de 75, porque páginas capitulares o páginas muy livianas podrían excluirse informalmente.
5. Crear checklist de estructura obligatoria.
6. Revisar contenido contra modalidad y rúbrica.
7. Si Erick dice “califica”, “ponle nota” o “esta es para entrega final”, incluir una calificación estimada por rúbrica además del veredicto. Para Práctica Profesional, puntuar informe escrito sobre 35 (5 antecedentes + 10 actividades/participación + 10 aplicación/resultados + 5 conclusiones/recomendaciones + 5 formato) y, si ayuda, convertirlo aproximadamente a /100 aclarando que no incluye evaluación mensual ni sustentación oral.
8. Revisar coherencia:
   - objetivos vs capítulos
   - metodología vs desarrollo
   - pruebas/resultados vs conclusiones
   - recomendaciones vs hallazgos
   - referencias vs estado del arte
   - si Erick aporta comentarios previos del estudiante/documento, usarlos como baseline explícito: verificar punto por punto si quedaron resueltos, parcialmente resueltos o pendientes, y priorizar hallazgos nuevos después de ese seguimiento.
9. Revisar evidencia del aporte propio:
   - diseño propio
   - implementación propia
   - configuración/integración propia
   - pruebas propias
   - resultados medibles
10. Revisar formato visible si el archivo lo permite; si solo hay texto extraído, marcar formato como no verificable. Para PDF final, verificar especialmente: carta 8.5x11, Arial 12 visible, numeración preliminar en romanos minúsculos, páginas capitulares sin número visible, y numeración ordinal del cuerpo.
11. Entregar correcciones priorizadas y texto sugerido cuando sea útil, en markdown. Para calificación final, usar un encabezado tipo `Calificación de Informe Final UTP/FISC`.

## Formato de respuesta recomendado

Veredicto: [Listo para revisión del asesor / Aprobable con correcciones / Riesgo ante tribunal / No listo]

Fortalezas:
- [2-3 puntos concretos]

Riesgos principales:
1. [Riesgo] ...
   Impacto en rúbrica/reglamento: ...
   Corrección recomendada: ...
   Texto sugerido si aplica: ...

Cumplimiento FISC:
- Estructura final: ...
- Resumen 250-500 palabras: ...
- Índices automáticos: ...
- Introducción: ...
- Cuerpo/capítulos por modalidad: ...
- Conclusiones alineadas a objetivos: ...
- Recomendaciones: ...
- Referencias APA/IEEE: ...
- Anexos: ...
- Formato: ...
- Mínimo 75 páginas computables: ...
- Certificación de revisión de español: ...
- Documentos para sustentación: ...

Rúbrica estimada:
- [criterio] alto/medio/bajo + razón breve

Correcciones por capítulo:
- Capítulo/Sección: problema + acción concreta

Siguiente paso:
- [acción única de mayor impacto]

## Reglas de calidad

- Si revisión es parcial, decir: “Revisión limitada al material recibido”.
- No afirmar cumplimiento de formato si solo se extrajo texto plano.
- No prometer aprobación; hablar en términos de riesgo, preparación y evidencia.
- Si el documento tiene IA, exigir métricas, datos, validación y limitaciones.
- Si el documento tiene IoT, exigir arquitectura, dispositivos, protocolo, datos, seguridad básica y pruebas.
- Si el documento es software, exigir módulos, usuarios, roles, diseño, implementación, pruebas y validación de resultados.
- Si el documento usa servicios externos, distinguir uso/integración de aporte propio.

## Verificación antes de finalizar

Confirmar que respuesta incluyó:
- veredicto
- elogio breve
- riesgos priorizados
- checklist FISC
- revisión por modalidad
- rúbrica estimada o criterios afectados
- siguiente paso concreto
