# P0 — DUST ROWS + CASCADE INTEGRATION (2026-09-11, zcode seat)

Both halves of P0 landed. Backup-first honored: pre-surgery map preserved at
`watch/inbox/mickey/BIBLIOGRAPHY_MAP.pre_dust_20260911.bak`.

## Part 1 — dust rows (docs/ref/BIBLIOGRAPHY_MAP.md)

Method: swept all 116 table rows of the map; probed the corpus (7,219 files,
scope docs/ watch/ configs/ mag/ handoff/ state/) for each row's arXiv id(s)
plus distinctive ref-cell tokens, anchored on the corpus-rarest probe (the same
anchor trick mag/cascade_research.py uses). A used_at pointer that resolves to
a real file containing the probe = consulted, row untouched. Nothing deleted.

Result: 65 rows flagged as dust-shaped, annotated in place, 0 deleted.

- **62 RELINKED** — the row's used_at was a label or stale pointer ("report
  section 2", "desk fold 09-11", "KV_OS_CHARTER Bellman organ"); the real
  consulting doc was found and appended inside the used_at cell:
  `· ⚠ DUST-RELINK 2026-09-11: consulted_by -> <doc> (+N more)`.
  Highlights: PBKV / RoleKV / KVFlow / TokenCake / τ^τ-bench / HAL /
  CacheWise -> docs/report_v1/SECTION2_KVOS_bibliography.md (+ FRONTIER_REVIEW_001.md);
  GVA, Belady/Bellman, Densing Law, MiniCPM5-2B -> watch/KV_OS_CHARTER_20260911.md;
  SHEPHERD/Kimi-K3, Nielsen info-geometry, OpenDesign Arena -> watch/inbox/DESK_FOLD_SEVEN_20260911.md
  (+ DESK_DSV41FLASH / DESK_DOGFOOD_VISUAL_DECK); Right to History ->
  docs/ref/MYCELIAL_SCIENCE_MAP.md; GLM family rows -> watch/GLM53_LINEAGE_DROP_20260901.md;
  PagedAttention / Prompt Cache / Preble -> their sha-pinned receipts under
  docs/report_v1/sources/receipts/; STRACE -> watch/INTAKE_STRACE_EDG_20260904.md;
  Narrator/Archivist -> watch/CORPUS_WAVE2_SYNTHESIS_20260901.md.
- **3 REVERTED, no pointer** — DeepSeek Harness + Agent Teams, Governance paper
  (night-audit find), Observer anatomy atlas. Their only viable probe was a
  generic word (matched 208 / 339 / 71 files), so any single "consulted_by"
  pointer would have been a false claim. They keep their original label
  pointers, honestly unmarked. (First pass had appended junk pointers; caught
  and stripped in the same turn.)
- **0 ORPHANED** — every row has at least one real consumer outside the map.

Tri-state note on the librarian's "27": that count does not reproduce under
this corpus rule — no row is consumer-less. The two weakest rows are Shen et
al. AdaptFM (2606.21238) and Emergent agent languages (2609.01491): their only
consumer is watch/LIBRARIAN_REPORT.md itself. If the librarian's own report
counts as index-not-consumer, those two are the true removal candidates. Both
are left RELINKED with that pointer stated plainly.

## Part 2 — cascade wired into the desk (mag/desk_tools.py)

- TOOLS dict: 5th entry `cascade_research` -> `cascade_research_tool()`, which
  calls mag/cascade_research.py's `run()` — the function its `main()` executes
  (main() prints + writes the JSON receipt; run() returns the verdict dict the
  gateway wants). Lazy sibling import (same pattern as kvos_block), stdlib only,
  no network, writes nothing, never holds keys.
- Passthrough args: `tier2_receipt` (tier 2 ingests a deepseek-seam receipt
  JSON) and `go` (tier 3 frontier dispatch emitted only with operator GO —
  launch law amendment 5; the gate is named, not paid).
- CLI: `python mag/desk_tools.py cascade "question" [--tier2-json F] [--go]`.
- Module docstring updated: four -> five callable organs + cascade blurb.

Test receipts (fired this turn):
- Gateway seam: `run_tool("cascade_research", question="what grounds the cache
  share invariant in kvos metering")` -> STATUS `ANSWERED-TIER-1`, stopped at
  tier 1 with 11 independent local sources (surfaces: bibliography-map + card;
  top hits: docs/ref/BIBLIOGRAPHY_MAP.md, watch/inbox/kvos_steal/BOT3_organs.md,
  watch/REGISTRY_GENERALIZATION_20260911.md). Registry now lists exactly:
  biblio.query, cascade_research, fence.strike, invariant.sheet, kvos.stats.
- CLI: `python mag/desk_tools.py cascade "cascade research stopping floor"` ->
  tier-1 verdict JSON, same STOP shape.

## Files touched
- docs/ref/BIBLIOGRAPHY_MAP.md — 62 dust-relink annotations (backup at
  watch/inbox/mickey/BIBLIOGRAPHY_MAP.pre_dust_20260911.bak)
- mag/desk_tools.py — cascade_research tool entry + CLI + docstring
- watch/inbox/mickey/P0_dust_cascade.md — this card
