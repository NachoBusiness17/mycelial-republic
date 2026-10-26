# SWEEP: agent-memory-continuity via arXiv (2026-10-10)

source-fetched: 2026-10-10. Seat: sweep-agent-memory-continuity-arxiv (dynamic workflow
dwfrun, area agent-memory-continuity). All eight banked items were fetched and read by this
seat this session; nothing is ask-carried.

## Doors status (run this session)

- arXiv export API (Atom XML): first two queries via WebFetch rendered green; the next two
  WebFetch calls TIMED OUT at 60s (twice). Per recipe fallback, the remaining six queries,
  all eight abs pages, six full-text HTML pages, and one PDF were fetched via curl over
  HTTPS (same arxiv.org door, different client; every curl exit 0, byte counts logged in
  `_tmp/`). No door 403ed. No fallback success is fabricated.
- WebSearch: not needed (API door carried the sweep); the day-9 seat hit WebSearch 429s, so
  this seat did not spend it.
- Recipe listing pages (/list/cs.CL/recent, /list/cs.LG/recent): NOT fetched; the export API
  with sortBy=submittedDate covered the new-listing function for the same window (same
  honest substitution the 09-30 and 10-01 sweeps recorded).

## Pass 1: broad sweep (30+ in-window candidates)

Eight export-API queries, all fetched this session (WebFetch 2 + curl 6):

1. abs:"skill library" OR abs:"skill induction" OR abs:"procedural memory" - 25 entries.
2. abs:"agent memory" AND cat:cs.CL - 30 entries.
3. abs:"world model" AND (abs:"specification" OR abs:"contract" OR abs:"declarative") - 25.
4. abs:"novelty" AND (research literature / literature review / prior work) - 25.
5. abs:"progressive disclosure" OR abs:"lazy retrieval" OR abs:"on-demand retrieval" - 20.
6. abs:"contradiction" AND abs:"knowledge graph" AND abs:"agent" - 18.
7. abs:"memory consolidation" AND abs:"agent" - 20.
8. abs:"route" AND abs:"memory" AND abs:"boot" - 1 (nothing on-point).

Roughly 160 entries returned, deduped to ~120 distinct titles; well over 30 sit inside the
2026-09-10..10-10 window. In-window shortlist beyond the banked eight: APDMem 2610.02472
(cataloged mirror row; agent-controlled progressive disclosure, the middle point between
harness-driven PD and runtime research; NOT banked, see overlap law), CADOC 2609.37012
(cache-aware dynamic object context), Router Within 2609.15982 (native skill routing from a
frozen LLM), Cartograph 2609.30293 (federated tool discovery), MemProbe 2609.30558
(stability-plasticity cognitive paradigms), DolphinBench 2609.24971 (cataloged mirror row;
Pareto frontier of agent memory), SkillGATE 2610.05489, TeleTune 2610.05437, SkillForge
2610.09832, EnSIMem 2609.27279, CAMG 2609.34422 (banked by the 09-30 sweep, not re-banked),
MemCodex 2609.39765 (full-read by the 10-01 seat, not re-banked), SAGE 2605.30711 (novelty
gate for memory evolution; 134 days old, outside window, named here so a future window with
a novelty-check ask can pull it), MemoryLACE 2609.03201 (lifecycle-aware consolidation
distinguishing updates from unresolved contradictions; 38 days old, just outside window,
same note).

## Pass 2: deep reads (8 items; 7 read end to end)

Fetched and read this session: full-text HTML for Skill-V, Memory-Skill Isomorphism, MemoWM,
SkillSpec, JAM, and the Workday progressive-disclosure report (short form, read whole);
EngramBench had no HTML rendering ("Untitled Document" page), so its 19-page PDF was
downloaded and text-extracted (pypdf, pages all read). Lineage-Aware Governance was read at
abs-page tier only (abstract in full); it is banked as the eighth item with that tier
marked. The 5-end-to-read floor is cleared twice over.

### 1. Skill-V: Verifiable Self-Evolving Skill Library (2610.11781, 2026-10-08)

