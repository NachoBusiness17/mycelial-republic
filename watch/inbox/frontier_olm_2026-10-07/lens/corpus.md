# Lens: corpus - what the estate already covers (frontier OLM 2026-10-07)

Method: all counts below are aggregations I ran this session over the live catalog with the repo venv:
`.venv\Scripts\python.exe -c ...` iterating `catalog/catalog.jsonl` and `catalog/tags.jsonl` line-by-line (json.loads per row, Counter aggregation). Catalog snapshot `2026-10-07T07:38:28Z` (catalog_manifest.json:28), incremental mode (catalog_manifest.json:26-27).

## Corpus size (counted)

- **1,195,926 rows** in `catalog/catalog.jsonl` (line-iteration count; manifest agrees: `tags_rows: 1195926`, catalog_manifest.json:38; summary `base_rows: 1130965` + `added: 55461` net of `vanished: 230530`, catalog_manifest.json:33-40).
- Kind distribution from `catalog/tags.jsonl` (1,195,926 rows scanned): config 698,188; other 175,390; prose 112,297; code 85,416; ledger 46,326; image 41,141; receipt 14,640; test 10,588; brief 6,205; card 2,505; corpus 1,781; state 1,449. Byte-identical to manifest `kind_counts` (catalog_manifest.json:8-21).
- Extensions (catalog.jsonl): .json 704,304; .md 124,141; .jsonl 47,171; .fragment 43,600; .py 41,168; .ts 36,129; .png 16,676; .txt 14,977; .sql 13,285; .webp 12,242.
- Zones: memory 664,668; lsa 334,790; ext:lsa_reboot_staging 56,343; runs 56,176; intake 20,374; watch 4,724.

## Research domains already on the shelves (counted)

Second-level dir counts (catalog.jsonl, `local_sovereign_agent/` prefix stripped):

| domain | dir | files |
|---|---|---|
| Biography / operator lifelog (bulk layer) | memory/biography_backup + memory/biography | 541,706 |
| Run ledgers / self-telemetry | memory/runs | 56,177 |
| General library | corpus/library | 52,316 |
| Agent state / ghost / sessions | memory/agent_state + memory/ghost + memory/agent_sessions | 94,058 |
| Oral history + social archive | corpus/oral_history (14,860) + corpus/social_archive (17) | 14,877 |
| Inbox receipts / work products | watch/inbox | 20,376 |
| ArXiv paper stash | state/arxiv | 4,998 |
| Tools/tooling corpora | corpus/tools | 6,029 |
| DFHack (Dwarf Fortress modding) | corpus/dfhack_full | 2,123 |
| GSTD dogfood + vast + fuel | state/gstd_full (1,038), state/vast (79), state/fuel (261) | 1,378 |
| Canon shelf | corpus/canon | 210 |
| Research packs + steals | memory/research_packs (834) + memory/steal (141) | 975 |
| Frontier/AI-safety research drops | research/system_prompts_leaks_20260912 (485), research/aiTruthCode (121), research/cl4r1t4s (84+77) | 767 |
| Docs | docs/ref (377) + docs/report_v1 (339) | 716 |

Game-engine estates (counted as top-level dirs): azerothcore-wow 10,356; vmangos-core 4,397; tortoise-wow 3,767; library_parked 3,748; the_margin_lean 9,164.

## What state/arxiv actually covers (4,998 files, title-sampled 14)

Titles sampled rows 1-14 of the zone: RLVR/data-efficient RL for LLMs ("DE-Venus"), gradient-aligned rewards for LLM reasoning, logit-based pre-training distillation ("ALRA"), adaptive latent reasoning ("RecurTrace"), symplectic/neural flows for orbital integration, self-consistency dynamical simulation, GPU symbolic regression via genetic programming, Grassmann-Plucker convolutional subspace parametrization, compact-embedding private retrieval ("Spruce", PIR), protein sequence/structure codesign ("SimpleDesign"), hybrid diffusion storm-surge synthesis, low-resource LLM ecosystems (Armenian).

## Read, not counted (cite the doc)

- CORPUS_CATALOG.md:9-21 curated shelves: library 66,715 files / 7,235.1 MB; watch_inbox 19,188 / 6,765.1 MB; oral_history 15,749 / 1,423.9 MB; canon 209 / 20.6 MB; frontier_thinking 11; tartaria_lives 11; telegram 2; docs_ref 382.
- CORPUS_CATALOG.md:24-31 bulk layers: logs 10,239 files / 12.25 GB; attic 145 / 3.2 GB; state 6,731; mag 2,422.
- Health flag: CANON MANIFEST: DRIFT - checked 205, missing 0, drifted 4 (CORPUS_CATALOG.md:5); run stamped 2026-10-07T13:19:27Z (CORPUS_CATALOG.md:3).

## Implication for the frontier sweep

Deep local coverage: RL/LLM training methods, dynamical systems, symbolic regression, PIR/private retrieval, protein codesign, diffusion, MMO/game-engine estates, oral-history archiving, operator biographics, AI-safety/system-prompt leak research. Weak by count: frontier_thinking (11 files), corpus/canon (210), tartaria_lives (11) - narrow shelves, not domains; the sweep should not re-derive what state/arxiv already banks (4,998 paper files), and the 4 drifted canon entries (CORPUS_CATALOG.md:5) should be resolved before those shelves are trusted.
