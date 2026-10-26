# V4 — JUICE: SHAKE, FLASH, SOUND, TENSION (2026-09-30)

Lane: last-mile wave, Z14's feel notes ("no sound, no shake, no win
celebration"). File ownership held: `roblox_to_godot/scripts/juice.gd` (new)
+ one hook in `roblox_to_godot/scripts/game.gd`. This seat made NO commit
(see "Commit sweep note").

## What landed

| Feel | Mechanism |
|---|---|
| Screen shake on boil | A Camera2D pinned at (576, 324) — the identity transform while idle — takes a <= 3 px offset that decays linearly over 10 frames. Direction rotates per frame through the hash -> 64-entry sine table (water_particles.gd idiom). Zero RNG |
| Crown-fill flash on WIN | One-shot expanding ring off the Crown (radius 30 -> 105 over 0.8 s, quadratic fade) + a standing 5 Hz pulse on the ring. Drawn on an internal CanvasLayer at layer 2 so it beats the HUD win panel (a 0.88-alpha full-screen ColorRect would swallow anything under it in the world canvas) |
| Procedural audio | AudioStreamGenerator synthesis, zero audio files: boil = 620 Hz sine blip, 90 ms, sin envelope (no click); WIN = C5/E5/G5 chord, 1.1 s. Phase advances by pushed frame index against `AudioServer.get_mix_rate()`; nothing samples the clock, nothing is random |
| Tension vignette | Radial GradientTexture2D built in code (transparent core, dark rim; corners clamp to full rim). Fades in over 0.5 s at crown >= 3 (alpha 0.75 at 3, 1.0 at 4), fades back out below 3. Draws over the board, under the HUD text |

Triggers: the host's `last_events` feed — the live water_event channel in BOTH
net modes (the graph's `water_event` signal is declared but never emitted;
water_particles.gd is the receipt). Boil strings: sovereign `"You boil 1 unit
at spring; it rises."` (game.gd `_try_boil`) and authoritative `"ada boils 1
at spring; it rises."` (server/world.py `_apply`). Authority untouched: juice
reads graph/pools/last_events/won and mutates nothing of the sim.

## Clock law

No wall clock anywhere. `clock` tracks `host.sim_time` frame for frame until
the win; game.gd freezes sim_time the frame `won` flips (its `_process`
early-returns), so after the win the clock keeps accumulating delta — the
same instrument sim_time itself is — because a frozen clock would freeze the
win celebration on its first beat. Probe-verified: clock advances past the
frozen sim_time after `_crown_filled()`.

## Verification (all byte-run 2026-09-30, Godot 4.3 console exe)

- Smoke, canonical lane command from repo root: `--headless --path
  roblox_to_godot --quit-after {60,300,900}` -> exit 0, BANNER ONLY, zero
  errors, zero warnings (all three, plus `MAG_HYDROLOGY=1` at 300f).
- Probe (throwaway `v4_probe.gd`, z14 run-then-delete idiom, deleted after):
  10/10 PASS, exit 0 — boil fires shake + queues a blip; shake decays to the
  pinned center in 10 frames; vignette ramps at crown 3 and fades below 3;
  win arms the flash, queues the chord, flash canvas sits on layer 2; burst
  decays (44 frames); juice clock runs past the frozen sim_time.
- Determinism: zero RandomNumberGenerator, zero randf/randf_range; all
  pseudo-variation is `absi(hash(int)) % 64` through the sine table; all
  phases derive from sim_time (or the post-win delta accumulator) and frame
  counts.

## Three real defects found and fixed by the byte-runs (fix comments in file)

1. `Camera2D.ANCHOR_DRAG_CENTER` does not exist in 4.3 — it is
   `ANCHOR_MODE_DRAG_CENTER` (found via `--dump-extension-api` on this exact
   binary, not from memory).
2. The 4.3 API keeps buffer I/O off the generator: `get_frames_available()` /
   `push_buffer()` live on `AudioStreamGeneratorPlayback`, taken from the
   player AFTER `play()` (API dump again). First draft pushed to the generator
   and failed type inference.
3. `bind()` runs pre-add_child (the water_particles contract), but
   `make_current()` and `play()` both error outside the scene tree: all node
   building moved to `_ready()`. Fix carried the evidence: the 60f smoke
   printed exactly those three ERROR lines before the move, banner-only after.

## Headless audio law (the mission's "must not error" clause)

Bisect: HEAD with the audio build at 300f headless trips
`WARNING: ObjectDB instances leaked at exit` (the dummy driver has no sink
for a live generator player); the pre-V-WAVE baseline (f8452e01a) is clean;
HEAD with only `_build_audio()` stubbed is clean — so the leak is the audio
path alone. Fix: `_build_audio()` returns early when
`DisplayServer.get_name() == "headless"`. No device -> no player -> the
smoke stays banner-only; on a real display the synth path runs in full. The
queue also caps at 1 s so a stalled device can never grow it unbounded.

## Commit sweep note (not this seat's action)

The mission said no commit; this seat made none. Three coordinator sweeps
captured the lane mid-flight: ff1c02822 took the first compiling juice.gd
(after fix 3, before the headless guard), and the later ac17d5da8 /
f6af8bf1d mega-commits took the final 353-line guarded version AND a
mid-flight copy of the probe. Byte-verified: HEAD (f6af8bf1d) juice.gd is
353 lines with the guard, identical to the working tree. The probe was
deleted after its last run (run-then-delete law), leaving the tree's only
roblox_to_godot delta as that deletion (` D v4_probe.gd`, 63 lines) — the
operator's sweep or commit should carry it.

## Files

- `roblox_to_godot/scripts/juice.gd` — NEW, 353 lines (four feels + receipts).
- `roblox_to_godot/scripts/game.gd` — the one hook: `const Juice` preload +
  12 lines in `_ready` between `_build_player()` and `_build_hud()` (draw
  order: vignette over the board, under HUD text). No other game.gd change.
- `watch/inbox/last_mile_20260930/V4_JUICE.md` — this receipt.
- `roblox_to_godot/v4_probe.gd` — created, run (10/10 PASS), deleted.
