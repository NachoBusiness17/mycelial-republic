# X9 — MOTION ROWS: THE FLOCK POLICY AS TABLE DATA (2026-09-30)

Lane: UniMate-seeded build (water engineering wave). No commit (operator's fence).

## What landed

| File | Change |
|---|---|
| `server/protocol_table.py` | Motion dialect: optional per-row `args` payload law, `ProtocolDispatch.ask()` (gate -> payload -> handler), `MOTION_SPEC`/`MOTION_TABLE`/`MOTION_DIGEST`/`MOTION_DISPATCH` |
| `roblox_to_godot/systems/fish_brain.gd` | NEW. The flock policy as a pure `decide(fish_id, tick, snapshot)` emitting motion rows |
| `tests/test_motion_rows.py` | NEW. 51 tests: table validate/reject + fish_brain determinism-by-construction |

## The dialect

`MOTION_TABLE` compiles the v0 base rows (boil/valve/join/tag, byte-identical) plus five motion verbs, each `{intensity_q8: u8, dir: target}` with a `rig_*` handler (the apply-step owner is the Godot rig, not `MountainWorld._apply` — the server adopts them in a later lane; no orphan handlers):

| verb | handler | flock.gd branch it ports |
|---|---|---|
| idle | rig_idle | tire/rest else-branch (l.51-53); rest depth = `q8(1 - fatigue)` |
| flee | rig_flee | threat branch (l.48-50); urgency = proximity; dir = pool farthest from player |
| pursue | rig_pursue | game.gd `_pull_fish_to_water` (l.29-30); urgency = dist/TRAIL_RADIUS; dir = wettest |
| carry | rig_carry | tired window (l.77,85); intensity = fatigue itself; dir = wettest |
| dance | rig_dance | wiggle (l.74); intensity = pure tick wiggle phase; dir = nearest pool |

Typed rejects through the table: `UNKNOWN_VERB`, `UNKNOWN_SID` (state gate fires before the payload is read), `BAD_ARGS` (shape), `BAD_INTENSITY` (u8 law — bools rejected: a bool is a verdict, not an intensity), `UNKNOWN_TARGET` (dir must be a known node name). Ordering law held end to end: handler provably never fires on any refusal.

Digests: `MOTION_DIGEST ce259465f063f09dfb3187140c1c0781943be6bebb62c3cc86a13f182c61d637`; `PROTOCOL_DIGEST d41f7cba...` byte-identical to git HEAD (verified by compiling `git show HEAD:server/protocol_table.py` in a temp module — trust bytes, not test self-consistency).

## fish_brain.gd determinism

`decide()` is pure: `extends RefCounted`, no class state, static entry, no RNG, no wall clock (the W1 leak law), no snapshot mutation; schoolmate identity is the array index (Dictionary `==` is by value — flock.gd:64's `other == f` skips value-twins; the index does not). The estate box has no Godot binary (`watch/inbox/GODOT_SLICE_20260929.md:37`), so same-tick+snapshot=same-row is enforced by construction + structural tests (`tests/test_motion_rows.py`: signature, nondeterminism-token ban, mutation ban, dialect-tie to `MOTION_TABLE.verbs`); first executed determinism run lands when a binary does.

## Integration note (rig side — SPEC ONLY, not built)

game.gd becomes a row consumer: each `_process` it builds the snapshot `{fish, player_pos, pools, wettest}` (all already live: `flock.fish`, `player.global_position`, `pools`, `_wettest_pool()`), then for each alive fish calls `FishBrain.decide(fish_id, int(sim_time * 60.0), snapshot)` — tick from the W1 sim_time counter, never the wall clock — and applies the row with one steering line: `f.vel += DIR[verb](row, pools, player) * (row.intensity_q8 / 255.0) * delta` (flee pushes away from the player toward `pools[dir]`; pursue/carry steer toward `pools[dir]`; dance adds the wiggle; idle damps velocity), so flock.gd's inline boid math retires — the brain owns policy, the rig owns motion — and in AUTHORITATIVE mode the same row becomes a motion proposal through `MOTION_TABLE.ask(...)`, typed-reject or staged apply, which is the point of speaking rows instead of Vector2s.

## Tests (real counts, this tree, this moment)

- `pytest tests/test_motion_rows.py -q` -> **51 passed** (0.70s)
- `pytest tests/test_protocol_table.py -q` -> **25 passed** (0.65s; v0 regression proof)
- Collateral: `pytest tests/test_operating_protocol.py -q` -> 3 passed
