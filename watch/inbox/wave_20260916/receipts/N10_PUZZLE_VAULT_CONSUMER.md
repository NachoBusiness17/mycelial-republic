# N10_PUZZLE_VAULT_CONSUMER — receipt (in progress)

- Lane: N10, wave_20260916 — consume the R2 dogfood-orphan #1: mud.html puzzle vault (built, zero consumers).
- Law: receipt FIRST, appended as work proceeds. No git commands. No paid APIs. Canonical source = `dashboard/static/games/mud.html` (the `dashboard/static/mud.html` copy is stale/divergent — G1 defect, NOT touched here).
- Inputs: R2_GAME_SUBSYSTEM_GAPS.md (orphan #1), mud.html vault code L474–538, world tables L100–155, harness `scripts/test_mud_fifty.js` (51 lanes).

## Work log

- [2026-09-16] Receipt created first. Baseline gate captured below.
- [2026-09-16] Vault code read in full. Mechanics: `puzzleReset()` places key + chest at PUZZLE_SPOTS and re-seals the "gate" wall; `puzzleTick(dt)` (called from `update()` L1417 — the live loop) does key walk-over pickup (<26px), chime proximity audio (<240px), chest open (<34px, requires key held) paying **120 souls + full heal + makeLoot weapon + super orb**, and a two-plate gate (plates sink on <34px stand; both sink → `gateOpen=true`, `walls.find(w=>w.gate).open=true`, vision rebuild, "the vault is lit"). Exports already carry `puzzle`, `puzzleReset` on `window.MUD`. Render L1815 already colors `w.gate` walls brass (`#7a5c28`); `resolveWalls`/`rebuildVision`/render all honor `w.open`.

## Root cause (why nothing routes to it)

Three-part dead link, read from bytes:

1. **No wall in the world ever carried `gate: true`.** `walls` (L100–135) has no gate tag, so `walls.find(w => w.gate)` in `puzzleReset`/`puzzleTick` returns undefined both times — the `if (gateWall)` guards silently no-op. The two-plate puzzle "opens" a gate that does not exist. The brass gate color at render L1815 was painted for a wall that was never given the tag.
2. **Plate II was placed inside a sealed void pocket.** Plate 2 at (1720,1000) lies south of the forge in the pocket x1300–1920, y840–1200 — fully enclosed by the band `{x:1300,y:800,w:620,h:40}` (no door in it), the west flank `{x:1260,y:650,w:40,h:550}`, and the world border. Comment says it outright: "south of the forge — sealed drafts, nothing down there." The second plate could never be pressed, so the gate could never open even if it existed.
3. **Fleet level:** zero harness lanes, zero tiles, zero sessions ever touched the vault (R2 orphan #1). The key→chest payout technically works by walk-over, but no consumer ever verified a single soul of it.

Net: the vault was a decorative prop loop — plates unreachable, gate imaginary, reward ungated and unverified.

## Wiring (the minimal consumer)

- mud.html: tag the south band `{x:1300,y:800,w:620,h:40}` as the vault gate (`gate:true`) — the existing `puzzleReset`/`puzzleTick`/render/vision/collision machinery all already honor it; plate II moved (1720,1000)→(1720,700) onto the forge floor (reachable, inside forge x1300–1820 y440–760); chest placement pinned into the vault pocket (1720,1000) so the gate actually gates the reward; key placement = `farSpot(chest)` (all 6 PUZZLE_SPOTS are >500px from the pocket, so walk-to-it still pays, chimes still guide).
- Route a human now walks: find key anywhere (chimes) → sink plate I (infirmary floor, 220,340) → sink plate II (forge floor, 1720,700) → "an ancient gate grinds open — the vault is lit" → walk south through the opened band into the vault pocket → chest: 120 souls + full heal + weapon + super orb.
- Harness: new VAULT block in `scripts/test_mud_fifty.js` — scripted route (gate exists+sealed → sealed gate physically blocks → plate I → plate II → gate open → pocket walkable → key pickup → chest pays: souls Δ+120, full heal, loot drop row, super orb).

## Baseline gate (before wiring)

```text
51/51 lanes green
```

## Wiring diff summary

**`dashboard/static/games/mud.html`** (canonical source; 3 hunks):

1. Walls table: `// south of the forge — sealed drafts, nothing down there` / `{x:1300,y:800,w:620,h:40},` → `// south of the forge — THE VAULT GATE: plates I (infirmary) + II (forge) grind it open; the pocket pays` / `{x:1300,y:800,w:620,h:40,gate:true},`. The existing machinery (puzzleReset re-seal, puzzleTick open, resolveWalls skip, rebuildVision, brass render L1815) all already honored `gate`/`open` — the tag was simply never put on any wall.
2. Plate II moved out of the sealed void: `{ x: 1720, y: 1000, on: false }` → `{ x: 1720, y: 700, on: false }` (forge floor, inside forge x1300–1820 y440–760). Plate I (220,340, infirmary) unchanged.
3. `puzzleReset()`: chest pinned into the vault pocket — `puzzle.chest = { x: 1720, y: 1000 }` (behind the gate; the reward is now gated), key = `farSpot(chest)` (all 6 PUZZLE_SPOTS are >500px from the pocket, so walk-to-it still pays, chimes still guide). Player route: key anywhere → plate I (infirmary) → plate II (forge) → gate grinds open → walk south into the pocket → chest: 120 souls + full heal + weapon + super orb.

**`scripts/test_mud_fifty.js`** (1 hunk, after the fuse lane, before the report): new VAULT phase — fresh `startGame()`, 7 lanes (52–58): gate exists+sealed at reset · sealed gate physically blocks the pocket walk · plate I sinks · plate II sinks → gate grinds open (both `puzzle.gateOpen` and the wall's `open` flag) · opened gate yields (pocket enterable) · key walk-over pickup · chest pays — souls Δ exactly +120, full heal from 37 hp, weapon row (lootDrops/evlog `loot` event), super orb present.

## Harness + gate outputs (verbatim)

Stability: 4 consecutive full runs, all green.

```text
58/58 lanes green
58/58 lanes green
58/58 lanes green
58/58 lanes green
```

Full gate run (verbatim, harness numbering):

```text
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

58/58 lanes green
```

(51 legacy lanes byte-identical in names/order, renumbered by the harness only where the 7 new V lanes append — lanes 52–58.)

## Observations left for other lanes

- `site/dist/games/mud.html` (100,832 B) is byte-stale — it matches the divergent `dashboard/static/mud.html`, not games/ (105,849 B post-wiring). Any dist rebuild will pick the fix up; N10 did not touch dist copies.
- R2 orphans #2 (StS ascension), #3 (inventory loot loop), #4 (wow_world sessions), #5 (estate LOD link-in) remain open.

---

## VERDICT

**Why it was orphaned (one-line root cause):** the vault's gate machinery looked for `walls.find(w => w.gate)` but no wall in the world ever carried `gate: true` (the `if (gateWall)` guards silently no-op'd), and plate II sat at (1720,1000) inside the sealed south-drafts pocket where it could never be pressed — a dead link no harness lane ever consumed.

**Wiring:** gate tag on the south band + plate II moved to the forge floor + chest pinned behind the gate in the pocket; 7 new VAULT lanes script the full route (sealed-blocks → plates → gate opens → pocket enterable → key → chest pays 120 souls + heal + weapon + super orb).

**Gate:** 58/58 lanes green (51 legacy + 7 new), stable across 4 runs.

**Vault status: CONSUMED.**

---
*Receipt closed 2026-09-16. Bytes: dashboard/static/games/mud.html · scripts/test_mud_fifty.js. No git commands used. No paid APIs used.*
