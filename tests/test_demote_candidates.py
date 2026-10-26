"""Demote candidates (Q-049, 2026-09-28): one test, the full deterministic matrix.

The tmp ledger drives the REAL demotion path: mag.improve.load_config is
monkeypatched so ensure_dirs()/read_candidates()/update_candidate_status land
on tmp_path and the real memory/improve/candidates.jsonl is never touched.
update_candidate_status itself runs unpatched (the single status writer).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _row(cid: str, *, kind: str | None, feasible: object, status: str) -> dict:
    row = {"schema": "improve_candidate.v1", "id": cid, "claim": f"claim {cid}",
           "detail": "", "source": "pytest", "source_urls": [], "local_feasible": feasible,
           "status": status}
    if kind is not None:
        row["kind"] = kind
    return row


def test_demote_gap_shapes(tmp_path, monkeypatch):
    import mag.improve as imp
    from tools.demote_candidates import frontier_gap_shapes, run

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

    rows = [
        # runtime: 2 cheap terminal fails (rate 0.0 < 0.6 -> GAP), 2 open targets,
        # plus one already-demoted row (never re-touched)
        _row("r-fail1", kind="runtime", feasible="true", status="rejected"),
        _row("r-fail2", kind="runtime", feasible="true", status="rejected"),
        _row("r-open-new", kind="runtime", feasible="true", status="new"),
        _row("r-open-hold", kind="runtime", feasible="true", status="hold"),
        # open row of the gap shape that never claimed cheap: stays
        _row("r-open-unknown", kind="runtime", feasible="unknown", status="new"),
        _row("r-demoted", kind="runtime", feasible="true", status="demoted"),
        # tesuji: 2 cheap terminal successes (rate 1.0) -> healthy, open row stays
        _row("t-ok1", kind="tesuji", feasible="true", status="promoted"),
        _row("t-ok2", kind="tesuji", feasible="true", status="promoted"),
        _row("t-open", kind="tesuji", feasible="true", status="new"),
        # risk: only 1 terminal row -> below min_terminal, never judged
        _row("k-fail1", kind="risk", feasible="true", status="rejected"),
        _row("k-open", kind="risk", feasible="true", status="new"),
        # model: terminals are NOT cheap (feasible unknown) -> n=0, never judged
        _row("m-fail1", kind="model", feasible="unknown", status="rejected"),
        _row("m-fail2", kind="model", feasible="unknown", status="rejected"),
        _row("m-open", kind="model", feasible="true", status="new"),
        # kind-less row: fail-closed, never touched
        _row("x-open", kind=None, feasible="true", status="new"),
        # practice: rate exactly 0.6 (3/5) -> NOT a gap (< is the bar), open stays
        _row("p-ok1", kind="practice", feasible="true", status="promoted"),
        _row("p-ok2", kind="practice", feasible="true", status="promoted"),
        _row("p-ok3", kind="practice", feasible="true", status="promoted"),
        _row("p-fail1", kind="practice", feasible="true", status="rejected"),
        _row("p-fail2", kind="practice", feasible="true", status="rejected"),
        _row("p-open", kind="practice", feasible="true", status="new"),
    ]
    ledger = tmp_path / "candidates.jsonl"
    ledger.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8"
    )

    # shape map directly: runtime is the only gap
    gaps, shapes = frontier_gap_shapes(rows, success_bar=0.6, min_terminal=2)
    assert gaps == ["runtime"]
    by_kind = {s["kind"]: s for s in shapes}
    assert by_kind["runtime"]["rate"] == 0.0 and by_kind["runtime"]["open_n"] == 2
    assert by_kind["tesuji"]["rate"] == 1.0
    assert by_kind["practice"]["rate"] == 0.6  # boundary: not a gap
    assert by_kind["model"]["terminal_n"] == 0  # infeasible terminals are not cheap outcomes

    # dry: the two open runtime rows flagged, nothing written, no audit file
    dry = run(dry=True, paths=cfg["paths"])
    assert dry["ok"] is True and dry["scanned"] == 21
    assert dry["frontier_gap_shapes"] == ["runtime"]
    assert sorted(e["id"] for e in dry["demoted"]) == ["r-open-hold", "r-open-new"]
    assert all(e["action"] == "would_demote" for e in dry["demoted"])
    assert not (tmp_path / "demoted.jsonl").exists()
    assert all(r["status"] == orig["status"] for r, orig in zip(
        [json.loads(l) for l in ledger.read_text(encoding="utf-8").splitlines()], rows))

    # real apply: exactly the two open runtime rows demoted through
    # update_candidate_status; every other row untouched
    res = run(dry=False, paths=cfg["paths"])
    assert res["ok"] is True
    assert sorted(e["id"] for e in res["demoted"]) == ["r-open-hold", "r-open-new"]
    assert all(e["action"] == "demoted" for e in res["demoted"])
    assert res["blocked"] == []
    # reconcile: 21 = 14 not-a-gap-shape + 1 kind-less + 1 gap-shape non-cheap
    # open + 3 gap-shape non-open (2 terminal + 1 already-demoted) + 2 demoted
    assert res["skipped"] == {"cheap": 1, "kind": 1, "shape": 14, "status": 3}

    after = {r["id"]: r for r in
             (json.loads(l) for l in ledger.read_text(encoding="utf-8").splitlines())}
    assert after["r-open-new"]["status"] == "demoted"
    assert after["r-open-hold"]["status"] == "demoted"
    assert "auto-demote" in after["r-open-new"]["note"]
    assert after["r-open-new"]["demote_shape"] == "runtime"
    assert after["r-open-new"]["demote_rate"] == 0.0
    # non-targets untouched
    assert after["t-open"]["status"] == "new"
    assert after["k-open"]["status"] == "new"
    assert after["m-open"]["status"] == "new"
    assert after["r-open-unknown"]["status"] == "new"  # gap shape but never claimed cheap
    assert after["p-open"]["status"] == "new"  # 0.6 boundary shape not demoted
    assert after["x-open"]["status"] == "new"  # kind-less never touched
    assert after["r-demoted"]["status"] == "demoted"  # already demoted, no note rewrite
    assert "note" not in after["r-demoted"]
    assert after["r-fail1"]["status"] == "rejected"
    # audit rows: one per applied decision
    audit_lines = (tmp_path / "demoted.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(audit_lines) == 2
    assert {json.loads(l)["id"] for l in audit_lines} == {"r-open-new", "r-open-hold"}
    assert all(json.loads(l)["verdict"] == "demoted" for l in audit_lines)

    # idempotent: second run demotes nothing; the two demoted rows now skip at
    # the status stage (3 prior + 2 new)
    again = run(dry=False, paths=cfg["paths"])
    assert again["demoted"] == []
    assert again["skipped"]["status"] == 5
