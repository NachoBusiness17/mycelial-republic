"""SCS scorer: Jensen-Shannon divergence over choice sets.

Ordinary code, stdlib only (math + collections). No ML framework, no network.

A choice set is a list of picked options, e.g. ``["a", "b", "a"]``. Each set
is reduced to an empirical distribution over the union of both sets' supports
and scored with Jensen-Shannon divergence (JSD). With ``base=2`` JSD is
bounded in ``[0.0, 1.0]`` bits, so the SCS consistency score is defined as
``1 - JSD``: 1.0 means the two sets made identical choices, 0.0 means fully
disjoint choices.

Import (from the repo root, with the repo venv):

    from tools.scs import js_divergence, scs_divergence, scs_score

Run the self-test (also the default when executed as a script):

    python tools/scs.py --self-test

Returns
-------
``scs_score(a, b)`` -> ``{"divergence": float, "consistency": float,
"support": [labels]}`` with ``divergence + consistency == 1.0`` in bits.
"""

from __future__ import annotations

import argparse
import math
import sys
from collections import Counter
from typing import Hashable, Iterable, Sequence


def _as_vector(weights: Sequence[float]) -> list[float]:
    """Validate and normalize a weight vector into a probability vector.

    Zeros are kept (they carry support information); negatives and all-zero
    vectors are rejected.
    """
    if weights is None:
        raise ValueError("weights must be a sequence, got None")
    vec = [float(w) for w in weights]
    if not vec:
        raise ValueError("empty weight vector")
    if any(w < 0.0 for w in vec):
        raise ValueError("negative weight in vector")
    total = math.fsum(vec)
    if total <= 0.0:
        raise ValueError("weights sum to zero; not a distribution")
    return [w / total for w in vec]


def shannon_entropy(weights: Sequence[float], *, base: float = 2.0) -> float:
    """Shannon entropy of a distribution given as (possibly unnormalized,
    non-negative) weights. 0*log(0) terms contribute 0."""
    vec = _as_vector(weights)
    if base <= 0.0 or base == 1.0:
        raise ValueError("log base must be positive and != 1")
    log_div = math.log(base)
    h = 0.0
    for p in vec:
        if p > 0.0:
            h -= p * math.log(p) / log_div
    return h


def js_divergence(
    p: Sequence[float], q: Sequence[float], *, base: float = 2.0
) -> float:
    """Jensen-Shannon divergence between two vectors on the SAME support.

    JSD(P, Q) = H(M) - (H(P) + H(Q)) / 2 with M = (P + Q) / 2. Inputs are
    normalized defensively, so counts or unnormalized weights are accepted.
    With base=2 the result is bounded in [0.0, 1.0]; with base=e in
    [0.0, ln 2]. Symmetric in p and q. Raises ValueError on length mismatch.
    """
    pv = _as_vector(p)
    qv = _as_vector(q)
    if len(pv) != len(qv):
        raise ValueError(
            "support length mismatch: len(p)=%d len(q)=%d" % (len(pv), len(qv))
        )
    m = [(a + b) / 2.0 for a, b in zip(pv, qv)]
    val = shannon_entropy(m, base=base) - 0.5 * (
        shannon_entropy(pv, base=base) + shannon_entropy(qv, base=base)
    )
    # Floating point can land a hair under 0.0 for identical inputs.
    return max(0.0, val)


def choice_distribution(choices: Iterable[Hashable]) -> dict[Hashable, float]:
    """Reduce a choice set (any iterable of hashable picks) to an empirical
    distribution {label: probability}. Raises ValueError when empty."""
    counts: Counter = Counter(choices)
    if not counts:
        raise ValueError("empty choice set")
    total = math.fsum(counts.values())
    return {label: n / total for label, n in counts.items()}


def _union_support(a: Iterable[Hashable], b: Iterable[Hashable]) -> list:
    """Order-stable union of two choice sets' supports (insertion order,
    a's labels first). No sorting, so unorderable label types are fine."""
    return list(dict.fromkeys(list(a) + list(b)))


def scs_divergence(
    a: Iterable[Hashable], b: Iterable[Hashable], *, base: float = 2.0
) -> float:
    """Jensen-Shannon divergence (bits by default) between two choice sets.

    Each set is reduced to counts over the union of both supports; labels
    missing from one set contribute 0. Raises ValueError when either set is
    empty.
    """
    dist_a = choice_distribution(a)
    dist_b = choice_distribution(b)
    support = _union_support(dist_a.keys(), dist_b.keys())
    p = [dist_a.get(label, 0.0) for label in support]
    q = [dist_b.get(label, 0.0) for label in support]
    return js_divergence(p, q, base=base)


def scs_score(a: Iterable[Hashable], b: Iterable[Hashable]) -> dict:
    """SCS score for two choice sets: JSD in bits plus its complement.

    Returns ``{"divergence": jsd_bits, "consistency": 1 - jsd_bits,
    "support": [labels]}``. Identical choice distributions score
    consistency 1.0; fully disjoint ones score 0.0.
    """
    dist_a = choice_distribution(a)
    dist_b = choice_distribution(b)
    support = _union_support(dist_a.keys(), dist_b.keys())
    divergence = scs_divergence(a, b, base=2.0)
    return {
        "divergence": divergence,
        "consistency": 1.0 - divergence,
        "support": support,
    }


# ---------------------------------------------------------------------------
# Self-test: deterministic, stdlib-only, no fixtures. Run via
# ``python tools/scs.py`` or ``python tools/scs.py --self-test``.
# ---------------------------------------------------------------------------

