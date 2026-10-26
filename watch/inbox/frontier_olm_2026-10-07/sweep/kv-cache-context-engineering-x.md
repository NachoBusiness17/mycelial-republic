# Sweep: kv-cache-context-engineering via X (frontier_olm_2026-10-07)

source-fetched: 2026-10-07

Seat: sweep-kv-cache-context-engineering-x. Area feeds mag/context_compression.py
(degree-7 hub, lens/graph.md:22), the context-pack layer (whose propagation gap went
live in DOGFOOD2 night 1/3, lens/burns.md:151-153), and the corpus FTS retrieval organ
(1,195,926 rows, lens/corpus.md:8).

## Door health (this seat, this sitting)

- WebSearch (the X door's first leg): 11 queries issued, 2 hard timeouts at the 60s wall
  and 3 batches that returned MCP 429/1302 before succeeding on reworded retry; results
  consistently TRUNCATED x.com URLs to bare "https://x.com" with no status IDs, the same
  failure the OLM-x sibling reported (open-local-language-models-x.md:15-16). No X post
  from my candidate list was resolvable to a status ID this sitting.
- fxtwitter door: PROBED ALIVE this sitting, curl https://api.fxtwitter.com/jack/status/20
  returned HTTP 200 valid JSON ("just setting up myttr" parse check ok), consistent with
  lens/doors.md:24-28. But with zero status IDs surfaced by search, no candidate post
  could be resolved; per the ask's recipe the unresolvable X posts are banked at
  SNIPPET tier with the truncated URL and flagged as such (one such item banked, item 8).
- WebFetch: timed out on docs.x.ai subpages twice; every deep read below rode
  curl -s -m 30/40 from the repo shell (sibling-verified fallback,
  open-local-language-models-x.md:9-12). Reddit door stayed closed (lens/doors.md:35-38),
  no reddit items.

## Method

- Pass 1 (broad): 11 WebSearch queries (site:x.com and open-web) across the five
  research questions. 40 distinct candidates considered (census in the section below);
  date-window honesty: today is 2026-10-07, strict 30-day window opens 2026-09-07. Only
  a minority of candidates are strictly in-window (xAI compaction beta stamp 2026-09-04;
  the Playwright context-efficiency post; the Sep blog wave). I banked on strength and
  state each item's real date; the provider docs are living pages whose every quote was
  re-fetched and read TODAY (2026-10-07).
- Pass 2 (deep read): 9 documents read end to end this sitting via curl (bytes saved
  under sweep/_raw/: xai_what_breaks.html, xai_context_compaction.html, xai_how_it_works.html,
  anthropic_prompt_caching.html, anthropic_compaction.html, anthropic_context_editing.html,
  openai_prompt_caching.html, together_serving_v4.html, dailydoseofds_caching.html) plus
  deepseek_kv_cache.html read for overlap confirmation. That is 7 banked deep reads (item
  8 is snippet-tier) against the ask's >=5 floor.
- Overlap instrument (exact commands run this sitting): per-term
  grep -c -F "<phrase>" catalog/catalog.jsonl and
  rg -l -F -g "*.md" -g "*.jsonl" -g "*.json" "<phrase>" memory/ watch/inbox/frontier_olm_2026-10-06
  watch/inbox/frontier_olm_2026-10-07. Self-hit rule: memory/trajectory/steps.jsonl rows
  naming my own curl commands are THIS session's journal, not holdings; verified by
  reading the matched rows.

## Anti-rebank decisions (read before mining this area again)

1. DeepSeek Context Caching on Disk docs (api-docs.deepseek.com/guides/kv_cache): I
   fetched and read the page today; the prefix-unit matching semantics ("a subsequent
   request can only hit the cache if it fully matches a cache prefix unit", the SWA note,
   persistence at request boundaries / common-prefix detection / fixed intervals) are
   ALREADY ESTATE-HELD by memory/research_packs/20260809T021009Z_cache-aware-context-batching.answer.remote.md:44-49
   with an archived copy at memory/improve/deepseek_api/context_caching.txt (pack:265).
   NOT banked as an item. Today's fetch confirms the page still states the same rules;
   zero drift detected.
2. BreadthKV 2610.05685 and BARQ 2610.04490: banked day-6 (lens/burns.md:112-113). The
   eviction/quant paper frontier (KV-Kaizen, TaSQ, QuantMLA, PatchKV, DeferKV, LORE-KV
   2610.07643, MaskAhead 2610.06996, SoloQ 2610.07121) is fully enumerated in the
   sibling quant sweep's dedup list (quantization-compression-arxiv.md:18-22). None
   re-banked; my Q1 add is the SERVING-side item the paper seat does not hold (item 3).
3. DSv4.1-Flash 890 bytes/token: held (sibling HN quant, via memory/runs/gapwave/
   kvmem_digest.md:66 and zartbot analysis). The Together piece below is a different
   artifact (engine cache policy on V4 CSA/HCA/SWA, per-token footprints 3.4-3.8 KB on
   their B200 path, capacity math), verified absent from catalog and memory.
4. _avichawla posts: three OTHER posts banked prior (IDs 2075888860115120424 decoded
   2026-07-11, 2084909858386792674 decoded 2026-08-05, article 2096491130489872479
   decoded 2026-09-06; decode formula (id>>22)+1288834974657 run this sitting). The Aug
   27 caching article is a fourth, distinct artifact; blog.dailydoseofds.com greps 0 in
   catalog.
5. liao.gg, funes, memoryfields, RIME, MRAgent, Hindsight/Zep/Konig temporal-KG:
   banked by the agent-memory-x sibling today (agent-memory-continuity-x.md:53-154);
   its "compaction FAILED a task via flattened summaries" datapoint stays theirs.

## Pass 1 census (40 candidates considered; disposition each)

Banked deep-read (7): xAI What Breaks Caching doc; xAI Context Compaction doc; xAI
how-it-works doc (merged into item 1 evidence); Anthropic prompt caching doc; Anthropic
compaction + context-editing docs; OpenAI prompt caching doc (GPT-5.6 era); Together.ai
Serving DeepSeek-V4; Chawla KV/Prefix/Prompt/Semantic article. Banked snippet-tier (1):
"Cache engineering: the new skill that divides your bill by [N]" X post (Aug 24).
Confirmation-not-banked (1): DeepSeek context caching docs (see anti-rebank 1).
Rejected as held/duplicative (6): DSv4.1-Flash paper 2609.19969 + mem0 890B post +
TechTimes + Louis Bouchard KV benchmark (all the held 890B fact); NVFP4 KV vLLM X post
(Jun 23; sibling holds the NVFP4 thread via quant HN sweep); local-ai-zone KV evolution
history (headline number held). Rejected as weak/off-axis (25): DAIR.AI RAG-vs-LC opinion
post; Playwright CLI context-efficiency post (no ID, no numbers); seven-layer memory
architecture post (Feb, anecdote); Cache-2-Cache X post (no URL/date resolvable, noted
as a lead); DeepSeek-V4 1M Chinese X post (no ID; its CSA/HCA/SWA content is covered
better by banked item 3); Efficient Memory Sharing Multi-Agent KV post (Apr, no ID);
Spheron context-engineering blog; AppScale KV-cache engineering + prompt-caching
architecture blogs; baeseokjae caching guide; Digital Applied x2; Flexera; Modular
handbook; Traversaal; ML Mastery guide; dataaspirant LC-vs-RAG; meilisearch; usewire;
arXiv 2501.01880 (Jan 2025, out of window); Medium MahabubKarim; SuperAnnotate OP-RAG
(2024-5 era); AussieAI global KV; alphaXiv KV steering; PyTorch GB300 SGLang post
(5x throughput claim, vendor co-design piece, no cache-policy numbers; lead only).

## Banked items (8, strongest first)

### 1. xAI "What Breaks Caching" doc: reasoning-channel omission is the top cache-kill

https://docs.x.ai/developers/advanced-api-usage/prompt-caching/multi-turn (page states
"Last updated: March 16, 2026"; fetched and read 2026-10-07). RQ2, and the provider-side
canon for the estate's byte-identical-ask law. Verbatim: "Any change to earlier messages
breaks the cache. Only append new messages at the end." and "For reasoning models, you
must include reasoning_content from previous responses; omitting it is the top cause of
cache misses." Two sanctioned repair paths for reasoning models: send back the encrypted
reasoning_content, or use previous_response_id stateful chaining. The how-it-works page
adds: "Prompt caching is not 100% guaranteed. Cache entries can be evicted due to memory
pressure, and requests may be routed to different servers. Use x-grok-conv-id to
maximize cache hit rates." Overlap: catalog 0 hits for "What Breaks Caching" and
"x-grok-conv-id"; the 2026-08-09 cache pack holds xAI pricing ratios and prompt_cache_key
mention only (pack:58-65), not these invalidation semantics. GRAFT: the context-pack
layer's propagation gap is exactly a prefix-stability problem; xAI's law says any
mid-prefix byte change (a moved METER line, a refreshed state block) kills the whole
cache, so pack assembly must be append-only per provider contract.

