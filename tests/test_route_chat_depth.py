"""Depth enum validation and the D3 thinking wire (a06-sacred-cow#3,
a08-rails-laws r5, ractor D3 ruling 2026-10-04).

Pins the D3 contract (watch/inbox/ractor_engine/2026-10-04-parked-decisions/
SYNTHESIS.md:11-17): a depth string outside {mechanical, design} raises
ValueError (previously anything but "design" silently rode mechanical);
mechanical sends thinking:{type:disabled} on the wire for EVERY lane,
flagless included, because omission is a MEASURED ON state (d4 probe,
watch/inbox/go_wave_20261004/d4_thinking_probe.md), except the family with
a measured 400 on the key; design is the only ON path and refuses without
lane capability attestation (providers.yaml disable_thinking) or below
32000 max_tokens of headroom; banked rows carry depth, thinking_sent and
reasoning_tokens so the off state is verified from the response, not
assumed from the request.

Fully offline: fence, key lookup, DNS and urlopen are patched; the bank
lands in tmp_path.
"""
from __future__ import annotations

import json
import urllib.request

import pytest

import mag.route_chat as rc


class _FakeResp:
    def __init__(self, payload: bytes):
        self._payload = payload

    def read(self) -> bytes:
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


@pytest.fixture(autouse=True)
def _offline(monkeypatch, tmp_path):
    monkeypatch.setattr(rc, "USAGE", tmp_path / "usage.jsonl")
    monkeypatch.setattr(rc, "_fence",
                        lambda base_url, host: {"93.184.216.34"})
    monkeypatch.setattr(rc, "_keys_for",
                        lambda lane_cfg: [("FAKE_KEY_ENV", "sk-fake")])
    monkeypatch.setattr(
        rc.socket, "getaddrinfo",
        lambda *a, **k: [(2, 1, 6, "", ("93.184.216.34", 443))])
    captured = {}

    def fake_urlopen(req, timeout=0):
        captured["body"] = json.loads(req.data.decode())
        return _FakeResp(json.dumps({
            "choices": [{"message": {"content": "done"},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 3, "completion_tokens": 2},
        }).encode())

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    return captured


def test_depth_enum_rejects_unknown():
    # a06-sacred-cow#3: no enum validation existed; a typo'd depth rode
    # mechanical and read as law. Input validation fires before the try, so
    # this banks nothing and touches no network.
    with pytest.raises(ValueError, match="depth must be"):
        rc.route_chat("x", lane="deepseek", depth="vibes")


def test_mechanical_wires_thinking_disabled(_offline):
    # the real deepseek lane carries disable_thinking: true in
    # configs/providers.yaml; mechanical must now send it on the wire
    rc.route_chat("x", lane="deepseek", model="deepseek-v4-flash",
                  goal="depth wire probe")
    assert _offline["body"]["thinking"] == {"type": "disabled"}


def test_design_wires_thinking_enabled(_offline):
    # D3 gate: the real deepseek lane carries the capability attestation
    # (configs/providers.yaml disable_thinking: true) and the ask pays 32K
    # headroom, so design stays the one thinking-ON path
    rc.route_chat("x", lane="deepseek", model="deepseek-v4-flash",
                  depth="design", max_tokens=32_000,
                  goal="depth wire probe")
    assert _offline["body"]["thinking"] == {"type": "enabled"}


def test_design_refuses_unattested_lane(monkeypatch, _offline, tmp_path):
    # D3 gate arm (a): a lane with no disable_thinking attestation cannot
    # fire thinking-ON even by explicit ask; the refusal banks an error
    # row (a08-rails-laws r10 closed loop)
    monkeypatch.setattr(rc, "_load_lanes", lambda: {
        "plain": {"base_url": "https://plain.example.com/v1",
                  "default_model": "m-1", "api_key_env": "NO_SUCH_KEY"}})
    with pytest.raises(RuntimeError, match="attestation"):
        rc.route_chat("x", lane="plain", depth="design",
                      max_tokens=32_000, goal="depth wire probe")
    row = json.loads((tmp_path / "usage.jsonl").read_text(
        encoding="utf-8").splitlines()[-1])
    assert row["ok"] is False
    assert row["error"] == "RuntimeError"


def test_design_refuses_thin_headroom(_offline, tmp_path):
    # D3 gate arm (b): attestation alone is not enough; the founding burn
    # spent 15998 of a 16000 completion cap on reasoning
    # (memory/runs/hermes_burn/usage.jsonl line 1151), so a design ask
    # below 32000 headroom is refused before any network byte
    with pytest.raises(RuntimeError, match="headroom"):
        rc.route_chat("x", lane="deepseek", model="deepseek-v4-flash",
                      depth="design", goal="depth wire probe")
    row = json.loads((tmp_path / "usage.jsonl").read_text(
        encoding="utf-8").splitlines()[-1])
    assert row["ok"] is False


def test_lane_without_flag_still_sends_disabled(monkeypatch, _offline):
    # D3 2026-10-04 (parked-decisions SYNTHESIS.md:11-17): the carrier sends
    # the explicit off switch on mechanical for EVERY lane; omission is a
    # measured ON state. This pin replaced the omission-as-contract test.
    monkeypatch.setattr(rc, "_load_lanes", lambda: {
        "plain": {"base_url": "https://plain.example.com/v1",
                  "default_model": "m-1", "api_key_env": "NO_SUCH_KEY"}})
    rc.route_chat("x", lane="plain", goal="depth wire probe")
    assert _offline["body"]["thinking"] == {"type": "disabled"}


def test_measured_400_family_gets_no_thinking_key(monkeypatch, _offline):
    # D3 falsifier (1) in code: qwen3.7-flash 400s on any reasoning param
    # (inference_budget qwen-flash forbidden_keys), so it alone is exempt
    monkeypatch.setattr(rc, "_load_lanes", lambda: {
        "plain": {"base_url": "https://plain.example.com/v1",
                  "default_model": "qwen/qwen3.7-flash",
                  "api_key_env": "NO_SUCH_KEY"}})
    rc.route_chat("x", lane="plain", goal="depth wire probe")
    assert "thinking" not in _offline["body"]


def test_bank_carries_depth_and_reasoning_tokens(monkeypatch, _offline, tmp_path):
    rc.route_chat("x", lane="deepseek", model="deepseek-v4-flash",
                  goal="depth wire probe")
    row = json.loads((tmp_path / "usage.jsonl").read_text(
        encoding="utf-8").splitlines()[-1])
    assert row["depth"] == "mechanical"
    assert row["thinking_sent"] == "disabled"
    assert "reasoning_tokens" in row


def test_wire_thinking_pure_payload():
    assert rc.wire_thinking({}, "mechanical", "z-ai/glm-5.3-prime") == \
        {"thinking": {"type": "disabled"}}
    assert rc.wire_thinking({}, "design", "deepseek-v4-flash",
                            attested=True, max_tokens=32_000) == \
        {"thinking": {"type": "enabled"}}
    with pytest.raises(RuntimeError, match="attestation"):
        rc.wire_thinking({}, "design", "m-1")
    with pytest.raises(RuntimeError, match="headroom"):
        rc.wire_thinking({}, "design", "deepseek-v4-flash",
                         attested=True, max_tokens=16_000)
