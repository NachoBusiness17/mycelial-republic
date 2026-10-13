"""4chan-the-game — Primer face on room.jsonl. Engine owns posts."""
from __future__ import annotations

import json
from pathlib import Path

from mag.chan import catalog, check_steer, is_play_post, paint_tool, post, seed_keep, slugify, thread, trip_id


def _room(tmp_path: Path) -> Path:
    p = tmp_path / "room.jsonl"
    p.write_text("", encoding="utf-8")
    return p


def test_hides_grok_telemetry(tmp_path: Path):
    p = _room(tmp_path)
    rows = [
        {"ts": "1", "seat": "grok", "event": "post_tool_use", "thread": "keep", "text": "grep"},
        {"ts": "2", "seat": "grok", "event": "user_prompt_submit", "text": "hello"},
        {"ts": "3", "seat": "primer", "event": "thread_open", "thread": "keep", "text": ">be the Primer"},
        {"ts": "4", "seat": "cadence", "event": "beat_start", "thread": "night-shift", "text": "ns-1"},
        {"ts": "5", "seat": "anon", "event": "reply", "thread": "keep", "text": ">be me"},
    ]
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    assert is_play_post(rows[0]) is False
    assert is_play_post(rows[1]) is False
    t = thread("keep", path=p)
    texts = [x["text"] for x in t["posts"]]
    assert ">be the Primer" in texts
    assert ">be me" in texts
    assert "grep" not in texts


def test_primer_catalog_hides_mill(tmp_path: Path):
    p = _room(tmp_path)
    rows = [
        {"ts": "1", "seat": "primer", "event": "thread_open", "thread": "keep", "text": "hello keep"},
        {"ts": "2", "seat": "cadence", "event": "result", "thread": "night-shift", "text": "ns mill dump"},
        {"ts": "3", "seat": "deepseek", "event": "chan_post", "thread": "physics", "text": "turtles"},
    ]
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    rows.append({"ts": "4", "seat": "zcode", "event": "thread_open", "thread": "tangents", "text": "mill OP"})
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    face = catalog(path=p)
    slugs = {t["slug"] for t in face["threads"]}
    assert "keep" in slugs
    assert "physics" in slugs
    assert "night-shift" not in slugs
    assert "tangents" not in slugs
    mill = catalog(path=p, all_threads=True)
    mill_slugs = {t["slug"] for t in mill["threads"]}
    assert "night-shift" in mill_slugs


def test_post_and_sage_bump(tmp_path: Path):
    p = _room(tmp_path)
    seed_keep(p)
    a = post("keep", ">be me\n>post", path=p)
    assert a["ok"] and a["seat"] == "anon"
    b = post("keep", "sage this", sage=True, path=p)
    assert b["ok"] and b.get("sage") is True
    t = thread("keep", path=p)
    assert t["count"] >= 3
    assert t["posts"][-1]["event"] == "sage"
    cat = catalog(path=p)
    keep = next(x for x in cat["threads"] if x["slug"] == "keep")
    # sage does not bump — last bump is the non-sage reply
    assert keep["bumped"] == a["ts"]


def test_slug_and_trip():
    assert slugify("Hello Keep!!") == "hello-keep"
    assert slugify("") == "thread"
    assert len(trip_id("anon", "keep")) == 8
    assert trip_id("anon", "keep") == trip_id("anon", "keep")
    assert trip_id("anon", "keep") != trip_id("deepseek", "keep")


def test_paint_tool_is_greentext():
    t = paint_tool("grep", "pattern: wake")
    assert t.startswith(">tool grep")
    assert "pattern: wake" in t
    assert "{" not in t


def test_tool_event_is_play(tmp_path: Path):
    p = _room(tmp_path)
    rec = {
        "ts": "1",
        "seat": "claw",
        "event": "tool",
        "thread": "keep",
        "text": paint_tool("read_file", "chan.html"),
    }
    p.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    assert is_play_post(rec) is True
    texts = [x["text"] for x in thread("keep", path=p)["posts"]]
    assert any(">tool read_file" in x for x in texts)


