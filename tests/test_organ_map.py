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
    """SPEC (2026-09-29 wave5 suite-burn repair; the open_gaps>0 clause is superseded
    by the bank law). The operational graph must have explicit cycles (beta1 > 0),
    every edge honestly unverified, and Dirac-loop closure must be the receipt-backed
    act the committed law defines (mag/dirac_loop.py _known_invariants docstring,
    2026-09-27: "Closure is now a receipt-backed act: bank(loop_edge, receipt) ...
    Adding graph edges never closes loops - only banking the holonomy does"):
    closed_solved + open_gaps == n_loops, and every CLOSED loop's invariant must be
    a receipt-carrying row in watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl.

    The old `assert scan["open_gaps"] > 0` encoded a frontier that legitimately no
    longer exists: all 6 operational loops were banked closed with receipts (ledger
    history: 4638646d4 first bank, 79f0f50d5 loops 4+5, 6c43c15d2 loop 6,
    a23928aca closed 5 / open 1 then the last; all rows carry receipt=True). A
    positive-gap requirement could now only be satisfied by manufacturing a fake
    graph edge or un-banking real work, so the enforced law is the accounting and
    the receipt chain instead of a guaranteed gap."""
    import json
    from pathlib import Path

    from mag import dirac_loop
    from mag.organ_map import operational_graph

    graph = operational_graph()
    assert graph["nodes"] and graph["edges"]
    assert all(edge["verified"] is False for edge in graph["edges"])
    scan = dirac_loop.scan(scope="operational")
    assert scan["ok"] is True
    assert scan["betti1"] > 0
    assert scan["closed_solved"] + scan["open_gaps"] == scan["n_loops"], (
        f"loop accounting must add up: {scan['closed_solved']} closed + "
        f"{scan['open_gaps']} open != {scan['n_loops']} loops")
    ledger = (Path(dirac_loop.__file__).resolve().parents[1]
              / "watch" / "inbox" / "DIRAC_BANKED_INVARIANTS.jsonl")
    banked: dict[str, dict] = {}
    for line in ledger.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("invariant") and row.get("receipt"):
            banked[row["invariant"]] = row
    for lp in scan["closed"]:
        assert lp["invariant"] in banked, (
            f"closed loop without a banked receipt (closure must be a banked act): "
            f"{lp['edge']}")
    for lp in scan["open"]:
        assert lp["status"] == "open" and lp["invariant"] not in banked, (
            f"an open loop must be honestly labeled and unbanked: {lp['edge']}")


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
