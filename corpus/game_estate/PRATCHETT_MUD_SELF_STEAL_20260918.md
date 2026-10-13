# PRATCHETT + MUD RESEARCH SELF-STEAL — crosswalk into the mud and games (2026-09-18)

*Operator: "self steal pratchett discworld and our mud research we got from the new
stealth model to incorporate." Source: NPC=SEAT architecture (Pratchett row), UF-116
(DCC systems), UF-36 (governance constitutions), UF-37 (Evennia), UF-80 (next rung),
UF-89 (websocket relay), UF-01 (playerbots), UF-117 (WoW character architecture).*

## PRATCHETT MECHANICS → MUD IMPLEMENTATION (concrete, behind gates)

| Discworld | Mud system it feeds | Build |
|---|---|---|
| **Narrativium**: stories have gravity; events bend toward the story | `mud_lore` already has zone lore; add **lore gravity**: NPCs whose zone lore was read by a player get +1 dialogue depth on next encounter — the story physically pulls the NPC toward it | `lore_read_count` per zone, `npc_dialogue_depth = min(3, lore_reads)` |
| **Death SPEAKS IN CAPS**: system voices have typographic law | Player death text in the mud already has cause classes (`causeClass`); extend: every death gets an ALL-CAPS line from "DEATH" as a distinct voice, not the narrator's | `DEATH_VOICE` array, `deathCaps(cause)` — 5 lines |
| **Small Gods**: gods power up on belief | The 12 boon gods (BOONS[]) get **belief meters**: a god whose boon was drafted more times grows stronger (larger bonus, more draft weight). A god never drafted weakens. | `godBelief[12]`, `+0.1 per draft`, `draft_weight *= belief` |
| **The Watch**: institutions outlive heroes | The mud's `GRUDGE_KEY` and `BONES_KEY` persist per-player; add **institutional memory**: the innkeeper NPC remembers not just your grudge but your faction alignment | `factionAlignment[player] → npcGreeting` |
| **L-space: all libraries connect** | The corpus canon + imprint IS L-space; the mud's innkeeper becomes a **Librarian face** that cites the imprint when asked about lore | `chat_provider(z_ai3, imprint_slice, player_question)` — the Librarian IS the innkeeper |

## STEALTH MODEL RESEARCH → MUD IMPROVEMENTS

| Research row | Finding | Mud application |
|---|---|---|
| UF-116 (DCC) | The System is bureaucratic-sarcastic, issues absurd quests | The mud's DM face (when built) gets a **quest voice**: mundane tasks with grandiose framing ("bring me three rat tails and the symmetry of your intent") |
| UF-36 (ALFA charter) | NWN governance used a written charter with roles and amendment process | The mud's innkeeper/warden/guide get a **charter**: what each NPC can and cannot say/do, stored as data not hardcoded |
| UF-37 (Evennia) | Evennia's typeclass system: every object is a Python class with tags, aliases, and scripts | Our mud's `ROOM_STATE` and `npc` objects could carry **tags** (faction, mood, story-gravity) that persist across sessions |
| UF-89 (websocket) | Node ws handles 50-200 concurrent at 10k msg/s | Our relay at :8766 handles presence; upgrade to **ws for room state** when the NPC faces go live (chat needs lower latency than presence polling) |
| UF-01 (playerbots) | mod-playerbots gives each bot a class, spec, and equipment; bots form parties and run dungeons | Our bones ghosts + grudges + the NPC=seat architecture = **bot innkeepers** that remember you, serve boons, and have opinions |
| UF-80 (next rung) | Deepening RUINS GO beats AzerothCore spike for compounding value at $0/one week | Agreed — RUINS GO has the evolution loop and the gate; the mud gets the NPC faces; **both grow from the same D&D layer** |

## THE CROSS-GAME TRANSFER (what learns from whom)

| From | To | Mechanic | Build |
|---|---|---|---|
| RUINS GO | MUD | **Step-clock puzzle rooms**: a chamber where mud monsters only move on player command |superhot already proves the mud can host time-freeze; add one puzzle room |
| MUD | RUINS GO | **Boon drafts**: after boss kills, offer 1-of-3 boon cards (mud's BOONS ported to the engine's trait system) | engine v1.2: trait effects in step() |
| Frontier Souls | MUD | **Grudge → NPC dialogue**: the innkeeper mentions the thing that killed you (already filed as mud-locked grudge transfer) | `recordGrudge` → `innkeeperDialogue` |
| Swarm | MUD | **Escalation**: horde pressure increases with depth; mud spawns scale with how deep you've gone this session | `sessionDepth → spawnRate` multiplier |

## FALSIFIER

If after implementing the first 3 NPC faces (innkeeper, vault warden, bones guide)
a player cannot tell which face they're talking to within 3 exchanges, the faces
are not faces — collapse to one narrator and stop pretending the mesh has personality.
