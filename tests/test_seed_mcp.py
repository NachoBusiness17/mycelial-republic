"""B2-181 pins: seed-mcp server mechanics (2026-09-26).

Hermetic mini-estate + seed_rib.v0 seed; exercises every seed-mcp resource and
tool through handle(), plus one real stdio subprocess round-trip. The
full-estate falsifier run lives in tools/seed_mcp_cold_client.py.
"""
from __future__ import annotations

import base64
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.seed_mcp import SeedServer, handle
from tools.seed_rib import build as seed_build

REPO = Path(__file__).resolve().parents[1]

# HEADLESS law: explicit creationflags (ratchet tests/test_headless_law.py; bare-spawn-descent 2026-09-29)
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0


@pytest.fixture()
def estate(tmp_path: Path) -> Path:
    est = tmp_path / "estate"
    (est / "memory/law").mkdir(parents=True)
    (est / "memory/briefs").mkdir(parents=True)
    (est / "docs").mkdir(parents=True)
    (est / "memory/law/registry.json").write_text(
        json.dumps({"LAW-1": {"name": "rails_over_direction", "tier": "T0"}}), encoding="utf-8")
    (est / "memory/law/LAW_TEST.md").write_text("law body\n", encoding="utf-8")
    (est / "memory/briefs/latest.md").write_text("brief\n", encoding="utf-8")
    (est / "docs/DNA.md").write_text("residual + registry + leaf\n", encoding="utf-8")
    (est / "AGENTS.md").write_text("harness rules\n" * 40, encoding="utf-8")
    return est


@pytest.fixture()
def seeded(estate: Path, tmp_path: Path):
    seed_path = tmp_path / "seed.json"
    # wave5 suite-burn (2026-09-29): pointer_list=None keeps this fixture
    # compatible with both build() generations - the in-tree B2-479 exposure-
    # scoping edit added a required 4th positional `pointer_list` (str | None,
    # "if pointer_list" guarded, None = no forced pointers = the old behavior),
    # and the positional call without it broke all 15 fixtures with
    # "build() missing 1 required positional argument: 'pointer_list'".
    seed_build(estate, ["memory/law/registry.json", "AGENTS.md"],
               ["memory/law/*.md", "memory/briefs/*.md", "docs/*.md"],
               pointer_list=None, inline_max=64, out_path=seed_path)
    return seed_path


def server(seeded: Path, estate: Path) -> SeedServer:
    return SeedServer(seeded, estate)


def rpc(srv: SeedServer, method: str, params: dict | None = None, id_: int = 1) -> dict:
    msg: dict = {"jsonrpc": "2.0", "id": id_, "method": method}
    if params is not None:
        msg["params"] = params
    return handle(msg, srv) or {}


def result_of(srv: SeedServer, method: str, params: dict | None = None) -> dict:
    res = rpc(srv, method, params)
    assert "error" not in res, res
    return res["result"]


def tool(srv: SeedServer, name: str, args: dict) -> dict:
    res = result_of(srv, "tools/call", {"name": name, "arguments": args})
    assert not res.get("isError"), res
    return json.loads(res["content"][0]["text"])


def test_initialize_declares_tools_and_resources(seeded, estate):
    srv = server(seeded, estate)
    res = result_of(srv, "initialize", {})
    assert res["serverInfo"]["name"] == "seed-rib"
    assert res["capabilities"]["tools"] == {} and res["capabilities"]["resources"] == {}


def test_resources_list_three_uris(seeded, estate):
    srv = server(seeded, estate)
    uris = sorted(r["uri"] for r in result_of(srv, "resources/list")["resources"])
    assert uris == ["seed://brief-pointers", "seed://current", "seed://law-registry"]


def test_read_current_resource_is_seed_rib_v0(seeded, estate):
    srv = server(seeded, estate)
    text = result_of(srv, "resources/read", {"uri": "seed://current"})["contents"][0]["text"]
    seed = json.loads(text)
    assert seed["schema"] == "seed_rib.v0" and seed["entries"]


def test_law_registry_resource_is_live_bytes(seeded, estate):
    srv = server(seeded, estate)
    text = result_of(srv, "resources/read", {"uri": "seed://law-registry"})["contents"][0]["text"]
    assert json.loads(text)["LAW-1"]["tier"] == "T0"


def test_rebuild_subtree_matches_seed_rib_verify(seeded, estate, tmp_path):
    srv = server(seeded, estate)
    rb = tool(srv, "rebuild_subtree", {"into": str(tmp_path / "rb")})
    assert rb["ok"] and rb["inline_ok"] == rb["inline_total"] and rb["mismatches"] == []
    assert seed_rib_verify(seeded, estate, tmp_path / "rb2") == 0


