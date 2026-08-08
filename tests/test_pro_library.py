"""Pro library — the aimbot-for-AI (sense/match/inject/learn), folded into behavioral systems."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import mag.pro_library as pl
import mag.operator_inbox as oi
import mag.skill_ledger as sl
import mag.tesuji_shell as ts


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(pl, "LIB_PATH", tmp_path / "pro_library.json")
    monkeypatch.setattr(oi, "INBOX_PATH", tmp_path / "operator_inbox.json")
    monkeypatch.setattr(sl, "DECISIONS_PATH", tmp_path / "skill_ledger.jsonl")
    monkeypatch.setattr(sl, "LABELED_PATH", tmp_path / "rows.jsonl")
    monkeypatch.setattr(ts, "SHELLS_PATH", tmp_path / "tesuji_shells.jsonl")
    return tmp_path


def test_add_and_match_signature(isolated):
    pl.add_move("claimed edits but no file change, fake success, tool result empty", "steer",
                "Verify with git diff before declaring done.", effect="catches false-success")
    res = pl.match({"text": "the model claimed it updated llm.py but ran no tool — fake success likely"})
    assert res and res[0]["score"] > 0
    assert "fake success" in " ".join(res[0]["move"]["signature"]) or res[0]["hits"] >= 1


def test_aim_fires_steer_into_inbox(isolated):
    pl.add_move("agent looping, repeated tool, token burn", "steer",
                "Escalate to next tier; stop token bleed.", effect="stop loops")
    out = pl.aim_once({"text": "agent is looping, repeating write_file 5x, burning tokens"})
    assert out["ok"] is True
    assert len(out["fired"]) >= 1
    assert out["fired"][0]["injected"] is True
    st = oi.status()
    assert st["pending_n"] >= 1  # steer landed in the inbox (the seam)


def test_learn_folds_into_skill_ledger_and_tesuji_shells(isolated):
    pl.add_move("task vague, executor may fake", "spec",
                "Emit a penny-spec first, then designate the cheap executor.", effect="designations")
    data = pl._load()
    mid = data["moves"][0]["id"]
    r = pl.learn(mid, outcome="ok", goal="verify spec path")
    assert r["ok"] is True and r["win"] is True
    # folded into skill_ledger
    assert sl.progress()["decisions"] >= 1
    # folded into tesuji shells (capture on add)
    assert ts.read_shells()
    # behavioral events for fire+learn
    assert pl.stats()["total_wins"] >= 1


def test_seed_default_moves(isolated):
    r = pl.seed_default_moves()
    assert r["seeded"] == 5
    st = pl.stats()
    assert st["moves"] == 5
    assert set(st["by_kind"].keys()) <= {"steer", "spec", "tip", "skill"}
