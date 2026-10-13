"""persistence tests (LW5, 2026-09-30): S18 v1, replay-on-boot.

Laws proven:
  - save -> load rebuilds a byte-identical world: physics spec (volumes,
    steam, pipe open/primed), winner, scores, roster, and the chained rows
  - the chain CONTINUES across save/load: new rows append with the right
    seq/prev, and a third life boots from the second life's save
  - kind:snapshot rows ride the SAME chain (JSONL + save doc, one hash
    space), and the world.py save_interval wiring fires on tick multiples
  - a corrupt save refuses to boot (fail-closed, like the log chain law)
  - JSONL rows that outlived the save doc (crash between chain flush and
    doc write) replay too: boot recovers to the log's true tip

The drive script extends test_server_v0's SCRIPT with LW6 say/whisper
steps so replay covers every row kind the chain now carries.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from server.persistence import (  # noqa: E402
    SCHEMA,
    _apply_graph_spec,
    load,
    restore_world,
    save,
    verify_tail,
)
from server.world import (  # noqa: E402
    GENESIS,
    MountainWorld,
    load_log_rows,
    row_sha,
    verify_log_rows,
)

STEPS = [
    ("stage", "s1", "boil", "spring"),
    ("tick",),
    ("stage", "s2", "tag", "hollow"),
    ("stage", "s1", "valve", "p_bypass"),
    ("stage", "s2", "say", "the gate holds"),
    ("stage", "s1", "whisper", "ben|psst, open the bypass"),
    ("tick",),
    ("stage", "s1", "boil", "spring"),
    ("stage", "s2", "join", "terrace"),
    ("stage", "s1", "whisper", "ben|steam rises"),
    ("tick",),
    ("stage", "s1", "boil", "spring"),   # spring dry here: DRY_POOL reject
    ("stage", "s1", "boil", "gate1"),    # pooled XOR water is boilable
    ("tick",),
    ("stage", "s2", "tag", "crown"),
    ("stage", "s1", "boil", "crown"),    # steam condenses back at the crown
    ("tick",),
]


def _drive(w: MountainWorld) -> None:
    w.register_session("s1", "ada")
    w.register_session("s2", "ben")
    for step in STEPS:
        if step[0] == "stage":
            w.stage(step[1], step[2], step[3])
        else:
            w.tick()


def _fingerprint(w: MountainWorld) -> dict:
    """Every durable byte of a world (direct lines and pending staging are
    transient by law, not part of the save)."""
    return {
        "spec": w.graph.to_spec(),
        "winner": w.winner,
        "scores": dict(w.scores),
        "roster": {sid: dict(info) for sid, info in w.roster.items()},
        "rows": [json.dumps(r, sort_keys=True, separators=(",", ":"))
                 for r in w.rows],
    }


def _write_doc(path: Path, doc: dict) -> None:
    path.write_text(json.dumps(doc, sort_keys=True, separators=(",", ":")),
                    encoding="utf-8")


def _rechain(rows: list[dict]) -> list[dict]:
    """Re-hash a tampered row set into a VALID chain (test helper for the
    unknown-kind refusal: the chain must be intact so replay is the layer
    that rejects, not verify_tail)."""
    prev = GENESIS
    for i, r in enumerate(rows):
        r["seq"], r["prev"] = i + 1, prev
        r.pop("sha", None)
        r["sha"] = row_sha(r)
        prev = r["sha"]
    return rows


# ------------------------------------------------------------ byte-identity --

def test_save_load_rebuilds_a_byte_identical_world(tmp_path):
    """The boot path (log file + save doc): life two is life one, byte for
    byte, including the whole chained history and the roster. Interval
    saves lace snapshots through the chain, so the load actually REPLAYS
    the rows between the first tail snapshot and the end (adoption alone
    would prove nothing about determinism)."""
    log, sv = tmp_path / "chain.jsonl", tmp_path / "save.json"
    a = MountainWorld(log_path=log, save_path=sv, save_interval=2)
    _drive(a)
    out = save(a, sv)
    a.close()
    assert out["saved"] is True and out["tail_rows"] == len(a.rows)
    snaps = [r for r in a.rows if r["kind"] == "snapshot"]
    assert len(snaps) >= 3  # interval saves + the final manual one

    b = MountainWorld(log_path=log, save_path=sv)  # load-if-exists on boot
    try:
        assert _fingerprint(b) == _fingerprint(a)
        doc = json.loads(sv.read_text(encoding="utf-8"))
        assert b.node_volumes() == doc["volumes"]
    finally:
        b.close()
    # the log file itself is the shared history: one chain, two lives
    assert load_log_rows(log) == a.rows


def test_load_without_log_adopts_the_tail_and_replays(tmp_path):
    """load(path): a fresh world rebuilt by pure replay, no log file. The
    short script means the tail IS the whole chain (seq starts at 1), and
    the replay report proves rows were re-derived, not adopted."""
    sv = tmp_path / "save.json"
    a = MountainWorld(save_path=sv, save_interval=2)
    _drive(a)
    save(a, sv)  # final save: the doc's truth covers the last tick too

    w = MountainWorld()
    report = restore_world(w, sv)
    assert report["restored"] is True
    assert report["rows_replayed"] > 0  # real replay between snapshots

    b = load(sv)
    assert b.log_path is None
    assert _fingerprint(b) == _fingerprint(a)
    assert verify_tail(b.rows) is True
    assert b.rows[0]["seq"] == 1
    kinds = {r["kind"] for r in b.rows}
    assert kinds == {"action", "tick", "whisper", "snapshot"}


# ---------------------------------------------------------- chain continues --

def test_chain_continues_across_save_load(tmp_path):
    """Three lives, one chain: a saves, b boots + acts + saves again, c
    boots from b's save. seq/prev never reset; the world stays alive."""
    log, sv = tmp_path / "chain.jsonl", tmp_path / "save.json"
    a = MountainWorld(log_path=log, save_path=sv)
    _drive(a)
    save(a, sv)
    a.close()
    tip_a = load_log_rows(log)[-1]

    b = MountainWorld(log_path=log, save_path=sv)
    b.register_session("s3", "cy")
    assert b.stage("s3", "join", "terrace")["op"] == "ack"
    assert b.stage("s3", "valve", "p_bypass")["op"] == "ack"
    b.tick()
    save(b, sv)
    b.close()
    rows_b = load_log_rows(log)
    assert verify_log_rows(rows_b) is True
    # b's first new row links to a's snapshot tip (join, valve, tick, snap)
    first_new = rows_b[len(rows_b) - 4]
    assert first_new["seq"] == tip_a["seq"] + 1
    assert first_new["prev"] == tip_a["sha"]
    # the world moved on after the restore (not a frozen museum piece)
    assert rows_b[-2]["tick"] > tip_a["tick"]

    c = MountainWorld(log_path=log, save_path=sv)  # boots from b's save
    try:
        assert _fingerprint(c) == _fingerprint(b)
        assert c.stage("s3", "tag", "crown")["op"] in ("ack", "reject")
        c.tick()
        assert verify_log_rows(load_log_rows(log)) is True
    finally:
        c.close()


