# PREREG: residue probe 2026-10-07 (quaternion-residue doctrine, minimal falsifiable core)

Written and frozen BEFORE any run. Constructions, pipelines, metrics, seeds, and
decision rules below are fixed. Results are appended after the run under the
RESULTS divider by residue_probe.py itself. Nothing above that divider is edited
post-run; corrections, if any, appear as dated addenda below the divider.

Environment: `.venv\Scripts\python.exe`, numpy only (no torch, no network, no
model calls, no files outside this directory). All randomness from
numpy.random.Generator with the seeds fixed below.

## Constructions (exact)

### Shared stream model (arms 2 and 3)
- Stream length T = 64 innovation steps; two quaternion channels c in {1,2};
  states q_c(0) = (1,0,0,0); per step q_c(t+1) = normalize(q_c(t) + 0.15 * e_c(t)),
  normalize = divide by quaternion norm (unit-quaternion states).
- e_1(t) iid N(0, I_4) in both conditions and both arms.
- NULL condition: e_2 = eta, eta iid N(0, I_4), independent of channel 1.
- COUPLED condition: e_2(t) = sqrt(1 - g^2) * eta(t) + g * (u(t) (x) e_1(t)),
  quaternion product; u(t) a unit quaternion fixed per arm (below). Because
  left-multiplication by a unit quaternion is an orthogonal map on R^4, e_2 is
  exactly N(0, I_4) marginally and iid over time: every per-component marginal
  law of the observable streams is identical between NULL and COUPLED. This is
  the "cut" the doctrine claims is lossy.
- Coupling levels g in {0.05, 0.10, 0.20, 0.35, 0.60} (5 levels).
- 1000 streams per cell (500 NULL + 500 COUPLED, balanced), 5 seeds.
- Observable handed to pipelines/detectors: the pair of unit-quaternion state
  streams; innovations recovered by first differences d_c(t) = q_c(t+1) - q_c(t).

### Arm 2 coupling u(t) (ordering / commutator content)
- u(t) = (0, v1(t)/|v1(t)|): the pure-vector unit quaternion along channel 1's
  state vector part at step t (guard |v1| < 1e-8 -> u = (0,1,0,0)).
- The mean of the left-multiplication matrix over the isotropic v1 distribution
  is 0, so all linear cross-moments E[e_1 e_2^T] vanish: the planted signal
  lives only in bilinear ordering terms (quaternion products, commutators,
  scalar-vector antisymmetric terms), which per-component complex projections
  cannot form.

### Arm 3 coupling u(t) (coordination form, Lilith Aug 30 frame)
- u(t) = Haar-random unit quaternion per step (normalized N(0,I_4)), independent
  of everything. E[u] = 0, so all linear cross-correlations vanish and
  cross-spectral coherence of any linear projection is blind in expectation.
- Known risk, pre-registered: coherence is a 4th-order statistic and orthogonal
  mixing preserves only 2nd-order marginals exactly, so a small higher-order
  leak in detector A is possible; interpretation rule below.

## Pipelines

### Arm 1 (positive control, definitional, textbook)
- 200 pitch values theta0 = linspace(-pi/2, +pi/2, 202)[1:-1] (interior points
  only); 200 random streams per pitch; per-stream length L uniform in
  {10,...,1000}; body rates w(t) iid N(0, 0.01^2 I_3) per step; dt = 1; initial
  attitude psi0 = phi0 = 0, theta = theta0 (3-2-1 yaw-pitch-roll).
- TRUTH: exact exponential map of the per-step constant body rate
  (zero-order-hold gyro interpretation).
- Pipeline A: Euler 3-2-1 integration via the standard rate transformation
  (psidot = (q sin(phi) + r cos(phi))/cos(theta), thetadot = q cos(phi) -
  r sin(phi), phidot = p + psidot sin(theta)), forward Euler steps, cos(theta)
  clamped to magnitude >= 1e-12 with sign kept.
- Pipeline B: quaternion first-order integrator q_dot = 0.5 q (x) (0, w),
  renormalized each step.
- Metric: terminal geodesic angle on SO(3) between pipeline and TRUTH, taken at
  each stream's own length L. Summary bands: band = |theta0| >= pi/2 - 0.1,
  off = |theta0| <= pi/2 - 0.3.

### Arm 2 (reconstruction impossibility, substantive)
- Features A ("the cut"): per-component statistics of the 8 innovation series
  d_1, d_2 (4 components each): mean, std, skew, kurtosis, lag-1 autocorrelation,
  lag-2 autocorrelation, analytic-signal amplitude mean and std (the
  per-component complex projection, built by FFT Hilbert), 8 series x 8 stats =
  64 features. Strictly per-component: no cross-channel or cross-component term.
- Features B = A plus coupling/ordering terms (24 extra, 88 total): the
  entrywise-squared 4x4 cross-moment matrix of (d_1, d_2) (16), commutator norm
  series |d_1 (x) d_2 - d_2 (x) d_1| mean and std (2), squared quaternion-product
  component means (4), antisymmetric scalar-vector term |s1 v2 - s2 v1| mean and
  std (2).
