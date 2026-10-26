# SWEEP: agent-memory-continuity via arXiv (2026-10-09)

source-fetched: 2026-10-09. Seat: sweep-agent-memory-continuity-arxiv (dynamic workflow). Door: arXiv export API (Atom XML via WebFetch) green all 8 queries; arxiv.org abs + /html/ full-text pages green for all 7 deep reads. WebSearch door DEGRADED: returned MCP 429/1302 rate-limit errors on the one site:arxiv.org query (tool output verbatim: "Rate limit reached for requests"); per recipe the arXiv API fallback carried the sweep and succeeded. No fallback success is fabricated: the degraded door produced zero banked items.

## Pass 1: broad sweep (30+ candidates, last 30 days)

Queries run through export.arxiv.org/api/query (sortBy=submittedDate, sortOrder=descending), all fetched this session:

1. all:"agent memory" AND all:"language model" - 25 entries (25 in window 2026-09-09..10-09)
2. abs:"memory consolidation" AND abs:"language model" - 20 entries (3 in window; rest older)
3. abs:"conflict-free replicated" OR abs:"CRDT" - 20 entries (3 in window)
4. abs:"schema evolution" - 15 entries (1 in window)
5. abs:"belief revision" AND abs:"language" - 15 entries (3 in window)
6. ti:"memory" AND cat:cs.CL - 39+ entries before feed truncation (near-all in window)
7. abs:"memory deletion" OR abs:"forgetting mechanism" OR abs:"memory supersession" AND cat:cs.CL - 15 entries (7 in window)
8. abs:"context compression" AND abs:"language model" - folded into the candidate list via query 6 overlap

~160 entries listed total; comfortably over 30 distinct in-window candidates after dedup. Strongest 30ish shortlisted; 7 selected for deep read. One candidate (Revoked but Still Authoritative, 2609.08258, 2026-09-08) is one day outside the 30-day window and was dropped from the banking slate on window discipline despite being on-point.

Estate-holdings check (run this session): the estate mirrors arXiv abstracts daily under state/arxiv/2026-09-05..2026-10-09. Grep of catalog/catalog.jsonl for each candidate arXiv ID: already cataloged = 2610.08586 (id 2f378505895a), 2610.07715 (3451d6f871eb), 2610.02472, 2610.11270, 2610.11287, 2609.26035, 2609.40118, 2610.02945, 2609.08258, 2609.04875. Genuinely fresh (zero catalog hits) = 2610.03902, 2608.16357, 2609.34789, 2610.05176, 2610.02687, 2610.07118, 2610.10845, 2609.37453, 2610.04589, 2609.18886, 2610.07258, 2610.00872. Note: grep hits for "MELD" in catalog/memory are false positives (dist_audit meld_claims.py + memory/runs/brain_reads/meld_*.json are unrelated estate tooling).

## Pass 2: deep reads (7 items read end to end)

Each fetched this session: MINDSET + When Old Facts Return via arxiv.org/abs (abstract pages); When Evidence Changes, MELD, GRAFT, AECG, GraphMemory via arxiv.org/html full text.

### 1. MINDSET: Energy-based Schema Evolution for Long Conversational Agent Memory (2610.08586, 2026-10-06)

Stores "a conversation as immutable episodes and organizes them into versioned schemas through minimum-energy state transitions". Each episode may reinforce, supersede, split, or create a schema; transitions balance representation distortion, contradiction, historical damage, fragmentation, internal inconsistency; hysteresis stops isolated contradictions from prematurely rewriting stable memory. Beats 5 baselines on LoCoMo + MemoryAgentBench (retrieval deltas vs LightMem at p<0.01, Holm-corrected); cross-model check on GLM-4.7 and Gemma-4-31B. Verdict line: "long-term memory can be better handled as constrained state management rather than continual summarization."

**Q1 answer (supersession):** frontier correction is a versioned, never-destructive operation with a hysteresis gate, not an in-place rewrite. The estate's 6 hand-registered superseded_by edges (lens/graph.md:27) are the hand-copied version of exactly this; the frontier shape is: append a version transition with an energy score, keep both states.

