# W7 — RIVER: erosion/sediment layer (Watershed rung 4) - 2026-09-30

Mission (WC's river-bend steal, `watch/inbox/water_engineering_20260930/WF_SYNTHESIS.md`
§ "WC companion"): build rung 4 of the Watershed ladder on the integer
substrate — silt as a second integer per node; sill-threshold erosion
(flow > sill moves 1 silt + 1 elev-unit to the lowest neighbor);
deposition below; meanders emerge as the flow-path re-solves with
shifted elevations. File ownership: `mag/river.py` (new) +
`tests/test_river.py`. Commit: NONE (uncommitted, per lane law).

## The law as built (`mag/river.py`, 354 lines)

`River(FieldFlow)` — rung 2's sheet flow inherited (Q8 heads, dirty-block
activation, waste outlets), plus:

- **Silt grid**: second integer per cell. Silt is never created or
  destroyed, only moved — erosion requires the cell to HOLD loose
  material, so the initial mantle bounds total carving (the mountain
  armors; `add_silt()` can re-mantle).
- **Sill law (strict >)**: each tick, a cell whose throughput (inflow +
  outflow, `last_flow` — the shear meter) exceeds `sill_flow` moves
  1 silt + 1 elev-unit to its strictly-lowest-head neighbor
  (NEIGHBOR_OFFSETS tie-break; never uphill/equal). Waste cells never
  erode — they are the sea; arrivals pile up (`delta_silt()` meter).
- **Deposition**: passive — at/below-sill cells never send, so arrivals
  stay and the bed rises (point bars, the delta).
- **Meander coupling**: every transfer re-dirties moved cells, so the
  next water pass re-solves heads over the shifted bed — paths wander,
  abandoned channels stay carved.
- Determinism: integers only, no RNG (`det_noise()` is a pure integer
  hash), fixed iteration orders; `river.v1` spec round-trips.

## Collision rule — the corner WC left open, and the first cut that failed

What happens when a transfer lands on a cell eroding that same tick?
Landing there is a no-op conveyor (only the channel head could incise,
and it stalls one slope-step down). First cut cascaded the unit down
lowest-neighbor chains to the first quiet bed; test evidence killed it:
every eroder's unit rode to the one sea cell, the delta towered
+11 elev/tick, drainage clogged, the backed-up pool made chains ride
UPSTREAM, and the whole load dumped onto the armored spring pit (net
+50 elev at the spring, 2026-09-30). Final rule, split by load: SILT is
bed load — always lands on the direct lowest neighbor, walks 1
cell/tick even through eroding cells (silt stays conserved exactly);
the ELEV-unit is the suspended carve — settles only on a quiet bed or
the sea, else washes out with the water (`washed_out` meter). Elev
accounting: `start - now == eroded - deposited` (test-pinned).

## Tests — `tests/test_river.py` (9 tests), real runs

- `pytest tests/test_river.py -q` → **9 passed** (1.3 s).
- Watershed family `tests/test_river.py test_field_flow.py
  test_hydrology.py test_water_graph.py -q` → **47 passed** (4.7 s).
- Laws pinned: silt conservation on a 400-tick noisy run (+ elev
  accounting identity); erosion lowers / deposition raises (3x3 split
  board, exact values, tie-break pinned); sill is strict `>`
  (flow==sill does NOT erode); channel carves 100 ticks on a confined
  slope (spring exactly 50 = its mantle, walls untouched, delta raised,
  total_eroded >= 500); determinism (two 300-tick runs → equal
  `to_spec()` dicts); spec round-trip; bridge law — with no silt the
  tick is byte-identical to a plain FieldFlow (volumes, elevations,
  dirty order).
- Ratchet: `tools/violation_ratchet.py check --changed` → PASS, no new
  debt; river.py 354 lines (under the 400 cap).
- One test-authoring bug found and fixed en route (not engine): the
  slope-board formula `110 + (10-x)*10` built 210..110, so "carved =
  110 - 160 = -50" measured a phantom baseline; the engine had carved
  exactly 50. Fixed to `110 - x*10`.
