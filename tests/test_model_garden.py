"""model_garden tests (lane 2 RUNNER, 2026-10-01).

Covers the three CARRIER-PATCH guards as generalized (landed-skip,
REFUSED terminal, evidence preflight), the FAMILY_TABLE allowlist fence
plus the DNS-resolution SSRF half, and one mocked happy path (no real API
fires anywhere in this file: every execute path monkeypatches _call).
"""
from __future__ import annotations

import json
import socket

import pytest

from tools import model_garden as mg


@pytest.fixture
def garden(tmp_path, monkeypatch):
    """Synthetic mini-estate: ROOT/OUT_DIR/USAGE pointed at tmp_path."""
    monkeypatch.setattr(mg, "ROOT", tmp_path)
    monkeypatch.setattr(mg, "OUT_DIR", tmp_path / "watch" / "inbox" / "model_garden")
    monkeypatch.setattr(mg, "USAGE", tmp_path / "memory" / "runs" / "model_garden" / "usage.jsonl")
    return tmp_path


def stage_ask(root, ask_id="T1", **over):
    """Stage one ask dir + its evidence file; over keys replace ask.json."""
    d = root / ask_id
    d.mkdir(parents=True, exist_ok=True)
    (root / "ev.txt").write_text("MATERIAL-BYTES 123\n" + "filler " * 100,
                                 encoding="utf-8")
    meta = {"id": ask_id, "model": "test/model-x", "base_env": "GARDEN_TEST_KEY",
            "base_url": "https://api.deepseek.com/v1",
            "contract": "Deliver one spec.", "evidence": ["ev.txt"],
            "max_tokens": 64}
    meta.update(over)
    (d / "ask.json").write_text(json.dumps(meta), encoding="utf-8")
    return d


def _ok_call(seen=None):
    def fake(model, messages, max_tokens, key, base_url, retries=1):
        if seen is not None:
            seen.update(model=model, key=key, base_url=base_url,
                        body=messages[0]["content"])
        return {"usage": {"prompt_tokens": 100, "completion_tokens": 42,
                          "completion_tokens_details": {"reasoning_tokens": 7}},
                "choices": [{"message": {"content": "DELIVERABLE BYTES"}}]}
    return fake


# --- guard 1: landed-skip unless revision ----------------------------------

def test_landed_skip_beats_force(garden, monkeypatch):
    d = stage_ask(garden)
    mg.OUT_DIR.mkdir(parents=True)
    (mg.OUT_DIR / "T1.md").write_text("landed", encoding="utf-8")

    def boom(*a, **k):
        raise AssertionError("_call fired on a landed ask")
    monkeypatch.setattr(mg, "_call", boom)
    row = mg.run_ask(d, key="k", execute=True)
    assert row["ok"] and "skipped" in row


def test_revision_reopens_landed_ask(garden, monkeypatch):
    d = stage_ask(garden, revision=True, turn2_only=True)
    (d / "revision.md").write_text("tighten the spec", encoding="utf-8")
    mg.OUT_DIR.mkdir(parents=True)
    (mg.OUT_DIR / "T1.md").write_text("landed", encoding="utf-8")
    monkeypatch.setattr(mg, "_call", _ok_call())
    row = mg.run_ask(d, key="k", execute=True)
    assert row["ok"] and not row.get("skipped")
    out = (mg.OUT_DIR / "T1.md").read_text(encoding="utf-8")
    assert "landed" in out and "REVISION (turn 2)" in out


# --- guard 2: REFUSED terminal after 2 refusals ----------------------------

def test_refused_terminal_after_two(garden, monkeypatch):
    d = stage_ask(garden, ask_id="R1")
    calls = []

    def refuse(*a, **k):
        calls.append(1)
        return {"usage": {"prompt_tokens": 3, "completion_tokens": 0},
                "choices": [{"message": {"content": None,
                                         "refusal": "cannot comply"}}]}
    monkeypatch.setattr(mg, "_call", refuse)
    with pytest.raises(RuntimeError, match="REFUSED"):
        mg.run_ask(d, key="k", execute=True)
    assert not (d / "REFUSED").exists()  # first refusal: not terminal yet
    with pytest.raises(RuntimeError, match="REFUSED"):
        mg.run_ask(d, key="k", execute=True)
    assert (d / "REFUSED").is_file()
    row = mg.run_ask(d, key="k", execute=True)  # third cycle: skip on sight
    assert row["skipped"].startswith("REFUSED")
    assert len(calls) == 2  # no third fire, ever


def test_refusal_backfill_mints_marker(garden):
    d = stage_ask(garden, ask_id="R2")
    for _ in range(2):  # pre-marker ledger rows heal without a new fire
        mg._bank({"ts": "t", "id": "R2", "model": "m",
                  "model_family": "deepseek",
                  "base_url": "https://api.deepseek.com/v1",
                  "turn": 1, "refused": "snip", "ok": False})
    row = mg.run_ask(d, key="k", execute=True)
    assert (d / "REFUSED").is_file() and row["skipped"].startswith("REFUSED")


def test_refusals_scoped_per_family(garden, monkeypatch):
    # 2 deepseek refusals must NOT terminal an xai ask with the same id
    d = stage_ask(garden, ask_id="S1", base_url="https://api.x.ai/v1")
    for _ in range(2):
        mg._bank({"ts": "t", "id": "S1", "model_family": "deepseek",
                  "base_url": "https://api.deepseek.com/v1",
                  "turn": 1, "refused": "snip", "ok": False})
    monkeypatch.setattr(mg, "_call", _ok_call())
    row = mg.run_ask(d, key="k", execute=True)
    assert row["ok"] and not row.get("skipped")


