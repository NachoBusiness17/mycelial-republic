# Sweep: quantization-compression via Reddit (frontier_olm 2026-10-10)

source-fetched: 2026-10-10

Seat: sweep-quantization-compression-reddit. Feeds the 10-08 quant A/B receipt
(TIE AT CEILING: qwen2.5:7b Q4_K_M vs q8_0, 50/50 both arms, speed the only mover,
Q4 median 6.90 vs Q8 3.00 tok/s, frontier_olm_2026-10-08/sweep/quant_ab/SUMMARY.json;
burns lens section 2b, frontier_olm_2026-10-09/lens/burns.md:91-98), the five GPU
adoption gates (RIB_GPU_LADDER_20261001.md:10-23; box = RX 5600 XT RDNA1 gfx1010,
no FP8 path, :5-7), janitor sizing (configs/lanes.yaml:28-41), and the OnlineQAT
register row (2610.09346, state/arxiv/2026-10-08/2610.09346v1.txt + the day-9 steal
card watch/inbox/frontier_olm_2026-10-09/steal/quantization-compression.md).

## Doors (all probes this sitting, 2026-10-10)

- Recipe door old.reddit.com/r/LocalLLaMA/top.json: LOGIN-WALLED, not JSON. WebFetch
  and the web_reader MCP both returned the wall verbatim: "Log in to use old Reddit.
  To keep Reddit safe, accounts are required to access old Reddit." Same for the
  old.reddit HTML door (JS-gated landing page). www.reddit.com/top.json: HTTP 403
  Blocked. Same class as the 10-09 doors lens recorded (lor2).
- Recipe fallback (WebSearch site:reddit.com): DEGRADED. The backend ignored the
  site: syntax (returned non-Reddit results), then 1302 rate-limited five straight
  attempts during my burst; single sequential attempts later returned only non-Reddit
  rows. No fallback success claimed.
- WORKING DOOR (inherited from the 10-08/10-09 receipts): www.reddit.com/.rss via
  curl -A "research-sweep/1.0" with pacing. GREEN this sitting:
  r/LocalLLaMA search q=quantization t=month limit=100 (HTTP 200, 639,817 bytes,
  100 entries, 2026-09-19 through 2026-10-10); r/LocalLLaMA search q=QAT t=year
  (200, 209,358 bytes, 25 entries); r/MachineLearning top/.rss t=month (200, 77,530
  bytes, 25 entries; GREEN today where it 429'd on 10-09); r/LocalLLM top (200,
  77,841 bytes, 25); r/ollama top (200, 117,910 bytes, 25). Thread /comments/<id>/.rss:
  200 on nine threads; 429s hit in bursts and cleared on 75-240s backoffs.
  RED: r/LocalLLaMA top/.rss stuck 429 across three backoffs (90s, 180s) - covered by
  the search+ML+LocalLLM+ollama listings instead; the r/ML thread 1wgzpli stuck 429
  (100s, 240s backoffs) - OP body recovered from the cached top-month RSS entry,
  comments read from the estate's own day-8 intake
  frontier_olm_2026-10-08/sweep/_raw/fa_comments_1wgzpli.json.

## Pass 1: broad sweep (candidates considered, last 30 days)

Discovery corpus: 100 (quantization search) + 25 (QAT search, mostly out-of-window
Gemma-4-QAT context rows) + 25 (r/ML top) + 25 (r/LocalLLM top) + 25 (r/ollama top)
= 200 rows, deduped against the 10-09 sweep's 30-item list and the 10-08 sweep's
39-item list. Genuinely new in-window rows (posted after the 10-09 morning fetch or
never listed before), date | title | id:

1. 2026-10-10 | Basalt: Flash-Next at 665 tok/s structured, 354 prose on a 5090 +
   5060 Ti (2.6x Strata) (1x223ai)
2. 2026-10-10 | How to create my own benchmarks
3. 2026-10-09 18:41 | Qwen 3.8 Flash Next-GSQ-RCO-IQ2_XS at ~21 tok/s on just an
   RTX 3060 12GB + 16GB DDR4 RAM (1x1tclb)
