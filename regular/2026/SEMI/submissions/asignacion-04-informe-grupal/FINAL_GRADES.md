# A4 — Informe Escrito Grupal — Class 1 (1GS241)

36 students. Avg **87.7**. Grades + feedback entered in Teams. User clicks Return.

## Distribution

| Score | Count |
|---|---|
| 100 | 2 (GARCIA_ELIEL, RODRIGUEZ_ANGELICA — GAITD exemplary) |
| 95 | 3 (APARICIO, FERREIRA, ROMERO — Pasarelas: 16 pp, 10 APA, 3 members) |
| 92 | 7 (Front React Template + Stitch + RAG) |
| 90 | 13 (MongoDB+Docker + Full Stack + GitHub Template + CopilotCLI + CopilotKit) |
| 88 | 4 (Definición Problema + Claude Code) |
| 85 | 5 (Análisis Requerimientos + OpenRouter — APA weak) |
| 80 | 1 (DELGADO_EINAR — individual) |
| 0 | 1 (QUINTERO_ESTIVEN — no submission, no group) |

## Groups confirmed via PDF Integrantes parsing (14 groups)

1. **MongoDB+Docker (90)** — ACOSTA, CORDOBA
2. **Análisis Requerimientos (85)** — BUSTAMANTE, NUNEZ, ORTEGA_ALLISSON
3. **Front React Template (92)** — BARRERA, HE_KELVIN, MOSQUERA — 22pp
4. **Full Stack Arquitectura (90)** — BAZAN, TENSU, VALDESPINO — 11pp, 3 APA
5. **GitHub Template Plantilla (90)** — CARLOS_JAEN, ORTEGA_DAVID, RODRIGUEZ_GABRIEL — 371-line README
6. **Stitch (92)** — GONZALEZ_GABRIEL, RUIZ_ERIC — 14pp, 6 APA
7. **RAG/Neo4j (92)** — PAN_YINI, SAMANIEGO_YOEL — 15pp, 4 APA
8. **Pasarelas Pago IA Persistencia (95)** — APARICIO, FERREIRA, ROMERO — 16pp, 10 APA, 3 members
9. **GAITD/Skills.md/IA Requisitos (100)** — GARCIA_ELIEL, RODRIGUEZ_ANGELICA — 25pp, 16 APA, 6 conclusiones
10. **Definición Problema / Formulación FS (88)** — BEITIA, DUARTE — 15pp, 5 APA, only 1 conclusión
11. **OpenRouter (85)** — TORRES, GARCIA_CESAR — 10pp, 0 APA inline
12. **Claude Code (88)** — MARTINEZ, VARCASIA — 220-line MD
13. **CopilotCLI (90)** — JIMENEZ, RIOS — 674-line MD
14. **CopilotKit (90)** — ATHANASIADIS, GARCIA_JACK, DELBIONDO — RECOVERED 2 students from "0" scores via README discovery

## Cross-reference with A3 grades (retroactive observations)

Several students were under-graded in A3 because A4 PDF Integrantes parsing exposed group memberships that weren't obvious from A3 video evidence:

- **FERREIRA** A3=75 (no evidence found) → A4=95 (Pasarelas group). His A3 score should arguably be 95 too (group inheritance via Pasarelas).
- **RUIZ_ERIC** A3=75 → A4=92 (Stitch with GONZALEZ_GABRIEL). A3 should be 85+ via group inheritance.
- **ATHANASIADIS** A3=0 → A4=90 (CopilotKit with DELBIONDO+GARCIA_JACK). A3 should be 90 via group inheritance.
- **GARCIA_JACK** A3=0 → A4=90 (same CopilotKit group). A3 should be 90.

The PDF Integrantes signal is more reliable than video transcript opening lines (which Whisper sometimes mangles). When grading A3 and A4 of the same class together, parse A4 PDFs FIRST to build the group→members map, then apply to A3.

## Skill learnings

