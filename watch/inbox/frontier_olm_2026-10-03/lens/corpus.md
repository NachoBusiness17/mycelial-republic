# LENS: corpus - what the estate's corpus already covers

- Written: 2026-10-03 (frontier_olm lens gopher). Rebuilt over an earlier same-day pass at this path: every number it carried was re-verified by my own runs before adoption; the four cut-level deltas it left are corrected below and named.
- Sources read: `catalog/catalog_manifest.json`, `catalog/catalog.jsonl` (all 917,885 rows, five passes), `catalog/tags.jsonl` (row 1 sample), `catalog/junctions.jsonl` (row 1 sample), `CORPUS_CATALOG.md`, `state/arxiv/2026-10-02/2610.00958v1.txt` (line 1).
- Counting moment: catalog snapshot_ts `2026-10-03T07:33:39Z` (`catalog/catalog_manifest.json:28`). Every count below is mine unless marked "manifest" or "CORPUS_CATALOG.md claim".

## How counted

`wc -l catalog/catalog.jsonl` read 917,885 lines; my JSON parse of all rows found 0 bad rows; row keys `id, path, bytes, mtime, zone, ext, title` present on all 917,885, `age_days` on 917,785 (missing on 100). Arithmetic check: `kind_counts` sum, `age_counts` sum, and `summary.tags_rows` 917,885 (`catalog/catalog_manifest.json:38`) all equal my line count; `map_bytes` 261,013,216 (`catalog/catalog_manifest.json:22`) equals the on-disk `catalog.jsonl` size exactly. Passes (all `./.venv/Scripts/python.exe <script>`, left beside this file for replay): `_count_corpus.py` (zones, top dirs, keyword overlaps), `_count_corpus2.py` (shelf substrings, research/ and the_margin_lean subtrees), `_count_corpus3.py` (library/oral/arxiv/memory-corpus/biography/research_packs), `_count_corpus4.py` (4th-level project cuts, pd_* clusters), `_count_corpus5.py` (self-record cuts, MB byte sums, intake zone check). `tags.jsonl` row 1 carries `"kind": "prose", "age_class": "aging"` - kind/age labels, not research domains, so domain counting is path-prefix based. Catalog paths are rooted one level above the repo (`local_sovereign_agent/...` prefix) except bare vault-zone files; on-disk checks from repo root drop the prefix.

Corrections to the earlier same-day pass (cut-level artifacts, mine supersede): `mine/` 97,869 (was 97,867), `logs/` 6,472 (was 6,405), `memory/agent_state` 41,590 (was 41,589), `oral_history/seat_pools` children 11,873 (was 11,871).

## Corpus shape

- Total rows 917,885. Zones (my pass): memory 484,843; lsa 301,566; runs 53,976; intake (= watch/inbox, verified: all 18,045 intake rows carry `watch/inbox` in path) 18,045; watch 4,681; queue 897; doctrine 794; code 688; dashboard 614; vault 135; research 93. Top dir `local_sovereign_agent` holds 866,627 rows (94.4%); 51,258 rows sit outside it.
- Kind mix is a manifest claim, not my count (config 509,397 / prose 89,985 / code 75,196 / ledger 40,232 / image 32,069 / corpus 1,776; catalog_manifest.json:8-21). Age mix also manifest: stale 385,198 / aging 283,566 / fresh 246,589 / fossil 2,532 (catalog_manifest.json:2-7).

## Research domains already covered (my counts)

**1. LLM/agent engineering courseware + cookbooks** - the largest external research block. `corpus/library` = 43,146 rows / 4,689.7 MB (my byte sum): ms-genai-beginners 12,142; ms-agents-beginners 9,429; zcode-zai-org 6,810; mod-playerbots 5,019; openai-cookbook 3,120 / 1,131.4 MB; lmcache-src 2,331; evennia 1,579; kev 934; hf-agents-course 435; second-brain-os 275; wotlk-db 226; anthropic-courses 224. CORPUS_CATALOG.md's `library` shelf claims 57,383 files / 6,957.0 MB (`CORPUS_CATALOG.md:18`) - a wider shelf mapping than my 4-level prefix; both disclosed, do not difference them.

**2. AI-in-games / game-server codebases** - sibling repos in the scan: azerothcore-wow 10,356 rows / 899.0 MB; vmangos-core 4,397; tortoise-wow 3,767 / 383.1 MB; plus mod-playerbots 5,019 + wotlk-db 226 + evennia 1,579 inside library; `corpus/dfhack_full` 2,123 (Dwarf Fortress modding); `memory/corpus/game_design_docs` 38; `memory/corpus/shadertoy21k` 21,806 (shader code).

