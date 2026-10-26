# X3 — WATER WELD: the reprint pass-off handler

- **Wave:** coverage gap 3 (2026-09-29, .venv) · welding W3D's owed seam
- **Seam welded:** `watch/inbox/mates_leave_protocol/W3D_REPRINT.md` "Honest seams left open" item 2: REPRINT's water module pass-off no-oped (`handled: False`) because `water_computer.py` wasn't in that lane's file set.
- **Files:** `mag/water_computer.py` (the reprint pass-off only: `reprint_salvage()` + `_drained_spec()` + `handle()` atype routing + docstring line), `tests/test_reprint.py` (+3 tests, factory grew a `module_id` kwarg). No commit.

## The law (the water remembers)

A module's state lives in its own flag namespace, so on reprint the water module re-claims that namespace from the corpse the engine names (`camp["reprint_of"]`, with the `raw` hand-off line as fallback). This honors the W3D seam law: the module speaks in the pass-off; the engine's keep-list never grows.

- **Honest death** — graph mode: the corpse's `water:graph` spec carries as-died (topology + node volumes + valve positions + tick); legacy mode: `WATER_STATE_KEYS` (`water:source/work/out`, `water:phase`, `water:rain`, `water:ice`, `steam`, `charge`) carry as-died.
- **Cheat death** (`cheated()`/`scorched()` on the corpse, the engine's dropped-flag vocabulary) — the mode carries, the memory doesn't: graph topology drained (volumes + steam zeroed, every pipe shut, fireball semantics on the graph); legacy tanks reseeded via `seed()`. The water must not smuggle the cheat's effects (bucket height, nuke steam) back in through its own namespace.
- **Never carries** — `water:anchored` (the proof dedupe is per-campaign; the clone earns and anchors its own leaf) and the bare `flowed` flag (the out-height mirror re-fires on the clone's first tick: the level is remembered, the win verdict is re-walked).
- Unreadable/missing corpse → `handled: True` with an honest error, never a raise; the engine's try/except stays unbitten.

Return shape: `{ok, handled, events, water_salvage: {from_campaign, mode, dishonest, carried, volumes}}`; events ride the clone's log via the engine's existing pass-off logging.

## Tests (real counts, instrument named)

- `pytest tests/test_reprint.py -q` → **9 passed** (2026-09-29, .venv). Was 6 at W3D landing; +3 X3 tests: graph volumes carried (engine still folds `water:graph`/`water:anchored` into the knot while the module carries the spec onto the clone; `water:anchored` absent from the clone), legacy heights/phase/charge carried, cheat death drains (graph all-zero + shut; bucket corpse reseeds 3/0/0, no `cheat:bucket`).
- Water family regression `pytest tests/test_water_computer.py tests/test_water_graph.py tests/test_water_graph_campaign.py tests/test_water_graph_starvation.py tests/test_water_swarm.py -q` → **31 passed** (2026-09-29, .venv). W3D's narrower 2-file regression read 16; the 31 is the wider 5-file family, same instrument, different file set.
- Adjacent surface `pytest tests/test_adventure_moonshot.py -q` → **4 passed** (only other test file importing game_campaign).

Counts are executed outcomes (one `pytest -q` per named file set, one moment), not collected snapshots; no two counts from different moments were differenced.

## Seams left open

- `handle_game` wiring for the reprint verb remains open from W3D (engine-side, untouched here).
- Legacy-mode salvage carries `charge` (rain-wheel energy) under "the water remembers"; if the operator wants energy forfeited on death, it is a one-key edit to `WATER_STATE_KEYS`, not a law change.
