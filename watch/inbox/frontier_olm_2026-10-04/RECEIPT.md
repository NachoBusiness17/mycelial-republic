source-fetched: 2026-10-04

Fold receipt for `watch/inbox/frontier_olm_2026-10-04/`. Every byte count below was measured by this fold seat with `find "$R" -type f -printf '%s\t%P\n'` (git-bash find, st_size) at 2026-10-05, after the fold outputs were written; group sums were recomputed with the repo venv python (os.walk; note: os.walk cannot stat the `nul` device file, its 159 B comes from the find census). Lane material origin: the 32 lane payloads and confirmations handed to this fold in the ask; primary-fetch provenance for every find is in `register.jsonl`.

## 1. Fold outputs (written by this seat)

| bytes | file |
|---|---|
| 38500 | DIGEST.md (revised 2026-10-05 cold-reader pass: 20 fixes; first-write size was 25,246) |
| 24330 | register.jsonl (22 rows, parse-verified, ASCII-only) |
| 35151 | percolator_candidates.jsonl (10 rows, parse-verified, ASCII-only) |
| 20064 | RECEIPT.md (this file; count fixed after final write, see bottom) |

## 2. Sweep bank files (32, written by the lanes 2026-10-04; group sum 595,312 B)

| bytes | file |
|---|---|
| 13826 | sweep/open-and-local-language-models-arxiv.md |
| 13616 | sweep/open-and-local-language-models-hn.md |
| 21064 | sweep/open-and-local-language-models-reddit.md |
| 18763 | sweep/open-and-local-language-models-x.md |
| 18018 | sweep/quantization-and-compression-arxiv.md |
| 24802 | sweep/quantization-and-compression-hn.md |
| 15342 | sweep/quantization-and-compression-reddit.md |
| 20450 | sweep/quantization-and-compression-x.md |
| 17933 | sweep/agent-memory-and-continuity-arxiv.md |
| 29409 | sweep/agent-memory-and-continuity-hn.md |
| 29603 | sweep/agent-memory-and-continuity-reddit.md |
| 10890 | sweep/agent-memory-and-continuity-x.md |
| 19820 | sweep/swarm-orchestration-arxiv.md |
| 14900 | sweep/swarm-orchestration-hn.md |
| 18669 | sweep/swarm-orchestration-reddit.md |
| 12122 | sweep/swarm-orchestration-x.md |
| 15407 | sweep/finetuning-and-adaptation-arxiv.md |
| 14060 | sweep/finetuning-and-adaptation-hn.md |
| 15147 | sweep/finetuning-and-adaptation-reddit.md |
| 16373 | sweep/finetuning-and-adaptation-x.md |
| 18179 | sweep/kv-cache-and-context-engineering-arxiv.md |
| 18214 | sweep/kv-cache-and-context-engineering-hn.md |
| 17296 | sweep/kv-cache-and-context-engineering-reddit.md |
| 22122 | sweep/kv-cache-and-context-engineering-x.md |
| 14654 | sweep/evals-and-self-improvement-arxiv.md |
| 17508 | sweep/evals-and-self-improvement-hn.md |
| 18489 | sweep/evals-and-self-improvement-reddit.md |
| 26665 | sweep/evals-and-self-improvement-x.md |
| 12869 | sweep/inference-efficiency-arxiv.md |
| 29168 | sweep/inference-efficiency-hn.md |
| 16759 | sweep/inference-efficiency-reddit.md |
| 23175 | sweep/inference-efficiency-x.md |

## 3. Steal cards (10; group sum 100,401 B)

| bytes | file |
|---|---|
| 9169 | steal/agent-memory-and-continuity via x.md |
| 9491 | steal/evals-and-self-improvement.md |
| 12555 | steal/finetuning-and-adaptation.md |
| 8129 | steal/inference-efficiency via arxiv.md |
| 7376 | steal/kv-cache-and-context-engineering.md |
| 10723 | steal/open-and-local-language-models via x.md |
| 12147 | steal/open-and-local-language-models-arxiv.md |
| 10823 | steal/quantization-and-compression.md |
| 9197 | steal/quantization-and-compression via arxiv.md |
| 10791 | steal/swarm-orchestration via x.md |

