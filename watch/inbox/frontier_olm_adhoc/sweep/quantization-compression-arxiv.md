# SWEEP: quantization-compression via arxiv (frontier_olm_adhoc, run 2026-10-11)

source-fetched: adhoc · seat: sweep-quantization-compression-arxiv · moment: 2026-10-11
Doors: export.arxiv.org Atom API rendered clean on 4 targeted queries this run (no
HTTP 429, unlike the 10-10 run which was hard-limited); 8 abs pages fetched and read
end to end; 2 full-HTML texts additionally read (2610.06174, 2610.02462). WebSearch
not needed. Reddit door NOT touched: doors.md:52-60 holds the standing verdict that
old.reddit.com JSON is WebFetch-walled (three consecutive sessions), so the reddit
quant census (RQ2) is not completable from this seat and stays OWED per burns.md:131.

## Prior-bank baseline (what this run must NOT re-bank)

The 2026-10-10 run of this same seat banked: 2607.27275, 2610.07781, 2610.07853,
2512.05117v3, 2610.04403, 2610.07026, 2610.09183, 2512.18792. The 2026-09-28 sweep
banked: 2609.32042, 2505.19433, 2609.32459, 2609.14060, 2609.32474, 2609.14872,
2608.22472, 2609.31430. The OLM fold (corpus/steal/CORPUS_FOLD_FRONTIER_OLM_20261001.md,
per adhoc lens corpus.md:29) already banks the stratification law itself (induction
0.959 vs retrieval 0.554 retention, arXiv 2609.23125). None of my 8 banked items
overlap any of those. This file replaces the 10-10 receipt as the seat's current
sweep record; the 10-10 banked list above preserves its holdings map.

## Pass 1 coverage (30+ requirement)

Four API queries sorted by submittedDate desc: "LLM quantization" (40 results),
cat:cs.CL AND abs:quantization (40), abs:"function calling" AND abs:quantization
(20), abs:"tool calling" AND abs:quantization (15). 45 distinct in-window
(2026-09-11 onward) candidates counted, of which 4 already banked by prior sweeps.
In-window considered-not-banked remainder (titles read at feed level, no abs fetch,
no quotes claimed): 2610.12338 VFold, 2610.11214 KV-quant/linear-attention bridge,
2610.10738 Lossy Compressive Text Autoencoders, 2610.10058 Cache the Encoder Within,
2610.09346 OnlineQAT, 2610.08732 Semantic ID spaces, 2610.08164 Align Then Correct,
2610.07767 TRACE FP4 RL, 2610.07457 AlignQuant, 2610.07032 biomedical MT compression,
2610.06996 MaskAhead, 2610.06026 Differentiable Bit-Widths SVD, 2610.05685 BreadthKV,
2610.03027 TaSQ 1-bit KV, 2609.38169 STEPQuant, 2609.36965 Chinese-Jev INT8, 2609.36760
QuantMLA, 2609.36654 Schur Replay NVFP4, 2609.34259 QuantaSpike, 2609.33923 single
random probe sensitivity, 2609.33887 Redline, 2610.11226 DRO refinement, 2610.07522
Activation Denoising, 2610.04490 BARQ, 2610.00432 XOR-Trellis, 2610.00983
reconstruction loss scale, 2609.25916 CASA, 2609.21450 activation-guided
compensation, 2609.31009 G2PTQ, 2609.30820 looped transformers.

## Pass 2 deep reads

Abs pages end to end: 2610.06174, 2610.02462, 2609.16391, 2609.32902, 2610.09227,
2610.09202, 2609.30846, 2610.06251. Full HTML additionally: 2610.06174v1, 2610.02462v1.
Quote verbatim-ness cross-checked against the estate's independent daily-feed stubs
(state/arxiv/...) by `rg -c` for 6 of 8 items: all 6 phrase checks returned 1 (found).
2609.32902 and the CanonQ method name have no estate stub (rg zero hits estate-wide).

## RQ verdicts

### RQ1: stratification law on the janitor fleet (induction 0.959 vs retrieval 0.554)

