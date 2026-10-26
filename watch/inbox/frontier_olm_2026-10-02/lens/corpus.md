# LENS: corpus (what the estate's corpus already covers)

- Lens seat: lens-corpus (Mag Resource Harness, repo local_sovereign_agent)
- Moment: 2026-10-02
- Ask: which research domains the estate's corpus already covers, with real counts counted in-session
- Laws held: no fabrication; every count names its instrument; OWED marked, never asserted

## Method (what I actually ran)

1. Read `catalog/catalog_manifest.json` (45 lines) and `CORPUS_CATALOG.md` (33 lines) in full.
2. Sampled `catalog/catalog.jsonl` first 5 rows (fields per row: id, path, bytes, mtime, zone, ext, title, age_days).
3. Counted the whole file myself with this repo's venv interpreter (`.venv\Scripts\python.exe`, not bare python per AGENTS.md):
   - script `C:\Users\foste\AppData\Local\Temp\corpus_lens_count.py` (pass 1: totals, zones, top-level dirs, exts)
   - `C:\Users\foste\AppData\Local\Temp\corpus_lens_count2.py` (pass 2: two- and three-level dir drill, ext-by-dir, keyword substring probes over path+title lowercased)
   - `C:\Users\foste\AppData\Local\Temp\corpus_lens_count3.py` (pass 3: arXiv day span, state/library, targeted confirmations)
4. Cross-check that passed: the file is 246,509,780 bytes and my row count is 871,790 with 0 JSON parse errors; these match `catalog_manifest.json:23` (map_bytes 246509780) and `catalog_manifest.json:38` (tags_rows 871790) exactly. The corpus I counted is the manifest's own snapshot (`snapshot_ts` 2026-10-02T07:35:07Z, `catalog_manifest.json:28`).

All counts below are from these runs unless marked READ-ONLY.

## Corpus identity (counted)

- 871,790 catalog rows, 0 malformed lines, 154,140,858,404 bytes of filed content (sum of row bytes).
- Row zones: memory 439,964; lsa 300,935; runs 53,745; intake 17,831; external mirrors: Mag-backup.git 12,945; azerothcore-wow 10,356; the_margin_lean 9,164; vmangos-core 4,397; tortoise-wow 3,767.
- Top extensions: .json 471,695; .md 98,852; .jsonl 40,633; .ts 34,925; .py 31,092; extensionless 22,326; .fragment 21,800; .sql 13,277; .txt 12,304; .webp 12,238; .png 10,632; .tsx 9,370; .lean 9,061; .log 8,063; .cpp 5,184; .rs 5,124.

## Research domains covered (all counts mine, instrument noted)

