"""EG-20 regression: pass@K coverage beside win rate on the GPS battery.

The gap (ESTATE_GAPS_20261004.json EG-20): arena/gwap scored agreement
and wins, never pass@K, so the mesh-vs-frontier split could not be
predicted. The fix: tools/gps_mcp/coverage.py keys problems from gwap
scene_ids (arena run = shared scenario), counts unresolved-evidence rows
as excluded (never re-denominated), and predicts ROUTE_MESH /
ROUTE_FRONTIER / INSUFFICIENT with a problems floor. These tests pin the
keying, the exclusion, the floor, and the verdict arithmetic on
synthetic ledgers with known ground truth.
"""
import json
import sqlite3

import pytest

from tools.gps_mcp.coverage import (
    INSUFFICIENT,
    ROUTE_FRONTIER,
    ROUTE_MESH,
    coverage_report,
    mesh_vs_frontier,
    problem_key,
)


def _core(scene_id: str) -> bytes:
    return json.dumps(
        {"seq": 1, "ts_utc": "2026-10-05T00:00:00Z",
         "payload": {"schema": "gwap-payload-v1", "scene_id": scene_id},
         "prev_sha256": "0" * 64},
    ).encode("utf-8")


@pytest.fixture()
def db(tmp_path):
    conn = sqlite3.connect(tmp_path / "gps.db3")
    # static DDL, byte-identical to the production verdict_log shape
    conn.executescript(
        """
        CREATE TABLE verdict_log (
            ts TEXT, model_id TEXT, task_shape TEXT, verdict INTEGER,
            evidence_hash TEXT, evidence_resolved INTEGER,
            evidence_source TEXT, evidence_bytes BLOB
        );
        """
    )
    yield conn
    conn.close()


def _feed(conn, model: str, scene: str, verdict: int, resolved: bool = True) -> None:
    conn.execute(
        "INSERT INTO verdict_log VALUES (?,?,?,?,?,?,?,?)",
        ("2026-10-05T00:00:00Z", model, "arena-agreement-v1", verdict,
         f"hash-{model}-{scene}-{verdict}", int(resolved),
         "gwap" if resolved else "attested",
         _core(scene) if resolved else b""),
    )


# -- problem keying ---------------------------------------------------------


def test_problem_key_arena_run_strips_actor():
    assert problem_key(_core("arena-dnd0_20261004T032151Z-grok")) == "arena-dnd0_20261004T032151Z"


def test_problem_key_non_arena_scene_is_itself():
    assert problem_key(_core("night-judgment-lane-7")) == "night-judgment-lane-7"


def test_problem_key_unresolved_or_garbage_is_none():
    assert problem_key(None) is None
    assert problem_key(_core("arena-run-actor"), evidence_resolved=False) is None
    assert problem_key(b"not json") is None
    assert problem_key(json.dumps({"payload": {}}).encode("utf-8")) is None


# -- coverage report --------------------------------------------------------


def test_coverage_gain_fleet_beats_best_single(db):
    # 12 problems. sharpened: passes 8 alone (pass@1 0.667) but its misses
    # are missed by everyone; diverse: passes 3 different problems the
    # sharpened model missed -> fleet covers 11/12.
    for i in range(12):
        scene = f"arena-run{i}-x"
        sharpened = 1 if i < 8 else 0
        _feed(db, "model/sharpened", scene, sharpened)
        diverse = 1 if i >= 8 and i < 11 else 0
        _feed(db, "model/diverse", scene, diverse)
    db.commit()
    r = coverage_report(db, "arena-agreement-v1")
    assert r.problems == 12
    assert r.keyed_rows == 24 and r.excluded_rows == 0
    assert r.best_single_model == "model/sharpened"
    assert r.best_single_pass_at_1 == pytest.approx(8 / 12)
    assert r.fleet_solved == 11
    assert r.fleet_pass_at_k == pytest.approx(11 / 12)
    assert r.coverage_gain == pytest.approx(11 / 12 - 8 / 12)


