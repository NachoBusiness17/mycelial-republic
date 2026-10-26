"""lane_runner.flash_call rides mag/inference_budget recipes (2026-10-17 self-steal).

The elder lens died daily as "HTTP 200 with empty content" because the cage door
hand-rolled max_tokens=1536 while mag/inference_budget.py already held the cure.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag import inference_budget as ib  # noqa: E402
from mag import lane_runner  # noqa: E402


class _Resp:
    def __init__(self, payload):
        self._b = json.dumps(payload).encode("utf-8")

    def read(self):
        return self._b

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class _Opener:
    def __init__(self, payload):
        self.payload = payload
        self.bodies = []

    def open(self, req, timeout=None):
        self.bodies.append(json.loads(req.data.decode("utf-8")))
        return _Resp(self.payload)


def _arm(monkeypatch, model, payload):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("OPENROUTER_FLASH_MODEL", model)
    monkeypatch.setattr(lane_runner, "_safe_https_url", lambda url: True)
    op = _Opener(payload)
    monkeypatch.setattr(lane_runner, "_OPENER", op)
    return op


OK = {"choices": [{"message": {"content": "lens text"}, "finish_reason": "stop"}]}


def test_default_model_gets_recipe_floor(monkeypatch):
    op = _arm(monkeypatch, "openrouter/auto", OK)
    assert lane_runner.flash_call("s", "u", max_tokens=900) == "lens text"
    assert op.bodies[0]["max_tokens"] >= ib.DEFAULT_FLOOR_SMALL


def test_deepseek_thinking_disabled_injected(monkeypatch):
    op = _arm(monkeypatch, "deepseek/deepseek-v4.1-flash-1017", OK)
    lane_runner.flash_call("s", "u")
    assert op.bodies[0].get("thinking") == {"type": "disabled"}


def test_qwen_flash_reasoning_params_never_sent(monkeypatch):
    op = _arm(monkeypatch, "qwen/qwen3.7-flash", OK)
    lane_runner.flash_call("s", "u")
    for k in ("reasoning", "reasoning_effort", "thinking", "chat_template_kwargs"):
        assert k not in op.bodies[0]


def test_empty_reasoning_is_named_in_log(monkeypatch):
    burned = {"choices": [{"message": {"content": ""}, "finish_reason": "length"}],
              "usage": {"completion_tokens": 8000,
                        "completion_tokens_details": {"reasoning_tokens": 8000}}}
    _arm(monkeypatch, "openrouter/auto", burned)
    lines = []
    monkeypatch.setattr(lane_runner, "_log", lambda m: lines.append(m))
    assert lane_runner.flash_call("s", "u") == ""
    assert any("EMPTY_REASONING" in m for m in lines)