## 4. Lens files (6; group sum 72,826 B)

| bytes | file |
|---|---|
| 15188 | lens/burns.md |
| 4784 | lens/corpus.md |
| 3586 | lens/doors.md |
| 5623 | lens/graph.md |
| 27370 | lens/laws.md |
| 16275 | lens/questions.md |

## 5. Sweep instruments, harvests, and raw page receipts (53; group sum 28,885,133 B)

Lane-written harvest dumps and fetch instruments (kept as byte-checkable receipts; not fold content):

| bytes | file |
|---|---|
| 61855 | sweep/_am_p1_hits.json |
| 29184 | sweep/_am_page_49655089_oram_https_john_oram_ca_opinion_self_improvin.txt |
| 93204 | sweep/_am_page_49734038_rot_https_www_boolean_ai_blog_context_rot_qu.txt |
| 355939 | sweep/_am_page_49745176_copeca_https_github_com_jahala_copeca.txt |
| 650234 | sweep/_am_page_49807583_strata_https_github_com_oren198_Strata.txt |
| 294740 | sweep/_am_page_49861765_guide_https_www_cognee_ai_agent_memory.txt |
| 26361 | sweep/_am_page_49910148_reduck_https_blog_reduck_ai_browser_action_memo.txt |
| 12737 | sweep/_am_page_49945933_doc_https_liao_gg_blog_agents_dont_need_memo.txt |
| 44065 | sweep/_am_page_49950478_slm_https_arxiv_org_abs_2608_08253.txt |
| 488256 | sweep/_am_page_49951895_aura_https_github_com_chetto1983_Aura.txt |
| 3766 | sweep/_am_pass1.py |
| 3514 | sweep/_am_pass2.py |
| 3622 | sweep/_amc_deepread.py |
| 4113045 | sweep/_amc_harvest_AI_Agents.jsonl |
| 3279003 | sweep/_amc_harvest_ClaudeAI.jsonl |
| 2930878 | sweep/_amc_harvest_LLMDevs.jsonl |
| 4230415 | sweep/_amc_harvest_LocalLLM.jsonl |
| 3370680 | sweep/_amc_harvest_LocalLLaMA.jsonl |
| 678776 | sweep/_amc_harvest_MachineLearning.jsonl |
| 689420 | sweep/_amc_harvest_Rag.jsonl |
| 563676 | sweep/_amc_harvest_ollama.jsonl |
| 2524 | sweep/_amc_rank.py |
| 5757082 | sweep/_amc_reddit_harvest.jsonl |
| 5196 | sweep/_amc_reddit_harvest.py |
| 62731 | sweep/_amc_thread_1wfzp1a.txt |
| 14040 | sweep/_amc_thread_1wg41et.txt |
| 38132 | sweep/_amc_thread_1wjq4vh.txt |
| 14992 | sweep/_amc_thread_1wpo86h.txt |
| 26331 | sweep/_amc_thread_1wqudww.txt |
| 15525 | sweep/_amc_thread_1wu31ir.txt |
| 37396 | sweep/_amc_thread_1wui0hj.txt |
| 9198 | sweep/_amc_thread_1wwd5rd.txt |
| 542790 | sweep/_fta_reddit_harvest.jsonl |
| 21495 | sweep/_fta_thread_1wsgrma.txt |
| 18877 | sweep/_fta_thread_1wslgkw.txt |
| 14400 | sweep/_fta_thread_1wspn24.txt |
| 28170 | sweep/_fta_thread_1wsuag0.txt |
| 5185 | sweep/_fta_thread_1wtqpjt.txt |
| 6405 | sweep/_fta_thread_1wu8qa0.txt |
| 24181 | sweep/_fta_thread_1wu9zkn.txt |
| 25011 | sweep/_fta_thread_1wv05u1.txt |
| 772 | sweep/_gapkinds.py |
| 1543 | sweep/_ihn_fetch.py |
| 109094 | sweep/_ihn_page_49596054_specdec_amd.txt |
| 43451 | sweep/_ihn_page_49602817_14providers.txt |
| 12611 | sweep/_ihn_page_49621546_openrouter.txt |
| 22285 | sweep/_ihn_page_49650081_codex_limits.txt |
| 19349 | sweep/_ihn_page_49742415_mozilla_bench.txt |
| 10633 | sweep/_ihn_page_49848269_ollaya.txt |
| 21676 | sweep/_ihn_page_49857656_glm_flash_decision.txt |
| 33653 | sweep/_ihn_page_49897322_tcp_routing.txt |
| 14975 | sweep/_ihn_thread_49911500_routing_agents.txt |
| 2060 | sweep/_overlap.py |