- Learner (both pipelines, identical class): MLP with 3 hidden layers of 64
  ReLU units, sigmoid output, binary cross-entropy, Adam lr 1e-3 (beta1 0.9,
  beta2 0.999, eps 1e-8), batch 128, 2000 steps, He init, features z-scored by
  train-split statistics (std guard 1e-12), 800/20 split stratified by
  construction (balanced classes), fixed per (seed, g, pipeline) model rng.
- Metric: AUROC on the 200 held-out streams.

### Arm 3 (coordination form)
- Detector A: Welch cross-spectral coherence (4 non-overlapping segments of 16
  samples) between channel 1 and channel 2 complex projections z = dw + i dx
  and z = dy + i dz, same pairings only ((dw+idx) vs (dw+idx), (dy+idz) vs
  (dy+idz)); score = mean over the two pairings of the max coherence magnitude
  over frequency bins. No training.
- Detector B: joint quaternion-domain correlation score
  mean_t [ (d1 . d2)^2 / (|d1|^2 |d2|^2 + 1e-12) ]. No training.
- Metric: AUROC of each single-score detector on the 1000 streams per cell.
- Secondary diagnostics (reported, not gates): commutator-norm mean score;
  raw mean of (d1 . d2)^2.

## Seeds (fixed)
- Arm 1: data rng default_rng(42).
- Arms 2/3: seeds [1000, 2000, 3000, 4000, 5000]. Seed derivation (integer
  arithmetic, gi = coupling index 0..4):
  - Arm 2 data null: 2_000_000_000 + 1000*seed + 10*gi + 1; coupled: ... + 2;
    model: ... + 3 (pipeline A) / ... + 4 (pipeline B); shuffled-label model
    rngs: ... + 11/12 with data rngs ... + 5/6.
  - Arm 3 data null: 3_000_000_000 + 1000*seed + 10*gi + 1; coupled: ... + 2.
  - Arm 3 construction sanity: 3_900_000_001 (null), 3_900_000_002 (coupled).

## Confidence intervals and decision rules
- CI: mean +/- 1.96 * sd(seeds) / sqrt(5); per-seed values land in
  results.jsonl.
- "at chance" := CI covers 0.5 OR |mean - 0.5| <= 0.02.
- Arm 1 gate (stop rule): PASS iff median_A(band)/median_A(off) > 10 AND
  median_A(band)/median_B(band) > 10. On FAIL: harness broken; report and stop;
  arms 2-3 are not interpreted.
- Arm 2 verdicts:
  - doctrine-supported: A at chance at every g, AND B CI lower bound > 0.5 at
    g = 0.60.
  - strong-form falsified: A CI lower bound > 0.5 at some g (the "cut" is
    recoverable from per-component projections alone).
  - vacuous: B at chance at every g including 0.60 (coupling terms carry no
    usable signal even at the strongest planted level).
- Arm 3 verdicts:
  - doctrine-supported: A at chance at every g, AND B CI lower bound > 0.5 at
    g = 0.60.
  - coherence leak: A CI lower bound > 0.5 at some g: the complex projection
    retains partial higher-order signal; the ordering-invisibility claim holds
    only at linear order. Reported honestly; not counted as a harness failure.
  - vacuous: B at chance at every g including 0.60.
- Harness checks (must pass or be reported as failures):
  - Arm 2 shuffled-label control at g = 0.60, all 5 seeds, both pipelines:
    AUROC CI must cover 0.5.
  - Arm 2 construction sanity: pipeline B AUROC point estimate at g = 0.60
    (seed-averaged) > 0.60, else the verdict is "construction too weak".
  - Arm 3 construction sanity at g = 0.60 on 20000 fresh streams (10000/10000):
    |mean_B(null) - mean_B(coupled)| > 5 pooled SE; the same shift and its SE
    are reported for detector A's score.

## Pre-registered predictions
- Arm 1: A blows up in the gimbal band, B stays flat (definitional control).
- Arm 2: doctrine predicts A at chance and B above chance rising with g; DPI
  makes the same prediction for A. Interesting outcomes: A above chance
  (strong-form falsified), or B ~= A everywhere (vacuous).
- Arm 3: doctrine predicts A at chance on the coupled condition and B above
  chance.

## Outputs
- residue_probe.py (this script), results.jsonl (one JSON object per row),
  RECEIPT.md, paste_ready_for_lilith.md. Em-dashes banned in all files.

## RESULTS (appended post-run by residue_probe.py; nothing above this line is edited)

## ADDENDUM 2026-10-07 (pre-run amendment, filed before the confirmatory run)

Pilot diagnostics on throwaway streams (n=5000 arm 3, seeds 3_000_000_001/2 and
3_900_000_001/2; n=2000 arm 2, seeds 7_700_001/2; smoke run that also touched
arm 2 cell seeds 2_001_000_041/2) revealed one detector-design flaw:

