# FINAL_GRADES — A10 Juego de Damas con IA A* (/100)

Fecha: 2026-06-20. Calificado leyendo el código (rúbrica 6 criterios; A* en microservicio Bun = mayor peso, 25 pts). Notas ingresadas en Teams, SIN devolver (Return) — pendiente revisión y 2da pasada post-cierre.

`astar`: puro = A* real (open/closed,g/h/f) en micro Bun · impuro = micro pero algoritmo no-A* (minimax/greedy) · sin_micro = A* en backend, no microservicio · ausente = sin proyecto Damas.

## 1GS241  (34 con nota · prom 76.5/100)

| Nota | Estudiante | A* | c1 | c2 | c3 | c4 | c5 | c6 | Nota breve |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| **100** | ATHANASIADIS, NICOLAS | puro | 20 | 25 | 15 | 15 | 10 | 15 | A* real (AStarNode g/h/f, open/closedSet) en microservicio Bun en compose; validacion server-side; bcrypt+JWT+Mongo ranking; Stripe test; Playwright E2E+unit; README+compose completos. |
| **100** | BARRERA, ROY | puro | 20 | 25 | 15 | 15 | 10 | 15 | ai-service Bun independiente (/move, board JSON), A* puro: open/closed,g/h/f, h admisible. Backend valida (moveValidator), Clerk+Stripe+ranking Mongo, Playwright e2e+unit, README+compose(4 svc). |
| **100** | SAMANIEGO, YOEL | puro | 20 | 25 | 15 | 15 | 10 | 15 | ai-service/astar/search.ts A* canonico (PriorityQueue, closed Set, g/h/f, h admisible, reopen). Micro Bun (Dockerfile+compose), HTTP /internal/ai/best-move. Stripe+webhook, argon2, Playwright+unit. |
| **100** | ORTEGA, DAVID | puro | 20 | 25 | 15 | 15 | 10 | 15 | Micro Bun independiente (ai :4000, /ai/best-move) A* real (open set, g/h/f, popLowestF). Backend valida. PBKDF2+Mongo, Elo, Stripe, Playwright E2E+unit, compose app+ai+mongo. |
| **99** | CARLOS JAEN | puro | 20 | 25 | 15 | 15 | 9 | 15 | services/ai micro Bun+Hono (POST /ai/move, port 3002 compose) searchBestMoveAStar: frontier por f=pathCost+heuristic, bestSeen=closed. Stripe real, Mongo ranking, Playwright(mock)+unit. |
| **99** | RUIZ, ERIC | puro | 20 | 24 | 15 | 15 | 10 | 15 | rules-service micro (port 3002, /rules/checkers/analyze) astar.ts best-first open list f=g+h, sin closed explicito. bcrypt+Clerk, Mongo ranking, Stripe idempotente, unit+e2e Playwright. |
| **99** | RODRIGUEZ, GABRIEL | puro | 20 | 25 | 15 | 15 | 9 | 15 | Micro Bun+Hono independiente (3002, compose) A* real: open/closed, g=moveCost, h=estimate, f=g+h. Engine validado backend. scrypt+Clerk, ranking Mongo, Stripe PaymentIntents+webhook, unit+Playwright E2E. |
| **98** | GONZALEZ, GABRIEL | puro | 18 | 25 | 15 | 15 | 10 | 15 | Monorepo Bun: ai-service A* puro (PQ f=g+h, closed set), api valida, compose mongo+ai+api+web, Clerk JWT+ranking Mongo, Stripe, Playwright e2e+unit. |
| **97** | HE, KELVIN | puro | 20 | 25 | 15 | 15 | 7 | 15 | ai-service Bun (compose port 4100, /move) MinHeap openSet+closedSet, f=g+h; hibrido con alternancia MAX/MIN. Clerk+Mongo ranking, Stripe webhooks. Solo unit, sin e2e. |
| **97** | MARTINEZ, ANGEL | puro | 20 | 25 | 14 | 15 | 8 | 15 | Motor 8x8 completo, capturas multiples y reyes. A* puro: grafo explicito, min-heap f=g+h, open/closed, backup max/min para seleccion. Clerk JWT+ranking Elo, Stripe webhooks. 30 unit, sin E2E. |
| **97** | BAZÁN, CÉSAR | puro | 20 | 25 | 15 | 15 | 7 | 15 | Monorepo Bun: micro ai independiente (Hono, Dockerfile) /move A* puro (min-heap open, g/h/f, padres). Motor 3 variantes validado backend, Clerk JWKS+Elo Mongo, Stripe idempotente, 111 bun tests sin E2E. |
| **96** | CORDOBA, EMILY | puro | 20 | 25 | 14 | 15 | 7 | 15 | apps/ai/src/ai.ts A* real (MinHeap open, closed Set, g/h/f) micro Bun/Hono :3002 POST /move en compose. Stripe test+webhook, Clerk JWT, ranking Mongo. Solo unit, sin Playwright. |
| **96** | MOSQUERA, EINER | puro | 20 | 24 | 15 | 15 | 7 | 15 | A* genuino en microservicio aislado (3004, board->move): open/closed, g=cost+1, f=g+Chebyshev admisible, reconstruccion. Engine validado server-side. bcrypt+JWT+Elo, Stripe webhook. Solo 4 unit, sin E2E. |
| **95** | ACOSTA, REY | puro | 20 | 23 | 12 | 15 | 10 | 15 | Micro Bun astar-service separado, A* PURO (min-heap open, closed Set, g/h/f); engine valida en backend (27 tests), chains+coronacion. Clerk+ranking Mongo. Stripe test+webhook. Playwright E2E+unit. Docker+README completos. |
| **95** | ROMERO, DERLIN | puro | 18 | 25 | 15 | 15 | 7 | 15 | checkrbot: ai-service A* puro avanzado (MinHeap, tabla transposicion, h admisible), compose con healthchecks, Clerk+Stripe+ranking Mongo, unit tests (sin Playwright). |
| **95** | NUNEZ, IVAN | puro | 20 | 25 | 13 | 15 | 7 | 15 | A* purisimo: heap open, closed cost-map, g/h/f, goal test, micro Bun/Hono compose con healthcheck. Variante completa, Clerk, Stripe+webhook, ranking. Solo falta Playwright. |
| **93** | DELBIONDO, ANGEL | puro | 18 | 23 | 15 | 15 | 7 | 15 | Damas 8x8 valida backend. A* puro en micro Bun: heap propio f=g+h, open/closed. bcrypt+JWT, ranking, Stripe test. Solo unit, sin E2E. Docker completo. |
| **92** | PAN, YINI | puro | 20 | 25 | 11 | 15 | 10 | 11 | A* real (g/h/f, open/closed, sort por f, traceback) en micro Bun 'ai' en compose, POST /move JSON; ranking Mongo aggregation; Stripe full; e2e+unit. Auth 'toy' (JWT no verificado), sin README. |
| **90** | GARCIA, ELIEL | impuro | 18 | 21 | 15 | 15 | 7 | 14 | micro Bun 'ai' (/choose-move, Zod) best-first con frontier/visited/priority pero g/h/f no limpios (priority=depth*10-score). Clerk+Stripe checkout+webhook+Mongo, backend valida. Unit tests, sin E2E. |
| **86** | DELGADO, EINAR | puro | 18 | 23 | 13 | 15 | 2 | 15 | Micro Bun/Elysia independiente con A* real (open/closed, g/h/f, hash tablero) en compose. Engine completo valida, Clerk JWT, Stripe checkout+webhook, ranking Mongo. Sin tests. |
| **85** | RODRÍGUEZ, ANGÉLICA | puro | 17 | 24 | 13 | 13 | 5 | 13 | A* de libro: openSet/closedSet,g/h/f,h admisible, /best-move en rules-service Bun separado. Clerk+Stripe+ranking Mongo. Solo 1 test engine, sin E2E. README+compose(3 svc). |
| **81** | TENSU, ERIEL | puro | 13 | 24 | 11 | 15 | 7 | 11 | Micro ai (3001, board->move): MinHeap, open/closed, g/h/f, iterative-deepening A* real. Engine 10 variantes pero validado solo cliente. Clerk x-user-id spoofable+leaderboard Mongo. Stripe webhook. unit sin E2E. Dockerfile COPY roto. |
| **75** | ORTEGA, ALLISSON | impuro | 20 | 7 | 11 | 15 | 7 | 15 | Servicio Bun ai separado PERO astar.ts es minimax+alpha-beta etiquetado 'astar' (sin open/closed/g/f); el AI_DECISION.md lo admite. Engine valida. Clerk+ranking Mongo. Stripe test. Sin suite unit. Docs/Docker solidos. |
| **73** | VARCASIA, ANLLELINA | impuro | 20 | 7 | 13 | 15 | 5 | 13 | Micro IA independiente (FastAPI Python, no Bun) board JSON->move pero es Minimax+alfa-beta NO A* (README lo titula asi). Motor draughts completo validado server-side. Stripe test+webhook. Clerk JWT+ranking. Postgres no Mongo. Solo unit print, sin E2E. |
| **66** | GARCIA, JACK | sin_micro | 18 | 13 | 7 | 10 | 7 | 11 | A* real (open/closed,g/h/f) en ai.service.ts pero DENTRO del backend, no micro; compose solo api+web; SQLite no Mongo; auth falsa (clerkId localStorage sin JWT); Stripe test; unit sin E2E. |
| **66** | BEITIA, BETHEL | impuro | 12 | 14 | 8 | 15 | 9 | 8 | Micro Bun real (/best-move) pero NO en compose (solo mongo). findBestMoveAStar usa g/h/f pero f=2h, ordena DESC y toma max f, sin closed set ni goal test: best-first mal etiquetado A*. Motor client-side. |
| **63** | GARCIA, CESAR | sin_micro | 17 | 13 | 8 | 15 | 2 | 8 | Decision real es minimax alfa-beta en backend (no micro); 'astarOrder' solo ordena. Auth Clerk sin hash, sin endpoint ranking, sin tests, sin README. Stripe completo. (Teams: 'not turned in' pero hay codigo). |
| **63** | JIMENEZ, ALEX | sin_micro | 13 | 10 | 12 | 15 | 2 | 11 | Best-first tipo A* (open/visited/h/f) pero en FRONTEND (AIPlayer.ts), sin micro Bun ni HTTP. Stripe completo, Clerk JWT+ranking Mongo. Motor client-side sin validar backend. Sin tests. |
| **26** | DUARTE, ANA | ausente | 5 | 7 | 4 | 4 | 2 | 4 | NO hay proyecto Damas en el repo. Solo laboratorio1=PollClass e investigaciones. Sin motor, sin microservicio A*, sin pago. Minima por ausencia del entregable. |
| **26** | APARICIO, ANA | ausente | 5 | 7 | 4 | 4 | 2 | 4 | parcial-2 es 'SafeTech' (e-commerce). NO hay damas, motor checkers, IA ni microservicio A*. Proyecto equivocado. |
| **26** | FERREIRA, BRUNO | ausente | 5 | 7 | 4 | 4 | 2 | 4 | parcial-2 NO es Damas: es 'SafeTech' e-commerce. Sin motor damas, sin microservicio A*. Proyecto equivocado. |
| **26** | VALDESPINO, CHRISTIAN | ausente | 5 | 7 | 4 | 4 | 2 | 4 | No hay proyecto de Damas en ninguna carpeta (solo Pokemon asig-09, lab5, investigaciones). Entregable ausente. |
| **0** | BUSTAMANTE, DAVID | ausente | 0 | 0 | 0 | 0 | 0 | 0 | Sin proyecto Damas en todo el repo: solo readme personal + PollClass en Laboratorio5. Cero coincidencias damas/checkers/astar. |
| **0** | RIOS, GERALD | ausente | 0 | 0 | 0 | 0 | 0 | 0 | No entregó (Not turned in) y sin repo de Damas accesible. 0 por política. |

