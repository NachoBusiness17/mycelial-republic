# W4 — GHOST PERSONALITIES (mud champions remember their killers)

- **Wave:** 2026-09-16 · lane W4 · THE WEAVE top-10 #4
- **Agent:** ZCode subagent (ghost-personalities)
- **Status:** DONE — both gates green
- **Files:** `dashboard/static/games/mud.html` (feature), `scripts/test_mud_replay.js` (6 new GP lanes + snap `cg` field). No git commands used; Write/Edit for source only.

## Mission

The estate's four boss-tier enemies each got a persistent personality ghost that remembers who killed it: a per-champion grudge ledger in the SAFE_STORE, a personalized telegraph line on rematch, and an opening stance that adapts one seeded step per prior encounter.

## The four champions (ROOMS defs)

| room | class | champion | ghost |
|---|---|---|---|
| infirmary | ranger | MARSHAL QETH, RANGER-MARSHAL | ghostId `infirmary` |
| scriptorium | cleric | SISTER HALVANE, HIGH CLERIC | ghostId `scriptorium` |
| crypt | rogue | VERAK THE UNSEEN, ROGUE-CAPTAIN | ghostId `crypt` |
| forge | bmage | MAGUS OLDRIN, WAR MAGE | ghostId `forge` |

## Implementation summary

1. **Grudge memory (SAFE_STORE).** `localStorage['mud_ghosts']` via the game's guarded `SAFE_STORE` accessor (W2's, with a one-line repair: it now probes the injected `localStorage` param as well as `window.localStorage` — harnesses inject the param form; same object in a browser). Ledger per champion: `{ n: encounters, grudges: [...] }`, **capped at GRUDGE_CAP = 5, newest kept**. `recordGrudge(rid, verdict)` appends `{ v: 'slain'|'took', by: killerName, style: killStyle(), seed: runSeed, date: ISO }`; `killStyle()` is a pure read of the lore counters (kiting/brawling/rolling/fire/swarming, fallback 'first blood'). The memory also hangs on the definition at runtime (`ROOMS[rid].champion.grudges` / `.encounters`). Machine state, lore-class: deliberately NOT reset by `startGame`.
2. **Recording triggers.** Champion slain → `killEnemy` files `'slain'` (only when `e.ghostId` — the FUSED WARDEN is `isChampion` but has no ghostId: a body, not a personality). Champion defeats the player → `playerDie` files `'took'` via killing-blow attribution: `hurtPlayer(dmg, src, srcEnemy)` now carries the enemy ref (`player.lastHitEnemy`) alongside W2's `lastHit` string; enemy melee sites, projectiles and fire zones pass `owner`/`e`.
3. **Rematch telegraph.** On `spawnChampion`, a lived grudge speaks once: `grudgeTelegraph(rid)` picks **one line from a per-class 4-line lexicon (`GRUDGE_LEX`) — no free text** — by FNV-1a of the last grudge record + encounter count (a pure function of the record; **zero stream draws**), slots filled only from the record (`{K}`iller, `{S}`tyle, `{N}` encounters). Delivered as chronicle + message banner + `evlog {e:'telegraph', room, i, n}`.
4. **Opening-pattern shift (seeded law).** Each champion draws an opening stance from the seeded LCG at spawn (`rndi`), then the draw shifts **+1 step per prior encounter**: `open = (rndi(0, len-1) + seen) % len`. Three real stances per class (`GRUDGE_OPEN`): ranger open-fire/stalk/hunter (volleyCd/speed/dmg), cleric bless/zeal/ward (healCd/speed/maxHp), rogue ambush/phantom/duel (aggro/stealth/attackT), bmage open-fire/ember wall/slow burn (castCd/fire zone/speed). Same seed + same ledger n → same opening.
5. **Cross-lane repairs landed under this lane** (the shared file was externally rolled back to its 17:14 pristine state mid-wave, twice; the FX4/W5/W1A/W2/N9/N10 substrate was re-landed by a concurrent restorer and completed here where the gates demanded it): `hurt` evlog event restored in `hurtPlayer`; evlog `tomb` cause made deterministic (`dCauseLog` = `'a ' + enemy.type`) so the killer's Math.random cosmetic name stays out of the replay log (the flavored cause stays in the SAFE_STORE record + whisper; snap pins `causeClass`); BOONS `max: 3` on torch/hermes/time (N9 max law was dead without them); `ascendForNextRun` no longer bumps the in-session ladder (W5 no-double-bump lane); `spawnBoss` exported on the MUD handle.

