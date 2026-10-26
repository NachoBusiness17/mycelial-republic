# SWEEP: quantization-compression via arXiv (frontier_olm 2026-10-10)

source-fetched: 2026-10-10

Seat: sweep-quantization-compression-arxiv (dynamic workflow run, branch
mag/run-beta1-factory-build-audi-20260806T231709Z). Area: the 4 questions on the
estate's quant A/B (TIE AT CEILING, Q4 6.90 vs Q8 3.00 tok/s,
watch/inbox/frontier_olm_2026-10-09/lens/burns.md:96; instrument
watch/inbox/frontier_olm_2026-10-08/sweep/quant_ab/RECEIPT.md:38-43), the five
FP8/GPU gates (memory/rib/RIB_GPU_LADDER_20261001.md:10-23), and the OnlineQAT
day-9 register row (watch/inbox/frontier_olm_2026-10-09/register.jsonl row 6).

## Door status (honest)

- export.arxiv.org/api/query: WORKING, with degradation on first attempts. Five
  queries run (cat:cs.CL quantization; cat:cs.LG quantization+language model;
  quantization-aware training; FP8+inference; low-bit+decode), sortBy
  submittedDate descending. Two of five first attempts timed out at the 60 s
  WebFetch limit (the FP8 query and the CPU/edge query); both succeeded on
  retry with max_results cut from 15 to 10. Same shape the day-8 sweep measured
  for sortBy variants (its doors note, quantization-compression-arxiv.md:10).
- arxiv.org/abs pages: green all sitting, 9 fetched, zero 403s.
- arxiv.org/html/2610.09346v1 (OnlineQAT full text): green on first try (the
  day-8 sweep had found the html door intermittent; today it held).
- No /list/cs.CL/recent fetch needed: the API door covered the window.

## Pass 1 (broad sweep, window 2026-09-10..2026-10-10)

Five API queries returned 75 entries; union after dedup by arXiv ID is roughly
63 unique candidates, over the 30-candidate floor. IDs (newest first):
2610.12338, 2610.11482, 2610.11226, 2610.11214, 2610.10738, 2610.10058,
2610.09827, 2610.09346, 2610.09227, 2610.09212, 2610.09202, 2610.08732,
2610.08403, 2610.08164, 2610.07853, 2610.07781, 2610.07767, 2610.07522,
2610.07457, 2610.07121, 2610.07032, 2610.06996, 2610.06404, 2610.06387,
2610.06251, 2610.06174, 2610.06026, 2610.05685, 2610.05329, 2610.05265,
2610.03741, 2610.10933, 2610.10385, 2610.10641, 2610.10058, 2609.34185,
2609.33601, 2609.33586, 2609.33477, 2609.33135, 2609.32429, 2609.31341,
2609.31177, 2609.26621, 2609.26708, 2609.24875, 2609.23153, 2609.22870,
2609.21834, 2609.27453, 2609.14864, 2609.04263, plus out-of-window QAT feed
tail (2608/2607/2606 IDs) considered but not banked on window grounds.

## Pass 2 (deep reads, this sitting)

Ten abs pages fetched and read end to end: 2609.14864, 2610.09202, 2609.26621,
2610.07853, 2609.26708, 2609.22870, 2610.08164, 2609.34185, 2610.06251,
2610.11482. One full-text HTML read: 2610.09346 (OnlineQAT, hardware-cost
extraction for RQ2). Four of the ten deep reads turned out to be estate-held on
the overlap walk and were dropped from the bank (see ledger); their reads still
feed the question answers below.

## Overlap ledger (greps run this sitting)

Instrument: grep -ic per pattern over catalog/catalog.jsonl (fast single-file
pass); grep -rln per ID over watch/inbox/frontier_olm_2026-10-01 through
_2026-10-09; targeted greps over memory/ (frontier, rib, law, lenses). A
13-pattern recursive loop over catalog+memory+watch+state was killed for
slowness (its catalog-only prefix completed and is what the counts below use);
memory/ recursive hits were already known from the day-9 walk to be trajectory
process traces, and my targeted memory greps (rib/, law/, lenses/, frontier/)
returned the GPU ladder and no title banks.

