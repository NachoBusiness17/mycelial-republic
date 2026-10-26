# Lens: knowledge_graph.json (frontier olm, 2026-10-10)

Source: `memory/knowledge_graph.json` (schema `knowledge_graph.v2`, ts `2026-10-06T18:06:27.608164Z`, 4 days stale at reading).
Scale: 2938 nodes, 1256 edges, zero dangling edge endpoints.
Node kinds: module 1053, invariant 807, knot 400, case_law 300, doctrine 217, steal 140, superseder 6, superseded 6, landscape/family 9.
Edge rels: has_invariant 815, maps_to 300, why_context 117, already_inside 18, superseded_by 6. No weight field exists on edges, so thinness is measured structurally (degree, components, orphan rate).

Instrument: every number below came from these commands run this ask (repo venv, `.venv/Scripts/python.exe`, on the checked-out tree):

1. `./.venv/Scripts/python.exe -c` json.load + Counter over node kinds, edge rels, id prefixes, edge/node field keys.
2. Same interpreter: degree census (in+out per node), per-kind mean/zero-degree/max, dangling endpoint count.
3. Same interpreter: undirected connected components (stack DFS), hub of each large component, rel breakdown into `module:skills_pack.py`, zero-degree samples per kind.
4. Same interpreter: knot tension-field census + ts range, why_context heal census, landscape family dump, superseded_by edge dump, knot/steal edge listings.

## Most connected topics

| Node | Kind | deg (out/in) | What it is |
|---|---|---|---|
| `module:skills_pack.py` | module | 287 (0/287) | 287 of 300 case_law nodes `maps_to` it |
| `module:memlang.py` | module | 22 (22/0) | `why_context` to 21 knots + 1 invariant (graph_heal.v0) |
| `module:leaked_prompt_mine.py` | module | 21 (21/0) | `why_context` to 20 doctrine + 1 invariant |
| `module:skill_ledger.py` | module | 13 (0/13) | the other 13 case_law `maps_to` target |
| `invariant:law ` (trailing space in id) | invariant | 9 (0/9) | shared law invariant cited by 10 modules |
| `module:context_compression.py` | module | 7 (4/3) | hub of a 17-node module+invariant+family component |
| `module:ghost_ledger.py`, `module:constitutional_critique.py`, `module:rib_k8s.py`, `module:water_swarm.py` | module | 6 each | small invariant-spoke hubs |

Caveat on the crown: the top degree is a concentration artifact, not a topic. The `maps_to` relation puts 287/300 case-law nodes on one module and the remaining 13 on one other module; case-law connectivity discriminates nothing. True multi-rel hubs are memlang, leaked_prompt_mine, context_compression, ghost_ledger.

## Thinnest edges (what we know least)

1. **Knots are captured but never wired: 379/400 (94.8%) zero-degree.** Only 21 knots have any edge, all pendant `why_context` leaves of memlang. 238/400 knots have an empty `tension` field; the sampled non-empty tensions are opaque tokens (`fkb:_:d2`, `fkb:amd_`). Knot ts range is fresh (2026-10-03 to 2026-10-06), so this is a linking failure, not staleness. One knot carries a float (NaN) `tension`, a hygiene defect.
2. **Doctrine is 87.6% islands: 190/217 zero-degree.** The 27 connected ones all hang off leaked_prompt_mine's `why_context` spoke.
3. **Steals are 87.1% islands: 122/140 zero-degree.** Only 18 `already_inside` edges exist in the whole graph, all from the 9 `family:*` landscape nodes into just 8 distinct modules (browser_driver, browser_env, grok_free, cost_enforcer, ghost_ledger, grok_rightsize, corpus_expand, context_compression, skill_drop, knowledge_graph, code_map). 122 banked steals have no recorded "already inside the estate" link at all.
4. **36% of the graph is singletons: 1066 of 2938 nodes touch nothing; 1687 components total, largest 288.**
5. **Supersession is vestigial:** 6 `superseded_by` edges, all placeholder rows (`superseded:row-1` to `superseder:row-1` ... `row-6`).
6. **Landscape families are hollow labels:** all 9 `family:*` nodes have an empty `we_have` field.
7. **35.5% of modules (374/1053) have zero edges** beyond their own existence as nodes.

## Read for the frontier sweep

The graph's knowledge lives as per-module invariant spokes (has_invariant, 815 edges) and is densest exactly where a module author chose to annotate. The connective tissue that would let the sweep know what we already know is thinnest in three classes: knot-tension to doctrine/steal cross-links, steal to estate-module `already_inside` mapping (18 links for 140 steals), and supersession chains (placeholders only). Any frontier find should be checked against the 122 orphan steals and 190 orphan doctrines before it is treated as new; the graph currently cannot answer that check for ~87% of its own holdings. The snapshot is also 4 days old; knots minted since 2026-10-06 are not in it.
