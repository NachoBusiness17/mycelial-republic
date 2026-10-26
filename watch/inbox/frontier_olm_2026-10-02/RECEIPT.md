source-fetched: 2026-10-02

Fold receipt for watch/inbox/frontier_olm_2026-10-02/. Every byte count below was measured by the fold seat this sitting (`.venv/Scripts/python.exe` `os.path.getsize` walk over the run directory, and the same for the fold's own outputs). Companion files: DIGEST.md, register.jsonl, percolator_candidates.jsonl.

## 1. Fold outputs (measured)

| File | Bytes | Notes |
|---|---|---|
| DIGEST.md | 32,168 | executive summary, top steals, confirmed table, honest gaps, unconfirmed; revised this sitting for the cold-reader's 12 findings (register-row mapping column, count reconciliations, MemFit sourcing, term definitions, scheduling section) |
| register.jsonl | 25,967 | 23 rows, every line JSON-parsed clean this sitting |
| percolator_candidates.jsonl | 31,341 | 9 rows, every line JSON-parsed clean this sitting |
| unconfirmed_bnjmn_marie_20260914.md | 2,432 | landing spot for the Sep-14 run-variance finding held out of the confirmed set on its dating label (cold-reader issue 3) |
| RECEIPT.md (this file) | 12,095 | self-measured; see the fixed-point note in section 5 |

Em/en dash scan this sitting over DIGEST.md + register.jsonl + percolator_candidates.jsonl + unconfirmed_bnjmn_marie_20260914.md: EM 0, EN 0 (byte counts of `\xe2\x80\x94` / `\xe2\x80\x93`).

## 2. Run directory inventory (measured, 1,037,316 bytes excluding this file)

### run-dir root

| File | Bytes |
|---|---|
| DIGEST.md | 32,168 |
| register.jsonl | 25,967 |
| percolator_candidates.jsonl | 31,341 |
| unconfirmed_bnjmn_marie_20260914.md | 2,432 |

### sweep/ - 32 lane write-ups + 11 raw fetch JSONs + probe dir + tool state

| File | Bytes |
|---|---|
| sweep/agent-memory-continuity-arxiv.md | 8,016 |
| sweep/agent-memory-continuity-hn.md | 12,524 |
| sweep/agent-memory-continuity-reddit.md | 12,357 |
| sweep/agent-memory-continuity-x.md | 14,108 |
| sweep/evals-self-improvement-arxiv.md | 11,750 |
| sweep/evals-self-improvement-hn.md | 17,910 |
| sweep/evals-self-improvement-reddit.md | 14,763 |
| sweep/evals-self-improvement-x.md | 14,982 |
| sweep/finetuning-adaptation-arxiv.md | 11,809 |
| sweep/finetuning-adaptation-hn.md | 15,307 |
| sweep/finetuning-adaptation-reddit.md | 18,221 |
| sweep/finetuning-adaptation-x.md | 19,080 |
| sweep/inference-efficiency-arxiv.md | 11,014 |
| sweep/inference-efficiency-hn.md | 11,862 |
| sweep/inference-efficiency-reddit.md | 20,028 |
| sweep/inference-efficiency-x.md | 17,762 |
| sweep/kv-cache-context-engineering-arxiv.md | 14,205 |
| sweep/kv-cache-context-engineering-hn.md | 14,330 |
| sweep/kv-cache-context-engineering-reddit.md | 13,449 |
| sweep/kv-cache-context-engineering-x.md | 12,067 |
| sweep/open-and-local-language-models-arxiv.md | 14,374 |
| sweep/open-and-local-language-models-hn.md | 8,852 |
| sweep/open-and-local-language-models-reddit.md | 14,880 |
| sweep/open-and-local-language-models-x.md | 14,750 |
| sweep/quantization-compression-arxiv.md | 11,765 |
| sweep/quantization-compression-hn.md | 9,818 |
| sweep/quantization-compression-reddit.md | 14,538 |
| sweep/quantization-compression-x.md | 9,364 |
| sweep/swarm-orchestration-arxiv.md | 14,298 |
| sweep/swarm-orchestration-hn.md | 16,327 |
| sweep/swarm-orchestration-reddit.md | 18,541 |
| sweep/swarm-orchestration-x.md | 12,690 |
| sweep/sweep_arctic_qwen.json | 54 |
| sweep/sweep_fxt_alex_prompter.json | 7,664 |
| sweep/sweep_fxt_antling.json | 2,759 |
| sweep/sweep_fxt_ddalcu.json | 6,395 |
| sweep/sweep_fxt_jurbed.json | 4,126 |
| sweep/sweep_fxt_jvr0x_pirate.json | 40,221 |
| sweep/sweep_fxt_mertco.json | 2,859 |
| sweep/sweep_fxt_nahid_pro09.json | 9,357 |
| sweep/sweep_hn_qwenflash.json | 76,864 |
| sweep/sweep_tokenharbor_models.json | 32,551 |
| sweep/sweep_tokenharbor_models2.json | 154 |
| sweep/_fx/arctic_refetch_1s720r8.json | 4,596 |
| sweep/_fx/probe_arctic_fast.json | 36,534 |
| sweep/_fx/probe_arctic_spaced1.json | 36,534 |
| sweep/_fx/probe_arctic_spaced2.json | 36,534 |
| sweep/.mimosa/hook-status/sess_dwf-dwfrun-bc564831-...-actor_3_27-65d6facedc.json | 424 |

### steal/ - 9 cards + 6 probe scripts

| File | Bytes |
|---|---|
| steal/agent-memory-continuity via hn.md | 12,152 |
| steal/agent-memory-continuity-arxiv.md | 16,112 |
| steal/evals-self-improvement via x.md | 11,326 |
| steal/inference-efficiency.md | 17,277 |
| steal/kv-cache-context-engineering.md | 25,055 |
| steal/open-and-local-language-models.md | 14,646 |
| steal/open-and-local-language-models via reddit.md | 7,418 |
| steal/quantization-compression.md | 8,582 |
| steal/quantization-compression-arxiv.md | 20,816 |
| steal/_probe_ptb.ps1 | 1,823 |
| steal/_probe_ptb2.ps1 | 772 |
| steal/_probe_ptb3.ps1 | 278 |
| steal/_probe_ptb4.ps1 | 266 |
| steal/_probe_ptb5.ps1 | 1,318 |
| steal/_probe_ptb6.ps1 | 291 |

Cross-check: all 9 card byte sizes match the cards' own stated `chars` fields (12,152 / 16,112 / 11,326 / 17,277 / 25,055 / 14,646 / 7,418 / 8,582 / 20,816) - 9/9 exact.

### lens/ - 6 files

| File | Bytes |
|---|---|
| lens/burns.md | 14,487 |
| lens/corpus.md | 6,580 |
| lens/doors.md | 6,021 |
| lens/graph.md | 4,743 |
| lens/laws.md | 15,877 |
| lens/questions.md | 16,201 |

## 3. Find counts

### Items banked by the sweeps (counted by this seat from the fold input's items arrays; instrument = the items arrays themselves)

| Family | Items |
|---|---|
| open-and-local-language-models | 32 |
| evals-self-improvement | 30 |
| swarm-orchestration | 30 |
| finetuning-adaptation | 29 |
| quantization-compression | 28 |
| kv-cache-context-engineering | 27 |
| inference-efficiency | 26 |
| agent-memory-continuity | 25 |
| **Total** | **227** |

### Confirmed register rows: 23 (covering 20 unique URLs)

By exact area string: kv-cache-context-engineering 7 | quantization-compression-arxiv 4 | inference-efficiency 4 | open-and-local-language-models 3 | open-and-local-language-models via reddit 1 | quantization-compression 1 | agent-memory-continuity-arxiv 1 | agent-memory-continuity via hn 1 | evals-self-improvement via x 1. Sum = 23.

By door (rule: the confirming sweep lane's door as named in each register row's `source` field): arxiv 8 | hn 5 | reddit 5 | x 5. Sum = 23.

Multi-door finds: KVarN paper (arxiv + reddit + x rows, plus its HN thread as a separate find) and the llama.cpp decision-models blog (hn + reddit rows).

Content split of the 20 unique finds: 19 frontier-content finds + 1 door-verdict instrument row (register row 1, the PullPush/Arctic Shift verdict - kept because the confirmation pass elevated it at confidence 1 and the register mirrors the confirmation record; DIGEST.md section 3 carries the same note).

## 4. Checks the fold ran this sitting (commands and outcomes)

1. **ARXIV_REGISTER contradiction** (kv-arxiv lane: "append fired, results 933 to 934" vs kv hn/reddit/x lanes: "still OWED, zero rows"). Command: `.venv/Scripts/python.exe` count of "2606.03458" over `memory/runs/corpus_gap_research/ARXIV_REGISTER.json`. Output: 1 occurrence in 5,624 lines, verdict REAL, cited_in the 10-01 DIGEST KVarN entry. Verdict: append LANDED; the three zero-row reads predate it. Debt closed.
2. **PullPush coverage contradiction** (agent-memory-reddit lane: "no index for ids >= ~1wi, roughly 2026-09-11 onward" vs evals-reddit lane: read 1wtut1c of 2026-09-30 end to end). Command: `curl -s -m 25 "https://api.pullpush.io/reddit/search/submission/?ids=1wtut1c"`. Output: full data returned, scrape_utc 1790739909, author Input-X. Verdict: the blanket cutoff is refuted; coverage is spotty/lagging, not a wall; per-id pulls are the reliable path.
3. **nul junk file** (kv-hn lane disclosed creating and removing one instance at 10:33). Found at fold start: `./nul`, 62 bytes, mtime 2026-10-02 17:11, content `/usr/bin/bash: line 2: type: nul_pullpush_body.txt: not found` (read via `od -c`), untracked (`?? nul`). Same writer class as commit d2cd0c012, different instance and seat. Removed (`rm ./nul`, verified absent after). A second seat owes its own instance note.
4. **Workflow gate registry read**: `memory/workflows/REGISTRY.jsonl` - 60 rows at fold time. The `frontier-olm-mine` gate family sits at lines 31-40; latest row line 40, ts 2026-09-30T01:18:10Z, verdict PASS, script `.zcode/workflow-drafts/frontier-olm-mine.dwf.ts`, digest 2487787e949f, checks G1-multiplicity / G2-passoff / G3-steering and the rest all ok:true. **No 2026-10-02 olm-mine row exists yet at fold time** (today's latest rows are ractor-engine lines 59-60, 16:13:42/43Z). This fold's own gate row appends at submit per the gate contract; the pointer for this run is the family above.
5. **JSONL validation**: register.jsonl parsed to exactly 23 rows, percolator_candidates.jsonl to exactly 9 rows, zero parse errors; key sets as specced (register: area, source, title, url, date, quote, why, overlap, confidence; percolator: area, claim, source_url, estate_map, probe, steal_card_path, steal_card_bytes).
6. **Dash hygiene**: 0 em dashes, 0 en dashes across the four content outputs (DIGEST.md, register.jsonl, percolator_candidates.jsonl, unconfirmed_bnjmn_marie_20260914.md), re-scanned after the cold-reader revision pass.
7. **Z18 rerun reproduction** (cold-reader issues 5/9): command `.venv/Scripts/python.exe tools/duel_style_regression.py --json`; output reproduced steal card 3's claims byte-for-byte: pool 80 rows / n_eff 78, raw glm 37 vs 41 exact_binom_p 0.7142, Pearson r(char_diff,win) 0.399, M1 char_diff_norm p=0.0055, M2 glm_in_slot_a p=0.0297, identity_dummy_feasible true. Term checks: first ember-bearing duels.jsonl row carries `"judge": "fireworks/ember-1", "judge_cost": 0.0248`; `grep -c ember logs/duel/duels.jsonl` = 70 (the ember-only rows); M1/M2 defined at tools/duel_style_regression.py:200-212.
8. **usage.jsonl recount + line verification** (cold-reader issue 2): direct count over memory/runs/hermes_burn/usage.jsonl reads 241 rows, 3 with content_chars, 5 with finish_reason, 146 with reasoning_tokens - card 4's "3/241 carry content_chars" (direct field) and "0/241 join" (ledger-id join to per-ask results files) are different instruments, both true; goodput is computable today for 3/241 rows. Verified tools/lensing_ask.py:217,:219 bank finish_reason/content_chars and the tools/hermes_burn.py:375-379 row literal banks neither.
9. **Disk item recount for the 227 census** (cold-reader issue 7): a numbered-list counter over the 32 sweep lane files found a "Banked items" heading and countable "N. " entries on 8 of 32 files, all 8 matching the fold input's per-family counts exactly (59 items total); 6 files carry explicit "(N)" count headers; 18 use prose formats the counter cannot parse mechanically. No disk file contradicts the 227; byte-exact full corroboration NOT established, stated in DIGEST.md.
10. **Cold-reader revision pass**: all 12 findings addressed in place in DIGEST.md (register-row mapping column; 3/241-vs-0/241 reconciliation; Sep-14 finding banked at unconfirmed_bnjmn_marie_20260914.md; MemFit figures labeled full-text-sourced via the agent-memory lane's PDF door; card 3 price basis + term definitions; Victoria citation 1wujph3; disk recount statement; arctic-shift HOLD-and-retry recipe; Z18 receipt via fold rerun; #19 instrument-row annotation and 19+1 split; scheduling section for the Ollama upgrade owner/order and the unscheduled writer port).

## 5. Honest instrument notes

- The 227-item census is a count of the fold input's items arrays, not a re-read of the 32 banked sweep files (those corroborate 32/32 presence on disk; their per-file content was not re-diffed line by line by the fold).
- RECEIPT.md self-byte-count is a fixed-point: the number above was written, the file re-measured, and the line corrected; if the correction shifted the file, the current line states the post-correction measurement.
- The pullpush probe ran once from this seat; the agent-memory lane's specific missing ids (1ws8d1x, 1wi6j25, 1wjm9ez) were not re-tested and stay OWED.
- Fold outputs are uncommitted working-tree files at write time; staging and commit belong to the operator/lane that owns the run close.
