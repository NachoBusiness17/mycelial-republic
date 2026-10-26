# SWEEP: quantization-and-compression-x (frontier_olm_2026-10-04)

source-fetched: 2026-10-04. Area: quantization-and-compression via x. Seat: sweep gopher.
House laws held: ascii only, no em or en dashes, every claim cites a page fetched or a command
run this sitting. Bank file for the x-door lane; the sibling arXiv lane's bank is
`quantization-and-compression-arxiv.md` in this same directory and is treated as prior art
here, not duplicated.

## Method (what actually ran)

- Pass 1 (broad sweep): nine WebSearch queries on the x door plus companions (site:x.com GGUF
  quantization reasoning; site:x.com EXL3 EXL2; site:x.com KV cache quantization Q8; HN KV
  quantization outsized impact; arxiv quantization reasoning 2026; Unsloth dynamic quants
  x.com; arxiv KV cache quantization chain-of-thought; compression progress intrinsic reward
  2026; two URL-pinning follow-ups). 31 in-window or near-window candidates surfaced and were
  considered; the pool is enumerated at the bottom. X discovery stayed degraded exactly as the
  10-03 lane recorded (search engines truncate x.com to bare domains; the backend 1302'd
  twice); the fxtwitter resolution door WORKED (one article resolved end to end, item 4).
- Pass 2 (deep read): FIVE pages fetched and read end to end this sitting: arxiv.org/abs/
  2605.14831, arxiv.org/abs/2604.18701, arxiv.org/abs/2504.04823,
  lmsys.org/blog/2026-09-16-nvfp4-kv-cache, and the Mayhem4Markets EXL3 long-form article
  through api.fxtwitter.com (JSON, full article key points returned). Three further items
  stayed snippet-only because their doors degraded (unsloth.ai 403 + web_reader 500;
  openreview.net Cloudflare interstitial; energyflowx.com client-rendered shell on BOTH the
  WebFetch and web_reader doors); they are banked below as snippets with that said, per the
  recipe fallback. No fallback success is claimed for any of the three.
- Overlap instruments (run this sitting, from repo root): multi-pattern grep -F -f over
  catalog/catalog.jsonl (1,040,765 rows per lens/corpus.md:7), memory/, and the banked
  watch/inbox surfaces (*.md + *.jsonl, _raw excluded), patterns: 2605.14831, 2604.18701,
  Curiosity-Critic, "Interestingness as an Inductive", "Dynamic 3.0", "NVFP4 KV",
  nvfp4-kv-cache, uCOMb0EsPq, Mayhem4Markets, 2082487427138994230; plus targeted greps for
  2504.04823 and per-pattern attribution. The memory/trajectory/steps.jsonl hits for the two
  new arXiv ids are THIS SESSION's own command trace (file mtime 2026-10-04 12:21 local, hit
  content = my own grep strings), not prior estate knowledge.

## Answers to the five research questions

