# SWEEP: inference-efficiency via X - 2026-10-02

source-fetched: 2026-10-02

Seat: sweep-inference-efficiency-x (frontier sweep gopher, Mag Resource Harness).
Doors: WebSearch (Z.ai web_search_prime backend) for discovery; fxtwitter door
(`https://api.fxtwitter.com/<user>/status/<id>`) for resolution; WebFetch for the two
non-X primaries worth reading whole. Every banked item below was read in this session.
No em or en dashes anywhere in this file. Window: last 30 days (floor approx 2026-09-02,
snowflake-derived; the 10-01 sweep used ID >= 2094575964779446272 = 2026-09-01).

## Coverage against the four research questions

**Q1 - KV-recompute vs prefill beyond the banked 17.5/33.1/~49.4 pct decomposition and
the ~60 pct fill cliff; do they reproduce outside the original stack?**
No post-10-01 (Oct 1-2) X-indexed result surfaced; the freshest in-window item is
2026-09-24. The answer is still strong: the fill-cliff physics reproduces outside the
original stack at production scale. The banked decomposition came from doug.sh + HN
single-node discussion (frontier_olm_2026-09-30 DIGEST rows 7-11). The Nebius+WEKA
benchmark (2026-09-24, read end to end) replays 8 hours of captured production agentic
coding traffic (512-session active pool, contexts to 900k tokens) on 8x HGX B300 with
vLLM v0.23: HBM-only holding degrades over the soak (median TTFT 6.7s first hour to
7.9s last, timeouts 1.1 to 5.2 pct) and hits only 40 pct cache rate, while a shared
WEKA tier over GPUDirect RDMA holds 93 pct, cuts uncached tokens per request from
33,900 to 4,400, and lifts requests served 2.4x and output tokens per GPU-hour 3.7x
(169,000 vs 46,000). Their statement of the tradeoff is the decomposition's money
sentence: each turn "prefills the full history to process the few thousand tokens it
actually added" once KV blocks are evicted. The vLLM x AgentX report (2026-09-08,
read end to end) is the engine-side confirmation on real agent traffic: median 43
turns per session, median input 142k tokens, "Prefix-cache hit rate above 96%", and
shipped scheduler fixes ("--long-prefill-token-threshold", up to 93 pct TPGS gain,
"--prefill-schedule-interval") plus MooncakeStore distributed KV offloading. The
CompleteSkeptic bill math (2026-09-09) prices the same physics: cache reads are the
majority of a long-turn agent bill and the difference between 89 and 100 pct hit rate
is an 84 pct penalty in their simulator. REPRODUCTION VERDICT: yes, the cliff
reproduces on three independent stacks (doug.sh/HN single-node, Nebius/WEKA B300 farm,
vLLM AgentX fleet telemetry).

