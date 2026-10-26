"""Evidence-resolution gate for gps verdict_log (Q28, 2026-10-01).

Law under test (citation-resolution-gate-at-landing,
watch/inbox/ractor50/accuracy.md incident 1, applied to evidence hashes):
an evidence_hash must be recomputed from the cited evidence bytes at
append -- or verified at read -- never stored on trust.

    (a) append with real evidence (inline bytes or a file path) ->
        evidence_resolved True and the stored hash equals the sha256
        recomputed from the bytes
    (b) append with hash-only -> evidence_resolved False, the row is
        UNVERIFIED-class, and the audit counts it unresolved
    (c) tampered evidence file -> audit_evidence re-reads the cited file,
        recomputes, and reports the mismatch WITH the row id

Plus the surrounding contract: prefixed hash grammars ("duel:<hex>")
survive agreement, a claim contradicting its bytes lands mismatch (never
trusted), pre-gate ledgers migrate additively and audit their legacy
rows as unresolved (the honest reading of self-attestation), the duel
importer feeds bytes through the gate, and the CLI exits 1 only on
mismatch.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3

import pytest

from tools.gps_mcp.ledger import (
    CapabilityLedger,
    EVIDENCE_MISMATCH,
    EVIDENCE_RESOLVED,
    EVIDENCE_UNVERIFIED,
    main as ledger_main,
    sha256_hex,
)

# The frozen rubric -> shape key the duel importer accepts (router.py).
ADVERSARIAL_RUBRIC = [
    "section coverage", "defect severity",
    "evidence citations", "actionability",
]


@pytest.fixture()
def ledger(tmp_path):
    led = CapabilityLedger(tmp_path / "gps.db")
    yield led
    led.close()


def full_row(led, rowid):
    row = led.connection().execute(
        "SELECT rowid AS id, evidence_hash, evidence_resolved,"
        " evidence_source, evidence_bytes FROM verdict_log WHERE rowid = ?",
        (rowid,),
    ).fetchone()
    return row


# -- case (a): real evidence resolves at append -------------------------------------


def test_inline_evidence_resolves_and_stores_recomputed_hash(ledger):
    payload = b"the graded artifact, as bytes"
    result = ledger.record_verdict(
        "m1", "shape", True, evidence_bytes=payload,
        evidence_source="unit-test:inline",
    )

    assert result.evidence_resolved is True
    assert result.evidence_status == EVIDENCE_RESOLVED
    # no claim was made, so the stored hash IS the recomputation
    assert result.evidence_hash == sha256_hex(payload)
    row = full_row(ledger, 1)
    assert row["evidence_resolved"] == 1
    assert row["evidence_hash"] == hashlib.sha256(payload).hexdigest()
    assert bytes(row["evidence_bytes"]) == payload

    audit = ledger.audit_evidence()
    assert (audit["rows"], audit["agreed"], audit["mismatch"], audit["unresolved"]) == (1, 1, 0, 0)
    assert audit["resolved_at_append"] == 1


def test_file_evidence_resolves_via_path_and_cites_the_file(ledger, tmp_path):
    art = tmp_path / "artifact.txt"
    art.write_bytes(b"file-backed evidence")
    result = ledger.record_verdict(
        "m1", "shape", "pass", evidence_path=art,
    )

    assert result.evidence_resolved is True
    assert result.evidence_hash == sha256_hex(b"file-backed evidence")
    assert result.evidence_source == f"file:{art}"
    # audit re-reads the cited file and agrees
    audit = ledger.audit_evidence()
    assert (audit["agreed"], audit["mismatch"], audit["unresolved"]) == (1, 0, 0)


def test_agreeing_prefixed_claim_keeps_its_duel_form(ledger):
    """duel:<hex> and other prefixed grammars are claims, not corruption."""
    payload = b'{"winner": "A"}'
    claim = f"duel:{sha256_hex(payload)}"
    result = ledger.record_verdict(
        "m1", "shape", True, evidence_hash=claim, evidence_bytes=payload,
        evidence_source="duel-bank:test",
    )

    assert result.evidence_resolved is True
    assert result.evidence_hash == claim  # stored form preserved
    assert ledger.audit_evidence()["agreed"] == 1


def test_claim_contradicting_its_bytes_lands_mismatch_never_trusted(ledger):
    payload = b"what actually happened"
    result = ledger.record_verdict(
        "m1", "shape", True, evidence_hash="0" * 64, evidence_bytes=payload,
    )

    assert result.evidence_resolved is False
    assert result.evidence_status == EVIDENCE_MISMATCH
    row = full_row(ledger, 1)
    assert row["evidence_resolved"] == 0          # UNVERIFIED-class
    assert row["evidence_hash"] == "0" * 64       # the claim stays auditable
    assert bytes(row["evidence_bytes"]) == payload  # the disagreement too

    audit = ledger.audit_evidence()
    assert audit["mismatch"] == 1
    assert audit["mismatch_rows"][0]["recomputed_hash"] == sha256_hex(payload)


# -- case (b): hash-only rows are self-attestation, flagged never trusted -----------


def test_hash_only_append_lands_unverified_and_counts_unresolved(ledger):
    result = ledger.record_verdict("m1", "shape", True, "hash-x")

    assert result.evidence_resolved is False
    assert result.evidence_status == EVIDENCE_UNVERIFIED
    row = full_row(ledger, 1)
    assert row["evidence_resolved"] == 0
    assert row["evidence_source"] == ""
    assert row["evidence_bytes"] is None

    audit = ledger.audit_evidence()
    assert (audit["agreed"], audit["mismatch"], audit["unresolved"]) == (0, 0, 1)
    assert audit["unresolved_rows"][0]["evidence_hash"] == "hash-x"
    assert audit["resolved_at_append"] == 0


def test_missing_evidence_file_lands_unverified_with_the_citation_named(
        ledger, tmp_path):
    gone = tmp_path / "never-written.bin"
    result = ledger.record_verdict("m1", "shape", True, "h", evidence_path=gone)

    assert result.evidence_resolved is False
    assert result.evidence_status == EVIDENCE_UNVERIFIED
    assert result.evidence_source == f"file:{gone}"  # names what it cited
    audit = ledger.audit_evidence()
    assert audit["unresolved"] == 1
    assert audit["unresolved_rows"][0]["evidence_source"] == f"file:{gone}"


def test_file_source_without_path_still_resolves(ledger, tmp_path):
    """A caller may cite bytes with evidence_source='file:...' alone."""
    art = tmp_path / "cited.bin"
    art.write_bytes(b"source-cited bytes")
    result = ledger.record_verdict(
        "m1", "shape", True, evidence_source=f"file:{art}",
    )

    assert result.evidence_resolved is True
    assert result.evidence_hash == sha256_hex(b"source-cited bytes")
    assert ledger.audit_evidence()["agreed"] == 1


def test_ambiguous_evidence_refuses(ledger, tmp_path):
    art = tmp_path / "a.bin"
    art.write_bytes(b"x")
    with pytest.raises(ValueError, match="not both"):
        ledger.record_verdict(
            "m1", "shape", True, "h",
            evidence_path=art, evidence_bytes=b"y",
        )
    # nothing landed: the refusal precedes any write
    assert ledger.audit_evidence()["rows"] == 0


# -- case (c): tampered evidence file -> mismatch with the row id -------------------


def test_tampered_evidence_file_audit_reports_mismatch_with_row_id(
        ledger, tmp_path, capsys):
    art = tmp_path / "artifact.json"
    art.write_bytes(b'{"verdict": "pass"}')
    ledger.record_verdict("m1", "shape", True, evidence_path=art)
    original_hash = sha256_hex(b'{"verdict": "pass"}')

    # tamper AFTER the append: the row resolved honestly at its moment;
    # the audit must now catch that the bytes moved under the citation.
    art.write_bytes(b'{"verdict": "fail"}')

    audit = ledger.audit_evidence()
    assert (audit["agreed"], audit["mismatch"], audit["unresolved"]) == (0, 1, 0)
    hit = audit["mismatch_rows"][0]
    assert hit["id"] == 1                       # the row id, as the law asks
    assert hit["model_id"] == "m1"
    assert hit["stored_hash"] == original_hash
    assert hit["recomputed_hash"] == sha256_hex(b'{"verdict": "fail"}')
    assert hit["evidence_source"] == f"file:{art}"

    rc = ledger_main(["audit", str(ledger.db_path)])
    out = json.loads(capsys.readouterr().out)
    assert rc == 1                              # mismatch is a gate failure
    assert out["mismatch"] == 1
    assert out["mismatch_rows"][0]["id"] == 1


# -- legacy ledgers: additive migration, honest unresolved --------------------------


OLD_SCHEMA = """
CREATE TABLE verdict_log (
    ts            TEXT NOT NULL,
    model_id      TEXT NOT NULL,
    task_shape    TEXT NOT NULL,
    verdict       INTEGER NOT NULL,
    evidence_hash TEXT NOT NULL DEFAULT ''
);
"""


def test_pre_gate_ledger_migrates_additively_and_legacy_rows_read_unresolved(
        tmp_path):
    db = tmp_path / "legacy.db"
    conn = sqlite3.connect(db)
    conn.executescript(OLD_SCHEMA)
    conn.execute(
        "INSERT INTO verdict_log (ts, model_id, task_shape, verdict,"
        " evidence_hash) VALUES ('2026-09-30T00:00:00+00:00', 'old-m',"
        " 'old-shape', 1, 'duel:' || ?)",
        ("a" * 64,),
    )
    conn.commit()
    conn.close()

    led = CapabilityLedger(db)
    try:
        cols = {r["name"] for r in led.connection().execute(
            "PRAGMA table_info(verdict_log)")}
        assert {"evidence_resolved", "evidence_source", "evidence_bytes"} <= cols
        row = full_row(led, 1)
        assert row["evidence_resolved"] == 0    # legacy rows stay untrusted

        audit = led.audit_evidence()
        assert (audit["agreed"], audit["mismatch"], audit["unresolved"]) == (0, 0, 1)

        # new rows through the gate coexist with the legacy row
        led.record_verdict("new-m", "shape", True, evidence_bytes=b"z")
        audit = led.audit_evidence()
        assert (audit["agreed"], audit["unresolved"]) == (1, 1)
    finally:
        led.close()


# -- CLI contract -------------------------------------------------------------------


def test_cli_exit_codes(tmp_path, capsys):
    clean = CapabilityLedger(tmp_path / "clean.db")
    clean.record_verdict("m", "s", True, evidence_bytes=b"ok")
    clean.close()
    assert ledger_main(["audit", str(tmp_path / "clean.db")]) == 0
    assert json.loads(capsys.readouterr().out)["unresolved"] == 0

    bad = CapabilityLedger(tmp_path / "bad.db")
    bad.record_verdict("m", "s", True, "wrong", evidence_bytes=b"ok")
    bad.close()
    assert ledger_main(["audit", str(tmp_path / "bad.db")]) == 1
    capsys.readouterr()  # drain the mismatch report

    # unresolved-only is a finding, not a gate failure (pre-gate ledgers)
    unresolved_only = CapabilityLedger(tmp_path / "uo.db")
    unresolved_only.record_verdict("m", "s", True, "hash-only")
    unresolved_only.close()
    assert ledger_main(["audit", str(tmp_path / "uo.db")]) == 0
    assert json.loads(capsys.readouterr().out)["unresolved"] == 1

    assert ledger_main([]) == 2                 # usage error


def test_verdict_log_rows_shape_is_unchanged_for_the_momentum_path(ledger):
    """The 3-column read the momentum window uses keeps its exact shape."""
    ledger.record_verdict("m", "s", True, evidence_bytes=b"x")
    rows = ledger.verdict_log_rows("m", "s")
    assert set(rows[0]) == {"ts", "verdict", "evidence_hash"}


# -- duel importer integration: the gate's first in-repo caller --------------------


def _duel_row(ask_id, winner="A"):
    return {
        "ts": f"2026-10-01T00:00:{ask_id:02d}+00:00",
        "ask_id": ask_id,
        "mode": "blind",
        "a_model": "fam/a",
        "b_model": "fam/b",
        "winner": winner,
        "rubric": list(ADVERSARIAL_RUBRIC),
    }


def test_import_duel_bank_feeds_bytes_and_lands_resolved(tmp_path):
    from tools.gps_mcp.router import import_duel_bank

    led = CapabilityLedger(tmp_path / "duel.db")
    try:
        stats = import_duel_bank(led, [_duel_row(1)], source_path="test-bank")
        assert (stats["fed"], stats["verdicts"]) == (1, 2)
        assert all(
            r["evidence_resolved"] == 1
            for r in led.connection().execute(
                "SELECT evidence_resolved FROM verdict_log")
        )
        audit = led.audit_evidence()
        assert (audit["agreed"], audit["mismatch"], audit["unresolved"]) == (2, 0, 0)
        assert audit["resolved_at_append"] == 2

        # idempotency survives the gate: a re-feed skips both verdicts
        stats2 = import_duel_bank(led, [_duel_row(1)], source_path="test-bank")
        assert stats2["skipped_duplicate"] == 1
        assert stats2["verdicts"] == 0
        assert led.audit_evidence()["rows"] == 2
    finally:
        led.close()