Held, dropped from bank (re-banking is waste):
- 2609.14864 GGUF-metadata predictor: banked 10-01 (two sweeps), register row
  21 in the 10-03 DIGEST with verdict "constants do not transfer". My read
  confirms: active-parameter decode MAPE 13.1/14.4/36.1 percent vs
  total-parameter 49.4/55.3/51.9; leave-one-host-out 11.6/16.8/36.0.
- 2609.26708 Train Where the Quantized Model Goes: banked day-4 as Find 2
  (watch/inbox/frontier_olm_2026-10-04/sweep/quantization-and-compression-arxiv.md:125,
  deep-read list :16). Sub-3-bit retention 35 to 70 percent MATH-500, 66 to 91
  percent HumanEval stands as held.
- 2610.07853 Lost in the bf16 Cast: abs-read day-7 (its sweep :58), is the
  source of the A/B spec's export-cast rider (QUANT_AB_SPEC_AMEND.md:81-84 per
  the day-8 sweep :59). The 58.79 to 0.78 percent GSM8K collapse is held.
- 2610.08164 Align, Then Correct: banked day-7, register.jsonl row 21 with the
  51/84 percent gap-recovery quote.
- 2610.06251 HQQ shared stopping: banked day-6, re-banked-with-delta day-8
  (its item 2, day-8 sweep :65-73).
- 2610.07457 AlignQuant: abs-read day-7 (its sweep section 3, "Abs read",
  open code noted).
Unheld or held-with-new-delta, banked below: 2609.26621 (catalog mirror row
state/arxiv/2026-09-23 only, plus one 10-03 candidate-list line; never read),
2610.11482 (day-9 candidate list only), 2609.22870 (day-3/day-4 listing
mentions; day-4 owed its abs fetch at
frontier_olm_2026-10-04/sweep/quantization-and-compression-arxiv.md:245 and
nobody discharged it until now), 2610.09202 (day-9 sweep explicitly "NOT
banked" at its :41-45), 2609.34185 (zero footprint anywhere: 0 catalog rows, 0
sweep mentions), 2610.09346 OnlineQAT (held day-9 at abstract level; delta
banked here is the first full-text read).

## Answers to the four research questions

RQ1 (schemes postdating the A/B that claim to break the ceiling tie at
single-host constraints, reproducible numbers): No scheme in this window breaks
the tie AT THE ESTATE'S CONSTRAINTS. Every decode-speedup claim rides GPU
kernels the RX 5600 XT cannot run: AlignQuant 2.50x generation over BF16 on
INT8 tile kernels across three GPUs (held day-7), Dual-QK up to 3.75x decode
at 2-bit KV via SGLang at 128K context (named day-8/day-9 as a cache claim),
MpFA 2.81x on Blackwell B200 only, PrismQuant 1.22x CUDA Graph decode. The
reproducible-numbers instrument that does transfer to any host is the held
GGUF-metadata active-parameter predictor (fit per-quant scale factors on a
reference ladder; the estate's run_ab harness already logs tok/s medians it
could fit against). The quality-side single-host datum that IS new: 2610.11482
(bank item 2) runs 1,500 scored local-agent attempts on one consumer GPU and
puts a quantized 9B at 69.3 percent artifact success in about 6.5 GB. The
ceiling tie stands at Q4-vs-Q8 on 7B janitor scut; the frontier's actual move
is sub-4-bit (CanonQ item 4, OnlineQAT item 6, held 2609.26708), which is
exactly the unmeasured cell the estate's receipt names (RECEIPT.md:100-104).

