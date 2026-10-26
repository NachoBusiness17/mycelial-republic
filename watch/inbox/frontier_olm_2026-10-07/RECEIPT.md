source-fetched: 2026-10-07

# RECEIPT: frontier_olm_2026-10-07 fold (v3, full rewrite from fresh measurements)

## Premise note (this ask)

The triggering ask stated this file does not exist. At check time this ask it DID exist: `RECEIPT.md`, 14,324 bytes, the rev-2 version (first line `source-fetched: 2026-10-07`, 0 em-dashes, validated at the end of the rev-2 repair ask). Per the instruction it is rewritten now anyway; every number below was measured or re-derived during THIS ask, nothing carried over unverified. This version is authoritative.

## Fold gate

- This ask: acquired before any write - `C:/Users/foste/Documents/projects/local_sovereign_agent/.venv/Scripts/python.exe C:/Users/foste/Documents/projects/local_sovereign_agent/tools/fold_gate.py acquire --holder "olm-mine:2026-10-07" --wait 900` -> `HELD ...workflow-fold.lock holder=olm-mine:2026-10-07` (exit 0). Released before the final line of the reply.
- Same acquire/release pattern ran in the two prior asks of this fold (initial fold; rev-2 repairs).

## Outputs (byte counts measured this ask)

- DIGEST.md: 31,634 bytes (rev 2: 18 cold-reader repairs applied in place on 2026-10-07)
- register.jsonl: 20,499 bytes - 21 rows, one per confirmed find; parsed line-by-line this ask, all fields present
- percolator_candidates.jsonl: 34,689 bytes - 8 rows, one per steal card; parsed line-by-line this ask
- RECEIPT.md: this file; a file cannot contain its own final byte count, so its size is reported in the fold reply after this write.

## Every file with byte counts (measured this ask)

Measurement: repo venv python, `os.walk` over `watch/inbox/frontier_olm_2026-10-07` (excluding the `.mimosa/` hook-state subdirectories), printing `relpath size` per file. Walk result: 171 files, 15,915,439 bytes total at measurement time (that total includes the pre-rewrite 14,324-byte RECEIPT.md; the post-rewrite arithmetic is given in the fold reply).

