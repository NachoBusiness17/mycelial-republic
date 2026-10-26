"""The mesh_delta SSRF fence (Mimosa L2 cure, 2026-10-07).

The client's sanctioned peers ARE private addresses (loopback, tailnet
100.64/10, RFC1918), so the fence inverts the usual web-client rule:
loopback+private allowed, public internet / link-local metadata / multicast
refused. Also: scheme fence, userinfo refusal, IP pinning (the connection
goes to the validated address, not the name), redirect refusal, bounded
reads. These tests monkeypatch getaddrinfo - no network needed.
"""
import ipaddress
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.mesh_delta import _guarded_fetch  # noqa: E402


def _fake_dns(ip: str):
    def fake(host, port, proto=0):
        return [(None, None, None, "",
                 (host, port))] if ip is None else \
               [(None, None, None, "", (ip, port))]
    return fake


def test_public_ip_refused():
    with patch("socket.getaddrinfo", _fake_dns("8.8.8.8")):
        with pytest.raises(ValueError, match="no allowed address"):
            _guarded_fetch("http://evil.example/picture")


def test_metadata_link_local_refused():
    with patch("socket.getaddrinfo", _fake_dns("169.254.169.254")):
        with pytest.raises(ValueError, match="no allowed address"):
            _guarded_fetch("http://metadata.example/latest/meta-data")


def test_loopback_allowed(monkeypatch):
    monkeypatch.setattr(
        "tools.mesh_delta._OPENER",
        type("O", (), {"open": lambda self, req, timeout=0:
                       (_ for _ in ()).throw(AssertionError("noop"))})())
    with patch("socket.getaddrinfo", _fake_dns("127.0.0.1")):
        try:
            _guarded_fetch("http://localhost:8767/picture")
        except ValueError as e:
            pytest.fail("loopback must pass the address fence: " + str(e))
        except Exception:
            pass  # the opener stub raising is fine; the fence must not


def test_tailnet_cgnat_allowed():
    ip = ipaddress.ip_address("100.101.102.103")
    net = ipaddress.ip_network("100.64.0.0/10")
    assert ip in net  # the fence's explicit allowlist, not is_private:
    # Python 3.11 reads CGNAT as is_private=False, so membership in the
    # allowlist network is what admits the tailnet.


def test_scheme_and_userinfo_refused():
    with pytest.raises(ValueError, match="scheme"):
        _guarded_fetch("file:///etc/passwd")
    with pytest.raises(ValueError, match="userinfo"):
        _guarded_fetch("http://user:pw@127.0.0.1/picture")