def test_rows_written_after_the_save_replay_too(tmp_path):
    """Crash window: the chain flushed rows past the save doc (process died
    between chain flush and doc write). Boot replays doc tail + disk
    continuation and recovers to the log's true tip."""
    log, sv = tmp_path / "chain.jsonl", tmp_path / "save.json"
    a = MountainWorld(log_path=log, save_path=sv)
    _drive(a)
    save(a, sv)
    # no second save: these rows live only in the JSONL, ahead of the doc
    a.register_session("s3", "cy")
    assert a.stage("s3", "join", "terrace")["op"] == "ack"
    assert a.stage("s3", "valve", "p_bypass")["op"] == "ack"
    assert a.stage("s3", "whisper", "ada|still here?")["op"] == "ack"
    a.tick()
    a.close()
    final = load_log_rows(log)

    b = MountainWorld(log_path=log, save_path=sv)  # doc is stale on purpose
    try:
        assert b.node_volumes() == final[-1]["nodes"]
        assert b.graph.to_spec() == a.graph.to_spec()
        assert b.scores == a.scores and b.winner == a.winner
        assert [r["sha"] for r in b.rows] == [r["sha"] for r in final]
        # s3 is a session the save doc never saw: its sid is replay-synthetic
        # (rows carry user only), so compare the user set, not the sid keys
        assert {i["user"] for i in b.roster.values()} == \
            {i["user"] for i in a.roster.values()}
        # and the recovered world keeps going: chain continues from the tip
        n_before = len(load_log_rows(log))
        b.tick()
        assert len(load_log_rows(log)) == n_before + 1
        assert verify_log_rows(load_log_rows(log)) is True
    finally:
        b.close()


