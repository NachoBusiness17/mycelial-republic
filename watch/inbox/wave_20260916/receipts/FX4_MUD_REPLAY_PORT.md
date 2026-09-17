# FX4 — MUD replay law port (gen-2 fix, the biggest patch from G1's audit)

- **Date:** 2026-09-16
- **Lane:** wave_20260916 / FX4
- **Target:** `dashboard/static/games/mud.html` (canonical) — 100,832 B / 2,311 lines before, 105,849 B / 2,369 lines after
- **Reference:** `dashboard/static/games/toy.html` seeded LCG (same constants: `Math.imul(lcg, 1664525) + 1013904223`); house pattern per FX1 (`dashboard/static/games/swarm.html`): `startGame(forcedSeed)` auto-seed + `runSeed` recorded
- **Status:** DONE — replay test 11/11 green, fifty-lane gate 51/51 green × 10 consecutive runs (exit 0), syntax OK

## Scope (mission)

Port toy.html's replay law to mud.html: enumerate + classify every Math.random site, add the seeded
LCG + run seed (FX1 house pattern), port every gameplay-affecting site to the seeded stream in a
fixed draw order, prove it with the two falsifiers (same seed + same tape → byte-identical event
log; flip one input → named fork), keep the 51-lane gate green.

## Worklog

