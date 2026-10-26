source-fetched: adhoc

# FRONTIER OLM ADHOC MINE: FOLD RECEIPT (second edition, rewritten 2026-10-11)

Why a second edition: the carrying ask stated this file does not exist. Measured before this rewrite, it DID exist: 18,276 bytes, and a full Read this ask confirmed it was the unchanged first edition (its inventory still listed DIGEST.md at the pre-repair 25,888 bytes). The existence claim did not reproduce on this filesystem, and no cause for any deletion or touch is asserted (not investigated beyond the measurement and the read). The rewrite is warranted regardless: the cold-reader repair (16 issues fixed in DIGEST.md, same session) grew DIGEST.md from 25,888 to 36,715 bytes, making the first edition's inventory stale; that +10,827-byte delta is the entire directory change since the first edition (first-edition post-fold total 15,016,936 + 10,827 = current 15,027,763 bytes, exact). Every number below is measured fresh this ask.

Fold moment: 2026-10-11, this session (seat: folder, the fold gopher). Run directory: watch/inbox/frontier_olm_adhoc/ inside repo root C:/Users/foste/Documents/projects/local_sovereign_agent.
Gate: tools/fold_gate.py acquire --holder "olm-mine:adhoc" --wait 900 exited 0 ("HELD ... holder=olm-mine:adhoc") before the writes of every ask in this session (original fold, cold-reader repair, and this rewrite); released after writes in each ask.

## Instruments run this ask (exact commands and outputs)

1. Gate acquire (above), exit 0.
2. State check, this ask: os.path.exists -> RECEIPT.md True at 18,276 bytes; DIGEST.md 36,715; register.jsonl 22,556; percolator_candidates.jsonl 24,375; directory walk 281 files, 15,027,763 bytes.
3. Full Read of RECEIPT.md this ask (326 lines displayed): confirmed byte-identical first edition, first line "source-fetched: adhoc".
4. Counts re-derived this ask from register.jsonl by per-line json.loads: 23 rows, 0 parse errors; by area {swarm-orchestration 6, finetuning-adaptation 8, open-local-language-models 7, kv-cache-context-engineering 2}; by source door {arxiv 12, hn 7, reddit 4}. percolator_candidates.jsonl: 4 rows, 0 parse errors.
5. Registry scan this ask: memory/workflows/REGISTRY.jsonl full read, 177 lines, zero lines contain "adhoc"; last row ts 2026-10-11T02:07:34Z.
6. Post-write inventory walk (os.walk over the run directory) -> the table below; RECEIPT.md's own row is solved to a fixed point by the finisher and verified with os.path.getsize.

## Counts

Confirmed finds: 23 (register.jsonl rows, re-derived this ask).
- By area: swarm-orchestration 6, finetuning-adaptation 8, open-local-language-models 7, kv-cache-context-engineering 2.
- By discovery door (door = discovery channel, not URL host; register source fields are normalized door families): arxiv 12, hn 7, reddit 4.
- Novelty split (per the repaired DIGEST.md section 3 markers): 18 net-new, 5 prior banks confirmed again (Mozilla, Windows ML, RR-Evict, Slow Vale, Kolibri, each marked [P] in the DIGEST table).

Steal cards folded: 4 (percolator_candidates.jsonl rows) -> finetuning-adaptation, kv-cache-context-engineering (rev 2), open-local-language-models (rev 2), swarm-orchestration.

