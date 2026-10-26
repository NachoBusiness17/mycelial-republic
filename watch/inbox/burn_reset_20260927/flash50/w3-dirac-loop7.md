# w3-dirac-loop7: the 7th Dirac loop, the missing edge `organ:dirac_loop -> organ:swarm_surface` (rel `route_open_gap`)

Item: w3-dirac-loop7 (flash50) · 2026-09-28 · seat: zcode (workflow gopher)
Series: loops 1-6 closed in `watch/inbox/burn_reset_20260927/dirac_loops45.md` + `dirac_loop6.md` + `watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl` (6 rows); theory mapped in `watch/inbox/burn_reset_20260927/flash50/deep-dirac-theory.md` (Finding 1: two dark loops, betti1=8 vs n_loops=6). This item proposes a NEW edge: a topological mutation that grows the loop basis from 6 to 7. The edge is PROPOSED, not landed; every number below was produced by commands run during this ask.

## 1. The ask's check, run as named

Command: `.venv/Scripts/python.exe -m mag.dirac_loop scan` (operational scope is the module default, `mag/dirac_loop.py:295-312`).

Live verdict, 2026-09-28T20:39:59Z: `ok=true, betti1=8, n_loops=6, closed_solved=6, open_gaps=0`. All six enumerated loops are banked (ledger rows 2026-09-27T22:31Z through 2026-09-28T02:59Z). The organ graph is at `mag/organ_map.py:640-678` (`operational_graph`): 33 organ nodes (REGISTRY, `mag/organ_map.py:46-420`), 21 declared transitions (`mag/organ_map.py:650-672`). Circuit rank: `m - n + c = 21 - 33 + 20 = 8` (`mag/dirac_loop.py:257-269`).

## 2. The topological constraint that narrows the search

`beta1 = m - n + c`. Adding an edge between two organs in DIFFERENT components raises m by 1 and lowers c by 1: beta1 unchanged, no new loop (it is a tree edge). A 7th loop requires an edge between two organs ALREADY in the same connected component. The main component holds exactly 14 organs: context_pack, context_admission, swarm_surface, swarm_worker, context_checkpoint, verkle_knot, manifest, dirac_loop, openclaw, switchboard, blackboard, effect_broker, self_audit, water_computer (from the 21 transitions at `mag/organ_map.py:650-672`). The other 19 organs (operator_mode, policy_engine, harness, elder, fireball_cycle, main_channel, atlas, basecamp, session_bridge, ask_router, swarm_cycle, research_worker, read_archive, board_tailer, trajectory_rib, live_ops_readiness, switchboard_v2, fleet_structure, host_resolver) are isolated vertices: any edge touching one of them merges components and creates ZERO loops. So the rival couplings I found in code (effect_broker consults policy_engine at `mag/effect_broker.py:213-218`; worker senses the blackboard at `mag/swarm_worker.py:254-262`) are real wires but topologically cannot be the 7th loop today.

## 3. The proposed edge

```
("dirac_loop", "swarm_surface", "route_open_gap")
```

One line in the transitions tuple at `mag/organ_map.py:650-672`, same shape as its 21 siblings (`evidence_required: receipt:dirac_loop->swarm_surface`).

### Why this edge, grounded in how the estate actually operates

