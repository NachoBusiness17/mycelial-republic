source-fetched: 2026-10-06

Fold receipt for run olm-mine:2026-10-06, run directory watch/inbox/frontier_olm_2026-10-06/. Rewritten this sitting: the fold caller reported this file missing, while my own ls at the same moment showed it on disk at 28,713 bytes (mtime 2026-10-06 21:11), so I removed my own prior artifact and regenerated it under the fold gate (acquired before this write, released after) so every number below comes from one fresh census taken this sitting. Byte counts measured by tmp_fold_census.py (kept in this directory as the instrument) run with the repo venv python: os.path.getsize over an os.walk of this directory, with the \\?\ extended-length prefix where Windows refuses to stat the run dir's literal nul file.

## 1. Files written by the fold

| File | Bytes | Content |
|---|---|---|
| DIGEST.md | 39,879 | Executive summary, top steals with estate maps, confirmed-finds table, honest gaps, unconfirmed items with evidence, door health, glossary (includes the same-day cold-reader repair pass) |
| register.jsonl | 23,583 | 22 confirmed finds, one row each (area, source, title, url, date, quote, why, overlap) |
| percolator_candidates.jsonl | 35,845 | 10 steal rows (claim, source_url, estate_map, probe) for percolator review |
| tmp_fold_census.py | 2,269 | The census/validation instrument cited above (kept as evidence) |
| RECEIPT.md (this file) | 027034 bytes (self-count, fixed-width slot; patched in place after write and re-measured) | This receipt |

## 2. Every file in the run directory, with byte counts measured this sitting

Census moment: taken after DIGEST.md, register.jsonl, percolator_candidates.jsonl and tmp_fold_census.py were final and after the prior RECEIPT.md was removed, so this file appears only in the self-count slot above. 415 files measured; 2 entries named nul (reserved device name on win32) refused measurement even through the \\?\ prefix and are recorded as UNMEASURED, not guessed (an ls -la listing, not my measurement, shows one root-level nul at 82 bytes). Format: bytes<TAB>path relative to this directory.

