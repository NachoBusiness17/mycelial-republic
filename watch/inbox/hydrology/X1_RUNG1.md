# X1 RUNG 1: GRADED HEAD (The Watershed) — 2026-09-30

Lane X1 of the water wave. Spec: `watch/inbox/water_engineering_20260930/WF_SYNTHESIS.md` rung 1.

## What landed
- `mag/hydrology.py` (new): `HydrologyGraph(WaterGraph)` + `HydroNode`. water_graph.py is UNTOUCHED — the verdict layer keeps its boolean engine; the Watershed overrides only the head law.
- `tests/test_hydrology.py` (new): 12 tests.

## The law (integers only, no floats, no RNG)
- Node geometry: `cross_section` (int, default 1000, must be >= 1).
- `depth = volume * 1000 // cross_section` (milli-depth, small tanks still grade).
- `head = elev * 256 + depth` (Q8 elevation, HEAD_SCALE = 256).
- Flow: `min(cap, src.volume, (dHead * conductance) >> 8)`, conductance default 8. Bigger drop = bigger flow; dHead <= 0 = nothing moves (check-valve law survives); a filling pool raises its own head (backwater, equalization). Siphons keep their own law (prime at crest under positive head, then full bore).
- Spec: `hydrology.v1` schema with cross_section + conductance, exact roundtrip via `mag.hydrology.from_spec`.

## Test receipts (real counts, 2026-09-30)
- `pytest tests/test_hydrology.py -q`: **12 passed** (geometry, cross_section guard, conservation incl. steam through 60 ticks, graded 51 vs 19, backwater 12 < 19, cap saturation, no-uphill (elev + higher-head dst), equal heads no-flow, equalize-and-settle residual <= 31 with no slosh, determinism byte-identical state + event log, spec roundtrip + isinstance WaterGraph, in-process rerun of the whole legacy tests/test_water_graph.py suite).
- Water family (`test_hydrology + test_water_graph + test_water_computer + test_water_graph_campaign + test_water_graph_starvation + test_water_swarm`): **43 passed**.
- Full `pytest -q`: **7 failed, 2909 passed, 12 skipped, 3 errors, 1935.35s (0:32:15)**. Attribution: ZERO water/hydrology failures. Visible failures: test_dem_to_board x2, test_game_world_render_optics x1, test_headless_law x1 (+3 failed/3 errors truncated by my `tail -5`; the run's stdout was cut before the summary block, cache stale since 08-05). Isolation rerun: dem_to_board + render_optics PASS alone (order/concurrency — sibling lanes were writing trails/lane state during the 32-min run, git status shows live X-wave traffic). Remaining: `test_headless_ratchet_never_grows` — pre-existing repo debt (bare spawns 22 -> 34, baseline accepted 2026-09-29 by the bare-spawn-descent lane; offenders are tools/*.py, none mine). This lane touched only mag/hydrology.py + tests/test_hydrology.py + this receipt; nothing else imports hydrology.

## Next rung hooks
Depth-tint in the Godot view can read `node.depth` directly. Rung 2 (field layer) hangs off the same continuous head.
