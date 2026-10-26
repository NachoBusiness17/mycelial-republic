# Sweep: quantization-and-compression via arxiv (frontier_olm_2026-10-04)

source-fetched: 2026-10-04. House laws held: ascii only, no em or en dashes, every claim
cites a page fetched or a command run this sitting. Bank file for the sweep-quantization-and-
compression-arxiv lane; result JSON returned beside it by the same lane.

## Method (what actually ran)

- Pass 1 (broad sweep): four arXiv Atom API queries over export.arxiv.org, sorted submittedDate
  descending: (1) all:"quantization" AND all:"reasoning" max 30 (30 entries rendered); (2)
  all:"KV cache" AND all:"quantization" max 20 (20 rendered); (3) all:"intrinsic reward" AND
  all:"compression" max 20 (4 rendered); (4) all:GGUF OR all:"k-quants" OR all:"EXL2" max 15
  (15 rendered). Total rendered entries 69; after dedup and off-area rejection (VQ-VAE
  perception, driving, physics field quantization, clinical extraction), 32 in-area candidates
  were named and considered. Comfortably past the 30 bar.
- Pass 2 (deep read): TEN abs pages fetched and read end to end this sitting: 2609.26708,
  2609.38121, 2609.36760, 2609.30854, 2606.11417, 2609.06473, 2609.05881, 2607.18433,
  2607.14181, 2609.08637. Banked items below carry only quotes from those fetches; where the
  fetch tool's own rendering is the source of the exact wording it is marked (fetch rendering).
- Overlap instrument (run this sitting, from repo root): `rg -uu -F -o` over catalog memory
  watch/inbox docs state configs for ten arXiv ids (2609.26708, 2609.38121, 2609.36760,
  2609.30854, 2606.11417, 2609.06473, 2609.05881, 2607.18433, 2607.14181, 2609.25014), then a
  second `rg -uu -i -F` pass over six title phrases. Output counts quoted per item below.

## Answers to the five research questions

**RQ1 (published quant-versus-reasoning rungs; contradictions with banked rungs).** The banked
ladder (RATIO 2609.39801 W3 CoT inflation 2.94x GPTQ / 3.77x AWQ; quesma Qwen3.8-27B Q4_K_M
free, 2-bit about 1.25x tokens, 1-bit collapse; 2609.32042 Q3_K_M working edge, Q2_K cliff) now
gains measured rungs BELOW 4 bits and a method dimension. 2609.26708 measures 2.79 and 1.88
effective bits across four models: quantization-aware distillation alone leaves MATH-500 at 35
percent BF16 retention, on-policy distillation raises it to 70 percent (HumanEval 66 to 91
percent), and it names the mechanism "quantization-amplified exposure bias": deviations compound
along the model's own autoregressive trajectory. 2609.06473 shows a 7-9B model at NF4 losing
GSM8K 0.545 to 0.365 at alpha=0, so 4-bit-class weight damage is NOT uniformly free on math even
before any intervention. 2607.14181 adds the method ordering on exactly the estate's worker
family: AQLM matches or exceeds full precision, QuIP# degrades most, on Qwen2.5-Coder and
CodeLlama over McEval/CoderEval pass@1. NO item contradicts a banked rung; every new datum
coheres with the flat-then-cliff law (damage concentrates below 4 bits and surfaces in the
behavior channel first). The one pressure point: quesma's "Q4_K_M free" and 06473's NF4 -18
points are both 4-bit-class results with opposite readings, resolved by the method dimension
(Q4_K_M is a GGUF k-quant, NF4 a different format), which is the same method-dependence 25014
already banked (AWQ/GPTQ vs Q4_K_M PII divergence).

**RQ2 (KV-cache quantization levels vs reasoning; stacking bound).** The banked SoK row
(frontier_olm_2026-10-02 register.jsonl:6) already holds the spine: 8-bit KV free, 4-bit
near-free with per-channel keys, naive 2-bit loses more than 1 perplexity point without a
full-precision residual window. This sitting's reads add the MLA-family leg and the reasoning
channel: 2609.36760 reports the first joint INT4 caching of content and RoPE caches across four
MLA model families with only "minimal accuracy degradation", and INT2-content/INT4-RoPE stays
competitive on reasoning and code benchmarks (fetch rendering of the abs page), at 3.59x
physical compression and 128K context. Banked WUSH-KV (2609.38121, 10-02 sweep :24, :39) shows
2-bit KV reachable with data-adaptive transforms in SGLang. Stack bound: every reasoning-grade
sub-4-bit KV result rides custom transforms and kernels (SGLang, native low-bit attention
kernels) that the estate's llama.cpp/Ollama tier does not expose; and at the estate envelope
(CONTEXT=8k, 6 GB card, configs/lanes.yaml:28-37) the SoK's own crossover logic puts the janitor
fleet below the KV-dominates regime, so KV quant buys capacity, not speed or quality. The ladder
can therefore stack q8_0 KV (banked free) and 4-bit KV (near-free) under weight quant, but going
below 4-bit KV has no reasoning-grade evidence at naive quantizers, only transform-based results
on serving stacks the estate does not run.

