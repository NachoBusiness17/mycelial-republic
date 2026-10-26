# SWEEP: agent-memory-continuity via Hacker News

source-fetched: 2026-10-08
Seat: sweep-agent-memory-continuity-hn. Door: HN Algolia API (search_by_date + search), then news.ycombinator.com item threads. All quotes below are verbatim from pages fetched this session. ASCII only, no em dashes.

## Pass 1 (broad, this session)

Ten Algolia queries, all date-bounded `numericFilters=created_at_i>1788825600` (2026-09-08, i.e. the last 30 days) except the relevance door:

1. `"agent memory"` by date: 17 hits
2. `"LLM memory"` by date: 0 hits (nbHits 0, recorded as returned, not an error)
3. `"knowledge graph"` by date: 11 hits
4. `"context compaction"` by date: 3 hits
5. `embeddings search` by date: 8 hits
6. `"vector database"` by date: 9 hits
7. `"agent memory"` relevance (unbounded): 30 hits
8. `"event sourcing"` by date: 4 hits
9. `"append-only"` by date: 2 hits
10. `BM25` by date: 7 hits
(plus two extra families: `"memory consolidation"` 0 hits; `"context window" agent` 7 hits.)

In-window candidates considered: 49 distinct stories, 2026-09-08 through 2026-10-08. Strongest by engagement: "RIP, vector database" (402 pts / 116 comments, 10-01), "Launch HN: Magnitude" (194/99, 09-30), "Vespper Docx MCP" (38/18, 09-28). Magnitude and Vespper were considered and NOT deep-read (inference engine and doc MCP, off-area); they stay available for the next window.

## Pass 2 (deep reads, 10 items read end to end this session)

Each = the linked page fetched in full plus, where it existed, the HN thread fetched in full.

1. turbopuffer "RIP, vector database" (blog + 116-comment thread, id 49923466)
2. FutureOS "Context compaction, measured: FutureOS vs. Codex vs. OpenCode" (id 49795948)
3. Zep "Why we built a graph database service for agent memory" (Konig; followed blog.getzep.com 301 to www.getzep.com)
4. kolesnik.io "I made vector search the default. My agents did better with BM25" (id 49659803)
5. calpaterson "Agent memory as a file format" (blog + 96-comment thread, id 49508317; HN date 2026-08-31, 8 days before the window, reached via the relevance door)
6. motif-Labs/motif README (id 49877499)
7. Polign/recall README (id 49701788)
8. JayBase, which 308-redirects to aviansuite.com (id 49823815); redirected page fetched, product continues as AvianSuite on the open-source "Stellar Jay" append-only store
9. claix.dev "We Built an Alternative to Vector RAG for AI Agent Memory" (blog + 10-comment thread, id 49993820)
10. chengyixu/context-freshness-ledger README (id 49721941)

STRUCK, do not re-bank: item 9 (claix). The HN thread itself flags it: hnslop rates it 100% AI-generated, two commenters call it repetitive without an answer, esafak asks for benchmarks and none exist ("Measurements/benchmarks: None" per my read). Its one salvageable line (cmenge: agentic search "has pretty much become the default since LLMs became reasonably good at tool calling") is recorded here, not banked as an item.

## Readings against the five research questions

### Q1: cheapest instrument to promote isolated priors into verified edges (cite-allowlist as linker)

- PRO-graph witness (Zep Konig): facts are materialized as edges and every edge carries four timestamps (bi-temporal: world-truth and system-knowledge) plus an `extracted_from` provenance edge back to the source; contradictions set `invalid_at` rather than overwriting; edges are written through a per-graph WAL with monotonic sequence numbers and acked only when durable. Their diagnosis transfers: agent memory is "millions of smaller graphs, most cold at any moment", and their old general-purpose graph DB failed on workload fit, not on the graph model.
- COUNTER-witness (calpaterson memoryfields): deliberately NO linking at all; memory is a zip of Markdown pages with UUIDs and an optional deletable embedding cache; retrieval is a semantic jump in at most 2 tool calls; the essay rejects graph/hyperlink memory because traversal is slow, unreliable, noisy. HN thread adds the poisoning worry: one bad line contaminates everything downstream ("heresies" persist).
- Synthesis for the estate: the cheap linker is exactly what the ask guessed, with one Konig-sourced amendment. The P1 cite-allowlist gate already verifies whole-repo paths deterministically (port wave P1, commit 6685db6bc); promoting a knot/doctrine/steal node = appending edges whose `text` carries a gate-verifiable path:line cite, i.e. verification is path existence, not semantic judgment. The Konig amendment: an edge should also carry its provenance pointer and a validity marker, so a superseding lesson marks the old edge stale instead of deleting it. Counter-evidence to answer in the design note: calpaterson's traversal complaint does not bite because gate-verified edges are looked up by key, not walked.