### 2. Anthropic Compaction beta (compact-2026-09-04): provider compaction that keeps recent turns verbatim

https://platform.claude.com/docs/en/build-with-claude/compaction (beta header
compact-2026-09-04 = dated 2026-09-04, in-window; fetched and read 2026-10-07). RQ3.
Server-side summary written by Claude with three modes (on demand, at token threshold,
client SDK Compact); the decisive design for the estate's continuity question is
"Compaction that keeps recent turns: when the last few turns must reach Claude word for
word. The summary covers only the older turns." plus background compaction, preserved-
thinking conditions, re-compaction of compaction blocks, and the honesty hatch:
"Write your own summarization prompt: when the default summary drops something a later
turn needs." Context-editing sibling page (fetched) adds rule-based clearing
(clear_tool_uses_20250919, clear_thinking_20251015) as the non-summarizing alternative.
NO quality measurements published on the page; the mechanism is the steal. Overlap:
catalog 0 for "compact-2026-09-04"/"clear_tool_uses_20250919"/"context-editing"; pack has
one Anthropic line (minimums, pack:19). GRAFT: context-pack should adopt the same split:
N most-recent turns byte-verbatim, older turns summarized, with a user-overridable
summarizer prompt; that is a direct fix shape for the propagation gap (lens/burns.md:151-153).

