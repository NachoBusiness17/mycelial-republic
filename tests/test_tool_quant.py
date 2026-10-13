"""Stateless tests for mag.tool_quant — quant versions of all our tools (deterministic, $0)."""
from __future__ import annotations

from mag.tool_quant import quant_tool, scan_tools, turtle_join


def test_scan_tools_finds_tools():
    tools = scan_tools()
    assert isinstance(tools, list) and len(tools) > 0
    assert all("name" in t and "path" in t for t in tools)


def test_quant_tool_produces_merkle_root():
    tools = scan_tools()
    q = quant_tool(tools[0]["name"], tools[0]["path"])
    assert q["ok"] is True
    assert q["quant"]["root"] is not None and len(q["quant"]["root"]) > 0
    assert q["quant"]["n"] > 0


def test_quant_tool_deterministic():
    """Same tool -> same Merkle root (the stateless invariant: the quant is a pure function)."""
    tools = scan_tools()
    name, path = tools[0]["name"], tools[0]["path"]
    assert quant_tool(name, path)["quant"]["root"] == quant_tool(name, path)["quant"]["root"]


def test_turtle_join_dry_no_spawn():
    """Stochastic-deterministic turtle join in DRY mode (no swarm spawn) — deterministic."""
    j = turtle_join(tool="shape_map", enqueue=False)
    assert j["ok"] is True
    assert j["join"] == "deterministic quant + stochastic swarm"
    assert "turtle" in j and "turtles all the way down" in j["turtle"]
