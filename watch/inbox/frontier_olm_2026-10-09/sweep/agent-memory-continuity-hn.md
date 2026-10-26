# FRONTIER SWEEP: agent-memory-continuity via HN - 2026-10-09

source-fetched: 2026-10-09. Door: Hacker News (hn.algolia.com API + news.ycombinator.com threads). Seat: sweep-agent-memory-continuity-hn.

## Method (what actually ran)

- Pass 1 broad sweep: 12 Algolia queries (`search_by_date` + 1 relevance `search`), all with `numericFilters=created_at_i>1788912000` (2026-09-09 cutoff): agent memory, LLM memory, CRDT, knowledge graph, memory consolidation (0 hits), context window, "long-term memory", event sourcing, agent memory (relevance), vector database, bitemporal, MemGPT/Letta (0 hits). Candidate pool: 38+ stories collected; ~20 with real memory-continuity relevance.
- Pass 2 deep reads (9 items fetched and read this session): HN 50018178 (thin; the arXiv abstract is the content), arXiv 2610.10845, HN 49963394 (Minigraf thread), the "five failure modes" Medium article (403 on WebFetch; recovered full text via the web-reader MCP fallback - fallback succeeded, not fabricated), Zep Konig blog (followed 301 to www.getzep.com), Polign/recall README, temporal.io Pi post, HN 49980399 (Durable Actors thread), chengyixu/context-freshness-ledger README, HN 49923466 (RIP vector database thread).
- Overlap greps: the Bash tool's shell has no coreutils on this host (grep/head/tr/mkdir all `command not found`; the first catalog "0 hits" pass was FALSE - grep never executed). Re-ran with `.venv/Scripts/python.exe` over catalog/catalog.jsonl (383,869,989 bytes) and memory/ (713,340 files scanned, <3MB each), single pass, phrase counts + hit paths captured in the session log.

## Headline catch (dedup saved waste)

The Galahad 50M-token-window work is ALREADY in our catalog: `catalog/catalog.jsonl` carries "Working Around the Compute Ceiling: Byte-Exact Memory in Galahad Makes LLM Reading a One-Time Cost", `age_days: 0` (match at byte offset 226600147). A sibling lane banked it today. It is therefore NOT in the top-8 below; the digest commit f676ee787's staged hermes fix plus this same-day catalog entry already cover that thread of Q3.

## The 8 banked items (strongest first)

