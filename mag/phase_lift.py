"""phase_lift — test the ONE claim worth testing (operator tangent 2026-08-18).

THESIS: lifting real logits to complex (magnitude = probability, phase = a steerable
control signal) gives an ORTHOGONAL degree of freedom that can bias the token-collapse
rule without erasing the probability distribution.

    p = softmax(l / T),   z = p * e^{i*phi}

This module isolates that claim and A/B's it against ordinary greedy + temperature
sampling on MEASURABLE signals — steerability, distribution preservation (KL), and
coherence/diversity trade-off — NOT vibes.

HONEST SCOPE (the part that matters):
- This is PURE MATH on logits. It does not need a real model. We test the mechanism
  on synthetic logits first. If it can't move a controllable signal while keeping KL
  small on synthetic logits, wiring a real backend is pointless.
- Full V-dim logits are required (a truncated top-N logprobs vector would bias the very
  softmax we're trying to preserve). Real backends that expose full logits: Python
  transformers (model.forward().logits) or llama.cpp C++ (llama_get_logits). Chat APIs
  and Ollama's standard API do NOT give them. A backend adapter is intentionally NOT
  wired until the synthetic test passes.

Schema: phase_lift.v1 · deterministic · $0 · numpy-only (no torch required)
"""
from __future__ import annotations

import json
import math
import random
from typing import Any, Callable

import numpy as np

SCHEMA = "phase_lift.v1"