4. 2026-10-09 22:54 | Qwen3.8-27B UD-IQ4_XS Heretic + MTP on a 16 GB card with
   55-68 tok/s (1x1zhnx)
5. 2026-10-09 | A 24KB stand-alone HTML-LLM (toy, skipped)
6. 2026-10-08 | $2800 rig with 8x Radeon Pro V620 (held, day-8 bank item 8)
7. 2026-10-08 | [2506.13771] LittleBit (held, day-8 bank item 6)
8. 2026-10-08 | Comparing Qwen3.8-27B fine-tunes and baselining vs frontier
9. 2026-10-07 | 2x CMP 170HX 64GB: GLM-5.3-Flash at 384K context / ~90 tok/s (1x0b1ws)
10. 2026-10-07 | Can I run Swift 1.5 flash next iq3xxs in 16GB VRAM
11. 2026-10-06 | Qwen3.8-27B (Q6_K_XL) 110+ TPS at 256k ctx, KV buffer decoupled
12. 2026-10-06 | If you benchmark llama.cpp on AMD with official ROCm builds (held,
    day-8 bank item 2)
13. 2026-10-06 | DeepSeek V4.1 Flash on a DGX Spark: 113.6 GB VQ base + sidecars
14. 2026-10-06 | Benchmark: Local LLMs on Orange Pi 5 Plus (NPU offload)
15. 2026-10-06 | I quantized GLM-5.3-UNCENSORED to MXFP4 for AMD GPUs (1wz4vh6)
16. 2026-10-05 | k_llama.cpp MoE Optimizations: Expert Residency, Hybrid CPU/GPU,
    Q2_0 Support (1wynomx)
17. 2026-10-05 | 4-bit Qwen2.5 closer to fp16 than official AWQ (held, day-8 item 1)
18. 2026-10-05 | Infermeld: one GGUF across AMD + NVIDIA
19. 2026-10-03 | Running Qwen3.8 Flash Next 176B on a 16GB 3080 laptop
20. 2026-10-02 | Heavily quantized Qwen3.8-Flash vs Q8 Qwen3.8-27B (held, day-8
    item 4; re-read this sitting for its unquoted instruments, below)
21. 2026-09-29..10-09 held set from 10-09: 1x1bdvl, 1x1dt7q, 1x18bsm, 1x13fo2,
    1wzrw6x banked; 1ww528l, 1wpvep4, 1wtkzc5, 1wj6c4l held.
22. 2026-09-23 | GGUFs in transformers natively (stack-floor context)
23. 2026-09-22 | Dynamic Quantiser
24. 2026-09-21 | Splash Engine native 8-bit on Apple Silicon
25. 2026-09-20 | Postulate: context compaction is good for quantized models (held,
    day-8 read-not-banked)
26-30. r/ML: 44M ternary SHADOW (held, 10-06 bank, two sweeps); arXiv two-per-month
    limit; ICML spotlight row; misc non-quant. r/ollama: hallucination detection
    1.5B-120B (held via day-8 finetuning sweep drop list); DwarfStar (discovery-only
    again); 400+ agents on Qwen3-4B; M4 Max 27B bench. r/LocalLLM: 35B MoE
    self-host; dual-3080 40GB server; Gemma-5 expectations.

Out-of-scope: rig-price threads, "No think doesn't work", Billy Bass.

## Pass 2: deep reads (9 threads read this sitting; 6 banked, 3 held-deltas)

Raw RSS cached in _raw/ (thread_<id>.rss). Held threads re-read for their unquoted
instruments only, NOT re-banked.

### BANKED 1. 1x1tclb (2026-10-09 18:41, /u/zyxciss) - GSQ-RCO IQ2_XS at 21 tok/s on
a 3060 12GB + 16GB single-channel DDR4, via --moe-direct-io expert prefetch

