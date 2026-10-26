---
name: fts5-meters-schema-20260927
description: FTS5 caller census CLEAN + daily rebuild scheduler heals decay live
  + institutional cluster dated meters (NOBS = silence ≠ absence) + events key
  schema registry 30 keys both gates
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Three FTS5 + instrumentation lanes landed 9/27 as a cluster:

**B2-464 caller census**: every caller of corpus_search swept after the FTS5 wiring; product surface CLEAN, falsifier confirmed on exactly one caller (the spike script's `rows_scanned >= rows_indexed` predicate only true under pre-wiring lines-read semantics). Production index detected STALE honestly by its own gate (catalog rewritten by concurrent rescan mid-census).

**B2-465 rebuild scheduler**: `MagFtsIndexDaily` 09:00 daily (after census patrol 08:30) runs `tools/corpus_fts_rebuild.py --check --deep`, heals decay through the one sanctioned writer (tmp + os.replace), alerts only when non-fresh survives rebuild. First live run caught the real decay in the act (catalog rebuilt by concurrent rescan, index stale by mtime, healed on first fire, `verkle` search 62.4ms → 2.01ms).

**B2-469 dated meters**: institutional cluster (G20 blackout, national alert, MOEX XRP halt, G20 circuit breaker) now gets one dated row per class per day in `watch/inbox/DATED_METERS.jsonl` from the census patrol cron. States: RECEIPT (boundary-true candidate pointers) or NOBS. NOBS = silence is not evidence of absence (LAW-13 mechanical). Any future window scoring citing "no receipt" for these items without naming DATED_METERS voids itself.

**B2-342 schema registry** (already indexed): 30 writer keys pinned, both gates armed, two self-caught defects fixed pre-landing.
