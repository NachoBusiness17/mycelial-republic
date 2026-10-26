"""Mesh v2 tests - the salon verdict as executable law (2026-10-05).

Verdicts under test: per-writer signed feeds with merged room view; signatures prove
WHO and the chain proves WHAT; knot-before-rows; tamper detection at both layers;
broker provenance refusal with logged reasons; knot-at-every-commit; rate law;
the door's freshness header + named recall floor.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from mag.mesh import broker, door, feeds, knot

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def mesh_root(tmp_path):
    knot.seal(tmp_path)  # the knot-before-rows law: chain exists before any row
    return tmp_path


def test_two_writers_merged_room(mesh_root):
    feeds.append(mesh_root, "alpha", "say", {"msg": "first"})
    feeds.append(mesh_root, "beta", "say", {"msg": "second"})
    feeds.append(mesh_root, "alpha", "say", {"msg": "third"})
    room = feeds.room_view(mesh_root)
    assert room["ok"] and len(room["rows"]) == 3
    assert [r["body"]["msg"] for r in room["rows"]] == ["first", "second", "third"]
    assert feeds.verify_feed(mesh_root, "alpha")["ok"]
    assert feeds.verify_feed(mesh_root, "beta")["ok"]


def test_tampered_row_fails_signature(mesh_root):
    feeds.append(mesh_root, "alpha", "say", {"msg": "honest"})
    feedf = mesh_root / "feeds" / "alpha.jsonl"
    row = json.loads(feedf.read_text().splitlines()[0])
    row["body"]["msg"] = "forged"  # edit history: the sed -i attack
    feedf.write_text(json.dumps(row, sort_keys=True) + "\n")
    v = feeds.verify_feed(mesh_root, "alpha")
    assert not v["ok"] and v["violations"] and "signature" in v["violations"][0]["why"]


def test_knot_covers_then_names_unsealed(mesh_root):
    feeds.append(mesh_root, "alpha", "say", {"msg": "sealed row"})
    knot.seal(mesh_root)
    v = knot.verify_chain(mesh_root)
    assert v["ok"] and v["unsealed_leaves"] == 0
    feeds.append(mesh_root, "beta", "say", {"msg": "new row"})
    v2 = knot.verify_chain(mesh_root)
    assert v2["ok"] and v2["unsealed_leaves"] == 1  # named, not hidden
    knot.seal(mesh_root)
    assert knot.verify_chain(mesh_root)["unsealed_leaves"] == 0


def test_chain_tamper_detected(mesh_root):
    feeds.append(mesh_root, "alpha", "say", {"msg": "x"})
    knot.seal(mesh_root)
    chainf = mesh_root / "chain.jsonl"
    k = json.loads(chainf.read_text().splitlines()[0])
    k["merkle"] = "0" * 64  # forge the root
    chainf.write_text(json.dumps(k, sort_keys=True) + "\n")
    v = knot.verify_chain(mesh_root)
    assert not v["ok"] and any("tamper" in x["why"] for x in v["violations"])


def test_broker_refuses_unresolvable_provenance(mesh_root):
    p = broker.propose(mesh_root, "alpha", "claim", {"x": 1},
                       source_hashes=["f" * 64])
    assert p["ok"]
    out = broker.adjudicate(mesh_root, p["proposal_hash"], accept=True)
    assert out["decision"] == "refuse"
    assert any("not in library" in r for r in out["reasons"])
    refs = broker.refusals(mesh_root)
    assert refs and refs[-1]["reasons"]  # the refusal log law


def test_broker_accepts_and_cuts_knot(mesh_root):
    src = broker.put_blob(mesh_root, b"primary source bytes", note="the source")
    before = len((mesh_root / "chain.jsonl").read_text().splitlines())
    p = broker.propose(mesh_root, "alpha", "claim", {"x": 1},
                       source_hashes=[src["hash"]])
    out = broker.adjudicate(mesh_root, p["proposal_hash"], accept=True)
    assert out["decision"] == "accept" and out["effect_hash"]
    after = len((mesh_root / "chain.jsonl").read_text().splitlines())
    assert after > before  # knot-at-every-broker-commit law


def test_broker_refuses_missing_supersedes(mesh_root):
    p = broker.propose(mesh_root, "alpha", "claim", {"x": 1}, supersedes=["a" * 64])
    out = broker.adjudicate(mesh_root, p["proposal_hash"], accept=True)
    assert out["decision"] == "refuse"
    assert any("supersedes" in r for r in out["reasons"])


def test_rate_law_refuses_burst(mesh_root):
    refused = 0
    for i in range(feeds.RATE_PER_MIN + 6):
        if not feeds.append(mesh_root, "spammer", "say", {"i": i})["ok"]:
            refused += 1
    assert refused >= 5


def test_door_freshness_and_recall_floor(mesh_root):
    broker.put_blob(mesh_root, b"babel fish notes", note="babel fish notes")
    broker.rebuild_index(mesh_root)
    out = door.call(mesh_root, "search", {"query": "babel"})
    assert out["ok"] and len(out["hits"]) == 1
    assert "corpus_tip_hash" in out["freshness"] and "frozen" in out["freshness"]
    assert "invisible" in out["recall_floor"]  # the recall floor is NAMED


def test_door_get_and_propose(mesh_root):
    b = broker.put_blob(mesh_root, b"payload", note="p")
    got = door.call(mesh_root, "get_by_hash", {"hash": b["hash"]})
    assert got["ok"] and got["data"] == "payload"
    prop = door.call(mesh_root, "propose_write",
                     {"writer": "alpha", "kind": "note", "body": {"q": 1}})
    assert prop["ok"] and prop["status"] == "open"  # the door never commits


def test_door_stdio_roundtrip(mesh_root):
    broker.put_blob(mesh_root, b"stdio payload", note="stdio payload")
    broker.rebuild_index(mesh_root)
    reqs = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    call = {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
            "params": {"name": "search", "arguments": {"query": "stdio"}}}
    proc = subprocess.run(
        [str(ROOT / ".venv" / "Scripts" / "python.exe"), "-m", "mag.mesh.door",
         str(mesh_root)],
        input="\n".join(json.dumps(r) for r in (reqs, call)) + "\n",
        capture_output=True, text=True, cwd=str(ROOT), timeout=120)
    lines = [json.loads(x) for x in proc.stdout.splitlines() if x.strip()]
    assert len(lines) == 2
    assert lines[0]["result"]["tools"][0]["name"] == "search"
    assert len(lines[1]["result"]["hits"]) == 1
