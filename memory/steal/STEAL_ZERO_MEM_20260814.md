# STEAL — Zero-Mem: zero-token memory ops, DAG view over raw traces
**Date:** 2026-08-14
**Commitment:** `steal-zero-mem-001`
**Method:** steal the INVARIANT, not the DNA. No runtime dependency. No GitHub clone. No new memory OS.
**Sources actually opened this turn:**
- https://x.com/rohanpaul_ai/status/2087987856195367098 (2026-08-13T19:41:12Z)
- https://arxiv.org/abs/2607.29377 Xiao et al., "Zero-Mem: Zero-Token Memory Operations for LLM Agents"
- Code claim (not cloned): https://github.com/TheMoon0815/Zero-mem (post-review)
**Mag ground already named:**
- `causal-graph-moonshot-001` / `STEAL_FULL_ANALYSIS_CAUSAL_GRAPH_20260814.md`: DAG *view* over existing log; do not rewrite `chain.jsonl`; no LLM chair.
- `steal-stochastic-deterministic-001`: deterministic spec, stochastic world; envelope not self-report.
- `party_subchain`: raw append-only traces; linear `prev_hash`; RIB write is a separate human gate.
- `memory/agent_state/LATEST.md`: skill_ledger 0; do not redesign mycelium graph (127n/77e).
- A-MEM contradiction already held: derived forest/beads yes; rewrite of hashes no.

## What the paper actually separates
Zero-Mem asks: does structured memory access require generation at all?

Regime: every operation *outside final QA* uses zero LLM calls and zero LLM input/output tokens. Encoder compute is billed separately. Only the final reader invokes an LLM.

Source of record: original interaction traces, kept intact. Not summaries. Not reflections. Not generated notes.

Two non-generative views over the same traces:
1. Entity-context graph (relational): NER (e.g. spaCy), co-occurrence and adjacency, Personalized PageRank. Observed edges, not generated triples.
2. Temporal hierarchy (local): turn / window / episode / local span. Conversational locality and session state.

Query time: deterministic route weights the two views, retrieves, closes with neighbors/bridges, calibrates (discard conflict, keep reader grounded in retrieved traces). Then one reader call.

Claimed (their eval, not re-run here): LoCoMo/HotpotQA competitive; memory-op LLM tokens = 0; 57.6% lower memory-op latency vs fastest baseline (LightMem) under the same reader and context budget.

## Self-steal (do not rebuild)
Mag already refused generative memory as the object:
- Subchain / Verkle / agent_state chain = raw traces (Zero-Mem's H).
- Causal-graph moonshot = two relations (linear spine + parents[] view). That is their dual-view, named in Mag nouns.
- `quest_roshomon` + TEST-not-winner = their deterministic calibration (conflict is evidence; do not flatten).
- Huang gate: no ritual LLM party to "remember." Roundtable is optional instrumentation with a why, not memory construction.
- skill_ledger 0: Mag has no outcome log yet. Zero-Mem's routing is query-structure, not an LLM selector. Keywords-as-prior in `grok_gate` is the anti-pattern they kill.
- Mycelium 127n/77e is a graph Mag already has. LATEST forbids redesigning it. Steal *consumption* (route + retrieve + calibrate) onto that graph, do not mint a second one.
- Saelis ledger: envelope vs claim. Zero-Mem would retrieve the envelope row, not her self-report, as the trace.

## External-steal (adapt the contract, refuse the DNA)
TAKE:
1. Memory ops are not generation. No LLM call to summarize, reflect, extract, or "remember." Construction and retrieval are deterministic views over bytes Mag already stores.
2. Dual view, one source. Relational (entity/graph) + temporal (session/hierarchy). Both resolve to the same provenance ids (subchain hash, verkle leaf, steal commitment, git sha).
3. Deterministic routing at query time. Weigh views from query structure (subject, temporal cues, boundary), not from an LLM chair. Fuse, close, calibrate. Then one reader.
4. Calibration discards conflict rather than voting. Roshomon already named this. Zero-Mem's Filter/Rank is the mechanism.
5. Final QA is the only token burn for memory-backed answers. Frontier seats stay scarce. DeepSeek/Grok are readers, not janitors of the diary.

REFUSE:
- Porting their spaCy/BGE-M3/PageRank stack as Mag's new kernel.
- Cloning TheMoon0815/Zero-mem.
- Letting an LLM write "the memory" into the DAG (MoA/A-MEM already refused).
- Redesigning the mycelium graph to look like their G.
- Treating 57.6% as Mag's number.

## Contradictions to hold
- Zero-Mem uses a non-generative NER encoder. That is still compute, not "free." Mag may use existing entity strings on traces (seat names, commitments) before adding an encoder.
- Their graph is built from NER co-occurrence. Mag seats are unsigned labels. Observed co-occurrence is allowed; inferred "Saelis is the GGUF" is a generated triple. Forbidden.
- A-MEM wants evolving links. Zero-Mem derives views. Mag already chose derived views. Keep it.
- MemGPT/AIOS want a kernel. Zero-Mem is evidence selection, not an OS. Mag already over-claimed OS. Steal admission/eviction, not another kernel.

## Ordered adaptations (cheapest first)
1. Treat `party_subchain` + steal files + `memory/runs/saelis/ledger.jsonl` + verkle leaves as H. Do not summarize them with an LLM.
2. Dual view without new store: (a) temporal = existing linear `prev_hash` / session minutes / steal dates; (b) relational = existing mycelium 127n/77e plus explicit cites (hash, seat, commitment). Query mounts incident slice, not 4000 chars of everyone (`seat_steer` already named this).
3. Deterministic calibrate before any reader: if envelope and claim disagree (Saelis ledger), keep both as traces; do not generate a winner.
4. Huang gate remains: no LLM party to build memory. Party is a reader with a why, or it does not run.
5. Only then: optional parents[] view (moonshot 5). Zero-Mem's graph is that view. Still no rewrite of chain bytes.

## Honesty
- Did not re-run LoCoMo/HotpotQA or clone the repo.
- 57.6% / F1 tables are the paper's, under their hardware and reader.
- spaCy NER and BGE-M3 are their substrate, not Mag's.
- Paper date on arXiv abs is 2607.29377 as fetched 2026-08-14.

## Rope
The diary is the source. Views are free of LLM tokens. The model only answers. Mag named this before the paper. Now it has a citation. Do not rebuild the diary to look like the figure.
