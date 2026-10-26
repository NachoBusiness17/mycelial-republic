# FRONTIER SWEEP: agent-memory-continuity via arxiv (run 2026-10-11)

source-fetched: adhoc

Seat: sweep-agent-memory-continuity-arxiv (2026-10-11 run). Doors: export.arxiv.org Atom API (4 queries, all clean this session), arxiv.org/list/cs.CL + cs.LG recent, arxiv.org abs + html pages, WebSearch. A prior run of this same sweep (2026-10-10, API door degraded then) is preserved at agent-memory-continuity-arxiv.prior-2026-10-10.md; its 8 banked items (Hippocam, galahad-kv, QGMem, Attic-KV, Agentic-TTT, Right Memory in the Wrong Context, When to Remember When to Abstain, MemTrial) are DISJOINT from this run's 8, so the two runs are complementary, not re-banking.

Door health (this session): export.arxiv.org API answered all 4 queries. One WebSearch 429'd on its first call and recovered on retry; used only to discover GRAFT. arxiv.org/html/2608.29606v2 returned 404 (versionless html worked); abs 2610.05732 timed out once (retry succeeded). cs.LG recent listing rendered titles only. No fabricated fallbacks.

## Pass 1 (broad sweep): 55+ in-window candidates (2026-09-11..10-11)

Feeds pulled: all:"agent memory" (30 entries), abs:memory AND abs:"LLM agents" (30), abs:"knowledge graph" AND agent AND memory (25), abs:"memory consolidation" AND cs.CL (16, mostly older), plus both recent listings and search (GRAFT). In-window highlights beyond the banked set: MINDSET 2610.08586, MemoWM 2610.10778, HGP 2610.10071, DyadMem 2610.03020, MemFit 2610.00872, PrisMem 2610.06361, MemPilot 2610.06830, AECG 2610.05176, StateWise 2610.05241, When Evidence Changes 2610.03902, Mem++ 2610.02002, SkillForge 2610.09832, DAEDALUS 2610.08048, Memento 3 2610.11794, QGMem 2610.11920, MemTrial 2610.11732, MemCodex 2609.39765.

## Pass 2 (deep reads): 13 papers read end to end (arxiv.org/html) plus abs pages

Deep-read: MINDSET, GraphMemory, DAEDALUS, Memento 3, Selective Forgetting, BFR, HGP, GRAFT, QGMem, CASK, PACMI, SAGA, Agent Zero Memory. All quotes below were captured from pages fetched this session through the WebFetch channel; treat wording as channel-rendered (confidence 0.8); titles/dates from abs pages (0.95).

## Overlap verdict (commands run, not assumed)

Catalog: grep -i -c -F per phrase on catalog/catalog.jsonl (bash, this session). Memory: grep -r -i -l -F over memory/ for the 8 exact titles; 3 files matched, all verified by context grep as generic-phrase or sibling-trail coincidences.

- All 8 banked titles: 0 exact-title hits in catalog.jsonl AND memory/.
- GRAFT: 9 catalog hits are Sapling GraftOperation.ts, graft_test.py, a resume doc (unrelated).
- SAGA: 9 catalog hits are the estate's own mag/game_saga.py (unrelated).
- "Selective Forgetting": memory/ hits are the generic phrase in memory/runs/gapwave/gap_external_field.md and memory/runs/quote_audit_wide_20260925/inbox_concat.txt (concept usage, not the paper).
- Agent Zero Memory, PACMI, CASK, BFR: appear only inside a sibling sweep's grep-command trail in memory/trajectory/steps.jsonl (title seen in feed digests, nothing banked).
- Already catalog-stubbed by the estate's 06:30Z lsa sweep and therefore EXCLUDED from this bank despite deep reads: MINDSET 2610.08586, DAEDALUS 2610.08048, Memento 3 2610.11794, HGP 2610.10071, QGMem 2610.11920, Mem++ 2610.02002, MemCodex 2609.39765 (zone lsa, ~2KB title stubs, age 1-9 days). QGMem and Memento 3 also carry full detail in the prior run's write-up.

