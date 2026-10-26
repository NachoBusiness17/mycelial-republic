# W3 RESEARCH: memory-augmented agents vs our multiscale memory

Item: w3-research-memai, flash50 lane, 2026-09-28. Question: who has built the closest thing to
our multiscale memory (permanent chain / weekly ribs / daily packs / context window), and what
promotion approaches do they use between scales? No em-dashes per law.

## 0. Method (what was actually run and read this pass)

- 9 WebSearch rounds (MemGPT/Letta, Mem0, "Rem" x4 disambiguation, Zep/Graphiti, LangMem, MIRIX,
  RMM, A-MEM, MemOS, Claude memory tool, EverMemOS, sleep-time compute, ChatGPT memory,
  MemoryBank/Generative Agents). Two rounds hit transient 429 rate limits and were retried.
- 5 WebFetch primary-source reads: arxiv.org/html/2504.19413v1 (Mem0 full text), arxiv.org/abs/
  2304.03442 (Generative Agents abstract), arxiv.org/abs/2505.13239 (turned out to be an
  unrelated QKD paper, falsifying a model-recalled citation), arxiv.org/abs/2602.13530 (REMem
  abstract), langchain-ai.github.io/langmem/concepts/conceptual_guide (full guide), plus the
  arXiv API query that identified REMem.
- Local grounding: Read mag/memory_consolidate.py:1-60 (verified the estate's own paper citations
  and constants at lines 3-5, 46-50); dir listing of memory/rib/ (45 rib files, 2026-08-10 through
  2026-09-28); Read of the sibling flash50 artifact deep-multiscale-memory.md (the estate-side
  scale map this file compares against; its code-path claims are cited to that file, not re-verified
  line by line here except memory_consolidate.py).

## 1. The yardstick (our four scales, as grounded)

From the ask, grounded against the estate this pass:

- S0 context window: the working set. Frozen byte-identical prefix + capped evolving tail
  (deep-multiscale-memory.md S0 row; mag/context_pack.py A2 law).
