# Sweep: inference-efficiency via arxiv - 2026-10-10

source-fetched: 2026-10-10. Gopher seat: sweep-inference-efficiency-arxiv. Doors used: arXiv Atom API (export.arxiv.org: 6 search queries in the submittedDate window 2026-09-10..2026-10-10 plus 2 id_list fetches), one site:arxiv.org WebSearch, and the HN objectID 50032575 outbound article at data4sci.com. Every quote below is verbatim from a page fetched this session.

## Method

Pass 1 (broad sweep): queries "LLM serving", "KV cache", "speculative decoding", "efficient reasoning", "consumer GPU", "overthinking" returned ~110 entries, ~45 on-topic in-window; census exceeds the 30-item floor. Door degradations, honestly: (a) the first "KV cache" query timed out at 60s; retry at max_results=20 succeeded. (b) Four arxiv.org/abs fetches timed out at 60s late in the session; the fallback was the authoritative export.arxiv.org id_list API for those items (abstracts fetched from the API door, not the abs pages).

Pass 2 (deep read): 13 items read in full at abstract level or better; 2610.03228 and 2609.31619 additionally read end-to-end at arxiv.org/html full text. 8 banked after overlap pruning, strongest first.

## Overlap verdict and method (run before banking)

Instrument: `grep -c/-i/-F` per title and distinctive phrase against catalog/catalog.jsonl; per-ID grep against catalog; `ls state/arxiv/*/ID*` disk check; two-lane recursive grep of memory/ (13G, 752k files): big-file lane over ingest/registry.jsonl (5.3G), decisions_log.jsonl, runs/ trails, training/events.jsonl, trajectory/steps.jsonl, mesh indexes; small-file lane over the rest excluding tar/zip/pdf. Result: 5 of my 13 deep-read items were ALREADY HELD and were NOT banked (see next section); the 8 banked items have zero catalog hits by title, phrase, or ID, and no state/arxiv file on disk. The only memory/ hits for banked titles are in memory/trajectory/steps.jsonl, which records this session's and a sibling sweep seat's own grep commands (verified by reading sampled rows: my findstr loop appears verbatim there), i.e., the trajectory logger, not holdings. Name hits "Galahad"/"Lachesis"/"Comoe" in memory/ are Plato and Project Gutenberg ractor texts (pg1497, pg55201, pg22650, pg53985), classical corpus, unrelated. Note for the fold: a sibling sweep seat ran overlap greps over an overlapping title set TODAY (its command is recorded in steps.jsonl), so cross-seat dedupe within today's frontier_olm batch is worth a check before promotion.

## Grounding for RQ1: the HN objectID 50032575 article (read in full)

HN item 50032575 = "Local LLM Inference at Scale with vLLM" -> https://data4sci.com/blog/local-llm-inference-at-scale-with. Facts: single DGX Spark (GB10, 128GB unified LPDDR5x, 273 GB/s), vLLM, Qwen3.5-35B-A3B-FP8. "Starting with 34 tokens/s for single request and climbing to 284 tokens/s at the 256 requests level". Config: max_num_seqs=256, gpu_memory_utilization=0.50, enable_prefix_caching=True, 28.8 GiB KV cache, 69% prefix-cache hit on a 1,235-token shared prefix. The article states vLLM "was built from the ground up for Linux" and makes NO Windows claims. Implication: the vLLM-class win is BATCHING (8.4x single-to-256-batch), not single-stream decode (34 tok/s single-stream on a 273 GB/s part); the estate's Windows ollama fleet cannot inherit these numbers without a WSL/Linux bridge, itself a standing-wave cost. Instruments-only law applies: nothing there is reproducible on our Windows host as-published.

## Banked items (strongest first; all verified new)

### 1. arXiv:2610.03228 - Execution-Path Qualification and Realized Costs in Speculative Decoding on Consumer Systems (2026-10-02, Chengzhan Li, sole author)
Read: abs + full HTML. Hardware: Intel Arc B570, RTX 5070 Ti Laptop, MacBook Air M4, Core Ultra X7 358H w/ Arc B390. On QUALIFIED paths (captured token IDs exactly matching a frozen greedy reference), speculative decoding mostly LOSES to target-only on consumer stacks: RTX serialized 0.646x target/serialized latency (0/30 prompts favored serialization), 358H CPU 0.734x / NPU 0.352x, M4 mixed (0.842x representative vs 1.387x HumanEval k=2). Body: "Serialization is slower within this qualified measured boundary."
Estate fit (RQ3, RQ1): the instruments-only law vindicated in print. The 3-5x speculative-decoding multipliers all over this month's arXiv (APEX 4.27x, NSD 5.16x, AgSpec 4.37x) are datacenter/batched claims that do not survive qualified single-host consumer measurement. Feeds RIB_INFERENCE_BUDGET: any spec-decode A/B on the janitor fleet needs a qualification gate (frozen greedy reference, exact-ID match) or it is uninterpretable.

