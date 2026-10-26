# LW5 — PERSIST: S18 V1, REPLAY-ON-BOOT (2026-09-30)

Lane: last-mile wave (S18's v1 verdict: hash-chained JSONL + snapshots IS
ENOUGH; restore on boot by replaying the log, periodic kind:snapshot rows
in the same chain). No commit (operator's fence).

File ownership held: `server/persistence.py` (NEW) + `tests/test_server_persist.py`
(NEW) + minimal wiring in `server/world.py`. Note: world.py is a shared
surface this wave (LW6 chat landed say/whisper in the same file); the LW5
diff is confined to `__init__` (save_path/save_interval params + the
load-if-exists call) and one interval-save call at the end of `tick()`,
re-merged over LW6's landed text (mid-flight re-read, 2026-09-30).

## What landed

| File | Change |
|---|---|
| `server/persistence.py` | NEW. `save(world, path)` / `load(path)` / `restore_world(world, path)` + `verify_tail`. One `kind:"snapshot"` row joins the LIVE chain (full state rides the row: volumes, steam, pipe open/primed via `to_spec`, tick, winner, scores, roster), then the save doc is written atomically (tmp + os.replace): last N chain rows (default 512) + current volumes/tick anchors. Load = replay: verify the tail chain, anchor on its first snapshot row, re-derive every later action/tick/whisper row through the world's own `_apply`/`_whisper`/`graph.tick`/`_append_row`, assert each re-derived row equals the logged one byte for byte, check the doc's own anchors, then replay any JSONL rows that outlived the doc (crash between chain flush and doc write) and transplant graph + roster + scores + winner into the booting world |
| `server/world.py` | `MountainWorld.__init__(log_path, save_path=None, save_interval=0)`: load-if-exists on boot (one lazy-import call to `restore_world`); `tick()` fires `save()` when `save_interval > 0 and tick_no % save_interval == 0` (END of tick, after pending drained, so a snapshot never catches half-applied actions) |
| `tests/test_server_persist.py` | NEW. 7 tests (below) |

## Tests (real counts, `pytest -q`, repo venv, 2026-09-30)

- `tests/test_server_persist.py`: **7 passed** (0 failed, 0 skipped)
  1. save->load via the boot path (log + doc) rebuilds a byte-identical
     world: full fingerprint (to_spec, winner, scores, roster, every
     chained row) equal; interval saves lace snapshots so load REPLAYS the
     rows between the first tail snapshot and the end (adoption alone
     would prove nothing about determinism)
  2. `load(path)` without a log file adopts the doc tail; replay report
     proves rows re-derived (`rows_replayed > 0`)
  3. chain continues across THREE lives (a saves, b boots + acts + saves,
     c boots from b's save): seq/prev never reset, world stays alive
  4. crash window: JSONL rows past the doc replay too; boot recovers to
     the log's true tip, then keeps appending
  5. `save_interval` wiring: doc written exactly on tick multiples
     (3, not 2), boot restores at tick 6
  6. `kind:snapshot` rides the SAME chain: JSONL + doc last row byte-equal,
     prev-linked, spec/roster/scores inside
  7. fail-closed x4: edited row (hash), volumes lie (replay disagrees with
     doc anchor), snapshots stripped (no anchor), unknown row kind on a
     re-hashed VALID chain
- Adjacent suites, same instrument same moment: test_server_persist +
  test_server_v0 + test_chat + test_innkeeper + test_anticheat +
  test_water_graph: **73 passed**, 0 failed (LW6's say/whisper surface and
  the v0 server laws unharmed).

## Design laws carried

- Replay IS verification, not trust: every re-derived row is byte-compared
  to the logged one; first divergence refuses boot (same fail-closed class
  as the corrupt-chain law). The determinism law makes this free.
- The sid law: action rows carry `user` only, so replay resolves sids from
  the roster the anchor snapshot adopted; users registered after the anchor
  get synthetic `replay:<user>` sids mid-replay (touches no row bytes), and
  the next snapshot's roster is ADOPTED verbatim (sids are session
  bookkeeping physics cannot re-derive).
- Honest v1 losses: staged-but-unapplied actions and undelivered whisper
  direct lines die with the process (no rows, no durable state). Tail
  trimming/compaction is v1 debt (S18 item 3).

## Findings outside my fence (for the owning lanes)

- PRE-EXISTING ENGINE QUIRK (mag/water_graph.py, observed, deterministic,
  not touched): `tick()` can drive a source volume NEGATIVE (spring -1 in
  the test run). Cause: deferred gated-junction inflow is measured by
  `_available` from `src.volume` BEFORE earlier-inserted plain pipes
  (`p_bypass`) drain the same source, then the hold/commit branch
  subtracts it again. Live and replay produce the identical -1, so
  persistence is unaffected, but the physics can manufacture water debt.
- `water_graph.from_spec` drops `pipe.primed` (never reads it back); a
  primed siphon would replay unprimed and diverge next tick. Worked around
  in `_apply_graph_spec` (restores dynamic fields directly onto a freshly
  built Mountain board); the from_spec gap itself belongs to the water lane.
- `server/world.py` module docstring still says "v0 does not restore world
  state" (now stale); left untouched per file ownership.
- `server/server.py` CLI has no `--save`/`--save-interval` flags yet (world
  accepts the params; wiring the flag is the server lane's one-liner).
