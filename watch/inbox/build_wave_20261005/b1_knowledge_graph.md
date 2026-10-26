# B1 receipt: knowledge_graph four verified builder defects fixed (build-it-all wave, 2026-10-05)

Ask: fix the four verified defects in `mag/knowledge_graph.py` from the day-4 mine steal card
(`watch/inbox/frontier_olm_2026-10-04/steal/agent-memory-and-continuity via x.md`, estate map,
all line numbers verified there and in `watch/inbox/frontier_olm_2026-10-04/lens/graph.md`),
each with a cause+evidence comment citing the card, then regenerate and bank before/after
counts. Law: repo venv interpreter only, no em/en-dashes in anything written, no git commit,
blocked items filed never faked.

## The four fixes (all landed in mag/knowledge_graph.py, each comment cites the card)

1. Knot reader (was :102-104): rows of `memory/biography/verkle_chain.jsonl` (11,299 rows live)
   never carry `theme`/`summary`; they carry `dominant_theme`/`session_id`/`tension_index`/
   `filename`/`leaf_hash`. Label now backfills from `dominant_theme`, summary from
   session/tension/amended/filename. Proof: knot stubs (label "knot" + empty summary)
   400 -> 0; all 400 knots carry real labels; 400 distinct knot ids.
2. case_law id builder (was :123): `law:{str(r.get('id') or '')[:12]}` collapsed 300 rows
   onto the empty id `law:` because neither ledger schema carries `id`. Per the card's
   headline probe, ids now key on sha256(skill_id + job + ts) for skill_fired.v1 rows and
   sha256(schema + ts + goal) for skill_ledger.decision.v1 rows. Proof: distinct case_law
   ids 1 -> 300 (probe assertion (a)). Zero key collisions.
3. has_invariant dangling edges (was :164-165): 794+ edges pointed at `invariant:` targets
   that were never materialized as nodes, under a [:4] per-module cap. New
   `_nodes_invariants()` materializes one node per distinct normalized invariant text
   (804 nodes), wired into `build()` and the regenerated collector kinds; the [:4] cap is
   dropped so the edge fan carries every invariant the module node carries (805 -> 812
   edges). Same normalized text = one shared node, so the old degree-9 `invariant:law `
   collision becomes real connectivity.
4. maps_to builder (was :171-173): never fired because no node carried a non-empty
   `maps_to` (the loader read `maps_to`/`skill` fields neither ledger schema carries).
   case_law nodes now carry maps_to = the mag module that writes each schema
   (skill_fired.v1 receipts: mag/skills_pack.py:99-106; decision.v1:
   mag/skill_ledger.py:137), the only byte-backed module reference in the rows. Proof:
   maps_to edges 0 -> 300, all binding to 2 real module nodes (module:skills_pack.py,
   module:skill_ledger.py).

## Headline probe (card, falsifiable): PASS both assertions

- (a) 300 distinct case_law ids exist where before all 300 shared `law:`.
- (b) id-keyed lookup: recomputing the key for the ledger's last skill_fired.v1 row
  (ponytail-ladder, ts 2026-10-05T07:12:56Z) resolves graph node `law:02ee3cd8a9c2`
  whose summary is that exact event's content: "skill_fired ponytail-ladder job=default
  pack=excerpt chars_injected=180".

## Before/after graph counts (regenerated via build(); byte evidence in
_b1_before.json / _b1_after.json beside this receipt)

| metric | before (2026-10-05T07:12:34Z) | after (2026-10-05T07:14:52Z) |
|---|---|---|
| nodes | 2,115 | 2,919 (+804 invariant nodes) |
| edges | 836 | 1,143 |
| orphans (degree-0) | 1,506 | 1,204 |
| dangling edges | 834 | 29 |
| distinct case_law ids | 1 | 300 |
| knot stubs | 400 | 0 |
| maps_to edges | 0 | 300 (both targets real) |

Orphan drop: -302 (all 300 case_law + 2 modules now bound). Rebuild is idempotent
(2919/1143 twice); `known()` and `python -m mag.knowledge_graph status` verified live.

## Gates (the no-slop contract)

- pytest on the knowledge_graph test file found by `git grep -l knowledge_graph tests/`
  (tests/test_graph_heal.py, the only hit): 10 passed in 0.68s.
- `.venv/Scripts/python.exe tools/violation_ratchet.py check --changed`:
  scope=18 changed files; hits=12; registered=12; NEW=0; PASS (exit 0), zero new debt.

## Filed, not faked (out of the four-defect scope, untouched)

- 29 remaining dangling edges are the pre-existing already_inside defect (prose we_have
  entries never matching real module ids; lens/graph.md item 2) - not one of the four.
- Remaining orphan classes (447 module, 400 knot, 140 steal, 217 doctrine) need edge
  builders that link filed knowledge to code (lens section 4 (b)/(c)) - not one of the four.
- The graph file rebuilt clean: no graph_heal why_context edges existed on disk before or
  after (edge mix before rebuild was 794+31), so no heal history was clobbered.

## Files

- mag/knowledge_graph.py (88 insertions, 12 deletions, LF endings preserved)
- memory/knowledge_graph.json (regenerated)
- watch/inbox/build_wave_20261005/{b1_knowledge_graph.md,_b1_before.json,_b1_after.json}
