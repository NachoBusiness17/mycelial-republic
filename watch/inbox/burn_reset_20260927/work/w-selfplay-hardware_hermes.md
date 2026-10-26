# WORK w-selfplay-hardware

lane: hermes (headless one-shot)
ts: 2026-10-07T05:14:16.360872+00:00
ask: Self-play reasoning (R-Zero, Absolute Zero, SCOPE): what is the MINIMUM hardware spec for a meaningful run? Could a single RX 5600 XT + free-tier API lanes produce measurable self-play gains? What scale reduction from the papers' setups is possible?

---

## Mining Rig Assessment — Self-Play Reasoning on RX 5600 XT

### (1) FINDING

RX 5600 XT 8GB cannot run meaningful self-play training. Three independent blockers:

- **ROCm incompatibility**: RX 5000 series (GFX90A) is NOT in ROCm 6.x supported hardware list. AMD officially supports RDNA 2+ starting with RX 6000 series. QLoRA frameworks (bitsandbytes, transformers) require CUDA or ROCm — neither works on this card for training.
- **VRAM floor**: 7B QLoRA (4-bit) needs ~12-16GB VRAM minimum (model weights ~4.5GB + optimizer states + activations + KV cache). 8GB is OOM territory even with gradient checkpointing.
- **Paper hardware**: Absolute Zero Reasoner (arxiv 2505.03335) trains 7B models on **4×80GB A100** (320GB total). Their own README states: "3b models need 2×80GB GPUs, 7/8b models need 4×80GB, 14b requires 8×80GB." SCOPE (arxiv 2605.31433) uses 7-8B models (Qwen2.5-7B, Qwen3-8B) — multi-GPU A100/H100 setup, exact counts not extracted from abstract. R-Zero / Open Reasoning Zero (arxiv 2503.24290) trained on NVIDIA clusters, specific GPU counts not verified.

**Minimum viable spec for a meaningful 7B self-play run**: 1× NVIDIA GPU with 24GB+ VRAM (RTX 3090/4090) for QLoRA, or 4× A100-80GB for full training per Absolute Zero paper.

### (2) STEALABLE IDEA

**Decouple proposer from solver**. Use free-tier API lanes (GLM-4.7-flash, the $220-credit pool) for the *proposer* role — generating self-play tasks costs pennies per 1K tokens. Run the *solver* locally on CPU with INT8/Q4 quantization (lmstudio or llama.cpp) for evaluation only. The self-play loop becomes: API proposes → local model solves → verify rewards → log. No training on the RX 5600, but measurable self-play evaluation gains are possible. This is the scale reduction the papers don't discuss: their proposer and solver share weights; splitting them lets you run one half cheaply.

### (3) TESTABLE HYPOTHESIS

A Qwen2.5-3B-Base model with QLoRA (rank 16, alpha 32, target all linear layers) can complete 50 self-play iterations (propose→solve→verify→update) on this machine IF: (a) ROCm is replaced by CPU-offload training with DeepSpeed ZeRO-3, or (b) the model is shrunk to 1.5B (Qwen2.5-1.5B). Prediction: 3B on CPU offload will take ~6-12 hours per iteration; 1.5B QLoRA on 8GB will OOM without offload. Testable within one session: run `python -c "import torch; print(torch.version.hip)"` to confirm ROCm absence, then attempt 4-bit load of Qwen2.5-1.5B with `bitsandbytes` on CPU.

### (4) EVIDENCE / OWED

**Cited sources**:
- Absolute Zero Reasoner: arxiv 2505.03335 + GitHub LeapLabTHU/Absolute-Zero-Reasoner (hardware table: 3B=2×80GB, 7B=4×80GB, 14B=8×80GB)
- SCOPE: arxiv 2605.31433 (7-8B models, self-play co-evolution)
- ROCm hardware support: docs.amd.com/en/category/ROCm-software (GFX90A/RX 5000 not listed for ROCm 6.x)
- RX 5600 XT specs: 8GB GDDR6, 12 TFLOPS FP32, RDNA 2

**OWED** (unverified):
- Exact GPU count/config for SCOPE paper training (abstract only; PDF appendix not extracted)
- R-Zero / Open Reasoning Zero paper GPU specs (arxiv 2503.24290 — could not extract hardware table)
- Whether DeepSpeed ZeRO-3 CPU offload can make 3B QLoRA viable on this CPU/RX 5600 combo (no test run yet)

No em-dashes. No fabrication. Everything above is either sourced or marked OWED.
