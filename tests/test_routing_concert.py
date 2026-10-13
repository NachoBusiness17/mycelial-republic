from __future__ import annotations


def test_run_concert_step_scout_uses_nervous_glance(monkeypatch):
    from mag import routing_concert as rc

    monkeypatch.setattr(
        "mag.nervous_system.build_glance",
        lambda write=False: {"ok": True, "schema": "nervous_system.v1", "write": write},
    )

    plan = {
        "concert_id": "concert-test-1",
        "goal": "build something",
        "steps": [
            {"order": 1, "phase": "scout", "seat": "local", "status": "pending", "goal": "scout"}
        ],
    }

    out = rc.run_concert_step(plan, step_order=1, dry=False)
    assert out.get("ok") is True
    assert (out.get("output") or {}).get("schema") == "nervous_system.v1"
    assert (out.get("output") or {}).get("write") is False
