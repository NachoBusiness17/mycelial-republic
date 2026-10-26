# SWEEP: quantization-and-compression-x (frontier olm 2026-10-03, second pass)

source-fetched: 2026-10-03
Area: quantization-and-compression via x. Seat: sweep gopher. Window: 2026-09-03..2026-10-03.
This file REPLACES an earlier same-seat pass that answered a different research-question set;
that pass is preserved verbatim at `quantization-and-compression-x.pass0.md` in this
directory (the 20260928 fold lost its first pass to an overwrite with no copy; that failure
is not repeated here). Two passes per the ask: pass 1 broad sweep, 38 in-window candidates
considered (pool enumerated below); pass 2 deep read, 9 items fetched and read this session
(6 papers/pages, 3 X posts through the fxtwitter door). Banked items are only pages I
fetched myself this sitting.

## Door condition (honest record)

- fxtwitter door (https://api.fxtwitter.com/<user>/status/<id>): WORKED for status
  resolution, but X DISCOVERY failed first. Three `site:x.com` WebSearch queries returned no
  direct post URLs (search engines truncate x.com links to bare https://x.com with no status
  id, the same defect pass0 recorded); an "x.com/status" URL hunt returned nothing;
  syndication.twitter.com returned an empty JS shell. With no status ids of my own, I
  reused the ids pass0 harvested from AINews/latent.space aggregator pages and resolved
  three of them myself through fxtwitter (banked items 7-8 plus the stochasticchasm post).
  Aggregator-sourced Reddit-style numbers stay attributed to the aggregators, not read
  firsthand.
- `https://unsloth.ai/blog/dynamicv3`: HTTP 403 on WebFetch; web-reader MCP returned a 500
  network error on retry. Unsloth Dynamic v3's own blog is UNVERIFIED; the recipe IS
  independently attested inside 2609.04098, which I did fetch (see item 3). No fallback
  success claimed.
- The web search backend 1302-rate-limited 4 of about 13 queries (transient; worked around
  at lower width).
- Fetcher depth note: arxiv.org/abs pages returned abstracts only for two papers; full text
  was pulled via arxiv.org/html/<id>v1 where available. Depth per item is labeled.

## Citation drift found in the ask (flagged, not papered over)

- The ask cites "burns.md:103-106" for the 2-bit +25 pct output-token inflation and
  "burns.md:122" for the owed qwen2.5:7b Q4_K_M-vs-q8_0 A/B. No burns.md in the repo carries
  those claims at those lines (checked all four: 20260928 is 67 lines, 10-01 is 80, 09-30 is
  126 with line 122 = secret_gate_results, 10-02 is 173 with 103-106 = janitor verdict and
  122 = salon_mine). The +25 pct claim's actual estate home is
  `watch/inbox/frontier_olm_2026-10-02/sweep/quantization-compression-hn.md:8`. The claim is
  real and is re-verified at source this sitting (item 4).
- The estate map names "auto_quantize's quantization law in
  memory/percolator/invariants.json". Grep for `quant` in that file hits only the word
  "quantity" inside an unrelated co-termination controller (invariants.json:1997); there is
  no model-weight quantization law in the invariants file. `mag/auto_quantize.py:22` holds
  "LAW: Anomalies are NEVER quantized. Keep raw forever." - ANALYTICS-event quantization, a
  naming collision, already flagged "ANALOGY-ONLY bank" at
  `watch/inbox/frontier_olm_2026-10-02/DIGEST.md:29`. No invariant was changed by this sweep.

## Overlap receipts (grep commands run this sitting)

- 2609.14864: `grep -c "2609.14864" catalog/catalog.jsonl` = 0; ARXIV_REGISTER.json = 0; the
  three memory/trajectory/steps.jsonl hits are step_hash substrings (false positives). NEW.
- 2609.04098: `grep -c "2609.04098" catalog/catalog.jsonl` = 1: the 2,106-byte abstract stub
  `state/arxiv/2026-09-06/2609.04098v1.txt` (catalog id 19b9109a137c). Held abstract-only;
  full-text read is this sitting's new depth.
- 2609.04748: catalog title hit = 1 (the 1,812-byte abstract stub
  `state/arxiv/2026-09-07/2609.04748v1.txt`, id d7ae...); ARXIV_REGISTER row verdict REAL,
  cited_in `watch\inbox\frontier_olm_20260928\sweep\quantization-compression-arxiv.md`, plus
  MAP_BACKFILL.json/.md hits. Held abstract-only; its quant-ladder numbers are new to the
  estate this sitting.
- 2609.14060: ARXIV_REGISTER = 1 hit; catalog = 0. Registered, never read.
- 2608.06564: catalog = 0, register = 0, memory = 0. NEW.
- Quesma article: held four ways (dup register,
  `frontier_olm_2026-10-02/sweep/quantization-compression-hn.md:29`); banked here only as
  source re-verification with new verbatim quotes.
- DeepSeek V4.1 Flash 890 B/token: HELD at
  `frontier_olm_2026-10-02/sweep/quantization-compression-hn.md:21` (pass0's overlap ledger
  missed this because its grep pattern was "890 bytes", the held file writes "890 B/token").
  The nrehiew_ X primaries themselves are NOT held; banked as X-door primaries with the
  figure's overlap stated.

## Research-question verdicts

**RQ1 (Q4_K_M-matches-BF16 on agentic work; the owed qwen2.5:7b Q4_K_M-vs-q8_0 A/B):**
NOT RUN, still owed. This session executed no local A/B, and greps found no evidence it was
ever run (`memory/tool_quant/quant_ledger.json`: zero hits for qwen2.5/Q4_K_M/q8_0; no A/B
row in either 10-02 quantization sweep). What the window adds: at 27B, Quesma re-verified
verbatim - Q4_K_M matched BF16-replicated numbers on Terminal-Bench 2.1 (89 agentic tasks,
3h timeout), GPQA within noise, IFBench identical through 2-bit - and Q8_0 was SKIPPED on
Terminal-Bench ("safely interpolated" between BF16 and Q4_K_M arms), so even the flagship
never measured the Q4-vs-Q8 step the estate's A/B asks about at 7B. New design constraint
the A/B must absorb before firing: 2609.04748 (item 2) shows on qwen2.5-7b exactly that a
cache-enabled llama.cpp/vLLM endpoint flips agentic trajectories by quant level AND cache
state (single llama.cpp flag moved cross-arm divergence 38.8 pct to 1.2 pct), so an A/B
through a shared endpoint without pinning/resetting cache state measures serving history,
not the quant. Recipe: same ask set, q8_0 vs Q4_K_M arms, fresh server or prompt-cache flag
pinned per arm, per-arm classify_empty counts logged. The 10-02 UD-Q2_K_XL cell can ride the
same harness.

**RQ2 (post-10-02 agentic-retention papers; contradiction of 2-bit +25 pct output-token
inflation?):** No contradiction found; every in-window task-metric result points the same
direction, and the +25 pct finding re-verified verbatim at source (item 4). In-window
agentic-retention results: 2609.04748 (BFCL 80-episode trajectories across
F16/Q8_0/Q4_K_M/Q3_K_M on qwen2.5-7b/14B and llama-3.1-8b: divergence ladder, but "no
aggregate accuracy shift", flips in both directions); 2609.14060 (post-quant benign utility
ratios cluster at 1.00 across NF4/FP4/INT8 - quantization preserves capability, which is
why the backdoor transfers); 2608.06564v4 (16 models, 8 families, 400 BFCL tasks: at 3-bit
RTN "3 of 5 models lose more completed calls than correct tool selections", while GPTQ and
GGUF flip far fewer whether-to-call decisions than RTN - "no single 3-bit failure point";
the 3-bit floor is quantizer-dependent, a sharpening not an overturn). Held PolAgentBench
(2609.32042) already covers the Q8..Q2 cliff; not re-banked. Unsloth Dynamic v3 remains
unverified from its blog (403) - the 10-02 nuance stands: Q2_K-never has never been tested
against UD-Q2_K_XL-class dynamic mixes. One measured cell, still owed.

**RQ3 (GGUF metadata alone as a routing-grid serving column):** YES for a per-host decode
column, with named break points (item 1, full text). Predictor uses only pre-inference GGUF
metadata: file size S; total/active params P/P_a derived from tensor shapes and
expert-routing fields; per-layer KV metadata (h_i, d_i, sliding window w_i, recurrent-state
term); quant format q. Decode: T_hat = eta_{h,q} * B_h / D(c), eta a per-host per-quant
MEDIAN scale factor, B_h measured host bandwidth. Where it breaks: cross-host transfer is
incomplete (leave-one-host-out 11.6/16.8/36.0 pct MAPE, the RTX 36 pct arm the break); MoE
dense test errors 3.28-20.4 pct vs MoE 19.7-51.9 pct (Ling-mini 68.96 pct worst); prefill
"unsupported under this protocol" (P2 baseline 108.2 pct on RTX); quant format does not fix
kernel efficiency (low-bit ladder ordering flips by host: Q2 about 2.2 pct faster than IQ2
on Apple, IQ2 13.7 pct faster on RTX - "file compression alone therefore does not specify
kernel efficiency"); configuration-level decode ratios span 1.76-3.26x, "ruling out one
universal multiplier"; RTX cohort is 2 held-out configs and Windows shared-memory spill
"cannot be excluded". Grid recipe: metadata seeds the column, each host class fits its own
eta/phi and calibrates B_h; never ship one cross-host constant; leave the prefill cell blank.

**RQ4 (NVFP4/W4A4 Minima vs GGUF K-quants for linear-attention architectures):** The paper
(item 3, full text) contains NO integer-4-bit baseline - no INT4, AWQ, GPTQ, or GGUF arm -
so NVFP4-vs-K-quant is UNMEASURED in this window. What it establishes: Minima puts NVFP4
W4A4 on all 496 linear layers of Qwen3.8-27B (48 GatedDeltaNet + 16 attention), matches BF16
within seed noise (5-task avg -0.52; AIME25 86.7 both arms; RULER 100 both), 17.53 GiB vs
BF16 50.13 GiB, and needs native NVFP4 tensor cores (vLLM 0.27.1 on RTX PRO 6000, SM120) -
a different kernel world from llama.cpp integer quants, not servable by the estate's local
tier today. Transferable finding: the recurrent half is the EASY half (gate projections
compress about 11 pct GEMM error to about 2 pct output error via softplus/exp and sigmoid;
the delta-rule recurrence holds noise at a flat plateau and overwrites state along the
current key direction; the 32K perplexity gap shrinks with position), and both community
checkpoints it compares (Unsloth Dynamic v3 20.23 GiB, RadixArk 18.83 GiB) still shield
GDN+attention at FP8 with gates in BF16 - the field is protecting the half this paper shows
needs no protection. Boundary: the gate-shielding argument "is parameterization-dependent"
(log-space softplus/exponential decay), and GGUF tooling coverage for GDN hybrids was not
verified this session. K-quants on a future local GDN hybrid are low-risk BY MECHANISM,
unproven BY MEASUREMENT.

**RQ5 (quantization level x EMPTY_REASONING):** No in-window paper measures
hidden-reasoning-empty-content rates by quant level; the interaction is mechanistically
supported, not measured. Fetched-evidence chain: at 2-bit the model writes about a quarter
more tokens at the same turn count (item 4); 1-bit models lose to "running out of token
budget" as reasoning lengthens (item 4, GPQA section); PTQ inflates overthinking, and
token-specific penalties recover up to 9.8 points while cutting CoT length up to 51.3 pct
(RATIO 2609.39801, held abstract-depth 10-02); the estate's EMPTY_REASONING class is exactly
finish=length with an empty content channel and burned reasoning tokens
(`memory/rib/RIB_INFERENCE_BUDGET_20261001.md:54-58`). Lower bits plausibly raise the
finish=length rate and therefore EMPTY_REASONING incidence on budget-capped asks - but that
is cross-source inference, not a measurement, and none exists here or in the window. The
janitor-fleet probe is cheap and now fully specified: same ask sample through qwen2.5:7b at
q8_0 / Q4_K_M / Q3_K_M, count classify_empty outcomes per arm, cache state pinned
(2609.04748's control). OWED, not run.
Security rider the routing grid should hold (item 5): quantization-conditioned backdoors
reach up to 100 pct post-quant attack success with clean FP16 audits and failed weight-space
statistics; GPTQ's Hessian error-feedback breaks the attack (ASR 0.00) while AWQ transfers
(0.87); GGUF UNTESTED by the paper; the detection surface is behavioral cross-precision
comparison - the same instrument shape as Broken-on-Arrival's quantcheck, banked 10-02
(`frontier_olm_2026-10-02/sweep/quantization-compression-arxiv.md:26`), which model-garden
ingest could extend with a cross-precision behavioral diff before a quantized artifact
enters the routing grid.

## Banked items (8, strongest first)

1. Same Request, Different Answer: Quantization Amplifies Cache-Induced Divergence in LLM
   Serving (2609.04748, 2026-09-04) - full text. Changes how the owed A/B must be run.
2. GGUF-Metadata Prediction of Single-Sequence llama.cpp Throughput Across Three Systems
   (2609.14864, 2026-09-14) - full text. NEW. The routing-grid serving column math.
3. Benchmarking Qwen3.8 27B quantizations (Quesma, 2026-09-08) - full article. Held item
   re-verified at source; new verbatim quotes.
4. Why Gated DeltaNet Survives 4-Bit Quantization (2609.04098, 2026-09-06) - full text over
   the held 2 KB stub.
5. AGENTQ: Quantization-Conditioned Backdoor Attacks on LLM Agents (2609.14060,
   2026-09-12) - full text. Registered-but-unread.
6. Which Decisions Low-Bit Quantization Breaks, and How to Predict Them (2608.06564,
   2026-08-06, v4 2026-09-28) - ABSTRACT-DEPTH only; in-window via the v4 update.
7. stochasticchasm X post 2098154481750020375 (2026-09-10) - fxtwitter, fetched this
   sitting; id harvested by the preserved pass0.
8. nrehiew_ X post 2098170450526543892 (2026-09-10) - fxtwitter, fetched this sitting;
   figure overlap with the held 10-02 HN item stated.

## Pass-1 candidate pool (38, last 30 days unless marked)

arXiv API (query "quantization+agent", 30 returned; query "GGUF", 20 returned):
2610.00613 09-30 VQ geodesics agent tools; 2609.34064 09-28 perturbation-robust agent
policies; 2609.32042 09-25 PolAgentBench (HELD); 2609.23130 09-19 vLLM/llm-d inference
control plane; 2609.22870 09-19 full-pipeline FP8 RL; 2609.17786 09-15 FairCompressAgent;
2609.17652v3 09-15 Fathom (HELD); 2609.14976 09-14 MemRiskBench; 2609.14060 09-12 AGENTQ
(BANKED); 2609.11133 09-10 power control disaggregated serving; 2609.04748 09-04 cache
divergence (BANKED); 2609.02264 09-02 Codebook Agent; 2609.00442 08-31 DRLM edge; 2608.27513
08-27 DAMP recurrent-state quant (OUT by 7d); 2608.24215 08-23 Agentopia 8B (OUT);
2608.22472 08-23 small reasoning models function calling (OUT); 2609.14864 09-14 GGUF
metadata throughput (BANKED); 2609.18526 09-16 local-privacy serving failures (HELD);
2609.00665 09-01 SLM vs quantized sustainability (OUT by 2d); 2608.06564 v4 09-28 decision
breaks (BANKED); 2609.25014 08-02 4-bit PII leakage (OUT); 2609.37916 09-29 RLX compiler;
2609.30692 09-25 LUMO; 2609.24177 09-21 legal distillation; 2608.15693 08-16 edge survey
(OUT); 2607.10137v3 RDQ updated 09-10; 2607.14181 07-15 code-gen quant (OUT).
Web/X search: Unsloth Dynamic 3.0 GGUFs (unsloth.ai 09-23 snippet; blog 403, UNVERIFIED, not
banked); NVIDIA Nemotron 3 Ultra 550B NVFP4 X post (no status id, UNRESOLVED, not banked);
Step-3.5-Flash-Int4 (74.4 SWE-bench Verified / 51.0 Terminal-Bench 2.0 INT4, ModelScope, date
unconfirmed, not banked); NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4 (undated, not banked); "LLM
quantization without myths" (slash-digital.io 2026-09, not read); Hardware-Aware FP4
FlashAttention-4 (dair.ai 09-03 listing, not read); BOS-Sink Topology 4-bit weight-only
(alphaXiv, undated, not read); Nemotron 3 Ultra on Ollama cloud (daily.dev 08-23, OUT);
"Quantization Hurts Reasoning?" (arXiv 2025-08, OUT, foundational for the RQ5 direction);
Google TurboQuant (2026-03, OUT). pass0's pool (llamAmpere, TAK, Voodoo, MLX mixed, MXFP4
radiance, smol issues) is preserved with its file and not duplicated here.
