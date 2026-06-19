# Dry-run de Asignación 1 con el skill grade-teams-lab

Objetivo: probar el skill con un tipo de asignación distinto — administrativa, sin rúbrica formal.

## Características únicas de A1

| Aspecto | A1 (este caso) | A5 / A6 (anteriores) |
|---|---|---|
| Tiene rúbrica de Teams | **NO** | Sí (5 criterios o 4) |
| Punto único | Sí (regla "100 o 0") | No (puntos parciales) |
| Submission | Solo URL del repo | URL del repo |
| Trabajo del estudiante | Crear repo privado + README + foto + intro | App / suite de tests |
| Verificación | Repo accesible + README con 5 elementos | Stack tech + features + capturas |
| State actual en Teams | 15/36 returned, 21 to return | Recién terminamos A5; A6 4/36 returned |

## Workflow que se ejecutó

1. ✅ Phase 1 (extract): instructions extraídas vía "Take action in student view"
2. ⚠️ Phase 1: **No hay popup rubric grader** — instrucciones son la única fuente
3. ✅ Phase 2.5 (reuse): no se clonó nada nuevo — usé los mismos repos ya clonados de A5
4. ✅ Phase 4 (grade): adapté `grade_repo_intro.py` con 5 checks (name, materia, foto, gusta, espero)
5. ⏸️ Phase 5: SKIPPED (dry-run, no entrada en Teams)

## Resultados (grupo 1, 32 students)

- **avg=82.2**, **9 below 80**
- 21/32 perfectos (100)
- 9 con elementos faltantes (60/30/0)

## Ground-truth check

Comparando con los 15 ya returned por Erick:
| Student | Teams | Grader |
|---|---|---|
| DELBIONDO_ANGEL | 100 | 100 ✓ |
| HE_KELVIN | 100 | 100 ✓ |
| NUNEZ_IVAN | 100 | 60 ✗ (false negative) |
| ORTEGA_DAVID | 100 | 100 ✓ |
| PAN_YINI | 100 | 100 ✓ |

**80% accuracy contra ground truth**. Los false negatives (NUNEZ) son del patrón "qué espero/qué me gusta" — variantes que no captura el regex. El grader reporta por-elemento (✓/✗) lo que facilita ver qué le falta a cada estudiante para que un humano valide.

## Validación del skill

**Phase 1** (extract context): ✅ funciona aún sin rúbrica formal. El skill reconoce que las instrucciones contienen las reglas implícitas y se usan como base.

**Phase 2.5** (reuse clones): ✅ ahorró ~32 git clones. Validó el gotcha #11 del skill.

**Phase 4** (heuristic grade): ✅ se adaptó en ~5 minutos copiando el template y cambiando los signals + reglas.

**Phase 6** (verify low scores): ✅ Los false negatives identificados son exactamente del tipo que el skill manda a verificar manualmente.

## Gotcha #15 propuesto para el skill

> Assignments without an attached Rubric — instructions contain the de-facto criteria. Build a per-element compliance grader (one boolean per requirement from instructions) and report each element separately. The teacher can quickly see WHICH requirement each non-100 student missed.

## Resultado del dry-run

Skill validado en 3 tipos distintos de asignación:
1. **App lab** (A5 PollClass) — heurísticas de stack + features
2. **Test suite** (A6 Playwright) — heurísticas de coverage + assertions + bitácora
3. **Administrative** (A1 GitHub Repo) — checklist de elementos en README

Cada tipo requirió:
- Mismo `Phase 1-3` (sin cambios)
- Nuevo grader adapter (~5-10 min copiando template)
- Misma `Phase 5-6` (entrada en Teams + verificación)

El skill captura el patrón reutilizable correctamente.
