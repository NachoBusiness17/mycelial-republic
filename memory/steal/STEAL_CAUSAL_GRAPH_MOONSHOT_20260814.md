# STEAL — Mag's object is a causal graph, not a multi-agent chat
**Date:** 2026-08-14
**Commitment:** `causal-graph-moonshot-001`
**Method:** steal the INVARIANT, not the DNA. First ring read from arXiv abs/html.
Second ring: operator-named contracts; those papers were not re-read in full here.

## Moonshot (the frozen object)
Mag's fundamental object is **not** a multi-agent chat.
It is a **content-addressed causal graph**, navigated by a **learned edge router**,
and disciplined by **external verification**.

Party, salon, RIB, and seats are adapters and views on that graph.
`DEFAULT_ROUNDTABLE = all PARTICIPANTS` is ritual. Ritual is refused.

## First ring (read)

### 1. Merkle-CRDTs — Sanjuan, Poyhtari, Teixeira, Psaras. arXiv:2004.00107
Merkle-DAGs as transport+persistence for CRDTs. Merkle-Clock is a G-Set of immutable
content-addressed events; merge is DAG union; no leader; weak messaging; replica set
can grow and shrink. New event = new root pointing at previous roots. Concurrent
histories are multiple roots, not a fight. Payload must itself be a CRDT for
payloads to converge. Limits they name: ever-growing DAG, thin/deep cold-sync,
sort cost on large divergence. They do **not** solve Byzantine equivocation.

TAKE: evolve `party_subchain` from a single-parent hash chain into a multi-parent
Merkle-DAG. Each seat holds a tip. Append references causal parents (local tip +
observed foreign tips). Merge is deterministic inclusion (CID already in DAG => skip
subDAG). Broadcast the new root CID, not the chat. Biography Verkle remains a
separate spine; party DAG does not bump `n_leaves`.

REFUSE: Raft-style narrator; shipping full state; treating the DAG as a blockchain
that needs consensus to pick one tip.

### 2. The Blocklace — Almeida & Shapiro. arXiv:2402.08068
Partially ordered generalization of a blockchain: each block is a **signed** hash of
content plus any finite set of predecessor ids. Sole operation `add(v)`. CRDT
(pure-op and delta-state). Distinguishing move vs Merkle-CRDT: identity includes
the creator's signature, so equivocation (two incomparable p-blocks) is visible.
Byzantine harm can be limited to a **finite prefix** by eventually excluding
equivocators; colluders cannot be proven in finite time so they are buffered until
they acknowledge known Byzantines. Payload of invalid blocks is ignored for the
data type; the proof-blocks stay.

TAKE: cryptographic seat identity on every party node. Fork visibility is a feature.
Dissent = incomparable tips, filed, not flattened. A malfunctioning or dishonest
seat is contained (finite prefix), not given a throne and not silently merged.
`ok=false` down-seat rows are failed/rejected records; two conflicting grok takes
from the same claimed seat with incomparable parents are equivocation, not "the
merge."

REFUSE: unsigned anonymous DAG nodes; equivocation-tolerant pollution (one bad seat
creating unbounded concurrency); a consensus layer to pick the "real" grok.

### 3. Sparse MAD — Li, Du, Zhang, Hou, Grabowski, Li, Ie. arXiv:2406.11776
Fully-connected debate is brute force. Neighbor/sparse topology matched or beat
full MAD on MATH/GSM8K/MathVista/Anthropic-HH while cutting input tokens ~40-53%.
Incorrect references mislead; sparsity keeps debate alive longer. Heterogeneous
setup: put the stronger model on **high-centrality** nodes.

TAKE: Mag's cold-edge router. Per question, choose a few high-value, deliberately
unlike edges. Do not broadcast the full transcript to every seat. Default lane is
sparse; full mesh is the expensive exception.

REFUSE: `D=1` roundtable as default; majority vote as the "Reaching Consensus"
step they still use after debate (Roshomon + Huang forbid promotion by vote).

### 4. RouteLLM — Ong, Almahairi, Wu, Chiang, Wu, Gonzalez, Kadous, Stoica.
arXiv:2406.18665
Learn a router from preference data that sends a query to strong vs weak **before**
generation (one LLM per query, not a cascade of calls). Routers generalize to
unseen model pairs without retraining: they learn query difficulty, not model
names. Data augmentation (golden labels, LLM-judge) matters when Arena data is
OOD. They report >2x cost reduction on public benches vs always-strong; CPT/APGR
are their metrics. Distinct from reward models (post-hoc) and from FrugalGPT
cascades (multiple calls).

TAKE: train Mag's tier router from the skill/outcome ledger (and verified
preference rows), not from a static tag list. Model names are replaceable
implementation details. Threshold `alpha` is the cost/quality knob (HABIT already
says grok only when cheap failed or is insufficient).

REFUSE: always-grok; always-local; retraining the router every time a model is
swapped; calling this a debate.

