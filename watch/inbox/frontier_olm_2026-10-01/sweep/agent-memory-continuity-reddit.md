# sweep/agent-memory-continuity-reddit.md

source-fetched: 2026-10-01
Area: agent-memory-continuity · Door: reddit · Agent: sweep-agent-memory-continuity-reddit

## Door status (degraded, recorded per recipe)

The primary recipe door FAILED on every variant:

- `old.reddit.com/r/{LocalLLaMA,MachineLearning,LocalLLM,ollama}/top.json?t=month&limit=50` (WebFetch): all four returned only a "Welcome to Reddit" landing placeholder, zero posts.
- `www.reddit.com/r/LocalLLaMA/top.json` (WebFetch): HTTP 403 Blocked.
- `old.reddit.com` thread page via web_reader MCP: "whoa there, pardner!" network-policy block. `www.reddit.com` thread page via web_reader: "Please wait for verification".
- `r.jina.ai` proxy: 403. `redlib.catsarch.com` mirror: 429.

Working fallback doors (per the recipe's fallback clause, honestly degraded):

1. **WebSearch `site:reddit.com`** for discovery - works but throws intermittent 429s (roughly every other query).
2. **api.pullpush.io** (pushshift successor) for full-text reads - submission `?ids=` and `?subreddit=&q=&after=&before=` endpoints. Rate-limits hard: parallel calls 429 immediately, one call per 30-60s was reliable; after ~6 calls it locked up for 150s+.

Known holes in the fallback door: pullpush returned empty `data:[]` for 1w5l182, 1whlop5, 1w5w3xi, 1w03h1g, 1w0o56a (unreadable, therefore NOT banked even where titles looked strong); r/selfhosted 1wghnq7 ("Letta vs Mem0") is "[ Removed by moderator ]". Comment trees could not be read at all: every in-window candidate that had comments was removed, pullpush-empty, or out of window, so all deep reads below are OP-text end to end, no comment trees. Never verified: whether those pullpush-empty ids are deleted vs. just unindexed.

**Date-integrity caveat:** the pullpush fetcher (small model behind WebFetch) mislabeled created_utc twice (1wqv98w as "2026-06-05", 1wu345p as "2026-10-29"). All dates below are my own conversions from the raw epoch the fetch reported. Verified epochs: 1wqv98w=1790441236 (2026-09-26), 1wldl38=1789900363 (2026-09-20), 1wldz7u=1789901701 (2026-09-20), 1wu345p=1790769837 (2026-09-30), 1wu0miw=1790761355 (2026-09-30), 1wghnq7=2026-09-14, 1w0hztj=2026-08-28, 1vx97s4=2026-08-24, 1vw34ef=2026-08-23, 1v2c97j=2026-07-21, 1uy6yht=2026-07-17, 1uvhdcp=2026-07-13, 1uiuvzo=2026-07-01, 1ucg4cf=2026-06-22, 1u7y3ek=2026-06-17, 1u4o1jj=2026-06-16, 1ucf1zz=2026-06-25, 1uf8vbh=2026-06-28, 1sx1vju=2026-04-28, 1so9rvk=2026-04-18, 1sl7hh2=2026-04-14, 1s1jlnd=2026-03-23, 1tsemre=2026-05-31, 1tqaoio=2026-05-28, 1r8cnwq=2026-02-18, 1p5792k=2025-11-24.

## Pass 1 - candidate pool (37 in-window items considered)

From the `subreddit=AIMemory&after=1788220800&before=1790985600` window query (all fetched, most since removed): 1wu345p, 1wu0miw, 1wtzvba, 1wthklj, 1wth77t, 1wth4oy, 1wth4lg, 1wtgyol, 1wtgt5u, 1wtgp9n, 1wtgmkw, 1wtgkel, 1wtgf8x, 1wtg6hi, 1wtfyrh, 1wtfw8r, 1wtftvw, 1wtfsnq, 1wtflvi, 1wtfltw, 1wtfkor, 1wtfk19, 1wtfiqz, 1wtfiko, 1wtfh6i, 1wtfgp8, 1wtf8kl. That cluster is a same-day (early Sep) astroturf wave: 27 posts, nearly all "[removed]", score 1, 0-1 comments, titles all Hindsight-branded ("Memory Without Authority... with Hindsight", "Storing failed fixes in Hindsight taught my agent restraint", etc.). Source-quality caveat for any future Hindsight-heavy sweep: that subreddit's early-September memory "content" was a marketing flood, not practitioner signal.

Plus search/pullpush-verified in-window candidates: 1wqv98w, 1wldl38, 1wldz7u, 1wu0miw, 1wu345p, 1whlop5 (unreadable), 1w5w3xi (unreadable), 1w5l182 (unreadable), 1wghnq7 (removed), 1w0o56a (borderline, unreadable).

Considered and discarded as OUT of window (all date-verified above, kept here so the next seat never re-considers them): 1w0hztj Frona ontology memory, 1vx97s4 "what memory benchmarks are the best" (LoCoMo answer key "just awful"), 1vw34ef harness-vs-model, 1v2c97j procedural-vs-episodic memory, 1uy6yht wrong-abstraction debate, 1ucf1zz FERNme brain-like memory ("harmful recall" concept, explicit invalidation for facts vs decay for preferences), 1u7y3ek Claude Code Auto Memory internals (`~/.claude/projects/<project>/memory/` + MEMORY.md index, default-on since v2.1.59, `autoMemoryDirectory` config), 1u4o1jj memory rot, 1so9rvk "KGs are the wrong abstraction", 1shepc1 "why we ditched the KG approach", 1ux30vq reverse-engineering Cognee/Graphiti/Neo4j, 1v7ul0z Claude harness graph memory with "contradicts" edges + top-K dedup capping, 1s5dgq6 time-aware GraphRAG missing global entity dedup, 1s1jlnd LoCoMo/LongMemEval flaws (6.4% wrong answer key, judge accepts up to 63% wrong answers), 1sl7hh2 89.9% LoCoMo architecture post, 1tqaoio agent lifespan engineering, 1r8cnwq 8-system teardown (Graphiti: "bi-temporal edges, two-phase entity dedup with MinHash + LLM"), 1qw9hr4/1s2o9c6/1thyy3k/1u808ox Claude Code auto-memory internals threads.

## Pass 2 - deep reads (5 fetched end to end via pullpush)

### 1. 1wqv98w - "Giving Hermes Agent a long-term brain: What seeding Vectorize Hindsight actually looks like (84M tokens, 537 API calls, $0.85)" - r/hermesagent, 2026-09-26, score 1, 0 comments

Verbatim opening: "Like many people running agent workflows with Hermes, I hit the infamous wall with flat markdown". Content: seeded Cloudflare Vectorize via the Hindsight memory plugin from flat markdown; the seeding run on DeepSeek Flash took ~2 hours, 537 API calls, ~84M tokens, $0.85, and produced 275 memories, 17 documents, 7.2k links; resulting graph splits into World / Experience / Observation units connected mostly by temporal and semantic links; author cut over to a local tiered setup (38B model with Ollama fallback); explicitly prefers memory lifecycle states (valid / invalidated-with-reasons) over letting conflicting stale notes coexist.

Estate mapping: this is RQ1+RQ3 in one post, on a Hermes-shaped agent. The World/Experience/Observation trio maps onto rib (world law) / residual (experience) / registry (observation) far more cleanly than any other structure found this window. The valid/invalidated-with-reasons lifecycle states ARE the caches-auto-invalidate law as implemented by someone else, and the $0.85/84M-token seeding receipt is the exact shape of a hermes_burn ledger row. The flat-markdown wall it opens with is the AGENTS.md-clippy-bloat disease.

Overlap grep: `rg -i -n "hindsight|mnemosyne|honcho|shodh|soul\.md|vectorize" catalog/catalog.jsonl memory/` (xml/html excluded) -> zero hits. "hermes" appears 980x in catalog.jsonl but nothing on Vectorize/Hindsight seeding. NEW.

### 2. 1wu345p - "Mnemosyne vs mem0 / Honcho / Hindsight for a local-first personal agent: what are you actually running?" - r/AIMemory, 2026-09-30, score 1, 0 comments

Verbatim: "I want memory for one long-lived personal agent that runs on my own hardware. Right now that's Mnemosyne (SQLite, local, cheap on tokens)." The poster's two open questions are verbatim our open questions: (a) does an open-source toolkit exist for memory management - "inspecting, correcting, deduplicating, expiring stale facts, and visualizing memory as a graph", ideally across backends (that is the lens/graph.md repair problem and the caches-auto-invalidate law stated as a user demand, with zero market answer); (b) best practice for facts that change: "supersede, delete, or keep both versions with timestamps" (bitemporality = chain-is-truth for memory records). Names the candidate stack: Mnemosyne (SQLite, local, token-cheap, recall inconsistent, hard to inspect), Honcho, Hindsight, mem0/OpenMemory, Graphiti, Cognee, shodh-memory.

Estate mapping: candidate material for knowledge_graph.v2 repair tooling survey and for the laws record group. The estate's own answer (registry + residual with epochs, corpus FTS, verkle chain) is further along than anything this thread surfaces - the steal is the demand framing, not the tools.

Overlap grep: mnemosyne/honcho/shodh zero hits in catalog+memory; mem0 present only as AgentOps instrumentation code (catalog ids 342357-342360, `mine/raw/agent_bleeding_edge/AgentOps-AI/agentops/agentops/instrumentation/providers/mem0/*`) and one fold chunk titled "steal-mem0-addonly-verkle-20260812" (catalog line 335175) - instrumentation facet, not this comparison. NEW as comparison.

### 3. 1wldl38 - "If your Hermes Agent feels generic or forgetful, ask it this exact prompt" - r/hermesagent, 2026-09-20, score 1, 0 comments

Verbatim: "It will break down the exact roles of SOUL.md, AGENTS.md, USER.md, and MEMORY.md so you know precisely what to configure." Content: a copy-paste self-audit prompt that makes the agent act as "critical auditor" of its own memory files across four dimensions: (1) bottlenecks/friction (rigid guardrails, redundant directives, repetitive meta-commentary), (2) accuracy/alignment (stated workflows vs actual projects, outdated assumptions, conflicting instructions), (3) conciseness/token efficiency (bloat, duplicates, over-specified rules wasting the context window), (4) concrete edits (delete/rewrite/add per section), then produce a clean revised version.

Estate mapping: the Hermes file quartet is a coarse rib/residual/registry split (persona-law / law / user-model / memory index). The self-audit prompt is directly stealable as a `mag.cmd` command (dogfoodable on AGENTS.md the same way - the clippy bullet IS our bloat surface and census_drift_patrol already guards its grammar). This is a cheap, local, premium-judgment-free version of "refresh the doc with today's truth".

Overlap grep: SOUL.md zero hits; the file-quartet audit pattern not in evidence. NEW.

### 4. 1wldz7u - "I built an open-source local agent experiment with Ollama to explore what sits between 'chat' and actual everyday work" - r/ollama, 2026-09-20, score 1, 0 comments (WEAK)

Verbatim: "Like a lot of people here, I've been experimenting with running models locally through Ollama." Athena (github.com/theo79/Athena): modular Python local agent - agent loop + tool execution, local doc ingestion, memory, web access, permission guardrails, optional Gemini/OpenRouter cloud backends. Author explicitly says not production-ready. No memory architecture detail in the post body.

Estate mapping: r/ollama lane stays shallow this window; nothing here the estate has not already built deeper (janitors + biographer + orchestrator). Banked as breadth only.

Overlap grep: `rg -i -n "theo79|athena" catalog/catalog.jsonl` -> zero hits. NEW (trivially).

### 5. 1wu0miw - "Anyone genuinely using the memory layer and thinks it's worth it?" - r/AIMemory, 2026-09-30, score 1, 0 comments (DEMAND SIGNAL, not substance)

Verbatim (the entire post body): "Are you getting value for adding the memory layer? And if yes what sort of use cases are these?" Zero answers. Two days old at fetch time.

Estate mapping: weak evidence that the memory-layer hype cycle is ahead of demonstrated value - consistent with the estate's falsifier law (descent spend theater) and worth one line in the laws record group: nobody in-thread could name a use case, which is the same "memory wrote nothing the next seat needed" failure our rib system exists to prevent.

Overlap: generic, no distinct overlap check possible beyond the names above. NEW.

## Not banked, not read, on the record

1w5l182 (stale-fact decision logs), 1whlop5 ("I don't think AI agents have a memory problem"), 1w5w3xi (stress-test-my-memory-system) - pullpush `data:[]` on every attempt; 1wghnq7 moderator-removed. These four titles were the strongest remaining in-window matches for RQ3/RQ4; they are OWED content, not findings. Out-of-window thread read anyway: 1r8cnwq (2026-02-18, eight-system teardown - full architecture table, best single RQ4 pointer: Graphiti's "two-phase entity dedup with MinHash + LLM"; excluded from items because it is 7 months stale).

## Answer sketch for the four research questions

1. **Cross-session structures -> rib/residual/registry/leaf:** the closest public analog found is Hermes Agent's file quartet (SOUL/AGENTS/USER/MEMORY.md) plus Hindsight's World/Experience/Observation graph units (1wldl38, 1wqv98w). Claude Code's auto-memory (index file MEMORY.md + topic files loaded on demand, per-project directory) is the same registry/leaf split but its threads are Jun 2026, out of window.
2. **Relational memory eval:** nothing new IN window. The eval debate (LoCoMo/LongMemEval answer-key rot, judge reliability) peaked Mar-Aug 2026 (1s1jlnd, 1vx97s4). OWED: an in-window eval thread.
3. **Write policies (keep/compact/invalidate):** the window's one strong signal is 1wqv98w's explicit valid/invalidated-with-reasons lifecycle states over silent contradiction, plus 1wu345p's supersede-vs-delete-vs-keep-both question still unanswered by the market.
4. **Entity resolution for KG collapse:** nothing in window; best public mechanism on record remains Graphiti's two-phase MinHash + LLM dedup (1r8cnwq, Feb 2026, out of window) - if knowledge_graph.v2 wants one prior art pointer, that is it, with the age caveat.

## Method note

Every quote above was copied from pullpush JSON fetched in this session; every date is my own conversion of the reported epoch; every overlap line names the exact `rg` run. The 30-candidate bar is met by the in-window pool (37 listed), the 5-deep-read bar met by items 1-5. No comment trees were readable; no fabricated fallbacks.
