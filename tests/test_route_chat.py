"""The four offline checks the gap-analysis a08 lane spec'd (2026-10-04):
the fence and dormant gate execute as documented - zero network calls."""
import pytest

from mag.route_chat import _fence, _load_lanes, route_chat


def test_fence_refuses_loopback():
    with pytest.raises(RuntimeError, match="non-public"):
        _fence("https://127.0.0.1/v1", "127.0.0.1")


def test_fence_refuses_http():
    with pytest.raises(RuntimeError, match="non-allowlisted|refusing"):
        _fence("http://api.x.ai/v1", "api.x.ai")


def test_fence_allows_allowlisted_public_host():
    # no raise: the allowlisted public host passes the fence
    _fence("https://api.x.ai/v1", "api.x.ai")


def test_dormant_lane_refusal():
    lanes = _load_lanes()
    dormant = [name for name, cfg in lanes.items() if cfg.get("dormant")]
    if not dormant:
        pytest.skip("no dormant lane in providers.yaml")
    with pytest.raises(RuntimeError, match="DORMANT"):
        route_chat("x", lane=dormant[0])
