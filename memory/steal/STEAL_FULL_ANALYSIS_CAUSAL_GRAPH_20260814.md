# STEAL FULL ANALYSIS — causal-graph moonshot vs Mag bytes
**Date:** 2026-08-14
**Commitment:** `causal-graph-moonshot-001` analysis
**Ground:** `mag/party_subchain.py` (linear `prev_hash`), `mag/frontier_salon.py`
(`DEFAULT_ROUNDTABLE = list(PARTICIPANTS)`, `_shared_invariant` token overlap),
`mag/grok_gate.py` (keyword FRONTIER_SIGNALS / CHEAP_SIGNALS), `configs/lanes.yaml`
(static L0-L3 + `[priority]`), steals of 2026-08-14 (Du, A2A, causal-graph).
**Not:** a re-summary of the papers. Those live in
`memory/steal/STEAL_CAUSAL_GRAPH_MOONSHOT_20260814.md`.

## Verdict
The moonshot is the right object. Mag's runtime is still the wrong object.

On disk, Mag already has a frozen spec, a child hash chain, opaque seats, and a
human-gated RIB path. In motion, Mag still summons a full roundtable, broadcasts
the transcript, names token-overlap "consensus", and routes grok by string match.
That is a multi-agent chat with a cryptographic diary attached. The diary is soil.
The chat-as-object is glory that no longer serves.

## Gap matrix (first ring vs bytes)

| Steal | Mag now | Gap |
|---|---|---|
| Merkle-CRDT multi-parent DAG, per-seat tips, merge by inclusion | `party_subchain.append` sets `prev_hash` to `rows[-1]["hash"]`. One global head in `head.json`. Genesis anchors to verkle `last_leaf_hash`. Verify refuses a broken linear relation. | Linear chain, not a DAG. Concurrent seats are serialized by the append lock, which **hides** concurrency instead of recording it. No `tips()`. No parent set. |
| Blocklace signed identity, equivocation = two incomparable p-blocks, finite harm | Entries are unsigned JSON. `seat` is a string the caller claims. Two "ghost" rows with different takes are just n and n+1 on one chain. `ok=false` records down transports, not equivocation. | Identity is a label. Forks cannot exist, so they cannot be seen. Containment of a lying seat is not implemented because the datatype cannot represent a lie as a fork. |
| Sparse MAD unlike edges, not D=1 | `DEFAULT_ROUNDTABLE = list(PARTICIPANTS)`. `seat_steer.send` mounts up to 4000 chars of full subchain into every message unless the caller already injected a transcript. Salon round-robin is a complete order, not a sparse graph. | Full mesh by default. Cold-edge router does not exist. Grok/supergrok sit in PARTICIPANTS, so a ritual table burns the scarce seat. |
| RouteLLM learned router, models replaceable, one call per query | `should_use_grok` is regex-ish keyword lists. `lanes.yaml` is a static ladder (Ollama -> openrouter -> grok_harness needing `[priority]`). Skill ledger count was 0 in agent_state 2026-08-14. Copilot inbox tonight was ~50 identical grok-4 X scrapes. | Router learns nothing. It pattern-matches the prompt. Model names are the feature. The X-loop is the anti-pattern RouteLLM exists to kill. |
| Huang 2502.08788: no ritual party; beat single-seat CoT/SC; heterogeneity | `roundtable()` runs whenever called. No predicted-benefit gate. No single-seat baseline comparison. `_shared_invariant` still emits a "consensus" string. Heterogeneous seats exist in PARTICIPANTS but the default is "all of them." | The table is a ceremony. Huang's result is not wired. |

## What is already soil (do not rebuild)
- Doctrine RIB: frozen spec, interchangeable model, chain as ground truth.
- Linear subchain: content-addressed, verify-before-extend, atomic lock, does not bump biography `n_leaves`. Narwhal split is half-true: append is dissemination; RIB write is a separate process.
- Down seats as `ok=false` rows that do not stop the table.
- `quest_roshomon`: disagreement is evidence.
- A2A steal: Message vs Artifact vs Task; opaque seats; no public Agent Card of ghost/memlang/verkle.
- Du steal: independent round 1 named; TEST not winner; overlap is not truth (named, not coded).
- HABIT + `lanes.yaml` + `grok_budget.max_escalations_per_day: 2` + `[priority]`: the *policy* of scarcity. The *implementation* is still keywords.
- Ghost daemon down + human hallway: a liveness fact, not an architecture. Merkle-CRDT assumes weak messaging; Mag currently uses the operator as Broadcaster.

