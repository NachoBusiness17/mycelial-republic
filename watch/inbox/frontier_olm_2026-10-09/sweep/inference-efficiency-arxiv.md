# Sweep: inference-efficiency via arxiv (2026-10-09)

source-fetched: 2026-10-09. Gopher seat: sweep-inference-efficiency-arxiv (dynamic workflow child). Lane: speculative decoding + continuous batching + serving stack, last 30 days (2026-09-09..2026-10-09).

## Method (instrument + moments)

Pass 1 broad sweep: four export.arxiv.org API queries via WebFetch, sortBy submittedDate descending:

1. `all:"speculative decoding"` - 25 entries shown of 784 reported; all 25 in-window (09-30..10-08).
2. `all:"continuous batching"` - 25 of 57 shown; 3 in-window (DynaCore 2610.07443, vSkipper 2609.37062, vLLM/llm-d control plane 2609.23130); the rest pre-window and screened out.
3. `all:"LLM serving"` - first attempt TIMED OUT at 60s; retry returned 25 entries, ~23 in-window.
4. `all:"KV cache" AND all:"inference"` - 20 of ~1300 shown; ~18 in-window.

A fifth query (`all:"inference budget" AND cat:cs.LG`) timed out at 60s and was DROPPED, not retried: the candidate bar was already cleared. Total surfaced ~95 entries; ~64 distinct in-window candidates after dedupe. The 30-candidate bar is met with margin.

Pass 2 deep read: 8 arxiv.org/abs pages read end to end this session (HEAR, TokenRouter, BitNest, APEX, 2610.05305, EdgeAgent, vSkipper, DySCo). 7 banked as new; HEAR dropped as already banked TODAY by the kv-cache sibling (receipt below). Bank only what I read myself; every quote below is a verbatim fragment from the page I fetched.

## Banked items (strongest first)

### 1. APEX: Speculate smarter, not deeper (2610.07780, 2026-10-06)
vLLM-integrated learned controller; APEX-Router picks among EAGLE-3, n-gram, and draft-model speculation per request; APEX-Depth adapts draft length per verification block from censored survival feedback. Qwen3-8B, six workloads: up to 5.24x speedup, aggregate 4.27x (APEX-S); APEX-B 3.27x with a 41.0 percent relative wasted-token reduction vs fixed n-gram at k=16.
Quote: "We integrate APEX into vLLM and evaluate it with Qwen3-8B across six workloads, achieving up to 5.24X speedup over autoregressive decoding."
Estate mapping (Q1): this is the budget-guard class (lens/laws.md:154-158, six unwired fire surfaces) applied at the token level: waste is priced as a first-class loss term, exactly the shape RIB_INFERENCE_BUDGET wants on refire-prone carriers. Terminal-rule-compatible: draft rejection is one verification pass, not a refire of the same params (RIB_INFERENCE_BUDGET_20261001.md:44-78 via lens/laws.md:64-66).
Overlap: catalog stub only (state/arxiv/2026-10-07/2610.07780v1.txt, id fc5b9f5606ec, 1,716 B); no sweep bank day-8 or today; scoped memory grep zero hits. NEW.

### 2. BitNest: Bit-Nested Speculative Decoding (2610.02800, v1 2026-10-02, v2 2026-10-06)
Draft embedded in the target's own weight representation (low-precision base, residual refinement up), extended to the KV cache; 7B-8B edge-class LLMs: 95.2 percent average acceptance, 1.48-1.61x end-to-end vs FP16 autoregressive.
Quote: "embeds a low-precision draft directly into the higher-precision target representation"
Estate mapping (Q1): the cheapest recorded path to "local janitors up": speculative decoding with NO second resident model, which is the binding constraint on the estate's Ollama box. Pairs with the owed quant A/B lane (four pinned choices, watch/inbox/port_wave_20261007/QUANT_AB_SPEC_AMEND.md): a nested draft is a quant choice, not a model purchase.
Overlap: zero catalog hits; zero memory hits (scoped grep). NEW.

### 3. TokenRouter: Efficient Serving System for Token-Level LLM Routing (2610.12242, 2026-10-08, NeurIPS 2026, code public)
Request-centric programming, model-centric execution: a subserver per LLM, delayed-batching schedulers tuned by a throughput model. 2.01-64.15x decoding throughput over existing systems across routing algorithms, workloads, model pairs.
Quote: "TokenRouter achieves 2.01-64.15x higher decoding throughput than existing systems, substantially advancing the serving efficiency of token-level LLM routing."
Estate mapping (Q1+Q2): the serving-layer twin of RIB_ROUTING_CLASSES_20261002 (question-class routes before family or price); open code at github.com/thu-nics/TokenRouter. If the estate ever funds a local router pool (GPU-ladder gates), this is the control plane to steal before building one.
Overlap: catalog stub mirrored TODAY (state/arxiv/2026-10-09/2610.12242v1.txt, id faf7eed1d887, 06:30Z); no sweep bank; memory zero. NEW.

