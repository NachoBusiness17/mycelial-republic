# CORPUS LENS - frontier_olm 2026-09-30

Seat: lens-corpus gopher. Sources read this ask: `catalog/catalog_manifest.json`, sample of `catalog/catalog.jsonl` (first 3 rows), `CORPUS_CATALOG.md`.

## What I counted myself (not copied)

Command: `.venv/Scripts/python.exe <tmp script>` full pass over `catalog/catalog.jsonl` (two passes; script in `%TEMP%\lens_corpus_count.py`, `lens_corpus_count2.py`).

- **Total rows: 691,788** (my count; 0 unparseable lines). Cross-checks: manifest `summary.tags_rows: 691788` (`catalog/catalog_manifest.json:38`) and hand-summed `kind_counts` also equal 691,788 (`catalog/catalog_manifest.json:8-21`). The three instruments agree.
- **By zone (scan root, my count):** memory 355,237; lsa (this repo) 224,279; runs 51,805; intake 14,731; ext:azerothcore-wow 10,356; ext:the_margin_lean 9,164; ext:vmangos-core 4,397; ext:tortoise-wow 3,767; ext:research 767; research 91; watch 4,607.
- **Under `local_sovereign_agent/` (my count, 653,537 rows):** memory 407,098; mine/raw 97,865; corpus 60,375; agents 43,824; watch 20,566; logs 5,905; state 4,339; handoff 1,026; docs 578; canon 107; research 92.
- **`corpus/` third-level (my count, top rows):** library/ms-genai-beginners 12,142; oral_history/seat_pools 11,870; library/ms-agents-beginners 9,429; library/zcode-zai-org 6,810; library/mod-playerbots 5,019; library/openai-cookbook 3,120; oral_history/nacho_archaeology 2,981; library/lmcache-src 2,331; library/evennia 1,579; library/kev 934; dfhack_full/* ~1,760 visible; library/hf-agents-course 435; library/second-brain-os 275; library/wotlk-db 226; library/anthropic-courses 224.
- **`state/` (my count):** state/arxiv 3,776 rows; state/fuel 189; state/vast 77.
- **Extensions (my count):** .json 355,894; .md 81,339; .ts 34,913; .py 27,401; .jsonl 23,757; .fragment 21,800; .sql 13,276; .lean 9,061; .cpp 5,157.

## Research domains the corpus already covers

1. **AI/agent engineering curricula and SDK docs** - Microsoft genai/agents-for-beginners (21,571 rows combined, my count), openai-cookbook 3,120, anthropic-courses 224, hf-agents-course 435, zcode-zai-org 6,810 (all my counts).
2. **Game-world / bot-emulation engineering** - mod-playerbots 5,019, wotlk-db 226, evennia 1,579, dfhack_full (Dwarf Fortress), plus external WoW-emulation roots azerothcore-wow 10,356 + vmangos-core 4,397 + tortoise-wow 3,767 (my counts).
3. **arXiv-scale research papers** - state/arxiv 3,776 rows (my count).
4. **ML systems internals** - lmcache-src 2,331 (KV-cache serving), plus code-heavy estate: code 72,365 and test 7,394 kinds (`catalog/catalog_manifest.json:10-11,20`).
5. **Oral history / self-archaeology** - oral_history shelf 15,749 files / 1,423.9 MB (`CORPUS_CATALOG.md:15`); seat_pools 11,870 + nacho_archaeology 2,981 (my counts).
6. **Frontier-research intake** - watch_inbox 13,580 files / 6,438.9 MB and frontier_thinking 11 files (`CORPUS_CATALOG.md:17,19`).
7. **Esoterica / alternative history** - tartaria_lives 11 (`CORPUS_CATALOG.md:13`), ext:the_margin_lean 9,164 (my count).
8. **Canon / doctrine** - 209 canon files, 205 hashes verified (`CORPUS_CATALOG.md:5`); ractor_ribs 36 (`CORPUS_CATALOG.md:12`).
9. **Own-machine memory** - memory zone 355,237 rows, the single largest holding (my count).

## Freshness (manifest, snapshot 2026-09-30T07:32:33Z, `catalog/catalog_manifest.json:28`)

fresh 138,200 / stale 282,489 / aging 269,121 / fossil 1,978 (`catalog/catalog_manifest.json:2-7`). Stale+aging dominate: most mass is recent-estate machinery, not external research.

## OWED / not done

- Did not open or read individual research documents; domain labels are inferred from path prefixes I counted, not from content reads.
- Did not verify the CORPUS_CATALOG.md shelf table by recounting per-shelf file counts (I counted the catalog.jsonl rows, which include bulk layers the shelf table excludes).
- Map sha256 (`catalog/catalog_manifest.json:23`) not independently recomputed.
