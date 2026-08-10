"""Tests for mag.law — the code-as-law enforcement registry."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import mag.law as law


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    """Isolate law store to tmp_path so tests never touch the real registry."""
    monkeypatch.setattr(law, "LAW_DIR", tmp_path)
    monkeypatch.setattr(law, "REGISTRY", tmp_path / "registry.json")
    monkeypatch.setattr(law, "TRAIL", tmp_path / "enforcement_trail.jsonl")
    # no verkle in tests
    monkeypatch.setattr(law, "_verkle_anchor", lambda rec: "")


def test_seed_registers_default_operator_laws():
    res = law.seed()
    assert res["ok"]
    assert "LAW-1" in res["ids"]
    assert "LAW-3" in res["ids"]
    assert "LAW-4" in res["ids"]


def test_register_is_append_only():
    law.seed()
    r = law.register({"id": "LAW-99", "name": "test", "tier": "T1",
                      "trigger": "x", "condition": "y", "action": "z", "guardrail": "g"})
    assert r["ok"]
    # immutable: re-register same id fails
    r2 = law.register({"id": "LAW-99", "name": "dup"})
    assert not r2["ok"]


def test_enforce_reports_each_law():
    law.seed()
    res = law.enforce(apply=False)
    assert res["ok"]
    ids = [r["id"] for r in res["results"]]
    assert "LAW-1" in ids and "LAW-3" in ids


def test_enforce_logs_to_trail_on_apply():
    law.seed()
    res = law.enforce(apply=True)
    assert res["ok"]
    assert law.TRAIL.is_file()
    rows = [json.loads(l) for l in law.TRAIL.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert rows


def test_status_shape():
    law.seed()
    st = law.status()
    assert st["ok"]
    assert st["n_laws"] >= 4
    assert "registry" in st
