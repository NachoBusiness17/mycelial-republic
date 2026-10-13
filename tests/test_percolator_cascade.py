"""Invariant cascade (CP-1 port, 2026-10-03) - depends_on edges + proposals, never mutations.

Port of the localfirst-steal atlas lane's cascade ledger spec (watch/inbox/localfirst/
atlas.md section 4) onto the percolator registry. Laws under test:
  1. THE CASCADE FIRES ON A DEPENDENCY CHANGE - a parent invariant move (count change,
     removal, supersede) BFS-walks reverse depends_on edges and yields one PROPOSAL per
     dependent, shallowest first (depth recorded, cycle guard, max_depth/max_nodes caps);
  2. PROPOSALS, NEVER MUTATIONS - cascade() writes only the review pass
     (cascade_queue.jsonl, status pending) and the receipt ledger (cascades.jsonl,
     chained cascade_id); the invariant registry is byte-identical before and after,
     in every mode, including when routes are escalate;
  3. EDGES ARE DETERMINISTIC - declared edges (declare_depends_on) validate against the
     registry (unknown parent, self-edge: all-or-nothing reject); mined edges
     (mine_depends_on) are 16-hex hash citations + substring derivations only.

Every test runs against a tmp_path world (registry/seals/noise/explore/cascade paths all
redirected; fact_bus.publish_fact and destructive_receipt.record stubbed) - the live
memory/percolator/invariants.json is never touched, same discipline as
tests/test_percolator_z15.py.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from mag import percolator

PARENT = "aaaaaaaaaaaaaaaa"          # 16-hex synthetic canonical keys
CHILD = "bbbbbbbbbbbbbbbb"
GRAND = "cccccccccccccccc"
CYA = "dddddddddddddddd"
CYB = "eeeeeeeeeeeeeeee"
CITED = "0123456789abcdef"


def _iso_row(text: str, count: int = 3, **kw) -> dict:
    row = {"text": text, "count": count, "first_seen": "2026-10-01T00:00:00Z",
           "domain": "test", "last_seen": "2026-10-02T00:00:00Z",
           "decay_as_of": "2026-10-02T00:00:00Z", "cycle_hits": {}}
    row.update(kw)
    return row


@pytest.fixture
def world(tmp_path, monkeypatch):
    """Isolated percolator world; restores every patched module path on teardown."""
    monkeypatch.setattr(percolator, "INVARIANT_REGISTRY", tmp_path / "invariants.json")
    monkeypatch.setattr(percolator, "SEALS_DIR", tmp_path / "seals")
    monkeypatch.setattr(percolator, "NOISE_DIR", tmp_path / "noise")
    monkeypatch.setattr(percolator, "EXPLORE_QUEUE", tmp_path / "explore.jsonl")
    monkeypatch.setattr(percolator, "PERCOLATOR_CFG", tmp_path / "percolator.json")
    monkeypatch.setattr(percolator, "CASCADE_QUEUE", tmp_path / "cascade_queue.jsonl")
    monkeypatch.setattr(percolator, "CASCADES_LEDGER", tmp_path / "cascades.jsonl")
    monkeypatch.setattr(percolator, "_cfg_cache",
                        {"mtime": None, "data": dict(percolator._CFG_DEFAULTS)})
    # keep the live tree byte-still: no facts, no destructive-receipt ledger rows
    monkeypatch.setattr("mag.fact_bus.publish_fact",
                        lambda *a, **k: {"ok": True, "stub": True})
    monkeypatch.setattr("mag.destructive_receipt.record",
                        lambda *a, **k: {"ok": True, "stub": True})
    return tmp_path


def _write_registry(tmp_path: Path, invs: dict, false_positives: int = 0) -> None:
    (tmp_path / "invariants.json").write_text(
        json.dumps({"invariants": invs, "false_positives": false_positives}, ensure_ascii=False),
        encoding="utf-8")


def _read_registry(tmp_path: Path) -> dict:
    return json.loads((tmp_path / "invariants.json").read_text(encoding="utf-8"))


def _dep(key: str) -> dict:
    return {"kind": "invariant", "key": key}


# ── law 2 first: the cascade must never mutate the registry ──────────────────

def test_cascade_fires_on_dependency_change(world):
    """THE finish-line proof: a parent count change cascades a proposal to the dependent."""
    _write_registry(world, {
        PARENT: _iso_row("parent law text", count=5),
        CHILD: _iso_row("child law text", count=2, depends_on=[_dep(PARENT)]),
    })
    res = percolator.cascade(PARENT, change={"kind": "count-decay", "old": 5, "new": 2})
    assert res["ok"] is True
    assert res["route"] == "refresh"
    assert res["impacted"] == 1
    assert res["depths"] == [1]
    prop = res["proposals"][0]
    assert prop["key"] == CHILD
    assert prop["depth"] == 1
    assert prop["route"] == "refresh"
    assert prop["components"]["parent_count"] == 5
    # the proposal landed in the review pass, pending, never promoted
    queue = [json.loads(l) for l in (world / "cascade_queue.jsonl").read_text(
        encoding="utf-8").splitlines() if l.strip()]
    assert len(queue) == 1
    assert queue[0]["status"] == "pending"
    assert queue[0]["promoted"] is False
    assert queue[0]["key"] == CHILD
    assert queue[0]["route"] == "refresh"
    # the receipt ledger carries the chained cascade receipt
    ledger = [json.loads(l) for l in (world / "cascades.jsonl").read_text(
        encoding="utf-8").splitlines() if l.strip()]
    assert len(ledger) == 1
    assert ledger[0]["schema"] == "invariant_cascade.v1"
    assert ledger[0]["cascade_id"] == res["cascade_id"]
    assert ledger[0]["prev_cascade_id"] == ""
    assert ledger[0]["origin"]["key"] == PARENT
    assert ledger[0]["routes"] == {"refresh": 1, "escalate": 0}


def test_cascade_never_mutates_registry(world):
    """PROPOSALS, NEVER MUTATIONS: registry bytes identical before/after, escalate included."""
    before = {
        PARENT: _iso_row("parent law text", count=5),
        CHILD: _iso_row("child law text", count=2, depends_on=[_dep(PARENT)]),
    }
    _write_registry(world, before)
    raw_before = (world / "invariants.json").read_bytes()
    for kwargs in ({"change": {"kind": "count-decay", "old": 5, "new": 2}},
                   {"change": {"kind": "removed"}},
                   {}):
        res = percolator.cascade(PARENT, write=True, **kwargs)
        assert res["ok"] is True
    assert (world / "invariants.json").read_bytes() == raw_before
    after = _read_registry(world)["invariants"]
    assert after[CHILD]["depends_on"] == [_dep(PARENT)]   # edge intact, untouched
    assert after[CHILD]["count"] == 2                     # count untouched
    assert "cascaded_at" not in after[CHILD]              # no annotation mutation


def test_cascade_escalates_when_parent_removed(world):
    """A removed/expired parent breaks the dependent's premise: escalate proposals."""
    _write_registry(world, {
        CHILD: _iso_row("child law text", count=2, depends_on=[_dep(PARENT)]),
    })
    res = percolator.cascade(PARENT)  # origin absent from the registry = removed
    assert res["route"] == "escalate"
    assert res["kind"] == "removed"
    assert res["proposals"][0]["route"] == "escalate"
    res2 = percolator.cascade(PARENT, change={"kind": "superseded"}, write=False)
    assert res2["route"] == "escalate"
    res3 = percolator.cascade(CHILD, change={"kind": "expired"}, write=False)
    # origin present but explicitly expired: escalate, and CHILD has no dependents
    assert res3["route"] == "escalate"
    assert res3["impacted"] == 0


