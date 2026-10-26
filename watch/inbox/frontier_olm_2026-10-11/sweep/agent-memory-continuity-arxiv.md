# SWEEP: agent-memory-continuity via arXiv (2026-10-11)

source-fetched: 2026-10-11. Seat: sweep-agent-memory-continuity-arxiv (dynamic workflow dwfrun,
area agent-memory-continuity). All seven banked items were fetched and read by this seat this
session (arxiv.org full-text HTML per item); nothing is ask-carried. ASCII only, no em dashes.

## Doors status (run this session)

- export.arxiv.org API (Atom XML) via WebFetch: GREEN. Seven queries fired, all rendered
  (agent memory + cs.AI; long-term memory + LLM agent; memory + skill library; memory
  consolidation + cs.CL; shared memory + multi-agent + cs.MA; experience/trajectory reuse;
  memory drift/stale/update + cs.CL). One eighth query (lifelong + agent) timed out at 60s
  and was not retried. No 403s, no 429s. The agent-memory query alone returned 25 in-window
  entries, 17 of them unswept.
- Recipe listing pages (arxiv.org/list/cs.CL/recent, /list/cs.LG/recent): NOT fetched. The
  export API with sortBy=submittedDate covered the new-listing function for the same window;
  same honest substitution the 10-10 seat recorded. No fabricated fallback.
- WebSearch: not used; the API door carried the sweep.

## Pass 1: broad sweep (38 distinct candidates, window 2026-09-11..2026-10-11)

Query return sets deduped to 38 in-window candidates not previously swept, including:
2610.10265, 2610.09348, 2610.08048, 2610.07311, 2610.07782, 2610.03020, 2610.02150,
2610.06830, 2610.07657, 2610.07257, 2610.07261, 2610.05700, 2610.00238, 2609.36373,
2609.35233, 2609.34633, 2609.34372, 2609.34242, 2609.34132, 2609.32521, 2609.32256,
2609.32091, 2609.32584, 2609.38353, 2609.34988, 2609.34988-sibling 2609.33180, 2609.32630,
2609.33517, 2609.37930, 2609.36976, 2609.34603, 2609.23466, 2609.16053, 2609.14168,
2609.12655, 2609.28078, 2610.06879, 2609.33243. Outside-window anchors named, not banked:
2609.01852 The Memory Trust Gap (2026-09-01, stale stored facts override authoritative
evidence, capability-dependent; the RQ1 prior-art anchor), 2609.05510 Memory as
Infrastructure / SIx Harness (2026-08-31, months-scale persistent-memory ops record),
2609.04869 From Interaction Traces to Persistent Skills (2026-09-04).

## Pass 2: deep reads (7 items, all full-text HTML, read end to end)

Every item below was fetched this session from arxiv.org/html/<id>v1 and read in full.
Abstract pages also fetched for 2610.10265 and 2610.07311. SEVEN end-to-end reads; the
5-read floor is cleared.

## Overlap law outcomes (commands run this session, not assumed)

- grep per ID over catalog/catalog.jsonl (1,136,889 rows): zero rows for 2609.33517,
  2610.00238, 2609.32091, 2609.32521, 2609.23466; state/arxiv mirror stubs only (abstract
  ingest, no why layer) for 2609.34603 and 2609.34988; plus a bare root fetch artifact
  abs_2610.10265.html (mtime 2026-10-09) for the dropped item.
- grep per ID + title fragment over watch/inbox/*/sweep/*.md, watch/inbox/*/steal/,
  watch/inbox/*/register.jsonl, watch/inbox/*/DIGEST.md, memory/rib, memory/press,
  memory/research_packs, memory/frontier, memory/improve, corpus/steal/: zero for the five
  zero-catalog items; one no-claims pass-1 census listing for EvoCUE (disclosed below).
- DROPPED as re-banks (found by the overlap greps, not re-verified by re-read): 2610.07311
  MEMTRIM (banked item 3, frontier_olm_2026-10-07/sweep/agent-memory-continuity-arxiv.md);
  2609.38353 TAGGRAPH (banked in corpus/steal/CORPUS_FOLD_FRONTIER_OLM_20261001.md:13 plus
  the 10-07 sweep); 2610.10265 Stale, Misattributed, or Late (banked item 1,
  frontier_olm_2026-10-08/sweep/agent-memory-continuity-arxiv.md); 2610.09348 Relevance Is
  Not Sufficiency (banked item 5, same 10-08 sweep); 2609.37930 MGPO (full-text read and
  folded by the 10-03 x sweep, frontier_olm_2026-10-03/sweep/agent-memory-and-continuity-x.md
  RQ3 section). My own reads of these five corroborate the prior banks; nothing new added.

