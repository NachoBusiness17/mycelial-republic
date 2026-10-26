"""ldt_lattice tests — V7 lattice laws (Mickey17 W3 lane, 2026-09-30).

1. Lattice shape: 32 elements over the 5-way label set; join/meet are
   union/intersection with BOTTOM at the empty set; the cascade descent
   is a strictly-shrinking chain from the full set; depth="full" bottoms
   at a singleton.
2. Truth feasibility: over generated W3K rows the dataset's own label is
   always IN the feasible set (the lattice never excludes the truth —
   the projection can kill wrong answers, never right ones), and only
   the four cascade outcomes ever appear.
3. Monotonicity (the projection law, synthetic + deterministic): strict
   projection never answers outside F, never answers a row raw abstained
   on, keeps a feasible raw argmax; soundness(strict) >= soundness(raw)
   and coverage(strict) <= coverage(raw) at every threshold.
4. Soundness improves vs raw on a REAL (tiny) trained MLP: the laws hold
   empirically, answered_infeasible == 0, and the strict answers are a
   subset of the raw answers.
5. lattice_distribution: supported exactly on F, sums to 1 (empty F ->
   the certain-BOTTOM empty distribution).

AH8 v1 laws (2026-09-30, AE2's steal):

6. lattice_gate: gate[i, e] iff element e <= F_i (the EXACT lattice
   mask); BOTTOM gated on everywhere (abstention rides the lattice);
   per-row on-count is 2**|F_i| (illegal tier: 2, legal pair: 4).
7. setval_targets: the target is the singleton of the true label, and it
   is gated ON on every row (truth-in-gate law — gradients always have
   somewhere legal to land).
8. renormalize_gated: mass inside the gate resums to 1, gated-out
   columns exactly 0, gated-in ratios preserved.
9. train_model_gated parity + zero-gradient law: an all-ones gate with
   n_out=5 and y_elem=y reproduces train_model's dynamics; with l2=0, a
   gated-off output column stays BITWISE at init (the gate is
   self-enforcing — capacity never leaks to impossible atoms).
10. evaluate_setval: answered rows are singleton commits inside F
    (answered_infeasible == 0 by construction), hedges are counted
    separately with their contains-truth rate, and the metric contract
    matches a hand-computed reference on synthetic probs32.
11. subset_rows: deterministic, fraction=1.0 returns an unchanged copy
    (byte-parity with Z13's full-data recipe), strict subset rows keep
    file order.

IMP7 v2 laws (2026-09-30, AH8's named untested lever — superset targets):

12. truth_superset_idx: a legal-pair row's smallest truth-containing gated
    superset IS the pair (F itself — so "smallest" and "sampled" coincide
    on this dataset); an illegal-tier row has none (-1, not eligible).
13. superset_targets: frac=0.0 returns bit-identical v1 targets (the
    parity law behind run_v2's machine check); frac=1.0 switches every
    eligible row to its superset, ineligible rows keep the singleton;
    EVERY target stays gated ON; switched sets are nested in frac and
    deterministic per seed; out-of-range frac raises.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.legality_dataset import generate  # noqa: E402
from tools.legality_dataset import generate  # noqa: E402
from tools.ldt_lattice import (BOTTOM, LABELS, TOP, all_elements,  # noqa: E402
                               BOTTOM_IDX, SINGLETON_IDX, _ELEMENTS,
                               _ELEM_IDX, cascade_chain, evaluate_setval,
                               feasible_mask, feasible_set, join,
                               lattice_distribution, lattice_gate, meet,
                               project, setval_targets, superset_targets,
                               truth_superset_idx)
from tools.ldt_lattice import evaluate_lattice  # noqa: E402
from tools.ldt_train import (Featurizer, evaluate, forward,  # noqa: E402
                             init_params, renormalize_gated, rows_xy,
                             subset_rows, train_model, train_model_gated)

_FOUR_OUTCOMES = {frozenset({"illegal_unknown_verb"}),
                  frozenset({"illegal_unknown_target"}),
                  frozenset({"illegal_dry_pool"}),
                  frozenset({"legal_no_gain", "legal_gain"})}


def _rows(n: int = 150, seed: int = 23):
    train, val = generate(n, seed=seed, val_frac=0.1)
    return train + val


# ------------------------------------------------------------ lattice shape ----
def test_lattice_shape_and_descent_chain() -> None:
    elements = all_elements()
    assert len(elements) == 32 and len(set(elements)) == 32
    assert BOTTOM in elements and frozenset(LABELS) in elements

    s1, s2 = frozenset(LABELS[:2]), frozenset(LABELS[1:4])
    assert join(s1, s2) == s1 | s2
    assert meet(s1, s2) == s1 & s2
    for s in elements:                       # BOTTOM is the identity laws
        assert meet(s, BOTTOM) == BOTTOM
        assert join(s, BOTTOM) == s

    rows = _rows(80, seed=5)
    seen_full_top = False
    for r in rows:
        for depth in ("legality", "full"):
            chain = cascade_chain(r["graph"], r["verb"], r["target"], depth)
            assert chain[0] == frozenset(LABELS)      # level 0 = full set
            seen_full_top = True
            for a, b in zip(chain, chain[1:]):        # strictly shrinking
                assert b < a
            if depth == "full":
                assert len(chain[-1]) == 1            # oracle rung: singleton
            else:
                assert chain[-1] in _FOUR_OUTCOMES
        assert r["label"] in feasible_set(r["graph"], r["verb"], r["target"])
    assert seen_full_top


# -------------------------------------------------------- truth feasibility ----
def test_true_label_always_feasible() -> None:
    rows = _rows(150, seed=23)
    assert len(rows) >= 130
    outcomes = set()
    for r in rows:
        f = feasible_set(r["graph"], r["verb"], r["target"])
        assert r["label"] in f, f"truth {r['label']} excluded by {f}"
        outcomes.add(f)
    assert outcomes == _FOUR_OUTCOMES


# ------------------------------------------------------- projection law -------
def test_projection_never_violates_monotonicity() -> None:
    """Synthetic, deterministic: pinned probabilities over every feasible
    shape; the shrink-only laws must hold row by row at every threshold,
    and soundness/coverage must move in the legal directions."""
    rng = np.random.default_rng(99)
    n = 400
    shapes = sorted(_FOUR_OUTCOMES, key=sorted)
    feasibles, y = [], np.empty(n, dtype=np.int64)
    for i in range(n):
        f = shapes[i % len(shapes)]
        feasibles.append(f)
        lab = sorted(f)[rng.integers(len(f))]
        y[i] = LABELS.index(lab)
    raw = rng.random((n, len(LABELS))) + 0.05
    probs = raw / raw.sum(axis=1, keepdims=True)
    mask = feasible_mask(feasibles)

    for tau in (0.2, 0.35, 0.5, 0.7):
        pred_raw = probs.argmax(axis=1)
        pmax = probs.max(axis=1)
        answered_raw = pmax >= tau
        for i in range(n):
            cand, conf = project(probs[i], feasibles[i], tau, mode="strict")
            assert conf <= pmax[i] + 1e-12          # masking never raises conf
            if not cand:                            # BOTTOM is always legal
                continue
            (lab,) = cand
            assert lab in feasibles[i]              # never answer outside F
            if answered_raw[i] and LABELS[pred_raw[i]] in feasibles[i]:
                # feasible raw argmax must be kept verbatim
                assert lab == LABELS[pred_raw[i]]
            if cand:
                assert answered_raw[i]              # shrink-only: no new answers

        # raw metrics straight from the arrays (ldt_train.evaluate takes
        # params; here the arrays are the source of truth)
        corr_r = (pred_raw == y) & answered_raw
        cov_raw = answered_raw.sum() / n
        lat = evaluate_lattice(probs, feasibles, y, tau, mode="strict")
        assert lat["answered_infeasible"] == 0
        assert lat["answered_not_raw"] == 0
        assert lat["coverage"] <= cov_raw + 1e-12
        if lat["answered"] and answered_raw.any():   # soundness needs answers
            sound_raw = corr_r.sum() / answered_raw.sum()
            assert lat["soundness"] >= sound_raw - 1e-12


def test_projection_flips_or_kills_only_wrong_answers() -> None:
    """The mechanism of the soundness law, row by row: a raw answer whose
    argmax is infeasible was WRONG (truth is always feasible); after
    projection that row either abstains or answers inside F — it can
    never stay wrong-outside-F."""
    rng = np.random.default_rng(7)
    shapes = sorted(_FOUR_OUTCOMES, key=sorted)
    tau = 0.4
    for i in range(200):
        f = shapes[i % len(shapes)]
        feas = list(f)
        truth = feas[rng.integers(len(feas))]
        y = LABELS.index(truth)
        p = rng.random(len(LABELS)) + 0.05
        p /= p.sum()
        cand, conf = project(p, f, tau, mode="strict")
        if p.max() >= tau and LABELS[int(p.argmax())] not in f:
            # raw answered infeasibly -> raw was wrong; projection must
            # not reproduce that label
            if cand:
                (lab,) = cand
                assert lab != LABELS[int(p.argmax())]


# ------------------------------------------------- real tiny trained MLP ------
def test_soundness_improves_vs_raw_on_trained_mlp() -> None:
    train_rows, val_rows = generate(320, seed=41, val_frac=0.1)
    train_rows, val_rows = train_rows[:280], val_rows[:30]
    fe = Featurizer().fit(train_rows)
    Xtr, ytr = rows_xy(train_rows, fe)
    Xva, yva = rows_xy(val_rows, fe)
    params, _ = train_model(Xtr, ytr, hidden=[24], epochs=3, lr=2e-3,
                            batch=32, seed=13)
    probs, _ = forward(params, Xva)
    feasibles = [feasible_set(r["graph"], r["verb"], r["target"])
                 for r in val_rows]

    # pick the first threshold where raw actually answers enough to make
    # the comparison non-vacuous
    tau = None
    for t in (0.7, 0.5, 0.35, 0.25):
        m = evaluate(params, Xva, yva, threshold=t)
        if m["coverage"] >= 0.5:
            tau = t
            break
    assert tau is not None, "tiny MLP never reached usable coverage"

    raw = evaluate(params, Xva, yva, threshold=tau)
    lat = evaluate_lattice(probs, feasibles, yva, tau, mode="strict")
    assert lat["answered_infeasible"] == 0
    assert lat["answered_not_raw"] == 0
    assert lat["coverage"] <= raw["coverage"] + 1e-12
    assert lat["soundness"] >= raw["soundness"] - 1e-9


# ------------------------------------------------- lattice distribution -------
def test_lattice_distribution_support_and_mass() -> None:
    rng = np.random.default_rng(3)
    for f in _FOUR_OUTCOMES:
        p = rng.random(len(LABELS)) + 0.05
        p /= p.sum()
        d = lattice_distribution(p, f)
        assert set(d) == set(f)
        np.testing.assert_allclose(sum(d.values()), 1.0, atol=1e-9)
        for lab in d:
            assert d[lab] == 0.0 or lab in f
    assert lattice_distribution(p, BOTTOM) == {}


# ------------------------------------------------- AH8 v1: gate + targets ------
def test_lattice_gate_is_exact_subset_mask() -> None:
    rows = _rows(150, seed=31)
    feas = [feasible_set(r["graph"], r["verb"], r["target"]) for r in rows]
    gate = lattice_gate(feas)
    assert gate.shape == (len(rows), 32)
    for i, f in enumerate(feas):
        for e, elem in enumerate(_ELEMENTS):
            assert gate[i, e] == (elem <= f)   # iff subset — the exact mask
        assert gate[i, BOTTOM_IDX]             # abstain rides the lattice
        assert gate[i].sum() == 2 ** len(f)    # 2^|F| elements survive
    # tier outcomes gate to exactly 2 on ({tier}, BOTTOM); legal pair to 4
    tier = next(f for f in feas if len(f) == 1)
    legal = next(f for f in feas if len(f) == 2)
    i_t, i_l = feas.index(tier), feas.index(legal)
    on_t = {_ELEMENTS[e] for e in np.flatnonzero(gate[i_t])}
    on_l = {_ELEMENTS[e] for e in np.flatnonzero(gate[i_l])}
    assert on_t == {tier, BOTTOM}
    assert on_l == {legal, frozenset({sorted(legal)[0]}),
                    frozenset({sorted(legal)[1]}), BOTTOM}


def test_setval_targets_are_gated_on_singletons() -> None:
    rows = _rows(150, seed=17)
    feas = [feasible_set(r["graph"], r["verb"], r["target"]) for r in rows]
    y = np.array([LABELS.index(r["label"]) for r in rows], dtype=np.int64)
    t = setval_targets(y)
    assert t.shape == y.shape
    for i in range(len(y)):
        assert _ELEMENTS[t[i]] == frozenset({LABELS[y[i]]})  # {y} position
        # truth-in-gate law: the target element is feasible on its row
        assert lattice_gate([feas[i]])[0, t[i]]


# ------------------------------------------------- AH8 v1: renorm + training ---
def test_renormalize_gated_math() -> None:
    rng = np.random.default_rng(11)
    probs = rng.random((50, 32)) + 0.01
    probs /= probs.sum(axis=1, keepdims=True)
    feas = [sorted(_FOUR_OUTCOMES, key=sorted)[i % 4] for i in range(50)]
    gate = lattice_gate(feas).astype(np.float32)
    ren = renormalize_gated(probs, gate)
    np.testing.assert_allclose(ren.sum(axis=1), 1.0, atol=1e-6)
    # gated-out columns exactly zero; gated-in ratios preserved
    np.testing.assert_array_equal(ren[gate == 0.0], 0.0)
    i = 6
    on = gate[i] == 1.0
    ratios = ren[i, on] / ren[i, on][0]
    ref = probs[i, on] / probs[i, on][0]
    np.testing.assert_allclose(ratios, ref, atol=1e-5)
    # all-ones gate is the identity resum
    ident = renormalize_gated(probs, np.ones_like(gate))
    np.testing.assert_allclose(ident, probs / probs.sum(axis=1, keepdims=True),
                               atol=1e-6)


def test_train_model_gated_open_gate_reproduces_raw() -> None:
    """The generalization law: gate of all ones + n_out=5 + y_elem=y is
    train_model's exact recipe (same rng streams, same Adam, same l2)."""
    train_rows = _rows(120, seed=8)[:100]
    fe = Featurizer().fit(train_rows)
    X, y = rows_xy(train_rows, fe)
    gate = np.ones((len(y), len(LABELS)), dtype=bool)
    p_raw, _ = train_model(X, y, [16], 2, 1e-3, 32, seed=13, l2=1e-4)
    p_gated, _ = train_model_gated(X, y, len(LABELS), gate, [16], 2, 1e-3,
                                   32, seed=13, l2=1e-4)
    for k in p_raw:
        np.testing.assert_allclose(p_gated[k], p_raw[k], atol=1e-6,
                                   err_msg=f"open gate drifted on {k}")


