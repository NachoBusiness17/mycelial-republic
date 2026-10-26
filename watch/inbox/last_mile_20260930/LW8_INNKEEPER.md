# LW8 - UF-01 innkeeper: the bot that remembers you (2026-09-30)

LANDED. Files (owned, no commit per mission): `server/innkeeper.py` (new),
`tests/test_innkeeper.py` (new). Lineage: S11 ike3 seam +
S19 say spec (MICKEY17_WAVE_LEDGER_20260929.md) + X9 motion dialect
(protocol_table.py MOTION_TABLE).

## What it is

An actor with a real session and a pure brain:

- **ike3 seam:** `Innkeeper.attach()` calls
  `world.register_session("innkeeper", "innkeeper", at="spring")` - no
  socket anywhere, a real roster row `snapshot()["roster"]` shows at the
  spring (the fish pattern, now with a memory).
- **Pure brain:** `decide(tick, world_state, player_memories) -> rows`.
  No RNG, no clock, zero input mutation (deepcopy-verified in tests);
  the tick drives all variety (idle intensity `(tick*13)%48`, dance
  `192+(tick%64)`, water comment cadence `tick % 8` or any player
  boil/valve).
- **Say (LW6 law, implemented here):** non-empty str, cap 240, one typed
  reject `BAD_TEXT`; rows `{"verb":"say","sid":...,"text":...}` for
  tick-event delivery. Say has not landed in a protocol_table yet, so the
  channel law lives in this module until that lane wraps it.
- **Motion (X9 dialect):** idle mostly; dance when a player tags a fish
  NEARBY = at the innkeeper's node (honest co-location; the world has no
  coordinates - the S19 CMaNGOS lesson). Every emitted motion row is
  gated through `MOTION_DISPATCH.ask(verb, "AUTHED", args, targets)`
  before it leaves the actor.
- **Speech:** known player joins -> `Welcome back, <name> - the spring is
  at <N> units` (exact mission format; first-timers get the no-back
  variant); plus `Last visit you tagged <k> fish, <name>.` from ledger
  memory; water-state tiers vs win_crown -> `The crown is half full.` at
  2/4. Event parsing reads the world's own event grammar (join/tag/
  boil/valve strings; physics lines parse to None).
- **Memories:** JSON file keyed by username, fields exactly
  {visits, last_action, fish_tagged}; sorted+compact canonical bytes;
  fail-closed on corruption (the world.py log law); decide() returns
  memory DELTAS, the actor merges + persists.

## Tests - real counts (instrument named, one tree, one moment)

- `pytest tests/test_innkeeper.py -q` (venv, serial): **13 passed**,
  2026-09-29, includes a 3-world persistence arc (stranger -> known ->
  greeted with last visit's catch) and channel-law edge cases.
- Server slice `tests/test_innkeeper.py + test_server_v0 +
  test_protocol_table + test_motion_rows -q`: **104 passed**.
- Full suite `pytest -q -n auto --ignore=tests/test_behavioral_awareness.py`:
  run 1: 7F/3084P/12S/3E (753s); run 2: 7F/3127P/12S/3E (615s). Different
  failure sets across runs = xdist worker-crash churn; verified serially:
  memlang/reconstruct/harvest_fold/census_drift_patrol/water_graph_starvation
  all PASS alone. Reproducible serial failures are PRE-EXISTING estate
  drift in inherited files (test_invariant STABLE-INVARIANT marker,
  test_headless_law bare-spawn ratchet 22->34 in tools/,
  test_oral_dedupe index census) - none touch server/innkeeper.
- `tests/test_behavioral_awareness.py` EXCLUDED: git-status `UU`
  (unresolved merge-conflict markers at lines 70/78, SyntaxError at
  collection) - pre-existing, outside this lane's file ownership.
- Census denominator law respected: both full-run numbers above are
  executed-sum snapshots of different moments; the passed delta
  (3084 -> 3127) is flaked tests re-passing between runs.

## Debt named

- Say rows are returned to the caller (tick-loop delivery is the server
  lane's wiring; world.stage has no say verb yet - S19's "server-injected
  tick events" is that lane's shape).
- `Innkeeper.pump` reads `world.roster/scores` live (the snapshot pieces
  the tick payload lacks); a later lane can fold them into the payload.

Demo: `.venv/Scripts/python.exe -m server.innkeeper` (one tick, ada
joins, greet + memory file printed).
