"""P3 port lane (2026-10-07): tag-digest pinning + the thinking-default read.

Proofs the build rides on (watch/inbox/frontier_olm_2026-10-07):
- qwen3:4b and qwen3:4b-thinking served byte-identical registry manifests (steal/
  manifest_qwen3_4b*.json), so tags are mutable pointers and pins need a digest column.
- The daemon's POST /api/show exposes per-model thinking defaults in three measured
  shapes (sweep/show_resp_gemma4.json structured, sweep/show_resp_dsr1_15b.json
  capability without defaults, sweep/show_resp_qwen25_7b.json absent key).
All daemon HTTP is mocked here; nothing in this file touches localhost:11434.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import agent_state_router as asr
from mag import ollama_policy as op


# ---------------------------------------------------------------- thinking shapes


def _patch_show(monkeypatch, status: int, body: dict) -> list[tuple[str, str, dict]]:
    calls: list[tuple[str, str, dict]] = []

    def fake(method: str, path: str, req_body: dict | None = None, timeout: float = 3.0):
        calls.append((method, path, req_body or {}))
        return status, body

    monkeypatch.setattr(op, "_request_json", fake)
    return calls


def test_thinking_structured_default_on(monkeypatch):
    """Shape 1 (gemma4): values array with a boolean default, default True."""
    _patch_show(monkeypatch, 200, {
        "thinking": {"values": [False, True], "default": True},
        "capabilities": ["completion", "vision", "thinking"],
    })
    out = op.thinking_condition("gemma4")
    assert out["ok"] is True
    assert out["shape"] == "structured"
    assert out["default"] is True
    assert out["thinking"] == "on"
    assert out["assumed"] is False


def test_thinking_structured_default_off(monkeypatch):
    """Shape 1, off arm: a structured False default is the only OFF verdict."""
    _patch_show(monkeypatch, 200, {"thinking": {"values": [True, False], "default": False}})
    out = op.thinking_condition("some-model")
    assert out["shape"] == "structured"
    assert out["thinking"] == "off"
    assert out["assumed"] is False


def test_thinking_structured_string_level(monkeypatch):
    """Shape 1, level arm: string defaults (low/high/max class) pass through verbatim."""
    _patch_show(monkeypatch, 200, {
        "thinking": {"values": ["low", "high", "max"], "default": "max"},
    })
    out = op.thinking_condition("cloud-model")
    assert out["shape"] == "structured"
    assert out["thinking"] == "max"
    assert out["assumed"] is False


def test_thinking_capability_without_defaults(monkeypatch):
    """Shape 2 (deepseek-r1:1.5b): thinking advertised in capabilities, no values/default."""
    _patch_show(monkeypatch, 200, {"capabilities": ["tools", "thinking", "completion"]})
    out = op.thinking_condition("deepseek-r1:1.5b")
    assert out["ok"] is True
    assert out["shape"] == "capability_only"
    assert out["thinking"] == "on"
    assert out["assumed"] is True


def test_thinking_absent_key_assumes_on(monkeypatch):
    """Shape 3 (qwen2.5:7b): no thinking key anywhere assumes ON, never OFF (one-bug law)."""
    _patch_show(monkeypatch, 200, {"capabilities": ["completion", "tools"]})
    out = op.thinking_condition("qwen2.5:7b")
    assert out["ok"] is True
    assert out["shape"] == "absent"
    assert out["thinking"] == "on"
    assert out["assumed"] is True


def test_thinking_daemon_unreachable_assumes_on(monkeypatch):
    """Transport failure also lands on assume-ON, never OFF."""
    _patch_show(monkeypatch, 0, {"ok": False, "error": "connection refused"})
    out = op.thinking_condition("gemma:2b")
    assert out["ok"] is False
    assert out["shape"] == "unreachable"
    assert out["thinking"] == "on"
    assert out["assumed"] is True


def test_thinking_conditions_ledger(monkeypatch):
    """thinking_conditions reads /api/show per pinned model, one row each."""
    bodies = {
        "gemma4": {"thinking": {"values": [False, True], "default": True}},
        "qwen2.5:7b": {"capabilities": ["completion", "tools"]},
    }

    def fake(method: str, path: str, req_body: dict | None = None, timeout: float = 3.0):
        return 200, bodies.get((req_body or {}).get("model"), {})

    monkeypatch.setattr(op, "JANITOR", "gemma4")
    monkeypatch.setattr(op, "DESK_DEFAULT", "qwen2.5:7b")
    monkeypatch.setattr(op, "KEEP_ALIVE", "gemma4,qwen2.5:7b")
    monkeypatch.setattr(op, "_request_json", fake)
    out = op.thinking_conditions()
    assert out["n"] == 2
    rows = {r["model"]: r for r in out["conditions"]}
    assert rows["gemma4"]["thinking"] == "on"
    assert rows["qwen2.5:7b"]["shape"] == "absent"


# ---------------------------------------------------------------- digest pins


def _patch_tags(monkeypatch, status: int, models: list[dict]):
    def fake(method: str, path: str, req_body: dict | None = None, timeout: float = 3.0):
        assert method == "GET" and path == "/api/tags"
        return status, {"models": models}

    monkeypatch.setattr(op, "_request_json", fake)


def test_verify_pins_mismatch_refuses(monkeypatch):
    """The core gate: pinned digest vs installed digest differs -> REFUSED with all three."""
    monkeypatch.setattr(op, "JANITOR", "gemma:2b")
    monkeypatch.setattr(op, "DESK_DEFAULT", "gemma4-desk")
    monkeypatch.setattr(op, "KEEP_ALIVE", "gemma:2b,gemma4-desk")
    monkeypatch.setenv("MAG_PIN_DIGESTS", "gemma:2b=" + "a" * 64)
    _patch_tags(monkeypatch, 200, [
        {"name": "gemma:2b", "digest": "b" * 64},
        {"name": "gemma4-desk:latest", "digest": "c" * 64},
    ])
    out = op.verify_pins()
    assert out["ok"] is False
    assert len(out["refused"]) == 1
    r = out["refused"][0]
    assert r["tag"] == "gemma:2b"
    assert r["expected"] == "a" * 64
    assert r["actual"] == "b" * 64
    assert r["reason"] == "digest_mismatch"


def test_verify_pins_match_with_sha256_prefix(monkeypatch):
    """A pinned digest carrying the sha256: prefix matches the daemon's bare hex."""
    monkeypatch.setenv("MAG_PIN_DIGESTS", "gemma:2b=sha256:" + "a" * 64)
    _patch_tags(monkeypatch, 200, [{"name": "gemma:2b", "digest": "a" * 64}])
    out = op.verify_pins()
    assert out["ok"] is True
    assert out["matched"] == [{"tag": "gemma:2b", "digest": "a" * 64}]