Read in full (28 entries + full OP table). Stock llama.cpp mmap on the 68GB IQ2_XS
build: 1.41-2.12 tok/s, 1,140-1,565 major page faults/token, 208-312 MB/token SSD
I/O. Blocking demand-only version: 0.73 tok/s. Prefetch version: 20.14-21.13 tok/s,
~0 major faults, output BIT-EXACT to stock ("we're not getting those numbers by
dropping experts"). Tested under cgroup MemoryMax=6G. Honest rough edges: cold
start 3.5-4.5 tok/s, prefill struggles, and MTP speculation can HURT under SSD
offload (verifying 2-3 tokens loads the union of expert sets; confidence-gated
min-p 0.8 or suffix lookup better). OP's confession about v1: "doing that on an
already quantized model was hurting output quality and coherence" (pruning experts
for speed). Comment [3] supplies the audit instrument: /usr/bin/time -v major page
fault count to separate real prediction wins from a lucky page cache.

### BANKED 2. 1x1zhnx (2026-10-09 22:54, /u/ZestRocket) - Heretic UD-IQ4_XS + MTP on
16GB, with a per-quant KLD-vs-Q8 ladder

Read in full (20 entries). Copied Unsloth's per-tensor UD recipe onto llmfan46's
BF16 Heretic (uncensored Qwen3.8-27B, MTP head preserved), made 12/16/24GB builds,
measured mean KLD vs Q8_0 of the same weights on TWO domains (wikitext-2 prose /
llama.cpp source code): UD-Q5_K_XL 19.44GiB 0.0045/0.0037; i1-IQ4_XS 14.26GiB
0.0202/0.0149; UD-IQ4_XS 13.27GiB 0.0268/0.0192; Q3_K_M 0.0639/0.0456; i1-IQ3_M
0.0649/0.0465; UD-IQ3_XXS 10.18GiB 0.0904/0.0587; i1-Q2_K 0.1551/0.1017. Speed on
4080 (llama.cpp b11457, 15K prompt, 32K ctx, MTP 2 drafts, mean of 3 fixed seeds):
UD-IQ4_XS 55 tok/s code / 50 prose vs 29/29 without MTP. "2 draft tokens beat 3"
(68 vs 56 code at 40K; fewer rejected drafts). Bottleneck ranking: "VRAM by far...
once everything fits it's basically bandwidth and smaller file goes faster, MTP
acceptance was pretty much the same on every quant." AMD datum in replies: n=2 MTP
drafting also wins on R9700. Ninfer cross-check in-thread: same 10.2GB IQ3_XXS file
103-110 tok/s vs 70 in llama.cpp at 24K, holds ~80 tok/s at 23K where llama.cpp
drops to ~50.

### BANKED 3. 1x223ai (2026-10-10 00:58, /u/jesdga95) - Basalt: Blackwell-only Strata
fork, 2.6x Strata, plus the engine-KLD-fidelity check

OP + key exchange read (75 entries total). 665 structured / 354 prose tok/s at
IQ3_XXS on 5090+5060Ti (9950X, 32GB DDR5), 7,317 prefill at 64k; single 5090: 585/
316. Weights re-packed not re-quantized (.basalt file). Linux only, explicitly
strips AMD/Intel/pre-Blackwell NVIDIA. The load-bearing comment pair: critic
Hefty_Wolverine_553 calls the engine class "vibeslopped" - "optimizations that
actually lobotomize the model to get speedups, e.g. quantizing activations, weird
sampling settings (strata defaults to temp 0...)"; author answers with an engine
fidelity proof: "llama.cpp own KLD tool on the same IQ3_S GGUF vs Q8_0 gives KLD
0.175 / 89.2% top-1, Basalt measures 0.177 / 89.4%." Further scoping: s2d4 warns
"you can actually have lower KLD but not perform better than a lower quantization";
EXL3 suggested for better quality-per-size at some speed cost.

### BANKED 4. 1x0b1ws (2026-10-07 22:59, /u/Prudent_Appearance71) - 2x CMP 170HX
64GB HBM residency for GLM-5.3-Flash EXL3 3.05bpw at 384K ctx, plus a KLD
comparability clinic