# ---------------------------------------------------------------------------
# Core mechanism (pure math, numpy)
# ---------------------------------------------------------------------------
def softmax(l: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    l = np.asarray(l, dtype=np.float64) / temperature
    l = l - l.max()  # numerical stability
    e = np.exp(l)
    return e / e.sum()


def complex_lift(logits: np.ndarray, temperature: float = 1.0,
                 phase: np.ndarray | None = None) -> np.ndarray:
    """z = p * e^{i*phi}; magnitude = probability, phase = control signal."""
    p = softmax(logits, temperature)
    if phase is None:
        phase = np.zeros_like(p)
    phase = np.asarray(phase, dtype=np.float64)
    return p * np.exp(1j * phase)


def phase_collapse(z: np.ndarray, mode: str = "aligned_greedy",
                   target_phase: float = 0.0, alpha: float = 1.0,
                   rng: random.Random | None = None) -> int:
    """Collapse rules, parametrized by phase strength alpha:

    score = |z| * (1 + alpha * cos(arg(z) - target))      (alpha=0 -> pure magnitude)

    - aligned_greedy: argmax of score
    - phase_biased_sample: sample from score normalized (soft, lower KL)
    - magnitude_only: plain argmax on |z| (baseline)
    """
    mag = np.abs(z)
    ang = np.angle(z)
    rng = rng or random.Random()

    if mode == "magnitude_only":
        return int(np.argmax(mag))
    # clip keeps the alignment weight non-negative even when alpha*cos < -1
    # (sweep surfaced NaN at alpha=2.0 from negative "probabilities").
    align = np.clip(1.0 + alpha * np.cos(ang - target_phase), 0.0, None)
    if mode == "aligned_greedy":
        score = mag * align
        return int(np.argmax(score))
    if mode == "phase_biased_sample":
        probs = mag * align
        probs = probs / probs.sum()
        return int(rng.choices(range(len(probs)), weights=probs.tolist(), k=1)[0])
    return int(np.argmax(mag))


def step_ab(logits: np.ndarray, phase: np.ndarray | None = None,
            temperature: float = 0.8, target_phase: float = 0.0,
            seed: int = 0) -> dict[str, int]:
    """One-step A/B: (greedy, temp_sample, phase_controlled)."""
    rng = random.Random(seed)
    logits = np.asarray(logits, dtype=np.float64)
    greedy = int(np.argmax(logits))
    temp_sample = int(rng.choices(range(len(logits)),
                                  weights=softmax(logits, temperature).tolist(), k=1)[0])
    z = complex_lift(logits, temperature, phase)
    controlled = phase_collapse(z, mode="aligned_greedy", target_phase=target_phase, rng=rng)
    return {"greedy": greedy, "temp_sample": temp_sample, "controlled": controlled}


# ---------------------------------------------------------------------------
# Synthetic logits generator with a KNOWN controllable direction
# ---------------------------------------------------------------------------
def synthetic_logits(vocab: int = 1000, *, groups: int = 4,
                     group_sep: float = 3.0, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """Create logits whose tokens have a latent 'direction' (a phase) we can steer.

    Returns (logits, token_phase) where token_phase[i] is the KNOWN latent phase of
    token i (from `groups` clusters). This gives us ground truth to test steerability:
    setting target_phase = cluster k's phase should pull output toward that cluster.

    FIXED (v2): the first `groups` tokens are the PEAKS — token t (t in 0..groups-1) has
    a high logit and phase = 2*pi*t/groups, so EVERY cluster has exactly one reachable
    peak. (v1 bug: vocab//groups peaks only landed in groups 0 and 2 because 250 % 4 != 0,
    so targets 1 and 3 were unreachable and the mechanism was never exercised.)
    """
    rng = np.random.default_rng(seed)
    token_phase = np.zeros(vocab)
    logits = np.zeros(vocab)
    for t in range(groups):
        token_phase[t] = 2.0 * math.pi * t / groups  # cluster centroid phase
        logits[t] = group_sep  # one reachable peak per cluster
    for i in range(groups, vocab):
        group = i % groups
        token_phase[i] = 2.0 * math.pi * group / groups
        logits[i] = rng.normal(0.0, 0.4)
    return logits, token_phase


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def kl(p: np.ndarray, q: np.ndarray) -> float:
    """KL(p || q) in nats. p,q must be valid distributions over same support."""
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)
    eps = 1e-12
    p = p / p.sum()
    q = q / q.sum()
    return float(np.sum(p * np.log((p + eps) / (q + eps))))


def _distribution(z: np.ndarray, mode: str, target_phase: float,
                  alpha: float = 1.0) -> np.ndarray:
    """Effective sampling distribution induced by a collapse mode (for KL)."""
    mag = np.abs(z)
    ang = np.angle(z)
    if mode == "magnitude_only":
        return mag / mag.sum()
    align = np.clip(1.0 + alpha * np.cos(ang - target_phase), 0.0, None)
    if mode == "aligned_greedy":
        score = mag * align
        score = score - score.min()
        s = score.sum()
        return score / s if s > 0 else mag / mag.sum()
    if mode == "phase_biased_sample":
        probs = mag * align
        return probs / probs.sum()
    return mag / mag.sum()


def _entropy(p: np.ndarray) -> float:
    p = np.asarray(p, dtype=np.float64)
    p = p[p > 0]
    if p.size == 0:
        return 0.0
    return float(-np.sum(p * np.log(p)))


def _topk_mass(p: np.ndarray, k: int = 10) -> float:
    p = np.asarray(p, dtype=np.float64)
    return float(np.sort(p)[::-1][:k].sum())


def evaluate(n_trials: int = 200, vocab: int = 1000, groups: int = 4,
             temperature: float = 0.8, seed: int = 0) -> dict[str, Any]:
    """A/B the phase-controlled collapse vs baselines on synthetic logits.

    Metrics (all concrete):
      - steerability: how often phase-controlled output lands in the target cluster,
        for each target_phase (0..groups-1). Baseline greedy has ~1/groups chance.
      - distribution preservation: mean KL(phase-implied-dist || original softmax).
      - determinism: fraction of identical outputs across seeds (greedy=1.0 baseline).
    """
    logits, token_phase = synthetic_logits(vocab, groups=groups, seed=seed)
    rng = random.Random(seed)

    # per-target-phase steerability (controlled vs greedy baseline)
    steer = {}
    for t in range(groups):
        target = 2.0 * math.pi * t / groups
        hits_ctrl = 0
        hits_greedy = 0
        for _ in range(n_trials):
            z = complex_lift(logits, temperature, token_phase)
            c = phase_collapse(z, mode="aligned_greedy", target_phase=target, rng=rng)
            g = int(np.argmax(logits))
            # match by cluster index, not raw phase (float equality / int-truncation
            # bug in v1: int(token_phase[c]) == target was never true except target 0)
            if round(abs(token_phase[c] - target), 6) < 0.01:
                hits_ctrl += 1
            if round(abs(token_phase[g] - target), 6) < 0.01:
                hits_greedy += 1
        steer[str(t)] = {
            "target_phase": round(target, 4),
            "controlled_hit_rate": round(hits_ctrl / n_trials, 4),
            "greedy_hit_rate": round(hits_greedy / n_trials, 4),
        }

    # distribution preservation: KL(phase-dist || softmax) vs baseline greedy-dist
    p_soft = softmax(logits, temperature)
    z = complex_lift(logits, temperature, token_phase)
    kl_aligned = kl(_distribution(z, "aligned_greedy", 0.0), p_soft)
    kl_biased = kl(_distribution(z, "phase_biased_sample", 0.0), p_soft)
    # greedy as a distribution = one-hot at argmax -> large KL vs softmax
    one_hot = np.zeros_like(p_soft)
    one_hot[int(np.argmax(logits))] = 1.0
    kl_greedy = kl(one_hot, p_soft)

    return {
        "schema": SCHEMA,
        "n_trials": n_trials, "vocab": vocab, "groups": groups, "temperature": temperature,
        "steerability_by_target": steer,
        "distribution_preservation_kl_nats": {
            "phase_aligned_greedy": round(kl_aligned, 4),
            "phase_biased_sample": round(kl_biased, 4),
            "plain_greedy_onehot": round(kl_greedy, 4),
        },
        "verdict_hint": (
            "real mechanism" if kl_biased < kl_greedy and kl_biased < 0.2 else
            "needs tuning / possibly decorative"
        ),
        "note": "Synthetic-logits test. Passes => wire a real full-logits backend "
                "(transformers or llama.cpp C++). Fails => don't build the backend.",
    }


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="phase_lift")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("test", help="single synthetic A/B")
    sw = sub.add_parser("sweep", help="temperature x alpha grid")
    sw.add_argument("--trials", type=int, default=300)
    sw.add_argument("--vocab", type=int, default=1000)
    sw.add_argument("--groups", type=int, default=4)
    sw.add_argument("--modes", nargs="*", default=["aligned_greedy", "phase_biased_sample"])
    a = ap.parse_args(argv)
    if a.cmd == "sweep":
        print(json.dumps(sweep(a.trials, a.vocab, a.groups, a.modes), indent=2))
    else:
        print(json.dumps(evaluate(), indent=2))
    return 0