## The four telegraph lines as shipped

Canonical first grudge (`v: slain, by: lantern`, seed 20260916, 2026-09-16), verbatim from the game:

```
infirmary (1 prior): "Marked. lantern walks into my range again."
scriptorium (1 prior): "1 vigils end. This one, I finish."
crypt (1 prior): "The dark keeps my ledger, lantern. Your name is in it."
forge (1 prior): "Stand still this time, lantern. The ground will not."
deterministic: true
```

## Harness outputs (verbatim)

`scripts/test_mud_replay.js` (41 lanes — 35 pre-existing + 6 new GP lanes; mud.html 2,619 lines at gate time):

```
PASS 36 GP: a first encounter is memoryless — no telegraph; a slain champion files a dated grudge
PASS 37 GP: kill the champion twice — the rematch telegraph speaks, and the second differs deterministically
PASS 38 GP: the opening stance shifts exactly one seeded step per prior encounter
PASS 39 GP: same seed + same injected history -> byte-identical rematch (telegraph, stance, events)
PASS 40 GP: the ledger is capped (5, newest kept); a champion victory files "took" through the real kill path
PASS 41 GP: replay law with lived ghosts — same seed + tape + ledger twice -> byte-identical trace + evlog

41/41 lanes green
mud: 2620 lines, seed 20260916, 1800 steps @ 60fps, tape A 14 events, runSeed 20260916
```

(Lanes 1–35: R/F1/F2/G replay falsifiers, BD boon-draft, LOOT, ASC ascension, FLT fleet seed, BN bones — all PASS in the same run.)

`scripts/test_mud_fifty.js` (the mud gate):

```
63/63 lanes green
```

## Ghost-law — what the champions remember and what they can't

**They remember:** who killed them (`by` — the lantern's name), how the lantern tends to kill (`style` — the horde's read of your habits), the run seed and date of every recorded encounter, whether they slew you or you slew them (`slain`/`took`), and the running count of encounters — up to the 5 freshest grudges per champion, forever, across deaths and reloads. That memory is the only thing that changes on a rematch: the words they open with, and a one-step shift in their opening stance.

**They can't:** remember anything not filed (first encounters are memoryless — no telegraph, a plain seeded stance); speak a single word outside their class lexicon (no free text — the line index is a pure function of the record, never a stream draw); feed the ledger into the replay stream (same seed + same history replays byte-identically with lived ghosts — proven by GP-41); remember a body they never owned (the fused warden is champion-tier but ghostless — only the four named champions carry a `ghostId`); or remember more than five grievances (older grudges rot out FIFO, newest kept). A ghost is memory, not dice: the adaptation always rolls from the seeded stream, and the ledger only shifts it.

## Incident log (cross-lane, recorded for the coordinator)

- **23:50-era rollback:** `mud.html` (all three copies) was externally reverted to the 17:14 pristine state (~22:50) while the wave's test scripts kept the evening features. Same class of incident as the one FX4 logged in its receipt. The FX4/W5/W1A/W2 substrate was re-landed by a concurrent restorer (23:04/23:17/23:29 writes); this lane completed the missing pieces its gates demanded (listed above) and landed W4 on top. All fixtures converged green by 23:5x.
- The failed `hurt`-event / tomb-cause issues were replay-law violations (Math.random cosmetics reaching evlog/snap); fixes documented in Implementation summary §5.

## Status: DONE