## BANKED ITEMS (strongest first; the JSON result carries these 8)

### 1. Transformations for Evolving Property Graph Schemas (GRAFT) - arXiv 2609.34789 - 2026-09-28 - cs.DB - PVLDB 19(13)
Devillez, Dumbrava, Bonifati. Schema evolution as a finite meta-graph: vertices are schemas, edges are grounded meta-transformations composed of 11 atomic edits (AddLbl, RmvLbl, Add, Rem, AddE, AddProp, RmvProp, ReLbl, UpdTgt, UpdSrc) under Datalog-style Start*/Next* order constraints; Bron-Kerbosch clique compression; similarity-guided greedy/beam search. Guarantees (Thms 8-21): duplication-free enumeration, termination, soundness, losslessness by composition, greedy optimality for T-monotone sets. ICIJ scenario: naive application 1.57s at 73% similarity; idempotent insertion reaches 100% similarity in 8.9s over a 32-step sequence; linear growth to 42.14M nodes.
Quote (sec 4.3.1): "a schema S2 is related to a schema S1 if S2 can be obtained by applying a grounded instance of a meta-transformation to S1."
WHY HERE (Q1, graph.md:18): the regen that dropped all 117 why_context edges is an unconstrained schema rewrite; GRAFT is the published discipline making schema changes order-constrained, reusable, and provably lossless. Honest limit (sec 5.1.1): "GRAFT searches offline at the schema level, leaving instance data untouched", so instance-level edge survival still needs an estate-side test.

### 2. Selective Forgetting: A Graph-Based Memory Framework for Long-Term LLM Agents - arXiv 2608.28978 - 2026-08-29 - cs.AI
Rusu, Khanzadeh, Alalfi. The direct graph-vs-vector head-to-head Q2 asks for. Typed-node graph (9 labels, attributed edges, GPT-4o-mini extraction, 2-hop retrieval at a matched 5-root budget) LOSES to a flat vector baseline on LongMemEval: token F1 0.417 vs 0.468, paired bootstrap n=500, delta F1 -0.050, 95% CI [-0.085, -0.016]; judge 0.454 vs 0.536; assistant-turn recall judge falls 0.911 to 0.607 (entity decomposition discards surface form); graph's only win is temporal (0.293 vs 0.278). Forgetting works: one pass over a 27,021-node graph removes 9.8% of nodes at +0.001 F1.
Quote (sec 5): "structured abstraction can improve relational organization while simultaneously discarding information required for precise or verbatim recall."
WHY HERE (Q2, corpus.md:41): sharpest published evidence that graph coherence does not automatically beat embeddings; it wins only where typed temporal structure is queried. Authors' caveat (abstract): "these results characterise this extraction-based pipeline rather than graph-structured memory in general."

### 3. PACMI: Provenance-Aware Cascading Memory Invalidation for Long-Term LLM Agents - arXiv 2610.05732 - 2026-10-05 - cs.LG
Wang, Liu, Zhang, Wu, Duan, Zheng, Cai. Memory as a provenance graph (supports, used-by, update, contradict edges) with a validity lattice active < needs-verification < historical-only < superseded; BFS cascade, strongest state wins, nothing deleted. 0.99 accuracy vs 0.90 A-MEM-style (3 vs 29 errors of 300, McNemar p ~ 2.56e-6); the destructive LLM-only-update baseline collapses to 0.42 on historical queries; removing historical preservation drops Q3 1.00 to 0.36; cost 400 auxiliary LLM calls vs 100.
Quote (sec 3): "The state assignment is non-destructive throughout: original text is preserved, so a superseded record remains available as historical evidence."
WHY HERE (Q1 + Q4): the published measurement that in-place rewrites destroy historical recall while lattice-marked invalidation preserves it; the 117-edge drop is exactly the destructive branch failing. Honest limit (sec 6): dependency edges were annotation-supplied, so the estate would still need its own edge extraction.

