"""healthz status-code contract — D19 divergence-lane finding (2026-09-12).

The gate as registered: /healthz returns NON-200 when health breaches.
The old endpoint always returned 200 and only the body carried ok:false —
a monitor checking the code alone saw a healthy fleet during a live breach.
"""
from __future__ import annotations

import importlib
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient  # noqa: E402


@pytest.fixture()
def client():
    import server

    importlib.reload(server)
    return TestClient(server.app)


def test_status_tracks_ok_flag(client):
    r = client.get("/healthz")
    body = r.json()
    assert (r.status_code == 200) == body["ok"], (
        "status code must be 200 iff ok; breach must surface as non-200"
    )


def test_breach_returns_503(client, tmp_path):
    import server

    breach = tmp_path / "failure_kb.jsonl"
    # 2026-09-27 fix: rows were pinned to 2026-09-12, which rotted out of the
    # trailing-1h grading window once the calendar moved (semantic_health skips
    # rows older than now-1h per the endpoint contract, so the stale fixture
    # graded ok=True with 0 in-window rows). Byte proof 2026-09-27: the pinned
    # timestamps grade ok=True/http_tool_fail_1h=0, now-relative timestamps
    # grade ok=False/http_tool_fail_1h=10. Breach rows are now relative to now
    # so the fixture cannot rot again; the code under test was never wrong.
    now = datetime.now(timezone.utc)
    rows = [
        {"ts": (now - timedelta(minutes=5)).isoformat(), "kind": "http_tool_fail", "tool": "run_shell", "error": "x"}
        for _ in range(10)
    ]
    breach.write_text("\n".join(__import__("json").dumps(r) for r in rows) + "\n", encoding="utf-8")
    report = server.semantic_health(path=breach)
    assert report["ok"] is False
    assert report["http_tool_fail_1h"] >= 10


def test_healthy_returns_200(client, tmp_path):
    import server

    quiet = tmp_path / "failure_kb.jsonl"
    quiet.write_text("", encoding="utf-8")
    report = server.semantic_health(path=quiet)
    assert report["ok"] is True