def seed_rib_verify(seed: Path, estate: Path, into: Path) -> int:
    from tools.seed_rib import verify as seed_verify
    return seed_verify(seed, into, estate)


def test_verify_hash_spotchecks_rebuilt_files(seeded, estate, tmp_path):
    srv = server(seeded, estate)
    rb = tool(srv, "rebuild_subtree", {"into": str(tmp_path / "rb")})
    for e in json.loads(seeded.read_text(encoding="utf-8"))["entries"]:
        if e.get("carrier") != "inline":
            continue
        vh = tool(srv, "verify_hash", {"path": e["path"], "root": str(tmp_path / "rb")})
        assert vh["ok"] and vh["matches_seed"]


def test_verify_hash_detects_tampered_bytes(seeded, estate, tmp_path):
    srv = server(seeded, estate)
    (tmp_path / "tampered").mkdir()
    (tmp_path / "tampered" / "docs").mkdir()
    (tmp_path / "tampered" / "docs" / "DNA.md").write_text("mutated\n", encoding="utf-8")
    vh = tool(srv, "verify_hash", {"path": "docs/DNA.md", "root": str(tmp_path / "tampered")})
    assert vh["ok"] and vh["matches_seed"] is False and vh["seal"]


def test_verify_hash_refuses_void_path(seeded, estate):
    srv = server(seeded, estate)
    vh = tool(srv, "verify_hash", {"path": "../escape.md"})
    assert vh["ok"] is False and "void" in vh["error"]


def test_fetch_pointer_serves_seal_checked_bytes(seeded, estate):
    srv = server(seeded, estate)
    fp = tool(srv, "fetch_bounded_pointer", {"path": "AGENTS.md"})
    assert fp["served"] and fp["carrier"] == "pointer"
    raw = base64.b64decode(fp["bytes_b64"])
    assert hashlib.sha256(raw).hexdigest() == fp["sha256"]
    assert raw == (estate / "AGENTS.md").read_bytes()


def test_fetch_pointer_refuses_mutated_source(seeded, estate, tmp_path):
    bad = tmp_path / "bad_estate"
    bad.mkdir()
    (bad / "AGENTS.md").write_text("replaced bytes\n", encoding="utf-8")
    srv = SeedServer(seeded, bad)
    fp = tool(srv, "fetch_bounded_pointer", {"path": "AGENTS.md"})
    assert fp["served"] is False and "SEAL MISMATCH" in fp["reason"]
    assert "bytes_b64" not in fp


def test_fetch_pointer_without_source_stays_a_stub(seeded, tmp_path):
    srv = SeedServer(seeded, tmp_path / "nowhere")
    fp = tool(srv, "fetch_bounded_pointer", {"path": "AGENTS.md"})
    assert fp["served"] is False and "stub" in fp["reason"]


def test_fetch_inline_entry_points_at_the_seed_resource(seeded, estate):
    srv = server(seeded, estate)
    fp = tool(srv, "fetch_bounded_pointer", {"path": "docs/DNA.md"})
    assert fp["carrier"] == "inline" and fp["served"] is False and "seed://current" in fp["how"]


def test_join_protocol_shape(seeded, estate):
    srv = server(seeded, estate)
    join = tool(srv, "join_protocol", {})
    assert join["schema"] == "seed_join.v0"
    assert [s["id"] for s in join["steps"]] == [
        "read_seed", "obey_laws", "rebuild", "spot_check",
        "fetch_pointers", "briefs", "announce"]
    assert join["law_refs"] == ["LAW-1"]
    assert join["seed_sha256"] == hashlib.sha256(seeded.read_bytes()).hexdigest()
    assert "memory/briefs/latest.md" in join["brief_pointers"]


def test_unknown_tool_is_tool_error(seeded, estate):
    srv = server(seeded, estate)
    res = rpc(srv, "tools/call", {"name": "nope", "arguments": {}})
    assert res["result"].get("isError") is True


def test_stdio_subprocess_round_trip(seeded, estate):
    proc = subprocess.run(
        [sys.executable, str(REPO / "tools" / "seed_mcp.py"),
         "--seed", str(seeded), "--source", str(estate), "--seed-sha"],
        capture_output=True, text=True, creationflags=HEADLESS)
    assert proc.returncode == 0
    assert proc.stdout.strip() == hashlib.sha256(seeded.read_bytes()).hexdigest()
