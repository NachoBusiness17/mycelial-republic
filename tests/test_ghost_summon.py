"""Tests for mag/ghost_summon — deterministic intent discovery (current+future+coldest).

Hermetic: monkeypatches data dirs to temp so tests never touch live state. The module
reads via ROOT-relative paths, so we monkeypatch mag.ghost_summon.ROOT to a temp tree.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from mag import ghost_summon as gs


@pytest.fixture()
def tree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Build a small fake Mag tree and point ghost_summon at it."""
    (tmp_path / "memory" / "agent_state").mkdir(parents=True)
    (tmp_path / "memory" / "ideas").mkdir(parents=True)
    (tmp_path / "memory" / "biography" / "residual").mkdir(parents=True)

    (tmp_path / "memory" / "agent_state" / "LATEST.json").write_text(
        json.dumps({"next_moves": ["eat comms_trail into routing"],
                    "do_not_redesign": ["redesign the mycelium graph"]}),
        encoding="utf-8")

    (tmp_path / "memory" / "ideas" / "nodes.jsonl").write_text(
        "\n".join([
            json.dumps({"id": "n_a", "type": "open_loop", "status": "open", "title": "cold A", "body": "b"}),
            json.dumps({"id": "n_b", "type": "open_loop", "status": "open", "title": "warm B", "body": "b"}),
            json.dumps({"id": "n_c", "type": "project", "status": "open", "title": "cold C", "body": "b"}),
            json.dumps({"id": "n_done", "type": "open_loop", "status": "done", "title": "done D", "body": "b"}),
        ]),
        encoding="utf-8")
    (tmp_path / "memory" / "ideas" / "edges.jsonl").write_text(
        json.dumps({"id": "e1", "src": "n_b", "dst": "n_c"}) + "\n",
        encoding="utf-8")
    (tmp_path / "memory" / "ideas" / "orphans.jsonl").write_text(
        json.dumps({"id": "o1", "intent": "old orphan", "source": "system",
                    "first_seen": "2020-01-01T00:00:00+00:00"}) + "\n" +
        json.dumps({"id": "o2", "intent": "fresh orphan", "source": "system",
                    "first_seen": "2099-01-01T00:00:00+00:00"}) + "\n",
        encoding="utf-8")

    (tmp_path / "memory" / "biography" / "residual" / "seed.json").write_text(
        json.dumps({"session_id": "seed", "tldr": "t"}), encoding="utf-8")

    monkeypatch.setattr(gs, "ROOT", tmp_path)
    return tmp_path


def test_summon_schema(tree: Path) -> None:
    r = gs.summon("hello")
    assert r["ok"] is True
    assert r["schema"] == "ghost_summon.v1"
    assert r["deterministic"] is True
    for key in ("current", "future", "coldest_vertices", "core_invariants", "stale_skip", "brief"):
        assert key in r


def test_coldest_ranks_low_degree_first(tree: Path) -> None:
    cv = gs.coldest_vertices()
    titles = [v["title"] for v in cv]
    # n_a (0 conn) before n_b/n_c (1 conn); done nodes excluded
    assert titles[0] == "cold A"
    assert "done D" not in titles
    # every returned node is open
    assert all(v["type"] != "done" for v in cv)


def test_stale_skip_flags_old_orphans_and_do_not(tree: Path) -> None:
    ss = gs.stale_skip()
    assert "redesign the mycelium graph" in ss["do_not_redesign"]
    stale_ids = [o["id"] for o in ss["stale_orphans"]]
    assert "o1" in stale_ids          # old (2020) orphan flagged stale
    assert "o2" not in stale_ids      # fresh orphan not stale


def test_future_reads_next_moves_and_orphans(tree: Path) -> None:
    f = gs.future_state()
    assert "eat comms_trail into routing" in f["next_moves"]
    assert len(f["orphans"]) == 2
    assert len(f["open_loops"]) == 2  # only open open_loops (n_a, n_b); n_c is project


def test_core_invariants_present(tree: Path) -> None:
    ci = gs.core_invariants_status()
    assert "consent_first" in ci["invariants"]
    assert ci["newest_residual_age_s"] is not None


def test_gather_never_raises_on_missing(tree: Path) -> None:
    # remove all data dirs -> module must degrade gracefully
    import shutil
    shutil.rmtree(str(tree / "memory"), ignore_errors=True)
    g = gs.gather("x")
    assert "current" in g
    assert "future" in g
    assert "coldest_vertices" in g
