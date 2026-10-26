# V6 — fish flee push 2.5 -> 6.0 (Z14: zero chase tension)

Date: 2026-09-30 · Lane: V6 (ZCode) · Commit: NONE (uncommitted, per lane law)

## Mission (Z14)

"fish flee at 2.7 px/s vs a mouse cursor = zero chase tension; flee push needs
3x" — bump the flee push (2.5 -> 6.0, ~2.4x velocity gain preserving the tire
mechanic) and FLEE_RADIUS 14 -> 20 if too small for the new speeds.

## Changes (this lane's ownership: flock.gd flee tuning + one constant)

1. `roblox_to_godot/systems/flock.gd:62` — flee accel `2.5 -> 6.0` (was :49;
   the fix comment moved it). Receipt comment in-file names the cause.
2. `roblox_to_godot/systems/flock.gd:14` — `FLEE_RADIUS 14.0 -> 20.0` (was :9);
   header scale-law comment updated to stay truthful.
3. `roblox_to_godot/scripts/game.gd:66` — `BRAIN_FLEE_PUSH 2.5 -> 6.0`, THE
   one owned constant outside flock.gd. Required: the Z7 brain path is the
   live path (`_step_brain` runs every legal frame; flock.step is fallback),
   so the mirror had to ride or play would still flee at 2.5.

Fatigue accrual/decay, COAST_TIME, DRAG, CATCH_RADIUS, BRAIN_TIRED: untouched.

## Why it feels right (the math)

- Terminal flee speed under drag 0.985: `P / (60 * 0.015)` = 2.78 px/s old
  (the "2.7 px/s" Z14 measured) -> 6.67 px/s new.
- What the player actually meets is the BURST: fleeing spends fatigue at
  dt/COAST_TIME, so a fish gets ~0.8s of accel per approach. Probe (direct
  flock.step sim, 60Hz, player parked 5px away):
  `max_flee_speed=3.384` new vs computed `~1.43` old (2.78 * (1-0.985^47))
  = 2.37x, the intended ~2.4x.
- Tire law verified intact: `fatigue_full_at=0.78s` (= COAST_TIME 0.8),
  `dist_at_spent=6.5px` (spent fish coasts just outside CATCH_RADIUS 3.5),
  `fatigue_under_0.7_at=1.4s` (the fatigue>0.7 catch window lasts ~0.6s of
  ~2-3 px/s coasting — catchable with an active cursor), `catch_fired=true`
  (tired fish at dist 0 killed). Probe created, run, deleted
  (`v6_probe.gd`, pattern of Z14's z14_probe.gd). GDScript note: lambdas
  capture locals BY VALUE — first probe's signal-written counter never
  propagated; re-verified via direct dictionary reads.

## Verify

- Headless smoke `tools/godot/Godot_v4.3-stable_win64_console.exe --headless
  --path roblox_to_godot --quit-after {60,300,900}` -> exit 0, banner only,
  zero script errors (same clean signature as Z14_FEEL_PASS).

## Handoff notes (not this lane's ownership)

- `fish_brain.gd:30` mirrors `FLEE_RADIUS := 14.0  # flock.gd:9` — now stale
  in BOTH value (14 vs 20) and line cite (flock.gd:14). The brain path still
  TRIGGERS flee at 14px while the fallback triggers at 20. That lane should
  true it up (or the operator syncs it).
- Other in-file `flock.gd:NN` citations in game.gd's Z7 block drifted +5/+13
  lines from my receipt comments (flee push now :62, FLEE_RADIUS :14).
  Cosmetic; left for the game.gd owner.
- Working tree also carries other lanes' uncommitted work (water_graph.gd,
  terrain_loader.gd, game.gd Z7/Z14 edits predating this lane): untouched.
