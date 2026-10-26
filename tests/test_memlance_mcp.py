"""Memlance wire tripwires (P4, 2026-10-07): plant/witness/tally in
tools/mesh_delta.py's mcp mode.

Under test: plant stores one lance as a content-addressed chunk under
memory/mesh/lances/ ({aim, seed, planted_ts}; sha256 of the payload is the
seed_id); witness checks a target surface (chan row, context-pack source)
for unprompted citation and banks hit_ts + latency in the lances ledger;
tally reports per-seed hit rates. Fences under test: seed_id must be the
64-hex sha of a planted chunk (traversal refused), the chunk must pass its
own sha on read (tamper refused), and a witness surface must resolve inside
the repo fence (escape refused). All paths are sandboxed to tmp_path via
monkeypatched module globals; nothing here touches the real memory tree.
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import mesh_delta  # noqa: E402


@pytest.fixture()
def lance_repo(tmp_path, monkeypatch):
    """A fake repo root with the real layout: memory/mesh/lances under it.
    ROOT, MEMORY, LANCES, the ledger and the witness fence all point here,
    so read_chunk's memory-root fence is exercised for real."""
    repo = tmp_path / "repo"
    (repo / "memory" / "mesh" / "lances").mkdir(parents=True)
    monkeypatch.setattr(mesh_delta, "ROOT", repo)
    monkeypatch.setattr(mesh_delta, "MEMORY", repo / "memory")
    monkeypatch.setattr(mesh_delta, "WITNESS_FENCE", repo)
    monkeypatch.setattr(mesh_delta, "LANCES",
                        repo / "memory" / "mesh" / "lances")
    monkeypatch.setattr(mesh_delta, "LANCES_LEDGER",
                        repo / "memory" / "mesh" / "lances"
                        / "lances_ledger.jsonl")
    return repo


def _rpc(lines: list[str]) -> list[dict]:
    """Drive the real mcp_loop over a synthetic stdio session."""
    inp = io.StringIO("\n".join(lines) + "\n")
    out = io.StringIO()
    with patch.object(sys, "stdin", inp), patch.object(sys, "stdout", out):
        assert mesh_delta.mcp_loop() == 0
    return [json.loads(l) for l in out.getvalue().splitlines() if l.strip()]


def test_mcp_tools_list_shows_the_three_tools():
    replies = _rpc([
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"}),
        json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}),
    ])
    names = [t["name"] for t in json.loads(
        replies[1]["result"]["content"][0]["text"])["tools"]]
    for tool in ("picture", "delta", "fetch", "plant", "witness", "tally"):
        assert tool in names, "missing mcp tool: " + tool


def test_mcp_plant_round_trip_through_tools_call(lance_repo):
    replies = _rpc([
        json.dumps({"jsonrpc": "2.0", "id": 7, "method": "tools/call",
                    "params": {"name": "plant", "arguments": {
                        "aim": "the elder lane's next window",
                        "seed": "tally rides the picture"}}}),
    ])
    r = json.loads(replies[0]["result"]["content"][0]["text"])
    assert "seed_id" in r, "plant via tools/call must return a seed_id"
    chunk = lance_repo / "memory" / "mesh" / "lances" / (r["seed_id"]
                                                         + ".json")
    assert chunk.is_file()
    payload = json.loads(chunk.read_text(encoding="utf-8"))
    assert payload["aim"] == "the elder lane's next window"
    assert payload["seed"] == "tally rides the picture"
    assert payload["planted_ts"].endswith("Z")
    # the fetched seed_id equals the sha256 of the landed bytes
    import hashlib
    assert hashlib.sha256(chunk.read_bytes()).hexdigest() == r["seed_id"]


def test_plant_fetch_round_trip_via_chunk_door(lance_repo):
    r = mesh_delta.plant("aim at the night lane", "the seed text itself")
    assert r["dedup"] is False
    body = mesh_delta.read_chunk("memory/mesh/lances/" + r["seed_id"]
                                 + ".json", r["seed_id"])
    assert body is not None, "the chunk door must serve a planted lance"
    payload = json.loads(body.decode("utf-8"))
    assert payload["aim"] == "aim at the night lane"
    assert payload["seed"] == "the seed text itself"
    assert payload["planted_ts"].endswith("Z")
    # sha mismatch on the same path is refused by the shared chunk fence
    assert mesh_delta.read_chunk("memory/mesh/lances/" + r["seed_id"]
                                 + ".json", "0" * 64) is None


