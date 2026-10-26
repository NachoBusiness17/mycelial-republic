# SWEEP: quantization-compression via arXiv (frontier_olm_2026-10-06)

source-fetched: 2026-10-06. Seat: sweep-quantization-compression-arxiv (dynamic-workflow child).
Note: quotes below are verbatim except en-dashes normalized to plain hyphens per the seat
no-em-dash law (hook enforced).
Area map: deliberate-ask quantize target + quantizer v0.6 pack pipeline (law-row propagation into
flash packs) + GPU-ladder purchase gates (memory/rib/RIB_GPU_LADDER_20261001.md); weight quant must
not break scut accuracy, run quantization must not drop law rows.

## Door status (honest)

- arXiv API door GREEN. Six targeted queries against
  `https://export.arxiv.org/api/query?search_query=...` with
  `&sortBy=submittedDate&sortOrder=descending` - the recency-sort params flagged OWED at
  doors.md:28-29 (frontier_olm_2026-10-06/lens/doors.md) were EXECUTED this sweep and worked.
  Queries: broad (cs.LG+cs.CL x "quantization", 40 rows), "KV cache"+quantization (19),
  extreme/1-bit/2-bit (4), vector quantization/codebook (25), "GGUF" (8), small-model quantization (4).
- arXiv /html/ full-text door DEGRADED twice: `arxiv.org/html/2609.14864v1` timed out at 60s twice
  (both attempts), `arxiv.org/html/2609.38121v1` timed out once then succeeded on retry. The
  2609.14864 deep read is therefore abstract-page only (fetched twice, second pass verbatim-quote
  extraction); flagged on that item below. No 403s anywhere; fallback used is the recipe's own
  abs-page, not an invented success.

## Pass 1 census

~60 unique candidates considered (40+19+4+25+8+4 raw rows minus overlap). Strongest 20 shortlisted;
16 were found ALREADY BANKED by sibling sweeps (catalog ages 0-15d) and were NOT re-banked:

Structured Transforms (2609.11687, age 15), Quantization Thresholds Replicate (2609.32042, ages 0+2),
Capability Scaling-Down Laws (2610.02462, 1), TaSQ (2610.03027, 1), HyperThink (2610.03039, 1 +
full card f859317c3 per burns.md:131), BreadthKV (2610.05685, 0), StagQ (2610.05977, 0),
Differentiable Bit-Widths (2610.06026, 0), Anosognosia (2610.06174, 0), HQQ Shared Stopping
(2610.06251, 0), KV Cache Is the New Memory Wall (2609.30854, 0), WUSH-KV (2609.38121, 0),
Devil in the Reconstruction Loss Scale (2610.00983, 0), Disaggregated Quantization (2609.26333, 3),
KV-COBRA (2609.24298, 4), Softmax Reparameterization (2609.31291, 0). Evidence: rg window-greps of
catalog/catalog.jsonl this sitting (zones lsa/intake/reboot_staging).

8 genuinely-new items banked below, every one fetched and read this sitting (5 with full-HTML
end-to-end reads, 5 with abstract-page reads; overlap: 2610.04403 / 2610.04490 / 2610.00432 /
2610.04100 got both).

## Research-question verdicts

**RQ1 (bit ladder to the 2b janitor class).** 2610.04403 refines the banked shape (doors.md:40-42,
"4-bit holds up, 1-bit collapses" HN story): the real boundary is Q4_K_M-clean / Q4_K_S minus 3-6% /
Q2_K-cliff, and below 2B parameters the Q2 cliff is SILENT: inclusion probes stay green while
definitions drop 20-67%. WikiText-2 PPL does not calibrate the damage (44.7% vs 47.6% PPL penalty
separates 3.6% vs 43.6% definitional loss), and provider artifacts differ (Llama-3.2-1B Ollama build
-61.1% vs Unsloth -43.6%). So the owed scoped qwen2.5:7b Q4_K_M vs q8_0 A/B (burns.md:209) must be
scored with task-level probes on OUR scut, per artifact, with the provider pinned - PPL or
perplexity-adjacent scoring would read green through exactly the failure this paper isolates.
gemma:2b (our janitor class) sits inside the sub-2B dissociation regime; any ladder run below Q4
there needs a definition-style probe, not a fluency probe. Already-banked 2609.32042 corroborates
from the agentic side: all three models collapse between 3-bit and 2-bit on tool use, failure modes
differ per model.