- Full-suite attempts: run 1 died at COLLECTION —
  `tests/test_behavioral_awareness.py:70` held an unresolved git merge
  marker (`<<<<<<< Updated upstream`), pre-existing tree damage outside
  this lane's ownership; sibling lane AB1 fixed that file mid-session
  (commit 19dff2287). Run 2 (with the file ignored) reached ~87%+ and
  lost its summary line to a pipe (tail-masked exit; unusable as
  evidence — bytes or nothing). Run 3 (direct file redirect, complete):
  **`7 failed, 3197 passed, 12 skipped, 7 warnings, 3 errors in
  1994.39s (0:33:14)`** with `tests/test_behavioral_awareness.py`
  ignored (run launched before AB1's fix landed). Zero failures or
  errors touch river (grep count 0; this lane's 9 sit inside the 3197).
  The 7 failures + 3 errors are sibling-owned surfaces in flight during
  the run (organ_map x2, oral_dedupe, gods_number, headless_law,
  census_drift_patrol, healthz_status x3, and
  test_hydrology::test_boolean_engine_still_passes_its_own_tests —
  that last passes on immediate re-run and matched a sibling's
  unstaged `mag/water_graph.py` edit visible mid-run and gone after:
  shared-tree contention, not engine damage; river-family re-run green
  both before and after).
- SIBLING-COMMIT FACT: this lane committed nothing, but sibling lane
  LW6's sweep commit 69cb80f5c ("water has head+surface+terrain+
  particles") picked up `mag/river.py` + `tests/test_river.py` from the
  shared working tree while this lane was still testing. The files are
  byte-identical to what this lane built; the commit was not this
  lane's action (shared-tree hazard of wide lanes, flagged for the
  operator).

## 1000-tick trace (the meander), byte-verbatim from the run

Config: 20x64 grid, slope 6/col east, `det_noise` span 5, silt mantle
12, sea = east column (elev -60), pour 40/tick at row 10, col 0,
`cross_section=100`, `sill_flow=20`. Legend: `~` wet; digit = carve
depth vs baseline; `^` bar. Meters after 1000 ticks:
`eroded=2699 deposited=1090 washed=1609 drained=6561`;
`silt total=15360 == start=15360` (conservation held the whole run).
Determinism: second identical run → `to_spec()` equal (True), frames
equal. Trace file: `%TEMP%/w7_trace.txt` (regenerable; scratch, not
boarded). Migration (median wet row vs pour row at x=16/32/48 — the
bend swings 5 rows at x=48 over the run):

```
  t= 100  [2, 2, -3]
  t= 200  [3, 3, 0]
  t= 300  [2, 0, 1]
  t= 400  [2, 0, 0]
  t= 500  [2, 0, 1]
  t= 600  [1, 0, 0]
  t= 700  [1, 0, 1]
  t= 800  [1, 1, 1]
  t= 900  [1, 1, 1]
  t=1000  [1, 1, 2]
```

Read honestly: by t=400 a channel BELT has incised (rows 8-14) out of
the t=100 sheet; threads migrate laterally through the run; the spring
armors at carve 4; a `999` reach (3 cells carved to depth 9) opens by
t=700 and holds; new `5`/`1`/`2` scars open late (t=1000) as the belt
keeps rearranging; 6561 units drain to the sea. Braided-migrating, not
a single sine-wave — that is what these rules produce at this pour.

```
=== tick 100 ===
.............................................~..................
..........................................~~..~.................
........................................~~..~~..................
.......................................~........~...............
...........~~........................~~.....~~~~................
...........~~....~..................~~~.~..~~......~............
.......~.~~.....~~...............~~~.....~~~.~.~.~~~~...........
......~.~~.....~....~...........~.~~.......~....~~....~.........
..~~~~~~.~~~~~~~...~~~.........~~~.~~~......~~..................
~~~.~~~.~~~~~.~~~~~.........~.~~.....~~~.~~.....................
~~~~~~~~~~~.~~~~.~~~~..~...~.~....~~~~~~~~.~.~..................
.~~~~~~~~~~.~~~~~..~~~~.~~~~~.~..~.~~.~~~.~.~...................
..~.~~~~~~~~~~~~~~~~~~~~.~..~.~.~~~.~.~..~~.....................
...~~~~~~~~~~~~~~~~.~.~~~~.~~~~~.~.~~...~.~~....................
......~~.~..~~~....~.....~~....~~...~~~~.~..~...................
........~~~~~~~.~.........~.~~...~~.~~..........................
..........~................~~......~~...........................
.............................~..................................
...............................~................................
................................................................

=== tick 400 ===
......................~~.~~.~~..............~~.~..~~.~~....~~~..
.....................~~~..~~........~~~.~.~~..~~.~.....~~.~~.~~.
............~.......~.~..~~~~~..~.~~~~~~~~..~~~.~........~.~.~~.
..........~.~.~...~~~..~..~~.~~~~~~~~.~~..~..~..~.....~~~.~~~~~.
..........~~~~~~.~~~.~~.~~.~~.~~~~...~~~..~~~~~~..~.~~~~..~~~...
.........~~~~~.~~~~.~~~~~~~~...~....~~~~~~~~~~.....~.~..~~.~.~~.
.......~.~~~~~~~~~.~.~~~~.~~.~~~.~~~..~~.~~~~~~..~~~~..~~....~~.
......~.~~~~~~~~.~~.~~~~~~..~~~~~~~~~.....~~~.~.~~~...~.~~..~.~.
..~~~~~~~~~~~~~~~~~~~~.~~~~~~~.~~~.~~~.~~.~.~~....~~....~.~~~.~.
~~~.~~~~~~~~~~~~~~~.~~~.~.~.~~~~.~.~.~~~.~~.~~~.~~~~~~.~~~~~~~~.
~~~~~~~~~~~~~~~~~~~~~.~~~.~~.~~~~.~~~~~~~~~~~~~~~~.~~.~.~~~~~~..
.~~~~~~~~4~~~~~~~~~~~~~~~~~~~.~~.~.~~~~~~~~.~..~~~..~~..~..~....
..~.~~~~~~~~~~~~~~~~~~~~.~..~~~~~~~.~~~~.~~...~...~.~.~..~~~.~..
...~~~~~~~~~~~~~~~~.~~~~~~.~~~~~~~~~~..~~~~~~~.~~~.~~~~~.~..~.~.
.....~.~.~..~~~....~..~~.~~...~~~~~.~~~~.~~.~.~..~~~.~~.~~~.~~~.
........~~~~~~~.~....~~.~.~.~~~..~~~~~...~~.~..~~~.....~.~.~~...
.......~..~~....~.~~~..~...~~......~~~~~~.~~..~~.~~...~.~.......
...........~~..~~~~.....~....~.....~..~.~..~~~~...~.~....~......
............~~~~.~~.~..~~..~...~~.~......~.~~.~..~.~.~.~~..~....
................~~....~~~~~..................~.~~...~.~......~~.

=== tick 700 ===
......................~..~..~~...............~.~..~~.~~....~~~~.
.....................~~...~~........~~~.~.~~..~~.~.....~~.~~.~~.
............~.......~.~..~~~~~..~.~~~~~~~~..~~~.~.......~~.~.~~.
..........~.~.....~~...~..~~..~~~~~~~.~~..~..~~.~.....~~~.~~~~..
..........~~~~~2.~~~.~~..~.~~.~~~~...~~~..~~~~~~..~~~~~~..~~~...
.........~~~~~.~~~~.~~~~~~~~..~~....~~~~~~~~~~.~...~.~.~~~.~.~~.
.......~.~~~~.~~~~~~..~~~..~.~~~.~~~~~~~~~~~~~~~.~~~~~.~~~...~~.
......~.~~~~~~~~~~~.~~~~~~..~~~~~~~~~...~.~~~.~.~~~~~.~.~~..~.~.
..~~~~~~~~~~~~~~~~~~~~.~~~..~~.~~~.~~..~~.~.~~....~~..~.~.~~~.~.
~~~.~~~~~~~~~~~~~~~.~~~~~.~.~~~~~~.~.~~~.~~.~~~~~~~~~~.~~~~~~~~.
~~~~~~~~~~~~~~~~~~~~~~~~~.~~~~~~~.~~~~~~~~.~~~~~~~.~~.~~~~~~~~..
.~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~.~~~~~~~~....~~~..~~.~~..~....
..~.~~~~~~~~~~~~~999~~~~.~..~~~~~~~.~~~~.~~...~...~.~.~..~~~.~..
...~~~~~~~~~~~.79~~~~~~~~~..~~~~~~.~~..~~~~~~~.~~~.~~~~..~~.~...
.....~.~.~..~~~..~.~..~~~~~...~~~~~.~~~~.~~.~.~...~~.~~.~~~~~~~.
........~~~~~~~.~....~~.~.~~~~~..~~~~~...~~.~~.~~~.....~.~.~~...
.......~..~~....~.~~~..~...~~......~~~~~~.~~..~~~~~~...~.~.......
...........~~..~~~~.....~....~.....~..~.~..~~~~...~.~....~......
............~~~~.~~.~..~~..~...~~.~......~.~~.~~.~.~.~.~~..~....
................~~....~~~~~..................~.~~...~.~......~~.

=== tick 1000 ===
......................~..~..~~...............~.~..~~.~.....~~~~.
.....................~~...~~........~~~.~.~~..~~.~.....~~.~~.~~.
............~.......~.~..~~~~~..~.~~~~~~~~..~~~.~.......~~.~.~~.
..........~.~.....~~...~..~~..~~~~~~~.~~..~..~~.~.....~~~.~~~~~.
..........~~~~~2.~~~.~~..~.~~.~~~~...~~...~~~~~~..~~~~~~..~~~...
.........~~~~~.~~~~.~~~~~~~~..~~....~~~~~~~~~~.~...~.~.~~~.~.~~.
.......~.~~~~.~~~~~~..~~~..~.~~~.~~.~~~~~~~~~~~~.~~~~~.~~~...~~.
......~.~~~~~~~~~~~.~~~~~~..~~~~~~~~~...~.~~~.~.~~~~~.~.~~..~.~.
..~~~~~~~~~~~~~~~~~~~~.~~~..~~.~~.~~~.~~.~~~~~~...~~..~.~.~~~.~.
~~~.~~~~~~~~~~~~~~~.~~~~~.~~~~~~~~.~.~~~~~~~~~~~~~~~~~~~~~~~~~~.
~~~~~~~~~~~~~~~~~~~~~~~~~.~~~~~~~~~~~~~~~~~~~~~~~~.~~~~~~~~~~~..
.~~~~~~~~4~~~~~~~~~~~~~~.~~~~~~~~~~~~~~~~~~.~~~~~~~~~~.~~..~~.~.
..~.~~~~~~~~~~~~~999~~~~.~~~~~~~~~5~~1~~~~~..~~.~.~~~.~..~~~.~~.
...~~~~~~~~~~~.79~~~~~~~~~~~~~~~~~~~~~.~~~~~~~.~~~.~~~~~.~~.~.~.
.....~.~.~..~~~..~.~..~~~~~~~~~..~~~~~~~~~~.~~~~~.~~~~~~.~~~~~~~.
........~~~~~~~.~....~~...~~~~~~.~~~~~.~~~~.~~.~~~.~.~.~.~~~~.~.
.......~..~~....~.~~~..~..~~~~~.~.~~~~~~~.~~~.~~~~~~.~~.~.~.~...
...........~~..~~~~.....~...~~~.~~~~~~~~~..~~~~~..~.~~...~~.....
............~~~~.~~.~..~~..~...~~.~~~.~~~~~~~~~~~~.~.~~~~~~~~.~.
................~~....~~~~~.....~..~.~.~~~...~~~~..~~.~~~.~..~~.
```

Wet path (JSON positions): 766 wet cells at t=1000;
`River.wet_path()` returns the full `[[y,x],...]` row-major list (first
20: `[[0,22],[0,25],[0,28],[0,29],[0,45],[0,47],[0,50],[0,51],[0,53],
[0,59],[0,60],[0,61],[0,62],[1,21],[1,22],[1,26],[1,27],[1,36],[1,37],
[1,38]]`).

## Files

- `mag/river.py` (new, 354 lines) — engine + `det_noise`, `render`,
  `wet_path`, `river.v1` spec, meters (`total_eroded`,
  `total_deposited`, `washed_out`, `delta_silt`, `last_flow`).
- `tests/test_river.py` (new, 197 lines) — 9 tests.
- Nothing else touched. `water_graph.py` / `hydrology.py` /
  `field_flow.py` untouched (their suites re-run green as the bridge
  proof).
