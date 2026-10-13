"""ldt_lattice — V7: the LDT candidate-set lattice, v0 post-hoc projection.

Mickey17 W3K lane (2026-09-30). The rung after Z13's floor (plain MLP,
val accuracy 0.8545 / soundness 0.8830 @tau=0.7, models/legality_v0.npz):
the LATTICE is what makes LDT special — legality by CONSTRUCTION instead
of by confidence threshold alone.

The lattice (candidate-set semantics over the legality dataset's 5-way
label set, manifest order from tools/legality_dataset.py):

  elements   all 32 subsets of the 5 labels, ordered by subset inclusion
             (the powerset); JOIN = union, MEET = intersection.
  BOTTOM     the empty candidate set = ABSTAIN. The abstain head rides
             the lattice: refusing to answer IS a lattice element, not an
             exception bolted on the side.
  descent    a sample descends the lattice as Y10's constraint cascade
             (tools/legality_propagator.py — reused verbatim, not
             re-derived) eliminates candidates, one constraint per level:

               level 0  {unknown_verb, unknown_target, dry_pool,
                         no_gain, gain}            nothing consulted
               level 1  unknown_verb?  fires -> {illegal_unknown_verb}
                         passes -> drop it         (4 candidates left)
               level 2  unknown_target? fires -> {illegal_unknown_target}
                         passes -> drop it         (3 left)
               level 3  dry_pool?      fires -> {illegal_dry_pool}
                         passes -> drop it         (the legal pair left)
               level 4  crown physics (depth="full"): {legal_gain} xor
                         {legal_no_gain}

             Every step strictly shrinks the candidate set, so the descent
             is a chain under subset inclusion — that IS the "powerset
             ordered by the constraint propagation". Level 4 makes the
             lattice an oracle (Y10 is exact), so the v0 projection runs
             to level 3 only: legality is by construction, the crown
             physics stays the MODEL's job. That is the whole experiment.

v0 projection (post-hoc on Z13's logits — no end-to-end training yet):
the MLP's 5-way softmax is a distribution over the five SINGLETON
lattice elements. The projection conditions it on the sample's feasible
set F (the cascade's verdict as a candidate set): mass on labels outside
F is structurally impossible and is masked to zero.

  strict mode (primary): confidence = masked max, NOT renormalized. The
  model pays for every unit of mass wasted on impossible labels, so the
  projection only ever SHRINKS the answer set. Law (pinned by
  tests/test_ldt_lattice.py, and the reason this file exists): at every
  threshold, strict soundness >= raw soundness and strict coverage <=
  raw coverage. Proof sketch: masked max <= raw max, so every strict
  answer was already a raw answer; a raw answer whose argmax lay outside
  F was necessarily WRONG (the true label is always in F), and it either
  flips to the best feasible label or falls to BOTTOM — wrong answers
  are the only thing the projection removes.
  renorm mode (v1 preview): confidence renormalized inside F — answers
  MORE rows than raw (the denominator shrinks); soundness may move
  either way, reported so the end-to-end design sees the tradeoff.

v1 learned concept layer (AH8, 2026-09-30 — AE2's steal, built): a model
with a SET-VALUED head — logits over all 32 lattice elements, not just
the 5 singletons — TRAINED UNDER the exact lattice mask: gate[i, e] iff
element e is a subset of F_i, applied to the softmax so renormalization
happens INSIDE training (ldt_train.train_model_gated +
ldt_train.renormalize_gated, the one op shared with inference). Target =
the singleton of the true label (its lattice position). Gated-out
elements carry exactly zero gradient, so capacity is never spent
separating structurally impossible atoms — renorm conditioning is
learned, not applied. Inference: softmax over masked logits ->
renormalize (renorm mode) -> the argmax ELEMENT is the answer; DECISION
semantics keep the V7 bar comparable (answered = confident singleton
commit, hedge sets and BOTTOM = abstention, counted separately).

v2 superset-target training (IMP7, 2026-09-30 — AH8's named untested
lever, its falsifier narrowed the v1 loss to "targets never taught the
set-valued half of the head"): a fraction of training rows get as target
the SMALLEST truth-containing lattice SUPERSET of {y} inside the gate —
for a legal-pair row that is F itself (the honest hedge); an illegal-tier
row has no gated truth superset, so it keeps the singleton and is not
eligible. The knob is the fraction of ELIGIBLE rows switched (a literal
fraction-of-all-rows knob saturates at |legal|/n ~= 0.38 and would make
the 0.5/0.75/1.0 grid points coincide). "Smallest" and "sampled" coincide
on this dataset: the legal pair's only gated truth-containing strict
superset IS the pair. INFERENCE IS UNCHANGED from v1 (masked softmax ->
renormalize -> argmax element -> evaluate_setval decision semantics) —
only the target distribution moved. In this dataset every hedge contains
the truth BY CONSTRUCTION (the only non-singleton gateable element is
the legal pair, and the truth always survives the descent), so a hedge
never lies — it only declines to decide.

CLI: `--v1` runs the AH8 experiment — raw / renorm / v1-setval at
--fractions (default 1.0,0.5,0.25) of the train split, same val split
and tau as V7, frozen-Z13 reproduction check, saved v1 model. `--v2`
runs the IMP7 experiment: the same arms plus the superset-fraction grid
(--sup-fracs) at each train fraction; the v1 arm IS sup-frac 0.0 (same
seeds, same rng streams — parity with the AH8 receipt's numbers is a
machine check, not an assumption). Without --v1/--v2: load
models/legality_v0.npz, featurize the val split (the Featurizer's
train-fit vocabularies are frozen inside the npz), project, and print
raw vs projected soundness/coverage at the saved threshold plus a sweep.
$0, stdlib+numpy, deterministic (no wall clock, no rng).
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.ldt_train import (LABELS, Featurizer,  # noqa: E402
                             evaluate as raw_evaluate, forward, load_jsonl,
                             load_npz, renormalize_gated, rows_xy, save_npz,
                             subset_rows, train_model, train_model_gated)
from tools.legality_propagator import (crown_gain, dry_pool,  # noqa: E402
                                       unknown_target, unknown_verb)

# BOTTOM of the lattice: the empty candidate set = the abstain answer.
BOTTOM: frozenset[str] = frozenset()
TOP: frozenset[str] = frozenset(LABELS)

_ILLEGAL_SINGLETON = {"illegal_unknown_verb": frozenset({"illegal_unknown_verb"}),
                      "illegal_unknown_target": frozenset({"illegal_unknown_target"}),
                      "illegal_dry_pool": frozenset({"illegal_dry_pool"})}


# ---------------------------------------------------------- lattice order ----
def join(a: frozenset[str], b: frozenset[str]) -> frozenset[str]:
    """Lattice join: least upper bound under subset inclusion = union."""
    return a | b


def meet(a: frozenset[str], b: frozenset[str]) -> frozenset[str]:
    """Lattice meet: greatest lower bound under subset inclusion = intersection."""
    return a & b


def all_elements() -> list[frozenset[str]]:
    """All 32 lattice elements (every subset of the 5-way label set)."""
    out = [BOTTOM]
    for r in range(1, len(LABELS) + 1):
        out.extend(frozenset(c) for c in itertools.combinations(LABELS, r))
    return out


# ------------------------------------------------------------ the descent ----
def cascade_chain(spec: dict[str, Any], verb: str, target: str,
                  depth: str = "legality") -> list[frozenset[str]]:
    """The sample's descent through the lattice: level 0 (full set), then
    one strictly-smaller candidate set per constraint consulted, in Y10's
    elif order. A constraint that FIRES collapses the set to its illegal
    singleton and ends the descent (later constraints eliminate nothing —
    the verdict is already determined, exactly tools/legality_propagator
    .propagate's elif cascade). depth="full" consults level 4 (crown
    physics, the oracle rung); depth="legality" stops at the legal pair."""
    chain = [TOP]
    if unknown_verb(verb):
        return chain + [_ILLEGAL_SINGLETON["illegal_unknown_verb"]]
    cur = TOP - {"illegal_unknown_verb"}
    chain.append(cur)
    if unknown_target(spec, verb, target):
        return chain + [_ILLEGAL_SINGLETON["illegal_unknown_target"]]
    cur = cur - {"illegal_unknown_target"}
    chain.append(cur)
    if dry_pool(spec, verb, target):
        return chain + [_ILLEGAL_SINGLETON["illegal_dry_pool"]]
    cur = cur - {"illegal_dry_pool"}
    chain.append(cur)                                   # the legal pair
    if depth == "full":
        gain = crown_gain(spec, verb, target)
        chain.append(frozenset({"legal_gain" if gain else "legal_no_gain"}))
    elif depth != "legality":
        raise ValueError(f"depth must be 'legality' or 'full', got {depth!r}")
    return chain


def feasible_set(spec: dict[str, Any], verb: str, target: str,
                 depth: str = "legality") -> frozenset[str]:
    """The bottom of the sample's descent: every label the constraints
    have not eliminated. The dataset's own label is ALWAYS in it (pinned
    by tests), so the projection can kill wrong answers, never right
    ones."""
    return cascade_chain(spec, verb, target, depth=depth)[-1]


def feasible_mask(feasibles: list[frozenset[str]]) -> np.ndarray:
    """(n, 5) boolean matrix: mask[i, j] iff LABELS[j] is feasible for row i."""
    mask = np.zeros((len(feasibles), len(LABELS)), dtype=bool)
    for i, fs in enumerate(feasibles):
        for j, lab in enumerate(LABELS):
            mask[i, j] = lab in fs
    return mask


# ------------------------------------------------------------- projection ----
def project(probs: np.ndarray, feasible: frozenset[str], threshold: float,
            mode: str = "strict") -> tuple[frozenset[str], float]:
    """One row's post-hoc lattice projection.

    Returns (candidate_set, confidence): the answer is the argmax label
    inside `feasible` as the singleton lattice element, or BOTTOM (the
    empty candidate set = ABSTAIN) when the masked confidence is below
    threshold. strict mode reads the masked max as-is (shrink-only law);
    renorm divides by the feasible mass (can re-answer raw abstains)."""
    if mode not in ("strict", "renorm"):
        raise ValueError(f"mode must be 'strict' or 'renorm', got {mode!r}")
    idx = [j for j, lab in enumerate(LABELS) if lab in feasible]
    if not idx:
        return BOTTOM, 0.0
    masked = probs[idx]
    best = idx[int(np.argmax(masked))]
    conf = float(masked.max())
    if mode == "renorm":
        conf = conf / float(masked.sum())
    if conf >= threshold:
        return frozenset({LABELS[best]}), conf
    return BOTTOM, conf


def lattice_distribution(probs: np.ndarray,
                         feasible: frozenset[str]) -> dict[str, float]:
    """v0 lift of the 5-way softmax to a distribution over lattice
    elements: the conditional distribution over the feasible SINGLETON
    elements (the 27 non-singleton subsets carry zero mass at v0 —
    predicting genuinely set-valued candidates is the end-to-end v1
    step). Empty feasible set -> empty distribution (BOTTOM is certain)."""
    idx = [j for j, lab in enumerate(LABELS) if lab in feasible]
    if not idx:
        return {}
    masked = np.array([probs[j] for j in idx], dtype=np.float64)
    total = masked.sum()
    if total <= 0.0:
        return {LABELS[j]: 0.0 for j in idx}
    return {LABELS[j]: float(m / total) for j, m in zip(idx, masked)}


# ------------------------------------------- AH8: v1 learned concept layer ----
# AE2's steal, built (2026-09-30): a model that outputs a distribution over
# ALL 32 lattice elements (set-valued head) TRAINED UNDER the exact lattice
# mask — the same gate the v0 projection applies post-hoc becomes the
# differentiable gate the gradients live inside. Renorm conditioning is
# learned instead of applied: training optimizes the renormalized-within-
# mask quantity that renorm inference reads (one shared op,
# ldt_train.renormalize_gated). The element ordering is all_elements()
# (BOTTOM first, then subsets by size) — fixed forever by this index map.
_ELEMENTS: list[frozenset[str]] = all_elements()
_ELEM_IDX: dict[frozenset[str], int] = {e: i for i, e in enumerate(_ELEMENTS)}
BOTTOM_IDX: int = _ELEM_IDX[BOTTOM]
# the 5 lattice ATOMS (label singletons) in LABELS order
SINGLETON_IDX: np.ndarray = np.array(
    [_ELEM_IDX[frozenset({lab})] for lab in LABELS], dtype=np.int64)
# which elements are singleton commits (a decision), vs hedged sets vs BOTTOM
_ELEM_IS_SINGLETON = np.array(
    [len(e) == 1 for e in _ELEMENTS], dtype=bool)
_ELEM_SIZE = np.array([len(e) for e in _ELEMENTS], dtype=np.int64)


def lattice_gate(feasibles: list[frozenset[str]]) -> np.ndarray:
    """(n, 32) boolean: gate[i, e] iff _ELEMENTS[e] <= feasibles[i] — the
    EXACT lattice mask. A candidate set carrying any atom outside F is
    structurally impossible (no renormalization can make it an answer), so
    its column is gated off and its gradient is exactly zero. BOTTOM (the
    empty set) is a subset of every F: the abstain head is gated ON for
    every row — abstention rides the lattice, exactly like in v0. Row
    counts: an illegal tier (|F|=1) leaves 2 elements on ({tier}, BOTTOM);
    the legal pair (|F|=2) leaves 4 on — 2**|F| in general."""
    mask = np.zeros((len(feasibles), len(_ELEMENTS)), dtype=bool)
    for i, fs in enumerate(feasibles):
        for e, elem in enumerate(_ELEMENTS):
            mask[i, e] = elem <= fs
    return mask


def setval_targets(y: np.ndarray) -> np.ndarray:
    """Training target: the element index of the true label's lattice
    position = the singleton {y}. Always gated ON (the truth is always
    feasible — pinned by tests — so {y} <= F row by row)."""
    return SINGLETON_IDX[y]


def truth_superset_idx(y: int, feasible: frozenset[str]) -> int:
    """IMP7 v2: index of the SMALLEST gated element strictly containing
    {y} ({y} < e <= F), first-in-element-order on size ties; -1 when none
    exists (an illegal-tier row gates only {tier} and BOTTOM, so the
    smallest truth-containing superset degenerates to the singleton —
    that row is NOT eligible for hedge teaching). For a legal-pair row
    the answer is F itself: its only gated truth-containing strict
    superset IS the pair, so "smallest" and "sampled" coincide here."""
    truth = frozenset({LABELS[int(y)]})
    best, best_size = -1, 1 << 30
    for e, elem in enumerate(_ELEMENTS):
        if truth < elem <= feasible and len(elem) < best_size:
            best, best_size = e, len(elem)
    return best


def superset_targets(y: np.ndarray, feasibles: list[frozenset[str]],
                     frac: float, seed: int, sup_idx: np.ndarray | None = None,
                     ) -> tuple[np.ndarray, dict[str, int]]:
    """IMP7 v2 training targets: setval_targets (the v1 singletons) with a
    `frac` fraction of ELIGIBLE rows switched to their smallest truth
    superset. One fresh rng stream (seed+2) so v1's init/shuffle streams
    are untouched; frac=0.0 returns targets identical to v1's (parity
    law, machine-checked in run_v2). Every target is gated ON by
    construction: {y} <= F always, and the superset is chosen <= F.
    Returns (targets, stats) with stats naming eligible/switched rows."""
    if not 0.0 <= frac <= 1.0:
        raise ValueError(f"superset frac must be in [0, 1], got {frac!r}")
    if sup_idx is None:
        sup_idx = np.array([truth_superset_idx(int(yy), f)
                            for yy, f in zip(y, feasibles)], dtype=np.int64)
    t = setval_targets(y)
    rng = np.random.default_rng(seed + 2)
    eligible = sup_idx >= 0
    switch = eligible & (rng.random(len(y)) < frac)
    t[switch] = sup_idx[switch]
    return t, {"frac": float(frac), "n_eligible": int(eligible.sum()),
               "n_switched": int(switch.sum())}


def evaluate_setval(probs32: np.ndarray, feasibles: list[frozenset[str]],
                    y: np.ndarray, threshold: float) -> dict[str, Any]:
    """v1 inference + eval on the V7 contract. probs32 is the model's
    softmax over the 32 elements; the gate renormalizes it inside F
    (renorm mode, learned). The answer is the argmax element S*.

    DECISION semantics (the V7-comparable bar): a row is ANSWERED iff
    conf >= threshold AND S* is a singleton (a commit); correct iff the
    singleton is exactly {y}. A non-singleton S* above threshold (e.g.
    the legal pair when crown physics is uncertain) is a HEDGE: it does
    not decide the row, so it counts as abstention — reported separately
    with its contains-truth rate so honest hedging is visible without
    inflating the bar. BOTTOM or conf < threshold = abstain.

    Tripwire answered_infeasible: singleton commits outside F — must be
    0 by construction (the gate). This is the "predicted set never
    contains a truth-candidate outside the feasible set" law, pinned."""
    gate = lattice_gate(feasibles)
    renorm = renormalize_gated(probs32, gate)
    elem = renorm.argmax(axis=1)
    conf = renorm.max(axis=1)

    is_singleton = _ELEM_IS_SINGLETON[elem]
    answered = (conf >= threshold) & is_singleton
    correct = answered & (elem == SINGLETON_IDX[y])

    # by-construction law, verified not assumed (a >0 here is a bug in the
    # gate, an eval built on it, or a reload that dropped the mask)
    infeasible = 0
    for i in range(len(y)):
        if answered[i] and not (_ELEMENTS[elem[i]] <= feasibles[i]):
            infeasible += 1

    hedged = (conf >= threshold) & (elem != BOTTOM_IDX) & ~is_singleton
    hedge_truth = 0
    for i in range(len(y)):
        if hedged[i] and LABELS[int(y[i])] in _ELEMENTS[elem[i]]:
            hedge_truth += 1

    per_class = {}
    for c, name in enumerate(LABELS):
        m = y == c
        supp = int(m.sum())
        per_class[name] = {
            "support": supp,
            "recall": float((correct & m).sum() / supp) if supp else float("nan"),
            "answered_frac": float((answered[m]).mean()) if supp else float("nan"),
        }
    n_ans = int(answered.sum())
    n_corr = int(correct.sum())
    n_hedge = int(hedged.sum())
    return {
        "n": len(y), "threshold": threshold, "mode": "v1-setval-renorm",
        "coverage": n_ans / len(y) if len(y) else 0.0,
        "answered": n_ans, "answered_correct": n_corr,
        "answered_wrong": n_ans - n_corr,
        "soundness": (n_corr / n_ans) if n_ans else float("nan"),
        "answered_infeasible": infeasible,
        "hedged": n_hedge,
        "hedged_contains_truth": (hedge_truth / n_hedge) if n_hedge else float("nan"),
        "argmax_bottom": int((elem == BOTTOM_IDX).sum()),
        "per_class": per_class,
    }


