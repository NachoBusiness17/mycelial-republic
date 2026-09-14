# M5 — LIBRARIAN V1 UPGRADE (2026-09-11, mickey lane 5/7)

Done. `mag/librarian.py` upgraded v0 → v1 against
`watch/LIBRARIAN_METHOD_20260911.md` (the eight disciplines). Re-run, report
regenerated at `watch/LIBRARIAN_REPORT.md`, changes verified in the artifact.

## What was upgraded

1. **PULLED/HASHED per-row state** (discipline 7): the auditor now scans
   `docs/report_v1/sources/` — a receipt at `receipts/<arxiv-id>.md` marks a
   row PULLED; a ≥16-hex content hash in the receipt marks it PULLED+HASHED.
   Root PDFs match by name token. Id-less rows (CoT/ReAct/SWE-bench) reach
   their receipts through name aliases parsed from the map's own EXTRACTION
   PROTOCOL line.
2. **Tier-3 sorts first** (disciplines 3+7): bullets under THE UNNAMED DEBT
   parse as rows (v0 only read table rows) and open the report as a dedicated
   "TIER-3 GATE ROWS" section; every later section lists tier-3 rows first.
3. **RETRIEVAL-PLAN status** (discipline 1): any row naming a source (arXiv
   id, URL, or unnamed-debt source) with no pulled receipt is stamped
   RETRIEVAL-PLAN — a retrieval plan, not a citation set.
4. **ADJACENT-FIELD SWEEP section** (discipline 5): keyword scan of ecology,
   distributed systems, formal methods, safety engineering, economics against
   map + corpus; zero-coverage fields flagged in place.

## New audit numbers (v1 run, 2026-09-10T20:4xZ)

- docs scanned: 1,936 · map rows: 80 (7 tier-3)
- PULLED+HASHED: 5 · PULLED: 2 (7 rows backed by the 6 extraction receipts)
- RETRIEVAL-PLAN: 44 (the pull backlog, tier-3 rows at the front)
- UNREGISTERED: 161 (down from ~190 — unnamed-debt rows now count as mapped)
- DUST: 12 · NO-STATUS: 7 (down from 11 — tier-3 rows now carry computed state)
- ARCHIVE: 3 entries (2 PDFs + receipts/)

## Adjacent-field gaps (the sweep's answer)

- **formal methods: ZERO map coverage** (corpus: 12 incidental hits) — the gap.
  Model checking, TLA+, theorem provers: nothing. Lamport is in the map but as
  leader-election folklore, not as the formal-methods body it comes from.
- economics: 1 map hit (thinnest covered field) despite FrugalGPT living there.
- ecology 4, safety engineering 4, distributed systems 7 — represented, thin.

## NEXT:

NEXT: Pull the tier-3 RETRIEVAL-PLAN backlog in discipline-7 order (Belady
1966, Mattson 1970, Kraska 2018, LRU-K/ARC/LeCaR, Pope 2022, then the †
rows), writing receipts with hash + one verbatim excerpt each — that moment
is when a plan upgrades to a citation set.

SPAWNABLE: receipt-pull worker — takes the RETRIEVAL-PLAN list from
watch/LIBRARIAN_REPORT.md, fetches each primary, writes
docs/report_v1/sources/receipts/<id>.md (content hash + verbatim excerpt).
Needs egress — same gate as cite_gate's fetch door (operator GO required).
