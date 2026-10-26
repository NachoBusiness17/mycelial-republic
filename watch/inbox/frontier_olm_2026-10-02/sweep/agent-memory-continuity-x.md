# SWEEP: agent-memory-continuity via X - 2026-10-02

source-fetched: 2026-10-02. Door: WebSearch with site:x.com queries, then single posts resolved through the fxtwitter door (https://api.fxtwitter.com/&lt;user&gt;/status/&lt;id&gt;, JSON, no login). Two supporting deep reads off leads found on X (arxiv abstract page, GitHub README). Area owner: sweep-agent-memory-continuity-x. Complement to the HN sibling (sweep/agent-memory-continuity-hn.md); no re-banks of its items.

## Door health

- 7/7 fxtwitter status fetches returned HTTP 200 with full tweet objects. One transient ECONNRESET on rohanpaul_ai (first try) succeeded on immediate retry. Zero 403s.
- x.com/i/article/&lt;id&gt; and x.com/i/trending/&lt;id&gt; URLs are NOT resolvable through the fxtwitter door (it needs a username); where a tweet only pointed at an article, I read the door's rendering of the tweet plus its article preview data and flagged the quote provenance.
- Search-door rate limits: the backend threw MCP 1302/429 errors on nearly every query and auto-retried; two queries never returned X results at all ("policy as code"/"rules as code" + agent enforcement; "new memory architecture paper arxiv October 2026"). Everything else eventually landed.

## Estate map this feeds

- RQ1 doctrine-to-code 0-edge class (757 doctrine/steal/knot nodes, 0 edges; lens/graph.md:31) + repair sketch (graph.md:35-37, fold() already walks sources).
- RQ2 MemCodex pointer-beats-inline 60.8 vs 55.4 (banked: catalog id 505dff60dbfc, state/arxiv/2026-10-01/2609.39765v1.txt; lens/burns.md:94).
- RQ3 degree-9 invariant:law hub bug + 814 ghost endpoints (lens/graph.md:37).
- RQ4 warm boot + verkle chain continuity surface (AGENTS.md warm boot; mag.hermes_warm_boot).
- RQ5 400 empty-summary knots (graph.md:35: "the chain holds the text; the graph holds the hash").

## Pass 1 (broad, 11 search queries, ~70 distinct candidates considered)

Queries: agent memory architecture LLM benchmark; agent memory knowledge graph retrieval; "agent memory" benchmark eval long-term; agent memory session handoff continuity successor; content-addressed memory merkle agent; CLAUDE.md AGENTS.md coding agent memory lessons enforcement; "long-term memory" agent announcement; mem0 OR letta OR zep OR supermemory; GraphMemix MemoraX; agents memory "every session" cross-session persistent; OpenAI Dots persistent memory reactions; Claude Code compaction memory continuity. Zero-hit queries recorded: policy-as-code (X results), October-arxiv.

Window filter instrument: X snowflake decode `(id>>22)+1288834974657` via the repo venv python; cutoff 2026-09-02. Honest count: ~70 candidates considered, 21 decode inside the last-30-day window. The search door skews evergreen: most surfaced posts are 2026-05 through 2026-08. In-window set: rohanpaul_dots 09-29, akshay_not_search 09-29, recap_sep30_codex 09-30, dots_trending 09-30, roundtable_10_projects 09-28, turingpost_graphmemix 09-28, dhravya_company_brain 09-26, aml_shared_eval 09-19, jev_typesafe 09-16, dankornas_zer0dex 09-13, av1_12000_sessions 09-09, dair_agent_zero_memory 09-02, memorax_graphmemix x2 09-02, dots cluster x6 09-30..10-02 (roundtable_dots_blueprint, monokern, heybrain, dots_vs_muse, agent_team_247, dots_trending_governed). The ask's "consider at least 30 from the last 30 days" was not reached by the door; 21 is the true in-window considered count.

## Pass 2 (deep reads, 7 items read end to end)

1. @akshay_pachaar status 2104938749679607902 + door rendering of linked article "Agent Memory Is Not a Search Problem" (2026-09-29, 233 bookmarks).
2. @AgentMemoryL status 2101312784688726331, Agent Memory Challenge 2026 Cycle 2 announcement (2026-09-19).
3. @MemoraX_AI status 2095038508331401668 GraphMemix launch (2026-09-02) + arxiv abstract https://arxiv.org/abs/2608.26983 (submitted 2026-08-27).
4. @rohanpaul_ai status 2105001158930817478, OpenAI Dots writeup (2026-09-29).
5. @Av1dlive status 2097639365644279857, the 12,000-session shared second-brain prompt (2026-09-09, 1,634 bookmarks).
6. @RoundtableSpace status 2104477459525906866, 10 open-source memory projects thread (2026-09-28, 509 bookmarks) - all 10 t.co links resolved.
7. github.com/vectorize-io/agent-memory-benchmark README (lead resolved from item 6).

## Findings per research question

### RQ1 doctrine-to-code linkage (757 nodes, 0 edges)

The X leg's answer is a typed context taxonomy plus a measured claim that arrangement beats retrieval. The akshay article (via door) walks four generations of agent memory (full history, summaries, embeddings, knowledge graphs), calls the semantic/episodic/procedural taxonomy "non-actionable", and instead fixes on six Zep/Graphiti context types: facts, entities, episodes, thread summaries, observations, user summaries, each with a first-class accessor (`client.graph.search(...)`, `client.thread.get_user_context(...)`). That is a schema where every node/edge kind is declared and queried through a named type instead of free-text search - the shape the estate's fold() would need to emit doctrine-to-module edges as a typed edge class rather than untyped strings. Its headline evidence: splitting a task across turns cost 15 models 39% accuracy across 200,000+ simulated conversations (door rendering; quote provenance flagged, not verified against the article body). The Dots writeup adds the governance half at product scale: "Actions that change anything follow built-in approval defaults, adjustable through Custom Rules" with an auto-review screening account-touching steps - doctrine attached to the runtime as configurable code, the same law-to-effect shape as the estate's workflow gate. The fuller build-time answer remains the HN sibling's OKF code_refs find; the X leg contributes the typed-edge vocabulary and the measurement argument for why the linkage layer is the lever: structure, not retrieval quality, moved accuracy.

### RQ2 retrieval comparisons vs pointer/BM25 baselines (MemCodex 60.8 vs 55.4)

No X-swept post-10-01 system publishes a pointer-vs-inline or pointer-vs-BM25 comparison that beats MemCodex 60.8 vs 55.4. What landed instead is the apparatus to run that comparison class:
- AMB (vectorize-io/agent-memory-benchmark, 128 stars): an open benchmark shipping "datasets, prompts, scoring logic, and results" where memory backends are CLI pluggable (`--memory bm25`, `--memory hindsight-cloud`). Its PrecisionMemBench metric is pointer-shaped: "the score is the fraction of cases whose returned belief-ID set satisfies every assertion" - scoring by belief-ID set, not by prose overlap. "AMB starts from accuracy because it's the hardest to fake, and tracks speed and token cost alongside it", retrieval time split from generation, ingestion time recorded. Numbers live at agentmemorybenchmark.ai and in external_results.json / results-manifest.json (not read; OWED).
- GraphMemix (arxiv 2608.26983, announced on X 09-02): organizes memory as query-aware evidence forests - "By organizing memory into a query-relevant subgraph, the method avoids substantial lifecycle cost and recovers low-similarity complementary evidence", explicitly against "naive embedding similarity matching that introduces incomplete and redundant context". Abstract is qualitative only: "a new Pareto frontier between accuracy and lifecycle cost", four multimodal benchmarks, 27 LVLMs. No numbers on the abstract page; full-paper tables unread (OWED).
- Agent Memory Challenge Cycle 2 (X post 09-19): shared eval across Textual, Coding, Multimodal tracks, "testing not just what agents store, but whether they retrieve current, useful evidence when it matters"; registration 2026-09-20 to 10-31, RMB 150,000 prize pool for open-source teams. The HN sibling already banked the leaderboard site (placeholder scores, Cycle 1 published 08-12); the X post adds the dates and prize, nothing score-bearing.

Verdict: MemCodex 60.8 vs 55.4 stands unchallenged in everything I read. The nearest new quantitative rival class is AMB's belief-ID-set metric, which is the right instrument shape for the estate to re-run pointer-vs-BM25 at its own scale.

### RQ3 ID-collision, slugification, dangling references

Thin on the X leg, two partial mechanisms: (a) Graphiti's entity/fact model does entity resolution at ingest with typed edges (facts reference entities as first-class nodes), keeping identity in one place instead of scattered slugs; (b) GraphMemix sidesteps global-slug uniqueness altogether - forests are query-conditioned subgraphs, so the collision surface shrinks with query scope instead of one merged namespace. No post read addressed slug generation schemes (matches the HN sibling's open sub-question; still OWED). The estate's content-slug law (slugify invariants with content, not prefix) has no frontier counter-proposal in this window.