### 2. arXiv:2610.02491 - What Does a Token Cost? A Mixture-of-Agents Measurement of Sufficient Per-Token Compute (2026-10-01, Zhixu Du et al.)
Read via API door. A 15-model Mixture-of-Agents panel where each agent tries to reproduce a reference sequence token by token; the smallest successful agent's cost defines the token's sufficient compute. "a 0.5B agent reproduces 92--95\% of reference tokens" and "The MoA-map helps drafting use 32.6\% fewer draft tokens" with roughly 20% lower projected latency.
Estate fit (RQ2, RQ3): an outside instrument for the estate's cheap-janitor-first doctrine. It quantifies, per token, when the small local model is ENOUGH: a 0.5B agent reproducing 92-95% of reference tokens is the arithmetic behind routing most work to gemma:2b and climbing only on the divergent tail. This is a measurement method (per-token sufficient compute) the estate's quant A/B instrument could adopt as a grading column.

### 3. arXiv:2610.08378 - Lachesis: Lifetime-Aware KV Cache Placement for Agent Serving across HBM and High-Bandwidth Flash (2026-10-06, Jaehoon Yang et al.)
Read: abs. High-bandwidth flash gives ~10x HBM capacity at HBM-class read bandwidth but finite write endurance; Lachesis places KV segments by lifetime (temporal/structural/inter-worker axes read from the agent harness) so HBM absorbs the writes. "Lachesis extends HBF lifetime by 1.19-3.13x over HBM-first placement, reaching 3.3-12.2 device-years." Under continuous 24x7 full load, HBF outlasts its 5-year warranty.
Estate fit (RQ4): the standing-wave question answered WITH a new budget class: serving-stack growth onto flash is absorbable only if writes are budgeted in device-years (write-endurance lifetime), a unit smith's DISK ETA alerts can adopt directly. Caveat: trace-driven simulation, not hardware measurement; treat numbers as planning units.

### 4. arXiv:2610.11358 - RaReCache: Cross-Model KV Cache Reuse via Rank Disagreement-based Selective Recomputation (2026-10-08, Sreetama Sarkar et al.)
Read via API door. A large target model decodes from a cache prefilled by a small source model, selectively recomputing the few information-dense positions where a rank-disagreement metric flags divergence; largely removes sensitivity to source model size, five benchmarks, two model families, single GPU. "at the target's saturation load, reduces median and 99th-percentile time-to-first-token (TTFT) by 5.0x and 6.4x" on a single GPU.
Estate fit (RQ1): the exact fleet shape we run, small scut prefills for the big worker. If the estate ever fronts ollama with a shared context (corpus packs, session briefs), small-source prefill + selective recompute on one consumer GPU is the published mechanics for it; 3.04x prefill speedup at a 30% recompute budget per the serving query's abstract line.

### 5. arXiv:2610.11245 - Read What Matters: Query-Adaptive Quantization for KV Caches (2026-10-08, Siddharth Bhandari et al.)
Read via API door. KV entries stored in progressive codes whose prefixes support multiple precisions; each decoding query allocates key-channel then value-token prefixes. "reading four bits on average from an eight-bit cache increases C4 perplexity by at most 0.66%" with 39% lower latency than a TurboQuant baseline on an A10G.
Estate fit (RQ1, RQ4): read precision as a budget dial. For a memory-bound single host, the write happens once at full precision and the per-query READ cost is chosen per need; that asymmetry is a new lever for the GB/day ledger (reads are not writes; flash endurance accounting separates them). Hardware was a datacenter A10G, so numbers are directional for us.

### 6. arXiv:2610.09025 - SPIN: Shadow Predictive Indexer for Sparse Attention (2026-10-06, Yao Fu et al.)
Read via API door. Lightweight history-based prediction of important KV blocks so the indexer stops scoring the whole cache every step; KV blocks and speculative decoding treated as first-class; evaluated in vLLM serving on long-context and agentic benchmarks. "SPIN improves output throughput by up to 14.9% and reduces median inter-token latency by up to 13.2%" (from the serving-door listing: 30-40% sparsity).
Estate fit (RQ1): the honest face of vLLM-class engine work: 14.9% output throughput, 13.2% ITL, not 5x. Agentic long-context workloads in a real engine; the kind of claim an instruments-only law can actually test.

### 7. arXiv:2610.03394 - EdgeAgent: On-Device LLM Inference for End-User Multi-Agent Systems on CPU-GPU Unified Memory Architectures (2026-10-02, Yuhai Long et al.)
Read: abs. Multi-agent on-device serving co-designed for UMA: zero-copy UMA-aware tensor parallelism, predictability-driven draft budgets, async suspend-and-yield evicting stalled agents during tool calls. "Adding the agent-aware scheduling lifts the full EdgeAgent system to a 1.77x speedup under extreme tool-use latencies" (UMA-aware execution alone 1.29x). Apple M4 evaluation.
Estate fit (RQ1): the janitor-fleet shape (many small agents, tool-induced stalls, shared memory) measured as a first-class workload class. Not Windows, not CUDA; the portable idea is the scheduler: evict agents stalled on tools, budget drafts by observed per-sequence predictability.

