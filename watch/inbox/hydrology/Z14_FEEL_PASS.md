# Z14 - THE FEEL PASS: the slice gets played (2026-09-30)

The Mountain had hydrology (Z10), particles (X8), motion rows (X9/Z7), dual
mode (W1) - and no player. This pass ran it, read every tuning constant, and
judged it as a game designer would. Two small edits landed with receipts;
the rest of the judgment is banked below as FEEL NOTES for the lanes that
own those files.

## Method (byte-run, all numbers from logged invocations)

- Headless smoke, pre- AND post-edit, from repo root:
  `"tools/godot/Godot_v4.3-stable_win64_console.exe" --headless --path
  roblox_to_godot --quit-after {60,300,900}` -> exit 0, banner only, zero
  errors, all six runs (60/300/900 x before/after). 900 frames = 15 s =
  ~19 water ticks at the old pace, ~30 at the new one.
- Port 8800 confirmed quiet (`netstat -an | grep :8800` -> no listener), so
  every run fell SOVEREIGN after the 2 s probe deadline. Probe line
  `mode=2 (2=SOVEREIGN)` printed in every instrumented run.
- Instrumented probe: throwaway SceneTree script (`-s res://z14_probe.gd`,
  X8's run-then-delete idiom; deleted after the last run). It puppets the
  shepherd (player.gd set_process(false), position set directly), plays the
  README loop (settle 2.3 s -> shut p_drain at the waste end -> shut p_out at
  the hollow end -> measure -> boil x4), and prints per-second telemetry.

## The two edits (roblox_to_godot/scripts/game.gd, uncommitted, no other files)

1. `TICK_SECONDS 0.8 -> 0.5` (now line 45). The boil is the game's ONLY
   progress verb and its feedback is the NEXT tick (steam condenses at the
   Crown inside `graph.tick()`). Measured SPACE->condense dead air: 0.59 s
   and 0.80 s at the old pace; 0.50 s and 0.50 s after. Water moved 1
   unit/tick while fish and droplets animate at 60 fps - between ticks the
   board read as a slideshow; 2 ticks/s keeps the integer graph legible.
   Debt named in the code comment: `server/world.py` `TICK_MS = 800` is
   untouched (out of this lane's ownership), so AUTHORITATIVE mode keeps the
   old pace until the server gets its own feel pass.
2. `POOL_PULL 10.0 -> 22.0` (now line 56). Terminal drift under drag 0.985 is
   ~65.7*PULL/60 px/s. Pre-tune the school migrated a measured 11.0 px/s
   toward the wettest pool (stable-target plateau, per-second probe t=9..16:
   11.0 px/s straight-line, matching the 10.94 prediction) - a spring->hollow
   relocation (534 px) took ~49 s. The school-follows-water loop is the
   slice's only systemic feedback and it was invisible on play timescales.
   Post-tune plateau: 24.1-24.2 px/s (prediction 24.1). Governs BOTH the Z7
   brain path (`_apply_motion_row` pursue/carry) and the flock fallback
   (`_pull_fish_to_water`) - same constant, both cited in the comment.

## FEEL NOTES - the designer's judgment the code never had (banked, not built)

- TOO SLOW (fixed above): the 800 ms heartbeat and the 11 px/s school drift.
- NO CHASE TENSION: fish flee terminal speed is ~2.7 px/s (flee accel 2.5 in
  flock.gd, drag-limited) while the shepherd is a mouse cursor moving
  hundreds of px/s. Parking the cursor dead-center for 4 s: the school just
  disperses around it (mean dist 13->88 px, mostly POOL_PULL drift, one
  accidental tag of a tired fish dragged through the 3.5 px catch radius).
  The chase has no threat either direction. Fix belongs to flock.gd /
  BRAIN_FLEE_PUSH (2.5 -> ~8 with a fatigue-gated burst would be my first
  try) - out of this lane's ownership.
- THE KNIFE-EDGE ECONOMY (discovered while probing): unattended, the
  mountain destroys itself. Trace: spring 6 bleeds 1/tick to gate1 (XOR,
  sole inlet, passes); when the spring runs dry the XOR STARVED branch
  DELETES gate1's entire pool (t=6 in the pre-tune trace: gate1 4 -> 0,
  hollow unchanged), and `_move` never adds waste-node volume either - water
  that "reaches Waste" is simply gone. `graph.volume("waste")` is always 0,
  so the README's "boil twice as hard" recovery from Waste is currently
  impossible: Waste is a void. Net: 8 units in the world, win needs 4 in the
  Crown, and a first-time player who spends >8-13 s learning the controls
  has permanently lost half the water. Verdict: legitimate pressure,
  illegible. Nothing on screen names the starvation clock. Recommendations
  for the owning lanes: an event/HUD cue when a gated pool's inflow stops
  ("gate1 pools - inflow failing"), waste-node volume if the README's
  promise is real, or a first-run grace tick. None of this is a feel-pass
  constant; banked here.
- MISSING JUICE: no screen shake on boil, no sound anywhere (zero
  AudioStreamPlayers in the tree), the win is a flat dark ColorRect (the
  Crown's filling arc - the best juice in the slice - just freezes), and a
  fish tag has a particle splash ring but no score popup. Cheap wins next
  window: pulse the Crown arc + a one-shot ring burst on `_crown_filled`,
  shake on STARVED spills (they are the dramatic beat and they are silent).
- HINT/DISCOVERY ROUGH EDGE: `_update_hints` checks BOIL first, so near any
  WET pool the "E - valve" hint never shows even when a valve is in range -
  and VALVE_RADIUS (26) is tighter than BOIL_RADIUS (40), so valves are
  both hard to hit and undiscoverable exactly where they matter (gate1
  holds water, so its p_out valve hint is permanently suppressed). One-line
  candidate: show both hints when both are in range, and/or 26 -> ~36.
- WORLD BLEED TIMING: the unattended full-bleed to Waste took ~8.3 s
  pre-tune and lands ~1.6x faster post-tune. Correct direction for an
  arcade-length slice, but it makes the illegible starvation clock (above)
  hotter - the two findings travel together.

## Collision note

The Z7 (fish_brain wiring) + Z10 (head law) lane landed in game.gd mid-pass
(the file changed under this seat between the first read and the edits). The
edits were re-based onto the new file; the constants live above the Z7 block
and touch none of it. The brain path ran healthy in every probe
(`brain_fallback=0`). The other lane's uncommitted files (water_graph.gd,
terrain_loader.gd, z7_probe.gd) were left untouched.

## Files

- `roblox_to_godot/scripts/game.gd` - 2 constants + receipt comments (lines
  36-45, 47-56). No commit, per task.
- `watch/inbox/hydrology/Z14_FEEL_PASS.md` - this receipt.
- Throwaway probe `roblox_to_godot/z14_probe.gd` - created, run 5x, deleted.
