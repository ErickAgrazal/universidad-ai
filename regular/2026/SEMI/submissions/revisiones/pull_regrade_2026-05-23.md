# Pull y recalificacion por cambios remotos - 2026-05-23

Scope: todos los repos clonados localmente en `submissions/`.

## Pull/fetch

- Repos Git detectados: 114.
- Se hizo `fetch --all --prune` con prompts deshabilitados y timeout por repo.
- Se aplico fast-forward seguro cuando el repo local no tenia divergencia ni cambios locales relevantes.
- Repos no mezclados automaticamente:
  - `asignacion-05-pollclass/grupo-1/DELGADO_EINAR`: divergente; ya fue revisado manualmente contra `origin/main` durante el reclamo.
  - `asignacion-05-pollclass/grupo-2/DELGADO_EINAR`: divergente; duplicado del mismo caso.
  - `asignacion-05-pollclass/grupo-1/RODRIGUEZ_ANGELICA`: fast-forward fallo por estado local, pero el remoto se inspecciono para fechas.
  - `asignacion-05-pollclass/grupo-2/ADRIAN_WONG`: repo local sucio, sin cambios remotos nuevos.

## Cambios aplicados en Teams

No se presiono `Return`; solo se actualizaron puntaje y feedback.

| Grupo | Estudiante | Asignacion | Antes | Despues | Motivo |
|---|---|---:|---:|---:|---|
| 1GS241 | VARCASIA, ANLLELINA | A9 | 85 | 91 | El pull trajo una implementacion A9 mas completa dentro de la ventana tardia aceptada: Hono/Bun, MongoDB, importacion PokeAPI, salas, batalla, Docker, Clerk/Stripe y UI amplia. Deduccion restante por empaquetado inconsistente de TanStack Start y falta de suite de pruebas clara. |
| 1GS242 | DUTARY, CHRISTIAN | A9 | 88 | 93 | El pull trajo una entrega A9 mas solida con Hono/Bun, MongoDB, seed/import, battle service, rooms, Docker, Clerk/Stripe/shiny y documentacion tecnica amplia. Deduccion restante por empaquetado/TanStack Start inconsistente y falta de suite A9 clara. |

## Revisados sin cambio relevante

| Grupo | Estudiante | Asignacion | Nota | Resultado |
|---|---|---:|---:|---|
| 1GS241 | RODRIGUEZ, ANGELICA | A7 | sin cambio | El unico commit A7 antes de la hora era estructura/directorio; el codigo real de A7 llego despues del cierre. A9 ya estaba en 96. |
| 1GS241 | RODRIGUEZ, GABRIEL | A9 | 96 | Cambios validos, pero la nota ya reflejaba una entrega fuerte. |
| 1GS241 | ROMERO, DERLIN | A7/A9 | sin cambio / 96 | A9 ya estaba fuerte; A7 no requirio ajuste por esta pasada. |
| 1GS241 | SAMANIEGO, YOEL | A7/A9 | sin cambio / 97 | A9 ya estaba fuerte; A7 no requirio ajuste por esta pasada. |
| 1GS242 | DELGADO, FERNANDO | A9 | 84 | Se confirmo proyecto sustancial, pero siguen faltando TanStack Start claro y evidencia de pruebas/validacion mas fuerte. |
| 1GS242 | SANTIAGO, CESAR | A9 | 80 | La entrega existe y es funcional en alcance compacto, pero mantiene deducciones por no tener Docker, no TanStack Start claro y persistencia Pokemon incompleta. |
| 1GS242 | WU, IVAN | A9 | 75 | Se confirmo una app sustancial, pero la deduccion principal se mantiene porque no usa Hono/Mongo/Bun/TanStack y la logica de tipos esta hardcodeada. |

## Notas de fecha

- A9: entrega regular viernes 2026-05-22 11:59 PM; entrega tardia aceptada hasta sabado 2026-05-23 11:59 PM.
- A5/A6: los cambios nuevos detectados para esos laboratorios llegaron fuera de su ventana, salvo el caso de Einar que ya habia sido tratado como reclamo individual.
