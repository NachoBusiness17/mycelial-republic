"""Tests for the sovereign-toolkit crown jewels (pure stdlib, no deps)."""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import memlance
import stateless_boot
import verkle_knot


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
