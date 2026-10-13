"""hermes_burn: the inference_budget plan reaches the wire (2026-10-04).

Ruling: watch/inbox/ractor_engine/2026-10-04-parked-decisions/SYNTHESIS.md
:243-250 - plan_call merged thinking_control into plan.extra_body but _call
built {model, messages, max_tokens} only, so the nous-primes reasoning
{max_tokens: 6000} rail never reached the request. Fully offline: _call is
replaced, no key is read, no network is touched.
"""
from __future__ import annotations

import json

import tools.hermes_burn as hb


def test_build_body_merges_plan_and_core_keys_win():
    body = hb._build_body("z-ai/glm-5.3-prime",
                          [{"role": "user", "content": "x"}], 8000,
                          {"reasoning": {"max_tokens": 6000}, "model": "evil"})
    assert body["reasoning"] == {"max_tokens": 6000}
    assert body["model"] == "z-ai/glm-5.3-prime"
    assert body["max_tokens"] == 8000


def test_build_body_without_plan_is_the_old_shape():
    body = hb._build_body("m", [], 10)
    assert body == {"model": "m", "messages": [], "max_tokens": 10}


def test_fire_ask_sends_the_computed_plan(monkeypatch, tmp_path):
    (tmp_path / "ev.md").write_text("EVIDENCE HEAD bytes for the plan-wire probe\n",
                                    encoding="utf-8")
    ask = tmp_path / "asks" / "PW1"
    ask.mkdir(parents=True)
    (ask / "ask.json").write_text(json.dumps({
        "id": "PW1", "model": "z-ai/glm-5.3-prime", "contract": "c",
        "evidence": ["ev.md"], "max_tokens": 8000}), encoding="utf-8")
    monkeypatch.setattr(hb, "ROOT", tmp_path)
    monkeypatch.setattr(hb, "OUT_DIR", tmp_path / "out")
    monkeypatch.setattr(hb, "USAGE", tmp_path / "usage.jsonl")
    monkeypatch.setitem(hb.PRICING, "z-ai/glm-5.3-prime", (0.0, 0.0))
    monkeypatch.setattr(hb, "_system_for", lambda model: "SYS")
    seen: dict = {}

    def fake_call(model, messages, max_tokens, key, retries=1, extra_body=None):
        seen["body"] = hb._build_body(model, messages, max_tokens, extra_body)
        return {"choices": [{"message": {"content": "deliverable text"},
                             "finish_reason": "stop"}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 5,
                          "completion_tokens_details": {"reasoning_tokens": 0}}}

    monkeypatch.setattr(hb, "_call", fake_call)
    hb._fire_ask(ask, "not-a-key", execute=True)
    assert seen["body"]["reasoning"] == {"max_tokens": 6000}
    assert seen["body"]["max_tokens"] >= 8000
