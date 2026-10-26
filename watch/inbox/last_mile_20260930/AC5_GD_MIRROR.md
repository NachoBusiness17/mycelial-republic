# AC5 — Godot mirror of the V5 STARVED economy fix

**Seat:** water_graph.gd mirror owner · **Date:** 2026-09-30 · **No commit (working tree).**
**Files owned this lane:** `roblox_to_godot/systems/water_graph.gd` + this receipt.

## Mission

V5 (2026-09-29) fixed the STARVED economy in `mag/water_graph.py`: waste now
HOLDS volume, the STARVED spill ROUTES to waste, boil-from-waste recovers.
The Godot mirror still carried both deletion points (named in V5_ECONOMY.md's
"sibling surfaces" list at old `.gd:186` and `:262`/`:291`). Ported.

## The port (3 edits, byte-mirrored from the Python law)

1. **`_move` to waste, boolean branch**: `dst.volume += flow` added before
   the "to waste" event — the old early-return deleted every piped unit.
2. **`_move` to waste, hydrology (Z10 graded) branch**: same fix with
   `graded` — both head laws hold now.
3. **STARVED branch**: the old `node.volume = 0` with NO destination (event
   string lied "spilled to waste") now routes the pooled spill to the FIRST
   waste node in insertion order (`for n in nodes.values()` — Dictionary
   preserves insertion order, same determinism as Python's `values()`), and
   waste holds it. No waste node in the graph: volume is HELD at the
   junction, never deleted. Event grammar matches the Python engine exactly
   (basin name + "boil {basin} to recover them" hint) so HUD parsing and
   client/server logs stay aligned.

**Boil-from-waste needed no edit**: `boil()` already lifts ANY node's volume
and `_condense_steam()` already condenses at the highest `cold` node (manual
max-by-elev loop). The `_move` deletion was the only blocker. game.gd's HUD
already draws the WASTE pool and SPACE boils by it (`_try_boil`).

## Verification (bytes, not reports)

- **Required headless smoke**: `tools/godot/Godot_v4.3-stable_win64_console.exe
  --headless --path roblox_to_godot --quit-after 60` — **exit 0, zero ERROR /
  WARNING lines** (grep over captured log; banner only).
- **Functional probe** (throwaway `ac5_probe.gd`, SceneTree script mode,
  created-run-DELETED, X8/W3 idiom; `git status roblox_to_godot/` clean of
  it): 14/14 checks PASS, exit 0 — (A) piped-to-waste holds 3 boolean;
  (B) sill starve: hold-pool event, STARVED routes 4 to waste naming basin
  + boil hint, junction zeroed, `boil("waste",4)` lifts, condense at Crown
  (+4), economy conserved == 4 end to end; (C) no-waste-node STARVED holds
  4 at the junction with the honest event; (D) `hydrology=true` graded flow
  to waste holds 3. Probe log: `/tmp/ac5_probe.log`.
- Probe's own exit-time "ObjectDB leaked" note is the harness script's
  unfreed WaterGraph instances (script-mode artifact); the real-scene smoke
  above shows zero.

## Not ported (adjacent gaps, for their owners)

- **LW5 probe-time reservation** (W1_NEGVOL_FIX, `mag/water_graph.py`): the
  .gd still decrements `src` at gate phase, not probe time — the
  shared-source double-count shape is still open in the mirror. Separate
  law, separate lane; flagged, not smuggled into AC5.
- `tools/legality_propagator.py:186` STARVED zeroing — still stale vs the
  engine (carried over from V5's sibling-surfaces list).

**Receipt law:** every claim read from the files or from executed runs this
session (smoke + probe logs on disk); no hand-edited counts.
