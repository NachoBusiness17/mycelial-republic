"""memweave — the consensus weave + consensus-illusion guard, pure stdlib.

THE MECHANISM (our working implementation of this pattern):
  Run N cheap workers in PARALLEL, then flock-converge on consensus. Parallelism beats
  latency; consensus beats single-judgment; feed STRUCTURES not prose to cheap models.

  The CORE is the CONSENSUS-ILLUSION GUARD (verified 2026-08-11):
    agreement is only REAL if the agreeing witnesses are INDEPENDENT.
    N correlated hallucinations ≈ 1 opinion, not N.
  This is the fix for the #1 documented failure of swarm consensus: correlated answers
  (same training, same prompt, same reasoning path) counted as independent agreement.
  This guard reports the EFFECTIVE INDEPENDENT witness count so a weave never trusts a
  correlated consensus as a strong one.

ALGORITHM:
  * decompose(goal, n_bits)      -> fan a goal into bite-sized deterministic bits.
  * consensus_quality(answers)   -> effective independent agreement (Jaccard, tau=0.6).
  * weave(answers)               -> combine: pick the strongest independent answer.

PURE STDLIB — no dependencies. Runs: python -m pytest tests/ -q
Schema: memweave.v1
"""
from __future__ import annotations

from typing import Any

SCHEMA = "memweave.v1"
# RIB: independent-consensus weave (consensus-illusion guard) · verify: consensus_quality verdicts · tests: test_toolkit
TAU = 0.6  # Jaccard-overlap threshold: >= this => two answers are CORRELATED (not independent)


# ---------------------------------------------------------------- fan-out
def decompose(goal: str, n_bits: int) -> list[str]:
    """Decompose a goal into bite-sized deterministic bits (the task fan-out).

    Round-robin word bucketing into n_bits slices. Deterministic: same goal -> same bits.
    """
    n = max(1, int(n_bits))
    words = [w for w in (goal or "").split() if w]
    if not words:
        return [f"[memweave bit {i}] <empty goal>" for i in range(n)]
    buckets: list[list[str]] = [[] for _ in range(n)]
    for i, w in enumerate(words):
        buckets[i % n].append(w)
    return [f"[memweave bit {i}] {' '.join(b) if b else '(empty slice)'}"
            for i, b in enumerate(buckets)]


# ---------------------------------------------------------------- consensus guard
def _tok(s: str) -> set[str]:
    return set((s or "").lower().split())


def consensus_quality(answers: list[str], *, tau: float = TAU) -> dict[str, Any]:
    """Effective INDEPENDENT agreement across the flock's answers.

    Counts only answers that are NOT token-overlap-correlated with an already-counted one
    (Jaccard >= tau). Correlated answers collapse to a single opinion. Deterministic + $0.

    Returns {n_answers, n_independent, correlated, verdict}.
    Verdict: 'strong' if >=2 independent agree; 'correlated_weak' if they collapse;
             'single' if only one distinct opinion; 'empty' if no answers.
    """
    n = len(answers or [])
    if n == 0:
        return {"ok": True, "schema": "memweave.consensus.v1", "n_answers": 0,
                "n_independent": 0, "correlated": False, "verdict": "empty"}
    independent: list[int] = []
    for i in range(n):
        ti = _tok(answers[i])
        correlated = False
        for j in independent:
            tj = _tok(answers[j])
            if not ti or not tj:
                continue
            union = ti | tj
            if not union:
                continue
            if len(ti & tj) / len(union) >= tau:
                correlated = True
                break
        if not correlated:
            independent.append(i)
    n_ind = len(independent)
    verdict = ("strong" if n_ind >= 2 else
               "correlated_weak" if (n_ind < n and n >= 2) else
               "single")
    return {"ok": True, "schema": "memweave.consensus.v1", "n_answers": n,
            "n_independent": n_ind, "correlated": n_ind < n, "verdict": verdict,
            "independent_indices": independent}


# ---------------------------------------------------------------- weave
def weave(answers: list[str], *, tau: float = TAU) -> dict[str, Any]:
    """Combine the flock's answers by independent consensus.

    Returns the consensus verdict, the effective independent count, and the representative
    answer (the first independent one). A 'correlated_weak' or 'single' verdict means the
    flock did NOT produce trustworthy consensus — the caller should NOT treat it as strong.
    """
    q = consensus_quality(answers, tau=tau)
    idx = q["independent_indices"]
    consensus = (answers[idx[0]] if idx else None)
    return {"ok": True, "schema": SCHEMA, **{k: q[k] for k in
            ("n_answers", "n_independent", "correlated", "verdict")},
            "consensus": consensus}


if __name__ == "__main__":
    import json

    # 3 workers: two are independent, the third is a near-copy of the first (correlated)
    answers = [
        "route the heavy reasoning to the frontier model and keep the routine load local",
        "send expensive frontier reasoning elsewhere and run cheap routine work locally",
        "route the heavy reasoning to the frontier model and keep the routine load local",
    ]
    print(json.dumps(weave(answers), indent=2))
