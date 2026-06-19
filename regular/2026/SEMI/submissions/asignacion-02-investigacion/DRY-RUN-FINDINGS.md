# Dry-run de Asignación 2 con el skill grade-teams-lab

Objetivo: probar el skill con un tipo más — investigación/documentación con submission de PR.

## Características únicas de A2

| Aspecto | A2 | A5/A6 | A1 |
|---|---|---|---|
| Tiene rúbrica | Sí (7 criterios × 14.28%) | Sí | No |
| Tipo de submission | PR mergeado (no repo URL) | Repo URL | Repo URL |
| Trabajo | Markdown research + screenshots + git workflow | App / tests | README intro |
| State actual | 0/36 returned (recién empezaste a calificar) | A5: 36/36, A6: 4/36 | A1: 15/36 |
| Workflow del estudiante | Git branch + PR merge en repo de A1 | App nueva en repo | Crear repo |

## Workflow ejecutado

1. ✅ Phase 1 (extract rubric): 7 criteria con weights 14.28% c/u → `RUBRIC.md`
2. ✅ Phase 2.5 (reuse clones): no se clonó nada — mismos repos que A5
3. ✅ Phase 4 (grade): adapté `grade_investigacion.py` con 7 checks:
   - readme_lines, mention_2026 → Definición
   - markdown_table + tool_mentions → Comparación
   - screenshots_count, agent_screenshots → Capturas
   - readme_lines → README renderizable
   - mentions_copilot + screenshot → Uso Copilot
   - has_agent_explanation → Explicación agentes
   - gh_cli_commits + merge_commits → Commit con git/gh CLI
4. ⏸️ Phase 5: skipped (dry-run)

## Resultados grupo 1 (32 students)

- avg=75.1, **17 below 80** (más del 50%)
- 1 perfect 100 (ROMERO_DERLIN)
- Cluster de 25s: BEITIA, DELBIONDO, DELGADO, JIMENEZ — todos altos en A5

## Verificación de bajos

Spot-check de BEITIA_BETHEL (95 en A5, 25 en A2):
- main branch: `docs/`, `imagenes/`, `Laboratorios/`, `README.md` — **NO tiene `investigacion/agentic_development/`**
- Tiene 6 branches incluyendo `investigacion` ← **AHÍ está su A2**

Mismo gotcha #2/#11 del skill: A2 frecuentemente vive en branch separado (`investigacion`).

## Lo que el skill agarra bien

- ✅ Detecta cuando un estudiante tiene la estructura completa (ROMERO=100, ATHANASIADIS=93, DUARTE=93, etc.)
- ✅ Diferencia entre Excelente vs Bueno en criterios numéricos (Capturas: cuenta screenshots; Definición: cuenta líneas)
- ✅ Flaggea los 25s para verificación

## Lo que el skill recibe mal (false negatives previsibles)

- ❌ A2 en branch `investigacion` separado → no detecta nada → 25 falso
- ❌ Detección de "Comparación entre herramientas" via markdown table es heurística; algunos comparan con listas en lugar de tabla

## Verdad del dry-run

A2 mostró que **los false negatives del skill son consistentes con su diseño**: el grader heurístico es un draft, no la fuente de verdad. La fase de verificación manual (que el skill exige) atrapa estos casos.

Para A2 específicamente, si quisieras grado completo deberías:
1. Para cada estudiante con score <80, hacer `git checkout investigacion` (o branch equivalente) y re-correr el grader
2. Auto-script: detect branch with `investigaciones/agentic_development/` → re-clone or checkout → re-grade

Esa mejora justificaría una "Phase 4.5: branch-aware re-grading" en el skill — pero para el grading que ya hicimos manualmente (A5) no era necesario, era opcional.

## Validación final del skill

Cuatro tipos de asignación probados:
1. ✅ **App lab** (A5) — 69/69 graded, 9 manual corrections aplicadas
2. ✅ **Test suite** (A6) — adapter funciona, false negatives previsibles
3. ✅ **No-rubric admin** (A1) — 80% accuracy, false negatives identificados
4. ✅ **PR/research** (A2) — 47% pass-rate sin verificación de branches; ~75% si se checkean branches

El skill captura el workflow correcto. Cada tipo añade un template a `lib/` (4 templates total ahora):
- grade_template.py
- grade_playwright_template.py
- grade_intro_template.py
- grade_investigacion_template.py
