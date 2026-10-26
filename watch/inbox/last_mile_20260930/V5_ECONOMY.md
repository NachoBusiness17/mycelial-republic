# V5_ECONOMY — STARVED spill law fix (Z14 hidden economy flaw)

**Seat:** water_graph engine owner · **Date:** 2026-09-29 · **No commit (working tree).**
**Files owned this lane:** `mag/water_graph.py` + `tests/test_water_graph_starvation.py`.

## The flaw, verified against bytes

The engine TRULY DELETED water — this was not a UI problem. Two deletion
points in `mag/water_graph.py` (pre-fix):

1. **STARVED branch** (old line ~184): `node.volume = 0` with NO
   destination — the event string claimed "spilled to waste" but nothing
   received the units. Slow starters permanently lost pooled water.
2. **`_move` to waste** (old line ~237): `if dst.kind == "waste":
   ... return` fired BEFORE `dst.volume += flow` — every unit piped to
   waste was deleted too. Waste never held anything.

The recovery law already existed on paper: `boil()` works on ANY node's
volume and steam ignores pipes, condensing at the highest `cold` node.
Only the deletion blocked the loop.

## The fix (V5 economy law, 2026-09-29)

- **Waste is a basin, never a void.** `_move` now accumulates into waste
  (`dst.volume += flow`) before its "to waste" event.
- **STARVED spill routes.** The pooled spill goes to the FIRST waste node
  in insertion order (deterministic). No waste node in the spec: the
  volume is HELD at the junction (conservation beats deletion) and the
  event names the hold.
- **Event grammar** (HUD-parseable, count still in place, adds basin +
  recovery hint): `Junction {name} STARVED: {n} pooled units spilled to
  waste at {basin} ({why}; no inflow reached the gate; boil {basin} to
  recover them).`
- Recovery loop: player boils at waste -> steam -> condenses at cold
  crown. 8-unit economy conserved end to end.

## Tests (tests/test_water_graph_starvation.py)

Amended: `test_starved_event_fires_when_pooled_water_dies` (+ waste==4,
+ boil-hint assertion). Added: `test_piped_to_waste_is_held_not_deleted`,
`test_boil_from_waste_condenses_at_crown` (full recovery loop),
`test_starved_economy_conserves_total_units` (16 units conserved through
starve+boil, no hand-edits), `test_starved_without_waste_node_holds_at_junction`.

## Real counts (instrument + moment named)

- Targeted: `tests/test_water_graph_starvation.py` 8 passed;
  `tests/test_water_graph.py` 7 passed; `tests/test_water_graph_campaign.py`
  9 passed (24/24 on the trio, 2026-09-29 evening run).
- Adjacent: water_computer + mcp_bridge_r1 + propagator + legality_dataset
  + hydrology = 58 passed.
- Full `pytest -q --ignore=tests/test_behavioral_awareness.py`
  (2026-09-29, 2745.47s / 45:45 wall): **3104 passed, 14 failed, 12
  skipped, 3 errors**. Attribution: NONE of the failing files import
  water_graph (verified by grep across test_server_persist,
  test_server_v0, test_clerk_route_fix, test_cursor_bridge,
  test_desk_dialogue, test_debug_capsys, _diag_pid) — they are the
  Godot-server/clerk/desk lanes mid-flight in sibling seats (the
  .pytest_cache lastfailed was overwritten mid-read by a concurrent
  sibling pytest run, and test_server_persist-style failures are classic
  same-tree port/file collisions). Water lanes are 100% green above.
- Flake note: one transient all-error run right after editing (Windows
  file lock on fresh bytecode, likely AV scan); two consecutive reruns
  clean. Correction filed: an earlier draft of this receipt carried
  speculative full-suite numbers written before the run finished —
  replaced with the instrument's own figures above.

## Pre-existing breakage (not this lane, operator eyes)

- `tests/test_behavioral_awareness.py` is `UU` (unresolved merge conflict
  from the cursor/queue-lanes-behavioral-logging lane) — SyntaxError at
  collection, so it is ignored in the full run.
- The full run's 14 failures + 3 errors live in sibling lanes
  (server_persist, server_v0, clerk_route_fix, cursor_bridge,
  desk_dialogue, debug_capsys, memory/working planners); none import
  water_graph. The 3 errors are collection errors in `memory/working/`
  drafts.

## Sibling surfaces still carrying the OLD deletion law (for their owners)

- `roblox_to_godot/systems/water_graph.gd:186` (STARVED `node.volume = 0`)
  and `:262`/`:291` (`_move`/graded `_pipe_flow` to waste without
  holding) — the Godot mirror must adopt the basin law or client and
  server diverge.
- `tools/legality_propagator.py:186` — analysis-side STARVED zeroing;
  stale vs the engine until mirrored.
- `mag/water_computer.py:297` `_render_glass` filters waste nodes out of
  the campaign glass — held waste is now invisible to the player; show it
  (the game.gd HUD already draws a WASTE pool and supports SPACE-boil by
  it, so the UI side is nearly there).

**Receipt law:** bytes, not reports — every claim above was read from the
files this session; test numbers are from actual pytest runs named above.