## BANKED ITEMS (strongest first; the JSON result carries these 7)

### 1. TRACE: Governing Memory Validity in Evolving Multi-Agent Systems (2609.33517, 2026-09-27)

The formal answer to the warm-boot question. Core law: "Faithful retrieval does not establish
current eligibility for action" - a memory can be retrievable, relevant, and historically
correct yet inadmissible at re-entry. Mechanism: at departure, checkpoint D_a with source
receipts and state epoch; at return, bind to the absence delta: C = D_a + delta. Explicit
invalidation walks machine-readable links (revocations, supersession edges, validity
intervals); implicit invalidation runs a high-recall scanner then a grounded verifier. Four
separate gates (authorization, temporal validity, applicability, provenance) produce a
reason-coded audit trail; greedy weighted-set-cover admission under budgets fails CLOSED -
"when no selection meets the required coverage, the return is reset or blocked rather than
issued with an obligation silently omitted". Rejected content stays in audit storage but
cannot serve as a premise (functional forgetting). Results: on STALE Type II (implicit
invalidation) TRACE beats the strongest policy by 18.5-27.5 points across three actor
models; the ablation removing implicit invalidation costs -25.83 Overall; on ManBench-Return
"Reset achieves 96.38% Overall with Qwen... yet its VIA is zero" - restore and reset each
bottom out at 0% on one of the two axes, so neither policy alone preserves AND rejects.
Limitations: needs an authenticated return, preserved checkpoint, source receipts; missed
dependencies admit stale state, over-broad checks discard useful context; STALE Overall
falls 73.33% to 43.33% as absences lengthen.

Estate mapping: warm_state.json IS the departure checkpoint (chain tip + deployments +
session_brief, 989 bytes, read this session); rib_boot.json already computes the absence
signal as age_debt ("tip 1956 min old at boot -- AGE DEBT over 60 min: warm boot owed") but
nothing binds it to a delta over the chain grew while away, and nothing gates restored
memory on current eligibility. TRACE's C = D_a + delta plus fail-closed obligation coverage
is the named instrument for the warm-boot chain's missing third organ.

Overlap: zero hits for the ID and "current eligibility" across catalog/catalog.jsonl, all
sweep/steal/register/DIGEST files, memory/rib, memory/press, memory/research_packs,
memory/frontier, memory/improve, corpus/steal. Fully new.

### 2. CAVE-Mem: Boundary-Aware Experience Validation for Memory Search (2610.00238, 2026-09-23)

A training-free gate that decides whether a reused experience may override a fresh answer.
Four validity checks per intervention operator: substrate profile, answer contract (exact
slot), failure boundaries (temporal, count, quote), and positive cross-fitted utility
(estimated only from diagnostic trajectories outside the target block, so gold answers are
never queried). If nothing passes, "the system abstains to the base answer." Load-bearing
sentence: "reusable memory should include the conditions for use, not only the instruction
to reuse." Gains: LoCoMo GPT-4o-mini 60.35 F1, +5.85 over the strongest baseline; the gate
abstains often (NarrativeQA changed only 16 of 300 answers). Limitations: on Qwen2.5
backbones gains shrink under 2 F1 and the gate can trail Mem0 on temporal questions;
permissive thresholds admit high-variance edits, strict ones suppress useful low-frequency
corrections.

Estate mapping: this is the admission-side law for every rib/steal/bank card: a card should
carry its own conditions of use (boundary checks), and a fold's outcome stamp (held /
falsified / pending, knowledge_graph.py:675) is the same shape. The warm-boot chain restores
instructions with no conditions attached; CAVE-Mem is the read-side guard.

Overlap: zero hits for "CAVE-Mem" and "Boundary-Aware Experience Validation" across the same
grep set. Fully new.

### 3. EvoCUE / The Right Lesson at the Right Step (2609.34988, 2026-09-28)

