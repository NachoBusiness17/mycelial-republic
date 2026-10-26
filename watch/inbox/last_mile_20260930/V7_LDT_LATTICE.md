# V7 — LDT lattice scaffold, v0 post-hoc projection (2026-09-30)

## Result: PROVEN. The lattice projection lifts soundness 0.8830 -> 0.9862 @tau=0.7 on val (2000 rows), deleting exactly the 195 cross-tier errors and keeping every correct answer.

## Files (owned, uncommitted)

- `tools/ldt_lattice.py` — the candidate-set lattice + projection + CLI
- `tests/test_ldt_lattice.py` — 6 tests pinning the lattice laws

## The lattice

- Elements: all 32 subsets of the 5-way label set (powerset, order = subset inclusion; join = union, meet = intersection). **BOTTOM = the empty candidate set = ABSTAIN** — the abstain head rides the lattice.
- Descent: level 0 = full set; each level is one constraint of Y10's cascade (`tools/legality_propagator.py` — reused verbatim: `unknown_verb` -> `unknown_target` -> `dry_pool` -> legal pair). A firing constraint collapses the set to its illegal singleton and ends the descent (Y10's elif order). Level 4 (`depth="full"`, crown physics) exists but is NOT engaged by the v0 projection: it would make the lattice an oracle. Legality is by construction; the crown physics stays the model's job.
- v0 projection = post-hoc on Z13's logits (`models/legality_v0.npz`): mask the softmax to the feasible set F; strict mode reads the masked max un-renormalized; below tau -> BOTTOM.

## The law (why soundness cannot decrease)

Masked max <= raw max, so every strict answer was already a raw answer; the truth is always in F (verified: 0 val rows with label outside F), so a raw answer with argmax outside F was necessarily wrong — it either flips to the best feasible label or falls to BOTTOM. Wrong answers are the only thing removed. Pinned row-by-row + in-the-large by tests, and the empirical sweep shows strict soundness > raw soundness at every tau in {0.5, 0.6, 0.7, 0.8, 0.9}.

## Numbers (val split, n=2000, tau=0.7, saved Z13 model)

| mode | coverage | answered (corr/wrong) | soundness |
|---|---|---|---|
| raw Z13 | 0.9320 | 1864 (1646/218) | **0.8830** |
| lattice strict | 0.8345 | 1669 (1646/**23**) | **0.9862** |
| lattice renorm (v1 preview) | 0.9805 | 1961 (1923/38) | 0.9806 |

- 195 raw wrong answers killed (all cross-tier, e.g. predicting a legal label on an illegal_dry_pool row); correct count untouched (1646 = 1646). Tripwires: answered-infeasible = 0, answered-not-raw = 0.
- Renorm preview Pareto-dominates raw (higher soundness AND higher coverage than raw) — the v1 end-to-end signal.
- All 23 residual wrong answers are `legal_no_gain` <-> `legal_gain` — precisely the crown-physics distinction the lattice leaves to the model.

## Reproduce

```
.venv\Scripts\python.exe -m tools.ldt_lattice
.venv\Scripts\python.exe -m pytest tests/test_ldt_lattice.py -q   # 6 passed
# neighborhood: test_ldt_lattice + test_ldt_train + test_propagator + test_legality_dataset = 25 passed
```

## Next (v1)

End-to-end: model predicts a distribution over lattice elements directly (set-valued candidates, not just feasible singletons), abstain head trained as BOTTOM, renorm-mode conditioning learned instead of applied.
