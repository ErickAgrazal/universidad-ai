# Memoria operativa del curso

> **Nota de reubicación (2026-06-11)**: este archivo es la memoria del curso DS_IX 2026-SEMI y vive en `universidad/2026/SEMI/`. El directorio se reorganizó por año/semestre; las rutas históricas de abajo (`submissions/`, `materials/`, `pdf-qa/`, `scripts/`, …) resuelven relativas a esta carpeta `SEMI/`.

## 2026-05-22

### Programa oficial — Desarrollo de Software IX

- Fuente oficial del programa: `/Users/ea/Downloads/1493 DS_IX  Programa de Asignatura.pdf`.
- Resumen estructurado guardado en `COURSE_PROGRAM_DS_IX.md`.
- Datos generales:
  - Asignatura: **Desarrollo de Software IX**.
  - Código: **1493**.
  - Créditos: **4**.
  - Horas semanales: **2 teoría + 4 laboratorio**.
  - Requisito: **haber aprobado tercer año**.
- Propósito del curso: consolidar fundamentos de programación y llevar al estudiante al diseño e implementación de soluciones **Full Stack** con arquitectura cliente-servidor, backend, frontend y bases de datos.
- Competencia específica: desarrollar soluciones Full Stack integrando arquitecturas cliente-servidor, servicios backend, interfaces frontend y bases de datos, aplicando metodologías de programación, principios de ingeniería de software, calidad y seguridad informática.
- Resultado de aprendizaje principal: integrar frontend, backend y bases de datos en una aplicación web funcional usando frameworks y buenas prácticas de calidad y seguridad.
- Módulos oficiales:
  1. **Formulación de Proyectos Full Stack** — 2 semanas: problema, objetivos, alcance, requerimientos, arquitectura, desarrollo y pruebas.
  2. **Fundamentos Tecnológicos y Entorno de Desarrollo Full Stack** — 3 semanas: arquitectura Full Stack, frameworks, herramientas, Node.js, npm, Express.js, React y MongoDB.
  3. **Desarrollo e Implementación de Aplicaciones Full Stack** — 11 semanas: Node.js, Express, rutas REST, middlewares, errores, documentación de APIs, seguridad con cifrado y JWT, MongoDB/Mongoose/CRUD, React, hooks, formularios e integración frontend-backend.
- Metodología oficial: aprendizaje basado en problemas y proyectos, estudios de caso, demostraciones, exposición/discusión de ejemplos, ejercicios cortos, modelos experimentales, pruebas parciales y semestral, con trabajo individual y colaborativo.
- Evaluación oficial del PDF es recomendada/general: parciales hasta 33%, semestral entre 33% y menos de 50%, otras actividades hasta 33%. Para operación real del curso 2026 se mantiene la ponderación indicada por el profesor en esta memoria: Parciales 30%, Proyectos/Investigaciones 15%, Laboratorios 15%, Portafolio 5%, Semestral 30%, Asistencia 5%.
- El PDF del programa quedó en **Class Materials** en ambos salones Teams (`DES__SOFT_IX_1GS241_2026` y `DES__SOFT_IX_1GS242_2026`) con un único archivo por salón llamado `PROGRAMA_DE_ASIGNATURA.pdf`.
- Skill reutilizable creado: `dsix-chapter-pdf` en `/Users/ea/.codex/skills/dsix-chapter-pdf`.
  - Uso: generar capítulos PDF docentes para Desarrollo de Software IX siguiendo el programa oficial, el patrón visual del capítulo 1 y revisión visual antes de entregar.
  - Recursos: `references/course-program-dsix.md`, `references/chapter-pattern.md`, `scripts/build_chapter_pdf_template.py`.
  - Regla operativa: entregar el PDF aquí primero; no subirlo a Teams sin confirmación explícita.

### A8 — Parcial Teórico

- Política confirmada para preguntas de escoger varias/mejor respuesta:
  - **3 pts** solo si está perfecta.
  - **1 pt** si marcó al menos una opción correcta/buena, aunque haya omitido otras correctas o marcado una mala.
  - **0 pts** solo si no tiene ninguna buena.
- Preguntas abiertas:
  - Analizar contenido y asignar hasta 10 pts con criterio estricto.
  - Los 10 no deben ser fáciles; solo respuestas realmente completas merecen 10.
  - Si escribieron algo razonable, evitar bajar de 5 salvo respuestas vacías, irrelevantes o muy malas.