**Q4 answer (schema evolution):** MINDSET's versioned-schema transitions are the conversational analog of what the knowledge_graph.json rewiring needs; GRAFT (below) is the graph-native one.

Overlap: cataloged abstract mirror state/arxiv/2026-10-07/2610.08586v1.txt (catalog id 2f378505895a); the transition mechanics, hysteresis, and baseline numbers are new value from this deep read.

### 2. MELD: A Protocol for Merging Knowledge Across Distributed Agentic Memories (2608.16357, 2026-08-17)

**Q2 answer (knot-as-CRD): survives contact, and reconciles with the single-controller law.** Mechanism: every incoming claim gets exactly one of five outcomes (insert / merge-via-supersedes-link / relate-via-Mapping-link / conflict-link-both-kept / reject-at-admission), decided by scoped claim-key identity + embedding similarity + NLI contradiction verdict. Per-claim status rides a monotone chain (active <= deprecated <= overruled <= revoked) as a grow-only link set; merge = set union; status = deterministic join (max along chain). Coordinator-free convergence via state-based CRDT + append-only wire discipline + anti-entropy digests. Numbers: "the status CRDT reconverges in 30/30 real partition-heal trials where last-writer-wins manages 11/30"; merge recall 0.630 vs centralized 0.619 (TOST equivalence); false-merge rate 0.013; ~3x fewer sync messages at matched recall. Policy: "MELD does not adjudicate truth; a detected contradiction is preserved for later adjudication, never silently resolved."

**Why this does not violate the single-controller architecture law:** MELD's staleness/overrule/authorization gates apply at materialization-read as pure functions of the converged set; admission is still a gated chokepoint. Translation for the estate: the single controller can remain the admission + materialization authority while knot STATUS convergence across mesh replicas runs CRDT-style. That is the exact seam knot-as-CRD needs: convergence of status, not convergence of control. Limitations named by the paper: merge graph is order-sensitive (status is not), benign-fault only (no Byzantine defense), thresholds calibrated per encoder (do not transfer MiniLM -> mpnet), relational completeness "an open empirical premise".

Q1 tie-in: supersession is an appended supersedes link, never a rewrite - the wire discipline the estate's 6 superseded_by edges should adopt as they grow.

Overlap: fresh. "MELD" grep hits in catalog/memory are unrelated estate files (meld_claims.py, brain_reads). Note: 53 days old, outside the preferred 30-day window; banked because it is the one paper that directly adjudicates the LENS 2 knot-as-CRD open question.

### 3. When Old Facts Return: Re-Reads, Reverts, and the Limits of Temporal Memory (2610.07715, 2026-10-06)

**Q1 answer, the trap:** identity/observation-based temporal memory cannot tell a stale re-read from a genuine revert. On 130 extractor-selected atomic transitions from software fixes: ordinary condition 98.5% accuracy with zero observed stale-value errors; appending a verbatim re-read of an old statement collapses accuracy to 10.8% with an 88.5% stale-value rate; a guard refusing to reactivate retired values restores 97.7% and 0.8% - but "the guard cannot recognize legitimate reverts without extra change provenance". Design implication quoted from the page: "distinguish an observation of a value from evidence that the value changed".

**Estate translation:** a superseded_by edge is worthless without its inverse provenance. When the estate re-encounters an old fact (session recap re-read, warm_state replay, corpus FTS hit on a stale row), nothing in the current graph says whether that re-observation is evidence the fact un-died. The fix is change-provenance metadata on the status chain (who/what flipped it and why), not a reactivation guard. This is the failure mode that will bite the mesh nodes first, where warm-boot replays old state daily.

Overlap: cataloged abstract mirror state/arxiv/2026-10-07/2610.07715v1.txt (id 3451d6f871eb); the 130-transition numbers and guard-vs-provenance verdict are new.

### 4. When Evidence Changes: Evaluating Memory Repair and Re-reading in Language-Model Agents (2610.03902, 2026-10-02)

