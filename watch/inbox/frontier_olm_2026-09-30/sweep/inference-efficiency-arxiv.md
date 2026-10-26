# SWEEP: inference-efficiency via arXiv - frontier_olm 2026-09-30

source-fetched: 2026-09-30. Seat: sweep gopher (inference-efficiency-arxiv). Door: arXiv export API
(export.arxiv.org/api/query) worked; the first `all:"speculative decoding"` query and two others hit the
60s WebFetch timeout, retried with `abs:` prefixes and narrower terms, all succeeded. One WebSearch
returned a junk result set (MacUser 1994 archive) before the useful hits; re-issued with tighter terms.
No door degraded permanently, no fallback fabrication.

## Pass 1 (broad sweep, last 30 days: 2026-08-31 .. 2026-09-30)

Six arXiv API queries, 95 result rows, ~70 distinct candidates considered:

1. `abs:"speculative decoding"` (25 rows): LongSpark 2609.37029, DScale 2609.37532, SEED 2609.36590,
   H-Spec 2609.24197, SPECTRA 2609.24847, SpecQuant 2609.21704, NebulaSD 2609.29364, Mentored Decoding
   2609.30474, Acceptance-Aware Draft Training 2609.24150, Resource-Efficient SpecDec 2609.33184, and more.
2. `all:"continuous batching"` (5 rows): vSkipper 2609.37062, vLLM/llm-d control plane 2609.23130,
   Deadline-Aware Prefill Chunking 2609.07883, GrowPage 2609.03494, Energy-on-Blackwell 2609.29707.
3. `abs:"early exit" AND abs:"language model"` (9 rows): FlexEE 2609.17008, Calibrated Instrument
   2609.18005, One Size Does Not Fit All 2609.14144, AdaVSkip 2609.15131, Don't Drop Dropout 2609.05275.
4. `abs:"on-device" AND abs:LLM AND abs:inference` (20 rows): TierKV 2609.21172, mzCache 2609.01338,
   PELM 2609.09662, LLM Inference in a Flash 2609.16161, Dynamic Flow Static Graph 2609.34727, HA-NPU
   2609.32114, Consumer GPUs diffusion 2609.21849, nondeterminism across GPUs 2609.25624, llama.cpp
   multi-tenant flaw 2609.18526.
5. KV offload/DRAM (16 rows): Where Should the KV Cache Live 2609.16215, Janus SSD agentic 2609.36938,
   PulseInfer 2609.34555, py-kvcache 2609.11744, KV Cache Is the New Memory Wall 2609.30854, Mixed-Fidelity
   KV Runtime 2609.33536.
6. `abs:"inference cost"` (20 rows): RSI-Router 2609.34712, FragToken 2609.31552, JustQuant 2609.33601,
   NVFP4 quantization 2609.36654, READ LoRA 2609.31600.

## Pass 2 (deep reads, pages fetched and read end to end)

11 abs pages read in full: 2609.18005, 2609.17008, 2609.21172, 2609.09662, 2609.14144, 2609.34712,
2609.36938, 2609.16215, 2609.37029, 2609.01338, 2609.29707. Plus one non-arXiv page read end to end
(Stochastic Sandbox token-bucket post, 2026-09-15) for research question 3.

## Dedup (overlap greps run this session)

- `catalog/catalog.jsonl`: TierKV 0, RSI-Router 0, One Size Does Not Fit All 0, mzCache 0, LongSpark 0,
  Where Should the KV Cache Live 0, Janus/SSD-based Sparse KV 0, Energy/Blackwell 0. ALREADY HELD (do not
  re-bank): FlexEE (catalog ts 2026-09-16), PELM (2026-09-10), A Calibrated Instrument (2026-09-17),
  The KV Cache Is the New Memory Wall, H-Spec, SpecQuant, Ask the Tool Don't Guess, py-kvcache, Adaptive
  Prefill Chunking, Interactive Diffusion on Consumer GPUs.
- `memory/` recursive grep for all 8 finalist titles + IDs: only hit is `memory/trajectory/steps.jsonl`,
  which is this session's own logged tool calls (self-hit), not a prior holding. All 8 banked items are new.

## Answers to the five research questions (grounded in what I read/ran this session)

**Q1. Janitor-class receipts.** The closest measured-at-small-scale work: One Size Does Not Fit All
(2609.14144, 1.5B model, intended setting literally "small models on personal devices, where generation
is limited by memory bandwidth rather than computation"); TierKV (2609.21172, three mobile SoCs, 17.6x
prefill, 12.5-34% RAM-resident KV cut); mzCache (2609.01338, MobiCom 2026, llama.cpp base, Android);
already-held FlexEE (Llama2-7B/Llama3-8B, 1.27x/3.16x with 0%/50% weight offloading) and PELM (SenSys'26,
23.1% speedup + 52.4% energy cut). None of the new items ran on consumer Windows x86 desktops; mobile
SoC/Android/server-GPU is the published proxy. Windows-specific receipts remain OWED.

