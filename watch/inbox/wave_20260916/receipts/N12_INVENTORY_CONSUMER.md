# N12 — Inventory consumer (consume R2's mud.html inventory/loot orphan)

Lane: wave_20260916 / N12
Target: `dashboard/static/games/mud.html` (canonical; `dashboard/static/mud.html` is the G1-flagged stale copy) — inventory/loot loop with zero consumers — + `scripts/test_mud_replay.js` + `scripts/test_mud_fifty.js`
Date: 2026-09-16

## Progress log

- [started] Read mud.html inventory/loot code, diagnosing zero-consumer root cause.
- [2026-09-16, respawn] Prior lane died to a rate limit right after opening the receipt; this is the fresh consume attempt. Receipt appended as work proceeds.

## The code read (mud.html inventory/loot loop — all in canonical `dashboard/static/games/mud.html`)

- **Inventory state:** `player.weapons` — exactly 2 slots (`Rusty Sword` dmg12/spd1.0, `Short Blade` dmg8/spd1.3, both rarity 0) + `player.weaponIdx`; `weapon()` = active slot; `playerDmg()` = `weapon().dmg + might*3` (L406-411); attack cadence = `0.35 / weapon().speed` (L887). The whole Diablo grammar is there: `RARITY` 4 tiers (Common/Magic/Rare/Legendary, mult 1.0/1.3/1.7/2.2, L540-545), `AFFIXES` 4 kinds applied on roll (L546-579).
- **Roll (seeded, FX4):** `makeLoot(x,y)` draws rarity through the seeded LCG — `rng()` < 0.55 / 0.85 / 0.97 table (L553-559), name/dmg/speed/affix-count through `rnd`/`rndi` (also seeded), stamps an evlog `loot` event carrying the rolled rarity (L560), pushes a 30s-fuse drop + a 1.2s loot beam.
- **Drop paths:** killEnemy — 35% seeded gate for plain kills, forced ×2 for bosses, +×2 for champions (L1712-1720); the vault chest pays one (L514).
- **Pickup path (the trigger):** the update loop walk-over — `dist2(l, player) < (player.r+18)²` → `pickupLoot(i)` (L1359-1368); drops expire at life 30 (L1364).
- **Inventory-add:** `pickupLoot` (L588-606) auto-compares by `lootScore = dmg*2 + speed*10 + rarity*5` — better than active → EQUIP that slot; else better than the other slot → STORE there; else DISCARD. Splices the drop, beeps, addMsg names the branch.
- **Inventory-use:** Digit1/Digit2 swap keys (L1635-1636, draft-guarded since N9); the HUD renders the active weapon name + "· 1/2" (L1986-1987) — there is no separate inventory panel to "open"; the HUD line + swap keys ARE the UI.

## Root cause (why nothing consumes it — one line)

