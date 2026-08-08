"""State snapshot + pile classifier — deterministic (local model stubbed)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mag.skill_ledger as sl  # noqa: E402
import mag.state_snapshot as ss  # noqa: E402
import tools.pile_classify as pc  # noqa: E402


def _iso(monkeypatch, tmp_path):
    monkeypatch.setattr(ss, "PILE", tmp_path / "state_summaries.jsonl")
    monkeypatch.setattr(ss, "CLASSIFIED", tmp_path / "classified.jsonl")
    monkeypatch.setattr(ss, "TRAINING", tmp_path / "training_rows.jsonl")
    monkeypatch.setattr(pc, "PILE", tmp_path / "state_summaries.jsonl")
    monkeypatch.setattr(pc, "CLASSIFIED", tmp_path / "classified.jsonl")
    monkeypatch.setattr(pc, "TRAINING", tmp_path / "training_rows.jsonl")
    monkeypatch.setattr(sl, "record_decision", lambda *a, **k: {"ok": True, "stubbed": True})


def test_capture_appends_and_dedups(monkeypatch, tmp_path) -> None:  # type: ignore[no-untyped-def]
    _iso(monkeypatch, tmp_path)
    r1 = ss.capture_summary(goal="fix the guard", outcome="escalated", tier="ollama->deepseek",
                            kind="escalation", lessons=["loop on tool"], source="df")
    assert r1["ok"] is True
    # same state again → dedup by state_hash
    r2 = ss.capture_summary(goal="fix the guard", outcome="escalated", tier="ollama->deepseek",
                            kind="escalation", lessons=["loop on tool"], source="df")
    assert r2["ok"] is False
    assert ss.status()["pile"] == 1


def test_capture_normalizes_outcome_kind(monkeypatch, tmp_path) -> None:  # type: ignore[no-untyped-def]
    _iso(monkeypatch, tmp_path)
    r = ss.capture_summary(goal="g", outcome="WEIRD", kind="nonsense")
    assert r["row"]["outcome"] == "unknown"
    assert r["row"]["kind"] == "session_end"


def test_extract_json_strict() -> None:
    text = 'Some prose {"category": "escalation", "lesson_kind": "loop", "recommendation": "x", "tags": ["a"]} trailing'
    d = pc._extract_json(text)
    assert d is not None and d["category"] == "escalation"
    assert pc._extract_json("no json here") is None


def test_pile_classify_folds_and_is_idempotent(monkeypatch, tmp_path) -> None:  # type: ignore[no-untyped-def]
    _iso(monkeypatch, tmp_path)
    ss.capture_summary(goal="the guard double-counted tries", outcome="fail", tier="local",
                       kind="session_end", lessons=["metric bug"], source="retro")
    ss.capture_summary(goal="thinking beats tier on vague spec", outcome="ok", tier="local",
                       kind="session_end", lessons=["assumption falsified"], source="battery")

    def fake_classify(row, *, model, timeout=240.0):
        return {"category": "process", "lesson_kind": "metric_bug",
                "recommendation": "measure the instrument first", "tags": ["testing", "metrics"]}

    monkeypatch.setattr(pc, "classify_one", fake_classify)
    res = pc.run_pile(model="stub")
    assert res["classified_this_run"] == 2
    assert res["pending"] == 2
    # idempotent — second run classifies nothing new
    res2 = pc.run_pile(model="stub")
    assert res2["classified_this_run"] == 0
    # training rows were folded
    train = pc._read_lines(tmp_path / "training_rows.jsonl")
    assert len(train) == 2
    assert json.loads(train[0]["output"])["lesson_kind"] == "metric_bug"
