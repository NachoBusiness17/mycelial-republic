# deep-quantizer-theory: the thought quantizer as a compression system, measured

Bank: watch/inbox/burn_reset_20260927/flash50/deep-quantizer-theory.md
Seat: deep-gopher-deep-quantizer-theory, 2026-09-28. Tree: mag/run-beta1-factory-build-audi-20260806T231709Z.

## 0. Instruments run this ask (receipts)

- `.venv\Scripts\python.exe tools\thought_quantizer.py --check` -> `THOUGHT-QUANTIZER: fresh, 3.3h old (v0.3)`.
- `.venv\Scripts\python.exe watch\inbox\burn_reset_20260927\flash50\_quant_measure.py` (written this ask, banked beside this file) -> full JSON distortion census, quoted below.
- Two probes on `memory/percolator/invariants.json` (collision dump, length histogram) via inline `.venv\Scripts\python.exe -c`.
- Read: tools/thought_quantizer.py (all 247 lines), memory/corpus/quantized_thought/compile_report.json, the three instructions_*.jsonl packs.
- NOT run: a recompile (would overwrite the fresh packs and re-rank by a new `now`; I measured the shipped packs instead), and no downstream model run. Every semantic-loss statement below is therefore a structural proxy, labeled as such.

## 1. Premise reconciliation: the ask's formula is not the code

The ask states the quantizer applies `q = clip(round(x/s) + z)`. That is the canonical uniform scalar quantizer (USC): granular error bounded by s/2, MSE s^2/12 for a uniform source, plus unbounded overload error where the clip saturates. tools/thought_quantizer.py contains no arithmetic quantizer. It contains a linguistic projection chain:

- classify(): regex two-pass keep/refuse (tools/thought_quantizer.py:57-79), deadband FRAGMENT_MIN_CHARS=25 (:52), telemetry rejection (:44-47);
- dedupe by 60-char normalized signature (signature(), :103-107);
- salience weight = recency x shape, SHAPE_W in {1.0, 0.8, 0.6, 0.4} (:99-100, :151-152);
- rank-select top-N per tier, N = 24/12/12 (:167-169, defaults :228-230);
- project to_flash = first sentence clipped at 220 chars (:110-113), to_local = first 10 words of flash (:116-118).

So the honest formalization is not USC. It is a nested prefix-projection quantizer with a rejection region, and the interesting discovery is that it accidentally implements all four classical weight-compression moves at once:

| weight-compression move | thought-quantizer analog | code |
|---|---|---|
| quantization (INT4/FP8 step) | sentence/word truncation, 220-char and 10-word caps | :110-118 |
| structured pruning (score-ranked) | weight = recency x shape, top-N selection | :151-152, :162 |
| weight sharing (hashing trick) | 60-char signature dedupe | :103-107, :136-141 |
| pruning-to-zero (deadband) | fragment + telemetry refusal | :57-79, :143-148 |

The `[tag]` strip in to_flash (line 111, `re.sub(r"(?i)^\[[^\]]+\]\s*", "")`) is the zero-point z analog: a systematic offset removed so the lattice aligns with content rather than metadata.

## 2. Formalizing the error: the prefix property makes distortion exact

For a USC the reconstruction error needs the geometry of R. Here the reconstruction is a string prefix, so the Levenshtein distance between source and codeword is EXACTLY the discarded suffix length: d(x, Q(x)) = |x| - |Q(x)|. No alignment, no squared term. The nesting (measured on the live packs, section 3) makes the three-tier chain a successive-refinement code in the sense of Equitz and Cover 1991 (IEEE Trans. Inf. Theory 37(2):269-275): coarse layers are prefixes of fine layers, so the frontier pack is sufficient to reconstruct flash and local bit-exactly, and each coarser tier is what remains after peeling refinement bits. Measured nesting holds perfectly today: 12/12 flash rows equal to_flash(frontier), 12/12 local rows are byte-prefixes of their flash rows (_quant_measure.py section C).

The total distortion budget decomposes into five channels, only two of which are "quantization" in the USC sense:

