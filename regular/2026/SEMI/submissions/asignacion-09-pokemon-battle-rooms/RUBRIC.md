# Rubrica — Asignación 9: Pokemon Battle Rooms

Total: 100 puntos.

## 1. Datos Pokemon y persistencia (20 pts)

- **Excelente (20)**: Carga 300+ Pokemon desde PokéAPI, persiste correctamente Pokemon, movimientos, tipos, estadisticas, sprites y relaciones de daño en MongoDB. La app usa la base de datos durante la batalla y el proceso de importacion esta documentado.
- **Bueno (15)**: Carga y persiste la mayoria de los datos requeridos, con detalles menores incompletos o documentacion parcial.
- **Normal (10)**: Carga datos reales, pero faltan entidades importantes, hay dependencia excesiva de PokéAPI durante la partida o la persistencia es incompleta.
- **Deficiente (5)**: Data hardcodeada, menos de 300 Pokemon, sin persistencia funcional o sin proceso claro de importacion.

## 2. Salas, jugadores y flujo de batalla (20 pts)

- **Excelente (20)**: Permite crear sala, generar codigo unico, unir segundo jugador, lobby de espera, inicio de partida, equipos de hasta 6 Pokemon y condicion de victoria.
- **Bueno (15)**: El flujo principal funciona, con fallas menores en lobby, sincronizacion o manejo de casos borde.
- **Normal (10)**: Hay salas o batalla parcial, pero el flujo 1P vs 1P es incompleto o inestable.
- **Deficiente (5)**: No hay sistema de salas funcional o la batalla no permite dos jugadores.

## 3. Motor de turnos, dano, tipos y estados (25 pts)

- **Excelente (25)**: El backend valida acciones, evita doble accion, resuelve turnos, calcula daño con poder, stats, STAB, efectividad, aleatorio, critico y estados temporales de 3 turnos. La efectividad por tipo viene de PokéAPI.
- **Bueno (19)**: El motor funciona con la mayoria de reglas, pero omite algun detalle menor como prioridad, critico, precision o estados parciales.
- **Normal (13)**: El combate funciona parcialmente, pero el frontend calcula parte de la logica o faltan reglas importantes de daño/tipos/estados.
- **Deficiente (7)**: El combate es mayormente hardcodeado, no valida acciones o no implementa daño y turnos de forma verificable.

## 4. Interfaz, sprites y animaciones (15 pts)

- **Excelente (15)**: UI clara para crear/unirse/lobby/batalla, sprites consistentes, barras de vida, 4 botones de movimientos, cambio de Pokemon, log y animaciones basicas.
- **Bueno (11)**: UI funcional con algunos detalles visuales o animaciones incompletas.
- **Normal (8)**: UI permite jugar parcialmente, pero faltan pantallas, estado visual claro o consistencia de sprites.
- **Deficiente (4)**: UI incompleta o dificil de usar para demostrar la batalla.

## 5. Documentacion, Docker y demo (20 pts)

- **Excelente (20)**: README completo, instrucciones reproducibles, `docker-compose.yml` funcional, limitaciones conocidas, proceso de importacion documentado y demo en clase fluida.
- **Bueno (15)**: Documentacion y Docker funcionales con detalles menores faltantes.
- **Normal (10)**: Documentacion incompleta, Docker parcial o demo con fallas importantes.
- **Deficiente (5)**: Sin README util, sin Docker funcional o sin demo verificable.

## Notas de aplicación

- La entrega es individual.
- La entrega principal es el repositorio de GitHub.
- Las entregas tardias se aceptan hasta el sabado 23 de mayo de 2026 a las 11:59 PM.
- El PDF adjunto contiene formulas sugeridas y requisitos detallados. Las formulas no tienen que copiar Pokemon al 100%, pero la batalla debe ser consistente, verificable y razonable.
