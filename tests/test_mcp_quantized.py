"""Dogfood the MCP draft as compact persona-scoped tool cartridges.

The MCP surface is a projection/transport.  It must derive schemas from the
real callables, remain deterministic for cache reuse, and narrow exposure
without becoming an authority grant.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.mcp_server import (
    handle,
    quantized_cartridges,
    quantized_manifest,
    tools_manifest,
    write_quantized_cartridges,
)
from tools import TOOL_MAP


def test_manifest_uses_real_signatures_not_kw_lambdas() -> None:
    manifest = tools_manifest()
    assert len(manifest) == len(TOOL_MAP)
    assert all("kw" not in t["inputSchema"].get("properties", {}) for t in manifest)
    by_name = {t["name"]: t for t in manifest}
    assert "path" in by_name["read_file"]["inputSchema"]["properties"]
    assert "content" in by_name["write_file"]["inputSchema"]["properties"]


def test_persona_cartridge_is_smaller_and_stable() -> None:
    full = quantized_manifest("full")
    archivist = quantized_manifest("archivist")
    assert archivist["tool_count"] < full["tool_count"]
    assert archivist["manifest_sha256"] == quantized_manifest("archivist")["manifest_sha256"]
    assert archivist["authority"].startswith("projection_only")
    assert all("_meta" in tool for tool in archivist["tools"])


def test_profile_narrows_calls_but_does_not_grant_effects() -> None:
    denied = handle({
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": "write_file", "arguments": {"path": "x", "content": "x"}},
    }, "archivist")
    assert denied["result"]["isError"] is True
    assert "not in active MCP profile" in denied["result"]["content"][0]["text"]


def test_tools_list_is_profile_scoped() -> None:
    result = handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, "book")
    names = {tool["name"] for tool in result["result"]["tools"]}
    assert names == {"list_dir", "read_file", "search_files", "blackboard_read", "vision", "whisper_decode"}


def test_all_cartridges_share_one_registry() -> None:
    cartridges = quantized_cartridges()
    assert set(cartridges["profiles"]) >= {"archivist", "builder", "book", "full"}
    assert cartridges["profiles"]["full"]["tool_count"] == len(TOOL_MAP)
    assert cartridges["profiles"]["builder"]["tool_count"] < cartridges["profiles"]["full"]["tool_count"]
    assert len(cartridges["cartridges_sha256"]) == 64


def test_shared_cartridge_writer_is_atomic_and_round_trips(tmp_path) -> None:
    target = tmp_path / "shared" / "MCP_CARTRIDGES.json"
    payload = quantized_cartridges()
    receipt = write_quantized_cartridges(target, payload)
    assert receipt["ok"] is True
    assert receipt["cartridges_sha256"] == payload["cartridges_sha256"]
    loaded = __import__("json").loads(target.read_text(encoding="utf-8"))
    assert loaded["cartridges_sha256"] == payload["cartridges_sha256"]
    assert not list(target.parent.glob("*.tmp"))
