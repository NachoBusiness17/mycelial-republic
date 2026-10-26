# IMP9 — Near-miss adversarial splits: does the lattice cure them? (2026-09-30)

## Verdict: YES — projection cures the near-miss, and the cure is exactly where the thesis claims it

N4's OOD split (c) built and run: 600 propagator-verified (legal_gain graph, one-retype illegal twin) pairs, 3 families x 200. The SAME Z13 weights (frozen-recipe retrain, parity `yes` = byte-exact 0.8545 val / 0.8830 soundness vs `models/legality_v0.npz`) evaluated raw vs post-hoc lattice-projected (V7 `evaluate_lattice`):

| arm | twin acc | fooled→legal_gain | twin soundness@0.7 | twin coverage | orig acc | BOTH-correct pairs | distinguished |
|---|---|---|---|---|---|---|---|
| raw | **0.2083** | 250/600 | 0.2198 | 0.7583 | 0.4883 | 29/600 | 83/600 |
| strict | 1.0000 | 0 | 1.0000 | 0.1667 | 0.6483 | 389/600 | 600/600 |
| renorm | 1.0000 | 0 | 1.0000 | 1.0000 | 0.6483 | 389/600 | 600/600 |

Per family (raw twin acc): dry_pool 0.625, unknown_target_node **0.000**, unknown_target_pipe **0.000**. The raw model never once predicts `illegal_unknown_target` on any rename twin — 0/400.

## Files (owned, uncommitted)

- `tools/ldt_nearmiss.py` — the generator + experiment (400 lines, ratchet-clean): twin builders, propagator-verified pair sampler, pair metrics, frozen-recipe train + raw/strict/renorm arms
- `tests/test_ldt_nearmiss.py` — 7 tests: flip law + ENGINE agreement on both sides of every pair, render-diff minimality (dry twin = exactly one atom), rename order/shape preservation, determinism, featurizer OOV law, projection pin
- `logs/nearmiss_ds/nearmiss.jsonl` + `MANIFEST.json` — the durable adversarial set (600 pairs, sha256 `4d07694f2dc9…`, seed 4242)

## The domain mapping (honest, load-bearing)

N4's design says "retype one edge: pipe->gate". In THIS graph, `validate` consults only the verb table, target existence, and (boil/tag) target volume — no pipe-field retype can flip legality. So the three minimal retypes that flip `legal_gain -> illegal_*` ARE the generator: **dry_pool** (target volume atom k->0; one render atom flips), **unknown_target_node** (T->T_twin; the render keeps every non-identity atom, the featurizer drops the OOV name — the hole is the whole signal), **unknown_target_pipe** (P->P_twin; the literal one-edge retype for valve). Every pair is propagator-verified to flip exactly; tests pin engine agreement so the generator cannot drift from the engine it is adversarial for.

## Why the raw model collapses (measured, not guessed)

Training's `illegal_unknown_target` signal lives entirely in the eight FAKE-target onehot columns (ghost/moon/vent/sump, `tgt:p_*`); a near-miss twin carries a REAL `tgt:T` with a missing `n:T` state atom — a pattern the training distribution never shows, and one a bag-of-atoms featurizer can only see as one dropped column among ~250. Predicted-class census on rename twins: node family 82 `illegal_dry_pool` / 69 `legal_gain` / 49 `legal_no_gain`; pipe family 128 `legal_gain` / 72 `legal_no_gain`. The model guesses; the twins break every correlation it rode.

## The honest bar (receipt cannot soften this)

- **renorm twin 1.0 / coverage 1.0 is a PROOF, not a measurement**: the twin's feasible set is the illegal singleton, renorm pins conf to exactly 1.0. That IS the soundness-by-construction story demonstrated on adversarial twins — the symbolic cascade re-derives legality per-sample, so the edit that fools the MLP cannot fool the mask (250 fooled -> 0).
- **The measured costs**: strict (shrink-only) answers just 100/600 twins at tau=0.7 — the pin charges coverage when raw mass sat on legal_gain; renorm re-answers all (answered_not_raw=221, answered_infeasible=0; strict's answered_not_raw=0, law held).
- **The lattice does NOT touch the crown-physics tier**: originals (F={legal_gain, legal_no_gain}) improve only 0.4883 -> 0.6483, and that lift is entirely killing infeasible-illegal argmaxes, not better gain/no-gain discrimination. 211/600 originals still missed = pair accuracy ceiling 389/600 (64.8%). The lattice cures legality near-misses by construction; the winning-move tier stays the model's job, by design.

## Reproduce

```
.venv\Scripts\python.exe tools\ldt_nearmiss.py        # wall 18.9s (budget 600s)
.venv\Scripts\python.exe -m pytest tests/test_ldt_nearmiss.py tests/test_ldt_train.py tests/test_ldt_lattice.py tests/test_legality_dataset.py tests/test_propagator.py -q   # 49 passed, 7.72s, post-edit
```

Determinism: two full runs post-edit produced byte-identical near-miss sha256 and metrics. Ratchet: `tools/ldt_nearmiss.py` at 400 lines, zero NEW violations for owned files (the ratchet's remaining FAIL rows are `tools/pain_replication/*` — another lane's uncommitted files, untouched here).