OP + methodology exchange read (47 entries). Two unlocked CMP 170HX 64GB mining
cards (SM80, HBM, PCIe Gen2 x8, no P2P) hold the 320B-total/18B-active MoE fully
resident at 3.05bpw EXL3 (trellis bit allocation per tensor, not uniform 3-bit),
384K context in actual use, ~90 tok/s decode; compared on the same machine (5600X,
80GB DDR4) against Qwen3.8-Flash-Next AWQ INT4 + FP8 PLE on vLLM with DSH agent
tasks for task-completion time. The comment exchange is a KLD-methodology lesson:
"You can't compare two KLD benchmarks from two different tests like this"; OP
corrects the table, marks his checkpoint "not directly measured", cites an
independent artifact measurement (0xSero GLM-5.3-Flash EXL3 3.0bpw: KLD 0.050501,
92.997% top-1 over 51,175 positions); turboderp's chart places EXL3 3-bit at ~IQ4_XS
and EXL3 4-bit at about half the KLD of IQ4_XS.

### BANKED 5. 1wynomx (2026-10-05 23:33, /u/IceFog72) - ik_llama.cpp fork: expert
residency, bandwidth-adaptive CPU/GPU, Q2_0

Read in full (8 entries). Adds --moe-resident auto / --moe-resident-mib N (cap the
resident-expert VRAM cache; auto fills all free VRAM), profiler options, Q2_0
support sized for ISTA-DASLab GSQ-RCO Coder GGUFs, credits jadidbourbaki's n-gram
cache PR, integrates expert-residency ideas from arXiv 2608.16157 adapted to the
scheduler + quantized kernels. Concrete run: GSQ-RCO IQ1_M coder 2-shard, KV q4_0
with Hadamard caches, --defer-ple: 98.27 tok/s prefill / 10.26 tok/s decode.
Honest boundary: "this only helps when the full MoE does not fit in VRAM and the
GPU still has unused compute capacity, and free pci bus speed." Gemma-26B-a4b
needs --swa-compress on this fork (janitor-family datum). Upstream PRs intended.

### BANKED 6. 1wz4vh6 (2026-10-06 15:02, /u/bakatristan) - MXFP4 GLM-5.3-UNCENSORED
for AMD GPUs, converted with AMD Quark on MI355X

Read in full (4 entries, thin thread). dealignai's FP8 -> MXFP4, 423.75GB /
394.65GiB (~44% smaller than FP8 source), "Expert weights use MXFP4; attention,
routers and other sensitive layers stay at higher precision", README carries
source revision + validation results; scripts uploaded. Datacenter-class (MI355X
conversion host), not estate-provable, but it is the first open AMD-Quark MXFP4
weight set the sweep has seen: SOFTWARE-gate signal for the AMD lane, needs
MXFP4-capable silicon (MI/RDNA4), which the 5600 XT is not.

### HELD re-reads (not re-banked; deltas only)

- 1wvzmt3 (held, day-8 item 4; 85 entries re-read this sitting): the day-8 card
  quoted the top two answers only. New instruments now in evidence: (a) KLD
  thresholds from deadatreides1 - "Run llama-perplexity with --kl-divergence
  against the base on your own prompts. On gpt-oss I ended up treating KLD up to
  0.003 as 'can't tell the difference' and up to 0.01 as 'cheap but fine'"; (b)
  the tok/s ceiling formula - "The Q8 27B touches 25.4 GiB of weights per token...
  Divide your RAM bandwidth by that and you have the ceiling"; (c) answer-flip
  counter from gxcsoccer - on a 4B decision task, "8-bit gave the same answer as
  the original 119 times out of 120", while "4-bit... changed about 30% of the
  answers" with chat feeling identical; (d) LCBv6 quant ladder from
  Material-Database-24: Flash-Next BF16 91.9 / IQ3_XXS 86.29 / Q2 81.14, 27B BF16
  90.3 / Q4 ~86, "both stay about 95-98% of baseline at quants up to these points";
  (e) Bonsai-2 KLD corroboration (0.0011 vs 0.00022 between two int8 activation
  paths, "KLD catches differences PPL hides").
