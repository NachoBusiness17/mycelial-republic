# Q-020 / FW-01 — Harness trio after the second rollback (the five-suite morning wave)

- Date: 2026-09-28 · seat: queue-gopher2-Q-020 (workflow gopher) · cost: $0 (local node + local suites)
- Plan: `memory/plans/fifty_wide_20260917.md:12` — "mud replay 41/41 + mud fifty 63/63 + toy 15/15 + frontier 51/51 + swarm 32/32 — re-land per FX4/W5 if anything dropped"

## Final wave state (all commands run this session, 2026-09-28)

| Suite | Command | Result |
|---|---|---|
| mud replay | `node scripts/test_mud_replay.js` | **41/41 lanes green**, exit 0 |
| mud fifty | `node scripts/test_mud_fifty.js` | **63/63 lanes green**, exit 0 |
| toy | `node scripts/test_toy.js` | **15/15 lanes green**, exit 0 (was 13/15, 2 RED — re-landed, below) |
| frontier souls | `node scripts/test_frontier_souls.js` | **51/51 lanes green**, exit 0 |
| swarm dogfood | `node scripts/playtest_swarm.js` | **DOGFOOD VERDICT: 32/32**, exit 0 (was 0/10 crash — re-landed, below) |

Final sweep re-ran all five back-to-back: 41 + 63 + 15 + 51 + 32 = **202/202**. Nothing is dropped; no further re-land owed.

## Re-land 1 of 2 — swarm: kill-streak vars landed undeclared (game-breaking, fixed in game code)

- Symptom: every scenario died `ReferenceError: killMultT is not defined` at the first `update()` frame; DOGFOOD VERDICT 0/10, exit path crashed.
- Cause: commit `a5dd96176` added the kill-streak mechanic — reads `killMult`/`killMultT` in `gainXp()` (swarm.html:597-598 pre-fix) and a per-frame decay `if(killMultT>0){...}` at the top of `update()` (swarm.html:682 pre-fix) — but declared neither variable anywhere (`grep -n "let killMult"` → no match). First frame reads `killMultT` undeclared → ReferenceError → loop dead, in browser and harness alike.
- Fix (state init at the declaration site + per-run reset, not a guard branch):
  - `dashboard/static/games/swarm.html:163-165` — `let killMult=1,killMultT=0;` with a comment naming the cause (a5dd96176 added reads without an init) and the evidence (FW01 re-land 2026-09-28, playtest was 0/10).
  - `dashboard/static/games/swarm.html` startGame reset — `killMult=1;killMultT=0;` so a fresh run starts unstreaked.
- Proof: `node scripts/playtest_swarm.js` → **32/32**, exit 0, including `death+bonfire+charcoal` which previously died at `[stdin]:715`.

## Re-land 2 of 2 — toy: frozen tape stale against the deliberate walker rework (re-landed on the test side)

- Symptom: lanes 6 and 9 RED — TAPE_A bite outcome got `hit`, want `hit_dodged`; TAPE_A died 8 hits deep (verdict=dead, 9.3s).
- Cause: `git diff 2b85093f1 a5dd96176 -- dashboard/static/games/toy.html` shows a deliberate walker rework committed without carrying the tape: speed 70→95, 1.35 chase multiplier when d>60 ("closes the kite gap — no free range"), a 45% lunge at telegraph end ("dodge or bleed"), swing reach 55→38. `scripts/test_toy.js` untouched by that commit. Under the new physics the telegraph fires at t=0.55 and the bite lands at t=0.90; the old TAPE_A rolled at frame 56 (t≈0.933) — one frame late, ate the bite. Game design moved; the instrument (frozen tape) is what dropped.
- Fix (test-side re-land per FX4/W5; dodge law `rollT>0` at the bite unchanged, `toy.html:169`):
  - `scripts/test_toy.js` TAPE_A re-tuned: roll press 56→46 (roll window 0.767–1.047 covers the 0.90 bite), turn/swings 74/80/102 → 60/74/98 (both riposte swings now connect inside the stun+riposte window; kill at 1.65s). Probe used: `watch/inbox/burn_reset_20260927/queue/Q_020_toy_probe.js`.
  - TAPE_B flip predicate 56→46 (the one-entry flip must still target the roll press; the stale predicate made TAPE_B byte-identical to TAPE_A — caught by lanes 7-8 going red).
  - Re-land comment names cause + evidence in the tape block.
- Proof: `node scripts/test_toy.js` → **15/15**, receipt sha `9a7e7c42e3d7fbf3…`, verdict win, duration 1.65s; lane 9 fork verified (TAPE_A `hit_dodged` vs TAPE_B `hit` at t=0.9).

## Not done / notes

- The other three suites needed no changes: mud replay 41/41 and mud fifty 63/63 first run, frontier 51/51 first run.
- Note for the operator: swarm was browser-breaking since `a5dd96176` (every page load crashed at frame 1) — the boot-lane commit shipped without running `playtest_swarm.js`, which is exactly the drop FW-01 exists to catch.
- Files touched: `dashboard/static/games/swarm.html`, `scripts/test_toy.js` (both committed pathspec with this receipt), probe kept at `watch/inbox/burn_reset_20260927/queue/Q_020_toy_probe.js`.