**Q2. Cost per correct verdict per tier.** I ran the ledger math this session: `.venv/Scripts/python.exe`
over `training/cost_ledger.jsonl` (2,439 rows, moment 2026-09-30). ollama: 1,789 rows, 470 success,
usd_est sum $0.00. deepseek: 499 rows, usd_est sum $128.0618, 129 success, $0.99 per success-row. glm:
44 rows, 0 success, $0 priced. grok: 32 rows, 0 success, $0 priced. xai: 4 rows, 0 success. Two blockers
make the crossover OWED: (a) `outcome.success` is task-level, there is no verdict-correctness axis in the
ledger, so "per correct verdict" is not computable from it; (b) the funded-tier rows (glm/grok/xai) carry
usd_est 0.0, i.e. they are not priced in the ledger at all. Nobody in the corpus has computed the
funded-beats-local crossover; RSI-Router (2609.34712) is the published analogue (subtask-level routing
between a large and a small model at 48.3% of large-only cost with better task performance).

**Q3. Rate-limit model match.** No arXiv paper surfaced matching the estate's rolling-throughput /
first-contact-HOLD finding under token-bucket, rate-limit, or burst queries. Academic framing is
"admission control and fair scheduling" per the search synthesis, none of the 70 candidates models a
provider's rolling throughput cap from the client side. Closest external corroboration fetched and read:
Stochastic Sandbox "Token-Based Rate Limiting for LLM APIs" (2026-09-15): variable token cost per call,
bucket accumulates during quiet periods and enforces a sustained rate, capacity controls max burst. That
is consistent with (does not prove) the measured-envelope HOLD reading. A published provider model match:
not found, stated as such.

**Q4. Energy/time ceiling for overnight local inference.** Best measured anchor: Where Does the Energy
Go? (2609.29707, 2x RTX PRO 6000 Blackwell, Qwen3.8-27B): sequential agent workload consumes 63x more
system energy per output token than saturated serving; GPU-only telemetry misses 41-45% of system energy;
continuous batching improves system energy efficiency 3.2x from 1 to 16 req/s; extended thinking adds
21-75% tokens with <1% per-token energy difference. This is datacenter hardware, not consumer Windows;
treat as directional. Already-held PELM covers the on-device energy knob (speculative decoding + DVFS,
52.4% energy cut). Complexity verdict at estate scale: with ollama rows at $0.00 and a 9.34s test suite,
the estate's binding constraint is verdict quality and funded-tier pricing, not local tokens/sec; the
steal is the measurement instruments (calibrated judge, whole-system energy telemetry), not new serving
engines.

**Q5. Deliberate-ask economics vs current pricing.** The structural shape holds: `configs/cost_rates.yaml`
still prices cache hits at a 5-30x discount (glm-5.3: hit $0.26/M vs miss $1.4/M; grok-4.5: $0.3 vs $2.0;
deepseek-v4-flash offpeak: $0.007 vs $0.22), so the prefix-freeze mechanics that took hit-ratio 6.5% to 98%
(`watch/inbox/frontier_olm_2026-09-30/lens/laws.md:28`, citing `memory/rib/RIB_SELF_MY_EFFICIENCY.md:6-9`)
still pay. But the $161 to $3.60 absolute figures are from that rib's older price regime, and
`configs/cost_rates.yaml` has NO rows for glm-5.3-prime, qwen3.8-max-prime, or grok-4.7 (the current funded
set per `memory/rib/RIB_DRIVING_LADDER_20260928.md`). Re-measure with instrument, moment, and context named
(the ONE-BUG law, `lens/laws.md:18`): OWED. I did not run a paid re-measure this session.

## Banked items (8, strongest first)

1. **One Size Does Not Fit All: Setting Inference Depth from the Questions a Deployment Actually Asks**
   (arXiv:2609.14144, 2026-09-12, Kaplan). Quote: "on arithmetic word problems, three models each answered
   sixty questions correctly when run in full, and between 10 and 28 correctly under early exit". Why: the
   token-level-fidelity metric hid a 60/60 to 10-28 correctness collapse on a 1.5B model in exactly the
   janitor's memory-bandwidth regime; this is the receipts-not-vendor-claims trap for any early-exit or
   layer-skip knob the estate bolts onto gemma janitors. Overlap: 0 in catalog.jsonl, 0 real in memory/.
   Confidence 0.95.

2. **Where Should the KV Cache Live? Placement Policies Across GPU, CPU, and SSD for Long-Lived Sessions**
   (arXiv:2609.16215, 2026-09-14). Quote: "Tiering supports 73.02 times more concurrent sessions per GPU
   and lowers cost per session by 62.04 times. These gains come from tier capacities of 1 plus 8 plus 64,
   not placement policy." Why: negative-results receipts for consumer-tier memory tiering: prefetching
   never justified (oracle included), predicted reuse byte-identical to recency, decode compute-bound at
   batch size 1, which is the janitor's regime. Overlap: 0 / 0. Confidence 0.92.