```
DIGEST.md 31634
RECEIPT.md 14324                      (pre-rewrite, see Premise note)
percolator_candidates.jsonl 34689
register.jsonl 20499
lens/_organ_check.py 847
lens/burns.md 16892
lens/corpus.md 4484
lens/doors.md 4357
lens/graph.md 4736
lens/laws.md 26207
lens/questions.md 20976
steal/evals-self-improvement via reddit.md 8088
steal/finetuning-adaptation.md 19959
steal/gigafish_README.md 6991
steal/inference-efficiency.md 11467
steal/kv-cache-context-engineering.md 16755
steal/manifest_qwen3_4b-instruct.json 859
steal/manifest_qwen3_4b-thinking.json 859
steal/manifest_qwen3_4b.json 859
steal/manifest_qwen3_8b-instruct.json 69
steal/manifest_qwen3_8b-thinking.json 69
steal/manifest_qwen3_8b.json 859
steal/open-local-language-models via reddit.md 19891
steal/open-local-language-models.md 11535
steal/quantization-compression.json 5640
steal/quantization-compression.md 14582
steal/shell_escape_probe.txt 98
steal/shell_escape_probe_runner.py 867
steal/swarm-orchestration.md 24964
steal/tags_probe_olmreddit.json 7466
sweep/_overlap_check_kvcache.py 2665
sweep/agent-memory-continuity-arxiv.md 14858
sweep/agent-memory-continuity-hn.md 12790
sweep/agent-memory-continuity-reddit.md 13842
sweep/agent-memory-continuity-x.md 14165
sweep/evals-self-improvement-arxiv.md 18063
sweep/evals-self-improvement-hn.md 16235
sweep/evals-self-improvement-reddit.md 12204
sweep/evals-self-improvement-x.md 15252
sweep/finetuning-adaptation-arxiv.md 13389
sweep/finetuning-adaptation-hn.md 12689
sweep/finetuning-adaptation-reddit.md 15312
sweep/finetuning-adaptation-x.md 10944
sweep/fx_ollama_2028514180936908842.json 2767
sweep/inference-efficiency-arxiv.md 15061
sweep/inference-efficiency-hn.md 17396
sweep/inference-efficiency-reddit.md 20861
sweep/inference-efficiency-x.md 9955
sweep/kv-cache-context-engineering-arxiv.md 17797
sweep/kv-cache-context-engineering-hn.md 13910
sweep/kv-cache-context-engineering-reddit.md 21725
sweep/kv-cache-context-engineering-x.md 22861
sweep/local_api_tags.json 7466
sweep/nimble_public_benchmarks.md 38286
sweep/ollama_v0343_release.json 36539
sweep/open-local-language-models-arxiv.md 13517
sweep/open-local-language-models-hn.md 16228
sweep/open-local-language-models-reddit.md 18112
sweep/open-local-language-models-x.md 14800
sweep/quantization-compression-arxiv.md 14405
sweep/quantization-compression-hn.md 14565
sweep/quantization-compression-reddit.md 14005
sweep/quantization-compression-x.md 18824
sweep/show_body_gemma4.json 20
sweep/show_resp_dsr1_15b.json 7210
sweep/show_resp_gemma4.json 26285
sweep/show_resp_qwen25_7b.json 28757
sweep/swarm-orchestration-arxiv.md 14406
sweep/swarm-orchestration-hn.md 15405
sweep/swarm-orchestration-reddit.md 14260
sweep/swarm-orchestration-x.md 13636
sweep/tmp_overlap2_quant.py 2203
sweep/tmp_overlap_quant.py 2407
sweep/tmp_synd_quant.py 3324
sweep/tmp_synd_quant2.py 2402
sweep/hn_raw/bench.json 63098
sweep/hn_raw/cite.json 73237
sweep/hn_raw/contam.json 1132
sweep/hn_raw/evals.json 46037
sweep/hn_raw/judge.json 62993
sweep/hn_raw/reward.json 28460
sweep/raw/arctic_cmt_1wblnsk.json 196701
sweep/raw/arctic_cmt_1ws9ydg.json 203815
sweep/raw/arctic_cmt_1wv05u1.json 82070
sweep/raw/arctic_cmt_1wxz5qq.json 52447
sweep/raw/arctic_cmt_1wyaxyd.json 32982
sweep/raw/arctic_cmt_1wyruu5.json 232101
sweep/raw/arctic_ids_b1.json 63004
sweep/raw/rss_LocalLLM.xml 168209
sweep/raw/rss_LocalLLaMA.xml 147440
sweep/raw/rss_MachineLearning.xml 149179
sweep/raw/rss_ollama.xml 180656
sweep/tmp/comments_1r21ojm.json 116734
sweep/tmp/comments_1rrss36.json 207785
sweep/tmp/comments_1uxwp0i.json 150392
sweep/tmp/comments_1wcywl4.json 2254
sweep/tmp/comments_1wi17z6.json 81635
sweep/tmp/comments_1wixud0.json 2650
sweep/tmp/comments_1wms904.json 137375
sweep/tmp/comments_1wpqlhj.json 3214
sweep/tmp/comments_1wq76f6.json 67116
sweep/tmp/comments_1wrul9r.json 45269
sweep/tmp/comments_1wt03zh.json 93549
sweep/tmp/comments_1wtyc4y.json 19013
sweep/tmp/comments_1wv0b24.json 2
sweep/tmp/comments_1wvwdn1.json 2
sweep/tmp/comments_1wwp0q8.json 6378
sweep/tmp/comments_1wyf63m.json 106677
sweep/tmp/comments_1wyqjsc.json 12714
sweep/tmp/comments_1wzhtld.json 8955
sweep/tmp/comments_1wzlqac.json 2370
sweep/tmp/parse_rss.py 913
sweep/tmp/post_1wcywl4.json 7565
sweep/tmp/post_1wi17z6.json 3936
sweep/tmp/post_1wixud0.json 3437
sweep/tmp/post_1wms904.json 6415
sweep/tmp/post_1wpqlhj.json 5167
sweep/tmp/post_1wq76f6.json 19455
sweep/tmp/post_1wrul9r.json 3605
sweep/tmp/post_1wt03zh.json 9470
sweep/tmp/post_1wtyc4y.json 4074
sweep/tmp/post_1wv0b24.json 12852
sweep/tmp/post_1wvwdn1.json 3429
sweep/tmp/post_1wwp0q8.json 8438
sweep/tmp/post_1wyf63m.json 8340
sweep/tmp/post_1wyqjsc.json 7262
sweep/tmp/post_1wzhtld.json 4576
sweep/tmp/post_1wzlqac.json 15990
sweep/tmp/pp_candidates.jsonl 153794
sweep/tmp/read_cmts.py 625
sweep/tmp/read_ids_b1.py 702
sweep/tmp/sub_1qvs05z.json 6089
sweep/tmp/sub_1r3nda0.json 5131
sweep/tmp/sub_1r5q7xd.json 4305
sweep/tmp/sub_1rfg53c.json 6420
sweep/tmp/sub_1rxywnf.json 6726
sweep/tmp/sub_1s43ts3.json 3269
sweep/tmp/sub_1t4jpcw.json 5030
sweep/tmp/sub_1uxwp0i.json 5260
sweep/_raw/anthropic_compaction.html 385471
sweep/_raw/anthropic_context_editing.html 1608102
sweep/_raw/anthropic_prompt_caching.html 1914357
sweep/_raw/dailydoseofds_caching.html 310224
sweep/_raw/dataaspirant_lc_rag.html 336207
sweep/_raw/deepseek_kv_cache.html 33018
sweep/_raw/localaizone_kv_evolution.html 9379
sweep/_raw/nul 0
sweep/_raw/openai_prompt_caching.html 765273
sweep/_raw/synd_BrandonMusicKy.html 2236
sweep/_raw/synd_DeepSeek_AI.html 511398
sweep/_raw/synd_Fermonroyh.html 269059
sweep/_raw/synd_Qwen_Qwen.html 2221
sweep/_raw/synd_SOTAAZ.html 2175
sweep/_raw/synd_Togethercompute.html 125406
sweep/_raw/synd_UnslothAI.html 165703
sweep/_raw/synd_above_spec.html 2224
sweep/_raw/synd_eleutherai.html 2183
sweep/_raw/synd_ggerganov.html 571491
sweep/_raw/synd_ggml_org.html 162838
sweep/_raw/synd_ikawrakow.html 2181
sweep/_raw/synd_lmsysorg.html 605659
sweep/_raw/synd_ollama.html 111470
sweep/_raw/synd_rasbt.html 550750
sweep/_raw/synd_typesafeai.html 146563
sweep/_raw/synd_vllm_project.html 747871
sweep/_raw/together_serving_v4.html 570778
sweep/_raw/together_test.html 64145
sweep/_raw/xai_best_practices.html 386603
sweep/_raw/xai_context_compaction.html 520433
sweep/_raw/xai_how_it_works.html 393522
sweep/_raw/xai_what_breaks.html 483254
```

