# LM6 — DIGFLOOD: breach the wall, watch the water - 2026-09-30

Mission (operator, DFHack style): the classic DF moment — breach a wall,
watch water flood real terrain. We owned the pieces: `mag/river.py` (W7
erosion/silt FieldFlow) and the St Helens board
(`logs/terrain/N46W122_board.json`, 64x64 water_graph.v1, 4096 nodes,
elev 0..255, waste outlet `g30x0`, board hash `25e926f0...` — the board
`roblox_to_godot/scripts/terrain_loader.gd` renders). This lane built
the OPERATOR'S HAND over that board. File ownership:
`tools/mountain_digflood.py` + `tests/test_mountain_digflood.py` + this
receipt. Commit: NONE (uncommitted, per lane law).

## The tool (`tools/mountain_digflood.py`, 400 lines exactly)

Four verbs, no magic — the dig is the hand, the water obeys the physics:

- **`load --board <json>`** — board → `River` (the `from_board` grammar:
  `g{y}x{x}` nodes, `kind:"waste"` = the sea), mantles every land cell
  with `--mantle` silt (erosion needs loose material), keeps the
  pristine elev grid as the report baseline. State is `digflood.v1`
  (header + baseline + dig/pour logs + `river.v1`), default
  `logs/digflood/state.json`.
- **`dig <x> <y> [-k K]`** — the breach: one cell's elevation -K. The
  SPOIL LAW: those K units land on the cell as loose silt (the channel
  floor is debris; the flood carries it). Logged with before/after.
  Refuses waste cells ("the sea has no floor to a shovel"), bounds, K<1.
  Spoil added after a pour moves the conservation baseline with it.
- **`pour <x> <y> -n N -t T`** — N units/tick for T ticks at the source,
  running the river engine: water finds the dug channel, incises it,
  silts the slow reaches, grows the delta at the waste.
- **`flood-report`** — after T ticks: wetted cells, the max flow path,
  erosion/deposition/washed totals, delta growth, ASCII trace
  (`~` wet, digits carve depth, `^` bars), and the conservation audit
  (silt exact; elev = dug + carved - landed).

