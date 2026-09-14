# PERTURBATION BATTERY — the unified fold's Perturbation Test, fired (2026-09-06)

**Organ:** `mag/perturbation_battery.py` (one CLI, $0, no network, no daemons) ·
**JSON receipt:** `state/perturbation_battery.json` · **Salon license:**
`memory/runs/salons/unified_fold_20260906/SALON_ARTIFACT.md` (deepseek-pro's test:
cross-domain invalidation symmetry — corrupt one surface, another must measurably fail;
no propagation = the map is decoration). Vision-pass context:
`watch/inbox/VISION_PASS_SWEEP1_20260906.md`.

**Rules held:** ALL corruption on copies in `state/_perturb_tmp/` (cleaned after run);
live ledgers byte-identical before/after (tm tip 15f4290fad22, gw tip 1129e3557bce).
Each case logged `{case, corrupt, detector, caught}`.

## VERDICT: 3/5 caught — and that is EXACTLY the salon's predicted shape

Instruments **3/3 UP** · Expected-failures **2/2 CONFIRMED**.

| case | corrupt | detector | caught |
|---|---|---|---|
| P1_ledger | hash-valid rows with evidence-dead paths, appended to COPIES of both ledgers | grounding_wave v2 evidence audit + tesuji_map verify | **CAUGHT** — both twins: `EVIDENCE-MISSING` (gw row 25, tm row 156) |
| P2_voxels | 26 rows of `slab_1.csv` numbers shifted on the copy | regenerate fnv1a32 from data vs stored manifest hash (faithful `_build_shadow_walk.py` port) | **CAUGHT** — `ae26ba47` → `5c0265e2`; control: pristine data reproduces stored hash (detector not trivial) |
| P3_maze_residual | the OLD bogus flood (uniform diamond gradient ignoring walls — the maze's birth defect) vs CORRECT BFS, on the ported `_maze_sim_test.js` SDF (240x135) | physics-lab Bellman-residual: \|∇T\|=1 on reachable cells + reachability-leak | **CAUGHT** — bogus FAILS (10,971 leaked finite-T cells on unreachable cells); correct BFS PASSES (0 leaks, 0 violations, max residual 0.0) |
| P4_premise_poison | true-sounding claim citing a REAL file that does not support it (salon-artifact copy under a plausible measurement filename) | `mag.cite_gate` existence check | **MISSED — as predicted** (see FINDING 1) |
| P5_cross_domain | one maze wall removed from the SDF → BFS field hash moved `60817c97…` → `46d0f075…` | does any organ auto-invalidate cells bound to the old field hash? | **MISSED — as predicted** (see FINDING 2) |

## FINDING 1 (P4) — LAW-064 OBSERVATION-GATE gap, receipt in hand

cite_gate stamped the poisoned citation `LOCAL-VERIFIED`, `cite_rate 1.0`,
`complete=true`. The gate verifies the cited bytes **EXIST**, never whether they
**SUPPORT** the claim. Sound inference on a poisoned premise ships straight through
gate+salon+chain — the Royal Society rule gates publication and replication, not
observation (salon C4, deepseek-pro). This is a FINDING, not a bug: cite_gate does
exactly what it was built to do, and that is not enough.

**What LAW-064 must add** (observation gate, on top of existence):
1. **Premise-byte check** — a load-bearing claim must hash-cite the specific
   evidence span (file + line/byte range or sha of the quoted section), not just a
   path; the gate re-reads the span and string-matches the load-bearing figure/claim.
2. **Subject-match stub** — even $0-deterministic: claim keywords must appear in the
   cited span (would have flagged this probe: "slab 7 / 5,430" appears nowhere in a
   salon-chairs file).
3. **Witness independence = SUBSTRATE diversity** — blind witnesses that are copies
   of the same trained prior are one observation; local quant vs hosted vs foreign
   archive (the A6/Marathon instinct).

## FINDING 2 (P5) — cross-domain propagation ABSENT (C1 fuel, honest DISPUTED)

The field is sensitive — remove one wall and the BFS field hash moves. But no organ
carries a game-field content hash, so nothing downstream CAN invalidate: a ledger
cell that explicitly binds the old hash in its `resp_hash`/note stays verify-PASS
(156 cells, chain intact) after the world changed. The chain hashes the **ROW**,
never the **WORLD**. Dirty-radius re-probing exists as tesuji probe-policy prose,
not as a mechanism wired to surface content. Per the salon: no propagation = the
map (the unified-fold grammar's invalidation symmetry) is **not yet demonstrated**
across domains — C1 stays DISPUTED-with-a-path, and the transfer test (grok-cli's
half) still has to run by Sep 20.

**What would close it:** post surface-content hashes as first-class row fields
(`surface_hashes: {maze_field: …, manifest_data_hash: …}`) + a verify-time
re-derivation step that recomputes current surface hashes and flags stale bindings
as STALE-SURFACE (verdict-preserving, chain-append corrections only).

## P3 — the instrument that would have caught the birth defect on day one

Notable subtlety, now on record: the diamond gradient satisfies \|∇T\|=1 **locally**
everywhere reachable — the pure eikonal residual is BLIND to it. The catcher is the
reachability-leak term (finite T where BFS proves unreachable: 10,971 cells). Any
future flood/walk field check must ship BOTH terms; a residual-only check would
have passed the bogus maze.

## Battery falsifiers (standing)
- Re-run: `python -m mag.perturbation_battery` → expect instruments 3/3,
  expected-failures 2/2, JSON diff-clean except ts.
- If P1/P2/P3 ever report MISSED: an organ regressed — stop and fix before any
  further grounding posts.
- If P4 ever reports CAUGHT: LAW-064 landed — update this card and the salon
  scorecard.
