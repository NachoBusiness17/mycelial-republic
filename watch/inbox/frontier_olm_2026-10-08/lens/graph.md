# Lens: knowledge graph - most connected topics and thinnest edges

- Date: 2026-10-08 (lens-graph seat, frontier_olm run)
- Source read: `memory/knowledge_graph.json` (schema `knowledge_graph.v2`, ts `2026-10-06T18:06:27.608164Z`, 2,938 nodes / 1,256 edges - read from the file header)
- Method: parsed with `.venv/Scripts/python.exe` (repo venv) in five passes this session: schema/keys dump; degree + kind counters; undirected connected components; isolated-node sampling (seed 7); non-hub case_law / `already_inside` / empty-edge-text checks. All numbers below are from those runs against this file, not from any report.

## Shape

- Node kinds: module 1053, invariant 807, knot 400, case_law 300, doctrine 217, steal 140, landscape 9 (`family:*` ids), superseded 6, superseder 6.
- Edge rels: `has_invariant` 815, `maps_to` 300, `why_context` 117, `already_inside` 18, `superseded_by` 6.
- 1,687 connected components; largest is 288 nodes. 1,066 nodes (36%) have degree 0; 1,676 more have degree 1 - only ~196 of 2,938 nodes have degree >= 2.
- Edge text: 0 of 1,256 edges have empty `text` (edges are annotated; the thinness is structural, not textual).

## Most connected topics (what we know best)

1. `module:skills_pack.py` - degree 287, i.e. 23% of ALL edges. The 288-node "main" component is exactly skills_pack + the 287 `case_law` nodes that `maps_to` it. All skill case law hangs off one file.
2. `module:memlang.py` - degree 22: the 21 connected knots (all `2026-10-04_*_untagged_memlang-*.knot`) plus its invariant. It is the only module knots attach to.
3. `module:leaked_prompt_mine.py` - degree 21: centers the 22-node leaked-doctrine island (`doctrine:leaked anthropic/bolt/cline/cluely/cursor/...` via `why_context`).
4. `module:skill_ledger.py` - degree 13: exactly the 13 non-hub case_law nodes (`law:<sha12>` ids).
5. `invariant:law ` - degree 9, the most-linked invariant.
6. `module:context_compression.py` - degree 7, top target of `family:*` `why_context` edges.

## Thinnest edges (what we know least)

- **Knots: 379/400 isolated.** The 21 connected all point only at memlang.py. 162 of the 400 share the label `autonomous_janitor` (plus duplicate-label runs: `mag_hands` x10, `backfill-workflow-subagent-actor-*` x3-4 each) - duplicate identities, no way to tell which knot is which from the graph alone.
- **Doctrine: 190/217 isolated** (e.g. `socratic:aporia-is-progress`, `tesuji:route-through-architecture`, `shadow:no_throne`) - named lessons with zero recorded relationships.
- **Steal: 122/140 isolated** (2026-08-10..15 steals: `BRIAR_STEAL_20260810`, `DEEP_RESEARCH_MEMLANDS_20260811`, `PLAY_AS_WORK_20260814`, ...) - the steal corpus is catalogued but never woven to modules or doctrine.
- **Modules: 374/1053 isolated, and all 374 carry a written `purpose`** - known-but-unwoven, not empty stubs. Examples: `api_gateway.py`, `atlas.py`, `biography.py`, `autopilot.py`.
- **Invariants never cross-link:** 807 invariant nodes, avg degree 1.01 - each hangs off exactly one module via `has_invariant`; no invariant-to-doctrine or invariant-to-invariant edges exist.
- **Case law is a two-file monoculture:** all 300 case_law nodes have degree exactly 1; 287 point at `skills_pack.py`, 13 at `skill_ledger.py`. No case law maps to any of the other 1,051 modules.
- **The only family weave is 18 edges:** 9 `family:*` landscape nodes cover ~11 modules (browser_env, cost_enforcer, ghost_ledger, corpus_expand, context_compression, knowledge_graph, ...). Everything else in the estate has no family grouping.

## Reading for the frontier sweep

The graph is a catalog, not a web: two hub spokes (skills_pack, skill_ledger), one knot spoke (memlang), one doctrine island (leaked_prompt_mine), and a long tail of unconnected knowledge. The thinnest region is knot/doctrine/steal - mined lessons that exist as nodes but have no edges saying where they came from or what they apply to. Any frontier claim of "we already know X" backed by this graph should treat isolated nodes as unverified priors: the label exists, the linkage does not.