## 6. Host hook runtime state and stray (24 files; 45,708 B at this census moment) - present in the dir, not fold content

`.mimosa/` hook runtime state (session sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde), excluded from scrutiny per house precedent, listed for byte completeness:

| bytes | file |
|---|---|
| 2203 | .mimosa/finding-ledger/v1/events/batch-pretooluse-038f0bfefd9ceaa7cc9588d80b776fe1.json |
| 1399 | .mimosa/finding-ledger/v1/events/batch-pretooluse-a5434c74794b3f8ce3984303b712cbd2.json |
| 1809 | .mimosa/hook-state/sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_3_19.json |
| 434 | .mimosa/hook-status/sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_3_19-cb2e2cfd33.json |
| 589 | sweep/.mimosa/finding-ledger/v1/events/batch-pretooluse-1190ff2fa29ec1465cf88f5ef835b17b.json |
| 726 | sweep/.mimosa/hook-state/sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_3_30.json |
| 1397 | sweep/.mimosa/hook-state/sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_7_1.json |
| 406 | sweep/.mimosa/hook-status/sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_3_30-e2529a9cd2.json |
| 425 | sweep/.mimosa/hook-status/sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_3_31-b7f7b3622f.json |
| 492 | sweep/.mimosa/hook-status/sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_7_1-280005cd4c.json |
| 159 | nul (stray Windows device-name file at the dir root; flagged for deletion by an operator or a follow-up seat - the starter-kit v0.2 deleted one before; this seat did not touch it) |
| 1312 | sweep/.mimosa/finding-ledger/v1/events/batch-stop-20261005T053735303Z-47652-e6b1438e239c.json |
| 1184 | sweep/.mimosa/history/run-20261005T053735303Z-47652-e6b1438e239c.json |
| 177 | sweep/.mimosa/hook-state/sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_7_1.continue.json |
| 3766 | sweep/.mimosa/hook-state/sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_7_1.muutss62-14000-b20318c965.baseline/115b63271a4b83ca17251bee59442f06ae0e468b8aebd67556c3f3482c5bea30.source |
| 772 | sweep/.mimosa/hook-state/sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_7_1.muutss62-14000-b20318c965.baseline/15f28805158440067136ab7a955ffd17465909217d2f38b45243698d93fdad8a.source |
| 2060 | sweep/.mimosa/hook-state/sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_7_1.muutss62-14000-b20318c965.baseline/2ae8c4d693b1af1d49e0e959ea749a6ccf52effebff02267c8b7357b0f0d3e68.source |
| 1543 | sweep/.mimosa/hook-state/sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_7_1.muutss62-14000-b20318c965.baseline/4db4472c8c2af9cb8aaf9432b80f7b1e08b028fc660ebef25ba3c3fb679be505.source |
| 3514 | sweep/.mimosa/hook-state/sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_7_1.muutss62-14000-b20318c965.baseline/6b8c7d26540874ce5a589ea075ac6973c3f23b385fc6b5c3b2c4eabf7c42192d.source |
| 3622 | sweep/.mimosa/hook-state/sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_7_1.muutss62-14000-b20318c965.baseline/ab3efb5c10a0d0b4ef6a01f2d01eca13d4cbfbae2bb4bf07c5ac67ef82020553.source |
| 5196 | sweep/.mimosa/hook-state/sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_7_1.muutss62-14000-b20318c965.baseline/cb555bceed892c8d83679d89d095334e456f38a1ba3f405a579024e37f6b52be.source |
| 2524 | sweep/.mimosa/hook-state/sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_7_1.muutss62-14000-b20318c965.baseline/d59be7c17f345946f3028416eba6cdfc1d5b0d6acca31f31de03b2a4c92457fb.source |
| 4999 | sweep/.mimosa/reports/task-review-sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_7_1-20261005T053735303Z-47652-e6b1438e239c.json |
| 4999 | sweep/.mimosa/reports/task-review-sess_dwf-dwfrun-ab8d406e-3ddc-42b0-a0a9-54fa3e677cde-actor_7_1.json |

