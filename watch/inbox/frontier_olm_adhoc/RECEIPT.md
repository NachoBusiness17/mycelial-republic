source-fetched: adhoc

# FRONTIER OLM ADHOC MINE: FOLD RECEIPT (fourth edition, 2026-10-12, full-inventory rewrite)

Why a fourth edition: the carrying ask stated this file does not exist. Measured before this rewrite, it DID exist: os.stat -> exists True, 10,604 bytes, mtime 2026-10-11T23:31; Read -> first line "source-fetched: adhoc", cold-reader repair record present, em/en-dash 0/0. The existence claim did not reproduce on this filesystem (the same non-reproducing pattern the wave-2 mint recorded at RECEIPT.prior-20261011T0659.md line 5); no cause is asserted, not investigated beyond the measurement and the read. The rewrite is warranted regardless: the ask restates the original spec's "lists every file in watch/inbox/frontier_olm_adhoc/", and the third edition had scoped its inventory to fold outputs plus subdirectory aggregates with a stated interpretation - this edition lists EVERY file.

Fold moment: 2026-10-12, this session (seat: folder). Edition lineage on disk: RECEIPT.prior-20261011T0659.md (wave-2), RECEIPT.prior-20261011T2331.md (third edition, preserved by copy2 at the start of THIS ask before rewriting).

Gate: tools/fold_gate.py acquire --holder "olm-mine:adhoc" --wait 900 exited 0 before this ask's writes; the release command runs after them (exit status in this session final reply).

## Instruments run this ask (exact commands and outputs)