- Se auditó y corrigió A8 en ambos salones.
- Las preguntas abiertas quedaron calificadas para todos los estudiantes.
- Los ceros restantes son intencionales por respuestas en blanco o muy malas.
- Caso corregido explícitamente: pregunta TanStack donde el estudiante marcó Query/Router y una mala, pero omitió Table. Bajo esta política debía ser **1/3**, no 0.

### A9 — Proyecto individual: Pokemon Battle Rooms

- A9 fue creada/publicada en ambos salones el 2026-05-22.
- Fecha de entrega: **viernes 22 de mayo de 2026 11:59 PM**.
- Entrega tardía: hasta **sábado 23 de mayo de 2026 11:59 PM**.
- Inicialmente quedó adjunta una rúbrica `Asignacion9-PokemonBattleRooms` en modo **No points**.
- Teams desactivó la posibilidad de poner nota porque mostraba `Points are disabled for the selected rubric`.
- Corrección aplicada:
  - Se quitó la rúbrica sin puntos de ambas asignaciones publicadas.
  - Se configuró el campo real de nota en **100 pts**.
  - Verificado en Teams: ambas tablas de revisión muestran `/ 100`.
- No volver a adjuntar una rúbrica Teams sin puntos para A9.
- Usar la rúbrica resumida del enunciado/PDF como guía manual, o crear una rúbrica puntuable nueva solo si Teams permite confirmar que suma 100 pts antes de publicarla.
- A9 todavía **no está calificada**; solo está creada y corregida para permitir notas.

### Sistema de matrícula UTP — Precalificación

- Credenciales funcionales están guardadas en `~/.env.utp` con permisos `600`. No copiar credenciales a `MEMORY.md`, `AGENTS.md` ni respuestas.
- Para entrar: `matricula.utp.ac.pa` → perfil **PROFESOR(A)**.
- Ruta útil: **Lista de Precalificación / Capturar Precalificaciones**.
- Grupos visibles:
  - `1GS241` — Desarrollo de Software IX, codasig 1493, codhora 5208.
  - `1GS242` — Desarrollo de Software IX, codasig 1493, codhora 5214.
- El campo de captura se llama **Puntaje 8va Semana** y acepta puntuación numérica por estudiante.
- Ponderación del curso indicada por el usuario:
  - Parciales: **30%**
  - Proyectos / investigaciones: **15%**
  - Laboratorios: **15%**
  - Portafolio: **5%**
  - Semestral: **30%**
  - Asistencia: **5%** — todos tienen asistencia completa.
- Clasificación confirmada de asignaciones:
  - Parciales: A7, A8.
  - Proyectos / investigaciones: A2, A3, A4.
  - Laboratorios: A1, A5, A6.
  - Portafolio: sin asignación cargada todavía.
  - Semestral: sin asignación cargada todavía.
- Para la precalificación de 8va semana se generó preview recomendado con:
  - Fórmula corregida tras reclasificar A1 como laboratorio y agregar asistencia: `((Parciales*30) + (Proyectos/Investigaciones*15) + (Laboratorios*15) + (Asistencia*5)) / 65`.
  - Semestral excluido porque todavía no existe.
  - Portafolio excluido porque todavía no tiene asignación.
  - A9 excluida porque todavía no está calificada.
  - Asistencia completa para todos: 100 en el componente de asistencia.
  - Blancos sin nota en Teams excluidos; ceros explícitos sí cuentan.
- Archivos generados:
  - `precalificacion_8va_semana_recomendada.md`
  - `precalificacion_8va_semana_recomendada.csv`
  - `precalificacion_oficial_rosters.json`
  - Export Gradebook Teams para `1GS241` y `1GS242` en `.xlsx`.
- Promedios del preview recomendado:
  - `1GS241`: **81.2**
  - `1GS242`: **82.2**
- Pendiente antes de enviar en matrícula: `AGUILAR, JOHANNED` aparece en matrícula `1GS242` pero no aparece en Teams Gradebook; hay que decidir nota o dejarlo en blanco.
- No presionar **Enviar** en matrícula sin confirmación explícita del usuario.

### UTP matrícula — justificar asistencia docente

