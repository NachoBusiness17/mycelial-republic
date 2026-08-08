"""Steer bridge — memories → operator_inbox steering channel."""
from __future__ import annotations

from pathlib import Path

import pytest

import mag.operator_inbox as oi
import mag.steer_bridge as sb


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    """Point the bridge + inbox at tmp so tests never touch the real queue."""
    inbox = tmp_path / "operator_inbox.json"
    seen = tmp_path / "steer_bridge_seen.json"
    drop = tmp_path / "steer_agent.md"
    monkeypatch.setattr(oi, "INBOX_PATH", inbox)
    monkeypatch.setattr(sb, "DEFAULT_DROP", drop)
    monkeypatch.setattr(sb, "SEEN_STATE", seen)
    return {"inbox": inbox, "seen": seen, "drop": drop}


def test_drop_lines_skips_comments_and_headers(isolated):
    (isolated["drop"]).write_text(
        "# Steer agent\n"
        "> blockquote comment — must be skipped\n"
        "---\n"
        "\n"
        "- Real note one\n"
        "* Real note two\n"
        "1. Numbered note three\n",
        encoding="utf-8",
    )
    lines = sb._drop_lines(isolated["drop"])
    assert lines == ["Real note one", "Real note two", "Numbered note three"]


def test_sync_is_idempotent(isolated):
    (isolated["drop"]).write_text("- Guidance alpha\n- Guidance beta\n", encoding="utf-8")
    r1 = sb.sync_guidance_file()
    assert r1["committed_n"] == 2
    assert r1["skipped_n"] == 0
    r2 = sb.sync_guidance_file()
    assert r2["committed_n"] == 0
    assert r2["skipped_n"] == 2  # already seen — no duplicates
    # both notes are in the pending inbox exactly once
    st = oi.status()
    texts = [p["text"] for p in st["pending"]]
    assert texts.count("Guidance alpha") == 1
    assert texts.count("Guidance beta") == 1


def test_one_shot_steer_commits_pending(isolated):
    r = sb.steer("STEER: verify with git diff, do not re-implement", source="copilot-assistant")
    assert r["ok"] is True
    st = oi.status()
    assert st["pending_n"] == 1
    assert st["pending"][0]["source"] == "copilot-assistant"
    assert st["pending"][0]["text"].startswith("STEER:")
