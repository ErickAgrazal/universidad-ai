# Verificación de EJECUCIÓN REAL (backend tests + seed) — A9 1GS241 — 2026-06-12
MongoDB compartido (mongo:7) en :27017, una DB por estudiante. NO se levantó frontend (Clerk). Motor verificado vía tests reales; persistencia vía seed real contra Mongo (conteo independiente con mongosh).

| Estudiante | Tests motor (REAL) | Seed/persistencia (REAL) | Docker |
|---|---|---|---|
| GARCIA, ELIEL | 32 pass / 0 fail (engine+importer+services+api) | OK (pokemon/moves/typeRelations) | estático: compose+healthcheck |
| ROMERO, DERLIN | 70 pass / 0 fail | OK 1349 pokemon + 521 moves + 20 type_relations | estático: 3 servicios+healthchecks |
| SAMANIEGO, YOEL | 39 pass / 0 fail | OK 300 pokemon | compose+Dockerfile (pero frontend NO es TanStack Start) |
| BUSTAMANTE, DAVID | 8 pass + 1 archivo roto (mezcla bun:test/vitest) | OK 297 pokemon | compose+Dockerfile |
| RODRIGUEZ, GABRIEL | 3 pass (motor básico: doble acción, resolución, forzar cambio) | OK (probado con target reducido) | usa Clerk/Stripe |
| ATHANASIADIS, NICOLAS | 0 tests de backend (solo placeholder trivial en frontend) | OK (importer funciona; 11/300 parcial por lentitud PokeAPI) | — |
| RODRIGUEZ, ANGELICA | 0 tests (Vitest del README NO existe; script test roto) | OK 297 pokemon | compose SOLO la DB |
| DELGADO, EINAR | 0 tests (no hay script test; motor nunca ejecutado) | OK 292 pokemon | frontend NO compila (.output vs dist) |

## Reconciliación con el análisis estático (que sobreacreditó)
- DELGADO: estático proponía 90->100. Runtime: motor SIN tests (nunca ejecutado) + docker-compose roto. NO se sostiene 100. -> mantener 90.
- RODRIGUEZ ANGELICA: estático 96->98. Runtime: README miente sobre tests Vitest (no existen) + compose solo DB. NO se sostiene subir. -> mantener 96.
- ATHANASIADIS: estático 91->96. Runtime: sin tests de backend (motor no probado). Subida no respaldada. -> mantener 91.
- RODRIGUEZ GABRIEL: estático 96->99. Runtime: solo 3 tests básicos. Evidencia delgada. -> mantener 96 (o +1 marginal).
- BUSTAMANTE: estático 98->99. Runtime: 8 tests ok pero 1 archivo de test roto. Neutro. -> mantener 98.
- SAMANIEGO: 97->97. Runtime fuerte (39 tests) pero incumple stack TanStack Start. -> mantener 97.
- GARCIA ELIEL: estático 98->100. Runtime: 32 tests (incl. motor) + seed + limitaciones. RESPALDADO. -> 100.
- ROMERO: estático 96->99. Runtime: 70 tests + 1349 pokemon. RESPALDADO (coin-flip en orden de turno lo deja en 99, no 100). -> 99.

## CAMBIOS RESPALDADOS POR EJECUCIÓN (únicos defendibles):
- GARCIA, ELIEL: 98 -> 100
- ROMERO, DERLIN: 96 -> 99
- Resto: SIN CAMBIO.
