# Frontier sweep: quantization-compression via arXiv, 2026-10-08

source-fetched: 2026-10-08
instrument: WebFetch against export.arxiv.org/api/query (minimal shape) + arxiv.org/abs and /html pages; one WebSearch for the GPU-ladder price check; grep-based dedupe against catalog/catalog.jsonl, memory/, and state/arxiv.
ask: five research questions from the 2026-10-08 lens (lens/burns.md:205-208 for the owed A/B, lens/burns.md:70-71 for the day-6 bit-ladder subject, lens/doors.md:20-39 for the arXiv door recipe, lens/laws.md:189-191 for the GPU-ladder triggers), anchored on the amended A/B spec watch/inbox/port_wave_20261007/QUANT_AB_SPEC_AMEND.md (read in full this sitting; the A/B itself remains UN-RUN, no run receipt found, matching lens/burns.md:205-208).

## Door status (honest)

- export.arxiv.org/api/query: WORKING today in the minimal shape the doors memo prescribed (lens/doors.md:20-39: plain `search_query=all:<term>`, no phrase quoting, no sortBy). I additionally used a `submittedDate:[YYYYMMDDHHMM+TO+YYYYMMDDHHMM]` range clause INSIDE search_query; that is not the sortBy param the memo found toxic, and it worked on every fetch today (probe returned totalResults 40507 unfiltered, 472 for the wide window, then the 30-day window).
- arxiv.org/html/<id>v1 full-text reads: DEGRADED. Two of two attempts timed out at the 60s WebFetch limit (2609.28270v1 on first try, 2609.32042v1 twice). One retry of 2609.28270v1 with a lean prompt succeeded, so the HTML door is intermittent, not dead. Fallback used: arxiv.org/abs pages, which returned rich abstract-plus-metadata content for every item they served.
- No 403s anywhere today.

## Pass 1 census (broad sweep)

Four API fetches, all with the 30-day range clause [2026-09-08 .. 2026-10-08]:

1. `all:quantization AND cat:cs.CL`, max_results=30: 30 entries.
2. `all:quantization AND cat:cs.LG`, max_results=25: 25 entries.
3. `all:GGUF`, max_results=10: 8 entries.
4. `all:KV AND all:cache AND all:compression`, max_results=15: 15 entries.

Union after dedupe: roughly 67 unique candidates, comfortably over the 30-candidate bar. Full title lists were captured in the fetch outputs of this session; the strongest are named in the sections below and in the dedupe table.

## Pass 2 census (deep reads)

Six items read end to end, via abs page unless noted:

| arXiv id | Read depth | Note |
|---|---|---|
| 2610.06251 | abs page, rich | full numbers extracted (170/384 etc.) |
| 2609.28270 | abs page + FULL-TEXT html/v1 (retry) | the only true full-text read of the day |
| 2609.32042 | abs page, rich | html/v1 timed out twice; full text NOT read today; full text is already held estate-side anyway (see dedupe) |
| 2610.04403 | abs page, rich | already deeply mined by day-6, see dedupe |
| 2609.16085 | abs page, rich | genuinely new |
| 2609.14864 | abs page, rich | already banked 10-03, see dedupe |
| 2609.26823 | abs page, rich | genuinely new, read after dedupe pass |
| 2610.07522 | abs page, thin | page lacks models/numbers; weakest read of the day |

## Dedupe against estate holdings (grep receipts, all run this sitting)

