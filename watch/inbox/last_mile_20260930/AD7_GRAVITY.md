# AD7 — GravityPlane: AC1 steal #3 (Resonant wall-walk, banked for 3D)

**Seat:** gravity_plane.gd owner · **Date:** 2026-09-30 · **No commit (working tree).**
**Files owned this lane:** `roblox_to_godot/scripts/gravity_plane.gd` (new) + this receipt.

## Mission

AC_WAVE_SYNTHESIS.md steal #3: gravity-plane shifting — "rotate up-vector,
slerp camera, reparent to wall — pure math, brain-breaking", zero GPU cost.
The Mountain is a 2D water-graph top-down, so this lands as a STANDALONE 3D
script: NOT referenced by game.gd (grep-clean), NOT in any scene — the
mechanism banked for the 3D expansion, with the demo-scene wiring below.

## The mechanism (`extends Area3D`, ~200 lines, Godot 4.3)

On player entry (`body_entered`, player found via export or group
`gravity_player`) the volume does the three Resonant moves:

1. **Up-vector slerp, 0.4 s**: shortest-arc quaternion from the player's
   live `basis.y` onto the plane's outward normal; player basis is
   `Quaternion.slerp`-ed per tick with a smoothstep weight that lands at
   EXACTLY 1 (never a hair off target). Re-entry mid-shift re-targets from
   the current orientation, so chained volumes blend instead of snapping.
2. **Reparent to the wall surface**: `player.reparent(wall, true)` (world
   transform kept) — a rotating/moving wall then carries the player free.
3. **Camera pivot lockstep**: the SAME delta-quaternion slerps the camera
   pivot, so screen-down always reads as the new down without a snap.

Determinism guards: the antiparallel case (floor <-> ceiling, index 0 -> 1)
has no unique shortest arc, so `_shortest_arc` pins a stable fallback axis
(cross FORWARD, else cross RIGHT) — no cross-platform flake; all slerps are
plain double math, no renderer dependency.

## Deterministic test hook

- `shift_to(normal_idx)` — indexes `NORMAL_TABLE` (0 floor, 1 ceiling,
  2 east, 3 west, 4 south, 5 north); returns 0 / -1 bad index / -2 no
  player. Goes through the SAME `_begin_shift` as physics entry — the probe
  exercises the real path, not a mock.
- `auto_tick = false` + `tick(1.0/60.0)` loop — fixed steps, no frame-timing
  dependence; 24 ticks = 0.4 s (loop on `settled`, +1 tick for float tail).
- `probe_state()` — Dictionary with `align`/`camera_align` (dot vs target),
  `reparented`, `player_parent`, `phase`, `t`: everything a headless
  assertion needs. Assert shape: `align > 0.999 and camera_align > 0.999
  and reparented` after the tick loop (SceneTree script mode, AC5 idiom).

## Demo scene wiring (described here, NOT built — wire when 3D expansion lands)

```
GravityPlaneDemo (Node3D)
├─ Floor (StaticBody3D + BoxShape3D 20x0.5x20, collision layer 1)
├─ EastWall (StaticBody3D + BoxShape3D 0.5x6x20, layer 1)   <- wall surface
│   └─ GravityPlaneEast (Area3D, script gravity_plane.gd)
│       ├─ CollisionShape3D BoxShape3D 1.0x6x18  <- overlaps the space the
│       │                                            player walks through
│       ├─ plane_normal = (1,0,0)   <- wall's OUTWARD normal = new up
│       ├─ wall_surface -> EastWall (defaults to parent; explicit is clearer)
│       └─ monitoring on, collision_mask = 1
└─ Player3D (CharacterBody3D, layer 1, group "gravity_player")
    ├─ CollisionShape3D (CapsuleShape3D)
    └─ CameraPivot (Node3D, y=1.2)  <- camera_pivot export target
        └─ Camera3D (slight pitch; no roll of its own — pivot owns up)
```

Six volumes (one per NORMAL_TABLE entry) on six walls = the full demo:
walk into any doorway-field and the world leans you onto that wall.
Gravity FORCE is out of prototype scope on purpose: the future 3D
controller applies `velocity += -basis.y * 9.8 * delta` — after the shift,
`basis.y` already IS the new up, so nothing else changes.

## Verification (bytes, not reports)

- **Syntax check (mission-bounded: check-only, no game run):**
  `tools/godot/Godot_v4.3-stable_win64_console.exe --headless --path
  roblox_to_godot --check-only --script res://scripts/gravity_plane.gd`
  -> **exit 0**, banner only, zero SCRIPT ERROR lines.
- **Negative control (instrument proof, throwaway created-run-DELETED):**
  same command on a temp script with two deliberate parse errors ->
  **exit 1** + 3 SCRIPT ERROR lines; temp deleted, `git status
  roblox_to_godot/` shows only the new file (untracked).
- Not run (out of lane scope by mission): functional tick-loop probe and
  the 60-frame scene smoke — the hook above is the contract for whoever
  wires the demo scene.

## Not done / boundaries

- Not wired into game.gd or main.tscn (2D game; this is the 3D bank).
- No .tscn created — scene lives in this receipt until the expansion.
- Player controller, actual gravity acceleration, wall-slide movement:
  future 3D controller's lane.

**Receipt law:** exit codes and error lines quoted from executed runs this
session; no hand-counted claims.
