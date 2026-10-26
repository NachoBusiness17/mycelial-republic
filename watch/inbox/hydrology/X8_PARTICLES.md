# X8 - WATER PARTICLES: Watershed rung 3 landed (2026-09-30)

## What was built
`roblox_to_godot/systems/water_particles.gd` (new, 370 lines) - the client-render
droplet layer, rung 3 of the WF_SYNTHESIS ladder ("droplets with position+velocity
riding the field"). Integration in `roblox_to_godot/scripts/game.gd`: 1 preload
const + 1 var + a 5-line hookup in `_ready()` (after `_build_water()`, before
`_build_flock()`) + 1 tick line `particles.step(delta, sim_time)` in `_process()`.
No commit.

## Honest note on the cited design doc
The task brief said to READ `watch/inbox/water_engineering_20260930/WE_PARTICLE_DESIGN.md`.
That file does not exist - the folder holds only GB/WA/WB/WD/WF (byte-checked
2026-09-29 ~23:50 EDT). Built instead from the task brief's inline spec (pipe
flow = capsule velocity flow/cap; XOR junctions spawn curl rings with exp
falloff; advect + drag 0.985 + respawn at pipe srcs proportional to flow;
splash rings on water_event strings; sim_time-driven, zero RNG, authority
untouched) + WF_SYNTHESIS rung-3 language. Nothing was fabricated as "read".

## Mechanics
- Field, read-only off the integer graph: per pipe, flow = min(cap, src.volume)
  when open + head/prime allows (water_graph `_available` arithmetic recomputed
  client-side); inside the capsule corridor droplets get along-pipe velocity
  PIPE_SPEED * flow/cap with a parabolic radial profile + mouth-capture pull.
- XOR junction "passes"/"sill reached" events spawn curl rings: tangential
  velocity amp * exp(-dist/68px), 3.2 s decaying life, spin = hash(node_name)
  parity. Pooled gated nodes also carry a standing churn (amp prop. to volume)
  so held water visibly spins. Wet pools gather nearby droplets.
- Splash rings (drawn expanding arcs, colored per event kind: flow/junction/
  siphon/steam/waste/boil/fish-tag) parse the host's `last_events` feed - the
  graph declares `signal water_event` but never emits it, and `last_events` is
  the live channel in BOTH sovereign and authoritative modes.
- Determinism: zero RandomNumberGenerator. Per-droplet phase/jitter/lifetime
  from hash(index) through a 64-entry sine table; all time bases are the
  sim_time the caller passes (flock.gd W1 law - no wall clock anywhere).
  Respawn "proportional to flow" is a weighted round-robin wheel over integer
  flow units, not a random sample.
- Authority untouched: no tick/boil/open/close calls; renders as a child
  Node2D above the board, below the HUD CanvasLayer.

## Verification (byte-run, 2026-09-29 late)
- Canonical: `"tools/godot/Godot_v4.3-stable_win64_console.exe" --headless
  --path roblox_to_godot --quit-after 60` from repo root -> exit 0, zero
  errors. A 400-frame rerun (exercises the 0.8 s tick + event parsing):
  exit 0, zero errors.
- Instrumented pass (throwaway SceneTree script, run then deleted): fed all 9
  event-string shapes + a garbage string -> curls spawned (2 alive at cutoff),
  splashes lived and expired on schedule, feed-pop branch exercised, garbage
  parsed to nothing, spawner wheel advancing, field_at(gate1) = 90 px/s.
  steady state ~163 droplets alive at t=2 s from a 220 cap (spawn rate
  raised 1.4 -> 3.0/unit/s after the first run read thin).

## Known approximations (deliberate, render-only)
The host feed caps at 6 strings and both game.gd append paths trim to 3 per
tick; when the feed shrinks between frames the parser treats the last 3 as
new, which can double-ring a survivor in the rare >6 burst. Deterministic,
cosmetic, touches no authority.
