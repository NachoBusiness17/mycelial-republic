# SWEEP kv-cache-context (via x.com) - 2026-10-10

source-fetched: 2026-10-10. Area kv-cache-context, door x. Four research questions from the
10-10 ask: (Q1) what the owed kv-cache provenance re-audit needs from current cache-reuse
literature and whether lmcache-src already shelves it; (Q2) whether current context-engineering
results address the hermes long-session stall class (stalled compaction marks, overflow_reason,
commit f06008308); (Q3) whether the frozen-prefix efficiency law (cache 6.5 to 98 percent, cost
$161 to $3.60, laws lens law 15, memory/rib/RIB_SELF_MY_EFFICIENCY.md) extends to multi-turn
agent sessions and what breaks it; (Q4) the measured prefix-cache-rate vs answer-quality
relationship so sticky routing can be adopted without a hidden regression (2610.05833
byte-identical-asks necessary-not-sufficient already banked; mag/context_compression.py is a
degree-7 multi-rel hub per the 10-10 graph lens).

## Door log (honesty)

- WebSearch site:x.com partially honored, same degradation the 10-06 lens recorded; three
  separate query attempts mid-session returned MCP 429/1302 rate-limit storms. One 60s timeout.
- syndication.twitter.com timeline door: returned a 2,183-byte JS shell, zero statuses (probed
  once, screen-name LMCache_ai). Dead from this host today.
- fxtwitter door healthy: resolved 2/2 statuses byte-true JSON (api.fxtwitter.com/<user>/status/
  <id>), full text 1,862 and 2,284 chars, view/like counts included.
- Primary-source fallback per recipe: four items banked from their non-X primaries (two beri.net
  articles + vllm.ai blog + hermes-agent docs), one from byte-true arXiv export API XML, one
  (OpenAI Decisions API) from the verified beri.net front-page listing. Disclosed per item.
- Two guessed URLs 404ed before I stopped guessing and pulled exact URLs from search/sitemap
  (vllm.ai/blog/2026-05-06-mooncake-store; beri.net sitemap). No fabricated successes.

## Pass 1 census (bar: 30 candidates)

36 candidates considered across 12 WebSearch queries + arXiv export API probes. In-window
(2026-09-10..2026-10-10): 5 (both beri Oct-1 articles, beri Oct-8 Decisions-API listing,
"LLM API token inflation black-box audit" snippet, the older beri kv-eviction piece surfaced
undated). The window skews old because X search was degraded; the strongest in-window bytes are
the two beri articles and the Oct-8 Decisions API item. Dropped with reasons: Compaction Cliff
2608.22752 (already banked 10-05, watch/inbox/frontier_olm_2026-10-05/sweep/_raw/
passau_compaction.txt - cited below as shelf-hold, not re-banked); DailyDoseOfDS_ reshare of
Pachaar (same content as banked original); intelligentnoise.ai compaction piece (root page is a
different product, no resolvable article URL - unresolvable, dropped); LMCache unpatched-critical
flaw report (search-snippet only, zero verifiable bytes fetched - NOT banked, flag for the
security lane to verify); Tokencake/SwiftCache/Segment-Level KV Sharing/Persistent Q4 KV Cache
(arXiv snippets, arxiv-door material, left for that lane); CacheBlend V1-connector bug GitHub
issue (sibling door); VS Code Cache Explorer / anothercodingblog / Morph / Digital Applied /
Timory / CoreWeave / wheynelau (snippet-grade blogs, weaker than the eight banked).

## Pass 2 deep reads

Read end to end this sitting: fxtwitter JSON for both akshay_pachaar statuses (full text);
vllm.ai/blog/2026-05-06-mooncake-store via WebFetch (numbers extracted); beri.net
prompt-caching article + cloudflare auto-router article via WebFetch; hermes-agent.nousresearch
.com/docs/reference/faq via WebFetch (troubleshooting sections); arXiv 2601.06007v2 abstract via
byte-true export API XML. Front-page-listing grade only: beri.net OpenAI Decisions API article.

## The eight banked items (strongest first)

1. beri.net prompt-caching-savings-cost-per-provider-hit-rate-agent-loop-2026 (2026-10-01).
   The frozen-prefix law priced per breaker: fixed 30-turn loop saves 80 percent ($2.72 to
   $0.53) on Sonnet 5.5; timestamp on the first system-prompt line drops it to 6 percent
   ($2.56); timestamp inside a tool description goes negative, -24 percent ($3.36, cache
   writes cost 1.25x). Silent invalidators: dates, session ids, plan tiers, unsorted tool
   lists, unstable JSON key order, retrieved docs above instructions, mid-conversation
   thinking-setting switches; plus minimum prefix sizes, Claude 5-minute TTL, OpenAI routing
   overflow above ~15 requests/min per prefix. Tripwire: under 70 percent hit rate on an agent
   loop signals a volatile prefix. Quality NOT discussed - input discount only.
