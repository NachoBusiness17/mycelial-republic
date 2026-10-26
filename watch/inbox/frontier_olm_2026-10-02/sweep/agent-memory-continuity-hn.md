# SWEEP: agent-memory-continuity via HN - 2026-10-02

source-fetched: 2026-10-02. Door: Hacker News (Algolia API + news.ycombinator.com item pages). No 403s, no degraded door; every fetch below returned live content. Area owner: sweep-agent-memory-continuity-hn.

## Estate map this feeds

- RQ1 doctrine-to-code 0-edge class: watch/inbox/frontier_olm_2026-10-02/lens/graph.md:31 (757 doctrine/steal/knot nodes, 0 edges; "the graph records that laws and steals EXIST but never WHICH code they bind"), repair sketch at graph.md:35-37.
- RQ3 slug/collision/ghost class: graph.md:37 ("Slugify invariants with content, not prefix"; node-ify endpoints so ghosts go to zero).
- RQ2 pointer-beats-inline baseline: MemCodex 60.8 vs 55.4 (ask-provided).
- RQ4 continuity surface: warm boot (the mag.hermes_warm_boot module warm boot, AGENTS.md) + verkle chain tip.
- RQ5 400 empty-summary knots: graph.md repair sketch line 35.
- localfirst memory-project dig line already holds RAG-OS/AIDA/Atlas/LBrain/OwnMem/PAM/ragos (lens/burns.md:135-136); this sweep is the HN complement.

## Pass 1 (broad, 16 Algolia queries, ~55 distinct candidates in window created_at_i>1788307200 = since 2026-09-02)

Queries with hits: agent memory, LLM memory, knowledge graph, context engineering, Merkle tree, verkle, BM25, "memory layer", "episodic memory", memory benchmark agent, provenance, agent memory (relevance endpoint). Queries with ZERO story hits in window (negative result, recorded): "content addressable", "policy as code", "decision records"/"rules as code"/"executable spec", "content addressed", "chain tip"/checkpoint/session, "longmemeval"/"locomo". Interpretation: benchmark names and storage-theory terms never reach HN story headlines; they ride inside Show HN bodies and comment benchmarks.

Candidates considered (objectIDs, deduped across queries): 49931998, 49930166, 49929869, 49923182, 49911995, 49910148, 49892642, 49887024, 49884835, 49882129, 49878337, 49877752, 49877747, 49877499, 49877124, 49868130, 49866732, 49861765, 49856149, 49850669, 49840484, 49830214, 49828496, 49825414, 49819932, 49816163, 49807330, 49791877, 49784859, 49754725, 49768617, 49766795, 49762956, 49759013, 49757975, 49749689, 49749724, 49745176, 49749997, 49740741, 49740304, 49737804, 49730388, 49727859, 49721941, 49721129, 49715809, 49715402, 49713789, 49713894, 49712610, 49703919, 49702887, 49701788, 49698184, 49698073, 49696306, 49689904, 49689454, 49688290, 49687558, 49685838, 49684835, 49659803, 49647883, 49631258, 49628820, 49624196, 49624134, 49617529, 49613632, 49612293, 49609821, 49596543, 49595246, 49594849, 49593006, 49581240, 49560290, 49559069, 49556502, 49556719, 49552053, 49550931, 49535102. That is 30+ distinct items, well over the ask's bar.

## Pass 2 (deep reads, 11 items read end to end)

1. OKF Agent Memory repo + HN thread (81 pts, 32 comments): https://github.com/okf-memory/okf-agent-memory, https://news.ycombinator.com/item?id=49581240
2. ctx (git blame returning agent transcript) page + thread: https://ctx.rs/pro/, https://news.ycombinator.com/item?id=49727859
3. kolesnik.io BM25-vs-vector post + thread (0 comments): https://kolesnik.io/blog/my-agents-did-better-with-bm25
4. Awareness-Market repo: https://github.com/everest-an/Awareness-Market
5. Motif repo + thread (0 comments): https://github.com/motif-Labs/motif
6. past.dev BEAM 10M post: https://past.dev/blog/introducing-past-dev
7. Context Freshness Ledger repo + thread (0 comments): https://github.com/chengyixu/context-freshness-ledger
8. Repligraphs essay: https://lukechampine.com/repligraphs/
9. DeepMem repo: https://github.com/deepmemteam/deepmem
10. Agent Memory Leaderboard: https://agentmemoryleaderboard.ai/
11. Magnitude Launch HN thread (194 pts, 97 comments): https://news.ycombinator.com/item?id=49911995

