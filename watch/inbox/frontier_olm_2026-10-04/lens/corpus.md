# LENS: corpus - what research domains the estate already covers

Moment: 2026-10-04. Sources read this session: `catalog/catalog_manifest.json` (snapshot_ts 2026-10-04T07:59:54Z, catalog_manifest.json:28), `CORPUS_CATALOG.md` (run 2026-10-04T13:16:49Z, CORPUS_CATALOG.md:3), samples of `catalog/catalog.jsonl` and its sibling `catalog/tags.jsonl`. Every count below is one I counted myself this session by running Python row-groupings over `catalog/catalog.jsonl` (repo venv, `./.venv/Scripts/python.exe`), unless flagged as read from a file.

## Baseline numbers (counted)

- `catalog/catalog.jsonl`: **1,040,765 rows** counted (`TOTAL_ROWS`), matching the manifest's `summary.tags_rows: 1040765` (catalog_manifest.json:38) and my row count of `catalog/tags.jsonl` (also 1,040,765). The manifest's `summary.base_rows: 917885` (catalog_manifest.json:34) is the incremental base, not the live row count.
- Row kinds (read from catalog_manifest.json:8-20): config 580,948; prose 101,174; other 163,588; code 79,263; image 39,804; ledger 41,129; test 9,450; receipt 13,709; brief 6,205; corpus 1,776; card 2,410; state 1,309. My own read of `catalog/tags.jsonl` confirms all 1,040,765 rows carry only keys id/path/zone/kind/age_class/bytes/owner: it is a kind+age classification, NOT topical tags. No `tags` field exists anywhere in it.
- Zones (counted): memory 552,942; lsa 301,924; runs 54,350; ext:lsa_reboot_staging 52,992; intake 18,972; watch 4,702; the rest smaller.
- Freshness census (catalog_manifest.json:5-7): aging 341,784 / fresh 278,661 / stale 417,347 / fossil 2,973. Manifest discloses mode incremental (catalog_manifest.json:25-27); CORPUS_CATALOG.md:5 flags DRIFT: 205 checked, 0 missing, 4 drifted.

## Research domains COVERED, with counted sizes (catalog.jsonl row groupings)

1. **AI/agent engineering curricula and vendor docs** - `corpus/library/` subtree, 43,603 rows total (counted): ms-genai-beginners 12,142; ms-agents-beginners 9,429; zcode-zai-org 6,810; openai-cookbook 3,120; hf-agents-course 435; anthropic-courses 224. Sum of those six: 32,160 rows. (Shelf headline: library 66,713 files / 7,235.1 MB, CORPUS_CATALOG.md:18.)
2. **WoW-emulator / game-server archaeology and playerbots** (the game_estate domain): azerothcore-wow 10,356; mod-playerbots 5,019; vmangos-core 4,397; tortoise-wow 3,767; evennia (MUD engine) 1,579; wotlk-db 226; game_estate 69. Sum: 25,413 rows.
3. **Oral history archive** - 14,862 catalog rows containing `oral_history` (shelf: 15,749 files / 1,423.9 MB, CORPUS_CATALOG.md:15).
4. **Formal research papers** - 228 catalog rows ending `.pdf` whose path contains `corpus/papers_reference_nonredistributable`, filenames are arXiv IDs (0706.1347.pdf through 0812.4360.pdf et al.); 80 of those rows sit directly under `corpus/`. Plus canon: 930 rows containing `canon/` (shelf: 209 files, CORPUS_CATALOG.md:11).
5. **Harness reverse-engineering ("steal")** - 1,775 rows under `corpus/steal/` (ZCode operating playbook, tether/fan-out studies; manifest corpus kind 1,776 at catalog_manifest.json:12 corroborates).
6. **In-repo research dirs** - 767 rows in the `ext:research` zone + 94 rows in `research/` proper: system_prompts_leaks_20260912 485; aiTruthCode 121; cl4r1t4s 84 + cl4r1t4s_upstream_20260912 77.
7. **Serving/runtime source** - lmcache-src 2,331 rows (KV-cache/offload engine source).
8. **Humanities, physical compute, and micro-shelves** (thin but present, all counted): kev 934; second-brain-os 275; pd_physical_compute 154; human-atlas 118; ractor_starter 113; image-blaster 97; interference-search 63; wakers 51 + wakers knowledge_debt 8; pd_scifi 28; pd_siege_castle_fiction 18; tartaria 22 rows (shelf: 11 files, CORPUS_CATALOG.md:13); frontier_thinking 22 rows (shelf: 11 files, CORPUS_CATALOG.md:17); pd_counter_enlightenment 7; pd_east_asian 7; pd_child_development 7; pd_oldbooks 6; pd_south_asian 5; ingersoll_lockwood 4; pd_computing_history 4; pd_african_caribbean 3; pd_maths_history 2.
9. **Docs/doctrine** - docs/ref 2,865 rows; ractor_ribs 72 rows (shelf: 36 files, CORPUS_CATALOG.md:12); telegram 2 files (CORPUS_CATALOG.md:14).

## Coverage verdict for the frontier sweep

Deep: agent/LLM curricula (32K+ rows), WoW-emulator + playerbot code (25K rows), oral history, harness steal-map, arXiv paper shelf (228 PDFs). Thin: inference-serving internals (one source tree, lmcache), and no dedicated shelf for RL/post-training, evals/benchmarks, or robotics/hardware (those exist only inside the paper PDFs and curricula, if at all). Maths/science micro-shelves run 2-7 rows each. Because `catalog/tags.jsonl` carries no topical tags, domain coverage is inferable only from paths and shelves, not from a tag index; the 4 drifted canon entries (CORPUS_CATALOG.md:5) are unresolved at write time.
