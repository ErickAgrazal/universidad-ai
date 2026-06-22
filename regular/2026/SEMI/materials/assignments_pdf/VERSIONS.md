# Versiones del PDF del catálogo de asignaciones

Cada línea = una emisión del PDF (`ASSIGNMENTS_vNNN_fecha.pdf`). Los PDF en esta carpeta están gitignored (binarios); este registro y `scripts/build_assignments_pdf.py` sí se versionan. Regenerar con:
`uv run --with markdown --with xhtml2pdf regular/2026/SEMI/scripts/build_assignments_pdf.py --note "..."`

- v001 — 2026-06-22 07:57 — ASSIGNMENTS_v001_2026-06-22.pdf — versión inicial del catálogo (A1–A14)
- v002 — 2026-06-22 08:09 — ASSIGNMENTS_v002_2026-06-22.pdf — portada + bookmarks navegables + índice clicable (landscape)
- v003 — 2026-06-22 08:20 — ASSIGNMENTS_v003_2026-06-22.pdf — branding institucional UTP/FISC (logos en portada + encabezado por página)
