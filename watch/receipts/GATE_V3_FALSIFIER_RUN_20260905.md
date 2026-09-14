# GATE V3 FALSIFIER — RUN RECEIPT (2026-09-05)

The cave wall, cleared. Plato/Kirk flagged it in the panel fold ("built-but-unrun treated
as pending — an unrun falsifier is a shadow of knowledge"); the restful-watch doctrine
says fix when seen. Ran in-session, $0, no spawns.

## VERDICT: WEAK — gather more data (premise survives, unproven)

| Metric | Value | Read |
|---|---|---|
| Labeled rows | 9,176,340 (ractor_board runaway-evidence archive) | big data, tiny signal class |
| Label balance | 146 DONE vs 9,176,194 THIN (0.0016% positive) | extreme imbalance — treat AUC with suspicion |
| Holdout AUC | 0.848 | well above chance |
| 3-fold CV AUC | 0.806 ± 0.187 | variance huge (imbalance again) |
| Shuffled-label floor | 0.548 (mean of 5) | the honest floor |
| **Signal over floor** | **+0.258** | real but not decisive |

## EMERGING BANDS (logistic coefficients, positive pushes DONE)
- `forge` +14.6, `milestone` +10.9, `has_evidence` +5.1 — lanes/rows that carry evidence
  and hit milestones DO finish.
- `task.receipt` −5.9 (receipt-tagged rows skew THIN — receipts written before done),
  `cage` −5.8, `engine-b1` −4.7 — the known vapor organs show up in the weights.

## TRI-STATE
- SUPPORTED: plain categorical metadata carries discriminative signal (+0.258 over floor).
- UNPROVEN: the spectral premise at gate-v3 strength — 146 positives cannot carry a
  benchmark-gate decision. Gather more labeled DONE/THIN pairs before any build.
- DISPUTED: "the fleet's own metadata has no predictive structure" — dead. The weights
  literally rank the vapor organs (cage/engine-b1 negative) against the evidence-carriers
  (forge/milestone/evidence positive).

## WHAT IT FEEDS
- Gate v3 build: stays GATED on data volume (the cheap kill worked as designed — no
  embeddings, no shaders, $0).
- Emissions-vs-effect fold (C3): the model independently rediscovered the vapor organs —
  a second instrument agreeing with Baudrillard's hand audit.
- Next lawful step: relabel pass on newer boards + let night shift append labeled rows.

## RELABEL PASS (same day, second run — the falsifier's own "gather more data" step)
Combined archive + live board: **12,135,824 rows, 230 DONE** (+84 positives, +57% class).
Balanced-class logistic, holdout: **AUC 0.629**, shuffled floor 0.500 → **+0.129 over floor**.
Top bands replicate: `task.receipt` −5.1 (vapor, again), `milestone` +4.9, evidence +0.95.

**Honest read:** the first run's 0.848 was imbalance-inflated; with balanced weighting and
twice the positives the true signal is ~+0.13 — real, replicable, and directionally
identical (vapor rows predict THIN, evidence/milestone rows predict DONE). The verdict
firms to: **premise SUPPORTED as weak signal; gate v3 build remains gated until the
positive class grows ~10x.** The emissions-vs-effect finding has now replicated across
two runs and two methods. Second instrument confirmed; third run should ride night-shift
labels as boards grow.