# ------------------------------------------------------------------ eval ----
def evaluate_lattice(probs: np.ndarray, feasibles: list[frozenset[str]],
                     y: np.ndarray, threshold: float,
                     mode: str = "strict") -> dict[str, Any]:
    """Z13's evaluate contract, lattice side. soundness/coverage are
    computed exactly like tools.ldt_train.evaluate but over the PROJECTED
    answers; two tripwires ride along and must hold by construction:
    answered_infeasible == 0 (never answer outside F) and, in strict
    mode, answered_not_raw == 0 (projection is shrink-only)."""
    mask = feasible_mask(feasibles)
    neg = np.where(mask, probs, -np.inf)
    pred = neg.argmax(axis=1)
    conf = neg.max(axis=1).astype(np.float64)
    empty = ~mask.any(axis=1)
    pred = np.where(empty, -1, pred)
    feasible_any = mask.any(axis=1)
    conf = np.where(feasible_any, conf, 0.0)
    if mode == "renorm":
        mass = (probs * mask).sum(axis=1)
        with np.errstate(invalid="ignore", divide="ignore"):
            conf = np.where(feasible_any & (mass > 0), conf / np.maximum(mass, 1e-12), 0.0)
    elif mode != "strict":
        raise ValueError(f"mode must be 'strict' or 'renorm', got {mode!r}")

    answered = (conf >= threshold) & ~empty
    pmax = probs.max(axis=1)
    correct = pred == y

    n_ans = int(answered.sum())
    n_corr = int((correct & answered).sum())
    infeasible_answered = 0
    for i in range(len(y)):
        if answered[i] and LABELS[pred[i]] not in feasibles[i]:
            infeasible_answered += 1
    answered_not_raw = int((answered & (pmax < threshold)).sum())

    per_class = {}
    for c, name in enumerate(LABELS):
        m = y == c
        supp = int(m.sum())
        per_class[name] = {
            "support": supp,
            "recall": float((correct & m).mean()) if supp else float("nan"),
            "answered_frac": float((answered[m]).mean()) if supp else float("nan"),
        }
    return {
        "n": len(y), "threshold": threshold, "mode": mode,
        "coverage": n_ans / len(y) if len(y) else 0.0,
        "answered": n_ans, "answered_correct": n_corr,
        "answered_wrong": n_ans - n_corr,
        "soundness": (n_corr / n_ans) if n_ans else float("nan"),
        "answered_infeasible": infeasible_answered,
        "answered_not_raw": answered_not_raw,
        "per_class": per_class,
    }


