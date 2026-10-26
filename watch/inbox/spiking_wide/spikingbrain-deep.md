# SPIKINGBRAIN-DEEP: the full paper, the weights, the run-path (2026-10-01)

Lane: gala spiking-wide / spikingbrain-deep (division B). Dug the primary:
arXiv 2509.05276 full text (v1 and v4, all key numbers byte-identical across
versions), the official GitHub repo, the actual weight hosts, and this box's
hardware. Byte transcript: `watch/inbox/gala_20260925/spiking-wide/lanes/
spikingbrain-deep.check.txt`. Raw artifacts: same `lanes/` dir (`sb_*` files).

## 1. The TTFT table (the ~100x claim, exact terms)

v1 Table 4 / v4 Table 7. Config: SpikingBrain-7B under sequence parallelism
(ZeCO on the linear-attention module, P2P on the SWA module), Qwen2.5-7B
baseline on A2A, NVIDIA H100s, mean of 10 runs, metric is TTFT in ms:

| seq len | GPUs | SpikingBrain-7B | Qwen2.5-7B | ratio |
|---|---|---|---|---|
| 256k | 8 | 1015 | 7419 | 7.3x |
| 512k | 16 | 1037 | 14398 | 13.9x |
| 1M | 32 | 1054 | 27929 | 26.5x |
| 2M | 64 | 1070 | - | - |
| 4M | 128 | 1073 | - | - |

The caption defines the dash: "infeasible measurement due to resource
constraints". So the ">100x at 4M tokens" headline is a quadratic-trend
extrapolation past the last measured point. The largest measured head-to-head
is **26.5x at 1M**, and it took 32 H100s. Single/few-GPU reality (Table 5,
MetaX C550, latency for prompt + 128 output tokens at 128k): HuggingFace
1-GPU 15974 ms vs Qwen2.5-7B 38487 ms (2.4x); vLLM 4-GPU 12048 vs 45141
(3.7x); the paper's own text: "1.41x on HuggingFace and 2.75x on vLLM" at
128k. The linear-attention property is real; the 100x is a cluster-scale,
extrapolated, TTFT-only number.

## 2. The energy claim's actual anatomy

Eq. 27: E = average spikes x E_INT8add. Average spike count 1.13, INT8-add
energy ~0.03 pJ/op, so ~0.034 pJ per MAC. From there: "reduces energy
consumption by 97.7% compared with FP16 MACs and by 85.2% compared with INT8
MACs" (43.48x / 6.76x). This is a per-operation arithmetic estimate from
literature op-energy constants, not a measured whole-model per-token figure,
and it pays off only where spikes actually replace dense MACs. The paper's
own v4 Table 13 kills the GPU version: with spike encoding run as integer
activations on GPUs, "TTFT is identical to the corresponding non-spike
configuration" (H+S 4729.4 = H 4729.4 at 128k, parenthesized). The README
repeats it in deployment terms: W8ASpike is "pseudo-spiking ... rather than
true asynchronous event-driven spiking on neuromorphic hardware". Energy win
is a neuromorphic-hardware roadmap claim, not a spec of anything runnable.

## 3. The 69% sparsity claim's actual source

Activation-spike analysis by the authors on SpikingBrain-7B activations:
94.1% of values within [0,7], ~1% exceed 16, bitwise-ternary expansion gives
1.13 spikes/channel average with 18.4% of channels firing nothing, then at
step size 3 with inactive bits zero-filled, "the overall sparsity reaches
approximately 69.15%". It is activation sparsity under their spike coding,
not weight sparsity and not a hardware measurement. Its price (Table 6):
W8ASpike costs ~1-3 quality points (7B avg 0.6998 -> 0.6875).

## 4. Quality vs Qwen2.5, from the paper's own tables

