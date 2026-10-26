# SWEEP: quantization-compression via x (2026-10-10)

source-fetched: 2026-10-10

Area: quantization-compression. Seat: sweep-quantization-compression-x (day-10 of the
frontier_olm daily). Window: 2026-09-10 .. 2026-10-10. Estate ground read this sitting:
quant_ab/RECEIPT.md + SUMMARY facts via frontier_olm_2026-10-08/sweep/quant_ab/RECEIPT.md
(read in full, TIE AT CEILING, Q4 6.90 vs Q8 3.00 tok/s), memory/rib/RIB_GPU_LADDER_20261001.md
(read in full, five gates), frontier_olm_2026-10-09/lens/burns.md (full), day-9 and day-8
quantization-compression-x sweeps (full), day-9 quantization-compression-arxiv/-reddit
(targeted rg reads), today's lens/laws.md q12 row.

## Doors, honestly

- WebSearch `site:x.com`: DEGRADED HARD. Four strict site: queries plus five x.com-shaped
  retries returned ZERO x.com status URLs (the backend falls back to general web; repeated
  MCP 1302 rate-limit bursts inside single calls, same class day-8/9 recorded). The one
  in-window X find (bnjmn_marie, ~2026-10-03, "lossless quantization ... 3.3 bits per
  parameter", x.com profile snippet surfaced by search) is SNIPPET-BANKED with its profile
  URL per the recipe fallback; no status ID was discoverable, so its body was never fetched.
- fxtwitter: PER-STATUS DOOR VERIFIED ALIVE. One call made:
  api.fxtwitter.com/bnjmn_marie/status/2105481856812740726 resolved HTTP 200 (author +
  Oct 1 date + first 25 words confirmed as the day-8-banked ladder post; resolved as a
  door health check only, NOT re-banked). The user endpoint (api.fxtwitter.com/unslothai)
  works but returns NO timeline (profile fields only), confirming day-9's negative row.
  Zero NEW status IDs surfaced by search today, so the per-status door had nothing new
  to resolve.
- arXiv export API: WORKS over https ONLY this morning; plain http now 301-redirects to
  zero bytes (door-law update for lens/doors.md: add -L/https). Date-window query
  `all:quantization AND submittedDate:[202609100000 TO 202610102359]` returned 40 entries
  (receipt: sweep/_fx_arxiv_quant_window.xml). id_list batch for five deep reads:
  _fx_arxiv_idlist_deepread.xml. Title query: _fx_arxiv_statlossless.xml.
- GitHub doors: WebFetch on ggml-org/llama.cpp discussion 20969 (index + thread), gh api
  REST for its comment pages (created_at stamps + bodies), WebFetch on buun-llama-cpp and
  devYRPauli/turboquant-m1pro-evaluation README/FINDINGS. All HTTP 200.
- Unsloth docs: two redirect hops then one 60 s timeout, clean on retry (receipt: page
  unsloth.ai/docs/models/gemma-4/qat.md).

## Pass 1: candidate census (58+ considered)

arXiv 40-entry window listing (all titles + dates read from _fx_arxiv_quant_window.xml):
LLM-quant relevant = 2609.16085 (INT8 portable), 2609.11716 (why PTQ works), 2609.21834
(QAT endpoint descent / QAR), 2610.07522 (activation denoising), 2609.24322 (undetected
retrieval damage), 2610.00382 (quant vs inversion attacks), 2610.00983 (held day-8),
2610.11315 (W4A4 diffusion), 2609.33601 (JustQuant), 2609.38121 (WUSH-KV), 2610.08231
(OSFP4/NVFP4), 2609.25492 (RGSQ), 2610.06174 (held day-8), 2609.11582 (OmniKVQuant),
2609.30820 (looped transformers), 2609.14060 (AGENTQ backdoors), 2609.34867 (P4Q),
2610.05265 (Loopy), 2609.19880 (D-Quant), 2609.38166 (LeapQuant), 2609.35800 (HeadGuard),
2609.18131 (Colla-Q MoE), 2610.03218 (VisionMX), 2610.12444 (4-bit AdamW state),
2609.21450 (activation-guided compensation). Off-window arXiv surfaced by search: 2605.02404
(statistically-lossless, May 4 v2 Aug 9), 2505.23786 Mind the Gap GGUF attack (May 2025),
ZeroQAT (Aug 2025), "Token Inflation as a Hidden Cost of Low-Bit Reasoning" (Jun 2026),
"Which Quantization Should I Use? A Unified Evaluation" (Jan 2026). GitHub/web: TurboQuant
discussion 20969 + its fork ecosystem (TheTom turboquant_plus, Madreag turbo3-cuda,
spiritbuun buun-llama-cpp ~10-08, devYRPauli eval 10-05), NVIDIA DGX Spark forum thread
"Why TurboQuant saves DGX twice", Gemma 4 QAT Google blog (Jun 5, per search + day-9),
Unsloth QAT docs, HF google/gemma-4-12B-it-qat-q4_0, lmcache-src serde docs (estate-held).
X-surfaced: bnjmn_marie ~10-03 lossless post (snippet, unresolvable), datageek_ai /
vibhavagarwal5 TurboQuant posts (held day-9 degraded, not re-banked).

## Pass 2: deep reads (fetched and read this sitting)

1. llama.cpp discussion 20969 "TurboQuant - Extreme KV Cache Quantization" (WebFetch of
   thread + gh api comment pages: 100-comment pages 1..6 walked for stamps).
2. devYRPauli/turboquant-m1pro-evaluation FINDINGS.md (WebFetch, full extraction incl.
   the "Reproduction on 2026-10-05" section) + its Oct 5 discussion comment (gh api body).
3. spiritbuun/buun-llama-cpp README (WebFetch).
4. unsloth.ai/docs/models/gemma-4/qat.md (WebFetch; memory table, KLD table, Windows).
5. arXiv id_list batch: 2609.24322, 2609.16085, 2609.33601, 2609.21834, 2610.08231
   (abstracts read from _fx_arxiv_idlist_deepread.xml).
6. arXiv title query: 2605.02404 (abstract read from _fx_arxiv_statlossless.xml).

## Answers to the four research questions

- RQ1 (schemes postdating the A/B that claim to break the Q4/Q8 tie with reproducible
  numbers): at the WEIGHT layer, nothing in-window moves janitor-class PTQ off Q4-at-
  ceiling (held standing rule; today's census adds only out-of-domain or diffusion-model
  schemes: JustQuant is DiT/diffusion, W4A4 is diffusion, RGSQ/VisionMX are VLM). The
  ceiling-breaker CLAIMS live at two other layers, and both got read primary this sitting:
  (a) KV layer: TurboQuant turbo3/turbo4 claim "4.6x KV cache compression at 102% of q8_0
  speed, PPL within 1.3%" (TheTom, Mar 25, discussion 20969) and the buun fork extends the
  ladder to turbo2_tcq at 2.25 bpv ~7x compression, PPL 5.711 vs f16 5.683 (RTX 3090) -
  but the only INDEPENDENT reproduction read this sitting (devYRPauli, 2026-10-05) cuts
  the memory claim to 1.29x measured (unpacked storage) with HIGHER peak memory, and
  needle retrieval falls to 0% (stock MSE 4-bit) or 50% (hybrid at 2K). (b) CHECKPOINT
  layer: QAT-trained checkpoints INVERT the ladder rather than tie it - Unsloth measured
  naive Q4_0 conversion of Gemma 4 QAT at 70.2% top-1 vs 85.6% for their UD-Q4_K_XL
  (which is 200MB SMALLER), and "only one GGUF file for each Gemma 4 model" because
  HIGHER precision hurts accuracy on QAT checkpoints. That is a direct falsification of
  "Q8 is always the safe arm" for the QAT class: the tie the estate measured on PTQ
  qwen2.5:7b does not transfer.
- RQ2 (does QAT change the tie for janitor-class models, at what hardware cost on one
  Windows host): YES for the QAT-checkpoint class, and the cost is one download, $0:
  Gemma 4 QAT E2B needs 3 GB and E4B 5 GB total RAM+VRAM at 8k ctx (Unsloth table, read
  this sitting) - both fit the estate's 6 GB RX 5600 XT box; 12B needs 7 GB. Two
  corrections to day-9's proposed port: (1) do NOT pull qat-q4_0 (the naive conversion
  cliff above); pull unsloth UD-Q4_K_XL GGUFs; (2) the export-cast rider now has a
  published mechanism: Google trained int4 with Q4_0 in mind but llama.cpp's Q4_0
  conversion differs in scale handling (BF16 vs F16 scales), which is exactly why the
  same-format conversion loses 15.6 points. Training-side (OnlineQAT, held day-9) stays
  Lab-tier; today's theory increment is QAR (2609.21834): operates directly on the
  quantization code and is "both theoretically grounded and memory-efficient" versus
  QAT's shadow weights - the cheaper lane if the estate ever trains a quantized janitor.
