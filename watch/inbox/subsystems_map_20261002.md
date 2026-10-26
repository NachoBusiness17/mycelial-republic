# SUBSYSTEMS MAP 2026-10-02 (self-steal: the estate's first organ atlas)

Mission: name the actual subsystems of local_sovereign_agent; nobody had written
this map. Read-only except this receipt. Instruments: `git ls-files` + `wc -l`
+ `ls` + grep = **ugrep 7.8.4 WIN64** (its Windows output inserts a `\` between
dir and file; `mag/\x.py` below means `mag/x.py`). Moment: 2026-10-02.

Headline: `git ls-files 'mag/*.py' | wc -l` = **1,084 py files under mag/,
nearly all FLAT** (only mag/hermes_personas 11, mag/cli 3, mag/watch 2,
mag/tests 2, mag/ontology_compiler 1 are dirs; loop over `git ls-files mag/`).
Prefix census `git ls-files 'mag/*.py' | sed -e 's|^mag/||' -e 's|_.*||' | sort
| uniq -c | sort -rn`: top families game 32, corpus 22, ghost 19(+ghost.py),
swarm 19, ox 17, grok 16, voice 13, desk 13, frontier 12, session 11, seat 11,
rib 10, flock 10, agent 10; then a long singleton tail (~600 files, OWED).
Other roots: tools/ 426 tracked, scripts/ 241, tests/ 500 py on disk
(`ls tests/*.py | wc -l`; AGENTS census claims 455 files 2026-09-30),
memory/ 24,453, watch/ 18,819 (inbox: 1,108 .md), docs/ 829, dashboard/ 400,
corpus/ 503, configs/ 97, queue/ 86, roblox/ 70, server/ 19, catalog/ 14.
Receipt-mention counts: `grep -rli TERM watch/inbox --include='*.md' | wc -l`.

## Subsystem table (19; VERIFIED = byte-cited here, INFERRED = my grouping)

| # | Subsystem | Purpose | Primary organs | Size (files + LOC) | Liveness | Consumers | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | CLI front door | one entrypoint, 190+ subcommands | main.py (5,460 ln, 193 `add_parser`), mag/cmd via mag.cmd, mag/cli/ (3 f, 340 ln), mag/doctor.py | 6+ f / ~6k | regen: tools/regen_front_door.py renders docs/FRAMEWORK_LOAD.md (contract at its L162-179) | every seat (AGENTS load order #8) | VERIFIED |
| 2 | Verkle chain + seals | integrity tip over residual | mag/verkle_*.py (8 f, 3,115 ln), tools/verkle_dangling_repair.py, tools/verkle_restore_prep.py | 10 f / ~3.4k | tests: 6 test_verkle* + test_ag5_tip_verify (AGENTS); 623 inbox receipts | 97 py files match mag.verkle import grep | VERIFIED |
| 3 | Ghost-self + agent state | persistent self across windows | mag/ghost*.py (20 f, 9,771 ln), memory/agent_state/{LATEST.md,chain.jsonl,tip.json} | 20 f / 9.8k | FRAMEWORK_LOAD L41-45 tips it; 477 receipts | afk_loop.py, afk_orchestrator.py, ask_router.py, ai_landscape.py (grep mag.ghost) | VERIFIED |
| 4 | Hermes dispatch + burn | funded-tier driving ladder + personas + warm boot | mag/hermes_warm_boot.py (docstring L9-12: writes memory/warm_state.json), mag/hermes_personas/ (11: plato, fen, diogenes...), tools/hermes_burn.py | 14 f / ~1k | 694 receipts; memory/rib/RIB_DRIVING_LADDER_20260928.md; tests use ah* prefix (see N4) | main.py descend; AGENTS warm-boot order | VERIFIED |
| 5 | Rib memory (laws) | frozen operator law cards | mag/rib_*.py (10 f, 1,763 ln), memory/rib/ (52 md) | 62 f / ~2k | AGENTS cites RIB_THE_DESCENT_PROTOCOL_20261001.md etc. | 78 py files word-match `rib` (approx) | VERIFIED |
| 6 | Context packs + briefs | min-token seat packs, bonds, biography | mag/context_*.py (5 f, 2,755 ln), mag/bonds.py, mag/biography.py (638 ln), memory/briefs/ (FROZEN per AGENTS) | 7 f / ~3.4k | tests: 5 test_context*; mag.cmd context-pack/brief/bonds (AGENTS) | main.py + mag.cmd card | VERIFIED |
| 7 | Corpus + catalog + FTS | acquired knowledge store, searchable | mag/corpus_*.py (22 f, 5,719 ln), catalog/ (14 f: catalog.jsonl + catalog_fts.sqlite + junctions.jsonl), corpus/ (503 f: canon, dfhack_full, library, oral_history), tools/corpus_fts_rebuild.py | 540 f / ~6k py | MagFtsIndexDaily 09:00 (AGENTS); 1,273 receipts | ai_landscape.py, corpus_acquire.py, corpus_gap_research.py (grep mag.corpus) | VERIFIED |
| 8 | Shared surface (inbox) + switchboard + effect broker | durable cross-client landing + effect authorization | watch/inbox/ (SHARED_SURFACE_CONTRACT.json "purpose" key: "One durable landing zone..."), mag/shared_surface.py (447 ln), mag/switchboard.py (828), mag/effect_broker.py (890) | 3 f / 2.2k + inbox 1,108 md | 278/183/63 receipts; tests test_receipt_xref_gate, test_effect_broker_ah18 | board_directive.py, auth_switchboard.py, organ_map.py, routing_concert.py, spider.py (grep mag.switchboard) | VERIFIED |
| 9 | Queue + lanes + autorun | in-tray, worker lanes, plan drainer | mag/queue_*.py (5 f, 1,300 ln), mag/lanes.py (316), mag/autorun*.py (2 f), queue/ (86 f: lanes/ 13, handoff/, results/), configs/lanes.yaml | 93 f / ~1.9k py | tests: 3 test_queue*; main.py queue, queue-ops, probe-lanes, autorun | main.py commands + AGENTS escalation card | VERIFIED |
| 10 | Improve loop + promote | scout/eval/promote self-betterment | mag/improve.py + mag/improve/ (2 f, 3,114 ln), memory/improve/ (SEATS.md, HABIT.md, GOAL.md, MIRROR.md), MagImproveDaily 08:00 | 2 f / 3.1k + seeds | tests: 6 test_improve*; gates.jsonl feeds front door (FRAMEWORK_LOAD L168-170); 610 receipts | mag.cmd improve/promote; front-door regen | VERIFIED |
| 11 | Build-discipline gate stack | pre-push ratchet + citation + census + workflow gates | tools/workflow_gate.py, tools/violation_ratchet.py, tools/citation_lint{,_io,_numbers}.py, tools/census_drift_patrol.py, tools/freshness_check.py (8 files summed = 2,858 ln), githooks/ | 11 f / ~2.9k | AGENTS Build discipline block; memory/workflows/REGISTRY.jsonl | githooks/pre-push; every push | VERIFIED |
| 12 | Seat fleet + swarm + frontier | multi-seat fan-out, flocking, paid climbs | mag/seat_*.py (11 f, 3,183), mag/swarm_*.py (19 f, 4,621), mag/flock_*.py (10 f, 2,304), mag/frontier_*.py (12 f, 2,889), queue/lanes/ (elder, forge, harvest...) | 55 f / 12.6k | tests: 6 swarm, 3 frontier, 4 seat; 815 swarm receipts | 123 py word-match `swarm` (approx); fan-out-width law (AGENTS) | VERIFIED (grouping INFERRED) |
| 13 | Game estate (Mountain) | DFHack/WoW/worldgen games + world server | mag/game_*.py (32 f, 14,591 ln), mag/water_*.py + hydrology.py (4 f, 1,778), server/ (19 f; README L1-21 "THE ESTATE'S OWN WORLD SERVER v0", imports mag.water_graph.WaterGraph), roblox/ (70 f; README L1 titles it THE MOUNTAIN, the estate on Roblox; its title byte carries an em-dash, paraphrased here per hook law) | 125 f / ~17k py | tests: 14 game + 6 water + 5 mountain + 6 wow; 516 water receipts | server/world.py -> mag.water_graph (server/README.md L19-20) | VERIFIED |
| 14 | X + Grok sensing | free/funded external sensing lanes | mag/x_*.py (8 f, 1,913 ln), mag/grok_*.py (16 f, 4,196) | 24 f / 6.1k | AGENTS: grok-4.7 funded on XAI_SD_API_KEY; main.py grok-free, grok-mirror, grok-terminal | mag/grokbot*, mag/clawbot.py; steering consumes | VERIFIED files, INFERRED split from sensing/judgment |
| 15 | Voice + salon + personas | TTS/voice desk, staged conversation | mag/voice_*.py (13 f, 4,972 ln), mag/salon*, mag/chan.py, queue/phonesalon_runs.jsonl | 15+ f / ~5k | tests: 5 test_voice*; main.py tts; .agents/skills/salon + chan | 18 py word-match `voice` (approx) | INFERRED grouping, VERIFIED organs |
| 16 | Dashboard / desk UI | :8765 office window | dashboard/ (400 f: rest.py 5,553 ln, server.py 1,231, lan_proxy.py 370, static/), mag/desk_*.py (13 f, 4,589), dashboard-deploy/ | 414 f / ~11.5k py | tests: 8 desk; mag.cmd lab "product UI :8765" | operator + mag.cmd lab | VERIFIED |
| 17 | Local Ollama fleet + GPU | cheap janitors, vram budgets | mag/ollama*.py (1 f, 120 ln), mag/local_*.py (5 f, 1,547), mag/gpu_*.py (4 f, 799), mag/vram_*.py (2) | 12 f / ~2.7k | tests: 3 test_local*; AGENTS "local Ollama janitors first" | switchboard routing (INFERRED) | VERIFIED files |
| 18 | Steering + trajectory | retrocausal steering, session steering | mag/steer_*.py (9 f, 1,774 ln), mag/trajectory_*.py (4 f), queue/steer_agent.md, .agents/skills/retrocausal-steering | 14 f / ~2.5k | tests: 3 test_steer*, 3 test_trajectory*; main.py steer | 45 py word-match `steer` (approx) | VERIFIED organs, INFERRED merge |
| 19 | Cost + usage ledger | burn accounting, quota, rates | mag/cost_*.py (6 f, 1,954 ln), mag/usage_*.py (3 f, 699), configs/cost_rates.yaml, memory/runs/hermes_burn/usage.jsonl | 10 f / ~2.7k | tests: 4 cost + test_cost_rollup (AGENTS); DESCENT leg 8 banks here | hermes_burn carrier (AGENTS) | VERIFIED |

## Dependencies sketch (grep-derived, arrow = calls/imports)

- main.py -> mag/cli + every command family (193 add_parser). Front door
  (docs/FRAMEWORK_LOAD.md) is RENDERED by tools/regen_front_door.py from
  memory/improve/releases/gates.jsonl + memory/agent_state/LATEST.md (its L168-170).
- server/world.py -> mag.water_graph.WaterGraph (server/README.md L19-21:
  "one hydraulic truth in the estate, not two").
- ghost family consumed by afk_loop, afk_orchestrator, ask_router (grep mag.ghost);
  switchboard consumed by board_directive, auth_switchboard, organ_map,
  routing_concert, spider (grep mag.switchboard); verkle: 97 importing files
  (widest internal dependency); corpus consumed by acquire/research lanes.
- Gates: githooks/pre-push -> violation_ratchet + citation_lint + workflow_gate
  + census_drift_patrol (AGENTS Build discipline); workflow_gate writes
  memory/workflows/REGISTRY.jsonl; census patrol re-checks the AGENTS.md carrier
  line (parse_carrier, B2-249).
- Hermes dispatch -> ribs (RIB_DRIVING_LADDER) + burn ledger (usage.jsonl) +
  warm_state.json; claritas (mag/claritas.py, 100 ln) is imported by
  tools/hermes_burn.py, tools/model_garden.py, tools/build_seed.py,
  tools/cold_boot_test.py (grep claritas) = the prompt-face shared library.
- Improve loop -> memory/improve seeds -> promote gate -> releases/gates.jsonl
  -> front door regen (a closed loop, VERIFIED by FRAMEWORK_LOAD regen contract).

## Naming inconsistencies (evidence for the naming lane)

- N1 `surface` = 4 senses: (a) shared-inbox contract
  watch/inbox/SHARED_SURFACE_CONTRACT.json ("schema": "shared_surface.v1");
  (b) external client adapters mag/x_surface.py, mag/swarm_surface.py,
  mag/ecosystem_surface.py (12+ mag files contain "surface");
  (c) queue lane queue/lanes/android_surface; (d) .agents/skills "android surface".
- N2 `lanes` = 2 senses: escalation tiers configs/lanes.yaml + mag/lanes.py
  (AGENTS "L2 escalate ... see configs/lanes.yaml") vs worker lanes queue/lanes/
  (13 dirs: elder, forge, harvest, economist...). main.py probe-lanes touches both senses.
- N3 `dashboard` vs `desk`: dashboard/ (400 f) + dashboard-deploy/ vs mag/desk_*.py
  (13 f) + mag.cmd "lab ... product UI :8765" (AGENTS calls it "Office dashboard").
- N4 `hermes` vs `ah`: zero tests/test_hermes* (`ls tests/ | grep hermes` empty)
  but Hermes work rides ah-prefixed tests: tests/test_ah5_warmboot.py,
  tests/test_ah19_append_leaves.py, tests/test_effect_broker_ah18.py; zero
  mag/ah*.py modules exist (the prefix lives only in test names).
- N5 `ghost` vs `agent_state`: modules mag/ghost.py + mag/ghost_*.py (20 f) but
  state lives in memory/agent_state/LATEST.md whose tip line reads "ghost-self"
  (FRAMEWORK_LOAD L41). Two vocabularies, one actor.
- N6 three knowledge stores with near-synonyms: catalog/ (catalog.jsonl + FTS),
  corpus/ (raw acquisitions), memory/agent_corpus/ (per-agent). mag/catalog*.py
  (6 f) vs mag/corpus_*.py (22 f) split management across both.
- N7 `board`: container path /board/inbox (AGENTS table) vs mag/board_directive.py
  vs the same directory called "watch/inbox" on host: one surface, three names
  (the contract file itself canonicalizes all three, SHARED_SURFACE_CONTRACT.json
  "canonical" block).
- N8 root artifact: tracked file "C\357\200\272UsersfosteAppDataLocalTemplane_a12_commits.txt"
  (fancy colon U+F03A where a Windows path separator belonged) - a path-join bug
  fossil at repo root (`git ls-files | grep -F '\'` = exactly this one).

## OWED (honest)

- LOC for directory subsystems (dashboard/static, roblox lua: `find roblox
  -name '*.lua' | wc -l` = 0 tracked lua seen, place is src/ + rbxlx; corpus
  docs) not summed; only py LOC measured.
- Consumer counts from word-match greps (`swarm` 123, `surface` 83, `seat` 55,
  `rib` 78) are upper bounds: they match prose and cross-sense names (N1/N2).
- ~600 singleton mag/ modules (one-file prefixes) unmapped; a per-file
  dendrogram + which are dead (unimported) is owed.
- Runtime wiring of game/roblox/server verified static only (README + imports);
  no process was started.
- tests/ has 500 py on disk vs AGENTS 2026-09-30 census claim 455 files; drift
  attribution not re-run here (census patrol owns it).

FILE: subsystems_map_20261002.md · lane: research self-steal · instruments:
git ls-files, wc -l, ls, ugrep 7.8.4 WIN64 · commitment: subsystems-atlas-20261002