### RQ4 verifiable-continuity instruments

- @Av1dlive (09-09): after "20 billion tokens and 12,000 sessions" the author published a ~10.5k-char prompt (invited readers to "steal the prompt") that turns any coding tool's agent into an LLM-maintained wiki (Agentic Stack, SecondBrain/ directory). The fetch tool could not reproduce the full 11k chars; its structured rendering lists the relevant mandate: "end-to-end continuity verification, and a concrete handoff", plus provenance preservation and "separating knowledge from authority" - which is the estate's own "model text can propose; only the switchboard authorizes effects" law reinvented by a random harness builder. This is a hand-rolled warm-boot-equivalent: the wiki IS the chain tip and the prompt's verification section is the recall test. 1,634 bookmarks says the demand is real.
- Dots convergence (rohanpaul 09-29): the shared product shape across OpenAI/Meta is "persistent identity, a computing environment of its own, entry to a user's accounts and applications, a memory of what matters to that person, and autonomy sufficient to act without continuous prompting"; Meta's Muse launched Sept 8 in a Muse Secure VM. Dots-specific memory governance: read-only "proactive research" while the user is away; mutating actions behind approval defaults. Trending-page pitch (i/trending, unresolvable through the door, snippet banked): "persistent, governed memory across sessions, tools, and agents. One agent can pick up where another left off."
- Nothing found measures successor recall of a chain tip specifically - no handoff auditor, no recall-of-debts instrument (HN sibling independently reported the same OWED). The estate's warm boot + verkle tip remains ahead of the public field on this leg.

