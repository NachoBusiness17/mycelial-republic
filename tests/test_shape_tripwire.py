"""shape_tripwire tests (compost 2026-10-09, revival 1 pre-warm).

Synthetic ledger fixtures under tmp_path pin the counting law: the evidence
gate (>= MIN_ROWS verdict rows per shape), the 24/25 crossover boundary,
attention written only on breach, --dry writing nothing, the read-only open
(production ledger bytes never move), and the cannot-verify exit for a
missing db.
"""
from __future__ import annotations

import sqlite3

import pytest

from tools import shape_tripwire


def make_db(tmp_path, shape_rows: dict[str, int]) -> object:
    """Build a minimal gps ledger with the verdict_log table shape the
    production tools/gps_mcp/gps_ledger.db3 carries (ts, model_id,
    task_shape, verdict); insert n rows per named shape."""
    db = tmp_path / "gps_ledger.db3"
    # mkdir before connect: callers pass fresh subdirs (tmp_path / "a") so the
    # 24/25 fixture pair gets distinct db files, and sqlite3.connect refuses
    # to create a file inside a nonexistent directory (the 4 first-run
    # failures this cured, 2026-10-09, evidence: pytest run this sitting)
    tmp_path.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db)
    conn.execute(
        "CREATE TABLE verdict_log (ts TEXT NOT NULL, model_id TEXT NOT NULL,"
        " task_shape TEXT NOT NULL, verdict INTEGER NOT NULL,"
        " evidence_hash TEXT NOT NULL DEFAULT '')"
    )
    i = 0
    for shape, n in shape_rows.items():
        for _ in range(n):
            i += 1
            conn.execute(
                "INSERT INTO verdict_log VALUES (?, ?, ?, ?, '')",
                (f"2026-10-09T00:00:{i % 60:02d}Z", "m/test-model", shape, i % 2),
            )
    conn.commit()
    conn.close()
    return db


def test_counts_gated_shapes_only(tmp_path):
    db = make_db(tmp_path, {"alpha": 5, "beta": 6, "gamma": 7, "thin": 4})
    census = shape_tripwire.count_shapes(db)
    assert census["distinct_shapes"] == 4
    assert census["gated_shapes"] == 3  # thin (4 rows) fails the >=5 gate
    assert census["counts"] == {"beta": 6, "gamma": 7, "alpha": 5}
    assert census["verdict_rows"] == 22


def test_gate_boundary_exactly_min_rows_counts(tmp_path):
    db = make_db(tmp_path, {"edge": shape_tripwire.MIN_ROWS})
    census = shape_tripwire.count_shapes(db)
    assert census["gated_shapes"] == 1  # the gate is >=, not >


def test_breach_at_25_not_at_24(tmp_path, monkeypatch):
    alert = tmp_path / "attention.md"
    monkeypatch.setattr(shape_tripwire, "ALERT", alert)
    shapes24 = {f"shape-{i:02d}": 5 for i in range(24)}
    assert shape_tripwire.run(["--db", str(make_db(tmp_path / "a", shapes24))]) == 0
    assert not alert.exists()
    # distinct db so the 25-shape fixture is not a file the run created
    shapes25 = {f"shape-{i:02d}": 5 for i in range(25)}
    assert shape_tripwire.run(["--db", str(make_db(tmp_path / "b", shapes25))]) == 1
    assert alert.exists()


def test_attention_line_written_only_on_breach(tmp_path, monkeypatch):
    alert = tmp_path / "attention.md"
    monkeypatch.setattr(shape_tripwire, "ALERT", alert)
    below = {f"s{i}": 9 for i in range(shape_tripwire.CROSSOVER_MIN - 1)}
    assert shape_tripwire.run(["--db", str(make_db(tmp_path / "c", below))]) == 0
    assert not alert.exists()
    over = {f"s{i}": 9 for i in range(shape_tripwire.CROSSOVER_MIN + 3)}
    assert shape_tripwire.run(["--db", str(make_db(tmp_path / "d", over))]) == 1
    text = alert.read_text(encoding="utf-8")
    assert text.count("\n") == 1
    assert "GPS-EMBED cold-start crossover near:" in text
    assert f"{shape_tripwire.CROSSOVER_MIN + 3} distinct shapes" in text
    assert "rerun the one-command trial" in text
    assert shape_tripwire.TRIAL_RECEIPT in text
    assert shape_tripwire.TRIAL_COMMAND in text
    assert text.startswith("- ") and "SHAPE_TRIPWIRE" in text


def test_dry_prints_count_and_writes_nothing(tmp_path, monkeypatch, capsys):
    alert = tmp_path / "attention.md"
    monkeypatch.setattr(shape_tripwire, "ALERT", alert)
    breachy = {f"s{i}": 7 for i in range(shape_tripwire.CROSSOVER_MIN)}
    rc = shape_tripwire.run(
        ["--dry", "--db", str(make_db(tmp_path / "e", breachy))]
    )
    assert rc == 0  # --dry never breaches
    assert not alert.exists()
    out = capsys.readouterr().out
    assert f'"gated_shapes": {shape_tripwire.CROSSOVER_MIN}' in out
    assert "ALERT:" in out  # the alert is still printed, just not banked


def test_ledger_bytes_untouched_by_breach_run(tmp_path, monkeypatch):
    alert = tmp_path / "attention.md"
    monkeypatch.setattr(shape_tripwire, "ALERT", alert)
    db = make_db(tmp_path / "f", {f"s{i}": 6 for i in range(30)})
    before = (db).read_bytes()
    assert shape_tripwire.run(["--db", str(db)]) == 1
    assert db.read_bytes() == before  # read-only law: production bytes never move


def test_missing_db_is_cannot_verify_exit_2(tmp_path, capsys):
    rc = shape_tripwire.run(["--db", str(tmp_path / "nope.db3")])
    assert rc == 2
    assert "CANNOT-VERIFY" in capsys.readouterr().err


def test_live_ledger_quiet_today():
    """The production ledger at the 2026-10-09 sitting: 703 verdict rows,
    10 distinct shapes, 9 over the gate (one shape holds 4 rows) - far
    under the 25 crossover, so the live reading must be exit 0 quiet. If
    this pin ever fails RED it means the ledger grew semantic families:
    that is the tripwire doing its job, not a test defect."""
    if not shape_tripwire.LEDGER.is_file():
        pytest.skip("production gps ledger not on this seat")
    census = shape_tripwire.count_shapes(shape_tripwire.LEDGER)
    assert census["verdict_rows"] == 703
    assert census["distinct_shapes"] == 10
    assert census["gated_shapes"] == 9
    assert shape_tripwire.breach(census) is False