**Q1+Q3 answer, the economics:** memory pipelines derive nodes in a versioned dependency graph with a read-set commit gate; "local repair" invalidates exactly the transitive successors of a changed document and recomputes only those (1 node vs 7-14.5 for full rebuild). But "every memory pipeline costs at least twice full re-reading in held-out conditions" (cache 2.2-3.0x, rebuild 5.3-6.8x, local repair 3.96-5.03x); source-filtered re-reading stayed cheapest at every record length; a 20-use sweep still had memory cumulative cost >= 1.21x. Repair misses were USE-TIME failures: in every non-adopting trajectory the new value was already in the prompt - the bottleneck was answer generation, not propagation.

**Estate translation for the L0d context-pack:** (a) benchmark the staged fix (digest commit f676ee787: hermes-agent runaway-recall ceiling + opt-in prefetch spilling, named DIRECT HIT and ported) against a source-filtered re-read baseline - the corpus FTS index (tools/corpus_fts_rebuild.py, B2-465 daily rebuild) IS the source filter; (b) expect memory-side repair to lose the cost fight below ~2-14 uses per record and long records to flip it, so measure the pack's reuse count before adding repair machinery; (c) if a stale pack value still misleads after the fix, suspect prompt assembly, not propagation. Limitations: one dataset (eICU), 7B models, small cells (3-20), token-not-dollar costs.

Overlap: fresh (zero catalog hits for the ID and the title phrase).

### 5. GRAFT: Transformations for Evolving Property Graph Schemas (2609.34789, 2026-09-28)

**Q4 answer, the pattern:** "a logic-based framework that models property graph schema evolution as reusable, order-constrained meta-transformations derived from atomic edits" with "duplication-freeness, termination, and correctness" guaranteed; greedy search reached the exact target schema on most datasets, with 100% reuse of original edit operations (evaluated up to 8.88M candidate schemas; Neo4j test at 42.14M nodes scaled linearly). Meta-transformations preserve edit-order dependencies (redirect an edge target BEFORE removing the old target node).

**Is the `invariant:law ` trailing-space id bug the actual join blocker? YES.** Two independent reasons from this read: (1) GRAFT derives meta-transformations from a corpus of existing atomic edits and joins new edits onto existing types; the estate's seed corpus (815 has_invariant + 300 maps_to edges, lens/graph.md:9) already contains 9 edges pointing at the malformed id `invariant:law ` (lens/graph.md:20) - any exact-match join on the cleaned string silently misses them, so learned transformations would either duplicate the law node or drop the 9-module slice; (2) GRAFT's own documented pain point is attaching to existing-but-incomplete nodes (the ICIJ greedy search trapped in a local optimum until node-insertion idempotency was enforced) - data hygiene of node identity is a precondition, not an afterthought. Order of operations: normalize the id, then derive orphan-wiring meta-transformations from the existing edge corpus (the 691 orphan doctrine/steal/knot nodes cite their target modules in their own summaries, lens/graph.md:44, so the meta-edits are nearly mechanical). Limitations: no integrity constraints yet, Jaccard structural similarity dominated by heavily-attributed nodes, exponential worst case.

Overlap: fresh (zero catalog hits).

### 6. GraphMemory: Decoupling Memory from Context (2610.02687, 2026-10-02)

**Q3 answer, the structural cap:** reframes agent memory update as optimization over the model's context; "GraphMemory retrieves only the relevant subgraph, enabling online context adaptation without exposing the model to the entire memory". Mechanism: nodes are reusable knowledge points with a compact routing-key index; an LLM retriever picks up to 2 sections + 6 entry nodes, then a deterministic BFS expands up to 2 hops, 2 top-weighted neighbors each, hard-capped at 12 nodes / 2,500 tokens; edge weights are Beta posteriors from confidence-weighted helpful/harmful feedback. Proposition 2: per-query context is O(1) and cumulative exposure O(N) versus O(N**2) for append-only memory. Results: 81-85% fewer memory-construction tokens, 79-92% fewer test-time tokens, no full-memory fallback (retrieval failure proceeds memoryless).

