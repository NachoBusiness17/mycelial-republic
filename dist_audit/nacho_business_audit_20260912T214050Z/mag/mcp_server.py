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
      python -m mag.mcp_server --quantize archivist  (stable compact cartridge)
      python -m mag.mcp_server --quantize all --out watch/inbox/MCP_CARTRIDGES.json
      python -m mag.mcp_server --profile builder    (serve a bounded profile)
"""
from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import os
import sys
from pathlib import Path
from typing import Any

SCHEMA = "mcp_tool_map.v1"
PROTOCOL_VERSION = "2025-06-18"
SERVER_INFO = {"name": "mag-tool-map", "version": "1.0.0"}

# These are capability projections, not permission sets.  A spawned server can
# expose fewer tools to a model body to save context and reduce accidental
# surface area; the existing guards/switchboard/effect broker still decide
# whether a call may execute.
ROLE_TOOLSETS: dict[str, tuple[str, ...]] = {
    "archivist": (
        "list_dir", "read_file", "search_files", "blackboard_read",
        "pheromone_trail", "scan_measure", "scan_probe", "scan_grid",
        "mean_field", "whisper_decode",
    ),
    "scout": (
        "list_dir", "read_file", "search_files", "swarm_sense",
        "pheromone_trail", "scan_measure", "scan_probe", "scan_grid",
        "mean_field", "research",
    ),
    "builder": (
        "list_dir", "read_file", "search_files", "write_file", "apply_patch",
        "run_python", "run_shell", "blackboard_read",
    ),
    "adversary": (
        "read_file", "search_files", "blackboard_read", "pheromone_trail",
        "scan_measure", "scan_probe", "scan_grid", "mean_field", "swarm_sense",
    ),
    "governor": (
        "list_dir", "read_file", "search_files", "blackboard_read", "pheromone_trail",
    ),
    "historian": (
        "list_dir", "read_file", "search_files", "blackboard_read", "pheromone_trail",
        "whisper_decode",
    ),
    "salon": (
        "list_dir", "read_file", "search_files", "blackboard_read", "pheromone_trail",
        "research", "vision",
    ),
    "steward": (
        "list_dir", "read_file", "search_files", "blackboard_read", "pheromone_trail",
        "research",
    ),
    "book": (
        "list_dir", "read_file", "search_files", "blackboard_read", "vision",
        "whisper_decode",
    ),
    "full": (),
}

ROLE_DESCRIPTIONS = {
    "archivist": "bounded inventory and lossless evidence retrieval",
    "scout": "low-cost exploration and candidate discovery",
    "builder": "contract-bound implementation and local verification",
    "adversary": "read-only challenge, measurement, and stop-signal generation",
    "governor": "policy inspection without direct effect execution",
    "historian": "continuity, archive, and provenance work",
    "salon": "canon-bound analysis and proposal synthesis",
    "steward": "resource, route, and reservoir analysis",
    "book": "Primer/ractor design review over canonical pointers",
    "full": "backward-compatible complete local tool projection",
}

_READ_TOOLS = {
    "list_dir", "read_file", "search_files", "blackboard_read", "pheromone_trail",
    "scan_measure", "scan_probe", "scan_grid", "mean_field", "swarm_sense",
    "whisper_decode",
}
_MUTATING_TOOLS = {"write_file", "apply_patch", "run_shell", "run_python",
                   "pheromone_drop", "blackboard_post"}
_MODEL_OR_EXTERNAL_TOOLS = {"research", "vision", "voice_turn"}


def _tool_meta(name: str) -> dict[str, str]:
    """Return compact, honest metadata for a capability projection.

    This metadata describes the surface; it never grants the capability.  The
    values intentionally use UNKNOWN where a call-specific meter is required.
    """
    if name in _MUTATING_TOOLS:
        return {
            "effect_class": "mutating_or_executing",
            "risk": "guarded",
            "authority": "switchboard_and_effect_broker",
            "cost_kind": "local_compute_or_unknown",
            "exhaustion": "deny_or_defer",
        }
    if name in _MODEL_OR_EXTERNAL_TOOLS:
        return {
            "effect_class": "model_or_external",
            "risk": "provider_dependent",
            "authority": "broker_or_explicit_refusal",
            "cost_kind": "unknown_until_metered",
            "exhaustion": "reroute_or_stop",
        }
    if name in _READ_TOOLS:
        return {
            "effect_class": "read_or_deterministic_compute",
            "risk": "low_or_local",
            "authority": "read_guard",
            "cost_kind": "deterministic_local",
            "exhaustion": "retry_or_defer",
        }
    return {
        "effect_class": "unknown",
        "risk": "unknown",
        "authority": "explicit_policy_required",
        "cost_kind": "unknown",
        "exhaustion": "operator_gate",
    }


def _load_tool_map() -> dict[str, Any]:
    from tools import TOOL_MAP

    return TOOL_MAP


def _load_tool_functions() -> dict[str, Any]:
    """Load real callables for signatures; TOOL_MAP remains the call registry.

    TOOL_MAP deliberately uses ``**kw`` lambdas for normalization.  Introspecting
    those lambdas produced a fake required ``kw`` argument in the first MCP
    dogfood pass.  The underlying function map is the correct signature source.
    """
    from tools import TOOL_MAP, _FN

    functions = dict(_FN)
    if "vision" not in functions:
        from mag import vision

        functions["vision"] = vision.describe
    for name, fn in TOOL_MAP.items():
        functions.setdefault(name, fn)
    return functions


def _profile_names(profile: str) -> list[str]:
    if profile not in ROLE_TOOLSETS:
        raise ValueError(f"unknown MCP profile: {profile}")
    names = sorted(_load_tool_map())
    selected = ROLE_TOOLSETS[profile]
    if not selected:  # full profile
        return names
    return [name for name in selected if name in names]


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
        annotation = p.annotation
        if isinstance(default, bool) or annotation in (bool, "bool"):
            t = "boolean"
        elif isinstance(default, int) or annotation in (int, "int"):
            t = "integer"
        elif isinstance(default, float) or annotation in (float, "float"):
            t = "number"
        entry: dict[str, Any] = {"type": t}
        if default is not None and not isinstance(default, (bool, int, float)):
            entry["default"] = default
        props[name] = entry
        if p.default is inspect.Parameter.empty:
            required.append(name)
    return {"type": "object", "properties": props, "required": required}


def tools_manifest(profile: str = "full") -> list[dict[str, Any]]:
    """Return a compact, profile-scoped manifest from live callable signatures."""
    functions = _load_tool_functions()
    out = []
    for name in _profile_names(profile):
        fn = functions[name]
        doc = (inspect.getdoc(getattr(fn, "__wrapped__", fn)) or "").strip().splitlines()
        out.append({
            "name": name,
            "description": (doc[0] if doc else f"mag tool: {name}")[:240],
            "inputSchema": _param_schema(fn),
            "_meta": {"mag": {"profile": profile, "quantized": True, **_tool_meta(name)}},
        })
    return out


def quantized_manifest(profile: str = "full") -> dict[str, Any]:
    """Build a timestamp-free, content-addressed capability cartridge.

    The cartridge is a projection for model context.  Its digest makes the
    exact tool surface cacheable and auditable; it is not an authority grant.
    """
    tools = tools_manifest(profile)
    body = {
        "schema": "mcp_quantized_manifest.v1",
        "profile": profile,
        "purpose": ROLE_DESCRIPTIONS[profile],
        "authority": "projection_only; execution remains guarded by Mag",
        "source": "tools.TOOL_MAP + tools._FN signatures",
        "tool_count": len(tools),
        "tools": tools,
    }
    canonical = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    body["manifest_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return body


def quantized_cartridges() -> dict[str, Any]:
    """Build every persona cartridge once for shared cache/manifest filing."""
    profiles = {profile: quantized_manifest(profile) for profile in sorted(ROLE_TOOLSETS)}
    body = {
        "schema": "mcp_quantized_cartridges.v1",
        "purpose": "share stable, bounded tool projections between model bodies",
        "authority": "projection_only; execution remains guarded by Mag",
        "profiles": profiles,
    }
    canonical = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    body["cartridges_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return body


def write_quantized_cartridges(path: str | Path, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """Atomically file a generated cartridge for other model bodies to read.

    This writes a projection only. It does not register tools, grant effects,
    or alter the live tool registry. The temporary sibling plus ``os.replace``
    prevents a reader from observing a half-written shared cartridge.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    value = payload if payload is not None else quantized_cartridges()
    encoded = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    temporary = target.with_name(f".{target.name}.{os.getpid()}.tmp")
    try:
        temporary.write_text(encoded, encoding="utf-8")
        os.replace(temporary, target)
    finally:
        try:
            temporary.unlink()
        except OSError:
            pass
    return {
        "ok": True,
        "path": str(target),
        "schema": value.get("schema"),
        "cartridges_sha256": value.get("cartridges_sha256"),
        "profile_count": len(value.get("profiles") or {}),
    }


