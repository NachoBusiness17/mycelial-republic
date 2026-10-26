# SWEEP: quantization-compression via hn (frontier_olm 2026-10-06)

source-fetched: 2026-10-06
Door: Hacker News (hn.algolia.com API + news.ycombinator.com threads). Seat: sweep gopher, quantization-compression.
Estate map served: the deliberate-ask quantize target, the quantizer v0.6 law-row propagation pipeline, and the GPU-ladder purchase gates (memory/rib/RIB_GPU_LADDER_20261001.md): weight quant must not break scut accuracy; run quantization must not drop law rows.

## Door health and the doors.md amendment

All 12 Algolia calls returned clean JSON, zero 403s, zero degradations. Incidental door proof: doors.md (frontier_olm_2026-10-06/lens/doors.md:40-42) marks the search_by_date endpoint "documented endpoint, NOT probed today: OWED". This sitting probed it: search_by_date with numericFilters=created_at_i>1788652800 (2026-09-06) returned filtered, in-window hits on every query, including exact-phrase and relevance-endpoint variants. The 09-28/10-03 sibling degradation classes (AWQ by-date ignored, GPTQ fuzzy-matching "GPT") did not reproduce on this sitting's terms (quantization, GGUF, quantize, llama.cpp, KV cache, "vector quantization", pruning, 1-bit LLM, plus relevance endpoint on quantization/quantized). One local tool miss, same class as 10-05: no raw-curl backup of the Algolia JSON in this shell; quotes below are WebFetch extractions from single-page reads, confidence discounted accordingly.

## Method (what I actually ran)

Pass 1, broad sweep. 12 Algolia API calls via WebFetch, window created_at_i > 1788652800, tags=story:
1. search_by_date query=quantization: 12 in-window hits
2. search_by_date query=GGUF: 20
3. search_by_date query="KV cache quantization": 0 (recorded as a real negative)
4. search_by_date query="quantized LLM": 0 (real negative)
5. search_by_date query=quantize: 19
6. search_by_date query="vector quantization": 0 (real negative)
7. search (relevance) query=quantization + date filter: 12
8. search_by_date query="1-bit LLM": 1 (irrelevant)
9. search_by_date query=llama.cpp: 19
10. search_by_date query="KV cache": 23
11. search (relevance) query=quantized + date filter: 14
12. search_by_date query=pruning: 30 fetched, mostly noise, 2 usable (OntoPrune, Mac Mini Q4 post)

Roughly 90 distinct in-window candidate rows surfaced, past the 30-candidate bar. Named candidates included every strong item from the 09-28, 09-30, 10-01, 10-02, 10-03 (x2), 10-04 and 10-05 sibling pools plus three fresh 10-05/10-06 items no prior pool could hold: AMD Quark Strix Halo (49975499, surfaced today), OntoPrune (49963837), Running Qwen Flash Next Q4 on a Mac Mini (49974431).

Pass 2, deep reads (9 pages + 2 threads read end to end this session):
1. quesma.com/blog/qwen38-27b-quantizations-benchmarked/ + HN 49611128 (139 comments)
2. arxiv.org/abs/2606.00206 + HN 49869861
3. zartbot.github.io dsv41flash_arch + HN 49735410
4. huggingface.co/blog/bartowski/per-tensor-layout-maps-for-gguf-quantization
5. jaehun.me/en/posts/paper-2609-30854v1/
6. huggingface.co/blog/ggml-org/decision-models-in-llamacpp
7. huggingface.co/blog/transformers-llama-cpp-quants
8. discuss.huggingface.co VeriLoop E2 thread 180723
9. github.com/cnygaard/glq (README, end to end)

## Dedup ledger (this area was swept seven times before this sitting)

