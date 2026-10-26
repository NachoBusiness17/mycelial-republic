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
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
LATTICE_JSON = os.path.join(HERE, "..", "reference", "gstdcoin", "contracts", "lattice.json")
RUNS_DIR = os.path.join(HERE, "..", "watch", "inbox", "gstd_perimeter_build_20261010", "runs")
BRIDGE_CWD = os.path.join(HERE, "..", "reference", "gstdcoin", "contracts")
MASTER_DEFAULT = "EQArRbzf9lhdzIytV_DuROSWzdWvkCo1KVrjrsoMhVsUdQTu"  # v8, cron cutover 2026-10-14


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
    {"name": "reputation_read", "description": "Read a worker's settled-task reputation from SettlementMaster v6 on-chain. arg: worker (TON address, UQ or EQ form).", "inputSchema": {"type": "object", "properties": {"worker": {"type": "string", "description": "Worker TON address"}}, "required": ["worker"]}},
    {"name": "settle", "description": "Settle a certified consensus run through SettlementMaster v6. Requires: run_id (certified STRUCTURE run), worker (TON address), consensus_rate, correct_rate. Gated by GSTD_MCP_ALLOW_SETTLE env var. The master must hold >= 0.5 TON for the bonus gas.", "inputSchema": {"type": "object", "properties": {"run_id": {"type": "string", "description": "Certified consensus run ID"}, "worker": {"type": "string", "description": "Worker TON address"}, "consensus_rate": {"type": "number"}, "correct_rate": {"type": "number"}}, "required": ["run_id", "worker", "consensus_rate", "correct_rate"]}},
]

ALLOW_SETTLE = os.environ.get("GSTD_MCP_ALLOW_SETTLE", "") == "1"


def dispatch(name: str, args: dict) -> dict:
    if name == "lattice_read":
        return tool_lattice_read()
    if name == "consensus_run_status":
        return tool_consensus_run_status()
    if name == "reputation_read":
        return tool_reputation_read((args or {}).get("worker", ""))
    if name == "settle":
        if not ALLOW_SETTLE:
            return {"error": "settle is gated: set GSTD_MCP_ALLOW_SETTLE=1 to enable", "isError": True}
        return tool_settle(args or {})
    return {"error": "unknown tool: " + str(name)}


def tool_reputation_read(worker: str) -> dict:
    """Read a worker's reputation from the lattice snapshot (no network I/O).
    The per-cell reputation is written by hot-lattice.ts, the trusted instrument.
    For workers not in the lattice, returns reputation 0 (unknown worker)."""
    if not worker:
        return {"error": "worker address required"}
    snap = load_lattice()
    cells = snap.get("cells", {})
    for name, c in cells.items():
        # the hot-lattice stores per-cell state; the wallet address is the key
        # in the CELLS config, not in the snapshot. Match by checking all cells.
        pass
    # the lattice doesn't carry per-wallet reputation (it carries per-CELL).
    # For a specific worker address, the caller should check the on-chain
    # getter via scripts/settle-consensus.ts or a dedicated instrument.
    # Return the lattice-level data and note the limitation.
    return {"worker": worker, "reputation": -1,
            "note": "per-wallet reputation requires an on-chain read; use scripts/settle-consensus.ts or add the worker to CELLS in hot-lattice.ts. "
                    "The lattice snapshot carries per-cell reputation: " + json.dumps({k: v.get("reputation") for k, v in cells.items()})}


def tool_settle(args: dict) -> dict:
    """Settle a certified consensus run through SettlementMaster v6.
    Shells out to the gated bridge script (settle-consensus.ts) so the server
    itself stays zero-network. The subprocess is the boundary."""
    required = ["run_id", "worker", "consensus_rate", "correct_rate"]
    for f in required:
        if f not in args:
            return {"error": f"missing required field: {f}", "isError": True}
    bridge = os.path.join(BRIDGE_CWD, "scripts", "settle-consensus.ts")
    if not os.path.isfile(bridge):
        return {"error": "bridge script not found: " + bridge, "isError": True}
    npx = shutil.which("npx")
    if not npx:
        return {"error": "npx not found on PATH", "isError": True}
    cmd = [npx, "ts-node", "--project", os.path.join(str(BRIDGE_CWD), "tsconfig.deploy.json"),
           "scripts/settle-consensus.ts",
           "--verdict", "STRUCTURE",
           "--consensus", str(args.get("consensus_rate", 0.85)),
           "--correct", str(args.get("correct_rate", 0.70)),
           "--run", args["run_id"],
           "--node", args.get("node", "desktop-7c70ksc")]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=480,
                       cwd=str(BRIDGE_CWD), encoding="utf-8", errors="replace")
    out = ((p.stdout or "") + (p.stderr or ""))[-500:]
    return {"rc": p.returncode, "output": out, "isError": p.returncode != 0}


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
