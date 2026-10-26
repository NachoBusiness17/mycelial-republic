source-fetched: 2026-10-09

Fold receipt for the olm-mine 2026-10-09 mine fold. Seat: folder. The fold compressed the ask's mine material into DIGEST.md, register.jsonl, and percolator_candidates.jsonl; the fold seat did not re-fetch any source. Quotes and claims in the data files are carried verbatim from the ask's confirmation and steal material, cited per row. Every byte count below was measured this session with .venv\Scripts\python.exe (os.path.getsize / os.walk over the fold tree; json.loads over register.jsonl and memory/workflows/REGISTRY.jsonl).

Rediscovery note, recorded not papered over: at the start of this ask the receipt was reported missing, but on this host the file measured present and intact (os.path.exists True; 8,037 bytes; first line "source-fetched: 2026-10-09"; 112 lines; the copy written earlier today). The ask ordered a rewrite per the original spec, so this file is rewritten fresh with the complete per-file inventory, all counts re-measured now.

## Files written by this fold

| file | bytes | rows |
|---|---|---|
| watch/inbox/frontier_olm_2026-10-09/DIGEST.md | 35,393 | rev 2, post cold-reader revision |
| watch/inbox/frontier_olm_2026-10-09/register.jsonl | 26,132 | 24 confirmed finds |
| watch/inbox/frontier_olm_2026-10-09/percolator_candidates.jsonl | 31,963 | 7 steals |
| watch/inbox/frontier_olm_2026-10-09/RECEIPT.md | (this file; measured after this write and reported in the run result) | - |

Validation run this session: every line of register.jsonl and percolator_candidates.jsonl parsed with json.loads, 0 errors; em-dash (U+2014) and en-dash (U+2013) counts 0/0 for all four fold outputs; non-ASCII lines 0 everywhere except register.jsonl row 7 (a source-verbatim curly apostrophe in a source title).

## Complete inventory: every file under watch/inbox/frontier_olm_2026-10-09/

155 files, 5,947,067 bytes total, excluding RECEIPT.md itself (a file cannot contain its own final byte count; its row closes the table and its measured size is reported in the run result).

