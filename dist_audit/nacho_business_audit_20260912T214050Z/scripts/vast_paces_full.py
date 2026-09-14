"""vast_paces_full — rent, paces, gate, destroy. One shot, fully receipted.

The operator order (09-05): "really put that 5090 through the paces — serious fun
shit that gives us good data." This script IS the cook phase, hardened:
  select -> asks-door launch -> wait ollama live -> vast_paces suite (model ladder
  + concurrency ladder) -> ARENA-BENCH --live scores the box's 32B through the
  Blind Gate -> DESTROY -> receipts land in repo before the machine dies
  (Lessig: provenance crosses the border before jurisdiction closes).

SSRF hardening (Mimosa, guards defined in-file so they are auditable here):
every URL passes _guard() — scheme pinned to http/https, host allowlisted
(console.vast.ai for API) or public-IP-literal (bench box), DNS resolved with all
resolved IPs public (private/loopback/link-local/reserved refused), box endpoints
are IP literals (no DNS, no rebinding), redirects disabled on every call.

Run:  python scripts/vast_paces_full.py --arm        # money moves
      python scripts/vast_paces_full.py              # dry: select only
Kill-word: python state/vast/experiment.py teardown
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "state" / "vast"))
sys.path.insert(0, str(ROOT))

from experiment import select, _receipt, BOOT_TIMEOUT_S, MAX_COOK_USD  # noqa: E402
from launch_vast import balance, _h  # noqa: E402

API_HOST = "https://console.vast.ai"  # literal, the ONLY fleet-side host
API_HOSTNAME = "console.vast.ai"
BUNDLES_URL = API_HOST + "/api/v0/bundles/"
INSTANCES_URL = API_HOST + "/api/v0/instances/"
ASKS_URL = API_HOST + "/api/v0/asks/"
ARENA = ROOT / "mag" / "arena_bench.py"


def _guard(url: str, allow_hostnames: frozenset[str]) -> str:
    """SSRF gate: validate scheme, host, and every resolved IP before any request."""
    p = urlparse(url)
    if p.scheme not in ("http", "https"):
        raise RuntimeError(f"guard: bad scheme in {url[:80]}")
    host = p.hostname or ""
    if host in allow_hostnames:
        infos = socket.getaddrinfo(host, p.port or 443, proto=socket.IPPROTO_TCP)
        ips = {i[4][0] for i in infos}
    else:
        ips = {host}  # box endpoints must be IP literals — no DNS, no rebinding
    for s in ips:
        try:
            a = ipaddress.ip_address(s)
        except ValueError:
            raise RuntimeError(f"guard: non-IP host {host!r}")
        if (a.is_private or a.is_loopback or a.is_link_local or a.is_reserved
                or a.is_multicast or a.is_unspecified):
            raise RuntimeError(f"guard: non-public address refused: {s}")
    if p.username or p.password:
        raise RuntimeError("guard: userinfo in url refused")
    return url


def _api(path_suffix: str) -> str:
    """vast API url: literal base + int-forced path suffix, guarded."""
    return _guard(API_HOST + "/api/v0/" + path_suffix, frozenset({API_HOSTNAME}))


def _box(ip: str, port: int, path: str) -> str:
    """Box endpoint url: public IP literal + port + /api/ path, guarded."""
    a = ipaddress.ip_address(str(ip))  # raises if not an IP literal
    if not (0 < int(port) < 65536) or not path.startswith("/api/"):
        raise RuntimeError("guard: bad box endpoint path/port")
    return _guard(f"http://{a}:{int(port)}{path}", frozenset())


def _wait_live(inst_id: int, deadline_s: int) -> tuple[str | None, float]:
    """Poll until the box's ollama answers; endpoint built via _box guard."""
    t0 = time.time()
    while time.time() - t0 < deadline_s:
        insts = requests.get(_api("instances/"), headers=_h(), timeout=60,
                             allow_redirects=False).json().get("instances", [])
        inst = next((i for i in insts if int(i.get("id", 0)) == inst_id), None)
        if inst and inst.get("actual_status") in ("running", "ok"):
            m = (inst.get("ports") or {}).get("11434") or {}
            if m.get("ip") and m.get("host_port"):
                try:
                    if requests.get(_box(m["ip"], int(m["host_port"]), "/api/tags"),
                                    timeout=8, allow_redirects=False).status_code == 200:
                        return _box(m["ip"], int(m["host_port"]), "/api"), time.time() - t0
                except Exception:
                    pass
        time.sleep(20)
    return None, time.time() - t0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", action="store_true")
    args = ap.parse_args()

    box = select()
    if not box:
        print("no box meets rails — abort")
        return 2
    print(f"select: {box}", flush=True)
    if not args.arm:
        print("dry-run: nothing spent")
        return 0
    if balance() < 5:
        print("credit < $5 — refusing")
        return 2

    _receipt("paces_launch", box=box, ceiling_usd=MAX_COOK_USD)
    body = {"image": "ollama/ollama:latest", "disk": 40, "label": "arena-cook",
            "env": {"OLLAMA_HOST": "0.0.0.0:11434"}, "onstart": "echo BOX-UP"}
    ok = None
    for attempt in (1, 2):
        r = requests.put(_api(f"asks/{int(box['id'])}/"), headers=_h(),
                         data=json.dumps(body), timeout=60, allow_redirects=False)
        if r.status_code in (200, 201):
            ok = r.json()
            break
        _receipt("launch_fail", attempt=attempt, status=r.status_code, body=r.text[:150])
    if not ok:
        _receipt("abort_two_failures", box=box)
        return 2
    inst_id = int(ok.get("new_contract") or ok.get("new_instance_id") or box["id"])
    t_start = time.time()

    ep, boot_s = _wait_live(inst_id, BOOT_TIMEOUT_S)
    if not ep:
        _receipt("boot_timeout", inst_id=inst_id, waited_s=round(boot_s, 1))
        requests.delete(_api(f"instances/{int(inst_id)}/"), headers=_h(), timeout=60,
                        allow_redirects=False)
        _receipt("destroyed", inst_id=inst_id, reason="boot_timeout")
        return 2
    _receipt("boot_ok", inst_id=inst_id, boot_s=round(boot_s, 1), endpoint=ep)

    # THE PACES — model ladder + concurrency ladder
    pr = subprocess.run([sys.executable, str(ROOT / "scripts" / "vast_paces.py"),
                         "--endpoint", ep], capture_output=True, text=True, timeout=5400)
    _receipt("paces_suite_done", inst_id=inst_id, rc=pr.returncode,
             tail=(pr.stdout or "")[-600:])

    # THE GATE SCORES THE BOX — Blind Gate vs the biggest ladder model, on hardware
    ar = subprocess.run([sys.executable, str(ARENA), "--live", "--candidate",
                         "qwen2.5:32b-5090", "--endpoint", ep, "--model",
                         "qwen2.5:32b-instruct-q4_K_M"],
                        capture_output=True, text=True, timeout=1800)
    _receipt("arena_on_box", inst_id=inst_id, rc=ar.returncode,
             tail=(ar.stdout or "")[-600:])

    spend = box["dph"] * (time.time() - t_start + boot_s) / 3600
    requests.delete(_api(f"instances/{int(inst_id)}/"), headers=_h(), timeout=60,
                    allow_redirects=False)
    _receipt("destroyed", inst_id=inst_id, est_total_usd=round(spend, 2),
             ceiling_usd=MAX_COOK_USD)
    return 0


if __name__ == "__main__":
    sys.exit(main())
