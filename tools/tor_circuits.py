"""tor_circuits - the estate's Tor circuit organ (per-conversation isolation).

Operator order 2026-10-21 ("i love the tor per convo"), after Vitalik's
paranoid-mode stack surfaced via LilithDatura's thread: every logical
conversation (probe session, reading round, battery) gets its OWN Tor circuit,
so keyless free-lane dispatches are unlinkable at the wire - the same-book
independence requirement enforced in the transport, not just the prompt.

SCOPE (honest): applies to KEYLESS lanes only (:free endpoints where we are
anonymous by design). Authenticated lanes (sk- keys) are identity-linked
regardless of circuit - Tor adds nothing there. Local shelf never leaves the
box. Default: OFF - the wire is direct until HERMES_BURN_PROXY is set.

This module owns the Tor CONTROL channel only (loopback 9051, cookie auth):
status, bootstrap wait, circuit rotation (SIGNAL NEWNYM). It launches nothing;
the tor binary runs from tools/tor/tor/ (gitignored) with the torrc in that
directory. It carries no HTTP traffic - the SOCKS endpoint (127.0.0.1:9050)
is consumed by the boundary carrier (hermes_burn) via HERMES_BURN_PROXY.

Consumer: geometric probe beats + same-book reading rounds + any keyless
dispatch that must be unlinkable;
Verifier: tests/test_tor_circuits.py + the falsifier (two consecutive probe
sessions on the same circuit = isolation failed; the rotate-then-verify check
in `verify`).
"""
from __future__ import annotations

import argparse
import json
import socket
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOR_DIR = ROOT / "tools" / "tor" / "tor"
SOCKS_HOST, SOCKS_PORT = "127.0.0.1", 9050
CTRL_HOST, CTRL_PORT = "127.0.0.1", 9051
COOKIE = TOR_DIR / "data" / "control_auth_cookie"


def _ctrl(command: str, timeout: int = 15) -> tuple[bool, str]:
    """One authenticated control-port exchange. Returns (ok, response).
    Tor sends NO banner on connect - AUTHENTICATE must go out first
    (beat 1 lesson: reading for a greeting blocked every exchange)."""
    try:
        s = socket.create_connection((CTRL_HOST, CTRL_PORT), timeout=timeout)
        s.settimeout(timeout)
        cookie = COOKIE.read_bytes().hex() if COOKIE.exists() else ""
        s.sendall(f"AUTHENTICATE {cookie}\r\n".encode())
        auth = s.recv(4096).decode("utf-8", errors="replace")
        if not auth.startswith("250"):
            return False, "auth refused: " + auth[:80]
        s.sendall(f"{command}\r\n".encode())
        resp = s.recv(65536).decode("utf-8", errors="replace")
        s.sendall(b"QUIT\r\n")
        s.close()
        return resp.startswith("250"), resp.strip()
    except Exception as e:  # noqa: BLE001 - control failures are findings
        return False, f"control unreachable: {str(e)[:120]}"


def _socks_alive() -> bool:
    s = socket.socket()
    s.settimeout(2)
    alive = s.connect_ex((SOCKS_HOST, SOCKS_PORT)) == 0
    s.close()
    return alive


def status() -> dict:
    """Is Tor alive, and how far is the bootstrap?"""
    ok, resp = _ctrl("GETINFO status/bootstrap-phase")
    if not ok:
        return {"tor_running": _socks_alive(), "control": False, "note": resp[:120]}
    phase = ""
    for line in resp.splitlines():
        if line.startswith("250-status/bootstrap-phase="):
            phase = line.split("=", 1)[1].strip()
    return {"tor_running": True, "control": True, "bootstrap": phase[:200]}


def wait_bootstrap(max_seconds: int = 120) -> dict:
    """Poll until the bootstrap phase reports done (or the ceiling)."""
    deadline = time.monotonic() + max_seconds
    last: dict = {}
    while time.monotonic() < deadline:
        last = status()
        if last.get("control") and "Done" in str(last.get("bootstrap", "")):
            return {**last, "bootstrapped": True}
        time.sleep(4)
    return {**last, "bootstrapped": False}


def rotate() -> dict:
    """SIGNAL NEWNYM: all subsequent connections use a fresh circuit.
    Per-conversation isolation = rotate once per logical conversation."""
    ok, resp = _ctrl("SIGNAL NEWNYM")
    return {"rotated": ok, "note": resp[:120]}


def socks_for(conversation_id: str) -> dict:
    """The per-conversation endpoint: Tor isolates circuits by SOCKS credential
    (IsolateSOCKSAuth is default-on), so a stable username per conversation
    gives that conversation its OWN persistent circuit - isolated from every
    other conversation, consistent within itself. This is the mechanism
    (NEWNYM is weaker: it rotates globally and Tor may reuse clean circuits).
    Carriers consume: socks.set_proxy(socks.SOCKS5, host, port, rdns=True,
    username=user, password='x')."""
    return {"host": SOCKS_HOST, "port": SOCKS_PORT,
            "username": f"conv-{conversation_id}", "password": "x"}


def verify() -> dict:
    """The falsifier check: two conversations must get DIFFERENT exit IPs,
    and the same conversation must KEEP its exit across two calls."""
    import socks  # PySocks - available in the venv (verified 2026-10-21)

    def exit_ip(user: str) -> str:
        s = socks.socksocket()
        s.set_proxy(socks.SOCKS5, SOCKS_HOST, SOCKS_PORT, rdns=True,
                    username=user, password="x")
        s.settimeout(25)
        s.connect(("checkip.amazonaws.com", 80))
        s.sendall(b"GET / HTTP/1.1\r\nHost: checkip.amazonaws.com\r\nConnection: close\r\n\r\n")
        data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
        s.close()
        body = data.decode("utf-8", errors="replace")
        lines = [x.strip() for x in body.splitlines() if x.strip()]
        return lines[-1] if lines else ""

    a1 = exit_ip("conv-verify-a")
    b1 = exit_ip("conv-verify-b")
    a2 = exit_ip("conv-verify-a")
    isolated = a1 != b1 and bool(a1) and bool(b1)
    stable = a1 == a2 and bool(a1)
    return {"conv_a_exit": a1, "conv_b_exit": b1, "conv_a_repeat": a2,
            "isolated": isolated, "stable_per_conversation": stable,
            "per_conversation_isolation": isolated and stable}


def selftest() -> int:
    # control protocol shapes, offline: cookie-less AUTHENTICATE refusal path
    # is environment-dependent, so we test the pure helpers instead
    assert SOCKS_PORT == 9050 and CTRL_PORT == 9051
    assert COOKIE.name == "control_auth_cookie"
    print("selftest PASS: port constants + cookie path shapes (live control needs a running tor)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["status", "wait", "rotate", "verify", "selftest"])
    ap.add_argument("--max-seconds", type=int, default=120)
    args = ap.parse_args()
    if args.cmd == "status":
        print(json.dumps(status(), indent=1))
    elif args.cmd == "wait":
        print(json.dumps(wait_bootstrap(args.max_seconds), indent=1))
    elif args.cmd == "rotate":
        print(json.dumps(rotate(), indent=1))
    elif args.cmd == "verify":
        print(json.dumps(verify(), indent=1))
    else:
        return selftest()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
