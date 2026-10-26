# sweep: quantization-compression via Hacker News - 2026-10-11 (confirmation pass)

source-fetched: adhoc

Gopher: sweep-quantization-compression-hn (third seat of this name: the 2026-10-10
adhoc wave wrote the prior file at this path, and the 2026-10-11 daily lane wrote
frontier_olm_2026-10-11/sweep/quantization-compression-hn.md; both were read in full
this sitting before this write). This file supersedes the 10-10-dated file at this
path. Its banked items (Compress and Forget, Saluki, UWSH, Dead Salmons correction,
Quesma delta, OptR) remain the bank of record; this sitting is the confirmation pass
the adhoc DIGEST owed for this area (watch/inbox/frontier_olm_adhoc/DIGEST.md named
quantization-compression confirmation as OWED), plus two net-new deltas.

Ask: five research questions on janitor-fleet stratification, the reddit quant
census, quantized-lattice decision force, sovereign-isolation quantizer bars, and
sub-4-bit structured-output reliability. Recipe: HN Algolia search_by_date + search,
then news.ycombinator.com item threads.

## Door health (run record, this sitting)

- hn.algolia.com: clean on 9 of 9 WebFetch calls (8 by-date, 1 would-be relevance
  batch was cut when breadth was reached). numericFilters=created_at_i>1789084800
  (2026-09-11, 30-day window) honored on every query.
- Query-shape negatives stated as negatives: "3-bit" nbHits 0; "ternary" matched
  Terry Tao / cushioned-shoes noise (same trap class the 10-10 sibling named);
  "pruning" mostly front-page noise but surfaced ALHR and DeltaTensors.
- news.ycombinator.com item pages: clean (Janus 49926773, DSv4.1 49735410, Swift
  49727511, Bonsai-2 reddit pointer 50002054).
- ONE timeout: huggingface.co/blog/ggml-org/decision-models-in-llamacpp (60s, not
  retried verbatim). Not fabricated over: the subject is thrice-banked (10-03 item 2,
  10-05 model table, 10-06 Julia-1 delta) and my Ollama-blog fetch covered the
  same surface from the vendor side.
- Reddit wall re-confirmed a THIRD consecutive session, this time on the exact
  Bonsai-2 URL (r/LocalLLaMA comments/1wju8ky, resolved via HN 50002054): WebFetch
  returned a bare "Reddit" stub, zero post content. Matches doors.md:52-60 (standing
  verdict). The reddit quant census to its 30-item floor stays impossible through
  WebFetch; curl + browser UA remains the unprobed instrument (OWED, unchanged).

## Pass 1 - broad census (9 queries, 30-day window; 43 distinct candidates considered)

Queries: quantization, quantized, llama.cpp, GGUF, "kv cache", ollama,
"structured output", "model compression", ternary/pruning (noise-heavy, disclosed).
Distinct candidates (id, pts, date) - the full list, deduped:
50043847 EmbeddingGemma2 browser 1p 10-11; 50034625 LoRA over GGUF 1p 10-10;
50002054 Prism-ML Bonsai 2 ByteShape reddit compare 1p 10-08; 49980637 Hopf
Spherical 1p 10-06; 49975499 AMD Quark Strix Halo 1p 10-06; 49833102 UkisAI series
1p 09-24; 49823211 quant-delta-predictor 1p 09-23; 49822130 Lifeboat 6p 09-23;
49804932 VLA Jetson Thor 2p 09-22; 49778955 QLoRA explainer 1p 09-20; 49743523
Weaviate 4-bit rotation 5p 09-17; 49727511 Swift-Qwen3.8-27B 33p/17c 09-16;
49703818 GSQ-RCO 2x3090 9p 09-14; 49676635 bartowski layout maps 3p 09-12;
50002660/49997807 WinML llama.cpp 10-07/10-08; 49942092/49934323 llama.cpp Decision
Models 10-02/03; 49911995 Magnitude 194p/97c 09-30; 49859982 prompt lookup drafting
89p 09-26; 49812339 Transformers runs llama.cpp quants 09-23; 49742415 Mozilla
server benchmark 09-17; 49926773 Janus GGUF Vulkan 106p/19c 10-01; 49847732
VeriLoop IQ1_M ladder 09-25; 49813964 Bonsai-2-27B 09-23; 49774861 Bonsai-8B 09-20;
49869861 quantized overthinking arXiv 13p 09-27; 49966238 EasyCommand 09-05 class;
49734038 context rot 09-16; 50013834 Self-Pruning KV 6p 10-08; 49945575 KV memory
wall 10-03; 49735410 DSv4.1 KV 131p/10c 09-17; 49758259 vLLM prefix warm 09-18;
50020238 ALHR 35.3x KV 10-09; 49783349 DeltaTensors 09-21; 49911910 token
compression CLI 14p 09-30; 50025042 Kisoku 1.6B 2p 10-09; 49882932 Return removed
Ollama 09-28; 49938916 justine.lol CPU matmul 10-02; 49906337/49908997 Ollama Jev
decision models 09-30; 49748997 seangoedecke Jev 15p 09-18; 50032037 "Do We Still
Need Models Like Jev?" 10-10; 49861867 Credence 09-27; 49878572 jeva.cpp 09-28;
49921633 Sriti cascade router 10-01.

