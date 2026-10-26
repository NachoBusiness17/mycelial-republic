"""tests/test_verkle_dangling.py — fixture-estate tests for the marker-backfill
repair (tools/verkle_dangling_repair.py, W3N lane 2026-09-30).

The law under test: dangling rows get classified into an append-only side
ledger (evidence_lost markers ONLY where the data says lost), and the chain,
tip and repair-state marker stay byte-exact throughout — the repair is a
classification, never a rewrite (Q-001 operator gate).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag.verkle_knot import build_leaf_from_dossier  # noqa: E402
from tools.verkle_dangling_repair import (  # noqa: E402
    Estate, _postcondition_problems, classify, main, merge_check, verify_candidate,
)


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


def _row(leaf: dict, filename: str, index: int, evidence_lost: bool = False) -> dict:
    row = {
        "ts": "2026-09-30T00:00:00Z",
        "filename": filename,
        "leaf_hash": leaf["leaf_hash"],
        "session_id": leaf["session_id"],
        "amended": False,
        "evidence_lost": evidence_lost,
        "index": index,
        "n_leaves": index + 1,
    }
    return row


@pytest.fixture()
def estate(tmp_path: Path) -> Estate:
    """Fixture chain exercising every classification:
      row 0 healthy          knot lives in knots/
      row 1 flagged          dangling + evidence_lost already on the row
      row 2 recoverable      dangling, unflagged, hash-verified copy in a backup
      row 3 name-decoy       dangling, unflagged, same-name copy whose content
                             hash does NOT match -> truly lost (hash-gate)
      row 4 vanished         dangling, unflagged, no copy anywhere -> truly lost
    """
    es = Estate(tmp_path)
    es.knots.mkdir(parents=True, exist_ok=True)
    backup = es.root / "memory" / "biography_backup_fixture" / "knots"
    backup.mkdir(parents=True, exist_ok=True)

    leaves = {sid: build_leaf_from_dossier(_dossier(sid))
              for sid in ("sess-healthy", "sess-flagged", "sess-recoverable",
                          "sess-decoy", "sess-vanished")}
    fn = {sid: f"2026-09-30_0000_session_{sid}_{leaves[sid]['leaf_hash'][:8]}.knot.json"
          for sid in leaves}

    (es.knots / fn["sess-healthy"]).write_text(
        json.dumps(_knot_doc(leaves["sess-healthy"], fn["sess-healthy"])), encoding="utf-8")
    # the recoverable row's knot exists ONLY in the backup, content-exact
    (backup / fn["sess-recoverable"]).write_text(
        json.dumps(_knot_doc(leaves["sess-recoverable"], fn["sess-recoverable"])),
        encoding="utf-8")
    # the decoy: same FILENAME as the dangling row, different session content
    (backup / fn["sess-decoy"]).write_text(
        json.dumps(_knot_doc(leaves["sess-healthy"], fn["sess-decoy"])), encoding="utf-8")

    rows = [
        _row(leaves["sess-healthy"], fn["sess-healthy"], 0),
        _row(leaves["sess-flagged"], fn["sess-flagged"], 1, evidence_lost=True),
        _row(leaves["sess-recoverable"], fn["sess-recoverable"], 2),
        _row(leaves["sess-decoy"], fn["sess-decoy"], 3),
        _row(leaves["sess-vanished"], fn["sess-vanished"], 4),
    ]
    es.chain.parent.mkdir(parents=True, exist_ok=True)
    es.chain.write_text(
        "".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8", newline="")
    return es


def _sha(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def test_classify_counts_and_markers(estate: Estate) -> None:
    before_chain = _sha(estate.chain)
    before_knots = sorted(p.name for p in estate.knots.iterdir())
    result = classify(estate, estate.default_ledger)
    assert result["ok"] is True and result["chain_mutation_required"] is False
    assert result["dangling_total"] == 4
    assert result["recoverable_by_hash"] == 1
    assert result["truly_lost"] == 2          # decoy + vanished
    assert result["already_flagged_in_chain"] == 1
    assert result["classified_rows_intact"] is True
    assert result["live_chain_motion"] is None
    assert _sha(estate.chain) == before_chain
    assert sorted(p.name for p in estate.knots.iterdir()) == before_knots  # untouched


def test_ledger_shape_and_hash_gate(estate: Estate) -> None:
    classify(estate, estate.default_ledger)
    lines = [json.loads(l) for l in
             estate.default_ledger.read_text(encoding="utf-8").splitlines() if l.strip()]
    entries = [e for e in lines if e["kind"] == "dangling_classification"]
    assert len(entries) == 4
    by_class = {e["classification"]: e for e in entries}

    rec = by_class["recoverable_by_hash"]
    assert rec["evidence_lost"] is False and rec["recovered_from"]
    lost = [e for e in entries if e["classification"] == "truly_lost"]
    assert len(lost) == 2
    for e in lost:
        assert e["evidence_lost"] is True      # markers land where data says lost
    flagged = by_class["already_flagged_in_chain"]
    assert flagged["evidence_lost"] is None    # chain already carries the flag

    # hash-gate: the decoy same-name copy must NOT have verified
    decoy = [e for e in entries if e["session_id"] == "sess-decoy"][0]
    assert decoy["classification"] == "truly_lost" and not decoy.get("recovered_from")
    # LF-only byte law inside the ledger (B2-393)
    assert b"\r" not in estate.default_ledger.read_bytes()
    # summary line records the no-mutation contract
    summary = [e for e in lines if e["kind"] == "run_summary"][0]
    assert summary["chain_mutation_required"] is False


def test_idempotent_rerun_appends_only_summary(estate: Estate) -> None:
    classify(estate, estate.default_ledger)
    first = [json.loads(l) for l in
             estate.default_ledger.read_text(encoding="utf-8").splitlines() if l.strip()]
    result = classify(estate, estate.default_ledger)
    assert result["skipped_in_ledger"] == 4
    second = [json.loads(l) for l in
              estate.default_ledger.read_text(encoding="utf-8").splitlines() if l.strip()]
    # classifications deduped by (session_id, leaf_hash): zero new lines
    first_cls = [e for e in first if e["kind"] == "dangling_classification"]
    second_cls = [e for e in second if e["kind"] == "dangling_classification"]
    assert len(first_cls) == len(second_cls) == 4
    # the rerun appends exactly one run_summary — the journal shape
    assert len(second) - len(first) == 1 and second[-1]["kind"] == "run_summary"


def test_merge_check_clears_regression_without_chain_writes(estate: Estate) -> None:
    raw = merge_check(estate, estate.default_ledger)
    assert raw["dangling_unflagged_raw"] == 3
    assert raw["ok"] is False and raw["state"] == "regression"  # guard's raw alarm

    classify(estate, estate.default_ledger)
    after = merge_check(estate, estate.default_ledger)
    assert after["dangling_unclassified_effective"] == 0
    assert after["ok"] is True and after["state"] == "healthy_with_side_ledger"
    # strict marker view stays honest: recoverable rows are flagged nowhere
    assert after["dangling_unflagged_markers_only"] == 1
    # and the chain file was never rewritten to get here
    assert after["dangling_unflagged_raw"] == 3


def test_verify_candidate_requires_full_hash_match() -> None:
    leaf = build_leaf_from_dossier(_dossier("sess-x"))
    doc = _knot_doc(leaf, "any.knot.json")
    assert verify_candidate(doc, leaf["leaf_hash"]) is True
    tampered = json.loads(json.dumps(doc))
    tampered["tension_index"] = 0.99
    assert verify_candidate(tampered, leaf["leaf_hash"]) is False
    doc.pop("tension_index")  # canonical field missing -> refuse
    assert verify_candidate(doc, leaf["leaf_hash"]) is False


def test_cli_exit_ladder(estate: Estate, capsys) -> None:
    # classify: ok -> 0
    assert main(["classify", "--root", str(estate.root)]) == 0
    capsys.readouterr()
    # check: healthy with side ledger -> 0
    assert main(["check", "--root", str(estate.root)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["dangling_unclassified_effective"] == 0
    # cannot-verify: missing chain -> 2
    estate.chain.unlink()
    assert main(["check", "--root", str(estate.root)]) == 2


def test_row_without_filename_is_not_dangling(estate: Estate, tmp_path: Path) -> None:
    rows = [json.loads(l) for l in estate.chain.read_text(encoding="utf-8").splitlines()]
    rows.append({"session_id": "no-file-row", "leaf_hash": "ab" * 32})  # no filename
    estate.chain.write_text("".join(json.dumps(r) + "\n" for r in rows),
                            encoding="utf-8", newline="")
    assert len(estate.dangling_rows()) == 4  # unchanged — chain_guard's predicate


def test_postcondition_allows_live_append_refuses_strip(estate: Estate) -> None:
    """The first real run refused on live tail appends (B2-387 motion law):
    a concurrent fold moving chain+tip is legitimate; alteration of a
    classified row is refusal. The detector must tell them apart."""
    rows = [json.loads(l) for l in estate.chain.read_text(encoding="utf-8").splitlines()]
    dangling = estate.dangling_rows(rows)

    # live tail append: classified rows all survive byte-identical -> clean
    appended = rows + [_row(build_leaf_from_dossier(_dossier("sess-live-late")),
                            "2026-09-30_0001_session_live_00000001.knot.json", 5)]
    assert _postcondition_problems(dangling, appended) == []

    # flag stripped off a classified row -> refusal
    stripped = [dict(r) for r in rows]
    for r in stripped:
        if r.get("evidence_lost"):
            r["evidence_lost"] = False
            break
    assert _postcondition_problems(dangling, stripped)

    # classified row vanished (pre-repair restore shape) -> refusal
    assert _postcondition_problems(dangling, rows[:-1])