Corroborated in shape, three independent ways; still unfired on gemma:2b/gemma4.
- 2610.02462 (full HTML): across a 12-checkpoint panel including Gemma-3 270M-27B and
  Gemma-4 31B, "Compression changes capabilities unevenly and in no fixed order"; the
  capability-loss predictor takes (params, tokens, reference loss, config) and the
  shared density response halves the configuration measurements needed (within 0.020
  nats/token). That half-grid law is what makes the fold's named-but-unfired janitor
  induction/retrieval battery affordable: fit on half the quant steps, predict the rest.
- 2609.16391 (retrieval leg): at INT2, near-identical reconstruction error coexists
  with retention spread of 1.3 to 65.9 percent of full precision, and "Every heuristic
  fails to transfer as stated". Mechanism for the 0.554 leg: the metric most PTQ
  pipelines optimize (weight reconstruction) does not predict retained retrieval.
- 2609.32902: aggregate metrics hide the damage: ternary models "retain as little as
  6% of an identically trained fp16 model's capacity" while perplexity rises only
  1.4-1.6x. Judge by retained capability, never by perplexity or loss.
OWED, unchanged: no in-window paper runs an induction-vs-retrieval battery on
gemma:2b/gemma4; the estate fleet test remains ours alone.

### RQ2: reddit quant census (30-item floor, burns.md:131)