### RQ5 surfacing content behind content-addressed hashes (400 empty-summary knots)

Thin. The AMB repo ships published numbers as files next to a manifest (external_results.json / results-manifest.json) - results as immutable artifacts with a manifest surface, the same keep-address-as-join-key pattern the HN sibling extracted from Motif/ctx. GraphMemix's forests keep evidence compact and human-queryable while the underlying multimodal assets stay addressed by the source system. No X post addressed hash-bare surfacing directly; the sibling's pattern (derived, rebuildable human surface carrying the address as a field; fail loud instead of inventing content) stands unchallenged.

## Overlap instrument (exact commands run)

- `grep -c MemCodex catalog/catalog.jsonl` = 1 (row 806443, the banked arxiv stub id 505dff60dbfc).
- Batch: `for t in <14 terms>; do grep -ilF "$t" catalog/catalog.jsonl; grep -rlFi "$t" memory/ watch/inbox/frontier_olm_2026-10-02/; done`. Counts: Graphiti catalog=1 / memory+frontierolm=21 (Graphiti estate-known); AgentMemoryL + agentmemoryleaderboard 0 / 9 (files: memory/runs/gapwave/agent_memory_challenge_2026.md, mickey17_v2 lanes, quote_audit concat, trajectory/steps.jsonl, sibling sweep/agent-memory-continuity-hn.md - challenge known, Cycle-2 X post new); GraphMemix 0 / 1; "GPT-6 Astra" 1 / 111 (Dots launch widely held - highest dup risk of the set); "20 billion tokens" 0 / 1; agentic-stack-desktop 0 / 1; agent-memory-benchmark 0 / 1; OpenViking 0 / 2; evidence forest 0 / 2; "context types" 0 / 1; hindsight catalog=1; memU catalog=1; cognee catalog=1. The single memory/ hit for the non-agent-memory items is in every case memory/trajectory/steps.jsonl (today's live step ledger, not a holding). Deep-read substance (six context types, belief-ID-set metric, Cycle-2 dates/prize, 12,000-session prompt) is in no holding grepped.

## Not banked, with reasons

- Heybrain/monokern/RoundtableSpace Dots hype posts (promo noise, no mechanism).
- x.com/i/article/2105940449441759384 "General long-horizon capability is a prerequisite for RSI" (10-02, on-topic for RQ4): /i/article unresolvable via door; search snippet only, not read end to end - left for the next seat with the door caveat.
- dair_ai "Agent Zero Memory" (09-02) and Turing Post GraphMemix repost (09-28): title-level only, not deep-read.
- mem0 "A Brain in a Git Repo"/GBrain (06-26) and "Second Brain and the Wall it Hits" (07-07): strongest RQ5 fits on the whole sweep but outside the 30-day window - considered, not banked.
- zer0dex dual-layer memory (09-13), Dhravya company brain (09-26), Jev/TypeSafe (09-16), Daily-recap Codex-harness (09-30): in-window, title-snippet only, not deep-read; banked as leads in this file's pass-1 list, not as items.
- All out-of-window evergreen cluster (harness anatomy, Cursor Merkle indexing, Walrus, ontology explainers): considered in pass 1, out of window.

## OWED

1. agentmemorybenchmark.ai leaderboard numbers + external_results.json (does any provider's pointer-mode beat 60.8?).
2. GraphMemix full-paper tables (2608.26983) - the only new-architecture quantitative claims in window.
3. Slug-generation schemes: zero X or HN coverage in this window; the estate's content-slug law has no external counterparty to steal from or beat.
4. A successor-recall instrument (recall chain tip + open debts) - neither door found one; warm boot + verkle appears to be ahead of the public field.
5. The RSI long-horizon article body (/i/article, needs a non-fxtwitter door).
