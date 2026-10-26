"""mountain_legends — Legends Mode for the Mountain (LM5, 2026-09-30).

Dwarf Fortress renders world history as a browsable chronicle; this tool
renders the Mountain's hash-chained event log (server/world.py JSONL:
append-only rows, sha256 over the row minus its own sha, genesis prev =
64 zeros, seq strictly increments) as a markdown chronicle:

  epochs      phase transitions of the water economy: first boil, first
              fracture, first crown fill, first siphon prime/break, first
              XOR resolution, WIN, the spring failing, the Still World
  notables    fractures (with stress counts), siphon breaks, starvations,
              firsts — the events a dwarf would tell stories about
  sagas       per-node journeys; the COLD crown's rise gets its own verse
  timeline    ASCII: per-node volume histogram + epoch markers per tick
  stats       rows by kind, events by type, the water ledger

The chain is verified WHILE rendering: a forged row is named (seq + why)
and the chronicle is stamped untrusted (exit 2, the gate convention).
Legends mode that detects rewritten history is the closed-corpus law in
game form: trust bytes, not reports.

Usage:
    .venv/Scripts/python.exe tools/mountain_legends.py replay logs/world_server.jsonl
    .venv/Scripts/python.exe tools/mountain_legends.py run --ticks 500
    .venv/Scripts/python.exe tools/mountain_legends.py run --ticks 500 --actors demo
        (--actors demo registers Urist the waste-boiler + Oddam the
        gate-disputer on a fixed, deterministic script so the boil/crown
        epochs can fire; --log PATH also persists the fresh chain)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.world import GENESIS, MountainWorld, row_sha  # noqa: E402

# The board the log came from (server/world.py build_mountain_graph); used
# only to annotate sagas, and only for node names the log actually carries.
BOARD_ANNOTATIONS = {
    "spring": "the source, elev 10", "terrace": "elev 6",
    "gate1": "the XOR gate, elev 5", "hollow": "elev 3",
    "waste": "the drain basin, elev 0", "crown": "the COLD crown, elev 14",
}

EVENT_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("fracture", re.compile(r"^Pipe (\S+) FRACTURES \(stress (\d+)\): spray to (\S+)\.$")),
    ("siphon_prime", re.compile(r"^Siphon (\S+) primes at crest \((\d+)\)\.$")),
    ("siphon_break", re.compile(r"^Siphon (\S+) breaks \(intake dry\)\.$")),
    ("xor_pass", re.compile(r"^Junction (\S+) passes \((\S+) sole inlet\)\.$")),
    ("sill_pass", re.compile(r"^Junction (\S+) sill reached \((\d+) inlets\)\.$")),
    ("gate_hold", re.compile(r"^Junction (\S+) holds (\d+) below gate")),
    ("starved", re.compile(r"^Junction (\S+) STARVED")),
    ("condense", re.compile(r"^Steam condenses at (\S+) \(\+(\d+)\)\.$")),
    ("to_waste", re.compile(r"^(\S+): (\d+) to waste at (\S+)\.$")),
    ("flow", re.compile(r"^(\S+): (\d+) (\S+)->(\S+)\.$")),
    # action echoes ride INSIDE tick event lists (world._apply returns them);
    # last so the pipe grammar above wins on its own strings
    ("verb:valve", re.compile(r"^(\S+) (opens|shuts) (\S+)\.$")),
    ("verb:boil", re.compile(r"^(\S+) boils .* at (\S+)")),
    ("verb:join", re.compile(r"^(\S+) joins at (\S+)\.$")),
    ("verb:tag", re.compile(r"^(\S+) tags a fish at")),
    ("verb:say", re.compile(r"^(\S+): (.+)$")),
]

# epoch marker letters on the timeline
MARKERS = {"first_boil": "B", "first_fracture": "F", "siphon_prime": "P",
           "siphon_break": "S", "crown_fill": "C", "win": "W",
           "first_xor": "X", "spring_dry": "D", "still_world": "Q",
           "condense": "R", "starved": "V"}


def classify(ev: str) -> tuple[str, re.Match | None]:
    for etype, rx in EVENT_PATTERNS:
        m = rx.match(ev)
        if m:
            return etype, m
    return "other", None


def chain_verdict(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Verify while rendering; name the first forged row and the why."""
    prev, expect = GENESIS, 1
    for row in rows:
        if row.get("seq") != expect:
            return {"ok": False, "seq": row.get("seq"),
                    "why": f"seq {row.get('seq')!r} appears where {expect} is due"}
        if row.get("prev") != prev:
            return {"ok": False, "seq": row["seq"],
                    "why": "prev link mismatch: row is not sealed on its parent"}
        if row.get("sha") != row_sha(row):
            return {"ok": False, "seq": row["seq"],
                    "why": "sha mismatch: body does not hash to its seal "
                           "(row edited after sealing)"}
        prev, expect = row["sha"], expect + 1
    return {"ok": True, "tip": rows[-1]["sha"] if rows else GENESIS}