### 3. Together.ai "Serving DeepSeek-V4": cache POLICY, not architecture, sets realized capacity

https://www.together.ai/blog/serving-deepseek-v4-why-million-token-context-is-an-inference-systems-problem
(dated 2026-05-11 by search; fetched and read 2026-10-07; out of strict window, banked on
strength). RQ1, the agentic-serving measurement framework the paper seat does not hold.
Verbatim: "A full-SWA implementation actually had a higher per-token KV footprint than
our V3 path - roughly 3.8 KB per token versus 3.4 KB - because the engine was storing
the full sliding-window state. The practical gain came from cache policy. By keeping
only the SWA states most likely to be reused, we increased total KV-cache capacity on a
single NVIDIA HGX B200 node from roughly 1.2M tokens to 3.7M tokens with minimal
changes." Also: V4 needs three concurrent cache types (CSA stride-4 8-token
neighborhoods with 128 selected entries; HCA stride-128 -> ~8K entries at 1M context;
SWA), "prefix caching becomes a per-cache-type policy decision", "test SWA full-store
against recompute-on-hit", and the agentic metric: "For long-context agents, measure
cache hit rate, decode throughput, and cost per completed task." Overlap: catalog 0 for
"serving-deepseek-v4"/"together.ai/blog"/"3.8 KB per token"; memory hits are my own
steps.jsonl journal rows. GRAFT for mag/context_compression.py: retention decisions are
per-cache-TYPE, not global; BreadthKV-style count-buying is an engine-policy question,
and the estate's equivalent is which pack layers stay verbatim vs recomputed.