Where a lesson lives is part of the lesson. EvoCUE attaches each learned update to a
specific edge in an explicit agent state machine: "a learned update is an instruction or
short executable skill attached to a specific edge, with an applicability rule that
determines when it runs." Edits are localized by residual goals (requirements the public
history does not show as satisfied); a paired trial restores the checkpoint immediately
before the edit to compare parent vs edited programs. Applicability rules are at most two
equality tests on categorical pre-edit state features. Location ablation: the same
instruction solves 5 of 16 dev tasks when available at first entry vs 14 of 16 at the
recurring entry - "What matters is whether the instruction is available when the completion
decision is made." AppWorld 13.7% to 79.2% Test-Normal from a minimal controller.
Limitations: applicability rules inferred from a finite task set; paired trials need
restorable execution states; unbounded instruction injection at every step gets costly.

Estate mapping: the behavior-card deck IS this shape - operator input SHAPES with warmed
invocable lanes (RIB_BEHAVIOR_CARDS_20260928.md head, read this session) - which makes it
the design source for the oral_history miner (RQ3): a card minted from a session transcript
needs (1) the operator-turn segmenter, (2) recurrence clustering (the deck's own EVIDENCED
bar: "demonstrated repeatedly in the record"), (3) an invoke lane plus applicability rule
per card. A quote extractor is not the instrument; an edge-attacher is.

Overlap: named once in frontier_olm_20260928/sweep/evals-self-improvement-arxiv.md pass 1
as "strongest candidates not deep-read (no claims made about them)" - an explicit non-bank;
the 20260928 seat made no claim and this is the first full-text read and first bank.
Catalog carries only the state/arxiv/2026-09-29 abstract stub (row b31983311f0e).

### 4. Memory as Middleware / ALTK-Evolve (2609.32091, 2026-09-25, IBM)

Architecture claim: "A memory store persists information; memory middleware defines how
experience is captured, consolidated, isolated, retrieved, shared, edited, forgotten, and
governed across agents." The middleware owns the cross-cutting concerns no individual agent
should re-implement. ALTK-Evolve is the reference implementation: typed memory namespaces
(episodic/semantic/procedural), typed records carrying trigger/applicability condition and
provenance, four-step extraction (segment, subtask, generalize, consolidate), gists that
are "an index, not a replacement", write-path reconciliation choosing "add, update, merge,
supersede, quarantine, or reject" instead of blind append, and agent-facing surface limited
to six operations with curation as a governed, human-visible act. Host-native interposition
binds the same logical behavior to each host's own primitive (Claude Code plugins, Codex
instruction-file pointer, hooks for Claw Code). AppWorld: scenario-goal 50.0% to 64.3%,
Hard 19.1% to 47.6%, attributable to memory as a separable layer. Limitations: preliminary
IBM technical report, feasibility evidence not a complete evaluation; open agenda includes
consistency semantics for learned experience, memory transactions, forgetting policy.

Estate mapping: the estate already half-built this (rib vault + warm_state + context_pack
are the middleware; RIB_MD_RECORD is the record law). The two absent pieces are the
write-path reconciliation verb set (the estate appends; supersede/quarantine exist only in
SUPERSEDED.md prose) and the condition-of-use field on typed records (pairs with CAVE-Mem).
Per-agent scoping and provenance channels are steal-card material for warm_state schema v2.

Overlap: zero hits for the ID, "ALTK", and the title phrase across the same grep set. Fully
new.

### 5. MemAgent: Learning to Manage Heterogeneous Memory Providers (2609.32521, 2026-09-26)

A trained router (Qwen3.5-4B LoRA) treats memory itself as a three-phase routing problem
across 13 heterogeneous providers (trajectory summaries, insight extraction, workflow
templates, executable skills, knowledge graphs, procedural scripts, KBs): Begin picks a
provider to recall from after parallel probing (scores withheld so the model cannot learn a
pick-the-highest shortcut), In injects a rule-based working-memory summary, End selects a
SUBSET of providers to store the trajectory into, avoiding indiscriminate storage. Reward
is per-decision (correctness, judge attribution, downstream reuse) with no ground-truth
routing labels. "MemAgent improves average accuracy by 10.0% over the baseline and
outperforms every single-provider method across all three benchmarks" (75.7% vs 65.7%
no-memory, best single provider 71.0%) at under 0.3% routing overhead; a hindsight oracle
over all providers reaches 89.6%, so routing headroom remains. No single provider dominates
(AWM +6.1% on GAIA, -0.6% on WebWalkerQA). Limitations: delayed feedback makes per-provider
credit assignment hard; GAIA L1 doubles as memory-population task; the 5-provider pool
trails the 13-provider pool (69.8% vs 75.7%).

