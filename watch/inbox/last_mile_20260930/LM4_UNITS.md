# LM4 - mountain_units: DFHack-style units for the fish school (2026-09-30)

LANDED. Files (owned, no commit per lane law): `tools/mountain_units.py`
(new, 400 lines exactly - at the violation_ratchet FILE_LINE_CAP, zero
findings), `tests/test_mountain_units.py` (new), this receipt.

## What it is (mission: DFHack's units, ours)

- `units` - runs the sim N ticks (default 600 = 10s at 60Hz) on the DEFAULT
  board and dumps every fish: id, state, intensity (Q8), position as a CELL
  (20px board-anchored tile), AGE in state (frames + seconds), current
  TARGET (the row's dir pool). Summary: population by state, transitions
  count, POP_CAP headroom.
- `unit <id> --trace` - one fish's full event history: every motion row
  {tick, verb, intensity_q8, dir, fatigue, pos} plus the caught event.
- Deterministic: spawn jitter is the only RNG, riding random.Random(seed)
  (default 20260929 = game.gd:180's own seed); cross-process byte-identical
  JSON proven (sha256 47825b69c10b05e8..., two runs `cmp` clean).

## The unit model it reads (all ports cited per-line in-file)

- brain: `roblox_to_godot/systems/fish_brain.gd` decide() - the pure
  policy; ONE motion row per fish per tick
  {idle|flee|pursue|carry|dance, intensity_q8 u8, dir pool}.
- rig: `roblox_to_godot/scripts/game.gd` _step_brain/_apply_motion_row -
  steering (X9 formula accel*(q8/255)), fatigue (dt/COAST_TIME), drag
  0.985, catch (<3.5px AND fatigue>0.7 kills), move; water ticks every
  30 frames (TICK_SECONDS 0.5).
- board: `server/world.py build_mountain_graph` - the estate's own
  WaterGraph, not a reimplementation (the mountain_gods_number fidelity
  law). Unboiled, it drains all 8 units to waste by water tick 8, so
  wettest honestly reports "" (dry) - pursue only fires while water lives.
- gate: every emitted row passes `server/protocol_table.py
  MOTION_DISPATCH.ask` (the real Python table) before it applies. An
  illegal row is a LOUD typed UnitsError - an inspector reports incidents,
  it never silently swaps to the flock fallback physics.

## Model choices named (this tool's own laws, not estate ports)

- Player: player.gd follows the mouse (human input, not deterministic), so
  the tool scripts it: `hunt` (chases nearest alive fish at 220 px/s,
  exercises flee->fatigue->carry->catch; 12/12 caught by t325) or `still`
  (parked at the board corner - the no-threat snapshot fish_brain.gd:84-85
  models; dance-only school, 0 dead).
- CELL = 20px grid anchored at player.gd's BOARD rect corner.
- NOT ported: the pheromone trail - the brain path writes it but nothing
  on that path reads it (only the flock fallback's trail_steer does);
  running it here would be orphan behavior.
- FLEE_RADIUS kept at fish_brain.gd's 14, NOT flock.gd's 20 - that drift
  is V6_FISH_FLEE.md's named handoff, ported as-is with an in-file cite.

## Verify - real counts (instrument named, one tree, one moment)

- `pytest tests/test_mountain_units.py -q` (venv): **26 passed** (2026-09-29).
- Neighbor slice `test_mountain_units + test_motion_rows +
  test_protocol_table + test_innkeeper -q`: **115 passed**.
- `tools/violation_ratchet.py check --changed`: mountain_units.py ZERO
  findings (the FAIL in the same run is other lanes' uncommitted debt:
  tools/pain_replication/*, duel_harness.py growth - untouched here).
- Demos: `units --ticks 600` (hunt: 12 dead, 48 transitions, headroom 45),
  `units --player still` (12 dance, 47 transitions, headroom 33),
  `unit 7 --ticks 600 --trace` (326 rows ending
  `t325 caught (fatigue 0.7083)` - the tire law visible in the trace:
  fatigue 0.667 -> 0.688 -> caught).

## Debt named

- Trace rows are per-frame (bounded by --ticks cap 100k); a --since filter
  is a later lane if traces grow past comfort.
- The tool reads the flock/fish model as a Python PORT of the .gd sources;
  when the estate gets a Godot binary (GODOT_SLICE_20260929), a headless
  equivalence run against the real flock would true-up the port (same
  debt class as test_motion_rows.py's structural laws).