**Max flow path = thalweg on the carved bed**: strictly-lowest-head walk
(elev + standing volume) from the last pour source; at a WET pit it
crosses the lowest rim — fill-and-spill, the engine's own pooling law —
so the route reads through lakes; a dry pit ends it. First-found-wins
ties (the engine's determinism device).

Determinism: integers only, no RNG, no clocks; state JSON in fixed
construction order. Proven twice below (synthetic byte-identical states
in-test; the full St Helens CLI sequence re-run → `cmp` byte-identical).
CLI coords are `<x> <y>` = column, row (map reading; node `g{y}x{x}`).

## Physics learned en route (test evidence, not taste)

- **A flat reservoir floor self-captures.** Point-pour on a flat floor:
  the spring incises below its outlet (rung 4's documented stall), the
  notch AGGRADES (below-sill arrivals land), and the breach never drains
  — drained=0 after 370 ticks. The synthetic dam board therefore slopes
  its reservoir to the dam (80/70/62/55) so water arrives moving. This
  is real morphology (deep-at-the-dam is how reservoirs actually sit),
  not a workaround.
- **cross_section 1000 vs 100**: at 1000 the DEM's wide flat valleys
  fill at depth 1:1 (slow, surface tension dominates); at 100 each
  volume unit buys 10x head and the flood pushes across flats — the
  St Helens run uses `--cross-section 100` (the W7 trace's choice too).

## Tests — `tests/test_mountain_digflood.py` (11 tests)

`pytest tests/test_mountain_digflood.py -q` → **11 passed**. Laws pinned:
load (g-grammar, waste parsing, mantle 40 cells x 6, pristine baseline);
dig (elev -K, silt +K spoil, logged, baseline frozen; bounds/waste/K<1
→ exit 2); **the DF moment** — WITHOUT the dig the dam holds
(drained=0, water never past col 3, no thalweg through the wall), WITH
the 26-deep dig it drains, incises past the hand-carve
(elev 46 → lower), wets the downstream slope, and the delta grows;
flood-report carries every dossier field with engine-matching numbers;
meters survive the state round-trip (`drained`, `total_eroded`,
`tick_count` — `river.v1` `from_spec` restarts meters by design, the
CLI restores them); session byte-determinism (two full sessions →
identical state bytes); thalweg on a dry slope, at a dry pit, and
through the dug notch to the sea; missing board/state → exit 2.

- Watershed family (dem_to_board, field_flow, river, hydrology,
  water_graph, digflood): **84 passed**.
- Ratchet: `tools/violation_ratchet.py check --changed` — this lane's
  files scan clean (`violations_in` = 0); `tools/mountain_digflood.py`
  at exactly 400 lines (the cap). The `--changed` FAIL the gate prints
  is 4 NEW violations in `tools/pain_replication/*` (untracked sibling
  lane in flight, `?? tools/pain_replication/`): cwd-relative-path x2,
  file-too-long, except-pass — not this lane's files, not this lane's
  debt to register.
- Full suite: THREE attempts, none landed. Attempt 1 died at
  COLLECTION — `tools/mountain_reveal.py:384` holds a live SyntaxError
  (`render_prospect    else:` — sibling lane mid-edit in the shared
  tree; `tests/test_mountain_reveal.py` imports it). Attempts 2 and 3
  (with that file and `tests/test_behavioral_awareness.py` ignored —
  the same file W7's run ignored) were killed by the environment
  mid-run at 14% and 22% (EXIT=127, no summary line, log
  `%TEMP%/lm6_fullsuite2.log` / `lm6_fullsuite3.log` — bytes or
  nothing, unusable as evidence). Ownership-relevant evidence stands:
  this lane's 11 + the 84-test watershed family green in-session; the
  shared tree has sibling lanes in flight (untracked
  `tools/pain_replication/`, a hot `tools/mountain_reveal.py`).

## THE BREACH — St Helens board, byte-verbatim commands

Site selection (probe, deterministic): poured 150 ticks into six cold
pits; `g35x7` (floor elev 8, a closed depression 12 cells from the map
outlet `g30x0`) pools 30 wet cells with the biggest active catchment —
the lake. Its lowest dry rim neighbor is `g31x0` (elev 0, west edge):
flat-connected to the waste at equal elevation, so the lake is held by
surface tension alone until the hand opens it. THE classic setup.

```text
.venv/Scripts/python.exe tools/mountain_digflood.py load --state logs/digflood/sthelens.json --cross-section 100
  [load] N46W122 64x64 elev 0..255 waste g30x0 hash 25e926f09e3b65d2...
  [load] mantle 6 silt/cell on 4095 land cells (total 24570)
.venv/Scripts/python.exe tools/mountain_digflood.py pour 7 35 -n 24 -t 150 --state ...
  [pour] g35x7 +24/tick x 150 ticks (tick 150); drained 2; eroded 297
.venv/Scripts/python.exe tools/mountain_digflood.py dig 0 31 -k 12 --state ...
  [dig] g31x0 elev 0 -> -12 (-12); spoil +12 silt on the cell; 1 dig(s) logged
.venv/Scripts/python.exe tools/mountain_digflood.py pour 7 35 -n 24 -t 600 --state ...
  [pour] g35x7 +24/tick x 600 ticks (tick 750); drained 6636; eroded 5210
```

The lake: 150 pre-dig ticks pool 3600 units, 30 wet cells, drained 2
(a hair of the pool finds a low rim — 2 of 3600, the wall holds). Then
ONE dig — the operator's hand, 12 units into the saddle — and 600 ticks
of 24/tick: the flood. Water ledger exact: 11364 standing + 6636
drained = 18000 poured.

`flood-report` (full text also at `logs/digflood/sthelens_report.txt`,
75 lines with the 64-row trace; state at `logs/digflood/sthelens.json`):

```text
flood-report — N46W122 64x64, tick 750
  digs: 1 | g31x0 0->-12
  pour: g35x7 +24/tick x 600 ticks
  wetted cells: 53 (1% of the board), water standing 11364 units, drained to sea 6636
  max flow path (thalweg on the carved bed): 19 cells g35x7 -> reached the sea at g30x0; 18 cells still wet
    g35x7 g35x6 g34x7 g33x6 g32x5 g31x5 g30x5 g29x5 g28x5 g29x4 g30x3 g31x3 ...
  erosion: 5210 units carved by water (gross 498 below baseline, gross 21 raised, net 477 lost = dug 12 + water net 465) | washed out 465
  silt: on board 24582 (conserved == at first pour: True)
  delta: 5 silt parked at waste g30x0, bed raised 5 — growth from zero baseline
  audit: silt CONSERVED; elev accounting 477 = 12 dug + 5210 carved - 4745 landed OK
```

Trace rows 28-36 (the flood belt; `^` bars at the belt edges — the rest
of the 64x64 board is `.` untouched):

```text
.....~..........................................................
~~~~~~~~.....~.................................................
^~~~~~~~~~~^~...................................................
~~~~~~~~~.......................................................
.~~~~~~.........................................................
..~~~~~.........................................................
..~~~..~........................................................
~~...~~~~~^.....................................................
```

Read honestly: the water left the spring pit (it carved itself 6 deep
then armored on its mantle), sheeted NW as a belt ~9 rows wide, found
the dug notch at the west edge, and drained 6636 units to the sea. The
channel incised 5210 elev-units total (the whole belt carved, deepest
at the notch and spring), 4745 units landed as bars (the `^` cells),
465 washed out through the eroding thalweg, and the waste cell `g30x0`
grew a delta: +5 silt parked, bed raised +5. The first thalweg draft
(head-descent only) died in the spring pit — the fill-and-spill rim
rule was added so the route reads through pools; on the carved bed it
now walks 19 cells spring-to-sea.

Determinism proof: the exact four-command sequence re-run into a second
state → `cmp logs/digflood/sthelens.json sthelens2.json` →
**BYTE_IDENTICAL** (139,817-byte states, identical bytes).

## Files

- `tools/mountain_digflood.py` (new, 400 lines) — load/dig/pour/
  flood-report CLI; digflood.v1 state; spoil law; thalweg with
  fill-and-spill; meters round-trip.
- `tests/test_mountain_digflood.py` (new, 233 lines) — 11 tests.
- `logs/digflood/sthelens.json` + `sthelens_report.txt` — the breach
  run's durable artifacts (regenerable byte-identically from the
  commands above).
- `mag/river.py`, `mag/field_flow.py`, the board, `terrain_loader.gd`:
  untouched (ownership respected; their suites re-run green inside the
  84-family).