def load_rows(path: Path) -> tuple[list[dict[str, Any]], str | None]:
    rows: list[dict[str, Any]] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            return rows, f"line {i} is not JSON ({exc.msg}) — history breaks mid-file"
    return rows, None


def drive_actors(world: MountainWorld, t: int) -> None:
    """The demo saga, fixed script, zero RNG: Oddam opens the shut siphon
    and says a line; every second tick Urist boils the lowest wet pool so
    steam finds the crown. Deterministic (same script, same history)."""
    if t == 1:
        world.stage("s2", "say", "the mountain must drink.")
        world.stage("s2", "valve", "p_bypass")
    if t == 2:
        world.stage("s1", "whisper", "Oddam|the gate will starve, watch it.")
    if t % 2 == 0:
        for name in ("waste", "hollow", "terrace", "gate1", "spring"):
            if world.graph.nodes[name].volume > 0:
                world.stage("s1", "boil", name)
                return


def fresh_run(ticks: int, actors: str, log_path: Path | None
              ) -> tuple[list[dict[str, Any]], int, str]:
    world = MountainWorld(log_path=log_path)
    initial = sum(n.volume + n.steam for n in world.graph.nodes.values())
    source = f"fresh run on the default mountain board (server/world.py), {ticks} ticks"
    if actors == "demo":
        world.register_session("s1", "Urist", "waste")
        world.register_session("s2", "Oddam", "spring")
        source += ", actors=demo (Urist boils, Oddam disputes the gate)"
    for t in range(1, ticks + 1):
        if actors == "demo":
            drive_actors(world, t)
        world.tick()
    rows = world.rows
    world.close()
    return rows, initial, source


def detect_epochs(ticks: list[dict[str, Any]], actions: list[dict[str, Any]],
                  firsts: dict[str, tuple[int, int, str]]
                  ) -> list[dict[str, Any]]:
    def row_of(tick: int) -> dict[str, Any]:
        return next(t for t in ticks if t["tick"] == tick)

    epochs: list[dict[str, Any]] = []

    def add(code: str, tick: int | None, name: str, ev: str) -> None:
        if tick is None:
            epochs.append({"code": code, "tick": None, "name": name, "note": ev})
        else:
            r = row_of(tick)
            epochs.append({"code": code, "tick": tick, "name": name, "note": ev,
                           "seq": r["seq"], "sha": r["sha"][:12]})

    boil = next((a for a in actions if a["verb"] == "boil" and "boils 1 at" in a["event"]), None)
    add("first_boil", boil["tick"] if boil else None, "The First Boil",
        f"{boil['event']}" if boil else "never: no hand ever lifted steam")
    for code, etype, name in (
            ("first_fracture", "fracture", "The Rupture"),
            ("siphon_prime", "siphon_prime", "The Siphon Wakes"),
            ("siphon_break", "siphon_break", "The Siphon Breaks"),
            ("first_xor", "xor_pass", "The First Verdict"),
            ("condense", "condense", "First Rain"),
            ("starved", "starved", "The Starving")):
        hit = firsts.get(etype)
        add(code, hit[0] if hit else None, name,
            hit[2] if hit else f"never: no {etype} event in this history")
    crown = next((t for t in ticks if t["nodes"].get("crown", 0) > 0), None)
    add("crown_fill", crown["tick"] if crown else None, "The Crown Drinks",
        f"crown holds {crown['nodes']['crown']} at tick {crown['tick']}"
        if crown else "never: the crown stayed dry all age")
    win = next((t for t in ticks if t["winner"]), None)
    add("win", win["tick"] if win else None, "The Crowning",
        f"crown >= 4, winner sticky from tick {win['tick']}"
        if win else "never: the win was never reached")
    dry = next((t for t in ticks if t["nodes"].get("spring", 1) == 0), None)
    add("spring_dry", dry["tick"] if dry else None, "The Spring Fails",
        f"spring volume hits 0 at tick {dry['tick']}" if dry else "the spring never ran dry")
    empties = [i for i, t in enumerate(ticks) if not t["events"]]
    still = None
    if empties and empties[-1] == len(ticks) - 1:
        run_start = len(ticks) - 1
        while run_start in empties:
            run_start -= 1
        still = ticks[run_start + 1]["tick"]
    add("still_world", still, "The Still World",
        f"from tick {still} no pipe moves, no gate speaks: quiescence"
        if still else "the water never came to rest")
    return epochs


