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


# -- event ledger split (B2-28, 2026-09-26) ------------------------------------------------

def test_load_events_missing_file_is_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(ll, "EVENTS", tmp_path / "absent.jsonl")
    assert ll.load_events() == []


def test_load_events_reads_schema_rows_and_refuses_schemaless(tmp_path, monkeypatch):
    events = tmp_path / "EVENTS.jsonl"
    good = {"ts": "2026-09-26T00:00:00Z", "id": "E1", "kind": "finding",
            "detail": "d", "schema": "event.v1",
            "origin": {"file": "watch/inbox/LINKS.jsonl", "line": 1}}
    bad = {"ts": "2026-09-26T00:00:00Z", "id": "E2", "kind": "finding"}
    events.write_text(json.dumps(good) + "\n", encoding="utf-8")
    monkeypatch.setattr(ll, "EVENTS", events)
    assert ll.load_events()[0]["id"] == "E1"
    with events.open("a", encoding="utf-8") as f:
        f.write(json.dumps(bad) + "\n")
    with pytest.raises(ValueError):
        ll.load_events()  # schema-less row cannot rot back in unannounced


def test_load_events_skips_only_named_backfilled_rows(tmp_path, monkeypatch):
    # No-erase backfill (SCOUT_CHARTER_20260926.md section 4, 2026-09-29): a
    # schema-less row is repaired by an appended carrier row whose origin names
    # it (origin.replaces = its id); the named debt is accepted and skipped,
    # while the test above proves unnamed schema-less rows still raise.
    events = tmp_path / "EVENTS.jsonl"
    good = {"ts": "2026-09-26T00:00:00Z", "id": "E1", "kind": "finding",
            "detail": "d", "schema": "event.v1",
            "origin": {"file": "watch/inbox/LINKS.jsonl", "line": 1}}
    bad = {"ts": "2026-09-26T00:00:00Z", "id": "E2", "kind": "finding"}
    carrier = {"ts": "2026-09-29T00:00:00Z", "id": "E2-BACKFILL", "kind": "finding",
               "detail": "d", "schema": "event.v1",
               "origin": {"file": "watch/inbox/EVENTS.jsonl", "line": 2,
                          "replaces": "E2"}}
    with events.open("w", encoding="utf-8") as f:
        f.write(json.dumps(good) + "\n")
        f.write(json.dumps(bad) + "\n")
        f.write(json.dumps(carrier) + "\n")
    monkeypatch.setattr(ll, "EVENTS", events)
    served = ll.load_events()
    assert [r["id"] for r in served] == ["E1", "E2-BACKFILL"]


# -- scout check-gate (B2-27, 2026-09-26) ---------------------------------------------------
# The B2-06 shape: free-resource-scout re-confirmations of an already-filed
# canonical must carry duplicate_of AT SUBMISSION (they landed silent before).

def test_check_url_gate_reports_known_with_first_entry(ledger):
    ll.add_urls(["https://www.thundercompute.com/blog/free-cloud-gpu-credits"],
                note="scout find", writer="free-resource-scout")
    verdict = ll.check_url(
        "https://www.thundercompute.com/blog/free-cloud-gpu-credits?utm_source=daily")
    assert verdict["known"] is True
    assert verdict["first_entry"]["writer"] == "free-resource-scout"


def test_known_canonicals_first_filing_wins(ledger):
    # B2-122 (2026-09-26): the dict comprehension was last-writer-wins, so
    # check_url.first_entry and add_urls duplicate_of pointed at the NEWEST
    # dupe row, not the first filing. The ledger is append-only with monotonic
    # seq, so first occurrence in file order is the earliest filing.
    ll.add_urls(["https://ex.com/orig"], note="original", writer="first-writer")
    ll.add_urls(["https://ex.com/orig?utm_source=reconfirm"], writer="dupe-writer")
    verdict = ll.check_url("https://ex.com/orig")
    assert verdict["first_entry"]["writer"] == "first-writer"
    assert verdict["first_entry"]["note"] == "original"
    third = ll.add_urls(["https://ex.com/orig?utm_campaign=third"], writer="third-writer")
    assert third[0]["duplicate_of"] == "https://ex.com/orig"


