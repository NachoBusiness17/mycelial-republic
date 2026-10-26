# FRONTIER SWEEP: kv-cache-context-engineering via hn - 2026-10-08

source-fetched: 2026-10-08. Gopher seat: sweep-kv-cache-context-engineering-hn (this session).
Estate feeds named by the ask: deliberate-ask frozen-prefix carriers (lens/laws.md:75-77), the P3
thinking-default reader (lens/burns.md:117), context_compression.py invariants
(memory/percolator/invariants.json), per-family cache grammar rows in the model garden, the
omission-is-measured-ON law (lens/laws.md:28-30), the RAM-cache mtime-fingerprint law
(lens/laws.md:103-105), and the invariant cross-link gap (lens/graph.md:29).

## Prior-sweep collision (read BEFORE banking; this door is on its third run)

This exact sweep name ran 2026-09-30 and 2026-10-07. Both banks were read in full this session:

- 09-30 bank (watch/inbox/frontier_olm_2026-09-30/sweep/kv-cache-context-engineering-hn.md +
  register.jsonl + steal/kv-cache-context-engineering.md): deep-read doug.sh, Yandex,
  boolean.ai context-rot, agentic-kv-cache README, HN 49643543, zartbot, LensVLM card,
  m-reschreiter dynamic-tools, Ask-HN-49783040, Prompt Trees; banked replay.doctor as a
  story-text instrument lead ONLY (register row 10, "not a verified number"); listed Fathom,
  Internet-for-the-KV-Cache, GPT-6 caching, Magnitude as considered-but-NOT-banked.
- 10-07 bank (watch/inbox/frontier_olm_2026-10-07/sweep/kv-cache-context-engineering-hn.md):
  banked future-os compaction-measured, doug.sh, mempko keepalive, boolean.ai context-rot,
  LensVLM, Yandex agent-runtime, j9s.io; explicitly NOT banked zartbot (catalog holds 14 rows
  incl. a corpus .txt copy), LRU/agentic-kv-cache (09-28 percolator candidate +
  memory/runs/lru_null_arm experiment), Magnitude ("vendor-thread numbers only").

Today's rule therefore: none of the 09-30/10-07 banked items are re-banked. Four of them
(doug.sh, agentic-kv-cache README+thread, zartbot post, LensVLM card) were re-read end to end
this session as a consistency check; every fact I extracted matched yesterday's bank (numbers
reproduced: 55%->95% cached / TTFT 26-28s->7.3s / 12,622-token prefix match / 890 B/token /
8k-20k-50k hit rates 83.48-93.92-95.76 / TTL-300s byte-identical to LRU-leaf). Zero drift
found; no re-bank.

## Method (two passes, as ordered)

- Pass 1 broad: 8 hn.algolia.com queries (7 search_by_date + 1 relevance /api/v1/search), all
  tags=story with numericFilters created_at_i>1788825600 (2026-09-08, 30-day window):
  "kv cache" (21 hits), "prompt caching" (11), "context engineering" (11), "prefix caching"
  (3), "llama.cpp" (24), "context compression" (5), "vllm" (30, mostly LLM-fuzzy noise),
  relevance "cache kv llm" (7, all dupes). Unique candidates considered: ~55, over the 30 floor.
- Pass 2 deep: 14 fetch attempts, 12 pages/threads read end to end: zartbot dsv41flash,
  agentic-kv-cache README + HN thread 49643543 (58 comments), doug.sh, HN thread 49735410,
  replay.doctor, HN threads 49911995 (99 comments) and 49911910 and 49807383, HF LensVLM-9B,
  jaehun.me memory-wall post, arXiv 2609.17652 (Fathom), arXiv 2608.01526,
  jadidbourbaki prompt-lookup post. Two doors died: openai.com/index/
  better-prompt-caching-for-gpt-6/ returned HTTP 403 (recipe fallback thread 49807383 read;
  2 comments, only OutOfHere's 1024-token minimum, byte-identical to what the 10-07 sweep
  filed as OWED), and github.com/DOMINICALI1/kv-cache-migrator returned 404.

## Overlap instrument

