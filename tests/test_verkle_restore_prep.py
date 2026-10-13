"""tests/test_verkle_restore_prep.py — fixture-estate tests for the Q-001
restore prep (tools/verkle_restore_prep.py, Y11 lane 2026-09-30).

The law under test: --dry reports the full plan (row count, knot paths,
expected tip) and writes nothing; --confirm executes ONLY with the literal
OPERATOR-GO-Q001 string, copies verified backup bytes back into knots/,
re-links every restored row by hash, verifies the full chain post-restore,
and leaves chain/tip/marker/ledger byte-exact.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag.verkle_knot import _merkle_root, build_leaf_from_dossier  # noqa: E402
from tools.verkle_dangling_repair import Estate, classify  # noqa: E402
from tools.verkle_restore_prep import main  # noqa: E402

GATE = "OPERATOR-GO-Q001"


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


def _knot_doc(leaf: dict, filename: str) -> dict:
    doc = dict(leaf)
    doc["filename"] = filename  # fold() adds filename AFTER hashing — mirror it
    return doc


@pytest.fixture()
def estate(tmp_path: Path) -> Estate:
    """Fixture chain shaped like the live Q-001 surface:
      row 0 healthy     knot lives in knots/
      row 1 flagged     dangling + evidence_lost on the row (stays dangling)
      row 2 recoverable dangling, one hash-verified backup copy
      row 3 recoverable dangling, TWO verified copies (old + new backup) —
                        the TAIL row, so the restore must also refresh
                        latest.knot.json (the _sync_latest_knot law)
    """
    es = Estate(tmp_path)
    es.knots.mkdir(parents=True, exist_ok=True)
    old_backup = es.root / "memory" / "biography_backup_20260921" / "knots"
    new_backup = es.root / "memory" / "biography_backup_20260926" / "knots"
    old_backup.mkdir(parents=True, exist_ok=True)
    new_backup.mkdir(parents=True, exist_ok=True)

    sids = ("sess-healthy", "sess-flagged", "sess-recov-a", "sess-recov-b")
    leaves = {sid: build_leaf_from_dossier(_dossier(sid)) for sid in sids}
    fn = {sid: f"2026-09-30_0000_session_{sid}_{leaves[sid]['leaf_hash'][:8]}.knot.json"
          for sid in sids}

    (es.knots / fn["sess-healthy"]).write_text(
        json.dumps(_knot_doc(leaves["sess-healthy"], fn["sess-healthy"])), encoding="utf-8")
    (old_backup / fn["sess-recov-a"]).write_text(
        json.dumps(_knot_doc(leaves["sess-recov-a"], fn["sess-recov-a"])), encoding="utf-8")
    # recoverable B exists in BOTH backups; the newer one (20260926) must win
    (old_backup / fn["sess-recov-b"]).write_text(
        json.dumps(_knot_doc(leaves["sess-recov-b"], fn["sess-recov-b"])), encoding="utf-8")
    (new_backup / fn["sess-recov-b"]).write_text(
        json.dumps(_knot_doc(leaves["sess-recov-b"], fn["sess-recov-b"])), encoding="utf-8")

    rows = []
    for i, sid in enumerate(sids):
        row = {
            "ts": "2026-09-30T00:00:00Z",
            "filename": fn[sid],
            "leaf_hash": leaves[sid]["leaf_hash"],
            "session_id": sid,
            "amended": False,
            "index": i,
            "n_leaves": i + 1,
        }
        if sid == "sess-flagged":
            row["evidence_lost"] = True
        rows.append(row)
    hashes = [r["leaf_hash"] for r in rows]
    root = _merkle_root(hashes)
    rows[-1]["verkle_root"] = root  # the chain-consistency law needs the tail root
    es.chain.parent.mkdir(parents=True, exist_ok=True)
    es.chain.write_text("".join(json.dumps(r) + "\n" for r in rows),
                        encoding="utf-8", newline="")
    es.tip.write_text(json.dumps({
        "schema": "verkle_tip.v1", "root": root, "n_leaves": len(hashes),
        "last_filename": fn["sess-recov-b"],
        "last_leaf_hash": hashes[-1], "last_session_id": "sess-recov-b",
    }, indent=2) + "\n", encoding="utf-8")
    return es


def _sha(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def _rows(es: Estate) -> list[dict]:
    return [json.loads(l) for l in es.chain.read_text(encoding="utf-8").splitlines() if l.strip()]


def _classified(es: Estate) -> None:
    """Produce the side ledger the restore consumes (the W3n classify step)."""
    result = classify(es, es.default_ledger)
    assert result["ok"] and result["recoverable_by_hash"] == 2


def test_dry_reports_plan_and_writes_nothing(estate: Estate, capsys) -> None:
    _classified(estate)
    before = {"chain": _sha(estate.chain), "tip": _sha(estate.tip),
              "ledger": _sha(estate.default_ledger),
              "knots": sorted(p.name for p in estate.knots.iterdir())}
    assert main(["--dry", "--root", str(estate.root)]) == 0
    report = json.loads(capsys.readouterr().out)

    assert report["mode"] == "dry" and report["ok"] is True
    assert report["rows_to_restore"] == 2
    assert report["rows_already_present"] == 0
    copies = {c["session_id"]: c for c in report["knot_copies"]}
    assert set(copies) == {"sess-recov-a", "sess-recov-b"}
    for c in copies.values():
        assert (estate.root / c["source"]).is_file()      # real backup bytes
        assert c["dest"].endswith(c["filename"])          # lands in knots/
        assert c["dest"].startswith("memory")
    # newest backup wins for the double-copy row
    assert "biography_backup_20260926" in copies["sess-recov-b"]["source"]

    root = _merkle_root([r["leaf_hash"] for r in _rows(estate)])
    assert report["expected_tip"]["root"] == root
    assert report["expected_tip"]["live_tip_matches_chain"] is True
    assert report["post_restore"] == {"dangling_before": 3, "dangling_after_expected": 1,
                                      "dangling_unflagged_after_expected": 0}
    assert report["writes"] == "NONE — dry reports only"
    assert report["gate"].endswith("any other confirm string refuses")

    # byte-exact no-write across every surface the tool can see
    assert _sha(estate.chain) == before["chain"]
    assert _sha(estate.tip) == before["tip"]
    assert _sha(estate.default_ledger) == before["ledger"]
    assert sorted(p.name for p in estate.knots.iterdir()) == before["knots"]
    assert not (estate.tip.parent / ".verkle.lock").exists()  # no lock left behind


def test_confirm_restores_end_to_end_and_is_idempotent(estate: Estate, capsys) -> None:
    _classified(estate)
    before = {"chain": _sha(estate.chain), "tip": _sha(estate.tip),
              "ledger": _sha(estate.default_ledger),
              "marker": _sha(estate.marker)}
    old_backup = (estate.root / "memory" / "biography_backup_20260921" / "knots")
    rows = {r["session_id"]: r for r in _rows(estate)}

    assert main(["--confirm", GATE, "--root", str(estate.root)]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["ok"] is True and report["restored"] == 2

    # the knots came back as the backup bytes, hash-linked to their rows
    for sid in ("sess-recov-a", "sess-recov-b"):
        dst = estate.knots / rows[sid]["filename"]
        assert dst.is_file()
        src = old_backup / rows[sid]["filename"]
        assert dst.read_bytes() == src.read_bytes()       # byte-exact re-embed
    verify = report["full_chain_verify"]
    assert verify["ok"] and verify["restored_links_verified"] == 2
    assert verify["dangling"] == 1                        # only the flagged row remains
    assert verify["dangling_unaccounted_effective"] == 0  # regression cleared
    assert report["chain_moved_under_lock"] is None
    assert report["planned_rows_intact"] is True
    # the TAIL row was restored -> latest.knot.json mirrors it again
    latest = estate.tip.with_name("latest.knot.json")
    assert report["latest_knot_refreshed"] is not None and latest.is_file()
    assert latest.read_bytes() == (estate.knots / rows["sess-recov-b"]["filename"]).read_bytes()
    # expected tip was computed from the chain and matches the untouched tip
    assert report["expected_tip"]["live_tip_matches_chain"] is True

    # chain/tip/marker/ledger byte-exact through the write path
    assert _sha(estate.chain) == before["chain"]
    assert _sha(estate.tip) == before["tip"]
    assert _sha(estate.default_ledger) == before["ledger"]
    assert _sha(estate.marker) == before["marker"]

    # idempotent rerun: everything already present, nothing copied, still green
    assert main(["--confirm", GATE, "--root", str(estate.root)]) == 0
    again = json.loads(capsys.readouterr().out)
    assert again["ok"] and again["restored"] == 0 and again["already_present"] == 2


def test_wrong_confirm_string_refuses_without_writes(estate: Estate, capsys) -> None:
    _classified(estate)
    before_knots = sorted(p.name for p in estate.knots.iterdir())
    before_chain = _sha(estate.chain)

    assert main(["--confirm", "OPERATOR-GO-Q001-typo", "--root", str(estate.root)]) == 3
    refusal = json.loads(capsys.readouterr().out)
    assert refusal["refused"] is True and GATE in refusal["error"]
    assert "nothing was written" in refusal["error"]

    assert sorted(p.name for p in estate.knots.iterdir()) == before_knots
    assert _sha(estate.chain) == before_chain
    assert not (estate.tip.parent / ".verkle.lock").exists()


def test_tampered_backup_is_skipped_by_hash(estate: Estate, capsys) -> None:
    """Trust bytes, not reports: a backup altered after classification must
    NOT be restored even though the ledger still lists it as recoverable."""
    _classified(estate)
    rows = {r["session_id"]: r for r in _rows(estate)}
    src = estate.root / "memory" / "biography_backup_20260921" / "knots" / rows["sess-recov-a"]["filename"]
    doc = json.loads(src.read_text(encoding="utf-8"))
    doc["tension_index"] = 0.99  # content no longer recomputes to the leaf_hash
    src.write_text(json.dumps(doc), encoding="utf-8")

    assert main(["--confirm", GATE, "--root", str(estate.root)]) == 1  # incomplete
    report = json.loads(capsys.readouterr().out)
    assert report["ok"] is False
    assert report["restored"] == 1                       # only the intact row
    assert report["rows_to_restore"] == 1                # re-planned under the lock
    assert report["rows_source_unverifiable"] == 1       # shortfall is surfaced
    assert report["unverifiable_keys"] == ["sess-recov-a|"
                                           + rows["sess-recov-a"]["leaf_hash"]]
    assert not (estate.knots / rows["sess-recov-a"]["filename"]).is_file()
    assert (estate.knots / rows["sess-recov-b"]["filename"]).is_file()
    assert report["full_chain_verify"]["restored_links_verified"] == 1


def test_missing_chain_is_cannot_verify(estate: Estate, capsys) -> None:
    _classified(estate)
    estate.chain.unlink()
    assert main(["--dry", "--root", str(estate.root)]) == 2
    out = json.loads(capsys.readouterr().out)
    assert "cannot-verify" in out["error"]
