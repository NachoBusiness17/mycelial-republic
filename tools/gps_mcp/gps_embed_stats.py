"""Model-free statistics + split helpers for the GPS embedding trial.

Kept free of the ONNX pull (and of ledger imports) so the fleet test
suite can exercise the trial's arithmetic on any seat; see
tools/gps_mcp/gps_embed_trial.py for the trial itself and
watch/inbox/gps_embed/GPS_EMBED_TRIAL.md for the landed numbers.
"""

from __future__ import annotations

import math
import random
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Any, Optional

import numpy as np

TRIAL_SEED = 20261006
HOLDOUT_FRACTION = 0.3
KNN_K = 3


def wilson_ci(correct: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return (0.0, 0.0)
    p = correct / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def mcnemar_exact_p(b: int, c: int) -> float:
    """Exact McNemar test p-value (two-sided binomial on discordant pairs)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(0, k + 1)) * (0.5 ** n)
    return min(1.0, 2 * tail)


def knn_vote(
    query: np.ndarray,
    candidates: dict[str, np.ndarray],
    labels: dict[str, str],
    k: int = KNN_K,
) -> tuple[Optional[str], list[dict[str, Any]]]:
    """kNN over candidate shape vectors; majority vote of the neighbors'
    winner labels; distance-tie broken toward the NEAREST labeled
    neighbor. Note the filed rule's bite: an exact self-match (cosine
    1.0) can be OUTVOTED 2-1 by cross-shape neighbors - the grading
    misses in the landed trial are exactly this, banked in the receipt.
    """
    if not candidates:
        return None, []
    sims = {
        s: float(np.dot(query, v) / (np.linalg.norm(query) * np.linalg.norm(v) + 1e-12))
        for s, v in candidates.items()
    }
    ranked = sorted(sims.items(), key=lambda kv: (-kv[1], kv[0]))
    top = ranked[: min(k, len(ranked))]
    detail = [
        {"neighbor_shape": s, "cosine": round(sim, 6), "winner": labels[s]}
        for s, sim in top
    ]
    votes: Counter[str] = Counter(labels[s] for s, _ in top)
    best = max(votes.values())
    tied = sorted(m for m, n_votes in votes.items() if n_votes == best)
    if len(tied) == 1:
        return tied[0], detail
    for s, _ in top:  # tie: nearest neighbor in the tied set wins
        if labels[s] in tied:
            return labels[s], detail
    return None, detail  # unreachable, keeps the signature honest


def read_verdict_rows(ledger_db: Path | str) -> list[dict[str, Any]]:
    """All verdict_log rows in rowid order, read-only."""
    con = sqlite3.connect(f"file:{ledger_db}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    try:
        cur = con.execute(
            "SELECT rowid AS id, ts, model_id, task_shape, verdict"
            " FROM verdict_log ORDER BY rowid"
        )
        return [dict(r) for r in cur.fetchall()]
    finally:
        con.close()


def stratified_holdout(
    rows: list[dict[str, Any]],
    fraction: float = HOLDOUT_FRACTION,
    seed: int = TRIAL_SEED,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Per-shape deterministic holdout. Every shape with n >= 2 keeps at
    least one row in train (a train-empty shape would make method A's
    string key miss by construction instead of by evidence, and the
    split must not decide the race)."""
    by_shape: dict[str, list[dict[str, Any]]] = {}
    for r in rows:
        by_shape.setdefault(r["task_shape"], []).append(r)
    train: list[dict[str, Any]] = []
    held: list[dict[str, Any]] = []
    for shape in sorted(by_shape):
        group = by_shape[shape]
        rng = random.Random(f"{seed}:{shape}")
        order = list(range(len(group)))
        rng.shuffle(order)
        n_hold = round(fraction * len(group))
        if len(group) >= 2:
            n_hold = min(n_hold, len(group) - 1)
        else:
            n_hold = 0
        hold_ids = {order[i] for i in range(n_hold)}
        for i, r in enumerate(group):
            (held if i in hold_ids else train).append(r)
    return train, held
