# FRONTIER SWEEP - kv-cache-context-engineering via Hacker News (pass 2 of this seat, 2026-10-11)

source-fetched: adhoc · 2026-10-11 · seat sweep-kv-cache-context-engineering-hn

Door: HN Algolia API (`search_by_date`, `tags=story`) for "KV cache" (30 hits), "context
engineering" (30), "prompt caching" (30), "cache eviction" (20), "context window" (20), plus
item threads on news.ycombinator.com for strong hits with comment meat. No 403s anywhere. One
degradation: research.yandex.com/blog/the-kv-cache-as-an-agent-runtime returned HTTP 504 twice
(retried once); that item is OWED, not banked (bank only what I read).

## Relationship to the earlier pass of this seat (same day, same path)

A prior run of this ask already banked 8 items here (doug.sh prefix-cache warmth, dacorvo/funes
recall-vs-compaction, future-os compaction measurement, WorkOS MCP token costs, Stagehand
Playwright tokens, the zartbot DeepSeek-v4.1-Flash HN thread delta, Magnitude YC S25 engine,
Skillzero). Overwriting this path per the ask; those 8 remain the prior pass's record and are
treated as holdings for overlap purposes below. This pass mines the delta AFTER them: nothing
below repeats them, the estate-held DeepSeek-V4.1-Flash desk assess (catalog c83aa3495b5f), or
the estate-held agentic-kv-cache acquisition (LRU-leaf wins, memory/percolator/candidates.jsonl).

## Pass 1 - broad sweep census

Strictly in the 30-day window (created 2026-09-11..2026-10-11): 31 story candidates counted
from the five query lanes (KV cache lane 13: embed/KV, self-pruning, memory wall, token CLI,
internet-for-KV, CREAM joke post, KV bank, Ask HN swarm caching, vLLM warm, DeepSeek flash,
j9s agentic, cache-hit-not-proof, MoE viz; context-engineering lane 5; prompt-caching lane 4:
emschwartz, Revefi, GPT-6 caching x2; eviction lane 2: 2609.28870 + routing Show HN; context
window lane 7: Replay auditor, Slowave, Skillzero, elephant tweet, Ask HN, pastebudget, twigg).
Plus 6 near-window (2026-09-01..09-10) considered and mostly set aside: LRU/agentic-kv-cache
(held), DeepSeek PDF trio (held), zero-copy migrator, Yandex runtime (504), claude.dev repost.
Total considered: 37. Requirement (>=30 in-window) met.

## Pass 2 - deep reads (8 banked, all read end to end this session)

### 1. When Fancy Eviction Fails: Rethinking Cache Replacement For LLM Prefix Reuse (arXiv 2609.28870)
Liu, Yu (Minlan Yu), Yang (Juncheng Yang); v1 2026-09-24, v2 2026-10-01. HN 49927418 (2026-10-01,
1 pt, no thread meat). Production traces from two companies, 14 eviction algorithms, HBM-constrained
and large-pool settings. Headline: sophisticated policies barely beat LRU because "prefix reuse is
dominated by the regular pacing of active sessions"; but prefix caching is NOT a solved old problem:
heavy-tailed session footprints and attention-length-variable miss costs (miss cost grows with
sequence length) are new. Contributions: compute-savings ratio metric, two offline oracles
(Belady-style upper bounds), and three recommendations: recency base + quick demotion for one-hit
prefixes, compute-aware PARTIAL eviction for costly misses, capacity-dependent eviction granularity.
Traces + simulator to be released.
RQ3 verdict for the estate: round-robin tail eviction (RR-Evict, banked pending burns.md:119) now
has TWO independent field studies against it: this paper (14 arms, fancy loses to LRU under session
pacing) and the estate-held agentic-kv-cache (LRU-leaf 83.48% beat every custom policy). The win
axis is not the eviction POLICY, it is avoiding eviction entirely (freeze the prefix) plus
compute-aware partial eviction when you must evict. That reframes RR-Evict's pending test: run it
against an LRU-leaf arm and a freeze-the-prefix arm, or do not run it (gap-fold G1 law:
beat LRU/ARC/PBKV/Belady arms or it is decoration).