2. arXiv 2601.06007v2 "Don't Break the Cache: An Evaluation of Prompt Caching for Long-Horizon
   Agentic Tasks" (v1 2026-01-09, v2 2026-01-31). The multi-turn extension evidence Q3 asked
   for: 500+ agent sessions on DeepResearch Bench, 10,000-token system prompts, OpenAI/
   Anthropic/Google, three strategies (full context, system-only, exclude dynamic tool
   results). Savings 41-80 percent, TTFT 13-31 percent better; strategic block control =
   dynamic content at the END of the system prompt, avoiding dynamic traditional function
   calling. This is the Beri article's cited PwC study (77.8/79.3/38.3 percent per-model).
3. beri.net cloudflare-ai-gateway-auto-router (2026-10-01). Q4's only measured sticky-vs-
   success set found: Opus 5.5 96.6 percent success at $0.0210/success vs cloudflare/auto
   86.6 percent at $0.0084 (router ~3.9x Opus failure rate, 97 tasks x 3 samples); switching
   rarely pays off, model move re-writes 100K-token context at 12.5 to 25x the read price
   (reads 0.1x base, writes 1.25x, Opus reads 0.05x); check "cache-read share before and
   after routing. If it falls, the switching penalty isn't protecting you." Launched 2026-09-30.
4. x.com/akshay_pachaar/status/2079205538613854555 (2026-07-20, fxtwitter full read). The
   three breakers of pure prefix caching, named: RAG multi-document (B cached without
   awareness of A), document-order permutation (every permutation a miss), growing
   conversation history. Alibaba production data: 10 percent of KV blocks serve 77 percent of
   hits. CacheBlend (LMCache team, EuroSys 2025 best paper) selectively recomputes boundary
   tokens: 2 to 4x faster multi-document queries "with no quality loss" - the only explicit
   quality claim in the sweep, and it is the vendor's own. Realistic ceiling cited: 60-85
   percent hit rates when prefix is stable.
5. vllm.ai/blog/2026-05-06-mooncake-store (2026-05-06). Multi-turn trace anatomy: agent
   alternates reasoning/action tool-call steps; by turn 30 context ~80K, longest beyond 180K;
   each turn adds a few hundred to few thousand tokens; input:output 131:1; inter-turn delay
   5.2s median to 81.4s P99; ~3.8 GB FP8 KV per 100K context. Cache hit 1.7 to 92.2 percent,
   3.8x throughput, 46x lower TTFT; round-robin routing stressed cross-node fetches on
   purpose; cache-aware routing named as future work. Zero quality/accuracy claims - Q4's
   silence is systemic in the serving literature.
6. hermes-agent.nousresearch.com/docs/reference/faq (live, fetched 2026-10-10). Upstream Q2
   machinery: bounded compaction passes, and when they cannot fit, the turn ends with
   "Context length exceeded: compression could not reduce the rebuilt request below the safe
   threshold" rather than silent llama.cpp truncation; the unmeasured-server stall class
   ("typically a background memory review from an earlier session (thread=bg-review in
   logs/agent.log)" holding the single slot); model switching resets the prompt cache because
   "the cache key includes the model"; HERMES_STREAM_READ_TIMEOUT=1800 for large-context
   local streams. This is the upstream the estate's relay-hardening day (f06008308) ported
   overflow_reason from.
7. x.com/akshay_pachaar/status/2075222711887106519 (2026-07-09, fxtwitter full read). LMCache
   architecture argument: KV cache management as a daemon OUTSIDE the inference engine (no
   fate-sharing); a single GPU throws away ~15 TB/day of reusable cache; H200 + 235B model:
   14x TTFT, 4x decode; plugs into vLLM, SGLang, TensorRT-LLM. Corroborates our own shelf
   read (item overlap below).
8. beri.net/article/openai-decisions-api-public-beta-gpt-6-luna-pricing-cache-discount-vs-jev-
   clef-zdr-residency (2026-10-08, front-page listing grade). GPT-6 Luna on the Decisions API
   bills only input at $0.10/1M and drops the cached-input discount, so long shared rubrics
   cost roughly 4x the Responses API. Pricing-side Q4: an API surface where cache reuse is
   structurally impossible is an anti-sticky trap for rubric-heavy agent loops.

## Q1 answer (re-audit needs + shelf)

