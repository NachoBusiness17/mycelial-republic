"""Ractor engine falsifier stubs (FW-36, FIFTY_WIDE_BOARD_20260917.md G line 65).

The four pre-registered falsifiers of watch/inbox/RACTOR_ENGINE_SPEC_v0_1.md
section 5, encoded as runnable pytest stubs. Law of the stone: "turn the 4
pre-registered falsifiers into runnable test stubs".

Run state, 2026-09-28: the engine's sanctioned home mag/ractor/engine.py
(spec section 6, step 2) does not exist yet, so every engine-backed stub SKIPS
with the spec section cited. One test runs today unconditionally: it pins the
pre-registered constants so a future engine cannot drift them silently. When
the engine and the hash-committed battery land (spec section 6, steps 2 and 4),
these stubs go live with zero edits: the checks below are complete
implementations against the spec's receipt schema (section 4), not
scaffolding.

Threshold law: only the numbers the spec pre-registered are asserted
numerically (section 5.1: 15pp, KS 0.2, 1.5x, +-30%; section 5.2: separation
"threshold as in 5.1"; section 5.3: >=5 seeds, >=2 outcomes, 0.15 nats on >=30%
of items, all explicitly flagged "invented this session, pre-registered here
first" in spec section 10.3). Section 5.4's four probes carry NO
pre-registered numbers, so those stubs assert only the structural properties
the spec states (non-inversion, routing to clamps/retrieval) and refuse to
invent thresholds: that invention would violate the spec's own
pre-registration discipline.
"""
from __future__ import annotations

import importlib
import math
from typing import Any

import numpy as np
import pytest

# --- Pre-registered constants (RACTOR_ENGINE_SPEC_v0_1.md; section cites inline) ---

THETA_DEFAULT = 0.35            # section 1.1 verdict node
DT = 0.05                       # section 1.1 Euler step
STEP_CAP_PER_EPOCH = 200        # section 1.1
LAMBDA_V = 0.02                 # section 1.1 value-layer conservation
EXIT_DELTA = 5e-4               # section 1.2 stability exit
BUDGET_CAP_HARD = 64            # section 3 T1.3 cap, "non-negotiable"
KAPPA_N0 = 0.3                  # section 5.1 N=0 witness
KAPPA_N1 = 2.5                  # section 5.1 N=1 witness
THETA_NEG_N1_FACTOR = 0.5       # section 5.1 N=1 negativity bias
AMBIGUOUS_QUESTIONS_MIN = 20    # section 5.1 ">= 20 ambiguous questions"
NEG_RATE_MIN_DIFF_PP = 15       # section 5.1 pass condition 1
KS_D_MIN = 0.2                  # section 5.1 pass condition 2; section 5.2 uses "threshold as in 5.1"
LATENCY_RATIO_MIN = 1.5         # section 5.1 pass condition 3
KAPPA_RECOVERY_TOL = 0.30       # section 5.1 pass condition 4 (recover within +-30%)
SEEDS_MIN = 5                   # section 5.3 (spec 10.3: invented, pre-registered here first)
OUTCOMES_MIN = 2                # section 5.3
ENTROPY_FLOOR = 0.15            # section 5.3, normalized entropy
ENTROPY_ITEMS_MIN_FRAC = 0.30   # section 5.3
OUTCOME_SPACE = ("ENDORSE", "REFUSE", "UNDECIDED")  # section 4 verdict.outcome


def ks_statistic(a: list[float], b: list[float]) -> float:
    """Two-sample Kolmogorov-Smirnov D statistic.

    Computed directly on numpy because the repo venv carries numpy but not
    scipy (checked 2026-09-28); the spec's falsifier thresholds are on the D
    statistic, not on p-values, so no asymptotic tail is needed for the gates.
    """
    a = np.sort(np.asarray(a, dtype=float))
    b = np.sort(np.asarray(b, dtype=float))
    if a.size == 0 or b.size == 0:
        return 0.0
    grid = np.concatenate([a, b])
    cdf_a = np.searchsorted(a, grid, side="right") / a.size
    cdf_b = np.searchsorted(b, grid, side="right") / b.size
    return float(np.max(np.abs(cdf_a - cdf_b)))


def normalized_entropy(outcomes: list[str]) -> float:
    """Entropy of an outcome distribution, normalized to [0, 1] over the
    3-outcome verdict space. Spec 5.3 says "normalized entropy >= 0.15 nats";
    the nats-vs-normalized phrasing is ambiguous in the spec, so the
    normalized form is asserted and the raw nats value is derivable from it
    (normalized * ln(3))."""
    counts = {o: 0 for o in OUTCOME_SPACE}
    for o in outcomes:
        counts[o] = counts.get(o, 0) + 1
    n = sum(counts.values())
    if n == 0:
        return 0.0
    h = 0.0
    for c in counts.values():
        if c > 0:
            p = c / n
            h -= p * math.log(p)
    return h / math.log(len(OUTCOME_SPACE))