- Daily packs: hours-day scale budgeted pack layers (janitor 1,200 chars measured live in the
  sibling file's check 1), residual bonds (S1.5), quantizer law packs, pile case law (S2.5).
- Weekly ribs: memory/rib/, 45 files counted this pass, dated 2026-08-10 to 2026-09-28,
  judgment-tier doctrine injected at boot with a 2,800-char cap (context_pack _rib_doctrine, per
  the sibling file S3 row).
- Permanent chain: memory/biography/verkle_chain.jsonl, hash-linked append-only knots, 8,247
  knots / 5.78MB measured by the sibling artifact this pass, tip pointer + amend-not-erase law.

The signature property to test the field against: a tamper-evident permanent record, a
human/judgment-authored weekly tier, a compiled daily tier, and visible staleness on every
derived view (deep-multiscale-memory.md section 5), with promotion gated on recurrence and
pressure (mag/memory_consolidate.py:46-50 constants, verified this pass).

## 2. The survey (closest thing to ours, per system)

### 2.1 MemGPT / Letta (arXiv 2310.08560; docs.letta.com)

Scales: main context vs external context; inside that, core memory (always-visible free-text
blocks, now "memory blocks" in Letta), recall memory (searchable conversation log), archival
memory (vector store). Two tiers plus a third store, i.e. window + daily + permanent, but no
weekly/judgment tier and no hash chain.
Promotion: the agent itself pages between tiers via self-edit tools (core_memory_append/
core_memory_replace, archival_memory_insert/search). Self-editing is the promotion mechanism; the
estate's mag/memory_consolidate.py:12-13 implements MemGPT's other half, recursive summary folded
on memory pressure (PRESSURE_CHARS 8000 at line 46).
Background pass: "sleep-time compute" (Letta): a separate sleeptime agent shares memory blocks
with the primary agent and rewrites/consolidates them during idle periods (search coverage:
codepointer.dev, manthanguptaa.in summaries). This is the field's version of our day-end pile
habit and tide machinery. Verified at secondary-source depth this pass; the Letta blog itself was
not fetched (OWED-1).

### 2.2 Mem0 (arXiv 2504.19413, fetched full HTML this pass)

Scales: one long-term store per user/agent (text vector store), optional graph variant Mem0g.
Not multiscale by time; multiscale only by representation.
Promotion (verified verbatim this pass): a two-phase pipeline. Extraction phase: an LLM pulls
candidate memories from the new exchange. Update phase: top-s similar existing memories are
retrieved and the LLM chooses among exactly four operations: "ADD for creation of new memories
when no semantically equivalent memory exists", "UPDATE for augmentation of existing memories
with complementary information", "DELETE for removal of memories contradicted by new
information", "NOOP when the candidate fact requires no modification to the knowledge base".
Mem0g marks obsolete relations "invalid rather than physically removing them to enable temporal
reasoning". This is LLM-judged consolidation at write time: promotion happens at every message,
not on a cadence, and there is no permanent-vs-weekly distinction, no receipts, no staleness
rendering.

### 2.3 REMem (the "Rem" in the ask; arXiv 2602.13530, ICLR 2026 poster, verified via arXiv API this pass)

The ask's "Rem" resolved: after three ambiguous search rounds, the arXiv API query
ti:"Reasoning with Episodic Memory in Language Agents" returned exactly one entry: "REMem:
Reasoning with Episodic Memory in Language Agent", Shu, Jonnalagedda, Gao, Jimenez Gutierrez,
Qi, Das, Sun, Su, arXiv 2602.13530v3. A model-recalled candidate citation (arXiv 2505.13239) was
fetched and FALSIFIED: that id is a quantum key distribution paper (ORR), not REMem.
Mechanism (abstract depth this pass): two-phase framework. Offline: it "converts experiences
into a hybrid memory graph that flexibly links time-aware gists and facts". Online: "an agentic
retriever with carefully curated tools for iterative retrieval over the memory graph". Beats Mem0
by 3.4% and HippoRAG 2 by 13.4% on episodic recollection/reasoning, with "more robust refusal
behavior for unanswerable questions". Promotion between scales is not described in the abstract
(OWED-2): REMem is an indexing+retrieval architecture, not a cadence-based consolidator.

### 2.4 Zep / Graphiti (arXiv 2501.13956)

Scales: three subgraph tiers, episodic (raw interaction data), semantic (entity-relation edges),
community (summaries). Closest structural analog to our chain/ribs/packs layering, but tiers are
by content type, not by time horizon or authority.
Promotion: LLM extraction of entities/relations from episodes into the semantic tier; every edge
carries bi-temporal metadata (valid time t_valid, transaction time t_invalid); new contradictory
information invalidates old edges (t_invalid set) rather than deleting them, and the transaction
timeline consistently prioritizes new information for edge invalidation (search round 2 coverage
of the paper HTML, getzep.com, neo4j blog). Invalidated-not-deleted is the same spirit as our
amend-not-erase and soft-decay laws, achieved with timestamps instead of hash chains.

### 2.5 LangMem (LangChain; conceptual guide fetched full this pass)

Scales: window handled by the host agent; long-term store split semantic / episodic / procedural;
semantic stored either as a Profile (single schema document, "updates in place") or a Collection
(unbounded records searched at runtime). The Profile-vs-Collection split is a scale distinction:
profile is the "current state" shelf, collection is the archive.
Promotion: two formation modes. Hot path: "Active memory writing during conversation for
'immediate updates when critical context emerges'". Background: an LLM reflects after the fact,
"finding patterns and extracting insights without slowing down the immediate interaction". The
update loop: "The system must reconcile new information with previous beliefs, either deleting/
invalidating or updating/consolidating existing memories", with "a memory enrichment process that
strives to balance memory creation and consolidation". Multi-stage formation is explicit: managers
"consolidate and generalize from existing memories based on new conversation information", and
episodes feed semantic and procedural tiers (prompt optimizers turn feedback trajectories into
updated system-prompt rules). Retrieval weighs "importance" and "strength, a function of how
recently/frequently it was used". This is the field's most explicit episodic-to-procedural
promotion ladder, and procedural promotion (rewrite your own prompt/system rules) is the closest
published analog to our ribs being judgment-tier doctrine injected at boot.

### 2.6 MIRIX (arXiv 2025, Wang et al.)

Scales: six memory components: Core, Episodic, Semantic, Procedural, Resource Memory, Knowledge
Vault; each managed by dedicated manager agents within an eight-agent architecture, with active
retrieval on user input (search round 3 coverage: arxiv listing, marktechpost, mirix docs).
Multiscale by content class and by manager authority, not by time. Promotion: manager agents
route and rewrite between components (secondary-source depth; the per-component routing rules are
OWED-3). The Knowledge Vault is a notable tier the estate lacks as a distinct scale (operator-law
vs secret material separation lives in our ribs/contracts instead).

### 2.7 A-MEM (arXiv 2502.12110, NeurIPS 2025)

Promotion by network evolution: Zettelkasten note construction (atomic notes with keywords/tags),
automatic link generation between new and existing notes, and "Memory Evolution": existing notes
are continuously updated/refined as new knowledge arrives (search coverage + MCP implementations).
Promotion here is structural (grow the graph, refine old nodes) rather than cadence-based; closest
analog to our percolator repeat-detection, but A-MEM refines on every insertion with no recurrence
gate.

### 2.8 MemOS (MemTensor, open sourced 2025)

Scales: three memory representations unified by the MemCube abstraction: plaintext memory
(text, tree-graph managed), activation memory (KV cache state), parameter memory (weights).
Promotion: MemScheduler, "a predictive scheduling framework: based on the current conversation
and user profile, it proactively organizes and selects memory states (e.g. promoting plaintext to
activation memory) ahead of time" (search round 4 coverage). This is promotion between
representation scales (where a fact physically lives), the same axis as our window-vs-pack-vs-
chain placement; vendor benchmark claims (159% over OpenAI) unverified (OWED-4).

### 2.9 EverMemOS (arXiv 2601.02163, EverMind, Jan 2026)

Promotion: engram-lifecycle framing with explicit "consolidation and transformation (e.g.
episodic-to-semantic organization)" for "structured long-horizon reasoning" (search round 4
coverage + huggingface listing). This is the system our own code already cites for episodic-to-
semantic consolidation (mag/memory_consolidate.py:4, verified this pass), i.e. the estate judged
it the closest published mechanism for our S2.5 pile-to-case-law corridor. Full mechanism detail
not fetched (OWED-5).

