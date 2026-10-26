"""persistence: S18 v1, the world survives its process (replay-on-boot).

S18's verdict (watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md, agent 6d4d5a87):
the hash-chained JSONL is strictly stronger than a KV save (auditable AND
replayable), so v1 persistence is not a database. It is:

  save(world, path)   append ONE kind:snapshot row to the LIVE chain (the
                      full authoritative state rides the row: volumes,
                      steam, pipe open/primed/stress/fractured, tick,
                      winner, scores, roster), then dump a JSON save doc
                      holding the last
                      N chain rows plus the current volumes as an
                      independent check anchor. Atomic write (tmp + replace)
                      because this file is boot-critical.
  load(path)          rebuild a world by REPLAYING the saved tail: restore
                      state from the first snapshot row in the tail, then
                      re-derive every later action/tick row through the
                      world's own _apply/tick/_append_row and assert each
                      re-derived row equals the logged one byte for byte.
  restore_world(...)  same replay, booting INTO an already-constructed
                      world (the load-if-exists call in MountainWorld), so
                      its log wiring (seq/prev/fh) survives.

Replay is verification, not trust: the determinism law (world.py docstring;
the test_server_v0 fresh-worlds proof) says the same row sequence re-derives
the same bytes, so a save that cannot replay to itself is refused at boot
with ValueError, exactly like a corrupt chain. Physics, tick rows, scores
and winner are re-derived; the snapshot row's roster is ADOPTED verbatim
because sids are session-scoped and action rows record only `user`.

Crash window: rows can land in the JSONL after the save doc was written
(chain flush precedes the doc write). restore_world replays those disk rows
too, so boot recovers to the log's true tip, not the doc's stale one.

Honest v1 limits: staged-but-unapplied actions and undelivered whisper
direct lines carry no durable state and die with the process (save normally
fires at the end of tick(), where pending has just been drained); tail
trimming/compaction is v1 debt (S18 item 3).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from mag.water_graph import WaterGraph  # noqa: F401 - type hint only
from server.world import GENESIS, MountainWorld, row_sha

SCHEMA = "world_persist.v1"
DEFAULT_TAIL_ROWS = 512
CHAIN_FIELDS = ("seq", "prev", "sha")


# ------------------------------------------------------------- snapshots ----
def snapshot_payload(world: MountainWorld) -> dict[str, Any]:
    """The state a kind:snapshot row carries. `spec` is the full physics
    state (to_spec: volumes + steam + pipe open/primed + tick), because the
    tick rows' `nodes` volumes alone would lose steam in flight and siphon
    prime state, and replay byte-equality would silently break."""
    return {
        "kind": "snapshot",
        "tick": world.graph.tick_count,
        "nodes": world.node_volumes(),
        "spec": world.graph.to_spec(),
        "winner": world.winner,
        "scores": dict(world.scores),
        "roster": {sid: dict(info) for sid, info in world.roster.items()},
    }


def _apply_graph_spec(graph: WaterGraph, spec: dict[str, Any]) -> None:
    """Restore dynamic graph state onto a freshly built Mountain board.

    Receipt (why not from_spec): water_graph.from_spec rebuilds topology
    from a spec but never reads the `primed` field back, so a siphon that
    had primed would replay unprimed and the next tick would diverge. The
    board itself is fixed (build_mountain_graph), so only the dynamic
    fields (volume/steam/open/primed/stress/fractured/tick_count) are
    restored, and the node and pipe name sets must match the board or the
    save is refused.

    AC2 wear law, persistence cut (2026-10-01, Q23 lane root-cause while
    landing actor_class): to_spec emitted per-pipe `stress` and `fractured`
    but this restore dropped both, so the replay board's pipes rebooted at
    the fresh-board defaults — a save doc with a SECOND snapshot after its
    anchor then diverged at replay ("snapshot row disagrees with replayed
    state"; 5 tests red on HEAD, tests/test_server_persist.py) and fracture
    timing itself replayed wrong, because stress is cumulative throughput.
    tools/mountain_reveal.py open_replay fixed the same drop on the reveal
    path (LM2); this is the boot path's cut of that law. Old docs whose
    specs predate the fields boot at stress=0 / not fractured — the same
    defaults the engine gives a fresh pipe (Pipe.stress=0 / fractured=
    False, mag/water_graph.py; mirrored by from_spec's p.get defaults).
    """
    if set(spec.get("nodes", {})) != set(graph.nodes):
        raise ValueError("snapshot node set does not match the Mountain board")
    if set(spec.get("pipes", {})) != set(graph.pipes):
        raise ValueError("snapshot pipe set does not match the Mountain board")
    for name, n in spec["nodes"].items():
        graph.nodes[name].volume = int(n.get("volume", 0))
        graph.nodes[name].steam = int(n.get("steam", 0))
    for name, p in spec["pipes"].items():
        graph.pipes[name].open = bool(p.get("open", True))
        graph.pipes[name].primed = bool(p.get("primed", False))
        graph.pipes[name].stress = int(p.get("stress", 0))
        graph.pipes[name].fractured = bool(p.get("fractured", False))
    graph.tick_count = int(spec.get("tick", 0))


# ------------------------------------------------------------------ save ----
def save(world: MountainWorld, path: Path | str,
         tail_rows: int = DEFAULT_TAIL_ROWS) -> dict[str, Any]:
    """Snapshot the world: one kind:snapshot row joins the live chain (so
    the checkpoint is inside the same tamper-evident append-only log, not a
    side file the chain cannot vouch for), then the save doc is written
    atomically: the last `tail_rows` chain rows + the current volumes."""
    if tail_rows < 1:
        raise ValueError("tail_rows must be >= 1")
    row = world._append_row(snapshot_payload(world))
    tail = [dict(r) for r in world.rows[-tail_rows:]]
    doc = {
        "schema": SCHEMA,
        "seq": row["seq"],
        "tick": world.graph.tick_count,
        "volumes": world.node_volumes(),
        "winner": world.winner,
        "rows": tail,
    }
    p = Path(path)
    if str(p.parent) not in ("", "."):
        p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(doc, sort_keys=True, separators=(",", ":")),
                   encoding="utf-8")
    os.replace(tmp, p)
    return {"saved": True, "seq": row["seq"], "tick": world.graph.tick_count,
            "tail_rows": len(tail)}


# ------------------------------------------------------------- integrity ----
def verify_tail(rows: list[dict[str, Any]]) -> bool:
    """Chain check for a TAIL of the log (world.verify_log_rows requires
    seq to start at 1; a save's tail starts at whatever seq the history had
    reached). Raises ValueError on the first break, like load_log_rows."""
    prev: str | None = None
    last: int | None = None
    for row in rows:
        if not isinstance(row, dict) or any(k not in row for k in CHAIN_FIELDS):
            raise ValueError("save row is missing chain fields (seq/prev/sha)")
        if last is not None and (row["seq"] != last + 1 or row["prev"] != prev):
            raise ValueError(f"save tail chain broken at seq {row['seq']}")
        if row["sha"] != row_sha(row):
            raise ValueError(f"save row hash does not cover its row (seq {row['seq']})")
        prev, last = row["sha"], row["seq"]
    return True


# ---------------------------------------------------------------- replay ----
def _sid_for(w: MountainWorld, user: str) -> str:
    """Resolve an action row to a sid. Action rows record `user` only, so
    replay uses the roster the last snapshot adopted (a user always
    registers before acting, and roster entries are never removed). A user
    the roster lacks (registered after the anchor snapshot, acting inside
    the tail) gets a synthetic sid: rows carry no sid, so this touches no
    row bytes, and the next snapshot's roster adoption heals the name."""
    sid = None
    for s, info in w.roster.items():
        if info["user"] == user:
            sid = s
    if sid is None:
        sid = "replay:" + user
        w.register_session(sid, user)
    return sid


def _replay_row(w: MountainWorld, row: dict[str, Any],
                tick_events: list[str]) -> None:
    """Re-derive ONE chained row on w through the world's own machinery and
    assert byte-identity with the logged row. First divergence raises
    ValueError: the log no longer describes a world this code can rebuild.

    `tick_events` mirrors live tick()'s event assembly: action rows hand
    their event strings to the tick row they precede (live tick() collects
    them from _apply before the physics runs), so replay buffers them the
    same way and a tick row's events are buffer + physics events.
    """
    kind = row.get("kind")
    if kind == "action":
        if row["tick"] != w.graph.tick_count + 1:
            raise ValueError(
                f"seq {row['seq']}: action row claims tick {row['tick']} "
                f"but replay is at tick_count {w.graph.tick_count}")
        tick_events.append(w._apply(
            {"sid": _sid_for(w, row["user"]), "user": row["user"],
             "verb": row["verb"], "target": row["target"]}, row["tick"]))
    elif kind == "whisper":
        # LW6 direct line: delivered at receipt, outside the canonical tick.
        # Re-derive through _whisper so the audit row and the event string
        # come from the same code that wrote them. The direct outbox itself
        # is transient delivery state: replay fills it, boot does not adopt
        # it (whispers in flight when the process died are gone, the same
        # honest loss class as staged-but-unapplied actions).
        if row["tick"] != w.graph.tick_count + 1:
            raise ValueError(
                f"seq {row['seq']}: whisper row claims tick {row['tick']} "
                f"but replay is at tick_count {w.graph.tick_count}")
        w._whisper(row["user"], row["target"])
    elif kind == "tick":
        if row["tick"] != w.graph.tick_count + 1:
            raise ValueError(
                f"seq {row['seq']}: tick row claims tick {row['tick']} "
                f"but replay is at tick_count {w.graph.tick_count}")
        events = list(tick_events)
        events.extend(w.graph.tick())
        tick_events.clear()
        if w.graph.nodes["crown"].volume >= w.WIN_CROWN:
            w.winner = True
        w._append_row({"kind": "tick", "tick": row["tick"], "events": events,
                       "nodes": w.node_volumes(), "winner": w.winner})
    elif kind == "snapshot":
        want = {k: v for k, v in snapshot_payload(w).items() if k != "roster"}
        got = {k: v for k, v in row.items()
               if k not in CHAIN_FIELDS and k != "roster"}
        if want != got:
            raise ValueError(
                f"seq {row['seq']}: snapshot row disagrees with replayed "
                f"state; the save cannot replay to itself")
        # roster rides the row verbatim (sids are session bookkeeping that
        # action rows cannot re-derive; see _sid_for)
        w.roster = {str(sid): dict(info) for sid, info in row["roster"].items()}
        w._seq, w._prev = row["seq"], row["sha"]
        w.rows.append(row)
        return  # the adopted row IS the logged row, byte-identical
    else:
        raise ValueError(f"seq {row.get('seq')}: unknown row kind {kind!r}")
    if w.rows[-1] != row:
        raise ValueError(
            f"seq {row['seq']}: replay diverges from the logged row "
            f"(determinism broken or the log was edited)")


def restore_world(world: MountainWorld, path: Path | str) -> dict[str, Any]:
    """Replay-on-boot: rebuild `world` (already constructed, log already
    wired by MountainWorld.__init__) from the save doc at `path`.

    Steps: verify the doc's tail chain; anchor on its first kind:snapshot
    row; replay every later row on a scratch world asserting byte-identity;
    check the doc's own anchors (volumes/tick at save time); replay any
    JSONL rows the disk chain gained past the doc (crash window); then
    transplant graph + roster + scores + winner into the booting world.
    """
    p = Path(path)
    doc = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
        raise ValueError(f"{p}: not a {SCHEMA} save doc")
    rows = doc.get("rows")
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{p}: save doc carries no rows")
    verify_tail(rows)
    anchor_i = next((i for i, r in enumerate(rows)
                     if isinstance(r, dict) and r.get("kind") == "snapshot"), None)
    if anchor_i is None:
        raise ValueError(f"{p}: tail has no kind:snapshot row to anchor replay")
    anchor = rows[anchor_i]
    for key in ("spec", "winner", "scores", "roster"):
        if key not in anchor:
            raise ValueError(f"{p}: anchor snapshot row lacks {key!r}")

    w = MountainWorld()  # scratch replay board; no log of its own
    _apply_graph_spec(w.graph, anchor["spec"])
    w.winner = bool(anchor["winner"])
    w.scores = {str(u): int(s) for u, s in anchor["scores"].items()}
    w.roster = {str(sid): dict(info) for sid, info in anchor["roster"].items()}
    w._seq, w._prev, w.rows = anchor["seq"], anchor["sha"], [anchor]
    tick_events: list[str] = []
    for row in rows[anchor_i + 1:]:
        _replay_row(w, row, tick_events)

    # the doc's own truth anchors: replaying its tail must land exactly on
    # the state the doc claims it saved
    if doc.get("volumes") != w.node_volumes():
        raise ValueError(
            f"{p}: replayed volumes {w.node_volumes()} disagree with the "
            f"doc's volumes anchor {doc.get('volumes')}")
    if doc.get("tick") != w.graph.tick_count:
        raise ValueError(
            f"{p}: replayed tick {w.graph.tick_count} disagrees with the "
            f"doc's tick anchor {doc.get('tick')}")

    # crash window: rows the on-disk chain gained after the doc was written
    extra: list[dict[str, Any]] = []
    if world.rows:
        tip = w.rows[-1]
        idx = next((i for i, r in enumerate(world.rows)
                    if r["seq"] == tip["seq"]), None)
        if idx is None or world.rows[idx]["sha"] != tip["sha"]:
            raise ValueError(
                f"{p}: save tail tip (seq {tip['seq']}) does not line up "
                f"with the event log loaded from disk")
        extra = world.rows[idx + 1:]
    for row in extra:
        _replay_row(w, row, tick_events)

    # transplant: state from the replay, chain position from the boot world
    world.graph = w.graph
    world.roster = {sid: dict(info) for sid, info in w.roster.items()}
    world.scores = dict(w.scores)
    world.winner = w.winner
    world.pending = []
    if not world.rows:  # booted without a log file: adopt the whole doc
        world.rows = list(rows)  # tail (replay covered only post-anchor)
        world._seq, world._prev = rows[-1]["seq"], rows[-1]["sha"]
    return {"restored": True, "anchor_seq": anchor["seq"],
            "rows_replayed": (len(rows) - anchor_i - 1) + len(extra),
            "seq": w._seq, "tick": w.graph.tick_count,
            "volumes": w.node_volumes()}


def load(path: Path | str) -> MountainWorld:
    """Rebuild a fresh world from a save doc by pure replay (no log file,
    no live server): the mission's load(path) shape."""
    w = MountainWorld()
    restore_world(w, path)
    return w
