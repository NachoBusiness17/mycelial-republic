# FRONTIER SWEEP: kv-cache-context-engineering via hn - 2026-10-07

source-fetched: 2026-10-07. Gopher seat: sweep-kv-cache-context-engineering-hn (this session).
Estate feeds named by the ask: mag/context_compression.py (degree-7 hub, lens/graph.md:22), the
context-pack layer whose propagation gap is live (lens/burns.md:151-153, commit 04ee7066d DOGFOOD2),
the corpus FTS retrieval organ (1,195,926 rows, lens/corpus.md:8), and the byte-identical-ask
cache-hit law (corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md).

## Method (two passes, as ordered)

- Pass 1 broad: 17 hn.algolia.com `search_by_date` queries filtered to created_at_i > 2026-09-07
  (phrases incl "KV cache", "prompt caching", "context compaction", "attention sink" (0 hits),
  "long context", "agent memory", "sliding window attention", "prefix caching", "RAG vs" (0),
  "context rot", "needle in a haystack" (0), "memory wall") + 2 relevance `/api/v1/search` queries.
  About 60 distinct candidate stories. The Algolia door never 403'd; three queries simply had zero
  hits and are named above.
- Pass 2 deep: 13 pages/threads read end to end (HN threads 49643543, 49735410, 49807383, 49820496,
  49508317, 49911995 + pages: agentic-kv-cache README, zartbot dsv41flash (via web reader after two
  WebFetch timeouts), doug.sh, future-os-blog, research.yandex.com, HF apple/LensVLM-9B, mempko,
  j9s.io, boolean.ai, calpaterson.com, siddhantkhare.com). Minimum was 5; 13 done.

## Overlap instrument and the self-echo discovery

Mandated check run as: `rg -i -uu -o -e <18 phrases> memory catalog/catalog.jsonl | sort | uniq -c`
(ripgrep 15.2.0; memory/ = 9.3 GB, 583,783 files, measured). A first attempt reading every file in
Python was killed at about 25 minutes as impractical at that scale. Critical finding:
memory/trajectory/steps.jsonl is THIS session's live trajectory log and contains every phrase I typed
or fetched (100x agentic-kv-cache, 31x "LRU is harder to beat", 23x LensVLM, etc.) - all such hits
are self-echo, not holdings, and were excluded from overlap verdicts. Genuine holdings surfaced
elsewhere (see NOT banked).

## Banked (7, strongest first; all zero rows in catalog/catalog.jsonl)

### 1. Context compaction, measured: FutureOS vs. Codex vs. OpenCode
source-fetched: 2026-10-07 - https://future-os-blog.github.io/posts/context-compaction-measured.html (HN 49795948, 2026-09-22)
Quote: "FutureOS retained 147 (83%). OpenCode retained 83 (47%). Codex retained 68 (38%). None fell for a decoy."
The only head-to-head compaction measurement found in the window: grow sessions to window-fill,
force compaction, then 178 recall questions (8 decoys). Retention scope is the whole game: FutureOS
keeps original user/assistant prose and compresses only tool output into a ~2,048-token evidence
index (83% recall at 5.7% of original tokens); Codex keeps no assistant text (38% recall at 0.6%).
Tool output is 96.1% of chars but 90% of follow-up questions target prose. Autonomous retrieval made
ZERO tool calls (145-149 recall, noise); only forced verification reached 93.3% - retrieval does not
close the gap behaviorally. Cost per recall point and break-even turns (61/46/110) tabulated. Page
fetched twice with independent prompts; all numbers reproduced identically. FEED: the context-pack
propagation-gap fix - compaction policy should be judged by forced recall against pre-compaction
session content, which is exactly the instrument the dogfood gap lacks. Overlap: 4-5 phrase hits,
all self-echo in steps.jsonl; zero catalog.

### 2. Keeping vLLM's Prefix Cache Warm Between Agent Turns
source-fetched: 2026-10-07 - https://doug.sh/posts/vllm-kv-cache-agents/ (HN 49758259, 2026-09-18)
Quote: "A lookup walks the prompt from the start and stops at the first block that doesn't match."
Local-runtime invalidation semantics with receipts: vLLM prefix cache walks block hashes (each block
hashes itself plus all prior blocks), so shuffled tool-schema keys (Bifrost/mcp-go JSON key iteration
order) broke prefixes on 8% of turns at 94-96% identical prompts, matching only 12,622 tokens before
divergence. On hybrid linear-attention models (Qwen3.8-27B) states save only at 2048-token
boundaries, neutering the CPU offload tier. Compaction itself is listed as a prefix breaker (history
replaced by summary forces full re-read) - the RQ2/RQ3 bridge. 55% to 95% cached took TTFT from
26-28s to 7.3s; worst wait 514s to 54s. FEED: the estate's byte-identical-ask cache-hit law verified
in the wild; the "shared content first, volatile content last" ordering law is directly portable to
context-pack assembly. Overlap: 26+37 phrase hits, all self-echo; zero catalog.