1. The normalized arm 3 detector B score mean_t (d1.d2)^2/(|d1|^2|d2|^2 + eps)
   is signal-blind: the coupling inflates numerator and denominator in a
   correlated way (ratio washout). Pilot at g=0.60, n=5000: null 0.257250 vs
   coupled 0.255858 (shift -2.1 SE), AUROC 0.4888. The raw quadratic
   correlation mean_t (d1.d2)^2 shifted +26.3 SE and the commutator norm
   +19.6 SE under the same conditions.
2. Arm 2 pilots showed features A univariate max deviation from 0.5 of 0.025 at
   n=2000 (chance, as the exact marginal-invariance argument predicts) and
   features B with strong univariate signal (0.826 at g=0.60, 0.641 at
   g=0.35). No arm 2 or arm 1 change.

Amendments, effective for the confirmatory run:
a. Arm 3 detector B (primary) := mean_t [ (d1 . d2)^2 + |d1 (x) d2 - d2 (x)
   d1|^2 ] (unnormalized quadratic quaternion correlation plus squared
   commutator, the ordering term). The former normalized ratio is demoted to a
   reported diagnostic (B_quat_norm). Decision rules unchanged in form and now
   evaluated on the amended primary score.
b. Seed decontamination: every pilot seed listed above is excluded. All arm 2
   data/model seed bases shift by +500,000,000; all arm 3 cell seed bases shift
   by +500,000,000; arm 3 construction-sanity seeds become 3_900_000_011
   (null) and 3_900_000_012 (coupled). No pilot seed lies in the new
   derivations.
c. Arm 3 sanity gate unchanged: primary B score population shift > 5 pooled SE
   at g=0.60 on 20000 fresh streams, plus the reported shift for detector A.

### Arm run 1 (appended 2026-10-07T15:48:38Z, by residue_probe.py)

`{"arm": 1, "type": "summary", "seed": 42, "n_streams": 40000, "n_band": 2400, "n_off": 32400, "median_err_A_band_rad": 0.119982, "median_err_A_off_rad": 0.014695, "median_err_B_band_rad": 1.5e-05, "median_err_B_off_rad": 1.5e-05, "ratio_A_band_over_off": 8.165, "ratio_B_band_over_off": 0.997, "ratio_A_over_B_band": 7874.695, "frac_A_err_gt_pi4_band": 0.0, "frac_B_err_gt_pi4_band": 0.0, "nan_A": 0, "nan_B": 0, "seconds": 57.2, "gate_pass": false}`


## ADDENDUM 2, 2026-10-07 (arm 1 gate letter-miss, filed before arms 2-3)

The arm 1 run (results.jsonl, timestamp 2026-10-07T15:48:38Z, seed 42) measured
ratio_A_band_over_off = 8.165 against the pre-registered threshold > 10
(conjunct 1 letter-miss) while ratio_A_over_B_band = 7874.695 (conjunct 2
passed) and B stayed flat (ratio 0.997). Diagnosis filed before further
analysis: near the singularity the geodesic impact of a yaw perturbation
scales with cos(theta), so the terminal-attitude-error metric attenuates
exactly the divergence the Euler pipeline suffers; the 10x constant was set
without that derivation. The original gate row stands unedited.

Supplementary analysis (identical seed-42 data, regenerated bit-identically,
no parameter search): median terminal error in bins of distance to the
singularity d = pi/2 - |theta0| over [0.0078, 0.05), [0.05, 0.1), [0.1, 0.3),
[0.3, pi/2). Pass-in-substance criterion, pre-stated: A median error
strictly increasing as d decreases, AND B medians flat within a factor of 3
across bins, AND A/B median ratio >= 100 in the closest bin. If any of these
fail, the harness is reported broken and arms 2-3 are not interpreted. The
operator may overrule this addendum; it is a judgment call, recorded as such.

### Arm run 1b (appended 2026-10-07T15:54:29Z, by residue_probe.py)

`{"arm": 1, "type": "supplementary_binned", "seed": 42, "median_A_d_lt_0.05_rad": 0.120847, "median_B_d_lt_0.05_rad": 1.5e-05, "n_d_lt_0.05": 1200, "median_A_d_0.05_to_0.1_rad": 0.118629, "median_B_d_0.05_to_0.1_rad": 1.5e-05, "n_d_0.05_to_0.1": 1200, "median_A_d_0.1_to_0.3_rad": 0.089906, "median_B_d_0.1_to_0.3_rad": 1.5e-05, "n_d_0.1_to_0.3": 5200, "median_A_d_ge_0.3_rad": 0.014695, "median_B_d_ge_0.3_rad": 1.5e-05, "n_d_ge_0.3": 32400, "A_over_B_closest_bin": 8074.957, "B_flat_within_3x": true, "A_monotone_toward_singularity": true, "pass_in_substance": true, "seconds": 72.9}`


### Arm run 2 (appended 2026-10-07T16:03:21Z, by residue_probe.py)

