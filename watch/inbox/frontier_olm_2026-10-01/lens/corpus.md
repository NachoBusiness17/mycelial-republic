# LENS: corpus, what the estate's corpus already covers

Lens gopher, 2026-10-01. Instrument: `.venv/Scripts/python.exe` counts over `catalog/catalog.jsonl` (691,788 rows parsed this session; snapshot_ts 2026-09-30T07:32:33Z, `catalog/catalog_manifest.json:28`; matches tags_rows 691,788 at `catalog/catalog_manifest.json:38`). Manifest kind mix: config 350,035 / code 72,365 / prose 71,924 / other 112,531 / image 31,865 / ledger 23,558 / receipt 11,254 / test 7,394 (`catalog/catalog_manifest.json:8-20`). Shelf cross-check: `CORPUS_CATALOG.md` run 2026-10-01T13:15:15Z (canon drift: 205 checked, 4 drifted, `CORPUS_CATALOG.md:5`). Where shelf-scan and catalog counts differ (library 57,380 vs 42,961; oral_history 15,749 vs 14,859) it is two instruments at two moments (10-01 scan vs 09-30 snapshot); both cited, never differenced (census denominator law, AGENTS.md).

## Domains the corpus already covers (my counts)

1. AI agent platforms + coding-agent source harvests (`local_sovereign_agent/mine/raw/`, 97,865 rows): `agent_platform` 72,329 (facebook 10,971, BerriAI 9,281, codestoryai 8,712, voideditor 8,179, meltylabs 7,504, anomalyco 6,303, cline 3,936, continuedev 2,923, OpenHands 1,956, openai 1,361, modelcontextprotocol 980, jj-vcs 681); `agent_bleeding_edge` 14,468 (incl. Google A2A protocol); `mesh_comm` 5,297; `steal_protocol` 4,118; `narrative_corpus` 1,653.
2. Agent/LLM curricula + API docs (`corpus/library/`, 42,961): ms-genai-beginners 12,142; ms-agents-beginners 9,429; zcode-zai-org (z.ai docs) 6,810; openai-cookbook 3,120; lmcache-src 2,331; hf-agents-course 435; anthropic-courses 224.
3. MMO private-server emulation (sibling repos): azerothcore-wow 10,356 + vmangos-core 4,397 + tortoise-wow 3,767 + mod-playerbots 5,019 + wotlk-db 226, sum 23,765; plus DFHack (Dwarf Fortress) 2,123 and evennia 1,579.
4. GPU/shader code: `memory/corpus/shadertoy21k/codes` 21,804 of shadertoy21k 21,806.
5. Formal math: `the_margin_lean` repo (mathlib4) 9,164 rows.
6. Session corpora / oral history: `corpus/oral_history/` 14,859 (grok_sessions 11,674, nacho_archaeology extracted 2,969, codex_sessions 193); `memory/ghost/` 22,356; telegram shelf 2 jsonl (gold_standard, MrPool_Q).
7. Estate self-history (`memory/`, 407,098 rows; zero under pytest-tmp, counted): biography 60,806 (knots 42,139, derived 9,287, residual 8,364); runs 51,805 (orchestrator 16,382, fleet_round 14,350, forge_daemon 5,389); briefs 6,206; mail 5,336; research_packs 799.
8. Web3/crypto: `reference/gstdcoin/` 1,381 (contracts, ai backend/frontend, gstdbot).
9. Esoterica + curated canon: ractors 310 (weird_prophetic 58, esoterica 52, cs_classics 49, scifi_pd 38, plato 22); canon dirs (mycology 52, ai 33, electronics 30, esoteric 23, moonshot 21, founding_law 14); tartaria_lives 11; frontier_thinking 11.

## Gaps (no catalog pocket found; absence-of-pocket, not proof of absence)

No domain pocket counted for: bioinformatics, chip/hardware design, robotics, climate/energy, medicine, econ/finance beyond gstdcoin, physics simulation. Frontier sweep should treat these as unmined ground.

## Instruction to the sweep

Any frontier find touching domains 1 through 3 or 6 through 7 likely duplicates estate knowledge: grep corpus first (prior-art sweep clause, `memory/rib/RIB_THE_DESCENT_PROTOCOL_20261001.md`).
