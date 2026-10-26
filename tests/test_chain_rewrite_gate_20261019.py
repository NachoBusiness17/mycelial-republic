"""CHAIN_REWRITE_GATE_20261019 - v1 amend / _rewrite_chain refuse without flag."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from mag import verkle_knot as vk


def _dossier(sid: str, *, commit_salt: str = "1") -> dict:
    return {
        "session_id": sid,
        "time": {
            "created_at": {"iso_minute": "2026-10-19T12:00:00Z", "unix_minute": None, "date": None},
            "updated_at": {"iso_minute": "2026-10-19T12:00:00Z", "unix_minute": None, "date": None},
        },
        "scalar_knot": {
            "duration_minutes": 0.1,
            "tension_index": 0.1,
            "residual_weight": 1.0,
            "theme_vector": {
                "dominant": "biography",
                "basis": list(vk.THEME_BASIS),
                "raw": [0.0] * len(vk.THEME_BASIS),
                "normalized": [0.0] * len(vk.THEME_BASIS),
            },
        },
        "content_commit": {"hex": commit_salt * 8},
    }


@pytest.fixture
def estate(tmp_path, monkeypatch):
    bio = tmp_path / "biography"
    knots = bio / "knots"
    knots.mkdir(parents=True)
    monkeypatch.setattr(vk, "ROOT", tmp_path)
    monkeypatch.setattr(vk, "BIO", bio)
    monkeypatch.setattr(vk, "KNOTS", knots)
    monkeypatch.setattr(vk, "CHAIN", bio / "verkle_chain.jsonl")
    monkeypatch.setattr(vk, "TIP", bio / "verkle_tip.json")
    monkeypatch.setattr(vk, "LATEST", bio / "latest.knot.json")
    monkeypatch.setattr(vk, "EVOLUTION", bio / "topic_evolution.json")
    monkeypatch.setattr(vk, "LOCK", bio / ".verkle.lock")
    return bio


def test_rewrite_chain_refuses_without_flag(estate, monkeypatch):
    monkeypatch.delenv("MAG_ALLOW_CHAIN_REWRITE", raising=False)
    with pytest.raises(PermissionError, match="chain rewrite refused"):
        vk._rewrite_chain([{"leaf_hash": "a" * 64, "session_id": "s"}])


def test_v1_amend_refuses_without_flag(estate, monkeypatch):
    monkeypatch.delenv("MAG_ALLOW_CHAIN_REWRITE", raising=False)
    monkeypatch.setattr(vk, "chain_mode", lambda: vk.CHAIN_MODE_V1)
    r1 = vk.append_verkle_knot(_dossier("sess-gate", commit_salt="1"))
    assert r1.get("ok") is True
    r2 = vk.append_verkle_knot(_dossier("sess-gate", commit_salt="2"))
    assert r2.get("ok") is False
    assert "refused" in str(r2.get("error", "")).lower()
    rows = [json.loads(x) for x in vk.CHAIN.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows) == 1
    assert rows[0]["leaf_hash"] == r1["leaf_hash"]


def test_v2_append_still_works_without_flag(estate, monkeypatch):
    monkeypatch.delenv("MAG_ALLOW_CHAIN_REWRITE", raising=False)
    monkeypatch.setattr(vk, "chain_mode", lambda: vk.CHAIN_MODE_V2)
    r1 = vk.append_verkle_knot(_dossier("sess-v2", commit_salt="1"))
    r2 = vk.append_verkle_knot(_dossier("sess-v2", commit_salt="2"))
    assert r1.get("ok") and r2.get("ok")
    assert r2.get("amended") is False
    rows = [json.loads(x) for x in vk.CHAIN.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows) == 2


def test_consolidate_refuses_without_flag(estate, monkeypatch):
    monkeypatch.delenv("MAG_ALLOW_CHAIN_REWRITE", raising=False)
    monkeypatch.setattr(vk, "chain_mode", lambda: vk.CHAIN_MODE_V1)
    monkeypatch.setenv("MAG_ALLOW_CHAIN_REWRITE", "1")
    vk.append_verkle_knot(_dossier("a", commit_salt="1"))
    monkeypatch.delenv("MAG_ALLOW_CHAIN_REWRITE", raising=False)
    out = vk.consolidate_chain_one_leaf_per_session()
    assert out.get("ok") is False and out.get("skipped") is True