- Login: usar credenciales guardadas en `~/.env.utp` y entrar al perfil **PROFESOR(A)**.
- Ruta del sistema:
  1. Menú lateral **Asistencia**.
  2. **Justificar Asistencia**.
  3. Filtros: Año `2026`, Periodo `I SEM.`
  4. Click **Buscar**.
- El listado muestra columnas: `Tipo`, `Fecha`, `Horario`, `Marcaciones`, `Periodos`, `Recuperados`, `Justificacion`, `Bloqueado`, acciones `Justificar` y `Recuperar`.
- Para justificar una fila:
  1. Click **Justificar** en la fila.
  2. En el formulario **JUSTIFICACIÓN DE ASISTENCIA IRREGULAR**, elegir `ENFERMEDAD` en `Justificación`.
  3. En `Observación`, escribir `Problemas estomacales`.
  4. Click **Registrar**.
  5. Confirmación esperada: `El registro ha sido insertado satisfactoriamente`.
  6. Volver a **Justificar Asistencia** y **Buscar** para verificar que la fila cambió a `ENFERMEDAD`.
- Selectores Playwright usados con éxito:
  - Perfil docente: texto exacto `PROFESOR(A)`.
  - Menú oculto: `#AJust` con `evaluate(el => el.click())` si el click normal falla por estar oculto.
  - Buscar asistencia: `#cphContenido_lnkbBuscar`.
  - Justificar filas: `#cphContenido_gvAsistencia_lnkbJustificar_0`, `#cphContenido_gvAsistencia_lnkbJustificar_1`, etc.
  - Fecha del formulario: `#cphContenido_txtFecha`.
  - Select de justificación: `#cphContenido_ddlJustifica`.
  - Observación: `#cphContenido_txtObservacion`.
  - Registrar: `#cphContenido_lnkbRegistrar`.
- Caso aplicado el 2026-05-22:
  - `30/04/2026`, horario `5:50 - 8:15`, `3` periodos: cambiado de `Sin Justificar` a `ENFERMEDAD`, observación `Problemas estomacales`.
  - `06/04/2026`, horario `5:50 - 8:15`, `3` periodos: cambiado de `Sin Justificar` a `ENFERMEDAD`, observación `Problemas estomacales`.
  - Ambas quedaron con `Recuperados: 0` y `Bloqueado: No`; el sistema todavía muestra acción `Recuperar`.
- Caso aplicado el 2026-06-06:
  - `01/06/2026`, horario `5:50 - 8:15`, `3` periodos: aparece verificado como `ENFERMEDAD CERTIFICADA`.
  - `02/06/2026`, horario `5:50 - 8:15`, `3` periodos: cambiado de `Sin Justificar` a `ENFERMEDAD CERTIFICADA`.
  - `03/06/2026`, horario `7:30 - 9:55`, `3` periodos: cambiado de `Sin Justificar` a `ENFERMEDAD CERTIFICADA`.
  - Observación usada para esta semana: `Problemas estomacales. Los estudiantes tuvieron actividades asignadas para realizar.`
  - Quedaron con `Recuperados: 0` y `Bloqueado: No`.

## 2026-05-23

### Regla operativa — repos locales antes de recalificar

- Antes de revisar, recalificar o responder reclamos sobre repositorios clonados localmente, **actualizar/verificar primero el remoto**.
- Flujo preferido:
  1. Ejecutar `git fetch --all --prune` en el clon local.
  2. Comparar contra `origin/main`, `origin/master` o la rama explícitamente entregada por el estudiante.
  3. Si el clon tiene archivos locales generados por nosotros (`GRADING.md`, `GRADING-A6.md`, reportes, etc.), **no hacer `git pull` directo** si puede mezclar o pisar cambios locales.
  4. En esos casos, revisar el remoto con `git ls-tree`, `git show origin/<rama>:<archivo>`, `git log origin/<rama>`, o crear una copia limpia temporal.
- Motivo: caso Einar Delgado, donde el clon local estaba viejo y el remoto actualizado sí contenía `README.md`, `Laboratorios/Lab_5`, Playwright y Pokemon. No volver a calificar solo con una copia local sin fetch previo.

### A9 — pull general y recalificacion por cambios remotos

