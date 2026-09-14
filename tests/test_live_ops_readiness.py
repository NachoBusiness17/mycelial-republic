from mag.live_ops_readiness import snapshot


def test_readiness_is_observer_only():
    result = snapshot()
    assert result["schema"] == "live_ops_readiness.v1"
    assert result["spend"] == {"provider_calls": 0, "estimated_cost": 0, "secrets_read": False}
    assert "do not start a second supervisor" in result["laws"]
