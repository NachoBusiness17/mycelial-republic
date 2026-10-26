# Sweep: quantization-compression via x - 2026-10-06

Area: quantization-compression via x. source-fetched: 2026-10-06. Every item below was fetched
and read by this seat during this ask; notes carry the stamp. Quotes are verbatim from the
fetched pages as returned by the fetch instrument. House laws held: ascii only, no em or en
dashes, every claim names what was read or run, nothing run is claimed as run.

## Door status (honest)

- The X door degraded again this cycle, same shape as the 10-05 sweep
  (watch/inbox/frontier_olm_2026-10-05/sweep/quantization-compression-x.md:9-15): most
  `site:x.com` WebSearch volleys came back rate-limited (MCP error -429 / code 1302) or with
  zero indexed x.com hits; X is largely unindexed. Four fxtwitter resolves DID succeed
  (analogalok 2090400471458759145 and 2090432439386874143, TeksEdge 2090228570253861075,
  mfranz_on 2096225605142355983, all via https://api.fxtwitter.com, HTTP 200 full JSON) but
  every one is dated Aug 20 or Sep 5 2026, outside the 30-day window, so they bank as context
  rows, not items.
- One X-profile lead (x.com/Anbeeld, Ivan Neustroev, KV cache quantization) could not resolve
  to a status id: the fxtwitter user endpoint https://api.fxtwitter.com/Anbeeld returns profile
  metadata only (bio, counts, 515-tweet count, website anbeeld.com), no timeline. Per the
  recipe fallback the search-result snippet is banked below UNRESOLVED, and its two headline
  claims were then checked against the author's own site and NOT found there; never assert
  them.
- Working doors that carried the sweep: the arXiv export API sorted by submittedDate (the
  recipe doors.md:28-29 marked OWED; executed today, answered with in-window rows) and the
  author's own site anbeeld.com (articles index fetched end to end, then three articles read
  end to end).

## Anti-rebank fence

Prior quantization sweeps hold a large 2609.x + early 2610.x id set
(watch/inbox/frontier_olm_2026-10-0{1,2,3,4,5}/sweep/quantization*.md); the STEPQuant,
WUSH-KV, QuantMLA, TORQUE, PQ-HSA, FlashLoop, QuantWM, KV-COBRA, D-Quant rows returned by
today's feed read are all already title-known there and are NOT re-banked. 2610.03039
(HyperThink) is a banked card (lens/burns.md:131) and is used only as the RQ5 anchor. Of
today's items, 2610.04403 and 2610.04490 read zero hits in catalog/catalog.jsonl and memory/;
2610.03027, 2610.05685, 2610.02462, 2610.06174, 2610.05977 hold auto-fetched abstract
snapshots in state/arxiv/ (catalog rows, mtimes 2026-10-05/06) with no sweep, register, or
memory mining hit, so the deep read plus estate synthesis is the new content and the overlap
is stated per item. ERRATUM (folded after first write, caught by the completed deep grep): an
earlier draft claimed zero prior-sweep hits for "Anbeeld"; the deep grep disproves that -
Anbeeld the TOOL is already banked: watch/inbox/frontier_olm_2026-10-02/sweep/
kv-cache-context-engineering-hn.md read github.com/Anbeeld/beellama.cpp end to end (README:
"Variance-normalized KV-cache quantization (KVarN)"), and the 10-03 arctic sweep files
(arctic_LocalLLaMA.json, thread_1wr5ylm.json) mention the fork. What is new today is the
author's benchmark ARTICLES (the long-context KV tables, the KVarN + precision-tail
measurements, the Gemma 4 31B QAT-vs-non-QAT study), which no prior file holds; the two
Anbeeld items below bank the articles with this overlap stated. KVarN the METHOD is also
already registered (memory/runs/ds_batches/gapfold_items.jsonl names arXiv 2606.03458, and
2606.03458 sits in the prior-sweep id fence), so KVarN gets a context row, not an item. The
"BARQ" substring hits in memory/corpus/ai_canon/dlb_* and memory/runs/
quote_audit_wide_20260925/inbox_concat.txt are false positives (different token), so 2610.04490
stays genuinely new.

