"""Passive lifecycle — on/off policy for stack pieces."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def test_build_lifecycle_schema():
    from mag.lifecycle import build_lifecycle

    lc = build_lifecycle()
    assert lc.get("schema") == "mag_lifecycle.v1"
    assert lc.get("ok") is True
    assert "pieces" in lc
    assert "posture" in lc
    ids = {p["id"] for p in lc["pieces"]}
    for need in ("backend", "dashboard", "lab", "drainer", "remote_seats", "browser_env"):
        assert need in ids
    for p in lc["pieces"]:
        assert p["should"] in ("on", "off")
        assert p["actual"] in ("on", "off")
        assert "token_class" in p
        assert "mode" in p


def test_remote_seats_passive_by_default():
    from mag.lifecycle import PIECE_DEFS, _policy_should

    remote = next(p for p in PIECE_DEFS if p["id"] == "remote_seats")
    should, reason = _policy_should(
        remote,
        power_off=False,
        wanted={},
        queue_depth=0,
        fleet_running=0,
        operator_active=False,
        drainer_allowed=False,
        browser_enabled=False,
    )
    assert should is False
    assert "idle" in reason.lower() or "never" in reason.lower() or "Passive" in reason or "off" in reason.lower()


def test_drainer_off_when_queue_empty():
    from mag.lifecycle import PIECE_DEFS, _policy_should

    drain = next(p for p in PIECE_DEFS if p["id"] == "drainer")
    should, _ = _policy_should(
        drain,
        power_off=False,
        wanted={"drainer": True},
        queue_depth=0,
        fleet_running=0,
        operator_active=False,
        drainer_allowed=True,
        browser_enabled=False,
    )
    assert should is False  # passive — no work to drain


def test_drainer_on_when_queue_and_allowed():
    from mag.lifecycle import PIECE_DEFS, _policy_should

    drain = next(p for p in PIECE_DEFS if p["id"] == "drainer")
    should, _ = _policy_should(
        drain,
        power_off=False,
        wanted={"drainer": True},
        queue_depth=2,
        fleet_running=0,
        operator_active=False,
        drainer_allowed=True,
        browser_enabled=False,
    )
    assert should is True


def test_power_off_forces_all_should_off():
    from mag.lifecycle import PIECE_DEFS, _policy_should

    for defn in PIECE_DEFS:
        should, reason = _policy_should(
            defn,
            power_off=True,
            wanted={"backend": True, "drainer": True},
            queue_depth=5,
            fleet_running=3,
            operator_active=False,
            drainer_allowed=True,
            browser_enabled=True,
        )
        assert should is False, defn["id"]
        assert "power off" in reason.lower()


def test_reconcile_dry_run():
    from mag.lifecycle import reconcile

    r = reconcile(dry_run=True)
    assert r.get("schema") == "mag_lifecycle_reconcile.v1"
    assert r.get("dry_run") is True
    assert "applied" in r
    assert "lifecycle" in r


def test_auto_reconcile_noop_or_dict(monkeypatch, tmp_path):
    from mag import lifecycle

    # B2-403: auto_reconcile(force=True) used to write the REAL
    # state/lifecycle_latest.json (lifecycle._write_lifecycle_state) and the
    # REAL state/temperature_stacks_latest.json (temperature_stack.STATE_PATH
    # via track_lifecycle_into_improve); both pointers ride tmp_path now.
    monkeypatch.setattr(lifecycle, "_write_lifecycle_state", lambda *a, **k: None)
    import mag.temperature_stack as ts
    monkeypatch.setattr(ts, "STATE_PATH", tmp_path / "temperature_stacks_latest.json")

    # force path always returns a dict
    r = lifecycle.auto_reconcile(force=True)
    assert r is not None
    assert r.get("ok") is True
    # disable via env
    monkeypatch.setenv("MAG_NO_AUTO_PASSIVE", "1")
    assert lifecycle.auto_reconcile() is None
    monkeypatch.delenv("MAG_NO_AUTO_PASSIVE", raising=False)



# B2-81 (2026-09-26): the ollama probe must not mistake a LIVE daemon for an
# absent one. The old probe (bare urlopen, 0.6s, proxy-inheriting) logged 89
# lifecycle_gap:ollama rows while the server answered /api/tags 200 within
# 0-14s of 20 of the 21 verifiable gap observations. Pins: proxy env is
# ignored on loopback, an HTTP wedge falls back to the socket listener check,
# and a truly absent daemon names refusal in the detail.
def test_ollama_probe_ignores_proxy_env(monkeypatch):
    import http.server
    import threading

    from mag import lifecycle

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"{}")

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        port = srv.server_address[1]
        monkeypatch.setattr(lifecycle, "OLLAMA_TAGS_URL", f"http://127.0.0.1:{port}/api/tags")
        # dead proxy on the loopback port the old probe would have honored
        monkeypatch.setenv("http_proxy", "http://127.0.0.1:9")
        monkeypatch.setenv("HTTP_PROXY", "http://127.0.0.1:9")
        up, cause = lifecycle._ollama_up()
        assert up is True, cause
        assert cause.startswith("11434")
    finally:
        srv.shutdown()


def test_ollama_probe_socket_fallback_when_http_wedged(monkeypatch):
    import socket as socket_mod

    from mag import lifecycle

    # tags URL refused instantly (nothing accepts there) ...
    monkeypatch.setattr(lifecycle, "OLLAMA_TAGS_URL", "http://127.0.0.1:1/api/tags")

    class FakeConn:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    calls = []

    def fake_create(address, timeout=None):
        calls.append(address)
        return FakeConn()

    # ... but a listener answers on the daemon endpoint: present, not absent
    monkeypatch.setattr(socket_mod, "create_connection", fake_create)
    up, cause = lifecycle._ollama_up()
    assert up is True
    assert "socket" in cause
    assert calls and calls[0] == ("127.0.0.1", 11434)


def test_ollama_probe_absent_names_refusal(monkeypatch):
    import socket as socket_mod

    from mag import lifecycle

    # port 1 on loopback: nothing listens, connection refused instantly; the
    # socket fallback is stubbed to refuse too so the test is hermetic (it
    # must not depend on whether a real daemon holds 11434 on this host)
    monkeypatch.setattr(lifecycle, "OLLAMA_TAGS_URL", "http://127.0.0.1:1/api/tags")

    def refuse(address, timeout=None):
        raise ConnectionRefusedError("stubbed")

    monkeypatch.setattr(socket_mod, "create_connection", refuse)
    up, cause = lifecycle._ollama_up()
    assert up is False
    assert "refused" in cause or "unreachable" in cause
    actual, detail = lifecycle._actual_process("ollama", {})
    assert actual is False
    assert detail == cause