**3. arXiv LLM research, daily full-text pulls** - `state/arxiv` 4,261 rows across 29 days, 2026-09-07 through 2026-10-02, ~230-254/day (top: 2026-09-16 254, 2026-09-07 253, 2026-09-22 252, 2026-10-02 250). Content spot-check mine: `state/arxiv/2026-10-02/2610.00958v1.txt:1` reads "# Role-aware Heuristic Episodic Attention for Conversational LLMs" (cs/CL).

**4. Canon / esoteric / alternative-knowledge** - `memory/corpus` 22,427 rows: shadertoy21k 21,806, ractors 310, mycology_canon 52, game_design_docs 38, training_pdfs 36, ai_canon 33, electronics_canon 30, esoteric_canon 23, moonshot_canon 21, quantized_thought 19, founding_law 14, augmentation_canon 9. Library holds small `pd_*` clusters (pd_physical_compute 154, pd_scifi 28, pd_siege_castle_fiction 18, pd_counter_enlightenment 7, pd_east_asian 7, pd_child_development 7, pd_oldbooks 6, pd_south_asian 5, pd_computing_history 4, pd_african_caribbean 3, pd_maths_history 2) plus ingersoll_lockwood 4. CORPUS_CATALOG.md shelves: `tartaria_lives` 11 files (`CORPUS_CATALOG.md:13`), `canon` 209 / 20.6 MB (`CORPUS_CATALOG.md:11`), `telegram` 2 (`CORPUS_CATALOG.md:14`).

**5. Oral history / estate biography** - `corpus/oral_history` 14,860 rows / 1,413.4 MB (seat_pools children 11,873: grok_sessions 11,674 + codex_sessions 193 + session_index 2 + marathon_body 2 + the_wall 2; nacho_archaeology extracted 2,969 + zip parts; 4 recovered single-file documents); `memory/biography` 71,151 + `memory/biography_backup` 297,112. CORPUS_CATALOG.md `oral_history` shelf claims 15,749 files / 1,423.9 MB (`CORPUS_CATALOG.md:15`).

**6. Frontier intelligence / receipts** - `watch/inbox` (zone intake) 18,045 rows / 6,620.3 MB by my count and zone check (CORPUS_CATALOG.md:19 claims 16,886 - same-day drift, both disclosed); `frontier_thinking` shelf 11 files (`CORPUS_CATALOG.md:17`); `memory/research_packs` 829 rows (largest: 20260920_matt_davey_black_swan); `memory/runs` 53,976; external AI archaeology `research/` subtree 767 rows (system_prompts_leaks_20260912 485, aitruthcode 121, cl4r1t4s 84, cl4r1t4s_upstream 77) and `corpus/` root 101 rows (papers_reference_nonredistributable 80, social_archive 17).

**7. Estate self-record (operational, not external research)** - agents/ 113,366; mine/ 97,869; memory/agent_state 41,590; memory/ghost 25,634; logs/ 6,472.

**Cross-cutting keyword overlaps (non-exclusive, one path can hit several; do not sum)** - rag/memory/retrieval terms 567,539; burn/cost/budget/ledger terms 25,055; local-llm/inference terms 14,522; verkle/merkle/proof terms 9,139; workflow/gate/lint terms 6,317; prompt/persuasion terms 5,833.

## Thin / absent domains (gap side, for the frontier sweep)

Counted near-zero coverage: formal mathematics (pd_maths_history 2), economics/markets (no top-level or shelf hits in my cuts), law/policy beyond founding_law 14, biology beyond mycology_canon 52, climate/energy (none), electronics hardware (electronics_canon 30). These are absences in my path-prefix tallies, not proof of absence outside the scanned tree (the catalog walks `Documents/projects/` siblings; anything outside that root is invisible to this lens).

## Reader takeaways for the olm

1. The corpus is deep on AI/agent engineering (courseware + arXiv daily pulls + game-server AI) - a frontier find in that space is likely already half-covered; grep `corpus/` before relearning.
2. The esoteric/canon shelf is curated but small (tens of files per canon) - depth lives in the estate's own synthesis, not in source volume.
3. Economics/markets, formal math, law, and climate are the genuinely open flanks - near-zero files counted.
4. Retrieval is ready for the sweep: `catalog_fts.sqlite` 266,641,408 bytes and `receipt_fts.sqlite` 38,929,197 bytes on disk (`ls -la catalog/`, this session), FTS refreshed 2026-10-03 09:00.