NOT completed: the reddit door is WebFetch-walled (doors.md:52-60 standing verdict)
and this seat's door is arXiv. What arXiv contributes to the census: 2610.06251 is
the measured version of the loudest r/LocalLLaMA lore class ("the quant changed my
model's answers"): swapping an unrelated batch-mate question changes 4-bit HQQ
answers in 170/384 comparisons, cause isolated to the shared stopping rule, and the
FP32 mitigation reduces cache fingerprints without stopping answer changes. The
census floor stays OWED to a curl-side reddit door.

### RQ3: can the 24 provenance-only rows ever carry decision force (laws.md:85, 89)?

The window delivers the decisive external negative. 2610.06174 (full HTML): models
cannot self-report their quantization state; classification from generated text sits
under 40 percent, barely above chance. Internal probes hit near 100 percent after the
first quantized layer, but a LoRA trained to read those fingerprints "fails entirely
to generalize across quantization methods": unseen AWQ/RTN 8-bit models are uniformly
predicted "16-bit", and even a group-size change collapses it. Implication for the
ghost: a quantized lattice cannot certify its own substrate state, and trained
readouts overfit the exact quantization method, which is precisely the 17-of-21
trust-bytes probe failure pattern. Decision force stays external: the path:line
receipt (laws.md:114) is the only carrier, now with published evidence behind it.

### RQ4: sovereign-isolation quantizer acceptance bars (burns.md:123-126)

Two measured bars this window, joining the banked 2610.07853 export-provenance bar:
- 2609.30846 I-Parakeet: the no-fallback bar demonstrated by construction, not
  promise: an integer formulation of relative-positional attention plus a minimax
  Swish approximation lets a 0.6B Conformer run "on a smartphone NPU without any
  floating-point operator or CPU fallback" at 4.97 percent WER, RTF 0.048, 7.5x over
  the CPU baseline. The acceptance-bar pattern for returneditor/Kisoku-class checks:
  eliminate the fallback path architecturally, then measure on-device.
- 2610.06251: the request-independence bar: a sovereign serving path must not let
  batch composition change answers; HQQ 4-bit fails it today (170/384), and the
  paper's fix ladder (fixed iterations or request-local stopping) is the audit spec.
Composite sovereign bar now citable as three named tests: no cloud suffix (ours),
no fallback path (I-Parakeet pattern), no batch coupling (2610.06251 audit).

### RQ5: sub-4-bit structured output on 1-8B (headroom above the tie, burns.md:250)

Headroom exists but lives in QAT-style canonicalization, not post-hoc GGUF steps:
- 2610.09202 CanonQ: W2A4KV2 across LLaMA3-1B/3B/8B plus Qwen3-1.7B;
  "CanonQ-Omni achieves up to 14.28x lower WikiText-2 perplexity" than prior SOTA
  at that regime, and on instruction-tuned MobileLLM-Pro-1B the relative gains are
  41.7 percent HumanEval pass@1 and 39.1 percent GSM8K exact match. Code generation
  is structured output; this is the strongest in-window evidence that 2-4 bit
  joint compression can hold it at 1-8B.
- Negative rider, 2609.32902: post-training quantization "recovered no measurable
  capacity below 4 bits". Sub-4-bit via PTQ stays closed; sub-4-bit via QAT with
  canonical source mapping is where a re-run has headroom.
- Consistency with banked holdings: the 3-to-2 bit GGUF cliff (2609.32042) and the
  Q4_K_M knee (2610.07026) both sit on the PTQ side of that line.

## Banked items (8, strongest first; overlap stated)

1. 2610.06174 Anosognosia in LLMs (2026-10-05): overlap = daily-feed stub only
   (state/arxiv/2026-10-06/2610.06174v1.txt), zero prior sweep banks; delta = full
   HTML read (probe numbers, GPTQ/AWQ/RTN 8/4-bit, LoRA generalization failure).
2. 2610.02462 Capability Scaling-Down Laws (2026-10-01): stub only
   (state/arxiv/2026-10-05/); delta = full HTML read (panel, RTN 3-8 bits, half-grid
   law, no-fixed-order finding).
3. 2609.16391 Where PTQ Breaks Text Embedders (2026-09-14): stub only
   (state/arxiv/2026-09-16/); delta = deep abs read (INT2 retention spread,
   heuristic-transfer failure, 109M-student-beats-teacher result).
4. 2610.09202 Few Bits, One Law / CanonQ (2026-10-06): stub only
   (state/arxiv/2026-10-08/); method name zero estate hits; delta = deep abs read.
5. 2609.32902 Linger and Lose (2026-09-26): ZERO estate hits anywhere (rg over
   catalog, memory/, corpus/, both prior sweep dirs); fully new.
6. 2610.06251 Shared Stopping Decisions in HQQ (2026-10-05): stub only
   (state/arxiv/2026-10-06/); delta = deep abs read (170/384, cause isolation).
7. 2609.30846 I-Parakeet (2026-09-25): stub only (state/arxiv/2026-09-28/); delta =
   deep abs read (no-FP/no-fallback bar, WER/RTF numbers).
8. 2610.09227 Quantize by Drift (2026-10-06): stub only (state/arxiv/2026-10-08/);
   delta = deep abs read (Spearman 0.911, honest minus-one-point allocation negative).

## Feeds

- memory/corpus/quantized_thought/: the Anosognosia negative (substrate cannot
  self-certify; readouts are method-overfit) belongs beside the inflated-echo law as
  the external invariant answering laws.md:85-89; the Linger-and-Lose law (judge
  retained capacity, not loss) is the compiler-side measurement discipline.
- memory/frontier/HELP_WANTED.md quantized-lattice-fold ask (corpus.md:41): cite
  2610.06174 as published grounds that decision force needs an external carrier.
- RIB_GPU_LADDER quant-on-current-box decision (laws.md:50): the sub-4-bit headroom
  is QAT-shaped (CanonQ), not another GGUF step; the half-grid law (2610.02462)
  prices the janitor battery re-run at half the quant steps.

## Honesty block

- Fetched and read this ask: 4 API queries, 8 abs pages, 2 full-HTML papers. All
  quotes verbatim from those fetches; 6 of 8 independently confirmed against the
  estate's own feed stubs by `rg -c` (all found); 2609.32902 quote rests on my fetch
  alone (no stub exists) and carries the lower confidence in the JSON result.
- Overlap instrument: `rg -il "<title phrase>" catalog/catalog.jsonl memory/ corpus/
  watch/inbox/frontier_olm_20260928 watch/inbox/frontier_olm_adhoc`, run 2026-10-11
  by this seat. An initial plain `grep -ril` over state/ was killed for slowness and
  redone with rg; catalog title hits were then read in full (all were stub pulls).
- Not run: any estate gate, test suite, or live janitor measurement; the reddit
  census; any full PDF beyond the two HTML reads. Feed-level items carry no quotes.
- The ask's lens citations (corpus.md:29, laws.md:85/89/114, burns.md:123-131/250,
  doors.md:52-60) were opened and read at those lines this session before use.
