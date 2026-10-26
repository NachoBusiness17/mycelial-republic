# Z3 - ST HELENS BOARD RENDERED IN GODOT (2026-09-29)

Mission (this lane's spec of record): load `logs/terrain/N46W122_board.json`
(water_graph.v1, 4096 nodes, X7 bridge) into the Godot slice, render it, and
toggle it with T. No design doc owned the render layer (WF_SYNTHESIS only
names "the Godot view" as rung-1 depth-tint); this receipt is the record.

## What landed

1. **`roblox_to_godot/scripts/terrain_loader.gd` (new)** — self-contained
   Node2D. Loads the board JSON (path order: `STHELENS_BOARD` env override ->
   `globalize_path("res://")/../logs/terrain/N46W122_board.json` -> `res://`
   copy), validates schema/shape-vs-node-count, then converts to
   `systems/water_graph.gd` field-for-field per `mag/water_graph.py
   from_spec()`: add_node(elev/kind/sill/volume) per node, add_pipe
   (src/dst/cap/siphon/crest/open) per pipe (board ships zero — WF rung 2's
   sheet-flow pipes are NOT fabricated here), tick_count from spec. The
   spec's `steam` field is ignored exactly as python from_spec ignores it.
2. **Render**: 64x64 minimap of filled quads, top-right (5 px cells, 320x320
   — the full map cannot fit 1152x648). Elevation ramp 0..255 (lowland ->
   foothill -> upland -> subalp -> snow lerp stops), cold pits tinted slate,
   waste outlet magenta, volume as brightness lerp toward aqua (cap 4 units),
   steam as a white dot; header line carries tile/shape/counts/hash8/tick,
   footer carries click hint + last events. The terrain's OWN water graph
   ticks underneath (Timer 0.8 s, matching the Mountain board).
3. **Playable**: left-click a wet minimap cell boils 1 unit; steam condenses
   at the highest cold node (engine law) — brightness visibly teleports.
   Deterministic demo water, honestly labeled: spec loads verbatim (all
   volumes 0), then one RAIN_SEED=3 deposit at the highest plain node so the
   brightness path has something to show. No RNG anywhere.
4. **One menu hook in `game.gd`**: KEY_T in `_unhandled_key_input` lazy-loads
   the loader on first press (zero cost until asked), then toggles
   visibility/timer. The Mountain board and its water graph keep running
   underneath the minimap. No other game.gd behavior touched.

## Verification (byte-run, 2026-09-29, Godot 4.3 console exe)

- Canonical: `"tools/godot/Godot_v4.3-stable_win64_console.exe" --headless
  --path roblox_to_godot --quit-after 60` from repo root -> exit 0, zero
  errors (run twice: after the code landed, and after throwaway cleanup).
- Instrumented pass (throwaway SceneTree script, run then deleted; X8
  precedent): nodes=4096 rows=64 cols=64 cold=238 waste=g30x0 (byte-matches
  the board); rain g9x15 vol 3; boil lifted 1 -> event `Steam condenses at
  g7x20 (+1).` (highest cold node, 0 -> 1); click-to-boil wet branch lifted
  (3 -> 1 after two boils), dry branch printed `g0x0 is dry - nothing to
  boil.`; toggle on/off ran; exit 0, zero errors.

## Boundaries

- Concurrent traffic observed mid-lane: sibling lanes landed a Z10 hydrology
  port into `systems/water_graph.gd` (+ `graph.hydrology`, KEY_H in game.gd)
  and throwaways `z10_smoke_temp.gd` / `z14_probe.gd`; not this lane's
  edits. My loader rides the add_node/add_pipe/tick/boil/volume API, which
  Z10 kept compatible (trailing-default args only); both smokes above ran
  against the co-landed tree.
- No commit (operator's push). No pipes synthesized; no elevation or volume
  data altered on disk.