## Pass 2 - deep reads this sitting (12 pages fetched and read end to end)

Janus thread 49926773; zartbot DSv4.1 teardown; DSv4.1 thread 49735410; bartowski
layout-maps blog; arXiv 2606.00206 abs; quant-delta-predictor README; seangoedecke
Jev post; prism-ml Ternary-Bonsai-8B-gguf card; Ollama Jev decision-models blog;
VeriLoop HF discuss thread 180723; hscq README; Swift thread 49727511; Bonsai-2-27B
card; reddit Bonsai-2 URL (walled, disclosed above). One timeout (decision-models
HF blog), disclosed. Every quote below is verbatim from a page fetched this sitting.

## Dedup ledger - the held map (all greps actually run this sitting)

Instruments: catalog/catalog.jsonl pattern grep (counts printed in-session);
grep -ril over watch/inbox/frontier_olm_20260928 + 2026-09-30 + 2026-10-01..10-11 +
frontier_olm_adhoc (the standing law, burns.md:253-255); targeted reads of the
10-05, 10-06, 10-07, 10-10, 10-11 daily banks and the prior file at this path.

HELD, re-read first-hand this sitting, numbers reproduced with zero drift - do not
re-bank: bartowski layout maps (10-02 item 2 + adhoc item 3); arXiv 2606.00206
(10-01, percolator rows 18/19; logit-penalty 12-23% CoT cut reproduced);
quant-delta-predictor (10-03 cycle 2 item 4; 93.23% coverage and -39.5pp
adversarial tail reproduced); DSv4.1 Flash teardown + thread incl. nchmy "paid 50x
more than expected" and mmastrac 5M-session compactor (10-02 item 1 + 09-30
register line 8); VeriLoop ladder (10-05 + 10-06 register row 15); Swift thread
(10-03 evals-and-self-improvement-hn.md:113, same kisjovan quotes and quant-
overthinking comment); Janus + comment cluster (10-03 item 5 + 10-10 item 6, same
bitexploder V100 and gunalx Vulkan-ballpark content); seangoedecke Jev (09-28 bank,
prefill trick verbatim incl. the Qwen2.5-1.5B 2x-3x line); Ollama Jev blog (10-05
open-local bank lines 33/69/189: nimble 9B 91ms M5 Max, tev1 4B/0.8B, 0.35);
hscq Hopf (10-10 item 5, same rel-RMSE numbers); decision models llama.cpp
(10-03/10-05/10-06); Kisoku 1.6B (adhoc register row 18); returneditor (row 12);
GSQ-RCO (10-03 cycle 2 item 3); Mozilla servers benchmark (row 13); WinML (10-10
item 1); Bonsai-2-27B program (FREE_LANE_INTEL_BONSAI2_20260923.md holds 84.78 vs
86.32, night-run HTTP 500s, and the hardware-incompatible verdict: ggml type 143
needs the PrismML fork, CUDA/Metal only, no Vulkan, RX 5600 XT out).