1. deadband (rejection): inputs quantize to silence. 11 of 331 inputs refused at compile time (9 fragments, 2 telemetry; compile_report.json). The v0.3 heal (error-quoting laws kept when imperative-shaped, :149-150) recovered 37 rows that v0.2 would have zeroed (compile_report.json `error_quoting_laws_kept`).
2. misread (false dedupe merge): UNBOUNDED error, the one channel with no USC analog. Two distinct laws mapping to one codeword means one is silently REPLACED, not coarsened. Measured live: 328 distinct signatures over 341 kept rows, 6 signatures merge >1 distinct text, max fan-in 6. The fan-in-6 signature is `path outside jail: c:\users\foste\documents\projects\research\cl4r1t4s\_...` and it collapses SIX distinct jail-escape paths (behavioral, evolution, safety, semantic, structure lenses plus _manifest) into one codeword. The quantizer cannot distinguish which lens escaped the jail. This is a safety-relevant misread, not a rounding error.
3. selection loss (pruning): rows ranked 13-24 of the frontier pack are absent from flash/local entirely: 1,236 chars, 56.2% of the frontier pack's 2,200-char mass.
4. granular truncation: flash keeps 81.9% of its own 12 rows' frontier mass (789/964 chars); local keeps 74.7% of flash (589/789).
5. overload: the 220-char clip binds on 3 of 352 source first-sentences (would fire if those rows ranked in); it fired 0 times in the current packs.

Dominance result: selection (56.2%) dwarfs truncation (18.2% then 25.3% of the remainder). The estate's real "quantization" is pruning; the caps are almost idle. That is the opposite of the INT4/FP8 regime where the step size does all the work.

## 3. Measured rates (the ask's "information loss rate")

Char-mass retention, current tree (all from _quant_measure.py, sections B and H):

| tier | rows | chars | chars/row | ASCII bits/row | retention vs frontier |
|---|---|---|---|---|---|
| frontier | 24 | 2,200 | 91.7 | 733.3 | 1.0 |
| flash | 12 | 789 | 65.8 | 526.0 | 35.9% |
| local | 12 | 589 | 49.1 | 392.7 | 26.8% |

