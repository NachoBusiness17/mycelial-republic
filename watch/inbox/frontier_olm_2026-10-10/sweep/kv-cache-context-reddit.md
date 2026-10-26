# Sweep: kv-cache-context via reddit (frontier_olm 2026-10-10)

source-fetched: 2026-10-10. Seat: sweep-kv-cache-context-reddit. House laws held: ascii
only, no em or en dashes, every claim cites what was read or run this sitting.

## 0. Door report (why this is a search-door sweep, not a fetch-door sweep)

The recipe door and every fallback fetch door were tested live this sitting and ALL failed:

1. WebFetch https://old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50 -> Reddit
   landing page, no JSON payload.
2. WebFetch https://old.reddit.com/r/LocalLLaMA/top/?t=month (HTML) -> same landing page.
3. WebFetch an old.reddit.com thread URL (comments/1t47qbw) -> same landing page.
4. WebFetch https://www.reddit.com/r/LocalLLaMA/top.json -> HTTP 403 Blocked.
5. MCP webReader on old.reddit.com -> verbatim: "Log in to use old Reddit. To keep Reddit
   safe, accounts are required to access old Reddit."
6. MCP webReader on a www.reddit.com thread -> verbatim: "Reddit - Prove your humanity"
   CAPTCHA challenge.
7. curl api.pullpush.io (the door the estate's own corpus/social_archive/reddit_20261001
   used on 10-01) with a named UA -> verbatim: "Rate limit exceeded. This website does
   not provide free scraping resources for agents."

Per the recipe the degraded fallback (WebSearch site:reddit.com, whose backend CAN read
Reddit) was used for all Reddit-content mining. This matches the doors-laws row already
banked this run: "Reddit is CLOSED for this pass until a header or oauth recipe exists"
(watch/inbox/frontier_olm_2026-10-10/lens/questions.md:223-224). Reddit thread content in
this sweep is therefore snippet-tier except where the estate already holds fetched JSON.
One estate-held thread JSON exists and was read locally this sitting:
watch/inbox/frontier_olm_2026-10-07/sweep/tmp/sub_1r5q7xd.json (fetched by the 10-07
sweep; created_utc 1771189969 = 2026-02-16, so the thread itself predates the window).

## 1. Pass 1: candidates considered (41 named, last-30-days preferred)

