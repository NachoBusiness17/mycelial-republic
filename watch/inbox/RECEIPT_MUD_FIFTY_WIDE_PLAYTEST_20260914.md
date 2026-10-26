# Receipt — MUD fifty-wide playtest round · 2026-09-14

**Files:** `dashboard/static/games/mud.html` (canonical, 1,919 → 2,311 lines) · `site/dist/games/mud.html` (synced, cmp-identical) · `scripts/test_mud_fifty.js` (51-lane headless harness)

**Verdict:** the monastery was **unwinnable** before this round. It now plays start-to-victory with traps, a learning horde, and swarm-game behaviors, proven by 51 automated lanes × 6 consecutive green runs.

## The map was broken (all fixed, all harness-verified)
1. **Forge unreachable → game unwinnable.** d6 demanded the forge be cleared *and* 4 sigils, but d6 was the only way in; d5 dumped into a sealed empty pocket. Fix: d6 now opens after the crypt; new d7 (forge→nave) carries the 4-sigil gate.
2. **d4 was a painted-on door** — the top band wall segment covered its gap; scriptorium→crypt was solid wall forever (teleports had been hiding it).
3. **Dragon spawned in the forge** (1750,600), not the nave. Now (1600,220).
4. **Three void highways**: west x0–60, north y0–60, east x1820–1920 strips let you walk around the whole monastery (and enemies with it). Sealed; south dead pocket sealed; the pocket became **The Ossuary** (8th room: drip gauntlet, bear traps, spikes, third bonfire).
5. **AFK soul farm was back** — cleared rooms paid +60 souls *per frame* (the previous round's `st.cleared` guard had been lost). Restored.
6. **Fuse crash**: killing into a fusion spliced array members while callers held stale indices → `TypeError`. `killEnemy` is identity-based now; both loops guard.
7. **Doors never sealed** — `syncDoors` force-opened d1 every call. New model: a door opens when its room is paid; an active uncleared room seals its own doors.
8. Respawn point was a duplicate object key (150,150 = inside the infirmary) → courtyard bonfire.
9. Bonfire was a per-frame infinite heal + enemy reset while anything was aggroed. Now: one rest, 4s cooldown, counts `lore.fires`.

## New content
- **Traps:** bear traps (bite anyone — lure the horde through), dart plates (corridor nozzles, hit both sides), chandeliers (aimed swing drops them; 3 bodies beneath drop them alone), forge fire vents (rhythmic, warn-then-burn, both sides), doorway spikes now impale enemies too, spitter mines now blow up spitters.
- **Swarm-game steals:** pheromone trail (blind enemies track your freshest visible scent, 4s window — found + fixed a scan bug that killed the mechanic after 6s of play), ghost allies (riposte kills raise grateful ghosts for 9s), the shout (F: knockback + windup interrupt + wakes everything you knock), soul orbs that skitter from a loud approach, dragon phase-2 ("THE DRAGON OPENS ITS EYE" at half blood — faster, tears whelps from its own hide).
- **Immersive horde:** bell-ringers (champion rooms may spawn a runner that warns the next room — kill him or meet a formed-up squad; steal from the rookepoole influence-network thread: the signal is documented, not secret), champions now walk with a live escort, champion death routes the wounded (they escape through doors and the next room takes them in), kills draw keening mourners who rise angry, corpses stain the floor.

## Playtest instrument
`scripts/test_mud_fifty.js` — headless DOM-shim harness, drives `window.MUD`, 51 lanes: full walk-through progression (every door, seal, champion, sigil, phase-2, cascade, victory), all trap/swarm/behavior mechanics, perf (heavy room < 8ms/step). Run: `node scripts/test_mud_fifty.js`. Bugs this harness caught that reading never did: the fuse crash, the dead scent scan, d4's fake door, the resurrected AFK farm.
