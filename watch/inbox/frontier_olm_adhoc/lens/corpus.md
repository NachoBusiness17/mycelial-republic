# Lens: what the estate's corpus already covers

Seat: lens-corpus (frontier_olm_adhoc sweep). Date: 2026-10-11. This file supersedes the 2026-10-10 lens at this path (that lens read the 2026-10-10T08:55:28Z catalog snapshot; this one reads today's). Every count below was counted by this seat in this session via `.venv/Scripts/python.exe` streaming aggregations over full files (commands described inline), unless the line cites a file+line instead. Anything not verified is marked OWED, never asserted.

## 1. The sources this lens read

1. `catalog/catalog_manifest.json` - snapshot_ts 2026-10-11T08:51:55Z, mode incremental, scheduler MagCorpusRescanDaily 03:30, staleness budget 48h (`catalog/catalog_manifest.json:24-29`).
2. `catalog/catalog.jsonl` - 1,136,889 lines (PowerShell `Measure-Object -Line`), all parsed as JSON by my counters with zero failures; my row count matches `tags_rows` 1,136,889 (`catalog/catalog_manifest.json:38`).
3. `catalog/tags.jsonl` - 1,136,889 rows parsed, zero failures; matches `catalog/TAG_REPORT.md:5` ("Total tagged rows: 1136889"). Day-over-day: the 10-10 lens counted 1,469,737 tags rows; the tags file was rewritten to 1:1 with catalog.jsonl since.
4. `catalog/TAG_REPORT.md` - refreshed 2026-10-11T08:51:55Z (`catalog/TAG_REPORT.md:1`); kind/age/owner sidecar report.
5. `CORPUS_CATALOG.md` - curated-shelf report run 2026-10-11T13:21:34Z (`CORPUS_CATALOG.md:3`), canon manifest DRIFT: checked 205, missing 0, drifted 4 (`CORPUS_CATALOG.md:5`).
6. `corpus/CURRICULUM.md` - role-to-materials training taxonomy (read in full, 121 lines).
7. `corpus/steal/CORPUS_FOLD_FRONTIER_OLM_20261001.md` (read in full), `memory/frontier/HELP_WANTED.md` (read in full).

## 2. Research domains the corpus already covers

### 2a. Training-library domains (the named taxonomy, `corpus/CURRICULUM.md:24-83`)

Ten role domains across 33 materials, 24 weights-eligible (W) vs RAG-only (R), every license file-verified (`corpus/CURRICULUM.md:6-11`): Agents (24-29); Post-training/RL incl. the "WHALE gap" (31-36); Inference-opt/kernels - GPU MODE, vLLM, SGLang, Triton, Liger (38-43); Evals - "strongest open shelf" (45-50); Economist/cost - zero external W canon, internal burst doctrine IS the canon (52-54); Research/data (56-60); Builder (62-65); Embodied/Android (67-71); Security - OWASP LLM Top 10, GCG, JailbreakBench (73-76); General handbooks (78-83). The W clone queue at `corpus/CURRICULUM.md:85-89` (trl, verl, vllm, sglang, triton, helm, lerobot et al.) was still NOT started as of that doc (budget breach, `:107-109`); I did not verify those repos' absence from disk beyond my library counts below - OWED if the sweep wants certainty.

### 2b. On-disk corpus shelves (my catalog counts + CORPUS_CATALOG.md's disk instrument)

Catalog rows (my count, prefix `local_sovereign_agent/corpus/`): library 52,294; oral_history 14,858; tools 6,029; dfhack_full 2,123; canon 196; steal 69. CORPUS_CATALOG.md's disk walk reports library 66,715 files / 7,235.1 MB and oral_history 15,749 (`CORPUS_CATALOG.md:18,15`) - different instrument (disk find vs catalog walk, which excluded 3,018 machinery dirs per `catalog/catalog_manifest.json:34`); never difference the two. Day-over-day: the 10-10 lens found only 101 corpus/ paths in the machine catalog; today tags.jsonl carries 75,849 corpus/ paths (my count) - the corpus shelf entered the machine catalog, so catalog.jsonl is now a valid lens for corpus/ questions (the 10-10 lens's "read CORPUS_CATALOG.md, never catalog.jsonl" law is obsolete).

Library domains (my subdirectory count, top 20 of corpus/library): ms-genai-beginners 12,142; ms-agents-beginners 9,429; zcode-zai-org 6,810; ai-engineering-from-scratch 5,401; mod-playerbots 5,000; mixar 3,669; openai-cookbook 3,120; lmcache-src 2,331; evennia 1,579; kev 934; hf-agents-course 435; second-brain-os 275; wotlk-db 226; anthropic-courses 224; pd_physical_compute 154; human-atlas 118; ractor_starter 113; image-blaster 97; interference-search 63; wakers_20260906 51. Domains: GenAI/agents curricula, LLM serving (lmcache), game servers/bots (playerbots, evennia, wotlk-db), AR (mixar), physical computing, 3D anatomy atlas.

### 2c. Frontier-OLM domain - already deep, cite before re-mining