- El 2026-05-23 se hizo `fetch --all --prune` a 114 repos locales bajo `submissions/`.
- Se revisaron cambios remotos contra las ventanas de entrega de cada asignacion.
- A5/A6: cambios nuevos detectados fuera de fecha, salvo casos de reclamo ya tratados individualmente.
- A7: no se ajustaron notas por esta pasada; en casos revisados, el codigo relevante no estaba dentro de la ventana o no ameritaba cambio.
- A9: se aplicaron dos ajustes en Teams, sin presionar `Return`:
  - `1GS241` / `VARCASIA, ANLLELINA`: **85 -> 91**.
  - `1GS242` / `DUTARY, CHRISTIAN`: **88 -> 93**.
- Trazabilidad local:
  - `submissions/asignacion-09-pokemon-battle-rooms/GRADE_PROGRESS.md`
  - `submissions/revisiones/pull_regrade_2026-05-23.md`

### Matricula UTP — precalificacion / mediado de semestre

- Ruta verificada el 2026-05-23: entrar a `matricula.utp.ac.pa`, perfil `PROFESOR(A)`, luego `Lista de Precalificacion / Capturar Precalificaciones`.
- En la pantalla `Consulta de Listados de Precalificacion`, seleccionar `Año: 2026`, `Periodo: I SEM.` y presionar `Buscar`.
- El sistema lista las dos secciones de Desarrollo de Software IX:
  - `1GS241`, codhora `5208`.
  - `1GS242`, codhora `5214`.
- En cada fila aparece `Ver Lista Precalificacion`. Al abrirla se muestra `Listado de Precalificaciones` con una caja de texto por estudiante en la columna `Puntaje 8va Semana`.
- Las cajas aceptan solo valores numericos (`KeyCheckNumeros`) y tienen `maxlength=5`.
- Al final de la lista hay dos acciones: `Regresar` y `Enviar`.
- Regla: no presionar `Enviar` sin confirmacion explicita del usuario, porque ese es el boton que registra/envia la precalificacion.

### Reclamos grupo 2 — 2026-05-23

- Tras `fetch`, se recalificaron reclamos del grupo 2 y se actualizaron Teams sin presionar `Return`.
- A9: `GUERRA, LUISA` blank -> 88, `MENA, ELIAB` 82 -> 96, `SZOBOTKA, RAMSES` 89 -> 93. `WONG, ADRIAN` queda 96 y `JARAMILLO, OMAR` queda 110.
- A6: `DUTARY, CHRISTIAN` 25 -> 94, porque el repo actualizado contiene `pollclass/tests` con config Playwright, 8 casos, assertions, casos negativos y documentacion.
- `CISNEROS, AXEL`: no se cambiaron A2/A3/A5 porque los links GitHub/SharePoint provistos no son accesibles; A4 ya estaba acreditada en grupo 11 con 88.
- Importante: la carpeta local A9 `grupo-2/MENA_ELIAB` apuntaba al repo de Luisa Guerra. Eliab se reviso desde un clon limpio en `submissions/revisiones/reclamos_2026-05-23/ELIAB_poke-std6-v8`.

### A9 — penalizacion por entrega tardia hoy

- Regla del usuario: en A9, toda entrega realizada el 2026-05-23 cuenta como entrega tardia y lleva **-10 puntos**. Agregar esta razon en comments.
- Penalizaciones aplicadas en Teams sin presionar `Return`:
  - `1GS241` / `CARLOS JAEN`: 96 -> 86.
  - `1GS241` / `VARCASIA, ANLLELINA`: 91 -> 81.
  - `1GS242` / `CUBILLA, GABRIEL`: 85 -> 75.
  - `1GS242` / `GUERRA, LUISA`: 88 -> 78.
  - `1GS242` / `MENA, ELIAB`: 96 -> 86.
- Comentario de penalizacion agregado, sin nota aun, para pendientes tardios: `RUIZ, ERIC`, `TORRES, ALYSON`, `ESPINO, SIMON`, `GONZALEZ, SAMUEL`.
- Revisión posterior de A9 encontró dos pendientes tardíos adicionales con nota en blanco y comentario de -10 agregado: `ORTEGA, ALLISSON` y `LOPEZ, ROBERTO`.
- Al devolver A9 calificadas por solicitud del usuario, apareció otro pendiente tardío sin nota: `FERREIRA, BRUNO`; se agregó comentario de -10.
- A9 devueltas en Teams el 2026-05-23: 21 entregas con nota en `1GS241` y 17 entregas con nota en `1GS242`. Las entregas sin nota quedaron sin devolver.
- Pasada adicional de devolucion de reclamos recalculados fuera de A9 el 2026-05-23:
  - `1GS241` A7: se devolvio `Martinez, Angel` con 100 pts; conteo confirmado `To return 14`, `Returned 22`.
  - `1GS241` A1/A3/A5/A6 ya estaban con `To return = 0`; no habia filas pendientes por devolver.
  - `1GS242` A6 ya estaba con `To return = 0`; no habia filas pendientes por devolver.