# ------------------------------------------------------- snapshot + wiring --

def test_save_interval_autosaves_on_tick_multiples(tmp_path):
    """The world.py wiring: save_path + save_interval means every
    tick % interval == 0 lands a snapshot row and rewrites the doc."""
    sv = tmp_path / "save.json"
    w = MountainWorld(save_path=sv, save_interval=3)
    w.register_session("s1", "ada")
    w.tick()
    w.tick()
    assert not sv.exists()  # tick 2 is not a multiple of 3
    w.tick()                # tick 3: the snapshot fires
    assert sv.exists()
    doc = json.loads(sv.read_text(encoding="utf-8"))
    assert doc["schema"] == SCHEMA
    assert doc["tick"] == 3 and doc["rows"][-1]["kind"] == "snapshot"
    assert doc["rows"][-1]["tick"] == 3
    for _ in range(3):
        w.tick()            # ticks 4, 5, 6
    doc = json.loads(sv.read_text(encoding="utf-8"))
    assert doc["tick"] == 6 and doc["rows"][-1]["kind"] == "snapshot"
    w.close()

    b = MountainWorld(save_path=sv)  # boots at tick 6
    try:
        assert b.graph.tick_count == 6
        assert b.node_volumes() == doc["volumes"]
        assert b.rows[-1]["sha"] == doc["rows"][-1]["sha"]
    finally:
        b.close()


def test_snapshot_rows_ride_the_same_chain(tmp_path):
    """kind:snapshot is a row of the ONE chain: it lands in the JSONL with
    prev linked, and the save doc's last row is that same byte-identical
    row (one hash space, not a side file)."""
    log, sv = tmp_path / "chain.jsonl", tmp_path / "save.json"
    w = MountainWorld(log_path=log, save_path=sv, save_interval=2)
    w.register_session("s1", "ada")
    assert w.stage("s1", "boil", "spring")["op"] == "ack"
    w.tick()
    w.tick()  # interval 2: snapshot row appended after the second tick row
    w.close()
    rows = load_log_rows(log)
    assert [r["kind"] for r in rows] == ["action", "tick", "tick", "snapshot"]
    assert verify_log_rows(rows) is True
    assert rows[-1]["prev"] == rows[-2]["sha"]
    assert "spec" in rows[-1] and "roster" in rows[-1] and "scores" in rows[-1]

    doc = json.loads(sv.read_text(encoding="utf-8"))
    assert doc["rows"][-1] == rows[-1]
    assert doc["rows"][-1]["sha"] == rows[-1]["sha"]


# ------------------------------------------------------------- fail-closed --

