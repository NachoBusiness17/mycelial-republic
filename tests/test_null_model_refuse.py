"""B2-286 (2026-09-26): a null model is a named refusal, never a live 200-empty.

Disease (measured, B2-62 first probe cited by the brief): z_ai2/z_ai3 carried
no default_model, provider_default_model returned None, and a bare call sent
"model": null and got HTTP 200 with empty content + empty usage, so a dead
lane read ok=True. The fix: chat_provider and chat_messages refuse a resolved-
None model with a named error (free_local carve-out keeps ollama behavior).
"""
from __future__ import annotations

import json
import urllib.request

import models.providers as P


class _MustNotCall:
    """Sentinel urlopen: the refusal must fire BEFORE any wire traffic."""

    def __call__(self, req, timeout=None):  # noqa: ANN001, ARG002
        raise AssertionError("network call reached the wire with a null model")


class _Recording:
    def __init__(self, body: dict):
        self.payloads: list[dict] = []
        self._b = json.dumps(body).encode("utf-8")

    def __call__(self, req, timeout=None):  # noqa: ANN001
        self.payloads.append(json.loads(req.data.decode("utf-8")))

        class _Resp:
            def __init__(self, b):
                self._b = b

            def read(self):
                return self._b

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        return _Resp(self._b)


def _wire(monkeypatch, pcfg: dict, fake):
    monkeypatch.setattr(P, "get_provider", lambda pid: dict(pcfg))
    monkeypatch.setattr("models.quota.provider_budget",
                        lambda pid: {"budget_ok": True, "remaining": 999})
    monkeypatch.setattr("models.quota.record_usage", lambda *a, **k: None)
    monkeypatch.setattr("models.quota.pick_provider", lambda *a, **k: None)
    monkeypatch.setattr(urllib.request, "urlopen", fake)


def _zai3_pcfg(**extra) -> dict:
    """The B2-286 disease shape: openai_compat lane with NO default_model."""
    pcfg = {"id": "z_ai3", "kind": "openai_compat",
            "base_url": "https://api.z.ai/api/coding/paas/v4",
            "api_key_env": "ZAI_API_KEY_Lite", "timeout_seconds": 15,
            "models": ["glm-4.7-flash", "glm-5.3-flash"]}
    pcfg.update(extra)
    return pcfg


def test_bare_call_without_default_model_returns_named_error(monkeypatch):
    # the brief's falsifier: chat_provider('z_ai3', ..., tier=T2) without model
    # returns a named error instead of a 200-empty.
    monkeypatch.setenv("ZAI_API_KEY_Lite", "k-test")
    fake = _MustNotCall()
    _wire(monkeypatch, _zai3_pcfg(), fake)
    out = P.chat_provider("z_ai3", "sys", "hi", tier="T2")
    assert out["ok"] is False
    assert "null_model_refused" in str(out["error"])
    assert out["provider"] == "z_ai3"


def test_chat_messages_same_refusal(monkeypatch):
    monkeypatch.setenv("ZAI_API_KEY_Lite", "k-test")
    fake = _MustNotCall()
    _wire(monkeypatch, _zai3_pcfg(), fake)
    out = P.chat_messages("z_ai3", [{"role": "user", "content": "hi"}], tier="T2")
    assert out["ok"] is False and "null_model_refused" in str(out["error"])


def test_explicit_model_still_reaches_the_wire(monkeypatch):
    monkeypatch.setenv("ZAI_API_KEY_Lite", "k-test")
    body = {"choices": [{"message": {"content": "pong"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1}}
    fake = _Recording(body)
    _wire(monkeypatch, _zai3_pcfg(), fake)
    out = P.chat_provider("z_ai3", "sys", "hi", tier="T2", model="glm-4.7-flash",
                          max_tokens=2000)
    assert out["ok"] is True
    assert fake.payloads[0]["model"] == "glm-4.7-flash"


def test_free_local_keeps_its_behavior(monkeypatch):
    # ollama-class lanes (free_local) keep sending whatever they resolve, so
    # local behavior is unchanged by the refusal gate.
    pcfg = _zai3_pcfg(free_local=True, base_url="http://127.0.0.1:11434/v1")
    body = {"choices": [{"message": {"content": "local"}, "finish_reason": "stop"}],
            "usage": {}}
    fake = _Recording(body)
    _wire(monkeypatch, pcfg, fake)
    out = P.chat_provider("ollama", "sys", "hi", tier="T1")
    assert out["ok"] is True
    assert fake.payloads[0]["model"] is None
