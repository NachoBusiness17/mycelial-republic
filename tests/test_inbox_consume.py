"""Tests for tools/inbox_consume.py + tools/orphan_census.py (Mickey17 wave 3).

Pins the two behaviors the return-5 improvement stands on:
- the census classifies every content file into exactly one of
  never_registered / registered_missing / registered_never_consumed
  (+ consumed), joining disk against a fixture event log that carries the
  REAL log's path spellings: /board/inbox/ aliases, the B2-02 watch/inbox/
  prefix the fold drops, drive-letter absolutes, bare board/ paths and
  repo-file registrations;
- the consume op appends one valid event line for an existing inbox file,
  refuses ghosts and outside-surface paths, and flips the census.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import tools.orphan_census as oc
from tools.inbox_consume import consume, resolve_target
from tools.orphan_census import classify

CONSUMER = "wave3-test"


def _build_repo(tmp_path: Path) -> tuple[Path, Path, Path]:
    """Fixture repo mirroring the production shapes.

    ALPHA.md registered directly + on disk (never consumed)
    BETA.md  registered, file gone (dangling)
    GAMMA.md on disk, registered ONLY via the watch/inbox/ spelling the fold
             drops (B2-02): the census must join it, not orphan it
    DELTA.md autoseal-registered + consumed (the read op firing)
    EPS.md   on disk, never registered (the true orphan)
    outside: c:/ absolute, bare board/, and tools/probe.py at repo root
    """
    root = tmp_path / "repo"
    inbox = root / "watch" / "inbox"
    inbox.mkdir(parents=True)
    events = inbox / "index_events.jsonl"
    for name in ("ALPHA.md", "GAMMA.md", "DELTA.md", "EPS.md"):
        (inbox / name).write_text(f"content of {name}\n", encoding="utf-8")
    # fold control files: present on disk, skipped by the content census
    (inbox / "INDEX.json").write_text("{}", encoding="utf-8")
    # a registration of a repo file outside the inbox surface
    probe = root / "tools" / "probe.py"
    probe.parent.mkdir()
    probe.write_text("x = 1\n", encoding="utf-8")
    rows = [
        {"seq": 1, "ts": "2026-09-01T00:00:00Z", "op": "register",
         "file": "/board/inbox/ALPHA.md", "sha256": "a" * 64},
        {"seq": 2, "ts": "2026-09-01T00:01:00Z", "op": "register",
         "file": "BETA.md", "sha256": "b" * 64},
        {"seq": 3, "ts": "2026-09-01T00:02:00Z", "op": "register",
         "file": "watch/inbox/GAMMA.md", "sha256": "c" * 64},
        {"seq": 4, "ts": "2026-09-01T00:03:00Z", "op": "autoseal",
         "file": "DELTA.md", "sha256": "d" * 64, "bytes": 18},
        {"seq": 5, "ts": "2026-09-02T00:00:00Z", "op": "consume",
         "file": "DELTA.md", "consumer": "fixture-reader", "note": "read it"},
        {"seq": 6, "ts": "2026-09-01T00:04:00Z", "op": "register",
         "file": "c:/elsewhere/x.md", "sha256": "e" * 64},
        {"seq": 7, "ts": "2026-09-01T00:05:00Z", "op": "register",
         "file": "/board/graph/g.jsonl", "sha256": "f" * 64},
        {"seq": 8, "ts": "2026-09-01T00:06:00Z", "op": "register",
         "file": "tools/probe.py", "sha256": "0" * 64},
        "{'seq':NEXT} malformed grandfathered line, tolerant parse",
    ]
    with events.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row) + "\n")
    return root, inbox, events


@pytest.fixture()
def surface(tmp_path, monkeypatch):
    root, inbox, events = _build_repo(tmp_path)
    monkeypatch.setattr(oc, "ROOT", root)
    return inbox, events


def test_classify_three_classes(surface):
    inbox, events = surface
    c = classify(inbox, events)
    assert c["never_registered"] == ["eps.md"]
    assert c["registered_missing"] == ["beta.md"]
    assert c["registered_never_consumed"] == ["alpha.md", "gamma.md"]
    assert c["consumed"] == ["delta.md"]
    # content walk counts the 4 files, not INDEX.json or the log
    assert c["disk_files"] == 4
    assert c["registered_unique"] == 4
    # join-alias and outside buckets are counted, never silent
    assert c["meta"]["fold_blind_watch_prefix"] == 1
    assert c["meta"]["registered_outside_surface"] == 3
    assert c["meta"]["outside_confirmed_on_repo"] == 1
    assert c["meta"]["malformed_lines"] == 1
    assert c["meta"]["events_parsed"] == 8


def test_watcher_prefix_and_double_slash_join(surface):
    inbox, events = surface
    with events.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"op": "register", "file": "watch/inbox/EPS.md"}) + "\n")
        fh.write(json.dumps({"op": "register", "file": "fullsend_s2//w_1.json"}) + "\n")
    (inbox / "fullsend_s2").mkdir()
    (inbox / "fullsend_s2" / "w_1.json").write_text("{}", encoding="utf-8")
    c = classify(inbox, events)
    assert c["never_registered"] == []          # eps joined via the alias
    assert "fullsend_s2/w_1.json" not in c["registered_missing"]  # // collapsed
    assert c["meta"]["fold_blind_watch_prefix"] == 2


def test_consume_appends_valid_event(surface):
    inbox, events = surface
    before_lines = events.read_text(encoding="utf-8").splitlines()
    alpha_bytes = (inbox / "ALPHA.md").read_bytes()
    event = consume(events, inbox, "/board/inbox/ALPHA.md",
                    CONSUMER, note="reading the receipt")
    assert event is not None
    after_lines = events.read_text(encoding="utf-8").splitlines()
    assert len(after_lines) == len(before_lines) + 1
    appended = json.loads(after_lines[-1])
    assert appended == event
    assert appended["op"] == "consume"
    assert appended["file"] == "ALPHA.md"  # normalized inbox-relative posix
    assert appended["consumer"] == CONSUMER
    assert appended["note"] == "reading the receipt"
    assert "T" in appended["ts"]  # RFC3339-ish, fold ts tie-breaker
    # read op touches nothing but the log
    assert (inbox / "ALPHA.md").read_bytes() == alpha_bytes


def test_consume_flips_the_census(surface):
    inbox, events = surface
    assert "alpha.md" in classify(inbox, events)["registered_never_consumed"]
    assert consume(events, inbox, str(inbox / "ALPHA.md"), CONSUMER) is not None
    c = classify(inbox, events)
    assert "alpha.md" in c["consumed"]
    assert "alpha.md" not in c["registered_never_consumed"]


def test_consume_of_control_file_counts_as_consumed(surface):
    inbox, events = surface
    assert consume(events, inbox, "INDEX.json", CONSUMER) is not None
    c = classify(inbox, events)
    assert "index.json" in c["consumed"]      # read telemetry sees controls
    assert c["disk_files"] == 4               # content classes unchanged
    assert "index.json" not in c["never_registered"]


def test_consume_refuses_ghost_and_outside(surface, capsys):
    inbox, events = surface
    before = events.read_text(encoding="utf-8")
    # registered but missing from disk: a ghost, refusing keeps the join clean
    assert consume(events, inbox, "BETA.md", CONSUMER) is None
    # never-registered orphan: also just a file reference that does not exist
    assert consume(events, inbox, "NOPE.md", CONSUMER) is None
    # outside the inbox surface entirely (a real file, wrong surface)
    outside = inbox.parent.parent / "tools" / "probe.py"
    assert consume(events, inbox, str(outside), CONSUMER) is None
    # empty consumer name refuses even for a real file
    assert consume(events, inbox, "ALPHA.md", "  ") is None
    assert events.read_text(encoding="utf-8") == before  # zero appends
    assert "refused" in capsys.readouterr().err


def test_resolve_target_accepts_writer_spellings(surface):
    inbox, _ = surface
    host_abs = str(inbox / "ALPHA.md").replace("\\", "/")
    for ref in ("ALPHA.md", host_abs, "/board/inbox/ALPHA.md", "inbox/ALPHA.md"):
        assert resolve_target(ref, inbox) == (inbox / "ALPHA.md").resolve(), ref
    assert resolve_target("BETA.md", inbox) is None  # ghost
    assert resolve_target("../escape.md", inbox) is None


def test_consume_dry_run_appends_nothing(surface):
    inbox, events = surface
    before = events.read_text(encoding="utf-8")
    event = consume(events, inbox, "ALPHA.md", CONSUMER, dry_run=True)
    assert event is not None and event["op"] == "consume"
    assert events.read_text(encoding="utf-8") == before


def test_census_skips_its_own_output(surface):
    inbox, events = surface
    (inbox / "ORPHAN_CENSUS.json").write_text("{}", encoding="utf-8")
    c = classify(inbox, events)
    assert c["disk_files"] == 4
    assert "orphan_census.json" not in c["never_registered"]
