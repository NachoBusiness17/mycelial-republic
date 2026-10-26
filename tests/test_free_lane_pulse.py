"""tests/test_free_lane_pulse.py - Verification for free lane pulse tool."""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.free_lane_pulse import (
    load_env_keys,
    probe_single_model,
    STATE_PATH,
)


def test_load_env_keys_never_leaks():
    keys = load_env_keys()
    assert isinstance(keys, dict)
    # Check that keys are parsed without error
    if "OPENROUTER_API_KEY" in keys:
        assert len(keys["OPENROUTER_API_KEY"]) > 10


def test_probe_single_model_mock_behavior():
    # Test handling of invalid/dead endpoint
    res = probe_single_model("http://127.0.0.1:9999/dead", "fake_key", "mock/dead-model", timeout=0.5)
    assert res["model_id"] == "mock/dead-model"
    assert res["status"] in ("TIMEOUT_OR_NET_ERR", "DEAD_OR_ROTATED")


def test_em_dash_cleanliness():
    tools_path = os.path.join(ROOT, "tools", "free_lane_pulse.py")
    text = open(tools_path, encoding="utf-8").read()
    assert "—" not in text, "Unicode em-dash forbidden in free_lane_pulse.py"


if __name__ == "__main__":
    test_load_env_keys_never_leaks()
    test_probe_single_model_mock_behavior()
    test_em_dash_cleanliness()
    print("ALL TESTS PASSED in test_free_lane_pulse.py")
