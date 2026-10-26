#!/usr/bin/env python3
"""Q-039 bind+respond proof for tools/roblox_npc_gateway.py.

Runs the REAL entrypoint as a subprocess (no imports of its classes) in three
phases and prints one PASS/FAIL line per claim. Exit 0 only if every claim
passes. Banked next to this receipt: watch/inbox/burn_reset_20260927/queue/

Phase A  fail-closed: 0.0.0.0 bind with NO secret must refuse to start.
Phase B  public serve: 0.0.0.0 + NPC_GATEWAY_SECRET must
           b1 listen on 0.0.0.0:8771 (netstat byte evidence)
           b2 answer 401 with no auth header
           b3 answer 401 with a wrong secret
           b4 answer 200 JSON for correct secret + unknown head (no lane call)
           b5 answer 200 via the ask_lane free-family gate for a non-allowlisted
              model (deepest no-outbound path; writes one lane="gate" receipt row)
           b6 answer 413 for a body over the 64 KiB cap
           b7 answer 200 when reached on the host's LAN IP (off-loopback proof)
Phase C  backward compat: 127.0.0.1 with NO secret still serves auth-free.
"""
from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
GATEWAY = os.path.join(ROOT, "tools", "roblox_npc_gateway.py")
assert os.path.isfile(GATEWAY), f"gateway not found at {GATEWAY}"
PY = sys.executable  # proof is itself run with .venv\Scripts\python.exe
PORT = 8771
SECRET = "q039-proof-secret-7f3a"
CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0

results: list[tuple[bool, str]] = []


def check(ok: bool, label: str, detail: str = "") -> None:
    results.append((ok, label))
    print(f"{'PASS' if ok else 'FAIL'}  {label}" + (f"  | {detail}" if detail else ""))


def spawn(env_extra: dict) -> subprocess.Popen:
    env = dict(os.environ)
    env.update(env_extra)
    env["PYTHONUNBUFFERED"] = "1"  # else the child's banner sits in the pipe buffer and readline() blocks
    return subprocess.Popen(
        [PY, GATEWAY], cwd=ROOT, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, creationflags=CREATE_NO_WINDOW)


def wait_port(timeout: float = 10.0) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        with socket.socket() as s:
            s.settimeout(0.3)
            if s.connect_ex(("127.0.0.1", PORT)) == 0:
                return True
        time.sleep(0.15)
    return False


def wait_port_free(timeout: float = 10.0) -> bool:
    """Windows SO_REUSEADDR lets a new bind land on a dying socket's port; the
    next phase may only start once the old listener is actually gone."""
    end = time.time() + timeout
    while time.time() < end:
        with socket.socket() as s:
            s.settimeout(0.3)
            if s.connect_ex(("127.0.0.1", PORT)) != 0:
                return True
        time.sleep(0.15)
    return False


def post(url: str, body: dict, auth: str | None, timeout: float = 5.0) -> tuple[int, str]:
    headers = {"Content-Type": "application/json"}
    if auth is not None:
        headers["Authorization"] = auth
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
    except urllib.error.URLError as e:
        return -1, f"<urlopen error: {e}>"


def lan_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # no packet leaves; just picks the default-route IP
        return s.getsockname()[0]
    finally:
        s.close()


# ---- Phase A: fail-closed public bind without secret -----------------------
proc_a = spawn({"NPC_GATEWAY_HOST": "0.0.0.0"})
try:
    out, _ = proc_a.communicate(timeout=15)
    refused = proc_a.returncode != 0 and "refusing public bind" in (out or "")
    check(refused, "A fail-closed: 0.0.0.0 without NPC_GATEWAY_SECRET refuses to start",
          f"rc={proc_a.returncode}")
finally:
    if proc_a.poll() is None:
        proc_a.kill()

# ---- Phase B: public serve with secret -------------------------------------
proc_b = spawn({"NPC_GATEWAY_HOST": "0.0.0.0", "NPC_GATEWAY_SECRET": SECRET})
try:
    check(wait_port(), "B0 server accepts connections on port 8771")
    banner = ""
    try:
        banner = proc_b.stdout.readline().strip() if proc_b.stdout else ""
    except Exception:
        pass
    print(f"      banner: {banner}")

    ns = subprocess.run(["netstat", "-ano"], capture_output=True, text=True,
                        creationflags=CREATE_NO_WINDOW).stdout
    b1 = f"0.0.0.0:{PORT}" in ns and "LISTENING" in ns
    check(b1, "B1 netstat shows LISTENING on 0.0.0.0:8771 (non-localhost bind)")

    code, _ = post(f"http://127.0.0.1:{PORT}/npc", {"head": "nobody"}, auth=None)
    check(code == 401, "B2 POST with no Authorization -> 401", f"got {code}")
    code, _ = post(f"http://127.0.0.1:{PORT}/npc", {"head": "nobody"}, auth="Bearer wrong-secret")
    check(code == 401, "B3 POST with wrong secret -> 401", f"got {code}")
    code, body = post(f"http://127.0.0.1:{PORT}/npc", {"head": "nobody"}, auth=f"Bearer {SECRET}")
    ok4 = code == 200 and "no such head" in body
    check(ok4, "B4 correct secret + unknown head -> 200 JSON", f"{code} {body[:80]}")
    code, body = post(f"http://127.0.0.1:{PORT}/npc",
                      {"head": "elder", "model": "gpt-4"}, auth=f"Bearer {SECRET}")
    ok5 = code == 200 and "free families" in body
    check(ok5, "B5 correct secret + non-allowlisted model -> 200 via free-family gate",
          f"{code} {body[:80]}")
    code, body = post(f"http://127.0.0.1:{PORT}/npc",
                      {"head": "elder", "message": "x" * 70000}, auth=f"Bearer {SECRET}")
    check(code == 413, "B6 body over 64 KiB cap -> 413", f"got {code}")

    ip = lan_ip()
    code, body = post(f"http://{ip}:{PORT}/npc", {"head": "nobody"}, auth=f"Bearer {SECRET}")
    check(code == 200 and "no such head" in body,
          f"B7 reached on LAN IP {ip} (off-loopback)", f"{code} {body[:60]}")
finally:
    proc_b.terminate()
    try:
        proc_b.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc_b.kill()

# ---- Phase C: loopback dev without secret unchanged ------------------------
check(wait_port_free(), "C-pre port released before loopback phase")
proc_c = spawn({"NPC_GATEWAY_HOST": "127.0.0.1"})
try:
    check(wait_port(), "C0 loopback server accepts connections")
    code, body = post(f"http://127.0.0.1:{PORT}/npc", {"head": "nobody"}, auth=None)
    check(code == 200 and "no such head" in body,
          "C1 127.0.0.1 with no secret still serves auth-free (local dev unchanged)",
          f"{code} {body[:60]}")
finally:
    proc_c.terminate()
    try:
        proc_c.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc_c.kill()

passed = sum(1 for ok, _ in results if ok)
print(f"\n{passed}/{len(results)} claims pass")
sys.exit(0 if passed == len(results) else 1)
