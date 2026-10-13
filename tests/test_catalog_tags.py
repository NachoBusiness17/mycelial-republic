"""Tag-pass rule pins (B2-104, 2026-09-26): mag/catalog_tags.py.

The salon Appendix B transcription, pinned rule-by-rule: first-match
ordering (including the card-before-receipt trap), the LSA-prefix-stripping
so prefixed map paths classify like repo-relative ones, and the age-class
boundaries computed at run time. Tags v2 (Q-031, 2026-09-28): the owner
column pins.
"""
from __future__ import annotations

import datetime
import json

import mag.catalog_tags as ct


NOW = datetime.datetime(2026, 9, 26, 12, 0, 0, tzinfo=datetime.timezone.utc)


def _mt(days_ago, hour=12):
    mt = NOW - datetime.timedelta(days=days_ago)
    return mt.strftime("%Y-%m-%dT%H:%M:%SZ")


def test_kind_card_beats_prose_and_receipt():
    assert ct.classify_kind("watch/inbox/NOTE_20260918.md", ".md") == "card"


def test_kind_first_match_order_card_before_receipt():
    # Appendix B order: card = watch/*_YYYYMMDD.md is FIRST match, so a
    # dated watch note named "receipt" still tags card. Pinned so the
    # transcription cannot silently reorder the rules.
    assert ct.classify_kind(
        "local_sovereign_agent/watch/inbox/X_receipt_20260926.md",
        ".md") == "card"


def test_kind_prefixed_and_bare_paths_agree():
    # The map walks the projects parent, so repo files carry the
    # local_sovereign_agent/ prefix; the salon rules are repo-relative.
    for rel in ("watch/inbox/NOTE_20260918.md", "memory/briefs/latest.md",
                "memory/burns/LEDGER.jsonl", "mag/catalog_rescan.py"):
        ext = "." + rel.rsplit(".", 1)[-1]
        bare = ct.classify_kind(rel, ext)
        pre = ct.classify_kind("local_sovereign_agent/" + rel, ext)
        assert bare == pre, rel


def test_kind_receipt_by_name_and_by_parent():
    assert ct.classify_kind("docs/X_receipt_20260926.md", ".md") == "receipt"
    assert ct.classify_kind("memory/runs/receipts/a.txt", ".txt") == "receipt"


def test_kind_ledger_and_state():
    assert ct.classify_kind("memory/burns/LEDGER.jsonl", ".jsonl") == "ledger"
    # state = state/*.json, a real "state" path segment (382-row parity on
    # the Sep-18 base, probe 1); agent_state is a different segment.
    assert ct.classify_kind("state/boot.json", ".json") == "state"
    assert ct.classify_kind("memory/run/state/boot.json", ".json") == "state"
    assert ct.classify_kind("memory/agent_state/boot.json", ".json") == "config"
    assert ct.classify_kind("configs/lanes.json", ".json") == "config"


def test_kind_brief_beats_prose():
    assert ct.classify_kind("memory/briefs/latest.md", ".md") == "brief"


def test_kind_corpus_packs():
    assert ct.classify_kind("memory/corpus/game_design_docs/x.html", ".html") == "corpus"
    assert ct.classify_kind("memory/research_packs/p/pack.md", ".md") == "corpus"
    assert ct.classify_kind("memory/ingest/f.txt", ".txt") == "corpus"
    assert ct.classify_kind("memory/corpus/f.bin", ".bin") == "other"


def test_kind_test_beats_code():
    assert ct.classify_kind("tests/test_catalog_rescan.py", ".py") == "test"
    assert ct.classify_kind("mag/catalog_rescan.py", ".py") == "code"


def test_kind_image_config_prose_other():
    assert ct.classify_kind("a/b/screen.png", ".png") == "image"
    assert ct.classify_kind("configs/lanes.yaml", ".yaml") == "config"
    assert ct.classify_kind("docs/x.md", ".md") == "prose"
    assert ct.classify_kind("data/blob.dat", ".dat") == "other"


def test_age_class_boundaries():
    assert ct.age_class_of(_mt(0), NOW) == "fresh"
    assert ct.age_class_of(_mt(6), NOW) == "fresh"
    assert ct.age_class_of(_mt(7), NOW) == "aging"
    assert ct.age_class_of(_mt(29), NOW) == "aging"
    assert ct.age_class_of(_mt(30), NOW) == "stale"
    assert ct.age_class_of(_mt(63), NOW) == "stale"
    assert ct.age_class_of(_mt(64), NOW) == "fossil"


def test_owner_of_pins():
    # Repo files: owning directory after the map's projects-parent prefix.
    assert ct.owner_of("local_sovereign_agent/mag/catalog_tags.py") == "mag"
    # Bare repo-relative paths own the same as prefixed ones.
    assert ct.owner_of("mag/catalog_tags.py") == "mag"
    assert ct.owner_of("local_sovereign_agent/watch/inbox/x.md") == "watch"
    # Estate files outside the repo: the sibling project name.
    assert ct.owner_of("hermes-agent/venv/pyvenv.cfg") == "hermes-agent"
    # Top-level file with no owning directory.
    assert ct.owner_of("AGENTS.md") == "root"
    # Prefix strip is case-insensitive; the owner keeps stored case.
    assert ct.owner_of("Local_Sovereign_Agent/docs/x.md") == "docs"
    # Backslash paths (as some walkers emit) classify the same.
    assert ct.owner_of("local_sovereign_agent\\tools\\corpus.py") == "tools"


def test_run_tags_writes_owner_column(tmp_path):
    cat = tmp_path / "catalog.jsonl"
    rows = [
        {"id": "a1", "path": "local_sovereign_agent/mag/x.py", "ext": ".py",
         "bytes": 3, "mtime": _mt(1), "zone": "code", "title": "x"},
        {"id": "b2", "path": "hermes-agent/notes.md", "ext": ".md",
         "bytes": 4, "mtime": _mt(40), "zone": "ext:hermes-agent",
         "title": "notes.md"},
    ]
    cat.write_text(
        "".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    tags = tmp_path / "tags.jsonl"
    res = ct.run_tags(str(cat), str(tags))
    out = [json.loads(line) for line in
           tags.read_text(encoding="utf-8").splitlines()]
    assert [r["owner"] for r in out] == ["mag", "hermes-agent"]
    assert res["owners"] == {"mag": 1, "hermes-agent": 1}
    # v1 fields unchanged on the same rows.
    assert out[0]["kind"] == "code" and out[0]["age_class"] == "fresh"
    assert out[1]["kind"] == "prose" and out[1]["age_class"] == "stale"