# ------------------------------------------------------------------- cli ----
def _elem_names() -> list[str]:
    return [",".join(sorted(e)) if e else "BOTTOM" for e in _ELEMENTS]


def _pareto(a: dict[str, Any], b: dict[str, Any]) -> str:
    """Verdict of a vs b on the (soundness, coverage) plane: BEAT means
    both >= and one >; MATCH means equal on both; LOSE otherwise."""
    sa, ca, sb, cb = a["soundness"], a["coverage"], b["soundness"], b["coverage"]
    if sa >= sb and ca >= cb and (sa > sb or ca > cb):
        return "PARETO-BEAT"
    if sa == sb and ca == cb:
        return "MATCH"
    return "LOSE" if (sa < sb and ca < cb) else "TRADE"


def run_v1(args: argparse.Namespace) -> int:
    """AH8 experiment: the full table raw / renorm / v1-setval at
    25/50/100% train data, same featurizer recipe per fraction (fit on the
    SUBSET — less data means less vocabulary too, the honest axis), same
    val split (2000 rows, V7's), same tau. Parity law: both arms of a
    fraction eat the identical subset and featurizer."""
    t0 = time.perf_counter()
    hidden = [int(h) for h in args.hidden.split(",")]
    tau = args.threshold
    train_rows = load_jsonl(args.data / "train.jsonl")
    val_rows = load_jsonl(args.data / "val.jsonl")
    train_sha = hashlib.sha256((args.data / "train.jsonl").read_bytes()).hexdigest()
    _, _, frozen_cfg = load_npz(args.model)
    frozen = frozen_cfg.get("val_metrics", {})

    val_feas = [feasible_set(r["graph"], r["verb"], r["target"])
                for r in val_rows]
    yva = np.array([LABELS.index(r["label"]) for r in val_rows], dtype=np.int64)
    truth_out = sum(1 for i, r in enumerate(val_rows)
                    if r["label"] not in val_feas[i])
    print(f"AH8 v1 set-valued concept layer — train={len(train_rows)} "
          f"val={len(val_rows)} tau={tau} hidden={hidden} "
          f"seed={args.seed} epochs={args.epochs}")
    print(f"val truth-feasibility law: labels outside F = {truth_out} (must be 0); "
          f"head = {len(_ELEMENTS)} lattice elements "
          f"(raw arm head = {len(LABELS)})")

    fracs = [float(f) for f in args.fractions.split(",")]
    results: dict[str, Any] = {"threshold": tau, "train_sha256": train_sha,
                               "frozen_z13_val": frozen, "fractions": {}}
    best_v1: dict[float, dict[str, Any]] = {}

    print(f"\n{'frac':>5} {'arm':>10} {'params':>7} {'coverage':>9} "
          f"{'soundness':>10} {'answered(c/w)':>16} {'hedge(t)':>9}")
    for frac in fracs:
        sub = subset_rows(train_rows, frac, seed=args.seed)
        fe = Featurizer().fit(sub)
        Xtr, ytr = rows_xy(sub, fe)
        Xva = fe.transform(val_rows)

        feas_tr = [feasible_set(r["graph"], r["verb"], r["target"])
                   for r in sub]
        gate_tr = lattice_gate(feas_tr)
        ttr = setval_targets(ytr)
        # truth-in-gate law: the target element is gated ON on every train row
        assert gate_tr[np.arange(len(ttr)), ttr].all(), \
            "truth singleton outside its gate — gate/target mismatch"

        raw_params, _ = train_model(Xtr, ytr, hidden, args.epochs, args.lr,
                                    args.batch, args.seed, l2=args.l2)
        raw = raw_evaluate(raw_params, Xva, yva, threshold=tau)
        probs5, _ = forward(raw_params, Xva)
        renorm = evaluate_lattice(probs5, val_feas, yva, tau, mode="renorm")

        v1_params, losses = train_model_gated(
            Xtr, ttr, len(_ELEMENTS), gate_tr, hidden, args.epochs, args.lr,
            args.batch, args.seed, l2=args.l2)
        probs32, _ = forward(v1_params, Xva)
        v1 = evaluate_setval(probs32, val_feas, yva, tau)

        n_raw = sum(v.size for v in raw_params.values())
        n_v1 = sum(v.size for v in v1_params.values())
        for name, m, npar in (("raw", raw, n_raw), ("renorm", renorm, n_raw),
                              ("v1-setval", v1, n_v1)):
            hedge = (f"{m['hedged']}({m['hedged_contains_truth']:.2f})"
                     if name == "v1-setval" else "-")
            print(f"{frac:>5.2f} {name:>10} {npar:>7} {m['coverage']:>9.4f} "
                  f"{m['soundness']:>10.4f} "
                  f"{m['answered']:>7}({m['answered_correct']}/"
                  f"{m['answered_wrong']}) {hedge:>9}")
        best_v1[frac] = v1
        results["fractions"][f"{frac:.2f}"] = {
            "n_train": len(sub), "feature_dim": fe.dim,
            "raw": {k: v for k, v in raw.items() if k != "per_class"},
            "renorm": {k: v for k, v in renorm.items() if k != "per_class"},
            "v1_setval": {k: v for k, v in v1.items() if k != "per_class"},
            "params_raw": n_raw, "params_v1": n_v1,
            "final_loss_v1": losses[-1],
        }
        if frac == max(fracs):
            out = ROOT / "models" / "ldt_v1_setval.npz"
            save_npz(out, v1_params, fe, {
                "schema": "ldt_v1_setval.npz", "train_sha256": train_sha,
                "train_fraction": frac, "n_train": len(sub),
                "hidden": hidden, "epochs": args.epochs, "lr": args.lr,
                "batch": args.batch, "seed": args.seed, "l2": args.l2,
                "threshold": tau, "n_elements": len(_ELEMENTS),
                "gate_law": "element <= feasible_set (subset mask)",
                "target_law": "singleton of true label",
                "element_order": _elem_names(),
            }, labels=_elem_names())
            print(f"saved v1@{frac:.2f}: {out} ({n_v1} weight elements)")

    # the BAR, named by machine so the receipt cannot soften it
    full = f"{max(fracs):.2f}"
    ren = results["fractions"][full]["renorm"]
    checks = {
        "v1@100 vs renorm@100": _pareto(
            results["fractions"][full]["v1_setval"], ren),
    }
    if "0.50" in results["fractions"]:
        checks["v1@50 vs renorm@100 (the 1.95x test)"] = _pareto(
            results["fractions"]["0.50"]["v1_setval"], ren)
    if frozen and "soundness" in frozen:
        drift = (results["fractions"][full]["raw"]["soundness"]
                 - frozen["soundness"])
        checks["raw@100 reproduces frozen Z13"] = (
            "yes" if abs(drift) < 1e-9 else f"NO (drift {drift:+.6f})")
    print("\nBAR checks (soundness/coverage plane, tau="
          f"{tau}): " + json.dumps(checks, sort_keys=True))
    print(f"wall: {time.perf_counter() - t0:.1f}s (budget 600s)")
    print(json.dumps(results, sort_keys=True))
    return 0


