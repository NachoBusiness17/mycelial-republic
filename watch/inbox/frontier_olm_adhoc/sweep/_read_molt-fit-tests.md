# I built MOLT: a local fine-tuning system with fit tests, checkpoints, and deployment tracing

- url: https://reddit.com/r/LocalLLaMA/comments/1wyvc8k/i_built_molt_a_local_finetuning_system_with_fit/
- id: 1wyvc8k | score: 0 | comments: 2 | created: 2026-10-06T06:20:00+00:00
- author: MKP_Nimilka | domain: v.redd.it
- url_in_post: https://v.redd.it/96roxxgyhsth1

## SELFTEXT

I’ve been building MOLT, a local fine-tuning system for consumer NVIDIA GPUs.

The goal is not only to start a QLoRA run. It is to make the whole process from model and dataset to a working local adapter less fragile.

MOLT currently handles:

\- dataset detection, preparation, and validation

\- GPU, VRAM, system-RAM, storage, and thermal checks before a run

\- automatic microbatch fit testing

\- 4-bit NF4 QLoRA training with BF16 adapters

\- safe checkpoints with integrity checks and proper resume state

\- telemetry for VRAM, temperature, energy, clocks, and throughput

\- base-vs-adapter evaluation

\- local adapter chat, export/GGUF workflows, and runtime diagnostics

Under the hood, I’m also experimenting with custom CUDA/Triton kernel and runtime paths, memory planning, CUDA graphs, replay modes, and fused optimization where the hardware and shape are qualified.

On my RTX 4060 Laptop 8GB, a recent Qwen 3B training run reached about 1,005 training targets/sec end to end very close to my historical Unsloth run at about 1,007 targets/sec. That is not a broad “MOLT beats Unsloth” claim yet; I still need repeated, matched quality/energy/memory tests.

What I want MOLT to become is a reliable local fine-tuning environment: you bring the model and dataset; it checks the plan, runs safely, preserves the evidence, and helps verify the adapter actually works after deployment.

I’m looking for people who genuinely fine-tune on a single NVIDIA GPU and would be willing to test it. What would MOLT need to support before you would try it?

## COMMENTS (2 fetched, ranked by score)

--- u/--Spaci-- (score 2):

Do we not know what a screen recording is?

--- u/MKP_Nimilka (score 1):

Fair 😂 I filmed the laptop with my phone. This clip only shows the dataset preparation step before training starts. I’ll capture the terminal directly for the full walkthrough so it’s easier to read.

