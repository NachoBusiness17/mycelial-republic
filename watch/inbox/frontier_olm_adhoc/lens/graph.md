# Lens: knowledge_graph.json - hubs and thin ice (2026-10-11 snapshot)

Instrument: `memory/knowledge_graph.json`, schema `knowledge_graph.v2`, stamped `ts: 2026-10-11T09:09:54.151941Z`.
All numbers computed this session (2026-10-11) with `.venv/Scripts/python.exe` (stdlib json + collections) over the whole file: **2,944 nodes, 1,141 edges, zero dangling endpoints, zero empty-text edges.** The file is minified JSON, so path:line cites are meaningless here; claims cite node/edge ids and field values instead.

Shape: node kinds module 1,057 / invariant 809 / knot 400 / case_law 300 / doctrine 217 / steal 140 / landscape 9 / superseded 6 / superseder 6. Edge rels: has_invariant 817 / maps_to 300 / already_inside 18 / superseded_by 6. This file supersedes the 2026-10-10 lens over the `ts: 2026-10-06` snapshot.

## Most connected topics

1. **`module:skills_pack.py`, degree 272, and it is telemetry, not a topic.** All 272 edges are `maps_to` FROM case_law nodes (sample `law:ad321e80985d`, text `skill_fired memory-verkle job=default pack=excerpt chars_injected=298`, source `memory/improve/skill_ledger.jsonl`). 272 of 300 case_law nodes collapse onto this one module; the other 28 onto `module:skill_ledger.py` (degree 28). The estate's entire case-law layer covers exactly 2 modules, both the skill-firing ledger surface.
2. **`invariant:law ` (label "Law:", source `mag/agent_state.py`), degree 9.** A degenerate parser-artifact invariant whose entire text is the string "Law:", shared as the invariant of record by 9 modules. A junk hub.
3. **`module:context_compression`, degree 7 (3 in, 4 out)**: the only node in the graph with meaningful two-way connectivity.
4. Flat tail of 6-out modules holding the richest invariant sets: `constitutional_critique`, `rib_k8s`, `water_swarm`, plus `ghost_ledger` (6, with 2 in).

## Thinnest edges - what we know least

- **1,209 of 2,944 nodes (41%) are degree-0 singletons, and three whole kinds have zero edges anywhere: all 400 knots, all 140 steals, all 217 doctrines** (plus 450 modules and 2 landscape). The tension telemetry, the stolen frontier art, and the distilled laws are all captured as names and never linked to anything.
- **The only semantic cross-module layer that ever existed was dropped by the regen.** The prior lens (this file, 2026-10-10, over `ts: 2026-10-06`) counted 117 `why_context` edges; today `why_context` = 0, and `module:memlang.py` / `module:leaked_prompt_mine.py` fell from degree 22 / 21 to degree 1 each. Authoring cross-links without fixing whatever emits this graph is raking leaves; which builder writes it was not traced this session (OWED).
- **The evidence layer is the emptiest thing in the estate.** `we_have` filled on 9 nodes (all `landscape` families: agent_first_browser, mcp_stateless, webmcp, agent_access_model, agentic_wallets, aeo, readable_first, knowledge_graph_rag, agent_memory); `evidence`/`banked`/`outcome` filled only on the 6 `superseded:row-*` tombstones; `delta` on 8. 99%+ of nodes carry no proof pointer.
- **Module coverage is thin where it matters: 455 of 1,057 modules have an empty `invariants` list, and 468 of the 602 that hold invariants hold exactly one.** The typical module's behavior contract is either absent or a single line.
- **Knots carry almost no signal: only 43 of 400 have a numeric `tension` (max 0.572; top labels biography, mag_hands, mirror_meta), 201 are null, the rest unparseable strings.** They are spillover from `memory/biography/verkle_chain.jsonl`, not connected knowledge.
- **The only art-to-code bridge is 18 `already_inside` edges** from the 9 landscape families to modules (e.g. `family:agent_first_browser` -> `module:browser_driver.py`). The 140 steals have no bridge at all.
- **`superseded_by` is 6 stub rows** (`superseded:row-1` -> `superseder:row-1` style): placeholder, not lineage.
- **135 invariant ids carry leading/trailing whitespace** (e.g. `invariant:schema abundance rogue v1 deterministic `), fragmenting any id-keyed dedupe.

## Read for the frontier sweep

The graph the sweep should trust is: one telemetry hub (skills_pack), one artifact hub ("Law:"), and confetti. Highest-value graph work is unchanged from the prior lens but sharper now: (1) give case_law targets beyond the 2 ledger modules, (2) attach the 140 isolated steals and 217 isolated doctrines to the modules they earned, (3) land anything new as `we_have`/`evidence`/`banked` fields, not as new singleton nodes. New risk since the last lens: cross-links do not survive regeneration (why_context vanished 10-06 -> 10-11), so durability of any manual weaving must be settled with the graph builder first.
