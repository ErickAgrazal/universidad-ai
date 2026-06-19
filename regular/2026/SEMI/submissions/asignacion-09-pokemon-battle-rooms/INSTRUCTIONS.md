# Asignación 9 — Proyecto individual: Pokemon Battle Rooms

- **Due**: May 22, 2026 11:59 PM
- **Closes / late until**: May 23, 2026 11:59 PM
- **Points**: 100
- **Modalidad**: Individual

## Instructions

Desarrolla una aplicación web de batallas Pokemon 1P vs 1P mediante salas con código. La aplicación debe usar datos importados desde PokéAPI y persistidos en MongoDB. El sistema debe permitir crear partidas, unir dos jugadores, seleccionar equipos, resolver turnos de combate y aplicar reglas básicas de daño, tipos, estados y victoria.

### Stack obligatorio

- TanStack Start
- Bun
- Hono
- MongoDB
- Docker / Docker Compose

### Requisitos principales

- Cargar al menos 300 Pokemon desde PokéAPI.
- Persistir en MongoDB la data necesaria para jugar sin depender de PokéAPI en cada turno.
- Guardar Pokemon, movimientos, tipos, estadisticas base, sprites y relaciones de daño entre tipos.
- Cada Pokemon en batalla debe tener exactamente 4 movimientos validos obtenidos desde PokéAPI.
- Implementar salas: un jugador crea sala, el sistema genera codigo y el segundo jugador se une usando ese codigo.
- La batalla debe ser Jugador 1 vs Jugador 2, con equipos de hasta 6 Pokemon y un Pokemon activo por jugador.
- El backend debe validar jugadores, acciones, Pokemon activo, movimientos permitidos y evitar doble accion en un mismo turno.
- El frontend solo envia decisiones y muestra el estado actualizado; no debe calcular daño.
- El backend debe resolver turnos, daño, STAB, efectividad por tipo, factor aleatorio, golpe critico y estados.
- Las vulnerabilidades, resistencias e inmunidades por tipo deben salir de PokéAPI, no de una tabla hardcodeada.
- Si un movimiento aplica estado, el estado dura 3 turnos. Si el Pokemon cambia o se retira, el estado se elimina.
- La interfaz debe incluir crear sala, unirse a sala, lobby, batalla, sprites consistentes, barras de vida, movimientos, cambio de Pokemon, log y victoria/derrota.
- Incluir animaciones basicas para ataques, daño recibido, cambios de Pokemon, barras de vida o debilitamiento.

### Entregables

- Enlace al repositorio de GitHub con el codigo completo.
- `README.md` con descripcion, instrucciones para correrlo, reglas implementadas, fuente de datos y limitaciones conocidas.
- `docker-compose.yml` funcional.
- Script o proceso documentado de importacion desde PokéAPI.
- Aplicacion funcional con sala 1P vs 1P, turnos, daño, estados, sprites y victoria.
- Demo corta en clase.

### Demo esperada

- Levantar el proyecto.
- Crear una sala y copiar el codigo.
- Un segundo jugador se une desde otro navegador o sesion.
- Iniciar la partida.
- Mostrar Pokemon con sprites consistentes y exactamente 4 movimientos.
- Ejecutar varios turnos.
- Demostrar daño por tipo.
- Demostrar un estado temporal de 3 turnos.
- Cambiar un Pokemon y evidenciar que el estado se elimina.
- Mostrar victoria, derrota o avance claro hacia el final de partida.

## Reference materials

- PDF adjunto: `Proyecto_Pokemon_Battle_Rooms_UTP_FISC_sin_cuadro_proyecto_indiv.pdf`
