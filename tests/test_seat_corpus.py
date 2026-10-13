"""Seat send corpus: compile from Mag providers.yaml, never emit secrets."""
from __future__ import annotations

from mag.seat_corpus import SEND_LAWS, compile_corpus, show


def test_compile_has_deepseek_thinking_off(tmp_path, monkeypatch):
    from mag import seat_corpus as sc
    monkeypatch.setattr(sc, "OUT", tmp_path / "latest.json")
    out = compile_corpus()
    assert out["ok"] is True
    ds = out["lanes"]["deepseek"]
    assert ds["thinking"] == "off"
    assert ds["disable_thinking"] is True
    assert "T0" in ds["never"]
    blob = (tmp_path / "latest.json").read_text(encoding="utf-8")
    assert "sk-" not in blob
    assert "xai-" not in blob
    assert "gsk_" not in blob


def test_show_unknown():
    r = show("not-a-lane")
    assert r["ok"] is False
    assert "deepseek" in r["known"]


def test_send_laws_cover_openclaw_lanes():
    # B2-521: nvidia/cerebras dropped from the pin; the B2-133 dormant gate
    # (mag/dormant.py) removes dormant provider rows from SEND_LAWS entirely
    # (cerebras B2-36, nvidia B2-61), so the corpus only covers drivable seats.
    for k in ("deepseek", "groq", "openrouter", "ollama", "xai"):
        assert k in SEND_LAWS
