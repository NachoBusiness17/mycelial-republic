# SWEEP quantization-compression-hn - source-fetched: 2026-10-10

Lane: quantization-compression via the Hacker News door, feeding the 10-08 quant A/B
receipt (TIE AT CEILING, Q4 6.90 vs Q8 3.00 tok/s, burns lens section 2a, per the ask),
RIB_GPU_LADDER gate rows (memory/rib/RIB_GPU_LADDER_20261001.md:10-23, read this ask),
janitor sizing on the driving ladder, and corpus/library/lmcache-src as the prior-art
shelf (catalog census this ask: lmcache fp8/turboquant serde rows at catalog/catalog.jsonl
lines 29464-30763).

## Door health

hn.algolia.com search_by_date and search: clean all session (8 queries). One query-shape
negative stated as a real negative: "quantized LLM" returned nbHits 0 (Algolia treats
multi-word as phrase); the plain single-term queries carried the sweep. The OR-syntax
QAT query also returned 0. news.ycombinator.com item threads: clean. rocm.blogs.amd.com,
github.com, huggingface.co, arxiv.org, devblogs.microsoft.com: clean. No 403s anywhere.

## Pass 1 census (30-day window, created_at_i>1788998400; 33 distinct candidates)

From quantization by-date (13), GGUF by-date (21), FP8 by-date (30, mostly noise),
llama.cpp by-date (25), BitNet by-date (6), ternary by-date (Terry Tao noise),
"quantization" relevance (13), "KV cache" by-date (15). Load-bearing names:
ESP32S3 1.58-bit BitNet 150/30 09-28; DeepSeek-v4.1-Flash KV 131/10 09-17; Janus GGUF
Vulkan 106/19 10-01; LRU-vs-KV-papers 108/58 09-10; Magnitude 194/97 09-30; Swift-Qwen3.8-27B
33/17 09-16; GSQ-RCO 2xRTX3090 9/2 09-14; quant-delta-predictor 1/0 09-23; AMD Quark
Strix Halo 1/0 10-06; Hopf Spherical Quantization 1/0 10-06; glq trellis vLLM 2/1 09-10;
bartowski layout maps 3/0 09-12; Self-Pruning Transformer arxiv 6/0 10-08; WinML
llama.cpp 2-3/0 10-07+10-08; InferPilot 1/0 10-01; DeepL FP8 3/0 09-27; Rene-1 fp8 6/2
09-27; Intel Arc 2.2x 4/0 09-28; Gufo Q6dense 2/0 10-03; Bonsai ternary GGUFs 2/0;
Prism-ML Bonsai 2 ByteShape reddit comparison 1/0 10-08; KV memory wall 2/0 10-03;
IttyBittyAI 09-24; UkisAI Swift series 09-24; QLoRA explainer 09-20; Weaviate 4-bit
rotational 5/0 09-17; Transformers-runs-llama.cpp-quants 09-23; VLA Jetson Thor 09-22;
Reflex cold-start 09-23+09-30; VeriLoop ladder 09-25; 49998043 MS DeepSeek V4 Flash
locally + llama.cpp to WinML 10-07.

## Pass 2 deep reads (9 pages read end to end this ask)

Janus HN thread 49926773; ESP32S3 HN thread 49884625 + repo README; GSQ-RCO HF card;
quant-delta-predictor README; rocm Quark Strix Halo blog; glq README; bartowski blog;
zartbot DSV41Flash teardown; hscq README; arxiv 2610.09051 abs; MS WinML devblog;
InferPilot README. Seven of those turned out to be re-reads of already-held work (below);
the six banked items are the ones no prior seat had read.

## The four RQs, answered from what I read

