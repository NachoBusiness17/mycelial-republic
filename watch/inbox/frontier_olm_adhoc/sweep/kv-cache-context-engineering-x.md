# Frontier sweep: kv-cache-context-engineering via X (second pass of this path, 2026-10-11)

source-fetched: adhoc · swept 2026-10-11 · seat: sweep-kv-cache-context-engineering-x

This file OVERWRITES the first pass at this exact path (its 8 banked items are in git
history and are treated as holdings below; nothing here repeats them). Sibling banks in
this same tree treated as the dedupe floor: arXiv pass (RR-Evict 2609.32278,
Fancy-Eviction-Fails 2609.28870, Provenance 2609.38706, Request-Order 2610.05833,
Agent-Controlled-Forgetting 2610.10590, CADOC, KVSET, MCPacific), HN pass 1 + pass 2
(doug.sh, dacorvo/funes, future-os, WorkOS, Stagehand, zartbot DSV4.1F thread, Magnitude,
Skillzero, j9s.io, jaehun memory-wall, token-compression CLI, siddhantkhare
cache-hit-not-proof, emschwartz Jev prompt caching, Self-Pruning 2610.09051,
Internet-for-KV 2608.01526), reddit pass (Slow Vale, pi-optchat, KV transplants, vLLM
warm prefix cache, snapjudge, RTX PRO 6000 node, FRAMES, QSA offload), and the prior X
pass (Notation Matters, Don't Break the Cache, Manus, Governance Decay, louisbouchard,
Anthropic code-execution-with-mcp, Agentic Plan Caching, @philschmid tips).

## Door status (honest, again)

- WebSearch `site:x.com` lanes: refused or rate-limited most of the sitting (MCP 429
  code 1302 waves, two 60s timeouts at open), same wall the first X pass recorded. When
  the door did open it substituted general web results for x.com posts on every try.
- DuckDuckGo html + lite: CAPTCHA-walled (c21b). Google search page: error shell. xcancel
  nitter mirror: HTTP 451. nitter.poast.org: ENOTFOUND. threadreaderapp search: help-page
  only. Bing RSS works as a term door but silently drops the site: operator.
- Working X-URL discovery this sitting: HN Algolia comment lanes (commenters embed
  x.com/status URLs; numericFilters=created_at_i>1788998400 gave the 30-day window) plus
  local grep of the sibling seats' raw fetch files in this directory (~40 distinct status
  URLs, all snowflake-dated Nov-Dec 2025, outside window).
- fxtwitter door: clean JSON every time, no login, no 403s. Resolved and read this
  sitting: @kevin_flansburg/status/2050238819065299110, @mmastrac/status/2100626193943052784,
  @ggerganov/status/2067539416436867230, @lemire/status/2102369812806504705.
- Degradations (no fabricated fallbacks): completeskeptic.com "(KV) Cache Rules
  Everything Around Me" DNS-dead (ENOTFOUND x3, WebFetch + webReader both) - OWED, not
  banked. Blocks & Files OceanStor M900 article 404'd on both plausible URL shapes; banked
  as search-snippet fallback per recipe, flagged in its note. The ts.net "trained KV cache
  bank" demo page ENOTFOUND; banked from the author's HN comment (a page I did fetch via
  the Algolia items API), flagged. sohu M900 article: my guessed URL 404'd (my error,
  disclosed). z.ai webReader: two -429s and one -500 across the sitting, recovered on
  later calls.

## Pass 1 census

60+ candidates considered; 34 strictly inside the 30-day window (2026-09-11..10-11):
HN Algolia story lane "kv cache" 30-day (13 stories: DSV4.1-Flash zartbot + PDF trio,
Self-Pruning 2610.09051, KV-bank-as-Jev, j9s.io, CREAM joke post, memory-wall review,
internet-for-KV, embed/KV, token CLI, Ask HN swarm caching, vLLM warm, MoE viz) + comment
lanes (DSV4.1-Flash freak-out thread 2026-10-08, Qwen3.8-Flash-Next consumer thread
2026-10-04/05, Claude Haiku 5.5, How-many-GPUs, OpenTPU, Context Language Models, GLM 5.3
Flash month) + story lane "x.com" 30-day (30 stories, only lemire's optimization article
on-area) + vLLM x.com comment lane (12 hits) + context-engineering comment lane (14 hits,
zero X URLs) + z.ai searches (RR-Evict confirm; Sept shared-KV announcements: OceanStor
M900, TuringData ContextCube, Huawei Atlas 960, SageMaker HyperPod, AMD Infinity Context,
Mooncake InferenceX, SemiAnalysis Sept-21) + GitHub code search (20 repos) + sibling raw
grep (~40 URLs). Near-window considered: Kimi k2.6 Workers-AI post (May 2026), LMCache
zeros fix repo (Aug 21-25 2026), FlashMLA (2025). First-pass items all excluded as held.