```
0	sweep/doors/s_llamacompaction.rss
0	sweep/raw/conf_reddit_1r6gx75.xml
0	sweep/raw/conf_reddit_1wc6tka.xml
0	sweep/raw/conf_reddit_1wdp9qc.xml
0	sweep/raw/conf_reddit_1wlhh08.xml
0	sweep/raw/thr_1wxloam.xml
0	sweep/raw/thr_1wyeanf.xml
0	sweep/_raw/reddit_confirm_err.txt
6	sweep/judge2_prompt.md
21	sweep/doors/LocalLLaMA_top_month.json.err
21	sweep/doors/LocalLLM_top_month.json.err
21	sweep/doors/MachineLearning_top_month.json.err
21	sweep/doors/ollama_top_month.json.err
54	sweep/_raw/as_LocalLLM_p10.json
60	sweep/_raw/medium_agentsmd.txt
162	sweep/_raw/bing/n_nitter.privacyredirect.com.html
177	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.continue.json
177	sweep/overlap_patterns.txt
218	sweep/.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_3_23.json
218	sweep/.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_3_26.json
218	sweep/_raw/.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_3_12.json
305	sweep/doors/ff_deep/1wa26pn.post.json
328	sweep/raw/thread_1wqqott.txt
341	sweep/raw/conf_hn_49897103.json
368	sweep/raw/conf_hn_49826663.json
388	sweep/raw/conf_hn_49627340.json
406	sweep/_raw/bing/.mimosa/hook-status/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_3_32-74e522b2b1.json
421	sweep/.mimosa/hook-status/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_3_26-cf42516872.json
558	sweep/doors/ff_deep/1wd4xxv.post.json
738	sweep/_raw/bing/.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_3_32.json
796	sweep/doors/ff_deep/1wu8tpg.post.json
980	sweep/.mimosa/hook-status/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_3_18-a5387b9282.json
1221	deep_read_urls.json
1387	sweep/.mimosa/finding-ledger/v1/events/batch-pretooluse-8dd9555ec4747b98294e9b8bd5083598.json
1391	sweep/.mimosa/finding-ledger/v1/events/batch-pretooluse-c951c63d410010d4c90a8043713bfbd7.json
1391	sweep/.mimosa/finding-ledger/v1/events/batch-pretooluse-f0098219595a6260b66a98f39730ebaa.json
1414	sweep/.mimosa/finding-ledger/v1/events/batch-posttooluse-30a82f0002797ba37f1e7261511b2646.json
1421	sweep/raw/conf_hn_49966238.json
1632	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/2124f8e4c33786a4b780221926a8d09aa34434d0d0cbc6a37a6aa42f87084fee.source
1632	sweep/_raw/bing/parse_synd.py
1718	sweep/doors/ff_arctic_pass1_err.txt
1775	sweep/raw/conf_ec_data.json
1839	sweep/raw/conf_hn_49807276.json
1854	sweep/raw/conf_fx_2098125177116848591.json
1960	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/3bfb874f691ad02883102338ac761d53c882ac1be59a794e67fae325c2b1437e.source
1960	sweep/_hn_read_1006.py
1998	sweep/doors/anubis_sha256_worker.mjs
2035	sweep/_evals_frag_adjudicate.txt
2051	sweep/_raw/bing/fx_typesafeai_status_2106197282274324846.json
2087	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/c17eeea259da8121eb87853af34013db27ec8d0d744b61326e632db959aa0093.source
2087	sweep/_fx_resolve.py
2092	sweep/_raw/bing/n_xcancel.com.html
2120	sweep/raw/memlance_falsifier_result.json
2177	sweep/_raw/bing/synd_RasvtNl.html
2183	sweep/_raw/bing/synd_main_horse.html
2197	sweep/_raw/bing/synd_reflectionai_labs.html
2227	sweep/_raw/bing/synd_kaboroevich.html
2241	sweep/_memlance_falsifier_out.txt
2269	tmp_fold_census.py
2339	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/4243b11b5c83f0638ef362c054f836da58b6a09382c4741a25428bcc9cae95e5.source
2339	sweep/_confirm_reddit2.py
2374	sweep/doors/ff_deep/1wswxn2.post.json
2578	sweep/_raw/bing/fx_ollama_status_2106186667543666841.json
2599	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/b9b56322712a0056da47d10577157beb1e07a8dda59051f419e3e361358b4565.source
2599	sweep/_confirm_reddit.py
2629	sweep/_raw/bing/fx_ollama_status_2107186849370247235.json
2673	sweep/_raw/bing/n_nitter.tiekoetter.com.html
2713	sweep/_raw/bing/fx_typesafeai_status_2106183706989953339.json
2817	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/8556713e9ddfbef56e7d92fe9d368ce892b6c4491d6518a7c0ba53fcf6ac2b64.source
2817	sweep/_memlance_ab.py
2892	sweep/_raw/deep_1006/post_1wxwtto.json
2943	sweep/doors/ff_deep/1wh5elt.post.json
2952	sweep/raw/thread_1wd4tcw.txt
2964	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/39fbdcdd536e19c927c853e7f7e8252d9cb113e8900b84dda66e59bcb2e9a832.source
2964	sweep/_hn_census_1006.py
3004	sweep/_raw/bing/fx_UnslothAI_status_2104592692072304916.json
3033	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/add033f97161217c9f2602b1d1f0ba38fc24bbcab0da3c044c455871c975ffe4.source
3033	sweep/_memlance_delayed.py
3038	sweep/_raw/memsearch_pypi.html
3245	tmp_ff_deep_read.py
3245	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/b69acf9dc98c2618bd0a26cc4c12ed4c2118ea72c18f60e2a5161d6f27c38e70.source
3265	tmp_sweep_candidates.py
3265	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/2ea176ffed0b8951a6f053c5a08e442f16e61288765249773b0fa603e7d87843.source
3268	sweep/_raw/bing/fx_typesafeai_status_2105383804936626365.json
3338	sweep/_confirm_28_out.txt
3362	sweep/_raw/deep_1006/post_1wqenk2.json
3364	tmp_ddg_search.py
3364	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/0c4c9642fac13a2445c8063bd2b3c35ccf85025ebdd2b1db12de3f408ebc8ac1.source
3371	lens/graph.md
3469	tmp_reddit_search.py
3469	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/9a48ead5580a9f62dc7a4640b4249ee6b9bc7173454a3daadbc4c4f9182bd940.source
3655	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/07612f882e884e7b1ac1d6866446bba1fdbe00396ea28eb585b9dede6b40e1e8.source
3655	sweep/_raw/as_fetch_1006.py
3670	sweep/.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_3_18.json
3676	tmp_deep_read.py
3676	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/d495d2b2cac2f393b6e79afb61b73194307241f4367283ab6fde31b8f9e7d1f5.source
3687	tmp_reddit_html_fetch.py
3687	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/762179c6ee0b96dbc6f6e0c6866ed8a71b07b2d48aeedd5d7e955cb468049a5c.source
3706	sweep/judge2_bank_summary.json
3834	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/2806ab31d4bb91cdecfa3d69e1b7be3d07116969d46d2838d956fa3297c45cb1.source
3834	sweep/doors/mem_search_fetch.py
3898	sweep/_raw/deep_1006/post_1wskysi.json
3903	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.json
3912	tmp_anubis_read.py
3912	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/1ebdf336b64c0c1fdbcd1364cb61729b786f32b275f36fc4f6c2dfd8c8217461.source
3925	lens/doors.md
3997	sweep/doors/ff_deep/1wp6gal.post.json
4035	sweep/_raw/deep_1006/post_1wz6mga.json
4098	tmp_reddit_fetch.py
4098	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/bcfe1c34c620c95a240c6493aae0bceac8561ee4e9bb3114b22fc7f72df45a1b.source
4116	tmp_ff_arctic_posts.py
4116	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/1cfd10912c9e58f9f378a18ca214e6149c0b6b3bb2e75c026aaf90092ee90309.source
4122	sweep/raw/thread_1wqa5da.txt
4298	sweep/doors/ff_deep/1wvz1ex.post.json
4298	sweep/raw/thread_1wyt020.txt
4323	sweep/_raw/bing/fx_togethercompute_status_2104965564368359681.json
4346	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/a70d5aa71388a5d41af7de7e1938d9037523c7fa66a88000ea72c2a0d952d261.source
4346	sweep/_confirm_hn2.py
4549	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/6fa732b0528ac0b7ed525f721b19e2b9d4a19d506e06755b0a5bd3b7b9f902aa.source
4549	sweep/_confirm_fx_arxiv.py
4560	sweep/_raw/deep_1006/post_1wxysy1.json
4577	sweep/doors/ff_deep/1wp5vqr.post.json
4647	sweep/raw/conf_fx_2098233059242099175.json
4675	sweep/_raw/bydate_10_context_length.json
4682	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/16f239f82adda2d83f46f8c2394c1b7bc48091bf758875750cb947a0f8c063ce.source
4682	sweep/doors/thread_read.py
4862	sweep/raw/conf_fx_2097958286146605446.json
4987	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/a04d469fea09b7613e3c66088bc37a8ee3cc928d08e676aadf40384243e5acb9.source
4987	sweep/_confirm_hn.py
5243	sweep/_raw/reddit_confirm_out.json
5249	sweep/raw/conf_fx_2098053941800100294.json
5446	sweep/_raw/bing/n_lightbrd.com.html
5514	sweep/doors/ff_deep/1wv05u1.post.json
5550	sweep/_raw/deep_1006/com_1wskysi.json
5557	sweep/_raw/bing/n_nitter.space.html
5674	lens/corpus.md
5675	sweep/_raw/deep_1006/post_1wrfp50.json
5791	sweep/doors/anubis_main.mjs
5826	sweep/_raw/medium_agentsmd.html
5962	tmp_hn_kv_sweep.py
5962	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/9701f2173d3c0f55e296a4216674cf9ec7f625b4e0df791460f730db56732e67.source
6038	sweep/_raw/bing/fx_togethercompute_status_2107139875522879939.json
6120	sweep/_raw/kaush_agentsmd.txt
6150	sweep/doors/ddg_candidates.json
6185	sweep/doors/memsearch_MachineLearning_agent_memory.rss
6248	sweep/swarm-orchestration-arxiv.md
6404	sweep/_raw/bing/fx_UnslothAI_status_2107505698531868941.json
6525	__pycache__/tmp_ff_arctic_posts.cpython-311.pyc
6787	sweep/_raw/deep_1006/post_1wfmzez.json
6819	sweep/_raw/bing/fx_ollama_status_2105152056382345544.json
6826	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/9113516e8567323d44fd66254badaebdf4b7242146247c889563f92159827889.source
6826	sweep/raw/memlance_falsifier.py
6879	sweep/_read_tooling.txt
6924	sweep/raw/conf_dirac.html
7056	sweep/_raw/deep_1006/post_1woa5d3.json
7111	sweep/doors/ff_arctic_pass1_out.txt
7163	sweep/_raw/deep_1006/post_1wyddlt.json
7206	sweep/doors/ff_deep/1wg7dd5.post.json
7464	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/d837a05c3c73bfdbd5a41044af7892908219cfd4aa3f745d24e2c6e522e9f495.source
7464	sweep/_confirm_28.py
7482	sweep/_raw/deep_1006/com_1wz6mga.json
7573	__pycache__/tmp_anubis_read.cpython-311.pyc
7617	sweep/_raw/bing/fx_UnslothAI_status_2095852388888522890.json
7765	sweep/raw/thread_1wz3xnf.txt
8332	sweep/doors/__pycache__/thread_read.cpython-311.pyc
8720	sweep/raw/conf_hn_49807413.json
8948	.mimosa/hook-state/sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025-actor_6_6.mux66hyo-20384-8ebd675429.baseline/1936f2f3b0ca319f1bf2adfa267ca360374dec1fcae6acbe43fdbd26fa116ad1.source
8948	sweep/_evals_confirm_sweep.py
8957	steal/swarm-orchestration via arxiv.md
9008	sweep/raw/thread_1w7wb0n.txt
9040	sweep/raw/conf_fx_2098148674203488422.json
9615	sweep/swarm-orchestration-hn.md
9967	sweep/doors/thread_1wyt020.rss
10037	sweep/open-and-local-models-x.md
10719	sweep/judge2_results.jsonl
11133	sweep/raw/conf_reddit_1wu6cbl.xml
11248	sweep/inference-efficiency-x.md
11427	sweep/_evals_confirm_sweep_out.txt
11653	sweep/_raw/getzep_hindsight.txt
12071	sweep/quantization-compression-arxiv.md
12230	sweep/_raw/reddit_pass2_out.json
12513	sweep/doors/ff_deep/1wu8tpg.comments.json
12523	sweep/_raw/deep_1006/com_1wxwtto.json
12532	sweep/agent-memory-continuity-arxiv.md
12895	sweep/_raw/deep_1006/post_1wgii3h.json
12901	sweep/_read_skeptics.txt
13139	sweep/_raw/bydate_12_llamacpp_cache.json
13164	steal/quantization-compression via x.md
13546	sweep/_read_49765348.txt
13874	steal/agent-memory-continuity via arxiv.md
14002	sweep/kv-context-engineering-x.md
14051	sweep/raw/thread_1wai0iv.txt
14241	sweep/_raw/bing/ddg_specdec.html
14377	sweep/doors/ddg_site_reddit_com_AQLM_quantization_2_bit.html
14395	sweep/doors/ddg_site_reddit_com_r_LocalLLaMA_IQ2_quantization.html
14407	sweep/doors/ddg_site_reddit_com_r_ollama_quantization_q4_quality.html
14414	sweep/doors/ddg_site_reddit_com_r_LocalLLaMA_new_quantization_method_paper.html
14417	sweep/doors/ddg_site_reddit_com_r_LocalLLaMA_KV_cache_quantization_q4.html
14417	sweep/doors/ddg_site_reddit_com_r_LocalLLM_quantized_model_accuracy_loss.html
14422	sweep/doors/ddg_site_reddit_com_r_LocalLLaMA_2b_model_quantization_degradati.html
14423	sweep/doors/ddg_site_reddit_com_r_LocalLLaMA_bitnet_ternary_quantization.html
14433	sweep/doors/ddg_site_reddit_com_r_LocalLLaMA_quantization_small_model_collap.html
14434	sweep/doors/ddg_site_reddit_com_r_LocalLLaMA_dynamic_quantization_imatrix_un.html
14435	sweep/doors/ddg_site_reddit_com_r_LocalLLaMA_long_context_KV_cache_f16_quali.html
14886	sweep/agent-memory-continuity-x.md
15279	sweep/swarm-orchestration-reddit.md
15500	sweep/doors/thread_d5_vq_6_primitives.html
15559	sweep/raw/thread_1wlbqnl.txt
15625	sweep/quantization-compression-hn.md
15699	sweep/swarm-orchestration-x.md
15701	sweep/inference-efficiency-reddit.md
15805	sweep/agent-memory-continuity-reddit.md
15982	lens/burns.md
16229	steal/quantization-compression via arxiv.md
16326	sweep/raw/deepread_batch.xml
16377	sweep/_raw/bydate_07_context_compression.json
16441	sweep/open-and-local-models-arxiv.md
16479	sweep/evals-self-improvement-x.md
16572	sweep/doors/thread_d6_veriloop_iq1m_ladder.html
16946	sweep/doors/thread_d3_kv_fp8_int4_longctx.html
16963	sweep/evals-self-improvement-arxiv.md
17024	sweep/raw/srch_kolibri.xml
17103	steal/agent-memory-continuity via x.md
17173	sweep/inference-efficiency-arxiv.md
17379	sweep/doors/thread_d1_q4_0p6b_decision.html
17876	sweep/open-and-local-models-reddit.md
17903	sweep/open-and-local-models-hn.md
18404	steal/kv-context-engineering.md
18473	sweep/kv-context-engineering-reddit.md
18487	sweep/kv-context-engineering-arxiv.md
18628	sweep/finetuning-adaptation-x.md
18748	sweep/doors/thread_d9_13quant_vega.html
19092	sweep/_raw/bydate_03_prefix_caching.json
19160	sweep/_hn_census_1006_out.txt
19203	sweep/finetuning-adaptation-reddit.md
19480	steal/open-and-local-models via x.md
19945	sweep/evals-self-improvement-hn.md
20026	sweep/inference-efficiency-hn.md
20693	sweep/kv-context-engineering-hn.md
20750	sweep/_raw/cohorte_governed_writes.txt
20840	sweep/_raw/arxiv_aim_search.html
21077	sweep/doors/thread_1w7wb0n.rss
21126	sweep/_raw/reddit_pass3_out.json
21569	sweep/doors/ff_deep/1wp5vqr.comments.json
21582	sweep/raw/conf_reddit_1wdasar.xml
22112	sweep/raw/conf_arxiv_batch.xml
22207	sweep/_raw/memoria_readme.md
22416	sweep/agent-memory-continuity-hn.md
22690	sweep/finetuning-adaptation-arxiv.md
22728	sweep/quantization-compression-x.md
22943	sweep/doors/ff_deep/1wv05u1.comments.json
23220	lens/laws.md
23339	sweep/_raw/deep_1006/com_1wyddlt.json
23583	register.jsonl
23681	lens/questions.md
23802	sweep/quantization-compression-reddit.md
24456	sweep/doors/ff_deep/1wd4xxv.comments.json
24666	sweep/evals-self-improvement-reddit.md
24929	sweep/_read_home_training.txt
25406	steal/quantization-compression.md
25643	steal/finetuning-adaptation.md
25971	sweep/_raw/bydate_02_prompt_cache.json
26264	steal/agent-memory-continuity.md
26308	sweep/raw/conf_arcticshift.json
26746	sweep/doors/ff_deep/1wswxn2.comments.json
26892	sweep/doors/search_MachineLearning_quantization.html
26998	sweep/finetuning-adaptation-hn.md
27146	sweep/_raw/candidates.json
28504	sweep/_read_bench.txt
30959	sweep/_raw/rel_14_kv_cache.json
32306	sweep/_raw/deep_1006/com_1wxysy1.json
32623	sweep/_raw/deep_reads_out.json
32715	sweep/_raw/bydate_09_cache_hit.json
35261	sweep/_raw/deep_reads2_out.json
35749	sweep/_raw/kaush_agentsmd.html
35845	percolator_candidates.jsonl
36411	sweep/doors/ddg_site_reddit_com_r_LocalLLaMA_Q4_K_M_vs_Q8_0_quality.html
36776	sweep/doors/memsearch_LocalLLaMA_knowledge_graph.rss
38007	sweep/raw/conf_hn_49869735.json
38405	sweep/_raw/bing/synd_parsed2.txt
38829	sweep/_raw/bydate_04_kv_cache.json
39391	sweep/_raw/bydate_01_prompt_caching.json
39879	DIGEST.md
40776	sweep/_raw/cohorte_governed_writes.html
41004	sweep/raw/conf_shrewd_readme.md
41235	sweep/_raw/bing/synd_parsed.txt
41620	sweep/_raw/deep_1006/com_1wfmzez.json
43056	sweep/_raw/rel_13_prompt_caching.json
43316	sweep/doors/ff_deep/1wh5elt.comments.json
43599	sweep/_raw/aim_2609.12320.html
47581	deep_reads.json
51662	sweep/doors/thread_d10_44m_from_scratch.html
53152	sweep/_raw/bydate_05_context_engineering.json
53174	sweep/_raw/rel_15_context_engineering.json
53541	sweep/_raw/bing/fx_typesafeai_status_2105695667486355848.json
54471	sweep/_raw/rel_16_compaction.json
55676	sweep/raw/conf_hn_49748553.json
57919	tmp_rss_llamamonth.xml
57919	sweep/raw/rss_LocalLLaMA.xml
62122	sweep/doors/ff_deep/1wa26pn.comments.json
64199	sweep/raw/thread_1wl3828.txt
64203	sweep/doors/LocalLLaMA_top_month.html
64203	sweep/doors/LocalLLaMA_top_month_sr.html
65978	sweep/doors/search_ollama_quantization.html
66583	sweep/_localllama_rss.xml
67918	sweep/doors/candidates.json
68239	sweep/doors/thread_d8_phantom_kv_inject.html
69699	sweep/doors/thread_d11_prismml_bonsai_compare.html
70622	sweep/doors/search_ollama_KV_cache.html
71273	sweep/doors/ff_deep/1wp6gal.comments.json
71930	sweep/doors/ff_deep/1wvz1ex.comments.json
72675	sweep/raw/sweep_q3_peft.xml
74274	sweep/raw/sweep_q2_forget_distill.xml
77870	sweep/raw/sweep_q1_lora_agents.xml
79317	sweep/doors/LocalLLM_top_month.rss
79317	sweep/raw/rss_LocalLLM.xml
80393	sweep/doors/memsearch_candidates.json
82356	sweep/raw/conf_duanesh.html
84602	sweep/doors/MachineLearning_top_month.rss
84602	sweep/raw/rss_MachineLearning.xml
84693	sweep/doors/LocalLLM_top_month.html
84744	sweep/doors/ff_deep/1wg7dd5.comments.json
86480	sweep/doors/search_LocalLLM_quantized_accuracy.html
86602	sweep/doors/search_LocalLLaMA_ternary.html
91370	sweep/raw/thr_1wv4zzi.xml
93157	sweep/doors/ollama_top_month.html
93347	sweep/doors/MachineLearning_top_month.html
94256	sweep/raw/thr_1wvv6im.xml
95353	sweep/_raw/bydate_06_context_window.json
96060	sweep/doors/memsearch_LocalLLaMA_forget.rss
96133	sweep/doors/ollama_top_month.rss
96133	sweep/raw/rss_ollama.xml
98668	sweep/_raw/bydate_11_system_prompt.json
99458	sweep/doors/thread_d7_iq3xxs_vs_pq2.html
99946	sweep/doors/memsearch_LocalLLaMA_persistent_memory.rss
108533	sweep/_raw/bydate_08_context_rot.json
110190	sweep/doors/search_LocalLLaMA_IQ2.html
110590	sweep/_raw/bing/synd_ollama.html
112000	sweep/_raw/memsearch_pypi.json
118038	sweep/doors/search_candidates.json
118456	sweep/raw/conf_hn_49923692.json
120534	sweep/doors/search_LocalLLaMA_quantization.html
121466	sweep/_raw/bing/bing_specdec.html
124210	sweep/_raw/deep_1006/com_1wqenk2.json
125405	sweep/_raw/bing/synd_togethercompute.html
127522	sweep/raw/conf_fx_2097689256961466486.json
133686	sweep/raw/conf_needle_rpi.html
134003	sweep/_raw/bing/synd_Alibaba_Qwen.html
134806	sweep/raw/conf_2609.17848_full.html
137112	sweep/raw/srch_decision.xml
142077	sweep/doors/thread_d2_bonsai_98pct_fp16.html
143532	sweep/_raw/bing/synd_typesafeai.html
146571	sweep/_raw/getzep_hindsight.html
148092	sweep/doors/memsearch_ollama_memory.rss
151568	sweep/doors/search_LocalLLaMA_Q4_K_M.html
152292	sweep/doors/search_LocalLLaMA_KV_cache_quantization.html
157776	sweep/doors/memsearch_LocalLLaMA_summarization.rss
165695	sweep/_raw/bing/synd_unsloth.json
187443	sweep/doors/search_LocalLLM_quantization.html
192580	sweep/doors/memsearch_LocalLLaMA_long_term_memory.rss
194694	sweep/doors/thread_d4_stop_fp4_engines.html
194842	sweep/_raw/deep_1006/com_1woa5d3.json
201751	sweep/doors/s_llamamemory.rss
202491	sweep/_raw/deep_1006/com_1wrfp50.json
205671	sweep/doors/memsearch_LocalLLM_agent_memory.rss
208237	sweep/_raw/deep_1006/com_1wgii3h.json
244004	sweep/judge2_items.jsonl
267633	sweep/raw/deep_2610.01493.html
374269	sweep/raw/deep_2610.02542.html
451081	sweep/_raw/as_LocalLLaMA_p6.json
451155	sweep/_raw/as_LocalLLaMA_p22.json
456923	sweep/_raw/as_LocalLLaMA_p9.json
469486	sweep/raw/deep_2609.39346.html
469519	sweep/_raw/as_LocalLLaMA_p20.json
474622	sweep/_raw/as_LocalLLaMA_p12.json
481990	sweep/_raw/as_LocalLLaMA_p21.json
482342	sweep/_raw/as_LocalLLaMA_p0.json
484835	sweep/_raw/as_LocalLLaMA_p7.json
489928	sweep/_raw/as_LocalLLaMA_p17.json
491442	sweep/_raw/as_LocalLLaMA_p8.json
493266	sweep/_raw/as_LocalLLaMA_p10.json
494833	sweep/_raw/as_LocalLLaMA_p5.json
494889	sweep/_raw/as_LocalLLaMA_p18.json
499345	sweep/_raw/as_LocalLLaMA_p19.json
514922	sweep/_raw/as_LocalLLaMA_p1.json
515961	sweep/_raw/as_LocalLLaMA_p15.json
516374	sweep/_raw/bing/synd_rohanpaul_ai.html
518619	sweep/_raw/bing/synd_CloudflareDev.html
518890	sweep/_raw/as_LocalLLaMA_p13.json
520366	sweep/_raw/as_LocalLLaMA_p11.json
529229	sweep/_raw/as_LocalLLM_p9.json
531157	sweep/_raw/as_LocalLLaMA_p3.json
532375	sweep/_raw/as_LocalLLaMA_p2.json
543030	sweep/_raw/as_LocalLLaMA_p14.json
550509	sweep/_raw/as_LocalLLaMA_p16.json
559623	sweep/_raw/as_LocalLLaMA_p4.json
560990	sweep/_raw/as_ollama_p5.json
563387	sweep/_raw/as_ollama_p4.json
565499	sweep/raw/deep_2610.00928.html
571654	sweep/_raw/bing/synd_ggerganov.html
574440	sweep/_raw/as_ollama_p3.json
575776	sweep/_raw/as_ollama_p2.json
584546	sweep/_raw/bing/synd_danielhanchen.html
589117	sweep/_raw/as_ollama_p0.json
598656	sweep/_raw/as_LocalLLM_p7.json
605591	sweep/_raw/as_LocalLLM_p6.json
605614	sweep/_raw/as_ollama_p1.json
625046	sweep/_raw/as_LocalLLM_p8.json
643293	sweep/raw/deep_2610.05303.html
747868	sweep/_raw/bing/synd_vllm_project.html
762243	sweep/_raw/as_LocalLLM_p5.json
944048	sweep/_raw/as_rows_1006.jsonl
1089547	sweep/raw/deep_2610.06542.html
3843832	sweep/_raw/as_merged_1006.jsonl
9130585	sweep/doors/ff_arctic_posts.jsonl
```

