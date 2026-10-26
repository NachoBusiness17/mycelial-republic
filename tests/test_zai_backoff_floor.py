"""B2-62 (2026-09-26): z.ai lane client adaptive backoff on 1305 + reasoning floor.

SPEC: docs/ref/ZAI_API_EXPERT_REFERENCE.md §5.1 (spec'd BEFORE the code, same day).
MEASURED: watch/inbox/burn_wave_20260926/B2_04_probe_results2.json; 429 code 1305
"The service may be temporarily overloaded" ~1 in 3 calls at 6s spacing; one Lite 429
survived a single 15s wait (stretch needed); glm-4.7-flash ate the whole 600-token
budget on 2 of 7 burns (completion=600, content empty).
"""
from __future__ import annotations

import io
import json
import urllib.error
import urllib.request

import models.providers as P

BODY_1305 = json.dumps({"error": {"code": "1305",
                                  "message": "The service may be temporarily overloaded, "
                                             "please try again later"}})
BODY_1302 = json.dumps({"error": {"code": "1302", "message": "rate limited"}})
BODY_QUOTA = json.dumps({"error": {"code": "1308", "message": "usage limit hit"}})


def _http_error(code: int, body: str) -> urllib.error.HTTPError:
    return urllib.error.HTTPError("https://api.z.ai/api/coding/paas/v4/chat/completions",
                                  code, "err", {}, io.BytesIO(body.encode("utf-8")))