### 2. Improving Throughput by Optimising KV Cache Efficiency for Agentic Workloads (j9s.io, Joel Smith)
HN 49701675 (2026-09-14). vLLM custom fork, Qwen3-32B-FP8, single RTX 6000 Pro, OpenHands on
SWE-bench Lite through a logging/augmenting proxy. Agent traffic characterized: median ~15,146
prefill tokens/turn vs ~501 decode tokens, median inter-request gap 0.18s vs chat's 96.24s.
KV cost 256 KiB/token BF16 -> FP8 KV quant (`--kv-cache-dtype fp8_e4m3`) halves it and moved the
overload elbow from c=12..20 to ~c=40. CPU offload: 120GB RAM kept prefix reuse near 100%
(40GB behaved like FP8-only). The steal: state-aware eviction HINTS, madvise-inspired
(dontneed/pageout/willneed_soon/later), where the proxy parses tool calls and uses per-tool EWMA
gap durations vs load-time EWMA to reorder vLLM's LRU queue; GPU-local hit uplift 1.06x-1.44x,
throughput 1.04x-1.27x, honestly flagged as not statistically controlled (no repeated runs,
FP non-associativity run-to-run). Framing quote: "agency lives within the harness"; harness state
is normally "discarded at the API boundary" and is the underused eviction signal.
ESTATE FIT: the fleet already logs tool-call gaps (logs/provider_usage.jsonl timestamps); an
EWMA-gap hint layer over vLLM/Ollama eviction is implementable from existing telemetry. Direct
RQ3+RQ2 instrumentation pattern.

### 3. The KV Cache Is the New Memory Wall (jaehun.me review of arXiv 2609.30854, Dell SoK)
HN 49945575 (2026-10-03). Review by Jaehun Ryu of Singh's SoK "three regimes and five domains".
Core: long-context decode is memory-bandwidth-bound; per-step KV traffic overtakes weight traffic
past a batch-dependent crossover s*(b) (Llama-3-70B: 427.2k tokens at batch 1, 13.4k at batch 32;
0.33 MB/token BF16, 128k ctx = 42GB, 1M ctx = 328GB). REGIME RESULT (the RQ4 steal): identical
2-bit KV quantization yields 1.25x speedup at batch 1 (weight-bound) but 4.82x at batch 32
(KV-bound): same config, ~3.9x different outcome by regime. Placement: B200 loses 2x, MI300X up
to 8x effective bandwidth with pinned vs striped pages (2.0M vs 16.2M tok/s ceiling). Tiering:
fetch beats recompute (0.16s vs 25.0s for a 128k cache) but serves reuse between steps, not reads
within one. Five domains (quantization, eviction, paging, prefix caching, tiering) on one footprint
model; ~46x capacity / 6.6x traffic combined ceiling. Verdict line: "Almost every published number
is right on its own. But almost none of them can be interpreted together."
RQ4 verdict: the estate's refusal-regime finding (98.0 -> 80.5 keyword-refusal drop) has a systems
twin: quant+compression gains are regime-dependent by factors, so any janitor-fleet quant+compaction
config claim must state its batch/regime cell or it does not transfer. Extends the McNemar-style
regime discipline from refusal behavior to throughput claims.
OVERLAP: paper abstract already held (state/arxiv/2026-09-28/2609.30854v1.txt, catalog e4f43ee5d8b9);
the review post with the regime numbers and crossover law is the delta banked here.