1. **PDF Integrantes header is the highest-confidence group signal**: `pdftotext` first 60 lines → match `Integrantes:` block → extract names. Higher reliability than README/transcript (no Whisper mangling, no version drift).
2. **PDF authorship in filename is also strong**: `Diseno-Arquitectura-FullStack_Valdespino_TenSu_Bazán.pdf` directly names the 3 group members.
3. **Per-criterion structural scoring works**: Pages count, APA inline regex `\([0-9]{4}\)`, `Conclusión` mention count, `Bibliografía` section presence — these 4 numbers per PDF differentiate 85 from 92 from 100 cleanly without re-reading every PDF.
4. **Cross-assignment group inheritance**: groups from A4 PDFs reveal A3 group affiliations that were unclear at A3 time. Always run A4 group-detection BEFORE finalizing A3 scores when grading multiple assignments in same period.

## Next step (user)
Class 1 A4: Select all → Return.
Class 2 A4 (8 past due): same workflow pending.

---

# A4 — Class 2 (1GS242) — 33 students

Avg **81.8**. Grades + feedback entered in Teams.

## Distribution

| Score | Count |
|---|---|
| 95 | 6 (Stitch+CopilotKit + Backend Architecture) |
| 92 | 12 (Requerimientos FN/NF, Jaramillo+Sanchez, Opencode, medinet, Plantilla Bun, WONG inherits) |
| 90 | 2 (MENA+GUERRA Pre/Post IA) |
| 88 | 6 (TanStack + Grupo 11) |
| 85 | 1 (DELGADO_FERNANDO individual) |
| 78 | 3 (Formulación FS — weak APA/Bib/Concl) |
| 0 | 3 (BATISTA, ESPINO, VINA — no submission, no group) |

## Groups identified (12 confirmed)

| Topic | Members | Source | Score |
|---|---|---|---|
| Requerimientos FN/NF | CUBILLA+WU+WONG | IVAN_WU PDF + CUBILLA README 335 lines, 8 APA | 92 |
| Pre/Post IA Full Stack | MENA+GUERRA | MENA README 176 lines, 5 APA, 4 concl, bib | 90 |
| Jaramillo+Sanchez | JARAMILLO+SANCHEZ | JARAMILLO README 499 lines, 6 APA, 5 concl, 3 bib | 92 |
| Opencode | LINARES+GONZALEZ_SAMUEL | LINARES README 222 lines, 9 APA, 4 concl | 92 |
| medinet-project | SANTIAGO+SUAREZ+LOPEZ | 517-line README, 5 APA, 6 concl | 92 |
| Plantilla GitHub Bun | SZOBOTKA+BARRIOS | 330 lines, 10 APA, 3 concl | 92 |
| **Stitch+CopilotKit** | CACERES+HERRERA+MARIN | 379 lines, **11 APA, 9 concl** | **95** |
| TanStack | DUTARY+ABREGO+AVILA | 506 lines, 6 APA, 2 concl | 88 |
| DELGADO_FERNANDO Pre/Post IA | (individual) | 211 lines, **12 APA**, 3 concl | 85 |
| Grupo 11 | CISNEROS+GARCIA_GABRIEL+REYNA | GARCIA_GABRIEL README 466 lines, 6 APA, 2 concl | 88 |
| Formulación FS - Definición Problema | REYES+ORTEGA_HECTOR+GUDIÑO | 398 lines, **0 APA, 1 concl, 0 bib** (weak) | 78 |
| **Backend Architecture Grupo #4** | IZARRA+GONZALEZ_FABIANA+PORTELA | 607 lines, **13 APA, 7 concl** | **95** |

## Notable rescue: Backend Architecture group

IZARRA's Teams attachment said "Investigación Backend" — sounded vague. But deeper grep into `Laboratorios/Laboratorio Arquitectura Backend/README.md` revealed 607 lines of well-formatted APA prose. The README's `Integrantes:` block named GONZALEZ_FABIANA + PORTELA, who otherwise had only generic GitHub link submissions. All 3 jumped from "likely 75" to 95.

This validates the skill's pattern: **inspect Laboratorios/Tareas folders, not just investigaciones/Trabajos**. A4 informes sometimes live in lab-themed folders when the topic is technical (backend, frontend, deployment).

## Total A4 summary (both classes)

| Class | N | Avg | Status |
|---|---|---|---|
| 1GS241 (class 1) | 36 | 87.7 | Entered + feedback ✓ |
| 1GS242 (class 2) | 33 | 81.8 | Entered + feedback ✓ |
| **Total** | **69** | **84.8** | Pending user Return |

## Next step (user)
- Class 1 A4: Select all → Return
- Class 2 A4: Select all → Return