def test_cascade_bfs_is_transitive(world):
    """Grandchildren cascade: PARENT -> CHILD -> GRAND, shallowest first."""
    _write_registry(world, {
        PARENT: _iso_row("parent", count=9),
        CHILD: _iso_row("child", depends_on=[_dep(PARENT)]),
        GRAND: _iso_row("grand", depends_on=[_dep(CHILD)]),
    })
    res = percolator.cascade(PARENT, change={"kind": "reinforced"})
    assert res["impacted"] == 2
    assert res["depths"] == [1, 2]
    assert [p["key"] for p in res["proposals"]] == [CHILD, GRAND]


def test_cascade_cycle_guard_terminates(world):
    """A depends_on B, B depends_on A: the visited set breaks the cycle, walk terminates."""
    _write_registry(world, {
        CYA: _iso_row("cycle a", depends_on=[_dep(CYB)]),
        CYB: _iso_row("cycle b", depends_on=[_dep(CYA)]),
    })
    res = percolator.cascade(CYA, change={"kind": "count-decay"})
    assert res["ok"] is True
    assert res["impacted"] == 1
    assert [p["key"] for p in res["proposals"]] == [CYB]


def test_cascade_respects_max_depth(world):
    _write_registry(world, {
        PARENT: _iso_row("parent"),
        CHILD: _iso_row("child", depends_on=[_dep(PARENT)]),
        GRAND: _iso_row("grand", depends_on=[_dep(CHILD)]),
    })
    res = percolator.cascade(PARENT, max_depth=1, write=False)
    assert res["impacted"] == 1
    assert res["proposals"][0]["key"] == CHILD