| bytes | file (relative to watch/inbox/frontier_olm_2026-10-09/) |
|---|---|
| 35,393 | DIGEST.md |
| 17,969 | lens/burns.md |
| 6,725 | lens/corpus.md |
| 3,583 | lens/doors.md |
| 4,523 | lens/graph.md |
| 25,826 | lens/laws.md |
| 11,610 | lens/questions.md |
| 31,963 | percolator_candidates.jsonl |
| 26,132 | register.jsonl |
| 10,423 | steal/agent-memory-continuity.md |
| 16,863 | steal/finetuning-adaptation-arxiv.md |
| 9,627 | steal/open-local-language-models via arxiv.md |
| 8,953 | steal/quantization-compression via reddit.md |
| 9,942 | steal/quantization-compression.md |
| 18,923 | steal/swarm-orchestration via x.md |
| 27,587 | steal/swarm-orchestration.md |
| 218 | sweep/.mimosa/hook-state/sess_dwf-dwfrun-ce3840bf-ad45-4f20-9a72-e03846fe14bd-actor_3_20.json |
| 738 | sweep/.mimosa/hook-state/sess_dwf-dwfrun-ce3840bf-ad45-4f20-9a72-e03846fe14bd-actor_3_31.json |
| 218 | sweep/.mimosa/hook-state/sess_dwf-dwfrun-ce3840bf-ad45-4f20-9a72-e03846fe14bd-actor_3_7.json |
| 218 | sweep/.mimosa/hook-state/sess_dwf-dwfrun-ce3840bf-ad45-4f20-9a72-e03846fe14bd-actor_6_1.json |
| 418 | sweep/.mimosa/hook-status/sess_dwf-dwfrun-ce3840bf-ad45-4f20-9a72-e03846fe14bd-actor_3_20-72d6f7275e.json |
| 412 | sweep/.mimosa/hook-status/sess_dwf-dwfrun-ce3840bf-ad45-4f20-9a72-e03846fe14bd-actor_3_31-5ffbc33892.json |
| 426 | sweep/.mimosa/hook-status/sess_dwf-dwfrun-ce3840bf-ad45-4f20-9a72-e03846fe14bd-actor_3_7-ea45732b8d.json |
| 5,919 | sweep/_ais_fetch_ie.py |
| 218 | sweep/_fx/.mimosa/hook-state/sess_dwf-dwfrun-ce3840bf-ad45-4f20-9a72-e03846fe14bd-actor_3_8.json |
| 2,704 | sweep/_fx/arxiv_onlineqat_2610.09346.xml |
| 10,520 | sweep/_fx/arxiv_reverify_20261009.xml |
| 8,931 | sweep/_fx/fx_Fred834567_2098036015793660124.json |
| 8,768 | sweep/_fx/fx_Sumanth_077_2082834159937241270.json |
| 4,878 | sweep/_fx/fx_WesRoth_2063048224298996062.json |
| 3,736 | sweep/_fx/fx_cjzafir_2053341219380674816.json |
| 4,632 | sweep/_fx/fx_mfranz_on_2096225605142355983.json |
| 3,830 | sweep/_fx/fx_thesupermannx_2108098865073410484.json |
| 1,602 | sweep/_fx_fleetingbits.json |
| 5,143 | sweep/_fx_kye_v16.json |
| 3,909 | sweep/_fx_sethlazar.json |
| 2,542 | sweep/_fx_shashj.json |
| 2,687 | sweep/_fx_swarms_blogs.json |
| 2,991 | sweep/_fx_swarms_v16.json |
| 2,326 | sweep/_fx_tobyord2.json |
| 2,557 | sweep/_mem_hits.txt |
| 577 | sweep/_overlap_catalog.ps1 |
| 757 | sweep/_overlap_memory.ps1 |
| 188 | sweep/_overlap_pats.txt |
| 1,043 | sweep/_overlap_siblings.ps1 |
| 8,918 | sweep/_raw/arxiv_verify.xml |
| 60,250 | sweep/_raw/localllama_top_month.rss |
| 77,841 | sweep/_raw/localllm_top.rss |
| 116,277 | sweep/_raw/ollama_top.rss |
| 631,561 | sweep/_raw/quant_search_new.rss |
| 0 | sweep/_raw/rml_top.rss |
| 164,049 | sweep/_raw/thread_1wj6c4l.rss |
| 88,078 | sweep/_raw/thread_1wpvep4.rss |
| 27,780 | sweep/_raw/thread_1wtkzc5.rss |
| 17,252 | sweep/_raw/thread_1ww528l.rss |
| 12,880 | sweep/_raw/thread_1wzrw6x.rss |
| 9,749 | sweep/_raw/thread_1x13fo2.rss |
| 17,044 | sweep/_raw/thread_1x18bsm.rss |
| 11,207 | sweep/_raw/thread_1x1bdvl.rss |
| 5,300 | sweep/_raw/thread_1x1dt7q.rss |
| 4,426 | sweep/_redlib_ie.py |
| 4,501 | sweep/_redlib_listings.py |
| 2,218 | sweep/_synd_vwapster.html |
| 2,239 | sweep/_synd_yuto.html |
| 63,805 | sweep/_txt_1wj6c4l.txt |
| 40,275 | sweep/_txt_1wpvep4.txt |
| 15,209 | sweep/_txt_1wtkzc5.txt |
| 6,790 | sweep/_txt_1ww528l.txt |
| 4,874 | sweep/_txt_1wzrw6x.txt |
| 4,069 | sweep/_txt_1x13fo2.txt |
| 6,589 | sweep/_txt_1x18bsm.txt |
| 4,315 | sweep/_txt_1x1bdvl.txt |
| 1,951 | sweep/_txt_1x1dt7q.txt |
| 24,787 | sweep/_txt_ie2_a.txt |
| 49,928 | sweep/_txt_ie2_b.txt |
| 20,803 | sweep/_txt_ie_batch2.txt |
| 49,171 | sweep/_txt_ie_batch3.txt |
| 88,340 | sweep/_txt_ie_flash_overfit.txt |
| 16,565 | sweep/agent-memory-continuity-arxiv.md |
| 12,064 | sweep/agent-memory-continuity-hn.md |
| 14,253 | sweep/agent-memory-continuity-reddit.md |
| 18,564 | sweep/agent-memory-continuity-x.md |
| 4,878 | sweep/chainlora.json |
| 19,877 | sweep/elyhahami_continual.json |
| 15,285 | sweep/evals-self-improvement-arxiv.md |
| 11,178 | sweep/evals-self-improvement-hn.md |
| 15,858 | sweep/evals-self-improvement-reddit.md |
| 18,180 | sweep/evals-self-improvement-x.md |
| 12,056 | sweep/finetuning-adaptation-arxiv.md |
| 15,115 | sweep/finetuning-adaptation-hn.md |
| 18,978 | sweep/finetuning-adaptation-reddit.md |
| 16,090 | sweep/finetuning-adaptation-x.md |
| 18,802 | sweep/gannotti_daily.json |
| 2,621 | sweep/githubprojects_lora.json |
| 35,704 | sweep/gliner_decide.json |
| 4,770 | sweep/hei_lora.json |
| 64,014 | sweep/hrswati_jev.json |
| 31,199 | sweep/ie2_dwarfstar.html |
| 78,215 | sweep/ie2_m4max_bench.html |
| 34,092 | sweep/ie2_six_days_16gb.html |
| 68,913 | sweep/ie2_smartest_models.html |
| 41,618 | sweep/ie2_stopping_midtask.html |
| 38,304 | sweep/ie2_thank_you_v41.html |
| 42,051 | sweep/ie_battlemage_kv.html |
| 53,327 | sweep/ie_flags_70pct.html |
| 86,815 | sweep/ie_flashnext6gpu.html |
| 61,798 | sweep/ie_free_rank_speed.html |
| 23,219 | sweep/ie_free_tiers_agent.html |
| 18,154 | sweep/ie_listings_census.json |
| 225,454 | sweep/ie_overfit_engines.html |
| 31,245 | sweep/ie_pool16.html |
| 26,834 | sweep/ie_qwen3next_pillars.html |
| 29,747 | sweep/ie_ubatch_pp_tg.html |
| 24,964 | sweep/ie_vulkan_pp.html |
| 14,189 | sweep/inference-efficiency-arxiv.md |
| 18,749 | sweep/inference-efficiency-hn.md |
| 25,321 | sweep/inference-efficiency-reddit.md |
| 16,993 | sweep/inference-efficiency-x.md |
| 43,844 | sweep/jvr0x_pirate.json |
| 40,231 | sweep/jvr0x_pirate2.json |
| 15,029 | sweep/kv-cache-context-engineering-arxiv.md |
| 13,795 | sweep/kv-cache-context-engineering-hn.md |
| 18,214 | sweep/kv-cache-context-engineering-reddit.md |
| 12,390 | sweep/kv-cache-context-engineering-x.md |
| 244,867 | sweep/neurondaily_laya.json |
| 10,140 | sweep/open-local-language-models-arxiv.md |
| 23,364 | sweep/open-local-language-models-hn.md |
| 10,546 | sweep/open-local-language-models-reddit.md |
| 9,637 | sweep/open-local-language-models-x.md |
| 3,490 | sweep/overlap_scan.py |
| 18,131 | sweep/quantization-compression-arxiv.md |
| 15,058 | sweep/quantization-compression-hn.md |
| 16,994 | sweep/quantization-compression-reddit.md |
| 11,974 | sweep/quantization-compression-x.md |
| 6,436 | sweep/svpino_finetune.json |
| 14,830 | sweep/swarm-orchestration-arxiv.md |
| 15,876 | sweep/swarm-orchestration-hn.md |
| 16,727 | sweep/swarm-orchestration-reddit.md |
| 19,631 | sweep/swarm-orchestration-x.md |
| 365,061 | sweep/tmp/as_aiagents_30d.json |
| 71,629 | sweep/tmp/as_c_3arch.json |
| 225,995 | sweep/tmp/as_c_census.json |
| 22,736 | sweep/tmp/as_c_engram.json |
| 54 | sweep/tmp/as_c_optchat.json |
| 87,337 | sweep/tmp/as_c_optchat2.json |
| 64,487 | sweep/tmp/as_c_spotlight.json |
| 47,498 | sweep/tmp/as_deep8.json |
| 34,810 | sweep/tmp/as_ids1.json |
| 99,936 | sweep/tmp/as_ids2.json |
| 96,824 | sweep/tmp/as_ids3.json |
| 528,814 | sweep/tmp/as_llama_30d.json |
| 391,450 | sweep/tmp/as_llama_mem30d.json |
| 54 | sweep/tmp/as_localllama_memory.json |
| 191 | sweep/tmp/pp_localllama_memory.json |
| 11,310 | sweep/unsloth_docker.json |
| (this file) | RECEIPT.md |

