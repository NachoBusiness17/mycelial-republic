"""B2-412: the icon_drop fold-outcome arms pinned in the repo (port of the
B2-378 throwaway probe; the probe's exact sandbox pattern: tmp_path plus
monkeypatch on the module write-path constants).

The four arms (B2-378): a row with status "dropped" records outcome "ok";
"failed", "skipped_no_powershell" and a statusless row record the status
verbatim ("unknown" for statusless). Falsifier: revert _fold_training's
outcome to a hardcoded "ok" and the three non-dropped arms go red.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import mag.icon_drop as icon_drop


def _read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    """Redirect all four write paths into tmp (the probe's exact pattern)."""
    import mag.skill_ledger as sl
    import mag.training_events as te

    monkeypatch.setattr(icon_drop, "LEDGER", tmp_path / "icons" / "ledger.jsonl")
    monkeypatch.setattr(icon_drop, "desktop_folder", tmp_path / "desktop")
    monkeypatch.setattr(sl, "DECISIONS_PATH", tmp_path / "skill_decisions.jsonl")
    monkeypatch.setattr(te, "EVENTS_PATH", tmp_path / "training_events.jsonl")
    return tmp_path


def _run_fold(status):
    icon_drop._fold_training({"name": "Test Icon", "status": status,
                              "path": "nowhere"})


def test_dropped_row_folds_outcome_ok(sandbox):
    _run_fold("dropped")
    decisions = _read_jsonl(sandbox / "skill_decisions.jsonl")
    assert decisions and decisions[-1]["outcome"] == "ok"
    events = _read_jsonl(sandbox / "training_events.jsonl")
    assert events and events[-1]["outcome"]["status"] == "dropped"


def test_failed_row_folds_outcome_failed(sandbox):
    _run_fold("failed")
    decisions = _read_jsonl(sandbox / "skill_decisions.jsonl")
    assert decisions[-1]["outcome"] == "failed"


def test_skipped_row_folds_verbatim_status(sandbox):
    _run_fold("skipped_no_powershell")
    decisions = _read_jsonl(sandbox / "skill_decisions.jsonl")
    assert decisions[-1]["outcome"] == "skipped_no_powershell"


def test_statusless_row_folds_unknown(sandbox):
    _run_fold(None)
    decisions = _read_jsonl(sandbox / "skill_decisions.jsonl")
    assert decisions[-1]["outcome"] == "unknown"