**RQ1 (published quant-versus-reasoning rungs; contradictions with banked rungs).** The
flagship systematic ladder, "Quantization Hurts Reasoning?" (arXiv 2504.04823, COLM 2025,
read end to end this sitting), is ALREADY ESTATE-HELD: watch/inbox/kv50_findings.json
(2026-09-25) carries it verbatim ("lossless quantization can be achieved with W8A8 or W4A16
quantization, lower bit-widths introduce significant accuracy risks") and the 10-03 x lane
sighted it OUT as foundational. My read adds one nuance the held quote omits: on CoT length,
the abstract says quantized models "do not exhibit increased output lengths", which sits
AGAINST the banked ternary-PQ2 token-inflation datum (reddit 1wkorli, 3.10x tokens) ONLY
superficially: ternary PQ2 is a different quant class than 4/8-bit PTQ, so no banked rung is
contradicted, but the ladder probe should not assume token inflation generalizes from ternary
to k-quant arms. The untested rung the estate keeps owing (Q2_K-never vs UD-Q2_K_XL-class
dynamic mixes) is still unmeasured in everything I read; Unsloth Dynamic 3.0's own blog, the
one source that would carry it, failed a THIRD door attempt this sitting (403 WebFetch, 500
web_reader; same failure the 10-03 lane logged). No item I read contradicts a banked rung.

**RQ2 (KV-cache quantization levels vs reasoning; the stacking bound).** Public measurements
now triangulate the KV ladder cleanly. 8-bit KV: the energyflowx Qwen3-Coder-30B measurement
(SNIPPET ONLY, page is a client-rendered shell on both doors) reads "8-bit KV cache
quantization (Q8_0) scores slightly higher than FP16 baseline across both LongBench-v2 and
BigCodeBench metrics"; one counter-anecdote (latent.space AINews, q8 KV "worse or more
inaccurate" than bf16, reverted) could not be resolved to a primary page and stays anecdote
weight. 4-bit KV: the lmsys NVFP4 KV cache post (read end to end) quantifies the first
measured reasoning deltas vs FP8 KV: on Qwen3.8-27B, "NVFP4 scored 0.31 percentage points
lower than FP8 on GSM8K and 1.01 points lower on GPQA-Diamond", SWE-bench Verified 76.20 vs
77.80 (a 1.60 point gap), AIME 2025 matched at 98.33; the same post warns "two models and a
small set of tasks do not establish a general relationship between model size and
quantization tolerance". So the bound for stacking: weight quant plus KV q8_0 is supported at
zero-to-positive reasoning cost; weight quant plus 4-bit KV costs on the order of 0.3 to 1.6
points on reasoning-and-code tasks even when implemented by the vendor that invented the
format; below 4-bit KV the only reasoning-grade results ride custom transforms on serving
stacks the estate does not run (sibling arXiv bank, items 3 and the SoK row). The ladder can
stack, but the KV leg has a floor at q8_0 free / 4-bit about-one-point / nothing-naive-below.

**RQ3 (2026 compression-as-progress and intrinsic-reward lineage vs the amended percolator
candidate).** The lineage is ALIVE and it EXTENDS the amended candidate twice without
touching the amendment. (1) "Interestingness as an Inductive Heuristic for Future Compression
Progress" (arXiv 2605.14831, 2026-05-14, Vincent Herrmann and JUERGEN SCHMIDHUBER, read end
to end): the direct successor inside the dropped 0812.4360 lineage, co-authored by
Schmidhuber himself, and it proves "expected future progress depends exponentially on the
recency of the last observed breakthrough". For the percolator selector-port (bytes-to-verbs
steepness over 5 waves) that is a concrete upgrade: the curiosity ranking should be
recency-weighted, because the theory's own predictability result says recent steepness
carries the signal, not cumulative or stale steepness. (2) "Curiosity-Critic" (arXiv
2604.18701, 2026-04-20, v3 2026-06-16, EIML@ICML 2026 workshop, read end to end): grounds
intrinsic reward in improvement of CUMULATIVE prediction error with an online-estimated
asymptotic baseline, so "the reward is higher for learnable transitions and collapses toward
zero for stochastic ones, thereby separating epistemic (reducible) from aleatoric
(irreducible) prediction error online". Port shape for the candidate: normalize each lane's
bytes-to-verbs steepness against that lane's own baseline steepness so noisy or repetitive
lanes collapse toward zero instead of dominating the queue. Combined with the sibling lane's
sealed-audit theorem (2606.11417) and learnable-novelty estimator (2607.18433), the amended
candidate's kill-falsifier survives but gains three design constraints before wave one:
sealed frozen panel (sibling), recency weighting (this bank), per-lane baseline subtraction
(this bank). Nothing fetched falsifies the amended metric (carried-history retired + verbs
minted primary).

**RQ4 (format and bit-width for the janitor fleet on the operator's actual hardware;
stability across families).** Hardware envelope read this sitting from configs/lanes.yaml:57-64:
AMD Radeon RX 5600 XT, about 6 GB VRAM, 64 GB RAM, cuda: false, Ollama context 8192,
max_loaded 1; fleet task mix gemma:2b scut/routing, qwen-desk desk roles, qwen2.5-coder:7b
worker (lanes.yaml:31-40). On that envelope the X door produced a DECISIVE exclusion: the
EXL3 article (resolved end to end through fxtwitter) lists as drawbacks "NVIDIA-only (no
AMD/CPU support), served mainly via TabbyAPI", and its throughput claims run on RTX hardware;
EXL2/EXL3 is off the table for this GPU no matter how good the 3 bpw quality bump is. AWQ and
GPTQ kernels and the lmsys NVFP4 path (Blackwell SM12x/SM100/SM103 only, "experimental" in
SGLang) are likewise unreachable. The ranking that survives for the janitor fleet is the
banked one and it gains confirmation this window: GGUF k-quants in Ollama, Q4_K_M as working
default with Q3_K_M as the agentic edge (banked Quesma + 2609.32042 rungs), KV left at the
serving config the estate already runs (q8_0 KV, mag/vast_launcher.py:444 and :457), which
the energyflowx snippet and the lmsys FP8-KV baseline both say is the safe KV rung. Family
stability: the sibling's 2607.14181 (two families) plus OBC-Prune (Sep 2026, snippet-level:
"relative ranking generally persists across model families" on Qwen3 and R1-Distill-Llama-8B)
say the ranking is stable where it has been measured; EXL3's own 3 bpw bump shows the ranking
would NOT survive a backend swap, which the estate cannot make on this GPU anyway.