# the AH8 receipt's published v1@100 numbers (val n=2000, tau=0.7) — the
# v2 run's sup-frac-0.0 arm must reproduce them, machine-checked below
_V1_RECEIPT = {"coverage": 0.9855, "soundness": 0.9767}


def run_v2(args: argparse.Namespace) -> int:
    """IMP7 experiment: grid the superset fraction (--sup-fracs) of v2
    targets against the raw/renorm/v1 arms at each train fraction
    (--fractions). The v1 arm IS sup-frac 0.0 — same seeds, same rng
    streams — so parity with the AH8 receipt's published numbers is a
    machine check, not an assumption. THE BAR (from the IMP7 card):
    (1) Pareto-beat renorm@100 (0.9806 soundness / 0.9805 coverage), or
    (2) beat v1's coverage 0.9855 at equal-or-better soundness (0.9767).
    Best-arm selection is explicit and named; the receipt reports the
    whole grid regardless."""
    t0 = time.perf_counter()
    hidden = [int(h) for h in args.hidden.split(",")]
    tau = args.threshold
    train_rows = load_jsonl(args.data / "train.jsonl")
    val_rows = load_jsonl(args.data / "val.jsonl")
    train_sha = hashlib.sha256((args.data / "train.jsonl").read_bytes()).hexdigest()
    _, _, frozen_cfg = load_npz(args.model)
    frozen = frozen_cfg.get("val_metrics", {})

    val_feas = [feasible_set(r["graph"], r["verb"], r["target"])
                for r in val_rows]
    yva = np.array([LABELS.index(r["label"]) for r in val_rows], dtype=np.int64)
    truth_out = sum(1 for i, r in enumerate(val_rows)
                    if r["label"] not in val_feas[i])
    print(f"IMP7 v2 superset-target training — train={len(train_rows)} "
          f"val={len(val_rows)} tau={tau} hidden={hidden} "
          f"seed={args.seed} epochs={args.epochs}")
    print(f"val truth-feasibility law: labels outside F = {truth_out} (must be 0); "
          f"inference UNCHANGED from v1 (masked softmax + renorm + "
          f"evaluate_setval)")

    fracs = sorted({float(f) for f in args.fractions.split(",")})
    sup_fracs = [float(f) for f in args.sup_fracs.split(",")]
    if 0.0 not in sup_fracs:
        sup_fracs = [0.0] + sup_fracs          # the v1 parity arm is mandatory

    results: dict[str, Any] = {"threshold": tau, "train_sha256": train_sha,
                               "frozen_z13_val": frozen,
                               "v1_receipt_ah8": _V1_RECEIPT, "fractions": {}}
    params_at_full: dict[float, dict[str, np.ndarray]] = {}
    stats_at_full: dict[float, dict[str, int]] = {}
    fe_full: Featurizer | None = None

    print(f"\n{'frac':>5} {'arm':>12} {'params':>7} {'coverage':>9} "
          f"{'soundness':>10} {'answered(c/w)':>16} {'hedge(t)':>9} "
          f"{'switch':>11}")
    for frac in fracs:
        sub = subset_rows(train_rows, frac, seed=args.seed)
        fe = Featurizer().fit(sub)
        Xtr, ytr = rows_xy(sub, fe)
        Xva = fe.transform(val_rows)

        feas_tr = [feasible_set(r["graph"], r["verb"], r["target"])
                   for r in sub]
        gate_tr = lattice_gate(feas_tr)
        sup_idx_tr = np.array([truth_superset_idx(int(yy), f)
                               for yy, f in zip(ytr, feas_tr)], dtype=np.int64)

        raw_params, _ = train_model(Xtr, ytr, hidden, args.epochs, args.lr,
                                    args.batch, args.seed, l2=args.l2)
        raw = raw_evaluate(raw_params, Xva, yva, threshold=tau)
        probs5, _ = forward(raw_params, Xva)
        renorm = evaluate_lattice(probs5, val_feas, yva, tau, mode="renorm")
        n_raw = sum(v.size for v in raw_params.values())
        for name, m in (("raw", raw), ("renorm", renorm)):
            print(f"{frac:>5.2f} {name:>12} {n_raw:>7} {m['coverage']:>9.4f} "
                  f"{m['soundness']:>10.4f} {m['answered']:>7}"
                  f"({m['answered_correct']}/{m['answered_wrong']}) "
                  f"{'-':>9} {'-':>11}")

        frac_res: dict[str, Any] = {
            "n_train": len(sub), "feature_dim": fe.dim,
            "raw": {k: v for k, v in raw.items() if k != "per_class"},
            "renorm": {k: v for k, v in renorm.items() if k != "per_class"},
            "params_raw": n_raw, "v2": {}}
        for sf in sup_fracs:
            ttr, st = superset_targets(ytr, feas_tr, sf, args.seed,
                                       sup_idx=sup_idx_tr)
            # both target laws hold by construction — verified, not assumed
            assert gate_tr[np.arange(len(ttr)), ttr].all(), \
                "v2 target outside its gate — superset/target mismatch"
            v2_params, losses = train_model_gated(
                Xtr, ttr, len(_ELEMENTS), gate_tr, hidden, args.epochs,
                args.lr, args.batch, args.seed, l2=args.l2)
            probs32, _ = forward(v2_params, Xva)
            v2 = evaluate_setval(probs32, val_feas, yva, tau)
            arm = "v1-setval" if sf == 0.0 else f"v2(f={sf:g})"
            npar = sum(v.size for v in v2_params.values())
            hedge = f"{v2['hedged']}({v2['hedged_contains_truth']:.2f})"
            sw = f"{st['n_switched']}/{st['n_eligible']}"
            print(f"{frac:>5.2f} {arm:>12} {npar:>7} {v2['coverage']:>9.4f} "
                  f"{v2['soundness']:>10.4f} {v2['answered']:>7}"
                  f"({v2['answered_correct']}/{v2['answered_wrong']}) "
                  f"{hedge:>9} {sw:>11}")
            frac_res["v2"][f"{sf:g}"] = {
                **{k: v for k, v in v2.items() if k != "per_class"},
                "switched": st["n_switched"], "eligible": st["n_eligible"],
                "final_loss": losses[-1]}
            if frac == max(fracs):
                params_at_full[sf] = v2_params
                stats_at_full[sf] = st
                fe_full = fe
        results["fractions"][f"{frac:.2f}"] = frac_res

    # ---- THE BAR, named by machine so the receipt cannot soften it ----
    full = f"{max(fracs):.2f}"
    ren = results["fractions"][full]["renorm"]
    v1 = results["fractions"][full]["v2"]["0"]
    arms = results["fractions"][full]["v2"]
    checks: dict[str, str] = {}
    for sf_s, m in arms.items():
        label = "v1-setval" if sf_s == "0" else f"v2(f={sf_s})"
        checks[f"{label}@100 vs renorm@100"] = _pareto(m, ren)
        checks[f"{label}@100 vs v1@100"] = _pareto(m, v1)
    if frozen and "soundness" in frozen:
        drift = (results["fractions"][full]["raw"]["soundness"]
                 - frozen["soundness"])
        checks["raw@100 reproduces frozen Z13"] = (
            "yes" if abs(drift) < 1e-9 else f"NO (drift {drift:+.6f})")
    cov_drift = round(v1["coverage"], 4) - _V1_RECEIPT["coverage"]
    snd_drift = round(v1["soundness"], 4) - _V1_RECEIPT["soundness"]
    checks["v1 arm (f=0) reproduces AH8 receipt"] = (
        "yes" if abs(cov_drift) < 5e-5 and abs(snd_drift) < 5e-5
        else f"NO (cov {cov_drift:+.4f}, snd {snd_drift:+.4f})")
    for f_s in ("0.50", "0.25"):                 # the 1.95x data test, v2 side
        if f_s in results["fractions"]:
            best_sub = max(results["fractions"][f_s]["v2"].values(),
                           key=lambda m: (m["soundness"], m["coverage"]))
            checks[f"v2-best@{int(float(f_s)*100)} vs renorm@100"] = \
                _pareto(best_sub, ren)

    # best-arm selection: clause 1 first, then clause 2, else honest loss.
    # (arms keys are strings — format float(best) before :g; caught by the
    # first --v2 run 2026-09-30, crash-before-verdict, fix is type-only)
    clause1 = [s for s, m in arms.items() if _pareto(m, ren) == "PARETO-BEAT"]
    clause2 = [s for s, m in arms.items()
               if s != "0" and _pareto(m, v1) == "PARETO-BEAT"]
    if clause1:
        best = max(clause1, key=lambda s: (arms[s]["coverage"],
                                           arms[s]["soundness"]))
        verdict = (f"BAR-MET clause 1 (Pareto-beats renorm@100): "
                   f"v2(f={float(best):g})")
    elif clause2:
        best = max(clause2, key=lambda s: (arms[s]["coverage"],
                                           arms[s]["soundness"]))
        verdict = (f"BAR-MET clause 2 (beats v1 coverage at equal-or-better "
                   f"soundness): v2(f={float(best):g})")
    else:
        best = max(arms, key=lambda s: (arms[s]["soundness"],
                                        arms[s]["coverage"]))
        verdict = (f"BAR-MISSED (honest loss); max-soundness arm "
                   f"v2(f={float(best):g})")
    results["bar"] = {"checks": checks, "verdict": verdict,
                      "best_sup_frac": float(best)}

    out = ROOT / "models" / "ldt_v2_superset.npz"
    assert fe_full is not None and params_at_full  # full frac always runs
    save_npz(out, params_at_full[float(best)], fe_full, {
        "schema": "ldt_v2_superset.npz", "train_sha256": train_sha,
        "train_fraction": max(fracs),
        "n_train": results["fractions"][full]["n_train"],
        "hidden": hidden, "epochs": args.epochs, "lr": args.lr,
        "batch": args.batch, "seed": args.seed, "l2": args.l2,
        "threshold": tau, "n_elements": len(_ELEMENTS),
        "gate_law": "element <= feasible_set (subset mask)",
        "target_law": "smallest truth superset on switched eligible rows, "
                      "singleton elsewhere",
        "sup_frac": float(best),
        "sup_frac_stats": {f"{k:g}": v for k, v in stats_at_full.items()},
        "element_order": _elem_names(), "bar_verdict": verdict,
    }, labels=_elem_names())
    print(f"\nBAR checks (soundness/coverage plane, tau={tau}):")
    for k in sorted(checks):
        print(f"  {k}: {checks[k]}")
    print(f"VERDICT: {verdict}")
    print(f"saved best arm: {out} "
          f"({sum(v.size for v in params_at_full[float(best)].values())} "
          f"weight elements)")
    print(f"wall: {time.perf_counter() - t0:.1f}s (budget 900s)")
    print(json.dumps(results, sort_keys=True))
    return 0