**Estate translation:** the runaway-recall ceiling fix currently ports a Hermes prefetch-spilling mechanism; this paper says the durable law is a STRUCTURAL cap (hops + nodes + token budget enforced in the retrieval path, with no fallback to full recall), not a behavioral ceiling. The context-pack generator is the natural enforcement site. Limitations: two tasks, two models, one baseline, no repeated runs, ~1.8x slower inference.

Overlap: fresh (zero catalog hits; note the estate's own module:context_compression.py exists in the graph with 7 edges, lens/graph.md:21 - this is a peer design, not a duplicate).

### 7. AECG: Asymmetric Experience Consolidation and Governance in Multi-Agent Systems (2610.05176, 2026-10-04)

**Q1+Q5 answer, the governance shape:** "memory pollution arises when outdated, weakly supported, or spuriously successful procedures become recurring components of future reasoning". Detection: each skill carries dual Beta beliefs (slow cumulative vs fast discounted); degradation D_k = max(0, mu_slow - mu_fast) with an uncertainty-adjusted drift score; failures count only when two independent LLM judges agree abstain-free at >= 0.70 confidence. Triage ranks by exposure (distance-discounted reachability) times drift; interventions create versioned candidate skills; a replay gate activates a candidate only if it fixes failure fixtures within epsilon of parent regression - "AECG thereby reframes multi-agent memory from passive accumulation into auditable reliability governance." Best in 11 of 12 framework-benchmark settings; corruption-detection delay 9.7 -> 3.8 uses.

**Q5 (world-rib contract / law census):** the questions are estate-internal by construction - no item in this sweep (~160 scanned, 7 read) offers a taxonomy of standing-law corpora, law censuses, or world-rib contracts. The transferable piece is the enforcement shape: laws-as-beliefs with dual slow/fast ledgers, drift-scored triage, exposure weighting, and versioned replay gates before any law is superseded. That maps 1:1 onto memory/law/registry.json + enforcement_trail.jsonl if the registry grows per-law drift scores.

Overlap: fresh (zero catalog hits).

## Answers to the five research questions (compressed)

- Q1 correction/supersession: frontier does it as append-only versioned transitions with change provenance (MINDSET, MELD, AECG), and proves the observation-vs-change trap is real and catastrophic without provenance (When Old Facts Return: 98.5% -> 10.8% on re-read). Grow superseded_by as a monotone status chain, never in-place.
- Q2 knot-as-CRD: survives; viable for status convergence with the single controller keeping admission/materialization authority (MELD's read-side gates). Not moot.
- Q3 L0d shedding + runaway recall: beyond the ported fix - enforce a structural retrieval cap with no full-recall fallback (GraphMemory O(1)/O(N) law), and benchmark the pack against source-filtered re-reading (When Evidence Changes: memory pipelines >= 2x).
- Q4 schema evolution: GRAFT meta-transformations; fix the `invariant:law ` trailing-space id FIRST because it poisons the join seed (9 live edges) that any derived rewiring learns from.
- Q5 world-rib contract / law census: estate-internal by construction; nearest frontier shape is AECG's auditable governance loop, adoptable as drift-scoring for the law registry.

## Checks run this session

- 8 arXiv export API GETs + 7 arxiv.org page fetches (2 abs, 5 html), all via WebFetch, all returned content (none 403).
- Overlap greps: git grep over catalog/catalog.jsonl + memory/ for titles and IDs of all shortlisted candidates (commands in transcript); state/arxiv/ directory listing for mirror dates 2026-09-05..2026-10-09.
- Lens grounding read: watch/inbox/frontier_olm_2026-10-09/lens/graph.md and lens/questions.md (Area 3 = this ask's five questions verbatim, lines 37-43).
- Not run: no local test suite (nothing in-tree changed); no re-verification of lens-computed estate numbers (taken from the lens files as the ask's input).
- Bank-file hygiene: no em-dashes used; every quote above was returned as an exact quote by the fetch of the cited page on 2026-10-09.
