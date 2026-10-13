"""gps-mcp server: a plain stdlib JSON-RPC 2.0 stdin/stdout loop.

v0 speaks line-delimited JSON-RPC, not the full MCP wire protocol: a
real MCP client handshake is explicitly out of scope for v0. The tool
surface is MCP-shaped so wiring a real MCP transport later is
mechanical (mapping documented in README.md):

    MCP tools/list                          -> "tools/list"
    MCP tools/call {name: "ask", ...}       -> {"method": "tools/call",
                                                "params": {"name": "ask",
                                                           "arguments": {...}}}
    MCP initialize                          -> "initialize" (minimal reply)

Tools exposed (the BUILD spec's tool set):
    ask(task_shape, payload, constraints?)   -> single routing decision
    cascade(task_shape, payload, constraints?) -> escalating decision trace
    report_capability(model_id, task_shape)  -> ledger row or not-measured
    record_verdict(model_id, task_shape, verdict, evidence_hash?) -> new row state

Every successful tool result is returned MCP-style:
    {"content": [{"type": "text", "text": "<json>"}], "isError": false}

Env overrides: GPS_MCP_CONFIG, GPS_MCP_LEDGER, GPS_MCP_RECEIPTS
(defaults sit next to this file: config.json, gps_ledger.db3,
receipts.jsonl).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

if __package__ in (None, ""):  # allow direct script execution
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.gps_mcp.ledger import CapabilityLedger
from tools.gps_mcp.providers import ProviderRegistry, build_registry, load_config
from tools.gps_mcp.router import Router

PACKAGE_DIR = Path(__file__).resolve().parent

TOOL_DEFINITIONS = [
    {
        "name": "ask",
        "description": "Route one ask to the best measured endpoint and answer it.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task_shape": {"type": "string"},
                "payload": {"type": ["string", "object"]},
                "constraints": {
                    "type": "object",
                    "properties": {
                        "max_cost_usd": {"type": "number"},
                        "max_latency_ms": {"type": "integer"},
                        "min_confidence": {"type": "number"},
                        "pass_rate_threshold": {"type": "number"},
                    },
                },
            },
            "required": ["task_shape", "payload"],
        },
    },
    {
        "name": "cascade",
        "description": "Cheapest qualifying tier first, escalate one tier on low"
                       " confidence, max three tiers, full decision trace.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task_shape": {"type": "string"},
                "payload": {"type": ["string", "object"]},
                "constraints": {"type": "object"},
            },
            "required": ["task_shape", "payload"],
        },
    },
    {
        "name": "report_capability",
        "description": "Measured pass-rate, sample size, last-measured date and"
                       " cost for one (model_id, task_shape) pair.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model_id": {"type": "string"},
                "task_shape": {"type": "string"},
            },
            "required": ["model_id", "task_shape"],
        },
    },
    {
        "name": "record_verdict",
        "description": "Report a ground-truth outcome; the ledger updates as a"
                       " running mean and routing follows.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model_id": {"type": "string"},
                "task_shape": {"type": "string"},
                "verdict": {"type": ["boolean", "integer", "string"]},
                "evidence_hash": {"type": "string"},
            },
            "required": ["model_id", "task_shape", "verdict"],
        },
    },
]


class ServerState:
    def __init__(self, config_path: str | Path, ledger_path: str | Path,
                 receipts_path: str | Path):
        self.config_path = str(config_path)
        config = load_config(config_path)
        self.registry: ProviderRegistry = build_registry(config)
        self.ledger = CapabilityLedger(ledger_path)
        self.router = Router(self.registry, self.ledger, receipts_path)


def default_paths() -> tuple[Path, Path, Path]:
    config = Path(os.environ.get("GPS_MCP_CONFIG", PACKAGE_DIR / "config.json"))
    ledger = Path(os.environ.get("GPS_MCP_LEDGER", PACKAGE_DIR / "gps_ledger.db3"))
    receipts = Path(os.environ.get("GPS_MCP_RECEIPTS", PACKAGE_DIR / "receipts.jsonl"))
    return config, ledger, receipts


def make_state(
    config_path: Optional[str | Path] = None,
    ledger_path: Optional[str | Path] = None,
    receipts_path: Optional[str | Path] = None,
) -> ServerState:
    d_config, d_ledger, d_receipts = default_paths()
    return ServerState(
        config_path or d_config,
        ledger_path or d_ledger,
        receipts_path or d_receipts,
    )


def _freshness() -> dict[str, Any]:
    """mesh.door law (salon 2026-10-05): responses declare corpus state so callers
    know when they reason over a stale ledger. Corpus = ledger db + receipts."""
    import hashlib
    import time
    files = [p for p in (PACKAGE_DIR / "gps_ledger.db3",
                         PACKAGE_DIR / "receipts.jsonl") if p.exists()]
    if not files:
        return {"corpus_tip_hash": None, "last_growth_ts": None, "frozen": True}
    tip = hashlib.sha256(
        b"".join(hashlib.sha256(p.read_bytes()).digest() for p in files)).hexdigest()
    last = max(p.stat().st_mtime for p in files)
    return {"corpus_tip_hash": tip, "last_growth_ts": round(last, 3),
            "frozen": (time.time() - last) > 30 * 86400}


def _ok(req_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    if "freshness" not in result:
        result = {**result, "freshness": _freshness()}
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "content": [{"type": "text", "text": json.dumps(result)}],
            "isError": False,
        },
    }


def _err(req_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


def process_request(state: ServerState, request: dict[str, Any]) -> dict[str, Any]:
    """Handle one JSON-RPC request object. Pure w.r.t. state I/O: reads the
    request dict, returns the response dict. The loop does the I/O."""
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params") or {}
    if method == "initialize":
        return _ok(
            req_id,
            {
                "serverInfo": {"name": "gps-mcp", "version": "0.1.0"},
                "protocolVersion": "jsonrpc-2.0-stdio-v0",
                "capabilities": {"tools": {}},
            },
        )
    if method == "tools/list":
        return _ok(req_id, {"tools": TOOL_DEFINITIONS})
    if method == "tools/call":
        return _call_tool(state, req_id, params)
    return _err(req_id, -32601, f"method not found: {method!r}")


def _call_tool(state: ServerState, req_id: Any, params: dict[str, Any]) -> dict[str, Any]:
    name = params.get("name")
    args = params.get("arguments") or {}
    try:
        if name == "ask":
            if "task_shape" not in args or "payload" not in args:
                return _err(req_id, -32602, "ask requires task_shape and payload")
            decision = state.router.ask(
                args["task_shape"], args["payload"], args.get("constraints")
            )
            return _ok(req_id, decision.as_dict())
        if name == "cascade":
            if "task_shape" not in args or "payload" not in args:
                return _err(req_id, -32602, "cascade requires task_shape and payload")
            result = state.router.cascade(
                args["task_shape"], args["payload"], args.get("constraints")
            )
            return _ok(req_id, result.as_dict())
        if name == "report_capability":
            if "model_id" not in args or "task_shape" not in args:
                return _err(req_id, -32602,
                            "report_capability requires model_id and task_shape")
            row = state.ledger.report_capability(args["model_id"], args["task_shape"])
            if row is None:
                return _ok(req_id, {
                    "measured": False,
                    "model_id": args["model_id"],
                    "task_shape": args["task_shape"],
                })
            row["measured"] = True
            return _ok(req_id, row)
        if name == "record_verdict":
            for key in ("model_id", "task_shape", "verdict"):
                if key not in args:
                    return _err(req_id, -32602, f"record_verdict requires {key}")
            outcome = state.ledger.record_verdict(
                args["model_id"],
                args["task_shape"],
                args["verdict"],
                str(args.get("evidence_hash", "")),
            )
            return _ok(req_id, outcome.as_dict())
        return _err(req_id, -32601, f"unknown tool: {name!r}")
    except ValueError as exc:
        return _err(req_id, -32602, f"invalid params: {exc}")
    except Exception as exc:  # keep the loop alive on tool failure
        return _err(req_id, -32603, f"internal error: {exc}")


def main() -> int:
    state = make_state()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError as exc:
            response = _err(None, -32700, f"parse error: {exc}")
        else:
            if not isinstance(request, dict):
                response = _err(None, -32600, "request must be an object")
            else:
                response = process_request(state, request)
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
