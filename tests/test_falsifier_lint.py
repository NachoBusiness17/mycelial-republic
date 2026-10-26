"""falsifier_lint tests (WAVE invariant-percolator, 2026-10-20, wave 4).

Binds tools/falsifier_lint.py:
  flint.lint(root) -> report dict (counts, results, coverage)
  flint.main(["--root", tmp]) -> 0 ok / 1 FAILED / 2 UNVERIFIABLE

The battery pins the tri-state: a manual falsifier is UNMEASURED, never a pass;
a promoted row with no falsifier at all is a FAIL; a log_zero check only sees
rows inside its window.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import tools.falsifier_lint as flint

TOOL = Path(__file__).resolve().parents[1] / "tools" / "falsifier_lint.py"
NOW = datetime.now(timezone.utc)


def _iso(days_ago: float) -> str:
    return (NOW - timedelta(days=days_ago)).isoformat()


def _estate(tmp_path: Path, *, promoted: list[str], falsifiers: list[dict],
            log_rows: list[dict] | None = None, claims: list[dict] | None = None,
            absent_file: str = "logs/training_events.jsonl") -> Path:
    base = tmp_path / "memory" / "percolator"
    base.mkdir(parents=True, exist_ok=True)
    inv = {k: {"text": f"claim {k}", "count": 3, "domain": "behavioral",
               "first_seen": _iso(30), "last_seen": _iso(1)} for k in promoted}
    (base / "invariants.json").write_text(json.dumps({"invariants": inv}), encoding="utf-8")
    with (base / "promotion_ledger.jsonl").open("w", encoding="utf-8") as fh:
        for k in promoted:
            fh.write(json.dumps({"schema": "invariant_promotion.v1", "canonical": k,
                                 "promoted": True, "policy_sha": "x", "row_hash": "y",
                                 "blockers": []}) + "\n")
    with (base / "falsifiers.jsonl").open("w", encoding="utf-8") as fh:
        for entry in falsifiers:
            fh.write(json.dumps(entry) + "\n")
    logs = tmp_path / "logs"
    logs.mkdir(exist_ok=True)
    if log_rows is not None:
        with (logs / "failure_kb.jsonl").open("w", encoding="utf-8") as fh:
            for row in log_rows:
                fh.write(json.dumps(row) + "\n")
    (tmp_path / "watch").mkdir(exist_ok=True)
    with (tmp_path / "watch" / "claims.jsonl").open("w", encoding="utf-8") as fh:
        for row in (claims if claims is not None else []):
            fh.write(json.dumps(row) + "\n")
    assert absent_file  # documented default; the file is simply never created
    return tmp_path


def _entry(canonical: str, kind: str, **kw) -> dict:
    base = {"schema": "invariant_falsifier.v1", "canonical": canonical, "claim": "c",
            "kind": kind, "owner": "seat", "review_by": "2026-11-20", "note": "n"}
    base.update(kw)
    return base


def test_log_zero_passes_when_window_is_clean(tmp_path):
    root = _estate(tmp_path, promoted=["a" * 16],
                   falsifiers=[_entry("a" * 16, "log_zero", target="logs/failure_kb.jsonl",
                                      pattern="false-success", window_days=7)],
                   log_rows=[{"ts": _iso(30), "detail": "false-success"}])
    report = flint.lint(root)
    assert report["results"][0]["status"] == "PASS"   # old hit is outside the window


def test_log_zero_fails_on_recent_hit(tmp_path):
    root = _estate(tmp_path, promoted=["a" * 16],
                   falsifiers=[_entry("a" * 16, "log_zero", target="logs/failure_kb.jsonl",
                                      pattern="identical run_shell", window_days=7)],
                   log_rows=[{"ts": _iso(2), "detail": "5x identical run_shell calls"}])
    report = flint.lint(root)
    assert report["results"][0]["status"] == "FAIL"
    assert report["results"][0]["count"] == 1


def test_file_absent_passes_when_missing_and_fails_when_present(tmp_path):
    root = _estate(tmp_path, promoted=["a" * 16],
                   falsifiers=[_entry("a" * 16, "file_absent", target="logs/training_events.jsonl")])
    assert flint.lint(root)["results"][0]["status"] == "PASS"
    (root / "logs" / "training_events.jsonl").write_text("{}\n", encoding="utf-8")
    assert flint.lint(root)["results"][0]["status"] == "FAIL"


def test_field_complete_detects_missing_verifier(tmp_path):
    root = _estate(tmp_path, promoted=["a" * 16],
                   falsifiers=[_entry("a" * 16, "field_complete",
                                      target="watch/claims.jsonl", field="verifier")],
                   claims=[{"id": "c1", "verifier": "v"}, {"id": "c2"}])
    result = flint.lint(root)["results"][0]
    assert result["status"] == "FAIL"
    assert "1/2" in result["detail"]


def test_manual_is_unmeasured_not_pass(tmp_path):
    root = _estate(tmp_path, promoted=["a" * 16],
                   falsifiers=[_entry("a" * 16, "manual")])
    report = flint.lint(root)
    assert report["results"][0]["status"] == "UNMEASURED"
    assert report["counts"]["PASS"] == 0


def test_missing_entry_is_a_fail(tmp_path):
    root = _estate(tmp_path, promoted=["a" * 16, "b" * 16],
                   falsifiers=[_entry("a" * 16, "manual")])
    report = flint.lint(root)
    missing = [r for r in report["results"] if r["kind"] is None]
    assert len(missing) == 1 and missing[0]["status"] == "FAIL"
    assert report["coverage_pct"] == 50.0


def test_cli_exit_1_when_a_falsifier_fires(tmp_path):
    root = _estate(tmp_path, promoted=["a" * 16],
                   falsifiers=[_entry("a" * 16, "log_zero", target="logs/failure_kb.jsonl",
                                      pattern="boom", window_days=7)],
                   log_rows=[{"ts": _iso(1), "detail": "boom"}])
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(root)],
                        capture_output=True, text=True)
    assert cp.returncode == 1, cp.stdout + cp.stderr
    assert cp.stdout.startswith("FALSIFIER-LINT: FAILED")


def test_cli_exit_0_with_manual_debt_and_json_shape(tmp_path):
    root = _estate(tmp_path, promoted=["a" * 16], falsifiers=[_entry("a" * 16, "manual")])
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(root), "--json"],
                        capture_output=True, text=True)
    assert cp.returncode == 0, cp.stdout + cp.stderr
    report = json.loads(cp.stdout)
    assert report["schema"] == "falsifier_lint.v1"
    assert report["counts"] == {"PASS": 0, "FAIL": 0, "UNMEASURED": 1}
    assert report["coverage_pct"] == 100.0


def test_cli_exit_2_without_falsifier_file(tmp_path):
    base = tmp_path / "memory" / "percolator"
    base.mkdir(parents=True)
    (base / "invariants.json").write_text('{"invariants": {}}', encoding="utf-8")
    (base / "promotion_ledger.jsonl").write_text("", encoding="utf-8")
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(tmp_path)],
                        capture_output=True, text=True)
    assert cp.returncode == 2, cp.stdout + cp.stderr
    assert cp.stdout.startswith("FALSIFIER-LINT: UNVERIFIABLE")


# --- wave 5: duplicate rows and the nudge budget ------------------------------

def test_log_zero_dedupes_double_logged_rows(tmp_path):
    stamp = _iso(1)
    rows = [{"ts": stamp, "detail": "boom"}, {"ts": stamp, "detail": "boom"}]
    root = _estate(tmp_path, promoted=["a" * 16],
                   falsifiers=[_entry("a" * 16, "log_zero", target="logs/failure_kb.jsonl",
                                      pattern="boom", window_days=7, dedupe_ms=1000)],
                   log_rows=rows)
    result = flint.lint(root)["results"][0]
    assert result["status"] == "FAIL"
    assert result["count"] == 1 and result["raw"] == 2


def test_nudge_budget_passes_inside_two_nudges(tmp_path):
    rows = [{"ts": _iso(3), "phase": "collapse_nudge", "detail": "5x identical run_shell calls",
             "sig": "run_shell:aa", "session_id": "s1"}] * 4   # two events, logged twice
    root = _estate(tmp_path, promoted=["a" * 16],
                   falsifiers=[_entry("a" * 16, "nudge_budget",
                                      target="logs/failure_kb.jsonl", pattern="identical",
                                      max_nudges=2, window_days=30, dedupe_ms=1000)],
                   log_rows=rows)
    result = flint.lint(root)["results"][0]
    assert result["status"] == "PASS", result


def test_nudge_budget_fails_when_budget_exceeded(tmp_path):
    rows = [{"ts": _iso(d), "phase": "collapse_nudge",
             "detail": "5x identical run_shell calls", "sig": "run_shell:aa", "session_id": "s1"}
            for d in (5, 4, 3)]
    root = _estate(tmp_path, promoted=["a" * 16],
                   falsifiers=[_entry("a" * 16, "nudge_budget",
                                      target="logs/failure_kb.jsonl", pattern="identical",
                                      max_nudges=2, window_days=30, dedupe_ms=1000)],
                   log_rows=rows)
    result = flint.lint(root)["results"][0]
    assert result["status"] == "FAIL"
    assert result["offenders"][0]["nudges"] == 3
