# Sweep: agent-memory-continuity via arXiv (2026-10-05)

source-fetched: 2026-10-05. Area: agent-memory-continuity. Runner: sweep-agent-memory-continuity-arxiv (actor_3_9, sess_dwf-dwfrun-daecd119). All fetches this session: 10 arXiv pages (6 abs + 3 HTML full text + 1 API XML query set x6) + 1 WebSearch. Zero paid dispatches.

## Method

- Pass 1 (broad): 6 arXiv API queries via `https://export.arxiv.org/api/query?search_query=...` sorted by submittedDate desc, plus 1 WebSearch (`site:arxiv.org agent memory knowledge graph dangling entity identity`). Queries: "agent memory" (25 hits), "episodic memory"+"large language model" (25), "long-term memory"+"LLM" (25), "memory benchmark"+agents (25), "entity resolution"+"memory"+agent (0 hits, totalResults 0), "working memory"+"LLM agent" (14). Candidate pool: 60+ entries, ~45 inside the 30-day window (2026-09-05 to 2026-10-05). Door status: all arXiv API doors 200. WebSearch fired one upstream 429 (`MCP error -429 ... 1302`) mid-run but still returned results; no door 403'd.
- Pass 2 (deep): fetched and read 8 items; 3 of them end to end at full HTML (EnSIMem v2, MemCodex, DyadMem), 5 at full abstract page (GenMem, MemFit, LSTMem, Stashbird, VibeMemBench).
- Overlap grep: `rg` and `grep` are absent from this session's bash (exit 127 twice; verified `command not found`), so the scan ran as venv python one-shots (`./.venv/Scripts/python.exe C:/Users/foste/AppData/Local/Temp/overlap_scan_sweep.py` and `overlap_rows_sweep.py`, `sibling_sweep_check.py`), scanning catalog/catalog.jsonl + memory/** (474,020 files) for titles and arXiv IDs.

## Pass 1 inventory (in-window candidates, strongest families)

Entity identity / graph weld (RQ1): EnSIMem 2609.27279; GenMem 2609.34633; Stashbird 2609.34242; EMIR2 2609.32584; MemoryLACE 2609.03201; RoutePrism 2609.34160; TAGGRAPH 2609.38353; ID-RAG 2509.25299 (out of window, prior art surfaced by WebSearch, NOT fetched).
Narrative-to-code weld / isolation (RQ2): MemCodex 2609.39765; VibeMemBench 2609.23570; Coding Agent Memory Post-training 2609.34422; Vestrum 2609.33822; CoMemBench 2609.32192; MemArena inside MemCodex; Memory as Infrastructure 2609.05510 (2026-08-31, 5 days out of window, noted not fetched).
Recall / continuity evals (RQ3): DyadMem 2610.03020; MemFit 2610.00872; APDMem 2610.02472; Mnemon 2609.36059; DolphinBench 2609.24971; TWIST 2609.28575; CueMem 2609.12354; RIME 2609.34438; EvalMem 2609.22231 (09-03, 2 days out of window, noted not fetched); When Users Don't Ask 2609.03467 (out of window); UTILMEM 2608.30508 (out of window).
Tier architectures (RQ4): LSTMem 2609.33268; Interpreting at Write Time 2610.02897; GraphMemory 2610.02687; CreaMem 2609.08550; SimpleARM 2609.36595; JAM 2609.34385; RPMem 2609.23466; LifeFuse-Mem 2609.12436; AutoViewMem 2609.21940; MemAgent 2609.32521; PersMem 2609.34372.

## Pass 2 deep reads (the 8 actually fetched and read this session)

### 1. DyadMem: A Long-Term Memory Benchmark of How Agents Work with Users (2610.03020, 2026-10-02) - NEW, deep full-text

Genuinely unbanked: zero catalog rows, zero prior sweep receipts; the only memory/ hits are this session's own trajectory greps (memory/trajectory/steps.jsonl L58968, ts 2026-10-05T14:45Z, session actor_3_9 = this runner).
Design: 3,065 episodes / 50,961 sessions / 61,210 QA instances, fully synthetic LLM-generated dialogue, 5 domains, 6 memory categories (user_profile, fact, agent_identity, agent_method, agent_knowledge, episodic). The new construct is URAM (User-conditioned Relational Agent Memory): "URAM records how this particular agent should work with this particular user" (agent_identity + agent_method + agent_knowledge).
Lifecycle scoring: gold Capture entries (micro P/R/F1, semantic coverage matching), gold Update ops (macro of Add-F1 and Delete-F1 over 20,590 sessions), Recall (Recall@n primary plus Recall@n+4, Recall@All, Hit@1), and two QA modes: Gold-Memory QA vs Full-Pipeline QA, with the Gold-to-Pipeline gap delta-G2P = Acc_gold minus Acc_pipe as the headline metric.
Findings over 20 models: gold-bank QA 78.7 to 96.3 percent, but "Full-Pipeline QA averages only 47.7% for open-weight models and 57.4% for proprietary models"; capture under-extraction (open-weight recall 15.1 percent, model banks ~75 entries vs 323.6 gold); gold-conditioned update F1 18.6/24.5 percent; "the unsafe-deletion rate, the fraction of predicted deletions that are incorrect, averages 84.1% and 78.1% for the two groups"; URAM conditioning wins across all 20 models (+3.2/+3.7 QA). Stated limitations: synthetic data; G2P "an end-to-end gap rather than a causal allocation of error"; full-pipeline conflates memory quality with answer willingness (over-abstention 9.2 to 59.9 percent).
Estate use (RQ3, the 258,840 + 65,934-row biography shelf): this is the transplant-ready eval frame. Score the zknot recap and rib stack in DyadMem grammar: sample rows as gold support, run Recall@n of the boot recap against them, and add an unsafe-deletion-style metric for superseded facts the recap resurrects. The capture-recall 15.1 percent finding predicts our recap loses most bankable rows; measure before assuming otherwise.

