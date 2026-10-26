# Sweep: quantization-compression via Reddit (frontier_olm 2026-10-09)

source-fetched: 2026-10-09

Seat: sweep-quantization-compression-reddit. Area: quantization/compression on the Reddit door.
Feeds the burns LEDGER A/B queue (memory/burns/LEDGER.jsonl, 705 lines, byte-frozen since 10-07),
the UNMEASURED model-grid cells, the inference-budget terminal rule, and janitor-tier sizing.

## Standing rule this sweep tests (Q1 baseline)

The qwen2.5:7b Q4_K_M-vs-q8_0 A/B RAN 2026-10-08 and read TIE AT CEILING: 50/50 both arms,
byte-identical responses, spread 0.0pp, latency the only mover (3.99s vs 7.15s median, 1.79x)
- `watch/inbox/frontier_olm_2026-10-08/sweep/quant_ab/RECEIPT.md:38,:60`. Q1 asks whether anything
since 10-01 moved small-model quality off that ceiling.

## Doors: what worked, what degraded (all probes run this sitting)

- `old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=5` (recipe door): HTTP 302, SIZE 0,
  redirect to `old.reddit.com/login/?reason=lor2` (curl -w probe). CLOSED, same as the doors lens
  found at `watch/inbox/frontier_olm_2026-10-09/lens/doors.md:21-26`.
- `www.reddit.com/r/LocalLLaMA/top/.rss?t=month`: HTTP 200, 60,250 bytes, 25 entries. GREEN.
- `www.reddit.com/r/LocalLLaMA/search/.rss?q=quantization&restrict_sr=1&sort=new&t=month&limit=100`:
  HTTP 200, 631,561 bytes, exactly 100 dated entries spanning 2026-09-17 through 2026-10-09. GREEN.
  This is the 10-08 sweep's RSS recipe (`frontier_olm_2026-10-08/sweep/quantization-compression-reddit.md:27-33`),
  reused with the same `research-sweep/1.0` UA.
- Thread RSS `/comments/<id>/.rss`: GREEN with pacing. 9 threads fetched; two 429s hit at 38s
  spacing and both succeeded on 75-100s backoff retries. Degraded moments recorded, no evasion.
- `r/LocalLLM/top/.rss?t=month`: HTTP 200, 25 entries. `r/ollama/top/.rss?t=month`: HTTP 200,
  25 entries. Both IMPROVED vs 10-08, when they read 0 entries (10-08 sweep :32-33).
- `r/MachineLearning/top/.rss?t=month`: HTTP 429 after the r/ollama fetch; not retried further.
  The recipe's WebSearch fallback ALSO degraded today: 5 attempts (site: reddit.com queries) all
  returned z.ai 1302 rate-limit errors. r/ML coverage is therefore ABSENT today - recorded as
  degraded, no fallback success claimed.

## Pass 1: broad sweep (candidates considered, all dated in-window)

Discovery corpus: 25 (top month) + 100 (quantization search) + 25 (r/LocalLLM) + 25 (r/ollama)
listing entries, deduped against the 10-08 sweep's 39-candidate list and its 8 banked items.
Distinct candidates beyond yesterday's set (date | title | id), all evaluated for the four
research questions:

