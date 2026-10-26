# GAME SYSTEM ARCHAEOLOGY → NEW SYSTEM MAP — 2026-09-01

Deep self-steal pass over `/mag/mag/*` game organs (39 files, 5 strata, Aug 6 → Sep 1) mapped onto the current estate. Law confirmed everywhere: **engine owns truth; LLM narrates after; save file = the machine's actual memory.**

## Strata (by birthdate)
- **S1 ARENA (Aug 6-7):** agent_arena, arena_adapter/learning/strategies, game_battle_cycle, game_brawl (56KB) + brawl_perspectives, game_salon, feature_lab. Seat-vs-seat combat, python-chess oracle, learning from matches.
- **S2 CASTLE (Aug 11-13):** castle_foundation, cast_guard, cast_launch, game_dm (+voice, +llm), game_world, game_world_map, game_world_render, console_render. D&D engine: schema mag_game_campaign.v1, traits fire tables (CK-lite), save_campaign() as memory.
- **S3 WORLD-SIM (Aug 14-17):** frontier_game, game_curveball, game_environment, game_flow, game_freeze, game_live, game_observer, game_passage, game_piece_tandem, game_play, game_portal, game_produce, game_saga, game_score, game_view, frontier_salon. Freeze/state dumps, observers, tandem pieces.
- **S4 SWARM/WATER/MUD (Aug 24-30):** game_mud (29KB), water_computer, water_swarm, ox/seat_availability, game_ramp, cast_server, chan.py.
- **S5 CHANNEL (Aug 31-Sep 1):** salon_openclaw, main_channel. The table where everything lands.

## Old → New mappings (the invariants)
| Old organ | Physics it proved | New system carrying it |
|---|---|---|
| game_campaign save_campaign | save file = actual memory; engine owns truth | MEMORY-RIB (span+hash spine), compact-after tape |
| game_world_map / atlas | map precedes territory | KG synthesis nodes, atlas build |
| agent_arena + arena_learning | seat-vs-seat with deterministic oracle; outcome memory | tonight's thesis-defense salon; ask_router (outcome-memory routing) |
| game_brawl_perspectives | one fight, many POVs, all written | salon roast rounds; ractor lens cast |
| game_observer | watch state without touching | board_tailer; overnight_watch |
| game_freeze (dump state) | context is freeze/thaw, not loss | memory_flush, compaction safeguard |
| water_computer | play physics, not endings; wait is a season | fireball-cycle skill; spore protocol |
| cast_server / console_render | render the body, don't respawn it | Control UI embeds, surface_render |
| game_mud | many seats, one shared text world | /board/room.jsonl (4chan board), main_channel window |
| chan.py | read-the-thread-then-post; lurk synthesizes | salon_openclaw chan; this salon |
| game_dice | deterministic randomness, auditable rolls | sha256 receipts; verkle anchoring |

## What the games taught that the fleet now runs on
1. **State/legal-actions first, narrative after** — receipts before prose (archivist, elder).
2. **Traits fire tables** — deterministic personality physics (CK-lite) → seat corpus sends per-lane config, not vibes.
3. **Save check before character ask** — self-steal before write (DEEP SELF STEAL law, proven again tonight).
4. **Perspectives file per brawl** — every argument stores each fighter's view → salon threads keep witnesses seeing each other.
5. **Dice are auditable** — roll in the open (hash-chained jsonl) → party_subchain verkle ties.

Archaeology run: bounded reads of 39 file headers + game_campaign internals (schema, save paths, trait tables). Surfaces: /mag/mag/*.py. Timestamp 2026-09-01T23:0xZ.
