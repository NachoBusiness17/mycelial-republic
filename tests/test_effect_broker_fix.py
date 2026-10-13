"""effect_broker allow/denylist parsing — audit finding #6 regression tests.

FIX RECEIPT (2026-09-29, watch/inbox/last_mile_20260930/AG3_BROKER_SPLIT.md,
audit source watch/inbox/MAG_SYSTEMS_DEEP_ANALYSIS_20260930.md finding #6):
the broker built FS_ALLOWLIST / TOOL_CWD_ALLOWLIST / NETWORK_DENYLIST with
":".join(...).split(":"), which shredded Windows drive paths
("C:\\repo\\board" -> ["C", "\\repo\\board"]) and shredded "::1" into empty
strings.  Because `"" in url` is always True, EVERY network_access effect
was denied on Windows while the built-in self-test kept passing (it only
exercised the deny case).  These tests pin the fixed behavior: real lists,
no empty entries, a POSITIVE network path, and loopback denials.
"""
from __future__ import annotations

import importlib
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _auth(effect: str, event_id: str) -> dict:
    """A clean authority record that passes the reference-monitor gate."""
    return {
        "status": "AUTHORIZED",
        "granted_capabilities": [effect],
        "event_id": event_id,
        "budget": {"max_calls": 5},
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ttl_seconds": 900,
    }


class _FakeResp:
    """Stand-in for urllib's response so the positive test needs no network."""

    status = 200

    def read(self, n: int = -1) -> bytes:
        return b"<html>allowed</html>"

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def test_denylist_has_real_entries_and_no_empty_strings():
    from mag import effect_broker as eb

    # "::1" must survive parsing as one real entry; an empty entry would
    # match every url ("" in url is always True) and deny the world.
    assert "::1" in eb.NETWORK_DENYLIST
    assert "127.0.0.1" in eb.NETWORK_DENYLIST
    assert "localhost" in eb.NETWORK_DENYLIST
    assert "0.0.0.0" in eb.NETWORK_DENYLIST
    assert all(entry != "" for entry in eb.NETWORK_DENYLIST), (
        f"empty deny entry denies every url, got {eb.NETWORK_DENYLIST!r}")


def test_fs_allowlist_unshredded_on_windows_paths():
    from mag import effect_broker as eb

    # The old ":".join(...).split(":") turned "C:\\repo\\board" into
    # ["C", "\\repo\\board"]; the fixed default must be the four whole
    # repo roots, with no drive-letter or empty fragments.
    assert str(ROOT / "board") in eb.FS_ALLOWLIST
    assert str(ROOT / "patches") in eb.FS_ALLOWLIST
    assert str(ROOT / "memory") in eb.FS_ALLOWLIST
    assert str(ROOT / "bridge") in eb.FS_ALLOWLIST
    assert all(entry and entry != "C" for entry in eb.FS_ALLOWLIST), (
        f"shredded FS_ALLOWLIST: {eb.FS_ALLOWLIST!r}")
    assert str(ROOT) in eb.TOOL_CWD_ALLOWLIST


def test_network_positive_allowed_url_completes(monkeypatch):
    """POSITIVE case the old self-test never had: an ordinary external url
    passes the fixed denylist and the effect completes end-to-end."""
    from mag import effect_broker as eb

    monkeypatch.setattr(urllib.request, "urlopen",
                        lambda req, timeout=None: _FakeResp())
    auth = _auth("network_access", "test-net-positive-1")
    rec = eb.execute(
        "network_access", {"url": "https://example.com/index.html"}, auth)

    assert rec["status"] == "RECEIPT_COMMITTED"
    assert rec["result"]["ok"] is True, rec.get("error")
    assert rec["result"]["status"] == 200
    assert "allowed" in rec["result"]["body"]


def test_network_negative_loopback_family_denied():
    from mag import effect_broker as eb

    auth = _auth("network_access", "test-net-negative-1")
    for url in (
        "http://localhost:8000/secret",
        "http://127.0.0.1:8000/secret",
        "http://[::1]:8000/secret",
        "http://0.0.0.0:8000/secret",
    ):
        rec = eb.execute("network_access", {"url": url}, auth)
        assert rec["status"] == "RECEIPT_COMMITTED"
        assert rec["result"]["ok"] is False, url
        assert "denied pattern" in (rec.get("error") or ""), url


def test_fs_write_roundtrip_on_windows_path():
    from mag import effect_broker as eb

    tmp = ROOT / "memory" / "effect_broker_fix_test_tmp.txt"
    auth = _auth("fs_write", "test-fs-positive-1")
    rec = eb.execute("fs_write", {"path": str(tmp), "content": "x"}, auth)
    assert rec["status"] == "RECEIPT_COMMITTED"
    assert rec["result"]["ok"] is True, rec.get("error")
    if tmp.exists():
        tmp.unlink()

    outside = Path(tempfile.gettempdir()) / "effect_broker_fix_evil.txt"
    rec2 = eb.execute("fs_write", {"path": str(outside), "content": "x"}, auth)
    assert rec2["status"] == "RECEIPT_COMMITTED"
    assert rec2["result"]["ok"] is False
    assert "not in FS_ALLOWLIST" in (rec2.get("error") or "")
    assert not outside.exists()


def test_env_override_is_json_list_and_rejects_bad_entries(monkeypatch):
    from mag import effect_broker as eb

    env = "MAG_NETWORK_DENYLIST"
    try:
        # operator override: a JSON list replaces the default wholesale
        monkeypatch.setenv(env, '["10.0.0.1"]')
        mod = importlib.reload(eb)
        assert mod.NETWORK_DENYLIST == ["10.0.0.1"]
        assert mod._broker_network_access(
            {"url": "http://10.0.0.1/x"}, {})["ok"] is False

        # legacy colon format and empty-string entries must fail loud at
        # parse, never silently deny-everything / allow-everything
        for bad in ("127.0.0.1:localhost", '["127.0.0.1", ""]', "not-json"):
            monkeypatch.setenv(env, bad)
            try:
                importlib.reload(mod)
            except ValueError as exc:
                assert env in str(exc)
            else:
                raise AssertionError(f"bad {env}={bad!r} must raise ValueError")
    finally:
        monkeypatch.delenv(env, raising=False)
        importlib.reload(eb)  # restore real lists for other tests

    assert "::1" in eb.NETWORK_DENYLIST
