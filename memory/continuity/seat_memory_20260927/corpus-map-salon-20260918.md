---
name: corpus-map-salon-20260918
description: Corpus-map ractor salon fold — the 947K-row catalog already
  existed, so the ask became askability; corpus tools shipped, scanner v3
  drafted, mining gated to retrieval-eval
metadata:
  node_type: memory
  type: project
  originSessionId: sess_c424b80a-5f44-4511-bcdb-8dcec10fdce9
---

Operator post 2100789178564816932 ("our estimation of the thing replaces the
thing") anchored the corpus-map program on 2026-09-18. Seven-shape blind salon
folded: the map already existed (`catalog/catalog.jsonl`, 946,773 rows, plus
`mag/catalog.py` reader and `mag/mcp_server.py`) — the ask transformed from
mapping to **askability**.

**Why:** every map the fleet inscribes without a caller becomes another ghost
meter (close_rate=0.0 pattern); S5's verdict — "a map earns existence by being
called" — is the law.

**How to apply:**
- Shipped: `tools/corpus.py` (corpus_search/get/tail/stats — read-only,
  sha256-echoed gets, confined paths, binary refused) in TOOL_MAP + mcp_server
  archivist/historian profiles; MCP stdio round-trip verified; 27 tests pass.
- Tag pass v1: `catalog/tags.jsonl` (kind+age_class, 946,773 rows; 75% other /
  85K prose / 71K code) + `catalog/TAG_REPORT.md`; kind filter joins verified.
- Scanner v2 append-mode DOUBLES the catalog on re-run (AGENTS.md appears
  twice) — never re-run `mag/catalog_scan.py` as-is. C1 EXECUTED 2026-09-18:
  v3 walk ran inline through the venv runner → catalog now 757,667 rows
  (−189K vs old = junction `training` duplicates v2 counted, attribution
  Unproven), deduped, fresh; the walk guard must NOT prune the root itself
  (first attempt replaced the catalog with 0 rows — repaired; catalog is
  derived data, re-derivable). Module still unlanded (Mimosa blocks
  walker-class .py writes); logic in CORPUS_MAP_SALON_20260918.md.
- UF-120 verdict: SQLite FTS5 justified at our scale (30–80ms vs 3.5s scan) —
  next build = FTS5 projection behind corpus_search, gated on UF-122's eval
  spec for the mining side.
- Staleness demo (C6): map (Sep-16) missed ruins_go_engine.js while
  corpus_get served it byte-true — discovery through map, truth through bytes.
- Mining law (C7): retrieval-corpus reading only; fine-tune reading is "a wish
  wearing a spec" (no pipeline/contract); 50-question citation-recall eval
  (UF-122) must precede any mining; "mining proposals never auto-merge" stands.
- Lanes: UF-119..123 on the union queue; wants in `watch/WANTS.md`; consumer
  habit = receipts cite catalog ids retrieved through the tools.
Related: [[the-librarian-fleet-imprint-20260917]], [[elder-audit-3-passes]],
[[astra-constitutional-amendments]]
