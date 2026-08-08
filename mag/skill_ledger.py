"""Skill ledger — the "how far to the goal" counter + auto-produced items.

The system needs two things to right-size model use automatically:
  1. DECISIONS — verified routing decision+outcome pairs (case law), target ~100-1000,
     so the router learns which model + reasoning level works per task shape.
  2. LABELED ROWS — classified text rows for a home-grown LoRA classifier, target
     ~500-5000, produced by the "local bulk classify → DeepSeek sample audit" runner.

Every record is appended automatically (agent runs, router calls, classify runner)
and the counter is served over REST so the dashboard can show progress.

REST:
  GET  /api/v1/skill-ledger                  -> progress()
  POST /api/v1/skill-ledger/record           -> record_decision(body)
  POST /api/v1/skill-ledger/labeled-row      -> record_labeled_row(body)

CLI:
  main.py skill-ledger progress | record ... | labeled-row ... | seed-bench
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import ROOT

DECISIONS_PATH = ROOT / "memory" / "improve" / "skill_ledger.jsonl"
LABELED_PATH = ROOT / "memory" / "runs" / "classify" / "rows.jsonl"
BENCH_DIR = ROOT / "memory" / "runs" / "local_bench"

TARGETS = {"decisions": 1000, "labeled_rows": 5000}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _append(path: Path, row: dict[str, Any]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def _count(path: Path) -> int:
    if not path.is_file():
        return 0
    n = 0
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for _ in f:
            n += 1
    return n


def record_decision(
    *,
    goal: str,
    task_shape: str,
    provider: str,
    model: str,
    reasoning_level: str = "none",
    seat: str = "",
    outcome: str | None = None,
    detail: str = "",
    source: str = "router",
) -> dict[str, Any]:
    """Record one routing decision (+ optional verified outcome) as case law."""
    row = {
        "schema": "skill_ledger.decision.v1",
        "ts": _now(),
        "goal": (goal or "")[:300],
        "task_shape": task_shape,
        "provider": provider,
        "model": model,
        "reasoning_level": reasoning_level,
        "seat": seat,
        "outcome": outcome,  # None=decision only · ok/fail (verified)
        "detail": (detail or "")[:200],
        "source": source,
    }
    return _append(DECISIONS_PATH, row)


def record_labeled_row(
    *,
    text: str,
    label: str,
    classifier: str,
    confidence: float | None = None,
    audited_by: str | None = None,
    source: str = "classify_runner",
) -> dict[str, Any]:
    """Record one labeled row for the training pipeline (S-bin / eval fixtures)."""
    row = {
        "schema": "skill_ledger.labeled_row.v1",
        "ts": _now(),
        "text": (text or "")[:2000],
        "label": label,
        "classifier": classifier,
        "confidence": confidence,
        "audited_by": audited_by,
        "source": source,
    }
    return _append(LABELED_PATH, row)


def progress() -> dict[str, Any]:
    """Counter toward the targets — served over REST."""
    decisions = _count(DECISIONS_PATH)
    labeled = _count(LABELED_PATH)
    return {
        "ok": True,
        "schema": "skill_ledger.progress.v1",
        "decisions": decisions,
        "decisions_target": TARGETS["decisions"],
        "decisions_pct": round(100 * decisions / TARGETS["decisions"], 1),
        "labeled_rows": labeled,
        "labeled_target": TARGETS["labeled_rows"],
        "labeled_pct": round(100 * labeled / TARGETS["labeled_rows"], 2),
        "paths": {"decisions": str(DECISIONS_PATH), "labeled": str(LABELED_PATH)},
        "layman": (
            f"{decisions}/{TARGETS['decisions']} routing decisions · "
            f"{labeled}/{TARGETS['labeled_rows']} labeled rows"
        ),
    }


def seed_from_bench(*, limit: int = 200) -> dict[str, Any]:
    """Seed the ledger from the latest local_bench runs (task → model/outcome)."""
    if not BENCH_DIR.is_dir():
        return {"ok": False, "error": "no local_bench runs"}
    runs = sorted(BENCH_DIR.glob("*/results.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    added = 0
    for run in runs[:limit]:
        try:
            rows = json.loads(run.read_text(encoding="utf-8")).get("rows") or []
        except Exception:
            continue
        for r in rows:
            record_decision(
                goal=f"[bench] {r.get('task')}",
                task_shape=str(r.get("task")),
                provider=str(r.get("provider") or "ollama"),
                model=str(r.get("model")),
                reasoning_level="none",
                seat=str(r.get("provider") or "ollama"),
                outcome="ok" if r.get("ok") else "fail",
                detail=str(r.get("note") or "")[:100],
                source="bench",
            )
            added += 1
    return {"ok": True, "seeded": added, "progress": progress()}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="skill-ledger")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("progress")
    sub.add_parser("seed-bench")
    p_r = sub.add_parser("record")
    p_r.add_argument("--goal", required=True)
    p_r.add_argument("--task-shape", required=True)
    p_r.add_argument("--provider", default="ollama")
    p_r.add_argument("--model", required=True)
    p_r.add_argument("--reasoning", default="none")
    p_r.add_argument("--outcome", default=None)
    p_l = sub.add_parser("labeled-row")
    p_l.add_argument("--text", required=True)
    p_l.add_argument("--label", required=True)
    p_l.add_argument("--classifier", default="gemma4:latest")
    p_l.add_argument("--confidence", type=float, default=None)
    args = ap.parse_args(argv)

    if args.cmd == "progress":
        print(json.dumps(progress(), indent=2))
    elif args.cmd == "seed-bench":
        print(json.dumps(seed_from_bench(), indent=2, default=str))
    elif args.cmd == "record":
        r = record_decision(
            goal=args.goal, task_shape=args.task_shape, provider=args.provider,
            model=args.model, reasoning_level=args.reasoning, outcome=args.outcome,
        )
        print(json.dumps(r, indent=2))
    elif args.cmd == "labeled-row":
        r = record_labeled_row(text=args.text, label=args.label, classifier=args.classifier, confidence=args.confidence)
        print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