RQ2 (does OnlineQAT change the janitor tie, at what hardware cost on one
Windows host): No. Full text (html/v1, read this sitting): "All Stage 2 runs
use AdamW on eight GPUs with effective batch 64." The GPU model is never
specified, no GPU-hour or wall-clock accounting exists, and the paper's own
scope section disclaims compute-efficiency claims. Stage 2 is short (40 steps
at W3A16, 30 warmup + 120 steps at W2A16) but rolls out generation from the
quantized student against a frozen FP teacher, which the text itself flags:
"OPD incurs rollout generation". No code or checkpoint release links appear
anywhere in the HTML, so the consumption path that day-9's card planned (pull
released QAT checkpoints through Ollama) stays closed for THIS paper; the
consumable QAT artifacts remain the Gemma-4 *-it-qat tags (day-9 card probe,
still unrun). And the W2A16 average of 32.52 says two bits stay deeply broken
even with on-policy distillation, so QAT does not relocate the floor into
janitor territory; it sharpens the sub-4-bit cell only.

RQ3 (where is the quality floor below which hollow output starts, and how to
measure it): The estate stack now reads: Q4_K_M clean at >=1B (held 2610.04403,
re-verified day-9); 4-bit indistinguishable at +/-0.3 resolution (held
2609.18005); sub-3-bit failure arrives as repetitive degenerate loops, i.e. the
hollow-output signature, not as knowledge loss (held 2609.26708 day-4 Find 2);
at W2 even QAT-trained averages sit in the low 30s (OnlineQAT 32.52). New this
sitting: CanonQ's W2A4KV2 numbers (item 4) put reproducible boundaries on the
W2 cell, and 2609.26621 (item 1) hands over the measuring instrument the
STANDING_RAILS law lacks: cross-precision divergence is governed by the top-2
logit margin, so a floor probe should log per-token margin distributions, not
just end scores. The estate's 50/50 byte-identical tie is exactly what wide
margins on short tasks predict; margin telemetry on a difficulty-hardened
floor-near set (the owed RECEIPT.md:100-104 task class) is the cheap
instrument that would show the tie starting to break before scores move.
Riders already pinned (export-cast hash, serving-state pin) remain the
artifact-side guards; 2610.11482 adds the workspace-condition datum that
inspectable intermediate artifacts raise local-agent pass rates 26.7 to 52.0
points, which is the STANDING_RAILS material-must-render law's external twin:
rendered intermediate material is itself the recovery channel.

RQ4 (which of the five FP8/GPU gates is closest to lighting, any provable on
existing estate hardware): None lights and none is provable on the current box.
Gate 1 ARCH: fails hard, the box is AMD RX 5600 XT RDNA1 gfx1010, no FP8 path
(RIB_GPU_LADDER_20261001.md:5-7). Gate 2 VRAM: 6 GB against a 24 GB minimum
(rib:15; day-8 RECEIPT:62-63). Gate 3 PRICE: checked twice already, neither
trigger fires (day-8 sweep RQ4; day-8 x-sweep :113-125). Gate 4 SOFTWARE:
CUDA 12.8+ NVRTC plus vLLM/SGLang FP8 containers is NVIDIA-only (rib:19-20).
Gate 5 WORKLOAD: stays dark because 1 through 4 block anyway. This window's
FP8 papers confirm the arch wall rather than move it: 2609.22870 (item 3) is
what gate-5 demand looks like when it eventually fires (FP8 RL rollout
throughput), and its garbled-outputs failure mode under naive FP8 is itself a
floor datum; MpFA and the Blackwell softmax work are B200-only. The one
precision move provable on existing estate hardware from this sweep is not
FP8 at all: the selective FP32 LM-head recompute of item 1 is precision
bookkeeping, implementable in llama.cpp-class CPU/Vulkan stacks, and it is the
same trick class as the estate's temp-0 paired-seed discipline.

## Banked items (strongest first; quotes verbatim from pages fetched this sitting)