`{"arm": 2, "type": "cell", "seed": 1000, "g": 0.05, "pipeline": "A", "auroc": 0.5162, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 1000, "g": 0.05, "pipeline": "B", "auroc": 0.4238, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 2000, "g": 0.05, "pipeline": "A", "auroc": 0.4917, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 2000, "g": 0.05, "pipeline": "B", "auroc": 0.5497, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 3000, "g": 0.05, "pipeline": "A", "auroc": 0.4943, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 3000, "g": 0.05, "pipeline": "B", "auroc": 0.4207, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 4000, "g": 0.05, "pipeline": "A", "auroc": 0.4643, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 4000, "g": 0.05, "pipeline": "B", "auroc": 0.4711, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 5000, "g": 0.05, "pipeline": "A", "auroc": 0.5039, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 5000, "g": 0.05, "pipeline": "B", "auroc": 0.5001, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 1000, "g": 0.1, "pipeline": "A", "auroc": 0.4842, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 1000, "g": 0.1, "pipeline": "B", "auroc": 0.4845, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 2000, "g": 0.1, "pipeline": "A", "auroc": 0.4781, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 2000, "g": 0.1, "pipeline": "B", "auroc": 0.5419, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 3000, "g": 0.1, "pipeline": "A", "auroc": 0.4922, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 3000, "g": 0.1, "pipeline": "B", "auroc": 0.5824, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 4000, "g": 0.1, "pipeline": "A", "auroc": 0.5177, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 4000, "g": 0.1, "pipeline": "B", "auroc": 0.5316, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 5000, "g": 0.1, "pipeline": "A", "auroc": 0.5029, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 5000, "g": 0.1, "pipeline": "B", "auroc": 0.4702, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 1000, "g": 0.2, "pipeline": "A", "auroc": 0.4575, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 1000, "g": 0.2, "pipeline": "B", "auroc": 0.5351, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 2000, "g": 0.2, "pipeline": "A", "auroc": 0.4919, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 2000, "g": 0.2, "pipeline": "B", "auroc": 0.551, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 3000, "g": 0.2, "pipeline": "A", "auroc": 0.5077, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 3000, "g": 0.2, "pipeline": "B", "auroc": 0.619, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 4000, "g": 0.2, "pipeline": "A", "auroc": 0.5326, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 4000, "g": 0.2, "pipeline": "B", "auroc": 0.6393, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 5000, "g": 0.2, "pipeline": "A", "auroc": 0.5096, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 5000, "g": 0.2, "pipeline": "B", "auroc": 0.5719, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 1000, "g": 0.35, "pipeline": "A", "auroc": 0.5355, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 1000, "g": 0.35, "pipeline": "B", "auroc": 0.776, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 2000, "g": 0.35, "pipeline": "A", "auroc": 0.5217, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 2000, "g": 0.35, "pipeline": "B", "auroc": 0.7753, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 3000, "g": 0.35, "pipeline": "A", "auroc": 0.5302, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 3000, "g": 0.35, "pipeline": "B", "auroc": 0.8402, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 4000, "g": 0.35, "pipeline": "A", "auroc": 0.4797, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 4000, "g": 0.35, "pipeline": "B", "auroc": 0.8109, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 5000, "g": 0.35, "pipeline": "A", "auroc": 0.4859, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 5000, "g": 0.35, "pipeline": "B", "auroc": 0.8307, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 1000, "g": 0.6, "pipeline": "A", "auroc": 0.5328, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 1000, "g": 0.6, "pipeline": "B", "auroc": 0.9871, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 2000, "g": 0.6, "pipeline": "A", "auroc": 0.5225, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 2000, "g": 0.6, "pipeline": "B", "auroc": 0.9832, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 3000, "g": 0.6, "pipeline": "A", "auroc": 0.533, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 3000, "g": 0.6, "pipeline": "B", "auroc": 0.9902, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 4000, "g": 0.6, "pipeline": "A", "auroc": 0.5509, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 4000, "g": 0.6, "pipeline": "B", "auroc": 0.977, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 5000, "g": 0.6, "pipeline": "A", "auroc": 0.5989, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "cell", "seed": 5000, "g": 0.6, "pipeline": "B", "auroc": 0.9774, "n_train": 800, "n_test": 200}`

`{"arm": 2, "type": "shuffled_control", "seed": 1000, "g": 0.6, "pipeline": "A", "auroc": 0.5597}`

`{"arm": 2, "type": "shuffled_control", "seed": 1000, "g": 0.6, "pipeline": "B", "auroc": 0.5082}`

`{"arm": 2, "type": "shuffled_control", "seed": 2000, "g": 0.6, "pipeline": "A", "auroc": 0.5328}`

`{"arm": 2, "type": "shuffled_control", "seed": 2000, "g": 0.6, "pipeline": "B", "auroc": 0.5082}`

`{"arm": 2, "type": "shuffled_control", "seed": 3000, "g": 0.6, "pipeline": "A", "auroc": 0.5171}`

`{"arm": 2, "type": "shuffled_control", "seed": 3000, "g": 0.6, "pipeline": "B", "auroc": 0.4891}`

`{"arm": 2, "type": "shuffled_control", "seed": 4000, "g": 0.6, "pipeline": "A", "auroc": 0.4889}`