### 4. OpenAI prompt caching docs, GPT-5.6 era: explicit breakpoints, 1.25x writes, settings table

https://platform.openai.com/docs/guides/prompt-caching (live page, no date shown,
fetched and read 2026-10-07). RQ2. Verbatim: "For GPT-5.6 and later, cache writes cost
1.25x the standard, uncached input-token rate. Subsequent reads cost 0.1x that rate on
most of these models and 0.05x on GPT-6.1 Sol." Minimum cacheable length "1,024 tokens
for GPT-5.6 and later"; implicit AND explicit breakpoint modes with prompt_cache_options
ttl "30m"; cached-input discount "up to 95%"; "Cache reuse requires the entire rendered
prefix to match"; "maintaining a session doesn't guarantee a cache hit"; settings that
silently change the prefix: model, tools (names/descriptions/schemas/ordering),
parallel_tool_calls, text.format, reasoning.effort ("use a configuration update to
change effort while preserving the earlier prefix"), text.verbosity; a Prompt Caching
Dashboard and a Prompt Cache Diagnostics tool that reports where the prefix diverged.
Overlap: catalog holds only the openai-agents-python SDK impl files (3 rows:
run_internal/prompt_cache_key.py et al.), not doc semantics; pack:19 holds the old flat
1024 minimum one-liner. GRAFT: the settings table is a checklist for the harness's own
dispatch (tool-schema ordering and effort changes are cache killers); the diagnostics
endpoint pattern is the verification tool the byte-identical-ask law lacks.

### 5. xAI Context Compaction API: opaque encrypted compaction items

https://docs.x.ai/developers/advanced-api-usage/context-compaction (fetched and read
2026-10-07; page shows no date). RQ3. Verbatim: "Context compaction lets you shrink
those messages into a single opaque item that preserves the salient state - system
prompts, attached files, prior reasoning, and a compacted record of the turns - while
dropping the verbose tool output and back-and-forth." POST /v1/responses/compact returns
a compaction item passed back "verbatim"; "Treat encrypted_content as opaque - do not
parse or modify it"; compact "every N turns inside an agent loop, or once whenever your
bookkeeping shows the rendered context above a threshold"; "use_encrypted_content=True
is recommended for reasoning models so the model's reasoning content from prior turns is
preserved through the compaction." No measurements published. Overlap: catalog 0 for
"responses/compact"; "encrypted_content" appears only in litellm router code (2 rows).
CONTRAST worth banking: the estate's readable-first law (lens/corpus.md:48) is the exact
opposite bet; xAI's blob is unauditable by construction, which is precisely what the
estate's citation-lint doctrine refuses. Knowing both designs exist is the intel.

### 6. Chawla "KV vs Prefix vs Prompt vs Semantic Caching": the four-layer mechanics with the vLLM block-hash chain

https://blog.dailydoseofds.com/p/kv-vs-prefix-vs-prompt-vs-semantic (dated Aug 27, 2026
on page; fetched and read 2026-10-07; X post form Aug 28, unresolvable to ID). RQ1+RQ2.
Verbatim: "The first three are exact-match and correctness-neutral, so a miss costs you
money and latency. The fourth is fuzzy-match, and it will hand you a wrong answer with a
200." Mechanics held nowhere in the estate: vLLM caches "fixed-size blocks of 16 tokens
and identifies each block by a hash over the parent block's hash plus the token IDs
inside it"; "a block only matches if everything before it matched too"; partial trailing
blocks recompute every request; LRU eviction under memory pressure; RAG chunk reordering
shares NOTHING under the chain hash; "on traffic with genuinely unique prompts,
benchmarks have measured a throughput regression rather than a gain"; Anthropic "caps
that at 20 blocks, so adding more than 20 blocks of conversation between two calls
pushes the last write out of range and the hits stop"; GQA/MLA/FP8 as the three
cache-shrink axes; 70B BF16 at 128K ~= 40 GB cache. Overlap: catalog 0 for
"dailydoseofds"; the three held _avichawla posts are other artifacts (anti-rebank 4).
GRAFT: the estate's ask-stacking math (pack:92-100) gains the block granularity truth:
byte-identity must hold in 16-token block units, and a 20-block stride between
consecutive calls is the silent hit-killer on the Anthropic lane.