Integrity note: the block above is injected verbatim from the census output file (C:/Users/foste/AppData/Local/Temp/fold_census_1006_regen.txt, the redirect target of this sitting's census run) by script, not retyped; the diff assertion ran after injection and is recorded in section 5. Re-runnable: .venv/Scripts/python.exe watch/inbox/frontier_olm_2026-10-06/tmp_fold_census.py

## 3. Finds-by-area (register.jsonl, 22 confirmed rows; script output)

| Area | Confirmed finds |
|---|---|
| finetuning-adaptation | 7 |
| agent-memory-continuity | 3 |
| kv-context-engineering | 3 |
| agent-memory-continuity via arxiv | 2 |
| quantization-compression | 2 |
| agent-memory-continuity via x | 1 |
| open-and-local-models via x | 1 |
| quantization-compression via arxiv | 1 |
| quantization-compression via x | 1 |
| swarm-orchestration via arxiv | 1 |
| **Total** | **22** |

## 4. Finds-by-source (register.jsonl, 22 confirmed rows; script output)

Bucket rule: an area ending "via x" / "via arxiv" / "via hn" buckets to that lane; otherwise the source string's named door leads (Hacker News or hn.algolia -> hn; x.com or X door -> x; reddit -> reddit; arXiv -> arxiv).

| Source door | Confirmed finds |
|---|---|
| hn (hn.algolia.com API) | 7 |
| x.com (fxtwitter/vxtwitter/syndication doors) | 6 |
| reddit (Atom RSS / safereddit mirror) | 5 |
| arXiv (export API + abs/html) | 4 |
| **Total** | **22** |

## 5. Validation run and workflow gate row pointer

Validation (script output this sitting): REGISTER_ROWS 22; JSONL_VALIDATE register.jsonl rows=22 errors=0; JSONL_VALIDATE percolator_candidates.jsonl rows=10 errors=0. The BY_AREA and BY_SOURCE tables above are the script's own output, not hand counts. The injected census block was diffed line-for-line against the census output file after injection; result: 0 mismatches across all 415 lines (asserted by script this sitting).

Workflow gate row pointer: memory/workflows/REGISTRY.jsonl:124 - STATUS-ROW for olm-mine.dwf.ts, digest c7c95efcd512, script .zcode/workflows/olm-mine.dwf.ts, status active, fire_count 3, last_fire 2026-10-06T00:52:51Z PASS, latest_registry_row_digest matches (re-grepped this sitting). The same-day PASS gate rows for this workflow are memory/workflows/REGISTRY.jsonl:102-104 (ts 2026-10-06T00:52:43Z/45/51Z, digests 1d0e15d62fa1 / f8199bba6ead / c7c95efcd512, all G1-G8 checks true, including G7 no-fabrication and em-dash law and G8 width shape).