def test_cascade_respects_max_nodes(world):
    _write_registry(world, {
        PARENT: _iso_row("parent"),
        CHILD: _iso_row("child", depends_on=[_dep(PARENT)]),
        GRAND: _iso_row("grand", depends_on=[_dep(PARENT)]),
    })
    res = percolator.cascade(PARENT, max_nodes=2, write=False)  # origin + 1 dependent
    assert res["impacted"] == 1
    assert res["truncated"] is True


def test_cascade_write_false_is_pure(world):
    """write=False mints nothing: no queue, no ledger, no registry write."""
    _write_registry(world, {PARENT: _iso_row("parent"),
                            CHILD: _iso_row("child", depends_on=[_dep(PARENT)])})
    res = percolator.cascade(PARENT, write=False)
    assert res["impacted"] == 1 and res["write"] is False
    assert not (world / "cascade_queue.jsonl").exists()
    assert not (world / "cascades.jsonl").exists()


def test_cascade_chains_prev_cascade_id(world):
    """The receipt ledger hash-links: cascade 2 carries cascade 1's id as prev."""
    _write_registry(world, {PARENT: _iso_row("parent"),
                            CHILD: _iso_row("child", depends_on=[_dep(PARENT)])})
    r1 = percolator.cascade(PARENT, change={"kind": "count-decay", "old": 3, "new": 2})
    r2 = percolator.cascade(PARENT, change={"kind": "reinforced"})
    assert r1["prev_cascade_id"] == ""
    assert r2["prev_cascade_id"] == r1["cascade_id"]
    assert r2["cascade_id"] != r1["cascade_id"]


# ── edges: declared (fold time) and mined (retroactive, deterministic) ───────

def test_declare_depends_on_validates_and_merges(world):
    _write_registry(world, {PARENT: _iso_row("parent"),
                            CHILD: _iso_row("child")})
    res = percolator.declare_depends_on(CHILD, [PARENT])
    assert res["ok"] is True and res["added"] == [PARENT]
    assert _read_registry(world)["invariants"][CHILD]["depends_on"] == [_dep(PARENT)]
    # idempotent: re-declaring the same parent adds nothing
    res2 = percolator.declare_depends_on(CHILD, [PARENT])
    assert res2["ok"] is True and res2["added"] == []
    # unknown parent: all-or-nothing reject, registry untouched
    raw_before = (world / "invariants.json").read_bytes()
    bad = percolator.declare_depends_on(CHILD, ["ffffffffffffffff"])
    assert bad["ok"] is False and "unknown parent" in bad["error"]
    assert (world / "invariants.json").read_bytes() == raw_before
    # self-edge rejected
    assert percolator.declare_depends_on(CHILD, [CHILD])["ok"] is False


def test_mine_depends_on_hash_citation_and_substring(world):
    _write_registry(world, {
        CITED: _iso_row("anchor law"),                       # cited by 16-hex hash
        "1111111111111111": _iso_row(f"law {CITED} anchored"),  # hash citation
        "2222222222222222": _iso_row("5x identical run_python calls"),   # container
        "3333333333333333": _iso_row("5x identical run_python"),          # embedded child
    })
    rep = percolator.mine_depends_on(apply=False)
    assert rep["ok"] is True and rep["mode"] == "report"
    assert rep["edges"]["1111111111111111"] == [CITED]           # cites the anchor hash
    assert rep["edges"]["2222222222222222"] == ["3333333333333333"]  # contains the child text
    # report mode wrote nothing
    assert (world / "invariants.json").read_text(encoding="utf-8") == (
        world / "invariants.json").read_text(encoding="utf-8")
    app = percolator.mine_depends_on(apply=True)
    assert app["ok"] is True and app["mode"] == "apply"
    assert app["n_edges"] == 2
    reg = _read_registry(world)
    assert reg["invariants"]["1111111111111111"]["depends_on"] == [_dep(CITED)]
    assert reg["invariants"]["2222222222222222"]["depends_on"] == [_dep("3333333333333333")]
    # edge-free rows still carry the key
    assert reg["invariants"][CITED]["depends_on"] == []
    # counts and text untouched by the mining apply
    assert reg["invariants"][CITED]["count"] == 3
    assert reg["invariants"][CITED]["text"] == "anchor law"
    # pre-edit backup landed next to the registry
    assert (world / "invariants.json.bak-cascade-20261003").is_file() or \
        list(world.glob("invariants.json.bak-cascade-*"))


def test_cascade_reads_mined_edges(world):
    """End to end: mine edges, then the cascade fires over the mined graph."""
    _write_registry(world, {
        "2222222222222222": _iso_row("5x identical run_python calls"),
        "3333333333333333": _iso_row("5x identical run_python"),
    })
    percolator.mine_depends_on(apply=True)
    res = percolator.cascade("3333333333333333", change={"kind": "removed"})
    assert res["route"] == "escalate"
    assert res["impacted"] == 1
    assert res["proposals"][0]["key"] == "2222222222222222"