- `corpus/steal/CORPUS_FOLD_FRONTIER_OLM_20261001.md` (read in full) banks five mechanisms: refusal measurement is regime-dependent (KV-compression keyword-refusal drop 98.0 to 80.5, McNemar p~1e-8, arXiv 2609.31678); quantization damage is stratified and agreement-counterfeiting (induction 0.959 vs retrieval 0.554 retention, arXiv 2609.23125; determinism amplified not bias, arXiv 2609.07901); context measured as bytes that reach the model not bytes sent (96.6 percent compaction loss caught in the wild); cache/quant economics with stop rules; orchestration/judge laws (HiveMind arXiv 2604.17111, judge-panel IRR, MemCodex/TAGGRAPH/mem0/EMIR2 memory findings). Plus two falsifiable probes (janitor-tier induction/retrieval battery; reach-ratio on a seat tape).
- 13 inbox directories, 2,833 files counted under `local_sovereign_agent/watch/inbox/frontier_olm*`: 20260928 466; 2026-09-30 155; 10-01 138; 10-02 78; 10-03 496; 10-04 105; 10-05 142; 10-06 372; 10-07 170; 10-08 172; 10-09 148; 10-10 150; frontier_olm_adhoc 241 (at the 08:51Z snapshot, before this lens landed).
- Related folds same day: LOCALFIRST, MUSIC, SPIKING, RACTOR50, 48H (steal/ ls count above).
- Prior OLM priors: `memory/lenses/corpus_index.json` indexes answered research packs (per the 10-10 lens: 107 packs incl. "What is the Ollama project homepage promising?"; I did not recount that file this session - number inherited, marked as such).

### 2d. Machine-catalog research surfaces (my counts)

- `state/arxiv/` 5,508 files in day-folders (top days: 2026-10-08 256; 10-05 255; 09-16 254; 09-07 253). Sampled titles span RLVR-for-LLMs, neural flows, symbolic regression, protein codesign, private retrieval - broad ML/physics/bio intake, title-grade until pulled.
- `memory/research_polished/` 17 files, 16 topics (kv_cache_compaction duplicated): KV-cache compaction, GAP_ANALYSIS_MASTER, ENHANCEMENT_STACK, substrate_gpu, swarm_flock_wave, memory_engram, economics, game_world, astra_atlas_vision, canon_harvest, persona_ractor_salon, voice_wearable, misc bands 1-3.
- `memory/research_packs/` 824 files; top packs: matt_davey_black_swan 70; bibverify 14; virtual_desk_sources 13; entity_morphology 5; square_notation_steal 5; agent_mesh_salon 5; ssi_ilya_dig 4; traj_rib 4.
- `memory/corpus/` 22,425 files: shadertoy21k 21,806 (graphics dominates); ractors 310; mycology_canon 52; game_design_docs 38; training_pdfs 36; ai_canon 33; electronics_canon 30; esoteric_canon 23; moonshot_canon 21; ml 17; founding_law 14; augmentation_canon 9; quantized_thought 7; zcode_history 5.
- `corpus/canon/`: x_canon_2026_fx 137; matthew 22; esoteric_canon 15; founding_curriculum 14 + founding-law receipts.
- `watch/inbox/frontier_asks` 105 files; `memory/frontier/HELP_WANTED.md` (generated 2026-10-11T09:05:15Z) currently asks: verkle coherence vs vector embedding, quantized lattice fold for the ghost, route/audit task-shape gaps (`memory/frontier/HELP_WANTED.md:8-11`).
- External zones (my count): azerothcore-wow 10,356; the_margin_lean 9,164; vmangos-core 4,397; tortoise-wow 3,767 (WoW emulation); library_parked 3,748; mag-current-rebuild 2,815; ext:research 767; empir3-bridge 485; teach 366; mag-sovereign-kit 310; mycelial-republic 310; ai-job-search 96; the-mountain 59; ractor-salon 30. `mine/raw` 97,865 rows (tags owner "mine" 97,867 per `catalog/TAG_REPORT.md:31` - 2-row gap between instruments, unexplained, not reconciled).

### 2e. Headline shape (manifest, read not counted)

Kinds: config 707,940; other 170,513; code 83,693; prose 82,382; image 41,155; ledger 20,182; receipt 13,273; test 8,883; brief 3,979; card 2,493; corpus 1,894; state 502 (`catalog/catalog_manifest.json:8-21`). Ages: fresh 365,300; aging 329,238; stale 334,894; fossil 107,457 (`:2-7`). Zones (my count, top): memory 701,651; lsa 243,017; runs 56,432; lsa_reboot_staging 56,343; intake 20,179. Day-over-day: kind mix shifted hard (10-10 lens read config 948,329/prose 124,769; today 707,940/82,382) - kind rules were re-cut (TAG_REPORT cites "salon Appendix B kind rules" `catalog/TAG_REPORT.md:3`); do not trend across that seam.

## 3. Denominator honesty (read before quoting any count)

- catalog.jsonl 1,136,889 = tags.jsonl 1,136,889 = manifest tags_rows 1,136,889 - all three agree today (they did not on 10-10).
- The manifest's own summary block does not reconcile: unchanged 1,121,074 + refreshed 6,371 + added 2,955 = 1,130,400 vs tags_rows 1,136,889, delta 6,489 unexplained by any manifest field I read (`catalog/catalog_manifest.json:31-42`). Same class of gap the 10-10 lens flagged (then 55,859). OWED to the catalog_rescan owner; do not guess.
- Library counts: catalog 52,294 vs disk 66,715 (`CORPUS_CATALOG.md:18`) - walk excludes machinery; name the instrument.

## 4. What this means for the frontier OLM sweep

Already covered - cite, never re-mine: KV-cache compression, quantization stratification, context reach/compaction, judge ensembles, orchestration width, agent-memory consolidation (all in CORPUS_FOLD_FRONTIER_OLM_20261001.md); Ollama basics (pack-lens index, count inherited from the 10-10 lens, not recounted); GenAI/agents curricula and LLM-serving source (lmcache) on disk. Gap surface I found no coverage for anywhere I counted (candidates for the sweep): speculative decoding, on-device finetuning/LoRA at janitor scale, distributed inference scheduling beyond prefix cache, the un-cloned W queue of `corpus/CURRICULUM.md:85-89`. Gaps the estate itself names: the two HELP_WANTED stack asks and the economist lane's zero external W canon (`corpus/CURRICULUM.md:52-54`).