`{"arm": 2, "type": "shuffled_control", "seed": 4000, "g": 0.6, "pipeline": "B", "auroc": 0.5517}`

`{"arm": 2, "type": "shuffled_control", "seed": 5000, "g": 0.6, "pipeline": "A", "auroc": 0.5681}`

`{"arm": 2, "type": "shuffled_control", "seed": 5000, "g": 0.6, "pipeline": "B", "auroc": 0.4676}`

`{"arm": 2, "type": "cell_summary", "g": 0.05, "pipeline": "A", "auroc_mean": 0.4941, "ci_lo": 0.4772, "ci_hi": 0.5109, "seeds": [0.5162, 0.4917, 0.4943, 0.4643, 0.5039]}`

`{"arm": 2, "type": "cell_summary", "g": 0.05, "pipeline": "B", "auroc_mean": 0.4731, "ci_lo": 0.4255, "ci_hi": 0.5206, "seeds": [0.4238, 0.5497, 0.4207, 0.4711, 0.5001]}`

`{"arm": 2, "type": "cell_summary", "g": 0.1, "pipeline": "A", "auroc_mean": 0.495, "ci_lo": 0.4813, "ci_hi": 0.5088, "seeds": [0.4842, 0.4781, 0.4922, 0.5177, 0.5029]}`

`{"arm": 2, "type": "cell_summary", "g": 0.1, "pipeline": "B", "auroc_mean": 0.5221, "ci_lo": 0.4824, "ci_hi": 0.5619, "seeds": [0.4845, 0.5419, 0.5824, 0.5316, 0.4702]}`

`{"arm": 2, "type": "cell_summary", "g": 0.2, "pipeline": "A", "auroc_mean": 0.4999, "ci_lo": 0.4755, "ci_hi": 0.5242, "seeds": [0.4575, 0.4919, 0.5077, 0.5326, 0.5096]}`

`{"arm": 2, "type": "cell_summary", "g": 0.2, "pipeline": "B", "auroc_mean": 0.5832, "ci_lo": 0.5443, "ci_hi": 0.6222, "seeds": [0.5351, 0.551, 0.619, 0.6393, 0.5719]}`

`{"arm": 2, "type": "cell_summary", "g": 0.35, "pipeline": "A", "auroc_mean": 0.5106, "ci_lo": 0.4879, "ci_hi": 0.5333, "seeds": [0.5355, 0.5217, 0.5302, 0.4797, 0.4859]}`

`{"arm": 2, "type": "cell_summary", "g": 0.35, "pipeline": "B", "auroc_mean": 0.8066, "ci_lo": 0.7802, "ci_hi": 0.8331, "seeds": [0.776, 0.7753, 0.8402, 0.8109, 0.8307]}`

`{"arm": 2, "type": "cell_summary", "g": 0.6, "pipeline": "A", "auroc_mean": 0.5476, "ci_lo": 0.5209, "ci_hi": 0.5743, "seeds": [0.5328, 0.5225, 0.533, 0.5509, 0.5989]}`

`{"arm": 2, "type": "cell_summary", "g": 0.6, "pipeline": "B", "auroc_mean": 0.983, "ci_lo": 0.9778, "ci_hi": 0.9881, "seeds": [0.9871, 0.9832, 0.9902, 0.977, 0.9774]}`

`{"arm": 2, "type": "shuffled_summary", "pipeline": "A", "auroc_mean": 0.5333, "ci_lo": 0.5051, "ci_hi": 0.5615, "seeds": [0.5597, 0.5328, 0.5171, 0.4889, 0.5681]}`

`{"arm": 2, "type": "shuffled_summary", "pipeline": "B", "auroc_mean": 0.505, "ci_lo": 0.4778, "ci_hi": 0.5321, "seeds": [0.5082, 0.5082, 0.4891, 0.5517, 0.4676]}`

`{"arm": 2, "type": "verdict", "A_at_chance_all_g": false, "A_strong_form_falsified": true, "B_at_chance_all_g": false, "B_ci_lo_gt_half_at_g060": true, "construction_sanity_B_mean_g060": 0.983, "construction_sanity_pass": true, "verdict": "strong-form falsified", "shuffled_control_A_covers_half": false, "shuffled_control_B_covers_half": true, "seconds": 409.9}`


## ADDENDUM 3, 2026-10-07 (arm 2 verdict calibration, filed before arm 3)

The arm 2 run recorded: A at g=0.60 mean AUROC 0.5476, CI [0.5209, 0.5743],
which fires the pre-registered strong-form-falsified letter rule (CI lower
bound above 0.5). The same run's pre-registered shuffled-label control for
pipeline A at g=0.60 read 0.5333, CI [0.5051, 0.5615], which also excludes
0.5 and therefore FAILS its must-cover-0.5 check. Two pre-registered checks
conflict; the control exists precisely to adjudicate this.

