"""Byte-exact chain I/O tests (B2-393, 2026-09-26).

B2-83 rev 1 proved live that Path.write_text on Windows rewrites every LF in
the chain to CRLF while read_text translates it back (only a raw-byte diff
caught it). This file pins the cure and documents the damage mechanism:

- the falsifier shape: the OLD write_text form still reproduces the CRLF
  rewrite on a copy (proof the hazard was real, kept as a regression mirror);
- the four converted write sites' shapes keep LF byte-exact;
- chain_guard.check() trips crlf_rewrite on a CR-bearing chain and stays
  healthy on an LF chain.
"""
from __future__ import annotations

import json
from pathlib import Path

from mag import chain_guard as cg
from mag import verkle_knot as vk

ROWS = [
    {"leaf_hash": "a" * 64, "session_id": "s1"},
    {"leaf_hash": "b" * 64, "session_id": "s2"},
]


def test_rewrite_chain_writes_lf_only(tmp_path, monkeypatch):
    monkeypatch.setenv("MAG_ALLOW_CHAIN_REWRITE", "1")
    from datetime import datetime, timedelta, timezone
    monkeypatch.setattr(vk, "ROOT", tmp_path)
    monkeypatch.setattr(vk, "BIO", tmp_path)
    st = tmp_path / "state"
    st.mkdir(parents=True, exist_ok=True)
    exp = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
    (st / "chain_rewrite_approval.json").write_text(
        __import__("json").dumps({"allow": True, "expires_utc": exp, "by": "pytest", "purpose": "byte_exact"}),
        encoding="utf-8",
    )
    out = tmp_path / "verkle_chain.jsonl"
    monkeypatch.setattr(vk, "CHAIN", out)
    vk._rewrite_chain([dict(r) for r in ROWS])
    raw = out.read_bytes()
    assert raw and b"\r" not in raw
    assert raw.endswith(b"\n")
    assert [json.loads(l) for l in raw.decode("utf-8").splitlines()][0]["session_id"] == "s1"


def test_flag_script_write_shape_writes_lf_only(tmp_path):
    # the converted flag-script shape (write_bytes of the joined lines)
    out = tmp_path / "verkle_chain.jsonl"
    joined = "\n".join(json.dumps(r) for r in ROWS) + "\n"
    out.write_bytes(joined.encode("utf-8"))
    assert b"\r" not in out.read_bytes()


def test_old_write_text_shape_reproduces_the_crlf_rewrite(tmp_path):
    # the B2-393 falsifier, kept as a witness: the OLD shape on a copy of an
    # LF chain rewrites every LF to CRLF on Windows. Skipped on platforms
    # whose text mode does not translate (non-Windows) so the witness stays
    # honest instead of vacuous.
    import sys as _sys
    if _sys.platform != "win32":
        import pytest
        pytest.skip("CRLF translation is a Windows text-mode behavior")
    out = tmp_path / "verkle_chain.jsonl"
    out.write_text("\n".join(json.dumps(r) for r in ROWS) + "\n", encoding="utf-8")
    raw = out.read_bytes()
    assert raw.count(b"\r\n") == len(ROWS)


def test_chain_guard_trips_on_crlf_chain(tmp_path, monkeypatch):
    chain = tmp_path / "verkle_chain.jsonl"
    chain.write_bytes(
        ("\n".join(json.dumps(r) for r in ROWS) + "\n").encode().replace(b"\n", b"\r\n"))
    monkeypatch.setattr(cg, "CHAIN", chain)
    res = cg.check()
    assert res["ok"] is False
    assert res["state"] == "crlf_rewrite"
    assert res["crlf_bytes"] is True
    assert "CRLF" in (res["alarm"] or "")


def test_chain_guard_green_on_lf_chain(tmp_path, monkeypatch):
    chain = tmp_path / "verkle_chain.jsonl"
    chain.write_bytes(("\n".join(json.dumps(r) for r in ROWS) + "\n").encode())
    monkeypatch.setattr(cg, "CHAIN", chain)
    monkeypatch.setattr(cg, "MARKER", tmp_path / "no_marker.json")
    res = cg.check()
    assert res["state"] == "unmarked"
    assert res["ok"] is True
    assert res["crlf_bytes"] is False