## Contradictions to hold (do not "solve" with a chair)
1. **Merkle-CRDT is non-adversarial. Blocklace is Byzantine.** Mag seats (ChatGPT, Grok, Copilot) are not correct replicas under Almeida-Shapiro axioms. Steal fork-visibility and finite-harm *as a datatype*. Do not pretend a signed Mag DAG makes browser seats BFT.
2. **Du wants a common final answer. Huang says MAD often loses to CoT/SC.** Mag already refused Du's success metric. Keep TEST extraction. Add Huang's gate. Do not re-import consensus.
3. **Sparse MAD still majority-votes after debate.** Steal the topology, refuse the vote. Roshomon already forbids it.
4. **RouteLLM is one call. FrugalGPT is a cascade.** Mag's lanes look like a cascade (L0->L1->L2). RouteLLM says pick once from a learned P(win_strong). Both can live: cascade only when the estimate says cheap is insufficient. Keywords are neither.
5. **MoA wants a layered aggregator. Moonshot forbids a flattening throne.** Staged composition is allowed; a model that writes "the party's answer" into the DAG is not.
6. **A-MEM wants evolving links. Chain bytes are immutable.** Derived forest/beads yes; rewrite of `chain.jsonl` hashes no.
7. **MemGPT/AIOS want an OS kernel.** Mag already claims this (ghost, lanes, memory tiers) and then lets VS Code / CDP / notebooks become the kernel. The steal is admission/eviction rules, not another agent OS paper.

## The linear chain is not a bug — it is an incomplete clock
Sanjuan: a Merkle-Clock may have several roots. Mag's lock forces one root by making concurrent appends wait, then lining them up. That is causal *serialization*, not causal *history*. Two seats that actually moved without seeing each other get a fake happened-before from the lock. Roshomon evidence is destroyed at the datatype.

That is the single highest-leverage datatype change: optional `parents: [cid, ...]` plus per-seat last-cid. Keep `prev_hash` as a compatibility spine (the lock's total order) *and* record the real causal parents. Do not delete the linear verify. Add a second relation. Gossip: the moonshot is a DAG *view* over an existing log, not a greenfield store.

Blocklace then adds: hash of (payload, parents) signed by seat key. Without keys, "ghost" and "grok" and "9222" remain the same string-collision we already named ("this window is grok. 9222 is not").

## Router gap is not "add ML"
RouteLLM's point is: the feature is the *query*, labels come from *outcomes*, model ids transfer. Mag has the opposite: features are tokens in the goal string (`"architecture"`, `"janitor"`), labels do not exist (skill_ledger 0), model ids are hardcoded in `lanes.yaml`.

Cheap adaptation that is still a steal: log `(goal embedding or hash, lane chosen, outcome ok, spend)` into the skill ledger every dispatch. `should_use_grok` reads that table before the keyword list. Keywords remain a prior, not the posterior. Do not train a BERT router in this repo until the ledger has outcomes.

Huang gate is even cheaper and does not need a model: `roundtable()` refuses unless the caller passes `why` in {dissent, specialization, independent_evidence, error_detection} and a single-seat baseline is recorded in the same artifact. No why => no party. That kills ritual tonight.

## Ordered adaptations (cheapest first, no new throne)
1. **Huang gate** in `frontier_salon.roundtable`: require `why`; record a single-seat baseline field; default participants != all PARTICIPANTS (janitor/local only; grok `[priority]`).
2. **Rename** `consensus_invariant` -> `overlap_tokens`. Extract CHALLENGE as a list. Parse four fields as blocks. Do not write novel_deltas to rib_bus. (Already named in ghost n=8.)
3. **Sparse edges**: salon takes an edge list or degree cap. `seat_steer.send` mounts only the *incident* transcript slice, not 4000 chars of everyone.
4. **Outcome log** for `should_use_grok` / lanes. Keywords demoted to prior.
5. **Causal parents** on party_subchain nodes; `tips()`; keep linear `prev_hash` as the lock spine. Verify both relations.
6. **Seat signatures** once a local key per seat exists. Equivocation detector: two incomparable nodes with the same seat id.
7. **Compaction / GC** of the DAG is Sanjuan's open problem. Not this week. Do not drop unobserved history.

1-4 need no new cryptography. 5 is the Merkle-CRDT steal. 6 is Blocklace. 7 is deferred.

## Honesty
- This analysis did not re-run Huang's 5x9x4 eval or RouteLLM's Arena routers.
- Mag seats are not a BFT replica set. Blocklace finite-harm is a *containment metaphor* until signatures exist.
- Ghost daemon remaining down means Mag's Broadcaster is still the operator. A DAG does not remove that until something live consumes the tips.
- Second-ring papers remain operator-named; not re-read in full in the parent steal.
- Implementing 5-6 before 1-4 would be building a fancier diary for a ritual we refused.
