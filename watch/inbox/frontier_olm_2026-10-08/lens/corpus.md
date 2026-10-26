# Lens: what the estate corpus already covers (frontier OLM 2026-10-08)

Seat: lens-corpus subagent. Ask: which research domains the corpus already covers, with counts counted here.

## Instrument (what I ran)

All counts in this file are catalog **rows** (JSON lines) I parsed myself from
`catalog/catalog.jsonl` and `catalog/tags.jsonl` in this session, using the repo venv
(`.venv\Scripts\python.exe`), via two throwaway counters in `%TEMP%` (`lens_corpus_count.py`,
`lens_corpus_count2.py`) that read the jsonl line stream and `collections.Counter` the fields
`zone`, `ext`, `path` prefixes, and `kind`. Sampled rows were read with
`Get-Content catalog\catalog.jsonl -TotalCount 3` (schema: id, path, bytes, mtime, zone, ext,
title, age_days) and `Get-Content catalog\tags.jsonl -TotalCount 2` (adds kind, age_class, owner).
The catalog snapshot is 2026-10-08T07:55:47Z (`catalog/catalog_manifest.json:28`), same day as
this lens. Counts are rows, not deduped unique files (manifest records 40,102 base_dups,
`catalog/catalog_manifest.json:33`).

## Scale

- **1,266,929 total catalog rows** (my count; equals manifest `summary.tags_rows`
  `catalog/catalog_manifest.json:38`).
- My kind recount from `catalog/tags.jsonl` (1,266,929 rows parsed) **matches
  `catalog/catalog_manifest.json:8-21` exactly**: config 756,052; other 177,449; prose 118,224;
  code 86,464; ledger 49,792; image 41,164; receipt 14,931; test 10,785; brief 6,205; card 2,525;
  corpus 1,782; state 1,556.
- Biggest logical zones (my count): memory 718,730; lsa 350,682; runs 56,625; watch 4,744;
  queue 962; research 95.
- Estate-internal mass is mostly its own operational history: `local_sovereign_agent/memory`
  775,411 rows; `/agents` 145,896; `/watch` 26,765 (my counts).

## Research domains already on the shelves (counts mine)

| Domain | Where | Rows (my count) |
|---|---|---|
| LLM/agent engineering curricula + vendor docs | `corpus/library/` | 52,313 (ms-genai-beginners 12,142; ms-agents-beginners 9,429; ai-engineering-from-scratch 5,401; openai-cookbook 3,120; hf-agents-course 435; anthropic-courses 224; second-brain-os 275; wotlk-db 226) |
| Frontier sweeps raw feed | `mine/raw/` | 97,865 |
| Oral history / seat archaeology | `corpus/oral_history/` | 14,860 (seat_pools 11,871; nacho_archaeology 2,981) |
| Agent-harness + serving source mirrors | `corpus/library/zcode-zai-org` 6,810; `lmcache-src` 2,331; `kev` 934 | 10,075 |
| Game-server / MMO-bot stacks (repos) | azerothcore-wow 10,356; vmangos-core 4,397; tortoise-wow 3,767; library_parked/sourceofmana 2,967 + agentmemory 781; plus in-library mod-playerbots 5,019; mixar 3,669; evennia 1,579 | 32,534 |
| Reverse engineering tools | `corpus/tools/` (ghidra_12.1.4_PUBLIC 5,219; JDK-21 490+315) | 6,029 |
| Dwarf Fortress scripting | `corpus/dfhack_full/` 2,123; `corpus/df_mine/` 25 | 2,148 |
| Formal math | `the_margin_lean/mathlib4/` (Lean 4 mathlib mirror; path sampled) | 9,164 |
| Papers (arXiv PDFs, nonredistributable) | `corpus/papers_reference_nonredistributable/` | 82 |
| Research-steal receipts | `corpus/steal/` | 72 |
| Curated canon + ribs | `corpus/canon/` 210; `corpus/ractor_ribs/` 36 | 246 |
| Fringe/social archive | `corpus/social_archive/` 17; `corpus/tartaria_lives/` 11; `corpus/telegram/` 2 | 30 |
| Frontier thinking docs | `corpus/frontier_thinking/` | 11 |
| Game estate notes | `corpus/game_estate/` | 15 |

External research dir outside the repo: top-level `research/` 767 rows (my count of zone
`ext:research`).

## Doc-stated numbers I did not recount (CORPUS_CATALOG.md)

`CORPUS_CATALOG.md` (run 2026-10-08T13:21:30Z, line 3) reports curated shelves at file+MB
granularity (library 66,715 files / 7,235.1 MB, line 18; oral_history 15,749 / 1,423.9 MB, line
15; watch_inbox 19,576 / 6,787.3 MB, line 19; canon 209, line 11; bulk layers attic 145 / logs
9,983 / state 6,987 / mag 2,473, lines 26-30). Its shelf counts use a different denominator
(files walked, incl. un-ingested) than my catalog rows, so 66,715 vs my 52,313 for library is
instrument drift, not contradiction. Its canon line flags DRIFT: checked 205, missing 0,
drifted 4 (line 5) - resolve before trusting canon shelves (same doc).

## Gap shape for the frontier sweep

Deep on: agent/LLM engineering, harness source, game-agent stacks, RE tooling, formal math
mirror, own operational history. Thin on: standalone arXiv paper mass (82), frontier-thinking
digests (11), social/fringe archive (30). The `mine/raw` 97,865-row feed is the bulk
research surface; corpus/library is the curated taught surface.

## OWED

- Nothing asserted here beyond what I counted or sampled this session; every number is a
  session count or marked doc-stated. I did not open individual library collections to verify
  their content beyond sampled paths (zcode-zai-org/repo/*, mathlib4/*, steal/*.md,
  frontier_thinking/FT001_*, papers/*.pdf, canon/*.md/png, oral_history/seat_pools/history.jsonl).