def test_train_model_gated_zero_gradient_outside_gate() -> None:
    """l2=0 + a gate locking columns off => those output weights stay
    BITWISE at init: the gate is self-enforcing (gated-out p_j = 0 and
    target 0, so dL/dz_j = 0 — capacity never leaks to impossible atoms)."""
    train_rows = _rows(120, seed=9)[:100]
    fe = Featurizer().fit(train_rows)
    X, y = rows_xy(train_rows, fe)
    n_out = 6
    keep = [0, 2, 4]                          # only these columns learnable
    gate = np.zeros((len(y), n_out), dtype=bool)
    gate[:, keep] = True
    y_elem = np.array([keep[i % len(keep)] for i in range(len(y))],
                      dtype=np.int64)
    params, _ = train_model_gated(X, y_elem, n_out, gate, [16, 8], 3, 1e-3,
                                  32, seed=5, l2=0.0)
    init = init_params(fe.dim, [16, 8], n_out, 5)
    off = [j for j in range(n_out) if j not in keep]
    np.testing.assert_array_equal(params["W2"][:, off], init["W2"][:, off])
    np.testing.assert_array_equal(params["b2"][off], init["b2"][off])


# ------------------------------------------------- AH8 v1: set-valued eval -----
def test_evaluate_setval_contract_on_synthetic_probs() -> None:
    """Hand-computed reference vs evaluate_setval: answered = confident
    singleton commits (correct iff == {y}), hedges reported separately,
    answered_infeasible == 0 by construction."""
    rng = np.random.default_rng(21)
    shapes = sorted(_FOUR_OUTCOMES, key=sorted)
    n, tau = 300, 0.5
    feas = [shapes[i % 4] for i in range(n)]
    y = np.empty(n, dtype=np.int64)
    for i, f in enumerate(feas):
        labs = sorted(f)
        y[i] = LABELS.index(labs[rng.integers(len(labs))])
    gate = lattice_gate(feas)
    logits = rng.random((n, 32)) + 0.05
    probs = np.exp(logits - logits.max(axis=1, keepdims=True))
    probs /= probs.sum(axis=1, keepdims=True)
    # every 4th row: dominant mass on the legal-pair element => a hedge row
    legal = frozenset({"legal_no_gain", "legal_gain"})
    pair_idx = _ELEM_IDX[legal]
    for i in range(3, n, 4):
        probs[i] = 1e-6
        probs[i, pair_idx] = 1.0

    m = evaluate_setval(probs, feas, y, tau)
    ren = renormalize_gated(probs, gate)
    elem = ren.argmax(axis=1)
    conf = ren.max(axis=1)

    ans = corr = hedge = hedge_t = 0
    for i in range(n):
        e = _ELEMENTS[elem[i]]
        assert e <= feas[i]                     # argmax never leaves F
        singleton = len(e) == 1
        if conf[i] >= tau and singleton:
            ans += 1
            corr += int(e == frozenset({LABELS[int(y[i])]}))
        elif conf[i] >= tau and e:
            hedge += 1
            hedge_t += int(LABELS[int(y[i])] in e)
    assert m["answered"] == ans and m["answered_correct"] == corr
    assert m["answered_wrong"] == ans - corr
    assert m["answered_infeasible"] == 0        # the pinned by-construction law
    assert hedge > 0 and ans > 0                # the reference is non-vacuous
    assert m["hedged"] == hedge
    np.testing.assert_allclose(m["hedged_contains_truth"], hedge_t / hedge)
    np.testing.assert_allclose(m["coverage"], ans / n)
    np.testing.assert_allclose(m["soundness"], corr / ans)
    assert m["mode"] == "v1-setval-renorm"