## Findings per research question

### RQ1 doctrine-to-code linkage (757 nodes, 0 edges)

OKF Agent Memory is the direct frontier answer and the strongest bank of the day. Google's OKF v0.2 format carries a code_refs field for code-to-knowledge binding at record level, plus trust tiers separating "authoritative human law" from agent-generated drafts, provenance sources, lifecycle (status, stale_after), a 4-tier scope hierarchy (project>vendor>user>system, priorities 100/70/50/10) where upper layers strictly shadow identical concept IDs below, okf.lock pinning external bundles, and "okf validate knowledge --strict --drift" checking bundle conformance, graph connectivity, and description drift (~4ms). That is exactly the estate's missing edge class: law records that name the code they bind, validated at build time by a strict mode, and disambiguated by scoped shadowing instead of prefix slugs. The estate's mag/knowledge_graph.py fold() already walks sources per family rows (graph.md:36), so emitting doctrine-to-module edges at fold time plus a code_refs-style field is a direct steal.
ctx is the second half of the same answer from the other direction: code-to-origin linkage. ctx blame maps a line range to the agent session that produced the commit "with exact citations back to the original transcript and recorded tool calls", and grades evidence: it "distinguishes production evidence from review activity, and proven links from possible, conflicting, or missing evidence". The estate's knot nodes that hold a hash but no summary (RQ5) are exactly its "possible/missing evidence" tier. Motif adds the maintenance leg: "a note whose source files were reworked without it is marked possibly stale" and goes to a Review inbox; rulings never delete, they supersede, and confidence decays "with conflict, staleness and age".

### RQ2 retrieval comparisons vs pointer/BM25 baselines (MemCodex 60.8 vs 55.4)

No post-10-01 system publishes a pointer-vs-inline comparison, and nothing found beats the MemCodex pointer-beats-inline result on its own terms (no pointer-based baseline appears in any read page). Three independent corroborations of the underlying direction landed instead:
- kolesnik.io, 63-day production numbers on 1,126 historical searches: BM25 149/243 (61%) vs vector 323/883 (37%) success; 90-query head-to-head 41 wins vs 20 (29 ties); BM25 0.39s vs vector 0.99s mean latency. Core sentence: "for such a broad scope as agentic sessions it appeared to be an unnecessary complexity with too expensive a cost for the value it was bringing".
- HN comment by vshulcz on the OKF thread: 19k-session LongMemEval cross-tool run, "on the standard 500-session LongMemEval-S the same BM25 gets ~85% hit@1", "BM25 basically ties embeddings here at 1/100th the cost".
- Awareness-Market self-reports LongMemEval_S Recall@5 96.0 with a published ablation: vector-only 92.6, BM25-only 91.4, hybrid 95.6 (headline 96.0 vs ablation 95.6 is a small internal inconsistency I saw and am reporting). No Mem0 or pointer baseline; leaderboard rows mix QA accuracy with Recall@5, a caveat the README partially concedes. Credibility dents: self-reported, future-dated artifact string "2026-04 harness run" inside an October repo.
- past.dev (posted 10-01, the only true post-10-01 architecture in the set) claims 85.03% on BEAM 10M vs next published 68.0 (Exabase M-1), "Across a hundredfold increase in history it loses 7.05 points", with per-reader identity, dated documents returning "verbatim excerpts and source IDs", queryTimestamp time-travel reads, and deletion of derived memory. All vendor-published baselines, self-run harness; not a controlled comparison.
DeepMem (Vector+BM25+Time-Decay) publishes latency only (p50 73ms self-hosted; vs Mem0 cloud 643 vs 653ms) with no BM25/vector ablations and no LongMemEval/LoCoMo rows: considered, not banked, because its comparison class is empty. agentmemoryleaderboard.ai: three tracks (Textual/Coding/Multimodal), Cycle 1 published 2026-08-12 with no visible scores, Cycle 2 mid-Nov 2026; page read, placeholders only.

### RQ3 ID-collision, slugification, dangling references

