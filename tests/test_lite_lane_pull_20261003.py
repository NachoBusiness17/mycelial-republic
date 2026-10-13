"""Lite lane pulled from estate rotation (operator order 2026-10-03: "i gave
the lite lane to adam he's been using it we should remove it from rotation").

Four layers, each proven here:
1. providers.yaml z_ai3 dormant:true -> B2-133 gate drops it from fuel_feed
   FREE_LANES/CACHE_LANES (live-config tripwire: flipping the flag back
   without operator GO fails this file and names the receipt).
2. mag/lite_guard.check() denies every door by default (LITE_LANE_ACTIVE=1
   is the operator re-arm lever).
3. lane_runner.flash_call rides the env-pinned openrouter model only; no
   z.ai leg, and the old plain-ZAI_API_KEY fallback (the operator's own
   working lane, 08-29 hands-off fence) is gone.
4. .env carries the Lite key commented out (not asserted here; the key
   lookup returning empty is what layer 2's deny already covers).
Receipt: watch/inbox/LITE_LANE_PULL_20261003.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag import fuel_feed, lane_runner, lite_guard  # noqa: E402


def test_z_ai3_dormant_out_of_rotation():
    names = [l[0] for l in fuel_feed.FREE_LANES]
    assert "z_ai3" not in names, (
        "z_ai3 back in fuel_feed FREE_LANES: the 2026-10-03 operator pull "
        "(lane given to adam) was reverted without an operator GO; see "
        "watch/inbox/LITE_LANE_PULL_20261003.md")
    assert fuel_feed.CACHE_LANES == [], (
        "CACHE_LANES should be empty while the Lite cache-mining lane is "
        "dormant; a replacement cache lane is an operator routing call")


def test_lite_guard_retired_by_default(monkeypatch):
    monkeypatch.delenv("LITE_LANE_ACTIVE", raising=False)
    g = lite_guard.check("pytest")
    assert g["ok"] is False and g.get("retired") is True
    assert "adam" in g["deny"]


def test_lite_guard_rearm_lever(monkeypatch):
    monkeypatch.setenv("LITE_LANE_ACTIVE", "1")
    monkeypatch.setenv("LITE_DAILY_CREDITS", "999999")  # re-armed path paces, not denies
    g = lite_guard.check("pytest")
    assert g["ok"] is True and "retired" not in g


class _FakeResp:
    def __init__(self, payload):
        self._payload = json.dumps(payload).encode("utf-8")

    def read(self):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class _FakeOpener:
    def __init__(self):
        self.urls = []

    def open(self, req, timeout=None):
        self.urls.append(req.full_url)
        return _FakeResp({"choices": [{"message": {"content": "lens text"}}],
                          "usage": {"prompt_tokens": 3, "completion_tokens": 3}})


def test_flash_call_openrouter_only(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("OPENROUTER_FLASH_MODEL", "test/lane-model")
    monkeypatch.delenv("OPENROUTER_MODEL", raising=False)  # ox-alpha lane's var, never ours
    monkeypatch.setattr(lane_runner, "_safe_https_url", lambda url: True)
    opener = _FakeOpener()
    monkeypatch.setattr(lane_runner, "_OPENER", opener)
    out = lane_runner.flash_call("system", "user")
    assert out == "lens text"
    assert opener.urls == ["https://openrouter.ai/api/v1/chat/completions"]
    assert not any("z.ai" in u for u in opener.urls)


def test_flash_call_strips_crlf_and_defaults_model(monkeypatch):
    """Live-caught 2026-10-04 04:19: .env is CRLF, a shell export glues \\r onto
    the key (invalid header), and OPENROUTER_MODEL belongs to the ox-alpha lane
    (stealth/ox-alpha 404s on openrouter). flash_call must strip values and
    default the model to openrouter/auto when its own pin is unset."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key\r\n")
    monkeypatch.delenv("OPENROUTER_FLASH_MODEL", raising=False)
    monkeypatch.delenv("OPENROUTER_MODEL", raising=False)
    monkeypatch.setattr(lane_runner, "_safe_https_url", lambda url: True)
    seen = {}

    class BodyOpener(_FakeOpener):
        def open(self, req, timeout=None):
            seen["model"] = json.loads(req.data.decode("utf-8"))["model"]
            seen["auth"] = req.headers.get("Authorization", "")
            return super().open(req, timeout)
    monkeypatch.setattr(lane_runner, "_OPENER", BodyOpener())
    lane_runner.flash_call("system", "user")
    assert seen["model"] == "openrouter/auto"
    assert seen["auth"] == "Bearer test-key"  # no trailing \r


def test_flash_call_refuses_without_pin(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("OPENROUTER_FLASH_MODEL", raising=False)
    with pytest.raises(RuntimeError, match="flash lane down"):
        lane_runner.flash_call("system", "user")