- RQ3 (quality floor below which quantized local models emit hollow output, and how to
  measure it): two label-free instruments read this sitting, and they compose.
  (1) 2609.24322 (Undetected Damage of Quantization on Retrieval): top-1 retrieval
  churn of 14-46% while classification accuracy holds; the top1-vs-top2 score gap,
  measurable WITHOUT labels, "predicts which models will break under quantization" and
  per-input whether the quantized answer still matches full precision; survival is
  guaranteed only when the gap exceeds twice the largest rounding error. This is the
  formal version of the estate's strict-parse/material channels.
  (2) devYRPauli's needle-retrieval reproduction: stock 4-bit KV scores 0% at ALL FOUR
  context lengths (2K/4K/8K/16K) while generation stays coherent - retrieval silently
  dead is precisely the hollow-output shape STANDING_RAILS bans (material renders but
  is unfounded); hybrid K5/V4 50% at 2K with a "corrupted allele name" (plausible but
  wrong = worse than gibberition for a janitor). "Greedy decoding through a quantized
  cache turns small floating point differences into different tokens" - the estate's
  byte-identity channel (A/B: 50/50 byte-identical) is exactly the divergence detector
  here. PORT: add a staged-context needle task + the gap monitor to the quant_ab
  instrument; that also discharges the receipt's own OWED difficulty-hardened set
  (RECEIPT.md limitation 1) with a concrete design.
