---
name: games-infra-shader-audit-20260916
description: Operator order — complete audit + rewrite of all HTML games, the
  entire static infrastructure, and shaders; G1/G2/G3 audits LANDED, gen-2 fix
  lanes FX1/FX2/FX3 landed, V1 auditions 7/8 byte-verified; mud replay-law port queued
metadata:
  node_type: memory
  type: project
  originSessionId: sess_f8f2909b-0ac5-4763-abba-fbd8ba748f54
---

2026-09-16 night, operator: "Keep iterating on a warmed rib per ask and build momentum and
start generating our build... do a complete audit and rewrite of our HTML games debugging
and fixing as well as our entire static infrastructure and shaders." Two laws in the order:
(1) WARMED RIB PER ASK — every lane gets the warmed context pack, iteration compounds;
(2) momentum = audits feed fix lanes the same window.

## Audit findings (all landed)

- **G1 games** (7 games in dashboard/static/games/): all four harnesses green (mud 51/51,
  frontier 42/42, toy 12/12, swarm dogfood 32/32), zero syntax errors, zero dead ids — but
  6 of 7 games violate the replay law (96 unseeded Math.random sites; only toy.html
  complies), one FATAL (swarm bare localStorage dies in privacy mode), swarm audio 404s
  where deployed, duplicate-surface rot (static/ stale copies, mud diverged 31KB vs 100KB,
  playtest_swarm tested the stale copy, vislab catalog stale). Verdict: everything is PATCH,
  nothing needed a rewrite.
- **G2 static infra** (105 MB / 553 files / 159 HTML): INDEX graded F — 388 unindexed
  inbox files, 84 dead pointers, 13 hash mismatches, wrong root (highest-leverage fix,
  now Hermes' seeded directive H1). Estate pair diverged (main walk 144 commits vs LOD
  201). Root hygiene D (bak litter, .mimosa in served tree, 9.8MB raw JSONL at static
  root). Broken refs: zero real hits. :8765 is the docker-forwarded OpenClaw board, not
  host lab; served bytes match disk + a constant unexplained 756 B overhead.
- **G3 shaders** (24 sites/~30 programs): 2 blockers + cheap wins, ALL FIXED in FX3 —
  pipeline.html CARBPM ReferenceError froze every cartridge after frame 1; rings cartridge
  root cause was the manifest PROSE recording the wrong uniform name (docs that lie are
  runtime bugs); uniform fetches (uBPM/uSeed/iFrame) added; wipeout min(src.z,src.z) typo
  fixed in both copies; arena_operator_field WebGL guard added. KEY FINDING: the operator's
  belt-trick lattice is NOT a shader — Three.js scene in a worktree, Lipschitz march exists
  only as prose in lanes/elder.md, and wipeout's wobble violates the bound
  ([[belt-trick-shader-parable]]). Implementation design task queued, not a patch.

## Gen-2 fixes (landed)

- **FX1 swarm**: SAFE_STORE kills the FATAL (zero bare localStorage), audio walks both
  bases then procedural fallback, 13 gameplay RNG sites seeded on toy.html's LCG (cosmetic
  noise deliberately off the replay stream), 32/32 twice, harness retargeted to canonical.
- **FX2 surface reconcile**: mud divergence reconciled from canonical; ROOT CAUSE fixed —
  site/build.py GAMES list was missing toy.html + frontier_souls.html (frontier's dist
  copy was an untracked manual relic the next rebuild would have destroyed); vislab
  catalog regenerated (5→7 entries, sha-verified); playtest_swarm retargeted; rode out a
  concurrent-writer race with FX1 by waiting for settle (timing races between lanes are
  the new failure class — freeze before audit).
- **FX3 shaders**: the 5 fixes above; residuals queued (QUEUED manifest entries = dead
  deck cards, $('day') hardcoded '14', wipeout wobble).
- **FX4 MUD REPLAY-LAW PORT LANDED** (the biggest patch): 18 gameplay sites seeded on
  toy's exact LCG (`startGame(forcedSeed)` auto-seed + `runSeed` recorded), 7 cosmetic
  sites deliberately left unseeded with per-site justifications (render noise must never
  advance the replay stream); new `scripts/test_mud_replay.js` 11/11 — both falsifiers
  pass (same seed+tape → byte-identical evlog AND byte-identical 1800-step state trace;
  one flipped input → `INPUT_FORK @ step 160` / `STATE_FORK` / `EVENT_FORK`). Falsifier-
  caught bug: run 2 inherited run 1's corpse position (actor-reset law added). Incidents
  filed: an external revert mid-pass (re-applied via exact-match abort-on-drift script,
  33/33) and a 51-lane gate flake root-caused to a 9% super-orb drop triggering SUPERHOT
  time dilation inside fixed-step test windows — harness affordance `pump()` clears `M.G.super`,
  then 51/51 ten consecutive runs. Replay law now covers toy, swarm, mud; frontier (21),
  maze_arena (10), arrakis (7), arena (2) queue behind. Belt-trick GLSL implementation
  design also queued (see [[coldest-vertex-wave-20260916]] CV5).

## Auditions (V1) — 7/8 byte-verified green

Every suite re-run cold from a fresh vantage matched its receipt (session runner 11,
adapter 17, hydro sim 15, player ledger 17, link library 24, regression trio 24, toy.js
12/12 with sha match). The one red: wow_world.py was live-edited by its own lane
mid-audit — freeze the tree before claiming/auditing. Evidence hygiene: hydro receipt
lives in physical_computing/receipts (program-scoped), not wave receipts — scope folders
matter to auditors.

## Consumers landed (N-wave, 2026-09-16 late)

- **N9 boon draft (mud.html):** of HG2's 3 claimed bugs only 1/3 was live — the max-law
  was INVERTED (stack-designed boons could never repeat; fixed with `max: 3` + pool filter
  `(taken[b.id]||0) < (b.max||1)`), pick-swap fall-through already guarded (hardened
  structurally), mines-superhot already compliant (verified by probe: 0.06s decay in a
  1.0s window — pinned as a regression lane instead of "fixed"). 5 new BD replay lanes;
  replay 16/16, gate 58/58. Lesson: even the mining lanes' findings get byte-checked —
  2 of 3 claims dissolved.
- **N10 puzzle vault CONSUMED:** the gate was IMAGINARY — machinery looked for
  `gate: true`, no wall ever carried it; plate II was unreachable inside a sealed pocket;
  zero lanes collected the payout. Fixed: south band wall tagged `gate:true`, plate II
  moved to the forge floor, chest pinned in the pocket; human route = key → infirmary
  plate → forge plate → gate grinds → 120 souls + full heal + weapon + super orb.
  7 new harness lanes; gate 58/58 ×5 consecutive runs.
- **N11 estate LOD/relay CONSUMED:** deck WORLD card probes `GET /mud/state` live
  (players, lantern age, graceful OFFLINE with start command — 16/16 checks incl. port
  squat + timeout); escape-bug fixed (backslash escapes corrupting a JS path in a string
  literal). Relay found NOT running (:8766 squatted by the cast server) — noted, not
  started per lane law.

Related: [[coldest-vertex-wave-20260916]], [[research-wave-20260916]],
[[gaming-weave-20260916]].
