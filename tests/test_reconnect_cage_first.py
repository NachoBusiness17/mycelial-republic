"""Seats must grab the cage, not legacy host lab, when Mag looks down."""
from __future__ import annotations

from mag.health import HOST_LAB_LAST, reconnect_plan
from mag.runtime import read_heartbeat


def test_reconnect_plan_cage_first() -> None:
    p = reconnect_plan()
    cmd = " ".join(
        [
            str(p.get("command") or ""),
            str(p.get("first") or ""),
            str(p.get("doctor") or ""),
            " ".join(p.get("commands") or []),
        ]
    )
    assert "python main.py lab" not in cmd
    assert "mag.cmd doctor" in str(p.get("doctor") or "") or "mag.cmd doctor" in cmd
    assert "python main.py lab" in HOST_LAB_LAST
    assert "LAST RESORT" in HOST_LAB_LAST


def test_stale_heartbeat_note_is_not_host_lab() -> None:
    hb = read_heartbeat()
    note = str(hb.get("note") or "")
    if hb.get("alive"):
        assert "Integral process is up" in note
        return
    assert "python main.py lab" in note  # mentioned as forbidden
    assert "Do not run host" in note or "second supervisor" in note
    assert "mag.cmd doctor" in note or "docker compose restart mag" in note
