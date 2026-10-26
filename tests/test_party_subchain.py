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


def _write_rows(chain, rows) -> None:
    chain.CHAIN.parent.mkdir(parents=True, exist_ok=True)
    with chain.CHAIN.open("w", encoding="utf-8", newline="") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def test_v1_rows_still_verify_and_chain_upgrades_to_v2(tmp_path, monkeypatch):
    """Audit #12 fix: legacy v1 rows verify under the old hash rule; new rows are v2."""
    from mag import party_subchain as chain

    _isolated(chain, tmp_path, monkeypatch)
    v1_genesis = {
        "schema": chain.SCHEMA_V1,
        "kind": "genesis",
        "ts": "2026-08-14T10:48:11.440426Z",
        "seat": "chain",
        "ok": True,
        "move": chain.INVARIANT,
        "prev_hash": None,
        "parent_leaf_hash": "leaf-test",
        "parent_root": "root-test",
        "n": 0,
    }
    v1_turn = {
        "schema": chain.SCHEMA_V1,
        "kind": "turn",
        "ts": "2026-08-14T10:50:00Z",
        "seat": "legacy-seat",
        "ok": True,
        "move": "legacy move",
        "prev_hash": None,
        "parent_leaf_hash": "leaf-test",
        "parent_root": "root-test",
        "n": 1,
        "extra": {"legacy": "unauthenticated-under-v1"},
    }
    v1_genesis["hash"] = chain._hash_entry(v1_genesis)
    v1_turn["prev_hash"] = v1_genesis["hash"]
    v1_turn["hash"] = chain._hash_entry(v1_turn)
    _write_rows(chain, [v1_genesis, v1_turn])
    chain._write_head(v1_turn, {"parent_root": "root-test", "parent_leaf_hash": "leaf-test"})

    proof = chain.verify()
    assert proof["ok"] is True and proof["n"] == 2

    upgraded = chain.append(seat="chatgpt", ok=True, move="v2 move", kind="turn",
                            extra={"note": "authenticated"})
    assert upgraded["ok"] is True
    rows = [json.loads(line) for line in
            chain.CHAIN.read_text(encoding="utf-8").splitlines()]
    assert [r["schema"] for r in rows] == [chain.SCHEMA_V1, chain.SCHEMA_V1, chain.SCHEMA_V2]
    assert rows[-1]["prev_hash"] == rows[1]["hash"]
    mixed = chain.verify()
    assert mixed["ok"] is True and mixed["n"] == 3


def test_v2_extra_tampering_fails_verification(tmp_path, monkeypatch):
    from mag import party_subchain as chain

    _isolated(chain, tmp_path, monkeypatch)
    chain.genesis()
    chain.append(seat="chatgpt", ok=True, move="carry a payload", kind="turn",
                 extra={"note": "payload"})
    rows = [json.loads(line) for line in
            chain.CHAIN.read_text(encoding="utf-8").splitlines()]
    assert all(row["schema"] == chain.SCHEMA_V2 for row in rows)
    rows[-1]["extra"]["note"] = "mutated"
    _write_rows(chain, rows)
    chain._write_head(rows[-1], {"parent_root": "root-test", "parent_leaf_hash": "leaf-test"})
    proof = chain.verify()
    assert proof["ok"] is False
    assert any("content hash mismatch" in e for e in proof["errors"])


def test_appended_file_carries_no_crlf_bytes(tmp_path, monkeypatch):
    """Byte-exact law: appends stay bare-LF on Windows (newline="" fix, audit #12)."""
    from mag import party_subchain as chain

    _isolated(chain, tmp_path, monkeypatch)
    chain.genesis()
    chain.append(seat="chatgpt", ok=True, move="lf only", kind="turn",
                 extra={"k": "v"})
    raw = chain.CHAIN.read_bytes()
    assert b"\r\n" not in raw
    assert b"\r" not in raw
    assert chain.verify()["ok"] is True
