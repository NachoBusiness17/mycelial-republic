from __future__ import annotations


def test_recently_terminal_goal_blocks_successful_requeue(monkeypatch):
    from mag import governor_autorun as governor

    rows = [{
        "queue_id": "q-done",
        "goal": "run republic_os round to reinforce/prune graph",
        "status": "done",
        "created_at": "2026-08-31T03:50:00+00:00",
    }]
    monkeypatch.setattr("mag.orchestrator.list_queue", lambda limit=300: rows)
    hit = governor.recently_terminal_goal(rows[0]["goal"], cooldown_s=1)
    assert hit is not None
    assert hit["status"] == "done"
