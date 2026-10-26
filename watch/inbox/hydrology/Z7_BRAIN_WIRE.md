# Z7 — BRAIN WIRED: game.gd consumes fish_brain motion rows (2026-09-30)

Lane: water engineering wave. No commit (operator's fence). File touched:
`roblox_to_godot/scripts/game.gd` ONLY (the flock wiring section + its
preloads/consts/vars + one header line). `flock.gd` read-only as ordered;
`fish_brain.gd` untouched (X9's file).

## What landed

`_process` no longer calls `flock.step` directly. Per frame:

1. **Snapshot** (the contract fish_brain.gd documents): `{fish: flock.fish,
   player_pos, pools, wettest: _wettest_pool()}`; tick = `int(sim_time*60.0)`
   (the W1 law — never the wall clock).
2. **decide per alive fish** — `FishBrain.decide(i, tick, snapshot)`.
3. **Gate** — `_motion_row_legal()`, a rig-side mirror of MOTION_TABLE's
   payload law (server/protocol_table.py `_check_args`, read not linked):
   exact key set (BAD_ARGS), verb among the five (UNKNOWN_VERB), u8 with the
   bool-is-a-verdict rule (BAD_INTENSITY), dir a known node name
   (UNKNOWN_TARGET). ANY illegal row fails the WHOLE frame closed.
4. **Stage (AUTHORITATIVE only)** — `staged_motion[fish_id] = {tick, verb,
   intensity_q8, dir}`: the MOTION dialect shape verbatim, latest row per
   fish, bounded by school size. Not sent: the v0 wire carries no motion
   verbs (protocol_table's X9 note — the server adopts them in a later
   lane); this outbox is that lane's feed.
5. **Apply** — `_apply_motion_row()` with the X9 formula
   `accel * (intensity_q8 / 255.0) * delta`: flee = away-from-player +
   toward-far-pool (flock.gd:48-50); pursue/carry = pool pull (the
   `_pull_fish_to_water` port); dance = the wiggle (flock.gd:74), idle =
   rest-depth damping. Integration ported with citations: fatigue up/down
   (flock.gd:50,53), drag (:56), catch (:77-79 — emitted by INDEX, the X9
   identity law, fixing flock.gd:79's value-twin `fish.find`), move (:81),
   trail (:84-95, storage stays flock.gd's).
6. **Fallback** — on gate failure `_process` reruns the old math verbatim
   (`flock.step` + `_pull_fish_to_water`) and counts it in
   `brain_fallback_frames`. `_brain_trail_ok()` prechecks the inherited
   trail BEFORE any row applies, so a fallback frame never double-steps.

## Verification (byte-run, 2026-09-30)

- Canonical smokes (probe script deleted, final tree):
  `"tools/godot/Godot_v4.3-stable_win64_console.exe" --headless --path
  roblox_to_godot --quit-after 60` -> exit 0, zero errors; `--quit-after 300`
  -> exit 0, zero errors.
- Instrumented pass (throwaway SceneTree script, run then deleted, X8
  pattern): real main scene headless, 700 frames, player parked probe-side
  (its mouse-follow disabled) to pressure the school.
  - AUTHORITATIVE (live `server.server`, temp users file — `server/users.json`
    is empty so ada/steam could not auth): mode=AUTHORITATIVE, fallbacks=147,
    alive 9/12 (3 catches -> tag proposals sent), staged=12,
    `staged[0] = {"dir":"spring","intensity_q8":159,"tick":110,"verb":"dance"}`,
    verb census dance/idle/flee. Zero errors.
  - SOVEREIGN (no server): fallbacks=2, alive 8/12, score=4 (the rig's
    fish_killed emit drives the local score), trail capped 140, verb census
    pursue=426 / dance=301 / flee=65 / idle=27 / carry=21 — all five verbs
    exercised. Zero errors.
- Collateral: `pytest tests/test_motion_rows.py tests/test_protocol_table.py
  -q` -> 76 passed.

## Found defect (X9 owner's file — flagged, not fixed)

On a fully drained board `_wettest_pool()` returns `""` and fish_brain's
carry row emits `dir: ""` — typed-illegal under the dialect's non-empty
target law, so the rig rejects the frame and falls back (the 147/2
fallback counts above ARE this, engaged from ~tick 6 after the water
reaches Waste, self-recovering once no fish is tired). The fail-closed
contract works exactly as specified; the emitter should clamp wettest to
nearest-pool when the world is dry. fish_brain.gd is out of this lane's
fence (pinned by tests/test_motion_rows.py), so it stands as X9 debt.

Also noted (pre-existing, untouched): with an UNAUTHED server the client
prints one `get_available_bytes !is_open` ERROR from net_client.gd's
reject-path teardown race (W1 surface); with working auth the
authoritative run is clean.

Receipt: watch/inbox/hydrology/Z7_BRAIN_WIRE.md (this file).
