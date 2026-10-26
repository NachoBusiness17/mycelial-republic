# Z13 — LDT v0 TRAINING RUN (the baseline control, no lattice)

Lane Z13, 2026-09-29, Mickey17 W3K. Z12 manifest edge #1 asks for the LDT
training run; this lane lands its FLOOR first: a pure-numpy bag-of-atoms
classifier on the flat token render, no lattice projection (that treatment
comes later and must beat this number). No commit (operator order).

## Stack

- Data: `logs/legality_ds` 18k train / 2k val (seed 17, engine-labeled,
  sha256 train `466ebdb0…`). Touched nothing — read-only.
- Oracle standing: Y10 propagator agreement 7100/7100 cases (prior lane).
- Model: numpy-only MLP 250 -> 128 -> 64 -> 5 (softmax, Adam, log1p token
  counts + verb/tgt onehots, train-fit vocab only). 40,709 weight elements.
  Torch check: `pip show torch` = 2.13.0 PRESENT in venv, but the lane card
  says pure-numpy — numpy used anyway (determinism, zero CUDA variance).
- Code: `tools/ldt_train.py` (new). Weights: `models/legality_v0.npz`
  (params + vocabs + config + val metrics). Tests:
  `tests/test_ldt_train.py` — 100-sample 1-epoch smoke, predict shape
  (n,5), npz round-trip identity, threshold-0 soundness==accuracy
  invariant. 2 passed in 1.10s; with test_legality_dataset.py: 7 passed.
  Ratchet on changed files: PASS, no new debt.

## Real numbers (val n=2000, threshold 0.7, seed 13, 40 epochs, 15.3s wall)

Overall val accuracy **0.8545** (majority class 0.343; train 0.9873 —
bag baseline overfits, that gap is part of the floor's story).

| class | support | recall | answered |
|---|---|---|---|
| illegal_unknown_verb | 186 | 1.0000 | 1.000 |
| illegal_unknown_target | 478 | 1.0000 | 1.000 |
| illegal_dry_pool | 561 | 0.7986 | 0.904 |
| legal_no_gain | 686 | 0.8149 | 0.921 |
| legal_gain | 89 | 0.4270 | 0.685 |

Abstain-adjusted soundness: coverage **0.9320** (1864/2000 answered),
soundness = 1646/(1646+218) = **0.8830**. Accuracy on the 136 abstained
rows: 0.4632 — abstention genuinely concentrates the unknowable ones.

## Where the floor leaks (confusion, val)

Every error is binding/physics classes; syntax classes are perfect:
`legal_no_gain -> illegal_dry_pool` 109 and back 86 (is the TARGET pool
dry? needs tgt↔v:0 binding a bag cannot see); `legal_gain` recall 0.427
(crown delta needs steam/siphon propagation). Zero errors involving
unknown_verb/unknown_target — identity atoms suffice for those.

## Next edges

- Lattice rung v1: typed atom-position features (tgt-bound node state,
  steam path existence) on the same split — the delta over 0.8545/0.883 is
  the lattice's purchase price.
- Calibration: 0.7 is arbitrary; sweep threshold for a coverage/soundness
  curve before claiming the abstain head tuned.
- legal_gain is 89/2000 — stratified eval or more gain-hunting samples.
