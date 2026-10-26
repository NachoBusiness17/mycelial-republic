# Sweep: agent-memory-continuity via arXiv (2026-10-07)

source-fetched: 2026-10-07. Gopher seat: sweep-agent-memory-continuity-arxiv. Doors used: arXiv Atom API (export.arxiv.org, 6 queries, sortBy=submittedDate desc), arxiv.org abs pages, arxiv.org/html full texts. All quotes below are verbatim from pages fetched this session.

## Method receipts

- Pass 1 (broad): 6 API queries (agent memory window-filtered; LLM agents + long-term memory; KG construction + LLM; temporal KG; entity linking + KG; KG completion + LLM; memory consolidation + LLM) returned ~120 distinct titles; 63 fall inside the 2026-09-07..10-07 window. That is the 30+ candidate floor, cleared.
- Pass 2 (deep): 13 abs pages read (PACMI, Stashbird, EMIR2, Selection-vs-Extraction, Persistent-null, MemFit, TWIST, When-to-Remember, Think-Before-You-Link, TAGGRAPH, MEMTRIM, Right-Memory, MINDSET, DAEDALUS, PEARL = 15 counting all) plus 7 HTML full-text reads for verbatim quote extraction (EMIR2, TAGGRAPH, Stashbird, Persistent-null, TWIST, Think-Before-You-Link, When-to-Remember). Floor of 5 deep reads, cleared.
- Overlap instrument: grep -r -i over catalog/catalog.jsonl, memory/, and every prior lane write-up watch/inbox/frontier_olm_2026-{09-28,10-01..10-06}/sweep/*. Validation: findstr under this bash mangles /FLAGS (MSYS path conversion), all-zero results were discarded and redone with grep; positive control grep -c "arxiv" catalog/catalog.jsonl = 5275 lines. Control paper 2610.03902 ("When Evidence Changes", the ask's own baseline) is found in watch/inbox/frontier_olm_2026-10-06/sweep/agent-memory-continuity-arxiv.md and today's lens (burns.md, questions.md), and NOWHERE in catalog.jsonl or curated memory/ outside this session's own trajectory log (memory/trajectory/steps.jsonl, which echoes the ask text and my fetches and is excluded from overlap reckoning as a session log, not a holding).
- KEY FINDING that shaped this bank: this lane ran daily (09-28 through 10-06 predecessors) and already consumed the Sep 26..Oct 1 crop. Verified already-swept (do NOT re-bank): Stashbird 2609.34242 (4 sweep files), When Does Selection Replace Extraction 2609.34227 (6), TAGGRAPH 2609.38353 (3), EMIR2 2609.32584 (3), MemFit 2610.00872 (7), MemHarm 2609.34132 (10-01), JAM 2609.34385 (6), GraphMemory 2610.02687 (5), DyadMem 2610.03020 (10-05), Interpreting at Write Time 2610.02897 (10-05 + 10-06), MemPilot 2610.06830 (10-06), TWIST 2609.28575 (banked by the 09-28 run of this very lane; ARXIV_REGISTER verdict REAL), Think Before You Link 2609.10745 (catalog holding since 09-11, state/arxiv/2026-09-11/2609.10745v1.txt), Execution Consistency 2610.08101 (swept today by sibling lane swarm-orchestration-arxiv.md). The genuinely new surface was the Oct 2..6 crop plus two zero-hit older items.

## Banked items (8, strongest first)

### 1. PACMI: Provenance-Aware Cascading Memory Invalidation for Long-Term LLM Agents
- URL: https://arxiv.org/abs/2610.05732 · 2026-10-05 · cs.LG/cs.IR
- Quote: "This calls for two capabilities: dependency tracking to identify downstream effects and historical preservation to retain useful past records."
- Why: THE keyed-belief-retirement answer (Q5). Memories and new evidence live in a provenance graph with typed dependency edges; records sit on a four-state validity lattice; validity changes cascade to dependents; states drive retrieval and stale-premise detection. This is exactly "retire the stale belief without deleting still-valid neighbors": the cascade is keyed to dependency edges, not to topic proximity. Ships a 100-case/300-query diagnostic benchmark across five domains; highest final-answer accuracy; paired exact McNemar significance vs strongest baseline. Honesty signal we should steal: removing the premise checker raised final-answer errors 3 to 11 but the paired difference did NOT reach 0.05, and they say so.
- Overlap: zero hits for "PACMI", "Cascading Memory Invalidation", "2610.05732" across catalog.jsonl, memory/, and all prior sweep files; only hits were this session's trajectory log.
- Estate hook: mag/knowledge_graph.py edges could carry typed dependency + validity state; the four-state lattice maps onto the registry/law model (memory/law/registry.json) for belief retirement with witness trails.

### 2. MINDSET: Energy-based Schema Evolution for Long Conversational Agent Memory
- URL: https://arxiv.org/abs/2610.08586 · 2026-10-06 · cs.AI
- Quote: "a memory controller that stores a conversation as immutable episodes"
- Why: Best new Q2 (temporal flattening) + Q5 hybrid. Episodes immutable; schemas versioned via minimum-energy transitions where each new episode can "reinforce, supersede, split or create a schema"; transition objective includes distortion, contradiction, HISTORICAL DAMAGE, fragmentation, inconsistency; hysteresis stops isolated contradictions from destabilizing memory. Top LoCoMo answer F1 among 6 memory systems (850 questions); retrieval ranking beats LightMem at p<0.01 after Holm correction; cross-model check on GLM-4.7 and Gemma-4-31B. Frame steal: long-term memory as "constrained state management rather than continual summarization".
- Overlap: raw abstract bytes in today's catalog dawn pull (state/arxiv/2026-10-07/2610.08586v1.txt, mtime 2026-10-07T06:30:20Z); zero analysis in any sweep, lens, or memory file.
- Estate hook: supersede/split transitions with a historical-damage term is a direct upgrade path for the fold/supersede machinery (memory/fold_history/) where temporal flattening (arXiv 2609.36457, 244/381) bites us.

### 3. Understanding and Mitigating Inference-Time Overreliance Using Agentic Memory (MEMTRIM)
- URL: https://arxiv.org/abs/2610.07311 · 2026-10-05 · cs.AI
- Quote: "a plug-and-play framework that indexes memory evidence at write time and controls its reuse at read time"
- Why: The use-time half of Q1. Names the failure mode our zero-memory-call stat (40%, lens/burns.md:99-102) mirrors from the other side: memory distorts inference "even when they are benign, correctly stored, and appropriately retrieved", specifically under partial query-memory overlap. MEMTRIM indexes evidence at write, gates reuse at read, strips repeated/conflicting evidence, no retraining, works over embedding and structured memory. Access-policy shape: the dial is not call-more/call-less but admit-evidence-by-overlap.
- Overlap: zero hits for "MEMTRIM", "Inference-Time Overreliance", "2610.07311" anywhere checked.
- Estate hook: pairs with banked adoption-at-use (8-9/13 vs re-read 13/13, 2610.03902): re-read wins when overlap is partial; MEMTRIM is the policy that keeps memory useful when overlap is full.

### 4. Persistent Memory in Multi-Agent LLM Inference: What It Costs, What It Buys, and When You Can Tell
- URL: https://arxiv.org/abs/2610.07782 · 2026-10-06 · cs.LG, NeurIPS 2026 ML for Systems Workshop poster
- Quote: "Nothing a system learns on question i is intended to be useful for question j."
- Why: The write-vs-use question gets a measured NULL. Three-tier decomposed inference: peak KV working set ~14.3 MiB vs ~35 MiB single-pass; the persistent memory tier adds +0.368 MiB peak cache and produces no detectable accuracy change (+0.015, 95% CI [-0.011,+0.046]) across eight controlled dataset pairs at n=100/arm. Their structural diagnosis is the falsifier our estate needs: independent-item benchmarks leave recall nothing to retrieve. They also report four measurement corrections, three of which had inflated apparent benefit, and give detection conditions for valid agent-memory ablations.
- Overlap: raw abstract in today's catalog pull only (state/arxiv/2026-10-07/2610.07782v1.txt); zero analysis anywhere.
- Estate hook: before treating 40% zero-memory-call sessions as a defect, run their ablation-detection conditions: if session questions share no dependency structure, zero-call is correct behavior. This is the cheap falsifier for the burns.md claim.

### 5. The Right Memory in the Wrong Context: Verifying Retrieval Admissibility in Long-Term Agent Memory
- URL: https://arxiv.org/abs/2610.07309 · 2026-10-05 · cs.AI, NeurIPS 2026 "Who Verifies the Agents?" workshop, code on GitHub
- Quote: "relevant information that is inadmissible for the current request"
- Why: Q1/Q5 verification layer. Assigns each memory-query pair one of three statuses: "admissible, inadmissible, or unresolved"; compares routes at matched required-evidence recall; traces memory IDs from prompt exposure to disclosure. Reanalysis of RHELM + MemOps top-20 (3,767 queries): anchor recall 0.432 to 0.533, 80% recall feasibility 0.237 to 0.311, 98.3% drop in exact similarity evaluations; namespace routing associated with +0.053..0.068 accuracy in 1,523 paired cases (observational, they flag it as such).
- Overlap: zero hits for title fragments and ID anywhere checked.
- Estate hook: the three-status verdict is the same shape as our REAL/OWED/struck citation discipline; admissibility-by-namespace matches audience-bound memory instincts already in the estate (see swept Audience-Bound Persistent Memory 2609.36373).

### 6. When to Remember, When to Abstain: Category-Conditioned Retention for Reliable Agent Memory
- URL: https://arxiv.org/abs/2610.07100 · 2026-10-05 · cs.AI, NeurIPS 2026 Social Agent Workshop, 4 pages
- Quote: "a stricter bar on values alone reduces unsupported retentions from 6.2% to 4.0%"
- Why: Q1 write-boundary + Q5 wrongful-retention. Retention needs "a confidence bar conditioned on the semantic category of the assertion", not one global threshold: value/belief assertions are only 77.9% source-supported vs 96.2% for other categories (4,715 candidates, 100 synthetic personas); category conditioning cuts unsupported retentions ~36% relative while preserving ~13 points more coverage (95% CI 9.8..16.0). Framed as selective prediction at the write boundary.
- Overlap: zero real hits; the single catalog hit for "When to Remember" is a DIFFERENT paper (Traverse, 2609.37082, fetched 09-30).
- Estate hook: the percolator/facts lanes (memory/facts/behavioral.jsonl) can adopt category-conditioned bars cheaply; values/beliefs are exactly the class our burns flagged.

### 7. DAEDALUS: Bootstrapping Agent Memory from Self-Generated Tasks
- URL: https://arxiv.org/abs/2610.08048 · 2026-10-06 · cs.AI, 9+31 pages, code + traces at github.com/illuin-tech/daedalus
- Quote: "an explorer that interacts with the environment to generate challenging yet solvable tasks"
- Why: Q1 from the write side, no oracles. Agents "often lack the operational knowledge to act reliably in new environments"; DAEDALUS pairs the explorer with a solver, accepts a heuristic only after repeated in-context success, and uses outcomes to steer task difficulty. Mean success up 15.9 points, pass^5 up 2.2x over no-memory on AppWorld, tau2-bench, AutomationBench; heuristics transfer across model families; competitive with training-task methods at lower inference cost.
- Overlap: raw abstract in today's catalog pull only; zero analysis anywhere.
- Estate hook: acceptance-only-after-repeated-success is a falsifier shape for memory writes; matches the flock's self-evolution lane without external task oracles.

### 8. PEARL: Path-Entity Aligned Relational Learning with Contextual Subgraphs for Inductive Knowledge Graph Completion
- URL: https://arxiv.org/abs/2609.02216 · 2026-09-02 · cs.AI (35 days old; outside the strict 30-day preference, banked because it is the only zero-overlap measured method for the orphan-node question)
- Quote: "a large language model (LLM)-guided retriever to distill semantically relevant paths"
- Why: Q4 orphan stitching. Inductive KGC = predicting links for entities never seen in training, i.e., our 1,066 orphaned nodes (lens/graph.md:30-33). Prior methods "encode relational paths independently of their surrounding query subgraphs"; PEARL builds a query-specific contextual subgraph from the union of query-entity neighborhoods, uses the LLM-guided retriever to distill semantically relevant paths, then a bipartite path/entity/global interaction graph with dual-view contrastive denoising under stochastic perturbation (the anti-fabrication guard). Top average Hits@10 on WN18RR, FB15k-237, NELL-995.
- Overlap: zero hits for "PEARL" ID, "Path-Entity Aligned" anywhere checked.
- Estate hook: stitch orphans query-conditioned (build the subgraph around the query pair, not the whole forest) and keep the contrastive denoise step so induced edges survive perturbation; before investing, weigh TAGGRAPH's banked counter-evidence (BM25 0.867 vs best graph 0.844 MRR on LongMemEval-S) that lexical retrieval can rival graph traversal over agent histories.

## Question ledger (what is answered, what is OWED)

- Q1 write-time vs use-time: answered by items 3, 4, 6, 7 plus the predecessor bank (Selection-vs-Extraction 2609.34227: raw-turn selection non-inferior at tight budgets, "3,061 times less to write", extraction wins at generous budgets; JAM 2609.34385 just-in-time beats ahead-of-time). OWED: no new paper in this window directly measures a policy that cuts ZERO-memory-call session rates; nearest instruments are item 4's ablation-detection conditions and DyadMem's Gold-Memory vs Full-Pipeline drop (already swept 10-05). Next window: watch for access-policy papers reporting session-level memory-call telemetry.
- Q2 temporal flattening: item 2 (MINDSET) is the new measured architecture; EMIR2 (evolving states, MemConflict) and TWIST (belief-change supersession) already banked by predecessors.
- Q3 named open-source memory layers (Mem0/Letta/Zep): OWED for this window. Every 2026 measured-cost item naming those stacks (Stashbird 76.4x fewer ingestion tokens than Graphiti; MemFit; TAGGRAPH; JAZ vs Letta) is already in our sweep holdings from 09-28..10-06 runs; no NEW release-line paper from those vendors cleared the overlap bar this window. Re-banking would be waste.
- Q4 star-forest edge induction: item 8 (PEARL) is the new method; TAGGRAPH (banked) is the contrarian ROI evidence; Think Before You Link (catalog holding since 09-11) supplies the structural-rarity diagnostic for which orphans are even linkable.
- Q5 belief retirement + falsifiers: item 1 (PACMI) is the centerpiece; falsifier shapes across the bank: TWIST matched do-not-over-detect hard negatives (banked 09-28), PACMI's paired McNemar with the honestly-reported non-significant 3-to-11 ablation, MemHarm counterfactual regret (banked 10-01), MINDSET historical-damage term, DAEDALUS repeated-success acceptance gate.

## Doors status

export.arxiv.org API: healthy (6/6 queries returned; one 4-way parallel batch timed out at 60s, rerun sequentially succeeded, no degraded output). arxiv.org abs + html: healthy. No 403s. WebSearch: one query timed out twice, dropped; the recipe's site: search was not needed since API coverage exceeded the candidate floor.