### 3. Agentic Workflow's Cache Keepalive Costs 8x Too Much (mempko)
source-fetched: 2026-10-07 - https://blog.mempko.com/keeping-the-kv-cache-warm-measuring-prompt-cache-eviction-across-anthropic-openai-and-google/ (HN 49009301; posted 2026-07-22 - outside the 30-day window, surfaced via the recipe's relevance door /api/v1/search; disclosed)
Quote: "The convention is to ping every 30 seconds. That convention costs 8× more than necessary."
The measured cross-provider TTL study RQ2 asked for: Anthropic hard 5-min cliff (0/48 samples warm at
10 min; every read refreshes TTL; 1-hour tier at 2x write cost), OpenAI sticky (39/48 warm at 10 min;
docs say only "5 to 10 minutes"), Gemini sticky-with-lottery (20/24; explicit cache bills per
token-hour), DeepSeek-via-DeepInfra lossy (4/48; router pin is not machine pin). Break-even idle
horizons 46/36/36/12 min; at a 10-min pause keepalive only saves money on Anthropic. FEED: any
harness-side keepalive or cache-warmth policy for the remote specialist lane. Overlap: mempko 1 +
URL slug 1, both self-echo; zero catalog.

### 4. Quantifying Context Rot
source-fetched: 2026-10-07 - https://www.boolean.ai/blog/context-rot-quantified (HN 49734038, 2026-09-16)
Quote: "GPT-5.6 Sol loses about 25% of its solved tasks by 250k tokens of context regardless of whether the context was related to or unrelated to the task."
20-task terminal-bench v4 subset, prefill at 0k/250k/500k, two 1M-context frontier models:
GPT-5.6 Sol loses 25% of solved tasks by 250k (plus momentum-induced collapse, reverting to earlier
Q&A turns mid-task); Claude Opus 5 degrades only on related context (15% at 250k). Compaction
partially recovers (stated preliminary). FEED: the full-context baseline for RQ5 - every
guide/summary abstraction (context-pack included) must be scored against the rot curve, not against
"more tokens = more truth". Overlap: 3+7 hits, all self-echo; zero catalog.