1. 2609.26621 Greedy Decoding Is Not Precision-Invariant: Cross-Precision
   Output Divergence in LLM Inference (TMLR 2026). Quote: "Greedy decoding
   from large language models is commonly treated as deterministic. We show it
   is not precision-invariant". BF16 vs FP16 diverges on 49 to 100 percent of
   prompts across six models; selective FP32 LM-head recomputation buys +22 to
   36 pp exact agreement on A10G at under 4 percent latency overhead for
   low-batch single-stream; the fix fails under end-to-end FP8. Banked as the
   RQ3 instrument (margin telemetry) and the sharpest external frame for what
   the estate's byte-identical tie actually measured.
2. 2610.11482 Evaluating Local Language Model Agents for Reproducible Data
   Engineering. Quote: "Local open-weight agents can support a meaningful
   subset of software-intensive data-engineering work, but reliability depends
   on model capability". 15 mobility tasks, 10 local configurations, 1,500
   scored attempts, one consumer GPU; workspace condition +26.7 to 52.0 pp;
   best config 85.3 percent artifact success; a quantized 9B hits 69.3 percent
   at about 6.5 GB. The window's best single-host quality-side datum.
3. 2609.22870 Towards Full Pipeline FP8 Reinforcement Learning for LLMs.
   Quote: "We trace this instability to a previously overlooked cause:
   compounded FP8 quantization noise distorts the importance ratio". GRPO/DAPO
   at 8B to 32B; Calibrated Clipping eliminates entropy surges and restores
   BF16-comparable performance. Discharges the day-4 owed fetch; banked as the
   gate-5 demand shape and the naive-FP8 garbled-output floor datum.
4. 2610.09202 Few Bits, One Law: Toward W2A4KV2 (CanonQ). Quote: "The
   strongest gains arise under joint W2A4KV2 compression: across
   LLaMA3-1B/3B/8B, CanonQ-Omni achieves up to 14.28x lower WikiText-2
   perplexity". Joint weight/activation/KV quantization with frozen
   codebooks; also 57.9 percent higher mean zero-shot accuracy at the extreme
   setting; +41.7 percent HumanEval and +39.1 percent GSM8K at W2A16KV16 on
   MobileLLM-Pro-1B. The W2-cell boundary for RQ3.
5. 2609.34185 EntroPack: entropy-coded weight compression at arbitrary
   bitrates. Quote: "EntroPack, an entropy-coded weight compressor that
   supports arbitrary target bitrates without activation calibration or
   fine-tuning." About 24 percent lower relative L2 weight error than NF4 at
   roughly 4 bits per parameter, in BF16/FP8/INT8 containers; own-limitation:
   decode overhead scales with weight count, so it targets prefill-heavy not
   latency-sensitive decode. Clean-zero footprint; banked for the Q1 density
   lane with its honest single-host decode caveat.
6. 2610.09346 OnlineQAT (delta bank on a held item). Quote from the full text:
   "All Stage 2 runs use AdamW on eight GPUs with effective batch 64." The
   day-9 card read this paper at abstract level only and owed exactly this:
   hardware cost and release status. Full text gives eight unnamed GPUs, no
   GPU-hours, 40/150 training steps, no code or checkpoint links. RQ2 answered
   negative for the one-Windows-host question.

## OWED / not verified this sitting

- No pytest, no Ollama run, no A/B arm fired, no lane or pin change; every
  numeric claim above traces to a URL fetched this sitting or to a named
  estate file with line cites.
- Quotes are relayed verbatim by the fetch layer; numbers for items 1, 3, 4
  and 6 cross-check against my independent export-API feed summaries; items 2
  and 5 are single-fetch (confidence field carries this).
- The difficulty-hardened floor-near task set remains the estate's owed move
  (RECEIPT.md:100-104); margin telemetry (item 1) is proposed as its
  instrument, not yet specced.
- 2610.11482's model identities beyond the 9B quantized row are not on the
  abs page; full text not read.
- The 13-pattern recursive overlap loop over catalog+memory+watch+state was
  killed for slowness after its catalog-only prefix completed; the per-ID
  watch/inbox walk and targeted memory greps that decided every bank verdict
  did complete.
