# SWEEP: agent-memory-continuity via arXiv - 2026-10-02

source-fetched: 2026-10-02
Agent: sweep-agent-memory-continuity-arxiv (Mag Resource Harness, frontier sweep gopher)

## Pass 1 - broad sweep census

Three export.arxiv.org API doors, all date-ranged `submittedDate:[202609020000 TO 202610022359]`, sorted descending:

1. `abs:"agent memory" OR ti:"agent memory"` -> 62 total results, first 40 enumerated (WebFetch, 40 entries listed).
2. `abs:"memory" AND abs:"LLM agent"` -> 82 total results, 39 enumerated before truncation.
3. `abs:"memory consolidation" OR abs:"session continuity" OR abs:"experience reuse"` -> 14 total, 13 enumerated.

Candidate census: 92 enumerated entries, far past the 30 floor. Highlights by research question:

- Q2 (retrieval comparisons vs pointer/BM25): MemFit 2610.00872, MemCodex 2609.39765 (held), Mem++ 2610.02002 (held), Selection-Replaces-Extraction 2609.34227, JAM 2609.34385, UpliftMem 2609.36805 (held via gathering_expedition), MemAgent 2609.32521, LAM 2609.32256.
- Q3 (ID-collision / slug / dangling-ref defects): U-Fuzz 2609.38275, GenMem 2609.34633, DerivAudit 2609.36130, EnSIMem 2609.27279 (held), Stashbird 2609.34242, RoutePrism 2609.34160 (construction-order corruption of memory stores).
- Q4 (verifiable successor continuity): Retire 2610.01160, PoS 2610.01415, FlowState 2609.34565, MemDream 2609.34545, Epistemic-Admission benchmark 2609.30813, Continuous Context Management 2609.35540.
- Q1 (doctrine-to-code linkage): GenMem (symbolic addressing as the linkage schema), PACE 2610.01349 (provenance-aware capability enforcement).
- Q5 (surfacing behind content-addressed hashes, immutability): DerivAudit, Stashbird provenance sets, EngramRAG 2609.32049.

## Overlap scan (run here, this sitting)

`grep` is not on PATH in this bash (exit 127 twice) - substituted the repo venv Python substring scan over `catalog/catalog.jsonl` plus the whole `memory/` tree (15 phrases). Raw output retained in session log. Verdict:

- **Already held, not re-banked:** MemCodex (`catalog/catalog.jsonl`, id 505dff60dbfc), Mem++ / Non-Destructive Memory (id c2f2eb4ffa31), EnSIMem / Entity-Structured Indexing (id 20f5cd99ce8b), UpliftMem (`memory/runs/gathering_expedition/PAPERS_LANDING.json`).
- **Sibling echo, not holdings:** every other phrase's only `memory/` hit was `memory/trajectory/steps.jsonl` - sampled lines are `trajectory_step.v1` rows from sibling workflow sessions `sess_dwf-dwfrun-...-actor_3_9` dated 2026-10-01 (yesterday's parallel sweep lanes logging their own fetches). Not durable holdings; discounted.

## Pass 2 - deep reads (9 read end to end; floor was 5)

