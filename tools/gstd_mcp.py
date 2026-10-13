"""gstd-mcp server: stdlib JSON-RPC 2.0 line-delimited stdin/stdout loop.

Mirrors the gps-mcp idiom (tools/gps_mcp): MCP-shaped tool surface, plain
stdlib wire, every successful result as
    {"content": [{"type": "text", "text": "<json>"}], "isError": false}

SECURITY POSTURE (Mimosa-gated 2026-10-12): this server performs ZERO
network I/O. It serves two literal-path files written by trusted instruments:
  - lattice.json   (written by reference/gstdcoin/contracts/scripts/hot-lattice.ts:
                    per-cell hot models / VRAM / TON / on-chain reputation +
                    SettlementMaster v6 stats; freshness = file mtime)
  - the latest consensus run summary.json under the perimeter runs dir
Settlement is deliberately NOT exposed on this wire - settlement runs
through the gated bridge (scripts/settle-consensus.ts), never via MCP.

Tools:
    lattice_read()         -> the whole lattice snapshot + snapshot age
    consensus_run_status() -> latest local consensus run verdict + rates
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
LATTICE_JSON = os.path.join(HERE, "..", "reference", "gstdcoin", "contracts", "lattice.json")
RUNS_DIR = os.path.join(HERE, "..", "watch", "inbox", "gstd_perimeter_build_20261010", "runs")


def load_lattice() -> dict:
    with open(LATTICE_JSON, encoding="utf-8") as f:
        snap = json.load(f)
    age = round(time.time() - os.path.getmtime(LATTICE_JSON))
    snap["snapshot_age_s"] = age
    snap["fresh"] = age < 1800
    return snap


def tool_lattice_read() -> dict:
    snap = load_lattice()
    return {
        "captured_at": snap.get("captured_at"),
        "snapshot_age_s": snap.get("snapshot_age_s"),
        "fresh": snap.get("fresh"),
        "master": snap.get("master"),
        "baseRate_nano": snap.get("baseRate"),
        "taskCount": snap.get("taskCount"),
        "totalSettledTon": snap.get("totalSettledTon"),
        "cells": snap.get("cells", {}),
    }


def tool_consensus_run_status() -> dict:
    root = os.path.realpath(RUNS_DIR)
    best = None
    for d in sorted(os.listdir(root)):
        p = os.path.join(root, d, "summary.json")
        if os.path.isfile(p):
            m = os.path.getmtime(p)
            if best is None or m > best[0]:
                best = (m, p, d)
    if best is None:
        return {"note": "no local consensus runs found"}
    s = json.load(open(best[1], encoding="utf-8"))
    return {"run_id": s.get("run_id"), "verdict": s.get("verdict"),
            "consensus_rate": s.get("consensus_rate"),
            "correct_rate": s.get("consensus_correct_rate"),
            "noise": s.get("dead_salmon_control_rate"),
            "tasks": s.get("tasks"), "models": s.get("models"),
            "dir": best[2]}


TOOL_DEFINITIONS = [
    {"name": "lattice_read", "description": "The VRAM hot lattice snapshot: per tailnet cell - hot models, VRAM MB, TON balance, on-chain reputation; plus SettlementMaster v6 stats. Includes snapshot age (fresh < 1800s).", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "consensus_run_status", "description": "Latest local consensus harness run: verdict (STRUCTURE/WEAK/DEGENERATE/NOISE-CLASS), consensus vs noise rates, models, tasks.", "inputSchema": {"type": "object", "properties": {}}},
]


def dispatch(name: str, args: dict) -> dict:
    if name == "lattice_read":
        return tool_lattice_read()
    if name == "consensus_run_status":
        return tool_consensus_run_status()
    return {"error": "unknown tool: " + str(name)}


def main() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse: " + str(e)[:80]}}), flush=True)
            continue
        rid = req.get("id")
        method = req.get("method", "")
        params = req.get("params") or {}
        if method == "initialize":
            resp = {"jsonrpc": "2.0", "id": rid, "result": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "gstd-mcp", "version": "0.2.0"}}}
        elif method == "tools/list":
            resp = {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOL_DEFINITIONS}}
        elif method == "tools/call":
            name = params.get("name", "")
            args = params.get("arguments") or {}
            try:
                out = dispatch(name, args)
                resp = {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(out)}], "isError": False}}
            except FileNotFoundError:
                resp = {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": "lattice.json not found - run scripts/hot-lattice.ts to refresh"}], "isError": True}}
            except Exception as e:
                resp = {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": str(e)[:200]}], "isError": True}}
        elif method.startswith("notifications/"):
            continue
        else:
            resp = {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "method not implemented: " + method}}
        print(json.dumps(resp), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