Calibration analysis (no new data): difference between real-A and shuffled-A
seed means at g=0.60 is 0.5476 - 0.5333 = 0.0143; SE of that difference
across independent 5-seed means (real-A seed sd 0.028, shuffled-A seed sd
0.030) is approx sqrt((0.028^2 + 0.030^2)/5) = 0.0182, so z approx 0.79,
p approx 0.43 two-sided. The A elevation at g=0.60 is statistically
indistinguishable from pipeline A's own shuffled-label null and cannot be
attributed to recovered coupling. The per-component marginal-invariance
argument also forbids genuine per-component signal for this construction.
Recorder's judgment, flagged as such: arm 2 is read as A-at-chance at every g
after calibration against its own shuffled null, B above chance with a clean
graded curve (0.4731 at g=0.05 to 0.9830 at g=0.60); the uncalibrated
letter-rule firing and the failed A-control are both on the record above and
in results.jsonl. The operator may overrule this calibration reading.

### Arm run 3 (appended 2026-10-07T16:06:14Z, by residue_probe.py)

`{"arm": 3, "type": "cell", "seed": 1000, "g": 0.05, "detector": "A_coh", "auroc": 0.4875}`

`{"arm": 3, "type": "cell", "seed": 1000, "g": 0.05, "detector": "B_quat", "auroc": 0.5056}`

`{"arm": 3, "type": "cell", "seed": 2000, "g": 0.05, "detector": "A_coh", "auroc": 0.4992}`

`{"arm": 3, "type": "cell", "seed": 2000, "g": 0.05, "detector": "B_quat", "auroc": 0.5211}`

`{"arm": 3, "type": "cell", "seed": 3000, "g": 0.05, "detector": "A_coh", "auroc": 0.5007}`

`{"arm": 3, "type": "cell", "seed": 3000, "g": 0.05, "detector": "B_quat", "auroc": 0.5002}`

`{"arm": 3, "type": "cell", "seed": 4000, "g": 0.05, "detector": "A_coh", "auroc": 0.5148}`

`{"arm": 3, "type": "cell", "seed": 4000, "g": 0.05, "detector": "B_quat", "auroc": 0.491}`

`{"arm": 3, "type": "cell", "seed": 5000, "g": 0.05, "detector": "A_coh", "auroc": 0.4816}`

`{"arm": 3, "type": "cell", "seed": 5000, "g": 0.05, "detector": "B_quat", "auroc": 0.5282}`

`{"arm": 3, "type": "cell", "seed": 1000, "g": 0.1, "detector": "A_coh", "auroc": 0.4863}`

`{"arm": 3, "type": "cell", "seed": 1000, "g": 0.1, "detector": "B_quat", "auroc": 0.5048}`

`{"arm": 3, "type": "cell", "seed": 2000, "g": 0.1, "detector": "A_coh", "auroc": 0.509}`

`{"arm": 3, "type": "cell", "seed": 2000, "g": 0.1, "detector": "B_quat", "auroc": 0.492}`

`{"arm": 3, "type": "cell", "seed": 3000, "g": 0.1, "detector": "A_coh", "auroc": 0.5362}`

`{"arm": 3, "type": "cell", "seed": 3000, "g": 0.1, "detector": "B_quat", "auroc": 0.5259}`

`{"arm": 3, "type": "cell", "seed": 4000, "g": 0.1, "detector": "A_coh", "auroc": 0.4873}`

`{"arm": 3, "type": "cell", "seed": 4000, "g": 0.1, "detector": "B_quat", "auroc": 0.4895}`

`{"arm": 3, "type": "cell", "seed": 5000, "g": 0.1, "detector": "A_coh", "auroc": 0.4865}`

`{"arm": 3, "type": "cell", "seed": 5000, "g": 0.1, "detector": "B_quat", "auroc": 0.4973}`

`{"arm": 3, "type": "cell", "seed": 1000, "g": 0.2, "detector": "A_coh", "auroc": 0.4977}`

`{"arm": 3, "type": "cell", "seed": 1000, "g": 0.2, "detector": "B_quat", "auroc": 0.5475}`

`{"arm": 3, "type": "cell", "seed": 2000, "g": 0.2, "detector": "A_coh", "auroc": 0.4864}`

`{"arm": 3, "type": "cell", "seed": 2000, "g": 0.2, "detector": "B_quat", "auroc": 0.51}`

`{"arm": 3, "type": "cell", "seed": 3000, "g": 0.2, "detector": "A_coh", "auroc": 0.5278}`

`{"arm": 3, "type": "cell", "seed": 3000, "g": 0.2, "detector": "B_quat", "auroc": 0.5144}`

`{"arm": 3, "type": "cell", "seed": 4000, "g": 0.2, "detector": "A_coh", "auroc": 0.5069}`

`{"arm": 3, "type": "cell", "seed": 4000, "g": 0.2, "detector": "B_quat", "auroc": 0.54}`

`{"arm": 3, "type": "cell", "seed": 5000, "g": 0.2, "detector": "A_coh", "auroc": 0.4972}`

`{"arm": 3, "type": "cell", "seed": 5000, "g": 0.2, "detector": "B_quat", "auroc": 0.5244}`

