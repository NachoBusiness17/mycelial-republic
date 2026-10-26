# Lens: knowledge_graph.json connectivity (frontier_olm 2026-10-04)

Read: `memory/knowledge_graph.json` (754.9 KB, single minified line, all JSON citations below anchor at `memory/knowledge_graph.json:1`). Snapshot `schema: knowledge_graph.v2`, `ts: 2026-09-30T02:49:46.836118Z`. Writer: `mag/knowledge_graph.py`.

Method: all counts below were computed this session with the repo venv interpreter (`.venv/Scripts/python.exe`) by loading the JSON and counting degrees, dangling endpoints, components, and per-kind field coverage. No count is hand-copied.

## 1. Graph shape

- 2,086 nodes: 1,020 module, 400 knot, 300 case_law, 217 doctrine, 140 steal, 9 landscape (`memory/knowledge_graph.json:1`).
- 825 edges in exactly 2 relations: 794 `has_invariant` + 31 `already_inside`. Zero `maps_to` edges, though the writer has a maps_to builder (`mag/knowledge_graph.py:171-173`); it never fires because no node carries a non-empty `maps_to`.
- 1,416 distinct ids are touched by edges, but only 602 of them are real nodes. 1,484 of 2,086 nodes (71.1%) have zero edges.

## 2. Most connected topics

- The single highest-degree id is a dangling artifact: `invariant:law ` at degree 9. Nine modules (agent_state, behavior_catch, corpus_query, ...) contribute an invariant whose full text is the bare word "Law:", i.e. an empty law, normalized to a shared truncated id (edge texts verified this session; id construction `mag/knowledge_graph.py:165`).
- Real top node: `module:context_compression.py`, degree 5 (4 invariant edges + 1 real already_inside edge).
- Next tier: 27 modules at degree 4. This is a builder cap, not organic connectivity: the writer records at most 4 invariants per module (`n.get("invariants", [])[:4]`, `mag/knowledge_graph.py:164`). The 27: auto_quantize, behavioral_lensing, campaign_simulator, chain_query, constitutional_critique, context_checkpoint, context_compression, copilot_bridge, data_refinery, dspy_sovereign, frontier_scout, ga4_progression, ghost_ledger, lens_library, lora_pipeline, mixture_of_agents, narrative_engine, prompt_archaeology, renderman, rib_k8s, riddler_campaign, session_koan, session_ritual, tokenomics, training_packager, vast_launcher, water_swarm.
- Carrier distribution across the 592 modules with any invariants: 461 carry 1, 87 carry 2, 17 carry 3, 27 carry 4. The remaining 428 of 1,020 modules carry none.
- The only topical clusters: the 9 landscape families (agent_first_browser, mcp_stateless, webmcp, agent_access_model, agentic_wallets, aeo, readable_first, knowledge_graph_rag, agent_memory), each spanning 3 to 4 modules via already_inside. All 9 have empty purpose fields.
- Strictly over edges whose both endpoints are real nodes, exactly 3 nodes have any connection: family:readable_first (2), context_compression.py (1), corpus_expand.py (1). One connected component of size 3.

## 3. Thinnest edges: what we know least

1. **The law layer is unlinked.** All 794 has_invariant edges dangle: the writer emits `invariant:{_norm(inv)[:40]}` targets (`mag/knowledge_graph.py:165`) but never materializes invariant nodes (0 nodes with `invariant:` prefix in nodes[]). The estate's own invariants exist only as edge text truncated to 120 chars.
2. **The graph's connective tissue is 2 edges.** Only 2 of 825 edges join two real nodes: family:readable_first -> context_compression.py and family:readable_first -> corpus_expand.py (0.24% of edges). 29 of the 31 already_inside edges have a dangling `to` because the writer builds ids from prose we_have entries (`module:{Path(str(m)).name}`, `mag/knowledge_graph.py:169`), which never match real `module:<file>.py` ids.
3. **Half the estate is edgeless.** 1,057 knowledge nodes (knot 400 + case_law 300 + doctrine 217 + steal 140 = 50.7%) have zero edges each. Nothing links filed knowledge to the code it governs.
4. **knot: 400 content-less stubs.** Every knot has label "knot" and empty summary; only `tension` + `ts` carry data. Cause: the writer reads `theme`/`summary` fields (`mag/knowledge_graph.py:102-104`) that rows of `memory/biography/verkle_chain.jsonl` (8.0 MB, live) do not carry.
5. **case_law: 300 nodes, 1 id.** All 300 share the id `law:` (builder `law:{str(r.get('id') or '')[:12]}`, `mag/knowledge_graph.py:123`), label "law", empty summary and maps_to. Cause: `memory/improve/skill_ledger.jsonl` (2.4 MB, live) rows are `skill_fired.v1` events keyed schema/skill_id/job/pack_mode/chars_injected/ts (verified on its last row) with none of the id/title/move/pattern fields the loader expects.
6. **doctrine and steal: named but unconnected.** 217 doctrine nodes (sources: leaked_prompt_mine 31, attractor_tools 22, tesuji_capture 15, deep_research_steal 15, shadow_work 14, frontier_advice 9, plus hand-folded) and 140 steal nodes carry labels and source paths, zero purpose, zero edges.

## 4. Frontier implications

- The "most connected topics" reading is capped and artifact-laden: degree 4 is a write cap (`mag/knowledge_graph.py:164`), degree 9 is an empty-law collision. True semantic connectivity is the readable_first family cluster only.
- Cheapest unknowns to thicken, in order: (a) materialize invariant nodes from the 794 edge texts (the knowledge already exists in the graph); (b) normalize already_inside targets so the 9 families actually bind to modules; (c) backfill knot theme/summary from verkle rows and case_law title/move from skill_ledger rows, which would also fire the dead maps_to builder (`mag/knowledge_graph.py:171-173`).

Nothing in this file is speculative: every count was computed on the bytes this session; every mechanism claim cites the writer source.