Skills are "versioned, falsifiable contracts that link semantic intent to observable
behavioral criteria". The write gate is deterministic: "Language-model proposals are never
committed directly. Skill-V first verifies the contract schema, unique criterion
identifiers, allowed matcher types, criterion weights and severities,
criterion-to-procedure traceability, source skill identity, and monotonically increasing
versions", then performs shadow replay over the observed evidence pool with non-regression
criteria before commit. The read gate is an applicability filter: semantic retrieval alone
caps success at 71.9% vs 95.3% full, and the judge "labels 29.6% of retrieved candidates as
confidently inapplicable". Limitations read: no skill deletion (only boundary tightening),
and historical dependency: replay evidence goes stale when environment rules change, cure
named as time-weighted buffers (the same revert trap day-9's When Old Facts Return proved).
ALFWorld 95.3 / WebShop 85.9.

Q1+Q4: this is the chain model the 6 placeholder superseded_by rows want: monotone
versions + protected semantic constraints + replay-verified non-regression + read-side
applicability. Q2: the applicability filter is the false-already_inside-edge guard.

Overlap: zero hits in catalog/catalog.jsonl, memory/ (git grep), corpus/steal/, and every
prior watch/inbox sweep. Fully new.

### 2. Report: Progressive Disclosure of Agent Skills (2609.35692, 2026-09-28, Workday AI)

The route-map pattern measured in production shape: declare frontmatter of all N skills,
emit {"action":"load_skill","name":...}, load one body on trigger. Findings (Qwen2.5-7B /
Qwen3-8B / Qwen3-14B, N in {5,20,50,100}, 576 rollouts per core): "Progressive disclosure
demonstrates increasingly bigger token savings as N grows, up to 81.7% of tokens originally
used in the eager loading regime"; eager loading crashes 100% of rollouts at N=100 while PD
crashes zero; eager retrieval quality collapses (Qwen3-14B 1.00 at N=5 to 0.125 at N=50);
BUT latency rises 15% (1.75 to 2.01s at N=50) and one cell regresses (Qwen3-8B at N=20: PD
0.38 vs eager 0.68 success), so "neither regime consistently outperforms the other".

Q3: the production replication of the route-map 25x boot cut AND its failure conditions:
small libraries (N=5 savings 0.5-41%), weak routing models, latency-sensitive loops, and
single-skill tasks (their setup loads exactly one skill; multi-skill tasks untested).

Overlap: catalog/catalog.jsonl carries the daily-mirror row for the ID (grep hit, plus
tags.jsonl); zero sweep/steal/register/DIGEST mentions in any prior window; first deep read
and first bank. The mirror row is the estate's own daily abstract ingest, not a banked find.

### 3. Memory-Skill Isomorphism: One Skill Carrier, Two Native Uses (2609.16669, 2026-09-15)

The already_inside question answered as architecture: memory is not a service beside the
skill system; it IS a skill directory read by the same mechanism. Levels: resident
description (hot cues, governed 1,024-character cap) -> on-demand body (colder index plus
curation policy) -> reference/*.md (detailed memories); "The map phi reuses mounting,
routing, loading, and supporting-file lookup rather than building a second memory
retriever". Writes fork: "Historical evidence must preserve provenance, so it is appended.
Current procedures must track the best known state, so they are replaced and then
revalidated." Governance is the honest center: 4 write entries exist, only 1/4 reaches the
settlement ledger; priced operating point: one L1 lesson point adds 1,313 first-turn tokens
vs a 1,462-token baseline, 4,949 at k=5, session totals 1.18x; the paper repeatedly marks
its own evidence underpowered/selected (Fisher p=1.0, post-selection existence signal).

Q2: the already_inside automation is a shared read carrier with forked writes, not a
cross-linking job; Q1: the fork law is the supersession write semantics in carrier terms;
Q3: the 1,024-char resident cap is the boot_routes.md shape with a governed budget.

Overlap: zero hits anywhere (ID and title phrase). Fully new.

### 4. MemoWM: How World Models Change What Agents Need to Remember (2610.10778, 2026-10-07)

Formalizes memory allocation conditioned on a world model: an action-conditioned predictor
reconstructs omitted coordinates, and "A coordinate is retained when the expected task
impact of omitting it exceeds its predicted storage cost; otherwise, the model prediction
fills it." Writer and decoder share the same reconstructed history so selective omission
stays decodable. Results: 42.42% average accuracy across five long-term memory benchmarks
(+2.62 over best baseline) with 53.9% less experience-specific storage than MIRIX;
stronger world models cut per-experience storage at comparable quality; impact-selected
coordinates do ~1/166-1/176 the counterfactual damage of random ones; and the capacity
that minimizes total storage grows as more interactions are retained.

Q5: the world-rib contract's memory-side complement: a fact needs storing only when it has
"downstream value beyond the predictive prior"; the estate's re-derivable-territory guard
is the same law from the territory side. The shared-reconstruction discipline (one
re-derivation path for writer and reader) is what warm boot plus verkle restore must
guarantee; mag/context_pack.py restore_shed_section's sha check already approximates it.

Overlap: ID appears only in the day-9 x-sweep 25-row in-window census list
(frontier_olm_2026-10-09/sweep/agent-memory-continuity-x.md:17); never banked, never deep
read. Zero catalog/memory/corpus hits. This is the first read and bank.

### 5. SkillSpec: Consensus-Gated Agent Skill Evolution via Representation Specialization (2610.00704, 2026-09-30)

Two-phase: consensus-gated evolution then representation specialization. "An update is
committed only when paired evaluations reach consensus, requiring sufficient overall
improvement and non-negative aggregate paired gain in every repeated evaluation." Phase two
estimates process sensitivity (ordered-step dependence) and redundancy sensitivity from the
full optimization trajectory including rejected candidates, then selects flat, graph, or
hybrid representation; "The validated backbone remains immutable, while a derived artifact
is initialized and specialized in the selected representation." +6.89% average over SkillOpt
across three models; up to +24.59% over no-skill.

Q4: schema v3's per-node representation choice (when does a steal need graph edges vs a
flat row) gets measured signals, not vibes; the immutable-backbone-plus-derived-artifact
rule is supersession write discipline; the paired-gain-in-every-repeat gate is the
hysteresis MINDSET described, made cheap.

Overlap: zero catalog.jsonl hits for the ID; one token match in catalog/receipt_fts.sqlite
(derived FTS index artifact, no catalog row); zero memory/corpus/sweep hits. New.

### 6. EngramBench: A Capability-Grounded Benchmark for Skill-Evolution Harnesses (2609.39284, 2026-09-30)

Names the exact disease behind "122 orphan steals, ~87 percent blind": "current evaluations
of skill evolution in autonomous agents suffer from a critical identifiability problem:
they structurally confound genuine capability abstraction with rote solution leakage".
Axiom: capability overlap without solution overlap; 30 learning tasks, 13 unseen transfer
tasks, 48 multi-hour trajectories. Finding: static skill banks do not bypass the "last
mile" of exact implementation but act as an execution compass: without them, LLM invocations
spike 68.97%, reasoning tokens 131.76% (nearly 700k), error logs flood 14.76M characters
forcing 26 compactions; with them, coding time drops over 55%.

Q4: the novelty check the sweep should run against orphans: each steal needs a capability
fingerprint (what it does) distinct from its solution text (what it copies), and a wiring
counts only when capability overlaps without solution overlap.

Overlap: zero hits for ID and title phrase anywhere. Do not confuse with EngramRAG
2609.32049 (different paper, banked by the 09-30 sweep). New.

### 7. JAM: Just-In-Time Agent Memory with Runtime Agentic Research (2609.34385, 2026-09-28)

The ahead-of-time critique: "While this reduces online serving cost, such request-agnostic
memory construction can discard fine-grained information that later becomes important."
Memorizer keeps complete raw histories in a hierarchical page-store with compact
navigational summaries; a trained Researcher retrieves/inspects/integrates per request
(verified-trajectory SFT then Hint-guided GRPO on Memory-Gym synthesis). Beats AOT-style
memory systems at 79.53s one-time workspace construction (A-MEM 200.42s, Mem0 90.67s,
MemoryOS 41.36s, LightMem 6.82s), with query-time latency above one-shot systems; action
budget 5 -> 20 keeps improving with diminishing returns.

Q3: the boundary condition for route-map generalization: a precompiled index pays only
while the fine-grained record it compresses stays recoverable; the zknot recap and
warm_state.json carry operator intent whose loss is exactly JAM's failure case. The estate
shape that satisfies both: raw always on disk (page-store), route map resident, zoom
restore on trigger (already the context-pack shed pattern).

Overlap: named in the 09-30 sweep pass-1 census and abs-read then passed over by the 10-01
seat ("2609.34385 JAM (09-30 sweep pass-1, passed over)"); never banked, never full-read.
This is the first full-text read and first bank; the Q3 framing is new.

### 8. Lineage-Aware Memory Governance (2610.07258, 2026-10-05) [abstract-tier bank]

Introduces the Analytical Memory Unit: "a memory schema that attaches a full derivation
(lineage) graph to every cached result, gated by a retrieval policy that serves a hit only
when the requester is authorised for every column touched". Proof by construction that
lineage-gated retrieval blocks derivatively-sensitive leaks at O(n) worst case; eliminating
measured leakage required 75-90% recorded lineage completeness (90% deployment target);
removes 18.8-25.5% cross-department leakage at 13.8 microsecond overhead, keeping
81.5-82.6% of memory reuse; real-agent PoC: zero leaks over 9 round-trips, two conflicting
KPI logics caught automatically.

Q4+Q1: derivation-lineage edges are the tension/provenance link schema v3 needs: every
derived row (a steal, a supersession edge, a digest claim) should carry its derivation
graph, and the read side gates on lineage completeness, not content similarity.

Overlap: named once in the day-8 pass-1 census (frontier_olm_2026-10-08/sweep/
agent-memory-continuity-arxiv.md:7); not among day-8's 8 banked items; zero catalog/memory
hits. Read at abs-page tier only this session; full-text read OWED to the next window that
acts on it.

## Answers to the five research questions (compressed)

- Q1 (read-path contract): the day-9 contract gains its missing mechanical legs. Write
  side: Skill-V's deterministic schema-validation + shadow-replay + non-regression commit
  gate over monotonically versioned records; SkillSpec's consensus gate (paired gain
  non-negative in every repeat); Isomorphism's fork (append evidence, replace-and-revalidate
  state). Read side: applicability filtering (Skill-V: 29.6% confidently inapplicable;
  71.9% -> 95.3%) and lineage gating (2610.07258). Yes, the 6 placeholder rows can become a
  real chain: version + protected constraints + replay evidence + applicability flag.
- Q2 (already_inside automation): Memory-Skill Isomorphism: one carrier, shared read,
  forked writes; the link stops being a second retriever. EngramBench supplies the
  admission test (capability overlap without solution overlap); Skill-V's applicability
  judge keeps false edges out (missed-merge over false-merge, day-9's asymmetry, holds).
- Q3 (route-map 25x): generalizes with four conditions (Workday: savings grow with N; crash
  wall at N=100 eager-only; quality holds) and fails on small libraries, weak routers
  (Qwen3-8B N=20), +15% latency loops, and index-loss of fine-grained intent (JAM). The
  estate port is boot_routes.md PLUS the always-on-disk raw record PLUS sha-verified zoom;
  route map alone is not a memory, it is an index over one.
- Q4 (schema v3): four carries: per-node representation signals (SkillSpec process/
  redundancy sensitivity; GraphMemory Beta-posterior weights, day-9), supersession typing
  (Skill-V contract fields + monotone versions), derivation/tension links (2610.07258
  lineage graphs; MELD conflict-keep, day-9), and the capability-vs-solution split that
  makes a novelty check against the 122 orphans computable (EngramBench axiom).
- Q5 (world-rib): MemoWM: store only what exceeds the predictive prior; capacity that
  minimizes total storage grows with retained interactions; writer and decoder must share
  one reconstruction path. The rib schema needs derivable-from flags, reconstruction-cost
  bounds, and the shared-reconstruction discipline; a compiler-without-territory cannot
  express derivation direction or reconstruction cost at all.

## Checks run this session

- 8 export-API queries (WebFetch 2 green, 2 timed out, 4 via curl), 8 abs pages, 6 full-text
  HTML pages, 1 PDF (19 pages, pypdf-extracted), all curl exit 0; byte counts in _tmp/.
- Overlap: grep -c per ID over catalog/catalog.jsonl; git grep -l -F per ID and per title
  phrase over memory/ catalog/ CORPUS_CATALOG.md corpus/steal/ watch/inbox/ (prior windows
  only). A full recursive grep over memory/ was started, found too slow against telemetry
  jsonl, and was replaced by the tracked-files git grep; both facts recorded.
- Lens grounding read: frontier_olm_2026-10-10/lens/questions.md (area 3 = this ask's five
  questions), lens/graph.md (2026-10-09), lens/burns.md sections 2b/2c, day-9
  sweep/steal/register files, night_cools_20261010/grokbot_finds.md (route-map find),
  lens/laws.md open q4 (world-rib contract).
- Not run: any pytest (nothing in-tree changed); the estate's numbers (6 superseded_by
  edges, 140 steals, 18 already_inside, 122 orphan steals) are taken from the ask's lens
  inputs, not re-counted.
- Hygiene: no em-dashes; every quote verbatim from a page fetched this session (LaTeXML
  math-duplication normalized only in the PD 81.7% figure).

## OWED

- Lineage-Aware Governance full-text read (banked abstract-tier).
- SAGE 2605.30711 and MemoryLACE 2609.03201: out-of-window papers directly on the novelty
  gate and lifecycle-aware consolidation; a future window with that ask should pull them.
- APDMem 2610.02472: cataloged mirror row, agent-controlled progressive disclosure; read it
  before any route-map port so the agent-controlled variant is not reinvented.
