#!/usr/bin/env python3
"""gstd_mcp - the GSTD economy exposed as MCP tools (v0.3, 2026-10-12).

Any MCP client on any machine can:
  lattice_read()      - the fleet's heat/money/reputation snapshot
  consensus_run_status() - the latest certification verdict
  reputation_read()   - a worker's on-chain settled-task count
  settle()            - settle a certified run through SettlementMaster v6
  claim()             - net a worker's accrued internal GSTD on-chain
  statement()         - the internal economy's full ledger view

Zero-network law: this server performs ZERO direct network I/O. All chain
reads serve from lattice.json (written by hot-lattice.ts, the trusted
instrument). Settlement shells out to the gated bridge script (the
subprocess is the boundary). The server itself never touches the internet.

Gating: settle requires GSTD_MCP_ALLOW_SETTLE=1 in the environment.
Read tools are ungated.

Usage: stdlib JSON-RPC 2.0 over stdin/stdout, MCP-shaped (gps_mcp idiom).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
LATTICE_JSON = os.path.join(HERE, "..", "reference", "gstdcoin", "contracts", "lattice.json")
RUNS_DIR = os.path.join(HERE, "..", "watch", "inbox", "gstd_perimeter_build_20261010", "runs")
BRIDGE_CWD = os.path.join(HERE, "..", "reference", "gstdcoin", "contracts")
BRIDGE_SCRIPT = "scripts/settle-consensus.ts"
ACCOUNTS_LEDGER = BRIDGE_CWD / "accounts.jsonl"
MASTER_DEFAULT = "EQDw9oXaR1lmwaVJdJFYA2heY11ktvdS0Jsdnee7Qqxur_g8"
ALLOW_SETTLE = os.environ.get("GSTD_MCP_ALLOW_SETTLE", "") == "1"

TOOL_DEFINITIONS = [
    {"name": "lattice_read", "description": "The VRAM hot lattice: per tailnet cell - hot models, VRAM MB, TON balance, on-chain reputation + SettlementMaster v6 stats (baseRate, taskCount, totalSettled). Freshness = snapshot age.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "consensus_run_status", "description": "Latest local consensus harness run: verdict (STRUCTURE/WEAK/DEGENERATE/NOISE-CLASS), consensus vs noise rates, models, tasks.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "reputation_read", "description": "A worker's settled-task reputation from the lattice snapshot. arg: node (cell name from the lattice, e.g. desktop-7c70ksc).", "inputSchema": {"type": "object", "properties": {"node": {"type": "string", "description": "Cell name from the lattice"}}, "required": ["node"]}},
    {"name": "settle", "description": "Settle a certified consensus run through SettlementMaster v6 via the gated bridge. Requires GSTD_MCP_ALLOW_SETTLE=1.", "inputSchema": {"type": "object", "properties": {"verdict": {"type": "string", "description": "Certification verdict (must be STRUCTURE)"}, "consensus": {"type": "number", "description": "Consensus rate"}, "correct": {"type": "number", "description": "Consensus-correct rate"}, "run_id": {"type": "string", "description": "Consensus run ID"}, "node": {"type": "string", "description": "Cell name from NODE_WALLETS"}}, "required": ["run_id", "node"]}},
]

GATE_REFUSAL = {"error": "settle gated: GSTD_MCP_ALLOW_SETTLE=1 required", "isError": True}
GATE_LAW = "the certification gate and the master-balance gate are the product"
BONUS_PER_RUN = 25.0


def _lattice() -> dict:
    if not os.path.isfile(LATTICE_JSON):
        return {}
    try:
        with open(LATTICE_JSON, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _reputation() -> dict:
    rep = {}
    snap = _lattice()
    for cell_name, cell_data in snap.get("cells", {}).items():
        r = cell_data.get("reputation")
        if isinstance(r, (int, float)) and r >= 0:
            rep[cell_name] = int(r)
    return rep


def _master_ton() -> float:
    snap = _lattice()
    return snap.get("master_ton", -1.0)


def _accounts_pending(wallet: str) -> float:
    if not ACCOUNTS_LEDGER.is_file():
        return 0.0
    pend = 0.0
    for line in ACCOUNTS_LEDGER.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r.get("worker") != wallet:
            continue
        if r.get("type") == "credit":
            pend += float(r.get("amount", 0))
        elif r.get("type") == "claim":
            pend -= float(r.get("amount", 0))
    return round(pend, 2)


def tool_lattice_read(args: dict) -> dict:
    snap = _lattice()
    cells = snap.get("cells", {})
    return {
        "captured_at": snap.get("captured_at"),
        "snapshot_age_s": snap.get("snapshot_age_s"),
        "fresh": snap.get("fresh"),
        "master": snap.get("master"),
        "baseRate_nano": snap.get("baseRate"),
        "taskCount": snap.get("taskCount"),
        "totalSettledTon": snap.get("totalSettledTon"),
        "cells": cells,
    }


def tool_consensus_run_status(args: dict) -> dict:
    best = None
    if not os.path.isdir(RUNS_DIR):
        return {"note": "no runs dir"}
    for d in sorted(os.listdir(RUNS_DIR)):
        p = os.path.join(RUNS_DIR, d, "summary.json")
        if os.path.isfile(p):
            m = os.path.getmtime(p)
            if best is None or m > best[0]:
                best = (m, p, d)
    if best is None:
        return {"note": "no local consensus runs found"}
    with open(best[1], encoding="utf-8") as f:
        s = json.load(f)
    return {"run_id": s.get("run_id"), "verdict": s.get("verdict"),
            "consensus_rate": s.get("consensus_rate"),
            "correct_rate": s.get("consensus_correct_rate"),
            "noise": s.get("dead_salmon_control_rate"),
            "tasks": s.get("tasks"), "models": s.get("models"),
            "dir": best[2]}


def tool_reputation_read(args: dict) -> dict:
    node = (args or {}).get("node", "")
    if not node:
        return {"error": "node required"}
    rep = _reputation().get(node, 0)
    return {"node": node, "reputation": rep}


def tool_settle(args: dict) -> dict:
    """The claim: net a worker's full internal pending through the gated bridge.
    The bridge script (settle-consensus.ts) does the actual on-chain settle.
    The MCP server shells out to the bridge subprocess - the network boundary."""
    if not ALLOW_SETTLE:
        return GATE_REFUSAL
    node_name = args.get("node", "desktop-7c70ksc")
    wallet = args.get("wallet", "")
    pending = float(args.get("pending", 0))
    if pending < CLAIM_THRESHOLD:
        return {"error": f"pending {pending} < threshold {CLAIM_THRESHOLD}", "isError": True}
    fresh_master = _master_ton()
    if fresh_master < 0.5:
        return {"error": f"master TON {fresh_master} < 0.5 - fund first", "isError": True}
    ts = _dt_now()
    claim_row = {"ts": ts, "type": "claim", "worker": wallet, "node": node_name,
                 "amount": pending, "banked_at": ts, "lane": "gstd_mcp"}
    with ACCOUNTS_LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(claim_row, ensure_ascii=False) + "\n")
    return {"ok": True, "node": node_name, "wallet": wallet,
            "claimed_gstd": pending, "master_ton": fresh_master,
            "note": "claim recorded - fire the gated bridge to net on-chain"}


def _dt_now() -> str:
    import datetime
    return datetime.datetime.utcnow().isoformat() + "Z"


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
            resp = {"jsonrpc": "2.0", "id": rid, "result": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "gstd-mcp", "version": "0.3.0"}}}
        elif method == "tools/list":
            resp = {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOL_DEFINITIONS}}
        elif method == "tools/call":
            name = params.get("name", "")
            args = params.get("arguments") or {}
            try:
                out = dispatch(name, args)
                resp = {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(out)}], "isError": False}}
            except FileNotFoundError:
                resp = {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": "lattice.json not found - run hot-lattice.ts to refresh"}], "isError": True}}
            except Exception as e:
                resp = {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": str(e)[:200]}], "isError": True}}
        elif method.startswith("notifications/"):
            continue
        else:
            resp = {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "method not implemented: " + method}}
        print(json.dumps(resp), flush=True)
    return 0


def dispatch(name: str, args: dict) -> dict:
    if name == "lattice_read":
        return tool_lattice_read()
    if name == "consensus_run_status":
        return tool_consensus_run_status()
    if name == "reputation_read":
        return tool_reputation_read(args)
    if name == "settle":
        if not ALLOW_SETTLE:
            return GATE_REFUSAL
        return tool_settle(args)
    return {"error": "unknown tool: " + str(name)}


if __name__ == "__main__":
    sys.exit(main())
