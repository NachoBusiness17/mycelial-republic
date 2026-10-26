"""Voice shadow scout tests."""
from __future__ import annotations

from unittest.mock import patch

from mag import voice_shadow as vs


def test_shadow_context_empty_until_ready(tmp_path, monkeypatch):
    monkeypatch.setattr(vs, "SHADOW_DIR", tmp_path)
    sid = "sh-1"
    assert vs.shadow_context_for_local(sid) == ""
    vs.save_shadow(sid, {"status": "ready", "brief": "FACTS: SAM is Resizable BAR", "trigger": "smart access"})
    ctx = vs.shadow_context_for_local(sid)
    assert "SAM" in ctx or "Resizable" in ctx
    assert "Background scout" in ctx


def test_start_skips_phatic(tmp_path, monkeypatch):
    monkeypatch.setattr(vs, "SHADOW_DIR", tmp_path)
    out = vs.start_shadow_scout("sh-2", "thanks")
    assert out.get("status") == "skipped"


def test_start_kicks_thread(tmp_path, monkeypatch):
    monkeypatch.setattr(vs, "SHADOW_DIR", tmp_path)
    # B2-288 fix (2026-09-26): the scout daemon does its first import of
    # mag.voice_dig_board (note_scout_ready) INSIDE the thread; on a cold
    # import that single transition measured about 3.4s on this box while the
    # old deadline polled for 1.5s, so the test read status "running" and
    # failed standalone. Flake source is the fixed short deadline over a cold
    # import path, not the product: pre-import the board module on the main
    # thread and keep polling with an early break up to 15s.
    import mag.voice_dig_board  # noqa: F401  (move the cold import off the daemon)

    def fake_chat(*a, **k):
        return {"ok": True, "text": "FACTS: test\nREADY LINE: ready", "model": "deepseek"}

    with patch("models.providers.chat_provider", side_effect=fake_chat):
        out = vs.start_shadow_scout("sh-3", "what is AMD smart access memory")
        assert out.get("status") == "running"
        # wait briefly for daemon
        import time

        for _ in range(300):
            st = vs.shadow_status("sh-3")
            if st.get("status") in ("ready", "failed"):
                break
            time.sleep(0.05)
        st = vs.shadow_status("sh-3")
        assert st.get("status") == "ready"
        assert st.get("has_brief") is True
