# R4 FLOCK PARITY — GDScript vs Python, measured (refire complete)

**Mission (R4 refire, 2026-09-30):** the flock exists in FOUR implementations
with no cross-check. Build the cross-implementation harness per V2ASK3's
verdict, fix Q15 (constants single-source), tests, receipt.

- Verdict source: `watch/inbox/frontier_asks/volley2/results/V2ASK3.md` (Q14/Q15)
- The four: `dashboard/static/games/swarm.html` (JS original) ·
  `roblox/src/shared/Flock.luau` (Luau original) ·
  `roblox_to_godot/systems/flock.gd` (the game's engine) ·
  `mag/flock_positive.py` `step_threat` (the per-line Python port).
  V2ASK3 pair order rules pair 1 = GDScript <-> Python (hardest precision
  problem first: Godot Vector2 is float32, Python float64); JS and Luau pair
  against the Python reference later (N-1 harnesses, never N(N-1)/2).

## VERDICT: parity holds everywhere except ONE named law — the catch-tick move

Fresh full run (`--full`, seed 20260930, 24 sequences x 5 families, 1422
teacher-forced frames, wall 6.3s, Godot_v4.3-stable headless):

- **free_school / threat_sweep / hand_frames: ZERO divergence, max pos dev
  0.00e+00 (bit-identical positions through float32 quantized teacher
  forcing), max vel dev 4.77e-7 = exactly 1 ulp32(5-scale)** — inside the
  named epsilon.
- **First divergence: seq_002 (catch_hunt) tick 34, fish 0, tier_c_pos,
  |d|=3.95e-2 px > eps 9.79e-4.** Cause (named, not mysterious): the
  catch-tick law difference — `flock.gd:146-150` sets `alive=false` then
  still runs `f.pos += f.vel * dt` (the caught fish moves one last tick),
  while `mag/flock_positive.py:177-179` returns before the move (the fish
  freezes). All 60 divergence rows (30 pos + 30 vel) sit EXCLUSIVELY on
  fish caught that same tick — verified by re-walk: violations on
  non-caught fish = 0. threshold_edge diverges at tick 1 for the same
  reason (its catch-window probes die at tick 1).
- **Tier D (discrete: alive/caught/fleeing/neighbours): exact everywhere,
  0 band-edges needed.**
- **Free-run 60-tick smoke: GREEN** — centroid dist 0.0 px, spread ratio
  1.0 (float32-quantized per tick on the Python side to match Godot storage).
- Pinned by `tests/test_flock_parity.py::test_end_to_end_only_known_divergence_is_catch_tick_move`:
  if the port is ever trued up (one-line move after the catch branch),
  parity flips fully green and that pin updates in the same commit.

## The harness (Q14, V2ASK3 build order followed)

- `tools/flock_parity.py` — driver: gen (5 seeded families: free_school,
  threat_sweep, catch_hunt, threshold_edge, hand_frames) -> Python reference
  (`fp.step_threat` executed as-is, in index order matching flock.gd's
  in-place pass) -> GDScript headless (`tools/godot/Godot_v4.3-stable_win64.exe
  --headless --script res://tests/flock_parity_runner.gd`) -> compare ->
  free smoke -> codec echo. Exit law: `FLOCK_PARITY: ok|FAIL|ERROR` (0/1/2).
- **Teacher forcing** (V2ASK3's law): each tick's input is the reference's
  float32-quantized output, so chaos cannot compound; free-running compare
  is kept only as the flock-level smoke lane. Bring-up bug this pinned: the
  Python state once rode float64 residue while frames shipped float32 and
  flipped a neighbour verdict at exactly SCHOOL_RADIUS (19.99998 vs 20.0).
- **Float transport: float32 bit patterns in hex** (`0x%08x`), little-endian
  hand-composed on both sides — decimal JSON parses differently per runtime.
  Codec corpus (NaN, +-0, subnormals, +-inf, max f32, constants) echoes
  bit-identical through the real Godot process.
- **Named epsilon (Tier C):** |a-b| <= K*ulp32(max(|a|,|b|)) + 2e-6; K=32
  pos/vel (sin/cos wiggle + pow drag + N-1 float32 school roundings),
  K=4 fatigue/satiation (float64 Variants both sides). TIER_ABS=2e-6
  (bring-up-measured cancellation, V2ASK3's 1e-6*dt=1.7e-8 widened; still
  ~2000x under the smallest real law divergence: 4.3e-3 at catch).
- **Threshold band (Tier D):** |d^2 - R^2| <= 8*ulp32(R^2) counts as `edge`,
  never failure. 0 edges fired in the final run.
- **Value-twin guard:** flock.gd's school loop skips Dictionary-equal twins
  BY VALUE while Python counts them — the generator excludes twins and a
  tripwire raises if one ever forms.

## Tests (V2ASK3 Q14 tests 1-6, 45 green)

`tests/test_flock_parity.py` (30) + `tests/test_game_constants.py` (16):
codec round-trip (pure + through real Godot) · self-parity (Python exact;
two Godot processes byte-identical) · known answers (exactly-R does not
flee, R-1ulp does, R+1ulp does not — pure radial probes; tired fish at
1.0px AND at the 3.4px catch seam die at tick 1; mirror pair at exactly
SCHOOL_RADIUS schools nobody at tick 1, y-vel bit-identical every tick) ·
mutation sensitivity (7 constant mutants incl. CATCH_RADIUS-0.5 go red;
end-to-end mutant vs real Godot) · anti-sensitivity (1-ulp perturbation
stays green) · hash guard (stale constants_hash -> exit 3, no output) ·
teacher-forcing chain pin · the honest-verdict pin. Suite:
`./.venv/Scripts/python.exe -m pytest tests/test_flock_parity.py
tests/test_game_constants.py tests/test_flock_positive.py -q` = 45 passed.

Refire fixes (this window, on the interrupted first cut):
1. Codec test wrote the wrong bit pattern (`0x439ac000`=309.5, not 310.0;
   310.0 = `0x439b0000`) — test bug, engine was correct.
2. R-1ulp probes carried y=0.05 cross-axis offsets that swamp 1 ulp
   (~2.5e-3 vs 2e-6 on d^2) — moved pure radial (y=0.0) so the ulp alone
   decides; paper truth now real on both precisions.
3. CATCH_RADIUS-0.5 mutant survived: no corpus fish sat in (3.0, 3.5] with
   fatigue > TIRED — added the 3.4px catch-seam fish (id 5, fatigue 0.8).
4. hand_frames asserted no-schooling on EVERY tick, but the wiggle x-term
   reads pos.x (310 vs 290 -> different phase) so the gap legitimately
   leaves exactly-20.0 after tick 1 — pinned to the tick-1 seam.
5. GC pin test skipped TIRED silently — now parses step_threat's inline
   `> 0.7` literal and pins it to GC.TIRED (guarded skip, not silent).

## Q15: constants single-source — LANDED (R7 true-up + R4 guards)

The drift (V6_FISH_FLEE.md): `flock.gd FLEE_RADIUS=20` (Z14/V6 tuning) vs
`fish_brain.gd=14` (stale pre-V6 mirror) vs `tools/mountain_units.py=14`
vs `mag/flock_positive.py=20`. V2ASK3 Step 0 asked same-concept-or-rename:
same concept, 20 canonical (Z14 terminal-speed math; the pin test names it).
Now: `roblox_to_godot/systems/game_constants.gd` is the const leaf (V2ASK3
verdict form — const file, NOT autoload; narrowed to preload because the
headless estate never regenerates the script-class cache). Consumers alias
(`const FLEE_RADIUS := GC.FLEE_RADIUS`): flock.gd, fish_brain.gd (trued
14 -> 20), game.gd mirrors; `tools/mountain_units.py` trued to 20;
`mag/flock_positive.py` value-pinned by parse (LM9's file, outside R4
ownership — TRAIL_RADIUS/TRAIL_DROP not mirrored (trail is visual-only),
TIRED pinned via its inline literal). Guards (V2ASK3 falsifiers):
value pin, literal lint (no raw numeric literal of a registered name
outside GC in any .gd), alias pins, Python-twin pins, and the Q14
constants_hash guard (sha256 over NAME=float32-bits lines; GD runner
recomputes from its preload and exits 3 on mismatch — proven by test).
Current hash: 76c800a623f8605b... (digest-stamped in latest.json with
twin sha256s, so a dirty tree cannot hide behind a stale verdict).

## Debt (named, not hidden)

- **Catch-tick move law:** flock.gd moves the caught fish; the port freezes
  it. One-line fix in mag/flock_positive.py (LM9's file) trues it and flips
  parity fully green — operator call, pin updates same commit.
- V2ASK3's branch mutants (`<` vs `<=` swap, dt-drop, negated separation,
  stale velocity) need source-mutation tooling — not silently skipped:
  partially covered by the exactly-at-radius known-answer probes.
- JS (swarm.html) and Luau (Flock.luau) pairs vs the Python reference:
  pairs 2-3, not built this window.
- flock_positive.py TIRED is an inline literal (pinned by parse; naming it
  is LM9's edit).

## Amendment (merge window, 2026-09-30 late)

Two R4 agents executed this mission in one working tree (R7's game_constants
landing also arrived mid-flight); the merged state is byte-stable — the
driver digest above (5b7afc10d71d) is the merged file, and the "refire
fixes" list covers both agents' identical edits. Two items this window adds:

1. **mountain_units dry-board guard (latent bug the Q15 true-up exposed):**
   with FLEE_RADIUS 20, hunt-seed 11 tick 240 drains every pool but waste,
   `_wettest_pool` returns "", and the verbatim carry row `{dir: ""}` fails
   the real MOTION_DISPATCH gate (UNKNOWN_TARGET) — verified latent under 14
   (the old radius kept that fish below TIRED at the dry moment). The rig
   degrades gracefully (game.gd falls back on a failed row); the tool is
   loud by design, so `tools/mountain_units.py` decide() now falls back to
   the nearest pool for carry on a dry board. fish_brain.gd's carry branch
   carries the same unguarded wettest (harmless in the rig today): that
   lane's debt, named here.
2. **Final merged suite:** 125 passed across the six affected files
   (test_flock_parity + test_game_constants + test_flock_positive +
   test_mountain_units + test_motion_rows + test_hunger_ledger_parity),
   .venv pytest.

## Artifacts

- Driver: `tools/flock_parity.py` (sha256 5b7afc10d71d)
- GDScript runner: `roblox_to_godot/tests/flock_parity_runner.gd` (6a9840a2edb6)
- Single source: `roblox_to_godot/systems/game_constants.gd` (a2ce6e026c00)
- Tests: `tests/test_flock_parity.py` (8182a2f20e88), `tests/test_game_constants.py`
- Standing verdict + runs: `tools/flock_parity_out/latest.json`,
  `full_report.json`, `full_python.jsonl`, `full_godot.jsonl`,
  `free_report.json`, `codec_echo.jsonl`
- Twins measured: `mag/flock_positive.py` (3af565800210),
  `roblox_to_godot/systems/flock.gd` (d7c07df42380)
