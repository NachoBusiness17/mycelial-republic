"""Tests for the passive warning monitor (mag.warning_monitor)."""
import json
from pathlib import Path

import pytest

from mag.warning_monitor import extract_warnings, run, status


def _make_logs(tmp: Path, content: str) -> Path:
    log_dir = tmp / "logs"
    (log_dir / "orchestrator").mkdir(parents=True, exist_ok=True)
    (log_dir / "orchestrator" / "t1.out.log").write_text(content, encoding="utf-8")
    return log_dir


def test_extract_pulls_warning_lines(tmp_path):
    log_dir = _make_logs(
        tmp_path,
        "info: doing fine\nERROR: boom happened\nwarn: something slow\n",
    )
    out = extract_warnings(log_dir=log_dir)
    lines = {w["line"] for w in out}
    assert any("boom happened" in l for l in lines)
    assert any("something slow" in l for l in lines)
    # signatures unique
    assert len({w["sig"] for w in out}) == len(out)


def test_run_reports_and_dedups(tmp_path):
    log_dir = _make_logs(tmp_path, "ERROR: first warning\n")
    seen = tmp_path / "seen.json"
    calls = []

    def fake_report(w):
        calls.append(w["sig"])
        return {"ok": True}

    r1 = run(log_dir=log_dir, seen_path=seen, report=fake_report)
    assert r1["reported_n"] == 1
    assert len(calls) == 1

    # Idempotent: same content -> nothing new reported
    r2 = run(log_dir=log_dir, seen_path=seen, report=fake_report)
    assert r2["reported_n"] == 0
    assert len(calls) == 1

    # Dry run reports nothing to FKB but sees the line
    r3 = run(log_dir=log_dir, seen_path=seen, report=fake_report, dry=True)
    assert r3["dry"] is True
    assert r3["reported_n"] == 0


def test_status_shape(tmp_path):
    log_dir = _make_logs(tmp_path, "ERROR: something went wrong in the monitor\n")
    seen = tmp_path / "seen.json"
    run(log_dir=log_dir, seen_path=seen, report=lambda w: {"ok": True})
    # status() uses real SEEN_PATH by default; call recent/seen via run result
    assert Path(seen).is_file()
    data = json.loads(seen.read_text(encoding="utf-8"))
    assert len(data["seen"]) == 1