**RQ3 (compression-as-progress and intrinsic-reward lineage vs the amended percolator
candidate).** The lineage lives and it EXTENDS the amended candidate with a hard design
constraint. 2606.11417 makes the folk claim precise and proves it: if intrinsic reward is the
signed decrease of a fixed sealed-audit loss, cumulative reward telescopes to endpoint audit
improvement (finite panels bounded by 2 Delta_n), and the abstract names the failure modes
verbatim: "the guarantee disappears if progress is clipped, scored on the agent's own stream,
exposed to a high-capacity model on a reusable panel, or applied to a neural class that makes
Delta_n vacuous". The amended candidate (memory/percolator/candidates.jsonl:19, primary metric
"carried-history retired (bytes) + verbs minted", kill = lose on BOTH) is scored on the estate's
own lanes: that is own-stream scoring on a reusable panel, exactly two of the named failure
modes, so the amendment's metric confound fix is necessary but not sufficient; without a sealed
panel the 5-wave kill test is uninterpretable in both directions. 2607.18433 (Levin co-author)
supplies the second leg: a closed-form differentiable learnable-novelty estimator that splits
surprise into learnable and unlearnable parts, killing the noisy-TV failure, improving task
baselines in nine of ten RL environments with zero collapses. Port shape: keep the amendment's
primary metric, sign it (progress can go negative), freeze the audit set before wave one, and
prefer a finite symbolic audit panel (the estate's deterministic gates and checkers) because the
theorem itself says Delta_n is vacuous for neural model classes.

**RQ4 (format and bit-width for the janitor fleet on this hardware; family stability).** Within
the tier the estate can actually pull (GGUF via Ollama on the RX 5600 XT 6 GB, Vulkan), the
banked law stands and gains confirmation: Q4_K_M the working default, Q3_K_M the agentic edge,
Q2_K the cliff, and 2607.14181's method ranking (AQLM best, QuIP# worst, security stable) is
stable across BOTH tested families (Qwen2.5-Coder, CodeLlama) but AQLM/QuIP# are not available
in the Ollama GGUF tier, so the ranking does not change the fleet's practical choice; it does
warn that any future non-GGUF backend swap (exllamav3, AQLM runtimes) reopens the method
question. EXL2/EXL3: the community door DEGRADED this sitting. WebSearch returned only a GitHub
issue stub, a forum thread, a HuggingFace release card, and a vendor blog, none fetchable to a
primary quotable page; the snippet-level claim that a 2 bpw EXL3 quant fits about 60 percent
more context than an equivalent GGUF is UNVERIFIED and stays out of the banked set (OWED
below). Stability across families is supported where the estate holds controlled evidence
(14181 two families, 32042 three models: thresholds replicate, failure modes do not).

**RQ5 (seed rows for a quantization shelf).** The corpus lens (lens/corpus.md:26) is right that
no shelf exists. First rows, all verified this sitting or already banked with citations: spine
= 2609.30854 SoK (banked, register row 6 of the 10-02 cycle); throughput = 2609.14864 (banked);
measurement design = 2609.06473 (NEW, this bank) and 2608.06564 (banked 09-30); rungs = 26708 +
36760 + 38121 (this bank and banked); method ranking = 2607.14181 (NEW, this bank); registry
hygiene = 2609.05881 (banked 09-28); the intrinsic-reward / compression-progress lineage =
2606.11417 + 2607.18433 (NEW, this bank), which also seeds the missing RL/post-training shelf
alongside Pass-1 leads 2609.22870 (full-pipeline FP8 RL) and 2609.33548 (ternary sparse
zeroth-order BitNet finetuning), both named from the API listing only, NOT banked this sitting.

## Banked finds (this sitting, with overlap)

### Find 1: Signed compression progress is Goodhart-resistant ONLY on a sealed audit (2606.11417, 2026-06-09)

Quote (abstract, fetch rendering): "the guarantee disappears if progress is clipped, scored on
the agent's own stream, exposed to a high-capacity model on a reusable panel, or applied to a
neural class that makes Delta_n vacuous".

Why it matters: the amended curiosity-scored lane-selection candidate in the percolator
(candidates.jsonl:19) scores carried-history-retired plus verbs-minted on the estate's own
lanes; the theorem names that configuration (own stream, reusable panel) as exactly where the
Goodhart guarantee vanishes, so the candidate's 5-wave kill test needs a sealed, signed,
frozen-panel redesign before wave one or its outcome is uninterpretable. Lean 4 mechanization
and experiments (deviation scales n^-0.527; resists clip-farming, stream leakage, noisy-TV
curiosity; reusable audits exploitable) are on the abs page.

Overlap: ZERO hits for the id and the title phrase across catalog memory watch/inbox docs state
configs (rg run this sitting). The dropped Schmidhuber trio (git 756c78b1b + 9058dc238) and the
percolator rows 18/19 are the estate's prior art; neither names this paper. Genuinely new.

### Find 2: The sub-3-bit reasoning rung is measured, and the failure is exposure bias, not lost knowledge (2609.26708, 2026-09-22)

Quote (abstract, fetch rendering): "Across four models at 2.79 and 1.88 effective bits, OPD
raises average BF16 performance retention from 35% to 70% on MATH-500 and from 66% to 91% on
HumanEval".

Why it matters: this is the rung-below-4 data the reasoning-quant ladder probe (percolator row
7) predicted it needed; it also gives the diagnostic channel a name, quantization-amplified
exposure bias (long generations degenerate into repetitive loops that exhaust the decoding
budget), which matches the banked overthinking/empty-content channels and adds a concrete
falsifiable signature for the ladder's Q4 arm: loop-degeneration and budget exhaustion, not just
longer CoT. The fix is training-side (on-policy distillation through the quantized forward path
against a frozen FP teacher) and out of estate reach today; the diagnosis port is not.

Overlap: held abstract stub only (state/arxiv/2026-09-23/2609.26708v1.txt, 1,708 bytes, catalog
row 445f345aa09f, two digest.jsonl rows); ZERO hits in any frontier_olm digest, register, or
steal card before this sitting (rg this sitting). Never banked as a find. Genuinely new at the
banking layer.

### Find 3: MLA KV caching goes to INT4 jointly, INT2-content/INT4-RoPE stays reasoning-competitive (2609.36760, 2026-09-29, v2 09-30)

Quote (abs page, fetch rendering): "Content cache compressed to INT2 while RoPE key cache stays
at INT4, keeping competitive performance" on "challenging reasoning and code benchmarks"; 3.59x
physical cache compression at 128K context; 5.168x whole-job output throughput vs BF16 under
cache pressure.

Why it matters: this is the second KV rung leg the estate's KV-slot pilot and state-pool ceiling
row wanted, and it is family-specific evidence the banked SoK/WUSH-KV rows lack: the RoPE path
is the fragile half (its errors are amplified; the paper derives path-specific transforms fused
offline into weights with a positional-distortion bound). For the estate: another confirmation
that reasoning-grade low-bit KV is a transformed-weights game, and the first four-family
replication (the stability-across-families question) at the KV layer.

Overlap: id appears ONLY in the 10-03 sweep's raw query dump
(watch/inbox/frontier_olm_2026-10-03/sweep/_raw2/q1_kvcache.xml, 3 hits, listed never read);
ZERO hits in any digest, register, percolator, or steal file (rg this sitting). Genuinely new
at the banking layer.

### Find 4: Under quantization, capability cost is asymmetric and can dominate the intervention (2609.06473, 2026-09-06)

Quote (abs page, fetch rendering): "a substantial baseline capability shift for Mistral-NF4
(0.545 to 0.365 GSM8K at alpha=0), demonstrating that compression can dominate the steering
intervention". Also: reasoning-length shortening fails as a step function after only 12-30
percent shortening (model-dependent), while lengthening is graded until cap-runaway collapse;
steering-vector cosine vs FP16 stays 0.989-0.998 (INT8).

Why it matters: three ports. (1) Ladder design: the estate's Q4-vs-Q8 A/B predictions should
expect asymmetric dose-response, inflation graded, degradation cliff-like, and the paper's
censored iso-effect construction is the fix for floor-anchored ladders (the estate's
token-count comparisons are floor-bounded by caps, same trap). (2) The NF4 -18 GSM8K datum is
the strongest counterweight yet to any "4-bit is free on math" reading, resolved against
quesma's Q4_K_M only by the method dimension. (3) Sampler-side mitigations (the TSPD port from
banked RATIO) survive quantization structurally: the behavioral DIRECTION survives (cosine
0.989-0.998), the cost structure does not, so a penalty table tuned on FP may not transfer to
the Q4 arm; tune on the arm you run.