def test_witness_hit_banks_hit_ts_and_latency(lance_repo):
    r = mesh_delta.plant("aim at the bard lane", "greatest hit seed text")
    surf = lance_repo / "chan_row.md"
    surf.write_text("unprompted chatter quoting: GREATEST HIT SEED TEXT done",
                    encoding="utf-8")
    w = mesh_delta.witness(r["seed_id"], "chan_row.md")
    assert w["hit"] is True
    assert w["hit_ts"] == w["ts"]
    assert w["latency_s"] is not None and w["latency_s"] >= 0
    assert w["surface"] == "chan_row.md"


def test_witness_miss_has_no_hit_ts(lance_repo):
    r = mesh_delta.plant("aim", "a very distinctive seed phrase")
    surf = lance_repo / "quiet.md"
    surf.write_text("nothing here", encoding="utf-8")
    w = mesh_delta.witness(r["seed_id"], "quiet.md")
    assert w["hit"] is False
    assert "hit_ts" not in w
    assert w["latency_s"] is not None


def test_witness_partial_needle(lance_repo):
    r = mesh_delta.plant("aim", "full seed body with a UNIQUEMARK inside")
    surf = lance_repo / "partial.md"
    surf.write_text("...cites UNIQUEMARK only...", encoding="utf-8")
    w = mesh_delta.witness(r["seed_id"], "partial.md", needle="UNIQUEMARK")
    assert w["hit"] is True and w["needle"] == "UNIQUEMARK"


def test_tally_math_per_seed(lance_repo):
    a = mesh_delta.plant("aim a", "seed alpha text")
    b = mesh_delta.plant("aim b", "seed beta text")
    surf = lance_repo / "chan.md"
    surf.write_text("row cites seed alpha text verbatim", encoding="utf-8")
    mesh_delta.witness(a["seed_id"], "chan.md")   # hit
    mesh_delta.witness(a["seed_id"], "chan.md")   # hit again
    mesh_delta.witness(b["seed_id"], "chan.md")   # miss
    t = mesh_delta.tally()
    assert t["lances"] == 2
    per = {p["seed_id"]: p for p in t["per_seed"]}
    assert per[a["seed_id"]]["plants"] == 1
    assert per[a["seed_id"]]["witnesses"] == 2
    assert per[a["seed_id"]]["hits"] == 2
    assert per[a["seed_id"]]["hit_rate"] == 1.0
    assert per[b["seed_id"]]["hits"] == 0
    assert per[b["seed_id"]]["hit_rate"] == 0.0
    assert t["overall"] == {"witnesses": 3, "hits": 2, "hit_rate": 0.6667}


def test_tally_empty_ledger(lance_repo):
    t = mesh_delta.tally()
    assert t == {"lances": 0, "per_seed": [],
                 "overall": {"witnesses": 0, "hits": 0, "hit_rate": None}}


def test_path_fence_seed_id_traversal_refused(lance_repo):
    for bad in ("../../etc/passwd", "." + "a" * 63, "Z" * 64,
                "a" * 63, ""):
        w = mesh_delta.witness(bad, "any.md")
        assert "refused" in w["error"], "seed_id fence let through: " + bad


def test_path_fence_surface_outside_repo_refused(lance_repo):
    r = mesh_delta.plant("aim", "seed")
    outside = lance_repo.parent / "outside.txt"
    outside.write_text("seed", encoding="utf-8")  # a real file, outside fence
    w = mesh_delta.witness(r["seed_id"], "../outside.txt")
    assert "outside the witness fence" in w["error"]
    w2 = mesh_delta.witness(r["seed_id"], str(outside))
    assert "outside the witness fence" in w2["error"]


def test_tampered_lance_chunk_refused(lance_repo):
    r = mesh_delta.plant("aim", "honest seed")
    chunk = lance_repo / "memory" / "mesh" / "lances" / (r["seed_id"]
                                                         + ".json")
    payload = json.loads(chunk.read_text(encoding="utf-8"))
    payload["seed"] = "forged seed"
    chunk.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    w = mesh_delta.witness(r["seed_id"], "chan.md")
    assert "sha" in w["error"] and "refused" in w["error"]


def test_plant_refuses_empty_aim_or_seed():
    assert "refused" in mesh_delta.plant("", "seed")["error"]
    assert "refused" in mesh_delta.plant("aim", "")["error"]


def test_witness_unknown_seed_id_refused(lance_repo):
    w = mesh_delta.witness("a" * 64, "chan.md")
    assert "refused" in w["error"] and "64-hex sha" in w["error"]