## Items (strongest first)

1. **Saying, Not Knowing: Aggressively GGUF-Quantized Small Language Models Still Write Rare
   Words They Can No Longer Define** - arXiv:2610.04403 (Singh, Dadwhal, Vedak; submitted
   2026-10-03, read end to end). The estate's RQ1 answered in public for the first time this
   cycle: 27 GGUF K-quant artifacts across 13 families, 0.35B-14B, audited down the published
   ladder to Q2_K (~2.6 bits/weight) on 429 frequency-validated rare English words. Three
   regimes at Q2: unusable builds, severe semantic dissociation in sub-2B models, robust
   preservation above ~3B. Sub-2B definitions fall 20-67 percent below baseline, several times
   the inclusion loss; loss rises with rarity in 6 of 7 sub-2B artifacts; parameter count
   dominates (Spearman rho=0.72) while tokenizer vocab does not (rho=0.12); Q4_K_M stays
   lexically clean at 1B and up; and WikiText-2 perplexity fails to calibrate any of it (nine
   matched ladders, near-identical Q2 PPL penalties 44.7 vs 47.6 percent, yet one artifact
   keeps definitions at 3.6 percent loss and another loses 43.6 percent). This is the
   external prior for the owed qwen2.5:7b A/B and the 2b-class bit-ladder extension: expect
   the "4-bit holds" half to replicate at 2B, expect the 1-bit/2-bit collapse to be
   definitional and frequency-graded rather than perplexity-visible, and validate per
   artifact, never per family.

2. **KV Cache Quantization on Gemma 4 31B: Non-QAT vs QAT** - anbeeld.com
   (https://anbeeld.com/articles/kv-cache-quantization-standard-vs-qat-gemma-4-31b, read end
   to end; the site shows no publication date, but its subject gemma-4-31B only reached the
   Ollama library ~2026-10-01 per the 10-05 sweep's library pull
   (frontier_olm_2026-10-05/sweep/quantization-compression-x.md:93-99), so the article
   necessarily postdates it). Same weights bit (Q4_0), QAT vs non-QAT checkpoint, 32k context,
   BeeLlama v0.4.3, RTX 3090: mean KLD at q8_0 KV is 0.305575 non-QAT vs 0.015078 QAT (20.3x);
   at q4_0 0.880436 vs 0.090504 (9.7x); at q2_0 4.176003 vs 1.058423 (3.9x). QAT q4_0 KV
   (1057.5 MiB) beats non-QAT q8_0 KV (1997.5 MiB) on both KLD and same-top percent (86.337 vs
   85.115) while carrying 940 MiB less cache. Verdict verbatim: "The benchmark supports a
   qualified yes, not a finished deployment verdict." Overlap (corrected): Anbeeld the tool
   (beellama.cpp) is banked in the 10-02 kv-cache HN sweep; this Gemma 4 31B QAT-vs-non-QAT
   measurement study is new to the estate. For the estate map: this is the janitor
   family (gemma4) measured under the exact interaction the AQLM method-tier rule
   (lens/burns.md:57) predicts, now with numbers - checkpoint provenance (QAT vs not) is a
   tier of its own, 20x at the same nominal bit width.

3. **Tailoring the Quantization Space for 1-Bit KV Cache Compression (TaSQ)** -
   arXiv:2610.03027 (Cheong, Son, Yoo; submitted 2026-10-02, read end to end; overlap: catalog
   holds the auto-fetched abstract snapshot state/arxiv/2026-10-05/2610.03027v1.txt, no mining
   hit). 1-bit KV via vector quantization survives only after tailoring the VQ target space
   (query-guided channel weighting, cross-head normalization, covariance-aware channel
   grouping), with RoPE-compatible transforms that "can be easily merged into projection
   weights and codebooks"; SGLang on one RTX 6000 Ada serves "up to 14x larger batch sizes and
   achieves 1.87x higher peak throughput compared to the BF16 baseline" while outperforming
   low-bit KV VQ baselines on general, long-CoT, and long-context retrieval benchmarks. The
   B4 KV ladder's next rung down has a public recipe: 1-bit KV is viable, but only with
   activation-statistics-aware target shaping, never plain q4_0-style uniform grids.