### 2. LSTMem: Hierarchical Long Short-Term Online Memory for LLMs (2609.33268, 2026-09-27) - NEW

Genuinely unbanked: arXiv ID NO-HIT anywhere in catalog/memory (verified by scan); title hits only in trajectory.
Design: per-layer two-state online memory for a frozen backbone: "a cell state that accumulates history and a hidden state whose readouts correct the backbone's attention," with separate input/forget gates on what the cell stores and an output gate on what it exposes; cross-layer forward propagation plus block-end feedback. Improves MemoryAgentBench, LoCoMo, HotpotQA over the plain backbone (Qwen3-4B-Instruct); LSTM formulation beats an associative-memory ablation. Code: github.com/Longchentong/LSTMem.
Estate use (RQ4): this is the cleanest published argument that the estate's two-gate boot is architecturally right but under-specified: ribs = cell state (accumulate everything, write-once, verkle-knotted), zknot recap = hidden state (bounded readout). The paper's lesson is the missing piece is the OUTPUT GATE: an explicit, trained-or-ruled choice of what the recap exposes from the rib vault, separate from what the ribs store. The zknot rewrite is currently a summarizer; LSTMem says make it a gated readout that corrects attention (boot attention toward the live edges) rather than a compression of history.

### 3. EnSIMem: Entity-Structured Indexing for Long-Term Agent Memory (2609.27279, v1 2026-09-23, v2 2026-09-27) - RE-READ DELTA, deep full-text v2

Overlap (verbatim scan): catalog/catalog.jsonl L445368 (id 20f5cd99ce8b, text cached at state/arxiv/2026-09-24/2609.27279v1.txt); banked by sibling sweeps 09-28, 10-01, 10-02, 10-03 in this same area (watch/inbox/frontier_olm_*/sweep/agent-memory-continuity*.md); ARXIV_REGISTER verdict REAL. NOT re-banked here as new; this row banks the v2 full-text delta.
Delta: the paper does NOT solve cross-session entity identity, the exact estate wound (29-of-31 phantom already_inside welds from free-text id building at mag/knowledge_graph.py:237-239). The v2 text grounds entity identity only at prompt level: records are [entity][entity_type][property: value] with source turns, candidates "merged by episode identity," inverses emitted "only when entailed," and a rule not to infer facts "from world knowledge, episode adjacency, or an image URL." The fetch read states it plainly: "Entity dedup across sessions is not addressed." Headline numbers (v2): LoCoMo 90.6 percent, LongMemEval 92.8 percent, structured retrieval 96.59 vs dense-only 86.36 on the ablation subset; cost 14.4 s vs MEMORA 5.70 s.
Estate use (RQ1): confirms the fix design cannot be imported whole. Take EnSIMem's provenance-bearing index rows (every weld cites its evidence) but the estate must add the dedup/canonicalization layer EnSIMem skips: module ids minted from the module registry, and landscape already_inside edges fail-closed (drop or flag when the target id is absent from the registry) instead of synthesizing `module:{Path(m).name}` from free text.

### 4. MemCodex: Self-Programming Hierarchical Memory for Language Agents (2609.39765, 2026-09-30) - RE-READ DELTA, deep full-text

Overlap: catalog L806442 (cached state/arxiv/2026-10-01/2609.39765v1.txt); sibling sweeps 10-01, 10-02, 10-03. Delta rows banked here: the archive/rejection-log mechanism and MemArena, which the estate's RQ2 fix needs.
Delta: memory layers are actual programs behind a fixed five-method interface ("admit filters candidates, index keeps a bounded active set, and propose derives items for the layer above" on write; "score" and "route" on read). Evolution rewrites one method at a time: meta agent reads "the target layer's code, diagnosis and rejection log, then returns a subclass that overrides only that method." Accepted architectures live in a tree archive whose nodes store accuracy, tokens per question, and per-question verdicts; rejected children append to the parent's rejection log. Every derived item records in(x) (inputs read) and src(x) (exact raw source turns). Results: 60.8 percent avg with Qwen3.5-27B, +10.1 percent over the strongest adaptive baseline, 3.4x fewer context tokens; routing channel beats content-only 60.8 vs 55.4; per-method evolution beats whole-program rewrites; native architectures beat transferred ones by 1.5 to 2.8 points.
Estate use (RQ2): the direct answer to "link session records to the modules that implemented them" is MemCodex's linkage shape: a derived node carries src(x) back to raw turns, and weld attempts that fail replay go to a rejection log instead of silently materializing phantom nodes. Our already_inside welds are MemCodex's `propose` with no `admit` filter and no rejection log; that is the 1,204-isolated-node shape in one sentence.