1. 2026-10-09 | Release: Qwen-2B-RCOL Dynamic Low-Bit Quantization (IQ1_M, IQ2_M, IQ3_M) (1x1dt7q)
2. 2026-10-09 | LoRA over GGUF: Train Qwen3.8-Flash-Next in 40G VRAM (1x1bdvl)
3. 2026-10-09 | Quantization of Linear-Attention (Qwen & Kimi) (1x18bsm)
4. 2026-10-08 | Staging quantized weights to FP8 instead of fp16: 2x M6 matrix path, +40% MLX prefill (1x13fo2)
5. 2026-10-08 | Ran a 120B model across 6 computing devices (1x0ubuc)
6. 2026-10-07 | A stock GLM-Edge-1.5B-Chat on a 4GB Galaxy A04e completed a real Amazon cart task (1wzrw6x)
7. 2026-10-07 | My progress on a [new] model-architecture specific dynamic quant technique - v1 (1x083w0)
8. 2026-10-06 | 54gb vram for 35$ (1wz6ist, top-month RSS)
9. 2026-10-06 | What models do you want to see new dynamic quants for? (1wz5txe)
10. 2026-10-06 | I quantized GLM-5.3-UNCENSORED to MXFP4 for AMD GPUs (1wz4vh6)
11. 2026-10-05 | k_llama.cpp MoE Optimizations: Expert Residency, Hybrid CPU/GPU, Q2_0 Support (1wynomx)
12. 2026-10-05 | We swapped AdamW's optimizer states for a Fast Fourier Transform (1wyizhj)
13. 2026-10-05 | llama.cpp is now the default agent engine in Modly. Which models up to 8B work best for tool calling (1wyizhj sibling 1wyizhj? distinct id 1wyizhj listed; thread id in RSS)
14. 2026-10-03 | DwarfStar compresses frontier models to run them on local machines (r/ollama top-month RSS)
15. 2026-10-03 | I built Ninfer 4080 for 16GB class GPUs (1wwv0fj)
16. 2026-10-02 | 200 Task Custom Dataset Performance Result: 10 Popular Models, 2B MoE to 27B Dense (1ww528l)
17. 2026-10-02 | How do you keep a local multi-agent app usable on CPU-only / low-RAM machines? (1wvwmb5)
18. 2026-10-01 | converting Qwen3.8-27B-pi GGUF to MLX? (1wvbcm5)
19. 2026-09-30 | Victoria: Qwen3.8-Flash-Next with 44% of experts cut (1wujph3)
20. 2026-09-29 | Local Q2_K model dunked on DeepSeek V4.1-Flash mini test (1wtkzc5)
21. 2026-09-28 | TextCLF Quant Factory (1ws1ncf)
22. 2026-09-25 | Qwengram-0.8B n-gram memory transfer into Qwen3.5-0.8B (1wpvep4)
23. 2026-09-24 | UkisAI Swift Series / Bonsai 2 + GSQ-RCO, -63.4% thinking x1.95 speed (1wp6gal)
24. 2026-09-21 | REAP/MTP Qwen3.8-Flash-Next MLX builds, measured trade-offs (1wmlt6i)
25. 2026-09-21 | A better coder for the small-GPU/small-RAM crowd (1wmgokc)
26. 2026-09-21 | Uncensor without touching weights: 18MB KV-cache bank inject/unload (1wms904)
27. 2026-09-20 | Please stop with the FP4 inference engines (1wl56g2)
28. 2026-09-20 | How was your experience running Q1 Models (1wl2ey8)
29. 2026-09-18 | Prism-ML Bonsai 2 Joins Our Qwen3.8 Quantization Comparison (1wju8ky)
30. 2026-09-17 | Ternary Bonsai 2 (27B) <6GB, WebGPU (1wj6c4l, top-month RSS)

Out-of-scope or thin: PewDiePie/OpenAI ban thread, price/rig threads (1wynonf, 1wyfgn2), vLLM
learning threads, roleplay benchmark threads - none carry a quantization claim.

## Pass 2: deep reads (9 threads read end to end this sitting)

Each fetched via `curl -A "research-sweep/1.0" https://www.reddit.com/r/LocalLLaMA/comments/<id>/.rss`,
raw RSS + extracted text cached in this dir (`_raw/thread_*.rss`, `_txt_*.txt`); OP body and all
comment entries parsed and read.

1. 1x1bdvl (2026-10-09, woct0rdho) LoRA over GGUF: QLoRA with a GGUF base replacing bnb 4-bit;
   trains Qwen3.8-Flash-Next (125B-A6B + 51B engram) in 40 GiB VRAM, no CPU offload, 9.5 s/it at
   2048-chunk on Strix Halo (~200 tok/s); transformers 5.18 merged initial modern-GGUF support.
   THE KEY EXCHANGE: (a) OP trains on Q2_0 (MMQ ~1.5x faster than IQ4_NL) and serves the adapter
   on IQ4_NL - "as long as the LoRA rank is low, it will not learn the quantization error (which
   is mostly unbiased in modern quantization formats)"; (b) counter-datum from a Qwen3-4B
   tool-calling LoRA: merged into Q4_K_M the exact score fell 1.00 -> 0.69 (base level); Q8_0/fp16
   survived the merge - law candidate: adapter-on-quantized transfers, merge-into-Q4_K_M does not.
