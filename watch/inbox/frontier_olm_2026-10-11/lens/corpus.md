# LENS: corpus - what the estate already knows (2026-10-11)

Instrument of record: `catalog/catalog.jsonl`, 1,136,889 rows, snapshot_ts 2026-10-11T08:51:55Z (`catalog/catalog_manifest.json:28`), incremental rescan (`catalog/catalog_manifest.json:26-27`), tags_rows 1,136,889 (`catalog/catalog_manifest.json:38`) = TAG_REPORT total 1,136,889 (`catalog/TAG_REPORT.md:5`). My own tally read the same total with 0 bad-JSON rows. Manifest drift flag: "checked 205, missing 0, drifted 4" (`CORPUS_CATALOG.md:5`).

## Method (all counts below counted this session)

- `wc -l catalog/catalog.jsonl` -> 1136889.
- `./.venv/Scripts/python.exe C:/Users/foste/AppData/Local/Temp/lens_corpus_count_20261011.py` (top-level + second-level path tallies, zone tallies).
- `./.venv/Scripts/python.exe C:/Users/foste/AppData/Local/Temp/lens_corpus_count2_20261011.py` (corpus/, memory/, watch/, mine/, research/, library_parked/, reference/, state/ subtallies).
- `./.venv/Scripts/python.exe C:/Users/foste/AppData/Local/Temp/lens_corpus_count3_20261011.py` (corpus/library, state/arxiv, memory/research_packs, corpus/steal drills + extensions).
- Sampled rows by hand: `catalog/catalog.jsonl:1-4` (schema: id/path/bytes/mtime/zone/ext/title/age_days).

## Research domains already covered (counts = my catalog.jsonl tallies)

1. **AI/agents engineering, vendor-curated** - `corpus/library/` 52,294 rows: ms-genai-beginners 12,142; ms-agents-beginners 9,429; zcode-zai-org 6,810; ai-engineering-from-scratch 5,401; openai-cookbook 3,120; lmcache-src 2,331 (KV-cache/LLM serving); evennia 1,579 (MUD server); hf-agents-course 435; anthropic-courses 224.
2. **Daily arxiv sweep** - `state/arxiv/` 5,508 rows, dated dirs 2026-09-05..2026-10-09, ~230-256/day (top dir 2026-10-08: 256; 2026-09-16: 254).
3. **Game/virtual worlds + bot AI** - azerothcore-wow 10,356; vmangos-core 4,397; tortoise-wow 3,767; library_parked/sourceofmana 2,967; corpus/dfhack_full 2,123 (Dwarf Fortress); mod-playerbots 5,000 (in corpus/library); wotlk-db 226; world-games-corpus 81; the-mountain 59; game_estate 15.
4. **Formal math** - the_margin_lean/mathlib4 9,164.
5. **Frontier intel / scrapes / steals** - research/ 767 (system_prompts_leaks_20260912 485, aiTruthCode 121, cl4r1t4s 84 + cl4r1t4s_upstream 77); memory/steal 141; corpus/steal 69 (45 files + onionclaw_review 24); reference/gstdcoin 1,542; library_parked/agentmemory 781.
6. **Estate's own research record** - watch/inbox 20,179; memory/research_packs 824 (plus named packs: matt_davey_black_swan 70, entity_morphology 5, agent_mesh_salon 5, ssi_ilya_dig 4); memory/biography + biography_backup 577,859; memory/runs 56,432; corpus/oral_history 14,858; memory/briefs 3,980; memory/improve 844.
7. **Domain extensions** - corpus/library+state/arxiv extensions: .webp 12,219, .md 8,215, .py 6,351, .txt 6,260, .ipynb 4,044, .ts 3,549, .sql 2,130, .cpp 1,338.

## Instrument mismatch, disclosed

CORPUS_CATALOG.md shelf table reads library 66,715 files / 7,235.1 MB (`CORPUS_CATALOG.md:18`); my catalog.jsonl tally of `corpus/library/` reads 52,294. Different instruments: the rescan excludes 3,018 machinery dirs (`catalog/catalog_manifest.json:34`); the Librarian shelf walk ("The Librarian records; it never cleans", `CORPUS_CATALOG.md:32`) does not. Do not difference them.

## Gaps (absence claims bounded to the prefixes I counted)

Nothing in the tallied prefixes covers: ML systems benchmarks (mlperf et al.), peer-reviewed safety/alignment venues beyond the raw arxiv sweep, robotics/embedded, or non-English corpora. The arxiv sweep is raw dated drops with no visible topic index inside this catalog; topical curation lives downstream (memory/research_packs is thin at 824 rows vs 5,508 arxiv rows). These are bounded claims from path prefixes only; I did not grep titles.

## OWED

Nothing owed: every number above was counted this session; cited shelf/manifest figures are quoted with their own instrument named.