def test_unresolved_rows_excluded_and_reported_never_rekeyed(db):
    for i in range(12):
        _feed(db, "model/a", f"arena-run{i}-x", 1 if i < 6 else 0)
    _feed(db, "model/a", "arena-run0-x", 0, resolved=False)  # pre-a04 class
    db.commit()
    r = coverage_report(db, "arena-agreement-v1")
    assert r.excluded_rows == 1
    assert r.keyed_rows == 12
    assert r.problems == 12  # the unresolved row added NO new problem


def test_best_single_requires_attempt_floor(db):
    # one-shot 1/1 model must not wear the best-single crown over a
    # 0.5-rate model with real sample size
    for i in range(12):
        _feed(db, "model/steady", f"arena-run{i}-x", 1 if i < 6 else 0)
    _feed(db, "model/oneshot", "arena-run0-x", 1)
    db.commit()
    r = coverage_report(db, "arena-agreement-v1")
    assert r.best_single_model == "model/steady"
    assert r.best_single_pass_at_1 == pytest.approx(0.5)


# -- mesh vs frontier -------------------------------------------------------


def test_route_mesh_when_fleet_coverage_beats_frontier(db):
    for i in range(12):
        scene = f"arena-run{i}-x"
        _feed(db, "model/cheap1", scene, 1 if i < 5 else 0)
        _feed(db, "model/cheap2", scene, 1 if 5 <= i < 9 else 0)  # disjoint wins
        _feed(db, "model/premium", scene, 1 if i < 4 else 0)
    db.commit()
    v = mesh_vs_frontier(db, "arena-agreement-v1",
                         mesh_models=["model/cheap1", "model/cheap2"],
                         frontier_models=["model/premium"])
    assert v.verdict == ROUTE_MESH
    assert v.mesh_pass_at_k == pytest.approx(9 / 12)
    assert v.frontier_pass_at_1 == pytest.approx(4 / 12)


def test_route_frontier_when_premium_pass1_exceeds_fleet_coverage(db):
    for i in range(12):
        scene = f"arena-run{i}-x"
        _feed(db, "model/cheap1", scene, 1 if i < 2 else 0)
        _feed(db, "model/cheap2", scene, 1 if i == 2 else 0)
        _feed(db, "model/premium", scene, 1 if i < 9 else 0)
    db.commit()
    v = mesh_vs_frontier(db, "arena-agreement-v1",
                         mesh_models=["model/cheap1", "model/cheap2"],
                         frontier_models=["model/premium"])
    assert v.verdict == ROUTE_FRONTIER
    assert v.mesh_pass_at_k == pytest.approx(3 / 12)
    assert v.frontier_pass_at_1 == pytest.approx(9 / 12)


def test_inside_margin_is_insufficient_never_a_coin_flip(db):
    # 24 problems: mesh 12/24 = 0.500 vs frontier 13/24 = 0.5417, gap
    # 0.0417 inside margin 0.05 -> no prediction either way
    for i in range(24):
        scene = f"arena-run{i}-x"
        _feed(db, "model/cheap1", scene, 1 if i < 12 else 0)
        _feed(db, "model/premium", scene, 1 if i < 13 else 0)
    db.commit()
    v = mesh_vs_frontier(db, "arena-agreement-v1",
                         mesh_models=["model/cheap1"],
                         frontier_models=["model/premium"])
    assert v.verdict == INSUFFICIENT


def test_below_problems_floor_is_insufficient(db):
    for i in range(4):
        scene = f"arena-run{i}-x"
        _feed(db, "model/cheap1", scene, 1)
        _feed(db, "model/premium", scene, 0)
    db.commit()
    v = mesh_vs_frontier(db, "arena-agreement-v1",
                         mesh_models=["model/cheap1"],
                         frontier_models=["model/premium"])
    assert v.verdict == INSUFFICIENT
    assert "floor" in v.reason