4. **Spend Bytes on Breadth: Precision-Count Trade-offs for Decode-Time KV Compression in
   Long Chain-of-Thought Reasoning (BreadthKV)** - arXiv:2610.05685 (Runguo Li, sole author;
   submitted 2026-10-05, read end to end; overlap: catalog snapshot
   state/arxiv/2026-10-05/2610.05685v1.txt, no mining hit). At a fixed KV byte budget during
   decode-time reasoning, breadth (more tokens, lower precision, eviction combined) beats
   eviction-only in 17 of 18 settings, with bit-widths chosen by 60-problem end-to-end
   calibration instead of offline attention error. Sharpest number: on Qwen3-8B at the
   tightest budget, eviction-only sends 91 percent of AIME samples to the length cap vs 40
   percent for BreadthKV; matches a rate-distortion allocator (RDKV) with 27 percent less
   KV memory-time. Key diagnostic: most eviction loss comes from "derailed runs" that hit the
   length cap without answering - the same run-reliability-before-solvability gate the
   estate's fold law already carries (banked 2609.36526), now measured for KV bytes.

5. **Anosognosia in LLMs: Probing Self-Awareness of Quantized Computational Substrate** -
   arXiv:2610.06174 (Izawa, Minegishi, Yamakata; submitted 2026-10-05, read end to end;
   overlap: catalog snapshot state/arxiv/2026-10-06/2610.06174v1.txt, no mining hit). Models
   fail to self-report their quantization state from their own generated text; linear probing
   shows internal representations carry clear, method-specific fingerprints, but a shared LoRA
   trained across quantization levels fails on unseen methods (it maps method-specific
   fingerprints to labels, it does not generalize). RQ4's public half: a quantized model can
   never vouch for its own precision or provenance - MEASURED ON stamps must ride in the pack
   bytes (quantizer v0.6's design, lens/burns.md:138-141), because no runtime self-report will
   ever carry them.

6. **Capability Scaling-Down Laws for LLM Compression** - arXiv:2610.02462 (Cheng, Wu, Wan,
   Hong, Dong; submitted 2026-10-01, read end to end; overlap: catalog snapshot
   state/arxiv/2026-10-05/2610.02462v1.txt, no mining hit). Predictive laws for capability
   loss across pruning, quantization, and distillation as functions of size, training stage,
   compression settings, data availability; a compact density-response relation matches a
   full-measurement regression "to within 0.020 nats per token" on math and code across new
   Pythia states, pre-registered OLMo-2 test states, and Wanda pruning; sharing the density
   response across pruning levels halves the measurements needed. For the GPU-ladder purchase
   gates (memory/rib/RIB_GPU_LADDER_20261001.md) and the bit ladder: the field is moving from
   per-config A/B grids to fitted laws that predict the A/B - the estate's scoped A/B (owed,
   lens/burns.md:209) is the right size to seed such a fit, not a standalone datapoint.

7. **BARQ: Balanced Codebook Refinement for Low-Bit LLM Quantization** - arXiv:2610.04490
   (Cui et al.; submitted 2026-10-03, read end to end; overlap: ZERO hits in catalog and
   memory, genuinely new). Names the failure mode of codebook quantization at low bits -
   "imbalanced nearest-codeword assignments during fitting can leave some codewords
   insufficiently updated" - and fixes it with soft assignments via "entropically regularized
   optimal transport with uniform marginals" plus an assignment-weighted barycentric update,
   then hard encoding; lower perplexity and higher mean zero-shot accuracy than baselines at
   comparable bit budgets (no numbers on the abs page). RQ3/RQ5: the freshest evidence for
   the AQLM rule's direction (every new method is a constraint-specific fitting contract), and
   the concrete mechanics behind any quantized_thought-as-codebook bridge.