Three mechanisms to steal: (a) OKF scoped shadowing (strict override of identical concept IDs across a 4-tier scope stack) replaces fragile slug uniqueness with deterministic precedence; (b) OKF --strict --drift validation turns ghost endpoints into a build-time failure, the estate's 814-ghost-endpoint class; (c) Motif's possibly-stale marking on source-file rework is a dangling-reference detector for artifact-to-artifact edges. None of the three publishes a slugification scheme specifically; that sub-question stays open (OWED: no page read addressed slug generation).

### RQ4 verifiable-continuity instruments

Context Freshness Ledger (3 commits, 2 stars, tiny) is the closest direct hit: a JSON schema for reviewable freshness decisions with record_id, source.{kind,reference,observed_at}, scope, proposed_action, freshness.{review_by,status,reason}, human_return.{required,reason}; it "does not access accounts, call tools, send messages, infer permissions, or authorize an external action" and is "a format for a reviewable record, not a compliance or security certification". Human-gated, passive; weaker than warm boot + verkle tip, which is machine-checked. Repligraphs is the verification-theory complement: authorship proof by deterministic re-execution of "profiles, context, filesystem tree, transcript" with a manifest (version, model, inference, environment, initial_context, seed, temperature); verification fails when the model is quantized ("a lab that quantizes its model will find old repligraphs fail verification"), which rhymes with the estate's DELIBERATE-ASK quantize-target law. Nothing found measures successor recall of a chain tip specifically; the nearest published instruments are memory benchmarks (BEAM, LongMemEval), not handoff auditors. OWED: no successor-recall instrument found in this window.

### RQ5 surfacing content behind content-addressed hashes (400 empty-summary knots)

Direct hits are thin (the "content addressed" query returned zero HN stories in window). Partial answers read: Motif exports "a content-hashed manifest" while keeping human-readable notes alongside; ctx surfaces hash-addressed git objects through a derived attribution index built locally ("Missing local Git objects or ambiguous repository identity" degrade it honestly, and "ctx says it cannot prove the attribution" rather than guessing); Repligraphs binds identity by re-execution rather than by storage address; past.dev returns verbatim excerpts plus source IDs so the reader never consumes the hash bare. Pattern worth stealing: keep the immutable address as the join key, but require a derived, rebuildable human surface (index, manifest, excerpt) that carries the address as a field, and fail loud (cannot-prove) instead of inventing content. That maps 1:1 onto the graph.md repair line "the chain holds the text; the graph holds the hash".

## Overlap instrument (exact commands run)

- grep -icF "<phrase>" catalog/catalog.jsonl over 871,790 rows: 0 for okf-agent-memory, OKF Agent Memory, Git-native persistent memory, Agent Action Grammar, ctx blame, kolesnik, did better with BM25, Awareness-Market, awareness local, motif-labs, coding-agent history into a knowledge graph, past.dev, BEAM 10M, context-freshness-ledger, freshness ledger, repligraph, lukechampine, DeepMem, agentmemoryleaderboard, SelMem, Jev-Mem. LongMemEval: 10 catalog rows (benchmark itself estate-known). Magnitude: 6 catalog rows (generic-word noise, not banked).
- grep -rilF "<phrase>" memory/: every banked candidate phrase hits exactly one file, memory/trajectory/steps.jsonl, the sibling sweep's step ledger from today; title-known only. Deep-read substance (ablation tables, schema fields, evidence-grade semantics, thread benchmark comments) is not in any holding grepped. One transient grep error on memory/biography/knots/2026-08-18_0040_mag_mag-agen_aac4e52c.knot.json (file vanished mid-scan; moving-tree churn, matches the known knot-regeneration behavior).

## Not banked, with reasons

DeepMem (no comparison class), Agent Memory Leaderboard (placeholder scores), Magnitude (inference-engine throughput thread; KV quantization and RULER retrieval benchmark noted but off-area), SelMem/Jev-Mem/IngotDB/Recalld/Backpass/Slowave/Funes (titles swept, not deep-read; several are 1-2 point items), Merkle-tree-certificates PQ CA (immutability-adjacent, not memory), CUDA-verkle (GPU MSM, no memory-continuity content), Five failure modes around fact retirement (49877124, strong title for RQ3/RQ4, NOT read: left for the next seat rather than banked unread).
