"""The five executed offline fence/dormant-gate checks (a08-rails-laws r2/r7)
as pytest cases, so the front door cannot silently regress.

Offline by construction: the dormant gate and the unknown-lane raise fire
before any DNS or network call; the scheme and host refusals fire before
resolution; the loopback case resolves only "localhost" (no external DNS,
no connect). The bank is sandboxed to tmp_path because route_chat now banks
an ok:false error row on the exception path (a08-rails-laws r10) and the
production ledger must stay test-clean.
"""
from __future__ import annotations

import pytest

from mag.route_chat import _fence, route_chat


@pytest.fixture(autouse=True)
def _sandbox_bank(tmp_path, monkeypatch):
    import mag.route_chat as rc
    monkeypatch.setattr(rc, "USAGE", tmp_path / "usage.jsonl")


def test_dormant_saelis_b2_133_raise():
    # r2/r7: the dormant gate refuses before fence, keys, or network.
    with pytest.raises(RuntimeError, match=r"DORMANT \(B2-133 gate\)"):
        route_chat("x", lane="saelis")


def test_fence_refuses_http_scheme():
    with pytest.raises(RuntimeError, match="non-allowlisted"):
        _fence("http://api.example.com/v1", "api.example.com")


def test_fence_refuses_localhost():
    # localhost resolves to a loopback address (::1 on this host per the r7
    # execution, 127.0.0.1 elsewhere); either way the fence must refuse it.
    with pytest.raises(RuntimeError, match="non-public"):
        _fence("https://localhost/v1", "localhost")


def test_fence_refuses_host_mismatch():
    with pytest.raises(RuntimeError, match="non-allowlisted"):
        _fence("https://evil.example.com/v1", "api.x.ai")


def test_unknown_lane_raise():
    with pytest.raises(RuntimeError, match="unknown lane"):
        route_chat("x", lane="no_such_lane_go_wave_20261004")
