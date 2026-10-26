"""FISH_TANK_REMEDIATE_20261019 - host listener + untrusted LAN peer pins."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_compose_publishes_are_loopback():
    text = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
    for m in re.finditer(r'^\s*-\s*["\']?([0-9.]*:?\d+:\d+)', text, re.M):
        spec = m.group(1)
        assert spec.startswith("127.0.0.1:"), f"compose publish not loopback: {spec}"


def test_compose_owns_8766_for_mag_mcp_and_cast_lan_moves():
    text = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
    assert "127.0.0.1:8766:8766" in text
    from mag import cast_server
    assert cast_server.DEFAULT_PORT == 8766 and cast_server.LAN_PORT != 8766


def test_beacon_defaults_loopback(monkeypatch):
    src = (ROOT / "tools" / "gstd_beacon.py").read_text(encoding="utf-8")
    assert 'os.environ.get("GSTD_BEACON_HOST", "127.0.0.1")' in src
    assert '"0.0.0.0")  # all interfaces' not in src


def test_ollama_expected_loopback():
    """Ollama on the host must be 127.0.0.1:11434 (container reaches it via host.docker.internal)."""
    import os
    host = os.environ.get("OLLAMA_HOST", "127.0.0.1:11434")
    if host.startswith("http"):  # container-side client URL, not a bind
        pytest.skip("client URL form")
    assert not host.startswith("0.0.0.0")


def test_expose_lan_is_leasable():
    doc = json.loads((ROOT / "configs" / "restricted_leases.json").read_text(encoding="utf-8"))
    spec = doc["resources"]["expose:lan"]
    assert spec["max_ttl_s"] <= 14400


@pytest.fixture
def guard(tmp_path, monkeypatch):
    from mag import cast_guard
    monkeypatch.setattr(cast_guard, "PROBES_PATH", tmp_path / "probes.jsonl")
    monkeypatch.setattr(cast_guard, "LAN_PEERS_PATH", tmp_path / "peers.json")
    cast_guard._BLOCKS.clear()
    return cast_guard


def test_peer_classes(guard):
    assert guard.peer_class("127.0.0.1") == "loopback"
    assert guard.peer_class("100.96.161.76") == "tailnet"
    assert guard.peer_class("192.168.86.50") == "lan_untrusted"
    assert guard.peer_class("8.8.8.8") == "public"


def test_untrusted_peer_reads_display_only_and_notices(guard):
    assert guard.display_gate("192.168.86.50", "/beacon.json")["ok"]
    assert guard.display_gate("192.168.86.50", "/api/pull")["deny"] == "display_only"
    rows = [json.loads(x) for x in guard.PROBES_PATH.read_text().splitlines()]
    reasons = [r["reason"] for r in rows]
    assert reasons.count("notice:new_lan_peer:display") == 1
    assert "notice:non_display_route:display" in reasons
    assert guard.display_gate("100.96.161.76", "/anything")["ok"]
    assert not guard.display_gate("8.8.8.8", "/")["ok"]


def test_no_lease_means_no_lan(guard, monkeypatch):
    monkeypatch.setattr(guard, "lan_lease_live", lambda: False)
    from mag import platform_kill
    out = platform_kill.kill_lan_expired(dry=True)
    assert out["lease_live"] is False
    for h in out["killed"]:
        assert h["dry"] is True
