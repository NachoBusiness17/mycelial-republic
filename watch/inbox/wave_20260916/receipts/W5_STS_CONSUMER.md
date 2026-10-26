# W5 — StS Ascension Consumer (R2 dogfood-orphan consumption)

Lane: W5 · Date: 2026-09-16 · Repo: local_sovereign_agent
Mission: give mud.html's Slay-the-Spire-style Ascension system its first consumer.

## Log (append as you go)

- [started] Receipt filed first per wave-lane law. Locating StS Ascension code in `dashboard/static/mud.html` and harness at `scripts/test_mud_replay.js`.
- [found] Ascension lives in `dashboard/static/games/mud.html` (CANONICAL; `dashboard/static/mud.html` is the G1-flagged stale divergent copy — not wired here). Mechanics: `G.ng` (init 0), `spawnEnemy` + `spawnBoss` scale hp `1+a*0.15+ng*0.05` / dmg `1+a*0.22+ng*0.08` (a=min(ng,20)), `spawnCascade` counts 8+a whelps / 16+2a sparks. Persisted at `localStorage['mud_asc']`.
- [root cause] The only RAISE path is `nextLoop()` — reachable solely from a hand-pressed KeyR on the victory screen; the only CONSUME path is `startGame()` reading browser `localStorage['mud_asc']`, which every harness boot nulls (fresh shim, `getItem: () => null`). No lane/tile/session ever touches either. Ladder is hand-playable, machine-invisible.
- [wired] games/mud.html (pre-rollback): (a) boot-load `mud_asc` into `G.ng` after the G literal (title UI can show it); (b) title screen prints `ASCENSION N — the dragon remembers you` when ng>0; (c) victory gate calls `ascendForNextRun()` (persists ng+1) + evlog `victory` receipt — winning alone raises the NEXT run; (d) `startGame(forcedSeed, forcedAsc)` — optional asc pins the ladder for replays (seed + ascension = run identity), run receipt stamps `asc: G.ng`; (e) `persistAsc`/`ascendForNextRun` helpers, nextLoop refactored onto persistAsc (behavior-identical), both exposed on window.MUD (+`spawnBoss` test hook); (f) no bare Math.random touched — difficulty flows through the deterministic ng-multipliers only.
- [harness] `scripts/test_mud_replay.js`: 7 ASC lanes landed (survived the rollback — scripts/ not hit by the sync). Laws pinned: ascended replay identity; asc 0 vs 1 harder-by-formula; cap math (R2's falsifier); victory→persist→fresh-boot round-trip incl. title state; no-double-bump; ascension-is-a-dial-not-a-reseed (identical runSeed + puzzle placement); start-UI boot visibility. Plus `loadGame(storage)` param + `makeStorage` recording shim (the FLT lane built on the storage param — compatible).
- [GREEN pre-rollback] `node scripts/test_mud_replay.js` → **24/24 lanes green** (all 7 ASC PASS; R/F1/F2/G/BD + N12 LOOT lanes untouched-green). `node scripts/test_mud_fifty.js` → **63/63 lanes green** (after one export fix: `get lootBeams()` was missing from window.MUD — the N12 lane's cleanup line `M.lootBeams.length = 0` threw; pre-existing latent bug, not W5's, fixed with one export).
- [findings for W2] The bones lane's `tomb` evlog event carried `c: player.lastHit` — the killer's cosmetic Math.random name (grudge path `genName()`, FX4-classified cosmetic-allowed). At asc 0 TAPE_A killers stay unnamed (F1 passed); at asc 1 walkers survive 2 hits → grudge-named → tomb nondeterministic → F1 law broken ("Zugl" vs "Uvash Gravewhisper"). Recommendation: evlog `tomb` should carry a deterministic cause kind (e.g. `src.type`); flavor name belongs in `bonesWrite` machine state only.
- [INCIDENT — rollback hit landed work] At ~22:47, AFTER all gates ran green, `dashboard/static/games/mud.html` was externally reverted to the pristine 17:14-vintage baseline (100,832 B / 2,311 lines, no FX4 seedRun/evlog/lcg, no fleet/bones/N12/W5 wiring; `site/dist/games/mud.html` rolled in lockstep — identical bytes + identical mtime 17:14:03.590647800). This is the SAME incident FX4 documented mid-pass today and W1A is currently blocked on ("No FX4-era copy of mud.html exists anywhere on disk"; toy re-rolled once mid-flight too). Per W1A's precedent, W5 does NOT re-apply onto pristine (would fork a new divergent vintage and break FX4's exact-match atomic re-apply). Game-side patch is STAGED below; harness side is LANDED.
- [post-rollback probe] `node scripts/test_mud_replay.js` vs pristine → module-level crash in `snap()` at `M.lootDrops.map` (lootDrops getter is FX4's; absent on pristine) — expected, captured as incident evidence. Fifty-lane gate not meaningful vs pristine (seed-law lanes would fail).
- [re-land procedure] When the FX4-era mud.html returns, apply the 6 staged hunks below (exact-match anchors are FX4-era bytes), then run both gates. Expected: 24/24 + 63/63 as captured pre-rollback.
- [23:04 update] A new vintage landed at 23:04:47 (101,844 B): pristine + W1A fleet-seed law (`FLEET_DATE`/`FLEET_SEED`/`fleetSeedOf`, exports carry fleet getters), with an in-file staging note at L66-70: "STAGED on this vintage: the FX4 replay LCG (seedRun/runSeed + startGame(forcedSeed) wiring) is re-landing via the FX4/W5 restore". W5 holds its hunks for that restore — landing them on the current vintage would drift FX4's exact-match abort-on-drift anchors (startGame signature, victory gate are both FX4-anchored regions). W5's harness side remains landed and waiting; both green gate captures above are the acceptance evidence for the moment the restore lands.

## Root cause

The StS ascension ladder's only RAISE path was a hand-pressed KeyR on the victory screen (`nextLoop()`), and its only CONSUME path was a browser-`localStorage['mud_asc']` read in `startGame()` — a read every harness boot nulls (fresh storage shim) and no lane, tile, or session ever fed: the endgame difficulty loop was hand-playable but machine-invisible (R2 orphan #2).

## Wiring diff summary

Six hunks in `dashboard/static/games/mud.html` (STAGED — see INCIDENT; harness side LANDED):

1. Boot-load (after the `const G = {...};` literal):
```js
// StS ascension (W5 consumer): boot-load the persisted ladder so the title screen shows the
// ascension level before any run starts (startGame re-reads it; nextLoop/victory keep it fresh).
try { G.ng = Math.max(0, parseInt(localStorage.getItem('mud_asc') || '0', 10) || 0); } catch (e) {}
```
2. Victory gate — after `G.victoryTime = G.time;`:
```js
    ascendForNextRun();   // StS-steal (W5): winning a run raises the ladder — the NEXT run starts ascended
    evlog.push(Object.assign(evt(), { e: 'victory', ng: G.ng, nextAsc: G.ng + 1 }));   // replay receipt: ascension unlock
```
3. Title screen — after the `'press any key'` fillText:
```js
    if (G.ng > 0) {
      ctx.font = '16px monospace';
      ctx.fillStyle = '#f84';
      ctx.fillText('ASCENSION ' + Math.min(G.ng, 20) + ' — the dragon remembers you', BASE_W/2, BASE_H/2 + 45);
    }
```
4. `startGame` signature + ladder source + receipt stamp:
```js
function startGame(forcedSeed, forcedAsc) {
```
and replace the bare `try { G.ng = ...localStorage.getItem('mud_asc')... } catch (e) {}` with:
```js
  if (forcedAsc !== undefined) G.ng = Math.max(0, forcedAsc | 0);   // replay pin: seed + ascension = run identity
  else try { G.ng = Math.max(0, parseInt(localStorage.getItem('mud_asc') || '0', 10) || 0); } catch (e) {}
```
and the run receipt gains `asc: G.ng`:
```js
  evlog.push({ t: 0, e: 'run', seed: runSeed, asc: G.ng, key: ..., chest: ... });
```
5. Persistence helpers + nextLoop refactor (behavior-identical; both paths write the same value → no double-bump):
```js
function persistAsc(v) { try { localStorage.setItem('mud_asc', String(v)); } catch (e) {} }
function ascendForNextRun() { persistAsc(G.ng + 1); }
function nextLoop() {
  G.ng++;
  persistAsc(G.ng);
```
6. Exports: `nextLoop, ascendForNextRun, persistAsc, spawnEnemy, spawnBoss,` added to window.MUD (`spawnBoss` = test hook; the lootBeams getter fix for N12's lane is also staged: `get lootDrops() { return lootDrops; }, get lootBeams() { return lootBeams; },`).

Consumer semantics after wiring: win → `mud_asc = ng+1` persisted → any later fresh boot (browser or harness shim) starts ASCENDED, title shows the ladder, `startGame(seed, asc)` pins it for replays; KeyR's `nextLoop()` keeps identical in-session semantics; difficulty moves only through the deterministic ng-multipliers inside the seeded stream (same seed, different asc → same puzzle placement, strictly tougher horde).

## Harness outputs

PRE-ROLLBACK (both captured verbatim from this lane's runs tonight):

`node scripts/test_mud_replay.js` (includes the 7 new ASC lanes):
```
    asc 0->1 @ seed 20260916: walker hp 40 -> 48, dmg 14.0 -> 18.2; boss hp 500 -> 600; first run divergence @ step 0
    ng=20 (a capped): walker hp 200 (want 200), dmg 98.0 (want 98.0)
    win @ asc 2 -> mud_asc=3 -> fresh boot: title G.ng=3, walker hp 64 (want 64), run receipt asc=3
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
PASS 12 BD: draft offers are seeded — same seed + same level-up presses -> identical offer sequence
PASS 13 BD: offers are legal — known ids only, at most 3 cards, no duplicate within one offer
PASS 14 BD: max law — stackables re-offer below max, and a maxed boon leaves the offered pool
PASS 15 BD: picking a boon never swaps the weapon (both digit paths, with a live-swap control)
PASS 16 BD: mines dilate under SUPERHOT with the rest of the world (idle 0.06x law)
PASS 17 LOOT: pickup -> inventory-add -> inventory-use replays byte-identical (the N12 consumer loop)
PASS 18 ASC: replay law holds at ascension — same seed + same tape + asc=1 twice -> identical trace + evlog
PASS 19 ASC: ascension 0 vs 1, same seed -> deterministically different AND harder (ladder formula)
PASS 20 ASC: ladder math at the cap — G.ng=20 -> walker hp/dmg exactly on the StS-steal formula (R2 falsifier)
PASS 21 ASC: victory consumer — a win persists ng+1; a fresh boot reads it back and spawns ascended
PASS 22 ASC: no double-bump — victory persist then the KeyR nextLoop keeps the ladder at ng+1
PASS 23 ASC: ascension is a difficulty dial, not a reseed — same seed, asc 0 vs 1 -> identical stream + placement
PASS 24 ASC: start UI — a persisted ladder is live on the title screen before any run starts

24/24 lanes green
mud: 2402 lines, seed 20260916, 1800 steps @ 60fps, tape A 13 events, runSeed 20260916
```
(one earlier 23/24 run exposed the tomb-name nondeterminism described in [findings for W2]; after the lootBeams export fix and with the tomb event present, the asc-0 pair still matched — the asc-1 pair's divergence is named in the findings entry.)

`node scripts/test_mud_fifty.js` (the mud gate, grown to 63 lanes by V/N12/L lanes):
```
PASS 58 V: the vault pays — 120 souls + full heal + weapon row + sliver of time
PASS 59 L: the loot table rolls through the seeded stream (same seed -> same rarity sequence)
PASS 60 L: walk-over pickup equips a better weapon — stats move into the slot (add: equip branch)
PASS 61 L: a drop under the active slot is STORED in the free one; trash under both is DISCARDED
PASS 62 L: the swap keys are the use-path — Digit2/Digit1 wield the slots
PASS 63 L: kill-drops draw the same stream — same seed, same kills, same drop outcome

63/63 lanes green
```
(pre-fix run was 62/63 with lane 59 RED on the missing `lootBeams` export — latent N12-lane bug, fixed by W5 with one getter.)

POST-ROLLBACK incident probe (vs pristine 17:14-vintage game):
```
C:\...\scripts\test_mud_replay.js:175
    lo: M.lootDrops.map(l => [l.x, l.y, l.w.name, l.w.dmg, l.w.speed, l.w.rarity]),
                    ^
TypeError: Cannot read properties of undefined (reading 'map')
```
— expected: the pristine file predates FX4 (`lootDrops`/`runSeed`/`evlog`/`seedRun` all absent). Blocks every replay-harness lane, not just ASC.

## Orphan status

**CONSUMED** — qualified by the wave rollback incident. The R2 orphan #2 (StS ascension: no consumer) received its first consumers tonight and the full chain was verified green in bytes: victory → `ascendForNextRun()` → `mud_asc` persisted → fresh boot/title read it back → ascended spawns via the deterministic ladder formula → `startGame(seed, asc)` replay pin → 7 asserting lanes landed in `scripts/test_mud_replay.js` (24/24 green) + mud gate 63/63 green. The wave file-sync then rolled `games/mud.html` back to the 17:14 pristine vintage (the same incident FX4 and W1A recorded); per W1A's precedent the game-side hunks are STAGED above for atomic re-land the moment the FX4-era file returns, the harness side is LANDED, and the pre-rollback green outputs above are the proof bytes. Escalation: the mud canonical file needs FX4's port re-landed (or the 17:14 sync source fixed) before ANY mud game-side work can persist — third documented occurrence today.

*Receipt closed 2026-09-16. Bytes: dashboard/static/games/mud.html (staged hunks; landed pre-rollback then rolled back by the wave sync), scripts/test_mud_replay.js (7 ASC lanes + loadGame(storage)/makeStorage/replay-asc — LANDED), watch/inbox/wave_20260916/receipts/{FX4_MUD_REPLAY_PORT,W1A_SHARED_SEED,W2_MUD_BONES_FILES,R2_GAME_SUBSYSTEM_GAPS}.md. No git commands used. No paid APIs used.*
