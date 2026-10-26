# IMP7 — LDT v2: superset-target training (2026-09-30)

## Verdict: HONEST LOSS — TERMINAL for the concept-layer thesis on this lattice

v2 did what AH8's receipt named as the untested lever — it TAUGHT the set-valued half of the head (hedges went 0 → 555, every hedge containing the truth at rate 1.00) — and it still does not meet the bar: no superset fraction Pareto-beats renorm@100 (0.9806/0.9805) and none beats v1's coverage 0.9855 at equal-or-better soundness. AH8's pre-registered falsifier clause fires: "If that still trades, the concept-layer thesis on this lattice is dead and V7's post-hoc renorm stands as the ceiling." Both branches of the falsifier have now fired (v1: never taught; v2: taught, still trades). Banked as falsified; no softened reading.

## Files (owned, uncommitted)

- `tools/ldt_lattice.py` — v2 additions: `truth_superset_idx` (smallest gated truth-containing strict superset; -1 on ineligible illegal-tier rows), `superset_targets` (frac of ELIGIBLE rows switched, fresh rng stream seed+2 so v1 streams are untouched; frac=0.0 is bit-identical to v1), `run_v2` (full grid + machine BAR + model save), `--v2`/`--sup-fracs` CLI (the provider blip had landed the function bodies but died before wiring the CLI — this refire wired it). Refire fix, cause-named: the three verdict f-strings formatted a dict-key STRING with `:g` (`ValueError` on the first run after all training completed); fix is type-only (`float(best):g`), caught by run 1, green on run 2, identical numbers (determinism).
- `tests/test_ldt_lattice.py` — 18 tests (16 prior + 2 new v2 laws: `truth_superset_idx` legality/tier/-1; `superset_targets` frac=0 bit-parity, frac=1 full switch with all-targets-on-gate, seed determinism, switched-set nesting in frac, ineligible-never-switches, out-of-range raise)
- `models/ldt_v2_superset.npz` — best arm per the machine rule (max-soundness f=0.75 @100%: 0.9971/0.6845), 42464 weight elements
- Run log: `imp7_v2_run.log` (wall 109.8s, budget 900s — mission's 15-min CPU cap respected)

## What was built

Target-side only change, exactly per the IMP7 card: a `frac` fraction of ELIGIBLE rows (legal-pair rows — the only rows with a gated truth superset) get as training target the smallest truth-containing lattice superset, which on this dataset IS the legal pair F itself (so "smallest" and "sampled" coincide; a literal fraction-of-all-rows knob would saturate at |legal|/n ≈ 0.38 and collapse the 0.5/0.75 grid points). Illegal-tier rows keep the singleton (not eligible; their gate holds only {tier} and BOTTOM). Inference UNCHANGED from v1: masked softmax → renormalize → argmax element → `evaluate_setval` decision semantics (confident singleton = answered; hedge/BOTTOM = abstention). Training still `train_model_gated` (zero gradient outside the gate — the all-targets-on-gate law is asserted in the run, verified not assumed).

## Numbers (val n=2000, tau=0.7, seed=13, 40 epochs, hidden 128,64; grid = sup-frac × train-frac)

| train frac | arm | coverage | soundness | answered (c/w) | hedge (contains-truth) | switched/eligible |
|---|---|---|---|---|---|---|
| 100% (18000) | raw Z13 | 0.9320 | 0.8830 | 1864 (1646/218) | - | - |
| 100% | renorm (post-hoc) | 0.9805 | **0.9806** | 1961 (1923/38) | - | - |
| 100% | v1-setval (=v2 f=0) | **0.9855** | 0.9767 | 1971 (1925/46) | 0 (-) | 0/6838 |
| 100% | v2 f=0.1 | 0.9580 | 0.9729 | 1916 (1864/52) | 30 (1.00) | 683/6838 |
| 100% | v2 f=0.25 | 0.9010 | 0.9772 | 1802 (1761/41) | 120 (1.00) | 1698/6838 |
| 100% | v2 f=0.5 | 0.7715 | 0.9877 | 1543 (1524/19) | 337 (1.00) | 3360/6838 |
| 100% | v2 f=0.75 | 0.6845 | **0.9971** | 1369 (1365/4) | 555 (1.00) | 5064/6838 |
| 50% (9000) | renorm | 0.9760 | 0.9718 | 1952 (1897/55) | - | - |
| 50% | v1-setval | 0.9875 | 0.9737 | 1975 (1923/52) | 0 (-) | 0/3398 |
| 50% | v2 f=0.5 | 0.7710 | 0.9857 | 1542 (1520/22) | 342 (1.00) | 1684/3398 |
| 50% | v2 f=0.75 | 0.6620 | **0.9977** | 1324 (1321/3) | 574 (1.00) | 2547/3398 |
| 25% (4500) | renorm | 0.9765 | 0.9744 | 1953 (1903/50) | - | - |
| 25% | v1-setval | 0.9845 | 0.9726 | 1969 (1915/54) | 0 (-) | 0/1699 |
| 25% | v2 f=0.75 | 0.6570 | 0.9947 | 1314 (1307/7) | 605 (1.00) | 1274/1699 |

(Full grid incl. f=0.1/0.25 at 50% and 25% in the run log JSON; monotone in frac at every train fraction.)

## Machine BAR checks (the receipt cannot soften these)

- `raw@100 reproduces frozen Z13` = **yes** (0.8545/0.8830 byte-parity)
- `v1 arm (f=0) reproduces AH8 receipt` = **yes** (0.9855/0.9767 exact — frac=0 parity law machine-checked, not assumed)
- Clause 1, every v2 arm vs renorm@100: f=0.1 **LOSE**, f=0.25 **LOSE**, f=0.5 **TRADE**, f=0.75 **TRADE** → clause missed
- Clause 2, every v2 arm vs v1@100: all **LOSE** or **TRADE** (max v2 coverage 0.9580 < v1's 0.9855) → clause missed
- Data scaling: v2-best@50 and v2-best@25 vs renorm@100 both **TRADE** → still no 1.95x data-efficiency
- Tripwires: `answered_infeasible = 0` and `argmax_bottom = 0` in every arm (verified, by construction)

## Reading the loss

- **The lever mechanically worked.** v1's diagnosis ("singleton-only targets never teach set-valued answers; hedged=0") is CURED: hedges rise monotonically in frac (30 → 555 @100%) and every single hedge contains the truth (1.00 across all arms — by construction the only gateable non-singleton is the legal pair and truth always survives, but it is measured, not assumed). The honest hedge never lies; it declines to decide.
- **But the decision bar counts a hedge as abstention**, so teaching hedging converts would-be answers into abstentions: coverage falls monotonically (0.9855 → 0.6845) while soundness rises (0.9767 → 0.9971, wrong answers collapse 46 → 4). That is exactly the trade every conservative rule buys — nothing lattice-specific survives in it. Even crediting hedges as truth-carrying rows, v2@f=0.75 gives 1365 + 555 = 1920 < v1's 1925 correct < still under renorm's 1923 answered-correct at far higher coverage.
- **Why no arm can win here:** renorm@100's point (0.9806/0.9805) already sits near the ceiling of what confident-singleton committing achieves on this val split; the only move left on the (soundness, coverage) plane is trading along it. A learned head can slide along the tradeoff (v2 does, smoothly, in a controlled direction — the frac knob is a clean soundness-dial) but cannot dominate it. The 27 non-singleton atoms are live, trained capacity that can only ever buy abstention, never answers, because the decision semantics (rightly) refuse to let a set decide.
- **Both falsifier branches now fired:** v1 (never taught → collapsed to singletons) and v2 (taught → trades). Per AH8's pre-registration, the concept-layer thesis on THIS lattice is dead; V7's post-hoc renorm (0.9806/0.9805) stands as the ceiling, with v1@50% (0.9875/0.9737) the only within-lattice Pareto win ever recorded (fraction-local, not bar-relevant).

## Reproduce

```
.venv\Scripts\python.exe tools\ldt_lattice.py --v2            # grid: fractions 1.0,0.5,0.25 x sup-fracs 0.1,0.25,0.5,0.75 (+0.0 parity arm)
.venv\Scripts\python.exe -m pytest tests/test_ldt_lattice.py tests/test_ldt_train.py -q   # 18 passed
```

## Next (if the lane refires again — recommendation: do not, on this lattice)

The thesis is falsified at this rung; further target-side levers (mixup over elements, temperature on hedge rows) only re-parameterize the same soundness-for-coverage slide. If the concept layer is wanted anywhere, it needs a rung where set-valued answers are SCORABLE (partial credit for containing the truth), not one where they count as abstention — a different decision contract, not a different training target.
