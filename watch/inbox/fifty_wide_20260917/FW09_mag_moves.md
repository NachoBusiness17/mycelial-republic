# FW-09 — mag/ move map: old→new paths for the three moved-code ghost sources (2026-09-28)

Covers the three census-cited files: `watch/SELF_STEAL_GAME_ORGANS_20260901.md` (27 dead),
`watch/inbox/ATTIC_STRATA_20260911.md` (12 dead per 09-17 census; 11 with the 09-28-fixed
instrument), `watch/STEERING_LINEAGE_20260901.md` (12 dead). Every mapping below was verified
against the live tree on 2026-09-28 (exists() checks + `find`/`ls` on the named paths).

## Move 1 — `mag/mag/` double-nesting flattened → `mag/` (27/27 live twins verified)

`mag/mag/<X>` → `mag/<X>`. Full list from SELF_STEAL_GAME_ORGANS_20260901.md:
agent_arena, campaign, desk_observer, desk_timing, game_battle_cycle, game_brawl,
game_campaign, game_dice, game_dm, game_dm_llm, game_dm_voice, game_emulator, game_freeze,
game_live, game_mud, game_narrate, game_observer, game_passage, game_piece_tandem, game_play,
game_saga, game_score, game_world, game_world_map, game_world_render, riddler_campaign,
water_computer — all 27 exist at `mag/<X>.py` today.
Same move covers STEERING_LINEAGE's `mag/mag/grok_steer.py` → `mag/grok_steer.py` (live).

## Move 2 — 2026-09-08 kill list → `attic/kill_list_20260908/`

ATTIC_STRATA_20260911.md's dead set:
- `mag/hero_journey.py`, `mag/mag_soul.py`, `mag/mirror_persona.py`,
  `mag/moonshot_digital_twin.py`, `mag/quest_party.py`, `mag/reach_loop.py`,
  `mag/reach_protocol.py`, `mag/scrum_loop.py`, `mag/tesuji_steal.py`
  → `attic/kill_list_20260908/mag/<same name>` (all 9 verified present; archaeology copies
  also exist under `corpus/oral_history/.../mag-disk/` and `_archaeology_out/mag-disk-20260905/`
  — data, not the live tree).
- `watch/DAY_LEDGER_2026-09-07.md` → `attic/kill_list_20260908/watch/DAY_LEDGER_2026-09-07.md`
  (sibling days 09-04..09-06, 09-08, 09-09 still live in `watch/` — only 09-07 was killed).
- `watch/inbox/X_DRAFT_WRONG_WORLD_PARABLE_20260907.md` →
  `attic/kill_list_20260908/watch/inbox/X_DRAFT_WRONG_WORLD_PARABLE_20260907.md`.

## Move 3 — `mag/`-prefixed working dirs stripped → repo roots (STEERING_LINEAGE)

- `mag/memory/runs/<X>` → `memory/runs/<X>` — live twins verified for:
  alpha_steer/tuned.json, chatgpt_bot/STEER_TEST_PLAN_20260831.md, gap_map/stack.json,
  ghost_experimenter/steer_feedback.jsonl, invariant/state.json, openclaw_catalog/latest.json,
  research_packs/grok2_steering.json, steer/operator.json,
  zcode_audits/2026-08-25T1615Z_verkle_structure_audit.md (9 of 10).
- EXCEPTION (no twin): `mag/memory/runs/steer/STEER_PROFILES.md` — DELETED, not in the live
  tree nor `attic/`; last known home `memory/runs/steer/` (its sibling operator.json survives
  there). Recorded dead-by-deletion, not moved.
- `mag/watch/room.jsonl` → `watch/room.jsonl` (live).

## Counts reconciled

- 09-17 census said 27 + 12 + 12 = 51 for these three files; the fixed-instrument recount is
  27 + 11 + 12 = 50 (ATTIC_STRATA lost one to the mdx/jsonl/URL instrument fixes).
- 50 of 50 mapped: 47 moved-with-live-twin, 2 moved-to-attic (dead by design — killed), 1
  deleted (STEER_PROFILES.md). Zero mysteries left in these three files.
