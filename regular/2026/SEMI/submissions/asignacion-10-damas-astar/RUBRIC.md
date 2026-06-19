# Rúbrica — Asignación 10: Juego de Damas con IA A*

Total: 100 puntos.

## 1. Motor de damas: variante, reglas y validación backend (20 pts)

- **Excelente (20)**: Implementa completamente UNA de las 5 variantes: tablero correcto, movimientos legales, capturas simples y múltiples, coronación y fin de partida. El backend valida todo movimiento; el frontend no decide reglas. La variante está documentada.
- **Bueno (15)**: Las reglas principales funcionan con fallas menores en casos borde (capturas múltiples encadenadas, coronación a mitad de cadena, etc.).
- **Normal (10)**: Se puede jugar parcialmente, pero faltan reglas importantes de la variante o parte de la lógica vive en el frontend.
- **Deficiente (5)**: El juego no respeta reglas de damas reconocibles o los movimientos no se validan.

## 2. Microservicio IA en Bun con A* puro (25 pts)

- **Excelente (25)**: Microservicio Bun independiente (servicio propio en docker-compose) con endpoint HTTP que recibe el estado del tablero en JSON y retorna el movimiento. La búsqueda usa A* puro y verificable (estructura abierta/cerrada, g(n), h(n) explícitos). Sin minimax/alpha-beta/MCTS ni sustitutos.
- **Bueno (19)**: A* en microservicio funcional, con implementación poco clara en partes (heurística confusa o mal documentada) pero verificable como A*.
- **Normal (13)**: La IA responde desde un servicio separado pero el algoritmo no es claramente A*, o A* está implementado dentro del backend principal en vez del microservicio.
- **Deficiente (7)**: No hay microservicio, o la IA usa otro algoritmo (minimax, aleatorio, hardcodeado) aunque lo llame A*.

## 3. Login y ranking persistente (15 pts)

- **Excelente (15)**: Registro/login con contraseñas cifradas, sesión o JWT, ranking persistido en MongoDB y visible en la app, actualizado al terminar partidas.
- **Bueno (11)**: Login y ranking funcionan con detalles menores (ranking no se actualiza en vivo, validaciones débiles).
- **Normal (8)**: Login básico sin cifrado o ranking incompleto/no persistente.
- **Deficiente (4)**: Sin login funcional o sin ranking.

## 4. Pago en línea: fichas o tableros (15 pts)

- **Excelente (15)**: Pasarela integrada en modo prueba (ej. Stripe test) con flujo completo de compra de fichas o tableros, reflejado en la cuenta del usuario y persistido.
- **Bueno (11)**: El flujo de pago funciona con detalles menores (no se refleja en vivo, webhooks incompletos).
- **Normal (8)**: Checkout parcial o simulado sin pasarela real en modo prueba.
- **Deficiente (4)**: Sin integración de pago verificable.

## 5. Tests (10 pts)

- **Excelente (10)**: Pruebas E2E con Playwright (flujo de juego/login) además de unitarias del motor de reglas y/o A*, ejecutables y documentadas.
- **Bueno (7)**: Pruebas unitarias sólidas del motor o del A*, sin E2E.
- **Normal (5)**: Pocas pruebas triviales pero ejecutables.
- **Deficiente (2)**: Sin tests ejecutables.

## 6. Documentación, Docker y demo (15 pts)

- **Excelente (15)**: README completo (variante, arquitectura, microservicio, cómo correr, limitaciones), docker-compose levanta app + microservicio IA + MongoDB, demo fluida.
- **Bueno (11)**: Documentación y Docker funcionales con faltas menores.
- **Normal (8)**: Documentación incompleta, Docker parcial o demo con fallas importantes.
- **Deficiente (4)**: Sin README útil, sin Docker funcional o sin demo verificable.

## Notas de aplicación

- La entrega es individual.
- La entrega principal es el repositorio de GitHub.
- Entregas tardías se aceptan hasta el sábado 13 de junio de 2026 a las 11:59 PM.
- NO adjuntar rúbrica Teams sin puntos (bloquea la columna de notas — lección de A9). Los puntos por criterio van en las instrucciones; la nota se ingresa sobre 100.
- El criterio 2 (A* en microservicio Bun) es el de mayor peso por instrucción explícita del profesor: "Esto es importante en la calificación."
