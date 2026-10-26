# Z5 - FIELD_FLOW: Watershed rung 2, DF dirty-block sheet flow landed (2026-09-30)

## What was built
`mag/field_flow.py` (new) + `tests/test_field_flow.py` (new, 15 tests, all
green). No commit. Y2's top steal - Dwarf Fortress' dirty-block activation -
applied to the estate's heightfield: rung 1 (mag/hydrology.py) graded the
head on the verdict engine's pipes; rung 2 drops the pipes and lets water
sheet across the 2D integer grid dem_to_board emits.

## Mechanics
- Field: integer elevations + volumes per cell. Head law inherited from
  rung 1: head = elev*256 + depth, depth = volume*1000 // cross_section
  (Q8 head, milli-depth) - filling a cell raises its head, so backwater
  and filling pools come free.
- Flow: each tick a cell pours to every strictly-lower-head neighbor of
  its 8 (Moore, fixed offset order), flow_i = (dHead_i * conductance) >> 8,
  scaled down proportionally when wants exceed volume. Jacobi tick: all
  flows read start-of-tick volumes, commit at end - results are
  iteration-order-independent by construction. Never uphill; dHead <
  256//conductance rounds to zero (integer surface-tension floor: a
  1-unit droplet stays put, tested).
- DIRTY-BLOCK LAW: a tick processes only cells whose volume moved last
  tick (gross in OR out - conveyors stay wet) plus their neighbors.
  Quiescent water costs zero (settled board ticks at processed=0,
  tested). Wetted meter = last_processed / total_processed. Exactness: a
  cell is dropped only when it and all 8 neighbors were untouched, so its
  recomputed outflow is provably the same zero; both ends of any active
  edge stay dirty via the recipient+neighbor rule - the dirty tick lands
  the byte-identical state a full scan would, proven step-by-step by
  test_dirty_block_matches_full_scan_exactly_and_costs_less (60 ticks,
  snapshots equal, processed <= full every tick).
- Waste/outlet: dem_to_board's `waste` cell (lowest edge, the tile outlet)
  drains off-system into a `drained` counter; conservation law is
  total_volume + drained == poured (tested on both closed and outlet
  boards, every tick).
- from_board: water_graph.v1 dem board spec -> FieldFlow (elev/volume/
  waste from nodes g{y}x{x}); tested against the real synthetic 161x161
  tile through tools.dem_to_board.build_board.
- Determinism: integers only, no floats, no RNG, no clocks in the module;
  insertion-ordered dirty dict + fixed neighbor tuple = byte-identical
  runs (tested: snapshots, wetted-meter history, dirty insertion order).

## Tests (15 passed)
Puddle spreads (>= 9 wet cells, near-level surface, max-min <= 160) and
settles; settled board ticks at zero cost; droplet retention; downhill-
never-uphill; dirty == full exactness + cost; dirty-set law shape on a
hand-checkable 1x4 slope; conservation closed (every tick) and with waste
outlet; determinism; Q8 hand computation (dHead 306 -> raw 9); from_board
load + crater pour determinism; validation errors; perf sanity.

## Perf sanity (64x64 integer cone+crater, this host, 2026-09-30)
- Drip 6 units/tick x 1000 ticks: ~1.8-2.0 s, total_processed 310,772
  cells = 7.6% of the 4,096,000 a naive full scan would pay; 163,892
  volume units moved; vol == 6000 exactly (conservation).
- One 6000-unit pour, 1000 ticks: 882.9 ms, 140,420 cells = 3.4% of full;
  still creeping at tick 1000 (597 wet cells) - honest, not settled.
- Worst case, whole board flooded (193,600 units seeded), 200 ticks:
  432.2 ms, 49,508 processed (~123 cells/tick, 6% of full) - even a
  flooded board self-limits because equalized interiors sleep.

## Suite truth (byte-backed, 2026-09-30)
- Targeted: tests/test_field_flow.py 15 passed in 2.54s.
- Full `pytest -q` (40:29 on a loaded host): 3034 passed, 2 failed,
  12 skipped, 3 errors. All 5 red are FOREIGN to this lane's ownership:
  test_behavioral_awareness.py collection error + test_healthz_status.py
  x2 AttributeError (sibling lane mid-edit on server/persistence.py);
  test_headless_law ratchet (bare spawns 22->34, offenders all tools/ +
  other lanes' tests, none mine - this module spawns nothing);
  test_census_drift_patrol CLI test (hermetic tmp_path synthetic estate).
- Census delta attributed (B2-246 law): collect-only now reads 3,133
  tests / 1 error vs the AGENTS.md carrier claim 2,303 / 352 (2026-09-27
  census). This lane's share: +15 tests / +1 file (test_field_flow.py);
  the remaining ~815 are sibling-lane landings 09-27..09-30.

## Verdict
Rung 2 landed: the terrain boards are now playable sheet-flow surfaces
with quiescence that costs zero and a wetted meter that reads true. Next
rung can hand the field to water_particles.gd (X8) for client rendering.
