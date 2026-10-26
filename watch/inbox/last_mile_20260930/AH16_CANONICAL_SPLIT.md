# AH16 — CANONICAL SPLIT REDESIGN: grouped key-side holdout, 4-cell table (2026-09-30)

Seat: implementation (refire of AF1's data fact). Files owned: `tools/concept_predictor.py` (extended), `tests/test_concept_predictor.py`, this receipt. No commit.

## Mission

AF1 banked that next-canonical was UNSCORABLE: all 119 recurring-canonical occurrences sit in the train era, the chronological tail is pure novelty (0/287 in-vocab). AH16 makes the canonical question answerable without abandoning the honest forecast game: every head reports TWO splits.

## Design (spec-first: the module docstring was committed to the working tree before the code caught up)

- GROUPED (AH16): hold out a seeded random 15% (round, floor 1) of RECURRING key-groups — keys with >=2 occurrences among window keys — moving every window KEYED by a held group to holdout across its full timeline (scattered indices, not a tail). Key-side by design: target-side grouping would strip every training row of a held canon (unnameable by construction, a protocol ceiling); key-side keeps every recurring canon a trained class on both sides while the unseen-canon pressure moves to the conditioning side.
- CHRONO (AF1, kept): the time tail, labeled novelty-forecast.
- No-peeking featurizer law: the featurizer fits ONLY on events covered by train windows (context + target); for chrono this reduces exactly to `events[:cut]` (AF1's fit verbatim — lane-chrono reproduced AF1's accuracies bit-for-bit).
- Unified scoring protocol (AF1): every holdout window scores; OOV truth = miss for every predictor; `n_in_vocab` reports winnable rows. Parity: baseline and MLP see identical train windows, candidate vocab, scored rows. Seeded determinism: seed 13 holds canonical groups `c68e0b3b7891b698, d5c42653281b6828, d9d0058bd26a6c52, e220fbd0c986227d` and lane group `z_ai`.

## Results (4-cell table, holdout top-1 / top-3; data pinned sha256 6d9463a553cc, 1,921 rows — file grew 1,916 → 1,921 mid-session; the run's numbers are the pinned read)

| head | split | n scored (in-vocab) | baseline | MLP | verdict |
|---|---|---|---|---|---|
| next-canonical | grouped (AH16) | 15 (10) | .000 / .000 | **.067 / .267** | MLP BEATS baseline |
| next-canonical | chrono (novelty-forecast) | 289 (0) | .000 / .000 | .000 / .000 | UNSCORABLE |
| next-lane | grouped (AH16) | 55 (55) | .182 / .436 | **.545 / .909** | MLP BEATS baseline |
| next-lane | chrono (novelty-forecast) | 65 (64) | .462 / .785 | **.492 / .846** | MLP BEATS baseline |

- Canonical signal under recurrence representation: PRESENT, thin. 1/15 top-1, 4/15 top-3 vs a baseline that hits 0/15 on both (unigram fallback's top guesses never match the truths following held keys). Strict beat, falsifier did NOT fire — but n=15 (10 winnable), single seed: evidence exists, margin honest-thin.
- Lane grouped is the strongest cell: +0.364 top-1 / +0.473 top-3 over the bigram baseline, which collapses on unseen keys (unigram floor .182). Cold-start conditioning is exactly where sequence representation pays.
- Lane chrono reproduces AF1 exactly (.4923/.8462 vs .4615/.7846): the chrono code path is regression-clean under the redesign.
- Canonical chrono remains UNSCORABLE by data fact (0/289 in-vocab): the novelty tail persists; that column is the forecast game, not the recurrence game.

## Mechanism note (why the test suite does not assert a win)

Key-side grouping leaves the held canon's LAST-SLOT feature column untrained by construction (no train window is keyed by a held canon), so any transfer must come from deeper-context / cross-feature representation. A synthetic engineered to transfer (shared domain feature) still beat the baseline only marginally and hyperparameter-fragilely — the win is the experiment's outcome, not a law. Tests assert answerability (recurring canons nameable on BOTH sides, n_in_vocab > 0), the unseen-key baseline's exact unigram fallback, verdict wiring, full-timeline scattered membership, determinism, and the no-peeking fit mask. Held-group override raises ValueError on non-recurring names (a pinned rerun must never silently hold nothing and report UNSCORABLE — a fabricated non-result).

## Verification

- `tests/test_concept_predictor.py`: 10 passed (1.5s) — AF1's 6 + chrono-cut regression, grouped membership/determinism/override-fail-loud, no-peeking fit mask, grouped-cell answerability + wiring.
- Two full runs, identical accuracies all 4 cells; wall 216.0s / 92.1s (machine load), both under the 300s mission cap.
- Ratchet: `tools/violation_ratchet.py check --changed` PASS (0 new debt). Weights: `models/concept_predictor.npz`, schema `concept_predictor_v1` (4 cells, held groups + config inside).
- Census (instrument + moment named): `pytest tests/test_concept_predictor.py -q` → 10 passed in 1.53s, 2026-09-30. No full-suite number claimed here; operator's pre-push run is the census of record.

## Rerun

```text
.venv\Scripts\python.exe tools\concept_predictor.py
.venv\Scripts\python.exe -m pytest tests/test_concept_predictor.py -q
```

Verdict for the wave synthesis: with recurrence represented on both sides, the canonical head beats its frequency baseline for the first time (thinly: 1/15), and the lane head beats it decisively under cold-start conditioning (+0.36 top-1). The AE6 falsifier stays holstered on both heads; the honest open item is margin, not existence.