### 4. Show HN: Token compression CLI to save Codex/Astra costs (HN 49911910 thread)
2026-09-30, 14 pts, 5 comments, read in full. yolandac+Spencer: after subscription overage at
"$700/day per person on api", they fine-tuned a Qwen-based compression model into a proxy that
removes tool-call results before they reach the model WHILE KEEPING THE KV CACHE INTACT, trained
to preserve agent trajectory; 29.6% token cut, "up to 30% cost reduction", measured via
response.usage at the proxy. CLI free at github.com/spenmcke/compress (repo named in story text,
not independently fetched), ZDR, compression on by default.
The THREAD is the eval bar: SerhiiDrozdov asks whether task success was compared before/after
(nope) and enumerates anchor classes that must survive compression verbatim: HTTP status/body,
failing test name, stack trace, exit code, file path, validation error, database error.
ESTATE FIT RQ2 (reach ratio): this is a working reach-ratio intervention (bytes that reach the
model cut ~30% with the prefix kept cache-warm), and the thread critique is exactly the estate's
compaction eval bar (matched budgets, downstream task truth) applied by outsiders. Anchor-class
list goes straight into any tool-output compression policy.

### 5. A cache hit is not proof that you skipped the work (siddhantkhare.com/writing/kv-cache-truth-auditor)
HN 49699918 (2026-09-14). Narrow but exactly RQ1-shaped: a fail-closed audit chain (LLMTraceFX)
for cache-hit claims. Ten deterministic nine-token synthetic cases typed by MISS REASON (cold,
same-length-different-IDs, namespace isolation, capacity-evicted) and PARTIAL reuse (interior
mutation reuses 3/9, boundary 4/9, suffix 8/9). Five independent checks: independent token oracle,
observed prompt work, output-token identity cached-vs-no-cache, deterministic evaluator,
hash-bound verifier; offline reproducible. Honest scope: "A cache hit can be true and still fail
to prove that work was skipped"; "Timing and runtime memory remain null in this control. They are
not zero." Synthetic only, no billing/prefill/GPU claims.
ESTATE FIT RQ1: the provenance re-audit OWED (burns.md:234) can steal the shape: hit/miss claims
in provider_usage.jsonl should carry a typed-miss-reason column and an opportunity denominator
(the estate already names the denominator gap, kv_cache_compaction.md finding 3 caveat). The
interior-mutation 3/9 partial-reuse number is also a clean unit-test fixture for the reach-ratio
probe: a mid-prefix byte change does not cost the whole prefix at every provider, measure it.
OVERLAP: the URL appears as a source citation inside one unpromoted percolator candidate
(memory/percolator/candidates.jsonl, ts 2026-10-02, status candidate); the post's content was
never banked before this read.