**Q2 - cache-invalidation classes like the vLLM tool-schema key-order bug (78 to 95
pct cached share): shipped fixes or published reproductions since?**
Two published reproductions in-window. (a) The held Avi Chawla article (2026-09-06,
banked by the 10-01 kv-cache sweep, do not re-bank) enumerates vLLM prefix-cache match
breakers verbatim: "A timestamp in the system prompt, reordered JSON keys in a tool
schema, or different chat-template whitespace." (b) NEW: probiex007 (2026-09-24,
resolved through fxtwitter) restates the class from the provider side: "Change the
prompt structure, tool definitions, or ordering, and cache hit rates can fall sharply."
Shipped engine fixes: the vLLM x AgentX report names merged PRs (#44577, #43447,
#47782, #46188, #45444, #45659, #47317, #48582, #52079, #53152, #43584, #44230,
#43008) and two scheduling flags with measured gains; the flag fix
"--long-prefill-token-threshold" alone is credited with up to 93 pct total-tokens-per-
GPU-second gain. I did not verify individual PR bodies (OWED, see gaps).

**Q3 - linear-attention / hybrid / neuromorphic serving results with TTFT tables
comparable to the banked SpikingBrain-7B table (7.3x at 256k to 26.5x at 1M on H100s),
on hardware the five GPU gates would admit?**
Weakest lane; stated honestly. The five gates (memory/rib/RIB_GPU_LADDER_20261001.md:
10-24) require SM90/SM100 for full pay, 24 GB minimum VRAM, price triggers, vLLM/SGLang
on FP8, and real workload. No in-window item publishes a SpikingBrain-class TTFT table
on gate-admitted hardware. What the window does hold: (a) a negative result on consumer
VRAM - superalesha's 4x RTX 3090 GLM-5.3 Flash attempt (2026-09-07, read end to end):
the EXL3 Q4 checkpoint is 187.45 GB against a 96 GB budget, expert pruning of 62.5 pct
made it run but he wrote "I still didnt trust it with real work"; final fused path
~295 tok/s prefill at 4k context, ~284 tok/s prefill / 10.76 tok/s decode at 8k, and
quality plus long-context speed fell short. Ampere is "never buy" under gate 1, so this
confirms the gate rather than moving it. (b) A positive consumer datum, snippet-only
(see item 6): Qwen3.8-27B hybrid attention at 90-95+ tok/s through 100k context on ONE
RTX 3090, 240-262k ctx. (c) Out-of-window context, not banked: SpikingBrain2.0
(arXiv 2604.22575, v1 2026-04-24, read in full) reports "a 10.13x TTFT speedup at 4M
context" and serving beyond 10M tokens on 8x A100 under vLLM - already held
(watch/inbox/gala_20260925/spiking-wide/lanes/sb_gh_readme.md), its A100s fail gate 1,
and 5B/2.52x-at-250k FP8 numbers do not clear the banked 7B table's class. QSA
(Alibaba_Qwen 2026-08-26, resolved): "up to 7.6x faster in prefill and 4.9x faster in
decode" at 1M context - 37 days old, outside the window, context only.

**Q4 - the frontier's measured state of efficiency per landed deliverable (tokens or
dollars per artifact), the denominator the descent falsifier demands?**
The frontier is converging on the estate's own denominator, and the estate coinage now
has independent frontier confirmations. (a) probiex007 (2026-09-24): the builder advice
is to measure "cost per completed task, not cost per request" - grep proof the estate
already mints this phrase internally (memory/runs/compaction_eval/
steps_frozen_20260920.jsonl, memory/runs/quote_audit_wide_20260925/inbox_concat.txt);
the X post is corroboration, not new doctrine. (b) vLLM x AgentX measures serving-cost
per benchmark task: "a 14.6x-106x serving-cost advantage over Opus 5 API pricing" for
open stacks on the SemiAnalysis AgentX workload. (c) CompleteSkeptic (2026-09-09)
decomposes where the dollars actually go: cache reads dominate agent bills, so the
per-artifact cost is a cache-behavior property, not a model-price property. Out-of-window
context (not banked, both read end to end): Artificial Analysis AA-Briefcase
(2026-06-18) measured a roughly 800x cost-per-task spread across models ($0.04 DeepSeek
V4 Flash to $31 Claude Fable 5, GLM-5.2 max at $2.40 about 90 Elo under Opus 4.8 max at
under 25 pct of the cost); Signal65 PINNACLE (2026-08-31) measured "input tokens were
65% to 91% of the cost of a correct task on the hosted models" and that pricing by
output tokens alone understates cost per correct task by 3-11x. Those two are the
missing rungs if the estate ever wants a scoreboard to audit the descent falsifier
against; both are 32+ days old, so they ride as leads, not findings.

## Method and counts

- Pass 1: 11 WebSearch queries (site:x.com flavored); several hit 429/1302 rate-limit
  storms and were retried or re-phrased (the known account-cap behavior, see the
  fan-out width law in AGENTS.md). Approx 40 unique candidates surfaced, including
  r/Vllm and r/Qwen_AI primaries that are auth-walled from this network per the doors
  lens (doors.md:56) and were taken only as search snippets.