- frontier -> flash: 64.1% char-mass loss (81.9% retained on the shared 12 rows, plus the 12-row selection cut).
- flash -> local: 25.3% loss.
- full chain: 73.2% char-mass loss.
- row-rate: 3.9% of kept rows (12/307) reach flash; 3.6% of the compile-time stream (12/331) reach local.
- pack bytes vs source bytes: 8,193 / 109,231 = 13.33x, but that ratio is dominated by decimation (352 rows -> 24), not per-row coding. Per-row coding ratios: 1.394x (frontier:flash), 1.868x (frontier:local). Caveat: file-byte accounting includes JSON scaffolding (the flash pack's bytes/row actually RISES because both fields are stored); char-mass is the signal metric.

Semantic honesty: none of these are information rates in Shannon's sense. True loss needs a behavioral oracle (does the downstream seat act differently), which I did not run. The closest structural proxies measured: verb survival under IMPERATIVE_RE is 12/12 at every tier today (the verb-drop channel exists structurally but fired 0 times in the current packs), while payload survival provably fails (section 5).

## 4. The quantizer before the quantizer (new finding)

The frontier tier is supposed to be the lossless fine layer of the refinement code. It is not, and the loss happens upstream of the tool. Measured on the live 352-row source:

- 160 rows are EXACTLY 105 chars, all 160 distinct texts, all ending in the clipped parenthetical `Trust bytes, not)` (the word "reports" and the closing of the sentence are gone). 66 more are exactly 103 chars, 27 exactly 81. So 253/352 (71.9%) of the stream sits at pinned lengths: a fixed-budget clip writer, a pure-overload quantizer with no granular region.
- 64/352 (18.2%) source texts lack any terminal punctuation (consistent with hard clipping).
- The flagship law `212719f4b54d06e9` ("Elevate with a deliberate ask: frozen prefix ... output contract (<=N words, shape") is itself 128 chars, cut mid-phrase: the law that ENCODES the deliberate-ask contract cannot state its own contract, at any tier.

Consequence for the theory: successive refinement is only as good as its base layer, and the base layer is corrupt. The flash/local tiers' measured losses (section 3) understate total loss because the fine layer already lost an unmeasured fraction upstream. This also pollutes the salience signal: SHAPE_W sees clipped texts, so the clipped boilerplate tail ("Trust bytes...") stamps a verb into 160 rows and flattens the shape distribution the ranking depends on.

## 5. Comparison to INT4 / FP8 / NF4 weight quantization

Verified anchors: NF4 is the 4-bit datatype whose 16 levels sit at quantiles of N(0,1), information-theoretically matched to normally distributed weights (Dettmers et al., QLoRA, arXiv:2305.14314, NeurIPS 2023, with double-quantized constants); FP8 ships as E4M3/E5M2 (2022 industry spec) at 2x vs FP16, training-grade; INT4 uniform (GPTQ-era) is literally `clip(round(x/s)+z)` per group at 4x.

| regime | rate vs full precision | error model | calibrated to source? | worst failure |
|---|---|---|---|---|
| FP8 E4M3/E5M2 | 2x | float exponent shift, bounded relative | yes (per-tensor scales) | graceful |
| INT4 uniform | 4x | granular <= s/2 + overload | yes (group scales, Hessian-aware ordering in GPTQ) | outlier channels |
| NF4 | 4x | quantile-matched, zero-mean optimal | yes (normal quantiles) | graceful |
| thought_quantizer flash | 1.39x per-row | exact suffix loss + misread merges | NO (fixed 220, unexamined) | silent law replacement |
| thought_quantizer local | 1.87x per-row | exact suffix loss | NO (fixed 10 words) | payload death (below) |
| thought_quantizer full stack | 13.33x vs stream | dominated by selection | ranking IS the calibration | 97% of laws unreachable |

Four structural differences worth stating:

1. Calibration. Every weight quantizer fits its codebook to the source distribution (GPTQ's Hessian, AWQ's activation stats, NF4's Gaussian quantiles). The thought quantizer's constants (25, 220, 60, 10) are folklore: measured, 220 binds on 3/352 first-sentences while the 60-char signature ALREADY misreads (fan-in 6) and 10 words destroys payload. The step sizes are misallocated exactly where NF4 says to look: fit the codebook to the empirical distribution.
2. Error metric. Weights are judged by MSE/layer drift; instructions must be judged by behavioral fidelity: does the consuming seat's policy change? That is rate-distortion with a fidelity criterion defined on downstream action, not on text. The tool measures neither: its only gate is staleness (check(), :200-217), never error.
3. Boundedness. USC granular error is bounded by s/2. The dedupe misread is unbounded: six distinct jail-escape incidents become one. Weight sharing in the hashing-trick literature (HashedNets, Chen et al. 2015) accepts collision noise because weights average; laws do not average, they overwrite.
4. Source distribution. Weights are Gaussian-ish and i.i.d.; instructions are discrete, Zipfian, and long-range dependent. The measured order-0 char entropy of the frontier corpus is 4.639 bits/char (2223 chars; English prose order-0 is typically ~4.1-4.3, the excess is the symbol/path density of laws), and word unigram entropy 5.356 bits/word over only 344 tokens (severely sample-underestimated; both numbers are order-of-magnitude instruments, not estimates of true entropy). The top-10 words carry 52.3% of mass; "verify", "bytes", "trust", "declaring", "done" dominate. Law-space is low-entropy and verb-centric, which is precisely why 10-word truncation preserves the verb but not the payload.

## 6. Is there a theoretical minimum bit-depth for instruction preservation?

The question dissolves into two regimes:

(a) Reconstruction regime (shared codebook). If the decoder can expand class labels back into full laws, the minimum rate is the entropy of behavioral equivalence classes. Measured crude floor with the tool's own verb lexicon plus polarity: 6 distinct classes among the 24 frontier laws (2.585 bits/law), 20 among 341 kept (4.322 bits/law). Two caveats, both directions: the proxy undercounts variety (it ignores objects and parameters) and the upstream clip overcounts similarity (the "Trust bytes" tail stamps one class onto the 160-row clip family). Treat 2.6-4.3 bits/law as an order-of-magnitude floor for class-level variety. At that floor the entire local pack is ~50 bits; its ASCII form is 4,712 bits. Headroom ~90x.

(b) Character regime (no codebook). Shannon 1951 ("Prediction and Entropy of Printed English", Bell Syst. Tech. J. 30:50-65) bounds printed English at 0.6-1.3 bits/char via human prediction. The mean local law (49.1 chars) then has a floor of ~30-64 bits versus 392.7 ASCII bits: ~6x headroom even at zero behavioral distortion, IF the decoder carries the language prior. And it does: the tiers are consumed by models (frontier specialist, flash worker, local gemma janitor), so the CODEC IS THE MODEL. The tier ladder is really a joint source-channel design where each tier's decoder is a different model prior; the local tier is not "10 words of the law", it is "10 words plus gemma's prior over which law this is". That is a Wyner-Ziv-style side-information problem in structure: coarse tiers decode against a shared statute book (the model's trained prior plus the seat's other context), and compression fails ungracefully exactly when two laws are near-colliding under that prior, which the fan-in-6 merge demonstrates concretely.

So the answer: there is no universal minimum bit-depth. R_min = H(behavioral equivalence classes) with a shared codebook (measured order 2.6-4.3 bits/law here), or ~0.6-1.3 bits/char with a language-prior decoder. What IS universal is the phase transition: measured, instruction SHAPE (the verb) survives the 10-word cut 12/12 today, while instruction PAYLOAD provably dies there (row 1's local tier "Elevate with a deliberate ask: frozen prefix (cache-shared) + tight" carries zero of the 207-char contract, the output-constraint, or the shape clause). The local tier sits just above the shape cliff and far below the payload floor. Any theory of instruction quantization must be a two-fidelity theory: bits for the act, bits for the argument. INT4/NF4 have no such split because weights have no syntax.

## 7. The ask's four questions, answered

1. Quantization error: exact suffix loss under prefix projection (not s^2/12), decomposed into deadband (3.3%), misread merges (6 signatures, max fan-in 6, safety-relevant), selection (56.2% of frontier mass), granular truncation (18.2% then 25.3%), overload (3/352 latent), plus an unmeasured upstream clip (71.9% of the stream pinned at 81/103/105 chars).
2. Information loss rate frontier -> flash -> local: 64.1% / 25.3% char-mass per hop, 73.2% cumulative; 96.4% of the source stream never reaches any pack; structural verb survival 12/12 today, payload survival already failed at row 1. These are structural proxies; true semantic loss requires a behavioral oracle not run this ask.
3. Vs INT4/FP8/NF4: per-row coding (1.39x/1.87x) is weaker than FP8's 2x; the real compression (13.33x) is pruning-shaped, not quantization-shaped; uncalibrated constants; unbounded misread failures; and the estate ladder is a successive-refinement code with a corrupt base layer.
4. Minimum bit-depth: none universal; class-entropy floor measured at 2.6-4.3 bits/law with a shared codebook, 0.6-1.3 bits/char with a model-prior decoder, against 392.7 ASCII bits/law actually shipped, with a measured shape/payload phase transition at the 10-word cut.

## 8. Owed, falsifiable next steps

1. Fix the misread before tuning the caps: dedupe key on the full normalized text (cost: nothing; the sig is a key, not a payload). Falsifier: after the fix, live census shows 0 signatures with fan-in >1.
2. Calibrate FLASH_MAX_CHARS and LOCAL_MAX_WORDS against measured distortion: bind 220 to the kept stream's first-sentence length distribution, and gate the 10-word cut on a payload-survival probe (numbers, paths, thresholds present in flash but absent in local). Falsifier: a compile report that records the probe and a cap choice derived from it.
3. Repair the base layer: percolator rows carry clipped texts with no truncation flag; add one (or raise the budget) so successive refinement has a genuine fine layer. Falsifier: 0 source rows at pinned lengths, terminal punctuation census recovers.
4. Compile-time distortion gauge in compile_report.json (verb survival, payload survival, collision count), so check() gates error as well as staleness; weight quantizers report perplexity deltas, the thought quantizer currently reports only its age.
5. Extend the class census beyond (verb, polarity) with extracted arguments (file paths, numbers) to tighten the R_min floor estimate; current proxy is order-of-magnitude only.

## Sources (verified this session)

- [Shannon 1951, Prediction and Entropy of Printed English](https://essrl.wustl.edu) (Bell Syst. Tech. J. 30:50-65; 0.6-1.3 bits/letter)
- [QLoRA / NF4, Dettmers et al. 2023, arXiv:2305.14314](https://arxiv.org/abs/2305.14314) · [NeurIPS 2023 poster](https://neurips.cc/virtual/2023/poster/71815) · [NF4 explainer](https://zeroentropy.dev/concepts/nf4)
- [Equitz and Cover 1991, Successive Refinement of Information, IEEE Trans. Inf. Theory 37(2):269-275](https://isl.stanford.edu/~cover/papers/transIT/0269equi.pdf) · [ACM DL record](https://dl.acm.org/doi/abs/10.1109/18.75242)
- FP8 E4M3/E5M2: 2022 industry format spec (NVIDIA/Arm/Intel), per [comparison coverage](https://www.researchgate.net/)
- Estate: tools/thought_quantizer.py; memory/corpus/quantized_thought/{compile_report.json,instructions_frontier.jsonl,instructions_flash.jsonl,instructions_local.jsonl}; memory/percolator/invariants.json; instrument watch/inbox/burn_reset_20260927/flash50/_quant_measure.py
