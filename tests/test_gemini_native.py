"""B2-194 (2026-09-26): kind gemini_native for the express key.

The B2-63 receipt proved the express key's native home is
aiplatform.googleapis.com/v1/publishers/google/models/{model}:generateContent
with x-goog-api-key auth, and that the API was DISABLED on the key's project
at write time (403 PERMISSION_DENIED, both auth shapes). These pins are
fixture-first: they define the wire contract the lane must speak before any
live 200 can exist (the brief's live falsifier fires only after the operator
enables aiplatform on project 1055073037365 and reruns
watch/inbox/burn_wave_20260926/B2_63_vertex_probe.py).
"""
from __future__ import annotations

import json
import urllib.request

import pytest

import models.providers as P
import models.quota as Q


class _Resp:
    def __init__(self, b: bytes, status: int = 200):
        self._b = b
        self.status = status

    def read(self, n: int = -1):
        return self._b

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


_CANDIDATES_BODY = {
    "candidates": [
        {"content": {"parts": [{"text": "pong"}, {"text": "!"}], "role": "model"},
         "finishReason": "STOP"}
    ],
    "usageMetadata": {"promptTokenCount": 11, "candidatesTokenCount": 2},
}


@pytest.fixture()
def _quota_off(monkeypatch):
    monkeypatch.setattr(Q, "record_usage", lambda *a, **k: None)
    monkeypatch.setattr(Q, "provider_budget", lambda *a, **k: {"budget_ok": True, "tier": "test"})


_LANE = {"kind": "gemini_native", "base_url": "https://aiplatform.googleapis.com/v1",
         "default_model": "gemini-2.5-flash", "api_key_env": "GEMINI_EXPRESS_KEY"}


def _seat_resolvers(monkeypatch):
    monkeypatch.setattr(P, "get_provider", lambda pid: dict(_LANE))
    monkeypatch.setattr(P, "load_providers", lambda: {"defaults": {}})
    monkeypatch.setenv("GEMINI_EXPRESS_KEY", "test-key-123")


def test_chat_provider_gemini_native_wire_contract(monkeypatch, _quota_off):
    captured: dict = {}

    def _fake_urlopen(req, timeout=None):
        captured["url"] = req.full_url
        captured["headers"] = {k.lower(): v for k, v in req.header_items()}
        captured["body"] = json.loads(req.data.decode("utf-8"))
        return _Resp(json.dumps(_CANDIDATES_BODY).encode("utf-8"))

    _seat_resolvers(monkeypatch)
    monkeypatch.setattr(P.urllib.request, "urlopen", _fake_urlopen)
    out = P.chat_provider(
        "gemini_native_test",
        "be terse",
        "say pong",
        temperature=0.5,
        max_tokens=64,
        tier="T2",
    )
    assert out["ok"] is True, out
    assert out["text"] == "pong!"
    assert out["usage"] == {"prompt_tokens": 11, "completion_tokens": 2}
    assert captured["url"].endswith(
        "/v1/publishers/google/models/gemini-2.5-flash:generateContent")
    assert captured["headers"].get("x-goog-api-key") == "test-key-123"
    assert "Authorization" not in captured["headers"]
    assert captured["body"]["contents"][0]["parts"][0]["text"] == "say pong"
    assert captured["body"]["systemInstruction"]["parts"][0]["text"] == "be terse"
    assert captured["body"]["generationConfig"]["maxOutputTokens"] == 64


def test_chat_provider_gemini_native_missing_key_refuses(monkeypatch, _quota_off):
    seen = []

    def _boom(req, timeout=None):
        seen.append(req)
        raise AssertionError("wire reached with no key")

    _seat_resolvers(monkeypatch)
    monkeypatch.setenv("GEMINI_EXPRESS_KEY", "")
    monkeypatch.setattr(P.urllib.request, "urlopen", _boom)
    out = P.chat_provider(
        "gemini_native_test",
        "s",
        "u",
        tier="T2",
    )
    assert out["ok"] is False and "key" in out["error"].lower()
    assert seen == []


def test_chat_messages_gemini_native_named_refusal(monkeypatch):
    def _boom(req, timeout=None):
        raise AssertionError("tool loop hit the wire for a gemini_native lane")

    _seat_resolvers(monkeypatch)
    monkeypatch.setattr(P.urllib.request, "urlopen", _boom)
    out = P.chat_messages(
        "gemini_native_test",
        [{"role": "user", "content": "hi"}],
        tier="T2",
    )
    assert out["ok"] is False
    assert "gemini_native" in out["error"]
    assert "tool loop" in out["error"]


def test_doctor_gemini_native_deep_probe_alive(monkeypatch):
    import mag.doctor as D

    def _fake(req, timeout=None):
        return _Resp(json.dumps(_CANDIDATES_BODY).encode("utf-8"))

    monkeypatch.setattr(D.urllib.request, "urlopen", _fake)
    probe = D._probe_gemini_native_deep(
        "https://aiplatform.googleapis.com/v1", 5.0, "gemini-2.5-flash", "k")
    assert probe["status"] == "ALIVE"
    assert "generateContent" in probe["detail"]


def test_doctor_gemini_native_deep_probe_api_disabled(monkeypatch):
    import mag.doctor as D

    def _http_error(req, timeout=None):
        body = (b'{"error": {"code": 403, "status": "PERMISSION_DENIED", "message": '
                b'"Agent Platform API has not been used in project 1055073037365 '
                b'before or it is disabled."}}')
        raise urllib.error.HTTPError(req.full_url, 403, "Forbidden", {},
                                     __import__("io").BytesIO(body))

    monkeypatch.setattr(D.urllib.request, "urlopen", _http_error)
    probe = D._probe_gemini_native_deep(
        "https://aiplatform.googleapis.com/v1", 5.0, "gemini-2.5-flash", "k")
    assert probe["status"] == "AUTH-DEAD"
    assert "disabled" in probe["detail"].lower()