### 6. Please add prompt caching to Jev-style models (emschwartz.me, Evan Schwartz)
HN 49898130 (2026-09-29). Consumer-side proof of the estate's finding 1 doctrine: Scour classifies
~1.1M docs/month with Jev as a fuzzy-question classifier; his v28 question set (54 questions,
~2,150 tokens incl ~260 fixed overhead) is sent verbatim with every request and is ~88% of input
tokens. He avoids batching inputs together because of a documented warning: "Accuracy falls as
the state grows with content unrelated to the decision." Under $150/month today; asks providers
for prefix caching or registered question sets (typesafe-ai/typesafe-sdk-js#10), or a
many-questions-x-many-inputs API without state packing.
ESTATE FIT: independent field confirmation that the byte-identical frozen prefix is the unit of
economics on a NON-DeepSeek stack (Jev/System One), plus the state-packing accuracy warning is
the compaction-side regime caveat: batching for cache warmth can cost decision quality, the same
trade the dacorvo recall-vs-compaction A/B measured.

### 7. A Self-Pruning Transformer: Extreme KV-Cache Compression with Universal Attention (arXiv 2610.09051)
Wertheimer et al. (UIUC collab), submitted 2026-10-06. HN 50013834 (2026-10-08). Framework of
complementary decay mechanisms that PRESERVE RoPE and softmax attention (prior decay work reduced
to sliding-window-like eviction with "limited expressivity"); composite decay is the trainable
pruning criterion. Claims SOTA 10x KV compression that IMPROVES downstream performance vs SOTA
baselines and unpruned oracles, and "unprecedented $25\times$ compression at length 16k";
27 pages, 14 tables (benchmarks not named in the abstract).
ESTATE FIT: feeds the substrate thread (quant/eviction hardware tier). Caveat for the fold:
architecture-level (retraining required), so it cannot ride the janitor fleet; it is a
watch-item for the bare-metal steal, not a config. The improves-over-oracle claim deserves the
regime question from item 3 before trusting it.

### 8. An Internet for the KV Cache: Rethinking Classical Infrastructure Boundaries (arXiv 2608.01526)
Ray, Feamster, Jiang; submitted 2026-08-02 (out of paper window; surfaced by HN 49883064 on
2026-09-28, in sweep window). Position/vision paper, NO numbers: treat KV caches as
content-distribution objects; decouple compute from KV storage across clouds/datacenters; the
network becomes an active channel where "bandwidth, latency and pricing directly determines how
the KV Cache should be managed"; store-vs-recompute decisions driven by model+infra+app metrics.
ESTATE FIT: thin today (vision), but it is the networking establishment (Feamster, Jiang)
endorsing exactly the estate's CacheGen/CacheBlend cross-tier transport line as an
infrastructure-scale direction. Watch for the follow-up systems paper; do not act on it.

## Explicitly considered and NOT banked, with reasons
- Using KV cache as embeddings (breadbowl.ai, HN 50035357, 2026-10-10): title mismatch. It is a
  late-interaction embedding model (16 routing/value slots, Qwen3.5-0.8B, BEIR 51.54 vs teacher
  69.80), not an LLM KV cache technique. Real read, wrong area; noted in case the retrieval
  slot-shape idea matters to skills_pack later.
- The new rules of context engineering for Claude 5 generation models (claude.dev repost, HN
  50041438, 2026-10-11): same Jul 24, 2026 Thariq Shihipar post behind the July 463-pt thread;
  no new content on fetch; July original predates window and is a known position.
- Yandex "The KV cache as an agent runtime" (HN 49578969/49598646): HTTP 504 twice, OWED, never read.
- DeepSeek-v4.1-Flash (zartbot + PDFs) and LRU/agentic-kv-cache: estate-held; prior pass banked
  the zartbot thread delta already.
- Ask HN threads with 0-1 comments (49783040 provider KV caching for swarms; 49691257 Replay
  silent cache-miss auditor): no thread meat; Replay is interesting on title alone and unverified.

## RQ-by-RQ ledger (this pass's delta only; prior pass's ledger stands in git history)
- RQ1 provenance re-audit: item 5 supplies the audit-chain pattern (typed miss reasons, partial
  reuse counts, output identity, opportunity denominator) and item 1 supplies the compute-savings
  ratio + oracle framing for eviction claims. The reach-ratio probe itself (bytes reaching the
  model vs bytes sent) is still UNFIRED this pass: no public artifact found that measures it on a
  live seat; items 4 and 2 give the two intervention points (proxy-side stripping, hint-side
  retention) to instrument when it fires.
- RQ2 reach ratio: item 4 (29.6% cut keeping KV intact; anchor classes to preserve verbatim).
- RQ3 RR-Evict vs freeze-the-prefix: items 1 and 2 together say the eviction-policy axis is
  nearly exhausted (LRU-leaf + session pacing dominates; fancy loses), and the live axis is
  compute-aware partial eviction + harness-signal hints; freeze-the-prefix avoids the game.
- RQ4 regime dependence beyond keyword refusal: item 3 (identical 2-bit quant, 1.25x vs 4.82x by
  batch regime) + item 6 (state-packing accuracy warning) give two independent regime-dependence
  mechanisms for the janitor fleet's quant+compaction configs: state the regime cell or the
  number does not transfer.

## Degradations, honestly
No 403s. One 504 (Yandex, twice, retried once, OWED). No fabricated fallbacks.