def test_verify_pins_not_installed_refuses(monkeypatch):
    """A digest-pinned tag missing from the daemon is a refusal (identity unprovable)."""
    monkeypatch.setenv("MAG_PIN_DIGESTS", "gone-model=" + "a" * 64)
    _patch_tags(monkeypatch, 200, [{"name": "gemma:2b", "digest": "a" * 64}])
    out = op.verify_pins()
    assert out["ok"] is False
    assert out["refused"][0]["reason"] == "not_installed"
    assert out["refused"][0]["actual"] is None


def test_verify_pins_daemon_down_fail_closed(monkeypatch):
    """Digest pins exist but the daemon is unreachable: fail closed, not silent pass."""
    monkeypatch.setenv("MAG_PIN_DIGESTS", "gemma:2b=" + "a" * 64)
    _patch_tags(monkeypatch, 0, [])
    out = op.verify_pins()
    assert out["ok"] is False
    assert out["daemon_ok"] is False


def test_verify_pins_unpinned_warns_once(monkeypatch, capsys):
    """No digest pinned: warn-once listing the unpinned pins, gate stays open."""
    monkeypatch.setattr(op, "_UNPINNED_WARNED", set())
    monkeypatch.delenv("MAG_PIN_DIGESTS", raising=False)
    _patch_tags(monkeypatch, 200, [{"name": "gemma:2b", "digest": "a" * 64}])
    first = op.verify_pins()
    second = op.verify_pins()
    assert first["ok"] is True
    assert second["ok"] is True
    assert set(first["unpinned"]) == set(op.pinned_model_names())
    err = capsys.readouterr().err
    assert err.count("unpinned tags") == 1
    assert "gemma:2b" in err


