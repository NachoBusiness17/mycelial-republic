# PHOTON FAST SEARCH STEAL — 2026-09-24

source: Perplexity blog "Photon: Building a Retrieval and Ranking Engine From Scratch" (via https://pplx.ai/hermes-fast-search → perplexity.ai/hub/blog/photon) + @NousResearch status 2103244070407802905 · steal doctrine: cite, adopt patterns, build nothing twice

## What dropped (09-24)

Nous: "Web search in Hermes Agent is now fast and free. @perplexity_ai built Fast Search for agents, and it is free for all Nous Portal tiers."

Underneath: **Photon**, Perplexity's in-house Rust retrieval+ranking engine. Replaced an open-source engine that ran out of headroom — RAM-hungry, mmap page-fault disease (p99 800ms, 1.2s spikes during index rotation). Photon is now the default across Perplexity's stack AND ships as a **PPLX Fast** preset on the Search API.

## The numbers (receipts, not vibes)

- Fast preset single-search-call latency: **160ms p50 / 230ms p95**. Production p99 retrieval+ranking: **800ms → 65ms**.
- Six agentic benchmarks (WideSearch, BrowseComp, DSQA, FRAMES, SEAL-0, SEAL-Hard), 3,554 tasks: fast preset **$59.73 vs $187.60 = 68% cheaper**, same aggregate quality (64.3% vs 64.0%).
- Trade-off named by Perplexity themselves: −0.24 DCG relevance, −3pp answer availability on long-tail queries. Their ruling: **agent reasoning compensates** — fast for day-to-day agentic, deep/default for hard or ambiguous.
- Built by "a small engineering team working alongside a swarm of persistent coding agents."

## Engineering patterns worth keeping

1. Posting lists pick representation by length/density: inline page / sorted offsets / bitmaps.
2. WAND-style bounded traversal — driving list + probe lists, admission threshold rises as good candidates accumulate.
3. **docblob**: one lookup per document for all ranking features; Elias-Fano gaps; decode only matched terms.
4. Lock-free batch-aware cache: no allocation on hit, no lock (version check + retry), CLOCK eviction, io_uring with per-thread rings and preregistered FDs/buffers.
5. Build fully separated from serving: single-digit-hour full builds, ~30min replica deploys, caches warmed by replaying search logs BEFORE routing live traffic.
6. mmap lesson: **when the working set exceeds RAM, mmap is a latency bomb** — explicit async reads beat transparent page cache. Measure the tail, not the mean (p50 lies, p99 tells truth).

## Estate decode

1. **Convergence receipt (FTS5 steal #7 confirmed at scale).** Perplexity spent a team-year proving compact LEXICAL structures (posting lists, Elias-Fano, WAND) beat fat in-memory/vector stacks on both cost and latency for agentic search. The Librarian's planned SQLite FTS5 organ (72k curated files, no embeddings) is on the same axis. Adopt: docblob idea (one-record-per-doc ranking blob) if FTS5 ever strains.
2. **Cheap-lane doctrine receipt.** 68% cost cut with flat aggregate quality because the loop reasons around thinner retrieval — don't buy premium inputs the agent can compensate for. This is frontier-from-Flash applied to search.
3. **Swarm-built receipt.** "Small team + swarm of persistent coding agents" built production infrastructure — the fleet doctrine validated at Perplexity scale.
4. **Free-lane war data point.** Platforms now bundle search free to win agent developers. Ride the provider war, own the loop.

## Actionable state (probed same hour)

- HERMES_API_KEY_1/_2 confirmed ALIVE on host .env: `inference-api.nousresearch.com/v1/models` → HTTP 200 in 0.5s, OpenRouter-style catalog (fireworks/ember-1 = Kimi K3 reasoning build, etc.).
- Still **zero lanes registered** (the 09-23 doubled-keys audit finding stands).
- The tweet's free-search perk rides the Portal subscription these keys belong to → rescue the orphaned lane AND inherit free fast search.
- GO-shaped next step (awaiting operator): register Nous lane in free_tier.py (accept both key names, the NVIDIA-mismatch lesson), probe for a search endpoint, test one real search chore, append receipt here.
