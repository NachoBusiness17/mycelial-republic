"""tests/test_tip_byte_mutation.py - P2A signed-tip mutation test (2026-10-07).

Lane p2a-tip-mutation, pheromone-swarm-20261007. The register card: mutate
ONE byte of a COPY of memory/biography/verkle_tip.json and prove the verifier
(mag.verkle_knot._verify_chain_consistent) refuses it; also tamper the index
(n_leaves) and the root field. If the verifier does NOT refuse, that is the
finding (a forgeable tip) and it is banked with the exact repro.

Law: the LIVE tip and chain are never mutated. The session fixture copies the
live pair into tmp under the production verkle_lock (the same lock the writers
hold, so the snapshot is an internally consistent pair) and every mutation
lands on tmp copies of those bytes.

Landed classification (this tree, live snapshot): every single-byte mutation
inside a BOUND value span (root, n_leaves, last_leaf_hash) is refused with the
named mismatch; flips the verifier ACCEPTS are confined to decorative surfaces
(note, updated_minute, last_filename, last_session_id, schema), key names and
JSON structure. One sharp edge is pinned: renaming the last_leaf_hash KEY by
one byte makes the gate SKIP the tail-hash binding (the check at
mag/verkle_knot.py guards on `if tip.get("last_leaf_hash")`), while root and
n_leaves still refuse, so the chain pointer itself is not forgeable.

The exhaustive byte-position sweep is @pytest.mark.slow (a full-gate call over
the real ~11.6k-leaf chain costs ~0.4 s per position); the field tests run in
the default suite.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import verkle_knot as vk  # noqa: E402


def _value_span(data: bytes, marker: bytes, quoted: bool) -> tuple[int, int]:
    """Byte span [start, end) of a top-level tip VALUE in the pretty-printed file."""
    i = data.find(marker)
    assert i >= 0, f"marker {marker!r} not found in tip bytes"
    start = i + len(marker)
    if quoted:
        end = data.find(b'"', start)
        assert end > start, f"no closing quote after {marker!r}"
    else:
        end = start
        while end < len(data) and data[end : end + 1].isdigit():
            end += 1
        assert end > start, f"no digits after {marker!r}"
    return start, end


def _key_span(data: bytes, key: bytes) -> tuple[int, int]:
    """Byte span of the key CONTENT (inside its quotes) of a top-level field."""
    i = data.find(b'"' + key + b'"')
    assert i >= 0, f"key {key!r} not found in tip bytes"
    return i + 1, i + 1 + len(key)


def _mutated(data: bytes, pos: int) -> bytes:
    b = bytearray(data)
    b[pos] = (b[pos] + 1) % 256
    return bytes(b)


@pytest.fixture(scope="session")
def real_estate(tmp_path_factory) -> dict[str, Any]:
    """Copy the LIVE chain+tip pair into tmp under the production writer lock.

    The lock guarantees no writer interleaves between the two copies, so the
    snapshot is an internally consistent pair. The live files are only read.
    """
    out = tmp_path_factory.mktemp("tip_mutation_estate")
    chain_dst = out / "verkle_chain.jsonl"
    tip_dst = out / "verkle_tip.json"
    with vk.verkle_lock(timeout=120.0):
        shutil.copyfile(vk.CHAIN, chain_dst)
        shutil.copyfile(vk.TIP, tip_dst)
    data = tip_dst.read_bytes()

    spans = {
        "root": _value_span(data, b'"root": "', True),
        "n_leaves": _value_span(data, b'"n_leaves": ', False),
        "last_leaf_hash": _value_span(data, b'"last_leaf_hash": "', True),
        "note": _value_span(data, b'"note": "', True),
        "updated_minute": _value_span(data, b'"updated_minute": "', True),
        "key_last_leaf_hash": _key_span(data, b"last_leaf_hash"),
    }
    bound_spans = [spans["root"], spans["n_leaves"], spans["last_leaf_hash"]]

    # Baseline guard: the snapshot itself must verify. If the live pair were
    # ever torn, this fails loudly instead of faking a mutation result.
    old_chain, old_tip = vk.CHAIN, vk.TIP
    vk.CHAIN, vk.TIP = chain_dst, tip_dst
    try:
        ok, why = vk._verify_chain_consistent()
    finally:
        vk.CHAIN, vk.TIP = old_chain, old_tip
    assert ok, f"live snapshot not internally consistent, gate said: {why}"

    return {
        "dir": out,
        "chain": chain_dst,
        "tip": tip_dst,
        "tip_bytes": data,
        "spans": spans,
        "bound_spans": bound_spans,
    }


def _gate(monkeypatch: pytest.MonkeyPatch, estate: dict, tip_path: Path):
    monkeypatch.setattr(vk, "CHAIN", estate["chain"])
    monkeypatch.setattr(vk, "TIP", tip_path)
    return vk._verify_chain_consistent()


def _tampered_copy(estate: dict, name: str, pos: int) -> Path:
    p = estate["dir"] / name
    p.write_bytes(_mutated(estate["tip_bytes"], pos))
    return p


def test_untouched_copy_verifies(real_estate, tmp_path, monkeypatch) -> None:
    """The copy of the real tip verifies before any mutation (baseline)."""
    p = tmp_path / "verkle_tip.json"
    p.write_bytes(real_estate["tip_bytes"])
    ok, why = _gate(monkeypatch, real_estate, p)
    assert ok, why


def test_one_byte_flip_in_root_refused(real_estate, tmp_path, monkeypatch) -> None:
    """HEADLINE: mutate ONE byte of the copy; the verifier refuses it."""
    pos = real_estate["spans"]["root"][0]
    p = _tampered_copy(real_estate, "tip_root_flip.json", pos)
    assert p.read_bytes() != real_estate["tip_bytes"]
    ok, why = _gate(monkeypatch, real_estate, p)
    assert ok is False, f"forgeable tip: byte flip at root[{0}] accepted ({why})"
    assert "tip root mismatch" in why


def test_tampered_index_n_leaves_refused(real_estate, tmp_path, monkeypatch) -> None:
    """Flip one digit of the n_leaves index; the verifier refuses it."""
    pos = real_estate["spans"]["n_leaves"][0]
    p = _tampered_copy(real_estate, "tip_nleaves_flip.json", pos)
    ok, why = _gate(monkeypatch, real_estate, p)
    assert ok is False, f"forgeable tip: index byte flip accepted ({why})"
    assert "n_leaves mismatch" in why


def test_tampered_last_leaf_hash_refused(real_estate, tmp_path, monkeypatch) -> None:
    """Flip one hex char of the tail-hash binding; the verifier refuses it."""
    pos = real_estate["spans"]["last_leaf_hash"][0]
    p = _tampered_copy(real_estate, "tip_tailhash_flip.json", pos)
    ok, why = _gate(monkeypatch, real_estate, p)
    assert ok is False, f"forgeable tip: tail-hash byte flip accepted ({why})"
    assert "last_leaf_hash mismatch" in why


def test_decorative_field_flip_accepted_and_documented(
    real_estate, tmp_path, monkeypatch
) -> None:
    """Banked finding, not a forge: a byte flip inside `note` is NOT refused.

    The gate binds root + n_leaves + last_leaf_hash only; decorative fields
    carry no pointer authority and pass through. The assert proves the accepted
    flip changed none of the three bound fields (parsed tip compared).
    """
    import json

    pos = real_estate["spans"]["note"][0]
    p = _tampered_copy(real_estate, "tip_note_flip.json", pos)
    ok, why = _gate(monkeypatch, real_estate, p)
    assert ok is True, f"decorative flip unexpectedly refused: {why}"
    before = json.loads(real_estate["tip_bytes"])
    after = json.loads(p.read_bytes())
    for field in ("root", "n_leaves", "last_leaf_hash"):
        assert after[field] == before[field], f"{field} moved via a note flip"


def test_last_leaf_hash_key_rename_skips_binding(
    real_estate, tmp_path, monkeypatch
) -> None:
    """Sharp edge: renaming the last_leaf_hash KEY by one byte is ACCEPTED.

    The gate's tail-hash check is guarded on `if tip.get("last_leaf_hash")`,
    so an absent/renamed field silently skips the binding. Root + n_leaves
    still bind the chain identity, so this weakens the tip document, not the
    chain pointer. Exact repro: flip the first key char, gate returns True.
    """
    import json

    start, _ = real_estate["spans"]["key_last_leaf_hash"]
    p = _tampered_copy(real_estate, "tip_key_rename.json", start)
    ok, why = _gate(monkeypatch, real_estate, p)
    assert ok is True, f"key rename unexpectedly refused: {why}"
    after = json.loads(p.read_bytes())
    assert "last_leaf_hash" not in after
    before = json.loads(real_estate["tip_bytes"])
    assert after["root"] == before["root"]
    assert after["n_leaves"] == before["n_leaves"]


@pytest.mark.slow
def test_exhaustive_single_byte_sweep(real_estate, tmp_path, monkeypatch) -> None:
    """Every single-byte mutation of the copy: refused, or provably harmless.

    Property under test: any position the verifier ACCEPTS lies outside the
    three BOUND value spans (root, n_leaves, last_leaf_hash). An accepted flip
    inside a bound span would be a forgeable tip and fails this test.
    """
    data = real_estate["tip_bytes"]
    bound = real_estate["bound_spans"]
    p = estate_tip = real_estate["dir"] / "sweep_tip.json"

    old_chain, old_tip = vk.CHAIN, vk.TIP
    vk.CHAIN, vk.TIP = real_estate["chain"], p
    accepted: list[int] = []
    refused = 0
    try:
        for pos in range(len(data)):
            p.write_bytes(_mutated(data, pos))
            ok, _why = vk._verify_chain_consistent()
            if ok:
                accepted.append(pos)
            else:
                refused += 1
    finally:
        vk.CHAIN, vk.TIP = old_chain, old_tip
        estate_tip.unlink(missing_ok=True)

    assert refused > 0, "verifier accepted every mutation: the tip is forgeable"
    for pos in accepted:
        in_bound = any(a <= pos < b for a, b in bound)
        assert not in_bound, (
            f"forgeable tip: accepted byte flip at position {pos} inside a "
            f"bound value span"
        )
