# W2 — MUD Bones Files (NetHack-style dead runs haunt later runs)

Lane: THE WEAVE top-10 delight-per-effort #1 · Date: 2026-09-16 · Status: **DONE**
Files: `dashboard/static/games/mud.html` (canonical, 2,620 lines / ~116 KB final), `scripts/test_mud_replay.js` (7 new BN lanes, 35 total)
Gates: **replay harness 35/35 green (exit 0)** · **fifty-lane gate 63/63 green × 5 consecutive runs (exit 0)**

## ⚠ INCIDENT (filed first, per wave-lane law)

The wave fold's mirror-restore (~22:50) reverted `dashboard/static/games/mud.html` to the pristine
pre-FX4 vintage (100,832 B, mtime 17:14 preserved) — losing in one stroke the landed work of five
lanes (FX4 replay port, W5 ascension, W1A fleet mud-side staging, N10 vault, N12 loot token) plus
my first bones landing (23/23 edits, verified green-parse at 116,988 B). No backup existed anywhere
on disk (checked artifacts/, site/dist/, wave drafts, quarantine — all pristine). Following the
FX4 incident playbook, I rebuilt the entire base **atomically via exact-match, abort-on-drift
scripts** (60/60 edits) from the receipts + the surviving harness contracts, then re-landed bones
on top. W1A had pre-staged the file for exactly this ("STAGED on this vintage: the FX4 replay LCG
… re-landing via the FX4/W5 restore", mud.html L68-70). Concurrent-writer collisions with W4
(ghost personalities, landed 23:22 on top of my bones core — kept my `hurtPlayer(dmg, src)`, added
`srcEnemy`) were absorbed by re-reading and re-anchoring, never by clobbering.
**Clobber-cycle fix:** the revert vector was the stale `dashboard/static/mud.html` mirror. Both
derived copies (`dashboard/static/mud.html`, `site/dist/games/mud.html`) are now byte-synced to
canonical — a future fold-restore becomes a no-op.

## Implementation summary

**Bones (the mission):**
- `SAFE_STORE` (swarm.html house pattern) ported: one guarded localStorage accessor, in-memory fallback for private-browsing modes.
- **Bones pool** `localStorage['mud_bones']` via SAFE_STORE, cap `BONES_CAP = 10`, **FIFO** (`bonesWrite` shifts oldest past the cap; persisted every write). Pool is **machine state, like lore** — never reset by `startGame`; ghosts (the session's risen) are cleared on `startGame`.
- **On death** (`playerDie`): a bones record is filed — `{v:1, seed:runSeed, room:G.curRoom, x, y (death spot), cause (killer string), causeClass (deterministic class cause), name: ME.name (the `?name=` URL lantern name), stat, statV: hardestStat()}`. Hardest stat = max of might/vigor/swiftness, falling back to `grit = level`. Evlog receipt: `tomb` (deterministic class cause only).
- **On a later run entering the same room** (`roomTick` activation): the **bones-roll** — one seeded draw (`rng() < 0.5`, `forceBones` short-circuits house-style, no draw), then one seeded pick among that room's bones records → `spawnGhost`. Never bare Math.random.
- **The ghost**: deterministic drift (seek within 240px at `30 + 2×toughness` px/s, else sine/cos bob on a phase derived from the dead run's seed — **zero stream draws, zero Math.random in the entire ghost path**); haunts only its own room (despawns on room exit / 60s). **Toughness = 4 + 3×statV** (the dead run's hardest stat) → drives stamina burn (`5 + toughness` per touch, 1.6s cooldown) and snare (`0.25 + 0.05×toughness` s). **A ghost cannot kill: the touch never reads hp** — the every-enemy-can-kill law stays for the living; the dead teach, they don't execute. A ghost can be struck (same swing arc, no damage-jitter draw) and at 0 hp it rests (`grest`) — no loot, the dead don't pay.
- **Sanctified courtyard**: bones are filed everywhere, ghosts never rise in the courtyard.
- Evlog kinds added: `tomb`, `bones`, `whisper`, `grest` (all deterministic). Handle additions: `get ghosts()`, `get bones()`, `forceBones`, `bonesWrite`, `bonesSave`, `hurtPlayer`.

**Base restore (incident rebuild, per the other lanes' receipts):** FX4 seeded LCG + `startGame(forcedSeed)` + 19-site seed port + evlog (incl. the `hurt` event, missed in the first restore pass and caught by F1's non-vacuous lane) + cosmetic draws (`poof`, camera shake, ghost ph, names) moved off the stream; W5 ascension (boot read, `startGame(seed, asc)` pin, victory → `ascendForNextRun()`, `persistAsc`, no-double-bump `nextLoop`); N9 max-law draft (counts, stackables re-offer below max, `draftPick` swap isolation); N10 vault (gate wall tag, plate II to forge floor, chest pinned in the pocket); N12 `makeLoot` token; W1A fleet seed consumed as the no-seed default. W4's champion-grudge merge (landed mid-pass on top of bones) is honored: records gained `causeClass` so evlog/snapshot surfaces stay deterministic while the killer's (Math.random-fed) name remains whisper-only flavor — FX4's cosmetic-name classification still holds.

## Ghost lore line format

- Bones record (SAFE_STORE `mud_bones`): `{v:1, seed, room, x, y, cause, causeClass, name, stat, statV}`.
- Whisper (chronicle + message, on first touch): `UR-VABOK whispers: "a walker took me" — their grit still holds`
- Room-entry chronicle: `the air goes cold — UR-VABOK walks this room again`
- Rest: `the ghost of UR-VABOK rests — "a walker" it last said`
- Toughness: `4 + 3 × statV` (grit fallback counts the level); death spot and room are preserved exactly.

## Harness outputs (verbatim)

### scripts/test_mud_replay.js (35 lanes)

```
    A died to "a walker" in the refectory; B met UR-VABOK (toughness 7); whisper: "a walker took me" — stamina bottomed at 89.3
    ghost (toughness 13) touched a 1-hp bearer: hp 1, state play, snare 0.90s
    24 seeds x2 boots: haunt/no-haunt is a pure function of (seed, pool); hauntings rose 11/24
    pooled TAPE_A x2 (forced + natural roll): byte-identical incl gh/bn; hauntings fired 1x forced, 0x rolled
PASS 29 BN: die in run A -> run B entering the room meets A's ghost (name, cause, toughness carried)
PASS 30 BN: a ghost cannot kill — touching a 1-hp bearer leaves hp 1, state play, zero death events
PASS 31 BN: ghost spawning is seeded — same seed + pool -> identical haunt/no-haunt across 24 seeds x2
PASS 32 BN: replay law with bones — same seed + tape + pool twice -> byte-identical trace INCLUDING ghost fields
PASS 33 BN: bones are room-bound — the crypt dead do not haunt the refectory
PASS 34 BN: the courtyard is sanctified — bones are filed there but no ghost rises
PASS 35 BN: the pool is capped at 10, FIFO — bone #0 rots out first

35/35 lanes green
mud: 2620 lines, seed 20260916, 1800 steps @ 60fps, tape A 14 events, runSeed 20260916
```
(exit 0; also green: R 1-3, F1 4-6, F2 7-10, G 11, BD 12-16, LOOT 17, ASC 18-24, FLT 25-28)

### scripts/test_mud_fifty.js — the mud gate

```
63/63 lanes green   (× 5 consecutive full runs, exit 0 each)
```

## Replay-law compliance proof

1. **Seeded spawn**: the only door to `spawnGhost` is the roomTick bones-roll — `rng() < 0.5` (or the `forceBones` short-circuit, which consumes no draw) then `rng()`-indexed pick. BN lane 31: 24 seeds × 2 boots each → haunt/no-haunt and ghost position identical within each seed pair, probabilistic across seeds (11/24 rose). No `Math.random` anywhere in the ghost/bones runtime path (structural: spawn/ghostTick/swing-vs-ghost/whisper; the ghost's drift phase derives from the dead run's recorded seed).
2. **Byte-identical replay including the ghost**: BN lane 32 = F1 with a canned pool — same seed + same tape + same pool twice → byte-identical evlog AND byte-identical 1800-step state trace, with ghost state (`gh`) and the pool (`bn`) inside every step digest. A Math.random-fed haunting would break this identity — the lane is also the no-bare-random falsifier.
3. **Machine-state composition can't leak cosmetics**: the killer's genName-fed nickname is confined to the SAFE_STORE record + whisper (both outside evlog/snapshot or pinned via deterministic `causeClass`); caught by a real cross-run divergence (asc=1 probe, `$.bn[0][5]` differing between identical runs) and fixed at the law's root — the classification FX4 made for names survives composition with bones.
4. **Whole-suite replay law intact**: F1 (lanes 4-5), F2 named fork @ step 160 (7-9), seed sensitivity (11), BD seeded drafts (12), LOOT byte-identity (17), ASC asc=1 replay identity (18) — all green on the bones build; tape A's 14 events include `tomb`/`bones` receipts.

## Files touched

- `dashboard/static/games/mud.html` — bones + base restore (atomic exact-match patches: 60 + 3 edits, abort-on-drift)
- `scripts/test_mud_replay.js` — 7 BN lanes, `gh`/`bn` in snap(), `loadGame(storage, search)`, BN1 instrumentation widening
- `dashboard/static/mud.html`, `site/dist/games/mud.html` — derived byte-copies of canonical (clobber-cycle fix, per W3's surface law)
- Probe/patch working files deleted; deliverables are the game, the harness, and this receipt.

## Handoff notes

- W4's ghost personalities share the machine-state idiom (`mud_ghosts` ledger, SAFE_STORE) — `hurtPlayer(dmg, src, srcEnemy)` is now a shared surface: `src` feeds bones, `srcEnemy` feeds their grudge ledger.
- Bones currently spawn only on activation of uncleared rooms — cleared-room revisits don't roll (the sanctified-courtyard law generalizes: peace where the fighting is done). If a later lane wants revisits haunted, the roll moves to `roomOf` change instead of activation.
- The stray-super-orb SUPERHOT dilation hazard for fixed-step tooling (FX4 receipt, finding 1) still stands — `pump()` clears `G.super`.