2. 1x1dt7q (2026-10-09, jjusko20) Qwen-2B-RCOL: a modification of ISTALab's RCO quantizing on a
   strict VRAM budget, "significant KLD improvements, particularly in the 1 bit and 2 bit range",
   model-agnostic, no FP16 teacher in VRAM; IQ1_M divergence drastically cut at nearly the same
   size budget vs standard wikitext-imatrix quants (both calibrated on the same set, tested on two
   held-out sets). Honest limit stated by the author: "2B is a fairly small model and suffers from
   such low BPW"; the demo is 4/5 on one color task at IQ1_M vs "yikes" for standard imatrix IQ1_M.
   GGUFs: huggingface.co/trubisky/Qwen3.5-2B-RCOL.
3. 1x18bsm (2026-10-09, kroggens) STEPQuant thread: paper is arXiv 2609.38169 (link in comments);
   quantizes the GDN recurrent state of linear-attention Qwen/Kimi models. Community scoping: each
   27B sequence holds ~200MB recurrent state at F32 across 48 GDN layers, so this pays only at
   high concurrency ("not useful at all at the scale most private/local inference operates at").
   Field report (FullOf_Bad_Ideas): W8A8 + STEPQuant state quant at 320-1024 concurrency on
   8x3090 Ti under SGLang gave a sustained 20-30% throughput gain (~3500 -> ~4500 TPS at batch
   ~650) after PP-partition + fp8_e5m2 KV + chunked-prefill tuning.
4. 1ww528l (2026-10-02) 200-task tier list: Gemma-4-26B S-tier "even quantized down to iq3s it
   tops my charts"; Qwen3.5-4B matches Gemma-4-12B's 0.795 at 3.4GB vs 7.8GB (two VRAM bins down);
   Gemma-4-e2b punches above its weight at B-tier. Held: banked by the 10-03 window (10-07
   register.jsonl:4 overlap note: "Ling-3.0-tiny F-tier held via the 10-03 bank item 1 (1ww528l)").
   NOT re-banked; read this sitting to keep its quant-adjacent datums in evidence.
5. 1wpvep4 (2026-09-25) Qwengram-0.8B: frozen ~51B-param PLE n-gram memory as an external
   quantized sidecar + R=1 reader at decoder layers 3 and 9 with a dynamic token gate; PPL
   18.28 -> 17.35 (-5.05%) on Qwen3.5-0.8B; 2B follow-up -3.7 to -4% (gains shrink with scale).
   THE QUANT DELTA the estate's 10-02 bank does not carry: "Q8_0 retains 99.1% of the BF16 reader
   NLL gain" on a fixed WikiText-2 GGUF runtime test. Held since 10-02 (bank item 5); not re-banked.
6. 1wtkzc5 (2026-09-29) Q2_K anecdote: OP corrected the model name in-thread (DeepSeek V4.1-Flash,
   itself open-weight) and published the full 12-item suite + answer key + red flags
   ("Below 5 core correct: Likely broken, over-quantized, or using the wrong chat template").
   Held: 10-02 sweep banked it in narrative only (:35). The NEW delta is the published instrument
   itself - a 12-item cold-context quant smoke test the quant_ab harness could reuse.
7. 1wj6c4l (2026-09-17) Ternary Bonsai 2: ternary 27B at <6GB, "9x smaller than FP16 while
   retaining 98.2% of the intelligence" (model card, contested); quoted card numbers from comments:
   84.78 avg across 14 thinking-mode benchmarks vs IQ2_XXS 72.59, within 0.4 points of UD-Q4_K_XL
   at three times the footprint; community rebuttals target benchmark selection (old saturated
   benchmarks) and the Bonsai-1 track record; counter-datum: Bonsai-1.7B ran on a Jetson Nano at
   17 t/s "didn't hallucinate". Held via the banked sibling 1wjnklv (10-04 sweep :38, :157);
   not re-banked.