class _Resp:
    def __init__(self, body: dict):
        self._b = json.dumps(body).encode("utf-8")

    def read(self) -> bytes:
        return self._b

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _ok_body(text: str = "recovered") -> dict:
    return {"choices": [{"message": {"content": text}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5,
                      "prompt_tokens_details": {"cached_tokens": 8}}}


class FakeUrlopen:
    """Scripted urlopen: items are exceptions or 200-body dicts; records payloads."""

    def __init__(self, script: list):
        self.script = list(script)
        self.calls = 0
        self.payloads: list[dict] = []

    def __call__(self, req, timeout=None):  # noqa: ANN001, ARG002
        self.calls += 1
        self.payloads.append(json.loads(req.data.decode("utf-8")))
        item = self.script.pop(0)
        if isinstance(item, Exception):
            raise item
        return _Resp(item)


def _wire(monkeypatch, pcfg: dict, fake: FakeUrlopen) -> list[int]:
    """Isolate the client: fake provider row, quota + usage recording, clock."""
    monkeypatch.setattr(P, "get_provider", lambda pid: dict(pcfg))
    monkeypatch.setattr("models.quota.provider_budget",
                        lambda pid: {"budget_ok": True, "remaining": 999})
    monkeypatch.setattr("models.quota.record_usage", lambda *a, **k: None)
    monkeypatch.setattr("models.quota.pick_provider", lambda *a, **k: None)
    sleeps: list[int] = []
    monkeypatch.setattr(P.time, "sleep", lambda s: sleeps.append(s))
    monkeypatch.setattr(urllib.request, "urlopen", fake)
    return sleeps


def _lane_pcfg(**extra) -> dict:
    pcfg = {"id": "z_ai2", "kind": "openai_compat",
            "base_url": "https://api.z.ai/api/coding/paas/v4",
            "api_key_env": "ZAI_API_KEY_Pro", "timeout_seconds": 15,
            "models": ["glm-4.7-flash"], "default_model": "glm-4.7-flash"}
    pcfg.update(extra)
    return pcfg


# ── LAW 1: OVERLOAD BACKOFF ──

def test_1305_backs_off_15_then_30_and_recovers(monkeypatch):
    monkeypatch.setenv("ZAI_API_KEY_Pro", "k-test")
    fake = FakeUrlopen([_http_error(429, BODY_1305), _http_error(429, BODY_1305),
                        _ok_body("recovered")])
    sleeps = _wire(monkeypatch, _lane_pcfg(retry_overload=True), fake)
    out = P.chat_provider("z_ai2", "sys", "hi", tier="T2", max_tokens=2000)
    assert out["ok"] is True and out["text"] == "recovered"
    assert fake.calls == 3            # initial + 2 retries on the SAME key
    assert sleeps == [15, 30]         # adaptive stretch, B2-04 measured base


def test_1305_gives_up_after_attempts_and_reports(monkeypatch):
    monkeypatch.setenv("ZAI_API_KEY_Pro", "k-test")
    fake = FakeUrlopen([_http_error(429, BODY_1305) for _ in range(10)])
    sleeps = _wire(monkeypatch, _lane_pcfg(retry_overload=True), fake)
    out = P.chat_provider("z_ai2", "sys", "hi", tier="T2", max_tokens=2000)
    assert out["ok"] is False and "1305" in str(out["error"])
    assert fake.calls == 1 + P.OVERLOAD_ATTEMPTS   # bounded: 1 + 2, never infinite
    assert sleeps == [15, 30]


def test_no_flag_never_sleeps(monkeypatch):
    monkeypatch.setenv("ZAI_API_KEY_Pro", "k-test")
    fake = FakeUrlopen([_http_error(429, BODY_1305)])
    sleeps = _wire(monkeypatch, _lane_pcfg(), fake)   # no retry_overload
    out = P.chat_provider("z_ai2", "sys", "hi", tier="T2", max_tokens=2000)
    assert out["ok"] is False and fake.calls == 1 and sleeps == []


def test_non_overload_429_never_sleeps(monkeypatch):
    monkeypatch.setenv("ZAI_API_KEY_Pro", "k-test")
    fake = FakeUrlopen([_http_error(429, BODY_QUOTA)])
    sleeps = _wire(monkeypatch, _lane_pcfg(retry_overload=True), fake)
    out = P.chat_provider("z_ai2", "sys", "hi", tier="T2", max_tokens=2000)
    assert out["ok"] is False and fake.calls == 1 and sleeps == []


def test_1302_counts_as_overload_family(monkeypatch):
    monkeypatch.setenv("ZAI_API_KEY_Pro", "k-test")
    fake = FakeUrlopen([_http_error(429, BODY_1302), _ok_body("ok-1302")])
    sleeps = _wire(monkeypatch, _lane_pcfg(retry_overload=True), fake)
    out = P.chat_provider("z_ai2", "sys", "hi", tier="T2", max_tokens=2000)
    assert out["ok"] is True and sleeps == [15]


def test_should_burst_still_fires_after_exhaustion(monkeypatch):
    # the paid burst stays the LAST resort: an exhausted 1305 must still burst.
    assert P.should_burst(f"HTTP 429: {BODY_1305}")


# ── LAW 2: REASONING FLOOR ──

def test_floor_disables_undecided_thinking_under_1536(monkeypatch):
    # the B2-04 scar: max_tokens=600 + default thinking -> completion=600, empty.
    monkeypatch.setenv("ZAI_API_KEY_Pro", "k-test")
    fake = FakeUrlopen([_ok_body("one sentence")])
    _wire(monkeypatch, _lane_pcfg(retry_overload=True), fake)
    out = P.chat_provider("z_ai2", "sys", "hi", tier="T2", max_tokens=600)
    assert fake.payloads[0]["thinking"] == {"type": "disabled"}
    assert out["ok"] is True and out.get("reasoning_floor_applied") is True


def test_floor_respects_budget_at_or_above_1536(monkeypatch):
    monkeypatch.setenv("ZAI_API_KEY_Pro", "k-test")
    fake = FakeUrlopen([_ok_body("deep thought")])
    _wire(monkeypatch, _lane_pcfg(retry_overload=True), fake)
    out = P.chat_provider("z_ai2", "sys", "hi", tier="T2", max_tokens=1536)
    assert "thinking" not in fake.payloads[0]
    assert out.get("reasoning_floor_applied") is None


def test_floor_respects_explicit_thinking_true(monkeypatch):
    monkeypatch.setenv("ZAI_API_KEY_Pro", "k-test")
    fake = FakeUrlopen([_ok_body("coherent")])
    _wire(monkeypatch, _lane_pcfg(retry_overload=True), fake)
    out = P.chat_provider("z_ai2", "sys", "hi", tier="T2", max_tokens=600, thinking=True)
    assert "thinking" not in fake.payloads[0]   # explicit override wins over the floor
    assert out.get("reasoning_floor_applied") is None


def test_floor_never_disables_thinking_on_5_3(monkeypatch):
    # glm-5.3-flash forces thinking: disabled would 1210 (§10.1 lived scar).
    monkeypatch.setenv("ZAI_API_KEY_Pro", "k-test")
    fake = FakeUrlopen([_ok_body("5.3 answer")])
    _wire(monkeypatch, _lane_pcfg(retry_overload=True, default_model="glm-5.3-flash"),
          fake)
    out = P.chat_provider("z_ai2", "sys", "hi", tier="T2", max_tokens=600,
                          model="glm-5.3-flash")
    assert "thinking" not in fake.payloads[0]
    assert out.get("reasoning_floor_applied") is None


def test_floor_honors_provider_disable_thinking(monkeypatch):
    # provider already disables thinking: no double-set, no flag.
    monkeypatch.setenv("ZAI_API_KEY_Pro", "k-test")
    fake = FakeUrlopen([_ok_body("scut")])
    _wire(monkeypatch, _lane_pcfg(retry_overload=True, disable_thinking=True), fake)
    out = P.chat_provider("z_ai2", "sys", "hi", tier="T2", max_tokens=600)
    assert fake.payloads[0]["thinking"] == {"type": "disabled"}
    assert out.get("reasoning_floor_applied") is None


def test_floor_applies_in_chat_messages_path(monkeypatch):
    monkeypatch.setenv("ZAI_API_KEY_Pro", "k-test")
    fake = FakeUrlopen([_ok_body("toolless")])
    _wire(monkeypatch, _lane_pcfg(retry_overload=True), fake)
    out = P.chat_messages("z_ai2", [{"role": "user", "content": "hi"}],
                          tier="T2", max_tokens=600)
    assert fake.payloads[0]["thinking"] == {"type": "disabled"}
    assert out["ok"] is True and out.get("reasoning_floor_applied") is True


def test_helpers_unit():
    assert P._is_overload_body(BODY_1305) and P._is_overload_body(BODY_1302)
    assert P._is_overload_body("HTTP 429: service overloaded")
    assert not P._is_overload_body(BODY_QUOTA) and not P._is_overload_body("")
    assert P._thinking_disable_ok("glm-4.7-flash")
    assert P._thinking_disable_ok("glm-4.5-flash")
    assert not P._thinking_disable_ok("glm-5.3")
    assert not P._thinking_disable_ok("glm-5.3-flash")
