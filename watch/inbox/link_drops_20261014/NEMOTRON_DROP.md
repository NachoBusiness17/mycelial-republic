# LINK-DROP: Nemotron 3.5 Super VL - an open 120B/12B-active MoE for agents (2026-10-14)

Both drops read via the owned lane. NVIDIA AI announced **Nemotron 3.5
Super VL**: an open model, 120B total parameters with 12B active (MoE),
combining reasoning and tool use with text, image, document, and video
understanding, explicitly "for long-running AI agents." Open AND
customizable: weights, data, and recipes published on HuggingFace, with
the post-training approach and multi-token-prediction/inference
optimizations documented.

## Estate weight (three rows)

1. **Candidate battery model.** 12B ACTIVE parameters is our speed class
   (the battery runs gemma:2b through qwen-desk, 2B-8B) - but with
   120B-class knowledge behind the active experts. If a quantized GGUF
   runs acceptably on the estate hardware, the council upgrades from
   small-local to frontier-class-local at the same electricity cost.
2. **The multimodal organ candidate.** VL = text/image/document/video in.
   The estate banked a 1,980-item vision corpus and has the sensory-door
   lane pending - a local multimodal model that runs on our own metal is
   the missing organ for scoring our own media banked ($0, T1-safe).
3. **The vernacular thesis widening.** Weights + data + RECIPES open from
   the biggest vendor: thesis 31 ("open weights are the german bible") is
   now production posture from NVIDIA itself. The recipes matter as much
   as the weights - training method published is the latin ending.

## The hardware question (the falsifier)

The RX 5600 XT 8GB cannot hold 120B total weights in VRAM; the MoE
expert-offload path (llama.cpp --n-cpu-moe / partial expert offload) is
the test: 12B active means per-token compute is small, but the full
weight set needs disk->RAM streaming. Verdict method: quantize (Q4), run
the battery's standard questions, compare correctness vs
qwen-desk/deepseek-r1 and latency vs gemma:2b. Pass bar: beats or matches
the battery median at under 2x the fastest cell's latency. Pass = council
rotation candidate. Fail = the sensory organ waits for hardware.

## Also noted

The "long-running AI agents" framing from NVIDIA is the DePIN/node
economy's job description - our drain loop is exactly that shape. The
big vendor is now building for our architecture.

Both LINKS rows registered.