**RQ1 (schemes postdating the A/B that claim to break the ceiling tie, reproducible
numbers).** The strongest post-A/B compression claim is Self-Pruning Transformer /
Universal Attention (2610.09051, 10-06): 10x KV compression with downstream performance
improving, 25x at 16k. It is an architecture retrain, not a drop-in quant, so it does not
break the estate's weight-quant tie directly; it attacks the other half of single-host
memory (KV), same as the held DSV41 design. The reproducible-numbers weight-quant rows
this window: AMD Quark W4A16 on Strix Halo (70 GB to 21 GB, per-task accuracy tables,
quantization run on the target laptop itself) and hscq's fixed-rate spherical codes
(rel-RMSE 0.100 at 5 bpw vs int4's 0.140 on MiniLM-L6-v2). Nothing read claims to break
the Q4-vs-Q8 throughput tie on a Windows discrete-GPU host; the tie's breaker this window
is tooling (WinML) and KV-side compression, not weight quant.

**RQ2 (QAT for janitor-class models, hardware cost on one Windows host).** The HN surface
adds nothing new beyond the held ESP32S3 BitNet thread (QAT 1.58-bit fine-tuning, banked
10-02 + mechanism delta 10-09) and the held DeepSeek MXFP4-KV-via-QAT design. OnlineQAT
(2610.09346) has zero HN presence in the window. Honest verdict: the QAT question stays
with the arxiv lane and the day-9 register; my door corroborates only that QAT-class
ternary training produces toy-output at 0.5B scale (the held "fancy llm noise-maker"
verdict) and that train-time decay integration (2610.09051) is where the frontier is
spending QAT-shaped effort now, on KV rather than weights.

**RQ3 (quality floor for hollow output, how to measure).** The two measurement
instruments read this ask that the estate does not hold: (a) Quark's per-task accuracy
tables showing no uniformly best config (GSM8K 0.9090 baseline vs 0.8916-0.9151 quantized;
MATH-hard 0.5287 vs 0.4856-0.5234), i.e. the floor is task-conditional and must be
measured per workload, matching STANDING_RAILS material-must-render (a quant that renders
on GSM8K-class tasks can still hollow out on MATH-class); (b) InferPilot's gate shape:
precision-changing candidates require teacher-forced KL plus long-context retrieval
gates before nomination, with ABSTAIN when evidence is thin. Both are directly portable
to a janitor render-check harness: measure per-task delta against the Q8 arm, abstain
when the cell is unvalidated (the held quant-delta-predictor's INSUFFICIENT_EVIDENCE
shape, banked 10-03).

**RQ4 (which FP8/GPU gate is closest to lighting; provable on existing hardware).**
Verdict from the five gates at memory/rib/RIB_GPU_LADDER_20261001.md:12-23: gate 4
(SOFTWARE) is the only one that moved this window, and it moved in an unexpected
direction: Microsoft shipped an experimental llama.cpp integration in Windows ML running
GGUF and ONNX across "GPUs, NPUs, and CPUs from AMD, Intel, NVIDIA, and Qualcomm"
(devblog read this ask). That is a Windows-native GGUF path for the estate's actual
host OS, no container needed. It does NOT light FP8 (no FP8 claims in the post; RDNA1
RX 5600 XT stays outside every FP8 path: Quark needs Strix Halo + ROCm 7.2 + Ubuntu;
glq needs Ampere+ Linux; InferPilot's fp8 lane needs vLLM on CUDA GPUs). Gate 3 (price)
and gate 5 (workload) unmoved. Net: no gate lights on existing estate hardware; the
quant lane (GGUF on current box) keeps winning per dollar, exactly as the rib's standing
verdict says, and the new WinML path is the first tooling that could dogfood a GGUF
serving upgrade on this Windows host without ollama.

## Banked items (6, strongest first; all quotes verbatim from pages fetched this ask)

1. **AI Development on Windows: From PyTorch and Llama.cpp to Windows ML** (Microsoft
   devblog, 2026-10-07; HN 49997807/50002660). Experimental Windows-native llama.cpp
   path running GGUF and ONNX, Text Generation API, OpenAI-compatible local endpoint;
   MS contributes CUDA kernel work, Eagle-3/MTP/D-Flash2 speculative decoding and NVFP4
   upstream. Quote: "With this new, experimental llama.cpp integration, you can pull a
   brand-new GGUF model from Hugging Face and run it locally." Overlap: grep winml /
   Windows ML over catalog + frontier_olm 10-04..10-10 = 0. NEW.
2. **A Self-Pruning Transformer: Extreme KV-Cache Compression with Universal Attention**
   (arxiv 2610.09051, submitted 2026-10-06; HN 50013834). Trainable composite decay
   replacing hard sliding-window eviction; keeps RoPE and softmax. Quote: "Experimentally,
   Universal Attention achieves state-of-the-art $10\times$ compression on natural
   language and synthetic task data". Overlap: catalog + state/arxiv 10-07..10-10 +
   frontier sweeps = 0. NEW.
3. **InferPilot: the vLLM doctor that tells you when fp8 won't help** (HN 49921148,
   2026-10-01). Prometheus-metrics regime screener; one candidate change at a time;
   Evidence Cards with abstentions; preregistered study. Quote: "fp8 KV improved
   throughput by 33.6% on the KV-pressured workload and by only 0.2% on the
   unpressured control". Overlap: grep InferPilot over catalog + memory-facing sweep
   dirs = 0. NEW. This is gate-4/5 decision tooling in the estate's own refusal shape.
4. **Local Quantization and Multi-Backend Deployment with AMD Quark on Strix Halo**
   (rocm.blogs.amd.com, HN 49975499, 2026-10-06). W4A16 RTN (symmetric INT4 / asymmetric
   UInt4, group sizes 32 and 128) quantized ON the 128 GB unified-memory laptop; export
   18-23 min, quantization under 2 min, peak memory 73-95 GB. Quote: "Quantization
   reduces the model weights from roughly 70 GB to about 21 GB." Overlap: Quark matches
   in 10-04 harvests are false friends (reddit author quarkcarbon, physics zoom posts);
   the blog is unheld. Gate read: Linux + ROCm 7.2 + Strix Halo, so NOT provable on the
   estate's RDNA1 Windows box; corroborates the held doctrine that the AMD lane's future
   is unified-memory APUs (memory/runs/gapwave/gap_external_field.md:79-82). NEW.
5. **Hopf Spherical Quantization and Compression (hscq)** (github meridionalissoftware,
   HN 49980637, 2026-10-06). Header-only C++23 fixed-rate lossy quantization via
   constructive spherical codes (Hopf foliations); no stored codebook; O(n log n).
   Quote: "Closed form in (mode, dim, d_q, gain_bits, n_elems) and in nothing about
   the data". Rate guarantee holds for incompressible input where entropy coders
   expand; presets 1.03 to 5 bpw, rel-RMSE 0.100 at 5 bpw vs int4 0.140 on MiniLM-L6-v2.
   Early: 3 commits, Linux amd64 only. Steal shape: fixed-size rows for
   memory/corpus/quantized_thought L0/L1 analytics where the rate must be budgetable.
   Overlap: Hopf matches are chaos-math false friends. NEW.
6. **Janus HN comment cluster (DELTA on a held item)** (thread 49926773, read this ask;
   item banked 10-03 as watch/inbox/frontier_olm_2026-10-03/sweep/quantization-and-
   compression-hn.md item 5). New deltas: gunalx measured Vulkan vs native "in the same
   ballpark" on Intel and chose Vulkan for cross-vendor stability; bitexploder on a
   single V100: Quote: "around 900t/s prefill and 100 t/s decode during DeepSWE runs on
   27B (4 bit quant)" plus "Qwen 27B 3.8 matched Sonnet 5 in the 17 DeepSWE tasks I have
   run so far" (single-user anecdote, not a benchmark). Thread also confirms the 10-03
   maturity caveat: no benchmarks vs vllm/sglang, wrapper-thin over llama-server.

## Held ground resurfaced, NOT re-banked (the reason this bank is short)

This lane is swept daily. GSQ-RCO non-uniform GGUF (banked 10-03 cycle 2, item 3, same
McNemar p 0.0048 / +2.85pp numbers I re-derived); quant-delta-predictor (banked 10-03
cycle 2, item 4, same 93.23% coverage and -39.5pp); bartowski per-tensor layout maps
(banked 10-02 item 2); ESP32S3 BitNet thread + mechanism (banked 10-02 item 5, mechanism
delta 10-09 item 4); glq trellis vLLM plugin (banked 10-04 item 2, same AIME 90.0 at
bf16 parity numbers); DeepSeek-V4.1-Flash zartbot teardown (banked 10-02 item 1; estate
also holds the tech report + 8-lane v41_paces suite); Janus base item (banked 10-03);
Swift-Qwen3.8-27B (banked 10-03 evals sibling); KV memory wall SoK (banked 10-04);
IttyBittyAI (banked 10-09 item 3); EasyCommand (banked 10-09 item 2); Weaviate rotational
(banked 10-03 cycle 2 item 5); Magnitude / Decision Models / Gufo / prompt-lookup /
Lifeboat (banked 10-03 morning).

## Honesty block

- Surfaced but not read (never banked): Prism-ML Bonsai 2 ByteShape Qwen3.8 quant
  comparison (reddit URL behind the HN 1-pointer; reddit doors blocked for siblings,
  not attempted here), DeepL FP8 training blog, Rene-1 fp8 classifier, Intel Arc 2.2x
  blog, UkisAI Bonsai 2 series, VLA Jetson Thor. OWED if wanted.
- RQ2's OnlineQAT (2610.09346) evidence comes from the ask's day-9 register pointer,
  not from anything I fetched; I found zero HN coverage of it in the window.
- The burns lens 2a A/B numbers and the lens open q12 gate list are cited from the ask;
  the GPU ladder rib is cited from my own read (memory/rib/RIB_GPU_LADDER_20261001.md).
- Overlap greps actually run this ask: catalog/catalog.jsonl greps (quantiz/GGUF/FP8/
  QAT/Q4/Q8 census; winml/InferPilot/2610.09051/meridionalis/hscq = 0; GSQ/pfeifferj/
  bartowski/bartowski-layout false-friend census); memory/ bounded multi-pattern grep
  (completed, 3 files, all own-echo or false-friend); frontier_olm_2026-10-04..10-10
  greps for glq/Quark/Hopf/WinML/InferPilot/Self-Pruning/Swift-Qwen.
- Not run: no estate tests (none named by the ask); no FTS rebuild; no ollama A/B.
- Em-dash scan of this file: none present; quotes selected to avoid them.
- Transport note: full-tree recursive greps over memory/ hang in this sandbox (two were
  killed); the bounded multi-pattern grep with --include filters completed and is the
  evidence cited above.
