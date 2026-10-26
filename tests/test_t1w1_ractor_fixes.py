"""tests/test_t1w1_ractor_fixes.py - T1W1 RACTOR EASY tickets (2026-10-01).

Pins the landed fixes distilled from the four stranger audits
(watch/inbox/hermes_burn/T1W1_RACTOR.md, BUILD REPORT section):

  ticket 2   hermes_warm_boot session_brief freshness is the artifact mtime,
             never the reader's clock (law L4)
  ticket 4   chain_repair's tip write rides _write_tip_atomic
  ticket 7   _verify_chain_consistent fails closed on a corrupt, absent,
             empty or count-lying tip over a non-empty chain
  ticket 8   knot retirement MOVES to a knots_attic sibling (never unlink);
             consolidate defers retirement until the conflicts check passes
  ticket 9   _rewrite_chain lands tmp + os.replace (no mid-amend truncation)
  ticket 11  grounding G2 bindings carry the FULL sha256; every read side
             still accepts the legacy 12-char cut for pre-2026-10 rows
  ticket 12  VerkleProof.verify binds the leaf count (index range + depth)

Every test runs against synthetic estates in tmp dirs; the live chain, tip,
knots, grounding tape and brief are never touched.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import grounding_wave as gw  # noqa: E402
from mag import hermes_warm_boot as hw  # noqa: E402
from mag import verkle_knot as vk  # noqa: E402


def _doss(session_id: str, salt: str = "1") -> dict:
    return {
        "session_id": session_id,
        "time": {
            "created_at": {"iso_minute": "2026-10-01T00:00:00Z", "unix_minute": 5000000,
                           "date": "2026-10-01"},
            "updated_at": {"iso_minute": "2026-10-01T00:01:00Z", "unix_minute": 5000001},
        },
        "scalar_knot": {"tension_index": 0.25, "duration_minutes": 1},
        "content_commit": {"hex": hashlib.sha256((session_id + salt).encode()).hexdigest()},
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


# ── ticket 7: the integrity gate fails closed on a lying tip ────────────────

def test_gate_refuses_corrupt_absent_and_empty_tip(estate) -> None:
    vk.append_verkle_knot(_doss("s7a"))
    vk.append_verkle_knot(_doss("s7b"))
    good_tip = vk.TIP.read_text(encoding="utf-8")

    vk.TIP.write_text("{not json", encoding="utf-8")
    ok, why = vk._verify_chain_consistent()
    assert ok is False and "missing or unreadable" in why

    vk.TIP.unlink()
    ok, why = vk._verify_chain_consistent()
    assert ok is False and "missing or unreadable" in why

    vk.TIP.write_text("{}", encoding="utf-8")
    ok, why = vk._verify_chain_consistent()
    assert ok is False and "missing or unreadable" in why

    vk.TIP.write_text(good_tip, encoding="utf-8")
    ok, why = vk._verify_chain_consistent()
    assert ok is True, why


def test_gate_refuses_count_lying_tip(estate) -> None:
    """A root alone does not bind leaf count under duplicate-last padding."""
    vk.append_verkle_knot(_doss("s7c"))
    vk.append_verkle_knot(_doss("s7d"))
    tip = json.loads(vk.TIP.read_text(encoding="utf-8"))

    tip["n_leaves"] = tip["n_leaves"] + 1
    vk.TIP.write_text(json.dumps(tip), encoding="utf-8")
    ok, why = vk._verify_chain_consistent()
    assert ok is False and "n_leaves mismatch" in why

    tip["n_leaves"] -= 2
    vk.TIP.write_text(json.dumps(tip), encoding="utf-8")
    ok, why = vk._verify_chain_consistent()
    assert ok is False and "n_leaves mismatch" in why


def test_corrupt_tip_blocks_append_then_heals_via_repair(estate) -> None:
    vk.append_verkle_knot(_doss("s7e"))
    vk.TIP.write_text("{torn", encoding="utf-8")

    res = vk.append_verkle_knot(_doss("s7f"))
    assert res["ok"] is False and "refusing to extend" in res["error"]

    healed = vk.repair_tip_if_consistent()
    assert healed["ok"] is True and healed["repaired"] is True
    ok, why = vk._verify_chain_consistent()
    assert ok is True, why
    assert vk.append_verkle_knot(_doss("s7f"))["ok"] is True


# ── ticket 8: retirement moves to an attic, refusal retires nothing ─────────

def test_v1_amend_retires_old_knot_to_attic(estate) -> None:
    r1 = vk.append_verkle_knot(_doss("s8", "salt1"))
    old_knot = vk.KNOTS / r1["filename"]
    assert old_knot.is_file()

    r2 = vk.append_verkle_knot(_doss("s8", "salt2"))
    assert r2["amended"] is True
    assert not old_knot.is_file(), "retired knot must leave the KNOTS namespace"
    attic = estate / "knots_attic" / r1["filename"]
    assert attic.is_file(), "the pre-amend leaf must survive a mid-amend crash"
    assert (estate / "knots_attic").parent == estate, "attic is a KNOTS sibling, never inside it"
    ok, why = vk._verify_chain_consistent()
    assert ok is True, why


def test_consolidate_refusal_retires_nothing(estate) -> None:
    vk.append_verkle_knot(_doss("s8a"))
    r_b = vk.append_verkle_knot(_doss("s8b"))
    rows = vk._load_chain_rows()
    first_knot = vk.KNOTS / rows[0]["filename"]
    assert first_knot.is_file()

    dup = dict(rows[0])
    dup["filename"] = "other.knot.json"
    conflicting = dict(rows[0])
    conflicting["leaf_hash"] = "e" * 64  # same sid, different leaf: refusal class
    (vk.KNOTS / "other.knot.json").write_text("{}", encoding="utf-8")
    vk.CHAIN.write_bytes(
        ("\n".join(json.dumps(r, ensure_ascii=False)
                   for r in rows + [dup, conflicting]) + "\n").encode("utf-8"))

    out = vk.consolidate_chain_one_leaf_per_session()
    assert out["ok"] is False and "conflicting" in out["error"]
    assert first_knot.is_file(), "a refusing repair must not retire any knot"
    assert (vk.KNOTS / "other.knot.json").is_file()
    assert not (estate / "knots_attic" / "other.knot.json").is_file()
    assert not (estate / "knots_attic" / rows[0]["filename"]).is_file()


def test_consolidate_success_retires_superseded_knot(estate) -> None:
    vk.append_verkle_knot(_doss("s8c"))
    vk.append_verkle_knot(_doss("s8d"))
    rows = vk._load_chain_rows()
    superseded = vk.KNOTS / rows[0]["filename"]
    assert superseded.is_file()

    dup = dict(rows[0])
    dup["filename"] = "renamed.knot.json"
    (vk.KNOTS / "renamed.knot.json").write_text("{}", encoding="utf-8")
    vk.CHAIN.write_bytes(
        ("\n".join(json.dumps(r, ensure_ascii=False) for r in rows + [dup]) + "\n").encode("utf-8"))

    out = vk.consolidate_chain_one_leaf_per_session()
    assert out["ok"] is True, out
    assert not superseded.is_file()
    assert (estate / "knots_attic" / rows[0]["filename"]).is_file()


# ── ticket 9: chain rewrite is atomic and byte-exact ────────────────────────

def test_rewrite_chain_atomic_no_residue_lf_only(estate) -> None:
    for i in range(3):
        vk.append_verkle_knot(_doss(f"s9-{i}"))
    before = vk.CHAIN.read_bytes()

    res = vk.append_verkle_knot(_doss("s9-0", "amended"))  # v1 amend rewrites the file
    assert res["amended"] is True
    chain_bytes = vk.CHAIN.read_bytes()
    assert b"\r" not in chain_bytes, "CRLF leaked into the chain (B2-393 law)"
    assert chain_bytes != before, "the amend must have rewritten the file"
    assert not list(estate.glob("*.tmp")), "atomic rewrite left tmp residue"
    ok, why = vk._verify_chain_consistent()
    assert ok is True, why


# ── ticket 12: the proof binds the leaf count ───────────────────────────────

def test_proof_verify_binds_leaf_count(estate) -> None:
    for i in range(6):
        vk.append_verkle_knot(_doss(f"s12-{i}"))
    p = vk.prove()
    n = p["n_leaves"]
    assert p["verified"] is True, "prove's self-check binds n"

    proof = vk.VerkleProof(index=p["index"], leaf_hash=p["leaf_hash"],
                           path=p["path"], root=p["root"])
    assert proof.verify(n_leaves=n) is True
    # replay onto a claimed count that excludes this index must refuse
    assert proof.verify(n_leaves=p["index"]) is False
    # NB: a claimed n in the SAME ceil(log2) band with the same root cannot be
    # distinguished inside the proof (duplicate-last padding, CVE-2012-2459
    # class); that residual is closed by the tip binding root AND count as a
    # pair, which ticket 7's gate enforces against the recomputed truth.
    # cross-band count (wrong path depth) must refuse
    assert proof.verify(n_leaves=2) is False
    # forged out-of-range index
    forged = vk.VerkleProof(index=n + 3, leaf_hash=p["leaf_hash"],
                            path=p["path"], root=p["root"])
    assert forged.verify(n_leaves=n) is False
    # legacy call without n keeps the root-only check
    assert proof.verify() is True


# ── ticket 4: chain_repair's tip rides the atomic writer ────────────────────

def test_chain_repair_tip_rides_atomic_writer(estate, monkeypatch) -> None:
    for i in range(3):
        vk.append_verkle_knot(_doss(f"s4-{i}"))
    rows = vk._load_chain_rows()
    rows[-1]["verkle_root"] = "a" * 64  # the committed-race class the tool heals
    vk.CHAIN.write_bytes(
        ("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n").encode("utf-8"))
    ok, _ = vk._verify_chain_consistent()
    assert ok is False

    import tools.chain_repair as cr
    monkeypatch.setattr(cr, "CHAIN", vk.CHAIN)
    monkeypatch.setattr(cr, "TIP", vk.TIP)
    calls: list[dict] = []
    real = vk._write_tip_atomic

    def spy(tip: dict) -> None:
        calls.append(dict(tip))
        return real(tip)

    monkeypatch.setattr(cr, "_write_tip_atomic", spy)

    assert cr.repair() == 0
    assert len(calls) == 1, "the repaired tip must go through _write_tip_atomic"
    ok, why = vk._verify_chain_consistent()
    assert ok is True, why
    assert not list(estate.glob("*.tmp"))


# ── ticket 2: brief freshness is the artifact's own mtime ───────────────────

def test_session_brief_reports_mtime_not_read_time(tmp_path: Path, monkeypatch) -> None:
    brief = tmp_path / "latest.md"
    brief.write_text("frozen brief bytes", encoding="utf-8")
    frozen = datetime(2026, 9, 26, 18, 1, 29, tzinfo=timezone.utc)
    os.utime(brief, (frozen.timestamp(), frozen.timestamp()))
    monkeypatch.setattr(hw, "BRIEF", brief)

    sb = hw._session_brief()
    assert sb["ok"] is True
    got = datetime.fromisoformat(sb["updated"])
    assert got == frozen, "a FROZEN brief must read as frozen, not updated-now"
    assert (datetime.now(timezone.utc) - got).days >= 5


# ── ticket 11: G2 bindings widen to the full digest, reads take both ────────

@pytest.fixture()
def wave(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(gw, "LEDGER", tmp_path / "GROUNDING_WAVE.jsonl")
    monkeypatch.setattr(gw, "LOCK", tmp_path / "GROUNDING_WAVE.lock")
    monkeypatch.setattr(gw, "VIEW_MD", tmp_path / "view.md")
    monkeypatch.setattr(gw, "VIEW_STATIC", tmp_path / "view_static.md")
    return gw


def test_g2_binding_is_full_digest(wave, tmp_path: Path) -> None:
    ev = tmp_path / "g2ev.md"
    ev.write_text("original bytes", encoding="utf-8")
    wave.post("bound claim", "UNPROVEN", ev.as_posix(), seat="a")

    row = gw._rows()[0]
    full = hashlib.sha256(b"original bytes").hexdigest()
    bound = row["src_sha256_12"][ev.as_posix()]
    assert len(bound) == 64 and bound == full, "new bindings carry the full sha256"

    # read sides accept BOTH widths for the same bytes
    assert gw._src_ok(ev.as_posix(), full) is True
    assert gw._src_ok(ev.as_posix(), full[:12]) is True  # legacy rows keep verifying
    assert gw._src_ok(ev.as_posix(), "0" * 12) is False
    assert gw._src_ok(ev.as_posix(), "0" * 64) is False

    # mutation is flagged at full width, and legacy-width rows still audit clean
    assert gw._evidence_mutated(gw._rows()) == []
    rows = gw._rows()
    rows[0]["src_sha256_12"][ev.as_posix()] = full[:12]  # simulate a legacy row
    assert gw._evidence_mutated(rows) == []
    ev.write_text("mutated bytes", encoding="utf-8")
    assert gw._evidence_mutated(gw._rows()) != [], "mutated evidence must be flagged"
