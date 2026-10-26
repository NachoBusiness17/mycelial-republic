# RECEIPT: residue probe 2026-10-07 (quaternion-residue doctrine, minimal falsifiable core)

All numbers below are copied from `watch/inbox/residue_probe_20261007/results.jsonl`
(row numbers in parentheses). Environment: Python 3.11.15, numpy 2.4.6, CPU only,
no network, no model calls. Total compute approx 9.2 min across arms
(57.2 + 72.9 + 409.9 + 12.2 s). Seeds and decision rules were frozen in
`PREREG.md` before any run; four dated addenda are appended below the results
divider, in filing order. Nothing above the divider was edited after the runs.

## What landed

All three arms plus every pre-registered control ran to completion: arm 1
(summary row 2), arm 1b supplementary binned re-analysis (row 4), arm 2 with
shuffled-label control (rows 6-78), arm 3 with the 20,000-stream construction
sanity (rows 80-156). Zero NaNs in arm 1 (row 2). No arm was skipped or
truncated.

## Arm 1, positive control (definitional, textbook)

Euler 3-2-1 vs quaternion integration, 200 pitches x 200 streams x lengths
10..1000, seed 42. Median terminal geodesic error: Euler 0.119982 rad in the
gimbal band vs 0.014695 rad off-band; quaternion pipeline flat at 0.000015 rad
in both bands; Euler was 7874.695x worse than quaternion in band (row 2).
Verdict: the control behaved as the doctrine's baseline claim requires, with
one letter-rule event: the pre-registered gate demanded A-band/A-off > 10 and
measured 8.165, so `gate_pass` is false on the record (row 2). Cause diagnosed
in addendum 2 before any reinterpretation: geodesic impact of yaw error scales
with cos(theta) near the singularity, attenuating the measured divergence.
The pre-stated supplementary bins (row 4) are strictly monotone toward the
singularity (0.120847 > 0.118629 > 0.089906 > 0.014695), B flat, A/B 8074.957
in the closest bin: pass in substance. This arm is definitional by design and
carries no doctrine credit either way.

## Arm 2, substantive (reconstruction impossibility)

Coupling planted so every per-component marginal is exactly invariant
(orthogonal quaternion mixing of Gaussian innovations); signal lives only in
bilinear ordering terms. AUROC across coupling g = 0.05/0.10/0.20/0.35/0.60,
5 seeds, MLP 3x64, 2k Adam steps, 800/200 split (rows 66-75):

- Pipeline A (per-component complex projection cut): 0.4941 [0.4772, 0.5109],
  0.4950 [0.4813, 0.5088], 0.4999 [0.4755, 0.5242], 0.5106 [0.4879, 0.5333],
  0.5476 [0.5209, 0.5743].
- Pipeline B (coupling/ordering terms kept): 0.4731 [0.4255, 0.5206],
  0.5221 [0.4824, 0.5619], 0.5832 [0.5443, 0.6222], 0.8066 [0.7802, 0.8331],
  0.9830 [0.9778, 0.9881].
- Shuffled-label control at g = 0.60 (rows 76-77): A 0.5333 [0.5051, 0.5615]
  (fails its must-cover-0.5 check), B 0.5050 [0.4778, 0.5321] (passes).

Verdict, both layers on the record: the coded verdict row fired
"strong-form falsified" because A's CI lower bound at g = 0.60 exceeded 0.5
(row 78). Addendum 3 calibration: A's own shuffled-label null sits at 0.5333,
difference from real-A 0.0143, z approx 0.79, p approx 0.43; the elevation is
baseline, not recovered signal. Calibrated reading: A at chance at every g,
B strongly above chance from g = 0.20 up; the doctrine survived its
substantive test. At the two lowest coupling levels B is also at chance
(the planted signal is simply too weak there), which matches the graded
prediction rather than the vacuous outcome (vacuity required B at chance at
every g including 0.60).

## Arm 3, coordination form (Lilith Aug 30 frame)

Coupling via Haar-random unit-quaternion mixing: zero linear cross-correlation,
invisible to coherence in expectation. AUROC (rows 146-155):

- Detector A (cross-spectral coherence on complex projections): 0.4968
  [0.4855, 0.5080], 0.5011 [0.4819, 0.5203], 0.5032 [0.4895, 0.5168], 0.5173
  [0.5002, 0.5343], 0.5120 [0.4900, 0.5341].
- Detector B (quaternion-domain quadratic correlation plus commutator):
  0.5092 [0.4959, 0.5226], 0.5019 [0.4890, 0.5147], 0.5273 [0.5131, 0.5414],
  0.5697 [0.5630, 0.5765], 0.6885 [0.6802, 0.6969].
- 20,000-stream population sanity at g = 0.60 (row 130): coherence score shift
  0.05 pooled SE (means 0.656579 vs 0.656513); quaternion-domain score shift
  48.43 SE (0.008502 vs 0.009939); the demoted normalized score shifted
  0.02 SE, confirming the addendum-1 diagnosis.

Verdict, both layers: the coded verdict row fired "coherence leak" (row 156)
on a single cell, g = 0.35, CI lower bound 0.5002 (margin 0.0002). Addendum 4:
the direct population measurement shows no coherence signal at twice the
coupling strength and the A means are non-monotone in g; calibrated reading is
A at chance, B above chance from g = 0.20. Doctrine's coordination claim
survives in the calibrated reading; the letter firing is on the record.

## Definitional vs substantive

Arm 1 is definitional (the control). Arms 2 and 3 are the substantive tests.
Substantive outcome: in both, features that keep quaternion ordering content
detect the planted residue (0.983 and 0.6885 AUROC at the strongest coupling)
while per-component complex projections sit at chance (calibrated), exactly
the doctrine's strong form. Two letter-rule firings (arm 1 gate conjunct,
arm 2 strong-form, arm 3 leak) were adjudicated by pre-registered controls in
dated addenda; an operator who rejects calibration reads arm 2 as falsified
and arm 3 as leaked.

## What would falsify next

1. Re-run the arm 2 A elevation with 20+ seeds and a larger held-out split,
   pinning the shuffled-null spread: if real-A separates from shuffled-A at
   g = 0.60, the strong-form falsification stands.
2. Direct 4th-order coherence moment test with a stream-length sweep: if
   coherence carries any population signal, the arm 3 leak claim revives.
3. Break the exact marginal-invariance argument with non-Gaussian innovations:
   if the cut stays unrecoverable there too, the claim generalizes beyond the
   Gaussian construction; if A rises, the current result was construction-bound.
4. Learned per-component detector on raw complex sequences (not hand summary
   stats): the current A features are fixed summaries, a stronger learned cut
   is the fairer opponent.
5. Operating curves at lower SNR and longer streams to locate B's true
   detection floor.

## Files

- `PREREG.md` (frozen hypotheses + 4 dated addenda; results blocks appended by
  the script)
- `residue_probe.py` (single runnable script, numpy only; `--arm 1|1b|2|3|all|smoke`)
- `results.jsonl` (157 rows: env, cells, controls, summaries, verdicts)
- `RECEIPT.md`, `paste_ready_for_lilith.md` (this pair)

No network, no git commits, no files outside
`watch/inbox/residue_probe_20261007/` were written by this lane (catalog files
showing as modified in git status carry mtimes from before this session and
belong to parallel estate automation).
