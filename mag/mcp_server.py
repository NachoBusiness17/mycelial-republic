"""mcp_server — serve the mag TOOL_MAP over the Model Context Protocol (stdio).

Operator ask (design doc Next #5, 2026-08-25): "serving our tool catalog as MCP
so the bodies consume each other." This is that server. Any MCP-capable body
(zcode, cursor, claude, codex, opencode) spawns it and gets the mag tool
registry NATIVELY — no bridge code, no prompt glue, no seat-specific adapters.

WHY STDIO JSON-RPC BY HAND: the venv has no `mcp`/`fastmcp` package and this
system's law is stdlib-only. MCP is JSON-RPC 2.0 over stdio with a fixed
handshake (initialize → notifications/initialized → tools/list, tools/call) —
small enough to implement exactly, and every byte is inspectable.

SECURITY POSTURE: the tool registry ALREADY runs inside this repo's backend
(dashboard /run_task dispatches the same TOOL_MAP). Spawning this server grants
nothing the local process doesn't already have; it is transport, not authority.
It does NOT expose file paths outside what filesystem.py itself allows.

Schema: mcp_tool_map.v1 · stdio transport · reuse: tools.TOOL_MAP (single source)
CLI:  python -m mag.mcp_server            (speak MCP on stdio — for clients)
      python -m mag.mcp_server --list     (human list of exposed tools)
"""
from __future__ import annotations

import argparse
import inspect
import json
import sys
from typing import Any

SCHEMA = "mcp_tool_map.v1"
PROTOCOL_VERSION = "2025-06-18"
SERVER_INFO = {"name": "mag-tool-map", "version": "1.0.0"}


def _load_tool_map() -> dict[str, Any]:
    from tools import TOOL_MAP

    return TOOL_MAP


def _param_schema(fn: Any) -> dict[str, Any]:
    """Best-effort JSON Schema from the signature (stdlib-only, no registry upkeep).

    The registry stays compiled-from-code: signature drift updates the schema.
    """
    props: dict[str, Any] = {}
    required: list[str] = []
    try:
        sig = inspect.signature(fn)
        real = getattr(fn, "__wrapped__", fn)
        sig = inspect.signature(real)
    except (TypeError, ValueError):
        return {"type": "object", "properties": props}
    for name, p in sig.parameters.items():
        if name in ("self", "kwargs", "args"):
            continue
        t = "string"
        default = p.default if p.default is not inspect.Parameter.empty else None
        if isinstance(default, bool) or p.annotation is bool:
            t = "boolean"
        elif isinstance(default, int) or p.annotation in (int, "int"):
            t = "integer"
        elif isinstance(default, float) or p.annotation in (float, "float"):
            t = "number"
        entry: dict[str, Any] = {"type": t}
        if default is not None and not isinstance(default, (bool, int, float)):
            entry["default"] = default
        props[name] = entry
        if p.default is inspect.Parameter.empty:
            required.append(name)
    return {"type": "object", "properties": props, "required": required}


def tools_manifest() -> list[dict[str, Any]]:
    from tools import _normalize_args  # noqa: F401  (documented reuse below)

    out = []
    for name, fn in _load_tool_map().items():
        doc = (inspect.getdoc(getattr(fn, "__wrapped__", fn)) or "").strip().splitlines()
        out.append({
            "name": name,
            "description": doc[0] if doc else f"mag tool: {name}",
            "inputSchema": _param_schema(fn),
        })
    return out


def call_tool(name: str, arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Dispatch through the SAME registry + arg-normalizer the backend uses."""
    from tools import TOOL_MAP, _normalize_args

    args = _normalize_args(name, arguments)
    if args is None:
        return {"content": [{"type": "text", "text": json.dumps(
            {"ok": False, "error": f"unknown tool: {name}"})}], "isError": True}
    try:
        result = TOOL_MAP[name](**args)
    except Exception as e:  # noqa: BLE001 — tool boundary, report don't crash
        return {"content": [{"type": "text", "text": json.dumps(
            {"ok": False, "error": f"{type(e).__name__}: {e}"})}], "isError": True}
    if not isinstance(result, (str, bytes)):
        result = json.dumps(result, ensure_ascii=False, default=str)
    return {"content": [{"type": "text", "text": str(result)}]}


# ────────────────────────────── MCP stdio protocol ──────────────────────────

def _rpc(id_: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": id_, "result": result}


def _err(id_: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}}


def handle(msg: dict[str, Any]) -> dict[str, Any] | None:
    method = msg.get("method")
    id_ = msg.get("id")
    if method == "initialize":
        return _rpc(id_, {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": SERVER_INFO,
        })
    if method == "notifications/initialized":
        return None  # notification — no response
    if method == "ping":
        return _rpc(id_, {})
    if method == "tools/list":
        return _rpc(id_, {"tools": tools_manifest()})
    if method == "tools/call":
        p = msg.get("params") or {}
        return _rpc(id_, call_tool(str(p.get("name") or ""), p.get("arguments")))
    if id_ is not None:
        return _err(id_, -32601, f"method not found: {method}")
    return None


def serve() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            resp = _err(None, -32700, "parse error")
        else:
            resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    ap = argparse.ArgumentParser(prog="mcp-server", description="Serve mag TOOL_MAP over MCP stdio")
    ap.add_argument("--list", action="store_true", help="print the tool manifest and exit")
    args = ap.parse_args(argv)
    if args.list:
        print(json.dumps(tools_manifest(), indent=2, ensure_ascii=False)[:4000])
        return 0
    return serve()


if __name__ == "__main__":
    raise SystemExit(main())