### Q2: identity key for collision-free knot labels; does estate_query corr_id already carry it

- turbopuffer thread (benesch, turbopuffer): the new primary index is "an automatically generated internal ID: (segment ID, doc ID)"; the user-facing id "turns into a secondary index at the storage layer". That is the exact shape our knots need: identity = internal key (session id or content digest), human label demoted to a non-unique secondary attribute.
- Motif: sessions carry tool-prefixed ids (`claude-code:88b19192`, `codex:99bfccc0`), notes cite source sessions, exports use "a content-hashed manifest"; cross-project duplicates collapse into one knot behaviorally.
- memoryfields: per-record UUID in frontmatter, no dedup scheme beyond that.
- Estate answer this sweep can support: label is a display name, not a key. A composite key of (session id, digest) already exists in estate machinery: the estate_query corr_id join (AGENTS.md commands row) and the P3 tag-digest pinning (boot verify refuses digest mismatches) both prove the estate already treats digest+id, not name, as identity. What I did NOT verify this session: the actual knot-minting code path in knowledge_graph.json's writer; that check is owed to whoever builds the key change. None of today's reads contradicts the corr_id-based key.
- HN thread silence is itself a datapoint: neither big thread (116 and 96 comments) discusses memory-record dedup or identity keys substantively; this is unsolved-in-public, not just unsolved-here.

### Q3: build or retire the append-only LEDGER writer

- The ledger has been byte-frozen since 2026-10-07 08:09:26 local with max ts 2026-09-28T19:30:00Z (burns lens section 1, instrument-tagged). Three public reference designs read today:
  - Polign/recall: corrections are rule-based supersede, old values stay queryable via `as_of=`, forgetting records a withdrawal, never a delete; identity is subject+predicate within a namespace; single-writer enforced by AgentID + lease. This is amend-never-rewrite (RIB_MD_RECORD_20260921.md:6-26 via laws.md:33-34) as shipped code.
  - Stellar Jay / AvianSuite (ex-JayBase, 308 redirect verified live): append-only Go store, AGPL-3.0, "every change is kept, attributed and reversible"; reversal is a new record, not an edit.
  - Context Freshness Ledger: a record format forcing source, observed_at, scope, proposed_action, review_by/status/reason into one reviewable row; explicitly not a compliance mechanism; no identity hash.
- Build-or-retire read: the record supports BUILD. A minimal LEDGER writer is three invariants, all three witnessed in shipped public code today: append-only file + per-row monotonic ts (Konig WAL shape), correction = new row referencing the old row (Polign supersede / Stellar Jay reversal), and a reader that refuses unknown schema (P3 boot-verify analog). Retire would orphan the ledger's 705 rows mid-arc; nothing read today argues the instrument is wrong, only that it was never minted. The operator decision remains his, but the evidence now points one way.

### Q4: which memory writes violate their own read contracts; ReFold restore door as continuity primitive

- FutureOS measured post (page-dated 2026-08-04, HN-submitted 09-22): forced compaction, then a 178-question memory exam (8 decoys, zero decoy falls). Originals-first projection recalled 147/178 (83%), OpenCode summary+tail 47%, Codex (user text + whole-history summary, assistant text dropped) 38%. Load-bearing number: tool output is 96.1% of window characters but only ~10% of what follow-up questions reference; assistant+user text is 3.9% of volume but 90% of questions. Retrieval leg FAILED open-book: autonomous retrieval recovered nothing across five rounds (zero tool calls); forced tool use recovered 20/28 (93.3%) - "the gap is behavioural, not capability". Verbatim: "A cheap compaction isn't cheap if it drops what later turns need."
- Map to the estate: ReFold reversible sheds (sha-addressed stubs, restore door proved 4290 chars, port wave P5) is the same originals-stay-on-disk shape: compaction changes the projection, the shed holds the original. The FutureOS failure leg is the warning for our restore door: a restore mechanism the model must choose to invoke will not be invoked; continuity that matters must be inside the projection (deterministic evidence index), not behind a tool call. That is a design constraint on the day-6 write-time/use-time contract subject, not a violation finding: I did not audit zknot/warm_state/world_state write paths this session, so the question "which writes violate their own read contracts today" remains OWED; what today's reads add is the exam instrument (questions-only-answerable-from-memory after forced compaction) and the 83/47/38 ordering.