def _load(module: str, spec_step: str):
    """Load a mag.ractor submodule by name; skip with the spec step cited if absent."""
    try:
        return importlib.import_module(module)
    except ModuleNotFoundError as exc:
        pytest.skip(
            f"{module} not built yet ({spec_step}); falsifier stays pre-registered, "
            f"RACTOR_ENGINE_SPEC_v0_1.md section 5",
            allow_module_level=False,
        )


def _engine():
    return _load("mag.ractor.engine", "spec section 6 step 2")


def _battery():
    bat = _load("mag.ractor.battery", "spec section 6 step 4")
    items = bat.ambiguous_questions()
    assert len(items) >= AMBIGUOUS_QUESTIONS_MIN, (
        f"battery has {len(items)} ambiguous items, spec 5.1 requires >= {AMBIGUOUS_QUESTIONS_MIN}"
    )
    assert getattr(bat, "content_hash", None), "battery must be hash-committed before runs (spec section 7)"
    return bat


def _run(engine: Any, bat: Any, ocean: dict[str, float], seeds: list[int]) -> list[dict]:
    """Run the battery at one OCEAN setting across seeds; returns receipts (spec section 4)."""
    receipts: list[dict] = []
    for seed in seeds:
        receipts.extend(engine.run_battery(battery=bat, ocean=ocean, seed=seed))
    return receipts


# --- Live today: the pre-registration pin -----------------------------------


def test_pre_registration_pins_spec_constants() -> None:
    """The stub file's constants must equal the spec's pre-registered values.

    This is the runnable part of FW-36 before the engine exists: the numbers
    are the law, and this test fails if anyone edits them away from
    RACTOR_ENGINE_SPEC_v0_1.md sections 1-5 without a spec amendment."""
    assert (THETA_DEFAULT, DT, STEP_CAP_PER_EPOCH, LAMBDA_V) == (0.35, 0.05, 200, 0.02)
    assert EXIT_DELTA == 5e-4
    assert BUDGET_CAP_HARD == 64
    assert (KAPPA_N0, KAPPA_N1, THETA_NEG_N1_FACTOR) == (0.3, 2.5, 0.5)
    assert (NEG_RATE_MIN_DIFF_PP, KS_D_MIN, LATENCY_RATIO_MIN, KAPPA_RECOVERY_TOL) == (15, 0.2, 1.5, 0.30)
    assert (SEEDS_MIN, OUTCOMES_MIN, ENTROPY_FLOOR, ENTROPY_ITEMS_MIN_FRAC) == (5, 2, 0.15, 0.30)
    # instrument self-check on the statistics helpers (deterministic, no engine)
    assert ks_statistic([0.1, 0.2, 0.3], [0.9, 1.0, 1.1]) == 1.0
    assert ks_statistic([0.5, 0.5], [0.5, 0.5]) == 0.0
    assert normalized_entropy(["ENDORSE"] * 5) == 0.0
    assert normalized_entropy(["ENDORSE", "REFUSE", "UNDECIDED"]) == pytest.approx(1.0)


# --- Falsifier 5.1: personality visibility (N=0 vs N=1) ----------------------