def test_check_url_gate_unknown_passes(ledger):
    verdict = ll.check_url("https://ex.com/not-filed-yet")
    assert verdict == {"canonical": "https://ex.com/not-filed-yet",
                       "known": False, "first_entry": None}


def test_scout_reconfirmation_gets_duplicate_of_at_submission(ledger):
    ll.add_urls(["https://github.com/12britz/awesome-free-models"],
                writer="free-resource-scout", note="scout find")
    rows = ll.add_urls(["https://github.com/12britz/awesome-free-models"],
                       writer="free-resource-scout",
                       note="daily scout re-confirmation: alive")
    assert rows[0]["duplicate_of"] == "https://github.com/12britz/awesome-free-models"
    # stamped in the ledger bytes, not just in the returned row
    assert ll.load_ledger()[-1]["duplicate_of"] == "https://github.com/12britz/awesome-free-models"


def test_add_cli_flags_duplicate_at_submission(ledger, monkeypatch, capsys):
    ll.add_urls(["https://ex.com/r"], writer="free-resource-scout")
    monkeypatch.setattr("sys.argv",
                        ["prog", "add", "https://ex.com/r",
                         "--writer", "free-resource-scout",
                         "--note", "daily re-confirmation"])
    assert ll.main() == 0
    assert "DUPLICATE" in capsys.readouterr().out


# -- image-drop register (B2-172, 2026-09-26) -----------------------------------
# The third schema (canonical "image-drop:<name>", canonical_sha256 = FILE bytes)
# moved to its own register; these pins hold the split and the re-hash verifier.

def test_load_image_drops_missing_file_is_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(ll, "IMAGE_DROPS", tmp_path / "absent.jsonl")
    assert ll.load_image_drops() == []


def test_load_image_drops_refuses_schemaless_row(tmp_path, monkeypatch):
    reg = tmp_path / "IMAGE_DROPS.jsonl"
    reg.write_text(json.dumps({"canonical": "image-drop:x.png", "url": "x.png"}) + "\n",
                   encoding="utf-8")
    monkeypatch.setattr(ll, "IMAGE_DROPS", reg)
    with pytest.raises(ValueError):
        ll.load_image_drops()  # schema-less row cannot cohabit silently


def test_verify_image_drops_ok_and_mismatch(tmp_path, monkeypatch):
    import hashlib
    payload = b"png-bytes-here"
    f = tmp_path / "plate.png"
    f.write_bytes(payload)
    sha = hashlib.sha256(payload).hexdigest().upper()
    reg = tmp_path / "IMAGE_DROPS.jsonl"
    row = {"canonical": "image-drop:plate.png", "url": str(f),
           "canonical_sha256": sha, "schema": "image-drop.v1",
           "origin": {"file": "watch/inbox/LINKS.jsonl", "line": 256}}
    reg.write_text(json.dumps(row) + "\n", encoding="utf-8")
    monkeypatch.setattr(ll, "IMAGE_DROPS", reg)
    monkeypatch.setattr(ll, "ROOT", tmp_path)  # url resolved against ROOT
    verdict = ll.verify_image_drops()
    assert verdict["ok"] is True and verdict["rows"][0]["status"] == "OK"
    # tamper: one flipped byte must fail the verifier, never pass silently
    f.write_bytes(payload + b"x")
    verdict = ll.verify_image_drops()
    assert verdict["ok"] is False and verdict["rows"][0]["status"] == "MISMATCH"


def test_verify_image_drops_missing_file_named(tmp_path, monkeypatch):
    reg = tmp_path / "IMAGE_DROPS.jsonl"
    row = {"canonical": "image-drop:gone.png", "url": "no/such/gone.png",
           "canonical_sha256": "0" * 64, "schema": "image-drop.v1",
           "origin": {"file": "watch/inbox/LINKS.jsonl", "line": 256}}
    reg.write_text(json.dumps(row) + "\n", encoding="utf-8")
    monkeypatch.setattr(ll, "IMAGE_DROPS", reg)
    monkeypatch.setattr(ll, "ROOT", tmp_path)
    verdict = ll.verify_image_drops()
    assert verdict["ok"] is False and verdict["rows"][0]["status"] == "MISSING"
