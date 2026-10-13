"""D7 regression: GPS capability metabolism (decay + slash + epoch reset).

The door (eleven-doors D7-pheromone-metabolism): the stored running mean
never decays, so stale rows route dollars on dead evidence and live
dispute streaks dilute into the lifetime mean. The fix:
tools/gps_mcp/metabolism.py computes the routing-facing effective rate
read-only - alpha-decay toward the 0.5 prior (tau 14d), dispute-streak
slashing (0.85^min(streak,3)), and a drift-patrol-keyed epoch marker
that collapses pre-marker rows to the prior until re-measured. The
stored mean stays the audit surface.
"""
import sqlite3

import pytest

from tools.gps_mcp.metabolism import (
    PRIOR,
    TAU_DAYS,
    load_epoch,
    metabolic_rates,
    reset_epoch,
)

NOW = "2026-10-05T12:00:00Z"


@pytest.fixture()
def db(tmp_path):
    conn = sqlite3.connect(tmp_path / "gps.db3")
    conn.executescript(
        """
        CREATE TABLE capability (
            model_id TEXT, task_shape TEXT, pass_rate REAL,
            sample_size INTEGER, cost_usd_per_call REAL,
            last_measured TEXT, updated_at TEXT,
            PRIMARY KEY (model_id, task_shape)
        );
        CREATE TABLE verdict_log (
            ts TEXT, model_id TEXT, task_shape TEXT, verdict INTEGER,
            evidence_hash TEXT, evidence_resolved INTEGER,
            evidence_source TEXT, evidence_bytes BLOB
        );
        """
    )
    yield conn
    conn.close()


def _cap(conn, model, shape, rate, ts, n=50):
    conn.execute(
        "INSERT INTO capability VALUES (?,?,?,?,NULL,?,?)",
        (model, shape, rate, n, ts, ts),
    )


def _vlog(conn, model, shape, verdict, ts):
    conn.execute(
        "INSERT INTO verdict_log VALUES (?,?,?,?,?,1,'t',NULL)",
        (ts, model, shape, verdict, f"h-{model}-{shape}-{ts}-{verdict}"),
    )


def test_fresh_row_keeps_stored_rate(db):
    _cap(db, "m/a", "t1", 0.900, NOW)
    db.commit()
    r = metabolic_rates(db, now=NOW)[0]
    assert r.age_days == pytest.approx(0.0)
    assert r.decayed_rate == pytest.approx(0.900)
    assert r.effective_rate == pytest.approx(0.900)


def test_old_row_decays_toward_prior(db):
    # 2*tau old: exp(-2) of the distance to the prior remains
    import math

    _cap(db, "m/a", "t1", 0.900, "2026-09-07T12:00:00Z")
    db.commit()
    r = metabolic_rates(db, now=NOW)[0]
    assert r.decayed_rate == pytest.approx(PRIOR + 0.4 * math.exp(-2.0))
    assert r.effective_rate == r.decayed_rate


def test_fail_streak_slashes_and_caps(db):
    _cap(db, "m/a", "t1", 0.800, NOW)
    # 7 trailing fails: slash capped at 3
    for i in range(7):
        _vlog(db, "m/a", "t1", 0, f"2026-10-05T11:5{i}:00Z")
    db.commit()
    r = metabolic_rates(db, now=NOW)[0]
    assert r.fail_streak == 7
    assert r.slashed_rate == pytest.approx(0.800 * 0.85 ** 3)
    assert r.effective_rate == r.slashed_rate


def test_pass_breaks_the_streak(db):
    _cap(db, "m/a", "t1", 0.800, NOW)
    _vlog(db, "m/a", "t1", 0, "2026-10-05T11:50:00Z")
    _vlog(db, "m/a", "t1", 1, "2026-10-05T11:51:00Z")  # freshest is a pass
    db.commit()
    r = metabolic_rates(db, now=NOW)[0]
    assert r.fail_streak == 0
    assert r.effective_rate == pytest.approx(0.800)


def test_epoch_marker_collapses_pre_marker_rows_only(db):
    _cap(db, "m/old", "t1", 0.950, "2026-10-01T00:00:00Z")   # tainted era
    _cap(db, "m/fresh", "t1", 0.700, "2026-10-05T00:00:00Z")  # fresh epoch
    db.commit()
    epoch = {"epoch_ts_utc": "2026-10-04T12:00:00Z", "reason": "gps-dedupe cure"}
    rates = {r.model_id: r for r in metabolic_rates(db, now=NOW, epoch=epoch)}
    assert rates["m/old"].epoch_reset is True
    assert rates["m/old"].effective_rate == pytest.approx(PRIOR)
    assert rates["m/fresh"].epoch_reset is False
    # 12h old: slight decay toward the prior, epoch does not touch it
    import math

    assert rates["m/fresh"].effective_rate == pytest.approx(0.5 + 0.2 * math.exp(-0.5 / TAU_DAYS))


def test_epoch_roundtrip_and_corrupt_marker_ignored(db, tmp_path):
    marker_path = tmp_path / "epoch.json"
    marker = reset_epoch(marker_path, reason="test drift event", ts_utc="2026-10-04T12:00:00Z")
    assert marker["reason"] == "test drift event"
    assert load_epoch(marker_path) == marker
    marker_path.write_text("{not json", encoding="utf-8")
    assert load_epoch(marker_path) is None


def test_tau_constant_pinned():
    # the door's decay contract: tau 14d means a 14-day-old row keeps
    # exp(-1) of its distance from the prior - pin the constant so a
    # silent retune cannot ride in
    assert TAU_DAYS == 14.0
