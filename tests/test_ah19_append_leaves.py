"""tests/test_ah19_append_leaves.py - AH19 (audit finding #10, 2026-09-29/30).

The disease: every re-save of a live session AMENDED its chain row and rewrote
the WHOLE verkle_chain.jsonl (live forensics: 2,821/8,626 rows were amend
rewrites; every rib_bus publish of an unchanged invariant paid a full-file
rewrite too, because the fold stamped now() into the dossier).

The cure (chain_mode=v2 append-leaves, default v1 - live chain untouched until
an operator migrates), pinned here:
  1. v2 appends never rewrite prior rows (byte-prefix property) and never
     unlink prior knots.
  2. N re-saves grow the chain O(N): every earlier snapshot stays a byte
     prefix of the final file and each append adds ~one line of bytes
     (v1's O(n)-bytes-per-save write amplification is impossible).
  3. The verifier passes on pure-v2 chains AND mixed v1→v2 chains (the
     verifier handles v1 rows forever - flipping the flag mid-life is legal).
  4. v1 behavior is untouched: amend-in-place, one row per session, old knot
     unlinked, whole-file rewrite on amend.
  5. chain_mode() maps the configs flag and fails closed to v1.
  6. rib_bus: republishing an UNCHANGED invariant dedupes to a skip (fold
     minute pinned to first-seen ts); a CHANGED store appends exactly one new
     leaf per (domain, version) with the version pointer resolving the latest.
  7. chat_source.file_agent_session surfaces chain_mode/session_seq.

Spec: watch/inbox/last_mile_20260930/AH19_AMEND_PERF.md
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import chat_source as cs  # noqa: E402
from mag import rib_bus  # noqa: E402
from mag import verkle_knot as vk  # noqa: E402


def _dossier(session_id: str, tension: float = 0.25, commit_salt: str = "") -> dict:
    return {
        "session_id": session_id,
        "time": {
            "created_at": {"iso_minute": "2026-09-30T00:00:00Z", "unix_minute": 5000000,
                            "date": "2026-09-30"},
            "updated_at": {"iso_minute": "2026-09-30T00:01:00Z", "unix_minute": 5000001},
        },
        "scalar_knot": {"tension_index": tension, "duration_minutes": 1},
        "content_commit": {"hex": hashlib.sha256(
            f"{session_id}:{commit_salt}".encode()).hexdigest()},
    }


@pytest.fixture()
def estate(tmp_path: Path, monkeypatch) -> Path:
    """Point the whole verkle estate (chain/tip/knots/lock) at tmp_path."""
    monkeypatch.setattr(vk, "ROOT", tmp_path)
    monkeypatch.setattr(vk, "BIO", tmp_path)
    monkeypatch.setattr(vk, "CHAIN", tmp_path / "verkle_chain.jsonl")
    monkeypatch.setattr(vk, "TIP", tmp_path / "verkle_tip.json")
    monkeypatch.setattr(vk, "KNOTS", tmp_path / "knots")
    monkeypatch.setattr(vk, "EVOLUTION", tmp_path / "topic_evolution.json")
    monkeypatch.setattr(vk, "LATEST", tmp_path / "latest.knot.json")
    monkeypatch.setattr(vk, "LOCK", tmp_path / ".verkle.lock")
    (tmp_path / "knots").mkdir(parents=True, exist_ok=True)
    return tmp_path


@pytest.fixture()
def v2(monkeypatch) -> None:
    monkeypatch.setattr(vk, "chain_mode", lambda: vk.CHAIN_MODE_V2)


@pytest.fixture()
def v1(monkeypatch, tmp_path) -> None:
    # CHAIN_HARDEN_ITER2_20261020: flag + fresh approval; pin ROOT to tmp to dodge live fence
    monkeypatch.setenv("MAG_ALLOW_CHAIN_REWRITE", "1")
    monkeypatch.setattr(vk, "chain_mode", lambda: vk.CHAIN_MODE_V1)
    monkeypatch.setattr(vk, "ROOT", tmp_path)
    st = tmp_path / "state"
    st.mkdir(parents=True, exist_ok=True)
    exp = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
    (st / "chain_rewrite_approval.json").write_text(
        json.dumps({"allow": True, "expires_utc": exp, "by": "pytest", "purpose": "ah19_v1"}),
        encoding="utf-8",
    )


def _rows(estate: Path) -> list[dict]:
    text = (estate / "verkle_chain.jsonl").read_text(encoding="utf-8")
    return [json.loads(l) for l in text.splitlines() if l.strip()]


def _chain_bytes(estate: Path) -> bytes:
    return (estate / "verkle_chain.jsonl").read_bytes()


# ── 5. chain_mode() flag mapping (fail-closed to v1) ─────────────────────────

def test_chain_mode_flag_mapping(monkeypatch) -> None:
    import mag.policy as policy

    monkeypatch.setattr(policy, "load_policy", lambda: {"chain_mode": "v2"})
    assert vk.chain_mode() == "v2"
    monkeypatch.setattr(policy, "load_policy", lambda: {"chain_mode": "V1"})
    assert vk.chain_mode() == "v1"
    monkeypatch.setattr(policy, "load_policy", lambda: {})
    assert vk.chain_mode() == "v1", "missing flag must fail closed to v1"
    monkeypatch.setattr(policy, "load_policy", lambda: {"chain_mode": "v3"})
    assert vk.chain_mode() == "v1", "unknown flag value must fail closed to v1"


def test_live_config_is_v2_after_operator_migration() -> None:
    """Operator migrated to chain_mode v2 on 2026-10-17 (AH19 / CHAIN_FIXES)."""
    assert vk.chain_mode() == "v2", (
        "configs/mag.yaml chain_mode must stay v2 after the 2026-10-17 append-only migration")


# ── 1. v2 appends never rewrite prior rows ───────────────────────────────────

def test_v2_append_never_rewrites_prior_rows(estate, v2) -> None:
    r1 = vk.append_verkle_knot(_dossier("sess-ah19", tension=0.1, commit_salt="1"))
    assert r1["ok"] is True and r1["amended"] is False
    assert r1["chain_mode"] == "v2" and r1["session_seq"] == 1
    first_bytes = _chain_bytes(estate)
    first_knot = estate / "knots" / r1["filename"]

    r2 = vk.append_verkle_knot(_dossier("sess-ah19", tension=0.9, commit_salt="2"))
    assert r2["ok"] is True and r2["amended"] is False
    assert r2["session_seq"] == 2, "second save must be a NEW leaf at seq 2"
    assert r2["filename"] != r1["filename"], "seq suffix must keep filenames unique"

    # byte-prefix property: the v1 disease rewrote every prior row; v2 appends
    after = _chain_bytes(estate)
    assert after.startswith(first_bytes), "prior chain bytes were rewritten under v2"
    assert first_knot.is_file(), "v2 must never unlink prior knots (history is canonical)"

    rows = _rows(estate)
    assert len(rows) == 2
    assert [r["session_seq"] for r in rows] == [1, 2]
    assert all(r["chain_mode"] == "v2" for r in rows)


def test_v2_pointer_resolves_latest_with_v1_fallback(estate, v2) -> None:
    vk.append_verkle_knot(_dossier("sess-ah19", commit_salt="1"))
    r2 = vk.append_verkle_knot(_dossier("sess-ah19", commit_salt="2"))
    doc = vk.latest_leaf_for_session("sess-ah19")
    assert doc is not None
    assert doc.get("seq") == 2 and doc.get("leaf_hash") == r2["leaf_hash"]

    # pointer lost → fall back to the LAST matching chain row (exact for v1,
    # and for v2 the tail-most row of the session)
    (estate / "knots" / vk.session_pointer_v2("sess-ah19").name).unlink()
    fb = vk.latest_leaf_for_session("sess-ah19")
    assert fb is not None and fb.get("leaf_hash") == r2["leaf_hash"]


def test_v2_dedupe_is_pointer_driven(estate, v2) -> None:
    d = _dossier("sess-ah19-dup", commit_salt="same")
    r1 = vk.append_verkle_knot(d)
    r2 = vk.append_verkle_knot(json.loads(json.dumps(d)))
    assert r2.get("skipped") is True, "identical content must dedupe to a skip"
    assert r2["session_seq"] == 1, "skip reports the pointer's committed version"
    assert len(_rows(estate)) == 1


def test_v2_consolidation_refuses(estate, v2) -> None:
    vk.append_verkle_knot(_dossier("sess-ah19", commit_salt="1"))
    vk.append_verkle_knot(_dossier("sess-ah19", commit_salt="2"))
    out = vk.consolidate_chain_one_leaf_per_session()
    assert out.get("skipped") is True, "consolidation would destroy v2 seq history"
    assert len(_rows(estate)) == 2


# ── 2. N re-saves grow the file O(N), not O(N^2) ─────────────────────────────

def test_v2_n_resaves_grow_file_linear(estate, v2) -> None:
    seed = 60
    for i in range(seed):
        vk.append_verkle_knot(_dossier(f"sess-seed-{i}", commit_salt=str(i)))

    snapshots = [_chain_bytes(estate)]
    sizes = [len(snapshots[0])]
    resaves = 40
    for i in range(resaves):
        vk.append_verkle_knot(_dossier("sess-seed-0", tension=0.1 + i / 100,
                                       commit_salt=f"re{i}"))
        b = _chain_bytes(estate)
        snapshots.append(b)
        sizes.append(len(b))

    rows = _rows(estate)
    assert len(rows) == seed + resaves, "one line per append, nothing collapsed"

    # append-only: EVERY earlier snapshot is a byte prefix of the final file -
    # a single rewrite anywhere breaks this chain of prefixes.
    final = snapshots[-1]
    for snap in snapshots[:-1]:
        assert final.startswith(snap), "chain was rewritten mid-sequence (O(n) bytes/save)"

    # per-append byte cost stays ~constant (one new line). The v1 disease pays
    # bytes proportional to chain LENGTH per save; here every delta must be a
    # small multiple of the first append's own line, not a multiple of n.
    deltas = [sizes[i + 1] - sizes[i] for i in range(len(sizes) - 1)]
    first_line = deltas[0]
    assert first_line > 0
    assert max(deltas) <= 4 * first_line, (
        f"per-append bytes grew with chain length (max delta {max(deltas)} vs "
        f"first line {first_line}) - O(N^2) write amplification is back")


# ── 3. verifier passes on v2 and mixed v1→v2 chains ──────────────────────────

def test_verify_passes_on_pure_v2_chain(estate, v2) -> None:
    for i in range(5):
        vk.append_verkle_knot(_dossier(f"sess-{i}", commit_salt=str(i)))
    for i in range(5):  # re-saves → multiple rows per session
        vk.append_verkle_knot(_dossier(f"sess-{i}", commit_salt=f"re{i}"))
    ok, why = vk._verify_chain_consistent()
    assert ok is True, why
    assert len(_rows(estate)) == 10


def test_verify_passes_on_mixed_v1_then_v2_chain(estate, monkeypatch) -> None:
    monkeypatch.setenv("MAG_ALLOW_CHAIN_REWRITE", "1")
    monkeypatch.setattr(vk, "chain_mode", lambda: vk.CHAIN_MODE_V1)
    vk.append_verkle_knot(_dossier("sess-mixed-a", commit_salt="1"))
    vk.append_verkle_knot(_dossier("sess-mixed-a", commit_salt="2"))  # v1 amend
    v1_bytes = _chain_bytes(estate)
    assert len(_rows(estate)) == 1

    monkeypatch.setattr(vk, "chain_mode", lambda: vk.CHAIN_MODE_V2)
    vk.append_verkle_knot(_dossier("sess-mixed-a", commit_salt="3"))  # v2 append
    vk.append_verkle_knot(_dossier("sess-mixed-b", commit_salt="4"))

    ok, why = vk._verify_chain_consistent()
    assert ok is True, why
    assert _chain_bytes(estate).startswith(v1_bytes), "v2 must not rewrite the v1 prefix"
    assert len(_rows(estate)) == 3


# ── 4. v1 behavior untouched (amend-in-place stays byte-legal) ───────────────

def test_v1_amend_behavior_untouched(estate, v1, monkeypatch) -> None:
    monkeypatch.setenv("MAG_ALLOW_CHAIN_REWRITE", "1")
    r1 = vk.append_verkle_knot(_dossier("sess-v1", commit_salt="1"))
    assert r1["amended"] is False and r1["chain_mode"] == "v1"
    first_bytes = _chain_bytes(estate)

    r2 = vk.append_verkle_knot(_dossier("sess-v1", commit_salt="2"))
    assert r2["amended"] is True, "v1 must keep amend-in-place semantics"
    assert r2["session_seq"] is None

    rows = _rows(estate)
    assert len(rows) == 1, "v1 keeps one row per session"
    assert rows[0]["leaf_hash"] == r2["leaf_hash"]
    # the whole file WAS rewritten (that is v1's documented cost) and the old
    # knot was unlinked (that is v1's documented single-leaf-per-session state)
    assert not _chain_bytes(estate).startswith(first_bytes) or len(first_bytes) == 0
    assert not (estate / "knots" / r1["filename"]).is_file()


# ── 6. rib_bus: pinned fold minute + one leaf per (domain, version) ──────────

@pytest.fixture()
def rib_estate(estate, monkeypatch, tmp_path) -> Path:
    monkeypatch.setattr(rib_bus, "RIB_DIR", tmp_path / "rib_bus")
    (tmp_path / "rib_bus").mkdir(parents=True, exist_ok=True)
    return tmp_path


def test_rib_bus_republish_unchanged_dedupes(rib_estate, v2) -> None:
    inv = "never rewrite the chain to say the same thing"
    r1 = rib_bus.publish_rib(inv, domain="ah19", source="frontier", publish=False)
    assert r1["ok"] is True and r1["verkle"].get("ok") is True
    assert r1["verkle"]["session_seq"] == 1
    r2 = rib_bus.publish_rib(inv, domain="ah19", source="frontier", publish=False)
    assert r2["verkle"].get("skipped") is True, (
        "republishing an UNCHANGED invariant must dedupe to a skip - before the "
        "first-ts pin the now() minute changed the dossier hash every call")
    assert r2["version"] == 1
    sid_rows = [r for r in _rows(rib_estate) if r.get("session_id") == "rib_bus_ah19"]
    assert len(sid_rows) == 1, "dedupe skip must not append a second leaf"

    store = rib_bus._load_store("ah19")
    entry = store["ribs"][rib_bus._rib_key("ah19", inv)]
    assert entry["first_ts"], "first-seen ts must be persisted for the pin"


def test_rib_bus_first_ts_survives_republish(rib_estate) -> None:
    inv = "first_seen is load-bearing"
    r1 = rib_bus.publish_rib(inv, domain="ah19b", publish=False, fold=False)
    entry1 = rib_bus._load_store("ah19b")["ribs"][r1["key"]]
    import time as _t

    _t.sleep(1.1)  # ensure a fresh _now() minute-precision ts would differ
    rib_bus.publish_rib(inv, domain="ah19b", publish=False, fold=False)
    entry2 = rib_bus._load_store("ah19b")["ribs"][r1["key"]]
    assert entry2["first_ts"] == entry1["first_ts"] == entry1["ts"], (
        "first-seen ts must never drift on republish (the fold minute pins to it)")


def test_rib_bus_one_leaf_per_domain_version(rib_estate, v2) -> None:
    r1 = rib_bus.publish_rib("invariant one", domain="ah19c", publish=False)
    assert r1["version"] == 1
    r2 = rib_bus.publish_rib("invariant two", domain="ah19c", publish=False)
    assert r2["version"] == 2, "a changed store appends the next version leaf"

    rows = [r for r in _rows(rib_estate) if r.get("session_id") == "rib_bus_ah19c"]
    assert [r["session_seq"] for r in rows] == [1, 2], (
        "one leaf per (domain, version): session_seq IS the version")
    assert rows[0]["leaf_hash"] != rows[1]["leaf_hash"]

    doc = vk.latest_leaf_pointer("rib_bus_ah19c")
    assert doc is not None and doc.get("seq") == 2, "version pointer resolves latest"
    ok, why = vk._verify_chain_consistent()
    assert ok is True, why


# ── 7. chat_source surfaces the chain write model ────────────────────────────

def test_file_agent_session_surfaces_chain_mode(tmp_path, monkeypatch) -> None:
    seat = "_pytest_ah19_seat"
    seat_dir = tmp_path / "agent_sessions"
    monkeypatch.setattr(cs, "AGENT_SESS_DIR", seat_dir)
    seat_dir.mkdir(parents=True, exist_ok=True)
    (seat_dir / f"{seat}.json").write_text(json.dumps({
        "session_id": seat, "provider": "ollama", "model": "gemma:2b",
        "messages": [
            {"role": "user", "content": "pytest ah19: file this seat"},
            {"role": "assistant", "content": "filing one v2 leaf"},
        ],
    }), encoding="utf-8")

    import mag.biography as bio

    def fake_summarize(session_id, **kwargs):
        return {"ok": True, "session_id": session_id,
                "verkle": {"ok": True, "chain_mode": "v2", "session_seq": 3}}

    monkeypatch.setattr(bio, "summarize_session", fake_summarize)
    res = cs.file_agent_session(seat, use_llm=False)
    assert res["ok"] is True
    assert res["chain_mode"] == "v2", "the chain write model must be surfaced"
    assert res["session_seq"] == 3

    def fake_v1(session_id, **kwargs):
        return {"ok": True, "session_id": session_id,
                "verkle": {"ok": True, "chain_mode": "v1", "session_seq": None}}

    monkeypatch.setattr(bio, "summarize_session", fake_v1)
    res = cs.file_agent_session(seat, use_llm=False)
    assert res["chain_mode"] == "v1"
    assert "session_seq" not in res, "v1 has no seq - nothing to surface"
