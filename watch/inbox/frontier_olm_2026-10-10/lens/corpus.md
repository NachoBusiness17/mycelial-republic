# LENS: corpus - what research domains the estate already holds

Lens run 2026-10-10 by the lens-corpus subagent. Sources read in full: `catalog/catalog_manifest.json`, `CORPUS_CATALOG.md`. Source sampled and counted: `catalog/catalog.jsonl` (422,725,095 bytes, `wc -l` = 1,469,737 rows; `ls -la catalog/catalog.jsonl`; `head -c 2000`). Manifest snapshot_ts 2026-10-10T08:55:28Z (`catalog/catalog_manifest.json:28`), kind_counts sum 1,469,737 matches my `wc -l` (manifest lines 8-21, sum re-added by hand). Every count below is one I ran myself this session with awk over catalog.jsonl unless marked otherwise.

## Counting instruments (exact commands)

- Total rows: `wc -l catalog/catalog.jsonl` -> 1469737.
- Tree counts: `awk -F'"path": "' '{n=split($2,a,"\""); p=a[1]; split(p,seg,"/"); top=seg[1]; if (seg[2]!="") top=top"/"seg[2]; cnt[top]++} END {for (k in cnt) print cnt[k], k}' catalog/catalog.jsonl | sort -rn` (top 45 shown in session).
- corpus/ drill: same awk keyed on segments 1-3; corpus/library and corpus/oral_history keyed on segment 4.
- kind field is NOT in catalog.jsonl rows (verified: `sed -n '700000p' catalog/catalog.jsonl` shows id/path/bytes/mtime/zone/ext/title/age_days only); it lives in `catalog/tags.jsonl` (sampled via awk on `"kind": "`). kind "corpus" = 1,865 rows per manifest (`catalog/catalog_manifest.json:13`), e.g. `local_sovereign_agent/memory/archaeology/SYSTEM_PROMPTS_LEAKS_20260914.md` and `memory/corpus/ai_canon/chapters/dlb_autoencoders.html` (tags.jsonl samples).

## Estate top trees by catalog rows

| tree | rows |
|---|---|
| local_sovereign_agent/memory | 973,342 |
| local_sovereign_agent/agents | 147,146 |
| local_sovereign_agent/mine | 97,867 |
| local_sovereign_agent/corpus | 75,880 |
| local_sovereign_agent/watch | 27,611 |
| local_sovereign_agent/logs | 12,431 |
| local_sovereign_agent/state | 7,372 |
| local_sovereign_agent/reference | 1,480 |
| local_sovereign_agent/mag | 1,324 |

Caveat: manifest summary reports base_dups 59,210 (`catalog/catalog_manifest.json:32`): some trees are indexed from more than one zone root, so row counts are catalog rows, not unique files. My `corpus/steal` listing showed this concretely (MASTER_MICKEY17_V2.md appears 4x in catalog rows, once on disk).

## Research domains the corpus already covers (corpus/ tree = 75,880 rows, exact per-dir counts)

