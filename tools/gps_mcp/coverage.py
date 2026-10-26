"""pass@K coverage diagnostic beside win rate - EG-20 (eleven-doors, 2026-10-05).

The Sharpening Tax steal (arXiv 2610.01509, X_INTEL_PAPERS #2): win rate
(pass@1) alone cannot predict when a mesh of cheap attempts beats one
premium shot - post-training trades coverage for pass@1, so the two
diverge exactly where routing dollars should move. This module adds the
missing column to the GPS capability battery:

  win rate  = mean binary verdict per model (capability.pass_rate, pass@1)
  pass@K    = fraction of PROBLEMS where ANY of K fleet attempts passed

The problem key comes from the evidence, never a guess: every
evidence_resolved gwap row carries the canonical row core, whose payload
holds scene_id. Arena scene_ids are "arena-<run>-<actor>" - the SAME run
is the same scenario every fighter attempted, so the run is the shared
problem (verified on production bytes 2026-10-05: 209 keyed / 58
problems / 4 models; the 252 unkeyed rows are exactly the pre-a04
evidence_resolved=0 class, excluded AND reported, never silently
re-denominated - the census-denominator law).

Read-only over the same sqlite file the ledger owns; no writes, no
schema change. The routing verdict (mesh_vs_frontier) is a diagnostic:
the router itself stays the decision surface; this predicts what it
should decide.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# A prediction from fewer keyed problems than this is INSUFFICIENT, never
# a routing signal (thin-air coverage is the fabrication class the
# census-denominator law forbids).
MIN_PROBLEMS_FLOOR = 10


@dataclass
class ModelRow:
    model_id: str
    attempts: int
    passes: int

    @property
    def pass_at_1(self) -> float:
        return self.passes / self.attempts if self.attempts else 0.0


@dataclass
class CoverageReport:
    task_shape: str
    keyed_rows: int
    excluded_rows: int
    problems: int
    k_distribution: dict[int, int]
    models: list[ModelRow] = field(default_factory=list)
    fleet_pass_at_k: float = 0.0
    fleet_solved: int = 0
    best_single_model: str | None = None
    best_single_pass_at_1: float = 0.0
    coverage_gain: float = 0.0

    def as_dict(self) -> dict[str, Any]:
        return {
            "task_shape": self.task_shape,
            "keyed_rows": self.keyed_rows,
            "excluded_rows": self.excluded_rows,
            "problems": self.problems,
            "k_distribution": {str(k): v for k, v in sorted(self.k_distribution.items())},
            "models": [
                {"model_id": m.model_id, "attempts": m.attempts,
                 "passes": m.passes, "pass_at_1": round(m.pass_at_1, 4)}
                for m in self.models
            ],
            "fleet_pass_at_k": round(self.fleet_pass_at_k, 4),
            "fleet_solved": self.fleet_solved,
            "best_single_model": self.best_single_model,
            "best_single_pass_at_1": round(self.best_single_pass_at_1, 4),
            "coverage_gain": round(self.coverage_gain, 4),
        }


def problem_key(evidence_bytes: bytes | None, *, evidence_resolved: bool = True) -> str | None:
    """Problem key from the canonical gwap row core, or None.

    "arena-<run>-<actor>" keys to the run (the shared scenario every
    fighter attempted). Any other scene_id keys to itself (the scene is
    the problem). Unresolved evidence, unparseable bytes, or a payload
    without scene_id key to None - excluded and reported, never guessed.
    """
    if not evidence_resolved or not evidence_bytes:
        return None
    try:
        core = json.loads(evidence_bytes.decode("utf-8"))
        sid = core["payload"]["scene_id"]
    except Exception:  # noqa: BLE001 - any shape drift is an exclusion, not a crash
        return None
    if not isinstance(sid, str) or not sid:
        return None
    parts = sid.split("-")
    if len(parts) >= 3 and parts[0] == "arena":
        return "-".join(parts[:-1])
    return sid


def coverage_report(
    db: sqlite3.Connection | str | Path,
    task_shape: str,
    *,
    models: list[str] | None = None,
) -> CoverageReport:
    """Compute the pass@K column beside win rate for one task shape."""
    if isinstance(db, (str, Path)):
        conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        try:
            return coverage_report(conn, task_shape, models=models)
        finally:
            conn.close()
    rows = db.execute(
        "SELECT model_id, verdict, evidence_bytes, evidence_resolved"
        " FROM verdict_log WHERE task_shape = ?",
        (task_shape,),
    ).fetchall()

    by_problem: dict[str, list[tuple[str, int]]] = defaultdict(list)
    per_model: dict[str, list[int]] = defaultdict(list)
    keyed = excluded = 0
    for model_id, verdict, evidence_bytes, evidence_resolved in rows:
        if models is not None and model_id not in models:
            continue
        key = problem_key(evidence_bytes, evidence_resolved=bool(evidence_resolved))
        if key is None:
            excluded += 1
            continue
        keyed += 1
        by_problem[key].append((model_id, int(verdict)))
        per_model[model_id].append(int(verdict))

    report = CoverageReport(
        task_shape=task_shape,
        keyed_rows=keyed,
        excluded_rows=excluded,
        problems=len(by_problem),
        k_distribution=Counter(len(ps) for ps in by_problem.values()),
    )
    report.models = sorted(
        (ModelRow(m, len(vs), sum(vs)) for m, vs in per_model.items()),
        key=lambda r: (-r.pass_at_1, r.model_id),
    )
    solved = sum(1 for ps in by_problem.values() if any(v for _, v in ps))
    report.fleet_solved = solved
    report.fleet_pass_at_k = solved / report.problems if report.problems else 0.0
    # best single on problems it actually attempted, with an attempt floor
    # so a one-shot 1/1 model never wears the crown (n>=10 matches the
    # estate's small-sample skepticism on the same data)
    ranked = [r for r in report.models if r.attempts >= MIN_PROBLEMS_FLOOR]
    if ranked:
        best = ranked[0]
        report.best_single_model = best.model_id
        report.best_single_pass_at_1 = best.pass_at_1
        report.coverage_gain = report.fleet_pass_at_k - best.pass_at_1
    return report


ROUTE_MESH = "ROUTE_MESH"
ROUTE_FRONTIER = "ROUTE_FRONTIER"
INSUFFICIENT = "INSUFFICIENT"


@dataclass
class MeshVsFrontier:
    verdict: str
    task_shape: str
    problems: int
    mesh_models: list[str]
    mesh_pass_at_k: float
    frontier_models: list[str]
    frontier_pass_at_1: float
    margin: float
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "verdict": self.verdict,
            "task_shape": self.task_shape,
            "problems": self.problems,
            "mesh_models": self.mesh_models,
            "mesh_pass_at_k": round(self.mesh_pass_at_k, 4),
            "frontier_models": self.frontier_models,
            "frontier_pass_at_1": round(self.frontier_pass_at_1, 4),
            "margin": round(self.margin, 4),
            "reason": self.reason,
        }


def mesh_vs_frontier(
    db: sqlite3.Connection | str | Path,
    task_shape: str,
    *,
    mesh_models: list[str],
    frontier_models: list[str],
    margin: float = 0.05,
) -> MeshVsFrontier:
    """Predict the routing split: any-of-K mesh attempts vs best frontier pass@1.

    The mesh side reuses coverage_report keyed to the mesh models' rows
    (fleet pass@K at realized K); the frontier side is the best single
    pass@1 among frontier models on the same battery. Verdict:
      ROUTE_MESH     mesh_pass_at_k beats frontier by more than margin
      ROUTE_FRONTIER frontier wins by more than margin
      INSUFFICIENT   inside the margin, or below the problems floor -
                     no prediction from thin air either way
    """
    mesh = coverage_report(db, task_shape, models=mesh_models)
    frontier = coverage_report(db, task_shape, models=frontier_models)
    mesh_k = mesh.fleet_pass_at_k
    frontier_1 = frontier.best_single_pass_at_1
    problems = min(mesh.problems, frontier.problems)
    if problems < MIN_PROBLEMS_FLOOR:
        verdict, reason = INSUFFICIENT, (
            f"{problems} shared keyed problems < floor {MIN_PROBLEMS_FLOOR}"
        )
    elif mesh_k - frontier_1 > margin:
        verdict, reason = ROUTE_MESH, (
            f"fleet coverage {mesh_k:.3f} beats best frontier {frontier_1:.3f}"
            f" by more than {margin}"
        )
    elif frontier_1 - mesh_k > margin:
        verdict, reason = ROUTE_FRONTIER, (
            f"best frontier {frontier_1:.3f} beats fleet coverage {mesh_k:.3f}"
            f" by more than {margin}"
        )
    else:
        verdict, reason = INSUFFICIENT, (
            f"inside margin {margin}: mesh {mesh_k:.3f} vs frontier {frontier_1:.3f}"
        )
    return MeshVsFrontier(
        verdict=verdict,
        task_shape=task_shape,
        problems=problems,
        mesh_models=mesh_models,
        mesh_pass_at_k=mesh_k,
        frontier_models=frontier_models,
        frontier_pass_at_1=frontier_1,
        margin=margin,
        reason=reason,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--db", default=str(Path(__file__).parent / "gps_ledger.db3"))
    parser.add_argument("--task-shape", default="arena-agreement-v1")
    parser.add_argument("--k-hint", type=int, default=None,
                        help="report fixed-k pass@k over problems with >= k attempts")
    parser.add_argument("--mesh", default=None, help="comma-separated mesh (cheap fleet) model ids")
    parser.add_argument("--frontier", default=None, help="comma-separated frontier model ids")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    args = parser.parse_args(argv)

    report = coverage_report(args.db, args.task_shape)
    lines: list[str] = []

    def emit(line: str = "") -> None:
        lines.append(line)

    emit(f"GPS COVERAGE: task_shape={args.task_shape}")
    emit(
        f"  keyed={report.keyed_rows} excluded(unresolved/no-core)={report.excluded_rows}"
        f" problems={report.problems}"
        f" K-dist={dict(sorted(report.k_distribution.items()))}"
    )
    emit(f"  {'model':40s} {'attempts':>8s} {'win rate':>9s} (pass@1)")
    for m in report.models:
        emit(f"  {m.model_id:40s} {m.attempts:8d} {m.pass_at_1:9.3f}")
    emit(
        f"  FLEET pass@K (any of realized K)     {report.fleet_solved}/{report.problems}"
        f" = {report.fleet_pass_at_k:.3f}"
    )
    if report.best_single_model:
        emit(
            f"  best single: {report.best_single_model} = {report.best_single_pass_at_1:.3f}"
            f"   coverage gain {report.coverage_gain:+.3f}"
        )
    if args.k_hint:
        conn = sqlite3.connect(f"file:{args.db}?mode=ro", uri=True)
        try:
            rows = conn.execute(
                "SELECT verdict, evidence_bytes, evidence_resolved FROM verdict_log"
                " WHERE task_shape = ?",
                (args.task_shape,),
            ).fetchall()
        finally:
            conn.close()
        by_problem = defaultdict(list)
        for verdict, evidence_bytes, evidence_resolved in rows:
            key = problem_key(evidence_bytes, evidence_resolved=bool(evidence_resolved))
            if key is not None:
                by_problem[key].append(int(verdict))
        elig = [ps for ps in by_problem.values() if len(ps) >= args.k_hint]
        if elig:
            solved = sum(1 for ps in elig if any(ps))
            emit(
                f"  FLEET pass@{args.k_hint} (problems with >= {args.k_hint} attempts)"
                f"   {solved}/{len(elig)} = {solved / len(elig):.3f}"
            )
        else:
            emit(f"  FLEET pass@{args.k_hint}: no problem has >= {args.k_hint} attempts")
    if args.mesh and args.frontier:
        mesh_models = [m.strip() for m in args.mesh.split(",") if m.strip()]
        frontier_models = [m.strip() for m in args.frontier.split(",") if m.strip()]
        verdict = mesh_vs_frontier(
            args.db, args.task_shape, mesh_models=mesh_models, frontier_models=frontier_models
        )
        emit()
        emit(
            f"  ROUTING PREDICTION: {verdict.verdict} - {verdict.reason}"
        )
        emit(
            f"    mesh (any-of-K) {verdict.mesh_pass_at_k:.3f}"
            f" vs frontier (best pass@1) {verdict.frontier_pass_at_1:.3f}"
            f" on {verdict.problems} shared problems"
        )

    text = "\n".join(lines)
    if args.json:
        payload: dict[str, Any] = report.as_dict()
        if args.mesh and args.frontier:
            payload["routing"] = mesh_vs_frontier(
                args.db,
                args.task_shape,
                mesh_models=[m.strip() for m in args.mesh.split(",") if m.strip()],
                frontier_models=[m.strip() for m in args.frontier.split(",") if m.strip()],
            ).as_dict()
        print(json.dumps(payload, indent=1))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
