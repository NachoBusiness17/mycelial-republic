# RECEIPT BODY FTS (fix-queue Q4) — 2026-09-27

**Gap closed:** the catalog FTS (`catalog/catalog_fts.sqlite`, 489,548 rows) indexes only `path` + `title`. Receipt BODIES were unsearchable: `corpus_search("PROBE-C")` returns 0 rows even though three intake documents discuss it in prose. The whole intake zone (10,331 cataloged files; 2,084 md/txt bodies, 22.3 MB) was findable by name only.

**Build:** `tools/receipt_body_fts.py` (stdlib-only self-steal of the B2-22/corpus_fts shape):
- `build` walks `watch/inbox` .md/.txt, indexes `relpath, title, body` via external-content FTS5 into `catalog/receipt_fts.sqlite` (atomic tmp-replace, meta table, 2,084 files → 36.7 MB, seconds).
- `check` is the freshness gate: walk stats vs meta; exit 0 fresh / exit 2 stale (same contract as the catalog FTS law).
- `query "terms"` prints path + mtime + «marked» snippet; `search_receipt_bodies()` importable for seats.

**Proofs (2026-09-27):**
1. `query "PROBE-C detector miss"` → 3 snippet hits (the _d falsifier receipt, the _c genesis, AND this session's APPEND_GATE_WIRED receipt written minutes earlier) vs `corpus_search("PROBE-C")` → 0. The unlock, measured both ways.
2. Staleness round-trip: append one line to a receipt body → `check` exit 2 naming the newer mtime → rebuild → exit 0 fresh. Detection heals by rebuild, per the B2-465 pattern.
3. Scope note: `query "weeping angel"` → 0 hits in intake because that term lives in the roblox lane, not in receipts; the index's charge is intake prose, not the whole estate.

**Adoption:** rebuild routinely via `check` → `build` (seconds, $0). No scheduled task registered yet (scheduling is an operator call per the census/FTS precedents). The staleness probe line appended to APPEND_GATE_WIRED_20260927.md during proof stays as evidence of the round-trip.

**Ledger:** the burn-ledger row citing this receipt banked THROUGH the wired append gate (`tools/ledger_lock.py append`), which required this file to exist first: the two Q-queue fixes enforced each other.