Overlap: ZERO hits for id and title phrase across catalog memory watch/inbox docs state configs
(rg this sitting). Genuinely new.

### Find 5: Learnable novelty: the closed-form estimator the compression-progress reward wanted (2607.18433, 2026-07-20)

Quote (abs page, fetch rendering): "novelty search, which seeks surprise, is transfixed by a
noisy television screen, while the free-energy principle, which avoids surprise, is most
content in a dark room". As intrinsic reward it improves task baselines in nine of ten
environments and collapses in none.

Why it matters: second leg of the RQ3 lineage (Michael Levin co-author). It gives the amended
lane-selection candidate a citable, differentiable estimator of learnable surprise, the exact
quantity byte-retirement approximates, and a measured answer to the noisy-TV failure mode the
Goodhart paper also flags. The percolator candidate's bytes-to-verbs ratio is a crude special
case; this is the theory's own quantity in closed form.

Overlap: ZERO hits for id and title phrase across catalog memory watch/inbox docs state configs
(rg this sitting). Genuinely new.

### Find 6: Method ranking on code generation, including GGUF, on the estate's worker family (2607.14181, 2026-07-15)

Quote (abs page, verbatim fragments): "AQLM consistently matches or exceeds the full-precision
baseline, whereas QuIP# exhibits the largest correctness degradation, particularly on complex
prompts." Six methods (GPTQ, AWQ, QuIP#, AQLM, BitsAndBytes, GGUF), two families
(Qwen2.5-Coder, CodeLlama), McEval/CoderEval pass@1 plus maintainability, reliability, security.

