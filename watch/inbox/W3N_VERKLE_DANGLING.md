# W3N — VERKLE DANGLING MARKER-BACKFILL (2026-09-30)

The W3 registry finding, repaired WITHOUT touching the chain: chain_guard's 300
unflagged dangling rows are now classified in an append-only side ledger the
guard can read. The real classification says the evidence is NOT lost — every
unflagged row's knot content exists on disk, hash-verified.

## Files (this lane's ownership; nothing committed)

- `tools/verkle_dangling_repair.py` — NEW. classify / check CLI. No write path
  to chain, tip, repair-state marker, or knots anywhere in the file.
- `tests/test_verkle_dangling.py` — NEW, 8 tests.
- `memory/verkle/repair_20260930.jsonl` — the side ledger (373 lines, LF-only).

## REAL classification (run 2026-09-30, live estate)

```
dangling_total 371 = recoverable_by_hash 300 + truly_lost 0 + already_flagged_in_chain 71
chain_mutation_required: false    classified_rows_intact: true
check: dangling_unclassified_effective 0 -> healthy_with_side_ledger
```

- All 300 unflagged rows hash-verify against
  `memory/biography_backup/biography_backup_20260921/knots/` — the canonical
  leaf recomputes to the row's `leaf_hash` (content proof, never a name match:
  `mag/verkle_knot._leaf_hash`, reused, not reimplemented).
- 0 truly-lost rows -> 0 evidence_lost markers written. The marker path exists
  and is tested (fixtures), but the data says nothing is lost.
- pointer_witness 370/371 (by-session_v2 pointers corroborate).

## Why a row's `evidence_lost` lives in the ledger, not the row

`leaf_hash` covers the whole row JSON — setting the flag in-chain changes the
hash and breaks every proof above it (Q-001: chain rewrite = operator gate).
Ledger lines are keyed `(session_id, leaf_hash)`, stable across compaction and
live appends; `check` merges them with chain_guard's exact regression law:
alarm = dangling row with NO honest record anywhere.

## The refusal that proved the guard rails

First real run REFUSED (exit 3): chain+tip sha moved mid-run — a live fold
appending while we walked (B2-387 motion law). Fixed by design, not a guard
branch: postcondition now refuses only if a CLASSIFIED row is altered/vanished
(flag-strip / pre-repair-restore shape); live tail motion is reported, not
feared. `tests/test_verkle_dangling.py::test_postcondition_allows_live_append_refuses_strip`
pins both sides.

## chain_guard raw view — deliberately unchanged

`python -m mag.chain_guard check` still reports state=regression,
dangling_unflagged=300 (rows 8442, tip_matches_chain=true). No side door: the
guard was not edited (outside this lane's ownership). Wiring `merge_check`
into `mag/chain_guard.py` is a ~10-line follow-up for its owner: read
`memory/verkle/repair_*.jsonl`, treat any classification for
`(session_id, leaf_hash)` as the honest record.

## OPERATOR GATES (Q-001 — not taken by this lane)

1. Restore the 300 verified knots from the 20260921 backup into
   `memory/biography/knots/` (disk-only, under `verkle_lock`) — after which
   they stop being dangling entirely.
2. In-chain flag backfill (the POWER_RESTORE_20260825 shape) — chain rewrite,
   needs the operator.

## Real test lines

- `pytest tests/test_verkle_dangling.py -q` -> 8 passed.
- Adjacent slice (artifact+audit+compaction+lock+dangling) -> 25 passed.
- `tools/violation_ratchet.py check --changed`: zero claims naming this lane's
  files (the FAIL rows are sibling lanes' debt: physical_compute_acquire,
  skills_pack, corpus_selfsteal, census_drift_patrol).

## Run

```
.venv\Scripts\python.exe tools\verkle_dangling_repair.py classify
.venv\Scripts\python.exe tools\verkle_dangling_repair.py check
```