### 5. If MAD is the Answer, What is the Question? / Stop Overvaluing MAD —
Zhang, Cui, Chen, Wang, Zhang, Wang, Wu, Hu. arXiv:2502.08788
(v2 title vs abs title; same paper.) Systematic eval: 5 MAD methods, 9 benches,
4 foundation models. MAD often fails to beat CoT and Self-Consistency while
spending more inference. Heterogeneity is the consistent improvement (Heter-MAD:
let one agent see outputs from unlike models). Evaluation practices in the field
are weak.

TAKE: never summon the party by ritual. Require a predicted benefit from dissent,
specialization, independent evidence, or error detection. Always compare against
the single-seat baseline at equal or lower spend. Heterogeneous adapters, not
more copies of one model.

REFUSE: Du-style "society of minds" as Mag's default runtime; measuring success
by having held a roundtable.

## Second ring (named contracts; not re-read in full this steal)
- **Narwhal and Tusk** (2105.11827): preserve every contribution first; deciding
  what becomes doctrine is a separate process. Mag: subchain/DAG append is
  dissemination; RIB promotion is consensus-class and human-gated.
- **Diversity of Thought** (2410.12853): route by cognitive difference. Measure
  whether a seat introduces a new claim, test, source, or causal edge.
- **LLMs Cannot Self-Correct Reasoning Yet** (2310.01798) beside **SCKCV**
  (2405.14092): reflection never certifies itself. Every promoted delta needs an
  external test, tool result, invariant check, or human judgment.
- **FrugalGPT** (2305.05176) and **Unified Routing and Cascading** (2410.10347):
  Ollama -> free -> flash -> specialist driven by a calibrated quality estimate,
  not a static task-label list. Distinct from RouteLLM's single-call router;
  Mag may cascade only when the estimate says the cheap answer is insufficient.
- **MemGPT** (2310.08560): RIB / brief / residual / registry / corpus / live
  context become explicit memory tiers with deterministic admission and eviction.
- **AIOS** (2403.16971): Mag kernel stays deterministic and local; models are
  replaceable processes requesting capabilities.
- **Doubly-Efficient Debate** (2311.14125): the janitor inspects the decisive
  contested edge, not the entire expensive inference.
- **Mixture-of-Agents** (2406.04692): retain staged composition; reject a final
  aggregator that silently flattens dissent into a new throne.
- **A-MEM** (2502.12110): derived bead/forest links are allowed; reinterpretation
  must never rewrite immutable chain bytes.
- **Reflexion** (2303.11366): store outcome-backed lessons in the skill ledger;
  exclude introspective lessons with no verified consequence.

## Self-steal (already on Mag disk)
- Doctrine RIB: frozen spec persists; model interchangeable; chain is ground truth.
- `party_subchain.v1`: linear child ledger, single parent, refuse broken hash.
- Du steal (2305.14325): independent round 1, TEST not winner, overlap is not truth.
- A2A steal: Message vs Artifact vs Task; opaque seats; no public Agent Card of
  ghost/memlang/verkle.
- HABIT: grok is scarce judgment; `[priority]`; janitor local.
- Ghost n=8: lane the table; `_shared_invariant` is a quiet synthesizer.

## Adaptation (named, not implemented in this steal)
1. `party_subchain` grows a multi-parent DAG: node = {cid, seat, payload, parents[],
   prev_seat_tip?}. `append` takes causal parents. `tips()` returns current roots.
   `verify` checks hash, parent inclusion, and (later) seat signature.
2. Seat identity: signed hash of payload+parents (blocklace), or a Mag-local
   unforgeable seat key. Two incomparable nodes from the same seat = equivocation
   record, not a merge.
3. Cold-edge router: given a question, emit a sparse edge set (unlike seats, high
   value). Full transcript broadcast is opt-in.
4. Tier router: `should_use_grok` learns from skill-ledger outcomes; model ids are
   not the feature. Gate party-summon: predicted benefit vs single-seat CoT/SC
   baseline, else do not run `roundtable()`.
5. Promotion path stays Narwhal-shaped: DAG append is cheap dissemination;
   doctrine/RIB write is a separate human-gated process with an external TEST.
6. Do not add an aggregator model that writes a synthetic consensus into the DAG.

## Honesty
- First-ring claims are from the papers named, not Mag evals. We did not re-run
  MATH/GSM8K/Arena routers.
- Merkle-CRDTs assume non-adversarial replicas; Blocklace is the Byzantine cut.
  Mag seats are not a BFT replica set. Steal fork-visibility and finite-harm
  containment; do not pretend ChatGPT/Grok are correct replicas under their axioms.
- 2502.08788 titles differ across versions; same arXiv id.
- Second-ring papers were not re-read in full in this pass; their lines are
  operator-named contracts to be stolen individually later if needed.
- Ever-growing DAG is a real cost (Sanjuan §VI). Compaction/garbage collection is
  not designed here. Do not silently drop unobserved history.