Why it matters: the only paper this estate holds that ranks quant METHODS including GGUF on
task quality at code, and it does it on qwen2.5-coder, the pinned worker model family
(configs/lanes.yaml:37). Security stable across all methods; robustness varies; the ranking is
stable across both families. DATE FLAG: submitted 2026-07-15, outside the 30-day preference
window; banked for the shelf-seed and method-ranking value, flagged here as read.

Overlap: ZERO hits for id and title phrase across catalog memory watch/inbox docs state configs
(rg this sitting). Genuinely new.

## Sighted, NOT banked (with reasons)

- 2609.30854 (KV SoK): already a register find, frontier_olm_2026-10-02/register.jsonl:6 with
  the 8-bit-free/4-bit-near-free/naive-2-bit-collapses math; my read re-confirms and adds
  nothing bankable. Do not re-bank.
- 2609.38121 (WUSH-KV): abs-read 10-01 (:44, :61) and carried in the 10-02 RQ2 fold (:24, :39);
  my read adds the QuEST-INT near-optimality proof sentence only. Do not re-bank.
- 2609.05881 (Broken on Arrival): banked in the 0928 cycle (steal card + prior-cycle card) and
  re-cited by today's sibling reddit sweep; 40+ estate hits. Do not re-bank.
- 2609.25014 (AWQ/GPTQ vs Q4_K_M PII): banked 09-30 (quantization-compression-x.md:34, :59,
  :72). Do not re-bank.
- 2609.32042 (thresholds replicate): held abstract + percolator rows 15/16 + prior sweeps.
  Do not re-bank.
- 2609.08637 (Gemma3/Qwen3 political compass at three quant levels): read end to end this
  sitting; quantization is a perturbation axis, levels unnamed on the page; no ladder value.
  Pass-1 lead only.
- 2609.23587 (efficiency-safety dilemma: quantization jailbreak resistance = degraded
  reasoning): Pass-1 API listing only, abs page not fetched; named as a next-window lead.
- 2609.22870, 2609.33548: RL/post-training shelf leads from the listing; abs pages not fetched;
  named, not banked.

## OWED / not run

- No probe executed: the reasoning-quant ladder (percolator row 7, the owed probe 5) was not
  fired this sitting; this sweep arms it with the exposure-bias signature (loop degeneration,
  budget exhaustion) and the censored-ladder warning, nothing more.
- EXL2/EXL3 community ranking: WebSearch returned snippet-level results only (GitHub issue
  stub, poweruser.forum thread, HF release card, startupfortune blog); no primary page fetched,
  the 2 bpw context-capacity claim is UNVERIFIED and stays OWED.
- 2609.23587, 2609.22870, 2609.33548 abs fetches owed next window.
- The RATIO Table-1 byte re-confirmation carried OWED from the 10-03 steal card (:80) remains
  owed.
- Door health: arXiv API and abs pages clean all sitting (14 fetches, zero failures);
  WebSearch intermittently rate-limited per the 10-03 digest note, worked once here with
  degraded result quality on niche community queries.