8. 1x13fo2 (2026-10-08 21:31) FP8/int8 staging in MLX: dequant-stage QMM operands to FP8 (M6) or
   int8 (M5+) instead of FP16 to hit the ~2x 8-bit matrix path: +40% prefill Qwen3-8B, +50%
   Qwen3.8-27B; decode untouched (bandwidth-bound, keep FP16 staging); measured worst-case ppl
   increase under 1%; weights exact for mxfp4, the cost is per-row power-of-two scales on
   activations; experimental fork mlx#4627, precisit blog + github.com/precisit/mlx
   staged-8bit-qmm branch.
9. 1wzrw6x (2026-10-07) GLM-Edge-1.5B-Chat at Q4_K_M GGUF, stock, no finetune, llama.cpp on a 4GB
   Galaxy A04e, completed a real two-item Amazon cart task (batteries + rubber ducks, stop before
   checkout) twice (8.5 min A04e, 3 min S21) through the E2LLM/SiFR structured browser perception
   layer (no screenshots, no raw HTML). Third in the author's series (Qwen3-0.6B on Note 8,
   Ministral 3 3B on S21).

## Overlap check (run this sitting)

Instrument: case-sensitive fixed-string greps over catalog/catalog.jsonl, memory/ (full recursive
single pass), and ALL prior frontier windows frontier_olm_2026-09-30 through -10-08 (the gapfold
lesson: sweep prior windows, not just catalog+memory). Patterns file kept at
`_overlap_pats.txt` (18 patterns: 7 thread ids + RCOL + Qwengram + STEPQuant + stepquant +
"Ternary Bonsai" + ternary-bonsai + "LoRA over GGUF" + "200 Task Custom Dataset" + Nex-N2.5 +
"Nex N2.5" + 2609.38169).