Instrument: one python pass over catalog/catalog.jsonl (1,266,929 lines), memory/ (recursive), state/arxiv/ (recursive), 13 phrases; validated by the control phrase 2610.07781, which hit exactly where the estate says the day-7 banked paper lives (catalog/catalog.jsonl:1195121, memory/trajectory/steps.jsonl, per the spec's own citation QUANT_AB_SPEC_AMEND.md:26-31). Follow-up greps over watch/inbox, memory/percolator, memory/corpus, state/arxiv settled each candidate.

- 2610.06251 Shared Stopping: HELD. Full text pulled 2026-10-06 (state/arxiv/2026-10-06/2610.06251v1.txt, catalog row catalog/catalog.jsonl:1071145; digest row state/arxiv/2026-10-06/digest.jsonl:256, published 2026-10-05). Day-6 sweep banked it (frontier_olm_2026-10-06/sweep/quantization-compression-arxiv.md:33, :79) and day-7 sweep lists it "previously banked" (frontier_olm_2026-10-07/sweep/quantization-compression-arxiv.md:19).
- 2609.28270 Quantization Price: abstract HELD since 2026-09-24 (state/arxiv/2026-09-24/2609.28270v1.txt, catalog row catalog/catalog.jsonl:445531; digest row state/arxiv/2026-09-24/digest.jsonl:122). Today's full-text read adds what the held abstract lacks.
- 2609.32042 PolAgentBench: HELD. abs HTML pulled 2026-09-28 (watch/inbox/frontier_olm_20260928/sweep/_raw/abs_2609.32042.html, catalog rows catalog/catalog.jsonl:674053 and :1116734), percolator candidate 2026-10-02 UNPROMOTED (memory/percolator/candidates.jsonl:15), day-7 sweep carries its numbers (frontier_olm_2026-10-07/sweep/quantization-compression-arxiv.md:13). NOT re-banked.
- 2610.04403 Saying, Not Knowing: HELD and heavily mined. Day-6 card 1 with a refetch confirmation and a STRUCK claim component (frontier_olm_2026-10-06/DIGEST.md:92: the "gemma:2b sits inside the dissociation regime" extrapolation was struck because the paper evaluates Gemma-2-2B, not Gemma 1), day-7 sweep item (frontier_olm_2026-10-07/sweep/quantization-compression-arxiv.md:15). NOT re-banked. My independent abs read today reproduces the held numbers (27 artifacts, 13 families, sub-2B definitions 20-67% down, near-identical Q2 PPL penalties 44.7%/47.6% splitting 3.6% vs 43.6% definition loss; "Q4_K_M lexically clean at >=1B"; "Validation must be per artifact"), which corroborates the day-6 card rather than extending it.
- 2609.14864 GGUF-Metadata Throughput: BANKED 10-03 (watch/inbox/frontier_olm_2026-10-03/register.jsonl, percolator_candidates.jsonl, steal/quantization-and-compression.md all match; sweeps 09-30 through 10-07 carry it). My read today adds the RTX 5080 detail (36.1% per-host MAPE, 36.0% leave-one-host-out, active-parameter model beats total-parameter 49.4/55.3/51.9; "low-bit model ladder changes ordering across runtime stacks"; "GGUF structure helps on all three systems, but fitted efficiencies are not universal"). NOT re-banked as new; the runtime-stack-ordering sentence is the one byte worth carrying into the per-role-ladder question (RQ3).
- 2609.16085 Is INT8 Portable: ZERO footprint anywhere in watch/inbox, memory/, state/arxiv. GENUINELY NEW. Banked below as item 1.
- 2609.26823 Qwen2-Audio text scores: ZERO footprint. GENUINELY NEW. Banked as item 3.
- 2610.07522 Activation Denoising: ZERO footprint. GENUINELY NEW. Banked as item 5.
- Also verified HELD from my pass-1 pool (not re-banked): 2610.06174, 2609.36760, 2609.38169, 2609.39329, 2609.26333, 2609.37988, 2610.03027, 2610.06286, 2610.06479, 2609.30854 (day-7 sweep "previously banked" list, frontier_olm_2026-10-07/sweep/quantization-compression-arxiv.md:19); 2609.11687 (day-6 sweep :29); 2609.24799 (16 files), 2609.30820 (6 files), 2610.00983 (7 files), 2609.21450 (4 files), 2609.23585 (3 files), 2609.16391 and 2609.24322 (2 files each). Unheld pass-1 candidates left unbanked for depth reasons: 2610.05329 (0 files, weight-averaging-for-PTQ theory, background only), 2610.02462-family and the long tail of KV-cache titles.

## Banked items (strongest first)

### 1. arXiv 2609.16085, Is INT8 Portable? A Cross-Platform Measurement Study of Quantized Inference on Embedded and Automotive Accelerators (2026-09-14) - NEW

Verbatim from the abs page: "Quantize once, deploy anywhere" is unsafe for embedded and automotive deployment, where per-input determinism and redundancy matter.

Why it matters: this is direct, measured support for the amended A/B's EXPORT-CAST RIDER (QUANT_AB_SPEC_AMEND.md:81-84, from 2610.07853). Same ONNX artifact and scales, seven hardware classes: cores with ARM dotprod/x86 VNNI speed up by up to 2.1x while cores lacking it slow down by 1.7x on the identical model and runtime; INT8 predictions match FP32 1000/1000 only when the integer kernel matches, otherwise 958-965/1000; one NPU fails silently (accuracy 0.75 to 0.005 with external scales ignored). The rider's demand (hash the exact GGUF blob, pin the conversion toolchain) extends one step: pin the KERNEL/runtime side too, because the same artifact on a different backend is a different arm. On this estate that means the Q4_K_M vs q8_0 verdict is only valid for llama.cpp on the RX 5600 XT, and must be re-stamped if the serving stack moves.

Overlap: zero hits (grep over watch/inbox, memory/percolator, memory/corpus, state/arxiv returned nothing; catalog+memory+state 13-phrase pass returned only my own grep echo at memory/trajectory/steps.jsonl:71864).

Confidence: 0.85 (quote extracted verbatim by the fetcher from the abs page; numbers are abstract-level, model names not on the page).

### 2. arXiv 2610.06251, Shared Stopping Decisions Change Answers in HQQ Cache Quantization (published 2026-10-05) - HELD since 2026-10-06, but its lesson is UNWIRED into the amended A/B instrument

Verbatim from the abs page: Replacing only the question batched with the target changes four-bit HQQ answers in 170/384 test comparisons across two models.

Why it matters: the estate holds this paper (see dedupe) but the 10-07 spec amendment cites only 2610.07781 and 2610.07853 (QUANT_AB_SPEC_AMEND.md:26, :83); it never cites 2610.06251. The amendment's kept leg "pin-or-reset serving-cache state between arms" (QUANT_AB_SPEC_AMEND.md:59-61) does not name batch composition or the stopping/iteration budget. This paper's mechanism: a shared average error decides when quantization-parameter updates stop, so batch composition leaks into the target's answer; replaying another execution's update counts reproduces the changed pair in both directions; "Fixing the original iteration budget removes this decision path without tuning"; and "Request-independence audits must cover stopping decisions as well as quantization groups." Sharpening for the owed A/B before it fires: the pin-or-reset leg should explicitly pin or reset batch composition and iteration budget, and the run should record whether any lane ran concurrent generations against the same model instance, because natural rebatching changes answers. Caveat carried honestly: the paper's substrate is HQQ cache quantization on its stack, not GGUF weight k-quants via /api/generate; it transfers as an evaluation-law prior, not as a measured GGUF fact. The estate's falsifier 2 shape (QUANT_AB_SPEC_AMEND.md:109-110) already demotes channels that come in flat; this is the same discipline applied to serving state.

Overlap: HELD at state/arxiv/2026-10-06/2610.06251v1.txt + digest row :256 + day-6 sweep :33/:79 + day-7 sweep :19. The delta banked here is the wiring gap to the 10-07 amendment, not the paper.

Confidence: 0.9 (numbers cross-check against the estate's held abstract dump; both my fetch and the held digest agree).

### 3. arXiv 2609.26823, Text Scores Do Not Establish Performance on Lexically Non-Diagnostic Speech Tasks: A Qwen2-Audio Quantization Case Study (2026-09-20) - NEW

Verbatim from the abs page: This case study shows why translation scores and performance on tasks beyond the transcript need separate evaluation.

Why it matters: an independent, published replica of the four-pinned-choices logic on a different modality. Fixed mixed 4/8-bit Qwen2-Audio-7B-Instruct allocations at 6 and 7 average bits per parameter: BLEU/chrF differences vs FP16 have intervals including zero on both allocations, while the same allocations show -3.71% (6-bit) and -1.17% (7-bit) emotion-accuracy differences, the 6-bit speaker interval excluding zero at an exact sign-flip p=0.0148. One scoring channel reads "no damage," a second channel on the same artifacts reads "significant damage," and same-budget controls do not identify the best allocation. This is exactly the amendment's choice-1/choice-2 structure (matched-task deltas swing and the full-pipeline pooled verdict as the only promotion number), arrived at independently, and it supports banking the strict-parse and thinking channels as separate riders rather than merging them (QUANT_AB_SPEC_AMEND.md:73-77, 85-90).

Overlap: zero footprint (id grep across watch/inbox, memory/percolator, memory/corpus, state/arxiv: 0 files).

Confidence: 0.85 (abstract-level read; the fetcher marked the abstract verbatim in segments).

### 4. arXiv 2609.28270, Predicting Quantization Price for Selecting PTQ Configurations Before Deployment (2026-09-23) - abstract HELD since 09-24; full-text numbers are today's addition

Verbatim from the full text (html/v1, retry succeeded): The resulting selector is most credible in the local, moment-stable, curvature-aligned regime tested by the evidence, and the same scope conditions identify where extending the price language beyond weight-space PTQ requires additional modeling.

Why it matters for RQ3 (per-role quant ladder): the paper sells a calibration-time price table and a budgeted price-guided selector, so a ladder could in principle be pre-ranked without running tasks. The full text tempers that hard: the reported correlations (rho 0.9470/0.9249 realized, 0.9483/0.9438 trace) are price vs KL DRIFT on OPT-125M and Qwen3-0.6B, not vs task accuracy; selection experiments ride Llama-3.2-1B/3B and Llama-3.1-8B with a GPTQ backend; and the conclusion sentence itself is scope-limited. So for this estate it is at most a cheap pre-screen channel ahead of the task-graded A/B, never a substitute for it, and the promotion gate (QUANT_AB_SPEC_AMEND.md:92-100) stands. The day-6 law "grade the actual task per artifact, never perplexity" (frontier_olm_2026-10-06/DIGEST.md:13) survives this paper's challenge intact.

Overlap: abstract held at state/arxiv/2026-09-24/2609.28270v1.txt + digest row :122; not in any day-6/7 sweep bank list. New bytes: the correlation targets, model list, backend, and the scope-limited conclusion sentence.

Confidence: 0.85 (fetched twice, abs and full text, consistent).

### 5. arXiv 2610.07522, Activation Denoising: A Robustness View on Parallel vs Sequential LLM Quantization (2026-10-05) - NEW

Verbatim from the abs page: we propose parallel quantization with activation denoising, which recovers much of the sequential benefit while keeping quantization fully parallel.

Why it matters: method-side support for treating the quantization PROCEDURE as part of the artifact. Parallel and sequential pipelines quantizing the same base model at the same bit-width produce weights that compound error differently (errors compound through the residual stream in parallel quant; sequential re-calibrates on already-quantized predecessors), and the paper's fix applies a general linear transformation rather than a function-preserving rotation. For this estate: two Q4_K_M files of the same base model from different exporters are different arms, which is the export-cast rider's premise (QUANT_AB_SPEC_AMEND.md:81-84) and a reason the per-role ladder (RQ3) must pin one exporter per ladder rung. Weakest read of the day: the abs page names no models or numbers, so this bank is claim-level only.

Overlap: zero footprint (id grep: 0 files).

Confidence: 0.7 (abs-page only; model/benchmark details unverified this sitting).

## RQ4 (GPU-ladder price trigger), light check, NOT deep market research

One WebSearch pass this sitting ("used H100 price 2026 RTX 5090 32GB Blackwell GPU price October 2026"). Reported October 2026 numbers: used non-refurbished H100 ~$15,000-28,000 (sources: compute.exchange/blogs/h100-gpu-price-2026, gpunex.com, mercatus-ai.com), RTX 5090 32GB ~$3,822 used / $4,999 new at B&H (bestvaluegpu.com/history/new-and-used-rtx-5090-price-history-and-specs). Against the rib's triggers (24GB+ Blackwell under ~$1200 or used H100 under ~$4000, lens/laws.md:189-191, RIB_GPU_LADDER_20261001.md:14-23): NEITHER trigger fires. Quant-versus-card economics do not flip for the AMD box; the quant A/B queue stays the cheap front. Caveat: aggregator-level numbers from one search pass, not verified on vendor listings; treat as a no-trigger reading with wide error bars, not a price receipt.

## What was NOT done

- The qwen2.5:7b Q4_K_M vs q8_0 A/B was NOT run (owed, lens/burns.md:205-208; this seat's charter is the sweep, firing belongs to the burns ledger per QUANT_AB_SPEC_AMEND.md:3-5).
- 2609.32042 and 2610.07522 full texts NOT read today (HTML timeouts; 32042's full text is already estate-held at frontier_olm_20260928/sweep/_raw/).
- No register rows written and no lane quant changed; per the estate map this sweep feeds the queue, the register/burn receipt is the parent's move.