### 2.10 RMM, Reflective Memory Management (arXiv 2503.08026, Mar 2025)

The only surveyed system whose paper names our problem in our terms: "prospective and
retrospective reflection mechanisms for managing memory promotion into a long-term store", plus
RL-refined retrieval (search round 3 coverage). Prospective = decide at write time what deserves
the long-term store; retrospective = re-judge after seeing how memory was used. Closest analog to
our two corridors (event-driven capture at session close = prospective; overnight pile
classification = retrospective), but learned with RL rather than receipt-gated.

### 2.11 Generative Agents (arXiv 2304.03442, abstract fetched this pass) and MemoryBank (arXiv 2305.10250)

Generative Agents: memory stream + retrieval by recency/importance/relevance + reflection:
agents "synthesize those memories over time into higher-level reflections" (abstract, verified
this pass; the importance-threshold trigger and 0.3/0.5/0.2 weights are implemented in our code
at memory_consolidate.py:48-50 but not stated in the abstract). This is the ancestor of every
threshold-triggered promotion above.
MemoryBank: Ebbinghaus forgetting-curve decay, "dynamically adjust memory strength according to
time and significance" (live search snippet via Springer coverage); day-level hierarchical
summaries reported in secondary coverage, not verified from the paper (OWED-6). This is the
demotion side (our soft-decay law), rarely the promotion side.