### 5. MemFit (2610.00872, 2026-10-01) - ALREADY BANKED (10-02, 10-03, 10-04 sweeps), abstract re-verified

Overlap: no catalog row, but sibling sweeps 10-02/10-03/10-04 banked it; NOT re-banked. Verbatim abstract claim: "stores each turn verbatim in an append-only store with near-instantaneous, LLM-free insertion, indexing turns with segment summaries rather than replacing them," SOTA on LoCoMo/MemGallery/LongMemEval-S at a fraction of cost. Estate note: validates the estate's append-only trail.jsonl habit and argues against summarizing the biography shelf.

### 6. Stashbird (2609.34242, 2026-09-28) - ALREADY BANKED (10-02, 10-04 sweeps), abstract re-verified

Overlap: no catalog row; sibling sweeps 10-02 and 10-04. Not re-banked. Claim: "On LoCoMo, Stashbird uses 76.4x fewer ingestion prompt tokens than Graphiti" via provenance-linked records plus lifecycle ops (updates, episode-level deletion). Estate note: the deletion operation is the piece our graph lacks for renaming modules.

### 7. VibeMemBench (2609.23570, 2026-09-20) - ALREADY HELD (catalog L444888, 10-03 sweep), abstract re-verified

Overlap: catalog row + 10-03 sweep. Not re-banked. Claim: benchmark "exposes the gap between the useful experience that repository history holds and the experience existing memory systems deliver"; 4 existing memory systems, 11 of 12 solver-system pairings failed to beat the memory-off baseline, while direct injection of verified history gave +1.1 to +4.5 points on 4 of 5 solvers. Estate note (RQ2): the graph lens should be scored on a downstream executable metric, not node counts, or it is one of the 11.

### 8. GenMem (2609.34633, 2026-09-28) - ALREADY BANKED (10-02 sweep), abstract re-verified

Overlap: sibling sweep 10-02 banked it with the "Symbolic Identifier" phrase hit. Not re-banked. Claim: SIDs are "a multi-level discrete token tuple drawn from a Cartesian-product address space" (<100 symbols factorizing a million-scale memory space); payloads rewrite at fixed addresses; addresses never change. Estate note (RQ1): the address-stability principle is exactly what module ids need: registry-minted, name-independent, stable across renames.

## Synthesis for the estate map (graph lens isolation + phantom welds -> fix design)

1. Weld grammar (fixes the 29-of-31 phantom already_inside): registry-minted stable ids (GenMem SID principle), provenance on every edge (EnSIMem index rows carry source turns), fail-closed edge creation with a rejection log (MemCodex admit/reject), lifecycle delete/supersede ops on rename (Stashbird). mag/knowledge_graph.py:237-239 currently does none of the four: it mints ids from `Path(str(m)).name` of free text and silently creates the target.
2. Isolation attack (1,204 isolated nodes / 41.3 percent): CoMemBench (unfetched, candidate list) measures memory sharing vs isolation across topologies; MemCodex shows the anti-isolation mechanism (derive-with-provenance + route). The estate's next graph pass should add the admit filter and rejection log before adding any more nodes.
3. Eval transplant for the biography shelf: DyadMem's G2P gap + capture/update/recall metrics port directly: gold-sample rows, measure recap Recall@n, update F1 on renames/supersessions, unsafe-deletion rate on stale facts.
4. Boot architecture: keep ribs as cell state and zknot as hidden state, but add the explicit output gate (LSTMem) so the recap is a readout policy over ribs, not a lossy re-summary.

## Honest gaps / OWED

- WebSearch rate-limited once upstream (429/1302); results still returned. No door 403.
- `rg`/`grep` unavailable in this bash (exit 127, `command not found`, twice); overlap counts are venv-python byte scans instead, instrument named above.
- ID-RAG (2509.25299) and Memory as Infrastructure (2609.05510) surfaced as prior art but are out of window and were NOT fetched; OWED a fetch if the estate wants the identity-graph prior-art line.
- Full HTML reads are via arXiv's experimental HTML render, transcribed by the fetch tool's reader model; quotes were flagged verbatim by that pass but byte-fidelity against the PDF is OWED for anything promoted into a rib.
- Candidates considered but not read this session (abstract-level API summaries only, NOT bankable): APDMem, Mnemon, CoMemBench, TWIST, CueMem, RIME, EMIR2, MemoryLACE, RoutePrism, GraphMemory, 2610.02897, CreaMem, RPMem, LifeFuse-Mem, MemAgent, JAM, PersMem, DolphinBench, Coding Agent Memory Post-training, Vestrum, TAGGRAPH.
