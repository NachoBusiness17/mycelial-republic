"""mountain_reveal — DFHack reveal/prospect for the Mountain (LM2, 2026-09-30).

DFHack's `reveal` shows the hidden map; ours shows world truth. The
Mountain (server/world.py's board over mag/water_graph physics) runs in
the dark: clients see their pool, the operator the dashboard, nothing
dumps the WHOLE world from the live board or a replay log. This is that
overlay:

  reveal    full dump: nodes (type/elev/volume/stress/steam), pipes
            (from/to/cap/flow/stress/fractured), junction gates,
            waste/boil state. `flow` is the read-only projection of what
            the pipe carries THIS tick (no mutation, no priming effects).
  prospect  stats: total water + drift vs the board endowment, per-node
            distribution, fracture-risk ranking (stress over the
            200+hash%201 threshold [200, 400] volume units — B1 2026-09-30,
            full-bore ticks to burst), boil
            capacity (steam condenses at the highest cold node).
  events N  last N world events with tick numbers (+ chain seq).

Sources: DEFAULT is the offline board (MountainWorld, no server, no
log; --ticks N runs the physics forward first). --from-replay FILE loads
a chained JSONL: chain verified first (tamper = exit 2), then REPLAYED
through the world's own machinery (persistence._replay_row,
byte-equality). Divergence means the log predates current physics (e.g.
pre-V5 logs whose waste deleted water) — degrade honestly to PARTIAL:
volumes from the last tick row, pipe load/steam unknown, exit 0 + banner.

Node `stress` (the engine loads PIPES, not nodes) is the sum of stress
on the node's incident pipes — derived, labeled, never invented.
Exit codes: 0 ok · 2 corrupt/tampered chain. $0, stdlib, read-only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag.water_graph import WaterGraph, fracture_threshold  # noqa: E402
from server.persistence import (  # noqa: E402
    _apply_graph_spec,
    _replay_row,
    verify_tail,
)
from server.world import MountainWorld, verify_log_rows  # noqa: E402

GATED = ("xor", "sill")


class CorruptLog(Exception):
    """Chain verification failed: hard exit 2 (tamper-evident refusal)."""


# ------------------------------------------------------------- sources ----
def open_offline(ticks: int) -> MountainWorld:
    """The default board offline; --ticks N runs the physics forward first."""
    w = MountainWorld()
    for _ in range(ticks):
        w.tick()
    return w


def _read_rows(path: Path | str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    if not rows:
        raise CorruptLog(f"{path}: replay log is empty")
    return rows


def _verify_chain(path: Path, rows: list[dict[str, Any]]) -> None:
    """Tamper check BEFORE any replay (full logs end-to-end, tails internally)."""
    if rows[0].get("seq") == 1:
        if not verify_log_rows(rows):
            raise CorruptLog(f"{path}: event log chain is corrupt (seq/prev/sha)")
    else:
        try:
            verify_tail(rows)
        except ValueError as e:
            raise CorruptLog(f"{path}: {e}")


def _anchor_replay(rows: list[dict[str, Any]]) -> tuple[MountainWorld, int] | None:
    """Anchor on the LAST kind:snapshot row when it carries the full spec
    (persistence's save shape); None -> replay from genesis."""
    idx = max((i for i, r in enumerate(rows) if r.get("kind") == "snapshot"),
              default=None)
    if idx is None:
        return None
    anchor = rows[idx]
    if any(k not in anchor for k in ("spec", "winner", "scores", "roster")):
        return None
    w = MountainWorld()
    _apply_graph_spec(w.graph, anchor["spec"])
    # LM2 (cause: _apply_graph_spec restores only open/primed, dropping the
    # spec's stress/fractured, so an anchored replay with accrued load
    # byte-diverged at the next snapshot — the gap reddening
    # tests/test_server_persist.py at HEAD. Evidence: save_interval=1 logs
    # diverge without this, replay clean with it). Spec carries them (LW5).
    for name, sp in anchor["spec"].get("pipes", {}).items():
        if name in w.graph.pipes:
            w.graph.pipes[name].stress = int(sp.get("stress", 0))
            w.graph.pipes[name].fractured = bool(sp.get("fractured", False))
    w.winner = bool(anchor["winner"])
    w.scores = {str(u): int(s) for u, s in anchor["scores"].items()}
    w.roster = {str(sid): dict(info) for sid, info in anchor["roster"].items()}
    w._seq, w._prev, w.rows = anchor["seq"], anchor["sha"], [anchor]
    return w, idx + 1


def open_replay(path: Path | str) -> tuple[MountainWorld, list[dict[str, Any]], str]:
    """-> (world, rows, mode). replay = re-derived byte-exact; partial =
    volumes from the last tick row (physics drift or unanchored tail)."""
    rows = _read_rows(path)
    _verify_chain(Path(path), rows)
    anchored = rows[0].get("seq") == 1
    start: int
    got = _anchor_replay(rows)               # snapshot anchor, tail or full
    if got is not None:
        world, start = got
    elif anchored:                           # full history: replay from genesis
        world, start = MountainWorld(), 0
    else:
        world = None
    if world is not None:
        tick_events: list[str] = []
        try:
            for row in rows[start:]:
                _replay_row(world, row, tick_events)
            return world, rows, "replay"
        except ValueError as e:
            print(f"PHYSICS DRIFT ({path}): {e}; log predates current "
                  "engine — PARTIAL fallback (volumes from last tick row; "
                  "pipe load/steam unknown).", file=sys.stderr)
    world = MountainWorld()
    last_tick = next((r for r in reversed(rows)
                      if r.get("kind") == "tick" and "nodes" in r), None)
    if last_tick is None:
        raise CorruptLog(f"{path}: no tick row to read volumes from")
    for name, vol in last_tick["nodes"].items():
        if name in world.graph.nodes:
            world.graph.nodes[name].volume = int(vol)
    world.graph.tick_count = int(last_tick.get("tick", 0))
    if not anchored:
        print(f"PARTIAL ({path}): tail without a snapshot anchor "
              "(seq starts mid-history); volumes from last tick row.",
              file=sys.stderr)
    return world, rows, "partial"


# --------------------------------------------------------- projections ----
def projected_flow(g: WaterGraph, p: Any) -> int:
    """What THIS pipe carries this tick, read-only (the availability law:
    closed/fractured/no-head/no-water -> 0; siphon primed or primable;
    else min(cap, src.volume)). Gated-junction outflow also needs its
    gate verdict — flagged via waits_gate, never guessed here."""
    if p.fractured or not p.open or g.nodes[p.src].volume <= 0:
        return 0
    src, dst = g.nodes[p.src], g.nodes[p.dst]
    head_ok = src.elev > dst.elev
    if p.siphon and not p.primed:
        if src.volume < p.crest or not head_ok:
            return 0
    elif not head_ok:
        return 0
    return min(p.cap, src.volume)


def node_stress(g: WaterGraph, name: str) -> int:
    """Sum of stress on the node's incident pipes (in + out). The engine
    loads pipes, not nodes; this is the derived wall-load reading."""
    return sum(p.stress for p in g.pipes.values()
               if p.src == name or p.dst == name)


def pipe_state(g: WaterGraph, p: Any) -> str:
    if p.fractured:
        return "burst"
    if not p.open:
        return "siphon-shut" if p.siphon else "shut"
    if p.siphon:
        return "siphon-primed" if p.primed else "siphon-unprimed"
    return "open"


def gate_reading(g: WaterGraph, node: Any) -> dict[str, Any]:
    """A junction's gate: rule, inlet states, projected pass/hold verdict."""
    inlets = [p for p in g.pipes.values() if p.dst == node.name]
    live = [p.name for p in inlets if projected_flow(g, p) > 0]
    need = 1 if node.kind == "xor" else max(1, node.sill)
    passes = (len(live) == need) if node.kind == "xor" else (len(live) >= need)
    rule = ("xor: exactly 1 delivering inlet" if node.kind == "xor"
            else f"sill: >= {need} delivering inlets")
    return {"node": node.name, "rule": rule, "need": need,
            "inlets": [{"pipe": p.name, "state": pipe_state(g, p),
                        "flow": projected_flow(g, p)} for p in inlets],
            "live_inlets": len(live), "verdict": "PASS" if passes else "HOLD"}


# ----------------------------------------------------------- payloads ----
def reveal_payload(w: MountainWorld, source: str, mode: str) -> dict[str, Any]:
    g = w.graph
    nodes = {n.name: {"type": n.kind, "elev": n.elev, "volume": n.volume,
                      "steam": n.steam, "stress": node_stress(g, n.name)}
             for n in g.nodes.values()}
    pipes = {p.name: {"from": p.src, "to": p.dst, "cap": p.cap,
                      "flow": projected_flow(g, p), "stress": p.stress,
                      "threshold": fracture_threshold(p.name),
                      "fractured": p.fractured, "state": pipe_state(g, p),
                      "waits_gate": g.nodes[p.src].kind in GATED}
             for p in g.pipes.values()}
    junctions = [gate_reading(g, n) for n in g.nodes.values()
                 if n.kind in GATED]
    colds = [n for n in g.nodes.values() if n.kind == "cold"]
    wastes = [n for n in g.nodes.values() if n.kind == "waste"]
    condense = (max(colds, key=lambda n: n.elev).name if colds else None)
    return {
        "source": source, "mode": mode, "tick": g.tick_count,
        "winner": w.winner, "win_crown": MountainWorld.WIN_CROWN,
        "crown_volume": g.nodes["crown"].volume if "crown" in g.nodes else None,
        "nodes": nodes, "pipes": pipes, "junctions": junctions,
        "waste_boil": {
            "waste_basins": {n.name: n.volume for n in wastes},
            "waste_held": sum(n.volume for n in wastes),
            "steam_in_flight": sum(n.steam for n in g.nodes.values()),
            "condenses_at": condense,
            "boilable_liquid": sum(n.volume for n in g.nodes.values()),
        },
    }


def prospect_payload(w: MountainWorld, source: str, mode: str) -> dict[str, Any]:
    g = w.graph
    liquid = sum(n.volume for n in g.nodes.values())
    steam = sum(n.steam for n in g.nodes.values())
    total = liquid + steam
    endow = sum(n.volume for n in MountainWorld().graph.nodes.values())
    dist = sorted(({"node": n.name, "volume": n.volume, "steam": n.steam,
                    "share_pct": round(100.0 * (n.volume + n.steam) / total, 1)
                    if total else 0.0}
                   for n in g.nodes.values()),
                  key=lambda d: -(d["volume"] + d["steam"]))
    risk = []
    for p in g.pipes.values():
        thr = fracture_threshold(p.name)
        ratio = round(p.stress / thr, 4)
        to_burst = None
        if not p.fractured and p.cap > 0 and p.stress < thr:
            to_burst = -(-(thr - p.stress) // p.cap)  # ceil, full-bore ticks
        risk.append({"pipe": p.name, "stress": p.stress, "threshold": thr,
                     "ratio": ratio, "fractured": p.fractured,
                     "full_bore_ticks_to_burst": to_burst})
    risk.sort(key=lambda r: (-r["ratio"], r["pipe"]))
    colds = [n for n in g.nodes.values() if n.kind == "cold"]
    return {
        "source": source, "mode": mode, "tick": g.tick_count,
        "total_water": total, "liquid": liquid, "steam": steam,
        "board_endowment": endow, "drift": total - endow,
        "distribution": dist,
        "fracture_risk": risk,
        "boil_capacity": {
            "boilable_liquid": liquid,
            "condenses_at": (max(colds, key=lambda n: n.elev).name
                             if colds else None),
            "waste_recoverable": sum(n.volume for n in g.nodes.values()
                                     if n.kind == "waste"),
        },
    }


def flatten_events(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """World events in order (tick rows unfold; actions carry their line)."""
    out: list[dict[str, Any]] = []
    for r in rows:
        if r.get("kind") == "tick":
            for ev in r.get("events", []):
                out.append({"seq": r.get("seq"), "tick": r.get("tick"),
                            "event": ev})
        elif r.get("kind") in ("action", "whisper"):
            out.append({"seq": r.get("seq"), "tick": r.get("tick"),
                        "event": r.get("event", "")})
    return out


# --------------------------------------------------------- renderers ----
def render_reveal(p: dict[str, Any]) -> list[str]:
    out = ["=== MOUNTAIN REVEAL ===",
           f"source: {p['source']}  mode: {p['mode']}  tick: {p['tick']}  "
           f"winner: {'YES' if p['winner'] else 'no'} "
           f"(crown {p['crown_volume']}/{p['win_crown']})",
           f"nodes ({len(p['nodes'])}):  (*stress = incident pipe load)"]
    for name, n in p["nodes"].items():
        out.append(f"  {name:<8} {n['type']:<5} elev={n['elev']:<3} "
                   f"vol={n['volume']:<3} steam={n['steam']:<3} "
                   f"stress={n['stress']}")
    out.append(f"pipes ({len(p['pipes'])}):  * outflow waits on its junction gate")
    for name, q in p["pipes"].items():
        flag = "*" if q["waits_gate"] else " "
        burst = " FRACTURED" if q["fractured"] else ""
        out.append(f"  {name:<10} {q['from']}->{q['to']:<7} cap={q['cap']} "
                   f"flow={q['flow']} stress={q['stress']}/{q['threshold']}"
                   f"{burst} {q['state']}{flag}")
    for j in p["junctions"]:
        ins = ", ".join(f"{i['pipe']}({i['state']}, flow {i['flow']})"
                        for i in j["inlets"])
        out.append(f"junction {j['node']}: {j['rule']}  [{ins}]  "
                   f"gate-now: {j['verdict']} ({j['live_inlets']} live)")
    wb = p["waste_boil"]
    out.append(f"waste: {wb['waste_held']} held at "
               f"{wb['waste_basins'] or {}} (boil it to recover)")
    out.append(f"boil: {wb['boilable_liquid']} liquid boilable · "
               f"{wb['steam_in_flight']} steam in flight · "
               f"condenses at {wb['condenses_at']}")
    return out


def render_prospect(p: dict[str, Any]) -> list[str]:
    out = ["=== MOUNTAIN PROSPECT ===",
           f"source: {p['source']}  mode: {p['mode']}  tick: {p['tick']}",
           f"water: {p['total_water']} total "
           f"({p['liquid']} liquid + {p['steam']} steam) · "
           f"endowment {p['board_endowment']} · drift {p['drift']}",
           "distribution:"]
    for d in p["distribution"]:
        out.append(f"  {d['node']:<8} vol={d['volume']:<3} steam={d['steam']:<3} "
                   f"{d['share_pct']}%")
    out.append("fracture risk (stress/threshold):")
    for r in p["fracture_risk"]:
        tail = ("FRACTURED" if r["fractured"] else
                f"~{r['full_bore_ticks_to_burst']} full-bore ticks to burst"
                if r["full_bore_ticks_to_burst"] is not None else "at threshold")
        out.append(f"  {r['pipe']:<10} {r['stress']}/{r['threshold']} "
                   f"({r['ratio'] * 100:.1f}%)  {tail}")
    b = p["boil_capacity"]
    out.append(f"boil capacity: {b['boilable_liquid']} units · condenses at "
               f"{b['condenses_at']} · waste recoverable: {b['waste_recoverable']}")
    return out


def render_events(evs: list[dict[str, Any]], n: int) -> list[str]:
    out = [f"=== MOUNTAIN EVENTS (last {min(n, len(evs))} of {len(evs)}) ==="]
    for e in evs[-n:]:
        out.append(f"  tick {e['tick']:>4}  seq {e['seq']:>4}  {e['event']}")
    return out


# ------------------------------------------------------------------- cli --
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="mountain_reveal: DFHack-style overlay for the Mountain "
                    "(reveal / prospect / events N).")
    ap.add_argument("command", choices=("reveal", "prospect", "events"))
    ap.add_argument("n", nargs="?", type=int, default=10,
                    help="events: last N (default 10)")
    ap.add_argument("--from-replay", metavar="FILE",
                    help="read a chained world JSONL instead of the board")
    ap.add_argument("--ticks", type=int, default=0,
                    help="offline only: run the physics N ticks first")
    ap.add_argument("--json", action="store_true", help="machine output")
    args = ap.parse_args(argv)
    if args.from_replay and args.ticks:
        ap.error("--ticks is offline-only (a replay carries its own history)")
    if args.n < 1:
        ap.error("n must be >= 1")
    if args.from_replay:
        try:
            world, rows, mode = open_replay(args.from_replay)
        except CorruptLog as e:
            print(str(e), file=sys.stderr)
            raise SystemExit(2)
        source = f"replay {args.from_replay}"
    else:
        world, rows, mode = open_offline(args.ticks), None, "offline"
        source = "default board (offline, no server)"
    if args.command == "reveal":
        payload, render = reveal_payload(world, source, mode), render_reveal
    elif args.command == "prospect":
        payload, render = prospect_payload(world, source, mode), render_prospect
    else:
        evs = flatten_events(rows if rows is not None else world.rows)
        if args.json:
            print(json.dumps({"events": evs[-args.n:]}, sort_keys=True))
        else:
            for line in render_events(evs, args.n):
                print(line)
        return 0
    if args.json:
        print(json.dumps(payload, sort_keys=True))
    else:
        for line in render(payload):
            print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
