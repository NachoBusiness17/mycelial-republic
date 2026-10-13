"""Strip-at-use law regression (B5, build wave 2026-10-05).

The five Bearer-from-env modules the CSV verdict named must strip the key
before it reaches an Authorization header. Cause: the 2026-10-04 CR-header
outage - .env on this box was CRLF, the key carried a trailing \\r into
"Bearer " + key, urllib rejected the header value, and the elder lane sat
down for 14 cycles (receipt watch/inbox/go_wave_20261004/CSV_VERDICT_20261004.md
residual note; permanent-law receipt watch/inbox/build_wave_20261005/b5_strip_at_use.md).

Sites under test:
  mag/auth_switchboard.py probe_key
  mag/autoglm.py _key env branch (exercised through act)
  mag/doctor.py _probe_remote_deep
  mag/fanout.py fire
  mag/flight_recorder.py api_call

A key with trailing \\r\\n must produce a clean header at every site. All
transport is faked: the capture opener/urlopen records the built Request and
raises, so no socket is ever opened.
"""
from __future__ import annotations

import urllib.request

import pytest

from mag import auth_switchboard, autoglm, doctor, fanout, flight_recorder  # noqa: E402

DIRTY = "sk-strip-use-unit\r\n"
CLEAN = "sk-strip-use-unit"
EXPECT_AUTH = "Bearer " + CLEAN


class _Captured(Exception):
    """Raised by the fake transport once the Request (and its headers) is built."""


def test_bearer_strip_at_use_five_sites(monkeypatch):
    seen = {}

    class FakeOpener:
        def open(self, req, timeout=None):
            seen["req"] = req
            raise _Captured("fake transport")

    def fake_urlopen(req, timeout=None):
        seen["req"] = req
        raise _Captured("fake transport")

    # 1. auth_switchboard.probe_key (x-api-key + Authorization from one key)
    monkeypatch.setattr(auth_switchboard, "_guard_probe_url", lambda url: None)
    monkeypatch.setattr(urllib.request, "build_opener", lambda *a, **k: FakeOpener())
    verdict = auth_switchboard.probe_key(DIRTY)
    assert verdict["ok"] is None  # fake transport wall, NOT a header rejection
    assert seen["req"].headers["Authorization"] == EXPECT_AUTH
    assert seen["req"].headers["X-api-key"] == CLEAN

    # 2. autoglm._key env branch -> act (Lite is first in KEY_NAMES)
    monkeypatch.setattr(autoglm, "_validate_endpoint", lambda: None)
    monkeypatch.setattr(autoglm, "_OPENER", FakeOpener())
    monkeypatch.setenv("ZAI_API_KEY_Lite", DIRTY)
    out = autoglm.act("data:image/png;base64,AAAA", "tap the button")
    assert out["ok"] is False  # fake transport error, header was already clean
    assert seen["req"].headers["Authorization"] == EXPECT_AUTH

    # 3. doctor._probe_remote_deep (headers shared by /models GET and chat ping)
    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    probe = doctor._probe_remote_deep("https://unit.test/v1", 5.0, "test-model", DIRTY)
    assert probe["status"] == "DOWN"  # fake transport, header already built + captured
    assert seen["req"].headers["Authorization"] == EXPECT_AUTH

    # 4. fanout.fire (key_env read off os.environ)
    monkeypatch.setattr(fanout, "guarded_fetch", lambda url: FakeOpener())
    monkeypatch.setenv("MAG_B5_STRIP_KEY", DIRTY)
    pack = {"base": fanout.DEFAULT_BASE, "key_env": "MAG_B5_STRIP_KEY", "shared_head": "HEAD"}
    lane = {"id": "L01", "context": "ctx", "task": "do it"}
    _lane_id, _text, _usage, _dt, err = fanout.fire(pack, lane)
    assert err == "fake transport"  # fake transport error, not a header rejection
    assert seen["req"].headers["Authorization"] == EXPECT_AUTH

    # 5. flight_recorder.api_call (api_call catches only HTTPError, so the capture raises)
    with pytest.raises(_Captured):
        flight_recorder.api_call("glm-5.3-flash", "ping", DIRTY, max_tokens=4, timeout=5)
    assert seen["req"].headers["Authorization"] == EXPECT_AUTH
