"""tests/test_knot_rehash_patrol.py — fixture-estate tests for the leaf-hash
rehash patrol (tools/knot_rehash_patrol.py, AH3 lane 2026-09-30, audit #9).

The law under test: sampled knot bodies recompute to their claimed leaf_hash
with the chain's OWN hashers (imported, never reimplemented), the dangling
census counts chain_guard's exact predicate, and a mismatch is reported as
an incident — never repaired (Q-001 operator gate).
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
from tools.knot_rehash_patrol import Estate, main  # noqa: E402


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


def _row(leaf: dict, filename: str, index: int) -> dict:
    return {
        "ts": "2026-09-30T00:00:00Z",
        "filename": filename,
        "leaf_hash": leaf["leaf_hash"],
        "session_id": leaf["session_id"],
        "amended": False,
        "index": index,
        "n_leaves": index + 1,
    }


def _write_chain(estate: Estate, rows: list[dict]) -> None:
    estate.chain.parent.mkdir(parents=True, exist_ok=True)
    with estate.chain.open("w", encoding="utf-8", newline="") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


@pytest.fixture()
def estate(tmp_path: Path) -> Estate:
    """Fixture chain: 5 present rows + 3 dangling rows + 1 no-filename row."""
    es = Estate(tmp_path)
    es.knots.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    for i, sid in enumerate(("sess-a", "sess-b", "sess-c", "sess-d", "sess-e")):
        leaf = build_leaf_from_dossier(_dossier(sid))
        fname = f"2026-09-30_0000_session_{sid}_{leaf['leaf_hash'][:8]}.knot.json"
        (es.knots / fname).write_text(json.dumps(_knot_doc(leaf, fname), indent=2),
                                      encoding="utf-8")
        rows.append(_row(leaf, fname, i))
    for i, sid in enumerate(("sess-lost-1", "sess-lost-2", "sess-lost-3")):
        leaf = build_leaf_from_dossier(_dossier(sid))
        fname = f"2026-09-30_0000_session_{sid}_{leaf['leaf_hash'][:8]}.knot.json"
        rows.append(_row(leaf, fname, 5 + i))  # filename references nothing on disk
    rows.append({"ts": "2026-09-30T00:00:00Z", "leaf_hash": "0" * 64,
                 "session_id": "sess-nofile", "index": 8})
    _write_chain(es, rows)
    return es


def test_clean_sample_all_match_exit_0(estate: Estate, capsys: pytest.CaptureFixture) -> None:
    code = main(["--root", str(estate.root), "--all"])
    out = capsys.readouterr().out
    assert code == 0
    assert "REHASHED 5/5 MATCH, DANGLING 3" in out


def test_dangling_census_exact_count(estate: Estate, capsys: pytest.CaptureFixture) -> None:
    main(["--root", str(estate.root), "--all"])
    assert "DANGLING 3" in capsys.readouterr().out
    rows = estate.load_chain_rows()
    # the no-filename row is excluded from both checks but reported
    assert len(rows) == 9


def test_sample_n_rehashes_only_n(estate: Estate, capsys: pytest.CaptureFixture) -> None:
    main(["--root", str(estate.root), "--sample", "2", "--seed", "7"])
    assert "REHASHED 2/2 MATCH, DANGLING 3" in capsys.readouterr().out


def test_sample_deterministic_with_seed(estate: Estate, capsys: pytest.CaptureFixture) -> None:
    main(["--root", str(estate.root), "--sample", "2", "--seed", "7", "--json"])
    first = json.loads(capsys.readouterr().out)
    main(["--root", str(estate.root), "--sample", "2", "--seed", "7", "--json"])
    second = json.loads(capsys.readouterr().out)
    assert first["rehashed"] == second["rehashed"] == 2


def test_edited_knot_body_is_incident_exit_1(estate: Estate,
                                             capsys: pytest.CaptureFixture) -> None:
    victim = sorted(estate.knots.glob("*sess-a_*.knot.json"))[0]
    doc = json.loads(victim.read_text(encoding="utf-8"))
    doc["tension_index"] = 0.99  # the post-commit edit the chain gate cannot see
    victim.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    code = main(["--root", str(estate.root), "--all"])
    out = capsys.readouterr().out
    assert code == 1
    assert "MISMATCH" in out
    assert "body_vs_knot" in out
    assert victim.name in out


def test_row_hash_disagreement_is_incident_exit_1(estate: Estate,
                                                  capsys: pytest.CaptureFixture) -> None:
    rows = estate.load_chain_rows()
    rows[0]["leaf_hash"] = "f" * 64  # chain row edited, knot body honest
    _write_chain(estate, rows)
    code = main(["--root", str(estate.root), "--all"])
    out = capsys.readouterr().out
    assert code == 1
    assert "knot_vs_row" in out


def test_unparseable_knot_is_incident_exit_1(estate: Estate,
                                             capsys: pytest.CaptureFixture) -> None:
    victim = sorted(estate.knots.glob("*sess-b_*.knot.json"))[0]
    victim.write_text("{not json", encoding="utf-8")
    code = main(["--root", str(estate.root), "--all"])
    assert code == 1
    assert "knot_unreadable" in capsys.readouterr().out


def test_missing_chain_exit_2(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    code = main(["--root", str(tmp_path), "--all"])
    assert code == 2
    assert "cannot-run" in capsys.readouterr().out


def test_torn_chain_line_exit_2(estate: Estate, capsys: pytest.CaptureFixture) -> None:
    with estate.chain.open("a", encoding="utf-8", newline="") as fh:
        fh.write('{"torn": tru\n')
    code = main(["--root", str(estate.root), "--all"])
    assert code == 2
    assert "cannot-run" in capsys.readouterr().out


def test_mutually_exclusive_args_exit_2(estate: Estate, capsys: pytest.CaptureFixture) -> None:
    assert main(["--root", str(estate.root), "--all", "--sample", "3"]) == 2
    assert main(["--root", str(estate.root), "--sample", "0"]) == 2


def test_json_verdict_shape(estate: Estate, capsys: pytest.CaptureFixture) -> None:
    main(["--root", str(estate.root), "--all", "--json"])
    verdict = json.loads(capsys.readouterr().out)
    assert verdict["ok"] is True
    assert verdict["rehashed"] == 5
    assert verdict["dangling"] == 3
    assert verdict["rows_without_filename"] == 1
    assert verdict["mismatches"] == []
    assert "operator-GO" in verdict["operator_gate"]


def test_live_hasher_imported_not_reimplemented() -> None:
    """The patrol must ride mag.verkle_knot's own _leaf_hash (one referee)."""
    import tools.knot_rehash_patrol as patrol

    assert patrol._session_leaf_hash is not None
    import mag.verkle_knot as vk

    assert patrol._session_leaf_hash.__module__ == vk.__name__
    body = {"a": 1, "b": [2, 3]}
    assert patrol.recompute_leaf_hash(
        {"leaf_hash": vk._leaf_hash(body), "filename": "x.knot.json", **body}, {}
    ) == vk._leaf_hash(body)


