# Asignación 10 — Proyecto individual: Juego de Damas con IA A*

- **Due**: Jun 12, 2026 11:59 PM
- **Closes / late until**: Jun 13, 2026 11:59 PM
- **Points**: 100
- **Modalidad**: Individual

## Instructions

Desarrolla una aplicación web de un juego de Damas (checkers) donde el jugador compite contra la computadora. La IA del oponente debe decidir sus movimientos usando el algoritmo A* — obligatorio y sin variaciones — implementado en un microservicio independiente en Bun. Usa la misma tecnología del proyecto 9.

### Variante del juego

Puedes implementar CUALQUIERA de las 5 variantes clásicas de damas (elige UNA y documéntala en el README):

1. Damas inglesas/americanas (8×8)
2. Damas internacionales (10×10)
3. Damas brasileñas (8×8)
4. Damas españolas (8×8)
5. Damas turcas (8×8, movimiento ortogonal)

### Stack obligatorio (igual al proyecto 9)

- TanStack Start
- Bun
- Hono
- MongoDB
- Docker / Docker Compose

### Requisitos principales

- Juego de damas funcional en la variante elegida: tablero, movimientos legales, capturas (incluyendo capturas múltiples), coronación (dama/reina) y condición de fin de partida.
- El backend valida los movimientos; el frontend solo envía decisiones y muestra el estado actualizado.
- **IA con A* (OBLIGATORIO)**: el oponente computadora elige su movimiento usando el algoritmo A*. Nada extra, no variaciones: NO minimax, NO alpha-beta, NO Monte Carlo. Solo A*, aunque no sea el algoritmo más eficiente para este problema.
- **Microservicio en Bun para la IA**: la lógica de A* debe vivir en un microservicio separado (servicio propio en docker-compose), que expone un endpoint HTTP que recibe el estado del tablero (JSON) y retorna el movimiento elegido. Este requisito pesa fuerte en la calificación.
- **Login**: registro e inicio de sesión con contraseñas cifradas, para identificar al jugador.
- **Ranking**: tabla de posiciones persistida en MongoDB (victorias/derrotas o puntaje tipo ELO simple), visible en la aplicación.
- **Pago en línea**: integración con una pasarela de pago en modo de prueba (ej. Stripe test mode) para comprar fichas o tableros (skins/cosméticos).
- **Tests**: como mínimo pruebas unitarias (motor de reglas y/o A*); de preferencia pruebas end-to-end con Playwright.

### Entregables

- Enlace al repositorio de GitHub con el código completo.
- `README.md` con: variante de damas elegida, instrucciones para correrlo, arquitectura (app + microservicio IA), cómo se invoca el microservicio A*, y limitaciones conocidas.
- `docker-compose.yml` funcional que levante app, microservicio IA y MongoDB.
- Aplicación funcional con login, partida vs IA, ranking y compra con pasarela en modo prueba.
- Tests ejecutables documentados en el README.
- Demo corta en clase.

### Demo esperada

- Levantar el proyecto con docker-compose.
- Registrarse / iniciar sesión.
- Jugar varios movimientos contra la IA, mostrando la llamada al microservicio (request con el estado, response con el movimiento).
- Demostrar una captura múltiple y una coronación.
- Terminar (o avanzar claramente) una partida y mostrar el ranking actualizado.
- Comprar una ficha o tablero con la pasarela en modo prueba.
- Correr los tests.

### Rúbrica (resumen — 100 pts)

1. Motor de damas: variante, reglas y validación en backend — 20 pts
2. Microservicio IA en Bun con A* puro (estado → movimiento) — 25 pts
3. Login y ranking persistente — 15 pts
4. Pago en línea (fichas/tableros) — 15 pts
5. Tests (unitarios mínimo; Playwright preferido) — 10 pts
6. Documentación, Docker y demo — 15 pts
