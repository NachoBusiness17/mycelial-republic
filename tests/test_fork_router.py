from __future__ import annotations

from pathlib import Path


def test_detect_fork_future_tangent_suggests_fork():
    from mag.fork_router import detect_fork

    res = detect_fork(
        "Wouldn't it be nice if we added a future feature set for later and did a gap analysis?",
        current_goal="Ship tests for router endpoint",
    )
    assert res["ok"] is True
    assert res["needs_fork"] is True
    assert res["action"] in {"suggest_fork", "auto_fork"}
    assert res["target"] in {"contract", "task"}


def test_detect_fork_direct_edit_stays_inline():
    from mag.fork_router import detect_fork

    res = detect_fork(
        "Implement fix in mag/router.py and add pytest for route.v2",
        current_goal="Implement fix in mag/router.py",
    )
    assert res["ok"] is True
    assert res["needs_fork"] is False
    assert res["action"] == "stay"


def test_confirm_fork_writes_artifacts(tmp_path, monkeypatch):
    import mag.fork_router as fr

    monkeypatch.setattr(fr, "ROOT", Path(tmp_path))
    out = fr.confirm_fork(
        "Explore a future feature set and draft a branch plan",
        current_goal="Fix dashboard lint",
        strategy="contract",
        spawn=False,
    )
    assert out["ok"] is True
    assert out["schema"] == "fork_confirm.v1"
    paths = out["paths"]
    assert Path(paths["json"]).is_file()
    assert Path(paths["markdown"]).is_file()


def test_rest_fork_detect_and_route_envelope_include_fork():
    from dashboard.rest import h_fork_detect, h_route

    code, body = h_fork_detect({}, {"goal": "it might be neat to plan a future branch"})
    assert code == 200
    assert body.get("schema") == "fork_decision.v1"

    code2, route_body = h_route({}, {"goal": "fix typo in README", "include_fork": True})
    assert code2 == 200
    assert route_body.get("schema") == "mag_intent.v1"
    fork = route_body.get("fork_decision") or {}
    assert fork.get("schema") == "fork_decision.v1"