Delta during the 2026-10-05 cold-reader pass: the Mimosa hook wrote 13 new runtime artifacts (a batch-stop event, a history run record, an actor_7_1.continue state, 8 baseline .source snapshots, and 2 task-review reports), and two prior rows changed size (actor_7_1.json 1705 -> 1397; the actor_7_1 hook-status 493 -> 492); the table reflects the current measurement. The 8 .source snapshots are byte-size-identical to the eight lane instrument scripts they cache (_am_pass1.py 3,766; _am_pass2.py 3,514; _amc_deepread.py 3,622; _amc_reddit_harvest.py 5,196; _amc_rank.py 2,524; _ihn_fetch.py 1,543; _overlap.py 2,060; _gapkinds.py 772) - consistent with source snapshots, stated as a size-match observation, not a byte-diff (no diff run).

## 7. Directory totals (measured)

129 files at the final census (2026-10-05, after the cold-reader pass). Stable measured content (everything except this receipt and the mutable runtime tail): 104 files, 29,751,653 B, decomposed as fold outputs 3 files / 97,981 B (DIGEST 38,500 revised + register 24,330 + percolator 35,151; the 4th fold output is this receipt, section 1), lens 6 / 72,826, steal 10 / 100,401, sweep banks 32 / 595,312, sweep raw receipts+instruments 53 / 28,885,133. The remaining 24 files (23 .mimosa hook runtime files, 1 stray nul) are host runtime state that mutates as hooks fire; find read them at 45,708 B and the whole directory at 29,817,029 B at the census moment behind section 1's numbers (grand includes this receipt at its stated self-size). Drift note: the hook REWRITES its state files per event, so this tail has been observed oscillating between 45,707 and 45,709 B across same-session measurements (grand correspondingly 29,817,029 to 29,817,031); a reader re-measuring and differing by a few bytes in the tail is seeing that oscillation, not an error - the stable 104-file content above is the auditable part.

## 8. Finds by area (register.jsonl, 22 rows)

| area | finds |
|---|---|
| agent-memory-and-continuity via x | 7 |
| finetuning-and-adaptation | 3 |
| quantization-and-compression | 3 |
| open-and-local-language-models-arxiv | 2 |
| swarm-orchestration via x | 2 |
| evals-and-self-improvement | 1 |
| inference-efficiency via arxiv | 1 |
| kv-cache-and-context-engineering | 1 |
| open-and-local-language-models via x | 1 |
| quantization-and-compression via arxiv | 1 |
| **total** | **22** |

## 9. Finds by source

By the verbatim lane source strings carried in register.jsonl (grouped where identical):

