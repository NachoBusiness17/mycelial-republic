# LENS: CORPUS - what the estate's corpus already covers (frontier OLM 2026-10-06)

Lens seat: lens-corpus. Ask: read `catalog/catalog_manifest.json`, sample `catalog/catalog.jsonl`, read `CORPUS_CATALOG.md`; report covered research domains with counts counted by this seat, not hand-copied.

## Instrument (what I actually ran)

- Full linear pass over `catalog/catalog.jsonl` with the repo venv: `.venv/Scripts/python.exe` counting script (temp file `tools/_lens_corpus_count_tmp.py`, deleted after the run) parsing every row and grouping by normalized path prefix. Output: TOTAL_ROWS 1,130,965, BAD_JSON 0. This row count independently reproduces the line counts I measured with `wc -l` on both `catalog/catalog.jsonl` and `catalog/catalog/tags.jsonl` (1,130,965 each) and matches `tags_rows: 1130965` at `catalog/catalog_manifest.json:38`.
- Cross-check that the method is sound: my top-prefix counts (memory 662,572; agents 128,175; mine 97,867; corpus 75,969; watch 25,782) are byte-identical to the estate's own tag-report owner column at `catalog/TAG_REPORT.md:30-34`.
- Direct reads: `catalog/catalog_manifest.json` (snapshot_ts 2026-10-06T07:36:37Z at line 28), `CORPUS_CATALOG.md`, `catalog/TAG_REPORT.md`, plus head samples of both jsonl files.

## Method caveat (disclosed, not hidden)

Catalog rows are one row per file, snapshot 2026-10-06T07:36:37Z (`catalog/catalog_manifest.json:28`). `CORPUS_CATALOG.md` is a different instrument run later the same day (2026-10-06T13:15:33Z, `CORPUS_CATALOG.md:3`) and its shelf table self-reports DRIFT ("checked 205, missing 0, drifted 4", `CORPUS_CATALOG.md:5`). So the doc's shelf counts and my catalog counts differ where shelves moved between the two moments (example: corpus/library is 52,316 rows in my pass vs 66,715 files in `CORPUS_CATALOG.md:18`). I report my own counts below and name the doc only where cited. Kind counts (config 642,329; prose 108,108; code 84,811; `catalog/catalog_manifest.json:8-21`) live in `catalog/tags.jsonl`, not in `catalog/catalog.jsonl` rows (my head sample shows catalog rows carry id/path/bytes/mtime/zone/ext/title/age_days only); they are the manifest's numbers, not mine.

## Domains the corpus already covers (counts = my pass unless line-cited)

**1. Frontier AI and agent-engineering curricula** (under `corpus/library/`, my pass): ms-genai-beginners 12,142; ms-agents-beginners 9,429; zcode-zai-org 6,810; ai-engineering-from-scratch 5,401; openai-cookbook 3,120; lmcache-src 2,331; evennia 1,579; hf-agents-course 435; second-brain-os 275; anthropic-courses 224. Total `corpus/library` 52,316 rows.

**2. Game-estate and private-server MMO research**: `corpus/dfhack_full` 2,123 (full DFHack source tree per sample paths); `corpus/df_mine` 25 (dfhack_datamodel.json, dfhack_economy.json + FOLDs); `corpus/game_estate` 15 (FROM_MUD_TO_WOW_20260914.md, ARENA_V2_CONSTELLATION_SALON_20260913.md per samples); top-level codebases azerothcore-wow 10,356; vmangos-core 4,397; tortoise-wow 3,767; library mods mod-playerbots 5,019; wotlk-db 226; plus world-games-corpus 81, game_roblox 27, roblox 96, roblox_to_godot 35, the-mountain 74.

**3. Oral history and operator-life archive**: `corpus/oral_history` 14,860 (seat_pools 11,871; nacho_archaeology 2,981; marathon_body 2; the_wall 2), incl. LETTER_TO_DAUGHTER.md and strike_the_chord_session_RECOVERED.md per samples.

**4. Rhetoric / propaganda / simulation theory (ractor ribs)**: `corpus/ractor_ribs` 36 rows, BAUDRILLARD and BERNAYS case-law dirs per samples.

**5. Fringe / alt-history / social intelligence**: `corpus/tartaria_lives` 11 (html); `corpus/telegram` 2 (gold_standard.jsonl, MrPool_Q.jsonl); `corpus/social_archive` 34 (reddit dumps as_aiagents_graph.json et al., path-dated 20261001); `corpus/tmp_enoch` 14.

**6. Academic papers**: `corpus/papers_reference_nonredistributable` 162 (arXiv-numbered PDFs, e.g. 0706.1347.pdf); `corpus/papers` 2 (librarian backfill ledgers, not papers).

**7. Frontier-model thinking captures**: `corpus/frontier_thinking` 11 (FT001_zai53_research_restock_20260904.md, FT_ASTRA_DOOR_* per samples); shelf mtime range 2026-09-04 to 2026-09-06 (`CORPUS_CATALOG.md:17`), i.e. frozen for a month.

**8. Research steals and system-prompt forensics**: top-level `research/` 862 rows (system_prompts_leaks_20260912 485; aiTruthCode 121; cl4r1t4s 84 + upstream 77; gaming_corpus 68); `corpus/steal` 61 (harness process laws, 2026-09-26 wave per sample names).

**9. Training and education material**: `corpus/training_materials` 27 (oxford_complex_numbers.pdf, alphaevolve_omega.pdf, drawing-right-brain PDF per samples); `corpus/tools` 6,029 (ghidra.zip, jdk21.zip binaries per samples).

**10. Canon, doctrine, harness self-knowledge**: `corpus/canon` 210 + top-level `canon/` 107; docs/ref 376; mycelial-republic 309; mag-sovereign-kit 310; teach 366; field-strike-the-chord 68; ai-job-search 96; nacho-business 43; the_margin_lean 9,164.

**11. The estate's own memory bulk** (process record, not external research): memory 662,572; agents 128,175; mine 97,867; watch 25,782; logs 7,888; state 6,507 rows.

## Thin spots for the frontier sweep (candidate gaps, from my counts)

- Formal academic coverage is 162 arXiv PDFs plus 27 training PDFs; `corpus/papers` holds 2 ledger rows, no paper bodies.
- `corpus/frontier_thinking` (11 rows) has not grown since 2026-09-06 (`CORPUS_CATALOG.md:17`).
- Social-intelligence capture is a single reddit dump of 34 rows path-dated 2026-10-01 and a 2-row telegram shelf.

## OWED

None. Every count above came from the pass run during this ask; the two-instrument library delta (52,316 vs 66,715) is stated as a caveat, not resolved.