def render_timeline(ticks: list[dict[str, Any]], epochs: list[dict[str, Any]],
                    width: int = 96) -> str:
    if not ticks:
        return "    (no ticks to draw)"
    total = len(ticks)
    per = max(1, -(-total // width))
    cols = -(-total // per)
    names = list(ticks[0]["nodes"])
    lines = ["    " + "".join(
        "+" if c % 10 == 0 else ("|" if c == cols - 1 else "-") for c in range(cols))]
    lab = [" "] * (cols + 12)
    for c in range(0, cols, 10):
        label = str(c * per + 1)
        if c + len(label) <= cols:            # never run past the right edge
            for j, ch in enumerate(label):
                lab[c + j] = ch
    lines.append("tick" + "".join(lab[:cols]).rstrip())
    for name in names:
        chars = []
        for c in range(cols):
            bucket = [t["nodes"][name] for t in ticks[c * per:(c + 1) * per]]
            chars.append(str(min(9, max(bucket))) if bucket else " ")
        lines.append(f"{name:<9}" + "".join(chars))
    tot = []
    for c in range(cols):
        bucket = [sum(t["nodes"].values()) for t in ticks[c * per:(c + 1) * per]]
        tot.append(str(min(9, max(bucket))) if bucket else " ")
    lines.append(f"{'SUM':<9}" + "".join(tot))
    marks = [" "] * cols
    for ep in epochs:
        if ep["tick"] is not None:
            col = (ep["tick"] - 1) // per
            while col < cols and marks[col] != " ":   # drift right on collision
                col += 1
            if col < cols:
                marks[col] = MARKERS.get(ep["code"], "?")
    lines.append("epochs   " + "".join(marks).rstrip())
    return "\n".join(lines)


def build_chronicle(rows: list[dict[str, Any]], source: str,
                    initial_total: int | None) -> dict[str, Any]:
    ticks = [{"tick": r["tick"], "nodes": r["nodes"], "events": r["events"],
              "winner": r["winner"], "seq": r["seq"], "sha": r["sha"]}
             for r in rows if r.get("kind") == "tick"]
    actions = [r for r in rows if r.get("kind") == "action"]
    whispers = [r for r in rows if r.get("kind") == "whisper"]
    ev_counts: Counter[str] = Counter()
    firsts: dict[str, tuple[int, int, str]] = {}
    for t in ticks:
        for ev in t["events"]:
            etype, _ = classify(ev)
            ev_counts[etype] += 1
            firsts.setdefault(etype, (t["tick"], t["seq"], ev))
    # actions are counted via their echoes in tick events; whispers never
    # land in a tick (they live outside the canonical tick), so count rows
    for w in whispers:
        ev_counts["verb:whisper"] += 1
    epochs = detect_epochs(ticks, actions, firsts)
    sums = [sum(t["nodes"].values()) for t in ticks]
    ledger = {"initial": initial_total,
              "first_row": sums[0] if sums else None,
              "final": sums[-1] if sums else None,
              "min": min(sums) if sums else None,
              "max": max(sums) if sums else None}
    return {"source": source, "rows": rows, "ticks": ticks, "actions": actions,
            "whispers": whispers, "ev_counts": ev_counts, "firsts": firsts,
            "epochs": epochs, "ledger": ledger}


def render(c: dict[str, Any], verdict: dict[str, Any]) -> str:
    out: list[str] = []
    tip = verdict.get("tip", "")
    if verdict["ok"]:
        out.append(f"# The Chronicle of the Mountain — {c['source']}")
        out.append(f"\n**CHAIN VERIFIED** over {len(c['rows'])} rows "
                   f"(seq 1..{len(c['rows'])}, tip sha `{tip[:12]}`). "
                   "Every row seals its parent; this history is byte-true.\n")
    else:
        out.append(f"# The Chronicle of the Mountain — {c['source']}")
        out.append(f"\n**FORGED HISTORY DETECTED** at seq {verdict['seq']}: "
                   f"{verdict['why']}. The chronicle below the forge line is "
                   "UNTRUSTED; the closed-corpus law refuses it.\n")
    out.append("## Epochs\n")
    out.append("| marker | tick | age | what happened | row |")
    out.append("|---|---|---|---|---|")
    for ep in c["epochs"]:
        mark = MARKERS.get(ep["code"], "?")
        tick = str(ep["tick"]) if ep["tick"] is not None else "-"
        row = f"{ep['seq']} / `{ep['sha']}`" if ep.get("seq") else "-"
        out.append(f"| {mark} | {tick} | {ep['name']} | {ep['note']} | {row} |")
    out.append("\n## The Timeline (digits = units of water, max per band)\n")
    out.append("```")
    out.append(render_timeline(c["ticks"], c["epochs"]))
    out.append("```")
    out.append("\n## Notable events\n")
    notables: list[tuple[int, str, str]] = []
    for t in c["ticks"]:
        for ev in t["events"]:
            etype, m = classify(ev)
            if etype in ("fracture", "siphon_break", "starved"):
                notables.append((t["tick"], etype, ev))
            elif etype in ("siphon_prime", "condense", "xor_pass") and \
                    c["firsts"].get(etype, (None,))[0] == t["tick"]:
                notables.append((t["tick"], "first " + etype, ev))
    for a in c["actions"]:
        if a["verb"] in ("boil", "valve", "say") and \
                not any(n[2] == a["event"] for n in notables):
            if a["verb"] == "say" or "boils 1" in a["event"] or \
                    len([x for x in c["actions"] if x["verb"] == a["verb"]]) <= 8:
                notables.append((a["tick"], "verb " + a["verb"], a["event"]))
    for w in c["whispers"]:
        notables.append((w["tick"], "whisper", w["event"]))
    for tick, etype, ev in notables[:32]:
        out.append(f"- tick {tick} [{etype}] {ev}")
    if len(notables) > 32:
        out.append(f"- ... and {len(notables) - 32} more (see stats)")
    out.append("\n## Sagas of the nodes\n")
    for name in (c["ticks"][0]["nodes"] if c["ticks"] else {}):
        vols = [t["nodes"][name] for t in c["ticks"]]
        first_wet = next((t["tick"] for t, v in zip(c["ticks"], vols) if v > 0), None)
        peak = max(vols) if vols else 0
        peak_tick = next((t["tick"] for t, v in zip(c["ticks"], vols) if v == peak), None) if peak else None
        gains = sum(max(0, b - a) for a, b in zip(vols, vols[1:]))
        ann = BOARD_ANNOTATIONS.get(name, "")
        head = f"### {name}" + (f" ({ann})" if ann else "")
        if name == "crown":
            head += " — the COLD crown's journey"
        out.append(head)
        wet = f"first water tick {first_wet}" if first_wet else "dry the whole age (no water ever arrived)"
        peak_s = f"peak {peak}" + (f" at tick {peak_tick}" if peak else "")
        out.append(f"- {wet}; {peak_s}; final {vols[-1] if vols else 0}; "
                   f"gained {gains} over the age")
        if name == "crown":
            win = next((t["tick"] for t in c["ticks"] if t["winner"]), None)
            out.append(f"- the crown drinks steam and keeps it: no outlet, "
                       f"so every gain is forever. "
                       + (f"CROWNED at tick {win} (crown >= 4)." if win
                          else "never crowned."))
    l = c["ledger"]
    out.append("\n## Stats\n")
    kinds = Counter(r.get("kind", "?") for r in c["rows"])
    out.append(f"- rows: {len(c['rows'])} total — " +
               ", ".join(f"{v} {k}" for k, v in sorted(kinds.items())))
    out.append(f"- ticks chronicled: {len(c['ticks'])}"
               + (f" (tick {c['ticks'][0]['tick']}..{c['ticks'][-1]['tick']})"
                  if c["ticks"] else ""))
    evs = ", ".join(f"{v} {k}" for k, v in sorted(c["ev_counts"].items()))
    out.append(f"- events by type: {evs or 'none'}")
    if l["initial"] is not None:
        out.append(f"- water ledger: {l['initial']} units at genesis; "
                   f"final row-sum {l['final']} (deletions are theft; "
                   f"steam in flight is invisible to row sums)")
    else:
        out.append(f"- water ledger (from rows only): first-row sum {l['first_row']}, "
                   f"final {l['final']}, min {l['min']}, max {l['max']} — a falling "
                   "sum with `to waste` events names the pre-V5 deletion law; "
                   "rises ride condensation")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Legends Mode for the Mountain")
    sub = ap.add_subparsers(dest="mode", required=True)
    rp = sub.add_parser("replay", help="chronicle a hash-chained JSONL replay")
    rp.add_argument("path", type=Path)
    rn = sub.add_parser("run", help="chronicle a fresh N-tick run")
    rn.add_argument("--ticks", type=int, default=500)
    rn.add_argument("--actors", choices=("none", "demo"), default="none")
    rn.add_argument("--log", type=Path, default=None,
                    help="persist the fresh chain here (append-only; an "
                         "existing file is continued, never truncated)")
    args = ap.parse_args(argv)
    if args.mode == "replay":
        rows, broken = load_rows(args.path)
        source = f"replay of {args.path}"
        initial = None
    else:
        rows, initial, source = fresh_run(args.ticks, args.actors, args.log)
        broken = None
    if broken:
        print(f"# The Chronicle of the Mountain — {source}\n\n"
              f"**FORGED HISTORY DETECTED**: {broken}.\n", file=sys.stderr)
        return 2
    verdict = chain_verdict(rows)
    chronicle = build_chronicle(rows, source, initial)
    print(render(chronicle, verdict))
    return 0 if verdict["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