**RQ2 (KV lower rung).** Banked B4 numbers (q8_0 KV decode 100.8 vs f16 55.9 t/s, burns.md:59) remain
the safe rung. WUSH-KV (banked by a sibling TODAY, age 0) shows 2-bit KV is viable only with
data-adaptive transforms computed from second-order statistics: naive transforms fail hard
(Hadamard PPL 258.29 vs WUSH 10.51 on Qwen3-8B, BF16 9.72) and the paper reports NO throughput
results (listed as future work). No read paper evidences a KV low-bit throughput win at 2b-class
context lengths. The q4_0 KV accuracy/throughput probe therefore stays OWED locally, and the
external frontier warns the naive version will cost accuracy without transform design.

**RQ3 (AQLM method-tier rule).** HOLDS, sharpened on two axes, no amendment earned:
(1) stage-specific: BARQ is a fitting-stage refinement for codebook methods (soft assignments
discarded after fitting; runtime unchanged) - it says nothing about scalar K-quant GGUF lanes;
XOR-Trellis is format+decoder-specific; SPHQuant needs a custom GEMV kernel; TORQUE is a
rotation-schedule result. (2) basis-specific: XOR-Trellis' own limitation section states
D-weighting is NOT beneficial when random Hadamard rotation is already applied - the same trick
flips sign across bases. Of 8 new items, zero claim cross-tier transfer and none target GGUF
K-quant lanes. Rung-amendment candidates if a 2-bit tier is ever opened: XOR-Trellis 2.25 bpw
rotation-free beats QTIP-with-Hadamard (8.00 vs 8.48 WT2, Llama-3.1-8B) and SPHQuant +30.3% decode
over QTIP on RTX A6000.

**RQ4 (run-quantization propagation).** No new external item bears on law-row propagation into flash
packs (quantizer v0.6, 620->625 rows, 2 flash rows MEASURED ON was 0/12, burns.md:139-140) or on the
13/338 truncation-literal loss growing with pack size (burns.md:90). Closest external analogs
(batched-decode answer leakage 2610.06251; quantization fingerprints 2610.06174) were banked by
siblings today. Propagation stays an estate-internal invariant test; the frontier offers no shortcut
and no counterexample.

**RQ5 (HyperThink bridge).** Source banked (burns.md:131). The sweep adds two falsifiable anchors on
the weight-space side: BARQ makes "codebook quality" measurable and gives sufficient conditions
(balance <-> lower distortion, retention conditions for finite Sinkhorn), so a concrete 2b bridge
test exists - Sinkhorn-balance-cluster the quantized_thought pack rows, measure conditioning quality
against codeword balance. FedFit independently shows disjoint vector banks rebuild adapter matrices
at up to 100x compression on Qwen2.5 with parity PPL. Verdict: the analogy is falsifiable as stated;
the untested half is whether pack rows cluster at all, which is an estate measurement, not an
external fact.

## Banked items (8, strongest first)

1. **Saying, Not Knowing: Aggressively GGUF-Quantized Small Language Models Still Write Rare Words
   They Can No Longer Define** (2610.04403, 2026-10-03). Deep read: abs + full HTML. 27 GGUF
   artifacts, 13 families, 0.35B-14B, ladders to Q2_K (~2.6 bpw), 429 rare words, two probes.
   Three regimes at Q2: total collapse (Qwen2.5-3B, Phi-3/3.5 >97% loss), silent sub-2B dissociation
   (definitions -20-67% at near-zero inclusion loss; Granite-4.0-H-1B inclusion -2.1% vs definitions
   -43.6%), robust above ~3B. Q4_K_M lexically clean at >=1B; Q4_K_S already -3-6% in some
   artifacts. Parameter count predicts damage (rho=0.72, p=1e-4); tokenizer vocab does not
   (rho=0.12). PPL fails as a calibrator. Quote: "In every sub-2B artifact, definitions fall 20-67%
   below the artifact's baseline, typically several times the inclusion loss."
2. **BARQ: Balanced Codebook Refinement for Low-Bit LLM Quantization** (2610.04490, 2026-10-03).
   Deep read: abs + full HTML. Entropically-regularized OT (Sinkhorn) forces equal codeword mass
   during fitting; drop-in for GPT-VQ-class codebook methods; mean 7.0% PPL cut over 60 paired
   configs, gains grow with codebook size (1.2% at K4 -> 10.4% at K256). Models Llama3.2-1B through
   Qwen3-32B at ~2.0-2.5 bpw. Quote: "BARQ achieves lower perplexity and higher mean zero-shot
   accuracy than the evaluated baselines at comparable bit budgets."
