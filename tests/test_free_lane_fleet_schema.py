"""Schema-door tests for the free-lane fleet (comics L1 landing, 2026-10-07,
fold watch/inbox/ractor_engine/2026-10-07-stupidmodel-comics). The typed
pass-through is keyed off the queue item: openai-kind seats carry
response_format in the json_schema shape, ollama seats format, cohere
neither; the cohere v2 content-block join runs on the message-content path
(the native shape cohere actually returns), not only the choices path.

No test touches the network: _OPENER is stubbed with a capturing fake and
cycle() runs against a stubbed fire() with tmp queue/ledger roots.
"""
from __future__ import annotations

import io
import json

from tools import free_lane_fleet as flf

SCHEMA = {
    "type": "object",
    "properties": {
        "panels": {"type": "array", "items": {"type": "object", "properties": {
            "pose": {"type": "string", "enum": ["flail", "kick"]},
            "cap": {"type": "string"}}}},
    },
    "required": ["panels"],
}

# Real literals from the PROVIDERS table so the SSRF allowlist passes.
P_OPENAI = {"id": "t-openai", "kind": "openai",
            "url": "https://api.mistral.ai/v1/chat/completions",
            "key_env": "", "model": "m"}
P_COHERE = {"id": "t-cohere", "kind": "cohere",
            "url": "https://api.cohere.com/v2/chat",
            "key_env": "", "model": "m"}
P_OLLAMA = {"id": "t-ollama", "kind": "ollama",
            "url": "http://localhost:11434/api/generate",
            "key_env": "", "model": "m"}


class _FakeOpener:
    """Captures request bodies; replies with a canned provider payload."""

    def __init__(self, payload: dict):
        self.payload = payload
        self.calls: list[dict] = []

    def open(self, req, timeout=90):
        self.calls.append({"url": req.full_url,
                           "body": json.loads(req.data.decode("utf-8"))})
        return io.BytesIO(json.dumps(self.payload).encode("utf-8"))


def _ok_choices(text):
    return {"choices": [{"message": {"role": "assistant", "content": text}}]}


def test_openai_schema_rides_response_format(monkeypatch):
    fo = _FakeOpener(_ok_choices("ok"))
    monkeypatch.setattr(flf, "_OPENER", fo)
    ok, out = flf.fire(P_OPENAI, "p", SCHEMA)
    assert ok and out == "ok"
    body = fo.calls[0]["body"]
    assert body["response_format"]["type"] == "json_schema"
    assert body["response_format"]["json_schema"]["schema"] == SCHEMA


def test_ollama_schema_rides_format(monkeypatch):
    fo = _FakeOpener({"response": "ok"})
    monkeypatch.setattr(flf, "_OPENER", fo)
    ok, out = flf.fire(P_OLLAMA, "p", SCHEMA)
    assert ok and out == "ok"
    assert fo.calls[0]["body"]["format"] == SCHEMA


def test_no_schema_leaves_bodies_untouched(monkeypatch):
    for p, payload in ((P_OPENAI, _ok_choices("ok")), (P_COHERE, _ok_choices("ok")),
                       (P_OLLAMA, {"response": "ok"})):
        fo = _FakeOpener(payload)
        monkeypatch.setattr(flf, "_OPENER", fo)
        ok, _ = flf.fire(p, "p")
        assert ok
        assert "response_format" not in fo.calls[0]["body"]
        assert "format" not in fo.calls[0]["body"]


def test_cohere_schema_left_as_is(monkeypatch):
    fo = _FakeOpener({"message": {"role": "assistant",
                                  "content": [{"type": "text", "text": "ok"}]}})
    monkeypatch.setattr(flf, "_OPENER", fo)
    ok, _ = flf.fire(P_COHERE, "p", SCHEMA)
    assert ok
    assert "response_format" not in fo.calls[0]["body"]


def test_cohere_native_blocks_joined_not_repr(monkeypatch):
    # The arm-A a03/a04/a13 defect: blocks at the TOP-LEVEL message.content
    # were str()-ed into a python repr instead of joined.
    fo = _FakeOpener({"message": {"role": "assistant", "content": [
        {"type": "text", "text": "PANEL 1"},
        {"type": "text", "text": "PANEL 2"}]}})
    monkeypatch.setattr(flf, "_OPENER", fo)
    ok, out = flf.fire(P_COHERE, "p")
    assert ok
    assert out == "PANEL 1 PANEL 2"
    assert "[" not in out and "'" not in out


def test_choices_path_blocks_still_joined(monkeypatch):
    fo = _FakeOpener(_ok_choices([{"type": "text", "text": "a"},
                                  {"type": "text", "text": "b"}]))
    monkeypatch.setattr(flf, "_OPENER", fo)
    ok, out = flf.fire(P_OPENAI, "p")
    assert ok and out == "a b"


def test_reasoning_fallback_survives_join_move(monkeypatch):
    # d4 law: empty content + reasoning_content banks the reasoning.
    fo = _FakeOpener({"choices": [{"message": {"role": "assistant", "content": "",
                                               "reasoning_content": "R"}}]})
    monkeypatch.setattr(flf, "_OPENER", fo)
    ok, out = flf.fire(P_OPENAI, "p")
    assert ok and out == "R"


def test_cycle_carries_queue_schema_and_banks_flag(monkeypatch, tmp_path):
    q = tmp_path / "q"
    q.mkdir()
    runs = tmp_path / "runs"
    (q / "a.json").write_text(json.dumps(
        {"id": "sch:1", "prompt": "p", "schema": SCHEMA}), encoding="utf-8")
    (q / "b.json").write_text(json.dumps(
        {"id": "sch:2", "prompt": "p"}), encoding="utf-8")
    monkeypatch.setattr(flf, "QUEUE", q)
    monkeypatch.setattr(flf, "RUNS", runs)
    monkeypatch.setattr(flf, "LEDGER", runs / "ledger.jsonl")
    monkeypatch.setattr(flf, "HEALTH", runs / "health.json")
    monkeypatch.setattr(flf, "PROVIDERS", [dict(P_OPENAI)])
    seen = []

    def fake_fire(p, prompt, schema=None):
        seen.append((p["id"], schema))
        return True, "ok"

    monkeypatch.setattr(flf, "fire", fake_fire)
    flf.cycle()
    assert ("t-openai", SCHEMA) in seen
    assert ("t-openai", None) in seen
    rows = [json.loads(l) for l in
            (runs / "ledger.jsonl").read_text(encoding="utf-8").splitlines()]
    assert any(r["work_id"] == "sch:1" and r["schema"] is True for r in rows)
    assert any(r["work_id"] == "sch:2" and r["schema"] is False for r in rows)
    # fired-ok queue items retire even under the schema flag
    assert not list(q.glob("*.json"))
