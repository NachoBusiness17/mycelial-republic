# RACTOR RESOLUTION - 2026-10-17: THREE CONTRADICTIONS RESOLVED INTO INVARIANTS

Classification: RECEIPT + RACTOR RESOLUTION
Producer: Antigravity (primary seat)
Workspace: local_sovereign_agent
Context: Wave Protocol Ractor Sweep (Dispute pricing at 10x)
Load Anchor: watch/inbox/harness_intel_20261013/CARD.md, queue/todo.md, memory/rib/RIB_FREE_USAGE_POLICY_20260823.md

---

## DISPUTE 1: Vulkan vs CPU Quantization Throughput on Navi10 / RX 5600 XT

### 1. The Contradiction
- Challenger (m012_openrouter3.md): Asserts that on gfx900/gfx1010 (RX 5600 XT), Vulkan offload for Q4_K_M quantizations is slower than CPU-only for intermediate layers (-ngl 33, -ngl 66) due to missing hardware DP4A instructions, forcing 32-bit floating point shader fallbacks.
- Resolver (queue/todo.md Stone 7 + README.md): Measures that llama-server.exe achieved 53% GPU utilization via Vulkan while CPU was pegged at 88-100%, and that offloading models removes the system DDR4 memory bandwidth bottleneck.

### 2. The Resolution (Ractor Synthesis)
Both measurements are byte-accurate under different boundary conditions. Navi10 lacks hardware INT4/INT8 dot-product acceleration (DP4A), meaning shader arithmetic on quantized weights requires float-unpack emulation. When only partially offloaded (-ngl 33 or 66), the host-to-device PCIe transfer overhead combined with float emulation shader latency exceeds CPU AVX2 throughput. However, at full offload (-ngl 99), memory bandwidth shifts entirely to GDDR6 (288 GB/s vs DDR4 40 GB/s), overcoming the arithmetic emulation penalty.

### 3. Permanent Invariant Minted
**INVARIANT-20261017-01 (Navi10 Offload Envelope):**
*On pre-RDNA2 architectures lacking DP4A, partial layer offload is forbidden. Local GPU inference must run either -ngl 0 (pure CPU) or -ngl 99 (full VRAM residency). Intermediate layer splits represent spend and latency waste.*

---

## DISPUTE 2: Persistent Memory in Multi-Agent Inference (Accuracy Lift vs Systems Continuity)

### 1. The Contradiction
- Challenger (Son et al. NeurIPS 2026, arXiv:2610.07782): Four rigorous measurement corrections proved that persistent memory in multi-agent systems produces a structural null (+0.015 accuracy delta, 95% CI [-0.011, +0.046]) across standard benchmarks.
- Resolver (Republic Compass docs/ref/REPUBLIC_COMPASS.md): Asserts that persistent memory and the Verkle/rib biography chain are the foundational sovereign moat of the estate.

### 2. The Resolution (Ractor Synthesis)
The conflict stems from an instrument category error. Single-question benchmark batteries reset task state between runs; in an amnesiac benchmark, memory recall has no informative historical signal to retrieve, guaranteeing a statistical null. The estate's persistent memory is an architectural continuity organ (preserving operational laws, avoiding re-climbing solved bugs, suppressing dead endpoints, and bounding token drift), not an in-context reasoning booster for isolated trivia.

### 3. Permanent Invariant Minted
**INVARIANT-20261017-02 (Longitudinal Memory Law):**
*Memory is continuity and constraint propagation, never single-turn accuracy lift. Benchmarks evaluating memory must run longitudinal task chains where Run N+1 depends on Run N's residual. Single-turn evaluations of persistent memory are declared invalid.*

---

## DISPUTE 3: Free-Lane Throttling: Instantaneous Concurrency vs Sustained Drip Rate

### 1. The Contradiction
- Challenger (RIB_FREE_USAGE_POLICY_20260823.md): Forcing free seats throttles them into empty 429 responses ("reward patience, not pressure").
- Resolver (RIB_MODEL_GARDEN_ROUTING.md:192): Recorded 459 consecutive mining rows with zero 429 errors over 69 hours of sustained mining.

### 2. The Resolution (Ractor Synthesis)
The provider rate-limit gate binds to instantaneous burst width, not continuous daily volume. The 459-row zero-429 record was achieved at spaced drip intervals (width 1-3 with pacing). The 429 storms (such as the 20,432 fail rows on groq/Estate FullScan) were triggered by un-paced parallel batch scripts firing simultaneously.

### 3. Permanent Invariant Minted
**INVARIANT-20261017-03 (Paced Width Envelope):**
*Free-tier provider limits are instantaneous width gates. Mining on the 1,000/day paid-tier key must hold width 3 with a minimum 5-second inter-request dispatch delay. Batch scripts exceeding width 3 without driver backoff are classified as self-inflicted outages.*

---

## Falsifier
If any permanent invariant above is contradicted by a byte-backed receipt with instrument, moment, and delta, the invariant is struck into memory/fold_history/SUPERSEDED.md.
