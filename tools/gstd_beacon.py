#!/usr/bin/env python3
"""gstd_beacon - the garage-wizard artifact beacon, v0 (2026-10-12).

Think torrents for AI artifacts: MCP servers, skills, memory ledgers, LoRA
weights, datasets. Nodes announce capabilities and artifacts; strangers find
them; GSTD settles the exchanges; dead-salmon controls keep fake artifacts
invisible.

v0 shape (tailnet-only, the estate fleet is the first swarm):
  - beacon.json: the announcement set. Each row = one artifact with a
    VERIFICATION block (the consensus run that proved it works, or the
    receipt pointer). Rows without verification are rumor-class and any
    buyer can filter them.
  - serve: hosts beacon.json on the tailnet interface so other cells can
    read it (bob/t90 fetch it over tailscale).
  - inventory: prints the seeded artifact set.

The anon model: a wallet keypair is the identity (pseudonymous, no names);
reputation is the trust; verification is the gate. Anon does not mean
trustless-free - it means trust is EARNED per wallet and portable.

Laws: no artifact is announced without its verification pointer; prices in
GSTD; the dead-salmon control is the null hypothesis for every claim.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
BEACON = Path(os.environ.get("GSTD_BEACON_JSON", str(ROOT := HERE.parent / "reference" / "gstdcoin" / "contracts" / "beacon.json")))
SERVE_HOST = os.environ.get("GSTD_BEACON_HOST", "0.0.0.0")  # all interfaces: tailnet + LAN (the Roku reads the LAN side)
SERVE_PORT = int(os.environ.get("GSTD_BEACON_PORT", "8777"))

VERIFIED = "consensus-verified"

# The fleet's first announced artifacts - every one VERIFIED tonight or by a
# receipted run. Seeds: artifact_type, name, path (estate-relative), hash TBD
# by the buyer, price_gstd (0 = reputation-gated free for new swarms).
ARTIFACTS = [
    {
        "type": "skill",
        "name": "consensus-harness",
        "desc": "5-model consensus battery with a dead-salmon control; STRUCTURE/WEAK/DEGENERATE verdicts. The verification instrument this beacon itself uses.",
        "path": "tools/consensus_harness.py",
        "price_gstd": 0,
        "verification": {VERIFIED: True, "runs": ["consensus-20261011T235925Z", "consensus-20261012T043333Z"], "verdicts": ["STRUCTURE", "STRUCTURE"]},
    },
    {
        "type": "skill",
        "name": "gstd-drain",
        "desc": "The standing earn loop: queue rows -> model battery -> certification gate -> on-chain settlement. The pattern any garage wizard can point at their own rail.",
        "path": "tools/gstd_drain.py",
        "price_gstd": 0,
        "verification": {VERIFIED: True, "fires": 2, "refusals_banked": 0, "note": "STRUCTURE settles landed +25 GSTD first poll; the master-funding law is in the receipt"},
    },
    {
        "type": "mcp-server",
        "name": "gstd-mcp",
        "desc": "Read-only MCP server over the GSTD rail: lattice_read (fleet heat/money/reputation) + consensus_run_status (latest certification). Zero-network-by-design: serves instrument-written snapshots.",
        "path": "tools/gstd_mcp.py",
        "price_gstd": 0,
        "verification": {VERIFIED: True, "smoke": "initialize/tools-list/both-calls green 2026-10-12"},
    },
    {
        "type": "organ",
        "name": "worker-reputation-map",
        "desc": "On-chain per-worker settled-task reputation (SettlementMaster v6 map + getter). The trust layer: reputation accrues only for committed settles, readable by anyone.",
        "path": "SettlementMaster.tact (workerReputation + worker_reputation getter, PR #1)",
        "price_gstd": 0,
        "verification": {VERIFIED: True, "live_read": "worker_reputation(DESKTOP)=5 after 5 committed settles"},
    },
    {
        "type": "receipt",
        "name": "three-bonus-leg-bugs",
        "desc": "Three testnet-receipted contract bugs (TEP-74 opcode mismatch 1435380091-vs-0xf8a7ea5, baseRate dust-cap default, bonus gas margin) with tx-graded evidence and the starvation law. Free - the co-contributor gift.",
        "path": "watch/inbox/gstd_perimeter_build_20261010/ (PR #1)",
        "price_gstd": 0,
        "verification": {VERIFIED: True, "evidence": "input cells decoded on-chain; 4 settles graded"},
    },
]

LAW = "beacon law: verified artifacts only - a claim without a dead-salmon-beating run behind it is rumor, and rumor is invisible."


def build_beacon() -> dict:
    return {
        "beacon_version": "v0",
        "updated_at": _dt.datetime.utcnow().isoformat() + "Z",
        "swarm": "garage-wizards-testnet",
        "settlement": {"currency": "GSTD", "master_v6": "EQDw9oXaR1lmwaVJdJFYA2heY11ktvdS0Jsdnee7Qqxur_g8", "rail": "consensus-certified settle, 85/10/5"},
        "anon_model": "wallet keypair = identity; reputation = trust; no names, no KYC",
        "law": LAW,
        "artifacts": ARTIFACTS,
    }


def write_beacon() -> None:
    BEACON.parent.mkdir(parents=True, exist_ok=True)
    BEACON.write_text(json.dumps(build_beacon(), indent=2), encoding="utf-8")
    print(f"beacon written: {BEACON} ({len(ARTIFACTS)} artifacts, all {VERIFIED})")


def serve() -> int:
    write_beacon()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path in ("/", "/beacon", "/beacon.json"):
                body = BEACON.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, fmt: str, *args) -> None:
            print("beacon:", fmt % args, flush=True)

    print(f"serving the beacon on {SERVE_HOST}:{SERVE_PORT} (tailnet only) - ctrl-c to stop")
    ThreadingHTTPServer((SERVE_HOST, SERVE_PORT), Handler).serve_forever()
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["write", "serve", "inventory"])
    a = ap.parse_args()
    if a.cmd == "write":
        write_beacon()
        return 0
    if a.cmd == "inventory":
        for art in ARTIFACTS:
            v = art["verification"]
            print(f"[{art['type']:11s}] {art['name']:26s} price {art['price_gstd']} GSTD | verified: {v.get(VERIFIED) or v.get('live_read', '?')}")
        return 0
    if a.cmd == "serve":
        return serve()
    return 2


if __name__ == "__main__":
    sys.exit(main())