def test_evaluate_setval_hedges_are_not_answers() -> None:
    """A high-confidence legal-pair prediction must NOT count as answered
    (it decides nothing) — it is a hedge, carrying its contains-truth rate."""
    legal = frozenset({"legal_no_gain", "legal_gain"})
    feas = [legal] * 4
    y = np.array([LABELS.index("legal_gain")] * 2
                 + [LABELS.index("legal_no_gain")] * 2, dtype=np.int64)
    probs = np.full((4, 32), 1e-6)
    pair_idx = _ELEM_IDX[legal]
    probs[:, pair_idx] = 1.0                   # all mass on the 2-element set
    m = evaluate_setval(probs, feas, y, 0.7)
    assert m["answered"] == 0 and m["coverage"] == 0.0
    assert m["hedged"] == 4
    np.testing.assert_allclose(m["hedged_contains_truth"], 1.0)
    assert m["answered_infeasible"] == 0


# ------------------------------------------------- AH8 v1: data subsets --------
def test_subset_rows_parity_and_determinism() -> None:
    rows = _rows(200, seed=44)
    full = subset_rows(rows, 1.0)
    assert len(full) == len(rows) and full == rows     # unchanged, byte-parity
    assert full is not rows                            # a copy, not an alias
    a = subset_rows(rows, 0.5)
    b = subset_rows(rows, 0.5)
    assert a == b                                      # deterministic
    assert len(a) == round(0.5 * len(rows))
    assert set(id(r) for r in a) <= set(id(r) for r in rows)   # subset
    assert [rows.index(r) for r in a] == sorted(rows.index(r) for r in a)
    q = subset_rows(rows, 0.25)
    assert len(q) == round(0.25 * len(rows))


