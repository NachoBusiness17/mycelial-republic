# STEAL — Persistent Mycelial-Republic OS (agent swarm as living OS)

**Stolen:** 2026-08-09 · sources: steal-protocol repos (bmas, flock, blackboard-core, agentswarm, subagent-router, ollama-harness) + our mycelial-republic docs + mag machinery.

## Stolen patterns (numbered)
1. **Stigmergic blackboard / control-unit-per-round** (bmas blackboard.py, orchestrator.py) → ghost as round-based control unit: each round read the graph, select which gpipes workers to activate, collect, write back, loop to consensus; Redlock-style ownership.
2. **Deterministic salience / self-reinforcement** (bmas salience.py) → `salience = w_c·confidence + w_r·recency(0.7^gap) + w_x·min(1, refs/3) − w_p·penalty(contradicted)` — edges sharpen with use AND prune failed paths (decay + contradiction penalty). Replace flat `+0.1` in research_lens.sharpen().
3. **Consumption records** (flock store.py ConsumptionRecord/AgentSnapshotRecord) → log which agent consumed which artifact → routing learns from use.
4. **Hybrid GraphRAG** (blackboard-core graph.py, persistence/) → semantic vector entry + structured graph traversal; pluggable durable backends (sqlite/json/redis/postgres).
5. **Cross-run durable memory injected at boot** (agentswarm memory.ts) → extend "PRIOR RUNS" memoryBlock to ALL seats so the OS never starts from zero after restart.
6. **Emergent priority scheduling** (agentswarm scheduler.ts) → priority-scored ready-queue over swarm goals (verify/modelTier/dependencies) instead of fixed cadence.
7. **Dual-write persistence** (bmas orchestrator.py) → hot live (desk/redis) + cold durable (sqlite/jsonl); history survives node death.
8. **Subscription-driven activation** (flock scheduler.py/subscription.py) → agents subscribe to artifact types; landing a pack auto-triggers the right cheap tier.
9. **Sparse activation / delegation profiles** (subagent-router activation.py) → codify activation profiles; model-choice is data, not debate (we already have agent_state_router + grok_free.route_surface).

## Existing local seeds (nucleus)
- `mag/research_lens.py` — self-referencing corpus + sharpen/fold_back (closest mycelium today)
- `mag/idea_graph.py` — nodes/edges.jsonl knowledge graph (substrate, not yet coordination)
- `mag/gpipes.py` — parallel fan-out subagents + merge
- `mag/ghost.py` — SENSE→pick_best→DEPLOY→MEASURE→COMPOUND (proto control unit)
- `mag/verkle_knot.py` — living Merkle–Verkle chain (persistence/anchor)
- `mag/cheap_swarm.py`, `mag/grok_terminal.py`, `mag/grok_free.py`, `mag/orchestrator.py`, `mag/steal_first.py`
- `mycelial-republic/src/mycelial_republic/vector_map/model.py` — hypergraph-style vector map (Node/Bond/Influence)
- Docs fully codify the vision: MAG_MYCELIAL_REPUBLIC_COMPASS, MYCELIAL_SCIENCE_MAP, COORDINATION_ELIAS_ROPE, FORTRESS_AND_REPUBLIC, CONSTITUTION.

## Gaps (the true "persistent OS" core)
1. No ONE living graph that IS the OS (idea_graph/research_lens/vector_map/verkle are separate).
2. No negative-signal reinforcement (no decay, no contradiction penalty, no prune).
3. No cross-restart durable OS state (no dual-write, no graph rehydrate on boot).
4. No self-organizing/emergent scheduling (command/cadence-driven only).
5. No consumption/learning records.
6. No distributed ownership/locking (single node).
7. Vision/machinery split (docs in mycelial-republic, machinery in mag).

## Roadmap (crude beginnings → persistent mycelial-republic OS)
- **Phase 1 — Nucleus:** unify idea_graph+research_lens+vector_map into ONE weighted directed graph store w/ pluggable durable backends + salience scoring + boot/rehydrate. *Exit: a graph that survives restarts and self-scores.*
- **Phase 2 — Self-organization:** control-unit/round loop on ghost+gpipes; priority ready-queue; consumption records; subscription activation. *Exit: agents coordinate through the graph.*
- **Phase 3 — Persistence:** dual-write; per-run memoryBlock for ALL seats; checkpointing. *Exit: swarm survives node death.*
- **Phase 4 — Sovereignty/distribution:** Redlock ownership + fork-equal peer handoff; v5 mesh/spores. *Exit: many beads, no king.*
- **Phase 5 — Self-reinforcing OS:** training_events as electrical trace; prune dead edges, reinforce green routes. *Exit: OS sharpens with use — the living republic.*