**RQ5 (seed rows for a quantization shelf).** The corpus lens (lens/corpus.md:26) is right
that no shelf exists. Combining this bank with the sibling arXiv bank, the shelf's first rows
are already enumerable: spine = 2609.30854 SoK (banked 10-02, register row 6); measurement
design = 2504.04823 (held, kv50_findings.json) + 2609.06473 (sibling); rungs below 4 bits =
2609.26708 (sibling) + 2609.32042 (held); KV ladder = SoK row + lmsys NVFP4 KV (this bank) +
NIGHT_EXTERNAL_MEMORY_20260911.md:22's vendor-stack row (NVIDIA NVFP4 KV, AMD TurboQuant
4-bit ROCm, OpenVINO INT4, ThinKV precision-by-thought-importance); method dimension =
2607.14181 (sibling) + the EXL3 article (this bank) as the community-format column;
community-dynamic-quant column = Unsloth Dynamic 3.0, STILL unverified at the source after
three window attempts (unsloth.ai 403 + 500 this sitting; only secondhand attestations exist:
OSCHINA report of about +10 pct same-size accuracy vs v2.0 with best KL divergence, debuting
on Qwen3.8-27B, and the buttondown AINews 1.78-bit vs 2.71-bit recommendation summary, both
aggregator-attributed, not banked as fact); RL/post-training co-shelf = 2604.18701 +
2605.14831 (this bank) + 2606.11417 + 2607.18433 (sibling) + the 2609.22870 lead (sibling,
unfetched).

## Banked finds (6, strongest first)

### Find 1: Schmidhuber's own successor proves interestingness is predictable from recency (2605.14831, 2026-05-14)

Quote (arxiv.org/abs/2605.14831, fetched this sitting): "We prove that expected future
progress depends exponentially on the recency of the last observed breakthrough."

Why it matters: the dropped 0812.4360/SICE lineage has a 2026 continuation co-authored by
Schmidhuber (Herrmann and Schmidhuber), and its theorem is a direct design input to the
amended curiosity-scored lane-selection candidate in memory/percolator/candidates.jsonl: the
bytes-to-verbs steepness ranking should weight recent waves, and the 5-wave kill window is
theoretically the right shape only if recency dominates. Formalizes interestingness via
Kolmogorov complexity and algorithmic statistics under Length, Algorithmic, and Speed priors.

Overlap: grep -F over catalog/memory/watch banked surfaces this sitting: ZERO hits outside
memory/trajectory/steps.jsonl, which is this session's own command trace (mtime 2026-10-04
12:21, hit strings are my own grep arguments). The sibling arXiv lane banked 2606.11417 and
2607.18433, not this id. Genuinely new.

### Find 2: Curiosity-Critic: baseline-subtracted cumulative progress is the tractable intrinsic reward (2604.18701, 2026-04-20, v3 2026-06-16)

Quote (arxiv.org/abs/2604.18701, fetched this sitting): "The reward is higher for learnable
transitions and collapses toward zero for stochastic ones, thereby separating epistemic
(reducible) from aleatoric (irreducible) prediction error online."

Why it matters: second living leg of the lineage. It shows prior prediction-error curiosity
"from Schmidhuber (1991) to learned-feature-space variants" are special cases of one baseline
approximation, and gives the percolator candidate its missing normalization: subtract each
lane's own asymptotic steepness baseline before ranking, or stochastic lanes (a lane whose
history is already maximally compressed) farm the queue. Evaluated on a stochastic grid
world vs prediction-error, visitation-count, and RND baselines.

Overlap: same zero-outside-self-trace result as Find 1 (grep this sitting). Genuinely new.

