# FW-38 — Walkers-through-walls: bug-or-feature decision memo

**2026-09-28 · Q-027 (burn-reset gopher) · task: fifty-wide 09-17 board §H**
Evidence probe: `watch/inbox/burn_reset_20260927/queue/Q_038_wallwalkers_probe.js` — **7/7 lanes
green** (node, fifty-harness DOM shim, seed 20260928, ascension 0). Every claim below was either
run in the probe or read at the cited line of `dashboard/static/games/mud.html` (2632 lines at
this writing).

## The question

"Walkers through walls" — can monastery natives cross geometry the player cannot? Decision
requested: which crossings are features to keep and which are bugs to fix.

## What the code actually does

There are THREE wall systems and they disagree about sealed doors (`doorRects`, rebuilt each
`syncDoors()` from locked `DOORS`, mud.html:364-365):

| system | built from | sealed doors? |
|---|---|---|
| bodies (`resolveWalls`, mud.html:980-997) | `walls.concat(doorRects)` | **YES** — except the skip at :983 |
| sight (`rebuildVision` → `visionSegs`, mud.html:221-231) | `walls` only | **no** |
| bolts (`update()` projectile loop, mud.html:1546-1550) | `walls` only | **no** |

So a sealed door stops **feet only**. The one deliberate exception at mud.html:983 —
`if (w.door && (e.runner || e.rout > 0)) continue; // the bell-passage: natives slip sealed doors`
— lets bell-ringers (`runner`, spawned mud.html:895-902) and routing escorts (`rout` set on
champion death at mud.html:1992-1999, value 3.5) walk through sealed doors.

## Findings, each proven in the probe

1. **Sealed doors stop the player** — lane 1: walking north into sealed d2 for 1.5s, player ends
   at y=454.0 = door south face (440) + player r (14). Never enters the rect.
2. **Bolts fly through sealed doors — BUG.** Lane 2: a projectile pushed at (345,470) flying
   north crossed the sealed d2 rect and reached y=253.3, well north of the door, while
   `d2.locked === true`. Cause: the projectile wall test at mud.html:1547 loops `walls`, not
   `walls.concat(doorRects)`. A spitter south of a sealed door can hit the player through it.
3. **Enemies aggro through sealed doors — BUG (same family).** Lane 3: a walker 170px north of
   the player across sealed d2 aggroed at frame 0 — `canSee` (mud.html:247-252) runs on
   `visionSegs`, which `rebuildVision` builds from `walls` only (mud.html:223). Sight, and
   therefore aggro and the ranger's LOS-checked volleys, ignore sealed doors. The player's own
   torch-light polygon (same `visionSegs`) also renders through sealed doors.
4. **Bodies still seal to the pixel — the control.** Lane 4: that same aggroed walker chased for
   4s and pinned at y=386.0 = door north face (400) − r (14). The seal is exact; nothing
   "walks through walls" here.
5. **The bell-passage is real and load-bearing — FEATURE.** Lane 5: an unkillable escort with
   the exact champion-death state (`rout = 3.5`) in the ossuary (north-flush: room rect ends at
   y840, band wall y800-840) crossed the sealed d5 rect, left the field at frame 40, and the
   re-home chronicle "fled — … takes them in" fired. Without the :983 skip, `resolveWalls`
   pins a north-flush-room router at y=854 **inside its own room forever** — `roomOf` never
   flips, the re-home at mud.html:1259-1268 never fires, and the rout mechanic softlocks. The
   skip was landed in the 51-lane playtest fix `8cc789d00` ("doors actually seal now" — the
   same commit that made doors solid made this relief valve necessary).
6. **No tunneling anywhere at current caps.** Lane 6: a 220 u/s enemy (the spawn cap,
   mud.html:794) into the 40px wall column x660-700 for 120 frames held at x ≤ 646, max frame
   step 3.67px. Math: worst case step = 220 × 1.25 (pack boost, mud.html:1318) × dt cap 0.05
   (mud.html:2591) = 13.75px, vs the minimum full-wall crossing of thickness 20 (border,
   mud.html:109-112) + 2r ≥ 38px. An order of magnitude of headroom. Projectiles (≤260 u/s,
   13px/frame, point-in-rect at mud.html:1548) cannot tunnel 40px bands either.

## Decision

- **FEATURE, keep:** the bell-passage door skip (mud.html:983). It is the rout/ringer mechanic's
  exit valve; removing it softlocks routing in north-flush rooms (crypt, forge, ossuary).
- **BUG, fix (follow-up, not landed here — this ask is the decision memo):** sealed doors must
  also stop sight and bolts. One-line-each fixes: `rebuildVision` includes sealed `doorRects`
  segments (mind the TDZ order documented at mud.html:232), and the projectile loop at :1547
  tests `walls.concat(doorRects)` (the existing `allWalls()` helper at :352 is currently dead
  code — tileWalkable at :273 inlines the same concat; route both through it). Re-run
  `Q_038_wallwalkers_probe.js` with lanes 2/3 inverted to assert the fix, plus the standard
  mud replay + fifty gates.
- **NOT a bug:** tunneling (impossible at caps, finding 6); ghost allies/remote lanterns render
  and pass freely by design (allies are ghosts, `mudOthers` is presence-only).

## How this was checked

- Probe: `node watch/inbox/burn_reset_20260927/queue/Q_038_wallwalkers_probe.js` → 7/7 (this session).
- Game gates unaffected by this memo (no code change): `node scripts/test_mud_replay.js` 41/41
  and `node scripts/test_mud_fifty.js` 63/63 were run after the FW-37 client edit to mud.html
  (see Q-027 §FW-37), which is the same file this memo reads.