def test_corrupt_save_refuses_to_boot(tmp_path):
    """Four corruptions, four refusals: edited row (hash breaks), volumes
    lie (replay disagrees with the doc anchor), snapshot stripped (no
    replay anchor), unknown row kind on an otherwise VALID chain."""
    log, sv = tmp_path / "chain.jsonl", tmp_path / "save.json"
    a = MountainWorld(log_path=log, save_path=sv, save_interval=2)
    _drive(a)
    save(a, sv)
    a.close()
    good = json.loads(sv.read_text(encoding="utf-8"))

    # control: the untouched doc boots
    b = MountainWorld(save_path=sv)
    b.close()

    # (a) edit a tail row's payload: the chain hash stops covering it
    doc = copy.deepcopy(good)
    doc["rows"][0]["tick"] = 99
    _write_doc(sv, doc)
    with pytest.raises(ValueError, match="hash does not cover"):
        restore_world(MountainWorld(), sv)

    # (b) volumes lie: chain intact, but replay lands elsewhere
    doc = copy.deepcopy(good)
    doc["volumes"]["crown"] = doc["volumes"]["crown"] + 1
    _write_doc(sv, doc)
    with pytest.raises(ValueError, match="disagree with the doc"):
        restore_world(MountainWorld(), sv)

    # (c) snapshot rows stripped (and the chain renumbered so it still
    # verifies): no anchor to replay from
    doc = copy.deepcopy(good)
    doc["rows"] = _rechain([r for r in doc["rows"]
                            if r["kind"] != "snapshot"])
    _write_doc(sv, doc)
    with pytest.raises(ValueError, match="no kind:snapshot row"):
        restore_world(MountainWorld(), sv)

    # (d) unknown row kind on a re-hashed VALID chain: replay itself refuses.
    # The row must sit AFTER the replay anchor (the first tail snapshot),
    # because replay only visits rows the anchor does not already cover.
    doc = copy.deepcopy(good)
    anchor_i = next(i for i, r in enumerate(doc["rows"])
                    if r["kind"] == "snapshot")
    after = next(i for i in range(anchor_i + 1, len(doc["rows"]))
                 if doc["rows"][i]["kind"] == "action")
    doc["rows"][after]["kind"] = "wormhole"
    _rechain(doc["rows"])
    _write_doc(sv, doc)
    with pytest.raises(ValueError, match="unknown row kind"):
        restore_world(MountainWorld(), sv)

    # the log file on disk was never touched by any of this
    assert verify_log_rows(load_log_rows(log)) is True


# ------------------------------------------- Q23: actor_class in the replay --
#
# Both tests use ONE manual save (save_interval left at 0) so the doc holds
# exactly one snapshot row, its anchor and last row: the rows past the doc
# (the crash window) then replay through _apply/_whisper at boot, which is
# the byte-equality surface actor_class must survive. (Written while the
# stress-replay debt was red on HEAD — _apply_graph_spec dropped pipe
# stress, so a doc with a SECOND snapshot after its anchor could not boot;
# that debt is fixed and pinned below, 2026-10-01, but these two keep the
# single-snapshot shape so actor_class stays the only variable they test.)

def test_q23_pre_change_save_doc_boots_and_replays_unchanged(tmp_path):
    """Grandfather law on the BOOT path: a save doc whose authored rows
    carry no actor_class (every pre-Q23 doc's exact shape) boots and its
    past-the-doc rows replay byte for byte — player rows still omit the
    field, so replaying an old doc lands on identical bytes."""
    log, sv = tmp_path / "old_chain.jsonl", tmp_path / "old_save.json"
    w = MountainWorld(log_path=log, save_path=sv)
    _drive(w)
    save(w, sv)
    # rows past the doc (the crash window): boot must re-derive them too
    w.stage("s1", "join", "terrace")
    w.tick()
    w.close()

    doc = json.loads(sv.read_text(encoding="utf-8"))
    authored = [r for r in doc["rows"]
                if r.get("kind") in ("action", "whisper")]
    assert authored and all("actor_class" not in r for r in authored)
    assert [r["kind"] for r in doc["rows"][-1:]] == ["snapshot"]

    again = MountainWorld(log_path=log, save_path=sv)
    try:
        assert verify_log_rows(again.rows) is True
        assert again.rows == load_log_rows(log)   # replay landed on the tip
        late = [r for r in again.rows if r.get("verb") == "join"
                and r.get("user") == "ada"]
        assert late and all("actor_class" not in r for r in late)
    finally:
        again.close()