Estate mapping: the tier ladder is a routing problem over memory surfaces the estate
already runs (warm_state, rib vault, knowledge_graph known()/context(), corpus FTS,
biography knots); nothing routes between them today - each surface is consulted by habit.
The Begin/In/End phases are the shape for a memory-router instrument, and End's
store-subset rule is the standing-wave budget law in instrument form.

Overlap: zero hits for the ID, "MemAgent", and the title phrase across the same grep set.
Fully new.

### 6. RPMem: Learning Long-Term Recurrent Parametric Memory Across Sessions (2609.23466, 2026-09-20)

Sessions compile into a fixed-shape latent memory via a frozen encoder plus trainable
Perceiver resampler; a recurrent gate (2d^2+d parameters, shared everywhere) blends the
incoming session with accumulated memory: ht = zt*ht-1 + (1-zt)*qt. The split that makes
continuity portable: "A model-specific decoder learned during compilation converts the
consolidated memory into LoRA parameters for the serving backbone" - on backbone
replacement, only a new decoder is fitted while memory, encoder, and gate are retained.
Transfer improved all 28 backbone-setting combinations, cross-model average 75.97% to
89.64%. Deployment numbers: session write 0.043s at 64 sessions (~22x faster than rank
concatenation, ~292x faster than Mem0), 1.00x memory growth, zero historical query tokens;
general capabilities stay within ~1.4-3.8pp of the base model. Limitation: applicability to
scenarios with substantially different memory needs remains unstudied.

Estate mapping: the estate's continuity is byte-carried (chain + ribs) and re-prompted per
seat; RPMem is the parametric alternative where continuity is compiled once and decoded per
model. Relevant to the tier ladder's local-janitor rung: a compiled estate latent decoded
into gemma/gemma4 adapters would carry seat continuity across model swaps without re-prompt
cost. The learned-gate-vs-averaging result (beats LoRA factor averaging by 31.31pp) says
consolidation must be learned, not averaged.

Overlap: zero hits for the ID, "RPMem", and the title phrase across the same grep set.
Fully new.

### 7. After the Fix: Transfer of Corrected Agent Experience (2609.34603, 2026-09-28)

The correction-loop honesty check. "The value of repairing experience is not the same as
the value of reusing it." Design: same failed task at two points (stop after failure U vs
continue through repair to acceptance C), both handed to the same target task against a
fresh-start baseline; 3,300 runs, six handoff formats, three regimes. ThinkingBox: repaired
experience beats uncorrected by +44/+29/+32pp and beats fresh start by 25/22/18pp - but
"12 of Full's 15-point larger correction gap over Skill come from worse uncorrected
performance, not better corrected memory" and "22 of Full's 46 upward transitions restore
observed baseline success" - much of repair value is just recovering what a fresh start
gives anyway. APEX: no aggregate correction benefit. Behavioral finding that transfers:
reusable obligations (an open-act-close lifecycle) transfer well while source-specific
choices (a discounting convention) wrongly override new target requirements. Limitations:
retrospective analysis, one execution per cell, no repeated-run reliability estimate.

Estate mapping: the CORRECTION card (stop, root-cause, mint law) and the amendment-not-
rewrite record law are validated in the abstract - but this paper prices the card: measure
corrected-vs-fresh before crediting the correction loop, and strip source-specific choices
out of transferred cards (the card deck's STEAL-ORDER/GENESIS-TESTIMONY shape already
distinguishes operator law from source specifics).

Overlap: catalog row 4101b36b45dd is the state/arxiv/2026-09-29 abstract stub only (1,459
bytes, no why layer); zero sweep/steal/register/memory hits for the ID or title. First read
and first bank.

## Answers to the four research questions (compressed, estate bytes cited)

- RQ1 (warm boot vs the 41% islands): the builder is LOCATED and READ: mag/knowledge_graph.py
  (751 lines). The lens/graph.md:41 OWED is cured. The islands are builder-shaped, not
  data-shaped: _edges() (knowledge_graph.py:297-339) mints only four relations
  (superseded_by, has_invariant, already_inside, maps_to); knot/doctrine/steal nodes carry
  none of the fields that branch reads (no superseded_by, no invariants, no maps_to, and
  kind is not module/landscape), so 400 knots + 217 doctrines + 140 steals are structurally
  unwireable by construction - the JSON never carried what the builder never minted. Two
  real drops also exist: _nodes_verkle() returns nodes[-400:] (knowledge_graph.py:128), so
  older chain knots never enter the graph at all, and _nodes_case_law() reads only
  skill_ledger.jsonl[-300:] (knowledge_graph.py:152). warm boot therefore restores chain +
  law + brief (warm_state.json 989 bytes + rib_boot.json 43,672 bytes, both read) but full
  seat continuity does NOT flow through the graph; per TRACE, continuity needs the
  absence-delta binding and eligibility gates the estate lacks (rib_boot's age_debt is the
  delta signal, unbound).