- RQ4 (which of the five FP8/GPU gates is closest to lighting, provable on estate
  hardware): gate 5 (WORKLOAD) is closest to lighting because it is an adjudication
  (DG1 / FP8 QPS demand), not a measurement - no external tooling change needed. Gate 4
  (SOFTWARE) moved closer in the open-tooling sense: OSFP4 (2610.08231) is a non-vendor
  NVFP4 quantization scheme with public code (github.com/neriahbd/OSFP4) retaining
  94-97% of VENDOR NVFP4 prefill throughput - but dogfooding it still requires an
  NVIDIA FP4 card, so it is NOT provable on estate hardware. Hard boundary datum read
  this sitting: the hottest open KV-quant lane (buun fork) requires CUDA or ROCm
  (tested RDNA3 gfx1100 / R9700, Windows ROCm 7.13), supports Vulkan NOT at all, and
  the estate's RX 5600 XT is RDNA1 gfx1010 - below every tested path. Gates 1/2 are
  hardware facts that cannot light on this box; gate 3 (price) was measured NOT fired
  on 10-06 (day-8 bank) and was NOT re-measured this sitting (disclosed). Net: no gate
  is provable on existing estate hardware; the honest closest-to-light is gate 5.

## Overlap ledger (instruments: venv python streaming grep over catalog/catalog.jsonl
1,343,390 rows; rg -i over memory/ (0 hits, all terms) and the day-6..9 mine dirs)

- TurboQuant: catalog 9 hits, ALL corpus/library/lmcache-src serde paths (docs/design/v1/
  distributed/serde/turboquant.md read this sitting: it is an L2 STORAGE serde backend,
  "does not implement an attention backend" - the day-9 inference-efficiency item 8
  "name collision, relationship unverified" flag is hereby RESOLVED: same algorithm
  family, different layer). day-9 item 8 banked the x snippet degraded (conf 0.5); my
  bank is the primary thread + reproduction + fork, the upgrade.
- 2609.24322: catalog 1 hit (state/arxiv/2026-09-22/2609.24322v1.txt title mirror,
  1,633 bytes); day-8 arxiv sweep listed it in a held-census line without reading. First
  read this sitting. Banked.