8. **KV Cache Quantization Benchmarks for Long Context** - anbeeld.com
   (https://anbeeld.com/articles/kv-cache-quantization-benchmarks-for-long-context, read end
   to end; no site date; subject qwen3.6 27b reached Ollama ~2026-10-01 per the 10-05 library
   pull, so necessarily in-window). Qwen 3.6 27B at 64k/128k, RTX 3090: q4_0 KV at 28.1
   percent of bf16 size leaves median PPL essentially untouched ("the entire PPL range is
   under 0.01") while the 99.9 percent KLD tail degrades 5.6x (0.130419 vs 0.023258) and
   99.9-percentile precision falls 100 to 89.84 percent; turbo2 at 13.3 percent size collapses
   the tail (0.903576 KLD, 41.47 percent precision); prefill speed is flat (~842-855 tok/s) at
   every level. Two structural findings: retrieval-style tests (passkey, needle at 32k, MMLU)
   all scored ~100 percent for every cache mode and were discarded as uninformative, and the
   same q8_0 KV did 4.5x more tail damage on IQ4_XS weights (0.017372) than on Q5_K_S weights
   (0.078709) - KV-quant damage is an interaction with the weight rung, not a constant.
   Overlap (corrected): the beellama.cpp fork the article runs on is banked (10-02 kv-cache
   HN sweep, README read end to end); these benchmark tables are new to the estate.

## Context rows (read, dated outside the 30-day window or unresolved; not items)

- Unsloth Dynamic 3.0 GGUF wave (TeksEdge share of the announcement, resolved via fxtwitter
  https://api.fxtwitter.com/TeksEdge/status/2090228570253861075, created 2026-08-20 00:05Z,
  1,828 likes): sizes UD-IQ1_S 6.2GB through UD-Q6_K 22GB for Qwen3.8-27B; "A 27B model
  entering 8GB-class hardware territory is crazy!"; links unsloth.ai/docs/basics/dynamic-3.0-ggufs
  and huggingface.co/unsloth/Qwen3.8-27B-GGUF. Refines the banked "1-bit collapses" shape
  (doors.md:40-42): with dynamic per-layer mixed quants, 1-bit at 27B retains ~77 percent
  accuracy per the announcement text surfaced in search (not re-verified on-page this sitting;
  marked accordingly). The rule amendment candidate for RQ1: collapse is a property of the
  quant METHOD at 1 bit, not of 1 bit itself.
- analogalok (fxtwitter 2090432439386874143, 2026-08-20): "I just quantized the Qwen 3.8 27B
  (dense) DFlash 2 drafter down to 2 bit." - a 2-bit speculative-decoding drafter holding
  acceptance; pairs with the same author's 2090400471458759145 A/B (Native MTP 66.85 t/s vs
  DFlash 2 77.44 t/s at 150k context). Quantized-drafter evidence for the fleet's cheap-rung
  shape; out of window, context only.
- mfranz_on (fxtwitter 2096225605142355983, 2026-09-05): generic llama.cpp praise
  (Q4_K_M/Q8_0 shrink 4-8x); one day out of window, no new measurement, listed for census.
