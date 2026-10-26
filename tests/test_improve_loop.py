"""Improve loop — cloud handoff + cycle wiring.

B2-402 (2026-09-26): the tests run isolated. Before the autouse fixture below
every run dropped a real cloud-*.json into queue/handoff/ (55 -> 56 in the
B2-359 probe window; 43 pytest-source files on bytes) and appended real
source=pytest rows to logs/behavioral_events.jsonl (53) and
memory/runs/improve_loop_trail.jsonl (72). The handoff dir, the trail and the
behavioral events sink are module constants, so the fixture redirects them to
tmp_path (the test_shared_surface_events surface-fixture shape). The
pytest-source residue that pre-dates the fixture was counted and removed
(file-shaped debt); the append-only trail/event/registry rows are registered
in watch/inbox/burn_wave_20260926/B2_402_test_isolation_20260926.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def _isolated_write_roots(tmp_path, monkeypatch):
    import mag.improve_loop as il

    handoff = tmp_path / "handoff"
    handoff.mkdir()
    monkeypatch.setattr(il, "HANDOFF_DIR", handoff)
    if hasattr(il, "TRAIL"):
        monkeypatch.setattr(il, "TRAIL", tmp_path / "improve_loop_trail.jsonl")
    try:
        import mag.operator_inbox as oi

        monkeypatch.setattr(oi, "EVENTS_PATH", tmp_path / "behavioral_events.jsonl")
    except Exception:
        pass
    yield


def test_cloud_handoff_write():
    from mag.improve_loop import ingest_cloud_handoffs, write_cloud_handoff

    res = write_cloud_handoff(claim="smoke test claim", source="pytest")
    assert res.get("ok") is True
    assert res.get("path")
    rows = ingest_cloud_handoffs()
    assert any(r.get("run_id") == res.get("run_id") for r in rows)


# slow: hangs past 120 s on full-tree gap_analysis / live Ollama (APPLY_ORDER.md triage 2026-10-04)
@pytest.mark.slow
def test_improve_cycle_schema():
    from mag.improve_loop import run_improve_cycle

    res = run_improve_cycle(source="pytest", max_improve=0, drain_one=False)
    assert res.get("schema") == "improve_loop.v1"
    assert "nervous" in res or "nervous_error" in res