## Finds-by-area (register.jsonl, 24 confirmed finds)

| area | finds |
|---|---|
| agent-memory-continuity | 9 |
| finetuning-adaptation-arxiv | 7 |
| swarm-orchestration | 3 |
| swarm-orchestration via x | 2 |
| open-local-language-models via arxiv | 1 |
| quantization-compression via reddit | 1 |
| quantization-compression | 1 |
| total | 24 |

## Finds-by-source (register.jsonl, by URL host)

| host | finds |
|---|---|
| arxiv.org | 19 |
| www.reddit.com | 3 |
| x.com | 2 |
| total | 24 |

Exact per-row source-door strings, including the degraded-door records, are preserved in the register's source field and carried verbatim by the digest and percolator files.

## Steals (percolator_candidates.jsonl, 7 rows)

One row per steal card; the seven cards cover seven distinct areas, one each: agent-memory-continuity, finetuning-adaptation-arxiv, open-local-language-models via arxiv, quantization-compression, quantization-compression via reddit, swarm-orchestration, swarm-orchestration via x (areas as given in the ask card material; the percolator rows themselves carry exactly the four spec keys, claim, source_url, estate_map, probe, with no area key). Each row carries claim, source_url, estate_map, probe, copied verbatim from the ask's card material. The cards were authored by the run's steal-round actor seats earlier on 2026-10-09 and sit under steal/; this fold authored none of them.

