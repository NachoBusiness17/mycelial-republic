"""Skill ledger — the right-sizing counter (decisions + labeled rows)."""
from __future__ import annotations

from pathlib import Path

import pytest

import mag.skill_ledger as sl


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(sl, "DECISIONS_PATH", tmp_path / "skill_ledger.jsonl")
    monkeypatch.setattr(sl, "LABELED_PATH", tmp_path / "classify" / "rows.jsonl")
    return tmp_path


def test_record_decision_and_progress(isolated):
    sl.record_decision(goal="classify a file", task_shape="classify", provider="ollama", model="gemma4:latest", outcome="ok")
    sl.record_decision(goal="multi edit", task_shape="edit_multi", provider="deepseek", model="deepseek-v4-flash", reasoning_level="none", outcome="fail")
    p = sl.progress()
    assert p["decisions"] == 2
    assert p["decisions_target"] == 1000


def test_record_labeled_row_increments_counter(isolated):
    sl.record_labeled_row(text="Add a timeout param", label="code", classifier="gemma4:latest", confidence=1.0)
    sl.record_labeled_row(text="file a note", label="note", classifier="gemma4:latest", audited_by="deepseek-v4-flash")
    p = sl.progress()
    assert p["labeled_rows"] == 2
    # audited row is persisted with the audit model
    lines = sl.LABELED_PATH.read_text(encoding="utf-8").splitlines()
    assert "deepseek-v4-flash" in lines[1]


def test_seed_from_bench_skips_missing(isolated):
    res = sl.seed_from_bench()
    assert res["ok"] is True
    assert res["seeded"] >= 0
    assert "progress" in res
