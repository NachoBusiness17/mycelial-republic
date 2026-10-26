# Lens: knowledge_graph.json (most connected topics, thinnest edges)

- Lens: `lens-graph`
- Date: 2026-10-02
- Source read: `memory/knowledge_graph.json` (single-line JSON, line 1; `schema: knowledge_graph.v2`, `ts: 2026-09-30T02:49:46.836118Z`, 772,996 bytes)
- Method: every number below was computed this sitting with `.venv\Scripts\python.exe` over the file (degree counts, unique-ID dedupe, ghost-endpoint scan, per-kind isolation counts, invariant-sharing census). No numbers were carried from any prior report.

## 1. Graph vitals

- 2,086 node entries, 1,786 unique IDs. The gap is one junk row duplicated 300x: id `law:`, kind `case_law`, label `law`, empty purpose, source `memory/improve/skill_ledger.jsonl`. The entire `case_law` kind is that one parse artifact, not 300 precedents.
- Real kinds: `module` 1,020, `knot` 400, `doctrine` 217, `steal` 140, `landscape` 9.
- 825 edges, only two verbs: `has_invariant` (794, module to invariant slug) and `already_inside` (31, family to module). Zero module-to-module, doctrine-to-module, steal-to-module, or knot-to-anything edges exist anywhere in the file.

## 2. Most connected topics

1. **The degree-9 hub is a bug.** `invariant:law ` (ID carries a trailing space; edge text is literally `Law:`) collects 9 modules: agent_state, behavior_catch, corpus_query, diary_node, field_steal, intention_brief, local_usable, session_freeze, voice_handoff. Every docstring invariant starting "Law:" was slugified to the same ID. The graph's single strongest tie is an artifact.
2. **Invariant sharing is otherwise nil.** Exactly one other invariant is shared by 2+ modules: `invariant:schema percolator v1 deterministic 0 dep` (module:percolator.py + module:percolator_heal_test.py). The module-invariant bipartite graph is 784 invariants wide and otherwise a 1-to-1 matching: no topic clusters emerge.
3. **The only genuine multi-module topics are 9 `landscape`/family nodes** with 31 `already_inside` memberships: agent_access_model 4, agentic_wallets 4, readable_first 4, agent_memory 4, agent_first_browser 3, mcp_stateless 3, webmcp 3, aeo 3, knowledge_graph_rag 3. All nine are frontier-watch themes (agentic browsers, MCP, wallets, RAG), none are estate organs.
4. **Best-instrumented modules carry 4 invariants** (27 of them: auto_quantize, behavioral_lensing, campaign_simulator, chain_query, constitutional_critique, context_checkpoint, context_compression, copilot_bridge, data_refinery, dspy_sovereign, frontier_scout, ga4_progression, ghost_ledger, lens_library, lora_pipeline, mixture_of_agents, narrative_engine, prompt_archaeology, renderman, rib_k8s, riddler_campaign, session_koan, session_ritual, tokenomics, ...). 461 modules have exactly 1 invariant.

## 3. Thinnest edges (what we know least)

1. **doctrine to code: 0 edges.** All 217 doctrine nodes are isolated. The estate's laws are graph-disconnected from the modules that should enforce them.
2. **steal to code: 0 edges.** All 140 steal nodes are isolated. Stolen intel is never linked to what (if anything) landed from it.
3. **knots: all 400 isolated and contentless.** Shape: `id: knot:<hash>`, `label: "knot"`, `summary: ""`, tension slugs like `fkb:guar`, source `memory/biography/verkle_chain.jsonl`. We stored hashes, not readable knowledge.
4. **66% of the graph is edgeless:** 1,184 of 1,786 unique nodes have degree 0 (427 module + 400 knot + 217 doctrine + 140 steal). Only 593 modules plus the 9 families carry any connection at all.
5. **Referential integrity is broken:** 814 edge endpoints resolve to no node entry. That is 794 invariant slugs (untyped by design) plus 29 mangled module IDs where prose leaked into the ID column (`module:Name headers)`, `module: kill-on-spend)`, `module: stateless_research (stateless doctrine)`, ...), all born in the family/already_inside rows.

## 4. Verdict

This is a module catalog with per-module docstring tags, plus 9 frontier-watch families; it is not yet a knowledge graph. The thinnest edge class in the estate is doctrine/steal/knot to code: 757 nodes, 0 edges. Second thinnest: module-to-module structure, where 1,020 modules share exactly 2 invariants. If the frontier sweep wants a "least known" target, it is the linkage layer, not any single topic: the graph records that laws and steals EXIST but never WHICH code they bind.

## Repair sketch (next seat)

- Give knot nodes their verkle payload summary (the chain holds the text; the graph holds the hash).
- Emit doctrine-to-module and steal-to-module edges at build time (`mag/knowledge_graph.py fold()` already walks sources per the family rows).
- Slugify invariants with content, not prefix (the `Law:` collision above), and node-ify every invariant/family endpoint so ghosts go to zero.
