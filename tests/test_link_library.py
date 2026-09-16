"""tests for mag/link_library.py -- the canonical URL registry (operator drop 2026-09-14).

Ledger-isolated: every test monkeypatches LEDGER to a tmp_path file, so the real
watch/inbox/LINKS.jsonl is never touched. The canonicalization law under test: the same
post arriving as five URLs must be ONE ledger row -- duplication is emphasis for humans,
drift for the ledger.
"""
from __future__ import annotations

import json

import pytest

import mag.link_library as ll


@pytest.fixture()
def ledger(tmp_path, monkeypatch):
    fake = tmp_path / "LINKS.jsonl"
    monkeypatch.setattr(ll, "LEDGER", fake)
    return fake


# -- canonicalization ------------------------------------------------------------------

def test_strips_tracking_param_s():
    url = "https://x.com/NachoQuixotic/status/2071636215309156788?s=20"
    assert ll.canonicalize(url) == "https://x.com/NachoQuixotic/status/2071636215309156788"


def test_twitter_and_mobile_hosts_collapse_to_x():
    for host in ("twitter.com", "mobile.x.com", "m.x.com"):
        assert ll.canonicalize(f"https://{host}/user/status/1") == "https://x.com/user/status/1"


def test_utm_and_tracking_params_die():
    url = ("https://airchilly.com/products/mushroom-container-farm/"
           "container-farm-introduction/?gad_source=1&gclid=abc&utm_campaign=x&keep=1")
    assert ll.canonicalize(url) == "https://airchilly.com/products/mushroom-container-farm/container-farm-introduction?keep=1"


def test_params_sorted_and_empty_dropped():
    assert ll.canonicalize("https://ex.com/p?b=2&a=1&a=&z") == "https://ex.com/p?a=1&b=2"


def test_fragment_dropped_and_default_port_stripped():
    assert ll.canonicalize("https://ex.com:443/p#m") == "https://ex.com/p"
    assert ll.canonicalize("http://ex.com:80/p") == "http://ex.com/p"
    assert ll.canonicalize("https://ex.com:8080/p") == "https://ex.com:8080/p"


def test_trailing_slash_stripped():
    assert ll.canonicalize("https://ex.com/dir/") == "https://ex.com/dir"
    assert ll.canonicalize("https://ex.com/") == "https://ex.com"


def test_userinfo_stripped():
    assert ll.canonicalize("https://user:secret@example.com/p") == "https://example.com/p"


def test_non_http_schemes_refused():
    for bad in ("ftp://ex.com/a", "file:///C:/x", "javascript:alert(1)"):
        with pytest.raises(ValueError):
            ll.canonicalize(bad)


def test_canonical_sha256_is_uppercase_and_stable():
    a = ll.canonical_sha256("https://x.com/a")
    b = ll.canonical_sha256("https://x.com/a")
    assert a == b and a == a.upper() and len(a) == 64


# -- host safety (the Mimosa guard) -----------------------------------------------------

@pytest.mark.parametrize("bad", [
    "http://localhost/a", "http://mine.local/a", "http://svc.internal/a",
    "http://10.1.2.3/a", "http://127.0.0.1/a", "http://192.168.1.4/a",
    "http://172.16.0.9/a", "http://172.31.255.1/a", "http://169.254.169.254/latest",
    "http://metadata.google.internal/computeMetadata/v1/",
])
def test_private_and_reserved_hosts_refused(bad):
    with pytest.raises(ValueError):
        ll.validate_host_safety(bad)


def test_public_host_allowed():
    ll.validate_host_safety("https://x.com/a")  # must not raise
    ll.validate_host_safety("http://172.32.0.1/a")  # 172.32 is public space


# -- ledger behavior (isolated to tmp) ---------------------------------------------------

def test_add_then_detect_duplicate(ledger):
    first = ll.add_urls(["https://x.com/u/status/9?s=20"], note="seed", writer="test")
    assert ledger.exists() and len(first) == 1
    entry = first[0]
    assert entry["canonical"] == "https://x.com/u/status/9"
    assert entry["duplicate_of"] == ""
    for key in ("seq", "ts", "canonical", "url", "canonical_sha256",
                "title", "duplicate_of", "writer", "note"):
        assert key in entry
    second = ll.add_urls(["https://mobile.x.com/u/status/9"], writer="test")
    assert second[0]["duplicate_of"] == "https://x.com/u/status/9?s=20"  # first submission's raw url
    assert len(ll.load_ledger()) == 2


def test_known_canonicals_maps_by_canonical(ledger):
    ll.add_urls(["https://ex.com/a"])
    known = ll.known_canonicals()
    assert list(known) == ["https://ex.com/a"]


def test_check_exit_codes(ledger, monkeypatch, capsys):
    ll.add_urls(["https://ex.com/known"])
    monkeypatch.setattr("sys.argv", ["prog", "check", "https://ex.com/known?utm_source=x"])
    assert ll.main() == 1  # known -> exit 1 (SystemExit wrapping happens at __main__)
    monkeypatch.setattr("sys.argv", ["prog", "check", "https://ex.com/unknown"])
    assert ll.main() == 0  # unknown -> exit 0


def test_dupes_reports_and_does_not_crash(ledger, capsys):
    ll.add_urls(["https://ex.com/one"])
    ll.add_urls(["https://ex.com/one?utm_campaign=again"])
    monkeypatch_argv = ["prog", "dupes"]
    import sys
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(sys, "argv", monkeypatch_argv)
    try:
        assert ll.main() == 0
    finally:
        monkeypatch.undo()
    out = capsys.readouterr().out
    assert "1 duplicate submissions on file" in out
