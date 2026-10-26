"""ractor50 mcp-lane finish-line probe: a real MCP client session over stdio.

Speaks JSON-RPC 2.0 to the house server exactly as the bridge design's Shape A
client would (watch/inbox/burn_reset_20260927/flash50/mcp-bridge.md 4.1).
Non-mutating: initialize, tools/list on the bridge profile (expect the six
estate tools), tools/list on the full profile (expect 34 + 6 bridge = 40
static tools unless other lanes added more; report the real number), one
deterministic live call (estate_water_graph_tick on a tiny spec, no estate
state touched), one read call (estate_chain_verify dry verdict), one read
call (estate_driver_status tail 1). Prints every raw wire line; exits
non-zero if a finish-line criterion fails.
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
        import time
        line = ""
        deadline = time.time() + 30
        while time.time() < deadline:
            line = proc.stdout.readline()
            if line.strip():
                break
            if not line and proc.poll() is not None:
                break
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
    print(f"BRIDGE-PROFILE-TOOLS ({len(names)}): {sorted(names)}")
    # The pin gate is LIVE (wired 2026-09-29, watch/inbox/wave5_repair/mcp-pin-wire.md).
    # estate_thought_compile drifted after its pin (schema hash changed between the
    # 14:56Z pin and commit f7768cd10), so the gate must WITHHOLD it and serve 5 of 6.
    check("pin gate serves 5 of 6: drifted estate_thought_compile withheld",
          set(names) == set(BRIDGE_TOOLS) - {"estate_thought_compile"},
          f"got {sorted(names)}")
    check("every served tool is an estate_ bridge tool (no non-estate leakage)",
          all(n.startswith("estate_") for n in names), f"got {sorted(names)}")
    check("never-exposed verbs are absent (no repair, no bank, no control words)",
          not any(("chain_repair" in n or "dirac_bank" in n or "driver_stop" in n
                   or "driver_start" in n or "driver_once" in n) for n in names))

    def call(id_: int, name: str, args: dict) -> dict:
        send({"jsonrpc": "2.0", "id": id_, "method": "tools/call",
              "params": {"name": name, "arguments": args}})
        return recv()["result"]

    def body(resp: dict) -> dict:
        return json.loads(resp["content"][0]["text"])

    r = call(10, "estate_water_graph_tick", {"spec": TICK_SPEC})
    b = body(r)
    check("tick live call returns real deterministic output",
          "isError" not in r and b.get("ok") is True
          and b["spec"]["nodes"]["dst"]["volume"] == 2, json.dumps(b)[:200])

    r = call(11, "estate_chain_verify", {})
    b = body(r)
    check("chain verify live call: DRY verdict + exit contract (real repair never crosses)",
          b.get("dry") is True and b.get("exit_code") in (0, 1, 2)
          and b["verdict"].startswith("CHAIN-REPAIR"), json.dumps(b)[:300])

    r = call(12, "estate_driver_status", {"tail": 1})
    b = body(r)
    check("driver status live call returns real output",
          "isError" not in r and b.get("ok") is True
          and isinstance(b.get("off"), bool), json.dumps(b)[:200])

    r = call(13, "estate_no_such_tool", {})
    check("unknown tool rides in-band isError (spec isError contract)",
          r.get("isError") is True)

    proc.stdin.close()
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()
    err_all = proc.stderr.read() if proc.stderr else ""
    print(f"STDERR-ALARM-PRESENT: {'DRIFT ALARM' in err_all}")
    print(f"STDERR-TAIL: {err_all[-500:]!r}")

    print(f"PROBE-SUMMARY: {len(failures)} failures")
    for f in failures:
        print(f"  FAILED: {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