### Q5: name one job where embeddings beat keyed lookup, or retire the class

- Against embeddings-as-primary, three independent measurements today:
  - kolesnik.io (pond, agent session archive): 1,126 real search calls over 63 days, ~99% inside Claude Code; BM25 149/243 (61%) successful vs vector 323/883 (37%); same-query A/B 41 BM25 wins vs 20 vector wins (29 ties); latency 0.39s vs 0.99s. Hybrid/RRF "unnecessary complexity with too expensive a cost". Author removed embeddings from the default path.
  - turbopuffer v3: ANN demoted from storage primary key to secondary index; the fix is "don't key on the ANN address"; BM25 and attribute filters are co-primary workloads.
  - GPS-embed (estate, killed 10-07): string keys 100.0 vs embedding-kNN 99.05, McNemar p=0.5, 60x over latency budget. Consistent with both.
- For embeddings, the one surviving job class, from Konig's numbers: exact kNN via AVX-512 in low single-digit milliseconds and IVF ~0.95 recall scanning a few percent of the corpus - embeddings are fine as ONE index among many, as a similarity detector, not as the recall path. The estate already runs this shape: the P2 contamination tripwire scores embedding twin-pairs (gemma:2b 0.9167/0.8333). The memoryfields thread gives the boundary condition in both directions: "keyword lookup will completely fail if every memory is just a vector" (morelandjs) vs semantic jump finding related-but-unkeyed prose.
- Verdict input for the estate: retire embeddings from retrieval-primary everywhere (already done by the GPS-embed kill); keep exactly one job class - cross-surface semantic dedup over prose priors (the contamination/duplicate-law detector), where no shared key exists by definition. That is a narrowing, not a retirement.

## Overlap gate (run this session)

`git grep -il <phrase> -- catalog memory corpus` over tracked files for: turbopuffer, "RIP, vector", "context compaction", memoryfields, calpaterson, "agentic retrieval", "experience graph", Polign, JayBase, AvianSuite, "context-freshness", Konig, BM25, "vector RAG", KnowledgeGraph, knowledge_graph. Findings:

- "turbopuffer" hits are vendored SDK files only: catalog/catalog.jsonl:353997 (letta turbopuffer_embedder.py), :354121 (integration test), :354623 (mem0 turbopuffer.mdx). Not the v3 post. Genuinely new.
- "context compaction" hits are arXiv rows: corpus/papers/librarian_backfill_20260927.jsonl:123 (2605.23296 Parallel Context Compaction) and :131 (2606.22528 Governance Decay). Papers, not the FutureOS measurement. Proximate, not duplicate.
- "agentic retrieval" hit is an unrelated arXiv row (catalog/catalog.jsonl:444501, TRACE).
- Konig / Polign / memoryfields / calpaterson / JayBase / AvianSuite / context-freshness / "RIP, vector" / "experience graph": no estate holdings (Polign hits are Gutenberg texts pg448/pg75725; Konig hits are computing-history classics).

## Unbanked candidates left for the next window (listed, NOT read)

Ask HN "If embeddings are so powerful, why are they mostly used for retrieval?" (49685838, 2 comments); "Five failure modes around fact retirement in agent memory, with measurements" (49877124); DeepMem hybrid Vector+BM25+Time-Decay (49612293); Gobstopper compaction proxy (49944789); Slowave local adaptive memory (49702887); ChronoVec versioned vector DB (49610716); Magnitude (49911995, 194 pts, off-area).

## Receipt

- Instruments: 12 Algolia API fetches (2 returned zero hits, recorded as returned), 8 HN thread/page fetches, 10 linked pages fetched in full (Pass 2 list above), redirect handling live-verified (getzep 301, jaybase 308). One query string (`"LLM memory"`) returned nbHits 0; recorded as-is.
- Overlap: `git grep -il` commands run this session over catalog/memory/corpus; a first plain `grep -ril` pass over memory/ was killed after 4+ minutes without completing (too slow on this tree) and replaced by git grep over tracked files; untracked drafts are NOT covered by the overlap gate. That is a stated limit, not a clean pass.
- Dates in items: page-shown date where the page surfaced one (FutureOS 2026-08-04); otherwise the HN submission date from the Algolia listing fetched this session.
- Not done: no pytest, no estate tool runs beyond git grep; knot-minting code path not read; zknot/warm_state/world_state write-contract audit not started (Q4 partial).
