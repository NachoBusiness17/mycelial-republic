"""Marker-penalty profile tests (port wave 2026-10-07, lane P6 port 2).

Covers the sampler-level reasoning-marker penalty leg: the shipped profile
loads and validates, the bridge accepts penalty_profile at the constructor and
--penalty-profile at the CLI, and the DEFAULT behavior is unchanged (no
profile, no logit_bias key, payload identical to the pre-profile bridge).

Mechanism citation: watch/inbox/frontier_olm_2026-10-03/steal/
quantization-and-compression.md:31 (training-free token-specific penalties
recovered up to 9.8 accuracy points while cutting CoT length up to 51.3
percent), staged as the cheap leg by watch/inbox/frontier_olm_2026-10-07/
steal/finetuning-adaptation.md find 1.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from mag.llama_cpp_bridge import (
    DEFAULT_PENALTY_PROFILE,
    LlamaCppBridge,
    load_penalty_profile,
    main,
    penalty_logit_bias,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
SHIPPED_PROFILE = REPO_ROOT / "configs" / "marker_penalty_profile.json"

BASELINE_KEYS = {"prompt", "temperature", "max_tokens", "stop"}


def test_shipped_profile_loads_and_carries_mined_markers():
    profile = load_penalty_profile(SHIPPED_PROFILE)
    markers = profile["markers"]
    for token in ("wait", "however", "alternatively", "actually",
                  "therefore", "hmm", "maybe"):
        assert token in markers, f"mined marker {token!r} missing from profile"
        assert markers[token]["bias"] < 0, "penalty biases must be negative"
    # The receipt census is banked beside the markers (mining is evidence, not
    # folklore): the two heaviest hits lead the bias ordering.
    assert profile["receipt_census"]["actually"] >= profile["receipt_census"]["wait"]


def test_load_penalty_profile_missing_path_raises():
    with pytest.raises(FileNotFoundError):
        load_penalty_profile(REPO_ROOT / "configs" / "no_such_profile.json")


def test_load_penalty_profile_malformed_body_raises(tmp_path):
    bad = tmp_path / "bad_profile.json"
    bad.write_text(json.dumps({"markers": {"wait": {"nope": 1}}}), encoding="utf-8")
    with pytest.raises(ValueError):
        load_penalty_profile(bad)
    empty = tmp_path / "empty_profile.json"
    empty.write_text(json.dumps({"markers": {}}), encoding="utf-8")
    with pytest.raises(ValueError):
        load_penalty_profile(empty)


def test_default_payload_has_no_logit_bias():
    # Default-behavior law: without a profile the payload carries exactly the
    # pre-profile keys, no logit_bias channel at all.
    body = LlamaCppBridge._completions_payload("p", 0.1, 256)
    decoded = json.loads(body.decode("utf-8"))
    assert set(decoded) == BASELINE_KEYS
    assert "logit_bias" not in decoded


def test_default_bridge_matches_legacy_payload_bytes():
    # The no-profile bridge body must be byte-identical to the pre-profile
    # inline payload (the exact json.dumps key order of the old code path).
    bridge = LlamaCppBridge()
    assert bridge.penalty_profile is None
    legacy = json.dumps(
        {
            "prompt": "p",
            "temperature": 0.1,
            "max_tokens": 256,
            "stop": ["\n\n", "</s>"],
        }
    ).encode("utf-8")
    assert LlamaCppBridge._completions_payload("p", 0.1, 256) == legacy


def test_profile_adds_logit_bias_and_nothing_else():
    profile = load_penalty_profile(SHIPPED_PROFILE)
    body = LlamaCppBridge._completions_payload("p", 0.1, 256, profile)
    decoded = json.loads(body.decode("utf-8"))
    assert set(decoded) == BASELINE_KEYS | {"logit_bias"}
    bias_map = decoded["logit_bias"]
    assert bias_map, "profile must yield a non-empty bias map"
    assert all(isinstance(v, float) for v in bias_map.values())
    # Every penalty is negative (suppression), none exceeds a mild clamp.
    assert all(v < 0 and v >= -100.0 for v in bias_map.values())


def test_penalty_logit_bias_prefers_token_id_form():
    profile = {
        "markers": {
            "wait": {"bias": -6.0, "token_id": 4013},
            "hmm": {"bias": -4.0},
        }
    }
    bias_map = penalty_logit_bias(profile)
    assert bias_map["4013"] == -6.0
    assert bias_map["hmm"] == -4.0


def test_bridge_constructor_accepts_profile_and_flag_default_off():
    # Path form loads; dict form rides as-is; the flag default is OFF (None).
    by_path = LlamaCppBridge(penalty_profile=SHIPPED_PROFILE)
    assert isinstance(by_path.penalty_profile, dict)
    assert "wait" in by_path.penalty_profile["markers"]
    by_dict = LlamaCppBridge(penalty_profile={"markers": {"wait": {"bias": -1.0}}})
    assert by_dict.penalty_profile == {"markers": {"wait": {"bias": -1.0}}}
    off = LlamaCppBridge()
    assert off.penalty_profile is None


def test_bridge_generate_move_fallback_unaffected_by_profile():
    # Fallback-mode law (never crashes): with or without the profile, a bridge
    # with no server returns the deterministic placeholder shape.
    prompt = "fallback probe"
    off = LlamaCppBridge().generate_move(prompt)
    on = LlamaCppBridge(penalty_profile=SHIPPED_PROFILE).generate_move(prompt)
    for res in (off, on):
        assert res["ok"] is False and res["fallback"] is True
        assert res["move"]  # deterministic placeholder, never empty
    assert off["move"] == on["move"]


def test_cli_accepts_penalty_profile_flag_off_by_default(capsys):
    # Without --penalty-profile: runs clean and reports fallback False only in
    # the sense of no server; the flag simply does not exist in the run.
    assert main(["--rounds", "1"]) == 0
    off_out = json.loads(capsys.readouterr().out)
    assert off_out["rounds"] == 1
    # With --penalty-profile: the CLI loads the shipped profile and runs the
    # same benchmark shape.
    assert main(["--rounds", "1", "--penalty-profile", str(SHIPPED_PROFILE)]) == 0
    on_out = json.loads(capsys.readouterr().out)
    assert on_out["rounds"] == 1
    assert DEFAULT_PENALTY_PROFILE.endswith("marker_penalty_profile.json")