| domain | evidence | rows (my awk counts) |
|---|---|---|
| AI/LLM engineering courses + cookbooks | corpus/library/{ms-genai-beginners, ms-agents-beginners, ai-engineering-from-scratch, openai-cookbook, hf-agents-course, anthropic-courses} | 12,142 + 9,429 + 5,401 + 3,120 + 435 + 224 = 30,751 |
| The harness's own source (zcode/zai org) | corpus/library/zcode-zai-org | 6,810 |
| LLM serving / KV-cache infra | corpus/library/lmcache-src (sampled paths .clang-format etc.) | 2,331 |
| ML canon + physics papers (textbook PDFs) | memory/corpus/ai_canon (33 rows: sutton_barto_reinforcement_learning_2nd.pdf, mackay_information_theory..., jurafsky_martin_slp3rd_draft.pdf, bartle_designing_virtual_worlds.pdf, arxiv_time_refraction_moussa_2208.07236.pdf, arxiv_transactional_kastner_1608.00660.pdf, arxiv_tsvf_aharonov_vaidman_0105101.pdf) + corpus/papers_reference_nonredistributable (82 arXiv-ID PDFs: 0706.1347, 0808.2669, 0810.4179 ...) | 33 + 82 = 115 |
| Game-server emulation / game AI | corpus/library/{mod-playerbots 5,019; evennia 1,579; wotlk-db 226} + corpus/dfhack_full 2,123 + corpus/df_mine 25 + sibling trees azerothcore-wow (data 7,671, src 1,768, deps 721), vmangos-core (sql 2,656, src 992, dep 652), tortoise-wow (dep 1,664, src 1,212), library_parked/sourceofmana 2,967 | corpus/ 8,972; sibling segments 22,988 |
| Reverse-engineering toolchain | corpus/tools (ghidra.zip, GhidraSmokeJava.java, jdk21.zip) | 6,029 |
| Estate's own operations research (steal/folds/laws) | corpus/steal 73 catalog rows (43 top-level .md on disk + onionclaw_review/ + dup-zone rows; TETHERED_LINK_STEAL_20260925.md, CORPUS_FOLD_SPIKING_20261001.md, MASTER_ML_MOONSHOT_20261007.md, ZCODE_OPERATING_PLAYBOOK_20260925.md ...) + corpus/canon 210 (THE_FIRST_LAW_20260912.md, INJECTION_FENCE.md, receipts_dec2025_mar2026.jsonl) + corpus/ractor_ribs 36 + corpus/frontier_thinking 11 (FT_RBN_grok_base01..05) | 330 |
| Own-session oral history | corpus/oral_history: seat_pools 11,871 (own seat transcripts), nacho_archaeology 2,981 (personal chat-archaeology zips: nacho-archaeology-part3-conversation-blobs.db.zip ...), loose docs 7 | 14,860 |
| Social/agent-community archives | corpus/social_archive (17 files: pullpush_comments.json, as_aiagents_graph.json, as_llmdevs_mem.json, kvarn_pullpush.json ...) + corpus/telegram 2 | 19 |
| Misc named repos | corpus/library/{mixar 3,669; kev 934; second-brain-os 275; pd_physical_compute 154; human-atlas 118; ractor_starter 113; image-blaster 97; interference-search 63; wakers_20260906 51} | 5,474 |
| Fringe/alternative history | corpus/tartaria_lives (11 .html essays: the-maps-still-say-tartaria.html, the-sky-before-the-flip.html ...) | 11 |
| Frontier-lab internals (leaked system prompts) | sibling research/system_prompts_leaks_20260912 tree 485 rows + memory/archaeology/SYSTEM_PROMPTS_LEAKS_20260914.md (kind corpus) | 485 |

Arithmetic note: corpus/ per-dir rows sum to 75,879 vs the 75,880 corpus total (1-row split between my two awk passes; unreconciled, immaterial).

## Cross-check vs CORPUS_CATALOG.md (the Librarian's own shelf view, run 2026-10-10T13:31:11Z, `CORPUS_CATALOG.md:3`)

The shelf table (`CORPUS_CATALOG.md:9-21`) counts DIFFERENT roots than catalog.jsonl rows, e.g. library shelf 66,715 files / 7,235.1 MB and oral_history 15,749 files vs my corpus/library 52,313 and corpus/oral_history 14,860 catalog rows; line 32 pins the Librarian's ledgers at state/library/catalog.jsonl. Both instruments agree in shape (library and oral_history dominate). Flag I will not paper over: `CORPUS_CATALOG.md:5` reads "CANON MANIFEST: DRIFT - checked 205, missing 0, drifted 4 - resolve before trusting the shelves", so 4 canon manifests drifted as of the 13:31Z run.

## Gaps the frontier sweep can treat as under-covered (from these counts only)

1. Physics/arXiv original papers: 82 redistributable-flagged PDFs + 3 named ai_canon papers is the whole academic-papers shelf; no broad arXiv corpus exists.
2. No non-game, non-RL textbook canon beyond Mackay/Jurafsky/Sutton-Barto/Bartle inside ai_canon (33 rows total).
3. Fringe-domain holdings (tartaria 11, social_archive 17) are tiny samples, not research corpora.
4. The 4 drifted canon manifests (`CORPUS_CATALOG.md:5`) are unresolved; shelf-level MB/counts inherit that caveat.
5. OWED (not verified this session): per-file byte totals for each domain from catalog.jsonl (I counted rows, not bytes, per domain); the FTS index freshness state (`catalog/catalog_fts.sqlite`, mtime Oct 10 09:00 per `ls -la catalog/`) was not probed with the B2-465 check.
