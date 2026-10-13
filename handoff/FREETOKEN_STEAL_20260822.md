# FREETOKEN STEAL — edge-native MoE serving, bandwidth-adaptive execution

Source: arXiv:2608.16157 (17 Aug 2026) · repo `FlashML-org/FreeToken` (flashml.ai)
Operator share 2026-08-22. Full research moonshot. Contracts only — adapt to our
deterministic/architecture-native shape, never wholesale copy.

## Thesis (one line)
Once sparse activation makes a model's *computation* feasible, local inference is no longer
"does it fit on the GPU" but "how well does the system orchestrate the machine it already owns."
Treat GPU + CPU + host memory + interconnect as ONE elastic platform.

## The five mechanisms (from paper + repo, grounded in actual code)

### 1. Bandwidth-adaptive execution — the q\* policy (THE steal)
When a decode step misses `m` experts, split them between PCIe cache-fill (GPU) and in-place CPU
execution so both finish together. Closed form:
```
B_P = measured PCIe expert-transfer bandwidth
B_H = measured CPU-side expert-processing bandwidth
residual host bw   B_R = max(B_H - B_P, 0)
T_fill(q) ≈ q·S/B_P          T_cpu(m-q) ≈ (m-q)·S/(B_H - B_P)
q* ≈ m·B_P/B_H               ->  q/(m-q) ≈ B_P/(B_H - B_P)
```
Code: `offload_kernels._ensure_experts_hybrid_cpu` — `fetch_fraction = pcie_bw/cpu_bw`,
Q16 fixed point so GPU kernel and CPU reference cap identically; `cost = max(f·(q-frac), (m-f)·frac)`
picks the integer fetch count. Production measures B_P and B_H on the actual machine
(`benchbw.py`), never from spec sheets. **The balance is measured, not guessed.**

### 2. Semantic-aware expert caching (decode)
Global LRU residency across ALL layers: `slot_for_id[layer,expert]`, `id_of_slot`, `usage`, `step`
(`lru_ensure` from flashlib slot_cache). Cache tracks the router's working set, not a load-time
static placement. `BY_RECENCY` fetches the most-recently-active misses first (prioritize recurring
misses). Single-pass eviction victim discovery; fused multi-bank copy.

### 3. Full-layer double-buffered prefill
Prefill activates ~all experts per layer, so don't fetch on demand — stream whole layers.
Two full-layer buffers borrow from the SAME slot pool as decode (no phase handoff): GPU computes
layer `l` while a transfer stream loads layer `l+1`. `_prefill_hit_d2d`: experts already resident
gather device-side (D2D); only misses cross PCIe. Hit/miss classified by `slot >= 2*num_experts`.

### 4. Semantic-aware state cache + radix prefix (agentic context edits)
Radix prefix tree for full-attention KV; **recurrent-state checkpoints anchored at semantic
boundaries** (thinking blocks, tool-call openers, tool outputs, turn boundaries) — exactly where
agent harnesses edit/truncate context. After an edit, restore from the deepest surviving anchor and
re-prefill only the new suffix. Dual-currency eviction: full-KV LRU over unlocked leaves + a second
swa/mamba currency (sliding-window + recurrent state snapshots) with tombstones. `toolcall_anchor_len`
marks the deepest reuse boundary that survives a client rewrite of an echoed tool call.
This is FreeToken's answer to the agentic re-prefill tax — it only re-computes the genuinely new part.

### 5. Elastic memory + FTW format + fast bootstrap
`plan_cache_budget`: split the runtime VRAM budget between KV pages and full-expert slots, rebuild
the cache at scheduler safe points without restart/reload. FTW weight format: experts pre-merged
into flattened `(layer*E+e)` banks, read with parallel direct I/O into final host layout, pin AFTER
fill (no zeroing gigabytes), no GPU warmup needed (first request runs the cold-cache decode path).

## Map to OUR modules (the adapt)