- RQ2 (agentmemory + ms-agents-beginners): absent patterns, from first-hand reads of the
  parked agentmemory README/AGENTS.md (C:/Users/foste/Documents/projects/library_parked/
  agentmemory, 781 catalog rows) and ms-agents-beginners/13-agent-memory notebook: (1)
  4-tier consolidation with Ebbinghaus decay + access strengthening + auto-evict; (2)
  recall hygiene (superseded versions excluded from every recall path while the version
  chain keeps history - the estate's BM25 ranker scores superseded-kind nodes); (3)
  PreCompact re-injection hook; (4) write-time provenance channels + per-agent scoping; (5)
  tool-mediated PULL memory (@tool save/retrieve) vs the estate's push-injection. Steal
  cards, not new research: knowledge_graph.py:48 shows v2 already stole GraphRAG + Mem0 +
  Letta; the recall-hygiene and PreCompact hooks are the missing steals. The AML competency
  model already banked at memory/runs/gapwave/agent_memory_challenge_2026.md names the same
  governance gaps.
- RQ3 (oral_history as second card miner): corpus/oral_history holds 8 top-level entries;
  seat_pools/codex_sessions 11,674 files + grok_sessions 193 (find counts this session),
  history.jsonl 28 lines, session_index.jsonl 50 lines - the mass is raw session files, so
  the volume is real. Per RIB_BEHAVIOR_CARDS_20260928.md (deck head + 10-05 amendment read),
  the deck's bar is EVIDENCED recurrence and the mount is real (VAULT_RIBS sixth mount);
  what the miner needs is an operator-turn segmenter over codex/grok session files, a
  recurrence clusterer, and per-card invoke lanes with applicability rules - EvoCUE's
  edge-attachment is the design source, not a quote extractor. The X miner
  (tools/behavior_cards_x.py, per the rib's consumer-census amendment) already proves the
  consumer path.
- RQ4 (the three unbanked olm runs): YES, the zero-confirmation gap (burns.md:107) is a
  register gap, not a work gap. frontier_olm_2026-10-10/sweep/agent-memory-continuity-arxiv.md
  (18,360 bytes, read this session) holds EIGHT fully-read banked items (Skill-V, Workday
  PD, Memory-Skill Isomorphism, MemoWM, SkillSpec, EngramBench, JAM, Lineage-Aware
  Governance); frontier_olm_adhoc/sweep/agent-memory-continuity-arxiv.md holds 43
  candidates + 7 full-text reads (Hippocam, QGMem, Memento 3, Attic-KV, Agentic-TTT, DPPM,
  galahad-kv) while its register.jsonl (23 rows, grepped this session) carries zero
  agent-memory-continuity rows. Before any new sweep fires: fold those two sweep files into
  the register. My own bank honored the union: five items I read were dropped as re-banks
  (MEMTRIM, TAGGRAPH, 2610.10265, 2610.09348, MGPO).

## Receipt

- Estate reads this session: lens files (graph/corpus/laws/burns), mag/knowledge_graph.py
  (full), memory/warm_state.json + memory/rib_boot.json (heads + wc -c),
  memory/rib/RIB_BEHAVIOR_CARDS_20260928.md (two sections), parked agentmemory README.md +
  AGENTS.md (heads + How It Works + search sections), ms-agents-beginners/13-agent-memory/
  13-agent-memory.ipynb (all markdown cells, venv python), memory/runs/gapwave/
  agent_memory_challenge_2026.md (head), prior sweep/steal/register files named above.
- Web reads: 7 arxiv.org/html full texts + 2 abs pages (all fetched 2026-10-11).
- Commands: the greps and find/wc counts named inline above; catalog grep instrument was
  plain grep -c/-m1 over catalog/catalog.jsonl.
- Not run: pytest (no code changed), no catalog writes, no register writes (folding the
  register is the fold-lane's job, named in RQ4).
