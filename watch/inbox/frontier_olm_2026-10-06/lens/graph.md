# Lens: knowledge graph - most connected topics, thinnest edges

- Source read: `memory/knowledge_graph.json` (schema `knowledge_graph.v2`, ts `2026-10-06T09:21:53.068021Z`). The file is a single-line JSON blob, so citations are file-level, not path:line.
- Instrument: repo venv interpreter `./.venv/Scripts/python.exe` over three throwaway analysis scripts (`kg_lens_analyze.py`, `kg_lens_analyze2.py`, `kg_lens_analyze3.py` in the session exec dir), each a plain `json.load` + Counter pass. Every number below is from those runs this session; nothing hand-copied.

## Shape

- 2,924 nodes / 1,133 edges. Node kinds: module 1,051 · invariant 807 · knot 400 · case_law 300 · doctrine 217 · steal 140 · landscape 9.
- Edge relations, total 1,133: `has_invariant` 815 (module to invariant), `maps_to` 300 (case_law to module), `already_inside` 18 (landscape family to module). Zero dangling endpoints (every edge endpoint resolves to a node).

## Most connected topics (what we know most)

| Node | Degree | What the edges are |
|---|---|---|
| `module:skills_pack.py` | 285 | 285 `maps_to` case laws (95% of all case law) |
| `module:skill_ledger.py` | 15 | 15 `maps_to` case laws |
| `invariant:law ` (id carries a trailing space) | 9 | 9 modules citing the law invariant via `has_invariant` |
| `module:context_compression.py` | 7 | has_invariant + already_inside |
| `constitutional_critique`, `ghost_ledger`, `rib_k8s`, `water_swarm` | 6 each | mixed |

The estate's best-evidenced organ is the skill pack/ledger pair: all 300 case-law nodes land on exactly those 2 of 1,051 modules (285 + 15). Case law samples seen: `law:2397fcca4c17` (memory-verkle), `law:1cece93bcfa7` (ponytail-ladder).

## Thinnest edges (what we know least)

1. **Case-law evidence is a two-module monoculture.** 300/300 case laws map to `skills_pack.py` (285) or `skill_ledger.py` (15); the other 1,049 modules have zero case law. Judgment history does not reach the rest of the codebase.
2. **The knot layer is fully disconnected.** All 400 `knot:*` nodes (labels like `backfill-workflow-subagent-actor-9-N`) have zero edges - no case law, no family, no invariant touches any knot.
3. **Doctrine (217 nodes) and steal (140 nodes) layers have zero edges each.** Two whole imported corpora are islands; nothing links them to modules or to each other.
4. **41% of all nodes are isolated:** 1,203 of 2,924 have degree 0 (all knots, all doctrine, all steal, plus 444 of 1,051 modules). 2,104 nodes have zero incoming edges.
5. **Thinnest relation: `already_inside` (18 edges)** - the only cross-layer semantic link, from 7 landscape families (agent_first_browser, agent_access_model, agentic_wallets, aeo, readable_first, knowledge_graph_rag, agent_memory) into 9 modules. Families `mcp_stateless` and `webmcp` have zero edges.
6. **Data hygiene:** invariant ids carry trailing spaces (`invariant:law `); exact-match lookups on the trimmed id return 0 and silently undercount the hub.

## Frontier read

The graph knows *what exists* (modules, invariants) far better than *what connects*: three whole layers (knots 400, doctrine 217, steal 140 = 757 nodes, 26% of the graph) float free, and case law covers 0.19% of modules. Wiring `maps_to` from case law beyond the skill-pack pair, and linking knots/doctrine/steal into the module graph, is the thinnest-edge frontier this lens can name.
