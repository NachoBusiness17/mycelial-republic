"""mountain_liquids tests — DFHack's wish, through the law (LM3, 2026-09-30).

Every test is a law: a legal op rides a staged verb and CONSERVES the
board's 8 units; any intervention not in the frozen table fails CLOSED
with a typed reject and leaves the world byte-identical (zero rows, zero
ticks, unchanged volumes). The gap table is pinned as data.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from server.world import MountainWorld, VERBS  # noqa: E402
from tools.mountain_liquids import (  # noqa: E402
    INVENTORY, OPS, apply_liquids, legal_vs_gap, main,
)

BOARD_TOTAL = 8  # spring 6 + hollow 2: the conserved economy


def fresh() -> MountainWorld:
    return MountainWorld()  # default board, in-memory, offline


def untouched(world: MountainWorld, result: dict) -> None:
    """Fail-closed contract: a refusal never mutated the world."""
    assert world.rows == [], "a rejected ask must leave zero log rows"
    assert world.pending == [], "a rejected ask must stage nothing"
    assert world.graph.tick_count == 0
    assert result["tick"] == 0 and result["staged"] == 0
    assert world.node_volumes() == {
        "spring": 6, "terrace": 0, "gate1": 0, "hollow": 2,
        "waste": 0, "crown": 0}


# ------------------------------------------------------------ legal ops ----

def test_boil_is_a_staged_verb_and_conserves():
    w = fresh()
    r = apply_liquids(w, "hollow", "boil")
    assert r["ok"] and r["verb"] == "boil" and r["staged"] == 1
    assert r["tick"] == 1
    assert r["total_before"] == BOARD_TOTAL == r["total_units"]
    assert any("boils 1 at hollow" in ev for ev in r["events"])
    assert w.graph.nodes["crown"].volume == 1  # steam condensed at the crown
    assert w.rows and w.rows[-1]["kind"] == "tick"  # chained through the log


def test_boil_amount_composes_n_legal_asks():
    w = fresh()
    r = apply_liquids(w, "hollow", "boil", 5)  # hollow holds only 2
    assert r["ok"] and r["staged"] == 5
    # the engine rows stay honest: 2 lifts, 3 dry-pool admissions
    lifts = [ev for ev in r["events"] if "boils 1 at hollow" in ev]
    dry = [ev for ev in r["events"] if "pool went dry" in ev]
    assert len(lifts) == 2 and len(dry) == 3
    assert w.graph.nodes["crown"].volume == 2
    assert r["total_units"] == r["total_before"] == BOARD_TOTAL


def test_open_gate_rides_the_valve_verb():
    w = fresh()
    r = apply_liquids(w, "p_bypass", "open")  # p_bypass starts SHUT
    assert r["ok"] and r["verb"] == "valve" and r["staged"] == 1
    assert w.graph.pipes["p_bypass"].open is True
    assert r["total_units"] == BOARD_TOTAL


def test_close_gate_rides_the_valve_verb():
    w = fresh()
    r = apply_liquids(w, "p_spring", "close")
    assert r["ok"] and r["verb"] == "valve"
    assert w.graph.pipes["p_spring"].open is False
    assert r["total_units"] == BOARD_TOTAL


def test_gate_already_in_desired_state_is_a_noop_not_a_mutation():
    w = fresh()
    r = apply_liquids(w, "p_spring", "open")  # already open
    assert r["ok"] and r["reason"] == "NOOP" and r["staged"] == 0
    assert w.graph.tick_count == 0 and w.rows == []
    r2 = apply_liquids(w, "p_bypass", "close")  # already shut
    assert r2["ok"] and r2["reason"] == "NOOP" and r2["staged"] == 0
    assert w.graph.pipes["p_bypass"].open is False


def test_open_on_a_fractured_pipe_fails_closed_ac2():
    w = fresh()
    w.graph.pipes["p_bypass"].fractured = True  # engine shape: burst -> shut
    w.graph.pipes["p_bypass"].open = False
    r = apply_liquids(w, "p_bypass", "open")
    assert not r["ok"] and r["reason"] == "FRACTURED_PIPE"
    assert w.graph.pipes["p_bypass"].open is False
    untouched(w, r)


def test_close_on_a_fractured_pipe_is_an_honest_noop():
    w = fresh()
    w.graph.pipes["p_bypass"].fractured = True
    w.graph.pipes["p_bypass"].open = False
    r = apply_liquids(w, "p_bypass", "close")
    assert r["ok"] and r["reason"] == "NOOP" and "fractured" in r["note"]
    assert w.rows == [] and w.graph.tick_count == 0


def test_dry_run_validates_but_never_stages():
    w = fresh()
    r = apply_liquids(w, "spring", "boil", 3, dry_run=True)
    assert r["ok"] and r["reason"] == "DRYRUN" and r["staged"] == 3
    assert w.rows == [] and w.pending == [] and w.graph.tick_count == 0
    assert w.node_volumes()["spring"] == 6


# ------------------------------------------------- fail-closed ladder ----

def test_source_on_has_no_verb_and_fails_closed():
    w = fresh()
    r = apply_liquids(w, "spring", "source-on")
    assert not r["ok"] and r["reason"] == "UNKNOWN_VERB"
    assert "no verb in any compiled table" in r["note"]
    untouched(w, r)


def test_source_off_fails_closed_the_same_way():
    w = fresh()
    r = apply_liquids(w, "spring", "source-off")
    assert not r["ok"] and r["reason"] == "UNKNOWN_VERB"
    untouched(w, r)


def test_arbitrary_dfhack_style_op_fails_closed():
    w = fresh()
    for op in ("flood", "wsource", "obsidian", "setwater", "rmwater"):
        r = apply_liquids(w, "spring", op)
        assert not r["ok"] and r["reason"] == "UNKNOWN_VERB", op
        untouched(w, r)


def test_unknown_node_and_pipe_fail_closed():
    w = fresh()
    assert apply_liquids(w, "lake", "boil")["reason"] == "UNKNOWN_TARGET"
    assert apply_liquids(w, "p_magic", "open")["reason"] == "UNKNOWN_TARGET"


def test_dry_pool_fails_closed_at_receipt():
    w = fresh()
    r = apply_liquids(w, "terrace", "boil")  # terrace starts volume 0
    assert not r["ok"] and r["reason"] == "DRY_POOL"
    untouched(w, r)


def test_amount_u8_law():
    w = fresh()
    for bad in (True, 0, -1, 256, 1.5, "3"):
        r = apply_liquids(w, "hollow", "boil", bad)
        assert not r["ok"] and r["reason"] == "BAD_INTENSITY", bad
        untouched(w, r)
    assert apply_liquids(w, "hollow", "boil", 1)["reason"] == "ACK"


def test_valve_carries_no_amount_on_the_wire():
    w = fresh()
    r = apply_liquids(w, "p_bypass", "open", 2)
    assert not r["ok"] and r["reason"] == "BAD_ARGS"
    untouched(w, r)


def test_ops_registry_only_maps_verbs_the_world_speaks():
    for op, spec in OPS.items():
        if spec["verb"] is not None:
            assert spec["verb"] in VERBS, (op, spec["verb"])


# ------------------------------------------------------- gap inventory ----

def test_inventory_rows_are_well_formed():
    rows = legal_vs_gap()
    assert rows is INVENTORY
    statuses = {"LEGAL", "GAP", "REFUSED-BY-LAW", "CONTRACT-ONLY"}
    for row in rows:
        assert set(row) == {"wish", "verb", "status", "note"}
        assert row["status"] in statuses
        assert row["wish"] and row["note"]
        if row["status"] == "LEGAL":
            assert row["verb"] != "-"
            for v in row["verb"].split(", "):
                assert v in VERBS, v


def test_inventory_answers_the_teaching_moment():
    wishes = " | ".join(r["wish"] for r in INVENTORY)
    assert "source-on" in wishes and "source-off" in wishes
    gap = [r for r in INVENTORY if r["status"] == "GAP"]
    assert {r["verb"] for r in gap} == {"-"}  # gaps name no verb
    refused = [r for r in INVENTORY if r["status"] == "REFUSED-BY-LAW"]
    assert any("deletion is theft" in r["note"] for r in refused)  # V5 law
    assert any(r["status"] == "CONTRACT-ONLY" for r in INVENTORY)  # X9 motion


# ----------------------------------------------------------------- CLI ----

def test_cli_inventory_exits_zero(capsys):
    assert main(["--inventory"]) == 0
    out = capsys.readouterr().out
    assert "legal-vs-gap" in out and "source-on" in out and "GAP" in out


def test_cli_exit_codes_are_the_law(capsys):
    assert main(["hollow", "boil"]) == 0
    capsys.readouterr()
    assert main(["spring", "source-on"]) == 2
    out = capsys.readouterr().out
    assert "FAIL CLOSED: UNKNOWN_VERB" in out
    assert main(["p_bypass", "open", "not-a-number"]) == 2
    assert "BAD_INTENSITY" in capsys.readouterr().out


def test_cli_missing_args_is_a_usage_refusal(capsys):
    assert main([]) == 2
    assert "need <node|pipe> <op>" in capsys.readouterr().err


def test_cli_json_emits_the_result_dict(capsys):
    import json
    assert main(["hollow", "boil", "2", "--json"]) == 0
    r = json.loads(capsys.readouterr().out)
    assert r["ok"] and r["verb"] == "boil" and r["staged"] == 2
    assert r["total_units"] == r["total_before"] == BOARD_TOTAL
