"""tests for mag/paste_pipeline._canonical_footer (B2-124, 2026-09-26).

The brief: the footer re-implemented the known-canonicals lookup inline
(canonicalize + known_canonicals().get) instead of calling the check_url()
single door (B2-27 gate law). After the refactor the footer must route
every URL through check_url and keep the annotate-never-gate contract
byte-for-byte: any failure degrades to an "(unresolved)" line, never an
exception out of the footer. Ledger-isolated: the real LINKS.jsonl is
never touched (check_url is monkeypatched, or ll.LEDGER points at tmp).
"""
from __future__ import annotations

import json

import pytest

import mag.link_library as ll
from mag.paste_pipeline import _canonical_footer


def test_footer_routes_through_check_url(monkeypatch):
    calls = []

    def fake_check_url(url):
        calls.append(url)
        return {"canonical": "https://x.com/a/status/1", "known": True,
                "first_entry": {"url": "https://x.com/a/status/1?s=20"}}

    monkeypatch.setattr(ll, "check_url", fake_check_url)
    out = _canonical_footer("see https://x.com/a/status/1?s=20 now")
    assert calls == ["https://x.com/a/status/1?s=20"]
    assert out[0] == "## Link canonical check (link_library \u2014 annotate, never gate)"
    assert out[1] == "- https://x.com/a/status/1?s=20"
    assert out[2] == "  links-canonical: https://x.com/a/status/1"
    assert out[3] == "  links-duplicate-of: https://x.com/a/status/1?s=20"
    assert out[4] == ""


def test_footer_unknown_canonical_gets_empty_duplicate_of(monkeypatch):
    monkeypatch.setattr(ll, "check_url", lambda url: {
        "canonical": "https://ex.com/fresh", "known": False, "first_entry": None})
    out = _canonical_footer("https://ex.com/fresh")
    assert out[2] == "  links-canonical: https://ex.com/fresh"
    assert out[3] == "  links-duplicate-of: "


def test_footer_failure_degrades_to_unresolved_never_raises(monkeypatch):
    def boom(url):
        raise ValueError("refusing private host: 127.0.0.1")

    monkeypatch.setattr(ll, "check_url", boom)
    out = _canonical_footer("drop https://127.0.0.1:8080/x here")
    assert out[1] == "- https://127.0.0.1:8080/x"
    assert out[2] == "  links-canonical: (unresolved: ValueError: refusing private host: 127.0.0.1)"
    assert out[3] == "  links-duplicate-of: "


def test_footer_no_urls_returns_empty():
    assert _canonical_footer("no links in this paste") == []


def test_footer_real_door_reports_first_filing(tmp_path, monkeypatch):
    ledger = tmp_path / "LINKS.jsonl"
    ledger.write_text(json.dumps({
        "seq": 1, "ts": "2026-09-16T00:00:00Z", "canonical": "https://ex.com/orig",
        "url": "https://ex.com/orig?utm=1", "canonical_sha256": "x",
        "title": "original", "duplicate_of": "", "writer": "t", "note": ""}) + "\n",
        encoding="utf-8")
    monkeypatch.setattr(ll, "LEDGER", ledger)
    out = _canonical_footer("re-drop https://ex.com/orig?s=20")
    assert out[2] == "  links-canonical: https://ex.com/orig"
    assert out[3] == "  links-duplicate-of: https://ex.com/orig?utm=1"
