# LENS: corpus coverage (frontier_olm 2026-10-05)

Lens seat: corpus. What the estate's catalog already covers, every number below counted by me this session unless marked otherwise.

## What I read

- `catalog/catalog_manifest.json` (whole file, 44 lines): snapshot_ts 2026-10-04T07:59:54Z, mode incremental, policy B2-104 C6 freshness with 48h staleness budget (lines 24-29), age_counts (lines 2-7), kind_counts (lines 8-21), summary with base_rows 917,885 / vanished 228,954 / tags_rows 1,040,765 (lines 30-42).
- `catalog/catalog.jsonl`: first 5 rows via PowerShell `Get-Content -TotalCount 5`; row fields are `id, path, bytes, mtime, zone, ext, title, age_days` (no per-row topic tags).
- `catalog/tags.jsonl`: same rows plus `kind, age_class, owner`; it holds NO free-form topic tags (my script output, `_corpus_lens_tags.py`). So domain coverage is derivable only from paths, kinds, and dir structure.
- `CORPUS_CATALOG.md` (33 lines): canon-manifest drift warning "checked 205, missing 0, drifted 4" (line 5); curated shelf table (lines 9-21); bulk layers (lines 23-30); "The Librarian records; it never cleans" (line 32).

## What I ran

1. `Get-Content catalog\catalog.jsonl -TotalCount 5` (5 rows, verified fields).
2. `.venv\Scripts\python.exe watch\inbox\frontier_olm_2026-10-05\lens\_corpus_lens_count.py`: 871,790 rows total; top path roots: local_sovereign_agent 820,601, Mag-backup.git 12,945, azerothcore-wow 10,356, the_margin_lean 9,164, vmangos-core 4,397, tortoise-wow 3,767, worktrees 1,487, research 767, mycelial-republic 309; zones: memory 439,964, lsa 300,935, runs 53,745, intake 17,831.
3. `_corpus_lens_tags.py`: tags.jsonl 871,790 rows (exactly matches catalog rows).
4. `_corpus_lens_third.py`: third-level breakdowns (below).
5. `_corpus_lens_final.py`: library shelves, mine/raw texture, research_packs, kind recount.

## Domains the corpus covers (my counts)

**1. Agent/LLM engineering (the deep shelf).** `corpus/library`: ms-genai-beginners 12,142 rows, ms-agents-beginners 9,429, zcode-zai-org 6,810, openai-cookbook 3,120, hf-agents-course 435, anthropic-courses 224 (`_corpus_lens_final.py` output). Scraped `mine/raw` 97,865 rows (ext: .ts 31,243, .py 15,757, .tsx 8,142, .rs 5,103); title keyword hits: agent 2,323, llm 1,007, mcp 875, eval 802, dataset 444, embedding 155, benchmark 92.

**2. Inference systems / KV cache.** lmcache-src 2,331 rows (same script).

**3. Game worlds as AI-society testbeds.** evennia 1,579, mod-playerbots 5,019, wotlk-db 226, dfhack_full 2,123 (mine); sibling repos as catalog rows: azerothcore-wow 10,356, vmangos-core 4,397, tortoise-wow 3,767 (count script).

**4. Self-knowledge / estate process.** memory/biography_backup 258,840 + biography 65,934 + runs 53,745 + agent_state 41,559; watch/inbox 17,831; docs/ref 372 (`_corpus_lens_third.py`).

**5. Graphics/shader corpus.** memory/corpus/shadertoy21k 21,806 rows (same script) - the single biggest curated set after biography.

**6. Canon micro-shelves (curated, small).** memory/corpus: mycology_canon 52, ai_canon 33, electronics_canon 30, moonshot_canon 21, quantized_thought 19, founding_law 14, augmentation_canon 9; corpus/canon 210 (vs doc's 209 files, CORPUS_CATALOG.md:11).

**7. Oral history / social archive.** corpus/oral_history 14,860 rows (mine) vs doc shelf 15,749 files (CORPUS_CATALOG.md:15); delta ~889 NOT resolved - different instruments (catalog rows post-exclusion vs raw file walk) and different moments (catalog snapshot 2026-10-04T07:59Z vs doc run 2026-10-05T13:16Z, line 3). Reported, not papered over.

**8. Humanities/essay pockets.** pd_physical_compute 154, human-atlas 118, interference-search 63, pd_scifi 28, tartaria_lives 11, frontier_thinking 11, ractor_ribs 36, corpus/papers_reference_nonredistributable 82 (mine).

**9. Q&A research packs.** memory/research_packs 829 rows, e.g. "what-is-the-ollama-project-homepage" pack with json+pdf+answers (`_corpus_lens_final.py`).

## Age and kind profile

- Age (manifest lines 2-7, I summed): total 1,040,765 = tags_rows (line 38); stale 417,347 (40.1%), aging 341,784 (32.8%), fresh 278,661 (26.8%), fossil 2,973 (0.3%).
- KIND DRIFT FOUND: manifest kind_counts (lines 8-21) sum to 939,591 by my arithmetic, which matches neither the 871,790 catalog rows nor tags_rows 1,040,765. My own kind recount from tags.jsonl: config 465,716, other 137,357, prose 88,205, code 75,123, ledger 40,063, image 32,069, receipt 12,856, test 8,797, brief 6,205, card 2,354, corpus 1,776, state 1,269 (sums to 871,790). The manifest's kind block is stale relative to its own snapshot; readers should trust the catalog/tags files, not that block.

## OWED / not done

- Did not verify the doc's `library` shelf (66,715 files, CORPUS_CATALOG.md:18) against disk; my corpus/library subtree count is 43,146 catalog rows under that path - scope difference (doc counts the whole shelf dir incl. non-cataloged?) unexplained, left OWED.
- Did not run the FTS index or corpus_search; coverage above is path/kind structure only, not full-text topical recall.
- Did not open shelf contents to judge depth/quality; counts are row counts, not evidence of coverage quality.
- The doc's canon drift "drifted 4" (line 5) unresolved by me; flagged for the librarian.