3. **XOR-Trellis: Ultra-Low-Complexity Dequantization and Curvature-Aware Hadamard-Free LLM
   Quantization** (2610.00432, 2026-09-30). Deep read: abs + full HTML. Trellis-coded FP4 weights at
   ~2.25 effective bpw with a ~14-gate XOR decoder; curvature-aware (LDL diagonal) Viterbi costs and
   energy ordering replace rotation entirely; beats QTIP+Hadamard rotation-free (8.00 vs 8.48 WT2,
   Llama-3.1-8B; 5.52 vs 6.31 on 70B-Instruct). Quote: "The positive correlation between anisotropy
   and GD supports the proposed mechanism: when conditional feature sensitivities are uneven,
   assigning equal branch-cost weight to every coordinate is increasingly mismatched to the Hessian
   metric."
4. **GGUF-Metadata Prediction of Single-Sequence llama.cpp Throughput Across Three Systems**
   (2609.14864, 2026-09-14). Abstract-page deep read ONLY (HTML timed out twice, flagged above).
   Roofline-shaped predictors from GGUF metadata; 318 measurements, 53 host-file configs, 2x M4 Max
   + RTX 5080; active-parameter decode model MAPE 13.1/14.4/36.1% vs 49.4/55.3/51.9% charging total
   params; leave-one-host-out 11.6/16.8/36.0%. Quote: "GGUF structure helps on all three systems,
   but fitted efficiencies are not universal." Estate use: throughput priors for the GPU-ladder
   gates must be host-fitted, never transplanted across machines.
5. **TORQUE: Optimizing What (not) to Quantize Before and After Rotation** (2609.36032, 2026-09-28).
   Abstract read. Jointly optimizes which coordinates stay high precision before AND after rotation
   under a fixed bit budget; proves top-k pre-rotation retention optimal per k; applications include
   KV-cache compression. Quote: "We derive a quantization error upper bound and prove that top-k
   pre-rotation retention minimizes it for each k."
6. **Progressive Multi-Ancestor Bit-Depth Distillation** (2610.04100, 2026-10-02). Deep read: abs +
   full HTML. Growing pool of descending-precision teachers stabilizes ultra-low-bit QAT; W2A2
   ResNet-18/CIFAR-100 +1.06% over best baseline; full teacher pool beats FP32-only by 1.33 pts.
   CAVEAT: CNN-only experiments (ResNet/MobileNetV2) - no LM evidence; transfer to the 2b janitor
   ladder is a hypothesis, not a result. Quote: "This multi-ancestor, multi-stage design stabilizes
   ultra-low-bit quantization by lowering quantization noise profiles"
7. **SPHQuant: Efficient extreme low bit weight quantization for Vision-Language Models**
   (2609.24875, 2026-09-21). Abstract read. Rotation-free spherical quantization isolates outlier
   magnitude into a radius; custom shared-memory GEMV kernel; matches SOTA extreme-low-bit and
   +30.3% decode throughput over QTIP on RTX A6000. Quote (verbatim prefix, source sentence longer
   than the fetcher's quote cap): "Experiments show that SPHQuant matches the performance of
   state-of-the-art extreme low-bit quantization methods while improving..."
8. **FedFit: Federated Fine-Tuning of LLMs via Vector-Bank Parameterization and Quantization**
   (2610.01537, 2026-10-01). Abstract read. Two disjoint global vector banks rebuild adapter
   matrices; blockwise quantization + client-side error feedback; parity PPL with federated LoRA at
   up to 100x higher compression on Qwen2.5. Quote: "Extensive experiments on Qwen2.5 models
   demonstrate that FedFit achieves perplexity performance comparable to standard federated LoRA
   methods"

## Not run here (owed stays owed)

The owed scoped qwen2.5:7b Q4_K_M vs q8_0 A/B (burns.md:209), the q4_0 KV accuracy probe, and the
2b bit-ladder run are Ollama-side estate experiments; this sweep seat fetched and read public
sources only and ran no local model. What the sweep changes is their scoring design (RQ1: task
probes not PPL, provider pinned, per-artifact) and their priors (RQ2: naive low-bit KV fails
without transform design; RQ3: tier rule stands).

## Instruments this sitting

rg window-greps over catalog/catalog.jsonl and memory/ (commands in the run transcript); six arXiv
API fetches; eleven arxiv.org abs/html fetches. Counts: 8 items banked / 16 already-held excluded /
~60 considered.
