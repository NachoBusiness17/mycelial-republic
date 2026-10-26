"""mag.ask serves the COMPILED section of SEATS.md, not the first 1200 chars
of the August hand matrix (BURNDOWN_20261004.md section 1), with a
freshness stamp from the section's own source anchor."""
from __future__ import annotations

from datetime import datetime, timezone

import mag.ask as ask

HAND = "# Mag seat matrix (August)\n" + ("L0 worker = gemma4 hand row\n" * 80)
COMPILED = (
    "## COMPILED SEAT REALITY (tools/compile_seats.py; regenerated)\n\n"
    "Source anchor (newest source timestamp): 2026-10-04T12:05:51+00:00. x\n\n"
    "### Seats and lanes as configured\n\n- Lane L0: local via ollama\n\n"
    "### Drift: hand matrix vs live config\n\n- worker drift row\n")
NOW = datetime(2026, 10, 4, 13, 0, tzinfo=timezone.utc)


def test_compiled_section_served_drift_first(tmp_path):
    p = tmp_path / "SEATS.md"
    p.write_text(HAND + "\n" + COMPILED, encoding="utf-8")
    t = ask.seats_text(p, now=NOW)
    assert "COMPILED SEAT REALITY" in t
    assert "gemma4 hand row" not in t
    assert "STALE" not in t
    assert t.index("worker drift row") < t.index("Lane L0")


def test_stale_anchor_is_named(tmp_path):
    p = tmp_path / "SEATS.md"
    p.write_text(HAND + COMPILED, encoding="utf-8")
    t = ask.seats_text(p, now=datetime(2026, 10, 20, tzinfo=timezone.utc))
    assert t.startswith("[STALE: compiled seat section anchored 2026-10-04")
    assert "compile_seats.py --swap" in t


def test_no_compiled_section_falls_back_loudly(tmp_path):
    p = tmp_path / "SEATS.md"
    p.write_text(HAND, encoding="utf-8")
    t = ask.seats_text(p, now=NOW)
    assert t.startswith("[STALE: SEATS.md has no compiled section")
    assert len(t) <= ask.SEATS_CAP


def test_gather_context_carries_compiled_seats(monkeypatch, tmp_path):
    (tmp_path / "SEATS.md").write_text(HAND + COMPILED, encoding="utf-8")
    monkeypatch.setattr(ask, "IMPROVE", tmp_path)
    blob, sources = ask.gather_context(question="which lanes are live")
    assert any(s["label"].startswith("SEATS.md compiled") for s in sources)
    assert "worker drift row" in blob
