"""tests for tools/env_contract.py -- the MiMo-steal env contract (AC8 #1).

Laws pinned here:

  round trip -- emit_manifest writes canonical bytes (sorted keys, no wall
  clock, trailing newline); read_manifest returns the same dict; the
  engine/verifier sha256 pins are the LIVE bytes of mag/water_graph.py and
  tools/legality_propagator.py.

  drift law -- validate_manifest recomputes the live sha and refuses
  ENGINE_DRIFT / VERIFIER_DRIFT / ENGINE_MISSING; it never warns in place
  of refusing, and it never consults the version string (bytes only).

  reward law -- rows are binary (gps feed shape) + exact label + 64-hex
  evidence; identical calls produce identical bytes; a foreign verdict or
  weak evidence hash refuses.

  gps-feed law -- feed_reward_file is two-pass fail-closed like
  mag/gwap_to_gps.py: a missing key map or one foreign row refuses with
  the ledger untouched (zero capability rows, zero verdict_log rows); a
  clean feed lands one record_verdict per row with the row's
  evidence_hash, and the capability running mean is exactly k/n.

  wiring law (AH7) -- run_legality judges the propagator against the
  engine (verdict = agreement, label = engine ground truth), validates the
  family manifest BEFORE judging (drift or a foreign family refuses with
  no reward.json and no ledger file at all), regenerates reward.json
  byte-identically for the same seed, and feeds the ledger under the
  explicit model_id legality-propagator-v1.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from tools.env_contract import (
    MANIFEST_SCHEMA,
    REWARD_SCHEMA,
    DEFAULT_ENGINE_PATH,
    DEFAULT_TASK_SHAPE,
    DEFAULT_VERIFIER_PATH,
    LABEL_SET,
    ROOT,
    EnvContractError,
    emit_manifest,
    emit_reward,
    feed_reward_file,
    read_manifest,
    run_legality,
    validate_manifest,
)
from tools.gps_mcp.ledger import CapabilityLedger

ENGINE = ROOT / DEFAULT_ENGINE_PATH
VERIFIER = ROOT / DEFAULT_VERIFIER_PATH


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _refuses(code: str, excinfo: pytest.ExceptionInfo[EnvContractError]) -> None:
    """Assert the machine reason code (.reason), not the prose message."""
    assert excinfo.value.reason == code, f"want {code}, got " \
                                        f"{excinfo.value.reason}: {excinfo.value}"


# ----------------------------------------------------------- manifest ----
def test_manifest_round_trip_against_live_bytes(tmp_path: Path) -> None:
    out = tmp_path / "family"
    m = emit_manifest(out)
    written = out / "manifest.json"
    assert written.is_file()
    # canonical bytes: sorted keys, tight separators, one trailing newline
    body = written.read_bytes()
    assert body.endswith(b"\n") and body.count(b"\n") == 1
    assert json.loads(body) == json.loads(
        json.dumps(m, sort_keys=True, separators=(",", ":")))
    # fixed field vocabulary: no wall-clock key can exist (timeout_sec is
    # a declared budget constant, not a stamp)
    assert set(m) == {
        "schema", "env_id", "engine", "engine_path", "engine_version",
        "engine_sha256", "verifier", "verifier_path", "verifier_sha256",
        "task_shape", "reward_style", "reward_schema", "timeout_sec",
        "determinism", "label_set"}
    assert m["schema"] == MANIFEST_SCHEMA
    assert m["reward_schema"] == REWARD_SCHEMA

    back = read_manifest(written)
    assert back == m
    assert m["engine"] == "water_graph"
    assert m["verifier"] == "propagator"
    assert m["task_shape"] == DEFAULT_TASK_SHAPE
    assert m["reward_style"] == "rule"
    assert m["timeout_sec"] == 0  # 0 = exact/instant, the declared advantage
    assert m["determinism"] == "seeded"
    assert m["label_set"] == [
        "illegal_unknown_verb", "illegal_unknown_target",
        "illegal_dry_pool", "legal_no_gain", "legal_gain"]
    # the pins are the LIVE engine/verifier bytes
    assert m["engine_sha256"] == _hash(ENGINE)
    assert m["verifier_sha256"] == _hash(VERIFIER)
    # the reader validates those same bytes clean
    ok = validate_manifest(written)
    assert ok["ok"] is True and ok["env_id"] == m["env_id"]
    assert ok["engine_sha256"] == m["engine_sha256"]


def test_manifest_emit_accepts_direct_json_path_and_is_deterministic(
        tmp_path: Path) -> None:
    f1 = tmp_path / "a.json"
    f2 = tmp_path / "b.json"
    emit_manifest(f1)
    emit_manifest(f2)
    assert f1.read_bytes() == f2.read_bytes()


def test_read_manifest_fail_closed(tmp_path: Path) -> None:
    good = tmp_path / "manifest.json"
    emit_manifest(good)

    with pytest.raises(EnvContractError) as ei:
        read_manifest(tmp_path / "nope.json")
    _refuses("MISSING_MANIFEST", ei)

    bad_schema = tmp_path / "foreign.json"
    row = json.loads(good.read_text(encoding="utf-8"))
    row["schema"] = "harbor.v9"
    bad_schema.write_text(json.dumps(row), encoding="utf-8")
    with pytest.raises(EnvContractError) as ei:
        read_manifest(bad_schema)
    _refuses("BAD_MANIFEST", ei)

    drop_field = tmp_path / "drop.json"
    del row["schema"]
    row["schema"] = MANIFEST_SCHEMA
    del row["engine_sha256"]
    drop_field.write_text(json.dumps(row), encoding="utf-8")
    with pytest.raises(EnvContractError) as ei:
        read_manifest(drop_field)
    _refuses("BAD_MANIFEST", ei)

    bool_timeout = tmp_path / "bool.json"
    row["engine_sha256"] = "0" * 64
    row["timeout_sec"] = True  # bool is an int subclass -- still a lie
    bool_timeout.write_text(json.dumps(row), encoding="utf-8")
    with pytest.raises(EnvContractError) as ei:
        read_manifest(bool_timeout)
    _refuses("BAD_MANIFEST", ei)


# -------------------------------------------------------------- drift ----
def test_validate_detects_engine_and_verifier_drift(tmp_path: Path) -> None:
    eng = tmp_path / "engine.py"
    ver = tmp_path / "verifier.py"
    eng.write_text("ENGINE v1\n", encoding="utf-8")
    ver.write_text("VERIFIER v1\n", encoding="utf-8")
    mf = tmp_path / "manifest.json"
    emit_manifest(mf, engine_path=eng, verifier_path=ver,
                  repo_root=tmp_path)  # outside any repo: sha256 version pin

    ok = validate_manifest(mf, engine_path=eng, verifier_path=ver,
                           repo_root=tmp_path)
    assert ok["ok"] is True

    eng.write_text("ENGINE v2  # drifted\n", encoding="utf-8")
    with pytest.raises(EnvContractError) as ei:
        validate_manifest(mf, engine_path=eng, verifier_path=ver,
                          repo_root=tmp_path)
    _refuses("ENGINE_DRIFT", ei)

    eng.write_text("ENGINE v1\n", encoding="utf-8")  # restore: clean again
    ver.write_text("VERIFIER v2  # drifted\n", encoding="utf-8")
    with pytest.raises(EnvContractError) as ei:
        validate_manifest(mf, engine_path=eng, verifier_path=ver,
                          repo_root=tmp_path)
    _refuses("VERIFIER_DRIFT", ei)

    with pytest.raises(EnvContractError) as ei:
        validate_manifest(mf, engine_path=tmp_path / "gone.py",
                          verifier_path=ver, repo_root=tmp_path)
    _refuses("ENGINE_MISSING", ei)


# ------------------------------------------------------------- reward ----
def test_reward_row_shape_normalization_and_determinism(
        tmp_path: Path) -> None:
    r1 = emit_reward("case-7", True, "A" * 64, label="legal_gain")
    r2 = emit_reward("case-7", 1, "a" * 64, label="legal_gain")
    assert r1 == r2
    assert r1["verdict"] == 1  # bool normalized to the binary feed shape
    assert r1["label"] == "legal_gain"  # exact vocabulary rides the row
    assert r1["evidence_hash"] == "a" * 64  # case-folded to canonical hex
    assert r1["task_shape"] == DEFAULT_TASK_SHAPE
    assert set(r1) == {"schema", "env_id", "task_shape", "case_id",
                       "verdict", "label", "evidence_hash"}
    assert emit_reward("c", "fail", "b" * 64)["verdict"] == 0
    assert emit_reward("c", "pass", "b" * 64)["verdict"] == 1

    with pytest.raises(EnvContractError) as ei:
        emit_reward("c", 2, "b" * 64)  # not binary; use `label` for nuance
    _refuses("BAD_VERDICT", ei)
    with pytest.raises(EnvContractError) as ei:
        emit_reward("c", 1, "short")
    _refuses("BAD_EVIDENCE_HASH", ei)
    with pytest.raises(EnvContractError) as ei:
        emit_reward("  ", 1, "b" * 64)
    _refuses("BAD_CASE_ID", ei)

    dest = tmp_path / "reward.json"
    emit_reward("case-7", True, "a" * 64, label="legal_gain", dest=dest)
    emit_reward("case-8", "fail", "b" * 64, label="illegal_dry_pool",
                dest=dest)
    lines = dest.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert lines[0] == json.dumps(r1, sort_keys=True,
                                  separators=(",", ":"))  # canonical JSONL


# ----------------------------------------------------------- gps feed ----
def test_reward_file_feeds_gps_ledger(tmp_path: Path) -> None:
    rp = tmp_path / "reward.json"
    emit_reward("c1", True, "a" * 64, label="legal_gain", dest=rp)
    emit_reward("c2", 1, "b" * 64, label="legal_gain", dest=rp)
    emit_reward("c3", "fail", "c" * 64, label="illegal_dry_pool", dest=rp)

    db = tmp_path / "gps.db"
    ledger = CapabilityLedger(db)
    try:
        report = feed_reward_file(rp, ledger, model_id="tiny-ldt")
        cap = ledger.report_capability("tiny-ldt", DEFAULT_TASK_SHAPE)
    finally:
        ledger.close()

    assert report["rows_seen"] == 3 and report["fed"] == 3
    assert report["evidence_hashes"] == ["a" * 64, "b" * 64, "c" * 64]
    assert report["model_ids"] == ["tiny-ldt"]
    assert cap is not None and cap["sample_size"] == 3
    assert cap["pass_rate"] == pytest.approx(2 / 3)  # running mean k/n


def test_feed_refusals_leave_ledger_untouched(tmp_path: Path) -> None:
    rp = tmp_path / "reward.json"
    emit_reward("c1", 1, "a" * 64, dest=rp)
    emit_reward("c2", 0, "b" * 64, dest=rp)

    db = tmp_path / "gps.db"
    ledger = CapabilityLedger(db)
    try:
        # no key map: model_id is never guessed (the gwap_to_gps law)
        with pytest.raises(EnvContractError) as ei:
            feed_reward_file(rp, ledger)
        _refuses("NO_KEY_MAP", ei)
        # partial map: the unmapped case refuses
        with pytest.raises(EnvContractError) as ei:
            feed_reward_file(rp, ledger, case_to_model={"c1": "m1"})
        _refuses("UNMAPPED_CASE", ei)
        # nothing was fed by either refusal
        assert ledger.connection().execute(
            "SELECT COUNT(*) FROM capability").fetchone()[0] == 0
        assert ledger.connection().execute(
            "SELECT COUNT(*) FROM verdict_log").fetchone()[0] == 0

        # one foreign row refuses the whole file (two-pass atomicity)
        with open(rp, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"schema": "nope"}) + "\n")
        with pytest.raises(EnvContractError) as ei:
            feed_reward_file(rp, ledger, model_id="m1")
        _refuses("BAD_REWARD_ROW", ei)
        assert ledger.connection().execute(
            "SELECT COUNT(*) FROM capability").fetchone()[0] == 0

        with pytest.raises(EnvContractError) as ei:
            feed_reward_file(tmp_path / "gone.json", ledger, model_id="m1")
        _refuses("MISSING_REWARD_FILE", ei)
    finally:
        ledger.close()


# ------------------------------------------------------- wiring (AH7) ----
def test_run_legality_judges_emits_and_feeds(tmp_path: Path) -> None:
    # a family manifest over the LIVE engine/verifier bytes, emitted to a
    # direct *.json path the way the wiring homes do
    mf = tmp_path / "env_manifest.v1.json"
    emit_manifest(mf)
    db = tmp_path / "gps.db"
    rp = tmp_path / "reward.json"

    rep = run_legality(cases=5, seed=17, manifest_path=mf, reward_path=rp,
                       ledger_path=db)

    # the judged subject is the propagator: agreement law says 100% here
    assert rep["cases"] == 5 and rep["agree"] == 5
    assert rep["agreement_rate"] == 1.0
    assert rep["fed"] == 5 and rep["model_id"] == "legality-propagator-v1"
    assert set(rep["labels"]) <= set(LABEL_SET)
    # reward.json regenerated per run: exactly this run's rows, canonical
    lines = rp.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 5
    row = json.loads(lines[0])
    assert row["schema"] == REWARD_SCHEMA
    assert row["task_shape"] == DEFAULT_TASK_SHAPE
    assert row["case_id"] == "legality-00017-0000"
    assert row["verdict"] == 1 and row["label"] in LABEL_SET
    assert len(row["evidence_hash"]) == 64 and row["evidence_hash"].islower()
    # determinism: same seed + same bytes -> byte-identical reward file
    rp2 = tmp_path / "reward2.json"
    run_legality(cases=5, seed=17, manifest_path=mf, reward_path=rp2,
                 ledger_path=None)
    assert rp2.read_bytes() == rp.read_bytes()
    # the feed landed in the ledger: one verdict_log row per judged case
    ledger = CapabilityLedger(db)
    try:
        cap = ledger.report_capability("legality-propagator-v1",
                                       DEFAULT_TASK_SHAPE)
        assert cap is not None and cap["sample_size"] == 5
        assert cap["pass_rate"] == pytest.approx(1.0)
        assert len(ledger.verdict_log_rows("legality-propagator-v1",
                                           DEFAULT_TASK_SHAPE)) == 5
    finally:
        ledger.close()


def test_run_legality_refuses_under_drift_and_mismatch(tmp_path: Path) -> None:
    eng = tmp_path / "engine.py"
    ver = tmp_path / "verifier.py"
    eng.write_text("E1\n", encoding="utf-8")
    ver.write_text("V1\n", encoding="utf-8")
    mf = tmp_path / "manifest.json"
    emit_manifest(mf, engine_path=eng, verifier_path=ver, repo_root=tmp_path)
    db = tmp_path / "gps.db"
    rp = tmp_path / "reward.json"

    # drift: engine bytes move under the manifest -> refuse BEFORE judging
    eng.write_text("E2  # drifted\n", encoding="utf-8")
    with pytest.raises(EnvContractError) as ei:
        run_legality(cases=3, manifest_path=mf, reward_path=rp, ledger_path=db,
                     repo_root=tmp_path)
    _refuses("ENGINE_DRIFT", ei)
    assert not rp.exists() and not db.exists()  # nothing judged, nothing fed

    # mismatch: a VALID manifest of a DIFFERENT family still refuses -- rows
    # that lie about their family are worse than no rows
    eng.write_text("E1\n", encoding="utf-8")
    other = tmp_path / "other.json"
    emit_manifest(other, env_id="some-other-family-v1", engine_path=eng,
                  verifier_path=ver, repo_root=tmp_path)
    with pytest.raises(EnvContractError) as ei:
        run_legality(cases=3, manifest_path=other, reward_path=rp,
                     ledger_path=db, repo_root=tmp_path)
    _refuses("MANIFEST_MISMATCH", ei)
    assert not rp.exists() and not db.exists()
