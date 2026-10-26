# lens: corpus - what the estate's corpus already covers

Ask: read catalog/catalog_manifest.json, sample catalog/catalog.jsonl, CORPUS_CATALOG.md; name the research domains already covered, with real counts counted by the lens itself.

Method: one aggregation pass over catalog/catalog.jsonl with `.venv\Scripts\python.exe` (git-bash heredoc, 2026-09-28 evening), counting rows by path prefix and named subdir. Every number below is from that pass unless marked otherwise.

Grounding checks run this ask:
- `wc -l catalog/catalog.jsonl` = 581,477 rows; equals manifest `summary.tags_rows` 581,477 (catalog/catalog_manifest.json:38) and tags.jsonl row count.
- catalog.jsonl byte size 160,053,773 == manifest `map_bytes` 160,053,773 (catalog/catalog_manifest.json:22).
- Manifest snapshot_ts 2026-09-28T07:33:37Z (catalog/catalog_manifest.json:28); counts are rows as of that snapshot plus same-day drift, not a live walk.

## Domains covered (rows counted by this lens in catalog/catalog.jsonl)

1. **LLM / agent engineering course libraries** (`local_sovereign_agent/corpus/library/`, 41,840 rows): ms-genai-beginners 12,142; ms-agents-beginners 9,429; zcode-zai-org 6,810; mod-playerbots 4,191; openai-cookbook 3,120; lmcache-src 2,331; evennia 1,579; kev 934; hf-agents-course 435; second-brain-os 275; anthropic-courses 224; human-atlas 118.
2. **Frontier-lab platform scrape** (`mine/raw/`, 97,865 rows): agent_platform 72,329 (facebook sapling tree), agent_bleeding_edge 14,468, mesh_comm 5,297, steal_protocol 4,118, narrative_corpus 1,653.
3. **Session oral history** (`corpus/oral_history/`, 14,858 rows): seat_pools/grok_sessions 11,674; nacho_archaeology/extracted 2,968; seat_pools/codex_sessions 193. The Librarian's shelf ledger (state/library/catalog.jsonl row, shelf=oral_history) says 15,747 files / 1,423.9 MB; CORPUS_CATALOG.md:15 agrees. Catalog rows vs shelf files differ by scan scope/moment; both stated.
4. **GPU shader code** (`memory/corpus/shadertoy21k/`, 21,806 rows, .fragment/.vert GLSL).
5. **Formal mathematics / Lean** (top-level repo `the_margin_lean/mathlib4`, 9,164 rows).
6. **WoW server emulation source** (top-level repos): azerothcore-wow 10,356; vmangos-core 4,397; tortoise-wow 3,767; plus mod-playerbots 4,191 under corpus/library (bot AI for player characters).
7. **Canon shelves** (`memory/corpus/`, 25 dirs, 22,410 rows total incl. shadertoy): ractors 310; mycology_canon 52; game_design_docs 38; training_pdfs 36; ai_canon 33; electronics_canon 30; esoteric_canon 23; moonshot_canon 21; founding_law 14; augmentation_canon 9; quantized_thought 9; plus 15 smaller dirs.
8. **System-prompt / AI-safety forensics** (`research/`, 767 rows): system_prompts_leaks_20260912 485; aiTruthCode 121; cl4r1t4s 84 + cl4r1t4s_upstream_20260912 77.
9. **arxiv pulls** (`state/arxiv/<date>/`, 3,306 rows; dated batches of roughly 239 to 254 rows per day, 2026-09-07 through 2026-09-25 visible in top clusters).
10. **Teaching corpus** (`teach/f_01..f_10/`, 366 rows).
11. **Frontier thinking notes** (`corpus/frontier_thinking/`, 11 rows; FT001_zai53_research_restock + FT_ASTRA_DOOR series, 2026-09-04/05).
12. **Receipt/landing zone** (`watch/inbox/`, 11,837 rows in the main map).
13. Whole-repo self-map: `local_sovereign_agent/` holds 543,361 of 581,477 rows; memory/ 311,514; agents/ 35,265.

## The Librarian's shelf view vs the main map

CORPUS_CATALOG.md:9-21 (run 2026-09-28T13:15, "CANON MANIFEST: VERIFIED (205 hashes match)", CORPUS_CATALOG.md:5) shows 11 curated shelves: canon 209 files, ractor_ribs 36, tartaria_lives 11, telegram 2, oral_history 15,747, game_estate 14, frontier_thinking 11, library 55,915 / 5,611.4 MB, watch_inbox 11,960 / 6,345.4 MB, docs_ref 365, handoff 1,024. Shelf ledger rows (state/library/catalog.jsonl) carry shelf/path/files/bytes and confirm library=55,915 files at corpus/library and oral_history=15,747 at corpus/oral_history. The library shelf (55,915 files) exceeds the 41,840 rows the main map carries for corpus/library: the Librarian scans files the main map does not include (or added after snapshot_ts). Both numbers are real; instruments differ. Not reconciled this ask (stated, not guessed).

## What the corpus does NOT cover (honest gaps for the frontier sweep)

- No biology, economics, or cryptography research corpora: noisy substring hits (bio 157,019 mostly inside "library", rl 13,104 inside "url/world", quantum 19, market 142, crypto 210) were inspected and rejected as path-overlap artifacts, not domains.
- No dedicated security-research or ML-paper library beyond the small arxiv pulls (3,306 rows) and canons above; arxiv intake is ~250 rows/day, not a back catalog.
- Deep coverage is: agents/LLM engineering, game servers, formal math, shaders, and the estate's own oral history. Anything outside those axes is greenfield for the frontier sweep.

## Caveats

- Counts are catalog rows (one file = one row) at manifest snapshot 2026-09-28T07:33:37Z plus same-day append drift; not re-walked live.
- Substring-count pass ran first; only prefix/subdir counts that survived inspection are reported above.
- mtime/age fields were read (catalog row schema: id, path, bytes, mtime, zone, ext, title, age_days) but age distributions were taken from the manifest, not recounted.