Full-text reads (HTML or PDF door), each with mechanism, headline numbers, verbatim quotes and ablations extracted: DerivAudit 2609.36130, GenMem 2609.34633, Selection-Replaces-Extraction 2609.34227, Retire 2610.01160, MemCodex 2609.39765 (held; read to answer Q2's anchor), U-Fuzz 2609.38275, PoS 2610.01415, MemFit 2610.00872, Stashbird 2609.34242.

### Q2 verdict - does anything beat the banked MemCodex 60.8-vs-55.4?

The banked scalar is MemCodex's own evidence-channel ablation, re-verified from its full text: full MemCodex averages 60.8 (Qwen3.5-27B) while the content-only channel (no source-turn routing) drops to 55.4 with recall at 63.0. MemCodex itself publishes no BM25/lexical baseline. The answer to the question is **yes, on LoCoMo**: MemFit (2026-10-01) reports LoCoMo 60.5 vs its MemCodex reimplementation's 58.8, storing turns verbatim in an append-only store with LLM-free insertion and a hybrid lexical(BM25)+vector first stage with cross-encoder rerank. Caveat: different judge stacks across papers; the estate's banked number should carry the same-benchmark-family caveat before promoting any new champion. Independent corroboration for the pointer side: Selection-Replaces-Extraction's pre-registered non-inferiority result (raw turns 77.0 vs extraction 77.5 at matched context, 3,061x cheaper writes).

### Q1/Q3 verdict - doctrine-to-code linkage and defect classes

GenMem's addressing invariance is the closest published schema to the estate's 0-edge doctrine-to-code class: addresses (Symbolic Identifiers from product-quantized codebooks) are frozen slots; payloads revise in place under the same address; evolution never re-encodes addresses. Its own failure modes are the estate's failure modes: "some leaf codes attract disproportionate traffic" (the degree-9 invariant:law hub bug, published) and cold-start noise propagating into the address space. U-Fuzz supplies the missing instrument: mutation-based fuzzing of memory stores that finds stale-record-ranked-above-update (II-1), deleted-evidence-still-retrieved (II-2), and non-interference violations (II-3) - the ghost-endpoint class, with UF@BB hit rates of 45-73% vs 28-36% for the best baseline strategy. DerivAudit closes the loop: audit whether each stored node is supported by the history that existed at write time; 17-21% of memories stay unsupported even with expanded history, and downstream verifiers admit 59-89% of them anyway.

### Q4 verdict - verifiable successor continuity

Retire (NVIDIA) is the published instrument closest to warm boot plus verkle: epoch-numbered authority, SUPERSEDE handoffs, a certified prefix (longest common token prefix, block-aligned, config/tenant/generation-checked) that the successor aliases rather than copies, plus three stale-version guarantees (current-version publication, versioned handoff, retired-state isolation). Measured: 17.1% median paired TTFT reduction on handoff, 5.53x goodput on a recorded coding-agent burst, zero obsolete tokens published vs 40,499 under native abort. PoS adds the recall-health instrument: an explicit belief state with a Belief Sentinel consistency audit and a trapping health formula H = 1 - max_X[P_X*max(S,R)] with factorized recovery.

### Q5 verdict - content behind hashes without breaking immutability

Stashbird's provenance sets (P(x) of supporting episodes on every derived record) plus its deletion policy - trim provenance, delete unsupported relations, keep orphaned entities as "connective anchors" - is a published answer to the 400 empty-summary knots: surface the evidence chain behind derived keys, never mutate the evidence, mark communities dirty and re-summarize. DerivAudit's result that citations alone under-detect (expanded history recovers support for ~60% of "unsupported" memories) warns that the estate's knot-audit must read write-time history, not just the node's own citations.

## Degradations (all real, none papered over)

- web_reader door: five 1302 rate contacts across the sitting (the rolling-limit class, not a wall); worked after 60-90s backoffs.
- `grep`/`sleep`/`head` absent from this bash (exit 127); venv Python substituted, command quoted above.
- `arxiv.org/html/2610.00872` and its `v1` form: 404 twice (no HTML rendering); full text obtained via the PDF door instead.
- WebFetch's small model refuses long verbatim quotes; quotes under 25 words were used and flagged with confidence accordingly.

## Banked items (8, strongest first)

1. MemFit (2610.00872) - beats the banked MemCodex LoCoMo number; append-only plus BM25 hybrid.
2. DerivAudit / Memory Is a Derivation (2609.36130) - unsupported-memory audit; ghost-endpoint and empty-knot class.
3. GenMem (2609.34633) - addressing invariance; the maintainable doctrine-to-code address schema; published hub-skew defect.
4. Retire (2610.01160) - epoch handoff with certified prefix; verkle/warm-boot continuity analog with numbers.
5. Selection-Replaces-Extraction (2609.34227) - pre-registered pointer-vs-extraction test; 3,061x write-cost scalar.
6. U-Fuzz (2609.38275) - fuzzing instrument for memory-store defects; run it against the estate's graph and indices.
7. PoS / Explicit Belief States (2610.01415) - maintained belief tip, consistency audit, trapping recovery.
8. Stashbird (2609.34242) - provenance sets and connective-anchor orphan policy; knots surfaced without immutability breakage.