### 7. Anthropic prompt caching doc: the invalidation hierarchy and per-model minimums

https://platform.claude.com/docs/en/build-with-claude/prompt-caching (fetched and read
2026-10-07). RQ2. Verbatim: "the cache follows the hierarchy: tools -> system ->
messages. Changes at each level invalidate that level and all subsequent levels."
Tool-definition edits invalidate the ENTIRE cache; "Changes to tool_choice or the
presence/absence of images anywhere in the prompt will invalidate the cache"; thinking
blocks "cannot be cached directly with cache_control. However, thinking blocks CAN be
cached alongside other content when they appear in previous assistant turns"; TTLs
5-minute or 1-hour; minimum cacheable 512 tokens (Opus 5.5/Sonnet 5.5/Haiku 5.5) up to
4,096 (older Opus); automatic caching mode moves the breakpoint forward as conversations
grow; cache diagnostics compare consecutive requests and report the divergence point;
unstable tool_use key ordering (Swift/Go JSON randomization) breaks caches. Overlap:
catalog 0 for "invalidates the cache"; pack:19 holds only the minimums range. GRAFT:
tool-definition stability is a HARDER law than message stability; any harness that
regenerates tool schemas per session (or emits unordered keys) is paying full prefill
every call while believing it caches.

### 8. SNIPPET-TIER X post: "Cache engineering: the new skill that divides your bill by [N]"

URL truncated by search to https://x.com (recipe fallback invoked; date from search
snippet Aug 24, 2026). RQ2 practitioner framing. Snippet verbatim: "The 256 rule: a
request can hit the prefix cache only when the previous request's prompt tokens exceeded
256. Below that, nothing is cached". NOT VERIFIED against any provider doc: Anthropic's
documented minimums are 512-4,096 and OpenAI's is 1,024; the 256 figure matches no
provider page I read today, so treat it as the post's claim about one specific provider
or a stale number. Banked because the post's framing (cache engineering as a bill-
dividing skill) matches the estate's ask-stacking doctrine and the number needs a
source before anyone quotes it. Overlap: catalog 0 for "divides your bill". Resolution
to full tier is OWED: needs the status ID.

## Question-by-question verdicts

