# HOPPER RENDER: hardware verdict on this box (gate 4)

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 · **Class:** RECEIPT / blocker, honestly named

## Box reality (verified live)

GPU: AMD Radeon RX 5600 XT (Navi 10 / gfx1010, 8GB class), NO NVIDIA card (no nvidia-smi), WSL2 = docker-desktop only. Ollama serves it via Vulkan/llama-server paths (box-burn doctrine), but diffusion video is a different runtime.

## Verdict: local LTX-Video render is NOT viable on this box

- LTX-Video (both 13B and the practical paths) is CUDA-first; RX 5600 XT has no ROCm-on-Windows support and torch-directml for video diffusion pipelines is experimental at best on 8GB.
- The pipeline we validated (LTX 13B FP8 i2v + forward/backward loop extension + RIFE to 60fps, 1-2.5h for 30s @ 1080p60) assumes an NVIDIA 24GB-class card.
- The box-burn GPU doctrine (llama-server Vulkan on the gfx1010) covers text inference, not this.

## Three honest paths when you want the render

1. **Cloud render lane (cheapest, ~dollars):** Replicate/fal.ai host LTX-Video endpoints; the 30s loop costs a few dollars per render; iteration happens remotely, result lands locally. Fits LAW-11-style credit spend on demanded artifacts.
2. **Borrow/buy NVIDIA:** any 24GB-class card (3090/4090) runs the whole validated pipeline locally.
3. **Do nothing yet:** the pipeline spec is preserved in W2_L06/REPORT_noir_shaders and this decision doc; it executes the day hardware exists.

No downloads or installs were attempted against a dead end; nothing was faked past the hardware gap.
