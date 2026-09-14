"""Receipts-first organ map and operational Dirac graph tests."""
from __future__ import annotations


def test_map_separates_callable_from_live() -> None:
    from mag.organ_map import map_organs

    out = map_organs()
    rows = {row["id"]: row for row in out["organs"]}
    assert rows["context_admission"]["callable_imports"] is True
    assert "INSTRUMENTED" in rows["context_admission"]["levels"]
    # A callable/verified organ is not promoted to LIVE without a recent receipt.
    assert "LIVE" not in rows["dirac_loop"]["levels"]
    # Atlas is now promoted only after the fireball dogfood chain leaves a
    # durable receipt; callable-without-evidence remains distinct from LIVE.
    assert "LIVE" in rows["atlas"]["levels"]
    # The broker has executable tests, wiring, and a recent successful board
    # receipt; nested result.ok is interpreted as live evidence.
    assert "VERIFIED" in rows["effect_broker"]["levels"]
    assert "LIVE" in rows["effect_broker"]["levels"]
    assert "GHOST" not in rows["effect_broker"]["levels"]
    assert "mag/dogfood_audit.py" in rows["read_archive"]["wired_by"]
    assert "memory/runs/read_archive/receipts.jsonl" in rows["read_archive"]["receipt_paths"]


def test_operational_graph_has_explicit_cycles_and_unverified_edges() -> None:
    from mag import dirac_loop
    from mag.organ_map import operational_graph

    graph = operational_graph()
    assert graph["nodes"] and graph["edges"]
    assert all(edge["verified"] is False for edge in graph["edges"])
    scan = dirac_loop.scan(scope="operational")
    assert scan["ok"] is True
    assert scan["betti1"] > 0
    assert scan["open_gaps"] > 0


def test_map_and_elder_surface_callable_orphans() -> None:
    from mag.elder import audit
    from mag.organ_map import map_organs

    out = map_organs()
    rows = {row["id"]: row for row in out["organs"]}
    for organ_id in ("session_bridge", "ask_router"):
        assert rows[organ_id]["callable_imports"] is True

    assert not any(code.startswith("caller_") for code in rows["ask_router"]["gap_codes"])
    assert "memory/runs/ask_router/receipts.jsonl" in rows["ask_router"]["receipt_paths"]

    assert rows["session_bridge"]["wired_evidence"] is True
    assert "memory/runs/session_bridge/receipts.jsonl" in rows["session_bridge"]["receipt_paths"]
    assert rows["read_archive"]["callable_imports"] is True
    assert rows["read_archive"]["wired_evidence"] is True
    assert not any(code.startswith("caller_") for code in rows["read_archive"]["gap_codes"])

    elder = audit()
    by_id = {row["id"]: row for row in elder["gaps"]}
    assert elder["gap_count"] == len(elder["gaps"])
    assert "ask_router" not in by_id