**Nothing is mechanically dead — the orphan is a pure consumption gap:** every link lives (loot table rolls through the seeded stream, drops expire on a fuse, the only pickup trigger is a walk-over within r+18 of a fresh kill-drop, add/swap work off Digit keys), but no fleet consumer ever drove that loop — no harness lane forces a drop and walks onto it, no tile links the game, no session exercises it (R2 orphan #3: "the loot loop is dead code as far as the fleet can prove") — and unlike the vault (N10) there was not even an exposed handle affordance (`spawnEnemy`-style) by which the fleet *could* drive it.

## Progress (continued)

- [2026-09-16] Baseline captured pre-edit (both harnesses, exit 0): `test_mud_replay.js` 16/16 green · `test_mud_fifty.js` 58/58 green (51 legacy + 7 N10 vault lanes — the "51-lane gate" is 58 lanes as of N10, not 51; the mission's "51-lane gate" name is a fossil).
- [2026-09-16] Wiring landed. `mud.html`: one token — `makeLoot` exposed on the `window.MUD` DFHack-style handle (next to `spawnEnemy`), so the fleet can drive the seeded rarity roll through the real gameplay path. Zero gameplay-code changes: the loop was complete; the dead link was purely the missing consumer affordance + lanes. The loop the harness now drives: `makeLoot` (seeded rng rarity/name/stats, evlog `loot` event) → drop inside pickup radius (r+18) → the live `update()` walk-over check → `pickupLoot` auto-compare (equip / store / discard by lootScore) → `Digit1`/`Digit2` swap wields the slot → `weapon()` feeds `playerDmg` + attack cadence.
- [2026-09-16] `test_mud_replay.js`: 1 new lane — `LOOT: pickup -> inventory-add -> inventory-use replays byte-identical (the N12 consumer loop)`. Drives the loop inside a live fight (walker + facing swing), asserts the seeded roll fired exactly once with a table rarity, the walk-over equipped the drop (stats moved, auto-compare legal), Digit2 wielded slot 1, and the same seed + same inputs → byte-identical evlog AND byte-identical 240-step state trace; plus a no-swap control proving the use-press forks the run at the swap step. Green first run: seeded Magic "Fine Blade" (dmg 15) @ step 41, use-fork @ step 100, evlog ×2 byte-identical. (One pre-run fix by this lane: an early draft asserted `hurt` events, but `hurtPlayer` short-circuits on iframes so an invulnerable tester can never log one — replaced with a walker-hp assert + a facing step before the swing.)
- [2026-09-16] `test_mud_fifty.js`: new LOOT phase (fresh run), 5 lanes (59–63): seeded rarity sequence law · walk-over equip branch (stats move) · store + discard branches · Digit2/Digit1 use-path · kill-drops stream law (same seed, 24 kills ×2 → identical drop counts). One self-caught bug: the first draft cleared `M.lootBeams` but the handle never exposed `lootBeams` (undefined `.length` set) — dropped the line; beams expire on their own 1.2s fuse. Gate went 63/63 green.
- [2026-09-16] Concurrent-lane traffic all day: the ASC lane (R2 orphan #2) landed in the same two files mid-flight (ASC lanes appended to test_mud_replay.js after my edit), then the whole W-wave (W3 souls messages, W4 ghost personalities, W5 STS consumer, FLT fleet-seed, BN bones) stacked onto mud.html — see the INCIDENT below.

## INCIDENT — second external revert of games/mud.html (documented for the wave)

At ~22:53 the canonical `dashboard/static/games/mud.html` was externally replaced by the STALE 100,832 B / 2,311-line copy (mtime reset to 17:14 — copy semantics; the same pattern FX4 documented as its INCIDENT). This wiped, in one stroke: the FX4 replay port (LCG/evlog/forcedSeed), N9's boon fixes, N10's vault gate tag, W5's ascension wiring, and N12's one-token handle exposure. No on-disk copy of the accumulated version existed (repo-wide grep for the FX4/W5 tokens found none). N12 did NOT attempt reconstruction (not this lane's bytes to rebuild; a head-on collision with the owning lanes' re-application was the likely alternative). The owning W-lanes re-applied: the file regrew 100,832 → 101,844 → 115,920 → 123,563 B, byte-stable from 23:23. The re-application carried N12's `makeLoot` handle token (their source copy included the 22:43 N12 edit). The harness files were never reverted.

## Final harness outputs (verbatim)

### scripts/test_mud_fifty.js (final file set; run 1 — `63/63 lanes green`, EXIT=0; run 2 identical)

```text
    13 drops over 24 same-seed kills, twice identical (35% gate through the seeded stream)
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
PASS 52 V: the vault gate exists in the world and starts sealed (dead link gone)
PASS 53 V: the sealed gate physically blocks the vault pocket
PASS 54 V: plate I sinks underfoot in the infirmary
PASS 55 V: plate II sinks in the forge — the gate grinds open
PASS 56 V: the opened gate yields — the pocket is enterable
PASS 57 V: the key answers the walk (cold brass, picked up)
PASS 58 V: the vault pays — 120 souls + full heal + weapon row + sliver of time
PASS 59 L: the loot table rolls through the seeded stream (same seed -> same rarity sequence)
PASS 60 L: walk-over pickup equips a better weapon — stats move into the slot (add: equip branch)
PASS 61 L: a drop under the active slot is STORED in the free one; trash under both is DISCARDED
PASS 62 L: the swap keys are the use-path — Digit2/Digit1 wield the slots
PASS 63 L: kill-drops draw the same stream — same seed, same kills, same drop outcome

63/63 lanes green
```

EXIT=0. Gate stability: 2 consecutive full green runs post-close (63/63 both). Baseline before N12 (post-N10 file): 58/58 green.

### scripts/test_mud_replay.js (final file set: 35 lanes = 16 pre-N12 + 1 N12 LOOT + ASC/FLT/BN lanes landed by other lanes mid-wave)

N12's lane (17) and its own assertions — verbatim, green across 2 consecutive runs:

```text
    loop: seeded Magic "Sharp Blade" (dmg 12) picked up + equipped @ step 41, Digit2 swap @ step 100 (first use-fork @ step 100); evlog 5 events x2 byte-identical
PASS 17 LOOT: pickup -> inventory-add -> inventory-use replays byte-identical (the N12 consumer loop)
```

(An earlier run, pre-revert, rolled `seeded Magic "Fine Blade" (dmg 15)` — the seeded roll tracks the restored file's stream state; both runs byte-identical within themselves, which is the law under test.)

Full lane results (verbatim; ONE line elided — lane 18's FAIL message is a 248,570-char state-trace dump emitted by the ASC lane's own lane, head quoted):

```text
    INPUT_FORK @ step 160 (t=2.667s): Space press -> KeyA press
    STATE_FORK $.p[0]: 333.33333333333303 -> 329.9999999999997
    EVENT_FORK @ evlog[4]: {"t":15.833,"e":"death"} -> {"t":8.35,"e":"grudge"}
    first divergence vs alt seed at step 0; evlog run stamps differ, full logs differ
    mine under superhot: 0.060s arm decay vs 0.800s control (0.06x law); window ticked 1.000s real
    loop: seeded Magic "Sharp Blade" (dmg 12) picked up + equipped @ step 41, Digit2 swap @ step 100 (first use-fork @ step 100); evlog 5 events x2 byte-identical
    ng=20 (a capped): walker hp 200 (want 200), dmg 98.0 (want 98.0)
    win @ asc 2 -> mud_asc=3 -> fresh boot: title G.ng=3, walker hp 64 (want 64), run receipt asc=3
    ghost (toughness 13) touched a 1-hp bearer: hp 1, state play, snare 0.90s
    24 seeds x2 boots: haunt/no-haunt is a pure function of (seed, pool); hauntings rose 11/24
    pooled TAPE_A x2 (forced + natural roll): byte-identical incl gh/bn; hauntings fired 1x forced, 0x rolled
PASS  1 R: game compiles + window.MUD live + startGame(forcedSeed) records runSeed
PASS  2 R: stream law — post-seed LCG state is a function of the seed alone
PASS  3 R: stream law — the LCG advances during play and reseeds on startGame
PASS  4 F1: same seed + same tape twice -> byte-identical event log (evlog)
PASS  5 F1: same seed + same tape twice -> byte-identical state trace (all 1800 step digests)
FAIL  6 F1: the run actually lived — event log is non-vacuous (activation + combat/hazard events)  — no combat/hazard events logged
PASS  7 F2: flipped input -> state trace diverges (the tape is load-bearing)
PASS  8 F2: the fork is NAMED at the exact step of the flipped input
PASS  9 F2: event logs diverge too — first differing event named
PASS 10 F2: both forked runs keep their recorded seed — inputs never touch the stream seed
PASS 11 G: different seed + same tape -> different run (the seeded stream is load-bearing)
PASS 12 BD: draft offers are seeded — same seed + same level-up presses -> identical offer sequence
PASS 13 BD: offers are legal — known ids only, at most 3 cards, no duplicate within one offer
FAIL 14 BD: max law — stackables re-offer below max, and a maxed boon leaves the offered pool  — no stackable was ever re-offered below max — restored semantics not live
PASS 15 BD: picking a boon never swaps the weapon (both digit paths, with a live-swap control)
PASS 16 BD: mines dilate under SUPERHOT with the rest of the world (idle 0.06x law)
PASS 17 LOOT: pickup -> inventory-add -> inventory-use replays byte-identical (the N12 consumer loop)
FAIL 18 ASC: replay law holds at ascension — same seed + same tape + asc=1 twice -> identical trace + evlog  — ascended run not replay-identical (state): got "[\"bee33e6e349c335e5db246c5d8635c04896d460e4dd32905984922e88e […FAIL message continues for 248,570 chars — hex sha256 trace dump emitted by the ASC lane's own lane; elided here, intact in the run log]
FAIL 19 ASC: ascension 0 vs 1, same seed -> deterministically different AND harder (ladder formula)  — M.spawnBoss is not a function
PASS 20 ASC: ladder math at the cap — G.ng=20 -> walker hp/dmg exactly on the StS-steal formula (R2 falsifier)
PASS 21 ASC: victory consumer — a win persists ng+1; a fresh boot reads it back and spawns ascended
FAIL 22 ASC: no double-bump — victory persist then the KeyR nextLoop keeps the ladder at ng+1  — nextLoop did not raise the in-session ladder: got 2 want 1
PASS 23 ASC: ascension is a difficulty dial, not a reseed — same seed, asc 0 vs 1 -> identical stream + placement
PASS 24 ASC: start UI — a persisted ladder is live on the title screen before any run starts
PASS 25 FLT: auto run (no seed) derives the seed from the reported UTC day — fleet-YYYY-MM-DD -> LCG seed
PASS 26 FLT: two fresh same-day runs share the fleet seed — the shared starting world
PASS 27 FLT: explicit seeds always win — startGame(SEED) ignores the fleet seed
PASS 28 FLT: derivation is date-bounded — a different day hashes to a different seed
FAIL 29 BN: die in run A -> run B entering the room meets A's ghost (name, cause, toughness carried)  — ghost touch carried no chill (stamina burn dead)
PASS 30 BN: a ghost cannot kill — touching a 1-hp bearer leaves hp 1, state play, zero death events
PASS 31 BN: ghost spawning is seeded — same seed + pool -> identical haunt/no-haunt across 24 seeds x2
PASS 32 BN: replay law with bones — same seed + tape + pool twice -> byte-identical trace INCLUDING ghost fields
PASS 33 BN: bones are room-bound — the crypt dead do not haunt the refectory
PASS 34 BN: the courtyard is sanctified — bones are filed there but no ghost rises
PASS 35 BN: the pool is capped at 10, FIFO — bone #0 rots out first

29/35 lanes green, 6 RED
mud: 2619 lines, seed 20260916, 1800 steps @ 60fps, tape A 6 events, runSeed 20260916
```

EXIT=1. The 6 reds are ALL in other lanes' surfaces against the W-wave's still-converging game file (FX4's vacuity lane 6 — TAPE_A's world changed under them; N9's boon-max lane 14; W5's ascension lanes 18/19/22 — `spawnBoss` missing from the handle their own receipt claims to expose; W4's bones lane 29). None execute after or depend on N12's code: lanes 6/14 run before N12's module-level code initializes; N12's replays use isolated fresh game instances; the fifty gate — which drives the SAME restored game file through the FULL progression — is 63/63 green twice. Filed here so the owning lanes see the exact joint state at N12 close.

## Wiring diff summary

**`dashboard/static/games/mud.html`** (canonical; 1 token — the loop itself was already complete):

- `window.MUD` handle: `…spawnEnemy, spawnCascade…` → `…spawnEnemy, makeLoot, spawnCascade…` — the fleet affordance (spawnEnemy precedent) that lets a harness drive the seeded rarity roll through the real gameplay path. Zero gameplay-code changes; the loop (seeded `makeLoot` roll → 30s-fuse drop → `update()` walk-over at r+18 → `pickupLoot` lootScore auto-compare equip/store/discard → Digit1/Digit2 wield → `weapon()` feeding `playerDmg`/attack cadence/HUD) was entire and merely unreachable by any fleet consumer. (Token survived the external revert via the W-lanes' re-application; verified on the restored handle.)

**`scripts/test_mud_replay.js`** (1 new lane, 2 helper functions + console line):

- `LOOT: pickup -> inventory-add -> inventory-use replays byte-identical (the N12 consumer loop)` — `lootReplay(withSwap)` drives the whole loop inside a live fight: trash both slots (any seeded roll wins the compare), facing swing on a walker, seeded `makeLoot` at the bearer's feet at step 40 (taken by the real `update()` walk-over check at step 41), Digit2 press at step 100. Asserts: exactly one seeded `loot` event with a table rarity; walk-over equipped the drop with stats moved and a legal compare; Digit2 wielded slot 1 (and the no-swap control keeps 0); the opening swing landed (walker hp < max); same seed + same inputs → byte-identical evlog AND byte-identical 240-step sha256 state trace (snap() carries weapons[] + weaponIdx); removing the swap press forks the run exactly at the swap step.

**`scripts/test_mud_fifty.js`** (1 new LOOT phase after the vault lanes, 5 lanes 59–63):

- L59 seeded table law (24 rolls ×2 same-seed boots → identical rarity sequences, all in [0,3]); L60 walk-over equip branch (drop consumed, stats moved into the slot, compare never picks worse); L61 store branch (drop under active slot fills the free one) + discard branch (trash under both dies); L62 use-path (Digit2/Digit1 wield the slots); L63 kill-drops stream law (24 same-seed kills ×2 → identical drop counts, 13/24 observed — the 35% gate flowing through the seeded stream).

## Files touched

- `dashboard/static/games/mud.html` — one handle token (`makeLoot` exposed beside `spawnEnemy`)
- `scripts/test_mud_replay.js` — the LOOT replay lane (+ `lootReplay`/`RARITY_OF` helpers)
- `scripts/test_mud_fifty.js` — the LOOT phase (5 lanes)
- `watch/inbox/wave_20260916/receipts/N12_INVENTORY_CONSUMER.md` — this receipt

## Observations left for other lanes

- The replay harness's 6 reds (6/14/18/19/22/29) belong to FX4-vacuity, N9-boon-max, W5-ascension, W4-bones — exact messages in the output above; the fifty gate green-lights the same file end-to-end, so these are lane-vs-file convergence drift inside the W-wave, not engine regressions.
- `dashboard/static/mud.html` (100,832 B) and `site/dist/games/mud.html` remain byte-stale divergent copies (G1 defect, flagged since R2; both prior lanes declined to touch dist copies — the revert incident is the strongest argument yet for deleting or redirecting them: the stale copy is now a known revert vector).
- R2 orphans #2 (StS ascension — W5, mid-flight), #4 (wow_world sessions), #5 (estate LOD link-in — N11, done) — tracked in their own receipts.

---

## VERDICT

**Why it was orphaned (one-line root cause):** nothing in the inventory/loot loop was mechanically dead — the orphan was a pure consumption gap: the only pickup trigger is a walk-over within r+18 of a fresh kill-drop, and no harness lane, tile, or session ever drove that loop (R2 orphan #3), with not even a `spawnEnemy`-style handle affordance by which the fleet could have driven it.

**Wiring:** one token on the `window.MUD` handle (`makeLoot`, spawnEnemy precedent) + one byte-identical-replay lane in `test_mud_replay.js` (seeded roll → real walk-over pickup → auto-compare equip → Digit2 wield, pinned under the F1 law with a named use-fork) + 5 lanes in the fifty-lane gate (seeded table law · equip · store/discard · use-path · kill-drop stream law).

**Gate:** `test_mud_fifty.js` 63/63 green ×2 (EXIT=0, full progression green against the restored post-revert file); N12's replay lane 17 green ×2 (byte-identical evlog + 240-step trace, use-fork named at step 100). Replay harness joint state 29/35 — the 6 reds are concurrent W-lane surfaces (documented above, not N12's).

**Inventory/loot status: CONSUMED.**

---
*Receipt closed 2026-09-16 (lane respawned once after a rate-limit death; survived one external file revert). Bytes: dashboard/static/games/mud.html · scripts/test_mud_replay.js · scripts/test_mud_fifty.js. No git commands used. No paid APIs used.*