- Pass 2: 14 full reads through fxtwitter/WebFetch: Alibaba_Qwen QSA post, AA-Briefcase
  posts, probiex007, CompleteSkeptic post (child article 404'd on fxtwitter, flagged),
  superalesha article, pupposandro article, avichawla KV-Engineer article, PINNACLE
  article, shmidtqq article, vLLM x AgentX article, NVIDIA KV-transfer post, Nebius blog,
  VAST/Lablup blog, llm-d blog, SpikingBrain2.0 arXiv abstract. That is 15 counting the
  arXiv page; at least 5 end-to-end reads of banked-class items are satisfied by the six
  banked items' reads alone.
- Window filter: snowflake-derived floor approx 2026-09-02. Out-of-window candidates
  were considered and filtered, not banked (list below).
- Overlap greps run per banked candidate against catalog/catalog.jsonl (871,790 rows)
  and memory/ plus watch/inbox/, phrases: SpikingBrain2.0, Nebius, WEKA,
  "Augmented Memory Grid", "cost per completed task", "Diogo Almeida",
  "KV Cache Engineering", "AA-Briefcase", PINNACLE, "GPT-6 Sol", "GLM-5.3 Flash",
  AgentX, 2608.03893, "KV cache transfer", "240K", Mooncake.
- Dedupe drops (genuinely held, not re-banked): Avi Chawla "KV Cache Engineering for
  LLM Serving" (already item 6 of watch/inbox/frontier_olm_2026-10-01/sweep/
  kv-cache-context-engineering-x.md); SpikingBrain2.0 (gala spiking-wide lane);
  NVIDIA cross-model KV transfer arXiv 2608.03893 (verified held in
  memory/research_packs/bibverify/MASTER_20260920.md, "cross-model KV transfer
  (2608.03893)"); Mooncake/LMCache KV-as-OS framing (memory/lattice/latest.md:32).

## Banked items (strongest first)

1. Nebius + WEKA - shared KV cache benchmark for agentic inference (2026-09-24)
   https://nebius.com/blog/posts/nebius-weka-shared-kv-cache-benchmark-hgx-b300
   Quote: "prefills the full history to process the few thousand tokens it actually added"
   Why: the fill cliff reproduces outside the original stack at production scale, and the
   fix class (shared KV tier over GPUDirect RDMA) ships with measured numbers - 93 vs 40
   pct hit rate, 4,400 vs 33,900 uncached tokens per request, 2.4x requests, TTFT p50
   1.05 vs 5.68s - the exact instrument shape the KV degradation ladder steal card wants.
   Overlap: "Nebius" hits are namesakes (research pack cites the SWE-rebench dataset);
   "WEKA" hits are agent-session/biography noise; "Augmented Memory Grid" 0 hits outside
   my own trajectory echo. Genuinely new.
   Confidence 0.9.

2. vLLM - vLLM x AgentX: Optimizing for Real-World Agentic Serving (2026-09-08)
   https://x.com/vllm_project/status/2097427730983776758
   Quote: "a 14.6x-106x serving-cost advantage over Opus 5 API pricing"
   Why: the engine-side state of the art for exactly this area - "Prefix-cache hit rate
   above 96%" on median 43-turn / 142k-input sessions, MooncakeStore offload, PCP 2.65x
   prefill speedup on DeepSeek V4, DCP 13 pct per-layer cut on Kimi K3, the
   "--long-prefill-token-threshold" prefill-stall fix worth up to 93 pct TPGS, and named
   PRs - one artifact answering Q1, Q2 and Q4 at once.
   Overlap: "AgentX" catalog hits are unrelated arXiv titles (2609.30001, AgentXploit
   2609.31318); Mooncake/KV-as-OS framing already held at memory/lattice/latest.md:32 -
   the new bytes are the agent-traffic measurements and the shipped-fix list.
   Confidence 0.85 (read through the fxtwitter article payload; excerpts verbatim,
   PR list as rendered by the reader).

3. probiex007 - on GPT-6 Sol/Luna agent economics (2026-09-24)
   https://x.com/probiex007/status/2103017100944298268
   Quote: "Change the prompt structure, tool definitions, or ordering, and cache hit rates can fall sharply."
   Why: the frontier restating both estate laws in one post - the invalidation class
   (Q2) and the descent falsifier's denominator: measure "cost per completed task, not
   cost per request" (Q4). Also carries the GPT-6 Sol/Luna 50 pct API price cut and
   up-to-90-pct discount on reused context.
   Overlap: "cost per completed task" already minted internally (compaction_eval
   steps_frozen_20260920.jsonl, quote_audit inbox_concat) - corroboration not doctrine;
   "GPT-6 Sol" naming held at memory/continuity/seat_memory_20260927/
   union-alpha-free-window-20260916.md:84 and x-radar-20260917-astra-leak.md:12; the
   measured economics detail is the new part.
   Confidence 0.9 (resolved through fxtwitter with verbatim excerpts).

4. CompleteSkeptic (Diogo Almeida) - (KV) Cache Rules Everything Around Me (2026-09-09)
   https://x.com/CompleteSkeptic/status/2097738214589215173
   Quote: "Wrote about the incredibly important KV cache: Why are people spending so much on agents; How is inference so profitable all of a sudden (+ why it won't last)"
   Why: the bill-side decomposition of agent serving cost - cache reads approx 76 pct of
   a modeled 100-turn bill, 84 pct penalty at 89 vs 100 pct hit rate, 95-to-98 pct hit
   saves approx 17 pct, 40-70x subscription subsidy math, and the claim that cache
   behavior constrains coding-agent design space. The Q4 denominator in accounting form.
   Overlap: "Diogo Almeida" held only for his JEV paper (x-drops-20260925-late.md:28,
   LINKS-338); the KV-cache economics article is not held. The child article
   (x.com/i/article/2097567913490411520) 404'd on the fxtwitter door - banked from the
   resolved parent post; article numbers are reader-door summaries.
   Confidence 0.75.

5. superalesha - I failed to make GLM-5.3 Flash usable on 4x RTX 3090 (2026-09-07)
   https://x.com/superalesha/status/2096976602127044995
   Quote: "I thought 'one more fix' would get GLM-5.3 Flash working properly on 4x3090."
   Why: a published negative result on exactly the hardware class the estate's GPU gates
   forbid (Ampere): 187.45 GB EXL3 Q4 checkpoint vs 96 GB budget, 62.5 pct expert pruning,
   quality collapse, 10.76 tok/s decode at 8k - the five-gate law in empirical form, and
   a methodology kit (REAP exact-replay 19/25, frequency-vs-importance correlation approx
   -0.22) worth raiding if any local-MoE pruning is ever attempted.
   Overlap: GLM-5.3 Flash is held as the MODEL the estate runs on ZCode (catalog +
   agent_sessions hits); the 4x3090 experiment and its artifact release
   (anonymousmaharaj/GLM-5.3-Flash-Research-Artifacts) are new.
   Confidence 0.85 (read through the fxtwitter article payload).

6. X article - How to hit 240K context and 90+ TPS with Qwen3.8-27B (approx 2026-09-04,
   snowflake-derived; UNRESOLVED thread)
   https://x.com/i/article/2095646450138874095
   Quote (search snippet, banked per the fallback rule): "allow users to reach 240,000-token context window, decoding at about 75 tokens per second through 100K tokens of context."
   Why: the positive consumer counterpart to item 5 - a hybrid linear-attention 27B held
   at 90-95+ tok/s through 100k generated tokens on a single 24 GB RTX 3090 (r/Qwen_AI
   1wg9tig config, r/LocalLLaMA 1wsmtd4 follow-up at 262k ctx) - the workload tier where
   hybrid attention beats the quant lane on gate-forbidden hardware.
   Overlap: "240K" hits in catalog/memory are unrelated (orphans audit, ai_canon HTML,
   MANIFEST). New.
   Confidence 0.55. NOTE: the i/article URL could not be resolved through fxtwitter
   (no author handle available; the door needs <user>/status/<id>) and the reddit
   primaries are auth-walled from this network (doors.md:56); banked as search-snippet
   only, never as a verified table.

## Out-of-window context (read, not banked, cited for the next seat)

- Artificial Analysis AA-Briefcase (2026-06-18): approx 800x cost-per-task spread,
  $0.04 (DeepSeek V4 Flash) to $31 (Claude Fable 5); GLM-5.2 max $2.40 at approx 90 Elo
  under Opus 4.8 max. https://x.com/ArtificialAnlys/status/2067744637155226101
- Signal65 PINNACLE (2026-08-31): "input tokens were 65% to 91% of the cost of a
  correct task on the hosted models"; output-only pricing understates cost per correct
  task 3-11x; B300 node held approx 3x the concurrent agents of H200.
  https://x.com/ryanshrout/status/2094489388562481167
- VAST Data + Lablup KV offload benchmark (2026-06-24): 2.09x mean TTFT, warm-reuse
  turns approx 3.3x faster, cold-turn approx 4s offload penalty, TPOT unchanged, 8x H100,
  vLLM 0.20.0 + LMCache, 140k-token agent contexts cycling 10 contexts.
  https://www.vastdata.com/blog/vastdata-lablup-kvcache-offload-benchmark
- Alibaba Qwen QSA (2026-08-26): "up to 7.6x faster in prefill and 4.9x faster in
  decode" at 1M-token context; 90 pct prefix-cache hit rate gives Qwen3.8-Flash-Next
  8.6x Qwen3.7-Plus prefill throughput.
  https://x.com/Alibaba_Qwen/status/2092591404698792378
- shmidtqq cache-engineering article (2026-08-24): Kimi K3 10x hit/miss pricing, 90+ pct
  hit on coding workloads, 512-token hash blocks; the bill-divided-by-10 skill class.
  https://x.com/shmidtqq/status/2091944893862072364
- llm-d cache-aware scheduling blog (2025-09-24): 57x P90 TTFT vs approximate
  scheduling, 25 pct throughput gain, 339 KB index over a 365 GB pool.
  https://llm-d.ai/blog/kvcache-wins-you-can-see
- avichawla four-caches article (2026-08-28) and hwchase17 KV-hit-rate post (2026-06):
  same class as held items; skipped.

## Gaps and OWED (stated, not filled)

- No post-10-01 (Oct 1-2) X-indexed result surfaced for any question; the window's
  freshest primaries are 2026-09-24. Q1's "post-10-01" frame is answered honestly as
  EMPTY for now, with the Sep 24 Nebius/WEKA result as nearest.
- vLLM AgentX PR bodies (#44577 et al.) not individually verified - the PR list came
  from the article text; a github.com pass is OWED before citing any single PR as a
  shipped invalidation fix.
- CompleteSkeptic's child article and the Qwen3.8-27B 240k article are unresolved
  through the fxtwitter door (404 and authorless i/article respectively); the reddit
  primaries behind item 6 (1wg9tig, 1wsmtd4) remain auth-walled - the PullPush /
  arctic-shift / redlib fallbacks stay OWED to the doors lane.
- rogerw0108's "KV cache sharing for agentic workloads / Kimi K3 deployment" post could
  not be resolved past the profile snippet; lead only.
- The Q3 verdict stands: no SpikingBrain-class TTFT table on gate-admitted (SM90/SM100)
  hardware published in-window; the banked 7.3x/26.5x H100 table remains the frontier
  reference, with SpikingBrain2.0 (April, A100s) already held as the successor paper.