- The five BANKED items (1x1bdvl, 1x1dt7q, 1x18bsm, 1x13fo2, 1wzrw6x): thread ids ZERO in
  catalog + memory; prior-window hits only as (a) a 09-28 passing mention of the author's earlier
  repo in `frontier_olm_2026-10-04/sweep/_fta_thread_1wslgkw.txt:113` ("Also possible to train
  LoRA over GGUF"), (b) raw r/LocalLLM harvest rows naming the 1wzrw6x author's EARLIER sibling
  experiments (arctic_LocalLLM.json, _amc_*_harvest.jsonl, as_rows.jsonl - raw intake, never
  banked; the 10-07 GLM-Edge thread itself postdates those harvests), (c) the STEPQuant PAPER
  (2609.38169) fetched raw by the 10-03 window (`_raw/q_2609.38169.html` 572,761 bytes + `.txt`
  109,638 bytes, catalog intake rows) - the 10-09 FIELD DATA (measured 20-30% sustained at
  320-1024 concurrency) is not in any prior window.
- The four HELD threads (1ww528l, 1wpvep4, 1wtkzc5, 1wj6c4l): confirmed held in the 10-02/10-03/
  10-04 windows as detailed in Pass 2; deliberately NOT re-banked.
- memory/ false positive disclosed: 229 case-sensitive "RCOL" hits inside
  memory/agent_sessions/orc-t*.json are id-fragment noise inside session command logs, not
  quantization content (context-checked one file); "Ternary Bonsai" hits in
  memory/runs/gapwave/splash_bonsai_livetranslate_verified_20260920.md + memory/runs/salon1/
  inputs/ are real but reference the already-banked Bonsai line, not new claims.
- Q3 verification GET (green arXiv door): `curl
  "https://export.arxiv.org/api/query?id_list=2610.04403,2610.09827,2609.38169&max_results=3"`
  returned HTTP 200, 8,918 bytes with all three titles and dates:
  "Saying, Not Knowing: Aggressively GGUF-Quantized Small Language Models Still Write Rare Words
  They Can No Longer Define" (2026-10-03), "Dual-QK: Sharp Queries and Flat Keys for Prunable
  2-bit KV Caches" (2026-10-07), "STEPQuant: When and Where Errors Matter in Delta-Rule Recurrent
  State Quantization" (2026-09-29).

## Answers the sweep feeds (scoping stated)

- Q1 (ceiling moved?): NO for weight quantization at janitor class - Q4-at-ceiling stands. The
  TIE receipt is the estate's own 50/50 byte-identical verdict (RECEIPT.md:38); every in-window
  community datum is consistent with it: the 200-task list puts an iq3s-quantized 26B on top,
  a stock Q4_K_M 1.5B completes real agent tasks on a 4GB phone, and the RCOL release improves
  the 1-2 BIT rungs (KLD tables) while its own author concedes 2B "suffers from such low BPW".
  What the frontier moved since 10-01 is everything EXCEPT the weight-Q4 axis: (a) below-Q4 bit
  ladder (RCOL at IQ1/IQ2 on 2B; Bonsai-2 ternary claiming UD-Q4_K_XL parity at 27B, contested),
  (b) activation/compute staging (FP8/int8 QMM, <1% ppl for +40-50% prefill), (c) recurrent-state
  quant (STEPQuant, concurrency-only), (d) non-quant quality levers for small models (Qwengram
  sidecar). The ceiling holds; the axes around it multiplied.
- Q2 (QAT/LoRA-on-quantized filling UNMEASURED cells, local-first): 1x1bdvl is the direct
  answer and it respects T0/T1: the whole recipe is local (40 GiB, no offload, GGUF in, adapter
  out). Two laws for the model-grid: train-arm quant and serve-arm quant may DIFFER (Q2_0 train,
  IQ4_NL serve) because low-rank adapters do not absorb modern formats' quant error; but the
  adapter must stay an artifact - merging into Q4_K_M lost a measured finetune (1.00 -> 0.69)
  while Q8_0/fp16 survived the merge.
- Q3 (day-8 mine's 6 unbanked cards re-verifiable via one arXiv GET): all 6 steal cards read
  (quantization-compression via hn, kv-cache-context-engineering, open-local-models via reddit,
  open-local-models, finetuning-adaptation, inference-efficiency-hn). TWO carry quantization
  claims one-GET re-verifiable: quantization-compression via hn (2610.04403) and
  kv-cache-context-engineering (2610.09827 Dual-QK 2-bit KV; its 2609.26219 PatchKV is KV
  recovery, not quantization). The verification GET RAN and returned all three titles
  (including 2609.38169, a bonus corroborating today's own item 3). The other four cards: two
  are GitHub/economics carriers, finetuning-adaptation's 2610.06851 is a non-quant token-cue
  paper already estate-held since 10-06, open-local-models' arXiv releases are already banked.
- Q4 (weight-sharing/pruning for sub-8B the corpus lacks): the corpus library still has ZERO
  rows for the one in-window pattern that matters (Qwengram: frozen 51B n-gram PLE sidecar onto
  0.8B/2B with measured quant retention) - catalog grep Qwengram returns only intake rows of the
  sweeps themselves. New sub-8B pruning/weight-sharing since the held Victoria/GSQ expert-cuts:
  nothing found in-window; the corpus gap stands. The 44M-param r/ML thread (1wgzpli, 09-15)
  remains unverified this sitting (r/ML RSS 429 + WebSearch 1302) - still OWED, not claimed.

## Honesty notes

- Door: recipe JSON door closed (lor2, reproduced); working door is www.reddit.com RSS with
  pacing (two 429s hit and cleared on backoff). r/MachineLearning top RSS 429 and the WebSearch
  fallback rate-limited (5x z.ai 1302) - r/ML coverage ABSENT today, no fallback success claimed.
- Scores/comment counts are not in RSS; "strong" = relevance to the four questions + depth read.
- All quotes are verbatim substrings of the fetched RSS text cached in this dir (_txt_*.txt);
  the three arXiv titles are verbatim from the one verification GET. Nothing quoted from search
  snippets; the DwarfStar and 1wyizhj-class candidates were discovery-only, NOT banked.
- The four held threads were deep-read anyway to answer Q1/Q4 with their deltas and to keep the
  not-re-banked discipline explicit; their holdings are cited, not re-claimed.
- No A/B re-run, no local probe fired: sweep seat, no burns-lane firing authority; the TIE stands
  as receipted.
