"""venue_mine tests -- routing, dedupe, and the venue-relative window.

No network here: the miner's fetchers are injected. The laws pinned:
  - every lexicon family carries an estate_binding (a hit with no consumer is
    curiosity, not signal);
  - anti-terms veto a row outright (keyword mining without negatives is a
    noise pump);
  - one URL matched by three families is ONE row with three reasons;
  - the recency window is venue-relative, because venue clocks lag the local
    one (2026-10-24: HN's newest "backpressure" story was 2026-08-26).
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import tools.venue_mine as vm

LEX = Path(__file__).resolve().parents[1] / "configs" / "signal_lexicon.json"


def test_lexicon_every_family_routes():
    lex = vm.load_lexicon(LEX)
    ids = [f["id"] for f in lex["families"]]
    assert len(ids) == len(set(ids))
    for fam in lex["families"]:
        assert fam["estate_binding"].strip()
        assert fam["triggers"] and fam["law"]


def test_anti_terms_veto_matches():
    fam = {"triggers": ["rate limiting"], "anti": ["rate my"]}
    assert vm.match_terms("Rate limiting in Postgres", fam) == ["rate limiting"]
    assert vm.match_terms("Rate my startup landing page", fam) == []


def test_build_queries_respects_per_family_and_filter():
    lex = vm.load_lexicon(LEX)
    qs = vm.build_queries(lex, per_family=2)
    assert len(qs) == 2 * len(lex["families"])
    only = vm.build_queries(lex, per_family=1, families={"falsifier"})
    assert only == [("falsifier", "falsifiable")]


def test_one_url_matched_by_two_families_is_one_row(monkeypatch):
    now = datetime.now(timezone.utc)
    story = {"venue": "hn", "url": "https://ex/1",
             "title": "Falsifiable design with backpressure and kill condition",
             "author": "a", "points": 40, "comments": 3,
             "published": now.isoformat()}
    monkeypatch.setattr(vm, "mine_hn", lambda q, days, per_query=30: [dict(story)])
    monkeypatch.setattr(vm, "VENUE_RATE_S", {"hn": 0, "lobsters": 0, "reddit": 0, "arxiv": 0})
    lex = vm.load_lexicon(LEX)
    rows, errors, windows = vm.mine(lex, {"hn"}, days=30, per_family=1,
                                    families={"falsifier", "backpressure"},
                                    reddit_subs=[])
    assert len(rows) == 1, rows
    assert set(rows[0]["families"]) == {"falsifier", "backpressure"}
    assert rows[0]["score"] > 0.2
    assert errors == [] and windows["hn"]["kept"] == 1


def test_venue_relative_window_drops_old_items(monkeypatch):
    now = datetime.now(timezone.utc)
    fresh = {"venue": "hn", "url": "https://ex/fresh", "title": "falsifiable claim",
             "points": 1, "published": now.isoformat()}
    ancient = {"venue": "hn", "url": "https://ex/old", "title": "falsifiable claim",
               "points": 1, "published": (now - timedelta(days=400)).isoformat()}
    monkeypatch.setattr(vm, "mine_hn", lambda q, days, per_query=30: [dict(fresh), dict(ancient)])
    monkeypatch.setattr(vm, "VENUE_RATE_S", {"hn": 0, "lobsters": 0, "reddit": 0, "arxiv": 0})
    lex = vm.load_lexicon(LEX)
    rows, _, windows = vm.mine(lex, {"hn"}, days=7, per_family=1,
                               families={"falsifier"}, reddit_subs=[])
    assert [r["url"] for r in rows] == ["https://ex/fresh"]
    assert windows["hn"]["kept"] == 1


def test_digest_names_the_binding():
    lex = vm.load_lexicon(LEX)
    md = vm.digest([{"venue": "hn", "url": "u", "title": "t", "points": 5,
                     "families": ["falsifier"], "matched": {"falsifier": ["falsifiable"]},
                     "score": 1.0, "estate_binding": "x", "law": "y", "action": ""}],
                   [], lex)
    assert "falsifier" in md and "binds to" in md