1. **The detector's own doctrine mandates it.** `mag/dirac_loop.py:18`: "A loop whose invariant is NOVEL = OPEN = a GAP the swarm/flock should fill." The module declares the handoff in its header law and the graph does not carry it. dirac_loop's only outbound edge today is `dirac_loop -> context_admission (observe)` (`mag/organ_map.py:660`); scan results otherwise die as JSON on stdout.
2. **The receiving organ is built for exactly this and says so.** `mag/swarm_surface.py:1-14`: "THE ONE shared primitive every task surface uses to route NOVEL research to the swarm: dedupe (by content anchor) + enqueue ... every new surface calls route_novel() and the swarm handles it." The operator's standing self-steal law is quoted in the same header (`mag/swarm_surface.py:6-7`): "this should be everywhere no? rightsize it ... weave it in though self steal don't invent."
3. **The primitive is proven at fleet scale.** `memory/swarm_surface/sent.jsonl` holds 2,191 routed rows across 100+ surfaces (live count run this ask; surfaces include autonomous_research, wow-clone-swarm, deep-research, corpus_ingest...). Call sites: `mag/autonomous_research.py:166,214,282,484,551`. None of the 100+ surfaces is named `dirac_loop`: the gap detector never routes.
4. **The estate already operates open-gaps-as-work-orders, one actor short.** `mag/ghost_server.py:38` serves `{"id": "quests/open", "desc": "the open loops / gaps to fill", "via": "dirac_loop.scan"}` to ghost actors. The concept is live; the swarm leg of the same contract is the missing edge.
5. **The current consumers only look, none dispatch.** `mag/dogfood_audit.py:137-144` probes dirac and reports; `mag/context_pack.py:19-31,931,1057` counts closed/total into every seat's pack ("Dirac visor"). Seats SEE the gap count and have no organ-level path to act on it.
6. **The drain side exists.** swarm_worker is wired for local drain (`mag/organ_map.py:120`, `mag/swarm_local_drain.py`) and k8s drain; `route_novel` enqueues via `swarm_worker.enqueue_task` (`mag/swarm_surface.py:77-88`) and is idempotent by anchor (`mag/swarm_surface.py:72-74`), so rescans cannot spam the queue.

## 4. Counterfactual scan: the edge creates exactly the 7th loop (in memory, tree untouched)

Method: loaded `mag.organ_map.operational_graph()` live, appended the proposed edge to the edge list in memory only, re-ran `mag.dirac_loop` `rank`/`fundamental_cycles`/`scan` against the patched graph, then restored. No file was modified.

```
BASELINE n_loops = 6
WITH-EDGE rank: n_vertices=33 n_edges=22 components=20 betti1=9
WITH-EDGE n_loops = 7
NEW LOOP edge = organ:dirac_loop->organ:swarm_surface
NEW LOOP path = organ:dirac_loop -> organ:self_audit -> organ:swarm_worker -> organ:swarm_surface
NEW LOOP labels = ['Dirac loop', 'self audit', 'swarm worker', 'swarm surface']
NEW LOOP invariant = fb7c4aa189df629afa82b89986110f99c51b46a6eeac473eb04fa82065fdbcfa
novel (not in banked ledger / lattice) = True
scan: betti1=9 n_loops=7 closed_solved=6 open_gaps=1
```