- 2610.08231: catalog 1 hit (state/arxiv mirror 10-07); day-8 x-sweep pass-1 listed the
  ID as considered-not-read. First read this sitting. Banked.
- 2609.21834 + 2609.33601: day-9 arxiv sweep "sweep-level (not banked)... None read
  beyond listing gists". Abstracts read this sitting; QAR banked, JustQuant left
  census-tier (DiT/diffusion focus, weak janitor fit).
- 2609.16085 Is INT8 Portable: BANKED day-8 as their item 1 (abs-page read with quotes).
  DROPPED from my bank; my id_list fetch merely re-confirms it lives.
- UD-Q4_K_XL: day-9 reddit lane used it only as a comparison anchor (Bonsai-2 parity
  claim). The Unsloth QAT docs page with the conversion-cliff numbers is unheld. Banked.
- 2605.02404 / Statistically-Lossless / Expected Acceptance Rate / buun-llama-cpp /
  spiritbuun / devYRPauli / turboquant_plus: ZERO hits in catalog and memory/. NEW.
- Held and NOT re-banked: bnjmn_marie Oct-1 ladder (day-8), FIT-GGUF (day-8), Gemma 4
  QAT WesRoth post (day-9), Sumanth 1-bit cliff (day-9), cjzafir 4B tie (day-9),
  Nex-N2.5 Mini (day-9), 2610.00983 + 2610.06174 + 2610.04403 + 2610.09827 + 2609.26219
  + 2610.06026 + LittleBit (day-6/7/8), datageek_ai + vibhavagarwal5 TurboQuant snippets
  (day-9 item 8), GPU price triggers (day-8, Oct-6 readings).

## Banked items (8, strongest first; quotes verbatim from pages fetched this sitting)

1. Unsloth Gemma 4 QAT docs (page undated; fetched 2026-10-10; Google release 2026-06-05
   per search + day-9) - RQ2 keystone with Windows-host costs.
2. arXiv 2609.24322 (2026-09-21, v2) - label-free quant-damage predictor. RQ3.
3. devYRPauli turboquant-m1pro-evaluation FINDINGS.md + 2026-10-05 comment - in-window
   independent reproduction. RQ1/RQ3.
4. llama.cpp discussion 20969 TurboQuant (OP 2026-03-25 OUT of window, marked; thread
   alive 09-12/10-05/10-10) - primary source, collision resolved. RQ1.
5. arXiv 2605.02404 (2026-05-04, v2 2026-08-09, OUT of window, marked) + bnjmn_marie
   ~10-03 post (IN window, snippet-banked per fallback) - EAR = the byte-identity
   channel formalized. RQ1.
6. spiritbuun/buun-llama-cpp (README updated ~2026-10-08, in window) - turbo/TCQ ladder,
   CUDA/ROCm-only boundary. RQ4/RQ1.
7. arXiv 2609.21834 QAR (2026-09-18, in window) - QAT endpoint theory + memory cost. RQ2.
8. arXiv 2610.08231 OSFP4 (2026-10-06, in window) - open NVFP4 scheme, 94-97% of vendor
   prefill. RQ4.

## Falsifier / caveats

- X search layer returned zero new status IDs today; only one X item is in the bank and
  it is snippet-tier (Marie ~10-03 post, body never fetched). The fxtwitter per-status
  door itself is alive (verified on the day-8 ID); the failure is ID discovery.
- arXiv items are abstract-level reads (export API); full texts not read.
- The Unsloth page is vendor documentation for their own GGUFs; its KLD/top-1 tables are
  self-reported, though the naive-Q4_0 cliff it reports is a claim AGAINST the naive path
  they could have hidden.
- TurboQuant OP is out of window (Mar 25); banked marked-as-such because its in-window
  reproduction (Oct 5) and fork updates (Oct 8) are the estate-relevant events.
- Gate-3 price triggers not re-measured this sitting; day-8's Oct-6 readings stand.
- No pytest run (not applicable to a sweep lane); no lane config changed; raw receipts on
  disk: sweep/_fx_arxiv_quant_window.xml, _fx_arxiv_idlist_deepread.xml,
  _fx_arxiv_statlossless.xml, _fx_arxiv_gguf_test.xml, _fx_arxiv_test2.xml.