### Materiales teóricos por módulo — Desarrollo de Software IX

- Se generaron PDFs teóricos por módulo en `materials/modulos/` usando el patrón visual del skill `dsix-chapter-pdf`.
- Se renderizaron a PNG para QA visual en `pdf-qa/modulos/` y se revisaron hojas de contacto; no se observaron tablas cortadas ni páginas dañadas.
- Estructura local final:
  - `MODULO_01_FORMULACION_PROYECTOS/`
    - `CAPITULO_01_FORMULACION_PROYECTOS_FULL_STACK.pdf`
  - `MODULO_02_FUNDAMENTOS_TECNOLOGICOS/`
    - `CAPITULO_02_ARQUITECTURA_FULL_STACK_Y_CICLO_DE_DESARROLLO.pdf`
    - `CAPITULO_03_ENTORNO_HERRAMIENTAS_Y_CONFIGURACION_FULL_STACK.pdf`
  - `MODULO_03_DESARROLLO_IMPLEMENTACION/`
    - `CAPITULO_04_BACKEND_NODE_EXPRESS_APIS_REST.pdf`
    - `CAPITULO_05_SEGURIDAD_APIS_AUTENTICACION_JWT.pdf`
    - `CAPITULO_06_MONGODB_MONGOOSE_CRUD.pdf`
    - `CAPITULO_07_REACT_COMPONENTES_HOOKS_FORMULARIOS.pdf`
    - `CAPITULO_08_INTEGRACION_FRONTEND_BACKEND_PRUEBAS.pdf`
- Se crearon esas tres carpetas en **Class Materials** de ambos salones:
  - `DES__SOFT_IX_1GS241_2026`
  - `DES__SOFT_IX_1GS242_2026`
- Se subieron los 8 PDFs a cada salón, distribuidos en las carpetas correspondientes.
- Verificación final por SharePoint REST confirmó los mismos conteos y nombres en ambos salones: Módulo I = 1 PDF, Módulo II = 2 PDFs, Módulo III = 5 PDFs.

### Planificación de cierre — actividades pendientes para Teams

- El usuario confirmó que los contenidos de React, MongoDB y Bun/Hono ya se trabajaron de forma intrínseca en PollClass, Pokemon Battle Rooms y el parcial #2. Por tanto, **no conviene crear laboratorios básicos aislados** de React forms, MongoDB CRUD o Hono API.
- En su lugar, las siguientes actividades se planifican como cierre de curso y deben convertirse luego en asignaciones de Teams:
  1. **Parcial #3 teórico**:
     - Formato similar a A8: Forms creado desde Teams, no desde Forms directo.
     - 20 preguntas de escoger la mejor respuesta + 2 preguntas de desarrollo.
     - Total sugerido: 80 pts, como el parcial teórico anterior.
     - Temas: ReactJS, MongoDB/Mongoose, Bun y Hono, con preguntas de criterio técnico y escenarios, no solo memoria.
  2. **Refactor técnico de proyecto existente**:
     - Categoría tentativa: Laboratorio aplicado.
     - No crear un proyecto nuevo; cada estudiante/grupo mejora una parte real de un proyecto ya trabajado.
     - Posibles focos: separar lógica de negocio de handlers Hono, mejorar modelos Mongoose, limpiar estado React, agregar validaciones, mejorar manejo de errores o documentar contrato API.
  3. **QA sobre proyecto existente**:
     - Categoría tentativa: Laboratorio aplicado.
     - Validar flujos reales del proyecto propio, con evidencia de ejecución, hallazgos y correcciones.
     - No repetir A6 como laboratorio genérico; debe aplicarse a un producto existente.
  4. **Plan de evolución a MVP**:
     - Categoría tentativa: Proyecto / preparación del semestral.
     - Basado en el comercio electrónico del parcial #2.
     - Debe incluir diagnóstico del POC actual, backlog priorizado, alcance MVP, riesgos técnicos, arquitectura propuesta y demo/estado actual.
  5. **Semestral**:
     - El usuario ya tiene claro que será una mejora sustancial del comercio electrónico desarrollado en el parcial #2.
     - Objetivo: sacar el proyecto del estado POC y convertirlo en un MVP funcional, demostrable y más estable.
     - El usuario se reunirá con los estudiantes para empujar el desarrollo lo más posible antes de la entrega.