# ------------------------------------------- IMP7 v2: superset-target laws -----
def test_truth_superset_idx_laws() -> None:
    # legal-pair row: the ONLY gated truth-containing strict superset is F
    # itself (the pair), so smallest == sampled == F on this dataset
    legal = frozenset({"legal_no_gain", "legal_gain"})
    for lab in sorted(legal):
        idx = truth_superset_idx(LABELS.index(lab), legal)
        assert _ELEMENTS[idx] == legal                 # the pair itself
        assert frozenset({lab}) < _ELEMENTS[idx]       # strictly contains truth
        assert _ELEMENTS[idx] <= legal                 # and stays inside F
    # illegal-tier row: F = {tier} gates only {tier} and BOTTOM — no strict
    # truth superset exists -> -1 (that row is NOT eligible for hedging)
    for tier in ("illegal_unknown_verb", "illegal_unknown_target",
                 "illegal_dry_pool"):
        assert truth_superset_idx(LABELS.index(tier), frozenset({tier})) == -1


def test_superset_targets_grid_laws() -> None:
    rows = _rows(300, seed=63)
    feas = [feasible_set(r["graph"], r["verb"], r["target"]) for r in rows]
    y = np.array([LABELS.index(r["label"]) for r in rows], dtype=np.int64)
    gate = lattice_gate(feas)
    sup_idx = np.array([truth_superset_idx(int(yy), f)
                        for yy, f in zip(y, feas)], dtype=np.int64)
    eligible = sup_idx >= 0
    assert eligible.any() and (~eligible).any()       # both populations exist
    base = setval_targets(y)

    # frac=0.0: bit-identical v1 targets (run_v2's parity arm, machine check)
    t0, st0 = superset_targets(y, feas, 0.0, seed=13, sup_idx=sup_idx)
    np.testing.assert_array_equal(t0, base)
    assert st0["n_switched"] == 0
    assert st0["n_eligible"] == int(eligible.sum())

    # frac=1.0: every eligible row switches to its superset (F itself for
    # the legal pair), ineligible rows keep the singleton; all targets on-gate
    t1, st1 = superset_targets(y, feas, 1.0, seed=13, sup_idx=sup_idx)
    assert st1["n_switched"] == st1["n_eligible"] == int(eligible.sum())
    for i in range(len(y)):
        if eligible[i]:
            assert _ELEMENTS[t1[i]] == feas[i]
            assert t1[i] != base[i]                   # a real switch happened
        else:
            assert t1[i] == base[i]
    assert gate[np.arange(len(t1)), t1].all()         # truth-in-gate law, v2

    # same seed -> deterministic; switched sets NESTED in frac (one rng
    # stream, thresholded per row: 0.25-switched ⊆ 0.75-switched)
    tm, stm = superset_targets(y, feas, 0.25, seed=13, sup_idx=sup_idx)
    th, sth = superset_targets(y, feas, 0.75, seed=13, sup_idx=sup_idx)
    td, _ = superset_targets(y, feas, 0.25, seed=13, sup_idx=sup_idx)
    np.testing.assert_array_equal(tm, td)
    assert stm["n_switched"] <= sth["n_switched"] <= st1["n_switched"]
    sw_m, sw_h = tm != base, th != base
    assert int((sw_m & ~sw_h).sum()) == 0
    assert int((sw_h & ~eligible).sum()) == 0         # never an ineligible switch

    # out-of-range frac raises (the knob is a probability)
    for bad in (-0.1, 1.5):
        try:
            superset_targets(y, feas, bad, seed=13)
            raise AssertionError(f"frac={bad} must raise ValueError")
        except ValueError:
            pass