### 2.12 File-based production memory: Claude memory tool and ChatGPT

Claude memory tool: a file-based /memories directory in the client environment; the agent reads
and writes it with view/create/str_replace/insert/delete/rename commands; the client implements
storage; files persist outside the context window across sessions (search round 5 coverage of
secondary writeups; docs.anthropic.com not fetched, OWED-7). Mechanically this is the closest
published analog to our ribs + packs: markdown files the agent curates itself, with the client
(harness) as the storage authority. No hash chain, no staleness rendering, no cadence.
ChatGPT: two layers, "Saved memories are details that you explicitly ask ChatGPT to remember or
that ChatGPT saves as useful context" (help.openai.com snippet, live this pass) plus reference
chat history (retrieval over past conversations). Promotion = the model's own save decision or an
explicit user save; the thinnest promotion mechanism surveyed.

### 2.13 Sleep-inspired consolidation cluster (SCM, rem-sleep, OpenClaw REM phase)

SCM "Sleep-Consolidated Memory" (arXiv 2604.20943, surfaced via search, not fetched), the
rem-sleep Claude Code skill (thdelmas) with NREM cluster-and-merge plus REM high-noise
associative recall, and OpenClaw's claimed "Light Sleep -> REM Sleep -> Deep Sleep" phases with
"promotion to permanent long-term storage" (skywork coverage, single source). Cluster: offline
consolidation passes at sleep-like boundaries. Verified only at search-snippet depth (OWED-8);
noted because the metaphor cluster (sleep phases = consolidation cadences) is the field converging
on our day-end pile / tide / overnight classify cadences.

## 3. Promotion-mechanism taxonomy (the ask's second question)

Every surveyed mechanism reduces to one of nine families:

1. LLM-judge consolidation at write time: Mem0 ADD/UPDATE/DELETE/NOOP (verified verbatim),
   LangMem reconcile loop. Promotion is continuous and cheap to bolt on, but has no cadence and
   no authority ladder.
2. Self-edit paging: MemGPT/Letta core block tools; agent moves facts itself between tiers.
3. Threshold-triggered reflection: Generative Agents importance threshold; MemGPT pressure fold
   (our PRESSURE_CHARS 8000 at memory_consolidate.py:46).
4. Offline/sleep consolidation pass: Letta sleep-time agents, SCM, rem-sleep, OpenClaw phases,
   MemOS MemScheduler (predictive variant). Time-bound or idle-bound reorganization. This is the
   field's answer to our daily packs + day-end pile.
5. Temporal invalidation: Zep bi-temporal edges; Mem0g invalid-not-deleted. Contradiction
   handling by timestamp, the weak version of our amend-not-erase + hash chain.
6. Decay/forgetting: MemoryBank Ebbinghaus; our 0.995/hr soft decay (memory_consolidate.py:48).
   Demotion-side only.
7. Network evolution: A-MEM note refinement and linking; graph grows and self-organizes on each
   insert.