## 1GS242  (32 con nota · prom 79.7/100)

| Nota | Estudiante | A* | c1 | c2 | c3 | c4 | c5 | c6 | Nota breve |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| **100** | CACERES, JORGE | puro | 20 | 25 | 15 | 15 | 10 | 15 | A* real (AStarNode g/h/f/parent, PriorityQueue por f, visited) en micro ai-service Bun en compose; bcrypt+JWT; Stripe checkout+webhook; Elo ranking Mongo; Playwright+unit; README+docs. |
| **100** | BATISTA, AARON | puro | 20 | 25 | 15 | 15 | 10 | 15 | Micro Bun+Hono independiente (/move JSON) A* real: open-heap por f, closed visited, g/h/f. Backend valida. Clerk JWT+Mongo Elo, Stripe webhook idempotente, Playwright E2E+unit, compose 4 svc. |
| **98** | SZOBOTKA, RAMSES | puro | 18 | 25 | 15 | 15 | 10 | 15 | services/ia A* puro (PQ, open/closed, f=g+h) en TODAS las dificultades, compose mongo+backend+ia+front, Clerk JWT+ranking+Stripe, Playwright e2e+unit, README. |
| **97** | ESPINO, SIMON | puro | 20 | 25 | 15 | 15 | 7 | 15 | ai-service stateless Bun (compose port 7070, /move) astar.ts frontier f=g+h con backup minimax (hibrido pero open/closed/f presentes). Clerk+Mongo ranking, Stripe. 22 unit, sin Playwright. |
| **97** | GONZALEZ, FABIANA | puro | 20 | 25 | 15 | 15 | 7 | 15 | Damas en rama 'proyectos'. Motor 8x8 captura obligatoria. A* puro en micro Bun (MinHeap, f=g+h, open/closed), proxy desde server. Clerk JWT+Elo Mongo, Stripe test 6 skins. 17 unit, sin E2E. |
| **96** | HERRERA, ISAI | puro | 20 | 25 | 15 | 15 | 10 | 11 | A* real (g/h/f/parent, openSet/closedSet, sort f) en micro Bun ai-service en compose, POST /ai/move; bcrypt+JWT; Stripe webhook; Elo ranking. App no en compose, sin README (hay PRD). |
| **96** | WONG, ADRIAN | puro | 20 | 25 | 14 | 15 | 7 | 15 | ai-service/engine/astar.ts A* puro (MinHeap open, visited closed, g/h/f, h admisible) micro Bun (Dockerfile, compose, POST /move); minimax coexiste pero A* seleccionable y testeado. Clerk+ranking, Stripe Checkout. bun unit, sin Playwright. |
| **95** | WU, IVAN | puro | 18 | 25 | 15 | 15 | 7 | 15 | 'damasChinas' pero motor real es damas 8x8 estandar. A* puro en micro Bun+Hono (3002): MinHeap, f=g+h, open/closed, heuristica multi-factor. Clerk+ranking, Stripe. Solo unit. compose solo PostgreSQL. |
| **95** | GUERRA, LUISA | puro | 20 | 23 | 14 | 15 | 8 | 15 | nexus-draughts (rama proyectos): micro Bun/Hono /ai/move A* real (open frontier,g/h/f,sort f; sin closed explicito). Backend valida, Stripe webhook+Mongo, Clerk JWT, Playwright E2E(15), compose 4 svc. |
| **94** | IZARRA, JORGE | puro | 19 | 23 | 15 | 15 | 7 | 15 | ai-service Bun (/internal/ai/move) astar.ts: open list,g/f,h=WIN-eval,f-sort (engine seleccionable, default minimax). Backend autoritativo (409), Clerk JWKS+Stripe webhook+Mongo. bun test amplio, sin E2E. compose 4 svc. |
| **94** | GARCIA, GABRIEL | impuro | 20 | 19 | 15 | 15 | 10 | 15 | A* real (MinHeap open, g/h/f) en ai-service micro Bun (POST /ai/move) pero minimax/alfa-beta es el motor real en medium/hard/expert; A* puro solo en easy. Stripe+webhook, Clerk, Playwright+unit. |
| **93** | REYNA, URIEL | impuro | 20 | 18 | 15 | 15 | 10 | 15 | Micro Bun(Hono) IA separado en compose, HTTP board->move. astar.ts best-first pero g=0/sin closed/sin f=g+h; greedy. minimax.ts sin usar. Clerk JWT+Mongo, Stripe full, Playwright+unit. |
| **92** | PORTELA, MICHAEL | puro | 20 | 23 | 13 | 11 | 10 | 15 | A* puro real (g+h open list, closed set, goal victoria) en micro Bun/Hono, explicitamente no-minimax. Variante completa, Clerk verifyToken, ranking, unit+Playwright. Stripe real pero compose por defecto STRIPE_MOCK. |
| **91** | SUAREZ, JEAN | puro | 19 | 24 | 15 | 11 | 7 | 15 | Micro Bun+Hono independiente (4000, Dockerfile+compose) A* real: openSet/closedSet, g/h/f, expansion por menor f, /ai/move. Engine completo validado backend. bcrypt+JWT+Mongo+Elo, Stripe Checkout, 25 unit sin E2E. |
| **90** | ORTEGA, HECTOR | impuro | 20 | 15 | 15 | 15 | 10 | 15 | Motor Damas completo y validado. Micro Bun con g/h/f y open/closed pero semantica minimax (turnos alternados, max-heap, fallback greedy). bcrypt+JWT, Stripe test, Playwright E2E+unit, docker 7 svc. |
| **89** | REYES, AMIR | puro | 18 | 23 | 15 | 15 | 7 | 11 | ai-service Bun separado usado real: A* open/closed/g/h/f, lowest-f. Caveat h no admisible. Validacion en vivo client-side. bcrypt+JWT+ranking Mongo. Stripe Checkout+webhook. Sin E2E. compose bug AI_SERVICE_URL. |
| **89** | MENA, ELIAB | puro | 18 | 25 | 10 | 12 | 10 | 14 | ai-engine/astar.ts A* real (MinHeap open, gScore closed, g/h/f) micro Bun :3002 POST /ai/move; rules/ valida. Stripe sin webhook + bypass /skin/purchase; Clerk confia clerkId sin verificar. Playwright+42 unit. |
| **89** | ABREGO, YIREIKIS | puro | 20 | 25 | 11 | 12 | 8 | 13 | Motor completo (captura obligatoria, cadena maxima, reyes). A* puro: priority queue, closed set, g+h, heuristica ponderada. Clerk+leaderboard Mongo, Stripe checkout+webhook. Solo unit. Falta README raiz. |
| **88** | LOPEZ, ROBERTO | impuro | 20 | 13 | 15 | 15 | 10 | 15 | ai-service Bun micro real (port 3001, POST /move) pero search.ts es negamax/minimax: declara AStarNode g/f y dice 'A* puro' sin openSet/closedSet reales. bcrypt+JWT+Mongo, Stripe test, e2e+unit. |
| **83** | DUTARY, CHRISTIAN | puro | 17 | 25 | 13 | 15 | 2 | 11 | Checkers: ai-service A* puro (min-heap f=g+h, visited, beam), backend valida, compose mongo+ai+backend+front, Clerk+Stripe(webhook sig)+ranking Mongo, docs PRD pero SIN tests. |
| **83** | AVILA, JOSE | impuro | 18 | 15 | 13 | 15 | 7 | 15 | Micro Bun separado con estructuras A* (PQ+closed) pero el motor decisivo es alpha-beta minimax (TT/killer). Backend valida, Clerk+svix, Stripe completo, compose con stripe-cli, tests IA. |
| **76** | SANTIAGO, CESAR | impuro | 18 | 7 | 15 | 13 | 10 | 13 | micro Bun real (/move, board JSON) pero algoritmo es greedy 1-ply+random, NO A* pese al README. Clerk+Stripe(Gold)+ranking Mongo, 2 variantes, Playwright E2E, README+compose(4 svc). |
| **76** | LINARES, ISABELLA | puro | 15 | 22 | 11 | 15 | 2 | 11 | checkers-proy2: ia-service A* real (open/closed,g/h/f) usado por defecto; minimax solo opcional inactivo. Clerk+Stripe checkout, ranking debil, Mongo, sin README ni tests. |
| **74** | GONZALEZ, SAMUEL | impuro | 18 | 7 | 11 | 15 | 8 | 15 | Proyecto real en parcial3 (no Parcial2). IA es minimax/alpha-beta (minimax.ts); aStarHeuristic solo es termino de eval, sin busqueda A*. Backend valida, Clerk, Stripe+webhook, Playwright e2e. |
| **74** | DELGADO, FERNANDO | impuro | 18 | 13 | 11 | 11 | 7 | 14 | Micro Bun/Hono independiente /ai/move pero 'A*' es greedy 1-ply (sin open/closed ni frontera). Motor 8x8 validado backend. Clerk+ranking Mongo sin JWT. Stripe Checkout sin webhook. 8 unit, sin E2E. |
| **71** | JARAMILLO, OMAR | impuro | 18 | 7 | 11 | 14 | 7 | 14 | Micro IA independiente (Python/FastAPI en compose, /ai/move) pero usa MINIMAX+alfa-beta, no A* (README lo admite). Motor valida backend. Clerk sin verificar JWT. Stripe completo. Solo Playwright E2E. README+compose excelentes. |
| **68** | VINA, DIEGO | puro | 20 | 25 | 8 | 4 | 7 | 4 | ai-engine Bun.serve independiente (/move) astar.ts A* puro (openSet/closedSet Map, g/h/f, sort f). Pero SIN Stripe, SIN docker-compose, auth solo X-User-Id sin JWT, solo unit. |
| **64** | CUBILLA, GABRIEL | ausente | 17 | 7 | 15 | 15 | 2 | 8 | IA es minimax+alfa-beta+TT+killer; 'A* apertura' es beam search. Monolito sin docker-compose ni microservicio. DB Postgres/Drizzle (no Mongo). bcrypt+JWT+Stripe. Sin tests. |
| **51** | GUDINO, JULIO | impuro | 10 | 9 | 11 | 8 | 5 | 8 | ai-service Bun con esqueleto A* PERO CODIGO MUERTO: App.jsx usa minimax local, nunca llama :3006. Engine en frontend, game-over con bug. bcrypt+JWT+Elo pero sin contenedor Mongo. Stripe sin fulfillment. README inexacto. |
| **26** | BARRIOS, JUSTIN | ausente | 5 | 7 | 4 | 4 | 2 | 4 | NO hay proyecto Damas. Solo Laboratorio5=PollClass e investigaciones. Sin motor de damas, sin A*, sin pago. Minima por ausencia. |
| **20** | SANCHEZ, GUSTAVO | ausente | 2 | 4 | 4 | 4 | 2 | 4 | Sin proyecto Damas; la entrega es de otro tema (pokemon_battle_rooms, pollclass). No hay damas/checkers ni A*. |
| **0** | BARRIA, JAIR | ausente | 0 | 0 | 0 | 0 | 0 | 0 | No entregó (Not turned in) y sin repo de Damas accesible. 0 por política. |

## ⚠️ Sin calificar (4) — repo inaccesible / sin link

Pendientes para revisión manual + 2da pasada post-cierre (Dom 21):

- **QUINTERO, ESTIVEN** (241): link `Xhennos/...` 404, dueño sin repos.
- **TORRES, ALYSON** (241): sin link GitHub; repo de curso sin Damas.
- **CISNEROS, AXEL** (242): link `axelcisnero/...` 404; sus otros repos no son Damas.
- **MARIN, ERIC** (242): sin link GitHub; repo de curso sin Damas.