The 7th loop is the gap-fill feedback circuit: dirac_loop detects an open gap, routes it through swarm_surface into the worker queue, the worker's health_probe feeds self_audit, and self_audit's audit_map feeds dirac_loop. The loop that fills loops. Its invariant is novel (a genuine open gap under the estate's own semantics: "open = novel invariant = a gap the swarm should fill", scan note at `mag/dirac_loop.py:311-312`). Because `dirac_loop -> swarm_surface` is a fresh vertex pair (no antiparallel twin), it enumerates cleanly under the current frozenset-keyed enumerator and is immune to Finding 1's dark-mode collapse (`flash50/deep-dirac-theory.md:55-64`): the 7th loop is nameable and bankable on day one.

## 5. What landing looks like (proposal; not executed here)

1. Spec first (this document is the spec): add `("dirac_loop", "swarm_surface", "route_open_gap")` to the transitions tuple at `mag/organ_map.py:650-672`. Expected graph delta, per the counterfactual: betti1 8->9, n_loops 6->7, open_gaps 0->1. Per the estate's own law (`mag/dirac_loop.py:199-202`), the new edge CLOSES nothing; it creates one new generator.
2. Wire the dispatch: when `scan()` finds an open loop, call `swarm_surface.route_novel(goal=<loop edge + labels + invariant>, surface="dirac_loop", lens="research")`; anchor dedupe makes rescan-idempotence free (`mag/swarm_surface.py:41-43,72-74`).
3. Fill and close: when the swarm work lands, the proving receipt runs `.venv/Scripts/python.exe -m mag.dirac_loop bank --edge "organ:dirac_loop->organ:swarm_surface" --receipt "<receipt>"`, writing invariant `fb7c4aa189df629afa82b89986110f99c51b46a6eeac473eb04fa82065fdbcfa` as the 7th ledger row.

Not landed in this item: the one-line transitions edit and the route_novel wiring change organ_map/dirac behavior consumed by dogfood_audit, context_pack, and the census surfaces; sibling lanes hold active claims on those files. Landing is an operator call; this item banks the proposal and the proof.

## 6. Checks run during this ask (exact commands and outputs)

1. `.venv/Scripts/python.exe -m mag.dirac_loop scan` -> ok=true, ts 2026-09-28T20:39:59Z, betti1=8, n_loops=6, closed_solved=6, open_gaps=0 (full JSON in session; six closed loop edges listed in section 1's ledger reference).
2. Counterfactual (inline python, in-memory edge append, patched `mag.organ_map.operational_graph`, restored after): output quoted verbatim in section 4. baseline n_loops=6; with-edge rank 33v/22e/20c/betti1=9; n_loops=7; new loop edge/path/labels as shown; invariant fb7c4aa189df629afa82b89986110f99c51b46a6eeac473eb04fa82065fdbcfa; novel=True (not in `_known_invariants()`); scan open_gaps=1.
3. `grep -n "route_novel" mag/swarm_surface.py mag/autonomous_research.py mag/swarm_worker.py tools/*.py` -> definition `mag/swarm_surface.py:63`; call sites `mag/autonomous_research.py:166,214,282,484,551`; no dirac_loop caller.
4. `grep -rn "dirac_loop" mag/*.py tools/*.py main.py` (excluding the module itself) -> consumers are `mag/context_pack.py:19-31,931,1057` (count into pack), `mag/dogfood_audit.py:137-144` (probe), `mag/ghost_server.py:38` (quests/open via dirac_loop.scan), `mag/organ_map.py:171` (registry). None routes to the swarm.
5. Ledger liveness: inline python over `memory/swarm_surface/sent.jsonl` -> 2,191 rows, 100+ distinct surfaces, last ts 2026-09-27T06:24:05Z; no surface named dirac_loop.
6. `grep -n "operator_mode|policy_engine|switchboard_v2" mag/effect_broker.py` -> policy_engine consulted at `mag/effect_broker.py:213-218` (rival edge, rejected as cross-component, section 2).
7. `grep -n "blackboard|swarm_tools" mag/swarm_worker.py` -> read-only sense at `mag/swarm_worker.py:254-262` (rival edge, rejected: sensing not dispatch, and cross-check of components shows blackboard is in-component but the worker->blackboard direction duplicates existing review circuitry without carrying the gap-fill contract).
8. Read: `mag/dirac_loop.py` (full, 348 lines), `mag/organ_map.py` (full, 701 lines), `mag/swarm_surface.py:1-130`, `mag/ghost_server.py:25-60`, `mag/context_pack.py:15-40`, `watch/inbox/burn_reset_20260927/dirac_loop6.md`, `dirac_loops45.md` (structure), `flash50/deep-dirac-theory.md` (full).

## 7. Not run / not claimed

- The edge is NOT in `mag/organ_map.py`; the with-edge numbers are an in-memory counterfactual, not a landed state. No test suite was run (no code changed). No bank() row was written (bank requires an enumerated loop plus a proving receipt; the receipt can only exist after the wiring lands).
- pytest, organ_map snapshot, and any eigen/spectral run were not part of this ask and were not executed.