def call_tool(name: str, arguments: dict[str, Any] | None,
              allowed_tools: set[str] | None = None) -> dict[str, Any]:
    """Dispatch through the SAME registry + arg-normalizer the backend uses."""
    from tools import TOOL_MAP, _normalize_args

    if allowed_tools is not None and name not in allowed_tools:
        return {"content": [{"type": "text", "text": json.dumps(
            {"ok": False, "error": f"tool not in active MCP profile: {name}"})}],
                "isError": True}
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


def handle(msg: dict[str, Any], profile: str = "full") -> dict[str, Any] | None:
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
        return _rpc(id_, {"tools": tools_manifest(profile)})
    if method == "tools/call":
        p = msg.get("params") or {}
        return _rpc(id_, call_tool(str(p.get("name") or ""), p.get("arguments"),
                                   set(_profile_names(profile))))
    if id_ is not None:
        return _err(id_, -32601, f"method not found: {method}")
    return None


def serve(profile: str = "full") -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            resp = _err(None, -32700, "parse error")
        else:
            resp = handle(msg, profile)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    ap = argparse.ArgumentParser(prog="mcp-server", description="Serve mag TOOL_MAP over MCP stdio")
    ap.add_argument("--list", action="store_true", help="print the tool manifest and exit")
    ap.add_argument("--profile", choices=sorted(ROLE_TOOLSETS), default="full",
                    help="restrict the exposed projection to one persona profile")
    ap.add_argument("--quantize", choices=["all", *sorted(ROLE_TOOLSETS)], metavar="PROFILE",
                    help="print a stable persona-scoped cartridge, or all profiles")
    ap.add_argument("--out", metavar="PATH",
                    help="atomically file a quantized cartridge (requires --quantize)")
    args = ap.parse_args(argv)
    if args.out and not args.quantize:
        ap.error("--out requires --quantize")
    if args.quantize:
        result = quantized_cartridges() if args.quantize == "all" else quantized_manifest(args.quantize)
        if args.out:
            print(json.dumps(write_quantized_cartridges(args.out, result), ensure_ascii=False))
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    if args.list:
        print(json.dumps(tools_manifest(args.profile), indent=2, ensure_ascii=False))
        return 0
    return serve(args.profile)


if __name__ == "__main__":
    raise SystemExit(main())