### 4. vSkipper: Translating Dynamic Layer Skipping into LLM Serving Gains (2609.37062, 2026-09-29)
Virtualization layer making layer skippers pluggable in SGLang while preserving continuous batching, paged KV cache, and captured decode graphs; motivated by FlexiDepth skipping 8 of 32 layers yet decoding SLOWER than base. Results: 36.8 percent mean latency cut on GSM8K at the load knee, 11.3 percent throughput under saturation; open SGLang fork (AKafakA/sglang-vskipper).
Quote: "vSkipper groups tokens by the skipper's decision and uses routed execution only when predicted to be profitable"
Estate mapping (Q1): the per-token compute cut that does NOT break the batch shape, i.e. the version of "run fewer layers" that survives a real engine. The FlexiDepth counterfactual (skipping that loses speed) is the cautionary twin of every naive local-speedup idea.
Overlap: zero catalog hits (grep 2609.37062: none); zero memory. NEW, and the least-held item on this list.

### 5. EdgeAgent: Orchestrating On-Device LLM Inference for End-User Multi-Agent Systems (2610.03394, 2026-10-02)
UMA-aware zero-copy tensor parallelism, dynamic draft budgets from real-time sequence predictability, asynchronous suspend-and-yield eviction of tool-stalled agents. Apple M4: 1.29x from UMA execution alone, 1.77x full system under extreme tool-use latencies.
Quote: "the UMA-aware execution alone contributes a 1.29x speedup over batched speculative decoding. Adding the agent-aware scheduling lifts the full EdgeAgent system to a 1.77x speedup"
Estate mapping (Q1): the draft-budget and tool-stall scheduling patterns transfer to the estate's local multi-lane fleet (gemma:2b janitor + gemma4 worker across queue/lanes); the measurement box is Apple silicon, not the estate's AMD/Windows, so numbers do not transfer, patterns do.
Overlap: zero catalog hits; today's swarm-orchestration sibling lists the ID in its pass-1 candidate line only (sweep/swarm-orchestration-arxiv.md:11), banked nothing; memory zero. NEW.

### 6. DySCo: Dynamic Sharding for Collaborative Edge-Cloud LLM Inference (2610.08268, 2026-10-06)
Keeps KV caches edge-local; dyForward runs contiguous layer ranges from resident shards without weight reloads; depth-synchronized batching advances heterogeneous requests to the deepest cut and batches the common suffix. At concurrency 8: 275 percent over FIFO, 48 percent over exact-match batching, 79 percent over round-robin; idle gaps cost up to 25 ms per decode step even excluding wait time. Artifact public (github.com/Large-scale-Sustainable-Computing-LSC/dysco-artifact).
Quote: "At an average concurrency of eight, DSB improves throughput by 275% over FIFO, 48% over exact-match batching, and 79% over round-robin interleaving"
Estate mapping (Q2): the first measured answer to "how do you batch when requests arrive at different depths"; the estate's split is tier-shaped (janitor/worker/judgment) not layer-shaped, but the idle-gap tax and the advance-to-deepest-then-batch-suffix move are the transferable parts for the dispatch shape.
Overlap: catalog stub (state/arxiv/2026-10-07/2610.08268v1.txt, id 8c7feb0811c8); no sweep bank; memory zero. NEW.

### 7. Characterizing Parallelism Strategies in LLM Inference (2610.05305, 2026-10-04, cs.DC)
Unified analytical model of TP/PP/hybrid latency (compute, inter-GPU communication, pipeline bubbles); explains why PP favors prefill while TP cuts decode latency; no headline numbers on the abstract page.
Quote: "a unified analytical framework for modeling distributed LLM inference under TP, PP, and HB"
Estate mapping (Q2+GPU ladder): the vocabulary the five-gate hardware law (RIB_GPU_LADDER_20261001.md:10-23 via lens/laws.md:98-99) will need the day a second card is on the table; also the honest frame for why the estate's concurrency envelope is a software shape, not a hardware one.
Overlap: zero catalog hits; zero memory. NEW. Confidence lower: the fetch model condensed this abstract, so my quote is the fragment it marked quoted, not a full-abstract read.

## Dedupe receipts (re-bank is waste)

- HEAR Protocol (2610.06597): BANKED TODAY by the kv-cache sibling as its slot 5 (sweep/kv-cache-context-engineering-arxiv.md:49) with a full-text read carrying numbers my abs read lacks (KV reuse 19.2% -> 87.6%, median TTFT 63.1s -> 4.6s on SCBench). My independent abs read converges on the headline set (1.61x batch, 2.23x TTFT reduction on SCBench; 1.23x BrowseComp-Plus; 2.45x DeepResearchBench). Dropped from my bank; the sibling's row is the one to consume.
- RaReCache (2610.11358): banked today by the same sibling (its instrument note, sweep/kv-cache-context-engineering-arxiv.md:8). Screened out of mine.
- Catalog mirror stubs (zone lsa) are abstract-level holdings, not banks: APEX, TokenRouter, DySCo stubs named above; the reads and estate mappings here are the new work on top.

