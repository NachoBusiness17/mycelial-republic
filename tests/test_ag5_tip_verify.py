"""tests/test_ag5_tip_verify.py — AG5 (audit finding #3, 2026-09-30).

Three diseases, three cures, all pinned here:
  A. The MAIN append path wrote the verkle tip with plain ``TIP.write_text``
     while ``_write_tip_atomic`` existed for exactly the torn-write disease.
     Pinned via a monkeypatch spy on both main-path writes (normal append and
     the CHAIN_RACE_REPAIR heal branch).
  B. No launch path verified the chain — the context-pack tip badge was a raw
     read. Pinned: the badge carries a verify verdict, a failed (or timed-out,
     or raising) verify renders ``tip: UNVERIFIED (<reason>)``, and boot is
     never blocked by the check.
  C. hermes_warm_boot._chain_tip reported keys ``leaves``/``tag`` that chain
     rows never carry (rows use ``n_leaves``/``dominant_theme``), so both
     fields were always empty; and --verify echoed a flag without running the
     gate. Pinned: row-schema field names + a real _verify_chain_consistent
     call behind --verify.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import context_pack as cp  # noqa: E402
from mag import hermes_warm_boot as hw  # noqa: E402
from mag import verkle_knot as vk  # noqa: E402


def _dossier(session_id: str, tension: float = 0.25) -> dict:
    return {
        "session_id": session_id,
        "time": {
            "created_at": {"iso_minute": "2026-09-30T00:00:00Z", "unix_minute": 5000000,
                            "date": "2026-09-30"},
            "updated_at": {"iso_minute": "2026-09-30T00:01:00Z", "unix_minute": 5000001},
        },
        "scalar_knot": {"tension_index": tension, "duration_minutes": 1},
        "content_commit": {"hex": hashlib.sha256(session_id.encode()).hexdigest()},
    }


@pytest.fixture()
def estate(tmp_path: Path, monkeypatch) -> Path:
    """Point the whole verkle estate (chain/tip/knots/lock) at tmp_path."""
    monkeypatch.setattr(vk, "CHAIN", tmp_path / "verkle_chain.jsonl")
    monkeypatch.setattr(vk, "TIP", tmp_path / "verkle_tip.json")
    monkeypatch.setattr(vk, "KNOTS", tmp_path / "knots")
    monkeypatch.setattr(vk, "EVOLUTION", tmp_path / "topic_evolution.json")
    monkeypatch.setattr(vk, "LATEST", tmp_path / "latest.knot.json")
    monkeypatch.setattr(vk, "LOCK", tmp_path / ".verkle.lock")
    (tmp_path / "knots").mkdir(parents=True, exist_ok=True)
    return tmp_path


def _spy_atomic(monkeypatch) -> list[dict]:
    """Wrap vk._write_tip_atomic with a recording spy (calls the real one)."""
    calls: list[dict] = []
    real = vk._write_tip_atomic

    def spy(tip: dict) -> None:
        calls.append(dict(tip))
        return real(tip)

    monkeypatch.setattr(vk, "_write_tip_atomic", spy)
    return calls


# ── A: atomic tip writes on the main append path ────────────────────────────

def test_append_path_writes_tip_atomically(estate, monkeypatch) -> None:
    calls = _spy_atomic(monkeypatch)
    res = vk.append_verkle_knot(_dossier("sess-ag5-append"))
    assert res["ok"] is True, res
    assert len(calls) == 1, "main append must write the tip through _write_tip_atomic"
    tip_on_disk = json.loads((estate / "verkle_tip.json").read_text(encoding="utf-8"))
    assert tip_on_disk["root"] == res["verkle_root"]
    assert tip_on_disk["n_leaves"] == 1


def test_heal_path_writes_tip_atomically(estate, monkeypatch) -> None:
    """CHAIN_RACE_REPAIR heal branch: force it and pin its tip write is atomic.

    Simulates the race class the heal exists for: the append computes a
    poisoned root for its own row (first single-leaf _merkle_root call is
    stubbed), then the post-append verify fails — the heal must rewrite the
    row's roots from disk truth and re-write the tip ATOMICALLY.
    """
    calls = _spy_atomic(monkeypatch)

    real_verify = vk._verify_chain_consistent
    seq = {"n": 0}

    def seq_verify():
        seq["n"] += 1
        if seq["n"] == 1:
            return real_verify()  # pre-append gate passes (genesis)
        return False, "simulated post-append race"  # triggers the heal branch

    monkeypatch.setattr(vk, "_verify_chain_consistent", seq_verify)

    real_merkle = vk._merkle_root
    poisoned = {"done": False}

    def poison_first_root(hashes):
        # first full-list (single-leaf) root call is the append's own row root
        if not poisoned["done"] and len(hashes) == 1:
            poisoned["done"] = True
            return "f" * 64
        return real_merkle(hashes)

    monkeypatch.setattr(vk, "_merkle_root", poison_first_root)

    res = vk.append_verkle_knot(_dossier("sess-ag5-heal"))
    assert res["ok"] is True, res
    assert len(calls) == 2, "heal branch must re-write the tip through _write_tip_atomic"
    # healed tip points at the recomputed-from-disk root, not the poisoned one
    tip_on_disk = json.loads((estate / "verkle_tip.json").read_text(encoding="utf-8"))
    assert tip_on_disk["root"] == calls[-1]["root"]
    assert tip_on_disk["root"] != "f" * 64
    row = json.loads((estate / "verkle_chain.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert row["verkle_root"] == tip_on_disk["root"]


# ── B: context-pack tip badge is a verdict, not a raw read ──────────────────

def _pack(tip_extra: dict) -> dict:
    tip = {
        "ok": True, "root_short": "abcdef012345…", "n_leaves": 7,
        "last_filename": "x.knot.json", "dig_edges_n": 0,
    }
    tip.update(tip_extra)
    return {"mode": "janitor", "ts": "2026-09-30T00:00:00", "tip": tip}


def test_unverified_tip_renders_reason() -> None:
    reason = "tip root mismatch (tip aaaa1111 vs recomputed bbbb2222)"
    text = cp.format_context_pack_text(_pack({"verified": False, "verify_reason": reason}),
                                       mode="janitor")
    assert f"- tip: UNVERIFIED ({reason})" in text
    # the confident raw badge is gone — no root/leaves claim beside the verdict
    assert "abcdef012345" not in text


def test_verified_tip_renders_badge_normally() -> None:
    text = cp.format_context_pack_text(_pack({"verified": True, "verify_reason": "chain consistent"}),
                                       mode="janitor")
    assert "UNVERIFIED" not in text
    assert "- tip: abcdef012345…" in text


def test_agent_preamble_rides_same_verdict() -> None:
    text = cp.format_agent_preamble(_pack({"verified": False, "verify_reason": "verify timeout >2s"}))
    assert "tip=UNVERIFIED (verify timeout >2s)" in text


def test_verify_tip_chain_flags_tamper(estate) -> None:
    vk.append_verkle_knot(_dossier("sess-ag5-a"))
    vk.append_verkle_knot(_dossier("sess-ag5-b"))
    rows = [json.loads(l) for l in
            (estate / "verkle_chain.jsonl").read_text(encoding="utf-8").splitlines()]
    rows[0]["leaf_hash"] = "0" * 64  # tamper -> recomputed root mismatch
    (estate / "verkle_chain.jsonl").write_text(
        "".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8", newline="")
    ok, why = cp._verify_tip_chain()
    assert ok is False
    assert "mismatch" in why


def test_verify_tip_chain_passes_clean_chain(estate) -> None:
    vk.append_verkle_knot(_dossier("sess-ag5-clean"))
    ok, why = cp._verify_tip_chain()
    assert ok is True, why


def test_verify_tip_chain_timeout_never_blocks(monkeypatch) -> None:
    def slow_verify():
        time.sleep(1.0)
        return True, "late"
    monkeypatch.setattr(vk, "_verify_chain_consistent", slow_verify)
    ok, why = cp._verify_tip_chain(timeout_s=0.1)
    assert ok is False and "timeout" in why


def test_verify_tip_chain_survives_raise(monkeypatch) -> None:
    def raising_verify():
        raise RuntimeError("chain unreadable")
    monkeypatch.setattr(vk, "_verify_chain_consistent", raising_verify)
    ok, why = cp._verify_tip_chain(timeout_s=2.0)
    assert ok is False and "verify raised" in why


def test_build_context_pack_carries_verify_verdict() -> None:
    pack = cp.build_context_pack(mode="janitor", fast=True)
    assert isinstance(pack["tip"].get("verified"), bool), (
        "tip badge lost its verify verdict — the launch path verifies nothing again")
    assert "verify_reason" in pack["tip"]


# ── C: hermes warm boot field names + real --verify ─────────────────────────

def _chain_row(sid: str = "sess-ag5") -> dict:
    leaf_hash = hashlib.sha256(sid.encode()).hexdigest()
    return {
        "ts": "2026-09-30T00:00:00Z", "filename": f"{sid}.knot.json",
        "leaf_hash": leaf_hash, "session_id": sid, "index": 41, "n_leaves": 42,
        "dominant_theme": "mag_hands",
        "parent_verkle_root": "a" * 64, "verkle_root": "b" * 64,
    }


def test_chain_tip_reports_row_schema_fields(tmp_path, monkeypatch) -> None:
    chain = tmp_path / "verkle_chain.jsonl"
    chain.write_text(json.dumps(_chain_row()) + "\n", encoding="utf-8")
    monkeypatch.setattr(hw, "CHAIN", chain)
    tip = hw._chain_tip()
    assert tip["ok"] is True
    assert tip["n_leaves"] == 42          # was always empty under the old "leaves" key
    assert tip["dominant_theme"] == "mag_hands"  # was always empty under "tag"
    assert "leaves" not in tip and "tag" not in tip


def test_warm_boot_verify_runs_the_real_gate(monkeypatch) -> None:
    monkeypatch.setattr(vk, "_verify_chain_consistent",
                        lambda: (True, "chain consistent (2 leaves)"))
    state = hw.warm_boot(verify=True)
    assert state["chain_verify"] == {"ok": True, "reason": "chain consistent (2 leaves)"}

    monkeypatch.setattr(vk, "_verify_chain_consistent",
                        lambda: (False, "last row root mismatch"))
    state = hw.warm_boot(verify=True)
    assert state["chain_verify"]["ok"] is False
    assert "mismatch" in state["chain_verify"]["reason"]


def test_warm_boot_without_verify_runs_no_gate(monkeypatch) -> None:
    def boom():  # the gate must not even be imported-called without --verify
        raise AssertionError("verify ran without --verify")
    monkeypatch.setattr(vk, "_verify_chain_consistent", boom)
    state = hw.warm_boot(verify=False)
    assert "chain_verify" not in state
