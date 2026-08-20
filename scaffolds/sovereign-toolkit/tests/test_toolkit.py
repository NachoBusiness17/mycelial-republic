"""Tests for the sovereign-toolkit crown jewels (pure stdlib, no deps)."""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import memlance
import stateless_boot
import verkle_knot
import ghost_pylance
import memweave


# ---------------------------------------------------------------- stateless_boot
def test_frozen_prefix_is_deterministic():
    a = stateless_boot.build_frozen_prefix(
        tools=["fetch(url)"], interfaces=["queue"], live_truth=["hit 98%"])
    b = stateless_boot.build_frozen_prefix(
        tools=["fetch(url)"], interfaces=["queue"], live_truth=["hit 98%"])
    assert a == b


def test_spawn_spec_has_no_persona_no_history():
    s = stateless_boot.spawn_spec(goal="x", tools=["t"], interfaces=["i"],
                                  live_truth=["f"])
    assert s["has_persona"] is False
    assert s["has_history"] is False
    assert s["frozen_prefix_sha"]


def test_frozen_prefix_contains_tools_and_live_truth():
    p = stateless_boot.build_frozen_prefix(
        tools=["fetch(url)"], interfaces=["queue + drainer"],
        live_truth=["cache hit rate 98%"])
    assert "fetch(url)" in p
    assert "queue + drainer" in p
    assert "cache hit rate 98%" in p


# ---------------------------------------------------------------- memlance
def test_grounding_verdict_verified_vs_unverified():
    assert memlance.grounding_verdict("measured 98% hit against the real bill")["verified"] is True
    assert memlance.grounding_verdict("this is an unverified estimate")["verified"] is False
    assert memlance.grounding_verdict("plain sentence")["verified"] is False


def test_explicit_unverified_dominates_generic_marker():
    # a generic marker is overridden by an explicit unverified marker
    v = memlance.grounding_verdict("confirmed approach, but this remains an unmeasured estimate")
    assert v["verified"] is False


def test_index_and_select_grounded():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "note.md"
        p.write_text("# cache economics\nMeasured 98% hit, verified against the bill.\n",
                     encoding="utf-8")
        idx = memlance.index([("mem", str(p))])
        assert len(idx) == 1
        assert idx[0]["verified"] is True
        sel = memlance.select("cache economics", idx, top_k=1)
        assert sel and sel[0]["path"] == str(p)


def test_select_only_returns_relevant():
    with tempfile.TemporaryDirectory() as d:
        rel = Path(d) / "rel.md"; rel.write_text("# cache economics\nverified.\n", encoding="utf-8")
        irr = Path(d) / "irr.md"; irr.write_text("# gardening\nmeasured.\n", encoding="utf-8")
        idx = memlance.index([("mem", str(d))])
        sel = memlance.select("cache economics", idx, top_k=5)
        paths = [e["path"] for e in sel]
        assert str(rel) in paths
        assert str(irr) not in paths


# ---------------------------------------------------------------- verkle_knot
def test_chain_append_and_verify():
    with tempfile.TemporaryDirectory() as d:
        c = verkle_knot.VerkleChain(d)
        c.append({"event": "birth"}, theme="stateless", session_id="abc12345")
        c.append({"event": "first_learn"}, theme="learn", session_id="abc12345")
        rows = c.replay()
        assert len(rows) == 2
        # parent link chains
        assert rows[0]["parent_verkle_root"] is None
        assert rows[1]["parent_verkle_root"] == rows[0]["verkle_root"]
        # verify passes on a clean chain
        assert c.verify()["ok"] is True


def test_chain_tamper_detected():
    with tempfile.TemporaryDirectory() as d:
        c = verkle_knot.VerkleChain(d)
        c.append({"event": "birth"}, theme="stateless", session_id="abc12345")
        c.append({"event": "second"}, theme="learn", session_id="abc12345")
        # tamper with the chain (rewrite a row's root)
        path = Path(d) / "verkle_chain.jsonl"
        lines = path.read_text(encoding="utf-8").splitlines()
        row = json.loads(lines[1])
        row["verkle_root"] = "0" * 64
        path.write_text(json.dumps(row, sort_keys=True) + "\n" + lines[0] + "\n",
                        encoding="utf-8")
        v = c.verify()
        assert v["ok"] is False