From WebSearch sweeps + HN Algolia + gh + direct fetches this sitting: (1) CVE-2026-105192
LMCache RCE, JFrog disclosure Oct 7; (2) vLLM CVE-2026-105756 cache_salt DoS; (3) six
unconfirmed LMCache GitHub security reports; (4) Launch HN Magnitude 49911995 Sep 30;
(5) Self-Compacting Language Model Agents arXiv 2606.23525; (6) vLLM RFC #44223 Semantic
KV Cache Reuse Interface; (7) Synap/Maximem why-we-built blog; (8) blog.lmcache.ai post
line (Oct 1 intro, Sep 22 Raw Block NVMe, Sep 7 KV-cache editing SDK, Aug 19 at-rest
encryption); (9) fresh r/LocalLLaMA post (~Oct 8) on the trade-off between dynamic
action spaces and prefix caching (snippet-tier only, no URL obtainable, OWED); (10)
r/LocalLLaMA 1r5q7xd persistent-memory thread (estate-held); (11) arXiv 2609.28870 When
Fancy Eviction Fails; (12) arXiv 2608.01326 Context Compaction Theory; (13) When
Prediction Doesn't Pay: Recency Is Near-Optimal for LLM Prefix Caches (Aug 27);
(14) Multi-Segment Attention (arXiv Jun 2026); (15) arXiv 2606.21238 Recency/Frequency
Adaptive KV Caching; (16) UniCache (ACM); (17) KVFlow (NeurIPS 2025); (18) DynaAct
(NeurIPS); (19) Efficient Serving for Dynamic Agent Workflows (H Zheng 2026);
(20) Anyscale token-load-aware routing (Aug 2026); (21) GMI Cloud cache-aware model
routing (page renders empty, dropped); (22) SGLang v0.4 cache-aware router; (23) Ray
Serve prefix-aware routing with imbalanced-load fallback; (24) verl RFC KV-cache-aware
LB (May 2026); (25) llm-d KV-Cache Wins You Can See; (26) Red Hat llm-d KV-cache-aware
routing; (27) TokenLake segment-level shared prefix pool; (28) TrueFoundry KV cache
routing (Jun 2026); (29) DigitalOcean The Inference Tax (Jun 2026); (30) NVIDIA Dynamo
Deploy LMCache MP docs (Sep 28, fetch 404'd); (31) vLLM docs LMCache examples (Sep 18);
(32) LMCache x Mooncake joint effort (May 26); (33) LMCache AMD MI300X multi-turn
agentic benchmark (May 12); (34) Context Compression for Long-Horizon AI Agents
(J Yan, preprints); (35) LCM Lossless Context Management (alphaxiv); (36) Copium
context-optimization layer (r/LocalLLaMA-credited GitHub); (37) arXiv 2606.19380
coding-agent framework with daemon compaction; (38) Mem0 memory-vs-context; (39) PreMAI
75-90 pct multi-turn cache hit claim (Feb 2026); (40) DeepInfra vLLM vs SGLang (Aug 4,
2026, cites RunPod 35.0 vs 32.8 tok/s); (41) RunPod engine comparison (Jun 23, 2026).

Anti-rebank exclusions (checked by grep this sitting, do NOT re-bank):
- arXiv 2609.28870 (When Fancy Eviction Fails): already held at abstract level by the
  mickey17 lane, memory/runs/mickey17_v2/runs/agent-engineering-frontier-sweep-40/lanes/
  kv-agents-week.json (grep hit: "2609.28870, submitted 2026-09-24) evaluates 14
  eviction algorithms on production traces"). I fetched and read the arXiv abs page to
  confirm, then excluded it from banking.
- arXiv 2608.01326 (Context Compaction Theory): already verified in the gapwave run,
  memory/runs/gapwave/gap_external_field.md (grep hit: "2608.01326 - VERIFIED
  (fetched). Formalizes compaction as two games"). Excluded after my own confirming read.
- KVFlow (NeurIPS 2025): held in memory/MEMORY.md and
  memory/research_polished/kv_cache_compaction.md (grep hits this sitting). Excluded.
- r/LocalLLaMA 1r5q7xd: estate-held JSON (see section 0). Not re-banked.

## 2. Pass 2: deep reads (6 end to end, all quotes verbatim from pages I fetched)

1. The Hacker News coverage of the JFrog LMCache disclosure (full article fetched).
2. HN item 49911995 Magnitude story + comments via hn.algolia.com API (curl; 30
   cache/agent-matching comments extracted and read).
3. arXiv 2606.23525 abs page (fetched in full).
4. vLLM RFC #44223 body via gh api repos/vllm-project/vllm/issues/44223 (fetched).
5. maximem.ai why-we-built-synap blog (fetched in full).
6. blog.lmcache.ai index (listing-tier read: titles + dates; post bodies NOT fetched,
   marked as such).
Plus two confirming reads that were then excluded on overlap (2609.28870, 2608.01326).

## 3. Findings against the four questions

### Q1: what the owed kv-cache provenance re-audit needs; does lmcache-src hold it

Needs a RISK row, not more reuse mechanics. The shelf holds the prior art: CacheBlend
multi-doc QA bench (corpus/library/lmcache-src/benchmarks/multi_doc_qa/README.md,
catalog id 75d97d0dcd94), CacheGen encoder/decoder/kernels
(catalog ids 7c5aef3caaf5, 312360a6f195, d18dc67a1f02), fleet-wide CacheBlend lookup
(corpus/library/lmcache-src/docs/design/v1/mp_coordinator/blend_lookup.md), in-process
blend (catalog id 8437c6e2fc07). What the shelf ALSO holds, verified by rg this sitting,
is the CVE-2026-105192 attack surface itself: the ZMQ ROUTER transport
(corpus/library/lmcache-src/lmcache/v1/rpc/zmq_transport.py:157-209, "ZMQ ROUTER socket
transport for synchronous RPC servers", bind at :174-175), the pickle transfer context
(corpus/library/lmcache-src/lmcache/v1/multiprocess/transfer_context/pickle.py), and the
SHM-to-pickle fallback (corpus/library/lmcache-src/lmcache/v1/multiprocess/server.py:354
"Disabling SHM, falling back to pickle."). Per the fetched Hacker News article the flaw
is unpatched (no fixed version), 9.8/10, affects 0.3.9 through 0.5.5 plus RCs and dev,
runs as root in official container images, and "LMCache's own example Kubernetes
deployment starts the server that way" (routable). The re-audit closes by stamping the
shelf snapshot's provenance (all shelf mtimes 2026-09-22T02:59:48Z per catalog rows,
same date as the engine's Raw Block NVMe post) and recording: shelf = affected-surface
present + unpatched upstream + RCE requires routable bind. The estate never binds
anything routable in local use, but the audit row must exist before any fleet reuse.

### Q2: does current work address the hermes long-session stall class

Partially, and the best port candidate is SelfCompact (arXiv 2606.23525, fetched this
sitting). Fixed-threshold compaction "can discard partial results mid-derivation" and
"unprompted models cannot reliably tell when their own context is rotting"; their fix is
a lightweight rubric for when to fire (sub-task resolved, trajectory converging) or
suppress (mid-derivation, stuck), measured at up to +18.1 points math, +5-9 agentic
search, at 30-70 pct lower per-question cost. That suppress-condition ("mid-derivation,
or when stuck") is the direct analog of the stalled-compaction-marks class in f06008308,
and the fire/suppress rubric is the port candidate for the overflow_reason driver-log
port. The theory floor is already estate-held (2608.01326 via gapwave): budget below the
one-way communication complexity floor means the query set cannot be answered within
target error, which is the honest bound to quote when a compaction stall is real rather
than a bug. No public work names overflow_reason itself; that port stays estate work.

### Q3: does frozen-prefix extend past single dispatches, and what breaks it

Extends when the prefix stays byte-stable: multi-turn chat reuse is the design center
(SGLang RadixAttention; PreMAI's 75-90 pct multi-turn hit claim, vendor-tier), and
Magnitude (HN 49911995, comments fetched) is building hybrid local/cloud switching
verbatim "even for the same tasks (without breaking your prefix cache)", plus "since we
use less memory for KV, you have more room for model weights when you're running longer
sessions" and a negative result worth stealing: quantizing "the KV cache to 8-bit keys
and 4-bit values... bombed decode speed for llama.cpp". What breaks it, verbatim from
vLLM RFC #44223 (fetched via gh): the reusable content is present "but the request
starts with a different instruction, chat wrapper, retrieval order, or paraphrased
lead-in. Exact prefix caching correctly misses in those cases." Tool results and
evolving state blocks live exactly in that class. Secondarily: routing (round-robin
destroys locality, TrueFoundry Jun 2026, snippet-tier), and eviction is NOT the breaker
(estate-held 2609.28870: LRU near-optimal under agentic session pacing).

### Q4: prefix-cache rate vs answer quality

No public paper I could actually read measures cache-hit rate against answer quality in
the last 30 days; that relationship is still UNMEASURED in readable public literature.
Nearest measured neighbors, both fetched this sitting: Synap's post (secondhand, from an
r/LocalLLaMA developer's tracking) "instruction adherence dropping from 94% to 41% as
context filled up" over 847 agent runs, and "the degradation is not linear, there is a
cliff, and developers feel it before they can instrument it" (that is context-FILL
decay, not cache-rate decay, but it is the cliff a cache savings would hide); and their
own LongMemEval 90.2 pct vs 71.3 pct next-closest. GMI Cloud claims cache-aware routing
"while preserving output quality" but the article body renders empty (fetched, no
content; dropped, do not cite as evidence). Practical law for the estate: sticky routing
adoption (2610.05833 bank holds the hit side, 5.6 to 96.45 pct) must carry the estate's
own quality gate fired on cached-vs-uncached A/B pairs, because nothing outside
measures it yet.

## 4. OWED from this sweep

- The fresh r/LocalLLaMA "dynamic action spaces vs prefix caching" post (~Oct 8):
  snippet-tier only; thread URL unobtainable through every door tested. Re-chase when a
  Reddit door reopens (header/oauth recipe, or a working mirror).
- When Prediction Doesn't Pay (Recency Near-Optimal, Aug 27): snippet-tier; companion to
  the already-bank 2609.28870, fetch if the eviction row ever needs a second source.
- GMI Cloud cache-aware model routing: page renders empty for fetchers; unreadable, not
  evidence.
- blog.lmcache.ai post bodies (Raw Block NVMe, KV-cache editing SDK): listing-tier read
  only; bodies OWED if the re-audit wants their numbers.
- NVIDIA Dynamo LMCache MP deployment docs: my fetch 404'd; deployment-tier detail OWED.

## 5. Instruments used this sitting (for the counts law)

WebFetch (8 calls, 3 usable), MCP webReader (4 calls, 0 usable), curl (HN Algolia search
+ item 49911995, pullpush 1 blocked), gh api (1 issue), rg/grep over catalog/catalog.jsonl
and memory/ (overlap checks, outputs quoted inline), python json.load on the estate-held
1r5q7xd.json, Read of lens/burns.md and lens/questions.md in full. No pytest, no
networked fetch of any estate-internal claim: all estate facts above cite file paths and
line numbers read this sitting.