8. Index-then-retrieve: REMem hybrid memory graph + agentic retriever; HippoRAG 2 (compared in
   REMem's abstract). Promotion into scale levels is absent; effort moves to retrieval reasoning.
9. Learned promotion: RMM prospective/retrospective reflection with RL-refined retrieval; the
   only system that trains the promotion decision.

Not one surveyed system uses recurrence-gating (a signal must be seen twice before it may be
promoted) as the promotion test; that is the percolator's law and it has no published twin found
in this sweep. The closest is A-MEM's evolution (no gate) and Generative Agents' threshold
(judged importance, not observed recurrence).

## 4. Verdict: who is closest to permanent-chain / weekly-ribs / daily-packs / window

- Closest single system by tier shape: Letta/MemGPT (window + always-visible core + searchable
  recall + archival, plus sleep-time background reorganization). It has three of our four scales
  and a live promotion mechanism, but nothing permanent-or-tamper-evident and no weekly judgment
  tier.
- Closest by promotion-ladder completeness: LangMem (episodic -> semantic -> procedural with
  explicit hot/background split and profile-vs-collection shelves).
- Closest by philosophy: Zep/Graphiti (invalid-not-delete, provenance from episodes) and EverMemOS
  (engram lifecycle, already cited in our own code).
- Closest to the rib layer specifically: Claude's file-based memory tool (agent-curated markdown
  under client authority) and LangMem procedural memory (system-prompt rules that evolve). No
  surveyed system separates a human/judgment-authored weekly doctrine tier from machine-compiled
  daily packs the way ribs vs quantizer packs do.
- Closest to the chain specifically: nothing. No surveyed system advertises a content-addressed,
  hash-linked, append-only permanent memory with a tip pointer, amend-not-erase, anchored
  operator-gated compaction, or staleness rendered in-band on derived views. The negative claim is
  scoped to this sweep: I searched for promotion and tier mechanisms, not exhaustively for
  "immutable ledger" keywords, and Mem0g/Zep's invalidation timestamps are the nearest neighbor.
- The sleep-consolidation cluster (Letta sleeptime, SCM, our tide/pile) is where the field and the
  estate independently converged: promotion needs a cadence, and the cadence everyone picked is
  "when the agent is otherwise idle".

## 5. OWED register (unverifiable from this pass, not filled with guesses)

- OWED-1: Letta sleep-time compute details from Letta's own blog/paper; secondary coverage only.
- OWED-2: REMem's hybrid memory graph node/edge schema and update/promotion policy; abstract only.
- OWED-3: MIRIX per-manager routing rules (which manager promotes what into which component).
- OWED-4: MemOS benchmark claims (159% temporal reasoning over OpenAI; +5.26% LoCoMo); vendor
  claims, untested here.
- OWED-5: EverMemOS full consolidation pipeline; search-level coverage only (our own code cites it).
- OWED-6: MemoryBank day-level hierarchical summarization; secondary coverage, paper not fetched.
- OWED-7: Claude memory tool from docs.anthropic.com directly; secondary writeups only.
- OWED-8: SCM (arXiv 2604.20943), rem-sleep skill internals, OpenClaw REM-phase claim; search
  snippets only, single sources.

## 6. Sources

Primary (fetched this pass): arxiv.org/html/2504.19413v1 (Mem0); arxiv.org/abs/2304.03442
(Generative Agents); arxiv.org/abs/2602.13530 (REMem); langchain-ai.github.io/langmem/concepts/
conceptual_guide (LangMem); export.arxiv.org API query (REMem identification); arxiv.org/abs/
2505.13239 (falsified REM candidate).
Secondary (search-result coverage this pass): arxiv.org/html/2501.13956v1 + getzep.com + neo4j
blog (Zep/Graphiti); arxiv.org/abs/2503.08026 (RMM); arxiv.org/abs/2502.12110 (A-MEM); MemTensor
MemOS coverage; arxiv.org/abs/2601.02163 + huggingface (EverMemOS); memx.app + docs.letta.com
coverage (MemGPT/Letta); codepointer.dev + manthanguptaa.in (sleep-time compute); arxiv.org/html/
2604.20943v1 (SCM); help.openai.com/en/articles/8590148 (ChatGPT memory); docs/mirix-ai.github.io
+ marktechpost (MIRIX); Springer coverage (MemoryBank); skywork.ai (OpenClaw REM phase);
docs.anthropic.com coverage via jakegoldsborough.com (Claude memory tool).
Estate-side (read this pass): mag/memory_consolidate.py:1-60; memory/rib/ listing (45 files);
watch/inbox/burn_reset_20260927/flash50/deep-multiscale-memory.md (sibling artifact).