def sweep(n_trials: int = 300, vocab: int = 1000, groups: int = 4,
          modes: list[str] | None = None) -> dict[str, Any]:
    """Grid: temperature x alpha. Reports steerability, KL vs softmax, entropy, top-10 mass.

    Decides (per operator rule): keep steerability >= 0.95 while KL stays comfortably below
    plain-greedy and competitive with mild temperature sampling -> proceed to real backend.
    """
    modes = modes or ["aligned_greedy", "phase_biased_sample"]
    temperatures = [0.6, 0.8, 1.0, 1.2]
    alphas = [0.0, 0.25, 0.5, 1.0, 2.0]

    logits, token_phase = synthetic_logits(vocab, groups=groups)
    p_soft = softmax(logits, 1.0)  # entropy / top-mass reference at T=1

    rows: list[dict[str, Any]] = []
    for T in temperatures:
        pT = softmax(logits, T)
        for mode in modes:
            for alpha in alphas:
                rng = random.Random(0)
                hits = 0
                for t in range(groups):
                    target = 2.0 * math.pi * t / groups
                    for _ in range(n_trials // groups):
                        z = complex_lift(logits, T, token_phase)
                        c = phase_collapse(z, mode=mode, target_phase=target,
                                           alpha=alpha, rng=rng)
                        if abs(token_phase[c] - target) < 0.01:
                            hits += 1
                steer = hits / n_trials
                z = complex_lift(logits, T, token_phase)
                d = _distribution(z, mode, 0.0, alpha)
                kld = kl(d, pT)
                ent = _entropy(d)
                topk = _topk_mass(d, 10)
                rows.append({
                    "T": T, "mode": mode, "alpha": alpha,
                    "steer": round(steer, 3), "kl_nats": round(kld, 4),
                    "entropy": round(ent, 3), "top10_mass": round(topk, 4),
                })

    # reference baselines
    pT1 = softmax(logits, 1.0)
    greedy_dist = np.zeros_like(pT1); greedy_dist[int(np.argmax(logits))] = 1.0
    ref = {
        "softmax_entropy": round(_entropy(pT1), 3),
        "softmax_top10_mass": round(_topk_mass(pT1, 10), 4),
        "plain_greedy_kl_nats": round(kl(greedy_dist, pT1), 4),
    }

    # Pareto: rows with steer >= 0.95, min KL per (T, mode)
    pareto = [r for r in rows if r["steer"] >= 0.95]
    pareto.sort(key=lambda r: r["kl_nats"])
    best = pareto[0] if pareto else None

    return {
        "schema": SCHEMA, "grid": {"temperatures": temperatures, "alphas": alphas},
        "n_trials": n_trials, "vocab": vocab, "groups": groups,
        "reference": ref,
        "rows": rows,
        "pareto_steer_ge_095": pareto,
        "best_by_kl": best,
        "verdict": (
            "proceed_to_real_backend" if (best and best["kl_nats"] < 0.20) else
            "retire_idea_or_retune"
        ),
    }


if __name__ == "__main__":
    raise SystemExit(main())
