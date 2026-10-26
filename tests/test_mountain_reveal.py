"""tests for tools/mountain_reveal.py — the DFHack reveal/prospect overlay.

All fixtures ride the DEFAULT Mountain board (server/world.py's
build_mountain_graph): offline mode constructs it directly, replay mode
writes a chain with MountainWorld in tmp_path and reads it back. The
drift/partial/tamper paths are exercised on chain-valid logs so every
exit the CLI can take is covered. Evidence style: byte-backed asserts
against the engine's own numbers, never hand-copied expectations.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.water_graph import fracture_threshold  # noqa: E402
from server.world import MountainWorld, row_sha  # noqa: E402
from tools import mountain_reveal as mr  # noqa: E402

BOARD_NODES = {"spring", "terrace", "gate1", "hollow", "waste", "crown"}
BOARD_PIPES = {"p_spring", "p_terrace", "p_out", "p_drain", "p_bypass"}
ENDOWMENT = 8  # spring 6 + hollow 2 (the docstring's "total water: 8")


def write_log(tmp_path: Path, name: str = "replay.jsonl") -> Path:
    """A real chain: one player boils, says, and ticks 4 times."""
    path = tmp_path / name
    w = MountainWorld(log_path=path)
    w.register_session("s1", "digger", at="spring")
    w.stage("s1", "boil", "spring")
    w.stage("s1", "say", "the gate holds")
    for _ in range(4):
        w.tick()
    w.close()
    return path


# ---------------------------------------------------------------- reveal --
def test_reveal_offline_default_board(capsys):
    assert mr.main(["reveal", "--json"]) == 0
    p = json.loads(capsys.readouterr().out)
    assert set(p["nodes"]) == BOARD_NODES
    assert set(p["pipes"]) == BOARD_PIPES
    assert p["mode"] == "offline" and p["tick"] == 0 and not p["winner"]
    spring, crown, gate1 = p["nodes"]["spring"], p["nodes"]["crown"], p["nodes"]["gate1"]
    assert (spring["volume"], spring["elev"], spring["type"]) == (6, 10, "plain")
    assert (crown["elev"], crown["type"]) == (14, "cold")
    assert gate1["type"] == "xor"
    assert p["pipes"]["p_bypass"]["state"] == "siphon-shut"   # board: STARTS SHUT
    assert all(q["cap"] == 1 for q in p["pipes"].values())


def test_reveal_offline_ticks_match_engine_truth(capsys):
    ref = MountainWorld()
    for _ in range(5):
        ref.tick()
    assert mr.main(["reveal", "--ticks", "5", "--json"]) == 0
    p = json.loads(capsys.readouterr().out)
    assert p["tick"] == 5
    assert {n: d["volume"] for n, d in p["nodes"].items()} == ref.node_volumes()
    assert p["winner"] == ref.winner


def test_reveal_junction_gate_and_gated_outflow_flag(capsys):
    assert mr.main(["reveal", "--ticks", "2", "--json"]) == 0
    p = json.loads(capsys.readouterr().out)
    (gate,) = p["junctions"]
    assert gate["node"] == "gate1" and gate["verdict"] in ("PASS", "HOLD")
    assert {i["pipe"] for i in gate["inlets"]} == {"p_spring", "p_terrace"}
    # outflow from a gated junction waits on the verdict — flagged, projected
    assert p["pipes"]["p_out"]["waits_gate"] is True
    assert p["pipes"]["p_spring"]["waits_gate"] is False


def test_reveal_waste_boil_block(capsys):
    assert mr.main(["reveal", "--ticks", "12", "--json"]) == 0
    p = json.loads(capsys.readouterr().out)
    wb = p["waste_boil"]
    # the 12-tick board drains everything into the waste basin (V5: it HOLDS)
    assert wb["waste_held"] == ENDOWMENT
    assert wb["condenses_at"] == "crown"
    assert wb["boilable_liquid"] == ENDOWMENT
    assert p["nodes"]["waste"]["volume"] == ENDOWMENT


def test_node_stress_is_incident_pipe_load(capsys):
    w = MountainWorld()
    for _ in range(3):
        w.tick()
    g = mr.reveal_payload(w, "t", "offline")
    hollow_load = sum(p_.stress for p_ in w.graph.pipes.values()
                      if p_.src == "hollow" or p_.dst == "hollow")
    assert g["nodes"]["hollow"]["stress"] == hollow_load
    # engine truth (B1 seam fix 2026-09-30, B1_FRACTURE_REACH.md): p_drain
    # (plain->plain) AND p_spring (gated inlet -> XOR) both load — full-bore
    # flow stresses the pipe at probe time too, so the board's main artery
    # can burst. 3 ticks x cap-1 full bore = stress 3 each. The old law
    # never loaded gated inlets (the seam LM2 flagged; B1 closed it).
    assert w.graph.pipes["p_drain"].stress == 3
    assert w.graph.pipes["p_spring"].stress == 3


# -------------------------------------------------------------- prospect --
def test_prospect_default_board_conservation(capsys):
    assert mr.main(["prospect", "--json"]) == 0
    p = json.loads(capsys.readouterr().out)
    assert (p["total_water"], p["liquid"], p["steam"]) == (ENDOWMENT, ENDOWMENT, 0)
    assert p["drift"] == 0
    shares = sum(d["volume"] + d["steam"] for d in p["distribution"])
    assert shares == ENDOWMENT
    assert {d["node"] for d in p["distribution"]} == BOARD_NODES


def test_prospect_fracture_risk_ranking(capsys):
    ref = MountainWorld()
    for _ in range(12):
        ref.tick()
    assert mr.main(["prospect", "--ticks", "12", "--json"]) == 0
    p = json.loads(capsys.readouterr().out)
    risk = p["fracture_risk"]
    ratios = [r["ratio"] for r in risk]
    assert ratios == sorted(ratios, reverse=True)          # ranked
    assert all(200 <= r["threshold"] <= 400 for r in risk)  # B1 hash band (volume units)
    assert all(r["ratio"] <= 1.0 for r in risk)
    by_name = {r["pipe"]: r for r in risk}
    for name, q in ref.graph.pipes.items():
        assert by_name[name]["stress"] == q.stress         # engine truth
        assert by_name[name]["threshold"] == fracture_threshold(name)
    pd = by_name["p_drain"]                                # plain->plain: loaded
    assert pd["stress"] == ref.graph.pipes["p_drain"].stress > 0
    assert pd["full_bore_ticks_to_burst"] == -(-(pd["threshold"] - pd["stress"]) // 1)


def test_prospect_flags_pre_v5_drift_from_real_log_shape(tmp_path, capsys):
    # a chain whose tick rows were written by the pre-V5 engine (waste
    # deleted water): replay under today's physics diverges -> partial,
    # and prospect must NAME the theft as drift, not hide it.
    rows = []
    prev = "0" * 64
    for seq in range(1, 4):
        row = {"kind": "tick", "tick": seq, "events": [],
               "nodes": {k: 0 for k in BOARD_NODES},  # old engine deleted it all
               "winner": False, "seq": seq, "prev": prev}
        row["sha"] = row_sha(row)
        rows.append(row)
        prev = row["sha"]
    path = tmp_path / "pre_v5.jsonl"
    path.write_text("\n".join(json.dumps(r, sort_keys=True) for r in rows),
                    encoding="utf-8")
    assert mr.main(["prospect", "--from-replay", str(path), "--json"]) == 0
    cap = capsys.readouterr()
    p = json.loads(cap.out)
    assert p["mode"] == "partial" and p["drift"] == -ENDOWMENT
    assert "PHYSICS DRIFT" in cap.err


# ---------------------------------------------------------------- events --
def test_events_offline_ticks_carry_tick_numbers(capsys):
    assert mr.main(["events", "4", "--ticks", "3", "--json"]) == 0
    p = json.loads(capsys.readouterr().out)
    evs = p["events"]
    assert len(evs) == 4
    assert all(1 <= e["tick"] <= 3 and e["seq"] >= 1 for e in evs)
    assert any("spring->gate1" in e["event"] for e in evs)


def test_events_replay_includes_actions_and_chat(tmp_path, capsys):
    path = write_log(tmp_path)
    assert mr.main(["events", "50", "--from-replay", str(path), "--json"]) == 0
    evs = json.loads(capsys.readouterr().out)["events"]
    text = " ".join(e["event"] for e in evs)
    assert "boils 1 at spring" in text        # the staged action, applied
    assert "digger: the gate holds" in text   # LW6 say line
    assert all(e["tick"] >= 1 for e in evs)


# ---------------------------------------------------------------- replay --
def test_replay_roundtrip_restores_state(tmp_path, capsys):
    path = write_log(tmp_path)
    world, rows, mode = mr.open_replay(path)
    assert mode == "replay"
    ref = MountainWorld()
    ref.register_session("s1", "digger", at="spring")
    ref.stage("s1", "boil", "spring")
    ref.stage("s1", "say", "the gate holds")
    for _ in range(4):
        ref.tick()
    assert world.node_volumes() == ref.node_volumes()
    assert world.graph.tick_count == ref.graph.tick_count
    assert world.winner == ref.winner
    assert world.scores == ref.scores
    assert mr.main(["reveal", "--from-replay", str(path), "--json"]) == 0
    p = json.loads(capsys.readouterr().out)
    assert p["tick"] == 4 and p["mode"] == "replay"


def test_replay_tampered_chain_exits_2(tmp_path, capsys):
    path = write_log(tmp_path)
    lines = path.read_text(encoding="utf-8").splitlines()
    i = next(i for i, l in enumerate(lines)
             if json.loads(l)["kind"] == "tick")            # a tick row has nodes
    row = json.loads(lines[i])
    row["nodes"]["spring"] = 99              # edit WITHOUT re-hashing
    lines[i] = json.dumps(row, sort_keys=True, separators=(",", ":"))
    bad = tmp_path / "bad.jsonl"
    bad.write_text("\n".join(lines), encoding="utf-8")
    with pytest.raises(SystemExit) as ei:
        mr.main(["reveal", "--from-replay", str(bad), "--json"])
    assert ei.value.code == 2
    assert "corrupt" in capsys.readouterr().err


def test_replay_tail_without_anchor_is_partial(tmp_path, capsys):
    path = write_log(tmp_path)
    lines = path.read_text(encoding="utf-8").splitlines()
    tail = tmp_path / "tail.jsonl"
    tail.write_text("\n".join(lines[1:]), encoding="utf-8")  # seq starts at 2
    world, rows, mode = mr.open_replay(tail)
    assert mode == "partial"
    last_tick = next(r for r in reversed(rows) if r["kind"] == "tick")
    assert world.node_volumes() == last_tick["nodes"]
    assert world.graph.tick_count == last_tick["tick"]


def test_replay_snapshot_anchor_shortens_replay(tmp_path, capsys):
    import server.persistence as pers
    w = MountainWorld(log_path=tmp_path / "snap.jsonl",
                      save_path=tmp_path / "snap.json", save_interval=2)
    w.register_session("s1", "digger", at="spring")
    for _ in range(4):
        w.tick()
    pers.save(w, tmp_path / "snap.json")
    w.close()
    path = tmp_path / "snap.jsonl"
    world, rows, mode = mr.open_replay(path)
    assert mode == "replay"
    assert world.node_volumes() == w.node_volumes()
    assert any(r["kind"] == "snapshot" for r in rows)


def test_replay_anchor_restores_pipe_stress(tmp_path):
    # LM2: persistence._apply_graph_spec drops stress/fractured, so an
    # anchored replay with accrued load diverged at the next snapshot row.
    # Our anchor adopts the spec's stress (LW5 roundtrip law); this log —
    # snapshots every tick, then two unsaved ticks — replays byte-clean.
    path = tmp_path / "stress.jsonl"
    w = MountainWorld(log_path=path, save_path=tmp_path / "s.json",
                      save_interval=1)
    for _ in range(3):
        w.tick()
    w.save_interval = 0                      # post-anchor rows: plain ticks
    for _ in range(2):
        w.tick()
    w.close()
    world, rows, mode = mr.open_replay(path)
    assert mode == "replay"
    assert world.node_volumes() == w.node_volumes()
    assert world.graph.tick_count == w.graph.tick_count == 5
    for name, p in w.graph.pipes.items():
        assert world.graph.pipes[name].stress == p.stress
        assert world.graph.pipes[name].fractured == p.fractured


def test_cli_text_render_smoke(capsys):
    assert mr.main(["reveal", "--ticks", "2"]) == 0
    out = capsys.readouterr().out
    assert "MOUNTAIN REVEAL" in out and "junction gate1" in out
    assert "p_bypass" in out and "siphon-shut" in out
    assert mr.main(["prospect", "--ticks", "2"]) == 0
    assert "MOUNTAIN PROSPECT" in capsys.readouterr().out
    assert mr.main(["events", "3", "--ticks", "2"]) == 0
    assert "MOUNTAIN EVENTS" in capsys.readouterr().out


def test_ticks_flag_rejected_with_replay(tmp_path, capsys):
    path = write_log(tmp_path)
    with pytest.raises(SystemExit):
        mr.main(["reveal", "--from-replay", str(path), "--ticks", "1"])