def test_leaf_hash_is_content_addressed():
    a = verkle_knot.leaf_hash({"x": 1})
    b = verkle_knot.leaf_hash({"x": 1})
    c = verkle_knot.leaf_hash({"x": 2})
    assert a == b
    assert a != c


# ---------------------------------------------------------------- ghost_pylance
def test_ghost_diagnose_undefined_name():
    r = ghost_pylance.diagnose(
        "import os\ndef f():\n    return missing_name\n")
    assert r["ok"] is True
    assert "missing_name" in r["undefined"]


def test_ghost_diagnose_clean_module():
    r = ghost_pylance.diagnose(
        "import os\ndef f(x):\n    return os.getcwd() + str(x)\n")
    assert r["ok"] is True
    assert r["undefined"] == []
    assert r["unused_imports"] == []  # os is used


def test_ghost_diagnose_unused_import():
    r = ghost_pylance.diagnose("import math\nx = 1\n")
    assert any(i["name"] == "math" for i in r["unused_imports"])


def test_ghost_diagnose_syntax_error():
    r = ghost_pylance.diagnose("def broken(:\n")
    assert r["ok"] is False
    assert r["syntax_error"] is not None


def test_ghost_symbols_and_self_check():
    syms = ghost_pylance.symbols("def a():\n    pass\nclass B:\n    pass\n")
    kinds = {s["name"]: s["kind"] for s in syms}
    assert kinds["a"] == "function"
    assert kinds["B"] == "class"
    with tempfile.TemporaryDirectory() as d:
        good = Path(d) / "good.py"; good.write_text("x = 1\n", encoding="utf-8")
        bad = Path(d) / "bad.py"; bad.write_text("def broken(:\n", encoding="utf-8")
        sc = ghost_pylance.self_check([str(good), str(bad)])
        assert sc["total"] == 2
        assert sc["clean"] == 1
        assert sc["ok"] is False


# ---------------------------------------------------------------- memweave
def test_memweave_decompose_is_deterministic():
    a = memweave.decompose("route the heavy reasoning to the frontier", 3)
    b = memweave.decompose("route the heavy reasoning to the frontier", 3)
    assert a == b
    assert len(a) == 3


def test_memweave_independent_agreement_is_strong():
    # two genuinely different phrasings -> independent, strong consensus
    q = memweave.consensus_quality([
        "send the heavy reasoning to the frontier model and keep routine local",
        "expensive frontier reasoning goes remote while cheap routine work stays local",
    ])
    assert q["n_independent"] == 2
    assert q["verdict"] == "strong"


def test_memweave_correlated_answers_collapse_to_one():
    # a near-copy of the first answer is NOT an independent witness
    q = memweave.consensus_quality([
        "route heavy reasoning to the frontier model and keep the routine load local",
        "route heavy reasoning to the frontier model and keep the routine load local",
        "keep the heavy reasoning on the frontier and run the routine load locally",
    ])
    # two independent, but the duplicate is correlated -> n_independent == 2
    assert q["n_independent"] == 2
    assert q["n_answers"] == 3


def test_memweave_consensus_illusion_flagged():
    # THREE identical answers: one opinion masquerading as three -> correlated_weak
    q = memweave.consensus_quality(["alpha beta gamma"] * 3)
    assert q["n_independent"] == 1
    assert q["verdict"] == "correlated_weak"
    assert q["correlated"] is True


def test_memweave_weave_returns_consensus():
    answers = ["keep heavy reasoning on the frontier and routine local"] * 2
    w = memweave.weave(answers)
    assert w["verdict"] == "correlated_weak"
    assert w["consensus"] == answers[0]
    assert w["n_independent"] == 1