def test_verify_cli_exit_codes(monkeypatch):
    """--verify exits 1 on refusal, 0 when clean."""
    monkeypatch.setattr(op, "_UNPINNED_WARNED", set())
    monkeypatch.setattr(op, "JANITOR", "gemma:2b")
    monkeypatch.setattr(op, "DESK_DEFAULT", "gemma4-desk")
    monkeypatch.setattr(op, "KEEP_ALIVE", "gemma:2b,gemma4-desk")
    monkeypatch.setenv("MAG_PIN_DIGESTS", "gemma:2b=" + "a" * 64)
    _patch_tags(monkeypatch, 200, [{"name": "gemma:2b", "digest": "b" * 64}])
    assert op.main(["--verify"]) == 1
    monkeypatch.setenv("MAG_PIN_DIGESTS", "gemma:2b=" + "b" * 64)
    assert op.main(["--verify"]) == 0


# ---------------------------------------------------------------- consumption point


def test_resolve_daemon_thinking_overrides_local_pin(monkeypatch):
    """A state whose model is a pinned local tag gets the daemon-read level + source."""
    monkeypatch.setattr(op, "JANITOR", "gemma:2b")
    monkeypatch.setattr(op, "DESK_DEFAULT", "gemma4-desk")
    monkeypatch.setattr(op, "KEEP_ALIVE", "gemma:2b,gemma4-desk")
    monkeypatch.setattr(
        op, "thinking_condition",
        lambda model, timeout=3.0: {
            "ok": True, "model": model, "shape": "structured", "default": False,
            "thinking": "off", "assumed": False,
        },
    )
    monkeypatch.setattr(asr, "AGENT_STATES", {
        "local-janitor": {"desc": "test", "model": "gemma:2b", "thinking_level": "none"},
    })
    out = asr.resolve("local-janitor")
    assert out["ok"] is True
    assert out["thinking_level"] == "off"
    assert out["thinking_source"] == "daemon"
    assert out["thinking_condition"]["shape"] == "structured"


def test_resolve_remote_state_keeps_hand_level(monkeypatch):
    """Remote models keep the hand-curated level, stamped thinking_source=hand."""
    out = asr.resolve("research-agent")
    assert out["ok"] is True
    assert out["model"] == asr.PRO
    assert out["thinking_level"] == "high"
    assert out["thinking_source"] == "hand"


def test_resolve_daemon_down_on_local_pin_assumes_on(monkeypatch):
    """Daemon unreachable for a local pin: level ON with an explicit assume-on source."""
    monkeypatch.setattr(op, "JANITOR", "gemma:2b")
    monkeypatch.setattr(op, "DESK_DEFAULT", "gemma4-desk")
    monkeypatch.setattr(op, "KEEP_ALIVE", "gemma:2b,gemma4-desk")
    monkeypatch.setattr(
        op, "thinking_condition",
        lambda model, timeout=3.0: {
            "ok": False, "model": model, "shape": "unreachable",
            "thinking": "on", "assumed": True, "error": "connection refused",
        },
    )
    monkeypatch.setattr(asr, "AGENT_STATES", {
        "local-janitor": {"desc": "test", "model": "gemma:2b", "thinking_level": "none"},
    })
    out = asr.resolve("local-janitor")
    assert out["thinking_level"] == "on"
    assert out["thinking_source"] == "daemon_unreachable_assume_on"


def test_resolve_does_not_mutate_state_table(monkeypatch):
    """resolve copies the spec: the hand-curated table survives daemon overrides."""
    monkeypatch.setattr(op, "thinking_condition",
                        lambda model, timeout=3.0: {"ok": False, "thinking": "on",
                                                    "shape": "unreachable", "assumed": True})
    monkeypatch.setattr(asr, "AGENT_STATES", {
        "x": {"desc": "t", "model": "gemma:2b", "thinking_level": "none"},
    })
    monkeypatch.setattr(op, "JANITOR", "gemma:2b")
    monkeypatch.setattr(op, "DESK_DEFAULT", "gemma4-desk")
    monkeypatch.setattr(op, "KEEP_ALIVE", "gemma:2b,gemma4-desk")
    asr.resolve("x")
    assert asr.AGENT_STATES["x"]["thinking_level"] == "none"
    assert "thinking_source" not in asr.AGENT_STATES["x"]
