# COMPUTE DIG — our physical substrate vs the frontier's shopping list (2026-09-04)

> **[AUDIT-TYPED 2026-09-08]** status: LIVE · claims: the lab is burst-rich/memory-poor until Rocinante — API lanes frontier-class (50-wide flash, 27.85 rps receipted), local training ~zero without CUDA — SUPPORTED (all numbers receipted per cited cards) · falsifier: burst benchmarks fail to reproduce, or the box demonstrates real local training capacity before Oct 27

All numbers receipted (BURST_DOCTRINE_20260903.md, FRONTIER_MAP_DEEPSEEK_20260904.md,
CONCURRENCY appendix, uzu card, march-228). No vibes.

## WHAT WE HAVE TODAY (the box)
- **One box, 68.7GB unified memory** — currently runs GLM-4.7-Flash 30B-A3B
  (MIT, GGUF via llama.cpp/Ollama) + qwen2.5:32b side-by-side tonight-capable.
- GLM-4.6V-Flash 9B vision: local eyes lane, fits.
- Docker fleet: 6 containers, loopback-only; the box also hosts ollama, redis,
  browser seat, control plane.
- No CUDA. No discrete GPU. Metal/MLX is the local accelerator story; heavy
  training (CUDA-gated QLoRA stages) runs云端 via plan/API lanes only.
- Local TRAINING capacity: effectively zero beyond small finetune experiments —
  the campaign's Stage 0 preflight honest-fails without CUDA.

## WHAT WE HOLD ON THE API SIDE (the burst lanes — measured)
- glm-5.3-flash: 50-wide bursts, p50 1.7s @50, 27.85 rps sustained, 99.89%.
- glm-4-32b: 15-wide, 0.8s p50 — latency king.
- Night window: plan-door flash zero-metered (32.26M tok receipted); promo
  8AM-6PM PT unlimited-in-ZCode until Sep 20.
- Lite key: 50/50 concurrent, yearly package.
- Frozen-prefix cache mining: 99.5% hit rate standing wave on 4.7-flash.

## ROCINANTE (Oct 27): 4x Mac Studio M5 Ultra
- The supercomputing-cluster role, filled. Unified memory in the hundreds-of-GB
  class per node (4 nodes) = the first real LOCAL training + serving substrate.
- Docked targets already receipted: uzu specdec on M5 — beat ~63 tok/s baseline
  (Qwen3.6-27B M5 Max community-measured), reach 110-125.
- Day-one probe list exists (manifest pin owed).

## THE HONEST SHAPE
- We are a **burst-rich, memory-poor-until-October lab**: API concurrency is
  frontier-class (50-wide, near-free); local compute is a preview.
- "Mining like ox 23/7" = the night windows + promo windows + cache wave are
  ALREADY the mining machinery; what's missing is the ORGAN that keeps it fed
  (queue restock + claim-organ fix) and the DATA-ENGINEER role that treats
  the output as corpus, not exhaust.
- Physical gap vs frontier shopping list: distributed training infra (theirs:
  superclusters), custom kernels (theirs: CUDA/Triton; ours: Metal/MLX+uzu —
  thin), inference optimization (ours: burst scheduling + specdec targets),
  data engines (ours: room.jsonl + intake tapes — the smallest real one alive).

---
DISPOSITION: FOLDED - fed the five-demands synthesis + restock mandate (fire-15 structural fix: disposition lives IN the card; bard fire-10 stamped only the ledger — half-wire closed)