### 1. Five failure modes around fact retirement in agent memory, with measurements
https://medium.com/@dat999zx/five-failure-modes-around-fact-retirement-in-agent-memory-with-measurements-55148df8b7e0 (HN 2026-09-28, id 49877124)
Quote: "Negations pass similarity thresholds: the retrieval index matches surface tokens; polarity is not a token the embedder respects."
Why it matters: the only MEASURED write-time correction protocol found. Five failure modes with counts: negations passing similarity (polarity-token guard + top-20 neighbor contradiction scan before write); writes contradicting a decision nobody retrieved (write-time contradiction scoring); batch contamination (44 of 120 add_memory calls mention commit-siblings unrelated to the fact, marked needs_review with ranking demotion); file-change staleness mostly noise (867 of 903 flags still held, so only flag on path-gone or symbol-signature-gone, 5% real); session read-set staleness (symbol://path#Name locators with hash, refuse-once-then-release, shadow mode until >=95% precision). Directly answers LENS-3 Q1: supersession is a write-time discipline, not just an edge type.
Overlap: "fact retirement" 0 hits catalog + memory. New.

### 2. Zep Konig: why we built a graph database service for agent memory
https://www.getzep.com/blog/why-we-built-a-graph-database-service-for-agent-memory/ (HN 2026-09-15, id 49712610)
Quote: "Truth and knowledge are separate timelines, and Konig natively tracks both."
Why: the frontier's canonical supersession mechanism is four timestamps per edge (valid-from/valid-at + recorded-at/invalid-at) instead of overwrite or supersession edges: "Konig marks the old fact invalid using an `invalid_at` date instead of overwriting it, so history is preserved"; point-in-time queries ("what did the agent know on date X") fall out of the data model. Per-subject small graphs (millions of tiny graphs, rendezvous hashing) is also a containment pattern for our orphan/island problem. Maps to the estate: knowledge_graph.json edges gaining invalid_at + observed_at beats growing superseded_by beyond 6.
Overlap: concept family known - catalog already holds "Zep: A Temporal Knowledge Graph Architecture for Agent Memory" (age_days 51, byte offset 97289562); "konig" catalog hits are Konigsberg.lean/KonigLemma.lean mathlib files (false positives); `invalid_at` appears once in memory/agent_sessions/orc-t07cf6a2b23.json (estate chats know the name, artifact is new).

### 3. Polign Recall: typed agent memory with corrections and history
https://github.com/Polign/recall (HN 2026-09-14, id 49701788)
Quote: "When a fact changes, the new value replaces the old one by a rule, not by a model's judgment."
Why: corrections as a SCHEMA feature: subject-predicate-typed-value triples, single-valued predicates supersede by rule, old values stay queryable with `as_of` time travel, forgetting = withdrawal not delete. Best schema-evolution answer found for LENS-3 Q4: the predicate registry evolves "without changing what the agent remembered before", and free-text facts that fit no predicate are kept as "notes" promotable later - exactly a landing pattern for the 1,066 orphan nodes (orphan = note awaiting a predicate, not garbage).
Overlap: "Polign" 0 catalog; memory hits are Gutenberg texts (pg448, pg75725 - false positives). New.

### 4. Show HN: Minigraf - an embedded, bi-temporal graph database in Rust (HN thread read end-to-end)
https://news.ycombinator.com/item?id=49963394 (2026-10-05, 41 pts / 31 comments)
Quote: "If my notebook took the form of a temporal multiverse of entities, I'd lose the ability to use it properly."
Why: bi-temporal indexes (transaction time + valid time native, not timestamp properties) answer "what was the exact state of the db on september 12th" as a query - supersession without an edge type; the thread's best counterpoint is that a "temporal multiverse" notebook becomes unusable, i.e. correction machinery has a UX cost, and "bitemporal does not mean 'including timestamps'" (LadybugDB maintainer debate). Thread did NOT discuss CRDTs or schema evolution - noted absence.
Overlap: "minigraf" 0/0; "bi-temporal" already appears in memory/working.md and agent session logs (concept known in-estate, artifact new).

### 5. Durable Actors - OSS Durable Objects with configurable compute (HN thread read end-to-end)
https://news.ycombinator.com/item?id=49980399 (2026-10-06, 50 pts / 25 comments)
Quote: "handles one request at a time and has its own SQLite database"
Why (Q2 knot-as-CRD verdict): the frontier's newest durable-state substrate pitches SINGLE-WRITER serialized execution as the feature for agentic coordination; in 25 comments CRDTs and multi-writer merge never came up once. The single-controller architecture law already picked the side the frontier converged on; knot-as-CRD is moot for correctness. The live frontier lesson is the state-queryability critique: actors force duplication into another DB unless "emitting versioned domain events transactionally with the actor state" - which is what our edges.jsonl/delta_index already are. Also the durable-state vs durable-execution distinction (Temporal = execution, DO/actors = state).
Overlap: "durable actor" 0/0. New.

### 6. The immortal life of Pi (running the Pi coding agent on Temporal)
https://temporal.io/blog/the-immortal-life-of-pi-running-the-pi-coding-agent-on-temporal (HN 2026-10-08, id 50011940)
Quote: "Agent harnesses keep arriving at Durable Execution by solving the failures they encounter."
Why (Q5, world-rib contract): independent convergence with the estate's rib/zknot/tape design: "the transcript is the conversation state"; claims written under `<session>.jsonl.pending/` BEFORE any tool runs; dead worker mid-effect records "outcome unknown" and the model inspects the world instead of blind-retrying; stale appends rejected by lease. This is our law census + rib boot contract in industrial form - evidence the world-rib contract is frontier-grade, not estate-internal weirdness.
Overlap: "immortal life" memory hits are Gutenberg book titles (false positives). New.

### 7. Context Freshness Ledger - a tiny schema for reviewable agent memory
https://github.com/chengyixu/context-freshness-ledger (HN 2026-09-16, id 49721941)
Quote: "a format for a reviewable record, not a compliance or security certification"
Why (Q5 verdict): the frontier's memory-taxonomy answer to "is this memory still usable" is five review-time fields (source, observed time, scope, proposed action, review decision = current/stale/needs-person) plus a `human_return` escalation block and a `review_by` deadline. It has NO supersession/correction mechanism at all - which supports the verdict that the law census and world-rib contract cannot be answered by a frontier taxonomy; they are estate-internal by construction. The `review_by` deadline is still stealable for law-census review cadence.
Overlap: "context freshness ledger" 0/0; "context freshness" in memory/workflows/REGISTRY.jsonl is our own B2-60 D2 judge-independence note - name coincidence, different artifact.

### 8. RIP, vector database (turbopuffer) - HN thread read end-to-end
https://news.ycombinator.com/item?id=49923466 (2026-10-01, 403 pts / 116 comments)
Quote: "Updating one vector can move hundreds of attributes and their indexes."
Why (Q3-adjacent): recall-layer architecture lesson - vector-primary keying causes massive write amplification; v3 demotes the ANN index to a secondary index over a stable internal doc ID (Postgres-vs-InnoDB index-pointing debate in thread). Analogous to our recall ceiling: key recall on stable fact IDs, hang indexes off them, never rebuild-the-world on one correction. Thread had no agent-memory discussion (checked).
Overlap: "turbopuffer" 18 catalog hits (vendor familiar to the estate, gapwave run files in memory/), "rip vector" 0 - the post is a new artifact.

## Research-question verdicts (grounded in the reads above)

1. Correction/supersession (LENS 3): frontier does NOT supersede via edges; it bi-temporally invalidates (Konig `invalid_at`, Minigraf t-time/v-time) or rule-replaces with queryable history (Polign), plus write-time contradiction guards (item 1). Our 6 superseded_by edges are the wrong axis to grow; timestamped facts + history queries scale.
2. Knot-as-CRD (LENS 2): moot for correctness - frontier durable-state converged on single-writer (item 5); the open frontier question is state queryability, which our edge fabric already answers.
3. L0d context-pack shedding / runaway recall: beyond the ported hermes fix, the literature offers KV-state persistence (Galahad - already in catalog age_days 0) and stable-ID recall indexing (item 8). Nothing found that beats the in-tree staged fix for the ceiling itself.
4. Orphan re-wiring (1,066 orphans / 454 islands): Polign's registry-evolution + notes-promotion pattern (item 3) and per-subject graph containment (item 2) are the candidate rewires. The invariant:law trailing-space id bug question is NOT answered here: I did not read that code this session, so whether it is the actual join blocker is unverified by this sweep - that needs an estate-side grep, not an HN read.
5. World-rib contract / law census: estate-internal by construction; frontier taxonomy stops at review-time snapshots (item 7), while durable execution (item 6) independently re-derives our transcript-as-state + claims-before-effects design.

## Degradations

- Medium article 403'd on WebFetch; full text recovered via the web-reader MCP tool (fallback succeeded - content quoted from that fetch).
- Zep blog 301'd to www.getzep.com; followed and read there.
- Bash-tool shell lacks coreutils on this host; greps re-run via `.venv/Scripts/python.exe` (first false-zero pass discarded).
- HN 50018178 thread is 1 comment, no debate; the arXiv abstract was read instead and is the substantive content.
