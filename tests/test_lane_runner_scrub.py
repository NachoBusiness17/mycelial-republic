"""Regression: lane trail events must never carry raw credentials.

Cause: 2026-10-04, a CYCLE_FAIL detail carried the raw b'Bearer sk-or-v1-...'
header into queue/lanes/elder/trail.jsonl + surface.md and both dashboard
copies; the key byte-matched the live .env value and was caught pre-commit by
the prepush_credential_shape WARN (go_wave_20261004). Fix: _scrub_credentials
at the _trail chokepoint, prefix preserved for forensics.
"""
from mag.lane_runner import _scrub_credentials, _trail


def test_scrub_redacts_openrouter_key_keeps_prefix():
    # Synthetic fixture: same shape as the 2026-10-04 elder-leak key
    # (sk-or-v1- prefix, 56 hex chars) but never a real credential.
    detail = "lane-down: Invalid header value b'Bearer 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'"
    out = _scrub_credentials(detail)
    assert "sk-or-v1-dea[REDACTED]" in out
    assert "29294de13e255febbda" not in out


def test_scrub_redacts_bare_key_and_other_shapes():
    assert _scrub_credentials("key sk-abcdefghijklmnop1234567890 done").count("[REDACTED]") == 1
    assert _scrub_credentials("xai-abcdefghij0123456789").endswith("[REDACTED]")
    assert _scrub_credentials("gsk_abcdefghijklmnop").endswith("[REDACTED]")
    out = _scrub_credentials("AIzaSyA1234567890abcdefghijklmnopqrstuvw")
    assert "bcdefghij" not in out



def test_scrub_leaves_ordinary_detail_untouched():
    plain = "lane-down: connection refused after 3 tries (https://example.com/api)"
    assert _scrub_credentials(plain) == plain


def test_trail_chokepoint_writes_scrubbed_detail(tmp_path, monkeypatch):
    import mag.lane_runner as lr
    monkeypatch.setattr(lr, "LANES", tmp_path)
    _trail("elder", "CYCLE_FAIL", "fail Bearer sk-or-v1-aaaaaaaaaaaaaaaaaaaa2")
    row = (tmp_path / "elder" / "trail.jsonl").read_text(encoding="utf-8")
    assert "aaaaaaaa" not in row
    assert "[REDACTED]" in row
