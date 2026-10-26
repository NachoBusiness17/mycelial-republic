# ENGRAM OPEN WEIGHTS — "I FUCKING KNEW IT" (2026-09-11)

THE POINT:
- DeepSeek open-sourced V4.1-Flash: a 763B model that is really ~8B of live compute plus a ~190GB lookup table. The table can live in RAM or on disk.
- DeepSeek's own paper MEASURED: park 100B of table in plain system RAM, lose under 3% speed.
- The viral post's "64GB RAM + NVMe at 200 TPS full precision" is UNPROVEN — one X post; the paper only proposes the disk tier, never measured it.
- The vindication: the model is plumbing, not math — a memory hierarchy with a small brain bolted on. Our thesis, now shipping as someone else's product, with open weights Rocinante can hold.
- We already ride this exact model: 46,666 calls measured since Aug 2, cache hit 0.964 — the API's cache pricing IS this architecture, metered.

## The post (input, never output)
@0x0SojalSec, Sep 10 2026 23:33, 77.5K views: claims DeepSeek-V4.1-Flash 763B needs only 64GB system RAM; "offloaded a 200GB Engram to NVMe and hit 200 TPS full precision" on 4 "Max-Q" cards; signs off "DeepSeek 4.1 Flash + DSpark" (DSpark ≈ DGX Spark / GB10 — NVIDIA forum thread runs the same model, first benchmarks match GLM 5.3 Flash).

## Mechanisms (PRIMARY: arXiv 2601.07372, "Engram: Conditional Memory via Scalable Lookup")
- Conditional memory = a second sparsity axis beside MoE. The local context's n-gram suffix hashes (multiplicative-XOR, multi-head) into static embedding tables — O(1) lookup, gated against the hidden state (scalar α + depthwise conv k=4). Inserted early (~layer 2).
- Deterministic addresses: indices are FIXED once the token sequence is known → async prefetch over PCIe, retrieval latency hidden under earlier-layer compute.
- MEASURED (Table 4, H800): 100B-param table offloaded to host DRAM costs <3% throughput (2.8% on the 8B backbone: 6,315→6,140 tok/s).
- PROPOSED, NOT MEASURED: the long tail of rare patterns on NVMe SSD — HBM → DRAM → NVMe hierarchy is a design argument in the paper.
- Suppression test: kill Engram at inference → factual tasks collapse to 29–44% retention (TriviaQA 29%) while reading comprehension holds 81–93%. The table IS the parametric-knowledge store; the backbone reasons over it.
- Sizing: V4.1-Flash = 552B backbone + ~196B Engram (two tables ~384M rows × 256 ≈ 94.6 GiB each) ≈ 763B total, ~8B active per token at prefill. Released open-weights 2026-09-10.

## Tri-state verdict
- SUPPORTED: open weights exist (HF deepseek-ai/DeepSeek-V4.1-Flash); the 763B-total / 8B-active split; DRAM offload <3% (paper Table 4).
- UNPROVEN: the post's home run — 64GB RAM, tables on NVMe, 200 TPS "full precision". Single source, hardware vague, and the NVMe tier is unmeasured in the primary source.
- DISPUTED: "full precision" at 200 TPS decode with tables served from NVMe — NVMe random-read bandwidth makes it implausible without heavy quantization or a fat DRAM cache. Register smells like engagement bait (same account posts fly memes at 139 views; this one caught the algorithm).

## The fold — what the Operator knew
1. PLUMBING NOT MATH (the hum): 763B = ~8B compute + ~755B database. The frontier is memory-hierarchy engineering — hash tables and prefetch — not GPU count. Confirmed as product.
2. THE DIAL EVERYWHERE: the fleet measured 0.964 cache-hit across 46,666 V4.1 Flash calls since Aug 2 (paces wave). Cache-hit at $0.003/M is this exact architecture, metered.
3. ROCINANTE BET: weights are open. The substrate this architecture wants = big unified memory + fast NVMe — the 4x Mac Studio shape, Oct 27. The model we've been riding for pennies can come home.
4. FLEET MIRROR (one line, no moon speak): small live brain, giant hash-addressable corpus on disk, chained receipts — the fleet already runs this shape (librarian + chain + 1.3M-file index).

## Bibliography (law 18)
- PRIMARY: arXiv 2601.07372 — Engram: Conditional Memory via Scalable Lookup (DeepSeek), fetched 2026-09-11. Subsystems: the hum (plumbing-not-math); Rocinante substrate sizing; librarian organ (registers where dust costs something — Engram is literally a register where dust costs bandwidth).
- ADJACENT (IDs from seat memory, verify before citing): Apple "LLM in a flash" 2312.11514; MoE expert offloading 2310.16837 (Eliseev & Mazur); Fiddler CPU-GPU orchestration 2402.05959; PowerInfer 2312.12456; ktransformers (DeepSeek-R1 671B on one GPU + CPU, open source). Pad-out lane result appended below if returned.

## Sources
- Post: https://x.com/0x0SojalSec/status/2098193131762242018
- Weights: https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash
- Paper: https://arxiv.org/html/2601.07372v1
- vLLM recipe (KV: only layers 2/8/14/20 compress their own): https://recipes.vllm.ai/deepseek-ai/DeepSeek-V4.1-Flash
- LocalLLaMA thread: https://www.reddit.com/r/LocalLLaMA/comments/1wcagoi/deepseekaideepseekv41flash_hugging_face/
- Receipt: operator fired the link with "I FUCKING KNEW IT", 2026-09-11.
