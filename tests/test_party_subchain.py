"""Proofs for the Verkle-anchored, append-only party communication relation."""
from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor


def _isolated(module, tmp_path, monkeypatch):
    run_dir = tmp_path / "party_subchain"
    tip = tmp_path / "verkle_tip.json"
    tip.write_text(json.dumps({
        "root": "root-test",
        "last_leaf_hash": "leaf-test",
        "n_leaves": 7,
        "last_session_id": "session-test",
        "updated_minute": "2026-08-14T10:00Z",
    }), encoding="utf-8")
    monkeypatch.setattr(module, "DIR", run_dir)
    monkeypatch.setattr(module, "CHAIN", run_dir / "chain.jsonl")
    monkeypatch.setattr(module, "HEAD", run_dir / "head.json")
    monkeypatch.setattr(module, "LOCK", run_dir / ".append.lock")
    monkeypatch.setattr(module, "TIP", tip)


def test_append_mount_and_verify_the_relation(tmp_path, monkeypatch):
    from mag import party_subchain as chain

    _isolated(chain, tmp_path, monkeypatch)
    assert chain.genesis()["ok"] is True
    first = chain.append(seat="chatgpt", ok=True, move="propose a relay", kind="salon")
    second = chain.append(seat="grok", ok=False, move="", kind="salon")
    assert first["ok"] is True and second["ok"] is True
    proof = chain.verify()
    assert proof["ok"] is True and proof["n"] == 3
    mounted = chain.mount()
    assert mounted["verified"] is True
    assert "chatgpt: propose a relay" in mounted["transcript"]
    assert "grok: [unreachable]" in mounted["transcript"]


def test_broken_relation_is_neither_mounted_nor_extended(tmp_path, monkeypatch):
    from mag import party_subchain as chain

    _isolated(chain, tmp_path, monkeypatch)
    chain.genesis()
    chain.append(seat="chatgpt", ok=True, move="original", kind="turn")
    rows = [json.loads(line) for line in chain.CHAIN.read_text(encoding="utf-8").splitlines()]
    rows[-1]["move"] = "tampered"
    chain.CHAIN.write_text(
        "\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8"
    )
    assert chain.verify()["ok"] is False
    assert chain.mount()["ok"] is False
    refused = chain.append(seat="grok", ok=True, move="must not land", kind="turn")
    assert refused["ok"] is False
    assert "unverified" in refused["error"]


def test_concurrent_seats_serialize_on_one_hash_chain(tmp_path, monkeypatch):
    from mag import party_subchain as chain

    _isolated(chain, tmp_path, monkeypatch)
    chain.genesis()
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(
            lambda i: chain.append(seat=f"seat-{i}", ok=True, move=f"move-{i}"),
            range(12),
        ))
    assert all(result["ok"] for result in results)
    proof = chain.verify()
    assert proof["ok"] is True and proof["n"] == 13
