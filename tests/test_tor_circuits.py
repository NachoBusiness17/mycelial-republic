"""Tests for tools/tor_circuits.py - shapes and the socks credential contract.
Live control tests need a running tor; this file tests the pure parts.
Verifier: this file. Consumer: module docstring."""
from __future__ import annotations

from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import tor_circuits as tc  # noqa: E402


def test_ports_and_cookie_contract():
    assert tc.SOCKS_PORT == 9050 and tc.CTRL_PORT == 9051
    assert tc.COOKIE.name == "control_auth_cookie"
    assert tc.TOR_DIR.name == "tor"


def test_socks_for_gives_stable_per_conversation_credential():
    a = tc.socks_for("same-book-round3")
    a2 = tc.socks_for("same-book-round3")
    b = tc.socks_for("other-round")
    assert a["username"] == a2["username"] != b["username"]
    assert a["host"] == "127.0.0.1" and a["port"] == 9050
    # the credential is what tor isolates circuits by
    assert a["username"].startswith("conv-")


def test_verify_shapes_without_live_tor(monkeypatch):
    calls = []

    def fake_ctrl(cmd, timeout=15):
        calls.append(cmd)
        if cmd.startswith("SIGNAL"):
            return True, "250 OK"
        return True, '250-status/bootstrap-phase=NOTICE BOOTSTRAP PROGRESS=100 TAG=done SUMMARY="Done"'

    monkeypatch.setattr(tc, "_ctrl", fake_ctrl)
    st = tc.status()
    assert st["tor_running"] is True and st["control"] is True
    rot = tc.rotate()
    assert rot["rotated"] is True


def test_status_honest_when_tor_down(monkeypatch):
    monkeypatch.setattr(tc, "_ctrl", lambda cmd, timeout=15: (False, "control unreachable: timed out"))
    monkeypatch.setattr(tc, "_socks_alive", lambda: False)
    st = tc.status()
    assert st["tor_running"] is False and "unreachable" in st["note"]