### Find 3: The first vendor-measured 4-bit-KV reasoning deltas: about 0.3 to 1.6 points, workload-dependent (lmsys blog, 2026-09-16)

Quote (lmsys.org/blog/2026-09-16-nvfp4-kv-cache, fetched this sitting): "NVFP4 scored 0.31
percentage points lower than FP8 on GSM8K and 1.01 points lower on GPQA-Diamond" (Qwen3.8-27B;
SWE-bench Verified 381/500 vs 389/500; AIME 2025 matched at 98.33).

Why it matters: this prices the KV rung the ladder probe stacks UNDER weight quant: 4-bit KV
against an FP8 KV baseline costs about a third of a point on GSM8K, about one point on
GPQA-Diamond, 1.6 on SWE-bench, zero on AIME, while buying 26-30 percent decode throughput
and 1.78x capacity. Also names its own boundary ("two models and a small set of tasks do not
establish a general relationship between model size and quantization tolerance") and is
Blackwell-only, so it is a bound-finding for the ladder, not a serving option for the estate.

Overlap: "NVFP4 KV" as a concept is banked at watch/inbox/NIGHT_EXTERNAL_MEMORY_20260911.md:22
(citing developer.nvidia.com's NVFP4 KV post plus AMD TurboQuant and OpenVINO INT4; parked in
the Rocinante docket); the 10-03 sweep's tmp candidate dumps list it unbanked. The lmsys post
itself and its per-task deltas are new at the banking layer (grep this sitting).

### Find 4: EXL3 community verdict, resolved through the fxtwitter door: excellent and unusable on AMD (X long-form article, 2026-07-29)

Quote (verbatim post text via api.fxtwitter.com/Mayhem4Markets/status/2082487427138994230,
fetched this sitting): "Running a 70-billion-parameter language model on a single graphics
card sounds impossible."

Why it matters: closes the EXL2/EXL3 community-ranking gap the sibling arXiv lane left OWED
today ("EXL2/EXL3 community ranking: ... no primary page fetched ... UNVERIFIED and stays
OWED", quantization-and-compression-arxiv.md:242-244). Article key points (fetch rendering):
QTIP-based trellis quantization with Hadamard transforms; 70B at about 1.6 bpw under 16 GB
VRAM; near-FP16 quality at 6-8 bpw; a "repeatable and statistically significant" quality bump
around 3 bpw; drawbacks "NVIDIA-only (no AMD/CPU support), served mainly via TabbyAPI",
lacking vLLM/SGLang integration; GGUF stays the broad-hardware choice. For the operator's RX
5600 XT the AMD line is the verdict: the format ranks best-in-class and is excluded.

Overlap: the fxtwitter JSON is HELD since 10-01
(watch/inbox/frontier_olm_2026-10-01/sweep/_fx/Mayhem4Markets_status_2082487427138994230.json,
26,355 bytes, catalog row 03eb4091b522), and the 10-01 x lane DROPPED it as "thin"
(quantization-compression-x.md:42). Never banked as a find in any register; banked here with
that stated, at new depth (the AMD-exclusion and 3 bpw facts), and in service of a sibling's
named OWED. Not new to disk, new to the bank.

### Find 5: Weight quantization Pareto-dominates KV eviction for reasoning (OpenReview, date unknown, SNIPPET ONLY)

Quote (search-result snippet, openreview.net/forum?id=uCOMb0EsPq; full page Cloudflare-blocked
this sitting): "We find that NF4 and Int8 weight quantization strongly outperform baselines
and key-value (KV) cache token eviction methods on Pa[reto]" (snippet truncates at "Pareto").

Why it matters: "Reasoning-Focused Evaluation of Efficient Long-Context Methods" (J. Zhang et
al.) is direct published support for the banked ladder ordering (weights first, KV surgery
last): even 4-bit-class weight quant (NF4) beats KV intervention on the memory-reasoning
Pareto frontier. Banked as a snippet with the door failure stated; the primary fetch is OWED.

Overlap: grep this sitting: uCOMb0EsPq ZERO hits outside this session's own trace; the title
phrase appeared in my own searches only. Genuinely new at the banking layer, snippet-grade.

### Find 6: Q8_0 KV at or above FP16 on a coder model, snippet-grade (energyflowx, Mar 2026, SNIPPET ONLY)

Quote (search-result snippet, energyflowx.com/articles/qwen3-kv-cache-quantization; the page
body is a client-rendered shell on BOTH the WebFetch and web_reader doors this sitting, only
the meta description rendered): "8-bit KV cache quantization (Q8_0) scores slightly higher
than FP16 baseline across both LongBench-v2 and BigCodeBench metrics."

Why it matters: the first direct public datum on the exact rung the estate already serves
unmeasured (SAELIS q8_0 KV, mag/vast_launcher.py:444, :457; owed probe 5's KV arm): q8_0 KV
cost nothing and possibly helped on long-context and code benchmarks for Qwen3-Coder-30B on a
32 GB consumer GPU, twelve measured configurations per the meta description. Same
shell-disease class as the free-credit pricing pages the burns ledger closed on (client-side
rendering, no static body). Treat as supporting evidence, not a measurement receipt.

Overlap: grep this sitting: the URL slug nvfp4-kv-cache is unrelated; the energyflowx article
has ZERO estate hits outside this session's trace. Genuinely new, snippet-grade.

## Sighted, NOT banked (with reasons)

- Unsloth Dynamic 3.0 GGUFs: THIRD consecutive unverified window (10-03 x lane 403; this
  sitting 403 WebFetch AND web_reader 500 on unsloth.ai/blog/dynamic-v3). Secondhand only:
  OSCHINA report (about +10 pct same-size top accuracy vs v2.0, best KL divergence, debuts
  Qwen3.8-27B) and a buttondown AINews summary (1.78-bit upcast experiments, 2.71-bit-class
  recommended). Aggregator-attributed, never banked as fact. The 09-30 and 10-03 sweeps
  already sighted it unbanked; keep it sighted.
- 2504.04823 (Quantization Hurts Reasoning?, COLM 2025): read end to end this sitting but
  ALREADY HELD twice (kv50_findings.json 2026-09-25; 10-03 pass-1 OUT). Do not re-bank; my
  read's only addition (no CoT-length inflation at 4/8-bit PTQ) is recorded under RQ1.
- latent.space AINews q8-KV-worse-than-bf16-reverted anecdote: could not resolve to a primary
  page (search returns the domain only). Anecdote weight only; noted under RQ2 as the counter-
  datum to Find 6.
- OBC-Prune (alphaxiv, Sep 2026) and TRIM-KV (openreview qCaq3jGb0S): snippet-level only,
  family-stability and near-lossless-CoT support lines; abs pages not fetched, named for the
  next window.
- Google TurboQuant KV (generativeai.pub May 2026): sighted; the estate already separates it
  from LMCache's storage-layer TurboQuant (10-01 lane pre-read note). Not read to primary.
- dev.to GGUF guide, gigagpu/helloaihub/local-ai-zone format guides, ResearchGate GGUF IQ
  study, HF imatrix thread: vendor-guide class, snippet-level, no primary fetch, no ladder
  delta. Named and released.
- Q-Filters, Spectral Koopman, SkipKV, QubitCache, Thought-Aware KV Compaction, SeKV:
  KV-compression paper leads from search listings, not fetched this sitting; the KV shelf row
  in RQ5 covers the family.

## OWED / not run

- No probe executed: the reasoning-quant ladder (percolator row 7, owed probe 5) was not fired
  this sitting; this bank arms it (KV floor pricing from Find 3, q8_0 support from Find 6,
  exposure-bias signature from the sibling) and runs nothing.
- Unsloth Dynamic 3.0 primary: fourth attempt owed (try docs.unsloth.ai or the HF model card
  unsloth/Qwen3.8-27B-GGUF discussions next window).
- OpenReview uCOMb0EsPq primary fetch owed (Cloudflare; try the pdf endpoint or arxiv mirror).
- energyflowx twelve-configuration table owed (client-rendered shell; try web_reader with JS
  or find the author's HF/Reddit mirror).
- The 10-04 morning's Schmidhuber drop commits (756c78b1b, 9058dc238) predate this bank; my
  two lineage finds EXTEND the amended candidate, and the percolator rows were not edited by
  this sweep (no write to memory/percolator/ this sitting).
- Door health this sitting: fxtwitter WORKED (1 of 1); arxiv abs doors clean (3 of 3);
  lmsys clean; unsloth.ai 403 + 500 (third window running); openreview Cloudflare-blocked;
  energyflowx client-rendered shell on two doors; WebSearch 1302'd twice of nine queries and
  never returned in-window x.com status ids directly (the standing discovery defect).