### 4. Whose Memory Is It? Scope-Aware Commit Rules for Long-Term LLM Memory (CASK) - arXiv 2610.09008 - 2026-10-06 - cs.AI - NeurIPS 2026 LP4FM
Gu, Li. Names the failure where provisional reasoning (simulated tool outputs, relayed beliefs, explored plans) persists as fact once stripped of context: discourse ownership, the world/branch/speaker licensing a proposition. CASK learns a rank-16 ownership subspace via DAS, stores basis-invariant Gram features + logit diffs (46 features), gates commits: actual-world content gets a commit edge, scoped content stays retrievable under its owner only. Attachment accuracy 83.33% (3B); Cask@R95 cuts contamination 11.19 points vs flat memory; conflict adoption 1.03% vs 4.53%; ~1.29x inference overhead.
Quote (sec 3): "nonactual means scoped, not false: such a record remains useful when a query addresses its owner."
WHY HERE (Q1/Q5): authored cross-links dying in regen is a commit-boundary problem; CASK is a tested admission rule separating durable authored facts from derived provisional content at write time.

### 5. Relevance Is Not Sufficiency: What Actually Closes the Evidence Gap in Long-Term Memory QA (BFR) - arXiv 2610.09348 - 2026-10-07 - cs.AI
Li, Li, Xu, Li, Zeng, Yao, Lin, Li, Bi, Han. Recasts retrieval as building a sufficient evidence set: requirement decomposition, FCA prefilter (P=20), minimum-subset selection (avg 1.86 notes), budgeted acquisition of unseen records. LongMemEval-S judged accuracy 72.4% to 82.2%, Turn Hit 91.4%; LoCoMo judge 70.5 vs Mem0 59.0; robustness set Gold Hit 54.8% to 78.1%.
Quote (sec 6): "retrieval should deliver an answer-supporting evidentiary record, not simply a list of similar items."
WHY HERE (Q4/Q5): supplies the metric pair (Gold Hit, Turn Hit, LLM-Suff@Set) and the sufficiency framing to measure whether the 40-day-stale fold cure changes what memory can recall, and its evidence-set output is the evidence layer the graph lacks (9/6/6 filled, graph.md:19).

### 6. Decoupling Memory from Context: Structured Memory for Token-Efficient Test-Time Continual Learning (GraphMemory) - arXiv 2610.02687 - 2026-10-02 (v2 10-06) - cs.AI+cs.LG
Farhat, Desmond, Kyrillidis. ACE-style lesson nodes with directed edges carrying Beta(1,1) evidence counters (helpful S, harmful F) ranked by posterior mean; Retrieve-Generate-Reflect-Curate; bounded BFS retrieval (2 hops, 12 nodes, 2,500 tokens) gives O(1) retrieved content per query vs O(N) append-only. Build-cost numbers: 81-85% fewer memory-construction tokens (20M vs 131M on Formula/Claude, 84.7%), test tokens down 79-92%, money $24.00 vs $157.20 (Formula/Claude); accuracy trails append-only ACE by 2.9-4.0 points; per-query inference ~1.8x slower.
Quote (sec 5): "bounded retrieval changes memory-context scaling from linear growth under append-only prompting to a constant bound on retrieved content per query."
WHY HERE (Q2/Q4): the concrete build-cost column for graph memory. Honest caveat: the paper does NOT compare against a vector-store baseline (names embedding retrieval as future work), so it prices graph vs append-only, not graph vs embeddings.