Per-term grep of catalog/catalog.jsonl + memory (rib/, steal/, corpus/LINKS.jsonl,
frontier/*.jsonl, burns/LEDGER.jsonl, percolator/candidates.jsonl, both prior registers;
memory/trajectory/steps.jsonl excluded as self-echo per the 10-07 sweep's discovery). First
attempt (recursive grep over all of memory/) was killed at ~4 min as impractical; the bounded
depth-2 file list (9,278 files) is what ran. Findings folded per item below.

## Banked (7, strongest first; all with today's primary read)

### 1. The KV Cache Is the New Memory Wall (SoK synthesis)
source-fetched: 2026-10-08 - https://jaehun.me/en/posts/paper-2609-30854v1/ (HN 49945575,
2026-10-03). Reviews arXiv 2609.30854 (Tejinder Singh, Dell; SoK).
Quote: "Almost every published number is right on its own. But almost none of them can be
interpreted together."
Why: the coordinate system the per-family cache-grammar garden rows (RQ3) are missing: five
technique domains (quantization w_q, eviction r, paging phi, prefix sharing sigma, tiering
lambda) combine multiplicatively at the byte level; every published speedup is regime-conditional
(compute the crossover s* and s_cap first; same 2-bit quantization gives 1.25x at batch 1 vs
4.82x at batch 32). Bankable laws: "tiering is for reuse between steps, not for reads within a
step" (fetching a cached 128k context is 38x-2100x faster than recompute); lossless domains
(paging, prefix caching) never speed decode but change feasibility (paging cuts waste 60-80% to
under 4%); Llama-3-70B crossover at 427k tokens batch-1 but 13.4k at batch-32. RQ1 feed: the
prefix-stable boot block's saved tokens must be quoted with regime (batch, context, device),
never bare. Overlap: the raw paper abstract is held (catalog row e4f43ee5d8b9,
state/arxiv/2026-09-28/2609.30854v1.txt, 2,002 bytes) but no register/steal row exists and
neither prior sweep banked it; this pass adds the blog synthesis. Confidence 0.92.

### 2. Magnitude (YC S25) launch thread - Vulkan-backend KV machinery, both sides measured
source-fetched: 2026-10-08 - https://news.ycombinator.com/item?id=49911995 (99 comments,
2026-09-30). Product: github.com/magnitudedev/magnitude, Apache 2.0, Rust.
Quote: "Both prefill and decode are roughly 2x faster when served from llama.cpp" (francisjp,
M5 Max, vs Magnitude 0.2.1).
Why: RQ4's live question (does anything KV-worthy run past Metal) gets its first concrete
candidate: Magnitude lists Vulkan as a shipping backend (used for AMD/Strix Halo), with KV
cache quantization 8-bit keys / 4-bit values (TurboQuant-inspired, claimed KV memory cut by
over half) and hybrid paged attention sharing prefix caches across sessions via a prefix tree.
Counter-evidence in the same thread: kmike84 ("beating llama.cpp on speed is a low bar"),
bythreads (Rapid-MLX beats it on decode 175 vs 161 tok/s, TTFT 64 vs 111 ms), herf (20-30%
slower decode on 5070ti), francisjp above. Verdict for the estate: Vulkan KV quant + prefix
tree exists outside Metal, but on Apple/CUDA boxes llama.cpp still wins today; a Windows/Vulkan
trial on our box is the only honest test. Overlap: considered-not-banked by 09-30; 10-07 read
founder numbers and left unbanked; this is the first bank, incl. the skeptic numbers.
Confidence 0.90.

### 3. Show HN: Token compression CLI (spenmcke/compress) - the unanswered red test
source-fetched: 2026-10-08 - https://news.ycombinator.com/item?id=49911910 (5 comments,
2026-09-30). Tool: github.com/spenmcke/compress.
Quote: "It would also be useful to check whether the task success rate drops after compression"
(SerhiiDrozdov, unanswered in thread).
Why: RQ5's falsifiable-invariant question in the wild: a fine-tuned Qwen compressor trims
Codex tool-call outputs (29.6% token reduction, measured via proxy-side usage counting,
`codex --uncompress` opt-out) while keeping the KV prefix intact - and the exact objection the
estate's context_compression.py invariants must encode is raised and NOT answered: token
reduction is not success-rate preservation, and tool outputs hide load-bearing one-liners
(status codes, failing test names, exit codes, file paths). Pairs with 10-07's future-os
finding (retention scope beats summarization): the red test = forced recall / task success
after compaction, not tokens saved. Overlap: zero hits in catalog, rib, steal, LINKS, both
registers; not in either prior sweep's candidate list. Genuinely new. Confidence 0.90.

### 4. Fathom: per-query read depth over offloaded KV caches
source-fetched: 2026-10-08 - https://arxiv.org/abs/2609.17652 (HN 49893944, 2026-09-29).
Quote: "We present Fathom, a key scan in which each query decides how many bits of each key
channel to read."
Why: RQ4's offload leg with an honest boundary: 4-bit K cache in channel-major bit-plane
layout, per-query bit budget by reverse water-filling over variance-weighted channel
importance; 1.67x faster decode than 136-bit scans (Double Sparsity/Loki/SparQ) at 1M tokens
on Qwen3-8B; on real coding-agent sessions 92 bits matches the best 136-bit scan's accuracy;
explicitly NOT faster when the index is GPU-resident (it targets host-memory offload). Tells
the estate where offload research actually pays: only once the KV is already off the GPU.
Overlap: abstract snapshot held (catalog row 050b090834b5, state/arxiv/2026-09-17/
2609.17652v1.txt, 1,353 bytes); 09-30 sweep listed Fathom as considered-not-banked; this pass
deep-reads and banks the verdict. Confidence 0.93.

### 5. Replay Doctor - primary-page read of the banked silent-miss lead
source-fetched: 2026-10-08 - https://replay.doctor/ (HN 49691257, 2026-09-14).
Quote: "Replay Doctor reads the transcripts already on your disk and names the turn it broke
on, the cause, and the tokens re-billed at write prices."
Why: RQ1's instrument exists as product: replay diff names the breaking turn, cause, and
re-billed tokens; reads Claude Code, OpenAI Codex AND Ollama transcripts (our exact shapes);
cause taxonomy is a bankable law: "a re-render is frequent and small; a TTL expiry is rare and
enormous"; demo machine showed $631.77 re-billed across 123 sessions (~4% of $16,078.68 /
106.7M tokens). BSL 1.1, converts to Apache 2.0 2029-09-06. Overlap: banked 09-30 as a
story-text instrument lead only (register row 10, reddit door, "not a verified number"); today
adds the primary page (command grammar, provider list, cause split, license). Delta bank,
disclosed. Confidence 0.93.

### 6. Faster prompt lookup drafting in llama.cpp - CPU win, no KV relation
source-fetched: 2026-10-08 - https://jadidbourbaki.github.io/blog/prompt-lookup-llama-cpp/
(HN 49859982, 89 points, 2026-09-26).
Quote: "If the most frequent follower fails, the other candidate tokens will also fail"
(Lemire's threshold-before-score fix).
Why: RQ4 boundary evidence: the 42x drafting speedup (140x with Lemire's update) is pure CPU
data-structure work (segmented_map, sorted vectors, binary-fuse-filter constmap, 541 MB static
cache load 3.76 s -> 0.23 s) benchmarked on an M4 Pro CPU; the post names no Metal/CUDA/Vulkan
backend and no KV-cache or prefix-reuse mechanism. n-gram prompt-lookup drafting exploits
prompts that contain text the model will repeat - exactly the agent resend-history shape - so
it is a cheap local-lane win that does NOT depend on KV offload at all. Overlap: zero hits
(jadidbourbaki / prompt lookup absent from catalog, rib, steal, both registers). New.
Confidence 0.90.

### 7. An Internet for the KV Cache - the boundary-breaking vision, abstract-level
source-fetched: 2026-10-08 - https://arxiv.org/abs/2608.01526 (HN 49883064, 2026-09-28;
Ray, Feamster, Jiang).
Quote: infrastructure "should allow decoupling of compute and KV Cache storage across cloud
and datacenters."
Why: RQ3's long-game row: if KV becomes a network-distributed object, per-family cache
grammars stop being provider-proprietary and the frozen-prefix law gains a portability axis;
"bandwidth, latency and pricing directly determines how the KV Cache should be managed" is the
routing-class law in cache form. Abstract carries no numbers - position/vision paper; OWED: the
full paper is unfetched. Overlap: zero catalog/register hits; 09-30 listed as
considered-not-banked. Confidence 0.88.

## Answers to the research questions (what today's sweep adds; the rest OWED)

RQ1 (which ask paths mutate the frozen prefix; what a prefix-stable boot block saves): today's
additions are the SoK regime law (item 1: quote savings with batch/context/device or do not
quote), Replay Doctor's cause split (item 5: re-render frequent-and-small vs TTL
rare-and-enormous - the estate's per-turn attribution probe should bucket causes this way),
and the confirmation re-read of doug.sh (break taxonomy unchanged: shuffled JSON keys, live
status text near top, compaction, per-agent-before-shared ordering). The estate-side
measurement (which of OUR carriers mutate warm_state/briefs/world_state injections between
asks, in measured tokens) is NOT answerable from public sweep evidence; it needs the
logs/provider_usage.jsonl probe the 09-30 percolator row already specified. OWED, not run here.

RQ2 (do the P3 reader + omission-is-measured-ON law close the reasoning_content-omission miss
mode; do the six unwired carriers still drop reasoning): no public-source evidence this sweep
bears on our six carriers (stealth_driver, duel_harness, tesuji_fire, lane_runner, lite_scale,
wave_fire per lens/laws.md:154-158). That is an estate code probe, not a sweep finding. OWED.
Related banked context only: zartbot's V4.1-Flash post (re-read, unchanged) documents Bounded
Replay restoring decoder local state per turn, i.e. DeepSeek-side reasoning-state mechanics
live in the serving layer our carriers must mirror.

RQ3 (re-derive per-family cache grammars from primary vendor pages): NOT DONE this pass. The
xAI grammar is already vendor-documented in the estate (day-7: edit/remove/reorder breaks
prefix, reasoning_content omission top miss cause). The OpenAI GPT-6 page 403'd again today
(byte-identical door behavior to 10-07); fallback thread adds nothing beyond the already-filed
OutOfHere 1024-token-minimum quote. DeepSeek/Nous/Anthropic vendor pages were not fetched this
pass. What today adds instead is the meta-law for those rows (item 1): every grammar row must
carry its regime conditions or the rows cannot be interpreted together. OWED: a dedicated
vendor-page pass with a non-403ing door.

RQ4 (BreadthKV / BARQ / lmcache-src on llama.cpp/Ollama Windows/Vulkan; or non-steal):
BreadthKV/BARQ remain banked as day-6/7 steals with no new Windows/Vulkan port evidence in
this window (the agentic-kv-cache re-read confirms the research field is Metal/GPU-sim bound).
Today's candidates: Magnitude (item 2) is the only shipping Vulkan+KV-quant+prefix-tree engine
found, with in-thread counter-benchmarks; Fathom (item 4) says offload-depth tricks only pay
once KV is host-resident; prompt-lookup (item 6) is a KV-independent CPU win that works on our
box today. Net: KV offload on Windows/Vulkan is NOT proven a steal by public evidence; the
Magnitudes of the world need an on-box trial before any garden row flips from UNMEASURED.

RQ5 (falsifiable invariant set for context_compression.py): the sweep's two direct feeds are
item 3 (the unanswered success-rate objection = the red test: compaction must preserve task
success / forced recall, with anchors like exit codes and failing test names preserved
verbatim) and item 1 (regime-tagging of every number; lossless-before-lossy ordering). Red-test
shapes a new carrier must survive, honoring the mtime-fingerprint law (lens/laws.md:103-105):
(a) mutate the corpus file, assert the compressor sees the new bytes within one call (stale
snapshot = fail); (b) compact, then force recall against pre-compaction content; (c) assert
anchors verbatim post-compaction; (d) prefix stability: compacted output must not shift the
frozen-prefix bytes (doug.sh: compaction is a named prefix breaker). The cross-link gap
(lens/graph.md:29: 807 invariant nodes, avg degree 1.01) stays open - invariants exist but
carry no edges to each other or to doctrine; wiring those edges is an estate build, not a
sweep finding.

## Dead doors this pass (nothing fabricated)

- https://openai.com/index/better-prompt-caching-for-gpt-6/ - HTTP 403 (same as 10-07).
- https://github.com/DOMINICALI1/kv-cache-migrator - HTTP 404 (the "Zero-Copy KV-Cache
  Migration Protocol" story, HN 49619645, links a dead repo; not banked).

## Receipt

All 12 successful reads were WebFetch calls made this session (2026-10-08); quotes above are
verbatim from those fetches. Overlap greps run this session against catalog/catalog.jsonl and
memory (bounded depth-2 list, 9,278 files; full-recursive variant killed at ~4 min as
impractical, replaced not silently narrowed). Both prior same-door banks read in full before
any banking decision. No estate tooling was modified; this file is the only write.
