"""tests for mag/gwap_to_gps.py -- the fail-closed gwap -> gps bridge.

Chain law: the WHOLE session file must verify before anything is fed; a
tampered chain (or a missing file) refuses with the gps ledger untouched
(zero capability rows, zero verdict_log rows -- no partial feed of a broken
history). Verdict law: VERIFIED_AGREE scores pass, DISPUTE scores fail,
CHALLENGE and BLOCKED (and the v1 collusion downgrade, which lands on
CHALLENGE) are counted skips that never reach record_verdict. Evidence law:
the evidence hash is the row's row_sha256 (chain position), never the
build-time meter_credit.receipt_sha256. Key-mapping law: model_id comes from
scene_to_model first, else participant_to_model via the intent author (the
robber, the model under test); a miss or no map at all refuses; there is no
identity fallback. Schema law: a chain-valid row whose payload verdict is
foreign refuses rather than being binned.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from mag.gwap_payload import (
    BLOCKED,
    CHALLENGE,
    DISPUTE,
    VERIFIED_AGREE,
    SCHEMA,
    SessionLedger,
    build_payload,
    canonical,
)
from mag.gwap_to_gps import (
    DEFAULT_TASK_SHAPE,
    GwapToGpsError,
    feed_session,
)
from tools.gps_mcp.ledger import CapabilityLedger

UTC = "2026-09-29T12:00:00Z"
TAPE = {"sha256": "0" * 64, "engine_version": "test-engine-0"}
PARTS = [
    {"anon_id": "r1", "role": "robber"},
    {"anon_id": "c1", "role": "cop"},
]
ZERO = "0" * 64

C1 = {"subject": "a", "verb": "did", "object": "x"}
C2 = {"subject": "b", "verb": "did", "object": "y"}
C3 = {"subject": "c", "verb": "did", "object": "z"}


def _build(scene, intent_claims, report_claims, taboo_list=()):
    return build_payload(
        scene_id=scene,
        intent_struct={"author": "r1", "claims": list(intent_claims)},
        report_struct={"author": "c1", "claims": list(report_claims)},
        participants=PARTS,
        consent=True,
        created_utc=UTC,
        replay_tape_ref=TAPE,
        taboo_list=taboo_list,
    )


def payload_pass(scene):
    # identical triple sets, different order: score 1.0, no collusion fire
    return _build(scene, [C1, C2, C3], [C2, C3, C1])


def payload_fail(scene):
    # disjoint claims: score 0.0
    return _build(scene, [C1, C2], [dict(C3, object="elsewhere")])


def payload_challenge(scene):
    # 1 of 3 shared: 0.3333 lands inside the CHALLENGE band
    return _build(scene, [C1, C2, C3], [C1])


def payload_blocked(scene):
    # taboo token used by both sides: BLOCKED regardless of a 1.0 score
    vault = {"subject": "vault", "verb": "opened", "object": "door"}
    return _build(scene, [vault], [vault], taboo_list=["vault"])


def payload_collusion_challenge(scene):
    # copied claims in identical order between different authors: score 1.0
    # demoted to CHALLENGE by the v1 fingerprint
    return _build(scene, [C1, C2], [C1, C2])


def make_session(store, session_id, payloads):
    ledger = SessionLedger(session_id, store=store)
    for p in payloads:
        ledger.append(p, ts_utc=UTC)
    return ledger.path


@pytest.fixture()
def gps(tmp_path):
    ledger = CapabilityLedger(tmp_path / "gps.db")
    yield ledger
    ledger.close()


def refuses(exc_info, reason):
    assert exc_info.value.reason == reason


# -- clean feed ---------------------------------------------------------------------


def test_clean_feed_scores_and_audits(tmp_path, gps):
    path = make_session(tmp_path, "sess-clean", [
        payload_pass("scene-a"),
        payload_pass("scene-a"),
        payload_fail("scene-b"),
    ])
    scene_map = {"scene-a": "m-alpha", "scene-b": "m-beta"}

    report = feed_session(path, gps, scene_to_model=scene_map)

    assert report["rows_seen"] == 3
    assert report["fed"] == 3
    assert report["skipped"] == 0
    assert report["by_verdict"] == {
        VERIFIED_AGREE: 2, CHALLENGE: 0, DISPUTE: 1, BLOCKED: 0,
    }
    assert report["model_ids"] == ["m-alpha", "m-beta"]
    assert report["task_shape"] == DEFAULT_TASK_SHAPE
    assert report["chain_tip"] != ZERO

    assert gps.get_rate("m-alpha", DEFAULT_TASK_SHAPE) == (1.0, 2)
    assert gps.get_rate("m-beta", DEFAULT_TASK_SHAPE) == (0.0, 1)
    assert gps.task_shape_has_history(DEFAULT_TASK_SHAPE)
    assert len(gps.verdict_log_rows("m-alpha", DEFAULT_TASK_SHAPE)) == 2
    assert len(gps.verdict_log_rows("m-beta", DEFAULT_TASK_SHAPE)) == 1


def test_evidence_hash_is_row_sha_not_receipt(tmp_path, gps):
    path = make_session(tmp_path, "sess-evidence", [payload_pass("scene-a")])
    rows = SessionLedger("sess-evidence", store=tmp_path).rows

    feed_session(path, gps, scene_to_model={"scene-a": "m1"})

    logged = gps.verdict_log_rows("m1", DEFAULT_TASK_SHAPE)
    assert [r["evidence_hash"] for r in logged] == [rows[0]["row_sha256"]]
    assert logged[0]["evidence_hash"] != \
        rows[0]["payload"]["meter_credit"]["receipt_sha256"]


# -- fail-closed chain law ----------------------------------------------------------


def test_tampered_chain_refuses_and_writes_nothing(tmp_path):
    path = make_session(tmp_path, "sess-tamper", [
        payload_pass("scene-a"), payload_fail("scene-b"),
    ])
    lines = path.read_text(encoding="utf-8").splitlines()
    # flip one byte of the second row's payload without fixing any hash
    lines[1] = lines[1].replace("scene-b", "scene-hacked")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    db = tmp_path / "gps-tamper.db"

    with pytest.raises(GwapToGpsError) as ei:
        feed_session(path, db, scene_to_model={"scene-a": "m1", "scene-b": "m2"})
    refuses(ei, "BROKEN_CHAIN")

    check = CapabilityLedger(db)
    try:
        assert not check.task_shape_has_history(DEFAULT_TASK_SHAPE)
        assert check.get_rate("m1", DEFAULT_TASK_SHAPE) is None
    finally:
        check.close()


def test_missing_session_file_refuses(tmp_path, gps):
    with pytest.raises(GwapToGpsError) as ei:
        feed_session(tmp_path / "nope.jsonl", gps,
                     scene_to_model={"scene-a": "m1"})
    refuses(ei, "MISSING_SESSION")
    assert not gps.task_shape_has_history(DEFAULT_TASK_SHAPE)


def test_empty_session_feeds_zero_rows(tmp_path, gps):
    # SessionLedger only creates the file on first append; a zero-row session
    # is a file that exists with no lines, so create it explicitly.
    path = tmp_path / "sess-empty.jsonl"
    path.write_text("", encoding="utf-8")
    report = feed_session(path, gps, scene_to_model={"scene-a": "m1"})
    assert report["rows_seen"] == 0
    assert report["fed"] == 0
    assert report["skipped"] == 0
    assert report["chain_tip"] == ZERO
    assert not gps.task_shape_has_history(DEFAULT_TASK_SHAPE)


def test_unknown_verdict_refuses_even_on_a_valid_chain(tmp_path, gps):
    good = payload_pass("scene-a")
    forged = payload_fail("scene-b")
    forged["verdict"] = "SUPER_AGREE"

    def row(seq, payload, prev):
        core = {"seq": seq, "ts_utc": UTC, "payload": payload, "prev_sha256": prev}
        core["row_sha256"] = hashlib.sha256(
            canonical(core).encode("utf-8")).hexdigest()
        return core

    path = tmp_path / "sess-forged.jsonl"
    r1 = row(1, good, ZERO)
    r2 = row(2, forged, r1["row_sha256"])
    path.write_text(canonical(r1) + "\n" + canonical(r2) + "\n",
                    encoding="utf-8")

    with pytest.raises(GwapToGpsError) as ei:
        feed_session(path, gps,
                     scene_to_model={"scene-a": "m1", "scene-b": "m2"})
    refuses(ei, "UNKNOWN_VERDICT")
    assert gps.get_rate("m1", DEFAULT_TASK_SHAPE) is None
    assert not gps.verdict_log_rows("m1", DEFAULT_TASK_SHAPE)


# -- the four verdict branches + skip counting --------------------------------------


def test_all_four_verdict_branches(tmp_path, gps):
    path = make_session(tmp_path, "sess-four", [
        payload_pass("s1"),
        payload_challenge("s2"),
        payload_fail("s3"),
        payload_blocked("s4"),
    ])
    scene_map = {f"s{i}": "m1" for i in range(1, 5)}

    report = feed_session(path, gps, scene_to_model=scene_map)

    assert report["by_verdict"] == {
        VERIFIED_AGREE: 1, CHALLENGE: 1, DISPUTE: 1, BLOCKED: 1,
    }
    assert report["fed"] == 2
    assert report["skipped"] == 2
    # only the pass and the fail moved the needle: 1/2
    assert gps.get_rate("m1", DEFAULT_TASK_SHAPE) == (0.5, 2)
    assert len(gps.verdict_log_rows("m1", DEFAULT_TASK_SHAPE)) == 2


def test_skip_only_session_never_touches_the_capability_table(tmp_path, gps):
    path = make_session(tmp_path, "sess-skips", [
        payload_challenge("s1"),
        payload_blocked("s2"),
    ])

    report = feed_session(path, gps, scene_to_model={"s1": "m1", "s2": "m1"})

    assert report["fed"] == 0
    assert report["skipped"] == 2
    assert gps.get_rate("m1", DEFAULT_TASK_SHAPE) is None
    assert gps.verdict_log_rows("m1", DEFAULT_TASK_SHAPE) == []


def test_collusion_downgrade_lands_as_skip(tmp_path, gps):
    path = make_session(tmp_path, "sess-collusion",
                        [payload_collusion_challenge("s1")])
    row = SessionLedger("sess-collusion", store=tmp_path).rows[0]
    assert row["payload"]["verdict"] == CHALLENGE  # 1.0 score, demoted

    report = feed_session(path, gps, scene_to_model={"s1": "m1"})

    assert report["skipped"] == 1
    assert report["fed"] == 0
    assert gps.get_rate("m1", DEFAULT_TASK_SHAPE) is None


# -- key-mapping law ----------------------------------------------------------------


def test_participant_map_resolves_via_the_intent_author(tmp_path, gps):
    path = make_session(tmp_path, "sess-parts", [payload_pass("s1")])

    report = feed_session(path, gps, participant_to_model={
        "r1": "robber-model",
        "c1": "cop-model",  # instruments never route the verdict
    })

    assert report["model_ids"] == ["robber-model"]
    assert gps.get_rate("robber-model", DEFAULT_TASK_SHAPE) == (1.0, 1)
    assert gps.get_rate("cop-model", DEFAULT_TASK_SHAPE) is None


def test_scene_map_takes_precedence_over_participant_map(tmp_path, gps):
    path = make_session(tmp_path, "sess-prec", [payload_pass("s1")])

    report = feed_session(
        path, gps,
        scene_to_model={"s1": "scene-model"},
        participant_to_model={"r1": "robber-model"},
    )

    assert report["model_ids"] == ["scene-model"]
    assert gps.get_rate("scene-model", DEFAULT_TASK_SHAPE) == (1.0, 1)
    assert gps.get_rate("robber-model", DEFAULT_TASK_SHAPE) is None


def test_unmapped_scene_refuses_before_any_write(tmp_path, gps):
    path = make_session(tmp_path, "sess-unmapped", [
        payload_pass("s1"), payload_pass("s2"),
    ])

    with pytest.raises(GwapToGpsError) as ei:
        feed_session(path, gps, scene_to_model={"s1": "m1"})
    refuses(ei, "UNMAPPED_SCENE")
    assert gps.get_rate("m1", DEFAULT_TASK_SHAPE) is None
    assert gps.verdict_log_rows("m1", DEFAULT_TASK_SHAPE) == []


def test_unmapped_participant_refuses(tmp_path, gps):
    path = make_session(tmp_path, "sess-unmapped-p", [payload_pass("s1")])

    with pytest.raises(GwapToGpsError) as ei:
        feed_session(path, gps, participant_to_model={"c1": "cop-model"})
    refuses(ei, "UNMAPPED_PARTICIPANT")
    assert gps.get_rate("cop-model", DEFAULT_TASK_SHAPE) is None


def test_no_key_map_at_all_refuses(tmp_path, gps):
    path = make_session(tmp_path, "sess-nomap", [payload_pass("s1")])

    with pytest.raises(GwapToGpsError) as ei:
        feed_session(path, gps)
    refuses(ei, "NO_KEY_MAP")
    assert not gps.task_shape_has_history(DEFAULT_TASK_SHAPE)


def test_custom_task_shape_lands_under_its_own_key(tmp_path, gps):
    path = make_session(tmp_path, "sess-shape", [payload_pass("s1")])

    feed_session(path, gps, scene_to_model={"s1": "m1"},
                 task_shape="noir-agreement-hard")

    assert gps.get_rate("m1", "noir-agreement-hard") == (1.0, 1)
    assert gps.get_rate("m1", DEFAULT_TASK_SHAPE) is None
