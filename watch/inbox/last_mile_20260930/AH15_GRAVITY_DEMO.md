# AH15 — GravityPlane demo scene: AD7 follow-up (the scene AD7 described, built)

**Seat:** gravity_demo.tscn + gravity_demo_boot.gd owner · **Date:** 2026-09-30 · **No commit (working tree).**
**Files owned this lane:** `roblox_to_godot/scenes/gravity_demo.tscn` (new) + `roblox_to_godot/scripts/gravity_demo_boot.gd` (new) + this receipt.

## Mission

AD7 built `gravity_plane.gd` standalone with the demo-scene wiring described
in its receipt but not built. This lane builds the minimal demo per that
description, with the probe hook callable from the demo boot and a headless
verify — still NOT wired into the 2D game.

## What was built

Pattern match first: `project.godot` main_scene is `main.tscn`, and
`main.tscn` is a bare root node + script (game.gd builds everything in
code). The demo matches: `gravity_demo.tscn` = bare `Node3D` root +
`gravity_demo_boot.gd`; the boot constructs the whole scene in `_ready()`.

Constructed nodes (per AD7 §Demo scene wiring):

- **Floor** — StaticBody3D, BoxShape3D 20x0.5x20, layer 1, top face at y=0
  (+ visible BoxMesh; the demo is meant to be looked at).
- **EastWall / WestWall** — StaticBody3D 0.5x6x20 at x=±10.25, layer 1, each
  carrying a **GravityPlane Area3D** (script `gravity_plane.gd`), collision
  box 1x6x18 overlapping the walk-through space (world x in [9,10] /
  [-10,-9]), `plane_normal` (1,0,0) / (-1,0,0) = outward normals,
  `wall_surface` -> own wall (explicit), monitoring on, mask 1.
- **Player3D** — CharacterBody3D, layer 1, group `gravity_player`,
  CapsuleShape3D r=0.3 h=1.6 (feet at origin), no controller (future 3D
  controller's lane); child **CameraPivot** (y=1.2) wired as the volume's
  `camera_pivot`, carrying Camera3D (slight pitch, back 3.5 — pivot owns up).
- **PlaneLabel** — Label3D (billboard) showing current plane index + name +
  normal vector; updated on every accepted shift.
- One DirectionalLight3D so a real run is not a black screen.

## Probe hook (demo boot surface)

- `shift_to(plane_idx)` on the boot — routes to the wired volume for that
  index (2=east, 3=west; other indexes -1: the demo's own two-plane surface
  map, gravity_plane.gd's six-entry table stays in its own lane), calls the
  REAL `volume.shift_to` (`_begin_shift` path, not a mock), updates the
  label on success.
- `probe_settle(plane_idx)` — freezes `auto_tick` on all volumes, shifts,
  fixed-step `tick(1/60)` loop until settled (+1 float-tail tick), returns
  `probe_state()` + `ticks`. Deterministic: no renderer, no frame timing.
- `_run_headless_probe()` — under `DisplayServer.get_name() == "headless"`
  the boot probes planes 2 and 3 itself and `quit(0)` only if both give
  `align > 0.999 and camera_align > 0.999 and reparented`; one print line
  per plane so the log proves the probe ran.

## Verification (bytes, not reports — executed this session)

- **Import:** `tools/godot/Godot_v4.3-stable_win64_console.exe --headless
  --path roblox_to_godot --import` -> **exit 0**, **0** SCRIPT ERROR lines.
  (First run caught a parse error in my own boot script — `:=` inference on
  a Variant boolean at line 220; fixed to explicit `bool`, re-run green.
  The instrument was live from the first command.)
- **Scene run:** `… --headless --path roblox_to_godot
  res://scenes/gravity_demo.tscn` -> **exit 0**, **0** SCRIPT ERROR lines,
  output:
  `AH15 probe plane 2 -> OK ({ "phase": 2, "settled": true, "t": 0.4,
  "target": (1, 0, 0), "player_up": (1, 0, 0), "align": 1, "camera_up":
  (1, 0, 0), "camera_align": 1, "reparented": true, "player_parent":
  "EastWall", "ticks": 25 })` and plane 3 mirrored (target (-1,0,0),
  parent WestWall). 25 ticks = 24 + 1 float tail, exactly AD7's contract.
- **Negative control (throwaway, created-run-DELETED):** copy of the boot
  with the gate threshold raised to 1.1 (impossible; align maxes at 1.0) ->
  **exit 1**, both planes print FAIL — the quit code carries the verdict,
  not a vacuous 0. Temp script + tscn deleted.
- **Not wired into the 2D game:** `grep -rn gravity game.gd main.tscn
  project.godot` -> no matches (exit 1); only `gravity_demo.tscn` +
  `gravity_demo_boot.gd` reference the demo. `project.godot` untouched.
- **Tree hygiene:** Godot import cache under `roblox_to_godot/.godot/`
  deleted after verify (only the tracked `.gdignore` remains);
  `git status roblox_to_godot/` shows exactly the two new files untracked.

## Not done / boundaries

- No player controller / gravity force / wall-slide movement — future 3D
  controller's lane (unchanged from AD7).
- Two wall volumes, not six — the mission asked for two; the four unwired
  NORMAL_TABLE entries stay reachable through `gravity_plane.gd`'s own
  `shift_to` in its lane.
- No commit; working tree only (lane style).

**Receipt law:** exit codes, error-line counts, and quoted output all from
executed runs this session; no hand-counted claims.