| FreeToken mechanism | Our existing thread it folds into | Our module/doctrine |
|---|---|---|
| q\* bandwidth-balance (measured, closed-form) | rightsize-from-measured-reality | `connectivity_sizer`, `rightsize-constantly`, `one-sizer` |
| bandwidth-adaptive CPU/GPU split | kv-cache / cache economics | `cache-extract-joint`, `steal-kv-cache-optimization`, `cache-router-measured` |
| semantic-anchor checkpoints at tool-call boundaries | our agentic context edits (bus, tool turns) | the AOS bus / agent tool-call lifecycle |
| global LRU expert residency | cache-mined prefix, shared-slot discipline | `cache-router` / `scaling-swarms-cheaper-warm-prefix` |
| radix prefix + dual-currency eviction | memory as radix / wave-as-address | `wave-is-the-address`, `titor`, `verkle-knot-real-structure` |
| elastic VRAM split (experts vs KV) | VRAM ceiling doctrine | `tripartite-vram-triad`, `known-vram-ceiling-do-not-re-derive`, `automatic-compute-rightsize` |
| FTW format (own WEIGHT layout) | own formats doctrine (weight layout, NOT tokenization) | `bare_numpy`, `quantization-architecture-standing-wave` |
| (tokenizer — NOT FTW) | already have our own: Mag's BPE = RIB/STEER coordinate layer | `own-tokenizer-moonshot`, `token_chain` |
| flag-handshake CPU exec (doorbell + watchdog) | our coordination / drainer heartbeats | `orchestrator`, `process-reaper` |

## What it changes for us (the honest edge)
The biggest resonance is mechanism 1 + 4 together: **a measured, closed-form split** (q\*) applied to
**semantic-boundary checkpointing** (mechanism 4). That is exactly our doctrine — rightsize from
measured reality, checkpoint at semantic seams — but at the *hardware-resource* layer, not the
token/cache layer. If FreeToken's benchmarks hold, the local frontier ceiling (our VRAM ceiling) is
not a hardware constant but a *serving-software* function we can move. That reframes
"frontier only via API" into "frontier in our own room" — the sovereignty thesis made concrete.

## THE MERGE-TWO-LAYERS INVARIANT (folded 2026-08-22, operator "double tokenizers / meta token")
FreeToken q\* is NOT new to us — it is our OWN meta-token invariant at the hardware layer. One law,
many layers: **merge two sets with one handle.**
- FreeToken q\*      = merge two EXECUTION layers (GPU vs CPU) with a MEASURED bandwidth split.
- Our meta-token      = merge two TOKEN layers (stochastic frontier tokens + deterministic RIB/STEER
  coordinates) with a CONTENT-ADDRESSED ANCHOR. One memlang token (`MEM1` opcode + 32B verkle
  anchor, ~69B) RESOLVES to a whole meaning-set — seats receive coordinates, not payloads.
- The payoff both share = CHEAP REDUNDANT PROCESSES: one handle instead of re-transmitting the
  whole set (FreeToken: one expert fetch; ours: one anchor instead of full context). This is exactly
  what the 2026-08-16 harvest predicted: "meta tokens 2x token layers stochastic deterministic and
  tokenizers to merge the two — doesn't that make redundant processes more cheap and efficient."
- References (our own, verified): RIB_MEMWEAVE (memlang token), own-tokenizer-moonshot (Mag's BPE =
  RIB/STEER coordinate layer), single-surface-memlang (same token -> same invariant across surfaces),
  shufflebrain-hologramic (anchor reconstructs the distributed whole), steal_memlang_quantizer
  (deniable shared-memory: token alone insufficient without codebook+anchor).
- NOTE (honest, corrected): the `_tmp_spooky_probe` verkle knots are artifacts of mag/ghost_spooky
  (the AUTONOMY-LEVER probe), NOT a meta-token test — I initially conflated the two threads.

## Honest caveats (grounded, not verified by us)
- Benchmarks (77–83 tok/s Qwen3.6, 22–25 DSV4, 2.0x GLM-5.2 on PRO 6000) are the authors' own;
  we have not reproduced them. Hardware is CUDA/NVIDIA-specific; our box is AMD/Windows — the CPU
  executor's AMX/SIMD + cudaMemcpyBatchAsync paths likely don't map 1:1.
- q\* assumes PCIe + CPU contend for the same host-memory subsystem; that model is machine-specific.
- We did NOT clone their code into our tree (contracts only, per steal doctrine).

Schema: freetoken_steal.v1 · 2026-08-22 · routed to swarm + recorded
