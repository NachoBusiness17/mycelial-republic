"""Auto-promote gate (Q-002, 2026-09-28): one test, the full deterministic matrix.

The tmp ledger drives the REAL promote path: mag.improve.load_config is
monkeypatched so promote_apply's ensure_dirs()/read_candidates land on tmp_path
and the real memory/improve/candidates.jsonl is never touched. promote_apply
itself runs unpatched (mirror lens + playbook append + status rewrite).
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

NOW = datetime(2026, 9, 28, 12, 0, 0, tzinfo=timezone.utc)


def _row(cid: str, *, kind: str, feasible: object, status: str, created: object) -> dict:
    row = {"schema": "improve_candidate.v1", "id": cid, "kind": kind, "claim": f"claim {cid}",
           "detail": "", "source": "pytest", "source_urls": [], "local_feasible": feasible,
           "status": status}
    if created is not None:
        row["created"] = created
    else:
        row["date"] = (NOW - timedelta(days=3)).strftime("%Y-%m-%d")
    return row


def test_auto_promote_gate(tmp_path, monkeypatch):
    import mag.improve as imp
    from tools.auto_promote import eligibility, run

    cfg = {
        "enabled": True,
        "paths": {
            "root": tmp_path,
            "daily": tmp_path / "daily",
            "evals": tmp_path / "evals",
            "candidates": tmp_path / "candidates.jsonl",
            "playbook": tmp_path / "playbook.md",
            "state": tmp_path / "state.json",
        },
    }
    monkeypatch.setattr(imp, "load_config", lambda: cfg)
    # B2-402 isolation: the tesuji promote rides promote_apply's generic branch,
    # which emits a promote_gate training event; redirect the sink to tmp.
    import mag.training_events as te

    monkeypatch.setattr(te, "EVENTS_PATH", tmp_path / "training_events.jsonl")

    rows = [
        # eligible: practice, feasible string "true", 49h old, new
        _row("c-eligible-practice", kind="practice", feasible="true", status="new",
             created=(NOW - timedelta(hours=49)).isoformat()),
        # eligible: tesuji, feasible as real bool, no created (date fallback), hold
        _row("c-eligible-tesuji", kind="tesuji", feasible=True, status="hold", created=None),
        # eligible at the exact 48h boundary (>= is the bar)
        _row("c-boundary", kind="practice", feasible="yes", status="new",
             created=(NOW - timedelta(hours=48)).isoformat()),
        # skipped: fresh (1h old)
        _row("c-fresh", kind="practice", feasible="true", status="new",
             created=(NOW - timedelta(hours=1)).isoformat()),
        # skipped: local_feasible "unknown"
        _row("c-unknown", kind="practice", feasible="unknown", status="new",
             created=(NOW - timedelta(days=7)).isoformat()),
        # skipped: kind model (human gate)
        _row("c-model", kind="model", feasible="true", status="new",
             created=(NOW - timedelta(days=7)).isoformat()),
        # skipped: already rejected
        _row("c-rejected", kind="practice", feasible="true", status="rejected",
             created=(NOW - timedelta(days=7)).isoformat()),
        # skipped: unparseable timestamp, fail-closed
        _row("c-badts", kind="practice", feasible="true", status="new", created="not-a-timestamp"),
    ]
    ledger = tmp_path / "candidates.jsonl"
    ledger.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8"
    )

    # dry: the same three eligible, nothing written
    dry = run(dry=True, now=NOW, paths=cfg["paths"])
    assert dry["ok"] is True and dry["scanned"] == 8
    assert sorted(e["id"] for e in dry["promoted"]) == [
        "c-boundary", "c-eligible-practice", "c-eligible-tesuji",
    ]
    assert dry["promoted"][0]["action"] == "would_promote"
    assert all(r["status"] == orig["status"] for r, orig in zip(
        [json.loads(l) for l in ledger.read_text(encoding="utf-8").splitlines()], rows))

    # real apply: exactly the eligible three promoted via promote_apply
    res = run(dry=False, now=NOW, paths=cfg["paths"])
    assert res["ok"] is True
    assert sorted(e["id"] for e in res["promoted"]) == [
        "c-boundary", "c-eligible-practice", "c-eligible-tesuji",
    ]
    assert res["blocked"] == []
    assert res["skipped"] == {"age": 2, "kind": 1, "local_feasible": 1, "status": 1}

    after = {r["id"]: r for r in
             (json.loads(l) for l in ledger.read_text(encoding="utf-8").splitlines())}
    assert after["c-eligible-practice"]["status"] == "promoted"
    assert after["c-eligible-tesuji"]["status"] == "promoted"
    assert after["c-boundary"]["status"] == "promoted"
    assert "auto-promote" in after["c-eligible-practice"]["note"]
    # practice kind landed the playbook entry through promote_apply
    assert "c-eligible-practice" in (tmp_path / "playbook.md").read_text(encoding="utf-8")
    # ineligible rows untouched
    assert after["c-fresh"]["status"] == "new"
    assert after["c-unknown"]["status"] == "new"
    assert after["c-model"]["status"] == "new"
    assert after["c-rejected"]["status"] == "rejected"
    assert after["c-badts"]["status"] == "new"
    # audit rows: one per applied decision
    audit = tmp_path / "auto_promote.jsonl"
    assert sum(1 for _ in audit.open(encoding="utf-8")) == 3

    # idempotent: second run promotes nothing (statuses no longer open)
    again = run(dry=False, now=NOW, paths=cfg["paths"])
    assert again["promoted"] == []
    # the 3 promoted rows plus c-rejected; c-model skips at the kind stage
    assert again["skipped"]["status"] == 4

    # the pure predicate is directly checkable at the sub-boundary
    ok, reason = eligibility(rows[3], now=NOW, min_age_hours=48.0, kinds=("practice", "tesuji"))
    assert ok is False and reason.startswith("age:1.0h-under-48h")