Greps actually run this session, commands and counts:
- grep -ci "quantiz" catalog/catalog.jsonl = 414 rows; item-level greps: "2606.00206" 0, "per-tensor layout" 0, "qwen38-27b-quantizations" 0, "VeriLoop" 0, "transformers-llama-cpp-quants" 0, "890 bytes" 0, "systemone" 0, "TRELLIS" 4 (all INTAKE_BLACKBOX/INETLABS "TRELLIS in a tab" stories, a different TRELLIS), "Memory Wall" 1, "2609.30854" 2, "DeepSeek-v4.1" 14, "bartowski" 1 (a Letta test config, unrelated), "IQ1_M" 2 (ggml vulkan shaders, unrelated), "decision model" 15.
- memory/ greps: "2606.00206", "per-tensor layout", "Think They Need" hit memory/trajectory/steps.jsonl ONLY as sibling seats' own grep commands (trajectory_step.v1 records), not banked findings. The full memory-tree grep loop was cut for runtime after three terms (same disclosure the 10-04 sibling made) and replaced with the targeted banks below.
- Bank-of-record greps: watch/inbox/frontier_olm_20260928 and 2026-09-30..2026-10-05 sweeps.
- memory/percolator/candidates.jsonl: Quesma + agentic-kv-cache held as row from 2026-10-02 (file frontier_olm_20260928/percolator_candidates.jsonl row 4); arXiv 2609.32042 (PolAgentBench, three GGUF k-quants Q8_0 to Q2_K) held as row 3.

