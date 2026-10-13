"""tests for the gps verdict_log dedupe gate (a04, GO item 2).

Cause: the gwap double-bank minted fresh ts rows and the whole-file feed
re-fed them, so capability means rode 259 observations over 178 distinct
measurements (memory/runs/mickey17_v2/runs/run-0/lanes/a04-arena-gwap-gps.json
rows 2-3; corpus/steal/MASTER_MICKEY17_V2.md section 9 GO item 2). The gate:
record_verdict INSERT-that-skips on a repeated
(model_id, task_shape, evidence_hash) triple, backed by the partial UNIQUE
index ux_verdict_log_evidence_triple (partial so hash-less verdicts stay
legal). Evidence bytes participate in the key through the resolution gate:
bytes given without a claim adopt their recomputed sha256 as the key.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3

import pytest

from mag.gwap_payload import (
    BLOCKED,
    CHALLENGE,
    DISPUTE,
    VERIFIED_AGREE,
    SessionLedger,
    build_payload,
    canonical,
)
from mag.gwap_to_gps import DEFAULT_TASK_SHAPE, feed_session
from tools.gps_mcp.ledger import (
    EVIDENCE_DUPLICATE_SKIPPED,
    EVIDENCE_RESOLVED,
    UNIQUE_TRIPLE_INDEX,
    CapabilityLedger,
)

UTC = "2026-10-04T12:00:00Z"
TAPE = {"sha256": "0" * 64, "engine_version": "gps-dedupe-test-0"}
PARTS = [
    {"anon_id": "r1", "role": "robber"},
    {"anon_id": "c1", "role": "cop"},
]
ZERO = "0" * 64
C1 = {"subject": "a", "verb": "did", "object": "x"}
C2 = {"subject": "b", "verb": "did", "object": "y"}
C3 = {"subject": "c", "verb": "did", "object": "z"}


@pytest.fixture()
def ledger(tmp_path):
    led = CapabilityLedger(tmp_path / "dedupe.db3")
    yield led
    led.close()


def _raw_count(ledger, model="m", shape="shape"):
    return ledger.connection().execute(
        "SELECT COUNT(*) FROM verdict_log WHERE model_id = ? AND task_shape = ?",
        (model, shape),
    ).fetchone()[0]


# -- record_verdict dedupe gate -------------------------------------------------------


def test_duplicate_triple_skipped_no_new_row(ledger):
    first = ledger.record_verdict("m", "shape", True, "hash-a")
    assert first.evidence_status != EVIDENCE_DUPLICATE_SKIPPED
    assert first.sample_size == 1

    # same triple, even with the OPPOSITE outcome: one measurement, not many
    dup = ledger.record_verdict("m", "shape", False, "hash-a")
    assert dup.evidence_status == EVIDENCE_DUPLICATE_SKIPPED
    assert (dup.pass_rate, dup.sample_size) == (1.0, 1)
    assert _raw_count(ledger) == 1
    assert ledger.get_rate("m", "shape") == (1.0, 1)


def test_distinct_evidence_lands(ledger):
    ledger.record_verdict("m", "shape", True, "hash-a")
    second = ledger.record_verdict("m", "shape", False, "hash-b")
    assert second.evidence_status != EVIDENCE_DUPLICATE_SKIPPED
    assert second.sample_size == 2
    assert second.pass_rate == pytest.approx(0.5)
    assert _raw_count(ledger) == 2


def test_same_triple_different_pair_is_not_a_duplicate(ledger):
    ledger.record_verdict("m", "shape", True, "hash-a")
    other = ledger.record_verdict("m", "other-shape", False, "hash-a")
    assert other.evidence_status != EVIDENCE_DUPLICATE_SKIPPED
    assert _raw_count(ledger) == 1
    assert _raw_count(ledger, model="m", shape="other-shape") == 1


def test_hashless_verdicts_stay_legal(ledger):
    # the index is partial: evidence_hash = '' rows are distinct observations
    # by definition and the gate never collapses them
    ledger.record_verdict("m", "shape", True)
    ledger.record_verdict("m", "shape", False)
    assert _raw_count(ledger) == 2
    assert ledger.get_rate("m", "shape") == (0.5, 2)


def test_evidence_bytes_participate_in_the_key(ledger):
    # bytes given without a claim adopt their recomputed sha256 as the key:
    # the same bytes twice is one duplicate, different bytes are distinct
    r1 = ledger.record_verdict("m", "shape", True, evidence_bytes=b"payload-1")
    r2 = ledger.record_verdict("m", "shape", False, evidence_bytes=b"payload-1")
    r3 = ledger.record_verdict("m", "shape", True, evidence_bytes=b"payload-2")
    assert r1.evidence_status == EVIDENCE_RESOLVED
    assert r1.evidence_hash == hashlib.sha256(b"payload-1").hexdigest()
    assert r2.evidence_status == EVIDENCE_DUPLICATE_SKIPPED
    assert r3.evidence_status == EVIDENCE_RESOLVED
    assert r3.evidence_hash == hashlib.sha256(b"payload-2").hexdigest()
    assert _raw_count(ledger) == 2
    assert ledger.get_rate("m", "shape") == (1.0, 2)


def test_evidence_bytes_are_retained_and_reauditable(ledger):
    ledger.record_verdict("m", "shape", True, evidence_bytes=b"payload-1")
    audit = ledger.audit_evidence()
    assert audit["rows"] == 1
    assert audit["agreed"] == 1
    assert audit["resolved_at_append"] == 1


# -- the UNIQUE index backstop --------------------------------------------------------


def test_unique_index_rejects_a_raw_duplicate(ledger):
    ledger.record_verdict("m", "shape", True, "hash-a")
    with pytest.raises(sqlite3.IntegrityError) as ei:
        ledger.connection().execute(
            "INSERT INTO verdict_log (ts, model_id, task_shape, verdict,"
            " evidence_hash) VALUES (?, ?, ?, ?, ?)",
            ("2026-10-04T00:00:00+00:00", "m", "shape", 0, "hash-a"),
        )
    # sqlite names index-backed violations by column list, not index name
    assert "verdict_log.model_id" in str(ei.value)
    assert "evidence_hash" in str(ei.value)


class _RacedConn:
    """Simulates the lost race: one named SELECT cannot see the rival row a
    concurrent feeder committed between the SELECT and the INSERT, so the
    constraint (not the SELECT) is what fires."""

    def __init__(self, conn, blind_sql):
        self._conn = conn
        self._blind_sql = blind_sql
        self._blind = True

    def execute(self, sql, *args):
        if self._blind and self._blind_sql in sql:
            self._blind = False
            return _NoRow()
        return self._conn.execute(sql, *args)

    def __enter__(self):
        return self._conn.__enter__()

    def __exit__(self, *exc):
        return self._conn.__exit__(*exc)

    def __getattr__(self, name):
        return getattr(self._conn, name)


class _NoRow:
    def fetchone(self):
        return None


def test_race_backstop_returns_duplicate_skipped(ledger, tmp_path):
    ledger.record_verdict("m", "shape", True, "hash-a")
    # a second ledger instance on the same file, its dup SELECT blinded so
    # only the UNIQUE index can catch the repeat
    rival = CapabilityLedger(tmp_path / "dedupe.db3")
    try:
        rival.connection = lambda: _RacedConn(
            rival._conn, "SELECT 1 FROM verdict_log"
        )
        result = rival.record_verdict("m", "shape", False, "hash-a")
        assert result.evidence_status == EVIDENCE_DUPLICATE_SKIPPED
        assert "unique-index race lost" in result.evidence_source
        assert _raw_count(ledger) == 1
        assert ledger.get_rate("m", "shape") == (1.0, 1)
    finally:
        rival.close()


def test_non_triple_integrity_failure_still_raises(ledger, tmp_path):
    # the discriminator names the index: a lost race on the CAPABILITY
    # primary key is not a duplicate verdict and must not be swallowed as one
    ledger.connection().execute(
        "INSERT INTO capability (model_id, task_shape, pass_rate, sample_size,"
        " cost_usd_per_call, last_measured, updated_at)"
        " VALUES ('m', 'shape', 0.5, 1, NULL, ?, ?)",
        (UTC, UTC),
    )
    ledger.connection().commit()
    rival = CapabilityLedger(tmp_path / "dedupe.db3")
    try:
        # blind the capability SELECT so record_verdict takes the INSERT
        # branch against an existing primary key
        rival.connection = lambda: _RacedConn(
            rival._conn, "SELECT pass_rate, sample_size FROM capability"
        )
        with pytest.raises(sqlite3.IntegrityError) as ei:
            rival.record_verdict("m", "shape", True, "fresh-hash")
        assert UNIQUE_TRIPLE_INDEX not in str(ei.value)
        assert "capability" in str(ei.value)
    finally:
        rival.close()


def test_legacy_db_with_duplicates_fails_closed_at_open(tmp_path):
    # migration contract: a legacy db that still carries duplicate triples
    # refuses the index creation at open (fail-closed); the fix path is the
    # .bak pattern then dedupe, exactly what gps_ledger.db3 went through on
    # 2026-10-03 (commit c3ff9d1bd removed 81 rows) and the 2026-10-04
    # gpsdedupe bak for the index itself
    db = tmp_path / "legacy.db3"
    conn = sqlite3.connect(db)
    conn.execute(
        "CREATE TABLE verdict_log (ts TEXT NOT NULL, model_id TEXT NOT NULL,"
        " task_shape TEXT NOT NULL, verdict INTEGER NOT NULL,"
        " evidence_hash TEXT NOT NULL DEFAULT '')"
    )
    for _ in range(2):
        conn.execute(
            "INSERT INTO verdict_log (ts, model_id, task_shape, verdict,"
            " evidence_hash) VALUES (?, ?, ?, ?, ?)",
            (UTC, "m", "shape", 1, "hash-a"),
        )
    conn.commit()
    conn.close()
    with pytest.raises(sqlite3.IntegrityError) as ei:
        CapabilityLedger(db)
    # the index creation is what fires, named by its columns
    assert "verdict_log.model_id" in str(ei.value)
    assert "evidence_hash" in str(ei.value)


# -- the bridge feed: dedupe + byte-derived evidence + receipt ------------------------


def _payload_pass(scene):
    return build_payload(
        scene_id=scene,
        intent_struct={"author": "r1", "claims": [C1, C2]},
        report_struct={"author": "c1", "claims": [C2, C1]},
        participants=PARTS,
        consent=True,
        created_utc=UTC,
        replay_tape_ref=TAPE,
    )


def _payload_fail(scene):
    return build_payload(
        scene_id=scene,
        intent_struct={"author": "r1", "claims": [C1]},
        report_struct={"author": "c1", "claims": [C3]},
        participants=PARTS,
        consent=True,
        created_utc=UTC,
        replay_tape_ref=TAPE,
    )


def _make_session(store, session_id, payloads):
    session = SessionLedger(session_id, store=store)
    for p in payloads:
        session.append(p, ts_utc=UTC)
    return session.path


def test_bridge_refeed_is_idempotent_and_byte_resolved(tmp_path):
    path = _make_session(tmp_path, "sess-dedupe", [
        _payload_pass("scene-a"),
        _payload_fail("scene-b"),
    ])
    db = tmp_path / "gps-bridge.db3"
    scene_map = {"scene-a": "m-alpha", "scene-b": "m-beta"}

    first = feed_session(path, db, scene_to_model=scene_map)
    assert first["rows_seen"] == 2
    assert first["fed"] == 2
    assert first["skipped"] == 0
    assert first["distinct"] == 2
    assert first["duplicate_skipped"] == 0
    assert first["by_verdict"] == {VERIFIED_AGREE: 1, CHALLENGE: 0, DISPUTE: 1, BLOCKED: 0}

    gps = CapabilityLedger(db)
    try:
        # a04#6: the feed passes the canonical row core as evidence_bytes, so
        # the gate recomputes row_sha256 from bytes and the row lands
        # evidence_resolved=1 instead of self-attested
        audit = gps.audit_evidence()
        assert audit["rows"] == 2
        assert audit["agreed"] == 2
        assert audit["resolved_at_append"] == 2
        rows = gps.connection().execute(
            "SELECT evidence_resolved, evidence_bytes FROM verdict_log"
            " WHERE task_shape = ? ORDER BY rowid",
            (DEFAULT_TASK_SHAPE,),
        ).fetchall()
        assert all(r[0] == 1 for r in rows)
        ledger_rows = [
            line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
        ]
        for stored, line in zip(rows, ledger_rows):
            row = json.loads(line)
            core = {
                key: row[key]
                for key in ("seq", "ts_utc", "payload", "prev_sha256")
            }
            # the retained bytes are the exact hash preimage of row_sha256
            assert bytes(stored[1]) == canonical(core).encode("utf-8")

        # second feed of the SAME session: every triple is a duplicate, the
        # verdict_log does not move (the idempotence law, GO item 2)
        second = feed_session(path, gps, scene_to_model=scene_map)
        assert second["fed"] == 0
        assert second["duplicate_skipped"] == 2
        assert second["distinct"] == 2
        assert _raw_count(gps, model="m-alpha", shape=DEFAULT_TASK_SHAPE) == 1
        assert _raw_count(gps, model="m-beta", shape=DEFAULT_TASK_SHAPE) == 1
        assert gps.get_rate("m-alpha", DEFAULT_TASK_SHAPE) == (1.0, 1)
        assert gps.get_rate("m-beta", DEFAULT_TASK_SHAPE) == (0.0, 1)
        total = gps.connection().execute(
            "SELECT COUNT(*) FROM verdict_log"
        ).fetchone()[0]
        assert total == 2
    finally:
        gps.close()


def test_feed_receipt_line_prints_every_invocation(tmp_path, capsys):
    path = _make_session(tmp_path, "sess-receipt", [
        _payload_pass("scene-a"),
        _payload_fail("scene-b"),
    ])
    report = feed_session(path, tmp_path / "gps-receipt.db3",
                          scene_to_model={"scene-a": "m1", "scene-b": "m1"})
    out = capsys.readouterr().out
    line = [l for l in out.splitlines() if l.startswith("GPS FEED RECEIPT:")]
    assert len(line) == 1
    for field in ("rows_seen=2", "fed=2", "skipped=0", "distinct=2",
                  "duplicate_skipped=0", f"task_shape={DEFAULT_TASK_SHAPE}"):
        assert field in line[0]
    assert report["chain_tip"] in line[0]


def test_receipt_on_skip_only_session_carries_zeros(tmp_path, capsys):
    # a CHALLENGE-only session: nothing failable, distinct reads 0, nothing
    # printed is a lie
    payload = build_payload(
        scene_id="scene-challenge",
        intent_struct={"author": "r1", "claims": [C1, C2, C3]},
        report_struct={"author": "c1", "claims": [C1]},
        participants=PARTS,
        consent=True,
        created_utc=UTC,
        replay_tape_ref=TAPE,
    )
    path = _make_session(tmp_path, "sess-challenge", [payload])
    report = feed_session(path, tmp_path / "gps-skip.db3",
                          scene_to_model={"scene-challenge": "m1"})
    assert report["fed"] == 0
    assert report["skipped"] == 1
    assert report["distinct"] == 0
    out = capsys.readouterr().out
    assert "fed=0" in out and "distinct=0" in out
    gps = CapabilityLedger(tmp_path / "gps-skip.db3")
    try:
        assert gps.get_rate("m1", DEFAULT_TASK_SHAPE) is None
    finally:
        gps.close()