1. **LLM / agent-engineering curriculum**: corpus/library 43,149 rows, led by ms-genai-beginners 12,142, ms-agents-beginners 9,429, zcode-zai-org 6,810, mod-playerbots 5,019, openai-cookbook 3,120, lmcache-src 2,331, evennia 1,579, kev 934 (three-level dir counts over catalog.jsonl). Notebooks: 4,044 .ipynb under corpus/library (4,378 total).
2. **Formal math / Lean theorem proving**: the_margin_lean/mathlib4 9,164 rows; .lean ext 9,061 total, 9,060 of them under mathlib4. Keyword "theorem" 40.
3. **WoW private-server engine stack**: azerothcore-wow 10,356 rows (data 7,671, src 1,768; 7,653 .sql), vmangos-core 4,397 (sql 2,656), tortoise-wow 3,767 (dep 1,664, src 1,212), plus corpus/library/mod-playerbots 5,019. DFHack game-tooling: corpus/dfhack_full 2,123 (782 scripts).
4. **Rust systems code**: 5,124 .rs rows, 5,103 under mine/raw.
5. **Reverse engineering / security tooling**: Ghidra 5,223 rows anywhere, corpus/tools/ghidra_12.1.4_PUBLIC 5,219.
6. **Oral history / seat-tape corpora**: corpus/oral_history 14,860 rows (seat_pools 11,871, nacho_archaeology 2,981); substring "oral_history" hits 14,861.
7. **Biography / memory estate (the fleet's own behavior data)**: memory/biography_backup 258,840, memory/biography 65,934 (knots subtree 44,817), memory/runs 53,746, memory/agent_state 41,559 (versions 41,518), memory/ghost 24,423 (leak_reports 24,377), memory/briefs 6,206.
8. **Graphics / shader corpus**: memory/corpus/shadertoy21k 21,806 rows (21,815 shadertoy hits anywhere).
9. **Watch/inbox findings archive**: 17,833 rows, led by qdrop_export 4,980 (4,983 qdrop hits anywhere), burn_reset_20260927 2,495, mrpool_export 2,852, model_garden 1,453, gala_20260925 1,251, burn_wave_20260926 860, frontier_olm_20260928 235 (the prior olm run).
10. **Daily arXiv pulls**: state/arxiv 4,260 rows across 28 distinct day directories, 2026-09-05 through 2026-10-02.
11. **Frontier-mine keyword density (substring over path+title, rows)**: verkle 4,990; frontend 580; fine-tun(ing) 569; quantiz(ation) 264; econom(ics) 191; myceli(al) 481; lora 131; alignment 118; reinforcement 108; quantum 84; kubernetes 33; tartaria 12; biolog(y) 15.
12. **Vendor docs mirrors**: docs/ref/zai_docs_mirror 105; docs/mirrors/mcp 46; docs/report_v1/sources 337.

## READ-ONLY numbers (read, not recounted by me)

- Manifest kind_counts (`catalog_manifest.json:8-20`): config 465,716; other 137,357; prose 88,205; code 75,123; ledger 40,063; image 32,069; receipt 12,856; test 8,797; brief 6,205; card 2,354. Age (`catalog_manifest.json:3-7`): stale 355,743; aging 263,467; fresh 250,094; fossil 2,486.
- Curated shelf table (`CORPUS_CATALOG.md:9-21`): library 57,383 files / 6,957.0 MB; watch_inbox 16,608 / 6,537.5 MB; oral_history 15,749 / 1,423.9 MB; docs_ref 377; canon 209; handoff 1,024. Drift banner (`CORPUS_CATALOG.md:5`): checked 205, missing 0, drifted 4, "resolve before trusting the shelves".

## Discrepancies I did not reconcile

- Shelf-table "library" 57,383 files vs my counted corpus/library 43,149 rows: different roots and/or moments (shelf run 2026-10-02T13:15:18Z, `CORPUS_CATALOG.md:3`, vs manifest snapshot 07:35:07Z). The catalog's own state/library subtree has only 10 rows, so the shelf root is not fully inside this catalog walk. Both numbers stand as reported by their own instruments.
- Corpus is memory-estate heavy: biography_backup alone (258,840 rows) is about 30% of all rows. Domain breadth is real but the center of mass is the fleet's own behavior record, not external science.

## Frontier-sweep implications

Already deep (do not re-mine): agent/LLM curriculum, Lean/Mathlib, WoW emulator stack, seat-tape/oral-history training data, shadertoy, Ghidra/RE tooling, arXiv daily freshness (28 consecutive days).

Thin by my keyword probes (candidate frontier targets): quantum 84, biology 15, Kubernetes 33, economics 191, formal alignment 118 rows are small against the estate's 871,790-row mass. Caveat: keyword substring over path+title undercounts content that never names its domain in the path; treat "thin" as a lead, not a verdict.

## OWED

- Nothing in this lens is asserted without a count or a cited read. No OWED items.
- Not run (out of scope for this ask): corpus FTS full-text search (`catalog/catalog_fts.sqlite` per AGENTS.md B2-465); title-text domain classification beyond substring probes; reconciliation of the shelf-table library count.
