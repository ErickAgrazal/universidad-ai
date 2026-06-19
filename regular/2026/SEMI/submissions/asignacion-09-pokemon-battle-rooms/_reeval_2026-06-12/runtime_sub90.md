# Re-evaluación por ejecución — grupo <90 (repos clonados) — 2026-06-13
Mongo :27019. La ejecución mide CALIDAD; la penalización por tardanza se conserva. Criterio uniforme: 100 = stack completo (TanStack Start) + motor verificado por tests + seed; tope ~97 si motor verificado pero sin TanStack Start; sin cambio si motor sin pruebas.

## Tanda 1 (241)
- BARRERA, ROY (88, no tardía): install ok, 0 tests, seed ok (20 pkmn), NO TanStack Start. Motor no verificable + sin Start. SIN CAMBIO. Feedback: agregar tests del motor; migrar a TanStack Start.
- CARLOS JAEN (86 = base 96 −10 tardía): install ok, 2 tests del motor pasan, TanStack Start SÍ, seed ok. Base 96 justa (suite delgada, no full). SIN CAMBIO (tardía intacta). Feedback: ampliar pruebas del motor.
- GONZALEZ, GABRIEL (85, no tardía): 0 tests, seed ok (17), NO TanStack Start. SIN CAMBIO. Feedback: tests del motor + TanStack Start.
- MARTINEZ, ANGEL (83, no tardía): 0 tests, seed ok (20), NO TanStack Start. Backend con features pero no verificado. SIN CAMBIO. Feedback: tests del motor + TanStack Start.

## Tanda 2
- PAN, YINI (86, no tardía): 0 tests, seed ok (20), NO TanStack Start (Hono+TanStack Router). SIN CAMBIO. Feedback: tests del motor + TanStack Start.
- VARCASIA, ANLLELINA (81 = base 91 −10 tardía): 0 tests, seed ok (20), NO TanStack Start (Router+Vite+Clerk). SIN CAMBIO. Feedback: tests del motor + TanStack Start.
- BARRIOS, JUSTIN (75, no tardía): 0 tests ejecutables (script e2e sin config/specs), seed ok (20), NO TanStack Start (react-router-dom v7). SIN CAMBIO. Feedback: implementar pruebas + TanStack Start.
- CACERES, JORGE (85, no tardía): stack EQUIVOCADO — SQLite+Express+Vite, no Mongo/Hono/TanStack Start; sin tests ni seed. SIN CAMBIO. Feedback: el stack obligatorio era TanStack Start+Hono+MongoDB+Bun; agregar pruebas.

## Tanda 3 (242) + hallazgos de datos
- DELGADO, FERNANDO (84, no tardía): 0 tests, seed ok (40 pkmn), NO TanStack Start (Hono+Mongoose+TanStack Router). SIN CAMBIO. Feedback: tests del motor + TanStack Start.
- CUBILLA, GABRIEL (75 = base 85 −10 tardía): el clon local NO contiene proyecto A9 (solo lab1 + app encuestas Playwright). No verificable localmente; la nota original (75) se asignó con otra fuente. SIN CAMBIO. NO bajar por clon incompleto.
- GONZALEZ, FABIANA (88, no tardía): DISCREPANCIA — el repo solo tiene READMEs, cero código en todas las ramas e historial. No concuerda con 88. FLAG al profesor; no se actúa sin confirmar (posible entrega por otro repo/enlace).
- MENA, ELIAB (86 tardía): carpeta grupo-2/MENA_ELIAB tiene el repo EQUIVOCADO (luisa2212/guerra-luisa). Clon correcto: revisiones/reclamos_2026-05-23/ELIAB_poke-std6-v8 (re-verificado aparte).

## Tanda 4 (242)
- MENA, ELIAB (86 = base 96 −10 tardía; clon correcto en revisiones): 0 tests, seed ok (20 pkmn + 127 typeRelations), NO TanStack Start (Hono+Mongo OK; cliente Vite+TanStack Router). SIN CAMBIO. Feedback: tests del motor + TanStack Start.
- SANTIAGO, CESAR (80, no tardía): 0 tests; seed ROTO (importa modelos inexistentes src/server/models); el server usa Maps en memoria, no Mongo; NO TanStack Start. 80 ya es generoso. SIN CAMBIO. Feedback: arreglar persistencia Mongo, agregar tests, usar TanStack Start.
- WU, IVAN (75 = base 85 −10 tardía): 0 tests; NO usa MongoDB (Express+socket.io en memoria); NO TanStack Start. No cumple 4 requisitos del stack. SIN CAMBIO. Feedback: usar el stack obligatorio (TanStack Start+Hono+MongoDB+Bun), persistencia y tests.

## CONCLUSIÓN grupo <90 (14 repos clonados, ambos salones)
CERO cambios de nota. Todos confirmados justos o incluso generosos por ejecución: ninguno tiene suite de tests que pase para verificar el motor; la mayoría no usa TanStack Start; varios tienen persistencia rota/ausente o stack equivocado. Las penalizaciones por tardanza se conservan.

Flags de calidad de datos para el profesor:
- GONZALEZ, FABIANA (88): el repo clonado SOLO tiene READMEs, cero código en todas las ramas/historial. No concuerda con 88. Revisar su entrega real (¿otro repo/enlace?).
- CUBILLA, GABRIEL (75): el clon no contiene proyecto A9 (solo lab1 + encuestas). Nota asignada con otra fuente.
- MENA, ELIAB (86): carpeta grupo-2/MENA_ELIAB tiene el repo equivocado (luisa2212/guerra-luisa); clon correcto verificado en revisiones/reclamos_2026-05-23/ELIAB_poke-std6-v8.
- ~20 estudiantes <90 más no tienen repo clonado local (no re-evaluables sin re-clonar).

## Feedback aplicado al grupo <90 (ambos salones) — 2026-06-14
- 1GS241: 16 estudiantes con feedback (razón verificada/registrada + sugerencia de mejora), devueltos. Se coló y se quitó un stray (RIOS, GERALD, 0) antes de Return.
- 1GS242: 21 estudiantes con feedback + sugerencia, devueltos. Se coló y se quitó un stray (SUAREZ, JEAN, 0); se confirmó el conjunto exacto antes de Return.
- Total 37 feedbacks. CERO cambios de nota (todos confirmados justos por ejecución/registro).
- Excluidos los 0/no-entregó (sin proyecto que sugerir): 241 BEITIA, DUARTE, QUINTERO, RIOS, TORRES; 242 Cisneros, IZARRA, ORTEGA HECTOR, SUAREZ.
- Fuente de los textos: _reeval_2026-06-12/feedback_sub90.json.
- Lección Teams: la ÚLTIMA fila de la tabla (alfabéticamente, p.ej. WU) no renderiza su editor de feedback con viewport normal; se resolvió agrandando el viewport (height 1700) para que la fila no quede cortada. Los stragglers de selección (filas 0 adyacentes) se cuelan en la selección masiva: verificar el conjunto exacto antes de Return.