### 5. LensVLM: Compressing long context as images, expanding only relevant pages
source-fetched: 2026-10-07 - https://huggingface.co/apple/LensVLM-9B (HN 49820496, 91 pts, 2026-09-23)
Quote: "LensVLM is a 9B Vision Language Model (VLM) that scans compressed images of text, then selectively expands only the relevant pages to their uncompressed form via learned tools."
Apple, 9B (Qwen3.5-9B base), 5x/10x/15x compression of text-as-image with learned selective
expansion - the Turing-castle tour guide made literal: the guide holds compressed pages and expands
only what matters (lens/burns.md:160-161, the d01 shed finding). Local 7B-class scale. HN thread is
qualitative (rao-v calls the vision encoder "an expensive high fidelity RAG encoder" and suggests
page-level permutation invariance so each page's KV could be a retrievable chunk). OWED: the model
card carries no benchmark scores; paper arXiv:2605.07019 not fetched this pass. Overlap: 27 hits all
self-echo; zero catalog.

### 6. The KV cache as an agent runtime (Yandex Research)
source-fetched: 2026-10-07 - https://research.yandex.com/blog/the-kv-cache-as-an-agent-runtime (HN 49586561, 2026-09-05)
Quote: "This converts the cache from a flat append-only tensor into a reusable, multi-view memory."
RQ1/RQ3 alternative axis - reorganization over truncation: blocks stored once in block-local
coordinates, per-consumer query rotations give each stream a different causal view (RoPE relative
positions). Systems: Hogwild! Inference (shared attention memory, per-worker logical orderings) and
AsyncReasoning (thinker/writer split: up to 80x faster first non-thinking token, 12x lower
user-perceived delay, arXiv 2512.10931); SGLang serving stack; "Streams are processes. Cache blocks
are shared memory. Attention views are access mappings." CONCEPT OVERLAP DISCLOSED: the post URL has
zero catalog rows, but the Hogwild! Inference lesson is already held as corpus library
(corpus/library/ai-engineering-from-scratch/22-async-hogwild-inference/, catalog rows verified);
banked for the Yandex multi-view framing and numbers. Overlap: URL 2 hits self-echo; the 7 catalog
hogwild rows are the library lesson, not this post.

### 7. Improving Throughput by Optimising KV Cache Efficiency for Agentic Workloads
source-fetched: 2026-10-07 - https://j9s.io/posts/agentic_inference/ (HN 49701675, 2026-09-14)
Quote: "the harness's state is discarded at the API boundary, invisible to the layer making retention, eviction, and scheduling decisions."
Agentic-serving shape measurements: median 15,146-token prefill vs 501-token decode; ~3.9 GB KV per
trajectory (Qwen3-32B, 256 KiB/token BF16, 128 KiB/token FP8); FP8 moves the capacity elbow from
c~20 to c~40; madvise-style harness-state hints reorder vLLM eviction for 1.06-1.44x GPU-local
hit-rate and 1.04-1.27x throughput uplift. Author discloses results are not statistically powered.
FEED: the named discarded state is exactly what our context-pack carries across the API boundary -
the estate already holds that state, so the hint mechanism is stealable for the local Ollama lane.
Overlap: zero catalog hits for j9s.io / agentic_inference; self-echo only.

## NOT banked (known work - re-banking is waste)

- DeepSeek-V4.1-Flash (zartbot post, HN 49735410, 131 pts): catalog holds 14 rows including a corpus
  .txt copy of the post itself plus intake lane docs (LANE 1/8 API sweep, LANE 3 scaffold byte-drift,
  LANE 5 vision probe, LANE 6 encoding dig). I did read the full post this session (via web reader
  after two WebFetch timeouts): 890 B/token global main KV plus indexer (CED causal encoder-decoder,
  CSA2 512-dim latent with cross-layer sharing, HSI sparse indexer with 2048-block candidate pool,
  Engram conditional memory with two ~384M-row n-gram tables, FP4/MXFP4 QAT), runtime KV ~1/4 and
  persistent ~1/8 of V4-Flash, 1M context, explicitly motivated by agentic input-dominated loads.
  No new bank needed.
- LRU is harder to beat than the KV-cache papers suggest (agentic-kv-cache, HN 49643543, 108 pts /
  58 comments): already a 2026-09-28 percolator candidate (watch/inbox/frontier_olm_20260928
  frontier_mine row citing HN 49643543 + README, sources verified then) AND the estate already ran an
  lru_null_arm experiment (memory/runs/lru_null_arm/lru_null_arm_results.json, schema
  lru_null_arm.v1). Marginal thread-only nuances filed here for that existing candidate: author
  gauravapiscean in-thread ("The dominant waste is tight tool loops whose 88k-token working sets
  exceed cache capacity, not sessions idling past a TTL"; requests arriving after gaps longer than
  the 5-minute provider TTL account for 17.5% of recompute; 393 real Claude Code sessions; radix-leaf
  LRU at 83.48% / 93.92% / 95.76% hit rate at 8k/20k/50k blocks; TTL-300s arm byte-identical to
  LRU-leaf); achierius (in his first run the offline-oracle Belady policy lost to LRU, which he
  reads as a broken harness, not a result); wongarsu (from the part-4 tables some policies would
  start overtaking LRU at larger KV-cache sizes, and the 5-minute eviction never triggered in tests,
  which should have prompted reevaluating chosen cache sizes). BreadthKV (arXiv 2610.05685,
  lens/burns.md:112-113) remains the estate's own retained-token-count optimization; this null
  result is its cautionary sibling and was already known here.

## OWED / degraded doors (nothing fabricated)

- openai.com/index/better-prompt-caching-for-gpt-6/ - WebFetch returned HTTP 403; the web reader
  fallback hit MCP error -429 (rate limit) twice. Provider doc UNREAD. Thread-level evidence only
  (HN 49807383, 2 comments): OutOfHere: "The biggest continuing limitation I see is that the cached
  input has to be at least 1024 tokens." RQ2's provider-doc half is therefore covered only by the
  mempko measurements plus the doug.sh runtime semantics; a later pass with a working door should
  read the OpenAI page proper. Catalog already holds 44 prompt-caching-adjacent rows including
  today's w3-research-cachemech intake, so the topic is not dark, just this specific doc unread.
- LensVLM paper (arXiv:2605.07019) benchmark numbers; Yandex post gives no memory/cache-size
  figures; siddhantkhare "A cache hit is not proof that you skipped the work" read end to end but
  its validation is synthetic-only (10-case deterministic control; nice echo of our
  byte-identical-ask law, not banked); calpaterson "Agent memory as a file format" (191 pts, 96
  comments) read but is anecdote-class for RQ3 measurements, not banked; Magnitude YC S25 launch
  thread (194 pts, 99 comments) has vendor-thread numbers only (founder: TurboQuant-inspired KV
  quantization to 8-bit keys and 4-bit values, "drops KV memory usage by over half"), not banked.

## Verdict line for the lens

The measured late-2026 answer to "compaction that preserves continuity" is retention scope, not
smarter summarization (item 1: keep the prose, compress the tool output); the answer to "when does
long-context beat abstraction" is that full-context itself rots 15-25% by 250k tokens (item 4) while
a 9B guide-and-expand model runs at 5-15x compression (item 5); and the prefix-cache world
independently rediscovered our byte-identical-prefix law the hard way (items 2 and 3). All three
legs feed mag/context_compression.py and the context-pack gap fix.
