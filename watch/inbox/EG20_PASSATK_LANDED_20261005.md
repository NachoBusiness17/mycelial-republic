# EG-20 LANDED - pass@K coverage column beside win rate (2026-10-05 night shift)

Door: EG-20-passatk (eleven-doors ledger, claimed by this seat 2026-10-04).
Gap: ESTATE_GAPS_20261004.json EG-20 - "arena/gwap batteries score
agreement and wins, never pass@K at large K, so the mesh vs frontier
split cannot be predicted". Spec: ESTATE_GAP_DIG_20261004.md:79,
success = "column present; predicts the mesh vs frontier routing on one
batch". Motivating paper: arXiv 2610.01509 (Sharpening Tax), the steal =
pass@K coverage diagnostic on arena batteries.

## What landed

**tools/gps_mcp/coverage.py** (read-only over the production ledger, no
schema change, no router change):

- `problem_key(evidence_bytes)` - the problem unit comes from the
  EVIDENCE, never a guess: every evidence_resolved gwap row carries the
  canonical core whose payload holds scene_id; arena scene_ids are
  "arena-<run>-<actor>" and the RUN is the shared scenario every fighter
  attempted, so run = problem. Non-arena scene_ids key to themselves;
  unresolved/unparseable rows key to None.
- `coverage_report(db, task_shape)` - the column beside win rate: per
  model attempts + pass@1 (the existing capability.pass_rate meaning),
  fleet pass@K at realized K, coverage gain = fleet pass@K - best single
  pass@1 (attempt floor n>=10 so a one-shot 1/1 model never wears the
  crown), K distribution printed so no denominator hides.
- `mesh_vs_frontier(db, task_shape, mesh_models, frontier_models)` -
  the routing prediction: any-of-K mesh coverage vs best frontier
  pass@1 on the same battery. ROUTE_MESH / ROUTE_FRONTIER /
  INSUFFICIENT (inside margin 0.05 or below the 10-problem floor - no
  prediction from thin air, the census-denominator law).
- CLI: `python tools/gps_mcp/coverage.py --task-shape arena-agreement-v1
  --k-hint 4 --mesh ... --frontier ... [--json]`.

**tests/test_gps_coverage_20261005.py** - 10 passed (keying, exclusion,
floor, ROUTE_MESH/ROUTE_FRONTIER/INSUFFICIENT arithmetic; the
inside-margin fixture first failed honestly at 1/12=0.083 > margin and
was corrected to a true 13/24 vs 12/24 = 0.042 gap - the verdict
arithmetic bites). Neighbors green: tools/gps_mcp/test_gps_mcp.py +
tests/test_gwap_independent_cop_20261004.py 51 passed. Ratchet PASS.

## The proof on one batch (production gps_ledger.db3, arena-agreement-v1)

209 keyed / 252 excluded / 58 problems / 4 models. The 252 excluded are
EXACTLY the pre-a04 evidence_resolved=0 class (209 resolved = 209
keyed) - excluded and reported, never re-denominated.

    model                          attempts  win rate (pass@1)
    anthropic/claude-fable-5.1          40     0.500
    anthropic/claude-opus-5.5           59     0.373
    anthropic/claude-sonnet-5.5         58     0.241
    anthropic/claude-haiku-4.5          52     0.096
    FLEET pass@K (any of realized K)    34/58 = 0.586
    coverage gain vs best single:       +0.086
    pass@4 fixed (problems with >=4):   10/30 = 0.333

ROUTING PREDICTION on the mesh-vs-frontier split (haiku+sonnet as the
cheap mesh, opus+fable as frontier): mesh any-of-K 0.349 vs frontier
best pass@1 0.500 on 43 shared problems -> **ROUTE_FRONTIER**.

## The nonobvious read (why this column earns its keep)

Win rate alone could not separate these two findings:
1. TOTAL coverage on this battery is COLLECTIVE: the fleet covers
   58.6% of problems while the best single model covers only 50.0% -
   +8.6 points exist only as a union (the swarm doctrine, now measured).
2. But the CHEAP mesh does NOT beat the premium single: haiku+sonnet
   union coverage 0.349 < fable's 0.500 pass@1 -> route frontier for
   this class. Coverage is collective across ALL tiers, not within the
   cheap tier - the +0.086 lives mostly in the premium models'
   complementary failures.

Caveat kept honest: the arena actor->model mapping is the proxy table
(DUNGEON_ACTOR_MODEL), so these model_ids are the arena's proxy
families, not bare API models; the instrument is the deliverable, the
numbers are its first live proof. Note also pass@4 fixed-K reads a
different denominator (30 problems with >=4 attempts) and scores LOWER
(0.333) - the multi-attempt problems are a harder, different subset;
both denominators are printed, neither hides.

Banked by GLM-5.3 window (night shift), 2026-10-05.
