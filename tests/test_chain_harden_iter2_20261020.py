"""CHAIN_HARDEN_ITER2_20261020 - dual rewrite gate + rolling baseline + fork tool smoke."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from mag import verkle_knot as vk


def test_rewrite_refuses_flag_alone(monkeypatch, tmp_path):
    monkeypatch.setenv("MAG_ALLOW_CHAIN_REWRITE", "1")
    monkeypatch.setattr(vk, "ROOT", tmp_path)
    monkeypatch.setattr(vk, "BIO", tmp_path / "biography")
    vk.BIO.mkdir(parents=True)
    (tmp_path / "state").mkdir()
    # no approval file
    assert vk._chain_rewrite_allowed() is False
    with pytest.raises(PermissionError, match="fresh"):
        vk._refuse_chain_rewrite("test")


def test_rewrite_allows_flag_plus_fresh_approval(monkeypatch, tmp_path):
    monkeypatch.setenv("MAG_ALLOW_CHAIN_REWRITE", "1")
    monkeypatch.setattr(vk, "ROOT", tmp_path)
    monkeypatch.setattr(vk, "BIO", tmp_path / "biography")
    vk.BIO.mkdir(parents=True)
    st = tmp_path / "state"
    st.mkdir()
    exp = (datetime.now(timezone.utc) + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    (st / "chain_rewrite_approval.json").write_text(
        json.dumps({"allow": True, "expires_utc": exp, "by": "test", "purpose": "unit"}),
        encoding="utf-8",
    )
    assert vk._chain_rewrite_allowed() is True


def test_no_rewrite_check_seeds_and_passes(tmp_path, monkeypatch):
    import tools.chain_no_rewrite_check as nr
    chain = tmp_path / "verkle_chain.jsonl"
    chain.write_bytes(b'{"leaf_hash":"a"}\n{"leaf_hash":"b"}\n')
    base = tmp_path / "baseline.json"
    monkeypatch.setattr(nr, "CHAIN", chain)
    monkeypatch.setattr(nr, "BASE", base)
    assert nr.main() == 0  # seed
    assert nr.main() == 0  # pass+advance
    # rewrite prefix
    chain.write_bytes(b'{"leaf_hash":"Z"}\n{"leaf_hash":"b"}\n')
    # reset baseline to old prefix of 1 row
    raw = b'{"leaf_hash":"a"}\n'
    import hashlib
    base.write_text(json.dumps({
        "schema": "chain_no_rewrite_baseline.v1",
        "rows": 1,
        "prefix_bytes": len(raw),
        "prefix_sha256": hashlib.sha256(raw).hexdigest(),
    }), encoding="utf-8")
    assert nr.main() == 1


def test_fork_rehydrate_tmpdir(tmp_path, monkeypatch):
    import tools.chain_fork_rehydrate as fr
    bio = tmp_path / "biography"
    knots = bio / "knots"
    knots.mkdir(parents=True)
    # minimal knot matching leaf
    body = {"session_id": "s1", "schema": "verkle_knot_leaf.v1", "x": 1}
    # compute leaf like verkle
    leaf = vk._leaf_hash({k: v for k, v in body.items()})
    knot = dict(body)
    knot["leaf_hash"] = leaf
    knot["filename"] = "k1.knot.json"
    (knots / "k1.knot.json").write_text(json.dumps(knot), encoding="utf-8")
    chain = bio / "verkle_chain.jsonl"
    chain.write_text(json.dumps({"filename": "k1.knot.json", "leaf_hash": leaf, "session_id": "s1"}) + "\n", encoding="utf-8")
    tip = bio / "verkle_tip.json"
    tip.write_text(json.dumps({"root": "x", "n_leaves": 1}), encoding="utf-8")
    monkeypatch.setattr(fr, "BIO", bio)
    monkeypatch.setattr(fr, "CHAIN", chain)
    monkeypatch.setattr(fr, "KNOTS", knots)
    monkeypatch.setattr(fr, "TIP", tip)
    monkeypatch.setattr(fr, "ATTIC", bio / "knots_attic")
    monkeypatch.setattr(fr, "DIARY_DIR", bio / "diary_nodes")
    out = tmp_path / "fork"
    import sys as _sys
    monkeypatch.setattr(_sys, "argv", ["fr", "--out", str(out)])
    assert fr.main() == 0
    assert (out / "divergence.json").is_file()
    assert (out / "verkle_chain.fork.jsonl").is_file()