| source (as carried, truncated) | finds |
|---|---|
| x.com via WebSearch + fxtwitter door (api.fxtwitter.com JSON + curl); overlap greps vs catalog/memory/rib/watch | 7 |
| arXiv export API via curl (20 queries, sortBy=submittedDate proven) + arxiv.org/html deep reads + HN Algolia + Arctic Shift probe | 2 |
| WebSearch quoted-"x.com" + fxtwitter 3/3 + primary pages + snowflake dating | 1 |
| arxiv.org (export.arxiv.org Atom API + arxiv.org abs pages) | 1 |
| WebSearch x-door + fxtwitter/arXiv/lmsys fetches, estate greps | 3 |
| X-door search via WebSearch (degraded) + fallback literature (arXiv/OpenReview/Google/GitHub) | 2 |
| hn | 1 |
| reddit | 1 |
| x | 2 |
| arxiv | 1 |
| arXiv: 7 export.arxiv.org queries + 13 abs reads + 1 WebSearch + state/arxiv stubs | 1 |
| **total** | **22** |

Normalized primary-host tally (rule: host of the register url field; computed by the builder script this fold): arxiv.org 8, x.com 8, daymora.com 1, github.com 1, lmsys.org 1, news.ycombinator.com 1, old.reddit.com 1, research.google 1 = 22.

## 10. Workflow gate row

`memory/workflows/REGISTRY.jsonl:64` (86-line file, read via grep this fold):

{"ts": "2026-10-04T02:33:47Z", "name": "olm-mine.dwf.ts", "digest": "70571fea3957", "script": ".zcode/workflows/olm-mine.dwf.ts", "verdict": "PASS", "checks": [G1-multiplicity ok, G2-passoff ok, G3-steering ok, G4-salvage ok, G5-deliverable ok, G6-receipts ok, G7-laws ok]}

(All seven check objects carry ok:true in the row; the full row is in the file at the cited line.)

## 11. Checks run by this fold (with the exact commands)

- Byte census: `find "$R" -type f -printf '%s\t%P\n' | sort -k2` - produced every count in sections 1-7; group sums recomputed by `.venv/Scripts/python.exe` os.walk (which skips `nul`; its 159 B is from find).
- JSONL build+verify: `.venv/Scripts/python.exe /tmp/build_fold_olm.py` - wrote both JSONL files, asserted ASCII-only and no em/en dashes on every field, re-parsed every line with json.loads: register 22/22 rows, percolator 10/10 rows, parse-clean.
- Unconfirmed-evidence re-verification on disk (grep over the lane dumps):
  - `grep -c "classifier, not a planner" sweep/_fta_thread_1wspn24.txt` -> 1 (quote byte-present); recipe numbers read at :5, :7, :14, :22; `grep -i "escape\|hatch"` -> 1 hit at :65, in the author's COMMENT (post SELFTEXT clean, so the evidence's body-level claim holds and the substance exists one hop away).
  - `grep -c "shortcut check and an independent review" sweep/_fta_thread_1wv05u1.txt` -> 1 (quote at :32); the re-pick contradiction read at :184 and :186 ("Jeff ran unquantized in these numbers", "I haven't measured that yet", "If you do quantize it, re-pick the threshold"); 95.3/86.6/38x at :17, :60, :66; jeffhub ablation comment :163.
