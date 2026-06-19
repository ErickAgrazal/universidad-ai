# Re-evaluación A9 — estudiantes 90-99 sin razón registrada (1GS241)

Fecha: 2026-06-12. Método: revisión profunda repo por repo contra la rúbrica (datos 20, salas 20, motor 25, UI 15, docs 20), con evidencia de archivos. NO se aplicó penalización por tardanza (ninguno de estos 8 la tenía).

| Estudiante | Actual | Re-eval | Razón remanente |
|---|---:|---:|---|
| DELGADO, EINAR | 90 | 100 | Ninguna. Motor prioridad->velocidad, estados 3 turnos, ~292 pokemon documentado, README con limitaciones, docker-compose completo. El 90 lo subestimaba. |
| GARCIA, ELIEL | 98 | 100 | Ninguna. Tests pasan, prioridad+velocidad, limitaciones, todo al máximo. |
| ROMERO, DERLIN | 96 | 99 | Orden de turno por coin-flip fijo (no velocidad), documentado. 70 tests pass. |
| ATHANASIADIS, NICOLAS | 91 | 96 | Orden de turno coin-flip+alternancia (no velocidad) y sin tests de backend. |
| SAMANIEGO, YOEL | 97 | 97 | TanStack Start scaffolded pero frontend real es vanilla app.js -> incumple stack obligatorio. Funcionalidad completa. El 97 era justo. |
| BUSTAMANTE, DAVID | 98 | 99 | Falta sección "Limitaciones conocidas" en README. |
| RODRIGUEZ, GABRIEL | 96 | 99 | Falta sección explícita de limitaciones en README. |
| RODRIGUEZ, ANGELICA | 96 | 98 | docker-compose solo contieneriza la DB (no la app) + README anuncia tests Vitest inexistentes. |

Moderaciones: ATHANASIADIS y ROMERO bajados de la propuesta "100" del agente por el coin-flip (rúbrica lista "prioridad" como omisión menor del motor). SAMANIEGO se mantiene por incumplir TanStack Start.

PENDIENTE: (1) ¿aplicar en Teams? (2) Equidad: los demás <100 con razón ya registrada (84-93) no se re-evaluaron a fondo.

## Verificación con Playwright (2026-06-12) — RESULTADO: no concluyente

- Intenté levantar DELGADO con docker compose up --build: el frontend NO compila su imagen (Dockerfile copia /app/.output pero el build de TanStack Start/Vite genera dist/; el start es `vite preview`). docker-compose NO es funcional -> contradice el "docs 20/20" del análisis estático y descarta el 90->100.
- Los 8 proyectos dependen de Clerk (auth) + Stripe. Sin las llaves privadas de cada estudiante, el login de Clerk bloquea el flujo; NO se puede crear sala ni jugar batalla por Playwright. Verificación E2E inviable para los 8.
- CONCLUSIÓN: el análisis estático sobreacreditó (caso DELGADO probado). No hay base verificable para subir notas. Recomendación: NO cambiar notas; mantener las originales y, a lo sumo, agregar feedback solo donde haya evidencia sólida.