## Workflow gate row

memory/workflows/REGISTRY.jsonl:104 is the latest gate row naming this run's script (grep 'olm-mine' over the file, run this session, 15 matching lines): olm-mine.dwf.ts, digest c7c95efcd512, ts 2026-10-06T00:52:51Z, verdict PASS.
memory/workflows/REGISTRY.jsonl:124 is the STATUS-ROW for the same script (status active, digest c7c95efcd512).
No new gate row was written by this fold seat; the fold writes no gate rows. This is the pointer the spec asks for.

## Honesty notes

- DIGEST.md is at rev 2 (cold-reader findings 1-16 addressed; sweep-item total corrected from 226 to 227; the digest's area-by-source matrix is the authority on per-sweep item counts).
- The ask's confirmations channel arrived with an empty unconfirmed array; DIGEST.md's "Unconfirmed items" section lists the 10 degraded or secondhand sweep items with what confirmation would need; none entered register.jsonl.
- Known degraded doors this window, recorded per lane in the sweep notes and summarized in DIGEST.md "Honest gaps": reddit walled in all 8 reddit lanes with working fallbacks; arXiv green in all 8 lanes; HN green in all 8 HN lanes; fxtwitter green in 7 of 8 X lanes, the evals-x lane recovered via the WebFetch network path.
- Fold-gate holder olm-mine:2026-10-09 was acquired before any write this ask and released immediately after; the gate is never held across replies.
- Not run this session: pytest (this fold wrote prose and JSONL only; the ask named no test check), any source re-fetch, any estate-side probe (the probes are banked as percolator candidates for their owning lanes).