def _append_diary_row(estate: Estate) -> Path:
    """One diary_node leaf, faithful to seal_diary/append_diary_to_verkle law:
    hashed under b"diary-leaf:" with schema=mag_diary_node.v1 and kind (no
    type/leaf_kind), THEN the append path overwrites type/schema/leaf_kind and
    adds filename post-hash (mag/diary_node.py 617-647 + 474-476)."""
    from mag.diary_node import SCHEMA as DIARY_SCHEMA, _leaf_hash as diary_hash

    body: dict = {
        "schema": DIARY_SCHEMA,
        "kind": "diary_node_leaf",
        "seal_id": "diary-20260930-000000-abc123",
        "ts": "2026-09-30T00:00:00Z",
        "day": "2026-09-30",
        "channel": "voice",
        "voice_session_id": "voice-fixture",
        "title": "fixture seal",
        "summary": "s",
        "intention_goals": [],
        "turns_n": 0,
        "turns_excerpt": [],
        "last_brief": {},
        "dig_episodes": [],
        "frozen": {},
        "artifacts": [],
        "training": {},
    }
    body["leaf_hash"] = diary_hash({k: v for k, v in body.items() if k != "leaf_hash"})
    fname = f"2026-09-30_0000_diary_abc123_{body['leaf_hash'][:8]}.diary.knot.json"
    doc = dict(body)
    doc["filename"] = fname
    doc["type"] = "diary_node_leaf"
    doc["schema"] = "verkle_knot_leaf.v1"  # overwritten AFTER hashing
    doc["leaf_kind"] = "diary_node"
    (estate.knots / fname).write_text(json.dumps(doc, indent=2), encoding="utf-8")
    rows = estate.load_chain_rows()
    rows.append({
        "ts": "2026-09-30T00:00:00Z", "filename": fname,
        "leaf_hash": body["leaf_hash"], "session_id": body["seal_id"],
        "leaf_kind": "diary_node", "amended": False,
        "index": len(rows), "n_leaves": len(rows) + 1,
    })
    _write_chain(estate, rows)
    return estate.knots / fname


def test_diary_leaf_rehashes_clean_via_diary_hasher(estate: Estate,
                                                    capsys: pytest.CaptureFixture) -> None:
    _append_diary_row(estate)
    code = main(["--root", str(estate.root), "--all"])
    out = capsys.readouterr().out
    assert code == 0
    assert "REHASHED 6/6 MATCH, DANGLING 3" in out


def test_edited_diary_body_is_incident_exit_1(estate: Estate,
                                              capsys: pytest.CaptureFixture) -> None:
    diary_path = _append_diary_row(estate)
    doc = json.loads(diary_path.read_text(encoding="utf-8"))
    doc["summary"] = "edited after commit"
    diary_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    code = main(["--root", str(estate.root), "--all"])
    out = capsys.readouterr().out
    assert code == 1
    assert "body_vs_knot" in out
    assert diary_path.name in out


def test_audit_claim_carried_in_output(estate: Estate, capsys: pytest.CaptureFixture) -> None:
    """The dangling count is always read against audit #9's 372 claim."""
    code = main(["--root", str(estate.root), "--all"])
    out = capsys.readouterr().out
    assert code == 0
    assert "audit claim 372, delta -369" in out