Sweep items banked by the run (counted from the fold input's per-sweep items arrays; banks under sweep/): 241 total -> kv-cache-context-engineering 32, evals-self-improvement 32, open-local-language-models 31, inference-efficiency 31, quantization-compression 29, swarm-orchestration 29, finetuning-adaptation 29, agent-memory-continuity 28. Of these, 23 confirmed, 1 failed quote-level confirmation (MASS as banked by the hn sweep; evidence in DIGEST.md section 5), the remaining 217 sweep-banked but never quote-re-verified (DIGEST.md honest gap 2; quote-sweep OWED by name).

Session repair record: DIGEST.md repaired this session against 16 cold-reader issues (verified this session: all 16 fix markers present, [P] markers on exactly table rows 13/14/16/17/23, zero em/en-dashes); DIGEST.md now 36,715 bytes, the size this inventory records.

## Workflow gate row pointer

NOT FOUND for this run, re-verified this ask. memory/workflows/REGISTRY.jsonl read in full: 177 lines; zero lines contain "adhoc"; the only 2026-10-11 rows are 175-177 (mcp-landscape-wide-dig.dwf.ts, PASS, last ts 2026-10-11T02:07:34Z); the latest olm-mine family rows are 102-104 (olm-mine.dwf.ts, digest c7c95efcd512, PASS, 2026-10-06T00:52:51Z). This adhoc mine run (gate holder olm-mine:adhoc) has no gate-registered row of its own; DIGEST.md honest gap 3 classifies it as an incident, not registered debt (no debt entry naming it found in this fold's scope). Nearest verifiable pointers: REGISTRY.jsonl:102-104 (family) and REGISTRY.jsonl:175-177 (newest rows in the file).

## Honest notes

- The only files written by this session in the run directory are the four fold outputs (DIGEST.md, register.jsonl, percolator_candidates.jsonl, RECEIPT.md); the +10,827-byte directory delta since the first edition is entirely the DIGEST.md repair, verified arithmetically above.
- Source normalization: register source fields are door families (arxiv/hn/reddit); the fold input's longer per-sweep source strings live in the sweep banks.
- Title normalization: one source title (Sunk Cost) contained an en-dash; rendered with a plain hyphen per seat law (noted in DIGEST.md and the register row).
- MASS register row: quote field is the verified closest passage per the confirmation evidence; the sweep's banked quote failed verbatim verification (DIGEST.md section 5).
- First-edition numbers preserved for audit: first-fold walk 277 files / 14,925,841 bytes pre-output; first-edition post-fold 281 files / 15,016,936 bytes; first-edition RECEIPT.md 18,276 bytes (the size and content found on disk at the start of this ask).

## File inventory (bytes measured this ask)

Post-rewrite state including this file: 281 files, 15029255 bytes. Every file under the run directory is listed; sizes are os.path.getsize bytes.

```
DIGEST.md	36715
lens/burns.md	12998
lens/corpus.md	6671
lens/doors.md	5219
lens/graph.md	4251
lens/laws.md	24646
lens/questions.md	16624
percolator_candidates.jsonl	24375
register.jsonl	22556
steal/finetuning-adaptation.md	11262
steal/kv-cache-context-engineering.json	4723
steal/kv-cache-context-engineering.md	16032
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
sweep/.mimosa/hook-status/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_3_14-8462164d0f.json	418
sweep/.mimosa/hook-status/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_3_19-d9462c63fa.json	403
sweep/.mimosa/hook-status/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_3_23-249050b1ba.json	414
sweep/.mimosa/hook-status/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_3_8-9f5b344f53.json	981
sweep/.mimosa/hook-status/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_5_3-04c22f225a.json	524
sweep/_arxiv_csma.xml	14
sweep/_arxiv_ma.xml	14
sweep/_arxiv_swarm.xml	14
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
sweep/_fx/memento.html	44556
sweep/_fx/memfactory.json	4142
sweep/_fx/pachaar3d.json	52115
sweep/_fx/pauliusztin.json	8055
sweep/_fx/routemap.json	2411
sweep/_fx/witcheer.json	24263
sweep/_fx/yohei.json	59790
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
sweep/_list_csma.html	89087
sweep/_llama_top.json	0
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
sweep/_read_agilerl-arena.md	2355
sweep/_read_cost-before-burning-money.md	23898
sweep/_read_deepseek-rsi-reflections.md	46223
sweep/_read_imajev-15days.md	20575
sweep/_read_jeff-9-lora-router.md	24738
sweep/_read_lora-serving-11to90.md	1094
sweep/_read_medgemma-lora-scale.md	2988
sweep/_read_ml-ttt-loop.md	536
sweep/_read_molt-fit-tests.md	2353
sweep/_read_selfopt-inference-engine.md	5082
sweep/_read_sftmill-distill.md	5121
sweep/_read_zebra-6.5min-finetune.md	2249
sweep/_sakana_mass.html	79116
sweep/_sakana_mass.txt	28348
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
sweep/agent-memory-continuity-arxiv.md	21954
sweep/agent-memory-continuity-hn.md	12014
sweep/agent-memory-continuity-reddit.md	9986
sweep/agent-memory-continuity-x.md	7338
sweep/arxiv_offload.xml	14
sweep/evals-self-improvement-arxiv.md	13446
sweep/evals-self-improvement-hn.md	12306
sweep/evals-self-improvement-reddit.md	16961
sweep/evals-self-improvement-x.md	13765
sweep/fetch_arxiv.ps1	529
sweep/finetuning-adaptation-arxiv.md	14541
sweep/finetuning-adaptation-hn.md	16028
sweep/finetuning-adaptation-reddit.md	11752
sweep/finetuning-adaptation-x.md	12386
sweep/inference-efficiency-arxiv.md	13516
sweep/inference-efficiency-hn.md	13820
sweep/inference-efficiency-reddit.md	12470
sweep/inference-efficiency-x.md	11388
sweep/kv-cache-context-engineering-arxiv.md	11084
sweep/kv-cache-context-engineering-hn.md	12888
sweep/kv-cache-context-engineering-reddit.md	20086
sweep/kv-cache-context-engineering-x.md	14321
sweep/open-local-language-models-arxiv.md	16738
sweep/open-local-language-models-hn.md	9235
sweep/open-local-language-models-reddit.md	17585
sweep/open-local-language-models-x.md	19663
sweep/overlap_catalog_only.py	1126
sweep/overlap_check.py	2569
sweep/overlap_check2.py	2091
sweep/overlap_check3.py	2206
sweep/quantization-compression-arxiv.md	9500
sweep/quantization-compression-hn.md	11831
sweep/quantization-compression-reddit.md	11969
sweep/quantization-compression-x.md	15861
sweep/raw/.mimosa/hook-state/sess_dwf-dwfrun-5d623493-19bb-456c-ab09-50a858997092-actor_3_2.json	218
sweep/raw/art_hf_gsq.html	277283
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
sweep/swarm-orchestration-arxiv.md	12184
sweep/swarm-orchestration-hn.md	9534
sweep/swarm-orchestration-reddit.md	14566
sweep/swarm-orchestration-x.md	11966
- RECEIPT.md	19768 bytes (this file; solved to fixed point and verified by os.path.getsize)
```

FOLDGATE: acquired at open of every write ask this session (exit 0 each), released at close.
