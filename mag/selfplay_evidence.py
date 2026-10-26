"""Self-play evidence surface: append-only per-run masters plus a pointer file.

Move 6 (stockfish-door-20261007): the writer used to be last-write-wins on
one fixed name (memory/runs/selfplay/evidence_latest.json), so a rerun
destroyed the previous session's only record.  Evidence is now append-only:
each run lands its own timestamped file that is never rewritten, and
evidence_latest.pointer.json carries the pointer-plus-history shape the
dashboard already uses (dashboard/data/ESTATE_INDEX.pointer.json:
"pointer": true, "master": path, "ts", "note").
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

POINTER_NAME = "evidence_latest.pointer.json"


def write_session_evidence(
    report: Any, evidence_dir: Path
) -> tuple[Path, Path]:
    """Write one append-only evidence master and refresh the pointer file.

    report is a mag.selfplay_orchestrator.SessionReport (imported lazily by
    the caller to avoid a circular module import; duck-typed here).  Returns
    (evidence_path, pointer_path).
    """
    evidence_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    evidence_path = evidence_dir / f"evidence-{stamp}.json"
    suffix = 0
    while evidence_path.exists():
        # append-only allocator: a same-second rerun takes the next slot;
        # nothing already landed is ever overwritten
        suffix += 1
        evidence_path = evidence_dir / f"evidence-{stamp}-{suffix}.json"
    evidence_path.write_text(json.dumps(
        {
            "n_games": report.n_games,
            "n_correct": report.n_correct,
            "accuracy": report.accuracy,
            "elo": report.elo,
            "elo_vs_baseline": report.elo_vs_baseline,
            "avg_actor_ms": report.avg_actor_ms,
            "avg_scorer_ms": report.avg_scorer_ms,
            "bottleneck": report.bottleneck,
            "scorer_fallbacks": report.scorer_fallbacks,
            "scorer_ok_ratio": report.scorer_ok_ratio,
            "per_problem": report.per_problem,
        },
        indent=2,
    ))
    pointer_path = evidence_dir / POINTER_NAME
    pointer_path.write_text(json.dumps(
        {
            "pointer": True,
            "master": evidence_path.as_posix(),
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "n_games": report.n_games,
            "accuracy": report.accuracy,
            "elo": report.elo,
            "note": (
                "latest self-play session evidence; per-run masters are "
                "append-only; legacy evidence_latest.json predates Move 6 "
                "(2026-10-07) and is no longer written"
            ),
        },
        indent=2,
    ))
    return evidence_path, pointer_path