## Pass 2 deep reads (pages fetched and read end to end this sitting)

lmcache-hybrid-gdn-restore-fix README + EXPLAINER (gh api, full); AMD UltraQuant KV4 blog
(full); AMD ROCm 10.1 blog (full, date checked: 2026-10-05); fxtwitter JSON for the four
X posts above; lemire "A Summer of AI Optimization" (full - off-area, see below); HN
threads 50000488 (DSV4.1-Flash), 49813610 (KV-bank demo), 49953495 (Qwen Flash Next).

## Banked items (strongest first)

### 1. LMCache hybrid Mamba/GDN disk-tier restore silently corrupts; hit-rate metric lies
github.com/dl4rce/lmcache-hybrid-gdn-restore-fix (repo created 2026-08-21, pushed
2026-08-25; upstream issue LMCache#4701, fix PR #4731 opened 2026-08-25, NOT merged).
Deep-read README + EXPLAINER. Hybrid GDN+full-attention models (Qwen3.8-27B verified,
25:1 subpaging; Qwen3.5-0.8B 17:1) force vLLM's unified block size above the attention
kernel page size; `_SubpagedAttentionViewEdit` only pattern-matches the old 5-dim KV
layout, so on vLLM >= 0.26 (4-dim K/V-packed) the FA group is misclassified as
slot-compressed and the disk tier persists 1 of 25 kernel pages - ~4% of the attention
cache - with high reported hit rates and WRONG continuations, no exception. Second bug:
single-page staging buffer mutates shared meta.address between async copies, so the stored
object is ~96% zeros. Geometry-driven, not config-driven: bites the model class at any TP.
RQ1 verdict: this is the provenance re-audit's nightmare made public - the estate's
hit-ratio telemetry (prompt_cache_hit_tokens capture) counts hits, not correctness; any
hit-ratio claim over a hybrid-attention janitor on a disk/CPU KV tier needs a
wrong-continuation check or it is decoration. Bonus law from EXPLAINER bug 2: their own
debug instrumentation shadowed a variable (`st`), making every failure present as one
identical 180s hang - instrumentation bugs can mask the bug you are hunting.

### 2. UltraQuant KV4: native 4-bit MXFP4 KV cache for agentic serving on Instinct
rocm.blogs.amd.com/software-tools-optimization/ultraquant-kv4/README.html (2026-09-25;
arXiv 2606.20474). Deep-read. Qwen3.8-2.4T-A95B MXFP4 (262K ctx, KV on 23 of 92 layers),
MI355X x8, vLLM v0.19.2rc0: FP4-grid KV with shared pow2 scale per 32 channels +
Walsh-Hadamard rotation, FP4 goes straight into CDNA4 MFMA (no dequant). On a real
SemiAnalysis InferenceX agentic trace (long shared prefixes, short outputs, high
concurrency): +29% tok/s and -24% per-token latency vs fastest 8-bit KV at C=32; TTFT
1.7x sooner; decode-attention kernel 2.25x at 32K; accuracy within noise (GPQA-Diamond
92.9 vs 94.4; SWE-bench Lite 81/100 vs 78, and 88 vs 81 with MTP). RQ4 verdict: the
KV-quant lever measured in the exact regime the estate's regime-dependence law demands
(a stated serving cell: model, hardware, concurrency, trace type) - the template for any
janitor-fleet quant+compaction claim. Overlap note: quantization sibling bank holds DSv4.1
Flash teardown etc.; "UltraQuant"/"2606.20474" grep = zero hits catalog + memory.

### 3. Cloudflare Workers AI ships shared KV cache + speculative decoding for Kimi k2.6
x.com/kevin_flansburg/status/2050238819065299110 (2026-05-01; fxtwitter-resolved this
sitting; 39,713 views, 22 bookmarks). Kevin Flansburg (Workers AI): shared KV cache
"should boost cache hit rates, lowering TTFT and blended cost" and speculative decoding
"should improve TPS, especially for predictable output like tool calls". X-door native,
provider-side shared KV cache pitched at exactly the estate's tool-call-heavy relay
shape; the multi-tenant sharing question (whose prefix may ride whose cache) is the
production twin of the Provenance paper's cross-tenant salt finding the arXiv sibling
banked. Overlap: "Workers AI" grep over catalog = 0; "Kimi K2.6" = 1 catalog row (the
model name, unrelated to this announcement).

### 4. ROCm 10.1: AMD Infinity Storage + hipFILE fast path for KV-cache offload
rocm.blogs.amd.com/ecosystems-and-partners/rocm-10.1-blog/README.html (2026-10-05; Adam
Chan, Amy Wiebe, Liam Berry, Saad Rahim, Danny Guan, Anshul Gupta). Deep-read incl. date
check. "Checkpoints, key-value caches, and model parameters now outgrow the fast memory
nearest to the GPU"; AIS (debuted ROCm 7.14) moves data storage-to-memory without CPU
routing, and hipFILE's new async fast-path + batch I/O target "checkpoint engines and
KV-cache offloading systems" end-to-end. The cross-tier KV transport line
(CacheGen/CacheBlend, the "Internet for the KV Cache" position paper) going vendor-native.
Direct estate tie: the lmcache-src shelf ALREADY carries LMCache's hipfile backend
(catalog rows corpus/library/lmcache-src/lmcache/v1/gpu_connector/_hipfile_async.py and
storage_backend/hipfile_shim.py) - the shelf and the AMD road meet; audit the shelf's
backend against the 10.1 API when ROCm lands. Overlap: "hipfile" catalog hits are all
inside lmcache-src paths (not this post); the ROCm 10.1 blog itself = zero prior hits.

### 5. Huawei OceanStor M900: 64 PB all-flash KV-cache base tier for Atlas 960 (SNIPPET)
blocksandfiles.com/flash/2026/09/18/ (2026-09-18; snippet-banked fallback - the article
404'd on both plausible URL shapes from this seat, and Huawei's e.huawei.com product page
403'd; quote is verbatim from the z.ai search-result content field, per recipe). M900 =
scale-out all-flash cluster giving Atlas 960 SuperPoDs an up-to-64PB KV-cache base tier;
Chinese coverage adds KV-aware adaptive storage that "predicts KV cache lifecycles based
on data value" (24 DWPD endurance) over the UnifiedBus interconnect. Significance for the
estate: the KV working-set capacity question (KVSET, banked by the arXiv sibling) is
becoming a hardware product category; eviction/lifecycle prediction is being pushed into
the storage tier. Confidence capped at 0.7 for the snippet-only provenance.

### 6. Trained KV cache bank steers a 26B model into Jev-like behavior (SNIPPET)
news.ycombinator.com/item?id=49813610 (2026-09-23; demo page
gambler-relay-us-west1.leo-fish.ts.net/demo is DNS-dead from this seat - ENOTFOUND - so
the item rests on the author's comment, fetched verbatim via the Algolia items API).
Author faangguyindia: a 26B model "hacked using a trained KV cache bank, responding like
Gemma", latency under 127 ms; asks came from the "jev in python" thread; no writeup or
shareable weights yet. Signal for the estate's Jev lane (LiteLLM guardrail models,
snapjudge-style typed decisions): a TRAINED KV prefix bank as a model-substitution lever
is the Cache-to-Cache semantic-communication line (the reddit sibling's transplant post
is the same lineage) reaching the Jev form factor. Weak until the demo resurfaces; banked
as a follow-up lead, not a fact.

## Read, NOT banked (with reasons)

- lemire.me "A Summer of AI Optimization" (+ its X-article twin, fxtwitter-resolved):
  excellent, but zero KV/cache/context content (library speedups from cheap AI-assisted
  experimentation; ada 0.54->1.28 GB/s, simdutf 83->160 GB/s). Off-area; the perf-wave
  thesis belongs to the open-local/inference lanes.
- @mmastrac/status/2100626193943052784 (2026-09-17, in window, 1,134 likes): "I ran some
  real, live evals on Jev vs DiffusionGemma-as-Jev (my patch for vLLM!)" - real eval
  content, but the estate already holds mmastrac's 5M-session compactor work (quantization
  sibling dedupe ledger) and DiffusionGemma itself (corpus_selfsteal INDEX.json:108563,
  gapwave tech_transcripts.md:41); serving-substitution marginal for the KV area.
- @ggerganov/status/2067539416436867230 (2026-06-18): MTP-model-alongside-in-Q4_0 tip
  (~15% perf), no KV content.
- completeskeptic.com "(KV) Cache Rules Everything Around Me" (HN 2026-09-25): DNS-dead
  from this seat; OWED to the next seat.
- "AMD Infinity Context" (the z.ai-surfaced ROCm AIC session page): could not locate a
  canonical URL (blog hub does not list it; the ROCm 10.1 post does not name it); the
  verified AMD coverage this sitting is items 2 and 4. Not asserted.
- TuringData ContextCube (PR Newswire 2026-09-28): press release, no technical depth;
  the M900 row already carries the shared-KV-cluster signal.
- llama.cpp cross-thread KV-cache leak symptom (Qwen Flash Next HN thread, phacker007
  2026-10-05: "randomly threw in characters from other thread's KV cache") - corroborates
  the estate's llama.cpp cross-tenant state-restore holding (arXiv 2609.18526) but is HN
  comment territory, not X, and the estate already holds the law.

## RQ ledger

- RQ1 (provenance re-audit): item 1 is the sharpest public evidence that a high hit rate
  can coexist with wrong continuations - the re-audit bar should add a correctness probe
  beside prompt_cache_hit_tokens; item 4's Multi-Tier I/O statistics is the vendor-side
  meter to steal. The prior X pass's siddhantkhare audit-chain card (HN sibling item 5)
  already supplies the typed-miss-reason shape; this adds the silent-corruption case.
- RQ2 (reach-ratio probe on a live seat tape): FIRED as named, NOT COMPUTABLE as defined,
  and that is the finding. Command run: .venv/Scripts/python.exe over
  memory/agent_sessions/desk-deepseek.json (the tape the fold names). Result: 26 messages,
  42,642 transcript bytes (system 9,617 / assistant 24,652 / tool 8,321 / user 52), one
  summary/compact marker at message idx 21 - but last_traces is an EMPTY list, so the
  emitted-bytes denominator (bytes actually sent on the last ask) is not recorded anywhere
  in the tape. Reach ratio as defined cannot be computed from this instrument; the probe
  needs an emit-side log (sha256-frozen per emit, per the fold's own spec) before it can
  fire. No number is asserted. Numerator + compaction-marker scan above are the only
  computed facts.
- RQ3 (RR-Evict vs freeze-the-prefix): unchanged by this pass (nothing new beats the HN
  sibling's verdict: avoid eviction, or compute-aware partial eviction); item 5 shows the
  industry answer is to throw a 64PB storage tier at the problem instead of a smarter
  policy - capacity before policy, which is KVSET's working-set question.
- RQ4 (regime dependence beyond keyword refusal): item 2 is the cleanest measured KV-quant
  cell (model+hardware+trace+concurrency stated, accuracy within noise) - the reporting
  template the janitor fleet's quant+compaction configs should copy; item 1 adds the
  failure-regime twin (hybrid-attention geometry silently breaks disk-tier restore). Both
  extend the McNemar discipline: state the serving cell or the claim does not transfer.

## Overlap ledger (commands run this sitting)

- catalog/catalog.jsonl grep -i for: lmcache-hybrid-gdn, dl4rce, LMCache 4701, UltraQuant,
  2606.20474, kevin_flansburg, mmastrac, OceanStor, Infinity Storage, hipFILE, leo-fish,
  trained KV cache bank, Workers AI -> only "hipfile" hits, all inside lmcache-src shelf
  paths (item 4's overlap note); one "Kimi K2.6" model-name row (item 3's note).
- memory/ prose dirs (research_polished, frontier, improve, steal, rib, percolator, runs,
  briefs, assumptions.md, law) grep for the same set: DiffusionGemma known
  (INDEX.json:108563, tech_transcripts.md:41 - reason mmastrac dropped); zero for every
  banked title/ID. A full recursive grep over memory/ was too slow and was stopped;
  prose dirs + catalog + sibling banks are the coverage claimed here.
- Sibling-bank files (arxiv/hn/reddit/x + quantization-compression-hn): item-by-item
  check above; one shared name (mmastrac) resolved as account-held, item dropped.

## Provenance

Every quote is verbatim from a page this seat fetched (fxtwitter JSON, gh api raw README,
WebFetch page text, Algolia items API, or - items 5 and 6 only - the named search/comment
snippet, flagged in-place). Dates are the source's own dates. Hygiene: no em/en dashes
authored; transcribed URLs unchanged.