NET-NEW this sitting (banked below): Ternary-Bonsai-8B card specifics (census-
listed 09-28:16, 10-01, 10-03, 10-07 but never read; grep "lossless for
ternary"/"IFEval 81"/"Q2_0_g128" over every sweep tree = 0 hits) and the Bonsai-2
card's per-capability table + conventional-2-bit-collapse comparison.

## Banked items (strongest first)

### 1. Ternary-Bonsai-8B-gguf - instruction-following preserved at 1.58-bit, 8B scale
huggingface.co/prism-ml/Ternary-Bonsai-8B-gguf (HN 49774861, 2026-09-20).
Quote: "Each weight takes a value from {-1, 0, +1}, with one shared FP16 scale per
group of 128 weights."
Ternary (1.58-bit) Qwen3-8B; F16 16.38GB, Q2_0 (g128) 2.03GiB described as
"lossless for ternary" (Q2_0_g64 and PQ2_0 variants exist); EvalScope H100: Qwen3-8B
FP16 avg 79.3 vs Bonsai 75.5 at 1/8 the size, GSM8K 91 vs 93, IFEval 81.8 vs 81.5;
76 tok/s generation on M4 Pro Metal; needs the Prism fork (CPU NEON + Metal; Q2_0
not in mainline llama.cpp); Apache 2.0.
Why it matters: the only in-window sub-4-bit measurement at 8B scale that grades
instruction following (IFEval), the exact capability class the estate's Q5 asks
about for 1-8B models - and it holds at ternary where conventional 2-bit collapses.
Estate caveat carried from the held 27B intel: fork-only formats do not run on this
Vulkan box (RX 5600 XT), so this is evidence, not a deployable.
Overlap: census-listed four times, card never read before; strings grep 0 across
all frontier trees; the 27B sibling is heavily held (intel file + Saluki bench).

### 2. Ternary-Bonsai-2-27B card delta - the conventional-2-bit collapse comparison
huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf (HN 49813964, 2026-09-23).
Quote: "Retains thinking, reasoning, and agentic behavior deep in the sub-4-bit
regime, where conventional low-bit representations collapse"
New beyond the held intel file: PTQ1_0 1.75bpw/5.95GB vs PQ2_0 2.13bpw/7.21GB
(PQ2_0 faster on Hopper/Blackwell, PTQ1_0 on Ada/L4); 14-bench thinking-mode avg
FP16 86.32 / Bonsai 84.78 / UD-Q4_K_XL 85.18 / IQ2_XXS 72.59, with the collapse
datum: IQ2_XXS AIME26 57.5 vs Bonsai 95.83; tool calling 74.92 measured (biggest
drops: knowledge/reasoning and vision); "intelligence density" 0.457/GB; M5 Max
~47 tok/s at ~34W; Hadamard rotation baked in; Apache 2.0.
Why it matters: Q5's headroom question now has a same-model, same-card comparison
of sensitivity-allocated ternary vs conventional IQ2_XXS at 2-bit on agentic +
tool-calling benches - the clearest published "not all 2-bit is equal" row, and it
quantifies what the 10-05 Xyntetik shape/content law predicts.
Overlap: heavy and stated - the 27B program is held (FREE_LANE_INTEL_BONSAI2_
20260923.md: 84.78 vs 86.32, hardware verdict; adhoc Saluki item: Bonsai 2 = 70 on
Underdog Bench; 10-06 door captures). New = per-capability table, IQ2_XXS collapse
row, variant/throughput detail only.

Micro-delta folded here, not separately banked: the VeriLoop HF-discuss post (read
this sitting) records a forum user's 8-item forced-choice test where IQ1_M and
Q4_K_M made identical decisions (8/8 agreement, 5/8 correct each) - external
support for the estate's Q3 reading that quantization preserves decision SHAPE
while content-correctness is the unguaranteed half (the held Xyntetik law: "Shape
is guaranteed at any quantization. Contents are not.").

## Research-question verdicts (from what this sitting read or re-verified)

- Q1 (does the banked stratification law hold on gemma:2b/gemma4): no HN source
  benches the estate's janitor fleet; the 2B class stays below every model benched
  in this window (the 09-28 law, re-confirmed). Nearest evidence remains held:
  bartowski's 0.8B/4B sensitivity maps (KLD-proxy only), Xyntetik 1.7B-3B
  shape/content split, quant-delta-predictor's scheme-dominates-model finding, and
  2606.00206's behavioral damage at 1.5B+. The janitor-tier induction/retrieval
  battery stays un-fired; nothing on this door runs it for us.
- Q2 (reddit quant census): door walled third consecutive session, now confirmed
  on the exact Bonsai-2 thread URL. Census stays OWED behind curl+UA. What HN
  holds that the arXiv fold missed is practitioner lore, already banked: per-tensor
  layout maps, Unsloth UD non-uniformity, per-variant fork requirements.
- Q3 (can provenance-only rows carry decision force): every external datapoint
  this sitting re-verified says shape yes, content no (Xyntetik 50% argument
  agreement; VeriLoop 8/8 shape agreement; Credence/jeva.cpp banked as the local
  typed-decision cures). The path:line receipt stays the only content carrier;
  weight/count rows can carry routing shape at best.
- Q4 (sovereign REFUSE paths): unchanged from held rows - returneditor's
  cloud-suffix REFUSE + llama-server sidecar replacement (adhoc register row 12),
  Ollama local decision endpoints (10-05), WinML native GGUF (10-10 item 1). My
  Janus re-read re-confirms the wrapper verdict: the demonstrably-refusing local
  path IS llama-server; new runtimes wrapping it add no isolation property.
- Q5 (sub-4-bit structured output headroom): the 2026 answer, now with the Bonsai
  deltas: ternary-native weights (needs fork; IFEval/tool-calling preserved),
  sensitivity-allocated non-uniform GGUF (GSQ-RCO/IQ2-mix/UD/layout maps; held),
  and grammar-constrained decoding decoupled from weight quality (held XGrammar-2
  thread-cite). Re-run headroom above the closed ceiling tie (burns.md:250):
  proactive-interference probe (held adhoc item 1: 81.0 to 68.3 INT4), token-count
  logging (2-bit +25% output tokens), and content-scored argument agreement.

## OWED (not found, not run, never fabricated)

- Reddit quant census at its 30-item floor: blocked by the standing wall; curl+UA
  probe still unfired by any seat.
- Janitor-tier induction/retrieval battery on gemma:2b/gemma4: un-fired, no HN
  substitute exists.
- EmbeddingGemma2 browser demo (50043847): judged not bankable from its landing
  page by the 10-11 daily seat; not re-attempted here.
- The Bonsai-2 ByteShape comparison CONTENT (1wju8ky): unread by any seat through
  three sessions; the HF cards above carry the vendor-side numbers instead.

Counts law: 43 candidates enumerated from Algolia responses this sitting; 12 pages
read end to end; overlap greps run with counts shown above; no counts from
different instruments were differenced. Em-dash scan of this file: none present.