- Receipt opened before any edit (wave-lane law).
- Enumeration: 26 Math.random sites (G1's 25 + the draw()-shake pair counted once) classified one by one — table below.
- LCG ported: `seedRun`/`rng` (toy constants) + `rnd`/`rndi` rerouted onto the stream + `crnd` cosmetic escape hatch (swarm house carve-out).
- `startGame(forcedSeed)`: FX1 house auto-seed line verbatim; plus toy `start()` actor-reset law (fresh-run player/weapon/stat/spike/death state) — same seed + same inputs → same run requires the same initial actors. `lore` deliberately NOT reset (the horde learns across runs, by design — machine state, documented in-code).
- 19 direct `rng()` sites + all `rnd`/`rndi`-routed draws ported; cosmetic draws moved OFF the stream (poof → `Math.random`/`crnd`, draw()-shake → `crnd`) so render jitter can never advance the replay stream.
- `evlog`: append-only gameplay event log (18 event kinds), cleared on `startGame`, seed-stamped `run` event records seed + seeded puzzle placement. Exposed on the MUD handle with `runSeed`/`lcg` getters (+ `lootDrops`/`fireZones`/`deathClouds` for harness tracing).
- **INCIDENT:** mid-pass, `mud.html` was externally reverted to pristine (100,832 B, 17:14) between my test run and my next edit — likely another wave process. Re-applied the entire port atomically via an exact-match, abort-on-drift script (33/33 edits), then verified. No git commands used.
- `scripts/test_mud_replay.js` written: 11 lanes, both falsifiers + stream-law + seed-sensitivity guards. First run caught a real port bug (dirty carry-over state across runs) → the actor-reset in `startGame`; second run caught an over-strict lane (cross-seed evlog coincidence is legal — state trace is the load-bearing criterion).
- **GATE FIRE:** fifty-lane gate flaked 4/9 runs (lanes 44/45/48/49, mechanics phase). Root-caused with forced-seed replays + per-step forensics: a stray super-orb (9% kill drop, homing pickup) lights SUPERHOT (`G.super = 4`); the stationary tester then runs world-time at 0.06x and the lanes' fixed-step decay windows (`allies[0].t=0.05` + 5 pumps, orb `life=0.01` + 2 pumps, `mourn=0.05` + 5 pumps) silently stop being long enough. Mechanism is 100% pre-existing game code (nothing in the port touches it); A/B control (LCG swapped for `Math.random`, all else identical) passed 8/8 but is statistically compatible with luck. Fix: one harness affordance — `pump()` now clears `M.G.super` (no lane under test exercises SUPERHOT; same spirit as `god()` already covering walk-through hazards). Gate then passed 10/10.
- Probe/A-B working files deleted; deliverables are `test_mud_replay.js` (new) + the harness robustness fix in `test_mud_fifty.js` + the game port.
- Findings while in file (not fixed, out of scope): (1) stray-orb → SUPERHOT can still poison real fixed-step tooling built like the harness — recorded here so the next harness author uses the `pump()` affordance; (2) `startGame` still does not reset `G.victoryTime` (cosmetic, victory screen only); (3) relay `setInterval(relayTick, 250)` never torn down (already on G1's list, item 10).

## Site classification table (seeded vs cosmetic-allowed)

Original line numbers = G1 audit numbering (pristine file); final = current file. **Seeded** sites
draw from the replay stream; **cosmetic-allowed** sites stay on `Math.random` because they provably
cannot change game state (verified: no mechanic reads the value).

| Site (orig → final line) | What it rolls | Law |
|---|---|---|
| 66 → 74 | `rnd(a,b)` utility — rerouted onto the stream | SEEDED (via rnd) |
| 67 → 76 | `rndi(a,b)` utility — rerouted | SEEDED (via rnd) |
| — → 75 | NEW `crnd(a,b)` cosmetic utility | cosmetic escape hatch |
| 420 → 435 | `genName()` enemy names (×2 draws) | **cosmetic-allowed**: name feeds render label + chronicle text only; no mechanic reads `e.name` |
| 432 → 447 | `ME.id` relay session identity | **cosmetic-allowed**: load-time network identity, outside the run |
| 464 → 479 | `farSpot()` key/chest distance pick | SEEDED — walk-to-it pays 120 souls + loot + SUPERHOT |
| 475 → 490 | `puzzleReset()` key spot | SEEDED — same |
| 540 → 555 | `makeLoot()` rarity roll | SEEDED — weapon rarity/stats (pickup changes player power) |
| 547–551 → (via rnd) | loot prefix/name/dmg/speed/affix | SEEDED (via rnd/rndi) |
| 623 → 639 | spawn name gate (`Math.random() < 0.35`) | **cosmetic-allowed**: gates only `e.name` assignment |
| 624 → 640 | `homeSeed` wander phase | SEEDED — drives idle wander heading → positions → combat |
| 698 → 716 | bell-ringer spawn gate (`< 0.45`) | SEEDED — spawns a runner that prewarns rooms (forceBell short-circuits, no draw) |
| 699 → (via rndi) | bell-ringer spawn spot | SEEDED (via rndi) |
| 758–760 → 779–781 | `poof()` particle angles/speed/life/size | **cosmetic-allowed**: particles render and die, never read back; moved OFF `rnd` to `crnd`/`Math.random` |
| 882 → (via rnd) | swing damage jitter `rnd(0.9,1.1)` | SEEDED (via rnd) |
| 884 → 905 | boonCrit `< 0.2` | SEEDED — double damage |
| 893 → 914 | grudge roll `< 0.25` | SEEDED — speed ×1.15 (genName after it stays cosmetic) |
| 902 → 924 | boonChain `< 0.3` | SEEDED — chain lightning damage |
| 847 → (via rndi) | shout KABUKI line | SEEDED (via rndi; stepped in update, deterministic; text is flavor) |
| 1111 → 1133 | spitter mine lay | SEEDED — floor mines damage both sides |
| 1191 → 1214 | dodger dodge direction `< 0.5` | SEEDED — changes intercept geometry |
| 1222 → 1246 | dragon whelp summon angle | SEEDED — spawn positions |
| 1454 → 1478 | spike phase init (`× 3`) | SEEDED — spike up/down rhythm decides the bite |
| 1574 → 1598 | boon draft weighted roll | SEEDED — which boons the gods offer |
| 1685 → 1711 | loot drop gate `< 0.35` | SEEDED — drop table |
| 1677–78 → (via rnd) | soul orb spawn offset/velocity | SEEDED (via rnd) — orb position sets pickup timing |
| 1722 → 1748 | ghost ally gate `< 0.4` | SEEDED — allies deal real DPS (forceGhost short-circuits, no draw) |
| 1723 → 1749 | ghost render phase `ph` | **cosmetic-allowed**: `ph` feeds render alpha only (L2067) |
| 1728 → 1755 | mourn roll `< 0.45` | SEEDED — mourner rises angry |
| 1752 → 1782 | super orb gate `< 0.09` | SEEDED — SUPERHOT window |
| 1776–77 → 1807–08 | `draw()` camera shake | **cosmetic-allowed**: screen-space translate only; moved OFF `rnd` to `crnd` (swarm house carve-out) |
| 2212 → 2245 | k3 cascade scatter angle | SEEDED — spark spawn positions |

Tally: 25 G1 sites → 18 gameplay sites seeded (19 direct `rng()` + `rnd`/`rndi`-routed draws), 7 draws cosmetic-allowed (names ×3 sites, particles, shake ×2 lines, ghost ph), 1 meta (relay id). `draw()` contains ZERO seeded draws.

## Draw-order note

The stream is advanced only from deterministic contexts, so the draw sequence is a pure function of
(runSeed, input tape):

1. **Seeding order:** `startGame(forcedSeed)` → `seedRun` FIRST, then `puzzleReset` (1 + ≤40 draws:
   key spot, then chest spot retries), then the seed-stamped `run` evlog event. Fresh actor/spike
   state is reset before any world tick, so the first gameplay draw lands at a fixed stream offset.
2. **Sim-only draws:** every seeded draw happens inside `update(dt)` (fixed steps via `pump`/`step`)
   or the constructor-path helpers it calls (`spawnEnemy`, `makeLoot`, `spawnCascade`, `roomTick`,
   `puzzleReset`). Draws execute in code order per step: player attack block (damage jitter → crit →
   grudge → chain), enemy block in `enemies` array order (mine lay, dodge perp, whelp angle, …),
   then traps/spikes, killEnemy chain (loot → ghost → mourn → cascade → superorb), boon draft.
   `draw()` — the render pass — never draws from the stream (crnd/Math.random only), so render
   frequency cannot perturb replay.
3. **Conditional draws are legal:** short-circuit force flags (`forceBell`/`forceGhost`) skip draws;
   looped draws (`farSpot` retries ≤40, boon bag) consume a deterministic count given the same seed
   and state. The event log records the RESULT of each decision, not the draw count.
4. **Verboten:** nothing outside `update`/constructor paths may call `rng()`; render code uses
   `crnd`; the only remaining bare `Math.random` in sim-reachable code is the name pipeline
   (verified uncached by mechanics) — enforced by the `draw()` grep in the receipt check and by
   falsifier 1 (any stream-perturbing leak breaks byte-identity).

## Falsifiers

`scripts/test_mud_replay.js` (new, 11 lanes, toy.html's test pattern + fifty-lane shim): fresh game
instance per replay = page-reload semantics; fixed tape `[step, code, down]` at 60 fps; per-step
sha256 of a whitelisted mechanical-state snapshot (particles/damage numbers/loot beams/chronicle
text/names/ghost-ph/msg-text excluded — all Math.random-fed, none gameplay-read).

- **FALSIFIER 1:** same seed + same tape twice → byte-identical evlog (13 events) AND byte-identical 1800-step state trace.
- **FALSIFIER 2:** one flipped tape entry (`Space` press → `KeyA` press at step 160) → `INPUT_FORK @ step 160 (t=2.667s)`, `STATE_FORK $.p[0]: 333.33 → 329.99`, `EVENT_FORK @ evlog[4]: hurt@6.75 → grudge@6.017`.
- Guards: post-seed stream state is a function of the seed alone; stream advances during play and reseeds; different seed → divergent run (state divergence from step 0, seed-stamped run events).

## Harness outputs (verbatim)

### scripts/test_mud_replay.js

```
    evlog: 13 events over 1800 steps (clear, death, hurt, room, run)
    INPUT_FORK @ step 160 (t=2.667s): Space press -> KeyA press
    STATE_FORK $.p[0]: 333.33333333333303 -> 329.9999999999997
    EVENT_FORK @ evlog[4]: {"t":6.75,"e":"hurt","d":14,"hp":86} -> {"t":6.017,"e":"grudge"}
    first divergence vs alt seed at step 0; evlog run stamps differ, full logs differ
PASS  1 R: game compiles + window.MUD live + startGame(forcedSeed) records runSeed
PASS  2 R: stream law — post-seed LCG state is a function of the seed alone
PASS  3 R: stream law — the LCG advances during play and reseeds on startGame
PASS  4 F1: same seed + same tape twice -> byte-identical event log (evlog)
PASS  5 F1: same seed + same tape twice -> byte-identical state trace (all 1800 step digests)
PASS  6 F1: the run actually lived — event log is non-vacuous (activation + combat/hazard events)
PASS  7 F2: flipped input -> state trace diverges (the tape is load-bearing)
PASS  8 F2: the fork is NAMED at the exact step of the flipped input
PASS  9 F2: event logs diverge too — first differing event named
PASS 10 F2: both forked runs keep their recorded seed — inputs never touch the stream seed
PASS 11 G: different seed + same tape -> different run (the seeded stream is load-bearing)

11/11 lanes green
mud: 2369 lines, seed 20260916, 1800 steps @ 60fps, tape A 13 events, runSeed 20260916
```

### scripts/test_mud_fifty.js (run 1 of 10 consecutive green runs, exit 0)

```
PASS  1 game script compiles + window.MUD live
PASS  2 respawn point is the courtyard bonfire (dup-key bug gone)
PASS  3 d6 opens after crypt (forge is enterable)
PASS  4 d7 gates the nave on forge + 4 sigils
PASS  5 ossuary room registered (queue + drip + spots)
PASS  6 ossuary geometry walks (south pocket is a room, not a void)
PASS  7 dragon will spawn inside the nave, not the forge
PASS  8 P: locked d2 physically blocks (resolve, not just color)
PASS  9 P: d1 walk courtyard→refectory + the door seals behind you
PASS 10 P: refectory drips + clears + pays d2
PASS 11 P: infirmary spawns a bell-ringer (forced)
PASS 12 P: bell-ringer reaches d3 — scriptorium is prepop-warned
PASS 13 P: infirmary champion falls → sigil 1
PASS 14 P: scriptorium prepop room meets you aggroed
PASS 15 P: scriptorium clears → sigil 2
PASS 16 P: crypt — champion walks with a live escort
PASS 17 P: champion dies → wounded escort routs
PASS 18 P: rout feeds the next room (the monastery talks)
PASS 19 P: crypt clears → sigil 3
PASS 20 P: d5 drops into the ossuary (not a dead pocket)
PASS 21 P: ossuary clears (traps and all) — third bonfire nearby
PASS 22 P: d6 walks crypt→forge now that the crypt is paid
PASS 23 P: forge clears → sigil 4
PASS 24 P: d7 unlocks at 4 sigils + forge clear
PASS 25 P: the nave opens and the dragon wakes in the nave
PASS 26 P: dragon phase-2 at half blood (the eye opens)
PASS 27 P: phase-2 tears whelps from its hide
PASS 28 P: perf — heavy room steps under 8ms
PASS 29 P: dragon dies → shatters into 8 whelps
PASS 30 P: a whelp dies → 16 sparks
PASS 31 P: total clear → victory screen
PASS 32 M: cleared room pays souls ONCE, not per frame (AFK farm dead)
PASS 33 M: west flank is a wall now, not a highway
PASS 34 M: bonfire rests once, again only after cooldown, counts fires
PASS 35 M: bear trap bites the player + snare + rearm
PASS 36 M: bear trap bites enemies harder (lure-through works)
PASS 37 M: dart plate shoots whoever hurries over
PASS 38 M: chandelier auto-drops under a crowd of three
PASS 39 M: chandelier drops to a aimed swing and pays out
PASS 40 M: forge vents warn, then burn player and enemy alike
PASS 41 M: doorway spikes run enemies through too
PASS 42 M: the horde mines its own floor — and blows itself up
PASS 43 M: scent trail records while you move
PASS 44 M: a blind horde follows your fresh scent (swarm-steal)
PASS 45 M: riposte kills raise grateful ghosts (swarm-steal)
PASS 46 M: the shout knocks back, interrupts windups, and wakes the room
PASS 47 M: soul orbs skitter from a loud approach (swarm-steal)
PASS 48 M: super orbs expire instead of littering forever
PASS 49 M: grief — a kill makes nearby idle allies keen, then come for you
PASS 50 M: corpses stay in the floor
PASS 51 M: fuse replaces the champion (no double boss)

51/51 lanes green
```

Gate stability: 10 consecutive full runs after the SUPERHOT affordance fix — `exit=0 51/51` × 10.
(Pre-fix LCG build flaked 4/9 on lanes 44/45/48/49; A/B Math.random control 8/8 — mechanism and fix
documented in the worklog. The port itself preserves every probability exactly.)

## Files touched

- `dashboard/static/games/mud.html` — the port (LCG + forcedSeed + actor reset + 18-seed-site port + evlog + MUD handle getters)
- `scripts/test_mud_replay.js` — NEW: the two falsifiers + guard lanes
- `scripts/test_mud_fifty.js` — one robustness fix: `pump()` clears `M.G.super` (comment documents why)
- `watch/inbox/wave_20260916/receipts/FX4_MUD_REPLAY_PORT.md` — this receipt
