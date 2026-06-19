# Dry-run de Asignación 6 con el skill grade-teams-lab

Objetivo: validar que el skill funciona para otra asignación. **No se entraron grades a Teams.**

## Lo que funcionó ✅

1. **Extracción de rúbrica** vía Teams (Open pop up rubric grader) → `RUBRIC.md` generado correctamente
2. **Adaptación del grader**: copié `grade_template.py` → `grade_playwright.py` y solo cambié:
   - `find_project_root()` → `find_playwright_root()` con keywords distintos (`pollclass-playwright`, `lab6`, `playwright`)
   - Patrones de análisis: cuento `test()`, `expect()`, indicadores negativos en `.spec.ts`
   - Mapeo a rúbrica (4 criterios × 25% en lugar de 5 × 20%)
3. **Reutilización de los repos clonados**: usar los mismos repos de A5 ahorró ~60 git clones
4. **Output estructurado**: `GRADING-A6.md` por estudiante + scores agregados

## Lo que requirió verificación (igual que A5)

- **Cluster de 25s**: 6 estudiantes en g1 y 9 en g2 con score 25. Spot-checked ABREGO_YIREIKIS:
  - Tiene 4 branches en su repo. None contiene `*.spec.*` ni `playwright.config*`.
  - Sus otros repos (yireii, ds4, secretsanta) tampoco son Playwright.
  - **Conclusión**: probablemente no entregó A6, o lo hizo en repo privado al que no tengo acceso.

- **Discrepancia con grades pre-existentes en Teams**: 4 estudiantes (ACOSTA, APARICIO, ATHANASIADIS, BARRERA) ya tenían 100 en Teams. Mi dry-run les dio 81, 88, 69, 88 respectivamente. Esto es esperado — el grader es heurístico y tu juicio es la fuente de verdad. Casos a investigar:
  - ATHANASIADIS = 69 vs tu 100 → mi grader puede estar penalizando algo (poca cobertura detectada)
  - El grader debería re-calibrarse antes de aplicar

## Gaps del skill que el dry-run reveló

1. **Phase 2 ("discover repos") asume nuevos repos por asignación**, pero Lab 6 generalmente vive en el MISMO repo de PollClass. El skill debería decir explícitamente: "antes de clonar, primero busca Lab N dentro de los repos ya clonados de Lab N-1".

2. **Detección de "trabajo no entregado" vs "detección fallida"** es ambigua con scores 25. El skill debería:
   - Marcar 25s con "AUTO_DEFICIENTE" vs "NO_TRABAJO_DETECTADO"
   - El segundo caso requiere check manual obligatorio antes de entrar en Teams

3. **El grader heurístico de Playwright es MÁS ruidoso que el de PollClass**: muchos tests pueden estar en archivos sin convención `.spec.` (e.g. `tests/poll-vote.ts`). Necesita una heurística adicional: cualquier `.ts/.js` que importe `@playwright/test` cuenta como test file.

4. **No detectamos bitácora bien**: muchos students tienen el log en `README.md` del Lab 6 dir, no en archivo separado. El grader actual penaliza Bitácora=1 para varios que sí tienen documentación.

## Resultado del dry-run

Group 1: 32 estudiantes evaluados, avg=73, 12 below 80 (necesitan verificación manual)
Group 2: 37 estudiantes evaluados, avg=67, 17 below 80 (necesitan verificación manual)

**No se entró ninguna nota en Teams**. Los `GRADING-A6.md` quedaron en cada carpeta como referencia.

## Actualización propuesta al skill

Voy a:
1. Agregar gotcha #10: "Lab N tests often live inside the Lab N-1 repo" 
2. Agregar gotcha #11: "Score 25 = ambiguous — distinguish 'no work' from 'detection failed'"
3. Mejorar `grade_template.py` con detección por imports (`import * from '@playwright/test'` etc.)