- 1wyc2b0 (held, day-8 item 1): re-read to confirm its 3-bit floor line ("loses
  more than half of code and math ability") is already in the day-8 card. It is.
- 1wgzpli SHADOW-50M (held, 10-06 bank in two sweeps): completed the day-9 OWED
  verification this sitting (OP via r/ML top RSS + comments via the estate's day-8
  cached JSON). Delta worth carrying: the comment thread contains an EXECUTED
  adversarial ablation (CarefulHamster7184's self-confirming-trail attack -> OP's
  fix commit v1.1.2, trail restricted to tie-breaking, rival-link decay) and the
  trigger-miss instrument question from Deep_Ad1959: "how often does it decide not
  to emit [calc] when it should?... that is the failure i would want counted
  separately."
- 1wzdti3 (held, day-8 item 2): no delta; still the ROCm silent-CPU-fallback
  receipt, quality-invisible by perplexity, caught by wall-time ratio or rocm-smi.

## Overlap check (run this sitting)

- catalog/catalog.jsonl greps (case-sensitive fixed strings): 1x1tclb 0, 1x1zhnx 0,
  1x223ai 0, 1wz4vh6 0, 1wynomx 0, 1x0b1ws 0, moe-direct-io 0, Basalt 0,
  SHADOW-50M 0 hits in the load-bearing subtrees (full-tree walk not completed:
  the 1wgzpli row exists as day-8 raw intake, catalog.jsonl:1013759). "Heretic" in
  memory/ = 5 hits, all an X-URL mention of a DavidAU Heretic-named GGUF inside
  memory/runs/compaction_eval + forge_daemon prose (context-checked 2 files), not
  the KLD-ladder thread banked here.
- Prior frontier windows (09-30 through 10-09, sweep/ + steal/): 1x1tclb, 1x1zhnx,
  1x223ai, 1wz4vh6, 1wynomx, 1x0b1ws, moe-direct-io, Basalt: ZERO hits. SHADOW-50M
  matched the 10-06 quantization + finetuning sweeps (prior bank, hence held). The
  170HX class appears in 10-03 arctic_LocalLLM harvest JSONs as raw intake of an
  earlier 4-card thread, never banked as claims.
- Non-exhaustive-walk disclosure: the full memory/ recursive grep was stopped
  (biography-knot unreadable-path exits, same class the 10-09 card recorded); the
  bounded pass covered memory/frontier, percolator, steal_lens, improve, research,
  runs, rib, workflows with --include md/json/jsonl. memory/trajectory/steps.jsonl
  will now contain today's own fetch ids (self-contamination, disclosed).

## Answers to the four questions

Q1 (does anything postdating the A/B break the ceiling tie at single-host, with
reproducible numbers?): NOT on the weight-quality axis at Q4+ - every in-window
ladder (LCBv6 95-98% of baseline through Q4/IQ3_XXS; KLD 0.0045 at Q5_K_XL vs Q8;
the A/B's own 50/50) says the Q4 rung stays at ceiling. What moved is the DELIVERY
axis, and it moved an order of magnitude: bit-exact expert-IO orchestration
(1x1tclb: 10-15x at identical bits, cgroup-bounded, page-fault-audited), expert
residency with honest boundary conditions (1wynomx), MTP tuned to 2 drafts
(1x1zhnx: 1.7-1.9x, fixed seeds, acceptance invariant across quants), and HBM
residency of sub-4-bit trellis quants on secondhand mining cards (1x0b1ws). The
reproducibility currency has shifted from vendor rows to KLD-vs-Q8 + top-1 with
position counts, fixed-seed tok/s means, page-fault counters, and cgroup bounds.

Q2 (OnlineQAT for janitor class, Windows host): OnlineQAT itself has NO reddit
footprint in-window (searched q=QAT t=year; nothing newer than the estate-held
2610.09346 discussions) - the question stays where the day-9 card left it, and no
in-window thread reproduces W3A16/W2A16 on a Windows host. OWED, not guessed. The
transferable in-window QAT-adjacent facts: Google's Gemma-4 QAT line is the
production QAT existence proof but is q4_0-aligned and out the 30-day window
(discovery context only); if QAT checkpoints are adopted, pair them with MTP n=2
not n=3 (1x1zhnx) and do NOT expect MTP gains under SSD-offload MoE (1x1tclb);
and the janitor-class floor risk is quant x stack interaction, e.g. Gemma-26B-a4b
needing --swa-compress on the ik fork (1wynomx).

Q3 (hollow-output floor and how to measure it): the floor is TASK-SHAPED and
DOMAIN-SHAPED, not ppl-shaped - ppl stays close while code/math/agentic collapse
(held 1wyc2b0: at 3 bits "loses more than half of code and math ability"). The
in-window instrument set, convergent across five threads: (1) per-domain KLD vs a
Q8 reference of the same weights, with calibrated bands (0.003 can't-tell, 0.01
cheap-but-fine; 1wvzmt3) and a published ladder (1x1zhnx); (2) answer-flip rate on
fixed real inputs vs Q8 (119/120 at 8-bit, ~30% flips at 4-bit on decision tasks;
1wvzmt3); (3) a fixed capability probe that a sub-floor model visibly fails
(1wvzmt3: q3 failing a "pretty simple problem"; looping and malformed tool calls
reported at IQ3_XXS-class rungs); (4) engine-fidelity KLD (same GGUF through two
engines; 1x223ai) so a runtime swap cannot lobotomize silently; (5) trigger-miss
counting for tool/calc paths (SHADOW comments). Scoping law from 1x223ai: lower
KLD does not strictly imply better task output - KLD is a covariate, the
material-must-render gate stays primary. For quant_ab this means three addable
covariates: per-domain KLD vs q8_0, answer-flip rate, backend-engagement proof.

Q4 (which of the five gates is closest to lighting; provable on estate hardware?):
ARCH remains hard-fail for this box - nothing in-window changes RDNA1's lack of an
FP8 path (Basalt explicitly strips AMD; MLX FP8 staging is Apple M5/M6; MXFP4-AMD
exists but needs MI/RDNA4 silicon). The gates with in-window movement are SOFTWARE
(AMD Quark now emits open mixed-precision MXFP4 weights with validation READMEs,
1wz4vh6) and PRICE TRIGGER (secondhand 64GB HBM mining cards running 3.05bpw EXL3
at 384K, 1x0b1ws; 8x V620 256GB for ~$2800, held day-8) - both on non-estate
silicon, both still above the rib's per-dollar line where "the quant lane keeps
winning." WORKLOAD stays unlit (no real FP8/MoE QPS demand). Provable on the
existing 5600 XT + 64GB host TODAY: the delivery-axis and instrument steals -
KLD/floor instruments (llama-perplexity --kl-divergence is CPU-runnable),
answer-flip covariates on quant_ab, backend-engagement checks before any future
speed read (held ROCm-trap receipt: quality-side checks cannot catch silent CPU
fallback), and the expert-residency shape at llama.cpp scale once a non-CUDA path
exists (ik_llama is CUDA today). No FP8 gate is provable on this hardware; state
it plainly.

## Honesty notes

- Reddit doors: recipe JSON doors login-walled/403; RSS door green with pacing;
  WebSearch fallback degraded both by ignored site: syntax and 1302 bursts - no
  fallback success claimed.
- Scores/comment counts unavailable via RSS; "strongest" = fit to the four
  questions + depth read.
- Every quote is a verbatim substring of the cached _raw/*.rss text fetched this
  sitting. Nothing quoted from search snippets.
- The six banked items were each read end to end this sitting (entry counts: 28,
  20, 75-OP-and-key-exchange, 47-OP-and-key-exchange, 8, 4). Three held threads
  were also re-read for delta instruments; their holdings are cited, not re-claimed.
- No local probe fired, no A/B re-run: sweep seat, no burns-lane authority. The
  TIE stands as receipted.