- Headline-number spot checks in the bank files (grep -n): Mingbird 0.886 (sweep/open-and-local-language-models-arxiv.md:79), REGEXROUTE 76.43/76.41 (:102), TV median ratio 1.05 (sweep/inference-efficiency-arxiv.md:111), Google +80.9% (sweep/swarm-orchestration-x.md:138), 61% of failures (sweep/agent-memory-and-continuity-reddit.md:31), OpenRouter limits + free_model_daily_requests (sweep/open-and-local-language-models-hn.md:119,122), LIMBO idempotency 28%->4% (sweep/swarm-orchestration-arxiv.md:61,67), Mozilla config quote (sweep/inference-efficiency-hn.md:58), evalstats (sweep/evals-and-self-improvement-arxiv.md:29-31), Ask-HN census (sweep/finetuning-and-adaptation-hn.md:21).
- Workflow gate row: `grep -n "ab8d406e\|olm-mine\|fold" memory/workflows/REGISTRY.jsonl` -> row 64 (olm-mine.dwf.ts, PASS 7/7).
- Cold-reader pass (2026-10-05), checks run for the 20 DIGEST fixes: (a) loop_gaps census re-run: grep -o '"kind": "[^"]*"' training/loop_gaps.jsonl | sort | uniq -c -> 188 lifecycle_gap, 124 lifecycle_waste, 18 missing_capability, 16 missing_seat (346 rows); grep -c "" -> 346 lines; cmp training/loop_gaps.jsonl memory/training/loop_gaps.jsonl -> byte-identical; (b) missing_capability pollution spot-check (head rows carry name test_gap_unique_xyz, detail "unit", pollution field present); (c) 1wspn24 three-surface discharge: WebFetch of huggingface.co/mstrasser/Jeff-Qwen3.5-0.8B and github.com/firelex/jeff both returned escape absent, hatch absent, decision-row absent; (d) bank-anchor greps for the new line citations: lmsys NVFP4 sweep/quantization-and-compression-x.md:59-60; Noam Brown sweep/swarm-orchestration-hn.md:22; ft-arxiv :82-83, :116, :128; kapa sweep/evals-and-self-improvement-hn.md:40; 16-tool sentence sweep/swarm-orchestration-x.md:140,143; LIMBO sweep/swarm-orchestration-arxiv.md:52; 1wa5dp9 sweep/inference-efficiency-reddit.md:135; 1wxfdt9 sweep/quantization-and-compression-reddit.md:44; 1wsuag0 quote at sweep/_fta_thread_1wsuag0.txt:91 (grep count 1); 72%-problem sweep/evals-and-self-improvement-x.md:91,193; lens/doors.md:33-37 stale UNPROVEN note; web_reader X-profile variant sweep/finetuning-and-adaptation-x.md:11; Mingbird mechanism mapping steal/open-and-local-language-models-arxiv.md:7,19,21,23,25.
- Not run: pytest (no code changed by this fold), any estate probe (probe 5, reasoning-quant ladder, judge noise-floor, tank accounting, key-counter logger: all OWED and UNRUN, stated as such), any estate door re-probe (the fold's door-health contribution is byte-level bank-file verification only), citation_lint and census_drift_patrol (no tracked prose carriers changed by this fold; the fold outputs are new files in watch/inbox, the a05-r2 gate's --changed scope at next push).

## 12. Honest fold notes

- The 226 lane-item count in DIGEST.md section 1 is this fold's entry-by-entry count of the 32 lane arrays as handed over in the ask; it is not a recount of the bank .md files.
- The Mimosa PreToolUse hook blocked two earlier write attempts of the builder script (path-traversal flag on the constant output root); the landed script normalizes with os.path.realpath and enforces commonpath confinement before writing. No hook was loosened. Same false-positive class the 10-04 ft-reddit lane recorded.
- `nul` (159 B) is a stray device-name file, flagged in section 6, not deleted.
- Lane-reported discrepancies carried, not reconciled by this fold: FT census 345 (ft-hn card) vs 344 rows (Ask-HN find + ft-reddit lane); swarm-reddit lane's laws.md NOT FOUND vs lens/laws.md existing (27,370 B, measured).
- 2026-10-05 cold-reader pass: 20 fixes applied to DIGEST.md in place (window recount, U1/U2 carrier + disposition, funnel closure, per-lane 226 audit table, glosses for LIMBO/Jev/OPSD/72%-problem/Clef/glq/evalstats/kapa/thread ids, missing anchors, REGEXROUTE and Mingbird metric framing, literal card-filename note, confirmed-bar definition, row-18 capture route, Mingbird mechanisms named, S8 tau direction, S10 anchor, 1wspn24 README discharge, door-health spot-check naming, phrase rewrites, funded-credit scoping, ranked next actions 4.5); DIGEST grew 25,246 -> 38,500 B; register.jsonl and percolator_candidates.jsonl untouched; the Mimosa hook wrote 13 new runtime artifacts (section 6).
- RECEIPT self-size fixed-point: the count in section 1 was written as a placeholder, then replaced with the measured byte count and re-measured to confirm; the number below is the final measurement of this file as it stands.

receipt self-size: 20064 bytes (find-measured after the final write)