### Módulo extra — agentes de desarrollo con IA

- Se generó y publicó el PDF `MODULO_EXTRA_AGENTES_CLAUDE_CODE_OPENCODE_CODEX_MAYO_2026.pdf`.
- Ruta local: `materials/modulos/MODULO_EXTRA_AGENTES_DESARROLLO_IA/`.
- Tema: trabajo profesional con agentes como Claude Code, OpenCode y Codex; buenas prácticas para `AGENTS.md`/rules, skills, agentes/subagentes, MCPs, plugins, permisos, hooks y flujo production ready.
- Fuentes revisadas: documentación oficial de Claude Code, OpenCode, OpenAI/Codex, Model Context Protocol, Playwright MCP y GitHub MCP, con corte al **23 de mayo de 2026**.
- QA ejecutado:
  - `pdfinfo`: 9 páginas, tamaño carta.
  - `pdftotext`: texto extraíble y tabla de contenido correcta.
  - Render visual en `pdf-qa/modulo-extra-agentes/`; hoja de contacto revisada sin tablas cortadas.
- En ambos salones Teams/SharePoint se creó la carpeta exacta `modulo extra` dentro de **Class Materials**:
  - `DES__SOFT_IX_1GS241_2026`
  - `DES__SOFT_IX_1GS242_2026`
- Verificación SharePoint REST confirmó que ambos salones tienen el PDF con el mismo nombre y tamaño (`26025` bytes).

### Módulo extra — Git en desarrollo agéntico

- Se generó y publicó el PDF `MODULO_EXTRA_GIT_BUENAS_PRACTICAS_DESARROLLO_AGENTICO_MAYO_2026.pdf`.
- Ruta local: `materials/modulos/MODULO_EXTRA_AGENTES_DESARROLLO_IA/`.
- Tema: uso riguroso de Git cuando humanos y agentes modifican el mismo repositorio: ramas pequeñas, commits auditables, worktrees, pull requests, branch protection, CODEOWNERS, CI, conflictos, reglas para `AGENTS.md` y checklist production ready.
- Fuentes revisadas: documentación oficial de Git (`git-worktree` 2.54, abril 2026), Git book, GitHub protected branches, CODEOWNERS, GitHub Actions secure use, Claude Code worktrees, Codex `AGENTS.md` y OpenCode rules.
- QA ejecutado:
  - `pdfinfo`: 9 páginas, tamaño carta.
  - `pdftotext`: texto extraíble y tabla de contenido correcta.
  - Render visual en `pdf-qa/modulo-extra-git-agentes/`; hoja de contacto revisada sin tablas cortadas.
- Se subió a la carpeta `modulo extra` en ambos salones Teams/SharePoint:
  - `DES__SOFT_IX_1GS241_2026`
  - `DES__SOFT_IX_1GS242_2026`
- Verificación SharePoint REST confirmó que ambos salones tienen los dos PDFs del módulo extra:
  - `MODULO_EXTRA_AGENTES_CLAUDE_CODE_OPENCODE_CODEX_MAYO_2026.pdf` (`26025` bytes)
  - `MODULO_EXTRA_GIT_BUENAS_PRACTICAS_DESARROLLO_AGENTICO_MAYO_2026.pdf` (`25621` bytes)

### Ceros tardios — pull y recalificacion 2026-05-24