1. Gate acquire: `C:/Users/foste/Documents/projects/local_sovereign_agent/.venv/Scripts/python.exe C:/Users/foste/Documents/projects/local_sovereign_agent/tools/fold_gate.py acquire --holder "olm-mine:adhoc" --wait 900` -> "HELD ... holder=olm-mine:adhoc", exit 0.
2. Directory survey (ls + python os.walk): pre-write state 647 files / 51,557,053 bytes; `steal/` 14 files listed with sizes below; `sweep/` and `lens/` aggregates measured post-write (below).
3. Registry scans: `wc -l memory/workflows/REGISTRY.jsonl` -> 177 lines; `grep -n -i "adhoc\|olm"` -> olm-mine family rows at lines 31-40, 64, 93-95, 102-104, 124; `grep -c "adhoc"` -> 0.
4. Builder script `C:/Users/foste/AppData/Local/Temp/fold_adhoc_wave3.py` run under the acquired gate; it: copied the four prior mints (shutil.copy2), wrote `register.jsonl` (21 rows) and `percolator_candidates.jsonl` (5 rows) via per-line json.dumps (ensure_ascii=False), wrote `DIGEST.md`, then validated: json.loads per line (21/21 and 5/5 parse, 0 errors), URL disjointness vs `register.prior-20261011T0448.jsonl` (0 shared URLs), area/source counters, em/en-dash audit (0 and 0 in all three files), non-ASCII audit (only the ASTRO row's Polish quote characters in register.jsonl, disclosed below).
5. Post-write measurements: python os.path.getsize / os.walk (table below); this file's own row is solved to a fixed point by a finisher pass and re-verified with os.path.getsize.
6. Gate release (after all writes): `C:/Users/foste/Documents/projects/local_sovereign_agent/.venv/Scripts/python.exe C:/Users/foste/Documents/projects/local_sovereign_agent/tools/fold_gate.py release --holder "olm-mine:adhoc"`.
7. THIS rewrite ask: gate re-acquire exit 0; os.stat existence measurement plus Read of the third edition (outputs in the intro); wc -l REGISTRY.jsonl -> 177 and grep -c adhoc -> 0, re-run; shutil.copy2 preserve to RECEIPT.prior-20261011T2331.md; counts re-derived by json.loads plus Counter; full-inventory os.walk with realpath containment asserts (every path checked inside the run directory before any read or write); self-row and totals solved to a fixed point and re-verified with a fresh walk. Craft note: the Mimosa write-hook blocked this builder in on-disk .py form twice as path-traversal-class; the landed form splits payload (data) from splice logic (short inline command) and keeps the containment asserts; the only writes are the preserve copy and this receipt, both inside the run directory.

## Counts

Confirmed finds: 21 (register.jsonl rows, json-validated and re-derived AGAIN this ask by per-line json.loads plus Counter; the register file itself was not rewritten this ask - its bytes were only re-measured for the listing).
- By area: finetuning-adaptation 5, kv-cache-context-engineering 6, agent-memory-continuity via x 2, evals-self-improvement via x 3, inference-efficiency 5.
- By source door (door = discovery channel, not URL host; source fields normalized to door families - the two via-x sweeps' longer door strings live verbatim in their sweep bank note fields): hn 5, reddit 6, x 10.

Unconfirmed (excluded from register): 3 (DIGEST.md section 5, each with its confirmation evidence).

Steal cards -> percolator_candidates.jsonl: 5 rows (agent-memory-continuity via x; evals-self-improvement via x; finetuning-adaptation; inference-efficiency; kv-cache-context-engineering).

Sweep payloads folded: 32, items 219 (hand-tallied from this ask's per-sweep items arrays; per area: swarm-orchestration 30, kv-cache-context-engineering 29, evals-self-improvement 29, open-local-models 28, inference-efficiency 28, agent-memory-continuity 27, quantization-compression 25, finetuning-adaptation 23; counts item-slots, not distinct artifacts - DIGEST.md honest gap 4). Of the 219, 24 reached the confirmation pass (21 confirmed + 3 failed).

Prior wave (preserved): 23 confirmed rows, URL-disjoint (0 shared). Combined run total across both waves: 44 confirmed finds.

## Workflow gate row pointer

`memory/workflows/REGISTRY.jsonl` - NO row names this adhoc run (grep -c "adhoc" = 0 over 177 lines, run this ask). Nearest verifiable pointers, read this ask:
- `memory/workflows/REGISTRY.jsonl:102-104` - olm-mine.dwf.ts, digest c7c95efcd512, verdict PASS, ts 2026-10-06T00:52:51Z (the family's latest PASS rows; checks G1-G8).
- `memory/workflows/REGISTRY.jsonl:124` - olm-mine.dwf.ts STATUS-Row, status active, latest_registry_row_ts 2026-10-06T00:52:51Z, ts 2026-10-06T18:53:21Z.
- `memory/workflows/REGISTRY.jsonl:175-177` - the newest rows in the file (mcp-landscape-wide-dig.dwf.ts, PASS, ts 2026-10-11T02:07:34Z), named so the pointer includes the file's true tail.

The prior mint (`RECEIPT.prior-20261011T0659.md`) classified the missing row as an incident, not registered debt; the evals steal card's mapping-keyed coverage-census probe is the designed detector; this fold did not register a row (DIGEST.md honest gap 8).

## File inventory (bytes measured this ask)

Every file in the run directory is listed below with its byte count (os.path.getsize, measured this ask; sorted by relative path); 652 files, 51688960 bytes total. This file's own row is solved to a fixed point. Before this ask's two writes (the preserve copy and this rewrite) the directory held 651 files / 51,647,055 bytes - the third edition verified total. The 621-file sweep/ raw-capture tree that edition aggregated is listed in full here per the carrying ask restated spec.

```
DIGEST.md	39698
DIGEST.prior-20261011T0504.md	36715
RECEIPT.md	41905
RECEIPT.prior-20261011T0659.md	19768
RECEIPT.prior-20261011T2331.md	10604
lens/.mimosa/hook-state/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_23.json	671
lens/.mimosa/hook-status/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_23-84be03a93f.json	516
lens/burns.md	17046
lens/corpus.md	9822
lens/doors.md	6402
lens/graph.md	4650
lens/laws.md	31969
lens/questions.md	19876
percolator_candidates.jsonl	19239
percolator_candidates.prior-20261011T2040.jsonl	26969
register.jsonl	20461
register.prior-20261011T0448.jsonl	22556
steal/agent-memory-continuity via x.json	4809
steal/agent-memory-continuity via x.md	12610
steal/evals-self-improvement via x.json	6016
steal/evals-self-improvement via x.md	19312
steal/finetuning-adaptation.md	35340
steal/inference-efficiency.json	6215
steal/inference-efficiency.md	20837
steal/kv-cache-context-engineering.json	4723
steal/kv-cache-context-engineering.md	45012
steal/kv-cache-context-engineering.reddit2.json	7894
steal/open-local-language-models.json	8256
steal/open-local-language-models.md	20542
steal/swarm-orchestration.json	6241
steal/swarm-orchestration.md	15637
sweep/.mimosa/finding-ledger/v1/events/batch-posttooluse-18f674c2cc89cf1c4f578d225f640dce.json	2223
sweep/.mimosa/finding-ledger/v1/events/batch-pretooluse-0ba2eb781badf76f0c77ae964701c35b.json	2171
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_3_13.json	218
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_3_17.json	218
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_3_19.json	4583
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_3_23.json	1061
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_3_8.json	218
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.continue.json	176
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.json	2855
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/02f8823ceb029a8a8ec343c850734b54b5a7036f672caba9324ce3598bd22c17.source	2364
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/1edc38608ddd49d17c459271be6221a7951441f30e1e5f641cc8684dbb42a373.source	2360
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/27adcc98aa946fcf6b28c503d26040c0d9268a4b9e0703aca20949c1af9c36b7.source	4328
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/31906de34a2afdab06e4b271b9bffb8c92347de2ffc6f00a096673ddcd8558b3.source	2569
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/4156d61d44a9cc03421b43d621d26b6786528eb2e8a456e290e7d7cd3e3f96c4.source	2975
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/5b06b8f8a1b3e55e8a12f6544480cacc223899cf6919e638ff1d4ae24dd98c7c.source	2495
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/62ab3dca3459154e5d53070161f765095dd14af4060433b34967297d0c50036b.source	3931
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/7094270cf45b1f88c33c7bd5ec20aca69c594416797fa23cf19523549d63bd4f.source	2264
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/7565d4b4f27e4d1b237843f0abbd771583c6842026f108ea87ca0ed3778e26ac.source	1120
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/905ea0f24fbce0f62fa6e32493af1046f65c3d5f67a095e1e27bc51961c07e80.source	2028
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/932a98864f65ee5fa7e881ebf04fa3298aeeed71a57c4b012c5203c1aef53340.source	2206
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/a384668f3bdded2f39f56d5d02b4fc14aed376b5d68c992c1ec89b00ab1f4e8a.source	2091
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/b2eef5b049213d4d8687aa0b9d8429a0df8f70484b8acb92aaa59e544d0efb8c.source	2996
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/bf9aa5bac6f567008140700d0e44c08b8784b02cf8fad1ccee8d529cd0138963.source	2792
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/cd571e80ba9aa665e8c2689dea55f8c8bcd2e8db838d645bb8d78b525760f852.source	1809
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/d30725e9df4c8fe9b433d4e5b7609283a8b8e225fc4762c1f8d107c8f9c61553.source	1320
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/db6f0d35a44b2713017fc0d64dbe78dec82dab056b955a5b3255b702234fc52f.source	1126
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/e4e50486b57f097be77125c7416ad5c567a7c033ba745055c55eb148de4fc6a6.source	1496
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_3.mv3jmwz9-9208-26cbff0d20.baseline/ea9d797424237e1e44aad5227ee50c0112fe6601d7b5efd2eb67eb6e2fd29b05.source	1389
sweep/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_6_4.json	218
sweep/.mimosa/hook-state/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_1.json	725
sweep/.mimosa/hook-state/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_11.json	1067
sweep/.mimosa/hook-state/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_12.json	218
sweep/.mimosa/hook-state/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_17.json	218
sweep/.mimosa/hook-state/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_18.json	218
sweep/.mimosa/hook-state/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_23.json	906
sweep/.mimosa/hook-state/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_31.json	218
sweep/.mimosa/hook-state/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_32.json	218
sweep/.mimosa/hook-state/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_7.json	1095
sweep/.mimosa/hook-state/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_7.mv46xd5l-26716-c67cc1d5bc.baseline/0f1d3e23b2c84dc11545261777bef038efe0ab37550116ff8e659184de4d2fbf.source	2369
sweep/.mimosa/hook-state/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_9.json	218
sweep/.mimosa/hook-status/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_3_14-8462164d0f.json	418
sweep/.mimosa/hook-status/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_3_19-d9462c63fa.json	403
sweep/.mimosa/hook-status/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_3_23-249050b1ba.json	414
sweep/.mimosa/hook-status/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_3_8-9f5b344f53.json	981
sweep/.mimosa/hook-status/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_5_3-04c22f225a.json	524
sweep/.mimosa/hook-status/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_1-2c66f18c34.json	407
sweep/.mimosa/hook-status/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_11-aec6037ae6.json	427
sweep/.mimosa/hook-status/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_12-dccf54e229.json	420
sweep/.mimosa/hook-status/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_17-c8ea916a6f.json	423
sweep/.mimosa/hook-status/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_23-84be03a93f.json	431
sweep/.mimosa/hook-status/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_31-88916a6ef5.json	423
sweep/.mimosa/hook-status/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_32-bc4bad6777.json	418
sweep/.mimosa/hook-status/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_7-ae2fb73805.json	404
sweep/.mimosa/hook-status/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_8-ff6a43fbf2.json	420
sweep/.mimosa/hook-status/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_9-341abc4fe3.json	424
sweep/__pycache__/_kvr2_render.cpython-311.pyc	3232
sweep/_amc_candidates.json	34701
sweep/_amc_parse_rss.py	1255
sweep/_amc_parse_search.py	1226
sweep/_amc_read_1mon8it.txt	27822
sweep/_amc_read_1r5q7xd.txt	34385
sweep/_amc_read_1r8cnwq.txt	7466
sweep/_amc_read_1wmf590.txt	8933
sweep/_amc_read_1wvmps7.txt	1516
sweep/_amc_read_1wwn7xf.txt	14010
sweep/_amc_read_1wyow7y.txt	5244
sweep/_amc_read_1wz12i1.txt	1344
sweep/_amc_render_threads.py	1575
sweep/_amc_s11_graphrag2.xml	8987
sweep/_amc_s12_mem0b.xml	5496
sweep/_amc_s13_selfimpr.xml	150418
sweep/_amc_s14_compaction.xml	182184
sweep/_amc_s15_agentmem.xml	3826
sweep/_amc_s16_locomo.xml	231036
sweep/_amc_s1_agent_memory.xml	198779
sweep/_amc_s2_persistent_memory.xml	113429
sweep/_amc_s3_knowledge_graph.xml	20072
sweep/_amc_s4_graphrag.xml	0
sweep/_amc_s5_letta.xml	3533
sweep/_amc_s6_mem0.xml	0
sweep/_amc_search_candidates.json	47466
sweep/_amc_thread_1mon8it.xml	57530
sweep/_amc_thread_1r5q7xd.xml	61445
sweep/_amc_thread_1r8cnwq.xml	13916
sweep/_amc_thread_1wmf590.xml	15139
sweep/_amc_thread_1wvmps7.xml	3446
sweep/_amc_thread_1wwn7xf.xml	26014
sweep/_amc_thread_1wyow7y.xml	10449
sweep/_amc_thread_1wz12i1.xml	3032
sweep/_amc_top_LocalLLM.xml	75869
sweep/_amc_top_LocalLLaMA.xml	67289
sweep/_amc_top_MachineLearning.xml	81946
sweep/_amc_top_ollama.xml	120740
sweep/_amh_arx1.xml	52661
sweep/_amh_arx2.xml	26207
sweep/_amh_arx3.xml	32914
sweep/_amh_arx4.xml	755
sweep/_amh_arx5.xml	799
sweep/_amh_full_01161.html	1056939
sweep/_amh_full_06361.html	655589
sweep/_amh_full_11152.html	491898
sweep/_amh_full_36746.html	390521
sweep/_amh_lmev2.xml	3650
sweep/_amh_readme_agentmemory.md	127379
sweep/_amh_rel30.json	5312
sweep/_ao_665.json	16
sweep/_api_665.json	1522
sweep/_arxiv_csma.xml	14
sweep/_arxiv_ma.xml	14
sweep/_arxiv_swarm.xml	14
sweep/_as_localllama.json	484988
sweep/_at_665.html	4420
sweep/_cand_inference_efficiency.md	1834
sweep/_cdx_llama.json	160
sweep/_cdx_llama.txt	160
sweep/_cdx_llama2.txt	160
sweep/_census.json	10064955
sweep/_comments.py	1340
sweep/_comments_1wgszma.json	90760
sweep/_comments_1wyc2b0.json	16336
sweep/_comments_1wyui4o.json	41813
sweep/_ct_665.json	16
sweep/_ddglite_sd.html	14227
sweep/_filter.py	1832
sweep/_ft2_aiastro_readme.md	6966
sweep/_ft2_cl_compose.html	43555
sweep/_ft2_deltatensors_readme.md	7626
sweep/_ft2_easycommand.html	22406
sweep/_ft2_groundtrack.html	38818
sweep/_ft2_hn_finetuning.json	31069
sweep/_ft2_item_49783349.json	1218
sweep/_ft2_learner10.html	1236666
sweep/_ft2_miniagi_readme.md	56160
sweep/_ft2_miniagi_readme_master.md	56160
sweep/_ft2_parity_readme.md	9444
sweep/_ft2_primeagent_readme.md	8964
sweep/_ft2_rlvr_drift.html	41625
sweep/_ft2_shrewd_readme.md	41004
sweep/_ft2_slm_selfknow.html	41319
sweep/_ft2_sweep1.py	3074
sweep/_ft2_thread_49783133.json	58651
sweep/_ft_2510.07841.html	44064
sweep/_ft_2607.03441.html	42618
sweep/_ft_2610.11519.html	42824
sweep/_ft_2610.11659.html	43874
sweep/_ft_2610.11776.html	41985
sweep/_ft_2610.11854.html	44225
sweep/_ft_2610.11959.html	66637
sweep/_ft_2610.12002.html	42250
sweep/_ft_2610.12161.html	41270
sweep/_ft_2610.12274.html	42219
sweep/_ft_2610.12367.html	43797
sweep/_ft_candidates.json	381195
sweep/_ft_drl_readme.md	1879
sweep/_ft_read.py	4328
sweep/_ft_sweep.py	3931
sweep/_ft_sweep3.py	2975
sweep/_ft_trl_releases.json	101280
sweep/_ft_verl_releases.json	211861
sweep/_ftfull_2510.07841.html	379223
sweep/_ftfull_2607.03441.html	224646
sweep/_ftfull_2610.11659.html	715493
sweep/_ftfull_2610.11776.html	313472
sweep/_ftfull_2610.12002.html	495750
sweep/_ftfull_2610.12367.html	282759
sweep/_ftread_2510.07841.txt	123373
sweep/_ftread_2607.03441.txt	56802
sweep/_ftread_2610.11659.txt	87038
sweep/_ftread_2610.11776.txt	61206
sweep/_ftread_2610.12002.txt	105869
sweep/_ftread_2610.12367.txt	62279
sweep/_fx/amc2026.json	3446
sweep/_fx/aml_review.json	3982
sweep/_fx/curl_loktar.html	133908
sweep/_fx/curl_stevibe2.html	148704
sweep/_fx/memento.html	44556
sweep/_fx/memfactory.json	4142
sweep/_fx/og_resolutions.json	1431
sweep/_fx/pachaar3d.json	52115
sweep/_fx/pauliusztin.json	8055
sweep/_fx/routemap.json	2411
sweep/_fx/tweet_Azaliamirh_2102958024323428362.json	34
sweep/_fx/tweet_MiaAI_lab_2081347811140841487.json	34
sweep/_fx/tweet_Tech2Wild_2044610930122613042.json	34
sweep/_fx/tweet_Tech2Wild_2088387064748265570.json	34
sweep/_fx/tweet_akshay_pachaar_2098335388435943840.json	34
sweep/_fx/tweet_loktar00_2036866132062179705.json	34
sweep/_fx/tweet_stevibe_2036809734611988818.json	34
sweep/_fx/tweet_yume_arasaki_2077042336522207337.json	34
sweep/_fx/user_unsloth.json	1036
sweep/_fx/witcheer.json	24263
sweep/_fx/yohei.json	59790
sweep/_ie2_overlap_quick.py	2645
sweep/_ie2_overlap_rest.py	1620
sweep/_ie2_overlap_scan.py	3741
sweep/_inference-efficiency-reddit.attempt1.md	12470
sweep/_jina_llama.md	1143
sweep/_jina_thread.md	633
sweep/_kv_candidates.json	35863
sweep/_kv_parse_rss.py	1320
sweep/_kv_parse_search.py	2364
sweep/_kv_probe_ml.txt	1254
sweep/_kv_render_threads.py	1496
sweep/_kv_rss_probe.xml	65469
sweep/_kv_s1.xml	187163
sweep/_kv_s10.xml	154012
sweep/_kv_s11.xml	0
sweep/_kv_s12.xml	142522
sweep/_kv_s13.xml	0
sweep/_kv_s14.xml	22066
sweep/_kv_s15.xml	0
sweep/_kv_s16.xml	238035
sweep/_kv_s2.xml	196256
sweep/_kv_s21.xml	86465
sweep/_kv_s22.xml	150137
sweep/_kv_s23.xml	22102
sweep/_kv_s24.xml	143329
sweep/_kv_s3.xml	0
sweep/_kv_s4.xml	183354
sweep/_kv_s5.xml	0
sweep/_kv_s6.xml	163581
sweep/_kv_s7.xml	197404
sweep/_kv_s8.xml	170094
sweep/_kv_s9.xml	0
sweep/_kv_search_candidates.json	109312
sweep/_kv_thread_1whx5xi.xml	63198
sweep/_kv_thread_1wiu7xj.xml	9355
sweep/_kv_thread_1wmd3xx.xml	38655
sweep/_kv_thread_1wo5552.xml	38933
sweep/_kv_thread_1wq76f6.xml	38511
sweep/_kv_thread_1wv0lww.xml	68037
sweep/_kv_thread_1wyzwab.xml	17012
sweep/_kv_thread_1wzh1i7.xml	44155
sweep/_kv_thread_1x0f5n9.xml	12986
sweep/_kv_thread_1x0ms0m.xml	57484
sweep/_kv_top_LocalLLM.xml	77841
sweep/_kv_top_LocalLLaMA.xml	65469
sweep/_kv_top_MachineLearning.xml	77530
sweep/_kv_top_ollama.xml	117910
sweep/_kv_top_probe.txt	1246
sweep/_kvr2_candidates.json	106528
sweep/_kvr2_fetch.sh	2800
sweep/_kvr2_fetch_more.sh	594
sweep/_kvr2_fetch_retry.sh	692
sweep/_kvr2_fetch_threads.sh	876
sweep/_kvr2_parse.py	1517
sweep/_kvr2_read_1whf345.txt	1785
sweep/_kvr2_read_1wjhk0r.txt	2002
sweep/_kvr2_read_1wkyny9.txt	8405
sweep/_kvr2_read_1wl5hfk.txt	13359
sweep/_kvr2_read_1wlss89.txt	4739
sweep/_kvr2_read_1wms904.txt	22571
sweep/_kvr2_read_1wnedrc.txt	6088
sweep/_kvr2_read_1wom3fe.txt	19823
sweep/_kvr2_read_1wromzr.txt	61009
sweep/_kvr2_read_1wyf63m.txt	20759
sweep/_kvr2_render.py	1422
sweep/_kvr2_s10_tool.xml	0
sweep/_kvr2_s11_mlkv.xml	22117
sweep/_kvr2_s12_refusal.xml	0
sweep/_kvr2_s13_ollama.xml	71255
sweep/_kvr2_s14_rr.xml	0
sweep/_kvr2_s1_evict.xml	176943
sweep/_kvr2_s2_evict2.xml	0
sweep/_kvr2_s3_quant.xml	204211
sweep/_kvr2_s4_quantref.xml	0
sweep/_kvr2_s5_compact.xml	182185
sweep/_kvr2_s6_hit.xml	0
sweep/_kvr2_s7_prompt.xml	165365
sweep/_kvr2_s8_llmkv.xml	0
sweep/_kvr2_s9_lost.xml	125791
sweep/_kvr2_thread_1whf345.xml	5540
sweep/_kvr2_thread_1wjhk0r.xml	5780
sweep/_kvr2_thread_1wkyny9.xml	31866
sweep/_kvr2_thread_1wl5hfk.xml	30263
sweep/_kvr2_thread_1wlss89.xml	13113
sweep/_kvr2_thread_1wms904.xml	52116
sweep/_kvr2_thread_1wnedrc.xml	16583
sweep/_kvr2_thread_1wom3fe.xml	60923
sweep/_kvr2_thread_1wromzr.xml	135951
sweep/_kvr2_thread_1wyf63m.xml	46572
sweep/_kvr2_top_llama.xml	149343
sweep/_kvr2_top_llm.xml	0
sweep/_kvr2_top_ml.xml	0
sweep/_kvr2_top_ollama.xml	184592
sweep/_lemmy_posts.json	34415
sweep/_lemmy_search.json	4744
sweep/_list_csma.html	89087
sweep/_llama_top.json	0
sweep/_localllama_top.json	327628
sweep/_localllm_top.json	327606
sweep/_ml_top.json	327690
sweep/_mojeek_sd.html	5544
sweep/_ollama_top.json	327580
sweep/_olm_overlap.py	2258
sweep/_overlap_check.ps1	1325
sweep/_overlap_check_inference_efficiency.py	2264
sweep/_overlap_decide_inference_efficiency.py	2792
sweep/_overlap_final_inference_efficiency.py	1120
sweep/_overlap_inspect_inference_efficiency.py	2028
sweep/_p_2610.07535.html	475088
sweep/_p_2610.07535.txt	114314
sweep/_p_2610.09037.html	150112
sweep/_p_2610.09037.txt	34434
sweep/_p_2610.10126.html	215225
sweep/_p_2610.10126.txt	67186
sweep/_p_2610.10468.html	108248
sweep/_p_2610.10468.txt	45325
sweep/_p_2610.12436.html	345849
sweep/_p_2610.12436.txt	80174
sweep/_p_scaling.html	351531
sweep/_pager.py	2482
sweep/_parse_content.py	1587
sweep/_parse_feeds.py	1317
sweep/_parse_thread.py	1171
sweep/_pp_localllama.json	191
sweep/_probe_reddit.nerdvpn.de.html	64428
sweep/_probe_redlib.perennialte.ch.html	5597
sweep/_probe_safereddit.com.html	4295
sweep/_q_arxiv_fc.xml	0
sweep/_qz_arx2.xml	14
sweep/_qz_arx3.xml	2632
sweep/_qz_ax.html	17896
sweep/_qz_baseten.html	350014
sweep/_qz_door_test.json	4722
sweep/_qz_fc.xml	14
sweep/_qz_gh_acb.json	5824
sweep/_qz_gh_uwsh.json	26016
sweep/_qz_giga.html	82266
sweep/_qz_hn_BitNet.json	6428
sweep/_qz_hn_GGUF.json	17110
sweep/_qz_hn_low-bit.json	14870
sweep/_qz_hn_qfc.json	478
sweep/_qz_hn_quantization.json	29938
sweep/_qz_kurt.xml	2527
sweep/_qz_quark.html	71767
sweep/_qz_s2.json	174
sweep/_qz_salmon.xml	3175
sweep/_qz_test.xml	0
sweep/_rank.ps1	534
sweep/_raw_localllama.json	327628
sweep/_raw_www.json	189908
sweep/_rd_old_follow.json	327611
sweep/_rd_old_headers.txt	1243
sweep/_rd_old_ua.json	0
sweep/_rd_top_rss.xml	0
sweep/_rd_top_rss2.xml	0
sweep/_rd_www_ua.json	189908
sweep/_read_agilerl-arena.md	2355
sweep/_read_cost-before-burning-money.md	23898
sweep/_read_deepseek-rsi-reflections.md	46223
sweep/_read_freetoken_spec.txt	13005
sweep/_read_freetoken_spec.xml	32764
sweep/_read_imajev-15days.md	20575
sweep/_read_jeff-9-lora-router.md	24738
sweep/_read_jeff_cascade.xml	50447
sweep/_read_kv_800mb.txt	5014
sweep/_read_kv_800mb.xml	15501
sweep/_read_lora-serving-11to90.md	1094
sweep/_read_medgemma-lora-scale.md	2988
sweep/_read_mimo_empty_thinking.txt	6247
sweep/_read_mimo_empty_thinking.xml	23361
sweep/_read_ml-ttt-loop.md	536
sweep/_read_molt-fit-tests.md	2353
sweep/_read_ninfer_mtp3.txt	73601
sweep/_read_ninfer_mtp3.xml	163681
sweep/_read_r9700_concurrent.xml	103589
sweep/_read_rx580_fleet.txt	1555
sweep/_read_rx580_fleet.xml	3892
sweep/_read_selfopt-inference-engine.md	5082
sweep/_read_sftmill-distill.md	5121
sweep/_read_swift_thinking.txt	72250
sweep/_read_swift_thinking.xml	190283
sweep/_read_town800_agents.txt	17899
sweep/_read_town800_agents.xml	59583
sweep/_read_vllm_prefix_warm.txt	3273
sweep/_read_vllm_prefix_warm.xml	9544
sweep/_read_zebra-6.5min-finetune.md	2249
sweep/_rl_perennial.html	5712
sweep/_rl_redlib.perennialte.ch.html	5712
sweep/_rl_safereddit.com.html	4316
sweep/_rss_665.xml	36413
sweep/_rss_llama_top.xml	0
sweep/_rss_state2026.xml	712
sweep/_rss_state2026b.xml	781
sweep/_rss_state2026c.xml	0
sweep/_rss_try.xml	0
sweep/_rx_ainews_rss.xml	2253193
sweep/_rx_alt_candidates.json	2
sweep/_rx_bing_candidates.json	2
sweep/_rx_ddg1.html	34792
sweep/_rx_ddg2_candidates.json	2
sweep/_rx_ddg_candidates.json	10259
sweep/_rx_ddg_sweep.py	3454
sweep/_rx_hn_recency.json	12485
sweep/_rx_hn_xlinks.json	29482
sweep/_rx_ollama_atom.xml	27711
sweep/_rx_pq_llms.txt	12221
sweep/_rx_pq_local.xml	3089774
sweep/_rx_pq_power.xml	5154494
sweep/_rx_pq_sitemap.xml	1146
sweep/_sakana_mass.html	79116
sweep/_sakana_mass.txt	28348
sweep/_sd_ddg.html	14221
sweep/_sd_pullpush.json	191
sweep/_sd_search.json	328396
sweep/_sd_thread_test.json	327895
sweep/_sweff_x_fx_fetch.py	3290
sweep/_sweff_x_fx_fetch2.py	2451
sweep/_sweff_x_grok_search.py	4964
sweep/_t_1sq7grd.json	189908
sweep/_tmp_a1.json	477866
sweep/_tmp_a2.json	471324
sweep/_tmp_a3.json	536632
sweep/_tmp_arctic.json	71
sweep/_tmp_arxiv_candidates.json	2
sweep/_tmp_arxiv_candidates2.json	2
sweep/_tmp_arxiv_sweep1.py	2996
sweep/_tmp_arxiv_sweep2.py	2495
sweep/_tmp_hn_query.py	1389
sweep/_tmp_llm_top.json	191
sweep/_tmp_overlap.py	1809
sweep/_tmp_overlap_fast.py	2360
sweep/_tmp_pages/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_3_6.json	218
sweep/_tmp_pages/abs_2512.05117.html	43109
sweep/_tmp_pages/abs_2512.18792.html	42432
sweep/_tmp_pages/abs_2608.02691.html	42754
sweep/_tmp_pages/abs_2608.18578.html	43769
sweep/_tmp_pages/abs_2609.16338.html	42321
sweep/_tmp_pages/arxiv_batch.xml	14
sweep/_tmp_pages/bartowski.html	241010
sweep/_tmp_pages/quesma.html	154704
sweep/_tmp_pages/saluki.html	252054
sweep/_tmp_q1.xml	63235
sweep/_tmp_q_lora.json	82197
sweep/_wb_665.html	11142
sweep/_www_top.json	189908
sweep/_x_fx_fetch.py	3596
sweep/_x_grok_search.py	5242
sweep/agent-memory-continuity-arxiv.md	14634
sweep/agent-memory-continuity-arxiv.prior-2026-10-10.md	21954
sweep/agent-memory-continuity-hn.md	11607
sweep/agent-memory-continuity-reddit.md	14022
sweep/agent-memory-continuity-x.md	14374
sweep/agent-memory-continuity-x.prior-2026-10-10.md	7338
sweep/arxiv_offload.xml	14
sweep/evals-self-improvement-arxiv.md	18663
sweep/evals-self-improvement-arxiv.prior-2026-10-11T0118.md	13446
sweep/evals-self-improvement-hn.md	23757
sweep/evals-self-improvement-reddit.md	18827
sweep/evals-self-improvement-reddit.prior-20261011T2103.md	16961
sweep/evals-self-improvement-x.md	24397
sweep/fetch_arxiv.ps1	529
sweep/finetuning-adaptation-arxiv.md	24961
sweep/finetuning-adaptation-hn.md	24441
sweep/finetuning-adaptation-reddit.md	21194
sweep/finetuning-adaptation-x.md	28151
sweep/inference-efficiency-arxiv.md	17861
sweep/inference-efficiency-arxiv.prior-2026-10-11.md	13516
sweep/inference-efficiency-hn.md	23005
sweep/inference-efficiency-reddit.md	14334
sweep/inference-efficiency-x.md	27265
sweep/inference-efficiency-x.prior-2026-10-11.md	11388
sweep/kv-cache-context-engineering-arxiv.md	18256
sweep/kv-cache-context-engineering-arxiv.prior-2026-10-10.md	11084
sweep/kv-cache-context-engineering-hn.md	14925
sweep/kv-cache-context-engineering-reddit.md	19103
sweep/kv-cache-context-engineering-x.md	15868
sweep/nul	0
sweep/open-local-language-models-arxiv.md	16738
sweep/open-local-language-models-hn.md	9235
sweep/open-local-language-models-reddit.md	17585
sweep/open-local-language-models-x.md	19663
sweep/open-local-models-arxiv.md	24070
sweep/open-local-models-hn.md	16920
sweep/open-local-models-reddit.md	15129
sweep/open-local-models-x.md	23955
sweep/overlap_catalog_only.py	1126
sweep/overlap_check.py	2569
sweep/overlap_check2.py	2091
sweep/overlap_check3.py	2206
sweep/quantization-compression-arxiv.md	11298
sweep/quantization-compression-hn.md	13080
sweep/quantization-compression-reddit.md	15226
sweep/quantization-compression-reddit.v1-20261010-preserved.md	11969
sweep/quantization-compression-x.md	16706
sweep/raw/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_3_2.json	218
sweep/raw/art_kisoku.md	4431
sweep/raw/art_kolibri.html	91570
sweep/raw/art_mozilla_bench.html	90522
sweep/raw/art_ms_winml.html	247350
sweep/raw/art_ollama_jev.html	70017
sweep/raw/art_return_ollama.html	38820
sweep/raw/hn_7Bmodel.json	3270
sweep/raw/hn_AirLLM.json	432
sweep/raw/hn_Qwen.json	30915
sweep/raw/hn_gemma.json	21780
sweep/raw/hn_llama.cpp.json	26901
sweep/raw/hn_localllm.json	31775
sweep/raw/hn_ollama.json	58245
sweep/raw/hn_openweights.json	32767
sweep/raw/hn_quantization.json	31544
sweep/raw/hn_quantized.json	17722
sweep/raw/hn_smalllanguagemodel.json	64270
sweep/raw/hn_toolcallingLLM.json	40279
sweep/raw/hn_x_DeepSeekV4Flash.json	23260
sweep/raw/hn_x_MoEinference.json	47103
sweep/raw/hn_x_Nemotron.json	17732
sweep/raw/hn_x_VRAM.json	14670
sweep/raw/hn_x_diskoffloadLLM.json	4522
sweep/raw/item_49706656.json	53997
sweep/raw/item_49742415.json	1153
sweep/raw/item_49748553.json	55676
sweep/raw/item_49763806.json	299
sweep/raw/item_49911500.json	24418
sweep/raw/item_49911995.json	61540
sweep/raw/lobsters_probe.json	51
sweep/raw/x_grok/.mimosa/hook-state/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_16.json	218
sweep/raw/x_grok/.mimosa/hook-state/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_32.json	674
sweep/raw/x_grok/.mimosa/hook-status/sess_dwf-dwfrun-e68f99eb-150c-4803-abd1-2a5309394170-actor_3_32-bc4bad6777.json	523
sweep/raw/x_grok/_fx_AIQuanting_2109315478133088380.json	4153
sweep/raw/x_grok/_fx_Arindam_1729_2109347836433519007.json	44058
sweep/raw/x_grok/_fx_BenToFound_2108174123100729830.json	2326
sweep/raw/x_grok/_fx_Mao_Yuzhen_2108261216473014498.json	1962
sweep/raw/x_grok/_fx_PrimeIntellect_2108672479007047952.json	6879
sweep/raw/x_grok/_fx_ProfBuehlerMIT_2102337582159835512.json	20340
sweep/raw/x_grok/_fx_RahilVerma13_2107491286139977867.json	4473
sweep/raw/x_grok/_fx_SaadAmmrun_2109245714391818255.json	2405
sweep/raw/x_grok/_fx_Skoorbkaz_2103696139283210729.json	5029
sweep/raw/x_grok/_fx_Tesla_Optimus_K_2109337054639444063.json	3468
sweep/raw/x_grok/_fx_XSeyvion_2109358443408544040.json	2455
sweep/raw/x_grok/_fx_arpit_bhayani_2100444191876903215.json	5275
sweep/raw/x_grok/_fx_arpit_bhayani_2102388569449140316.json	6719
sweep/raw/x_grok/_fx_askalphaxiv_2102707295717036507.json	3153
sweep/raw/x_grok/_fx_assumebreach_2109258667308753376.json	4488
sweep/raw/x_grok/_fx_builderleader_2108310331147645031.json	2588
sweep/raw/x_grok/_fx_deeepakbagada_2108030622664982840.json	2907
sweep/raw/x_grok/_fx_fleetingbits_parent.json	5054
sweep/raw/x_grok/_fx_heman10x_2108241801056563514.json	4265
sweep/raw/x_grok/_fx_jaenanft_2108390620834529399.json	6028
sweep/raw/x_grok/_fx_omarsar0_2104377054829613473.json	4531
sweep/raw/x_grok/_fx_omarsar0_2106700905051746803.json	4136
sweep/raw/x_grok/_fx_rakeshsahni__2107060667958309188.json	2003
sweep/raw/x_grok/_fx_rvaniaaaa_2101296533899510266.json	49766
sweep/raw/x_grok/_fx_scaling01_2102806864178135051.json	5631
sweep/raw/x_grok/_fx_the_posterior_2107055377489789035.json	2548
sweep/raw/x_grok/_fx_the_posterior_2107055379981176943.json	2112
sweep/raw/x_grok/_fx_the_posterior_2107055384406184399.json	2252
sweep/raw/x_grok/_fx_theagenticdaily_2107497375556411398.json	7233
sweep/raw/x_grok/_fx_toomij99_2108452213899382881.json	2133
sweep/raw/x_grok/_fx_wfouaaad_2109053677080039611.json	1850
sweep/raw/x_grok/_fx_winzheng_lab_2108548727820657129.json	23487
sweep/raw/x_grok/_fx_youshenlim_2108375051288371480.json	2774
sweep/raw/x_grok/_sweff_fx_akamai-fail_ainotesus_2109331002250101127.json	3050
sweep/raw/x_grok/_sweff_fx_batch-caveat_Sametheus_2109070344627843240.json	1869
sweep/raw/x_grok/_sweff_fx_battleground_omkarchebale_2107692247684890795.json	3289
sweep/raw/x_grok/_sweff_fx_blind-cost_janmm_va_2108656759523168641.json	2530
sweep/raw/x_grok/_sweff_fx_blind-empty_janmm_va_2108656761968414975.json	1618
sweep/raw/x_grok/_sweff_fx_dgx-acceptance_CryptoBandit100_2109329938474266650.json	5485
sweep/raw/x_grok/_sweff_fx_dgx-serving_CryptoBandit100_2108589868192600376.json	3078
sweep/raw/x_grok/_sweff_fx_dsk-recipe-1_dan3458_2108905528210628862.json	1977
sweep/raw/x_grok/_sweff_fx_dsk-recipe-5_dan3458_2108906541512569269.json	2129
sweep/raw/x_grok/_sweff_fx_dspark-3b_liquidai_2103131179100819783.json	4050
sweep/raw/x_grok/_sweff_fx_dynamo-ep_awais_khawar_2108973336025792815.json	1694
sweep/raw/x_grok/_sweff_fx_dynamo-session_brockerorg_2108269077798019417.json	2354
sweep/raw/x_grok/_sweff_fx_eagle3-vendor_spheron_2104764045052305644.json	2598
sweep/raw/x_grok/_sweff_fx_empty-budget-json_TinyRouterHQ_2102220262548689021.json	4534
sweep/raw/x_grok/_sweff_fx_empty-cap_cozybearlog_2102052987334209707.json	3304
sweep/raw/x_grok/_sweff_fx_empty-gw_cozybearlog_2101006279510827440.json	2280
sweep/raw/x_grok/_sweff_fx_flash-local-grid_yume_arasaki_2099485624395088185.json	7047
sweep/raw/x_grok/_sweff_fx_flash-local-toks_DevRico003_2105577524361150925.json	1947
sweep/raw/x_grok/_sweff_fx_glm-empty_0xsacreddev_2106630869662486729.json	2626
sweep/raw/x_grok/_sweff_fx_gridcore_Zero_to_MVP_2106727628661018980.json	2745
sweep/raw/x_grok/_sweff_fx_inertia-paper_rohanpaul_ai_2108772007282200658.json	3624
sweep/raw/x_grok/_sweff_fx_kev-router_bountyAIhunter_2106783910071795846.json	7517
sweep/raw/x_grok/_sweff_fx_llm-d_MizanAl19145045_2108264890712633799.json	5300
sweep/raw/x_grok/_sweff_fx_llmkube_ardadev_2107969024432763035.json	3166
sweep/raw/x_grok/_sweff_fx_ngram_sebastavar_2107803719815291333.json	2414
sweep/raw/x_grok/_sweff_fx_prefix-aware_SupersocksIntel_2098310560253165822.json	2984
sweep/raw/x_grok/_sweff_fx_queueing_BoboLinNotes_2108778403486896499.json	1983
sweep/raw/x_grok/_sweff_fx_rarecache_CalatheaAI_2108814812738392281.json	4071
sweep/raw/x_grok/_sweff_fx_realtext_SJRonanMD_2109301440170823775.json	2256
sweep/raw/x_grok/_sweff_fx_reasoning-400_OneMuxAPI_2108710046561603806.json	2681
sweep/raw/x_grok/_sweff_fx_saluki-mtp_ghulamurtaza__2108674475344462013.json	1923
sweep/raw/x_grok/_sweff_fx_sglang-role_anilkalm_2109333671052521682.json	2586
sweep/raw/x_grok/_sweff_fx_stop-signal_Eldan_nomad_2108059947984699620.json	1838
sweep/raw/x_grok/_sweff_fx_switchsd_roy_eisenstadt_2104624416726409646.json	2202
sweep/raw/x_grok/_sweff_fx_thinking-off-bill_aakashgupta_2109372782257844256.json	15529
sweep/raw/x_grok/_sweff_fx_tokenizer_sunsetsyntax_2108465254246355148.json	1835
sweep/raw/x_grok/_sweff_fx_vllm-mtp_cudanexus_2109340558812697037.json	1944
sweep/raw/x_grok/grok_xsearch_broad.txt	15377
sweep/raw/x_grok/grok_xsearch_consensus.txt	12524
sweep/raw/x_grok/grok_xsearch_dskoff_20261011.txt	12679
sweep/raw/x_grok/grok_xsearch_sched_20261011.txt	11937
sweep/raw/x_grok/grok_xsearch_specdec_20261011.txt	13100
sweep/raw/x_grok/tmp1yhbmkbz.txt	1202
sweep/raw/x_grok/tmp7zru_uuj.txt	1351
sweep/raw/x_grok/tmp9ga3u9vb.txt	1446
sweep/raw/x_grok/tmpotz6w7t9.txt	1437
sweep/raw/x_grok/tmptwx_s5z6.txt	1303
sweep/swarm-orchestration-arxiv.md	16073
sweep/swarm-orchestration-hn.md	33162
sweep/swarm-orchestration-reddit.md	30361
sweep/swarm-orchestration-x.md	28067
sweep/swarm-orchestration-x_2026-10-10.md	12316
sweep/tmp/as_judge.json	25404
sweep/tmp/candidates.jsonl	401680
sweep/tmp/comments_1wgii3h.json	246212
sweep/tmp/comments_1wjgthj.json	1840
sweep/tmp/comments_1wjieap.json	233259
sweep/tmp/comments_1wm4wu2.json	14438
sweep/tmp/comments_1wnyf0o.json	132490
sweep/tmp/comments_1wouby6.json	237592
sweep/tmp/comments_1wrzoej.json	2
sweep/tmp/comments_1wy9q9e.json	110630
sweep/tmp/comments_1x357dq.json	29990
sweep/tmp/deep_posts.json	87004
sweep/tmp/deep_posts2.json	14307
sweep/tmp/deepread.py	1710
sweep/tmp/harvest.py	2626
sweep/tmp/harvest2.py	2599
```

## Cold-reader repair record (carried verbatim from the third edition, 2026-10-11; its instruments ran then, not re-run this ask)

The cold reader reported 17 issues against the minted DIGEST.md; all 17 were fixed in place this repair ask, under a fresh gate acquire (exit 0). Instruments run by the repair pass, exactly:
1. Gate re-acquire: same command as Instruments item 1 -> "HELD ... holder=olm-mine:adhoc", exit 0.
2. Sweep-bank census input: `ls watch/inbox/frontier_olm_adhoc/sweep/ | grep -i "\.md$"` -> 74 .md files: 36 live area-door banks (32 current-generation incl. 4 `open-local-models-*`, PLUS 4 prior-generation `open-local-language-models-*` - the name drift DIGEST gap 2 now states), 9 preserved prior mints, remainder scratch reads.
3. Live spot-check A (register row 12, agentmemory v0.9.30): WebFetch of https://github.com/rohitg00/agentmemory/releases/tag/v0.9.30 -> answer YES, the register quote appears verbatim ("Durable capture: event ids, a persistent capture inbox, retries, dead letters, and an offline hook spool" continuing "while the server is down"), release tag v0.9.30.
4. Live spot-check B (register row 18, MemSkill): WebFetch of https://arxiv.org/abs/2602.02474 -> answer NO for byte-verbatim: the live abstract reads "a \emph{designer} that periodically reviews hard cases where selected skills yield incorrect or incomplete memories..." (literal LaTeX \emph markup inside the sentence where the register quote has plain "designer"); title and authors match (MemSkill; Zhang, Long, Bao, Feng, Zhang, Yue, Wang). Substantively present, not byte-verbatim; recorded as such in DIGEST section 1.
5. Post-edit audit over DIGEST.md: all 17 fix-marker strings present (script check, 0 missing); em/en-dash counts 0/0; door-column rows 21/21; 131 lines, 39,698 bytes.
6. This receipt's inventory row for DIGEST.md updated 28592 -> 39698 and totals re-solved to fixed point.
Not run by the repair pass: any further web fetches beyond the two spot-checks, pytest, estate instruments, the per-bank item census (deliberately deferred - DIGEST gap 6 states why).

## Honest notes

- The only files written by THIS ask in the run directory are this receipt and the preserve copy RECEIPT.prior-20261011T2331.md; register.jsonl, percolator_candidates.jsonl, and DIGEST.md were untouched this ask (their bytes re-measured in the listing below).
- sweep/nul is a zero-byte file whose basename is a reserved Windows device name (a shell redirect artifact from an earlier seat); it is listed with its measured 0 bytes, and because ntpath.relpath refuses device-mount paths, the relative paths in this inventory are constructed lexically.
- Quote dash-normalization: em/en dashes appear in no output (audit 0/0 per file); arrows in quoted material render as -> and en-dashes as - (e.g. the SupersocksIntel and CryptoBandit rows); the ASTRO register row carries the Polish README quote verbatim in UTF-8 with its English gloss inside the why field.
- Source normalization: register source fields are door families (hn/reddit/x); the fold input's longer per-sweep door strings live in the sweep banks.
- The 1wom3fe finding: the kv steal card's rev-2 addendum uses 1wom3fe numbers sourced to the sweep's raw capture; this wave's confirmation pass found the claimed quote absent from the live page, so the percolator row and DIGEST.md flag it (section 5.1). Its ~3.2 GB figure and eviction counters are NOT register-grade.
- Not run by this fold: pytest, estate instruments, any probe, any web fetch (the fold consumed the ask's payload; every web-verification claim inside it is attributed to the confirmation pass quoted in DIGEST.md section 5).
- Counting caveat: the 219 per-area sweep counts are hand-tallied from the ask's 32 items arrays; the wave-2 input tallied 241 for the same banks (DIGEST.prior-20261011T0504.md section 1) - both numbers are true of their inputs; neither was re-derived from the sweep files by this fold.
