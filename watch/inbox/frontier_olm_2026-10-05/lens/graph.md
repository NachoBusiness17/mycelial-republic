# LENS: knowledge_graph.json (graph lens, 2026-10-05)

Source read: `memory/knowledge_graph.json` (1,191,521 bytes, mtime 2026-10-05 03:15:34 local). Schema `knowledge_graph.v2`, ts `2026-10-05T07:15:34.667608Z`. Contents: 2,919 nodes / 1,143 edges. Node kinds: module 1,049, invariant 804, knot 400, case_law 300, doctrine 217, steal 140, landscape 9. Edge relations, all three kinds the graph has: `has_invariant` 812 (module -> invariant), `maps_to` 300 (case_law -> module), `already_inside` 31 (landscape -> module). All counts from the analysis script banked beside this file: `watch/inbox/frontier_olm_2026-10-05/lens/_graph_analysis_tmp.py`, run this session with `.venv/Scripts/python.exe`.

## 1. Most connected topics (degree = edge endpoints touching the node)

| Degree | Node | What it is |
|---|---|---|
| 273 | `module:skills_pack` | mag/skills_pack.py; 273 case_law `maps_to` in-edges, zero out-edges |
| 27 | `module:skill_ledger` | mag/skill_ledger.py; the other `maps_to` sink |
| 9 | `invariant:law ` (label "Law:", empty summary) | hub invariant joining agent_state, behavior_catch, corpus_query, diary_node, field_steal, intention_brief, local_usable, session_freeze, voice_handoff |
| 6 | `module:constitutional_critique`, `module:rib_k8s`, `module:water_swarm` | most-invarianted mag modules |
| 5 | `module:context_checkpoint`, `module:context_compression` | context-layer modules |
| 4 | `auto_quantize`, `behavioral_lensing`, `campaign_simulator`, `chain_query`, `copilot_bridge`, `data_refinery`, `dspy_sovereign` (modules); landscape families `agent_access_model`, `agentic_wallets`, `readable_first`, `agent_memory` | the second tier |

Reading: the graph's center of mass is the skill-firing ledger, not the estate's knowledge. `skills_pack` plus `skill_ledger` soak up 300 of 300 `maps_to` edges because the builder hardcodes exactly those two targets (`mag/knowledge_graph.py:158` and `mag/knowledge_graph.py:164`, confirmed by the code comment at `mag/knowledge_graph.py:141` "binds it to real module: nodes").

## 2. Thinnest edges (what we know least)

1. **41.3% of the graph is isolated.** 1,204 of 2,919 nodes have degree 0: all 400 knots, all 217 doctrines, all 140 steals, and 447 of 1,049 modules. Nothing links session knots, folded doctrines, or stolen documents to any module or invariant, so the graph cannot answer "which code does this doctrine govern". The `memlang.py` routing table (`mag/memlang.py:84`) declares `learn`/`plant` as doctrine writes into this file, but the write path adds no edges.
2. **The landscape weld is broken.** Of 31 `already_inside` edges (the graph's only "we already have this" claims), 29 point at node ids that do not exist in `nodes` (for example `module: ghost_whisper (deniable memory)`, `module: allowlist)`). Only 2 resolve: `readable_first -> context_compression` and `readable_first -> corpus_expand`. Cause: `mag/knowledge_graph.py:236-239` runs `Path(str(m)).name` over the free-text `we_have` entries from `mag/ai_landscape.py`, producing ids like `module:browser_driver.py (Playwright-over-CDP, free frontends for agents)` that never match the collector's clean `module:<file>.py` ids. Nine landscape families therefore have degrees of 3 to 4 that are mostly phantoms; their real in-estate coverage is unverified in-graph.
3. **Case law collapses onto two sinks.** All 300 `maps_to` edges land on `skills_pack` (273) or `skill_ledger` (27). Skill-firing evidence never points at the domain modules that did the work, so the graph cannot rank a module by real-world use.
4. **The module layer is mag/-only.** All 1,049 module nodes source from `mag\*.py` (verified: directory histogram `{'mag': 1049}`). `tools/`, `scripts/`, `queue/`, githooks, and the test corpus have zero nodes, so graph connectivity says nothing about most of the estate's actual machinery.
5. **447 modules carry no documented invariant.** They sit in the graph as names with purposes but zero `has_invariant` edges: known to exist, unknown what law holds them.
6. **Only 3 relation types exist.** No doctrine->module, steal->module, knot->module, or invariant->invariant edges; cross-kind knowledge transfer is structurally impossible in the current schema beyond the three hardcoded builders in `mag/knowledge_graph.py:223-243`.

## 3. What to grow (thin-edge candidates for the frontier sweep)

- Repair the `already_inside` builder (`mag/knowledge_graph.py:236-239`) to resolve `we_have` free text to real module ids; that single fix converts 29 dangling claims into verifiable coverage assertions.
- Weld doctrines (217) and knots (400) to modules by source-path overlap; both node kinds carry a `source` field pointing at real files today.
- Widen `maps_to` beyond the two hardcoded sinks so case law spreads over domain modules.

## Method

Ran this session: `".venv/Scripts/python.exe" "watch/inbox/frontier_olm_2026-10-05/lens/_graph_analysis_tmp.py"` (degree, isolation, per-kind, per-directory, dangling-endpoint counts) plus two inline `.venv/Scripts/python.exe -c` probes (top-level structure; per-kind connected counts, real `already_inside` endpoints, `invariant:law ` children, module directory/extension histograms). Every number above is from those runs against the file's `ts 2026-10-05T07:15:34.667608Z` snapshot. Generator source cited from `mag/knowledge_graph.py` read this session. Nothing here is owed; all checks listed were executed.
