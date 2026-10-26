"""Bridge R1 finish-line probe: a real MCP client session over stdio.

Speaks JSON-RPC 2.0 to the house server (`python -m mag.mcp_server --profile
bridge`) exactly as the design's Shape A client would
(watch/inbox/burn_reset_20260927/flash50/mcp-bridge.md 4.1): initialize,
notifications/initialized, tools/list, then one live tools/call per estate
tool plus bad-input calls for the error shapes. Prints every raw wire line;
exits non-zero if any finish-line criterion fails.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3].parents[1]
PY = ROOT / ".venv" / "Scripts" / "python.exe"
BRIDGE_TOOLS = [
    "estate_water_graph_tick", "estate_dirac_scan", "estate_dirac_rank",
    "estate_chain_verify", "estate_thought_compile", "estate_driver_status",
]
TICK_SPEC = {
    "schema": "water_graph.v1", "tick": 0,
    "nodes": {"src": {"elev": 3, "kind": "plain", "volume": 5},
              "dst": {"elev": 0, "kind": "plain", "volume": 0}},
    "pipes": {"p1": {"src": "src", "dst": "dst", "cap": 2}},
}

failures: list[str] = []


def check(label: str, cond: bool, detail: str = "") -> None:
    print(f"PROBE-CHECK {'PASS' if cond else 'FAIL'}: {label}"
          + (f" :: {detail}" if detail and not cond else ""))
    if not cond:
        failures.append(label)


def main() -> int:
    proc = subprocess.Popen(
        [str(PY), "-m", "mag.mcp_server", "--profile", "bridge"],
        cwd=str(ROOT), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, encoding="utf-8")

    def send(msg: dict) -> None:
        line = json.dumps(msg, ensure_ascii=False)
        print(f">>> {line}")
        proc.stdin.write(line + "\n")
        proc.stdin.flush()

    def recv() -> dict:
        line = proc.stdout.readline()
        print(f"<<< {line.rstrip()}")
        return json.loads(line)

    send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init = recv()
    check("initialize answers with mag-tool-map",
          init.get("result", {}).get("serverInfo", {}).get("name") == "mag-tool-map")
    send({"jsonrpc": "2.0", "method": "notifications/initialized"})
    send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    listing = recv()
    names = [t["name"] for t in listing["result"]["tools"]]
    check("tools/list shows the estate bridge tools",
          all(n in names for n in BRIDGE_TOOLS),
          f"got {names}")
    check("tools/list shows ONLY the estate bridge tools on the bridge profile",
          set(names) == set(BRIDGE_TOOLS), f"got {sorted(set(names) ^ set(BRIDGE_TOOLS))}")

    def call(id_: int, name: str, args: dict) -> dict:
        send({"jsonrpc": "2.0", "id": id_, "method": "tools/call",
              "params": {"name": name, "arguments": args}})
        return recv()["result"]

    def body(resp: dict) -> dict:
        return json.loads(resp["content"][0]["text"])

    r = call(10, "estate_water_graph_tick", {"spec": TICK_SPEC})
    b = body(r)
    check("tick live call returns real output",
          "isError" not in r and b.get("ok") is True
          and b["spec"]["nodes"]["dst"]["volume"] == 2, json.dumps(b)[:200])
    r = call(11, "estate_water_graph_tick", {"spec": {}})
    check("tick bad spec rides isError",
          r.get("isError") is True and body(r).get("ok") is False)

    r = call(12, "estate_dirac_scan", {"scope": "operational"})
    b = body(r)
    check("dirac scan live call returns real output",
          "isError" not in r and b.get("ok") is True
          and isinstance(b.get("betti1"), int), json.dumps(b)[:200])
    r = call(13, "estate_dirac_scan", {"scope": "internet"})
    check("dirac bad scope rides isError",
          r.get("isError") is True and "scope must be one of" in body(r)["error"])

    r = call(14, "estate_dirac_rank", {"scope": "operational"})
    b = body(r)
    check("dirac rank live call returns real output",
          "isError" not in r and b.get("ok") is True and "beta1" in b,
          json.dumps(b)[:200])

    r = call(15, "estate_chain_verify", {})
    b = body(r)
    check("chain verify live call: dry verdict + exit contract",
          b.get("dry") is True and b.get("exit_code") in (0, 1, 2)
          and b["verdict"].startswith("CHAIN-REPAIR"), json.dumps(b)[:300])

    r = call(16, "estate_thought_compile", {})
    b = body(r)
    check("thought compile live call returns real output",
          "isError" not in r and b.get("ok") is True
          and b.get("report", {}).get("stats", {}).get("kept", 0) >= 0
          and b.get("pinned") is True, json.dumps(b)[:200])

    evil = ROOT / "watch/inbox/gala_20260925/ball-20260929/lanes/_bridge_probe_evil_out"
    r = call(17, "estate_thought_compile", {"out": str(evil)})
    check("compile caller-supplied out path refused with isError",
          r.get("isError") is True and "bridge pin" in body(r)["error"]
          and not evil.exists())

    r = call(18, "estate_driver_status", {"tail": 2})
    b = body(r)
    check("driver status live call returns real output",
          "isError" not in r and b.get("ok") is True
          and isinstance(b.get("off"), bool), json.dumps(b)[:200])

    r = call(19, "estate_no_such_tool", {})
    check("unknown tool rides in-band isError",
          r.get("isError") is True)

    proc.stdin.close()
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()

    print(f"PROBE-SUMMARY: {len(failures)} failures")
    for f in failures:
        print(f"  FAILED: {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