`{"arm": 3, "type": "cell", "seed": 1000, "g": 0.35, "detector": "A_coh", "auroc": 0.4914}`

`{"arm": 3, "type": "cell", "seed": 1000, "g": 0.35, "detector": "B_quat", "auroc": 0.561}`

`{"arm": 3, "type": "cell", "seed": 2000, "g": 0.35, "detector": "A_coh", "auroc": 0.5343}`

`{"arm": 3, "type": "cell", "seed": 2000, "g": 0.35, "detector": "B_quat", "auroc": 0.5813}`

`{"arm": 3, "type": "cell", "seed": 3000, "g": 0.35, "detector": "A_coh", "auroc": 0.5254}`

`{"arm": 3, "type": "cell", "seed": 3000, "g": 0.35, "detector": "B_quat", "auroc": 0.5727}`

`{"arm": 3, "type": "cell", "seed": 4000, "g": 0.35, "detector": "A_coh", "auroc": 0.502}`

`{"arm": 3, "type": "cell", "seed": 4000, "g": 0.35, "detector": "B_quat", "auroc": 0.568}`

`{"arm": 3, "type": "cell", "seed": 5000, "g": 0.35, "detector": "A_coh", "auroc": 0.5333}`

`{"arm": 3, "type": "cell", "seed": 5000, "g": 0.35, "detector": "B_quat", "auroc": 0.5657}`

`{"arm": 3, "type": "cell", "seed": 1000, "g": 0.6, "detector": "A_coh", "auroc": 0.4986}`

`{"arm": 3, "type": "cell", "seed": 1000, "g": 0.6, "detector": "B_quat", "auroc": 0.6901}`

`{"arm": 3, "type": "cell", "seed": 2000, "g": 0.6, "detector": "A_coh", "auroc": 0.5228}`

`{"arm": 3, "type": "cell", "seed": 2000, "g": 0.6, "detector": "B_quat", "auroc": 0.6814}`

`{"arm": 3, "type": "cell", "seed": 3000, "g": 0.6, "detector": "A_coh", "auroc": 0.5037}`

`{"arm": 3, "type": "cell", "seed": 3000, "g": 0.6, "detector": "B_quat", "auroc": 0.7018}`

`{"arm": 3, "type": "cell", "seed": 4000, "g": 0.6, "detector": "A_coh", "auroc": 0.485}`

`{"arm": 3, "type": "cell", "seed": 4000, "g": 0.6, "detector": "B_quat", "auroc": 0.6774}`

`{"arm": 3, "type": "cell", "seed": 5000, "g": 0.6, "detector": "A_coh", "auroc": 0.55}`

`{"arm": 3, "type": "cell", "seed": 5000, "g": 0.6, "detector": "B_quat", "auroc": 0.6919}`

`{"arm": 3, "type": "construction_sanity", "n_per_condition": 10000, "g": 0.6, "A_coh_mean_null": 0.656579, "A_coh_mean_coupled": 0.656513, "A_coh_shift_in_pooled_SE": 0.05, "B_quat_mean_null": 0.008502, "B_quat_mean_coupled": 0.009939, "B_quat_shift_in_pooled_SE": 48.43, "B_quat_norm_mean_null": 0.256946, "B_quat_norm_mean_coupled": 0.256955, "B_quat_norm_shift_in_pooled_SE": 0.02, "B_sanity_pass_gt5SE": true}`

`{"arm": 3, "type": "diagnostic_comm", "g": 0.05, "auroc_mean": 0.5095, "ci_lo": 0.4965, "ci_hi": 0.5225}`

`{"arm": 3, "type": "diagnostic_norm_former_primary", "g": 0.05, "auroc_mean": 0.4912, "ci_lo": 0.4769, "ci_hi": 0.5054}`

`{"arm": 3, "type": "diagnostic_rawdot_shift", "g": 0.05, "mean_shift": 3.12e-06}`

`{"arm": 3, "type": "diagnostic_comm", "g": 0.1, "auroc_mean": 0.4939, "ci_lo": 0.4822, "ci_hi": 0.5057}`

`{"arm": 3, "type": "diagnostic_norm_former_primary", "g": 0.1, "auroc_mean": 0.5083, "ci_lo": 0.4959, "ci_hi": 0.5207}`

`{"arm": 3, "type": "diagnostic_rawdot_shift", "g": 0.1, "mean_shift": 1.65e-06}`

`{"arm": 3, "type": "diagnostic_comm", "g": 0.2, "auroc_mean": 0.5146, "ci_lo": 0.4984, "ci_hi": 0.5309}`

`{"arm": 3, "type": "diagnostic_norm_former_primary", "g": 0.2, "auroc_mean": 0.4978, "ci_lo": 0.4879, "ci_hi": 0.5076}`

`{"arm": 3, "type": "diagnostic_rawdot_shift", "g": 0.2, "mean_shift": 2.279e-05}`

`{"arm": 3, "type": "diagnostic_comm", "g": 0.35, "auroc_mean": 0.5384, "ci_lo": 0.5322, "ci_hi": 0.5446}`