The re-audit (burns lens s4, carried since the 10-08 lens naming five unre-audited kv lane
items) does NOT need new cache-reuse literature for the concepts: the shelf already holds the
prior art. Verified this sitting by my own reads: corpus/library/lmcache-src/README.md:75
(non-prefix KV reuse "leverages CacheBlend to selectively recompute tokens for quality
recovery"), :69 (tiered offload "across requests, sessions, and engine instances"),
:143-144 (CacheBlend EuroSys citation), plus Mooncake listed among storage backends
(docs/source/developer_guide/extending_lmcache/storage_plugins.rst, and a
mooncake-store-preview.png asset already in docs). memory/research_polished/
kv_cache_compaction.md:9 holds the law lineage (SGLang/RadixAttention 2312.07104, CacheGen
2310.07240, CacheBlend 2405.16444) and memory/research_packs/bibverify/part1_summary.md:27-28
verified those ids. What the re-audit needs from CURRENT literature is only the measured
breaker taxonomy and quality frontier (items 1, 2, 3, 4 above): which byte patterns void the
prefix (timestamps, tool defs, order), the 60-85 percent realistic ceiling for stable prefixes,
and the one quality-annotated reuse result (CacheBlend's boundary-token recompute). None of
those specifics were on the shelf (all overlap greps 0, below).

## Q2 answer (long-session stall class)

Current results half-address it. The serving side (items 1, 2, 5) measures exactly the
agent-loop shape that produces the stall (131:1 input:output, turn-30 80K) and prices the
breakers, and the upstream hermes FAQ (item 6) now documents the bounded-compaction +
overflow-message contract plus the bg-review slot stall - the same class f06008308 ported.
The compaction-fidelity side is shelf-held: Compaction Cliff 2608.22752 (10-05 passau_compaction
.txt) shows 53 percent of safety rules survive one compaction round, 10 percent after five,
with Knowledge Triage (TypeCompact/TypeDecompose/TypeRetrieve) as the fix. Gap: nobody
publishes on the INTERACTION (cache-aware routing x compaction timing x slot-holding
background reviews); the estate's driver-log port (overflow_reason) is ahead of public art.

## Q3 answer (does the frozen-prefix law extend)

Yes, conditionally, and the conditions are now measured. Multi-turn agent sessions keep the
law alive as long as the frozen block is byte-stable and the volatile tail is appended at the
end (2601.06007: dynamic content at end of system prompt; Beri: append-only tails). What
breaks it, in cost order: a timestamp anywhere early (80 to 6 percent); dynamic tool
definitions (-24 percent, worse than no caching); tool-result blocks inside the cached region
(2601.06007's third strategy exists precisely to exclude them); document reordering and
multi-doc RAG (item 4's three breakers); model switching mid-session (hermes FAQ: cache key
includes the model); TTL expiry (Claude 5-minute window) and per-prefix rate overflow
(OpenAI ~15 rpm). The Mooncake numbers (item 5) are the multi-turn ceiling proof: 92.2
percent hit rate is reachable when the engine, not the app, owns reuse across turns.

## Q4 answer (cache rate vs quality)

The uncomfortable answer: the measured relationship is almost unpopulated. In this sweep,
serving-side papers report zero quality metrics (vLLM/Mooncake explicitly none), the pricing
literature treats caching as cost-only (Beri: "No quality/accuracy trade-off is discussed"),
and the only quality-adjacent bytes are (a) CacheBlend's vendor-claimed "no quality loss" for
non-prefix reuse, (b) Cloudflare's router numbers, which measure SUCCESS RATE against a
sticky-cache-preserving policy and show the cheap-routing failure rate is 3.9x Opus's - i.e.
the regression risk lives in routing decisions, not in cache reuse itself, (c) the banked
2610.05833 (request-order answer variation under selective reuse) and Compaction Cliff
(compaction, not caching, destroys rules). Adopt sticky routing WITH the router's own check:
cache-read share before/after + a success-rate holdout, because no public number yet says
higher hit rate is quality-neutral beyond the byte-identical-ask case.

## Overlap (grep commands and results, all run this sitting)

grep -c -F over catalog/catalog.jsonl: 'prompt-caching-savings-cost-per-provider' 0; 'One
Timestamp' 0; 'cloudflare-ai-gateway-auto-router' 0; '2079205538613854555' 0;
'2075222711887106519' 0; '2601.06007' 0; 'beri.net' 0; 'Rajesh Beri' 0; 'Knowledge Triage' 0;
'bg-review' 0; 'HERMES_STREAM_READ_TIMEOUT' 0; 'cf-aig-session-id' 0; '80K tokens' 0;
'131:1' 0; '15 TB' 0. Hits found and dispositioned: 'akshay_pachaar' 4 rows = two OTHER
statuses already banked by the 10-05/10-08 sweeps (2104938749679607902 Sep-29 article link,
2097421509220561028 Sep-8 NVIDIA KV-transfer post; both JSONs read this sitting to confirm
different content) plus a 2026-09-04 Martian intake card; my two July statuses are new bytes.
'mooncake-store' 1 row = lmcache-src docs PNG asset (shelf, declared). '2608.22752' 1 row =
the 10-05 passau_compaction.txt (already banked; excluded from the eight, cited as shelf).
Memory grep (bounded to research_packs, research_polished, rib, lenses, burns, improve):
CacheBlend/Mooncake held as bibliography-level prior art (kv_cache_compaction.md:9,
bibverify part1_summary.md:27-28) - concepts shelf-held, the posts' specifics not; the
Alibaba 10/77 stat, the breaker taxonomy, and every beri number: 0 hits.

## OWED

- X-native in-window coverage is thin (2 of 8 banked are X posts, both July): the syndication
  door dying today is the cause. The X-surface wire OWED (burns lens s4) blocks the better
  harvest; this sweep is the second consecutive lane to hit it.
- LMCache unpatched-critical-flaw report (search snippet, 0.3.9 through 0.5.5, no patch):
  never verified, never banked. The security lane should fetch The Hacker News item before
  anyone upgrades our shelf checkout.
- Decisions API item is front-page-listing grade; body unfetched (fetch budget spent on the
  two stronger beri articles).