- Regla del usuario: para estudiantes que estaban en 0, hacer `pull` nuevamente; si aparece evidencia calificable, asignar nota con **-30 puntos** por entrega demasiado tardia, posterior al limite tardio aceptado.
- Pull general: 119 repos revisados, 10 con cambios. Tres repos tuvieron pull no fast-forward o bloqueo por archivos no rastreados, pero no afectaron ceros pendientes o ya estaban cubiertos por revisiones previas.
- Cambios aplicados en Teams:
  - `1GS241`: `TORRES, ALYSON` A1 0 -> 70, A2 0 -> 60, A5 0 -> 65.
  - `1GS241`: `APARICIO, ANA` A2 0 -> 60, A5 0 -> 60.
  - `1GS241`: `VALDESPINO, CHRISTIAN` A2 0 -> 60, A5 0 -> 65.
  - `1GS241`: `GARCIA, JACK` A3 0 -> 90 por correccion de pertenencia de grupo ya documentada; no fue penalizacion tardia.
  - `1GS241`: `CORDOBA, EMILY` A9 0 -> 62; base 92 menos 30.
  - `1GS241`: `GARCIA, CESAR` A9 0 -> 52; base 82 menos 30.
  - `1GS242`: `AVILA, JOSE` A9 0 -> 64; base 94 menos 30.
- Trazabilidad completa en `submissions/revisiones/revision_ceros_tardios_2026-05-24.md`.

### Reclamo puntual Eric Marin / Michael Portela — 2026-05-24

- Se acepto la invitacion privada de GitHub para `ericmarin05/2026-1GS242-marin-eric` y se revisaron A1, A2, A5, A6 y A9.
- Ajuste docente final para Eric Marin:
  - A1 = 100.
  - A2 = 20 final: base 40 por investigacion muy superficial, menos 20 por entrega el 2026-05-23.
  - A4 = 95 sin cambio.
  - A5 = 85 final: tarde, pero no demasiado; penalizacion -10.
  - A6 = 44 final: base 94 menos 50 por entrega demasiado tardia.
  - A9 = 77 final: base 92 menos 15.
- Recalculo local generado en `submissions/notas_actuales_2026-05-24-eric-marin/`; Eric queda con `raw` 78.5, `precalificacion` 79 y `aporte_actual_65` 51.03.
- Teams actualizado y verificado para Eric Marin en `1GS242`: A1 100, A2 20, A5 85, A6 44, A9 77. A4 se mantiene en 95.
- Trazabilidad en `submissions/revisiones/revision_marin_portela_2026-05-24.md`.
- Michael Portela: el repo exacto `miketela/2026-1GS242-portela-michael` sigue inaccesible (`Repository not found` / `Page not found`). El repo publico `miketela/pokemon-Game-` solo contiene README, sin proyecto calificable. Hace falta invitacion o repo publico correcto para recalificar.
- Actualizacion posterior: la invitacion del repo de Michael fue aprobada y el repo quedo accesible. A9 revisada en `6._Proyecto_PokemonGame`: commit principal 2026-05-23 23:14:26 y ajuste E2E 23:18:14, ambos dentro de la ventana tardia. Nota final A9 = 86 (base 96 menos 10). Teams actualizado y devuelto el 2026-05-24 12:31 PM. Recalculo local generado en `submissions/notas_actuales_2026-05-24-eric-marin-michael-portela/`; Michael queda con `raw` 68.62, `precalificacion` 69 y `aporte_actual_65` 44.6.

### Devolucion masiva Teams — 2026-05-24

- Por solicitud del usuario, se revisaron ambos salones y se devolvio todo lo pendiente en Teams.
- `1GS242`: A7 tenia 3 pendientes en `Ready to grade`; se devolvieron los 3. El resto de asignaciones revisadas quedo con `To return = 0` o sin entregas que devolver.
- `1GS241`: A7 tenia 14 pendientes en `Ready to grade`; se devolvieron los 14. El resto de asignaciones revisadas quedo con `To return = 0` o sin entregas que devolver.
- Total devuelto en esta pasada: 17. No se modificaron notas; solo se presiono Return/devolver.
- Trazabilidad en `submissions/revisiones/teams_return_all_2026-05-24.md`.

### Outlook / pendientes administrativos — 2026-05-24

