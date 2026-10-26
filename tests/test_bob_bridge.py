"""tests/test_bob_bridge.py - Verification for Bob Bridge."""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.bob_bridge import (
    bank_receipt,
    build_probe_payload,
    build_ssh_command,
    dispatch_probe,
    execute_dry_run_probe,
)


def test_payload_builder():
    payload = build_probe_payload("test_p01", frame_count=24, scene_type="liquid_pour")
    assert payload["probe_id"] == "test_p01"
    assert payload["frame_count"] == 24
    assert payload["scene_type"] == "liquid_pour"
    assert "assertions" in payload


def test_ssh_command_construction():
    cmd = build_ssh_command(
        payload_path="/tmp/test.json",
        bob_host="bob.box",
        bob_user="tester",
        bob_key="/tmp/key"
    )
    assert cmd[0] == "ssh"
    assert "tester@bob.box" in cmd
    assert any("eval_probe.py" in arg for arg in cmd)


def test_dry_run_physical_plausibility():
    p_valid = build_probe_payload("valid_01", scene_type="gravity_drop")
    res_valid = execute_dry_run_probe(p_valid)
    assert res_valid["passed"] is True
    assert res_valid["verdict"] == "PHYSICALLY_PLAUSIBLE"
    assert res_valid["latent_distance"] < 0.35

    p_invalid = build_probe_payload("invalid_01", scene_type="counterfactual_levitation")
    res_invalid = execute_dry_run_probe(p_invalid)
    assert res_invalid["passed"] is False
    assert res_invalid["verdict"] == "PHYSICALLY_IMPLAUSIBLE"
    assert res_invalid["latent_distance"] > 0.50


def test_dispatch_fallback():
    payload = build_probe_payload("disp_01", scene_type="gravity_drop")
    res = dispatch_probe(payload, dry_run=True)
    assert res["passed"] is True
    assert res["dispatch_mode"] == "DRY_RUN_LOCAL_SIMULATION"


def test_receipt_banking(tmp_path=None):
    payload = build_probe_payload("bank_01", scene_type="gravity_drop")
    res = execute_dry_run_probe(payload)
    out_file = os.path.join(ROOT, "watch", "inbox", "TEST_BOB_RECEIPT.json")
    saved = bank_receipt(res, out_path=out_file)
    assert os.path.exists(saved)
    with open(saved, "r", encoding="utf-8") as fp:
        loaded = json.load(fp)
    assert loaded["probe_id"] == "bank_01"
    # Clean up test artifact
    if os.path.exists(out_file):
        os.remove(out_file)


def test_em_dash_cleanliness():
    tools_path = os.path.join(ROOT, "tools", "bob_bridge.py")
    text = open(tools_path, encoding="utf-8").read()
    assert "—" not in text, "Unicode em-dash forbidden in bob_bridge.py"


if __name__ == "__main__":
    test_payload_builder()
    test_ssh_command_construction()
    test_dry_run_physical_plausibility()
    test_dispatch_fallback()
    test_receipt_banking()
    test_em_dash_cleanliness()
    print("ALL TESTS PASSED in test_bob_bridge.py")