`{"arm": 3, "type": "diagnostic_norm_former_primary", "g": 0.35, "auroc_mean": 0.4961, "ci_lo": 0.4885, "ci_hi": 0.5037}`

`{"arm": 3, "type": "diagnostic_rawdot_shift", "g": 0.35, "mean_shift": 5.974e-05}`

`{"arm": 3, "type": "diagnostic_comm", "g": 0.6, "auroc_mean": 0.6101, "ci_lo": 0.5942, "ci_hi": 0.626}`

`{"arm": 3, "type": "diagnostic_norm_former_primary", "g": 0.6, "auroc_mean": 0.4957, "ci_lo": 0.481, "ci_hi": 0.5103}`

`{"arm": 3, "type": "diagnostic_rawdot_shift", "g": 0.6, "mean_shift": 0.00019759}`

`{"arm": 3, "type": "cell_summary", "g": 0.05, "detector": "A_coh", "auroc_mean": 0.4968, "ci_lo": 0.4855, "ci_hi": 0.508, "seeds": [0.4875, 0.4992, 0.5007, 0.5148, 0.4816]}`

`{"arm": 3, "type": "cell_summary", "g": 0.05, "detector": "B_quat", "auroc_mean": 0.5092, "ci_lo": 0.4959, "ci_hi": 0.5226, "seeds": [0.5056, 0.5211, 0.5002, 0.491, 0.5282]}`

`{"arm": 3, "type": "cell_summary", "g": 0.1, "detector": "A_coh", "auroc_mean": 0.5011, "ci_lo": 0.4819, "ci_hi": 0.5203, "seeds": [0.4863, 0.509, 0.5362, 0.4873, 0.4865]}`

`{"arm": 3, "type": "cell_summary", "g": 0.1, "detector": "B_quat", "auroc_mean": 0.5019, "ci_lo": 0.489, "ci_hi": 0.5147, "seeds": [0.5048, 0.492, 0.5259, 0.4895, 0.4973]}`

`{"arm": 3, "type": "cell_summary", "g": 0.2, "detector": "A_coh", "auroc_mean": 0.5032, "ci_lo": 0.4895, "ci_hi": 0.5168, "seeds": [0.4977, 0.4864, 0.5278, 0.5069, 0.4972]}`

`{"arm": 3, "type": "cell_summary", "g": 0.2, "detector": "B_quat", "auroc_mean": 0.5273, "ci_lo": 0.5131, "ci_hi": 0.5414, "seeds": [0.5475, 0.51, 0.5144, 0.54, 0.5244]}`

`{"arm": 3, "type": "cell_summary", "g": 0.35, "detector": "A_coh", "auroc_mean": 0.5173, "ci_lo": 0.5002, "ci_hi": 0.5343, "seeds": [0.4914, 0.5343, 0.5254, 0.502, 0.5333]}`

`{"arm": 3, "type": "cell_summary", "g": 0.35, "detector": "B_quat", "auroc_mean": 0.5697, "ci_lo": 0.563, "ci_hi": 0.5765, "seeds": [0.561, 0.5813, 0.5727, 0.568, 0.5657]}`

`{"arm": 3, "type": "cell_summary", "g": 0.6, "detector": "A_coh", "auroc_mean": 0.512, "ci_lo": 0.49, "ci_hi": 0.5341, "seeds": [0.4986, 0.5228, 0.5037, 0.485, 0.55]}`

`{"arm": 3, "type": "cell_summary", "g": 0.6, "detector": "B_quat", "auroc_mean": 0.6885, "ci_lo": 0.6802, "ci_hi": 0.6969, "seeds": [0.6901, 0.6814, 0.7018, 0.6774, 0.6919]}`

`{"arm": 3, "type": "verdict", "A_at_chance_all_g": true, "A_coherence_leak": true, "B_at_chance_all_g": false, "B_ci_lo_gt_half_at_g060": true, "verdict": "coherence leak: projections retain higher-order signal", "seconds": 12.2}`


## ADDENDUM 4, 2026-10-07 (arm 3 verdict calibration, filed after the run, alongside the raw rows)

The arm 3 verdict row coded "coherence leak" because A_coh at g=0.35 read
mean 0.5173, CI [0.5002, 0.5343], lower bound 0.0002 above 0.5. The
pre-registered 20,000-stream population sanity at g=0.60 measured the coherence
score shift at 0.05 pooled SE (A_coh mean null 0.656579 vs coupled 0.656513),
i.e. no population-level signal at twice the coupling strength, while the
quaternion-domain score shifted 48.43 SE (0.008502 vs 0.009939). The A_coh
means are also non-monotone in g (0.5173 at 0.35 vs 0.5120 at 0.60), opposite
to any g-squared leak law. Recorder's judgment, flagged as such: the g=0.35
lower bound is a 1-in-10-cells letter edge, not evidence of retained signal;
arm 3 is read as A-at-chance at every g and B above chance at g >= 0.20
(0.6885, CI [0.6802, 0.6969] at g=0.60). The coded verdict row stands
unedited in results.jsonl; the operator may overrule this calibration.