- UNRESOLVED SNIPPET (recipe fallback): a WebSearch result attributed to the x.com/Anbeeld
  profile the phrases "even the q4_0 result is not far behind bf16" and "Long-context
  retrieval actually went up 2.3pp". The fxtwitter user endpoint returned profile only (no
  timeline), so no status id or body could be verified; the author's own long-context article
  fetched this sitting contains NEITHER phrase (its retrieval tests all hit ~100 percent and
  were discarded, and no 2.3pp figure appears). The snippet is banked here with its URL
  (https://x.com/Anbeeld) as UNVERIFIED and is contradicted-on-site; do not cite either claim
  as truth.
- NVIDIA DGX Spark forum, user nmaine, 2026-03-31
  (https://forums.developer.nvidia.com/t/kv-cache-quantization-benchmarks-on-dgx-spark-q4-0-vs-q8-0-vs-f16-llama-cpp-nemotron-30b-128k-context/365138,
  read end to end): Nemotron-3-Nano-30B-A3B at 8k-64k context; q4_0 KV prompt processing
  collapses 92.5 percent at ~64k (282.7 to 21.3 tok/s, dequantization overhead) and RSS runs
  6-7 percent ABOVE f16 at every length ("scale/zero-point metadata overhead exceeds
  compression savings"); "q8_0 is the only quantization worth running - 2x compression, <5%
  speed hit at all context lengths." Out of window and single-hardware, but it is the sharpest
  published inversion of the "lower KV bits are faster" assumption and matches B4's banked
  q8_0-first result (lens/burns.md:59).
- StagQ (arXiv:2610.05977, submitted 2026-10-05, abs read end to end; overlap: catalog
  snapshot state/arxiv/2026-10-05/2610.05977v1.txt, no mining hit): a multi-precision weight
  stream, 2-bit group-wise affine base plus 1-bit refinement planes where "every supported
  precision is a readable prefix"; at two bits it leads the strongest multi-precision baseline
  on Llama-3.1-8B, Phi-4, and OLMo-2-7B by 3.1 to 7.0 MMLU points at a slightly lower logical
  rate. It misses the top-8 only because BARQ and the two anbeeld reads answer named estate
  questions more directly; it is the one-stream-whole-fleet shape for the GPU-ladder gates.
- KVarN (Huawei, arXiv 2606.03458) is already registered in the estate
  (memory/runs/ds_batches/gapfold_items.jsonl names the register append; the id sits in the
  prior-sweep fence), so the anbeeld.com KVarN article
  (/articles/kv-cache-quantization-benchmarks-kvarn-precision-tail, read end to end) banks as
  context: on Qwen 3.6 27B KVarN beats same-width standard quants by 2.6 to 12.6 percent KLD,
  kvarn5 lands within 0.000014 of q6_0 using 232 MiB less, but on Gemma 4 31B only 6 of 29
  Pareto rows are KVarN (vs 23 of 28 on Qwen) and a 1024-token exact tail costs 243-693 MiB on
  Gemma vs a flat 96 MiB on Qwen - even KV quant methods are model-tier-specific, the AQLM
  rule again.

## Answers to the five research questions (public evidence only; estate-side runs NOT executed this sitting)

- **RQ1 (owed qwen2.5:7b A/B + 2b-class ladder):** NOT RUN - the A/B is a local runtime job
  (ollama qwen2.5:7b Q4_K_M vs q8_0) and this sweep ran no local models; it stays OWED per
  lens/burns.md:209. What the public corpus now gives it: 2610.04403's audit predicts the
  7B rung is lexically clean at Q4_K_M (Q4_K_M clean at 1B+), predicts sub-2B collapse is
  definitional/rare-word and frequency-graded (20-67 percent definition loss at sub-2B Q2)
  and INVISIBLE to perplexity, so the scut battery needs definitional probes, not PPL, and
  per-artifact validation. The banked "4-bit holds, 1-bit collapses" shape (doors.md:40-42)
  replicates directionally at 27B (unsloth dynamic 1-bit 77 percent, out-of-window context
  row) and collapses harder at 2B (2610.04403) - parameter count (rho=0.72), not the ladder
  position, is the axis.
- **RQ2 (q4_0 KV accuracy + throughput at 2b context):** accuracy cost measured at 27B, not
  2B: q4_0 KV costs almost nothing in median PPL (5.4877 vs 5.4800) and 5.6x in the 99.9
  percent KLD tail (anbeeld long-context), and it does 4.5x more tail damage when weights sit
  one rung lower (IQ4_XS vs Q5_K_S) - so on a 2b model the q4_0 KV tail cost is expected
  WORSE than the 27B numbers, unmeasured. Throughput: q8_0-first survives everywhere read
  (B4 banked 100.8 vs 55.9 t/s; nmaine <5 percent hit at all lengths; anbeeld prefill flat
  q8_0 through q4_0), but the q4_0 win does NOT generalize - it inverted 92.5 percent at 64k
  on DGX Spark. At 2b context lengths specifically, nothing read measures KV-quant speed;
  that cell stays unmeasured. The 1-bit rung exists as a recipe (TaSQ, 14x batch / 1.87x
  throughput vs BF16) and as an allocation law (BreadthKV: buy breadth, not bits).
- **RQ3 (AQLM method-tier rule across GGUF lanes):** the rule holds and every post-09-06 read
  pushes it FURTHER toward specificity: QAT-vs-non-QAT is a 20.3x factor at the same nominal
  q8_0 KV on the estate's own janitor family (anbeeld Gemma 4 31B); the same KV quant changes
  damage 4.5x across weight rungs (anbeeld long-context); KVarN is Pareto-dominant on Qwen
  and near-irrelevant on Gemma (23/28 vs 6/29 Pareto rows); TaSQ tailors VQ space to the
  1-bit KV regime; BARQ balances codebook fitting; StagQ builds the multi-precision prefix
  stream; BreadthKV picks bit-widths by end-to-end calibration per workload. Rule amendment
  candidate: "a quant method is tier-specific AND weight-rung-interactive; checkpoint
  provenance (QAT or not) is part of the tier." Nothing read supports any universal method.
- **RQ4 (run-quantization propagation / truncation growth):** estate-side experiment NOT run
  (needs quantizer v0.6 pipeline access; this seat ran no pack compiles). Public evidence
  banks one load-bearing fact: 2610.06174 shows generated text carries almost no trace of
  quantization state, so no downstream reader - human or model - can recover provenance from
  pack output; MEASURED ON rows must be carried structurally (bytes, ids), which is exactly
  the v0.6 amendment (lens/burns.md:138-141). Truncation-vs-pack-size growth (13/338,
  lens/burns.md:90): no public measurement read this cycle; the estate instrument remains the
  only source; nothing found contradicts treating it as monotone in pack size until measured.
- **RQ5 (HyperThink VQ codebooks as law-packs in weight space):** the analogy is now
  falsifiable with public mechanics, though the experiment itself was NOT run here. TaSQ
  merges activation-statistics transforms into "projection weights and codebooks" (weight-side
  and lookup-side co-design), BARQ fits codebooks by balanced optimal transport, HyperThink
  (banked, lens/burns.md:131) predicts query-conditioned parameter updates. The measurable
  bridge on a 2b model: treat a quantized_thought law pack as a codebook, fit it with BARQ-
  style balanced assignment over law rows, and measure assignment distortion against task
  outcomes - if law rows have codebook structure (clusterable centroids with balanced mass),
  the analogy lives; if assignments collapse onto a few centroids, it is a metaphor. A shared
  LoRA probing internal fingerprints failed to transfer across methods (2610.06174), a
  caution: the bridge, if real, is method-local.

## Method receipt (instruments run this sitting)

- WebSearch volleys (X door): 8 queries across Q4_K_M/q8_0, KV q4_0, 1-bit collapse, AQLM,
  VQ codebooks, BitNet, danielhanchen Div-300, Anbeeld; repeated MCP -429 / 1302 rate limits;
  successes and their URLs attributed above.
- WebFetch reads to completion (11 pages): api.fxtwitter.com x4 (analogalok x2, TeksEdge,
  mfranz_on), api.fxtwitter.com/Anbeeld profile probe, arxiv.org/abs x6 (2610.05685,
  2610.03027, 2610.04403, 2610.02462, 2610.04490, 2610.06174, 2610.05977), anbeeld.com x5
  (home, /articles, long-context article, kvarn-precision-tail article, gemma-4-31b QAT
  article), forums.developer.nvidia.com DGX Spark thread, export.arxiv.org Atom x2 (KV-cache
  query 15 entries; cs.LG quantization query 30 entries).
- Overlap instruments: grep over catalog/catalog.jsonl and memory/ plus the five prior
  frontier_olm sweep dirs for 2610.04403 / 2610.03027 / 2610.05685 / 2610.02462 / 2610.04490 /
  2610.06174 / 2610.05977 / 2610.03039 / "TaSQ" / "BreadthKV" / "BARQ" / "StagQ" /
  "Anosognosia" / "KVarN" / "Anbeeld" / "Saying, Not Knowing" / "Scaling-Down Laws"; results
  stated per item above; catalog counts per id run individually (2610.04403: 0,
  2610.03027: 1 snapshot, 2610.05685: 1 snapshot, 2610.02462: 1 snapshot, 2610.04490: 0,
  2610.06174: 1 snapshot, 2610.05977: 1 snapshot, 2610.03039: 1 banked card).
- Local model runs: NONE. pytest: not run (no code changed). This file is a sweep record, not
  a code landing.
