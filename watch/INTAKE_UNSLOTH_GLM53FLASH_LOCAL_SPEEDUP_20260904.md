# INTAKE — Unsloth: GLM-5.3-Flash local GGUF 1.6-3.4x faster (2026-09-04)

Source: @UnslothAI 2095852388888522890 (Sep 4, 12:32Z, image verified via vision Read).
Optimized decoding + bonus MTP (multi-token prediction) in their llama.cpp PR and
Unsloth Desktop; GGUFs at huggingface.co/unsloth/GLM-5.3-Flash-GGUF.

## Score: 21/25 — BUILD NOW

| Axis | Score | Why |
|------|-------|-----|
| FIT | 5 | GGUF/llama.cpp runs on Apple Silicon — pure Rocinante substrate, no new vendor |
| PULL | 5 | This IS the fleet's own model lane: 5.3-flash unlimited promo + wall Sep 20 + Rocinante Oct 27 |
| COST | 4 | Free weights, free GGUFs; only cost is Oct 27 unbox time + a benchmark pass |
| WINDOW | 4 | Rocinante hardware 53 days out; quant table is the exact sizing spec for the buy (already bought — for tuning day one) |
| NOVELTY | 3 | MTP speculative decoding is a new surface; 5.3-flash itself already in the corpus |

## The load-bearing numbers (from the image, exact)
- Hardware table (unified RAM+VRAM): 1-bit 102GB / 2-bit 118GB / **3-bit 128-152GB /
  4-bit 164-212GB** / 8-bit 352GB / BF16 652GB.
- **Rocinante read: 4x M5 Ultra = 512GB unified → 4-bit (164-212GB) fits with ~300GB
  headroom for the fleet's containers + cache-mining grind. 8-bit at 352GB also fits.**
- Speedups: baseline→optimized→MTP n=3 = 3.33x at long context; 1.6x at short context.
  MTP sweet spot n=2-3; n=5 goes SLOWER (86.5→63.7 tok/s at 4096). tg32 @65k ctx: 20.66→48.99 tok/s on 1xB200.

## Tri-state claims
- Supported: 1.6-3.4x local GGUF speedup (their measured tables, method shown, reproducible via their llama.cpp PR).
- Supported: 3-bit runs on 128GB (their table; we have >512GB — comfortable margin).
- Unproven (on OUR surface): MTP n=3 speedup transfers to M5 Ultra unified memory — draft-token MTP is llama.cpp Metal-path dependent; measure on day one.
- Unproven: "on par with Claude Opus 4.8" (vendor claim, no fold of ours).

## Verdict: **BUILD** (R-1: ROCINANTE_DAYONE_BENCH)
Day-one Rocinante runbook line: pull unsloth GGUF 4-bit, llama.cpp with their PR, MTP n=2,
benchmark tok/s at 4k/16k/65k ctx alongside the fleet's container stack. Route via the
QLoRA campaign Stage 0 (environment recon) — same measurement harness, different model lane.
Calibration note: MTP is inference-only; QLoRA TRAINING path (Unsloth trainer) is a
separate lane and stays CUDA-dependent until proven otherwise on MPS.