- Limpieza de correo: se movieron a Elementos eliminados tandas de correos no importantes/promocionales, incluyendo `mensajes@listas.utp.ac.pa`, Anthropic login, KLM, Namecheap, Perplexity, Canva, ResearchGate, Microsoft Groups antiguos, reclutamiento/promos, Soluciones Analiticas, HAACI y correo sospechoso de honorary doctorate. No vaciar papelera salvo instruccion explicita.
- Regla para resumen de correos: ignorar por defecto promociones/listas y priorizar estudiantes, Teams, Secretaria Academica FISC, Vicedecanato, Decano FISC, Direccion de Investigacion, DPC, matricula/asistencia, practicas profesionales, notas, evaluaciones, contratos, encuestas y plazos.
- Zuleika / ausencias abril 2026: verificado en matricula UTP que las ausencias `06/04/2026` y `30/04/2026` estan justificadas como `ENFERMEDAD`; no volver a tratarlas como pendiente aunque aparezcan correos de recordatorio.
- Sindy Delosrios / correcciones: el usuario ya aviso a Luisa que se comunique con Sindy. No marcar como pendiente para el usuario salvo que pida seguimiento.
- Secretaria Academica FISC / encuesta modalidad de evaluacion semestral: el usuario ya lleno el formulario. No volver a marcar como pendiente.
- Matricula UTP / mid term: el usuario confirmo que ya aplico y subio las notas del mid term de sus estudiantes. No volver a listar como pendiente.
- Actas de profesor: el usuario confirmo que ya firmo y envio los montos de las actas de profesor. No volver a listar como pendiente.

## 2026-06-10 a 2026-06-12

### Asignaciones nuevas (sesiones con Claude Code)

- A11 `11. Parcial #3: React y Hono` creado como quiz Forms asociado en ambas secciones (20 MC 3 pts: 15 React 19 + 5 Hono; 2 desarrollo 10 pts; 80 pts; timer 30 min). Programado: 1GS241 lun 15-jun 7:30 PM (due 8:10 PM); 1GS242 mar 16-jun 7:30 PM (due 8:10 PM). Fuente auditable: `submissions/asignacion-11-parcial-react-hono/quiz.json`. Historial: se creó como "9.", se renumeró a 11 (el 9 era Pokemon Battle Rooms) y se renombró de "Parcial Teórico" a "Parcial #3" por instrucción del usuario. Drafts huérfanos de 241 ("7. Entrega de parcial #2" y "Untitled assignment") descartados con confirmación del usuario.
- A10 `10. Proyecto individual: Juego de Damas con IA A*` publicada 2026-06-11 en ambas secciones, due 12-jun 11:59 PM, cierre 13-jun 11:59 PM, 100 pts sin rúbrica Teams (lección A9). Requisitos: una de 5 variantes de damas vs computadora, A* OBLIGATORIO sin variaciones en microservicio Bun (criterio de mayor peso, 25 pts), login+ranking, pago en modo prueba, tests. Fuente: `submissions/asignacion-10-damas-astar/`. Pendiente de calificar.
- Próximo proyecto (A12, sin publicar): servidor MCP sobre el comercio electrónico del Parcial #2, integrado en Claude Code (.mcp.json) y ChatGPT (app/connector). Base documental ya publicada en Teams.

### Materiales (todo reemplazado en Class Materials de ambas secciones)

- Capítulos 2-8 extendidos de 5-6 a 10-14 págs (más teóricos, por corrección del usuario: material de estudio tipo libro, no tutorial). Nuevo pipeline: `scripts/chapters_ext/cap0N.py` + `scripts/build_module_pdfs_v2.py`; el builder viejo `build_all_module_pdfs.py` fue BORRADO (no re-crear).
- Capítulo 9 nuevo (integraciones externas: terceros, pagos, IA) — completa los temas de Módulo I U3; temario oficial 100% cubierto.
- Guía de estudio del Parcial #3 (React 19 y Hono) en MODULO_03; reescrita 2 veces hasta quedar teórica (v3).
- Módulo extra MCP (`MODULO_EXTRA_MCP_PROYECTOS_JUNIO_2026.pdf`) como base del A12.
- 15 diagramas vectoriales agregados en 11 documentos vía `scripts/diagrams.py` (capítulos 2-9, guía, módulos MCP y Git).
- Portafolio docente regenerado al 12-jun (A1-A11, materiales nuevos, bitácora, combinado con pypdf): `scripts/build_teacher_portfolio_pdfs.py`.

### Reorganización del workspace

- Estructura por año/semestre: `universidad/<año>/<SEM*>/`. Contexto genérico en `universidad/CLAUDE.md`/`AGENTS.md`; lo específico del semestre/asignatura en `SEMI/CLAUDE.md`/`AGENTS.md`/`MEMORY.md` (este archivo). Dumps de Playwright van a `SEMI/debug-dumps/`.