3. **Efficient Agentic LLM Serving over SSD-based Sparse KV Storage** (Janus, arXiv:2609.36938, 2026-09-29).
   Quote: "Janus outperforms existing works by up to 1.57-3.69 times (1.22-1.85 times on average) in terms
   of the time to first token latency, while maintaining decode efficiency." Why: agent loops that
   alternate inference and tool calls are the estate's own shape; SSD-centric KV with predicted reads
   overlaps storage with compute on commodity SSDs. Overlap: 0 / 0. Confidence 0.9.

4. **TierKV: Long-Context On-Device LLMs via Predictive Multi-Tier KV Caching** (arXiv:2609.21172,
   2026-09-18). Quote: "PMCO predicts future cache demand from prefill hidden states and jointly assigns
   tokens to exact, low-rank, and flash-offloaded tiers". Why: measured on three mobile SoCs, 17.6x prefill
   throughput and 12.5-34% RAM-resident KV reduction with full-context retention; the constrained-RAM
   playbook for janitor-class boxes. Overlap: 0 / 0. Confidence 0.9.

5. **Where Does the Energy Go? Profiling LLM Agent Inference on Blackwell GPUs** (arXiv:2609.29707,
   2026-08-31). Quote: "the sequential agent workload consumes 63x more system energy per output token than
   saturated serving". Why: first whole-system (NVML+RAPL+IPMI) energy receipts for agent-shaped workloads;
   quantifies the overnight-loop energy premium and the batching efficiency wall the offpeak queue lives
   under. Overlap: 0 / 0. Confidence 0.9.

6. **RSI-Router: Evolving Subtask-Level LLM Routing and Skills for Cost-Efficient Agents**
   (arXiv:2609.34712, 2026-09-28). Quote: "RSI-router consistently surpasses the DeepSeek-only baseline at
   roughly half the inference cost (48.3%) across five agentic benchmarks." Why: the published, measured
   form of the funded-beats-local crossover question: within-task large-small model collaboration with a
   Pareto router, the design template for a Mag driving-ladder router that the cost ledger cannot yet
   build. Overlap: 0 / 0. Confidence 0.9.

7. **mzCache: On-Device LLM Memory Management under Multitasking** (arXiv:2609.01338, 2026-09-01, MobiCom
   2026). Quote: "mzCache achieves 2.1-5.5x reduction in Time-to-First-Token compared to storage-backed
   partial offload and demonstrates its effectiveness in real multitasking scenarios." Why: llama.cpp-based,
   built for OS memory pressure evicting model weights and KV mid-run; the Windows desktop janitor lives
   under exactly this multitasking eviction. Overlap: 0 / 0. Confidence 0.9.

8. **Token-Based Rate Limiting for LLM APIs** (Stochastic Sandbox, 2026-09-15,
   https://stochasticsandbox.com/posts/token-based-rate-limiting-for-llm-apis-2026-09-15/). Quote: "For LLM
   rate limiting, each API call removes a variable number of tokens from the bucket rather than a fixed
   count." Why: the only fetched source modeling provider limits the way the estate measured them
   (variable-cost token bucket, quiet-period burst accumulation, sustained-rate enforcement); consistent
   with the rolling-throughput/HOLD envelope, not proof of it. Overlap: not in catalog.jsonl or memory/
   (checked "Token-Based Rate Limiting" indirectly via the pattern sweep; no engineering-blog entries are
   held). Confidence 0.9.

## Not banked, worth knowing

LongSpark 2609.37029 (fixed-cost drafter, drafter cost independent of prefix length; no hardware or
numbers on the abs page) and vSkipper 2609.37062 (layer-skip pluggable into serving engines while
preserving continuous batching) are strong follows if the estate ever runs long-context janitors.
Already-held-but-central: A Calibrated Instrument 2609.18005 (calibrated LLM-judge with null condition;
4-bit indistinguishable at +-0.3 resolution, early exit costs 2.5 points on math) is the instrument to
steal for Q2's correctness axis; it is in catalog.jsonl since 2026-09-17, so not re-banked.

## OWED ledger from this sweep

- Funded-vs-local cost-per-correct-verdict crossover: OWED (ledger lacks correctness axis and funded-tier
  pricing; run path: add verdict-correctness to outcome + price glm/grok/xai rows).
- glm-5.3-prime / qwen3.8-max-prime / grok-4.7 rows in configs/cost_rates.yaml: OWED.
- Deliberate-ask $161 to $3.60 re-measure on current funded pricing, instrument+moment+context named: OWED.
- Consumer-Windows-x86 receipts for early-exit/KV knobs at gemma:2b scale: OWED (published proxies are
  mobile SoC / Android / server GPU).
