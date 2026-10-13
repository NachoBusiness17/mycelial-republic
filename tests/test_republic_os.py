"""Tests for the persistent mycelial-republic OS (mycelium Phase 1 + republic_os Phases 2-5).

Isolated: monkeypatch the module-level store paths to tmp_path so tests never touch the
real memory/mycelium graph or republic locks/state.
"""
import mag.mycelium as mc
import mag.republic_os as ros


def _iso(monkeypatch, tmp_path):
    """Isolate mycelium + republic_os stores to tmp."""
    monkeypatch.setattr(mc, "NODES", tmp_path / "nodes.jsonl")
    monkeypatch.setattr(mc, "EDGES", tmp_path / "edges.jsonl")
    monkeypatch.setattr(mc, "SNAPSHOT", tmp_path / "snapshot.json")
    monkeypatch.setattr(ros, "STATE", tmp_path / "state.json")
    monkeypatch.setattr(ros, "LOCKS", tmp_path / "locks.json")


# --------------------------------------------------------------- mycelium ----
def test_salience_rises_with_reinforce_and_falls_on_contradict(monkeypatch, tmp_path):
    _iso(monkeypatch, tmp_path)
    a = mc.add_node("ghost", ntype="seat", trust=0.7)
    b = mc.add_node("artifact", ntype="artifact")
    mc.link(a["id"], b["id"], etype="handoff", protected=True)
    r = mc.reinforce(a["id"], b["id"], etype="handoff", reward=1.0, consumed=True)
    assert r["ok"]
    assert r["edge"]["refs_in"] == 1  # consumption recorded
    high = r["salience"]
    assert high > 0.5
    mc.contradict(a["id"], b["id"])
    after = mc.salience(mc._load_edges()[0])
    assert after <= high  # contradiction penalty reduces salience


def test_reinforce_protected_floor(monkeypatch, tmp_path):
    _iso(monkeypatch, tmp_path)
    a = mc.add_node("a", ntype="seat")
    b = mc.add_node("b", ntype="artifact")
    mc.link(a["id"], b["id"], etype="handoff", protected=True)
    e = mc.reinforce(a["id"], b["id"], etype="handoff", reward=-5.0, cost=5.0)
    # protected edges never fall below PROTECTED_FLOOR
    assert e["edge"]["weight"] >= 0.4


def test_dual_write_and_boot_rehydrate(monkeypatch, tmp_path):
    _iso(monkeypatch, tmp_path)
    a = mc.add_node("x", ntype="concept")
    b = mc.add_node("y", ntype="artifact")
    mc.link(a["id"], b["id"], etype="related")
    mc.dual_write()
    assert (tmp_path / "snapshot.json").is_file()
    # boot rehydrates from snapshot when jsonl is gone (OS never starts from zero)
    (tmp_path / "nodes.jsonl").unlink()
    (tmp_path / "edges.jsonl").unlink()
    mc.boot()
    assert len(mc._load_nodes()) == 2
    assert len(mc._load_edges()) == 1


def test_decay_marks_low_salience_non_protected(monkeypatch, tmp_path):
    _iso(monkeypatch, tmp_path)
    a = mc.add_node("a", ntype="seat")
    b = mc.add_node("b", ntype="artifact")
    mc.link(a["id"], b["id"], etype="related", protected=False)
    d = mc.decay(threshold=1.0)  # force everything below
    assert d["ok"]
    assert any(e.get("decayed") for e in mc._load_edges())


# ------------------------------------------------------------ republic_os ----
def test_redlock_ownership(monkeypatch, tmp_path):
    _iso(monkeypatch, tmp_path)
    assert ros.own("aos_grok", owner="ghost")["ok"]
    assert not ros.own("aos_grok", owner="other")["ok"]  # locked -> conflict
    assert ros.release("aos_grok", owner="ghost")["ok"]
    # after release another owner can acquire
    assert ros.own("aos_grok", owner="other")["ok"]


def test_seed_aos_builds_nodes_and_edges(monkeypatch, tmp_path):
    _iso(monkeypatch, tmp_path)
    s = ros.seed_aos()
    assert s["ok"] and len(s["nodes"]) == 5 and len(s["edges"]) == 4


def test_round_dry_no_spend(monkeypatch, tmp_path):
    _iso(monkeypatch, tmp_path)
    ros.seed_aos()
    r = ros.round_cycle(dry=True)
    assert r["ok"] and r["action"] == "round"
    assert r["queue_size"] >= 0


def test_memory_block_renders(monkeypatch, tmp_path):
    _iso(monkeypatch, tmp_path)
    ros.seed_aos()
    mb = ros.memory_block()
    assert mb["ok"]
    assert "REPUBLIC OS MEMORY" in mb["block"]
