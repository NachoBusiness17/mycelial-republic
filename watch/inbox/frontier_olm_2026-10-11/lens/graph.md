# Lens: knowledge_graph.json - most connected topics and thinnest edges

- Source: `memory/knowledge_graph.json` (schema `knowledge_graph.v2`, ts `2026-10-11T09:09:54.151941Z`; single-line JSON, 1,189,124 bytes via `wc -c`).
- Method: read the file, then three analysis passes with the repo interpreter (`.venv/Scripts/python.exe`, heredoc, 2026-10-11) computing degree counts over `edges[].from/.to`, relation counts over `edges[].rel`, kind cross-tabs, and union-find weak components. All numbers below are that command's output, not estimates.

## Graph shape

- 2,944 nodes / 1,141 edges; node kinds: module 1,057, invariant 809, knot 400, case_law 300, doctrine 217, steal 140, landscape 9, superseded 6, superseder 6.
- Only 4 relation types exist: `has_invariant` 817, `maps_to` 300, `already_inside` 18, `superseded_by` 6.
- 1,805 weakly connected components; largest is the skills_pack star (273 nodes), then skill_ledger (29), then the `invariant:Law never send 200 token system prompts` hub (20).
- Degree: mean 0.78, median 1, max 272. 1,209 nodes (41%) have degree 0; 1,587 have degree exactly 1.

## Most connected topics

| Degree | Kind | Node |
|---|---|---|
| 272 | module | skills_pack |
| 28 | module | skill_ledger |
| 9 | invariant | "Law:" (Law never send 200 token system prompts hub) |
| 7 | module | context_compression |
| 6 | module | water_swarm, rib_k8s, ghost_ledger, constitutional_critique |
| 5 | module | context_checkpoint, lora_pipeline |
| 4 | module | 40+ modules (percolator, frontier_scout, data_refinery, cost_enforcer, mixture_of_agents, ...) |

Caveat on the #1 hub: all 272 skills_pack edges are `case_law -> maps_to -> skills_pack`; the 300 `maps_to` edges in the whole graph have exactly 2 distinct targets (skills_pack 272, skill_ledger 28). The "most connected topic" is really "where case law got filed", not a densely reasoned cluster.

## Thinnest edges (what we know least)

1. Entire knowledge classes are wired to nothing. Zero-edge nodes by kind: knot 400/400, doctrine 217/217, steal 140/140, module 450/1057, landscape 2/9 (`mcp_stateless`, `webmcp`). Not one doctrine, knot, or steal node has a single edge to any module or to each other.
2. The judgment layer is disconnected from the code layer. The only cross-kind edges present are module->invariant (817), case_law->module (300, into 2 files), landscape->module (18), superseded->superseder (6). Doctrine->module, knot->module, steal->module counts are all zero in the kind matrix.
3. Orphan themes by label sample: 156 `autonomous_janitor` knots plus 215 session-file knots (e.g. `2026-08-13_1602_session_mag-agen_*.knot`), 16 `biography`, 9 `mag_hands`; doctrines like `context-rot-is-real`, `stable-prefix-for-cache`, `externalize-memory`, `length-neq-tier`, `distill-don't-dump`; steals like `CONTEXT_WINDOW_HOP_RIGHTSIZING_20260810`, `AGENTIC_INTERNET_STACK_STEAL_20260810`. This knowledge exists in the graph but nothing in the graph points at it.
4. Relation poverty: no edge type expresses "doctrine governs module", "steal fed module", or "knot resolved into doctrine". `superseded_by` has only 6 instances, so contradiction/versioning coverage is near-nil; its 6 uses are real errata rows (GSTD surface, 19M-token mine spend, 48h-synth F2 forecasts, 50-wide tally gap, STANDING_RAILS doc-first, borrow-target rule count).
5. Fragmentation: with 1,805 components over 2,944 nodes, the average piece of recorded knowledge is an island.

## Reading for the sweep

The graph's only strong signal is case law -> skills_pack/skill_ledger and modules carrying invariants. What we know least, per this artifact, is which doctrines and steals are already embodied in which modules: the estate records its laws (217 doctrines) and its stolen lessons (140 steals) but never links them to the 1,057 modules, so prior-art lookup over the graph returns almost nothing outside two skills files. Treat "doctrine X already known" claims made from this graph as unverifiable from graph structure alone; the thin edges are a wiring gap in the graph builder as much as a knowledge gap.

## Not run / limits

- I did not verify whether any other artifact (e.g. the graph builder script) stores links this JSON drops; this lens covers the JSON file only. The builder script was not located or read this session.
- Degree is computed on undirected incidence over `from`/`to`; edge `text` fields were read only for the already_inside and superseded_by samples quoted above.
