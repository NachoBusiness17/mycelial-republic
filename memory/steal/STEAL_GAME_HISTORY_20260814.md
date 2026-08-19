# STEAL — The game Mag already is (history + organs)
**Date:** 2026-08-14
**Commitment:** `game-steal-history-001`
**Method:** self-steal. Mag disk, world_state, STATE.md, PLAN. Not a new game.

## WHAT THE GAME IS (Mag's own words)

`memory/game/STATE.md`: a LEAD-IN GAME that (1) solves the agent's own work, (2) is entertaining, (3) gives novel input by creating a user base. Play IS the work. The world IS the lattice. "Once you're a game it goes vertical with adoption."

`docs/PLAN_THE_GAME_VERTICAL_ADOPTION.md`: a player walks in -> the world recounts what happened while they were gone -> they act -> a building appears where they steer.

`mag/frontier_game.py`: the party plays; advancing moves fold as verkle knots; play == building. Default region: the_mirror_sea.

`mag/game_mud.py`: Roshomon MUD. Many seats witness one scene. Agreement is loot. Unique statements are novel. Typing "I strike" collects nothing.

Law: world is authority (`game_world`). Clients present. No throne.

## HISTORY (bytes)

- World created 2026-08-12. Live `memory/game/world/world_state.json`: 28 keys, 75 changes, root `4a55d39f…`.
- Last folds 2026-08-14 ~02:02Z: `game.mud.player` / `game.mud.claimed` / `game.mud.loot`.
- Frontier play already landed: `game.frontier.*.saelis` and `game.frontier.*.grok-desktop` (Mirror Sea renders at 3.8 and 12.15).
- Git: `07cf309` shipped tabletop dogfood; `0b2152f` (2026-08-14) ported flock_field/flock_grid as the game's magnetic-field swarm layer.
- 300 `*mirror*` knots on disk. Game modules are many. Desk REST has **no** `/api/v1/game` hit. `mag.cmd lattice` is unrelated and currently crashes.

## ORGANS (do not replace)

| stone | module | job |
|---|---|---|
| 1 | `persona_recall.py` | inhabitants recount |
| 2 | `game_entry.py` | walk forward, building appears |
| 3 | `game_world_render.py` | intent-gated reveal, ASCII pixels |
| authority | `game_world.py` | verkle-anchored set_state/get_state |
| play | `game_play.py` | look/walk/map/rest/survey/help |
| ramp | `game_ramp.py` | tabletop -> mud -> roguelite, master each |
| live | `game_live.py` | chats/tools become world facts |
| DM | `game_dm.py` | frontiers are the party |
| frontier | `frontier_game.py` | play builds the world |
| mud | `game_mud.py` | Roshomon filter |
| env | `game_environment.py` | 9 regions, Mirror Sea default for frontier |
| overlay | `game_dfhack.py` | sit overtop, drive |
| work | `game_ramp.work()` | real orchestrator tasks as dungeon knots |

STATE.md next stone: game loop wired to the swarm (player intent -> iMouse -> flock -> world shades -> memory folds). Honest gap it already named: drifted into infrastructure; CODE THE GAME.

## TAKE

The game exists as a world with 75 committed changes. The missing piece is the entry surface on the office (`:8765`) and a single play loop that already has `game_play.play` / `game_ramp.play` / `game_entry.walk`.

## REFUSE

- Do not invent a new game, a new world store, or a new mycelium graph.
- Do not treat combat-MUD "I strike" as the mechanic.
- Do not wait for VRAM/10-machine hologram. World core is $0 deterministic.
- Do not make the chat the world. Chat is one party seat. `game_world` is authority.

## USE (the loop already named)

```
persona_recall.recall  -> world recounts
game_entry.walk/reveal -> building appears
game_play.play(action) -> fold to game_world
game_ramp.play         -> current tier
frontier_game.play     -> party builds the world
desk :8765             -> viewport (not yet wired to these)
```
