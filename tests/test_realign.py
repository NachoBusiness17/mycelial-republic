"""Tests for mag.realign: the operator realignment surface (Mickey17 W3, 2026-09-29)."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from mag import realign


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_fixture(root: Path, *, old_event: bool = True) -> None:
    """A small estate: one alert, one needs-operator queue row, one fresh receipt, one old receipt."""
    now = datetime(2026, 9, 29, 12, 0, 0, tzinfo=timezone.utc)
    fresh = (now - timedelta(hours=2)).isoformat()
    old = (now - timedelta(days=10)).isoformat()

    _write(
        root / "state" / "CURRENT.md",
        "# CURRENT\n\n"
        "- **status:** escalated_grok_ran\n"
        f"- **updated:** {fresh}\n\n"
        "## Goal\n\nold-files probe\n",
    )
    _write(
        root / "memory" / "attention.md",
        "---\n\n### Session record ready (first)\n\n"
        f"- ts: {fresh}\n- session: noise\n\n---\n\n"
        "### Census collect patrol fired (2026-09-29 08:30:02)\n\n"
        "- verdict: CENSUS-PATROL: COLLECT-DRIFT - collected drift: pytest holds 2478 vs carrier claim 2436 (exit 1)\n"
        f"- [priority][probe-alarm] provider_probe DOWN mistral -> {old}\n"
        f"- [priority][probe-alarm] provider_probe DOWN mistral -> {fresh}other\n\n",
    )
    events = [
        {"ts": fresh, "op": "register", "file": "W3_REALIGN_20260929.md", "purpose": "realign receipt", "writer": "t"},
        {"ts": old, "op": "register", "file": "ANCIENT_20260901.md", "purpose": "old receipt", "writer": "t"},
        {"ts": fresh, "op": "consume", "file": "ignored-op.md", "purpose": "not a registration", "writer": "t"},
    ]
    if not old_event:
        events = events[:1] + events[2:]
    _write(
        root / "watch" / "inbox" / "index_events.jsonl",
        "".join(json.dumps(e) + "\n" for e in events),
    )
    _write(
        root / "queue" / "queue_index.jsonl",
        json.dumps(
            {
                "id": "Q-001",
                "ts": "2026-09-25T19:15:38+00:00",
                "title": "Verkle noise compaction",
                "status": "open",
                "roam_verdict": "needs-operator: task rewrites the chain; operator must gate.",
            }
        )
        + "\n"
        + json.dumps({"id": "Q-009", "ts": fresh, "title": "closed thing", "status": "closed"})
        + "\n"
        + json.dumps({"id": "Q-010", "ts": fresh, "title": "plain open thing", "status": "open"})
        + "\n",
    )


def test_three_sections_render(tmp_path: Path) -> None:
    build_fixture(tmp_path)
    state = realign.collect(root=tmp_path, now=datetime(2026, 9, 29, 12, 0, 0, tzinfo=timezone.utc))
    text = realign.render(state)

    assert "NEEDS YOU" in text
    assert "MOVED" in text
    assert "IGNORED" in text
    # alert text surfaced plain, flood copies deduped to one line with a count
    assert "provider_probe DOWN mistral" in text
    assert "(seen 2 times)" in text
    # patrol verdict is an alert too
    assert "COLLECT-DRIFT" in text
    # needs-operator queue row, not the closed or plain-open rows
    assert "Q-001" in text
    assert "task rewrites the chain" in text
    assert "Q-009" not in text
    assert "Q-010" not in text
    # receipt linked by filename, non-register ops excluded
    assert "watch/inbox/W3_REALIGN_20260929.md" in text
    assert "realign receipt" in text
    assert "ignored-op.md" not in text
    # old registration counted, not listed
    assert "ANCIENT_20260901.md" not in text
    assert "counted but not shown" in text
    # CURRENT.md moved line
    assert "state/CURRENT.md" in text
    assert "escalated_grok_ran" in text


def test_stamp_updates_and_filters_next_run(tmp_path: Path) -> None:
    build_fixture(tmp_path)
    now = datetime(2026, 9, 29, 12, 0, 0, tzinfo=timezone.utc)

    first = realign.collect(root=tmp_path, now=now)
    record = realign.mark_visited(root=tmp_path, now=now, counts={"needs": 2, "moved": 1})
    stamp = json.loads((tmp_path / "state" / "last_operator_visit.json").read_text(encoding="utf-8"))
    assert stamp["schema"] == realign.SCHEMA
    assert stamp["previous_visit"] is None
    assert record["last_visit"] == stamp["last_visit"]

    # a new receipt lands after the visit
    new_ts = (now + timedelta(hours=1)).isoformat()
    with (tmp_path / "watch" / "inbox" / "index_events.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ts": new_ts, "op": "register", "file": "NEW_20260930.md", "purpose": "landed after visit"}) + "\n")

    second = realign.collect(root=tmp_path, now=now + timedelta(hours=2))
    text = realign.render(second)
    assert "NEW_20260930.md" in text
    assert "W3_REALIGN_20260929.md" not in text
    assert "Q-001" in text  # still waiting on the operator
    assert second["cold_start"] is False


def test_empty_delta_renders_nothing_moved(tmp_path: Path) -> None:
    build_fixture(tmp_path)
    now = datetime(2026, 9, 29, 12, 0, 0, tzinfo=timezone.utc)
    # everything already seen, no queue rows waiting, switch running
    realign.mark_visited(root=tmp_path, now=now + timedelta(hours=3))
    (tmp_path / "queue" / "queue_index.jsonl").write_text("", encoding="utf-8")

    state = realign.collect(root=tmp_path, now=now + timedelta(hours=4))
    text = realign.render(state)
    assert "nothing moved" in text
    assert "- (nothing needs you right now)" in text