def _one_line(m: dict[str, Any]) -> str:
    return (f"coverage={m['coverage']:.4f} answered={m['answered']} "
            f"(correct {m['answered_correct']} / wrong {m['answered_wrong']}) "
            f"soundness={m['soundness']:.4f}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--model", type=Path, default=ROOT / "models" / "legality_v0.npz")
    ap.add_argument("--data", type=Path, default=ROOT / "logs" / "legality_ds")
    ap.add_argument("--split", default="val", choices=("val", "train"))
    ap.add_argument("--threshold", type=float, default=None,
                    help="default: the threshold frozen in the npz config")
    ap.add_argument("--sweep", default="0.5,0.6,0.7,0.8,0.9",
                    help="comma-separated extra thresholds to table")
    # AH8 v1 mode: retrains from data, ignores the frozen model as input
    ap.add_argument("--v1", action="store_true",
                    help="run the AH8 experiment: set-valued 32-element head "
                         "trained under the exact lattice mask; tables "
                         "raw/renorm/v1-setval at --fractions of the data")
    ap.add_argument("--fractions", default="1.0,0.5,0.25",
                    help="v1/v2 mode: train fractions to table")
    # IMP7 v2 mode (the AH8 receipt's named untested lever)
    ap.add_argument("--v2", action="store_true",
                    help="run the IMP7 experiment: superset-target training "
                         "grid — a fraction of eligible rows target the "
                         "smallest truth-containing lattice superset; "
                         "inference unchanged from v1")
    ap.add_argument("--sup-fracs", default="0.1,0.25,0.5,0.75",
                    help="v2 mode: fractions of eligible rows switched to the "
                         "superset target (0.0, the v1 parity arm, is always "
                         "added)")
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--hidden", default="128,64")
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--batch", type=int, default=256)
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--l2", type=float, default=1e-4)
    args = ap.parse_args(argv)

    if args.v2:
        # v2 shares v1's protocol pin (tau=0.7, V7's bar)
        if args.threshold is None:
            args.threshold = 0.7
        return run_v2(args)

    if args.v1:
        # v0's --threshold default reads the npz; v1 pins V7's protocol
        if args.threshold is None:
            args.threshold = 0.7
        return run_v1(args)

    params, fe, config = load_npz(args.model)
    threshold = (args.threshold if args.threshold is not None
                 else float(config["threshold"]))
    rows = load_jsonl(args.data / f"{args.split}.jsonl")
    X = fe.transform(rows)
    y = np.array([LABELS.index(r["label"]) for r in rows], dtype=np.int64)
    probs, _ = forward(params, X)

    feasibles = [feasible_set(r["graph"], r["verb"], r["target"])
                 for r in rows]

    # truth-feasibility law: the dataset's own label must survive every
    # descent (if this fails, the projection could kill RIGHT answers).
    truth_out = sum(1 for i, r in enumerate(rows)
                    if r["label"] not in feasibles[i])
    short = {lab: lab.replace("illegal_", "").replace("legal_", "")
             for lab in LABELS}
    distinct = [",".join(short[l] for l in sorted(f))
                for f in sorted(set(feasibles), key=sorted)]

    print(f"model={args.model.name} split={args.split} n={len(rows)} "
          f"threshold={threshold}")
    print(f"feasible-set law: labels outside their feasible set: {truth_out} "
          f"(must be 0); distinct feasible sets = {distinct}")

    raw = raw_evaluate(params, X, y, threshold=threshold)
    strict = evaluate_lattice(probs, feasibles, y, threshold, mode="strict")
    renorm = evaluate_lattice(probs, feasibles, y, threshold, mode="renorm")

    # cross-tier kills: raw answers whose argmax the cascade rules out —
    # every one of them was wrong; the lattice deletes that error class.
    pred_raw = probs.argmax(axis=1)
    pmax = probs.max(axis=1)
    answered_raw = pmax >= threshold
    kills = sum(1 for i in range(len(rows))
                if answered_raw[i] and LABELS[pred_raw[i]] not in feasibles[i])

    print(f"\nraw      @{threshold}: {_one_line(raw)}")
    print(f"lattice strict @{threshold}: {_one_line(strict)} "
          f"infeasible-answers={strict['answered_infeasible']} "
          f"answered-not-raw={strict['answered_not_raw']} (both must be 0)")
    print(f"lattice renorm @{threshold}: {_one_line(renorm)} "
          f"(v1 preview; answered-not-raw={renorm['answered_not_raw']} is "
          f"expected > 0 there)")
    print(f"raw cross-tier errors killed to BOTTOM/flip: {kills}")

    print(f"\n{'tau':>5} {'raw sound':>10} {'lat sound':>10} "
          f"{'raw cov':>8} {'lat cov':>8} {'kills':>6}")
    for tau in [float(t) for t in args.sweep.split(",")]:
        r = raw_evaluate(params, X, y, threshold=tau)
        s = evaluate_lattice(probs, feasibles, y, tau, mode="strict")
        pr = probs.argmax(axis=1)
        pm = probs.max(axis=1)
        k = sum(1 for i in range(len(rows))
                if pm[i] >= tau and LABELS[pr[i]] not in feasibles[i])
        rs = f"{r['soundness']:.4f}" if r["answered"] else "  n/a"
        ss = f"{s['soundness']:.4f}" if s["answered"] else "  n/a"
        print(f"{tau:>5.2f} {rs:>10} {ss:>10} {r['coverage']:>8.4f} "
              f"{s['coverage']:>8.4f} {k:>6}")

    print(json.dumps({
        "threshold": threshold,
        "raw": {k: v for k, v in raw.items() if k != "per_class"},
        "lattice_strict": {k: v for k, v in strict.items() if k != "per_class"},
        "lattice_renorm": {k: v for k, v in renorm.items() if k != "per_class"},
        "raw_cross_tier_kills": kills,
        "truth_outside_feasible": truth_out,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
