---
name: corpus-search-fts5-stack-20260926
description: 9/26 corpus search stack rebuilt — FTS5 wired into corpus_search (4.4s scan → 2.5ms index, 3-layer freshness gate, never silently stale), catalog_rebuild.py landed (fresh 489K-row map, zero dupes), MagFtsIndexDaily 09:00 scheduler heals decay
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

The corpus search stack was rebuilt end to end on 2026-09-26 by burn lanes B2-22/B2-102/B2-103/B2-104/B2-465:

- **FTS5 wired into production** (B2-102, tools/corpus.py + tools/corpus_fts_rebuild.py): index-preferred path with a 3-layer freshness gate (mtime, then catalog-bytes meta table, then mode=ro read probe — never silently stale, falls back to scan and says why). Live A/B: ruins_go 3,862ms scan → 2.45ms fts5; worst index run 2.97ms vs 4,461ms full-scan median. Read-only law test-pinned; parity_note names the 3 mid-token delta rows (hermes/falsifier/garden) that are honest engine differences.
- **catalog_rebuild.py landed** (B2-103, the never-built salon Appendix A module): fresh map 489,038 rows, zero dup ids/paths, row-count stable across two runs; brief's "root drift" disease model corrected — the three path classes are ONE walk's shape, the live defect was consumer-side anchor ambiguity (corpus_get serving the repo's byte-different AGENTS.md for the map's bare-path row). 757,667→489,038 delta fully attributed to disk truth (biography_backup rotation, ghost prune, burn-wave growth).
- **Daily scheduler** (B2-465): MagFtsIndexDaily 09:00 runs corpus_fts_rebuild.py --check --deep, heals decay automatically, alerts via watch/inbox/fts_index_alerts.jsonl; first live fire caught a real mid-wave catalog rebuild and healed the index same cycle. Three live-fire defects fixed in-lane (detached-console hang, attention.md concurrent-append race, ts Z-suffix).

**Why:** UF-120's prediction (index beats scan 30-80ms) was beaten 10x, and the week-old-map staleness (qdrop 0 hits on both engines, C6) is structurally closed — freshness gate + scheduled rebuild + B2-104's dated-rebuild policy.

**How to apply:** corpus_search answers engine=fts5 when fresh, falls back to scan naming why; never trust rows_scanned across engines (they are different instruments — B2-464 caller census confirmed the product surface clean, falsifier only on the spike script); rebuild only via corpus_fts_rebuild.py (atomic tmp+replace); map-plane freshness policy is B2-104's receipt. Related: [[flash-lane-burn-20260926]].

**B2-104 freshness policy (the last piece, 9/26 evening):** the dated-rebuild/incremental design the salon demanded is filed — including the tags.jsonl re-run decision and who fires rescan on a schedule (MagFtsIndexDaily owns the index side; catalog v4 rescan decision priced separately as B2-466). B2-464 caller census confirmed the product surface clean post-wiring (falsifier fired only on the spike script, which hardcodes engine=scan and would silently become fts5-vs-fts5 on rerun — its rebuild also deletes the production db, B2-504). Remaining briefs: B2-331 MFT/USN fast-refresh spec, B2-332 catalog refresh + retag decision against the 271,669-row live-vs-filed drift.
