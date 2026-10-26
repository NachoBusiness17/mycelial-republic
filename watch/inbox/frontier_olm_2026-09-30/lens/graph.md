# Lens: knowledge_graph.json connectivity (frontier olm, 2026-09-30)

Source: `memory/knowledge_graph.json` (schema `knowledge_graph.v2`, ts 2026-09-30T02:49:46Z, 773 KB). Read in full via `.venv/Scripts/python.exe`; every number below is computed in this session from that file. Builder: `mag/knowledge_graph.py` (writes via `build()` at mag/knowledge_graph.py:448, `dream()` at mag/knowledge_graph.py:419).

## Shape

- 2,086 nodes, 1,787 distinct ids, 825 edges.
- Node kinds: module 1,020; knot 400; case_law 300; doctrine 217; steal 140; landscape 9.
- Edge relations, only two in the whole graph: `has_invariant` 794, `already_inside` 31.

## The graph is almost entirely virtual

After stripping whitespace, **823 of 825 edges have at least one endpoint that matches no node id**. Only 2 edges connect two real nodes: `family:readable_first` -> `module:context_compression.py` and -> `module:corpus_expand.py`. The rest are id-format mismatches between writer and reader.

Three mechanisms, all in the builder:

1. **Invariant edges target truncated virtual ids** (mag/knowledge_graph.py:165): `to: f"invariant:{_norm(inv)[:40]}"`. Invariants live as text arrays on module nodes, never as nodes, so all 794 `has_invariant` edges point at 40-char-truncated strings that exist nowhere. Examples: `invariant:schema percolator v1 deterministic 0 dep`, `invariant:schema mag agent arena v1`.
2. **maps_to edges embed free text into ids** (mag/knowledge_graph.py:172 builds `to: f"module:{Path(str(n['maps_to'])).name}"` while module node ids at mag/knowledge_graph.py:85 are real filenames): maps_to values like `browser_driver.py (Playwright-over-CDP, free frontend` produce target ids that never resolve. 29 of 31 `already_inside` edges dangle this way.
3. **All 300 case_law nodes share one literal id `law:`** (mag/knowledge_graph.py:123: `id: f"law:{str(r.get('id') or '')[:12]}"` with an empty id in the ledger). Three hundred case-law facts collapse to one un-linkable node; 299 are unreachable by any id-keyed consumer.

## Most connected topics (what we know most)

- **The 9 landscape family nodes are the only connective tissue**: family:agent_first_browser, mcp_stateless, webmcp, agent_access_model, agentic_wallets, aeo, readable_first, knowledge_graph_rag, agent_memory. Each carries 3 to 4 `already_inside` out-edges; `family:readable_first` is the sole node whose links actually resolve (degree 2).
- **Modules with 4 invariant-links each** (the lenient ceiling): auto_quantize, behavioral_lensing, campaign_simulator, chain_query, constitutional_critique, context_checkpoint, context_compression, copilot_bridge.
- **The most-referenced single target in the graph is `invariant:law `** (9 in-edges) from agent_state.py, behavior_catch.py, corpus_query.py, diary_node.py, field_steal.py, intention_brief.py, local_usable.py, session_freeze.py, voice_handoff.py. Its edge text is just `Law:` with nothing after: 9 modules cite a law with no body.

## Thinnest edges (what we know least)

- 823 of 825 edges (99.8 percent) fail id resolution; the edge layer is decorative until the three id defects above are fixed.
- 757 knowledge nodes have zero edges of any kind: 400 knots, 217 doctrines, 140 steals. The estate's accumulated lessons are isolated vertices; only the BM25 text search (mag/knowledge_graph.py:286) can reach them, never a graph walk.
- 428 of 1,020 modules (42 percent) carry an empty invariants array, so the `has_invariant` relation covers barely half the code estate.
- All 300 case_law facts are individually un-linkable (shared id `law:`).
- The 9-module unnamed law (`invariant:law `) is simultaneously the most-cited and emptiest fact in the file.

## What to fix first

Rank by leverage: (1) give every ledger row a real id so the 300 case-law nodes stop collapsing (mag/knowledge_graph.py:123); (2) emit invariant nodes instead of 40-char truncated virtual targets (mag/knowledge_graph.py:165), which converts 794 dangling edges into real structure; (3) normalize maps_to to the module node id convention (mag/knowledge_graph.py:85 vs :172). After those three, resolved-edge ratio goes from 2/825 to potentially all 825, and doctrine/knot/steal nodes need any first edge at all.
