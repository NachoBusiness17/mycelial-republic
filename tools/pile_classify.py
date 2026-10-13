"""Pile classifier — the long overnight classification job.

Drains the local pile (memory/pile/state_summaries.jsonl) that escalations and
session-close captures feed, classifies each entry with a LOCAL model (free,
offline-safe), and folds the classifications into case law + training rows.

Designed to run during downtime: on the scheduler, a night task, or GitHub
Actions. Idempotent — classified ids are skipped on re-run.

  escalation → pile (wired in decision_framework.escalate_on_loop)
  session close / run close → pile (mag.state_snapshot.capture_summary)
  Overnight: python tools/pile_classify.py [--once] [--limit 50] [--model gemma4:latest]

Output:
  memory/pile/classified.jsonl      classified rows (idempotent by id)
  memory/pile/training_rows.jsonl   training rows (feeds train/prepare.py)
  skill_ledger                       case-law fold (record_decision)

Write-back: every id landed in classified.jsonl is flagged classified=true
back into state_summaries.jsonl (atomic rewrite). Without this the in-pile
flag never moves and mag.state_snapshot.status() counts the rows as
unclassified forever (fix for the 2026-09-25 wave-1 tier-2 verdict).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import ROOT  # noqa: E402

from mag.state_snapshot import CLASSIFIED, PILE, TRAINING  # noqa: E402

CLASSIFY_SYSTEM = (
    "You are a training-data classifier for an agent framework. Given ONE state summary, "
    "output STRICT JSON only, no prose, with exactly these keys: "
    '{"category": "escalation|loop|success|design|exec|process|unknown", '
    '"lesson_kind": "metric_bug|assumption_falsified|guardrail|tooling|process|unknown", '
    '"recommendation": "<one short actionable sentence>", '
    '"tags": ["<1-3 short tags>"]}.'
)


def _extract_json(text: str) -> dict[str, Any] | None:
    m = re.search(r"\{.*\}", (text or ""), re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
        return d if isinstance(d, dict) else None
    except (json.JSONDecodeError, TypeError):
        return None


def _read_lines(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    out = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def classify_one(row: dict[str, Any], *, model: str, timeout: float = 240.0) -> dict[str, Any]:
    from tools.pupeteer_gauntlet import local_chat

    user = "State summary:\n" + json.dumps({k: row.get(k) for k in ("id", "kind", "tier", "goal", "outcome", "lessons")}, ensure_ascii=False)
    text = local_chat(model, CLASSIFY_SYSTEM, user, temperature=0.2, timeout=timeout)
    cls = _extract_json(text) or {
        "category": "unknown", "lesson_kind": "unknown", "recommendation": "", "tags": []
    }
    return cls


def run_pile(*, model: str, limit: int | None = None, fold: bool = True, timeout: float = 240.0) -> dict[str, Any]:
    rows = _read_lines(PILE)
    done = {r.get("id") for r in _read_lines(CLASSIFIED)}
    pending = [r for r in rows if r.get("id") not in done and not r.get("classified")]
    if limit:
        pending = pending[:limit]

    classified_out: list[dict[str, Any]] = []
    errors: list[str] = []
    for row in pending:
        try:
            cls = classify_one(row, model=model, timeout=timeout)
            row.update({**cls, "classified": True, "classified_ts": datetime.now(timezone.utc).isoformat()})
            _append(CLASSIFIED, row)
            classified_out.append(row)
            if fold:
                _fold(row)
        except Exception as e:  # noqa: BLE001
            errors.append(f"{row.get('id')}: {str(e)[:120]}")

    # write-back: flag classified=true in the source pile for every id that
    # exists in classified.jsonl (historical backlog + this run), so the
    # in-pile flag mag.state_snapshot.status() counts finally moves.
    written = _write_back(done | {r["id"] for r in classified_out})

    return {
        "ok": True,
        "schema": "pile_classify.v1",
        "model": model,
        "pile": len(rows),
        "pending": len(pending),
        "classified_this_run": len(classified_out),
        "pile_writeback": written,
        "errors": errors,
        "classified_total": len(done) + len(classified_out),
    }


def _write_back(ids: set[Any]) -> int:
    """Flag classified=true on pile rows whose id is in ids. Atomic rewrite.

    Reads raw lines (not _read_lines) so an unparseable historical line is
    preserved verbatim instead of silently dropped from the record.
    """
    if not PILE.is_file() or not ids:
        return 0
    out: list[str] = []
    changed = 0
    for line in PILE.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            out.append(line)  # preserve verbatim, never drop record lines
            continue
        if row.get("id") in ids and not row.get("classified"):
            row["classified"] = True
            changed += 1
        out.append(json.dumps(row, ensure_ascii=False))
    tmp = PILE.with_suffix(".jsonl.tmp")
    tmp.write_text("\n".join(out) + "\n", encoding="utf-8")
    tmp.replace(PILE)
    return changed


def _append(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def _fold(row: dict[str, Any]) -> None:
    """Fold a classified row into case law + a training row."""
    try:
        from mag.skill_ledger import record_decision

        record_decision(
            goal=row.get("goal") or f"pile:{row.get('id')}",
            task_shape=f"pile:{row.get('category', 'unknown')}",
            provider=row.get("tier") or "local",
            model=row.get("category") or "unknown",
            reasoning_level="none",
            seat="pile-classifier",
            outcome=row.get("outcome") or "unknown",
            detail=(row.get("recommendation") or row.get("lessons") or [""])[0][:200] if isinstance(row.get("lessons"), list) else str(row.get("recommendation") or "")[:200],
            source="pile_classify",
        )
    except Exception:
        pass
    # training row (feeds train/prepare.py)
    train = {
        "instruction": f"Classify this state: {row.get('goal', '')[:200]}",
        "output": json.dumps({"category": row.get("category"), "lesson_kind": row.get("lesson_kind"),
                              "tags": row.get("tags"), "outcome": row.get("outcome")}, ensure_ascii=False),
        "meta": {"source": "pile_classify", "id": row.get("id"), "tier": row.get("tier")},
    }
    _append(TRAINING, train)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="pile-classify", description="Overnight local classification of the state pile.")
    ap.add_argument("--model", default="gemma4:latest")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--no-fold", action="store_true", help="classify but skip ledger/training fold")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    res = run_pile(model=args.model, limit=args.limit, fold=not args.no_fold)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"pile={res['pile']} pending={res['pending']} classified_this_run={res['classified_this_run']} "
              f"total_classified={res['classified_total']} errors={len(res['errors'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