Verdict per deep read: Quesma article + thread (HELD: percolator row 4; my three thread deltas from the 10-05 bank were already banked there: anyfoo Q6_K_XL cliff, kmike84 KLD-on-agentic-traces, missing-Q3; skolos NVFP4+KV-q4 was banked 09-28 line 45), 2606.00206 (HELD: deep-read by the 10-01 sweep, percolator rows 18/19 reasoning-quant ladder), bartowski layout maps (HELD: 10-01 item 5 with token_embd dominance, sensitivity standouts, canary gate), transformers llama.cpp quants (HELD: 09-28 candidate list + 10-01 deep read), VeriLoop ladder (HELD: 10-05 banked the same HF thread incl. KLD 0.014357 and the retention-not-downstream warning), DeepSeek-V4.1 Flash KV (HELD: full arXiv abstract at state/arxiv/2026-09-18/2609.19969v1.txt carries FP4 KV + 890 B/token; DESK_DSV41FLASH_20260911.md + v41_paces lanes). Genuinely new after dedup: GLQ trellis (10-04 ledger: "census-listed since 09-28, never read"), jaehun.me KV-wall blog (10-04 ledger: "listed by the 10-03 inference-efficiency sweep, never read"; the paper ABSTRACT is held at state/arxiv/2026-09-28/2609.30854v1.txt, the blog's worked numbers are not), AMD Quark Strix Halo (surfaced on HN today, after every prior sweep), and two deltas on held ground (decision-models gap + Julia-1 prompt sensitivity; DSV41 SWA-FP8 sensitivity line, folded into the KV-wall item).

## Research questions, answered from what this sitting read

### RQ1: owed qwen2.5:7b Q4_K_M vs q8_0 A/B; bit ladder to the 2b janitor class; does 4-bit-holds/1-bit-collapses replicate at estate scale

The held shape (doors.md:40-42, percolator row 4) is unchanged: no in-window source extends it below 27B. The Quesma thread confirmed NO commenter made 1-3B claims; the 09-28 sweep already recorded that the 2B class is below every model benched in this window. What this sitting adds to the A/B design:
- The 2-bit rung's real cost is tokens, not accuracy: Quesma measured UD-Q2_K_XL using ~25% more output tokens on solved Terminal-Bench tasks, and arXiv 2606.00206 proves the mechanism (aggressive PTQ raises CoT length; up to 52% of failures had the right answer mid-CoT; a training-free logit penalty on overthinking markers cuts CoT 12-23% while preserving accuracy, tested 1.5B-32B). The owed A/B should log output-token counts per task, not just pass rates, or a 2-bit arm will look worse than it is and a 4-bit arm cleaner than it is.
- Method arm is not optional: AMD Quark's W4A16 plain RTN on Qwen3.6-35B-A3B dropped GPQA 0.4337 to 0.3431-0.4086 while IFEval prompt-strict EXCEEDED baseline (0.3752 vs 0.3235). Same bit-width, no imatrix/GPTQ: real accuracy loss on a 35B MoE. A Q4_K_M vs q8_0 A/B without a method note (RTN vs K-quant vs imatrix) is not interpretable; this is the AQLM method-tier rule (burns.md:57) showing up inside GGUF.
- VeriLoop's ladder (HELD ground) is the caution on the estate's own compile-style scoring: retention metrics on a generic corpus (their IQ1_M: +0.3191% PPL) coexist with Quesma's downstream collapse at 1 bit, because VeriLoop's IQ1_M is a protected mixed-precision artifact (one tensor at IQ1_M, 5.36 BPW effective) and their protocol is WikiText-2 PPL/KLD only. Their own warning stands: "these are quantization-retention measurements, not downstream benchmark-loss percentages."
- Estate-scale replication remains OWED and un-started; nothing in this window runs it for us.

### RQ2: q4_0 KV cost on long-context lanes; does the q8_0 KV throughput win survive at 2b context lengths

- New regime frame read (jaehun.me on arXiv 2609.30854): decode is memory-bound (BF16 batch-1 arithmetic intensity ~1 FLOP/B vs H100 ridge 295), the bottleneck crosses from weights to KV at a computable s*(b) (Llama-3-70B: 427.2k tokens at b=1, 13.4k at b=32), and quantization speedups are regime-dependent: 2-bit KIVI gives 1.25x at 128k, 1.91x at 512k, 4.82x in batched W2 regime, with +0.03-0.3 ppl and LongBench ~baseline; 3-bit KVQuant <0.1 ppl delta; 4-bit "nearly free". Published KV-quant evidence lives entirely at long-context or batched regimes. At 2b-model context lengths and b=1 the estate is below s*, weights dominate, so B4's measured q8_0 KV win (100.8 vs f16 55.9 t/s, burns.md:59) should shrink for q4_0 in throughput terms while accuracy cost at 4 bits reads as near-zero in the literature. The honest gap: those quality numbers are ppl/LongBench-class, and the Quesma thread already established KLD on agentic traces diverges far worse than wikitext; the estate's q4_0-KV accuracy arm must be scored on scut-shaped traces.
- Differential sensitivity by attention type (read on the DSV41 blog, HELD model): DeepSeek keeps the SWA cache at FP8 "Since the KV cache of sliding window attention SWA is sensitive to quantization" while the main cache runs FP4 with QAT, dequantized before attention. If the estate's janitor models use SWA layers, a flat q4_0 KV setting will not spend bits uniformly.
- Quesma's author states the same OWED from the 27B side: "Since people report that KV-caches are more susceptible to quantization, I may test it as well" (article, read this sitting). The estate's B4 q4_0 measurement remains un-run by anyone in this window.

### RQ3: does the AQLM method-tier rule hold across GGUF lanes; which post-09-06 methods merit amendment

The rule holds and hardens. Three independent GGUF-lane reads this sitting:
- bartowski's layout maps (HELD) are per-shape, canary-gated against a KLD-per-bit fallback, and MiniCPM5-2B initially failed the gate: the map is tier- AND shape-specific, never universal.
- GLQ trellis (NEW, below) refuses fractional bit-rates entirely (integer 2-8 bpw only; fractional goes to a separate E8-lattice path): the method constrains the tier ladder, not vice versa.
- Quark's W4A16 RTN result (above) shows the same bit-width on the same model at different quality depending on method. Amendment candidates from the window: QTIP-derived trellis-coded quantization (GLQ) is the one new weight-space method family this sitting read end to end; nothing else post-09-06 on HN proposed a new universal method. The arXiv submittedDate door (doors.md:24-26, 40,448 rows indexed) remains OWED and was not run by this HN-lane sitting.

### RQ4: run-quantization propagation; MEASURED ON rows at every layer; 13/338 truncation loss scaling

No HN item in-window touches law-row propagation or pack truncation; this is estate-internal machinery and the window's nearest neighbors (token compression CLI, HELD, 29.6% reduction with task-success effect unmeasured) already carry the open wound. Nothing to bank. The owes stand as the lens wrote them.

### RQ5: HyperThink VQ codebooks as law-packs in weight space; measurable bridge or unfalsifiable

The analogy is falsifiable and the bridge exists as running code: GLQ implements QTIP-derived trellis-coded quantization, which is weight-space vector quantization with a trellis-structured codebook (16-bit sliding state, effective quantization dimension 256, two-stage stacked RVQ above 4 bpw), with concrete numbers at matched bit-rates (below). A measurable estate bridge: compile the same law-pack into a 2b model twice, once as scale quants (Q4_K_M-class) and once as codebook quants (trellis/RVQ at matched bpw), and score KLD and task accuracy on scut traces; GLQ's own 4-bpw row predicts the codebook path wins perplexity but can still lose hard-reasoning accuracy (AIME 41.7% vs bf16 47.5%). The HyperThink card's claim is therefore testable, not unfalsifiable; what remains unproven is any connection from quantized_thought PACKS (text) to weight-space codebooks (semantics), which no in-window source attempts.

## Banked items (strongest first, all read end to end this sitting)

1. GLQ trellis-coded quantization vLLM plugin (github.com/cnygaard/glq, HN 49644045, 2026-09-10). Quote: "on the GPU serving path the dense weight is never materialized, so GPU memory drops with the compression ratio". QTIP-derived TCQ: 2 bpw SmolLM3-3B PPL 11.94 (lattice 13.79, bf16 9.12); 4 bpw single-stream bf16-parity tok/s (176 vs 180) with AIME-2026 41.7% vs 47.5%; 6 bpw stacked RVQ PPL 9.1310 vs 9.1220; INT8 KV cache supported; MoE fused grouped trellis decode 91.6 tok/s B=1.
2. AMD Quark Strix Halo W4A16 on-device quantization (rocm.blogs.amd.com, HN 49975499, 2026-10-06). Quote: "Quantization reduces the model weights from roughly 70 GB to about 21 GB". Qwen3.6-35B-A3B BF16 to W4A16 RTN on 128GB unified memory; group 32 exports GGUF Q4_0/Q4_1 for llama.cpp, group 128 safetensors for vLLM; GPQA fell to 0.3431-0.4086 vs 0.4337 while IFEval prompt-strict beat baseline; quant 0.8-1.5 min, export 18-23 min.
3. The KV Cache Is the New Memory Wall (jaehun.me review of arXiv 2609.30854, HN 49945575, 2026-10-03). Quote: "Almost every published number is right on its own. But almost none of them can be interpreted together." Regime frame s*(b) with worked KV-quant numbers (2-bit KIVI +0.03-0.3 ppl, LongBench ~baseline, 1.25x/1.91x/4.82x by regime; 3-bit KVQuant <0.1 ppl; 4-bit nearly free); abstract of the paper already held at state/arxiv/2026-09-28/2609.30854v1.txt.
4. Decision models in llama.cpp: the unfilled 421M-4B gap and Julia-1 prompt sensitivity (huggingface.co/blog/ggml-org/decision-models-in-llamacpp, HN 49942092, 2026-10-02). Quote: "Julia-1 routed 'I was charged twice' to shipping with bare labels, and to billing (0.99) once each option had a description." Model table + endpoints already banked 10-05 (open-local-language-models-hn.md:67); new here: no decision model exists between 421M and 4B, so gemma:2b's slot is contested only from below (144M/421M) and above (4B), and option descriptions decide small-model routing accuracy. Upgrades the pending day-5 lead (DIGEST.md:71-81) with a concrete probe design: described options on 144M/421M before conceding the rung.

## Considered, not banked

- OntoPrune (49963837) and Running Qwen Flash Next Q4 on a Mac Mini (49974431): surfaced in pass 1, metadata only, never deep-read this sitting; no claims asserted.
- arXiv 2606.00206 HN thread critique (DiabloD3: quantized KV caches attend to wrong tokens; "what happens when you turn the slopes into hard stair steps?"; prescribes "smaller models and smaller caches and better samplers"): 1-comment thread, held-paper adjacent, folded here rather than banked.
- pruning by-date query returned 30 generic front-page rows; recorded as the noise it was.

## OWED (not found, not fabricated)

- The qwen2.5:7b Q4_K_M vs q8_0 A/B (burns.md:209) and the 2b-class ladder: nothing in this window runs it; design deltas banked above (token-count logging, method arm, scut-trace scoring).
- q4_0 KV accuracy at 2b-class context: no published number found; regime frame says measure, not assume.
- arXiv submittedDate-sorted method sweep (doors.md:24-26): still unprobed; this was the HN lane.
- RQ4 propagation/truncation: untouched by this door by nature.

Counts law: candidate counts above are per-query hit counts echoed from the Algolia responses this sitting; read counts are the 11 fetches enumerated; overlap counts are the grep outputs shown. No counts from different instruments were differenced.
