"""cry_mine v0 regression: the demand-side frontier mine.

Operator idea (2026-10-05): mine cries for help to anticipate problems
and test them - feature requests, demand-verified. Pinned here: the
deterministic classifier (Annalea's row-0 cry -> quota_wall +
file_egress), ledger dedupe + append-only, the tri-state law (bytes vs
inferred_extra), the report's ranked mirror readout, and the HN sweep's
honest skip (non-distress hits never banked). Network calls mocked.
"""
import importlib
import json
from pathlib import Path

import pytest

import tools.cry_mine as cm


@pytest.fixture()
def ledger(tmp_path, monkeypatch):
    p = tmp_path / "cries.jsonl"
    monkeypatch.setattr(cm, "LEDGER", p)
    return p


ANNALea = ("@poteto poteto poteto poteto @bot @anyone \n\nHalp! \n\n"
           "I cant use my extra usage and I need my bot to give me a file "
           "off its computer!!!! Urgent!")


def test_row0_classifies_quota_wall_and_file_egress():
    assert cm.classify(ANNALea) == ["quota_wall", "file_egress"]


def test_benign_text_classifies_empty():
    assert cm.classify("loving the new agent features, great work team") == []


def test_ingest_dedupes_by_source(ledger):
    r1 = cm.ingest(text=ANNALea, source="x", source_url="https://x.com/a/1")
    assert r1["ok"]
    r2 = cm.ingest(text=ANNALea, source="x", source_url="https://x.com/a/1")
    assert not r2["ok"] and "duplicate" in r2["error"]
    rows = [json.loads(l) for l in ledger.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1


def test_ingest_separates_bytes_from_inference(ledger):
    r = cm.ingest(text="I hit the usage limit", source="x", source_url="u1",
                  note="", inferred_extra="screenshot shows 100% weekly bar")
    row = r["row"]
    assert "screenshot" not in row["text"]  # inference never masquerades as bytes
    assert "screenshot" in row["inferred_extra"]
    assert row["classes"] == ["quota_wall"]


def test_report_ranks_and_names_mirrors(ledger):
    cm.ingest(text=ANNALea, source="x", source_url="u1")
    cm.ingest(text="cursor hit the usage limit again", source="hn", source_url="u2")
    out = cm.report()
    assert "CRY MINE: 2 cries banked" in out
    assert out.index("quota_wall") < out.index("file_egress")  # x2 ranks above x1
    assert "tier ladder" in out  # the mirror is named beside the count


def _fake_urlopen(payload: dict):
    class FakeResp:
        def read(self):
            return json.dumps(payload).encode()

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    return FakeResp()


def test_hn_sweep_skips_non_distress(monkeypatch, ledger):
    payload = {"hits": [
        {"objectID": "1", "author": "a", "comment_text": ANNALea},
        {"objectID": "2", "author": "b", "comment_text": "nice article, thanks for sharing"},
    ]}

    class FakeOpener:
        def open(self, req, timeout=30):
            return _fake_urlopen(payload)

    monkeypatch.setattr(cm, "_OPENER", FakeOpener())
    got = cm.sweep_hn("anything")
    assert len(got) == 2
    banked = skipped = 0
    for c in got:
        if not cm.classify(c["text"]):
            skipped += 1
            continue
        r = cm.ingest(text=c["text"], source="hn", source_url=c["source_url"],
                      author=c.get("author"), note="query='anything'")
        banked += 1 if r.get("ok") else 0
    assert (banked, skipped) == (1, 1)
    rows = [json.loads(l) for l in ledger.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1 and rows[0]["source"] == "hn"


def test_fetch_tweet_parses_and_shapes(monkeypatch):
    payload = {"tweet": {
        "text": "Halp! I hit the usage limit",
        "author": {"screen_name": "someone"},
    }}

    class FakeOpener:
        def open(self, req, timeout=30):
            assert "fxtwitter.com" in req.full_url
            return _fake_urlopen(payload)

    monkeypatch.setattr(cm, "_OPENER", FakeOpener())
    r = cm.fetch_tweet("https://x.com/someone/status/12345")
    assert r["ok"] and r["author"] == "someone"
    assert r["url"].endswith("/status/12345")


# -- the SSRF fence (Mimosa L2 cure) -----------------------------------------


def test_guard_refuses_non_https_and_foreign_hosts():
    with pytest.raises(ValueError, match="https only"):
        cm._guarded_get("http://api.fxtwitter.com/a/status/1")
    with pytest.raises(ValueError, match="not allowlisted"):
        cm._guarded_get("https://evil.example.com/x")
    with pytest.raises(ValueError, match="not allowlisted"):
        cm._guarded_get("https://169.254.169.254/latest/meta-data")  # cloud metadata
    with pytest.raises(ValueError, match="not allowlisted"):
        cm._guarded_get("https://localhost:8080/health")  # loopback


def test_guard_admits_the_two_built_on_hosts(monkeypatch):
    class FakeOpener:
        def open(self, req, timeout=30):
            return _fake_urlopen({"hits": []})

    monkeypatch.setattr(cm, "_OPENER", FakeOpener())
    cm._guarded_get("https://api.fxtwitter.com/a/status/1")
    cm._guarded_get("https://hn.algolia.com/api/v1/search?query=x")