### 7. Principles that Guide, Actions that Inform: Agent Evolution via Knowledge Abstraction (SAGA) - arXiv 2610.06964 - 2026-10-03 - cs.AI+cs.LG
Ye, Xu, Ma, Yin, Li. Four levels with bidirectional evidence links (raw trajectories, episodic records, procedures, principles with condition/effect/mechanism/scope/exceptions); each node at most two parents (sparse auditable evidence graph); rejected principles enter an exclusion registry so equivalents cannot return; memory frozen before evaluation. ALFWorld 99.3% (vs Memento 53.0, ExpeL 46.3); ScienceWorld SFT+GRPO 66.9.
Quote (App. E): "the extracted principles are explanatory hypotheses supported by execution evidence, not established causal laws."
WHY HERE (Q3, laws.md:97): the ten-minute-self falsifier evidence. Decisive negative result: raw principles injected into prompts HURT (R4 below R3 in their ablation); gains came only from task-conditioned instantiation plus predicate checks. Prediction for the estate: a fold built only from controlled pitfall-bypass bytes will NOT beat prompt-only on held-out pitfalls unless fold entries carry applicability conditions and an exclusion registry.

### 8. Agent Zero Memory: Provenance-Aware Long-Term Memory for LLM Agents - arXiv 2608.29606 - 2026-08-30 - cs.CL
Wu, Zhu. Three parallel stores (episodic Memory Events timeline, entity-event ontology graph, hierarchical documentary memory L0/L1/L2); every item carries origin, immutable timestamp, and an evidence pointer resolving back to raw artifacts; answers read under a citation lock; updates non-destructive (corrections append). LongMemEval 95.60% (+0.73 SOTA), LoCoMo 93.60% (+1.10); across 8 backbones accuracy varies 3.4 points while cost varies ~30x (near-SOTA at ~20x lower cost).
Quote (sec 3.1): "an answer is read under a citation lock, whereby it may cite only evidence its reader actually opened, so fabrication is structurally excluded and the system abstains rather than guesses."
WHY HERE (Q5): the published design that fills an evidence layer per node (origin + timestamp + evidence pointer + citation lock) instead of adding degree-0 name nodes (graph.md:17). 42 days old, kept because nothing fresher matches the evidence-layer ask; noted per the 30-day preference.

## QUESTION-BY-QUESTION VERDICTS

- Q1 (builder + cross-link survival): builder identity OWED; no arXiv paper can name an untraced mag/ builder, that is estate introspection. Published cure pattern converges across GRAFT (lossless ordered schema transforms), PACMI (destructive rewrite measured collapsing 1.00 to 0.36), CASK (commit rules for authored vs provisional), MINDSET (immutable episodes; schemas only index them, never store content). Convergent law: authored bytes append-only, indexes derivable, so any regen rebuilds edges but can never destroy them.
- Q2 (verkle coherence vs vector on seat tapes): verdict on estate tapes OWED (needs the estate's own tapes). External evidence: graph side is not a guaranteed win (Selective Forgetting CIs; GraphMemory prices graph vs append-only only). Falsifier shape to copy: fixed retrieval budget, paired bootstrap over questions, per-question-type breakdown.
- Q3 (ten-minute-self falsifiers): week-over-week pitfall trend OWED (estate telemetry). SAGA's R4<R3 ablation predicts the controlled-corpus fold fails vs prompt-only without applicability conditions; its exclusion registry is the mechanism that stops rejected entries returning.
- Q4 (40-day-stale fold, mine_recon): recall delta OWED (estate instrument). BFR supplies the measurement (Gold Hit / Turn Hit / LLM-Suff@Set); PACMI warns a destructive refresh destroys historical recall (1.00 to 0.36), so the fold cure must be non-destructive.
- Q5 (evidence-layer designs): banked answer: Agent Zero Memory evidence pointers + citation lock, BFR sufficiency sets, CASK scoping keys, PACMI provenance edges; all four fill we_have/evidence/banked per node without degree-0 names.

## Instrument receipts
Catalog greps: grep -i -c -F per phrase (bash) on catalog/catalog.jsonl; context disambiguation with grep -i -oE ".{0,90}<phrase>.{0,90}". Memory greps: grep -r -i -l -F over memory/ (8 exact titles, completed, exit 0), context-verified. A 30-pattern PowerShell memory scan (_overlap_check.ps1, this dir) was stopped as redundant once targeted greps covered all banked titles; its one emitted row (MINDSET catalog=1) agrees with the targeted greps.
