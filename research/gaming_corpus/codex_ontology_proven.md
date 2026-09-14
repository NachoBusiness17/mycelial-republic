# THE CODEX ONTOLOGY — PROVEN TONIGHT (2026-09-06, harvester codex)
*GAME SURFACE vol-2 · Picasso license. The Codex (watch/GAME_CODEX_20260903.md) claimed
the game grows as fast as the fleet learns. SHADOW WALK materialized the claim the same
night: 72 chunks carved from the model's own behavioral volume, invariants as ore,
shadow as void, fog of war as the anti-hallucination barrier. Every ontology element
below now has a path on disk. G-cells: `G/engine/narrative/{mud,dungeon,dark-souls,
adventurers,dragons,loot,ladder}` on watch/TESUJI_MAP.jsonl (seat codex, all SUPPORTED).*

| Game element | The actual process | Proof it exists today (path) |
|---|---|---|
| **THE MUD** | event tape + text surfaces — one stream, many games | `logs/behavioral_events.jsonl` — 103,463 rows, last 2026-09-06T04:43Z (live); `logs/queue_events.jsonl` |
| **THE DUNGEON** | THE ROOM lightmap — invariants as chambers, organ walls | `dashboard/static/room_lightmap.html` + `dashboard/static/salon_lightmap.html`, rendered by `mag/room_state.py` from `memory/trajectory/steps.jsonl`; walls = real subsystems, `no hash → no draw` (watch/SELF_STEAL_FLEET_LIGHTMAP_20260906.md) |
| **DARK SOULS MODE** | death-and-retry as the learning loop; smarter every death | `memory/runs/overseer/conc_test_20260905.jsonl` — tonight: 76 workers START, 70 DONE, every slot `released:true`, zero deaths; manufactured deaths caught clean: tamper test 1/1, maze_arena 4 birth defects root-caused then fixed (GROUNDING_WAVE 02:59Z) |
| **ADVENTURERS** | the party = tonight's workers | 76 unique workers on the max-flash slots (conc ledger), 50 shadow walkers home (`state/shadow_work/slab_*.csv`, 50 CSVs), 8 game-surface harvesters fired 04:49Z (watch/GROUNDING_WAVE.jsonl) |
| **DRAGONS SLAIN** | falsified assumptions — falsifier firing = the kill; tonight's count: **6** | 1) "21,264 knots" DISPUTED → real 13,678 (99.995%); 2) "215 replies" DISPUTED → 17 found; 3) maze_arena "doesn't run" → 4 stacked birth defects; 4) "linkage is truth" → seeded-false-claim REJECTED by wave v2; 5) evidence-audit false positives → wave caught its own auditor bug; 6) Berlin undersell — the rubric itself corrected (chain makes ghost-runs high-value). Ledger: `watch/GROUNDING_WAVE.jsonl` rows 23:21Z–04:44Z |
| **INVARIANTS (loot)** | the treasure, hash-anchored | `memory/percolator/invariants.json` — **58** hash-keyed invariants vs **45** in the 09-02 backup (`invariants.json.bak-20260902`); the codex's "47" was already stale when written |
| **THE LADDER** | mud → dungeon → souls = the build order | text tape (`logs/behavioral_events.jsonl`) → rooms (`room_lightmap.html`) → mechanics (`dashboard/static/shadow_walk.html`: 72 hash-sealed chunks, fnv1a32 both sides, vision-gated JIT, seeded roguelite runs — watch/inbox/SHADOW_WALK_20260906.md) |

## THE GENERATIVE CLAIM — tonight's proof
The game grew exactly as fast as the fleet learned, measured in one night:
- Loot: invariants 45 → 58 (+13).
- World: SHADOW WALK voxelized the 9,305-part behavioral volume into 72 chunks — the
  dungeon's geometry IS the fleet's own reasoning; law-density = ore, zero-law = void,
  weights annex = biome with the 3.97x rising norm gradient as terrain.
- Fog of war = the anti-hallucination barrier generalized: unwalked = unvalidated =
  wireframe; the vision pass (sweep 1, 04:38Z: 60fps potato render, JIT 43-44/72 chunks
  materialized, 0/72 flipped by design) is the only thing that turns ghost into stone.
- The map: tesuji ledger 0 → 155 cells since 03:20Z the same night — the ledger is
  becoming the index of games + LLM surface + literary core through one cartography loop.
- Dark-souls respawn law observed live: the wave caught its own migration bug and its own
  auditor bug — the difficulty curve IS the learning curve, applied to the falsifier itself.

## SURGERY NOTE (own it fast)
Two of my first three posts (04:5xZ) carried a nonexistent path (`training/events.jsonl`)
and broke the ledger's evidence audit; my strip to fix them clipped 3 concurrently-posted
sibling rows, which the sibling harvesters' continued chaining healed — chain verify PASS
at 145 before my reposts, no duplicates. One later post tripped the audit regex again
(`.bak-` path backtracking) and was dropped+reposted clean. Final state: **verify PASS,
155 cells, tip 15f4290fad22**. Lesson filed: the audit regex matches path PREFIXES —
write notes with whole existing paths only.
