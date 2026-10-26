# LENS: knowledge_graph.json connectivity - most connected topics, thinnest edges

- Date: 2026-09-28
- Instrument: single read of `memory/knowledge_graph.json` (schema `knowledge_graph.v2`, ts `2026-09-28T19:47:25.519956Z`) via three `.venv/Scripts/python.exe -c` json.load passes in this session. The file is minified single-line JSON (745.7KB), so line cites are not meaningful; every number below is the printed output of one of those three passes, run during this ask.
- All counts below are of THIS file at THIS moment. The graph regenerates (fold() accumulates), so these are a snapshot, not constants.

## Shape of the graph

- 2,062 nodes / 817 edges.
- Node kinds: module 996, knot 400, case_law 300, doctrine 217, steal 140, landscape 9.
- Edge relations: `has_invariant` 786, `already_inside` 31. There are exactly two relation types in the whole graph.
- 806 of the 817 edge endpoints are `invariant:...` ids that are NOT materialized as nodes. The graph's densest layer (module invariants) is edge-only: invariants exist as `has_invariant` edges into the void, not as first-class nodes.
- 1,066 of 2,062 nodes (51.7%) have zero edges.
- Node id integrity: 1,763 unique ids for 2,062 nodes. One id, `law:`, is shared by ALL 300 case_law nodes (dup x300). Knot ids are all unique. This means every case_law node is addressable by the same id: the case_law layer is not individually addressable by anything that keys on id.

## Most connected topics (what we know most)

- Top real hub: `module:context_compression.py`, degree 5 (invariants: never lose sovereignty information; A/B test every compressed prompt; keep the original as fallback).
- 26 modules sit at degree 4, one each behind their invariant fan: water_swarm, vast_launcher, training_packager, tokenomics, session_ritual, session_koan, riddler_campaign, rib_k8s, renderman, prompt_archaeology, narrative_engine, mixture_of_agents, lora_pipeline, lens_library, ghost_ledger, ga4_progression, frontier_scout, dspy_sovereign, data_refinery, copilot_bridge, context_checkpoint, constitutional_critique, chain_query, campaign_simulator, behavioral_lensing, auto_quantize.
- Module degree distribution: mean 1.37, median 1, max 5. 458 of the connected modules sit at degree exactly 1 (one invariant, nothing else).
- The landscape layer is the only cross-kind bridge: 9 `family:*` nodes (agent_first_browser/Kitesurf, mcp_stateless, webmcp, agent_access_model, agentic_wallets/x402, aeo, readable_first, knowledge_graph_rag, agent_memory) each wired by `already_inside` to 2-5 estate modules (avg degree 3.44). These 31 edges are the only place an external idea is bound to the code that implements it. context_compression.py and corpus_expand.py each appear under multiple families (aeo, readable_first, agent_memory, knowledge_graph_rag territory).
- The single highest-degree "node" in the graph is fake: `invariant:law ` (degree 9) is an id-collision artifact. Nine modules (agent_state.py, behavior_catch.py, corpus_query.py, diary_node.py, field_steal.py, intention_brief.py, local_usable.py, session_freeze.py, voice_handoff.py) each have an invariant whose text is literally just "Law:" (empty after the prefix), so their truncated ids collide. Do not read this as a shared law; it is nine blanks.

## Thinnest edges (what we know least)

1. Entire knowledge namespaces are edge-orphans. knot (400 nodes), case_law (300), doctrine (217), steal (140): 1,057 nodes, ZERO edges between them. The estate's law layer (doctrine + case_law = 517 nodes) is completely disconnected from the module layer that supposedly implements it. You cannot currently ask "which doctrine does module X implement?" or "which law is enforced by zero modules?" from this graph; the answer to the second is unknowable, which is itself the finding.
2. Invariants are private. Of 777 distinct `invariant:` edge endpoints, exactly 2 have degree > 1. One is the fake `invariant:law ` collision (above). The only GENUINE cross-module shared invariant is `invariant:schema percolator v1 deterministic 0 dep` (text: "Schema: percolator.v1, deterministic + $0, deps: stdlib only", middle dots from the source normalized for this file's ascii scan), declared identically by module:percolator.py and module:percolator_heal_test.py. Everything else: 775 invariants each held by one module alone. There is no shared-law backbone; the graph cannot say two modules obey the same rule.
3. 409 of 996 modules are fully isolated (no invariants extracted, no edges). The 410 modules with an empty `invariants` field match this almost exactly. These are the estate's own code with nothing said about them: the least-known modules are our own.
4. case_law id collapse: all 300 case_law nodes carry id `law:`. Whatever downstream tooling consults known()/by-id (the graph's own family edge cites `mag/knowledge_graph.py` fold() and auto-consult known()), case_law lookups by id resolve to a 300-way pile.
5. `already_inside` (31 edges) is the rarest and richest relation and exists only for 9 landscape families. No doctrine, steal, knot, or case_law node participates in any relation except existence.

## The question the fleet isn't asking

The graph records what each module believes alone. It records nothing about agreement: the doctrine and case_law layers hold the estate's law, the module layer holds the estate's code, and there is not one edge between them. The thinnest edges are not weak ones, they are missing ones: law-to-module. The next build is not another invariant, it is the `implements` relation that binds each doctrine/case_law node to the modules that enforce it, plus deduplicating the invariant ids so shared laws become hubs instead of blanks. Until then, "which laws does the code actually enforce?" is a question the graph cannot answer.

## Checks run / not run

- RUN (this ask): json.load + analysis of memory/knowledge_graph.json, three passes:
  1. top-level shape, node/edge key shapes, kind and rel counters, degree ranking.
  2. degree-by-kind, isolation counts per kind, percolator invariant edges, already_inside dump, landscape dump, isolated-kind samples, invariants-field population.
  3. duplicate-id census, case_law/knot id uniqueness, invariant endpoints with degree > 1, module degree distribution (mean/median/max/dist), percolator shared-invariant modules, degree >= 4 hub list.
- NOT RUN: no regeneration of the graph (I read the standing file; fold() was not invoked), no cross-check against mag/knowledge_graph.py source behavior (the module is named in the graph's own edges but I did not read it this ask), no verification of the underlying source paths cited inside node `source` fields.
