# AF1 — CONCEPT PREDICTOR: LDT shape on the percolator stream (2026-09-30)

Seat: implementation. Files owned: `tools/concept_predictor.py`, `tests/test_concept_predictor.py`, this receipt. No commit. Mission: AE6's implied build (`AE6_CONCEPT_QUANTIZER.md`) — the `tools/ldt_train.py` numpy-MLP pattern applied to `memory/percolator/explore.jsonl` instead of token renders; must beat the frequency baseline on a chronological holdout or the falsifier fires.

## Shape (exactly as ordered)

- DATA: `(ts, source, domain, canonical, lane)` events sorted by ts; source normalized to stream classes (`fuel:*` → `fuel`, `ox:t*` → `ox`, `OX_RESIDENT*` → `ox_resident`, `moderation:*` → `moderation`). Run pinned: sha256 `899ebac78985…`, 1,907 rows (file grew 1,902 → 1,907 mid-session — live appends; the receipt's numbers are from the pinned read), 1,817 unique canonicals, 431 lane-bearing rows.
- FEATURES: one-hot (source|domain|canonical|lane) per each of the last K=8 events + 3h hour bucket of the newest event; all vocabs train-fit only, unseen → `other` bucket. Two heads = two independent numpy MLPs (`128,64` ReLU, stable softmax, minibatch Adam + l2, one rng stream; no torch, no deps beyond numpy).
- TARGETS: next-canonical (candidate vocab = 29 canonicals recurring ≥2x in train) and next-lane (lane-bearing subsequence, 7 train lanes — the AC10 game).
- BASELINE: frequency predictor, most-common next given current (bigram, deterministic `(-count, name)` ranking, unigram backoff + top-3 padding). Parity law: identical training windows, identical candidate vocab, identical scored holdout rows for baseline and MLP.
- EVAL: chronological holdout, last 15%. Unified protocol (fixed mid-build): every holdout window scores; OOV truth = miss for every predictor; `n_in_vocab` reports winnable rows. The first cut scored only in-vocab canonical truths and got 0/287 NaNs — a broken eval, not a result.
- Determinism: two full runs, identical accuracies (0.4923/0.8462/0.4615/0.7846); only wall time moved (32.8s vs 75.8s, machine load).

## Results (holdout, top-1 / top-3)

| target | n scored (in-vocab) | unigram | baseline | MLP | verdict |
|---|---|---|---|---|---|
| next-canonical | 287 (0) | .000 / .000 | .000 / .000 | .000 / .000 | UNSCORABLE |
| next-lane | 65 (64) | .508 / .508 | .462 / .785 | **.492 / .846** | MLP BEATS baseline |

- next-lane: MLP beats the mission baseline on top-1 (+0.031 = 2/65 rows) and top-3 (+0.062 = 4/65). Thin margin, named honestly.
- Caveat the table carries: unigram top-1 (.508) still edges MLP top-1 (.492) on lane — sequence conditioning has not yet beaten the marginal on top-1; it clearly does on top-3.
- next-canonical: UNSCORABLE, and that is a data fact, not a model failure — all 29 recurring canonicals' 119 occurrences sit strictly before the split; the entire 287-row holdout tail (since 2026-09-27T23:24Z) is `behavioral`-domain novelty only. The AE6 falsifier ("can't beat the frequency baseline") neither fires nor clears for canonical: no evidence exists in this era. Exact-canonical prediction over the full stream is UUID-guessing (1,817/1,907 unique).

## Bug receipt (tests earned their keep)

First featurizer cut placed the domain one-hot at `base + sD` (sD=0, the source block start) instead of `base + dD`, silently overwriting every source one-hot with the domain one-hot. Caught by the test suite's 4-per-event one-hot count invariant (13 lit columns ≠ 17 per window) before any result was banked; fix in `transform()` carries the comment. The bugfix (not tuning; config unchanged) is what moved lane MLP top-1 from tie (.462) to beat (.492): source signal restored.

## Verification

- `tests/test_concept_predictor.py`: 6 passed (0.82s) — extraction/sort/drop/normalize, window construction no-peeking, baseline sanity (bigram ≥ max unigram frequency on its own training set, ==1.0 on deterministic transitions, top-3 padding + candidate filtering), end-to-end small slice (loss falls, holdout top-1 ≥ 0.7 vs 1/3 chance).
- Full run: 32.8s / 75.8s wall (budget 180s), `$0`, weights at `models/concept_predictor.npz` (schema `concept_predictor_v0`, data sha + config inside).
- Census (instrument + moment named, per the census law): scoped pytest run 2026-09-30, `pytest tests/test_concept_predictor.py tests/test_ldt_train.py tests/test_percolator_z15.py -q` → **23 passed in 1.69s** (6 new + 17 neighboring, no interference). A full `pytest -q` was launched in the background and stopped after ~28 min without completing; no full-suite number is claimed here — the operator's pre-push run is the census of record.

## Rerun

```text
.venv\Scripts\python.exe tools\concept_predictor.py
.venv\Scripts\python.exe -m pytest tests/test_concept_predictor.py -q
```

Verdict for the wave synthesis: AC10's chooser has an empirical core candidate (lane head beats its frequency baseline), the canonical head needs a stream where recurring concepts actually fire in the eval era before the thesis is testable.
