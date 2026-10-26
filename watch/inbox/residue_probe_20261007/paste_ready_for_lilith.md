# Paste-ready reply for Lilith (plain register, numbers from results.jsonl)

Pre-registered probe, numpy only, seeds fixed, no model calls.

1. Control (Euler vs quaternion near gimbal lock): Euler median error 0.120
rad in the gimbal band vs 0.0147 away; quaternion pipeline flat at 0.000015
rad (Euler 7875x worse in band). Control behaved.

2. Substantive (planted ordering-only coupling between two quaternion
streams): after the per-component complex cut, an MLP scored AUROC 0.49,
0.50, 0.50, 0.51, 0.55 across five coupling strengths, indistinguishable from
its own shuffled-label null (0.533 at strongest coupling). Keeping the
coupling terms, the same learner scored 0.47, 0.52, 0.58, 0.81, 0.98. What
the cut deletes is recoverable; what it keeps is not.

3. Coordination (two residually coupled streams): cross-spectral coherence on
complex projections read 0.50 to 0.52, population shift 0.05 SE on 20,000
streams. Joint quaternion-domain correlation read 0.69 at strongest coupling
(48 SE shift).

Bottom line: the residue survived its substantive test in the calibrated
reading. Two letter-rule firings are on the record; if you distrust the
calibration, read arm 2 as falsified. Honest either way: the ordering terms
carry the signal; the projections do not.