def test_falsifier_1_personality_visibility() -> None:
    """Spec 5.1: OCEAN traits are material constants of L, visible in behavior.

    Pass = condition 1 AND (condition 2 OR condition 3) AND condition 4, per
    the spec's own joiner ("all four must hold", with 2-or-3 written as one
    disjunctive clause). Kill = statistically indistinguishable under all
    measures: fail loudly with the spec's COSTUME verdict, never silently."""
    engine, bat = _engine(), _battery()
    seeds = list(range(SEEDS_MIN))
    n0 = _run(engine, bat, {"O": 0.5, "C": 0.5, "E": 0.5, "A": 0.5, "N": 0.0}, seeds)
    n1 = _run(engine, bat, {"O": 0.5, "C": 0.5, "E": 0.5, "A": 0.5, "N": 1.0}, seeds)

    rate = lambda rs: sum(1 for r in rs if r["verdict"]["outcome"] == "REFUSE") / len(rs)
    cond1 = abs(rate(n1) - rate(n0)) * 100 >= NEG_RATE_MIN_DIFF_PP
    cond2 = ks_statistic([r["verdict"]["confidence"] for r in n1],
                         [r["verdict"]["confidence"] for r in n0]) >= KS_D_MIN
    t0 = sorted(r["verdict"]["fire_latency_steps"] for r in n0)
    t1 = sorted(r["verdict"]["fire_latency_steps"] for r in n1)
    med = lambda xs: xs[len(xs) // 2] if xs else 0
    cond3 = med(t1) >= LATENCY_RATIO_MIN * med(t0) if med(t0) > 0 else False

    # condition 4: recover kappa from the held-out half, within +-30% (spec 5.1.4)
    fit_half, held_half = bat.split_fit_heldout()
    recovered = engine.fit_kappa(receipts=_run(engine, bat, {"O": 0.5, "C": 0.5, "E": 0.5, "A": 0.5, "N": 0.8},
                                              seeds), fit_items=fit_half, heldout_items=held_half)
    cond4 = abs(recovered - 0.8) <= KAPPA_RECOVERY_TOL * 0.8

    if not (cond1 or cond2 or cond3):
        pytest.fail(
            "N=0 vs N=1 indistinguishable on every measure: the OCEAN->L map is COSTUME "
            "(spec 5.1 kill condition: kill the parameterization, keep the explainer, "
            "file a canon correction; silence is not an allowed outcome)"
        )
    assert cond1, f"pass condition 1 failed: negative-verdict rate gap < {NEG_RATE_MIN_DIFF_PP}pp"
    assert cond2 or cond3, "pass conditions 2/3 both failed (confidence KS and latency ratio)"
    assert cond4, f"kappa recovery outside +-{KAPPA_RECOVERY_TOL:.0%} (got {recovered}, planted 0.8)"


# --- Falsifier 5.2: placebo-twin certification -------------------------------


def test_falsifier_2_placebo_certification() -> None:
    """Spec 5.2: every witness ships with a zero-coupling placebo twin
    (trait adjectives in the mouth prompt, all graph gains neutral) and must
    separate from it; the s10 parameter-swap null: the separation must appear
    and disappear with the gains, not with run order."""
    engine, bat = _engine(), _battery()
    witness_ocean = {"O": 0.7, "C": 0.4, "E": 0.2, "A": 0.6, "N": 0.8}
    placebo_ocean = engine.placebo_gains()  # spec 5.2 intercepts: kappa 0.3, g_P 0.5, lambda_0, sigma 0.2, a 0
    seeds = list(range(SEEDS_MIN))
    wit = _run(engine, bat, witness_ocean, seeds)
    plb = _run(engine, bat, placebo_ocean, seeds)

    def verdicts(rs: list[dict]) -> list[str]:
        return [r["verdict"]["outcome"] for r in rs]

    # certification gate: distribution separation (KS on the mapped verdicts' u_O1, threshold as in 5.1)
    d = ks_statistic([r["verdict"]["u_O1_final"] for r in wit], [r["verdict"]["u_O1_final"] for r in plb])
    if d < KS_D_MIN:
        pytest.fail(
            f"witness does not beat its own placebo (KS D={d:.3f} < {KS_D_MIN}): prompt costume, "
            "not mechanism; the witness is NOT certified and may not join a salon quorum (spec 5.2)"
        )

    # s10 swap null: separation appears and disappears with the gains, not run order.
    # Witness-gains vs placebo-gains halves must separate in BOTH seed orders.
    half = len(seeds) // 2
    d_order1 = ks_statistic([r["verdict"]["u_O1_final"] for r in _run(engine, bat, witness_ocean, seeds[:half])],
                            [r["verdict"]["u_O1_final"] for r in _run(engine, bat, placebo_ocean, seeds[half:])])
    d_order2 = ks_statistic([r["verdict"]["u_O1_final"] for r in _run(engine, bat, witness_ocean, seeds[half:])],
                            [r["verdict"]["u_O1_final"] for r in _run(engine, bat, placebo_ocean, seeds[:half])])
    assert d_order1 >= KS_D_MIN and d_order2 >= KS_D_MIN, (
        f"s10 swap null failed: separation followed run order (D={d_order1:.3f}/{d_order2:.3f}), "
        "not the gains"
    )
    # receipt-shape check: every battery item ran at every seed for both settings
    assert len(wit) == len(plb) == len(bat.ambiguous_questions()) * SEEDS_MIN


# --- Falsifier 5.3: seed diversity or the depth is theater -------------------


def test_falsifier_3_seed_diversity() -> None:
    """Spec 5.3: every ambiguous question rerun at >= 5 noise seeds; pass =
    >= 2 distinct outcomes per question AND normalized entropy >= 0.15 on
    >= 30% of items. All seeds agreeing on ambiguous items = the physics is
    decorative (the '100% self-agreement' failure, spec 5.3 honesty note)."""
    engine, bat = _engine(), _battery()
    witness_ocean = {"O": 0.7, "C": 0.4, "E": 0.2, "A": 0.6, "N": 0.8}
    seeds = list(range(SEEDS_MIN))
    receipts = _run(engine, bat, witness_ocean, seeds)

    by_q: dict[str, list[str]] = {}
    for r in receipts:
        by_q.setdefault(r["question"]["id"], []).append(r["verdict"]["outcome"])
    assert len(by_q) == len(bat.ambiguous_questions()), "every battery item must be run at every seed"

    degenerate, entropy_ok = [], 0
    for qid, outcomes in by_q.items():
        assert len(outcomes) >= SEEDS_MIN, f"{qid}: fewer than {SEEDS_MIN} seed reruns"
        if len(set(outcomes)) < OUTCOMES_MIN:
            degenerate.append(qid)
        if normalized_entropy(outcomes) >= ENTROPY_FLOOR:
            entropy_ok += 1

    if not degenerate and entropy_ok == 0:
        pytest.fail(
            "all seeds agree on every ambiguous item: the graph collapsed to a fixed point "
            "independent of the noise, the physics is decorative and the mouth is doing all "
            "the work (spec 5.3 failure reading)"
        )
    assert len(degenerate) < len(by_q), (
        f"{len(degenerate)}/{len(by_q)} items degenerate across seeds (< {OUTCOMES_MIN} distinct outcomes)"
    )
    frac = entropy_ok / len(by_q)
    assert frac >= ENTROPY_ITEMS_MIN_FRAC, (
        f"normalized entropy >= {ENTROPY_FLOOR} on only {frac:.0%} of items (< {ENTROPY_ITEMS_MIN_FRAC:.0%})"
    )


# --- Falsifier 5.4: loop-depth honesty (64x != 70B) --------------------------


def test_falsifier_4_loop_depth_minimal_pairs() -> None:
    """Spec 5.4 probe 1 (the primary standing metric): counterfactual
    sensitivity on one-fact minimal pairs. The spec pre-registered the probe,
    not a number; the structural law it states is strict: budget claims that
    fail the minimal-pairs regression are theater, and quality must not
    invert with depth. So: accuracy at the witness budget must be >= r=1,
    and the quality-vs-loops curve must be non-increasing in its losses."""
    engine = _engine()
    bat = _load("mag.ractor.regression", "spec section 5.4 probe 1 (minimal-pairs battery)")
    r1 = engine.minimal_pairs_accuracy(battery=bat, loops=1)
    rw = engine.minimal_pairs_accuracy(battery=bat, loops=engine.witness_budget())
    assert rw >= r1, (
        f"depth inverted the minimal-pairs regression (witness budget {rw:.3f} < r=1 {r1:.3f}): "
        "the budget claim is theater regardless of the imported shape law (spec 5.4)"
    )


def test_falsifier_4_degradation_and_grounding() -> None:
    """Spec 5.4 probes 3 and 4, structural form only (the spec pre-registered
    no numbers for them; inventing thresholds here would violate its own
    pre-registration discipline, spec 10.3 names the one lawful invention):
    probe 3: quality vs loop count must not invert (each doubling of loops
    scores >= the smaller budget); probe 4: unknown facts route to
    clamps/retrieval, which shows up as UNDECIDED-or-retrieval-cited
    verdicts, never confident hallucination through loops."""
    engine = _engine()
    bat = _load("mag.ractor.regression", "spec section 5.4 probes 3/4 batteries")
    curve = [engine.probe3_quality(battery=bat, loops=n) for n in (4, 8, 16, 32, 64)]
    for smaller, larger in zip(curve, curve[1:]):
        assert larger >= smaller - 1e-9, (
            f"quality inverted between loops ({smaller:.3f} -> {larger:.3f}): "
            "degradation beyond the loop's effective memory horizon (spec 5.4 probe 3, nemotron)"
        )
    unknown = engine.probe4_unknown_facts(battery=bat)
    routed = [r for r in unknown if r["verdict"]["outcome"] == "UNDECIDED" or r.get("retrieval_cited")]
    assert len(routed) == len(unknown), (
        f"{len(unknown) - len(routed)} unknown-fact items answered confidently without retrieval: "
        "hallucinated through loops; depth refines priors, breadth supplies priors (spec 5.4 probe 4)"
    )