- Q1 (KV compression for agentic serving; retained-token optimizers): the paper frontier
  is fully enumerated by the sibling quant sweeps (anti-rebank 2); nothing new in-window
  supersedes BreadthKV's precision-for-count frame. My add is the serving-side datum
  (item 3): realized capacity is set by per-cache-type policy (keep/recompute/evict),
  with the 1.2M -> 3.7M token capacity number as the production measurement, plus the
  agentic cost metric "cost per completed task". Together explicitly promises per-token
  KV footprint and prefix-policy numbers as follow-ups ("We'll publish those numbers as
  the V4 kernels and cache policies mature") - a named OWED for the next sweep.
- Q2 (prompt-cache correctness, byte-identical-ask law): the strongest haul. Four
  providers documented today (items 1, 4, 6, 7 + DeepSeek confirmation): exact-prefix
  matching everywhere; reasoning channels are the agentic killer (xAI: reasoning_content
  omission = top miss cause; Anthropic: thinking blocks cache only inside prior
  assistant turns; OpenAI: reasoning.effort changes the prefix unless updated in-place);
  TTL semantics (Anthropic 5m/1h, OpenAI 30m option, xAI eviction + rerouting "not 100%
  guaranteed"); hidden invalidators (tool schemas, key ordering, images, verbosity,
  parallel_tool_calls); granularity truths (16-token blocks, 20-block lookback, prefix
  units on DeepSeek). The estate's law is byte-identical-ask; the docs say the contract
  is byte-identical RENDERED PREFIX INCLUDING TOOL DEFINITIONS AND SETTINGS.
- Q3 (compaction preserving continuity): provider mechanisms now exist on both coasts
  (items 2 and 5) but NEITHER publishes continuity measurements; the only measured
  compaction datapoint in the estate's orbit remains the sibling-held funes result
  (compaction FAILED a task via flattened summaries) plus Anthropic's own admission
  that default summaries drop things (item 2). The d01 shed propagation gap should be
  fixed with the kept-verbatim-recent-turns split (item 2's design), and the estate
  should MEASURE what providers won't: task-critical recall across a compaction
  boundary, which is exactly the Turing castle falsifier (lens/burns.md:160-161).
- Q4 (long-context vs retrieval at local scale): HONEST GAP. No in-window published
  measurement surfaced through this door that pits long-context ingestion against FTS
  retrieval on a local 7B-class model; the visible web consensus (dataaspirant,
  meilisearch, usewire) is listicle-tier; DAIR.AI's X post is an opinion ("I have yet
  to see a convincing paper"); arXiv 2501.01880 is out of window and not local-scale.
  The estate's own 1,195,926-row FTS organ remains unbenchmarked against long-context
  by anyone. OWED: a local A/B (FTS5 top-k vs full-context ingest at equal token budget
  on qwen2.5:7b), which no public source will hand us.
- Q5 (information loss in guide/summary abstraction): the honest state is that
  providers ship the abstraction (items 2, 5) while publishing no loss measurements,
  and the measurement work lives in the sibling seats (funes' flattened-summary task
  failure; temporal flattening 244/381 held day-6, lens/burns.md:100-102). The
  Playwright CLI context-efficiency post (snippet-tier, not banked) frames the
  practitioner version ("more work before context rot kicks in") without numbers.
  OWED: a designed loss probe - same task, full context vs context-pack, graded - is
  the estate's own instrument to build; nothing published this window does it.

## Not run / OWED

- No pytest, no estate-box measurements (none named by this ask).
- fxtwitter deep reads: 0 of my candidates resolvable (no status IDs surfaced); door
  verified alive on the known-post probe only.
- Item 8 resolution to full tier (needs status ID); Cache-2-Cache and the Chinese
  DeepSeek-V4 1M post remain leads (no URL/date); Together's promised follow-up numbers
  (per-token KV footprint, prefix-policy impact) are the named next-fetch.
- The "256 rule" figure is unverified against any provider doc read today; do not
  repeat it without the source post.

## Receipt (commands run this sitting)

WebSearch x11 (2 timeouts, 3 rate-limit batches, all queries eventually answered or
abandoned as stated); WebFetch x6 (docs.x.ai overview + prompt-caching + 2 timeouts,
anthropic 404 probe); curl x13 (docs.x.ai x4, platform.claude.com x3,
platform.openai.com x1, api-docs.deepseek.com x1, blog.dailydoseofds.com x1,
together.ai x3 incl. slug probes); fxtwitter probe x1 (HTTP 200); snowflake decode x3;
catalog greps x18 terms; rg over memory/ + 10-06/10-07 run dirs x12 terms; steps.jsonl
hit inspection; pack inspection (research_packs/20260809T021009Z read at lines
12-103, 265-282); sibling sweep files read: quantization-compression-arxiv.md,
quantization-compression-hn.md (grep tier), open-local-language-models-x.md (full),
agent-memory-continuity-x.md (full); lens files read: burns.md (full), corpus.md
(full), graph.md (full), doors.md (full). Raw fetches saved under
watch/inbox/frontier_olm_2026-10-07/sweep/_raw/ (12 files).