# --- guard 3: evidence preflight --------------------------------------------

def test_evidence_preflight_fails_closed(garden, monkeypatch):
    monkeypatch.setattr(mg, "_call", _ok_call())
    d = stage_ask(garden, ask_id="E1", evidence=[])
    with pytest.raises(RuntimeError, match="no evidence paths"):
        mg.run_ask(d, key="k", execute=True)
    d = stage_ask(garden, ask_id="E2", evidence=["nope.txt"])
    with pytest.raises(RuntimeError, match="missing on disk"):
        mg.run_ask(d, key="k", execute=True)
    # render step dropped the material: bytes absent from the body sent
    meta = json.loads((stage_ask(garden, ask_id="E3") / "ask.json")
                      .read_text(encoding="utf-8"))
    body = [{"role": "user", "content": "a body without the material"}]
    with pytest.raises(RuntimeError, match="absent from the message body"):
        mg._assert_evidence_in_body(meta, body)


def test_dry_mode_runs_preflight_offline(garden):
    d = stage_ask(garden, ask_id="D1", evidence=[])
    with pytest.raises(RuntimeError, match="no evidence paths"):
        mg.run_ask(d, execute=False)  # no key, no API: still fails closed


# --- allowlist fence + SSRF --------------------------------------------------

def test_family_allowlist_fence():
    for bad in ("http://api.x.ai/v1", "https://evil.example.com/v1",
                "https://api.deepseek.com.evil.io/v1",
                "https://user@api.groq.com/v1", "not a url"):
        with pytest.raises(RuntimeError, match="fence"):
            mg._endpoint(bad)
    url, host = mg._endpoint("https://inference-api.nousresearch.com")
    assert host == "inference-api.nousresearch.com"
    assert url == "https://inference-api.nousresearch.com/v1/chat/completions"
    assert mg._endpoint("https://api.deepseek.com/v1")[0] == \
        "https://api.deepseek.com/v1/chat/completions"
    assert mg._endpoint("https://api.groq.com/openai/v1")[0] == \
        "https://api.groq.com/openai/v1/chat/completions"
    full = "https://openrouter.ai/api/v1/chat/completions"
    assert mg._endpoint(full)[0] == full
    for host, fam in [("nousresearch.com", "nous"), ("api.x.ai", "xai"),
                      ("api.moonshot.ai", "moonshot"),
                      ("generativelanguage.googleapis.com", "google"),
                      ("api.groq.com", "groq"), ("openrouter.ai", "openrouter")]:
        assert mg._family_of(host) == fam


def test_fence_at_run_ask_entry(garden):
    d = stage_ask(garden, ask_id="F1", base_url="https://evil.example.com/v1")
    with pytest.raises(RuntimeError, match="not in FAMILY_TABLE"):
        mg.run_ask(d, key="k", execute=True)


def test_ssrf_resolution_fence(monkeypatch):
    def fake_getaddrinfo(host, port, proto=None, *a, **k):
        return [(2, 1, 6, "", ("10.0.0.5", 443))]  # private IP
    monkeypatch.setattr(socket, "getaddrinfo", fake_getaddrinfo)
    with pytest.raises(RuntimeError, match="non-public"):
        mg._assert_public_host("api.deepseek.com")


def test_call_fence_rejects_before_wire():
    with pytest.raises(RuntimeError, match="fence"):
        mg._call("m", [{"role": "user", "content": "x"}], 8, "k",
                 "https://evil.example.com")  # raises before any urlopen


# --- mocked happy path -------------------------------------------------------

def test_happy_path_banks_and_lands(garden, monkeypatch):
    d = stage_ask(garden, ask_id="H1")
    seen = {}
    monkeypatch.setattr(mg, "_call", _ok_call(seen))
    row = mg.run_ask(d, key="kk", execute=True)
    assert row["ok"] and row["model_family"] == "deepseek"
    assert row["cost_usd"] == 0.0  # unknown model: tokens banked, no price
    out = (mg.OUT_DIR / "H1.md").read_text(encoding="utf-8")
    assert "DELIVERABLE BYTES" in out and "test/model-x" in out
    led = json.loads(mg.USAGE.read_text(encoding="utf-8").strip().splitlines()[-1])
    assert (led["id"], led["model_family"], led["ok"]) == ("H1", "deepseek", True)
    assert led["base_url"] == "https://api.deepseek.com/v1"
    assert led["prompt_tokens"] == 100 and led["completion_tokens"] == 42
    assert led["reasoning_tokens"] == 7 and led["channel"] == "content"
    assert "MATERIAL-BYTES 123" in seen["body"]  # evidence reached the wire
    assert (seen["model"], seen["key"]) == ("test/model-x", "kk")


def test_cli_dry_and_usage_exit_codes(garden, capsys):
    stage_ask(garden, ask_id="C1")  # garden root doubles as the queue dir
    assert mg.main([str(garden), "--dry"]) == 0
    out = capsys.readouterr().out
    assert "C1 [deepseek]" in out and "PASS 1/1 asks" in out
    assert not mg.USAGE.exists()  # dry banks nothing
    assert mg.main([str(garden / "nope")]) == 2
    (garden / "empty").mkdir()
    assert mg.main([str(garden / "empty")]) == 2
