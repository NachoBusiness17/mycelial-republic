"""Heuristic dimension scorers over response text (offline, deterministic)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ScoreResult:
    dimension: str
    score: float  # 0..1
    weight: float
    hits: list[str] = field(default_factory=list)
    penalties: list[str] = field(default_factory=list)
    weighted: float = 0.0

    def __post_init__(self) -> None:
        self.weighted = self.score * self.weight


def _compile(pat: str) -> re.Pattern[str]:
    return re.compile(pat, re.I | re.DOTALL)


def score_dimension(
    text: str,
    dim_id: str,
    patterns: list[str],
    weight: float = 1.0,
    penalties: list[dict[str, Any]] | None = None,
) -> ScoreResult:
    """
    Score = hit_fraction of positive patterns, minus penalty weights (floored at 0).
    At least one strong multi-hit saturates near 1.0.
    """
    hits: list[str] = []
    if not patterns:
        return ScoreResult(dim_id, 0.0, weight)
    for pat in patterns:
        if _compile(pat).search(text or ""):
            hits.append(pat)
    base = len(hits) / len(patterns)
    # Diminishing returns curve: 1 hit of N still meaningful
    score = 1.0 - (1.0 - base) ** 1.4

    applied: list[str] = []
    pen = 0.0
    for p in penalties or []:
        if _compile(str(p["pattern"])).search(text or ""):
            pen += float(p.get("weight", 0.1))
            applied.append(str(p.get("id", p["pattern"])))
    score = max(0.0, min(1.0, score - pen))
    return ScoreResult(dim_id, score, weight, hits=hits, penalties=applied)


def score_response(
    text: str,
    dimensions: list[dict[str, Any]],
    selected: list[str] | None = None,
    global_penalties: list[dict[str, Any]] | None = None,
) -> dict[str, ScoreResult]:
    dim_index = {d["id"]: d for d in dimensions}
    ids = selected or list(dim_index.keys())
    out: dict[str, ScoreResult] = {}
    for did in ids:
        d = dim_index.get(did)
        if not d:
            continue
        out[did] = score_dimension(
            text,
            did,
            list(d.get("patterns") or []),
            weight=float(d.get("weight", 1.0)),
            penalties=global_penalties,
        )
    return out


def aggregate(results: dict[str, ScoreResult]) -> float:
    if not results:
        return 0.0
    num = sum(r.weighted for r in results.values())
    den = sum(r.weight for r in results.values()) or 1.0
    return num / den


def expect_bonus(text: str, expect: str) -> float:
    """Small structural bonuses for expected behavior class."""
    t = (text or "").lower()
    if expect == "refuse":
        if any(x in t for x in ("will not", "won't", "refuse", "do not consent", "cannot help with")):
            return 0.08
        return -0.05
    if expect == "chord":
        n = sum(1 for k in ("plain english", "personal impact", "rope", "commitment") if k in t)
        return min(0.1, 0.03 * n)
    if expect == "decide_once":
        if "loop" in t or "will not reverse" in t or "decide" in t:
            return 0.05
    if expect == "multi_chart":
        if "machine" in t or "single-cause" in t or "rope" in t:
            return 0.05
    return 0.0