(`sweep/_raw/nul` is a 0-byte Windows capture artifact.)

Totals reconciliation: the rev-2 record below quoted 171 files / 15,913,451 bytes; that walk ran while RECEIPT.md was still rev 1 (12,336 B) and before the rev-2 record was appended (+1,988 B -> 14,324 B), giving today's pre-rewrite total 15,913,451 + 1,988 = 15,915,439. The totals reconcile exactly; no unexplained drift.

## Counts (re-derived this ask by parsing register.jsonl and percolator_candidates.jsonl)

- Confirmed finds: 21 rows, all parse.
- Finds by area: open-local-language-models 7, swarm-orchestration 3, finetuning-adaptation 3, kv-cache-context-engineering 2, evals-self-improvement 2, inference-efficiency 2, quantization-compression 2. Total 21.
- Finds by source (discovery door, not URL host): x 11, reddit 6, arxiv 3, hn 1. Total 21.
- Percolator candidates: 8 rows, all parse.
- Unconfirmed with evidence: 3 (Ornith 1wyruu5; OpenAI prompt-caching claim; TokenProbe 2610.33970 find-as-stated); none entered in register.jsonl.
- Sweep lanes: 32 (8 areas x 4 doors); sweep items banked by lanes: 241 (folder tabulation of the lane payloads in the fold ask; the confirm round's selection rule: pool -> sort by confidence desc -> slice(0, CONFIRM_CUT=24), `.zcode/workflows/olm-mine.dwf.ts:326-335`).
- Normalization: area strings of the form '<area> via <door>' folded to area + source; register rows otherwise verbatim from the fold ask with two disclosed fold annotations (nimble 9-of-13 correction; Weave Router zero-overlap strike).

## Workflow gate row pointer (re-read this ask)

memory/workflows/REGISTRY.jsonl, 160 rows at this ask's read:
- Latest olm-mine gate PASS row: line 104, ts 2026-10-06T00:52:51Z, name olm-mine.dwf.ts, digest c7c95efcd512, script .zcode/workflows/olm-mine.dwf.ts, verdict PASS (checks G1-multiplicity, G2-passoff, G3-steering et al. all ok).
- Status row: line 124, STATUS-ROW active (ts 2026-10-06T18:53:21Z), status_basis latest_registry_row_digest c7c95efcd512, fire_count 3, last_fire_verdict PASS.
- No new olm-mine row exists for the 2026-10-07 fire folded here (16 olm-mine rows total; the newest registry rows at this read are a wide-dig STATUS-ROW 2026-10-07T08:41:27Z, RUNNER.dwf.ts PASS 11:57:06Z, and an unrelated workflow PASS 14:02:19Z): today's run rode the saved/amended workflow, which reuses the prior gate PASS rather than re-gating.

## Validation and revision history (which ask ran what)

- Rev 1 (initial fold ask): register.jsonl 21 rows + percolator_candidates.jsonl 8 rows written and JSON-validated; em-dash scan 0; card fidelity cross-check vs round-1 `steal/*.md` (2 of 8 verbatim-contained, 6 round-2 rewordings, spot-grep evidence recorded); lane-note size claims vs bytes (5 banks measured larger, all other claims within 4 B); a python builder script was blocked by the Mimosa write-time security hook, so the JSONL files were hand-written then machine-validated.
- Rev 2 (cold-reader repair ask): 18 fixes applied to DIGEST.md (21,059 -> 31,634 B; 7 sections, 21 table rows, 0 em-dashes). New checks run that ask: shell-door containment re-run (ok: True exit: 0; artifact `steal/shell_escape_probe.txt` 98 B kept; door UNCONTAINED); b11475 primary re-pull (0.28-vs-0.977 / GGML_METAL_FUSION_DISABLE=1 / "fails 27 of 28" verified verbatim); mine-script selection-rule read; lens bar-filing read (`lens/burns.md:92-94`); estate rung battery scores searched and NOT located (0 hits in memory/rib GATES/GARDEN/ROUTING score grep; battery-named files are the method-card battery, `tools/battery_rerun.py:1-24`) and stated OWED; the 5 larger-measuring banks re-measured unchanged.
- Rev 3 (this ask, receipt rewrite): premise checked (file existed at 14,324 B); full walk re-measured; register/percolator re-parsed with identical tallies; registry re-read (unchanged for olm-mine).

## Falsifiers / what was NOT run

- No probes fired by the folder seat in the rev-3 ask; the two EXECUTED probes on the books (registry manifest compare; /api/show daemon reads; plus the shell-door re-run at rev 2) belong to the steal round and the rev-2 repair pass, artifacts on disk as listed above.
- No pytest, no percolator promotion, no gate re-run: none named by this ask.
