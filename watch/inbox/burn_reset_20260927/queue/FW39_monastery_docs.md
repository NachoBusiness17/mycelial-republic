# FW-39 — The Monastery room-state machine, documented from code

**2026-09-28 · Q-027 (burn-reset gopher) · task: fifty-wide 09-17 board §H**
Source of truth: `dashboard/static/games/mud.html` (THE CRIMSON MONASTERY). Every state,
transition, and gate below was read at the cited line in this session; nothing is from memory
or from the continuity notes. Line numbers refer to the working tree at this writing (2,632
lines, FW-37 client edit included).

## World (mud.html:107-207)

- `WORLD_W 1920 × WORLD_H 1200` (:108). Eight rooms — `ROOMS` (:148-157): courtyard (start,
  bonfire, no queue), refectory (drip room: spawns one at a time), infirmary / scriptorium /
  crypt / forge (queue rooms with champions), ossuary (drip, no champion), nave (empty until the
  dragon). Progression order `ROOM_ORDER` (:207): refectory → infirmary → scriptorium → crypt →
  ossuary → forge → nave.
- Seven doors `DOORS` (:159-166). Each keys to the room it unlocks (`after`); d7 additionally
  needs 4 sigils (`needSigils: 4`, :165).
- `ROOM_STATE[rid] = { activated, cleared, idx, spawned, champOut, t }` (:178, allocated :881).
  This object IS the state machine; there is no enum — the booleans combine into five states.
- Cross-run memory hooks: `lore` (localStorage `mud_lore`, :476) and the bones pool (the dead
  rise; the courtyard is sanctified, :915).

## The five states

| state | condition | code |
|---|---|---|
| SANCTIFIED | courtyard only — born `activated+cleared` (:373, :381) | :373 |
| DORMANT | `!activated && !cleared` | :886 |
| ENGAGED | `activated && !cleared` — doors sealed (:890), queue spawning | :886-931 |
| CHAMPION | ENGAGED + `champOut` — champion walking | :933-938 |
| CLEARED | `cleared` — pays once per entry cycle (`return` at :885) | :939-952 |

## Transitions (roomTick, per frame, mud.html:876-953)

1. **DORMANT → ENGAGED** on player entry (`roomOf(player.x, player.y)`, :878-880). Entry side
   effects, in order: doors keyed `after === rid` lock (:890, `syncDoors()` :353-367 also
   re-derives every door: locked = after-room uncleared OR sigil gate OR next-room active
   :356-363); nave spawns the boss (:893); champion rooms may spawn the **bell-ringer** (45%
   seeded, `forceBell` override, :895-902) — a runner that sprints to the next room's door;
   non-drip rooms spawn their whole `queue` at the `spots` (:903-908); if the ringer rang, the
   next room's escorts **prepop aggro** (:909-912); the **BONES-ROLL** (50% seeded) may raise a
   haunting from the room's dead (:914-922).
2. **ENGAGED, drip rooms**: one enemy per 1.1s while the room is empty (`st.t` fuse, :925-931).
3. **ENGAGED → CHAMPION** when the queue is exhausted, at most one escort remains, and the room
   has a champion: `spawnChampion` (:933-938; champion body ×2.6 hp, ×1.4 dmg, ×1.15 speed cap
   200, :850-853, grudge-shifted opening from the champGhosts ledger, :857-865).
4. **CHAMPION/ENGAGED → CLEARED** when queue exhausted and `alive === 0`: doors keyed to the
   room unlock (:942), champion rooms grant a sigil (cap 4, :945-948), +60 souls (:950).
5. **CLEARED → DORMANT** on death or bonfire rest: `spawnAllEnemies` (:954-963) resets every
   uncleared room's state and deletes its field enemies; cleared rooms stay cleared — the
   monastery remembers your progress within a run.
6. **VICTORY** (not part of roomTick): `SIGILS.count >= 4 && G.naveEverActive` (:889 records the
   nave's first activation) `&&` no boss/k8/k3 alive && no living nave-room enemy (:1857-1858).
   The `naveEverActive` flag exists because the check originally fired on an empty board at run
   start (the "dragon falls by default" bug, fixed in the same gate).

## The natives' escape valve (cross-refs FW-38)

- **Bell-ringer** (`runner`, :1273-1284): ignores the player, sprints to `NEXT_AFTER[room]`'s
  door center (:204, :1274-1277); arrival inside 46px marks the next room `prepop` and removes
  it (:1278-1282). Kill it before it rings or the next room greets you aggroed.
- **Rout** (champion death, :1991-1999): surviving escorts below 60% hp get `rout = 3.5` and run
  (:1254-1271) for the nearest `ROUTE_EXIT[room]` door center (:206, :1256); once `roomOf`
  leaves their room they are **re-homed into the next uncleared room's queue** (:1259-1268) —
  the room you fight next is staffed by the room you just broke. Struck mid-flight, `rout = 0`
  (:1103): the router finds its nerve.
- Both pass **through sealed doors** by the `resolveWalls` skip at :983 — the bell-passage —
  which FW-38's probe proved load-bearing (a north-flush-room router pins forever without it).

## Death & memory around the machine

- Death resets uncleared rooms (:954-963 via `respawn` :2540-2549); the verkle-style rewind
  (`rewindBuf`, :452-454) can decline the reset once per run (:2572, :2578-2588).
- Kills feed the horde's persistent `lore` (kite/brawler tallies, :2000-2008) and the bones
  pool (`bonesWrite`, the hauntings the BONES-ROLL draws).
- Every transition appends to the replay `evlog` (`room` :888, `bell` :901, `champion` :865,
  `clear` :941, `sigil` :947, `victory` :1862) — same seed + same inputs → byte-identical log,
  the law `scripts/test_mud_replay.js` enforces (41/41 this session).

## Rationale (the machine's design, from the comments)

"Nothing wakes until it sees you — and once it sees you, it remembers" (:1289-1294: aggro needs
`canSee`, pack-pulls within 180px); "a cleared room pays once — not every frame you loiter"
(:885, the AFK-soul-farm guard restored in `8cc789d00`); "an active, uncleared room seals its
own doors — fight, then leave" (:354-355); "the void outside the rooms is not a road" (:141).
