# Lens: knowledge graph - most connected topics and thinnest edges

- Source: `memory/knowledge_graph.json` (schema `knowledge_graph.v2`, ts `2026-10-06T18:06:27.608164Z`; single-line JSON, all facts below cite `memory/knowledge_graph.json:1`).
- Method: loaded with `.venv/Scripts/python.exe`, computed degree per node, relation cross-tabs, orphan counts, and hub neighborhoods via the Python one-liners run in this session. No numbers below are hand-copied; every count was printed by a query executed 2026-10-07 against the file on disk.

## Shape

- 2,938 nodes, 1,256 edges, zero dangling endpoints.
- Node kinds: module 1053, invariant 807, knot 400, case_law 300, doctrine 217, steal 140, doctrine-adjacent superseded 6 + superseder 6, landscape 9.
- Edge relations (all five): `has_invariant` 815 (module -> invariant), `maps_to` 300 (case_law -> module), `why_context` 117 (module -> module 50 / doctrine 27 / knot 21 / steal 18 / landscape 1), `already_inside` 18 (landscape -> module), `superseded_by` 6.
- 1,256 edges cannot weave 2,938 nodes: the graph is a star forest around a handful of hubs, not a web.

## Most connected topics (degree)

| Degree | Node | Neighborhood |
|---|---|---|
| 287 | `module:skills_pack.py` | all 287 edges are `maps_to` in-edges from case_law; 287 of the 300 case_law nodes map to it (the other 13 map to `module:skill_ledger.py`) |
| 22 | `module:memlang.py` | 1 invariant + 21 `why_context` out-edges to knots |
| 21 | `module:leaked_prompt_mine.py` | 1 invariant + 20 `why_context` out-edges to doctrines |
| 13 | `module:skill_ledger.py` | 13 `maps_to` in-edges from case_law |
| 9 | `invariant:law ` (id has a trailing space; label `Law:`, empty text) | 9 `has_invariant` in-edges from agent_state, behavior_catch, corpus_query, diary_node, field_steal, intention_brief, local_usable, session_freeze, voice_handoff |
| 7 | `module:context_compression.py` | invariants + `already_inside` from landscape families |
| 6 | `module:constitutional_critique.py`, `module:ghost_ledger.py`, `module:rib_k8s.py`, `module:water_swarm.py` | invariant + why_context + landscape ties |
| 3 each | landscape families `family:readable_first`, `family:agentic_wallets`, `family:agent_first_browser`, `family:agent_access_model` | `already_inside` + `why_context` |

Read: skills_pack is the case-law gravity well (95.7% of all case law points at one file), memlang is the knot hub, leaked_prompt_mine is the doctrine hub.

## Thinnest edges (what we know least)

1. **Orphans: 1,066 of 2,938 nodes (36.3%) have zero edges.** By kind: 379 of 400 knots (94.8% unattached), 190 of 217 doctrines (87.6%), 122 of 140 steals (87.1%), 374 of 1,053 modules (35.5%), and the landscape family `family:mcp_stateless` (the only family with no module evidence recorded). Sampled orphan knots have labels but no purpose text (e.g. `autonomous_janitor`, `backfill-workflow-subagent-actor-4-10`); sampled orphan doctrines are bare labels (`frontier-label-vs-frontier-call`, `problem-knot:stigmergy-lattice-pheromone-trail`, `distill-to-bus`).
2. **Leaves: 1,676 more nodes (57.1%) sit at degree 1.** Every one of the 300 case_law nodes and 806 of 807 non-hub invariants have exactly one edge. Case law connects only to skills_pack/skill_ledger, so the graph records nothing about which other modules implement, honor, or violate any given case.
3. **Rarest relations:** `superseded_by` (6 edges, the entire superseded/superseder class, sourcing r11-lane errata rows) and `already_inside` (18 edges).
4. **`why_context` coverage is thin:** only 27 of 217 doctrines, 21 of 400 knots, and 18 of 140 steals have any why-context edge; 50 module-to-module edges total.
5. **Degenerate hub:** the degree-9 invariant `invariant:law ` carries no invariant text at all; nine modules cite an empty "Law:" node, which looks like a parse artifact, not knowledge.
6. **Bare modules:** only 602 of 1,053 modules carry any invariant; 374 have no invariant and no relation of any kind (sampled: `autorun_status.py`, `burn_steer.py`, `seed_percolator.py`, `catalog_rescan.py` - real landed work with zero graph connections).

## What the frontier sweep should aim at

The estate's least-known territory, in order: (a) the 379 unattached knots and 190 unattached doctrines - sealed artifacts with no recorded link to any module, mechanism, or law; (b) 122 unattached steals - harvested material never folded into the graph; (c) the 374 bare modules - code with no invariant captured; (d) case law's single-hub fan - what any case means outside skills_pack is unknown; (e) `family:mcp_stateless` - a landscape family named with zero module backing. Nothing in this lens is OWED: every count above was computed and printed in this session.