## Per-question coverage honesty

- Q1 (ladder shift without violating the terminal rule): APEX, BitNest, vSkipper, EdgeAgent are the down-shift candidates; all four raise local throughput per watt/byte rather than assuming a bigger box. Terminal-rule analysis: EMPTY_REASONING is terminal per (ask, family), never refire the same params (RIB_INFERENCE_BUDGET_20261001.md:44-78); speculative decoding is structurally compatible (rejection costs one verification pass, not a refire) and APEX is the paper that prices the actual bleed vector (wasted draft tokens, -41.0 percent relative). The wiring point for the estate remains the six hand-rolling fire surfaces (lens/laws.md:154-158).
- Q2 (frontier serving benchmarks vs the estate's free-lane rows): the digest row counts (openrouter 469 +7 below-threshold adds, groq 11, mistral 46) were confirmed from the commit itself (`git show f80961cd9 -s --format=%B`, this session). The estate's envelope is quota- and rolling-throughput-bound (fan-out width law: Task agents clean at widths 10-12, 109.4M tok/h at width 10; workflow children die on first 429/1302; free-lane drip law), while every headline multiplier here (TokenRouter 2.01-64.15x, HEAR 1.61x, DySCo 3.75x over FIFO) measures owned-GPU batch amortization. VERDICT: different economics, as the question suspected. The papers reconcile with the LOCAL janitor tier and the dispatch shape, not with free-lane row counts; free-lane adds track quota patience, not tokens/sec. Adjacent outside-window evidence: Service-Induced Congestion (2606.15555, 2026-06-14) proves eviction-driven limit cycles under continuous batching can cost up to 50 percent throughput, which is the failure class a 50-wide fan-out shares with a memory-constrained server.
- Q3 (day-8 mine's 32 unbanked sweeps): verified by ls - day-8 sweep dir holds 33 .md files of which exactly 32 form the 8-areas x 4-sources grid; 16 files carry efficiency-claim language (grep -l receipt, this session). Funded-tier-first order under descent leg 3 (one landed deliverable per premium turn, RIB_THE_DESCENT_PROTOCOL_20261001.md:30-56 via lens/laws.md:70-74): (1) AgentLoop's 88.44 percent token-cost cut (day-8 sweep/inference-efficiency-arxiv.md item 7), because the deliverable is the slot-closed guard wired into the six named fire surfaces and the guard itself enforces the terminal rule; (2) SoT's 582-parameter controller (same file, item 8; 62.6 percent generated-token cut at accuracy up); (3) Dual-QK's 6.8x KV compression / 3.75x decode throughput (day-8 sweep/kv-cache-context-engineering-arxiv.md:38) as a candidate axis for the owed four-pinned-choices quant A/B, CUDA/SGLang-only so a grammar row. NOT worth a premium turn: BreadthKV/BARQ/lmcache KV offload, closed as non-steal on this box and double-sourced (day-8 sweep/kv-cache-context-engineering-arxiv.md:60 plus the Metal-only b11465-b11475 finding, lens/burns.md:93-94).
- Q4 (zero-coverage or shelf canon): NOT zero coverage. Catalog census this session: 5,506 rows under state/arxiv (the daily mirror), 105 rows match "serving", 475 match "inference", 29 titles contain "speculative decoding", 57 match "speculative" anywhere; the mined banks already hold ReFold (day-7), Harness Tokenomics + IEC-Bench + AgentLoop + SELF-POT (day-8), HEAR + RaReCache (today, sibling lanes). What IS thin: the cs.DC serving-system layer. Continuous batching as a phrase: exactly 1 catalog row; vSkipper and 2610.05305 had zero hits anywhere; 4 of my 8 deep-read candidates had no catalog presence at all. The shelf holds the content-paper canon; the serving-stack canon is stub-level and this sweep is the first mined read of it.

## Instrument notes

- All fetches via WebFetch. Door health: export.arxiv.org degraded twice (two 60s timeouts: the LLM serving query passed on retry; the inference-budget query was dropped as unnecessary); all 8 arxiv.org/abs deep reads answered clean. No 403s; the fallback recipe was never needed and never faked.
- Quotes are verbatim fragments as rendered by the fetched pages; TokenRouter and DySCo abstracts were captured near-verbatim; 2610.05305 was condensed by the fetch model (disclosed on its item); vSkipper's abstract was condensed with marked verbatim fragments.
- Overlap greps (all this session): per-ID grep over catalog/catalog.jsonl for every banked and considered ID (receipts in item overlap fields); scoped memory grep over memory/frontier, research_packs, research_polished, burns, rib, zknot, improve, lenses for bitnest|edgeagent|tokenrouter|speculate smarter|compute-communication trade-offs: zero hits. A whole-memory grep was started and killed for time; the scoped pass is the receipt, and memory/trajectory showed sibling seats hunting the same day-8 reference concurrently.
- Banked 7 of 8 deep reads; no em-dash used in this file; everything I could not verify is stated as such above.
