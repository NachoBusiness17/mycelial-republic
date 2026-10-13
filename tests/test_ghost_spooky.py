"""Verify ghost_spooky is wired into every ghost_talk reply (long-standing per-prompt loop)."""
import json
from mag.ghost_talk import reply
from mag.ghost_spooky import probe, all_abilities, CATALOG


def test_spooky_always_in_reply():
    d = reply("what is the queue state")
    assert d.get("spooky"), "every ghost reply must carry a spooky block"
    sp = d["spooky"]
    assert sp.get("line"), "spooky block must have a human line"
    assert sp.get("levers"), "spooky block must list ghost's ability levers"
    # sense + fold are always present (ghost always senses, always learns)
    ids = [a["id"] for a in sp["levers"]]
    assert "sense" in ids and "fold" in ids


def test_spooky_tailors_levers_to_prompt():
    d = probe("rightsize the queue and clean up old tools")
    ids = [a["id"] for a in d["levers"]]
    assert "rightsize" in ids, "prompt about rightsizing should pull the rightsize lever"
    assert "retire" in ids, "prompt about cleaning old tools should pull the retire lever"


def test_catalog_complete():
    a = all_abilities()
    assert a["levers"], "catalog must be non-empty"
    assert len(a["levers"]) == len(CATALOG)


def test_probe_does_not_raise():
    r = probe("")
    assert r["count"] >= 2  # always sense + fold


def test_probe_carries_real_verkle_proof():
    r = probe("status")
    pr = r.get("prove") or {}
    assert pr.get("pointer", "").startswith("knot/"), "prove block must carry a knot pointer"
    assert pr.get("invariant"), "prove block must show the reconstruction invariant"
    assert pr.get("verified") is True, "the reconstruction must verify against the chain tip"
