# AH8 — LDT v1: learned set-valued concept layer under the exact lattice mask (2026-09-30)

## Verdict: HONEST LOSS — AE2's falsifier fires

v1 does NOT Pareto-beat renorm at 100% data (TRADE: +coverage / −soundness) and does not match renorm@100 with 50% or 25% of the data. The NCP 1.95x data-efficiency claim does not transfer to this rung. Banked as a falsified mapping, not a softened one.

## Files (owned, uncommitted)

- `tools/ldt_lattice.py` — v1 additions: `lattice_gate` (exact subset mask over all 32 elements), `setval_targets`, `evaluate_setval` (decision semantics: singleton commit = answered, hedge/BOTTOM = abstention), `--v1` CLI (raw/renorm/v1-setval at 25/50/100% data, frozen-Z13 parity check, saved model)
- `tools/ldt_train.py` — v1 additions: `train_model_gated` (cross-entropy to a target ELEMENT under a per-row boolean output gate — gated-out columns carry exactly zero data gradient; renormalization happens INSIDE training via the one shared op `renormalize_gated`), `subset_rows` (deterministic data-scaling axis, parity law)
- `tests/test_ldt_lattice.py` — 16 tests (6 v0 + 10 new v1 laws: exact-subset gate, truth-in-gate, renorm math, open-gate parity with `train_model`, zero-gradient-outside-gate at l2=0, hand-referenced `evaluate_setval` contract, hedge-not-answer semantics, subset determinism)
- `models/ldt_v1_setval.npz` — the trained 32-element head (42464 weight elements vs raw's 40709)
- Run log: `ah8_v1_run.log` (wall 33.5s, budget 600s)

## What was built

Head = logits over all 32 lattice elements (BOTTOM first, then subsets by size — element order frozen by the index map in the tool). Training: target = singleton of the true label (its lattice position), softmax gated by `gate[i,e] iff element e ⊆ F_i` (the EXACT lattice mask from V7's cascade), renormalized within the gate — so training optimizes the same renormalized-within-mask quantity renorm inference reads. Inference: softmax → gate → renormalize → argmax element; answered iff conf ≥ 0.7 AND argmax is a singleton; correct iff that singleton == {y}. Truth-feasibility law held (0 val labels outside F); `answered_infeasible` = 0 in every arm (by construction, verified not assumed).

## Numbers (val split, n=2000, tau=0.7, seed=13, 40 epochs, hidden 128,64)

| train frac | arm | coverage | soundness | answered (corr/wrong) |
|---|---|---|---|---|
| 100% (18000) | raw Z13 | 0.9320 | 0.8830 | 1864 (1646/218) |
| 100% | renorm (post-hoc) | 0.9805 | **0.9806** | 1961 (1923/38) |
| 100% | v1-setval (learned) | **0.9855** | 0.9767 | 1971 (1925/46) |
| 50% (9000) | raw | 0.9110 | 0.8875 | 1822 (1617/205) |
| 50% | renorm | 0.9760 | 0.9718 | 1952 (1897/55) |
| 50% | v1-setval | **0.9875** | **0.9737** | 1975 (1923/52) |
| 25% (4500) | raw | 0.9040 | 0.8883 | 1808 (1606/202) |
| 25% | renorm | 0.9765 | 0.9744 | 1953 (1903/50) |
| 25% | v1-setval | **0.9845** | 0.9726 | 1969 (1915/54) |

Machine BAR checks (the receipt cannot soften these): `v1@100 vs renorm@100 = TRADE`; `v1@50 vs renorm@100 (the 1.95x test) = TRADE`; `raw@100 reproduces frozen Z13 = yes` (0.8545 / 0.8830 exact — byte-parity law held).

## Reading the loss

- v1 trades everywhere on the bar's plane: it buys coverage (+0.0050 @100) at soundness' expense (−0.0040; 46 wrong vs renorm's 38). Within the SAME fraction it Pareto-beats renorm at 50% (cov +0.0115, snd +0.0019) but trades at 25% and 100% — not a stable dominance, so the bar stays missed.
- The hedge never fires: `hedged = 0` and `argmax_bottom = 0` in every arm. Singleton-only targets never teach set-valued answers — the 27 non-singleton atoms are live capacity that no gradient mass sits on, and the head collapses to singleton commits. The "honest hedge" semantics (legal pair at high crown-physics uncertainty) went unused; coverage gain came from sharper singleton confidence inside F, not from hedging.
- Why learned renorm loses to applied renorm at 100%: the post-hoc projection renormalizes a 5-way softmax conditioned on a model trained with ALL its capacity on the 5 decision atoms; the v1 head spreads its final layer over 32 columns (renormalization within 2–4 live elements amplifies whatever noise sits on them) — it pays a soundness tax for capacity it never needed. AE2's "their codebook is learned, ours is exact" divergence lands on their side here: exactness was already free; learning added nothing the mask didn't already give.
- Data scaling: v1@50 (0.9737/0.9875) and v1@25 (0.9726/0.9845) both fail to match renorm@100 (0.9806/0.9805) — no 1.95x, no data-efficiency edge for concept-space learning on this rung.

## Reproduce

```
.venv\Scripts\python.exe tools\ldt_lattice.py --v1
.venv\Scripts\python.exe -m pytest tests/test_ldt_lattice.py tests/test_ldt_train.py -q   # 16 passed
```

## Next (if the lane refires)

Target smoothing is the untested lever: put target mass on every gated-on SUPERSET containing the truth (not just {y}) so hedging is trained, not merely permitted — the falsifier here narrows the loss to "targets never taught the set-valued half of the head." If that still trades, the concept-layer thesis on this lattice is dead and V7's post-hoc renorm stands as the ceiling.
