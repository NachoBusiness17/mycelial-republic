# LENS: knowledge_graph.json - connectivity census (2026-10-09)

Instrument: read + computed over `memory/knowledge_graph.json` (1,212,819 bytes, mtime 2026-10-07 05:23 local), schema `knowledge_graph.v2`, graph `ts` 2026-10-06T18:06:27.608164Z. All numbers below were computed this session with `.venv/Scripts/python.exe` against the file; commands quoted per section. No numbers hand-copied.

## Shape

- 2,938 nodes / 1,256 edges.
- Node kinds: module 1,053; invariant 807; knot 400; case_law 300; doctrine 217; steal 140; landscape 9; superseded 6; superseder 6.
- Edge relations: `has_invariant` 815 (64.9%); `maps_to` 300; `why_context` 117; `already_inside` 18; `superseded_by` 6.
- Zero empty-text edges; 117 edges carry a `heal` field (all `why_context`).

## Most connected topics (degree, in+out)

| Node | Degree | Shape |
|---|---|---|
| `module:skills_pack.py` | 287 | 100% inbound `maps_to` from 287 distinct `case_law` nodes: one file is the precedent magnet of the whole estate |
| `module:memlang.py` | 22 | |
| `module:leaked_prompt_mine.py` | 21 | |
| `module:skill_ledger.py` | 13 | |
| `invariant:law ` (id carries a trailing space) | 9 | `has_invariant` from 9 modules: agent_state, behavior_catch, corpus_query, diary_node, field_steal, intention_brief, local_usable, session_freeze, voice_handoff |
| `module:context_compression.py` | 7 | |

The degree curve falls off a cliff after the hub: rank 2 is 22. Connectivity is a one-star graph, not a web.

## Thinnest edges (what we know least)

1. **`superseded_by`: 6 edges in the entire graph.** The estate almost never records what replaced what. All 6 are 2026-10-01..05 corrections (GSTD surface, the 09-29 mine spend, 48h-synth F2 forecasts, the 50-wide tally gap, STANDING_RAILS adoption story, the 28-vs-31 gate-rule count). Self-correction exists but is hand-registered, not wired.
2. **1,066 of 2,938 nodes (36.3%) are orphans (degree 0):** knot 379, module 374, doctrine 190, steal 122, landscape 1. Recorded, never linked.
   - Orphan doctrines include `tesuji:route-through-architecture`, `agentic-internet-stack`, `frontier-label-vs-frontier-call`, `problem-knot:stigmergy-lattice-pheromone-trail`, `ties-back-parent`.
   - Orphan steals include CONTEXT_WINDOW_HOP_RIGHTSIZING_20260810, VAULT_SALT_GRAPH_20260814, STEAL_ANCHOR_NEXT_GHOST_SPINE_20260814, FLOCK_STEAL_MEMWEAVE-TEST_20260810, BRIAR_STEAL_20260810.
   - Orphan knots are session tension records (autonomous-janitor fkb tensions, backfill-workflow subactor tensions, untagged LAW knots).
3. **451 of 1,053 modules (42.8%) have no `has_invariant` edge at all.** Half the code surface carries no stated invariant in this graph.
4. **`already_inside`: 18 edges, all inside the 9-node frontier landscape cluster** (agent_first_browser, agent_access_model, agentic_wallets, aeo, readable_first, knowledge_graph_rag, agent_memory wiring into cost_enforcer, ghost_ledger, context_compression, corpus_expand, browser_env, knowledge_graph, code_map, skill_drop, grok_free, grok_rightsize). Overlap-with-what-we-have is mapped for the frontier only; the rest of the estate's redundancy is unmapped.
5. **Fragmentation:** connected components (undirected): one 288-node component (the skills_pack case-law star), 454 two-node fragments (mostly module + its own invariant), 112 three-node, remainder tiny, plus the 1,066 singletons. Cross-domain connective tissue is nearly absent: of 1,256 edges, 815 are module-to-own-invariant bookkeeping.
6. **Landscape's lone orphan:** `mcp_stateless` ("MCP v2 - the protocol went STATELESS") is the only landscape node with zero edges. A frontier fact banked and wired to nothing.

## Data-quality flags

- The `invariant:law` node id is stored as `invariant:law ` with a trailing space (`repr` verified). Exact-match joins on the cleaned string silently miss it.
- Zero dangling edge endpoints (all 1,256 edge endpoints resolve to node ids), so the thinness above is genuine missing knowledge, not broken references.

## Frontier takeaway

The graph knows ONE thing densely (skills_pack precedents) and everything else thinly. The cheapest unknown-knowledge buys, in order: (a) wire the 691 orphan doctrine/steal/knot nodes to the modules they name (they cite sessions and files in their own summaries); (b) give the 451 invariant-less modules at least one stated invariant; (c) grow `superseded_by` and `already_inside` beyond the frontier cluster, since those two relations are the estate's only redundancy and correction memory in this graph.