def test_q23_bot_rows_round_trip_through_save_and_replay(tmp_path):
    """The new field is replay-honest: a bot's authored rows keep
    actor_class "bot" across save -> boot, because _apply/_whisper
    re-derive the class from the user name (a pure function of the row's
    own user field) and the re-derived row must equal the logged row."""
    log, sv = tmp_path / "bot_chain.jsonl", tmp_path / "bot_save.json"
    w = MountainWorld(log_path=log, save_path=sv)
    w.register_session("s_bot", "innkeeper")
    w.register_session("s1", "ada")
    w.stage("s_bot", "say", "rounds on the house")
    w.stage("s1", "boil", "spring")
    w.tick()
    save(w, sv)                                  # doc tip: the snapshot row
    w.stage("s_bot", "join", "terrace")          # past the doc: replayed
    w.stage("s_bot", "whisper", "ada|last call")
    w.tick()
    w.close()

    again = MountainWorld(log_path=log, save_path=sv)
    try:
        assert again.rows == load_log_rows(log)  # boot replayed to the tip
        bot_rows = [r for r in again.rows if r.get("user") == "innkeeper"]
        assert {r["kind"] for r in bot_rows} == {"action", "whisper"}
        assert all(r["actor_class"] == "bot" for r in bot_rows)
        ada = [r for r in again.rows if r.get("user") == "ada"]
        assert ada and all("actor_class" not in r for r in ada)
        assert verify_log_rows(again.rows) is True
    finally:
        again.close()


# ------------------------- stress/fracture on the anchor restore (2026-10-01) --
#
# Root cause of the 5-test red set on HEAD: _apply_graph_spec restored pipe
# open/primed but dropped stress/fractured, so the replay board's pipes
# rebooted at fresh-board defaults and any tail with a second snapshot after
# its anchor diverged. Pinned here so the wear law cannot silently leave the
# boot path again (tools/mountain_reveal.py holds the reveal-path pin, LM2).

def test_anchor_restore_carries_pipe_stress_and_fracture():
    """AC2 wear law on the BOOT path: the anchor restore lands per-pipe
    stress (cumulative full-bore throughput) and the burst flag on the
    replay board exactly as the spec carries them — else the next snapshot
    row disagrees and fracture timing replays wrong."""
    a = MountainWorld()
    _drive(a)
    spec = a.graph.to_spec()
    assert any(p["stress"] > 0 for p in spec["pipes"].values()), \
        "the drive must accrue stress or this pin is vacuous"
    spec["pipes"]["p_bypass"]["fractured"] = True  # pin the burst flag too
    b = MountainWorld()
    _apply_graph_spec(b.graph, spec)
    assert b.graph.to_spec() == spec


def test_pre_stress_spec_boots_with_fresh_pipe_defaults(tmp_path):
    """Old-doc grandfather law: a save doc whose pipe specs predate the
    stress/fractured fields (a pre-AC2 doc's exact shape — single manual
    save, so the anchor is the doc's only snapshot) still boots, defaulting
    each pipe the way the engine defaults a fresh one (stress=0, not
    fractured; Pipe defaults in mag/water_graph.py, mirrored by from_spec)."""
    sv = tmp_path / "old_save.json"
    a = MountainWorld(save_path=sv)
    _drive(a)
    save(a, sv)
    a.close()

    doc = json.loads(sv.read_text(encoding="utf-8"))
    snaps = [r for r in doc["rows"] if r["kind"] == "snapshot"]
    assert len(snaps) == 1  # the Q23 single-snapshot shape: anchor == tip
    assert any(p["stress"] > 0 for p in snaps[0]["spec"]["pipes"].values()), \
        "the strip below must actually strip something"
    for r in snaps:
        for p in r["spec"]["pipes"].values():
            p.pop("stress", None)
            p.pop("fractured", None)
    _rechain(doc["rows"])
    _write_doc(sv, doc)

    b = MountainWorld(save_path=sv)  # no log file: pure doc boot
    try:
        assert all(p.stress == 0 and not p.fractured
                   for p in b.graph.pipes.values())
        assert b.node_volumes() == doc["volumes"]
        assert verify_tail(b.rows) is True
    finally:
        b.close()