def test_seed_keep_once(tmp_path: Path):
    p = _room(tmp_path)
    assert seed_keep(p) is True
    assert seed_keep(p) is False
    t = thread("keep", path=p)
    assert t["count"] == 1
    assert t["posts"][0]["seat"] == "primer"


# ---------------------------------------------------------------------------
# check_steer — the board's own STEER channel consumer (tools/steer_read).
# The seed row landed in watch/inbox/STEER.md (mate "all", via hand-edit) is
# copied verbatim into tmp channels; the live channel is never touched.
# ---------------------------------------------------------------------------

SEED_ROW = (
    '{"id": "st_20260930_seed_1", "mate": "all", '
    '"steer": "keep rolling 24 wide; proven seats only; dogfood gps", '
    '"ts": "2026-09-30T00:00:00Z", "via": "hand-edit"}'
)


def _steer_channel(tmp_path: Path, *rows: str) -> Path:
    p = tmp_path / "STEER.md"
    p.write_text("# header comment row (file contract)\n" + "\n".join(rows) + "\n",
                 encoding="utf-8")
    return p


def test_check_steer_returns_seed_row_when_target_matches(tmp_path: Path):
    p = _steer_channel(tmp_path, SEED_ROW)
    out = check_steer("chan", path=p)
    assert out["ok"] is True
    # mate "all" applies to any target; the seed row is a hand-edit ORDER
    assert out["operative"]["id"] == "st_20260930_seed_1"
    assert out["card"].startswith(">steer from the operator (hand-edit):")
    assert "24 wide" in out["card"]  # greentext card carries the operator word verbatim


def test_check_steer_scoped_row_matches_its_target_only(tmp_path: Path):
    p = _steer_channel(
        tmp_path,
        '{"id":"f1","mate":"w9","steer":"other lane","ts":"2026-09-30T18:00:00Z","via":"hand-edit"}',
        '{"id":"f2","mate":"chan","steer":"paint slower","ts":"2026-09-30T10:00:00Z","via":"hermes-dm"}',
    )
    hit = check_steer("chan", path=p)
    assert hit["ok"] is True and hit["operative"]["id"] == "f2"
    miss = check_steer("w3", path=p)  # neither row applies to w3
    assert miss["ok"] is True and miss["card"] == "" and miss["operative"] is None


def test_check_steer_empty_when_proposals_only(tmp_path: Path):
    p = _steer_channel(
        tmp_path,
        '{"id":"p1","mate":"chan","steer":"seat guess","ts":"2026-09-30T11:00:00Z","via":"seat-guess"}',
        '{"id":"p2","mate":"all","steer":"no provenance","ts":"2026-09-30T12:00:00Z"}',
    )
    out = check_steer("chan", path=p)
    # proposals are asks, not orders: nothing is prepended, the board paints as usual
    assert out["ok"] is True
    assert out["card"] == "" and out["steer"] == "" and out["operative"] is None


def test_check_steer_latest_proposal_suppresses_older_order(tmp_path: Path):
    p = _steer_channel(
        tmp_path,
        '{"id":"o1","mate":"chan","steer":"older order","ts":"2026-09-30T10:00:00Z","via":"phone-relay"}',
        '{"id":"p1","mate":"chan","steer":"newer ask","ts":"2026-09-30T15:00:00Z","via":"seat-guess"}',
    )
    out = check_steer("chan", path=p)
    assert out["ok"] is True and out["card"] == ""  # latest wins, even when it is a proposal


def test_check_steer_missing_channel_is_dark_not_silent(tmp_path: Path):
    out = check_steer("chan", path=tmp_path / "nope.md")
    assert out["ok"] is False and out["card"] == "" and out["operative"] is None
