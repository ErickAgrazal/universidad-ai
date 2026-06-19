# Asignación 5 — Laboratorio: PollClass (Desarrollo Agéntico Full Stack)

- **Due**: April 8, 2026 11:59 PM
- **Closes**: April 18, 2026 11:59 PM
- **Points**: 100
- **Rubric**: Asignacion5 (ver RUBRIC.md)

## Instructions

En este laboratorio práctico, desarrollarán una aplicación web full stack completa (PollClass — Sistema de Encuestas en Vivo) utilizando desarrollo agéntico con OpenCode/Copilot en un período de 2 horas.

### Requisitos

- Utilizar OpenCode/Copilot en modo agéntico para generar el proyecto completo.
- **Stack tecnológico obligatorio**: React (Vite) + Bun.js + MongoDB + Tailwind CSS.
- La aplicación debe incluir:
  - **Vista del Profesor**: crear encuestas, ver resultados en tiempo real con gráficos, cerrar/eliminar encuestas.
  - **Vista del Estudiante**: unirse a una encuesta por código, votar, ver resultados.
  - **Base de datos**: modelos para encuestas (Poll) y votos (Vote).
  - Actualización de resultados por polling (`setInterval`), **no WebSockets**.
  - Validación de voto único por estudiante por encuesta.
  - Diseño responsive (los estudiantes votarán desde el celular).
- El PRD completo del proyecto está disponible en los archivos compartidos (Class Materials) del equipo en Teams.
- Deben alimentar el PRD a OpenCode como prompt inicial y dejar que el agente construya el proyecto.
- Todo el desarrollo debe realizarse durante la sesión de clase (2 horas).
- "Desplegar", usando ngrok (Si la red de la U lo permite).

### Entrega

- Enlace al repositorio de GitHub con el código completo.
- El repositorio debe incluir un README.md con instrucciones para correr el proyecto.
- Capturas de pantalla de la aplicación funcionando (mínimo 3: landing, vista profesor, vista estudiante).
- Captura de pantalla del historial de OpenCode mostrando el proceso agéntico.

## Reference materials

- `PollClass-PRD.md` (en Class Materials de Teams)