### 8. arXiv:2610.02800 - BitNest: Bit-Nested Speculative Decoding for Memory-Efficient LLM Inference Acceleration (2026-10-02, Chence Yang et al.)
Read via API door. Builds a strong low-precision draft INSIDE the higher-precision target so both share one physical weight set, extends progressive precision to the KV cache; 7B-8B edge-friendly models. "achieves an average speculative acceptance rate of 95.2% while closely preserving higher-precision model quality" and 1.48-1.61x end-to-end speedup over FP16.
Estate fit (RQ1, RQ3): the memory-bound single-host answer to speculative decoding: no separate draft weights to host (our VRAM ceiling), honest 1.5x-class gains on edge-sized models. Pairs with item 1's warning: 95.2% acceptance is their stack, ours must be qualified before banking any speedup.

## Read, verified ALREADY HELD, not banked (deepening notes for the owners)

These four were deep-read BEFORE the overlap check flagged them; the full-text deltas beyond our held abstract-text files are recorded here so the reading is not lost:

- 2609.31619 "Learning to Stop without Learning to Stop" - HELD: catalog id daa525a7bb8c, state/arxiv/2026-09-28/2609.31619v1.txt. My HTML full-text read adds: "ConfSFT reduces tokens by 11.1%, 10.3%, 19.2%, and 11.1% on Nemotron, Gemma, Qwen, and GPT-OSS, respectively", accuracy deltas +1.1/-0.7/0.0/-0.6 all n.s., trained on ~600-695 AIME problems. Directly covers our Gemma/Qwen janitor families. RQ2 evidence.
- 2609.39358 Galahad byte-exact memory - HELD: catalog id 0b71afd72154, state/arxiv/2026-10-01/2609.39358v1.txt. Abstract already carries the headline (100/100 at 0.59-0.64 s and 200-213 J; 262,144 logits bit-identical; works with llama.cpp; fails closed).
- 2610.03509 CoT Faithfulness and Monitorability - HELD: catalog id f46cfb080140, state/arxiv/2026-10-05/2610.03509v1.txt. The RQ2 caveat: "Faithfulness falls in most settings... Monitorability is more robust". Thinking-off savings should carry a faithfulness debit.
- 2610.07863 ReFold inter-turn context folding - HELD: catalog id 86a8722b6410, state/arxiv/2026-10-07/2610.07863v1.txt. 2.5x token cut, halved per-session KV, training-free, reversible; pairs with our compaction-stall work.
- 2609.40093 ThunderEP PCIe consumer-GPU expert parallel - HELD: catalog line + state/arxiv/2026-10-01/2609.40093v1.txt on disk (2.00x/1.53x over NCCL dispatch/combine, vLLM-integrated). Found during replacement search, dropped from banking.

Honorable mention, read and clean but not banked (slots went to single-host fits): 2610.09424 CoMoE, "improves inference throughput by up to 1.46x" on dual RTX 5090 approaching NVLink A800 at 23.4% cost. Multi-GPU rig, so directional only for us; carries the MoE-is-the-local-direction signal alongside the data4sci article's Qwen3.5 MoE choice.

## Answers to the four research questions

RQ1: vLLM-class advances reach a Windows ollama fleet only through (a) batching (the data4sci 8.4x needs 256 concurrent requests, a Linux-first engine, and 273 GB/s unified memory; we have none of the three as-published), (b) memory layers that survive down to llama.cpp-class runtimes (held Galahad item), (c) cross-model cache reuse (RaReCache, single GPU), and (d) scheduler-level eviction of tool-stalled agents (EdgeAgent). Nothing in this window was measured on Windows.

RQ2: yes, outside evidence exists to regrade the suspect rows, and it is two-sided: held-item ConfSFT gives ~10-20% thinking-token cuts at matched accuracy on our exact model families, while held-item 2610.03509 prices the faithfulness loss. Banked item 2610.02491 adds the per-token sufficient-compute method (0.5B reproduces 92-95% of reference tokens) as the grading instrument. The tie-at-ceiling quant A/B stays banked and instrument-scoped as instructed; EMPTY_REASONING rows untouched, never refired.

RQ3: the claim class that survives is item 1's: negative, qualification-gated consumer measurements, plus honest engine-level percentages (SPIN 14.9%/13.2%) and single-weight-set 1.5x-class wins (BitNest). The 3-5x spec-decode multipliers saturating this month's arXiv are the non-reproducible class for one consumer Windows host.

RQ4: standing-wave GB/day absorbs a local serving stack only with a NEW budget class: flash write endurance in device-years (Lachesis) and a one-time-cost ledger for repeated reads (held Galahad: corpus stored once at ~28 kJ, recovered after 13 questions; Read What Matters separates read precision from write cost). Not a bigger GB/day number: two new columns.

## OWED / not done

- No Windows-native serving benchmark found in-window; the Windows-gap claim rests on the data4sci article's Linux statement alone. OWED.
- Lachesis numbers are trace-driven simulation, flagged above.
- Four late-addition abstracts were read via the export.arxiv.org id_list API after arxiv.org/abs timed out; the API is the same authoritative metadata door, but no HTML full text was read for items 2, 4, 5, 6, 8. Stated, not hidden.