def self_test() -> int:
    """Run every check; return the number of checks run. Raises AssertionError
    on the first failure."""
    checks = 0
    ln2 = math.log(2.0)

    # 1. Identity: JSD(P, P) == 0 for a non-trivial asymmetric vector.
    p = [0.7, 0.2, 0.1]
    assert abs(js_divergence(p, p)) < 1e-12, "JSD(P,P) must be 0"
    checks += 1

    # 2. Symmetry: JSD(P, Q) == JSD(Q, P).
    q = [0.1, 0.8, 0.1]
    assert abs(js_divergence(p, q) - js_divergence(q, p)) < 1e-12, "JSD symmetric"
    checks += 1

    # 3. Bounds: 0 <= JSD <= 1 bit across a sweep of mixed vectors.
    grid = [i / 10.0 for i in range(11)]
    for a in grid:
        for b in grid:
            v = js_divergence([a, 1.0 - a], [b, 1.0 - b])
            assert -1e-12 <= v <= 1.0 + 1e-12, "JSD out of [0,1]: %r" % v
    checks += 1

    # 4. Known value: JSD((1,0), (0.5,0.5)) = H(0.75,0.25) - 0.5*H(0.5,0.5)
    #    = 0.8112781244591328 - 0.5 = 0.3112781244591328 bits.
    known = js_divergence([1.0, 0.0], [0.5, 0.5])
    assert abs(known - 0.3112781244591328) < 1e-12, "known JSD value off: %r" % known
    checks += 1

    # 5. Maximal divergence: disjoint supports of uniform mass -> exactly 1 bit.
    assert abs(js_divergence([1.0, 0.0], [0.0, 1.0]) - 1.0) < 1e-12, "max JSD = 1 bit"
    #    In nats the same pair is ln 2.
    assert abs(js_divergence([1.0, 0.0], [0.0, 1.0], base=math.e) - ln2) < 1e-12, \
        "max JSD in nats = ln 2"
    checks += 1

    # 6. Unnormalized inputs are normalized: JSD invariant to positive scaling.
    raw = js_divergence([7.0, 2.0, 1.0], [14.0, 4.0, 2.0])
    assert abs(raw) < 1e-12, "scaled duplicates must stay 0"
    checks += 1

    # 7. Choice sets, known value: a=(x,x,y) vs b=(x,y,y)
    #    p=(2/3,1/3), q=(1/3,2/3), m=(1/2,1/2) -> 1 - H(2/3,1/3) bits.
    a_set = ["x", "x", "y"]
    b_set = ["x", "y", "y"]
    expected = 1.0 - shannon_entropy([2.0, 1.0])
    got = scs_divergence(a_set, b_set)
    assert abs(got - expected) < 1e-12, "choice-set JSD off: %r != %r" % (got, expected)
    checks += 1

    # 8. Identical choice sets -> divergence 0, consistency 1.
    score = scs_score(["a", "b", "a"], ["a", "a", "b"])
    assert abs(score["divergence"]) < 1e-12 and abs(score["consistency"] - 1.0) < 1e-12, \
        "identical sets must score consistency 1.0"
    checks += 1

    # 9. Disjoint choice sets -> divergence 1, consistency 0.
    score = scs_score(["a", "a"], ["b", "b"])
    assert abs(score["divergence"] - 1.0) < 1e-12 and abs(score["consistency"]) < 1e-12, \
        "disjoint sets must score consistency 0.0"
    checks += 1

    # 10. Asymmetric sample sizes still score against the union support.
    score = scs_score(["a", "a", "a"], ["a", "b"])
    # p=(1,0), q=(1/2,1/2) -> 0.3112781244591328 bits (check 4's value).
    assert abs(score["divergence"] - 0.3112781244591328) < 1e-12, \
        "uneven-size scoring off: %r" % score["divergence"]
    assert score["support"] == ["a", "b"], "support must be union, insertion order"
    checks += 1

    # 11. divergence + consistency == 1 exactly, support labels hashable-mixed.
    score = scs_score([1, 2, 2], [2, 3])
    assert abs(score["divergence"] + score["consistency"] - 1.0) < 1e-12, \
        "score must be a partition of unity"
    assert score["support"] == [1, 2, 3], "int labels kept, no sort crash"
    checks += 1

    # 12. Error paths: empty set, negative weights, all-zero, length mismatch.
    for fn in (
        lambda: scs_divergence([], ["a"]),
        lambda: scs_divergence(["a"], []),
        lambda: js_divergence([0.5, -0.1], [0.5, 0.1]),
        lambda: js_divergence([0.0, 0.0], [0.5, 0.5]),
        lambda: js_divergence([1.0], [1.0, 0.0]),
        lambda: shannon_entropy([0.5, 0.5], base=1.0),
    ):
        try:
            fn()
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError from %r" % fn)
    checks += 1

    # 13. Determinism: same inputs, same bits, twice.
    assert scs_score(["a", "b"], ["b", "a"]) == scs_score(["a", "b"], ["b", "a"]), \
        "scorer must be deterministic"
    checks += 1

    print("SCS self-test: PASS (%d checks)" % checks)
    return checks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SCS scorer: JSD over choice sets")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run the built-in self-test (also the default with no args)",
    )
    args = parser.parse_args(argv)
    # No-arg invocation runs the self-test: the cheapest possible proof of
    # life for the next seat.
    if not args.self_test and argv:
        parser.print_help()
        return 2
    self_test()
    return 0


if __name__ == "__main__":
    sys.exit(main())
