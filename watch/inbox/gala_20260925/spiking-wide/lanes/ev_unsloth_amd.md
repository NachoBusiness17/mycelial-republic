# RAW EVIDENCE: WebFetch https://unsloth.ai/docs/basics/amd
# Fetched 2026-10-01 by lane nonnvidia-stacks (division B, spiking-wide). Verbatim fetch result below.

PROMPT: What AMD GPUs does Unsloth officially support for training and fine-tuning? List the exact GPU families/architectures named (RDNA versions, RX series numbers, Instinct/MI series), whether Windows and Linux are supported, and any statement about QLoRA/LoRA fine-tuning support or known limitations. Quote exact sentences where possible.

RESULT:
# AMD GPU Support in Unsloth

## Supported Hardware (from the support table)

- **RDNA 4** - Radeon RX 9000 Series (gfx1200, gfx1201) - Full support - Windows + WSL + Linux
- **RDNA 3.5** - Ryzen AI 300 / Ryzen AI MAX (Strix Halo) (gfx1150, gfx1151, gfx1152) - Full - Windows + WSL + Linux
- **RDNA 3** - Radeon RX 7000 Series (gfx1100, gfx1101, gfx1102) - Full - Windows + WSL + Linux
- **RDNA 2** - Radeon RX 6000 Series (gfx1030-gfx1034) - Full - Windows + WSL + Linux
- **RDNA 1** - Radeon RX 5000 Series (gfx1010, gfx1012) - **Vulkan inference only**
- **CDNA 4** - Instinct MI350 Series (gfx950) - Full - **Linux only**
- **CDNA 3** - Instinct MI300 Series (gfx940, gfx941, gfx942) - Full - **Linux only**
- **CDNA 2** - Instinct MI200 Series (gfx90a) - Full - **Linux only**
- **CDNA 1** - Instinct MI100 Series (gfx908) - Full - **Linux only**

## Key Claims

The page states: "Unsloth now officially supports AMD hardware, making it easy to run, train, fine-tune, RL, and deploy models locally on AMD GPUs."

Supported platforms: "Unsloth runs on Windows, WSL, and Linux, supporting RDNA 1-4, Radeon RX 9000 and 7000 series GPUs, Instinct MI350 and MI300 data center GPUs."

## QLoRA / LoRA Fine-tuning

- "4-bit training: bitsandbytes-based QLoRA support for Radeon and CDNA GPUs."
- "Train Gemma 4 models in 8GB VRAM or Qwen3.5 in 3GB VRAM," with claims of ~70% less VRAM and up to 2x faster training with "no accuracy loss."
- The RL section notes weight sharing with vLLM to halve memory usage.

## Known Limitations

- Older GPUs lack required hardware support: "We are actively working on supporting more AMD GPUs, however older ones unfortunately do not have the required hardware support."
- RDNA 1 supports only Vulkan inference, not full training.
- All CDNA (data center) GPUs are Linux-only.
- Multi-GPU distributed training is Linux-only: "On Windows, AMD ROCm does not yet provide a GPU-collective backend" - the docs advise using Linux for AMD multi-GPU training.
