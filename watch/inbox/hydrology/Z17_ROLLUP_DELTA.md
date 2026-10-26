# Z17 — ROLLUP DELTA: the metabolism instrument (rollup.json now diffs)

Lane Z17, 2026-09-29/30. Mission: the daily rollup is a snapshot nobody diffs
(the gap sentinel found the disease 2026-09-29); build the instrument that
computes and PUBLISHES per-lane daily deltas.

## Verdict

- `tools/rollup_delta.py` (400 lines, under the 400-line ratchet bar) diffs the
  current `dashboard/static/index_data/rollup.json` against the sentinel's
  recorded snapshots and emits `dashboard/static/index_data/ROLLUP_DELTA.json`
  beside it - one `fetch()` for any dashboard page (the the_index.html pattern).
- History union, byte-truth priority: own rich rows
  (`logs/rollup_delta/history.jsonl`, bytes+files+HOT/WARM/COLD/FROZEN, one row
  per rollup run ts, deduped) > sentinel bytes-only rows
  (`logs/gap_sentinel/history.jsonl`, byte deltas byte-true, files/temps null
  and named unmetered) > `--bootstrap-from` older index_data copy (diff-only,
  named in `window.source`, never recorded).
- Bars: GROWTH >5.0 GiB/day (the 12.59 GiB/day finding class); SHRINK past a
  1.0 MiB rewrite-noise floor = deletion event; gone lane = one deletion event
  of its full size. Windows <0.25d are evidence only, never flags (B2-215
  same-window law, inherited from the sentinel). Exit 0 ok/baseline, 1 flags,
  2 cannot-verify (fail-closed).

## Record - the real first reading

Window 2026-09-23T18:30:04Z -> 2026-09-29T14:23:05Z (5.83d, via bootstrap from
`dashboard-deploy/static/index_data`), estate 125.61 GiB total, **+65.03 GiB**.

- FLAG (exit 1): `GROWTH local_sovereign_agent` +55.67 GiB = **9.55 GiB/day**,
  files +3,871,700, HOT +67,871 - the 12.59-class disease persists at ~2x the
  bar, now per-lane and named.
- Top-3 growing: 1) `local_sovereign_agent` +55.67 GiB (+9.55/day);
  2) `Mag-prewipe-backup-20260927_git` +7.39 GiB (+1.27/day, appeared);
  3) `Mag-backup_git` +0.80 GiB (+0.14/day).
- Top-3 shrinking: **NONE - zero lanes net-shrank past 1 MiB**; no gone lanes,
  5 appeared lanes. The estate is monotonically growing this window. Only
  intra-lane loss signal: `Mag-backup_git` +0.80 GiB while files -27 / hot -22
  (grows while shedding). Deletion-event sensing arms for real once a second
  rollup run lands in history.
- Byte-truth spot audit vs raw rollups: `_mimosa` +143,264,991,
  `Mag-backup_git` +856,898,099, `azerothcore-wow`/`mycelial-republic` flat 0 -
  all match the emitted JSON. azerothcore flat means the WoW lanes idle.

## Tests and gates

- `tests/test_rollup_delta.py`: 9 passed - pure delta core (per-day by dim,
  appeared/gone, unmetered-never-fabricated), fixture rollups -> GROWTH/SHRINK
  flags + ROLLUP_DELTA.json shape + top lists, strict-growth/at-floor-shrink
  boundaries, evidence-only law, sentinel bytes-only source, bootstrap
  diff-only, dry-run, exit 2 fail-closed, CLI.
- Adjacent: `tests/test_gap_sentinel.py` 10 passed. Violation ratchet: this
  file lands at 400 lines (bar >400); the two NEW ratchet hits
  (`mag/percolator.py`, `mag/physical_compute_acquire.py`) are other lanes'
  active files, not Z17's.

## Response (operator)

- Run cadence: `python tools/rollup_delta.py` after any index run (or ride the
  gap sentinel daily task); history self-accumulates, bootstrap no longer
  needed. The next index run gets a real rich window (files/hot velocity live).
- Dashboard: `fetch("./index_data/ROLLUP_DELTA.json")` - `lanes[]` carries
  pre-rounded `*_gib` strings, `flags[]`, `top_growing`/`top_shrinking`,
  `window.source`, `unmetered_note`.
- The 9.55 GiB/day repo growth is the compaction lane's meter now: treat any
  sustained reading over the 5 GiB/day bar as the Q-001 verkle-compaction
  queue's evidence, and any future SHRINK flag as a deletion event to witness.