The upcycle is real (continued pretraining, +150B tokens, ~2% of Qwen's 7T),
but against its own parent Qwen2.5-7B the 7B pays (Table 1, base):
MMLU 65.84 vs 74.21, CMMLU 71.58 vs 81.73, C-Eval 69.80 vs 81.60 (8-12
points down), HellaSwag 70.89 vs 72.81, ARC-C 43.32 vs 44.04 (par). Chat
(Table 3): wins NQ (21.47 vs 17.67) and TrQA (57.03 vs 55.72); loses IFEval
42.70 vs 73.20 (instruction-following, -30.5) and long-context QuALITY 60.12
vs 73.63. "Comparable to baselines" is true versus the other linear-attention
models (Falcon-Mamba, Mistral-linear, Zamba), all of which the caption admits
were trained on less Chinese data. The honest summary: capability was traded
for the architecture, most visibly in instruction-following.

## 5. Weights status (the drop receipt was wrong on the where)

- HF `BICLab/SpikingBrain-7B`: API and page return HTTP 401; `author=BICLab`
  returns an empty list. There is no public HF model under that org. The only
  HF artifact anywhere is a third-party mirror `maujim/spikingbrain-v1-7b-base`
  (14 downloads, custom_code, MIT tag).
- The GitHub README states weights are on **ModelScope**, live today (HTTP
  200): `Panyuqi/V1-7B-base` (15.24 GB, 15 pytorch .bin shards, bf16),
  `Panyuqi/V1-7B-sft-s3-reasoning` (chat), `sherry12334/SpikingBrain-7B-VL`,
  `Abel2076/SpikingBrain-7B-W8ASpike` (30.78 GB safetensors).
- W8ASpike is not a deployment quant: its safetensors index (591 tensors)
  pairs every projection with a `*.weight_quantizer.scales` tensor and stores
  ~fp32-scale masters (30.78 GB, 2x the bf16 base). It is a fake-quant
  checkpoint for running the quantized sim, not a shrunken artifact. No
  GGUF/AWQ/GPTQ of this model exists anywhere I could find.
- ModelScope's own backend metadata for the base model: `ollama: null`,
  `vllm: null`, `sglang: null`, `lmdeploy: null` - zero out-of-box backends.

## 6. The estate run-path verdict

Architecture: `GLAswaForCausalLM`, model_type `gla_swa` - 28 layers, 14 GLA +
14 SWA alternating, hidden 3584, sliding_window 4096, bf16, 128k native
context, Qwen tokenizer. Probes run with positive controls (so the negatives
are valid):

- **llama.cpp**: `conversion/__init__.py` on master (the post-refactor model
  registry, 171 arch references) has zero hits for GLAswa/gla_swa/
  SpikingBrain/hymeta while Qwen3Next, NemotronH, Mamba, FalconH1, Llama all
  hit. Not convertible. No GGUF. **No Ollama rung.**
- **transformers**: `gla_swa` absent from upstream `models/__init__.py`;
  maujim config confirms `auto_map` custom code. Needs trust_remote_code plus
  flash-linear-attention (triton) - CUDA-shaped.
- **vLLM**: official path is the `vllm-hymeta` plugin (docker
  `spiking-brain:7b-v1.0`; pins torch 2.7.1, triton 3.3.1, flash_attn 2.7.3,
  fla 0.1, vllm 0.10.0). NVIDIA-CUDA + MetaX only.

This box: AMD Radeon RX 5600 XT (RDNA1, no NVIDIA adapter, outside ROCm
support), 64 GB RAM, 614 GB free, WSL2 + Docker present, Ollama ladder live
(qwen2.5:7b/32b, gemma:2b, ...). Verdict: **SpikingBrain-7B does not run on
our stack today on any of the three asked runtimes.** The drop receipt's
estate-map line "SpikingBrain-7B is runnable on the ladder TODAY" is
refuted by this lane. What tonight would have needed, on an NVIDIA box
(>=24 GB VRAM for bf16, ~16 GB for the W8A sim): clone the repo, docker
build, pull 15.24 GB from ModelScope, `vllm serve --dtype bfloat16`. That is
a one-evening job on the right hardware and impossible on this one. The port
that would make it ladder-native is a llama.cpp GLA+SWA hybrid kernel +
converter contribution: multi-week C++, not a tonight job.

## 7. Receipt corrections vs SPIKINGBRAIN_DROP_20261001.md

1. "open weights on HuggingFace" - wrong host; weights are ModelScope-only,
   BICLab HF org is empty (the maujim HF model is an unrelated third-party
   mirror).
2. "runnable on the ladder TODAY" - refuted (section 6).
3. "~100x TTFT" - sharpened: extrapolated past the last measured point
   (26.5x measured at 1M), 128 H100s + sequence parallelism, TTFT-only.
   The receipt's other tri-states (energy qualifier, brain wrapper) hold and
   are now byte-anchored.

## 8. What survives for the estate

- The upcycle steal stays valid and is now priced by the paper itself: +150B
  tokens (~2% of parent's tokens) buys the architecture swap at a cost of
  8-12 points on knowledge evals and ~30 points of IFEval. Any lora_pipeline /
  Track-F pricing probe should use those as the exchange rate.
- The long-context local rung stays OPEN: the property is real but the
  artifact is unreachable from this hardware. Watch the GLA+SWA porting
  effort in llama.cpp/flash-linear-attention land, or an NVIDIA host, before
  re-litigating.
- Table 13 is the receipt for a general law: efficiency claims measured on
  hardware that cannot exploit the mechanism (spikes on GPUs) are roadmap
  marketing until the hardware exists.

Ledger: this lane spent zero paid tokens; all fetches were curl + local
parsing on the free seat.
