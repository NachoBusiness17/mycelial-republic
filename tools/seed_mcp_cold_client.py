#!/usr/bin/env python3
"""seed_mcp_cold_client.py - the B2-181 falsifier driver (2026-09-26).

Plays a COLD agent session against the seed-mcp server over real stdio
JSON-RPC. Cold discipline, asserted here: this process NEVER opens the seed
file or any estate path. Every byte it did not mint itself arrives through
MCP (resources/read or tool results). It may read only its own workspace.

Sequence: initialize -> resources/list -> read the 3 resources ->
rebuild_subtree -> verify_hash per rebuilt inline file -> fetch_bounded_pointer
per pointer entry -> join_protocol -> prove the subtree is WORKING by running
the rebuilt tools/seed_rib.py (rebuild #2 from the saved seed, exit 0).

Exit 0 = COLD JOIN PASS (falsifier survived), 1 = FAIL, 2 = cannot verify.

  .venv/Scripts/python.exe tools/seed_mcp_cold_client.py \
      --seed watch/inbox/SEED_RIB_CURRENT_20260926.json --source .
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


class ColdClient:
    def __init__(self, python: str, server: Path, seed: str, source: str):
        self.proc = subprocess.Popen(
            [python, str(server), "--seed", seed, "--source", source],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding="utf-8")
        self._next_id = 0

    def call(self, method: str, params: dict | None = None) -> dict:
        self._next_id += 1
        rid = self._next_id
        req = {"jsonrpc": "2.0", "id": rid, "method": method}
        if params is not None:
            req["params"] = params
        assert self.proc.stdin is not None and self.proc.stdout is not None
        self.proc.stdin.write(json.dumps(req) + "\n")
        self.proc.stdin.flush()
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError(f"server closed during {method}")
            msg = json.loads(line)
            if msg.get("id") == rid:
                if "error" in msg:
                    raise RuntimeError(f"{method} rpc error: {msg['error']}")
                return msg["result"]

    def notify(self, method: str) -> None:
        assert self.proc.stdin is not None
        self.proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": method}) + "\n")
        self.proc.stdin.flush()

    def tool(self, name: str, arguments: dict) -> dict:
        res = self.call("tools/call", {"name": name, "arguments": arguments})
        text = res["content"][0]["text"]
        value = json.loads(text)
        if res.get("isError"):
            raise RuntimeError(f"{name} tool error: {value}")
        return value

    def close(self) -> None:
        if self.proc.stdin:
            self.proc.stdin.close()
        self.proc.wait(timeout=10)


def main() -> int:
    ap = argparse.ArgumentParser(description="cold-agent MCP join falsifier")
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--server", default="tools/seed_mcp.py")
    ap.add_argument("--seed", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--workspace", default=None)
    args = ap.parse_args()
    ws = Path(args.workspace) if args.workspace else Path(tempfile.mkdtemp(prefix="seed_cold_"))
    ws.mkdir(parents=True, exist_ok=True)
    checks: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str) -> None:
        checks.append((name, ok, detail))
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    client = ColdClient(args.python, Path(args.server), args.seed, args.source)
    try:
        init = client.call("initialize", {"protocolVersion": "2025-06-18",
                                          "capabilities": {}, "clientInfo": {"name": "cold"}})
        client.notify("notifications/initialized")
        check("initialize", init["serverInfo"]["name"] == "seed-rib",
              f"server {init['serverInfo']['name']} v{init['serverInfo']['version']}")

        res = client.call("resources/list")["resources"]
        uris = sorted(r["uri"] for r in res)
        check("resources_list", uris == ["seed://brief-pointers", "seed://current",
                                         "seed://law-registry"], f"{len(res)} resources {uris}")

        seed_text = client.call("resources/read", {"uri": "seed://current"})["contents"][0]["text"]
        seed = json.loads(seed_text)
        check("read_seed", seed.get("schema") == "seed_rib.v0",
              f"schema seed_rib.v0, {len(seed.get('entries', []))} entries")
        (ws / "seed.json").write_text(seed_text, encoding="utf-8")

        law_reg = json.loads(client.call("resources/read",
                                         {"uri": "seed://law-registry"})["contents"][0]["text"])
        check("read_law_registry", all(lid in law_reg for lid in seed.get("law_refs", [])),
              f"{len(seed.get('law_refs', []))} law_refs all present in the registry resource")

        briefs = json.loads(client.call("resources/read",
                                        {"uri": "seed://brief-pointers"})["contents"][0]["text"])
        check("read_brief_pointers",
              all(p["sha256"] for p in briefs.get("pointers", [])),
              f"{len(briefs.get('pointers', []))} sealed brief pointers")

        rebuilt = ws / "rebuilt"
        rb = client.tool("rebuild_subtree", {"into": str(rebuilt)})
        check("rebuild_subtree", rb["ok"] and rb["inline_ok"] == rb["inline_total"],
              f"inline {rb['inline_ok']}/{rb['inline_total']} hash-matched, "
              f"pointers {rb['pointer_total']} ({rb['pointer_source_checked']} source-checked, "
              f"{rb['pointer_unresolved']} stubbed), mismatches {rb['mismatches']}")

        bad = 0
        for e in seed.get("entries", []):
            if e.get("carrier") != "inline":
                continue
            vh = client.tool("verify_hash", {"path": e["path"], "root": str(rebuilt)})
            if not (vh["ok"] and vh["matches_seed"]):
                bad += 1
        check("verify_hash_spotcheck", bad == 0,
              f"{rb['inline_total']} rebuilt inline files verified against seals, {bad} bad")

        served = 0
        for e in seed.get("entries", []):
            if e.get("carrier") == "pointer":
                fp = client.tool("fetch_bounded_pointer", {"path": e["path"]})
                if fp.get("served"):
                    raw = base64.b64decode(fp["bytes_b64"])
                    if hashlib.sha256(raw).hexdigest() == e["sha256"]:
                        out = ws / "bounded" / e["path"]
                        out.parent.mkdir(parents=True, exist_ok=True)
                        out.write_bytes(raw)
                        served += 1
        check("fetch_bounded_pointer", served == rb["pointer_total"],
              f"{served}/{rb['pointer_total']} pointer entries fetched seal-checked")

        join = client.tool("join_protocol", {})
        check("join_protocol", join["schema"] == "seed_join.v0" and len(join["steps"]) == 7
              and join["law_refs"] == seed.get("law_refs", []),
              f"{len(join['steps'])} steps, law_refs {len(join['law_refs'])}")

        # Working-subtree proof: the REBUILT seed_rib.py runs and re-verifies
        # the seed (rebuild #2), entirely inside the workspace.
        rebuilt_tool = rebuilt / "tools" / "seed_rib.py"
        r2 = ws / "rebuilt2"
        run = subprocess.run([args.python, str(rebuilt_tool), "verify", "--seed",
                              str(ws / "seed.json"), "--into", str(r2)],
                             capture_output=True, text=True)
        check("working_subtree", run.returncode == 0,
              f"rebuilt tools/seed_rib.py re-verified the seed: "
              f"{run.stdout.strip().splitlines()[-1] if run.stdout.strip() else run.stderr.strip()}")

        failed = [c for c in checks if not c[1]]
        print(f"\nCOLD JOIN {'PASS' if not failed else 'FAIL'}: {len(checks) - len(failed)}/{len(checks)} checks, workspace {ws}")
        return 0 if not failed else 1
    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(main())
