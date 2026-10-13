"""mountain_digflood — the DFHack moment: dig the breach, watch the flood.

LM6 (2026-09-30, operator: "the classic DF moment - breaching a wall and
watching water flood real terrain"). The estate owns the physics:
mag/field_flow.py (rung 2 sheet flow) + mag/river.py (W7 rung 4: silt,
sill erosion, deposition, the delta). The terrain is on disk:
logs/terrain/N46W122_board.json, the 64x64 St Helens DEM board
(tools/dem_to_board.py X7) that roblox_to_godot/scripts/terrain_loader.gd
renders in the Godot slice. This tool is the OPERATOR'S HAND over that
board, four verbs, no magic:

  load <board.json>   water_graph.v1 board -> River (g{y}x{x} grammar,
                      kind "waste" = the sea), mantle land cells with
                      --mantle silt (erosion needs loose material), keep
                      the pristine elev grid as baseline, write state
                      (digflood.v1 = header + river.v1).
  dig <x> <y>         the breach: lower ONE cell by K units (--depth);
                      the spoil law lands those K as loose silt (the
                      channel floor is debris, the flood carries it).
                      Logged in state. Refuses waste/out-of-bounds.
  pour <x> <y>        add N units/tick (--rate) for T ticks (--ticks)
                      and run the river engine: water finds the dug
                      channel, incises it, silts the slow reaches,
                      grows the delta at the waste.
  flood-report        after T ticks: wetted cells, the max flow path
                      (thalweg: strictly-lowest-head walk over the
                      CARVED bed from the last pour source), erosion /
                      deposition / washed totals, delta growth (silt
                      parked + bed raised at waste vs baseline), the
                      ASCII trace, and the conservation audit (silt
                      never created or destroyed; every carved elev-unit
                      landed or washed out — plus the hand-dug term).

Determinism: integers only, no floats, no RNG, no clocks; state JSON in
fixed order — same commands, byte-identical state (test-pinned). $0,
stdlib. CLI coords are <x> <y> = column, row (g{y}x{x}); outputs default
to logs/digflood/; no effects beyond files, no switchboard.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:      # script-mode: find mag/ next to tools/
    sys.path.insert(0, str(REPO))

from mag.field_flow import DEFAULT_CONDUCTANCE, DEFAULT_CROSS_SECTION  # noqa: E402
from mag.river import DEFAULT_SILL_FLOW, River, from_spec  # noqa: E402

DIGFLOOD_DIR = REPO / "logs" / "digflood"
DEFAULT_BOARD = REPO / "logs" / "terrain" / "N46W122_board.json"
DEFAULT_MANTEL = 6           # silt units seeded per land cell at load
DEFAULT_DEPTH = 8            # elev units a dig lowers (the breach notch)
DEFAULT_RATE = 24            # water units poured per tick
DEFAULT_TICKS = 300
SCHEMA = "digflood.v1"


# --------------------------------------------------------------- state ----
def load_board_spec(path: str | Path) -> dict[str, Any]:
    """Read a water_graph.v1 board JSON from disk."""
    p = Path(path)
    if not p.is_file():
        raise ValueError(f"board not found: {p}")
    try:
        spec = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"board is not JSON: {p}: {exc}") from exc
    if not isinstance(spec, dict) or not isinstance(spec.get("nodes"), dict) \
            or not spec["nodes"]:
        raise ValueError(f"not a water_graph.v1 board (no nodes): {p}")
    return spec


def build_river(board: dict[str, Any], mantle: int,
                sill_flow: int, cross_section: int,
                conductance: int) -> tuple[River, dict[str, Any]]:
    """Board nodes -> River (the from_board grammar: g{y}x{x} names,
    kind 'waste' outlets, elev/volume fields). Returns (river, header)."""
    from mag.field_flow import _parse_gname  # the board grammar, shared
    nodes: dict[str, Any] = board["nodes"]
    hdr = board.get("dem_board") or {}
    shape = hdr.get("shape")
    coords = [(name, _parse_gname(name)) for name in nodes]
    if shape:
        h, w = int(shape[0]), int(shape[1])
    else:
        h = w = max(max(y, x) for _, (y, x) in coords) + 1
    elev = [[0] * w for _ in range(h)]
    vol = [[0] * w for _ in range(h)]
    waste: set[tuple[int, int]] = set()
    for name, (y, x) in coords:
        if not (0 <= y < h and 0 <= x < w):
            raise ValueError(f"node {name} outside shape {(h, w)}")
        if elev[y][x] or vol[y][x]:
            raise ValueError(f"duplicate node for ({y}, {x})")
        node = nodes[name]
        elev[y][x] = int(node.get("elev", 0))
        vol[y][x] = int(node.get("volume", 0))
        if str(node.get("kind", "plain")) == "waste":
            waste.add((y, x))
    if not waste:
        raise ValueError("board has no waste outlet (kind == 'waste')")
    silt = [[0 if (y, x) in waste else mantle for x in range(w)]
            for y in range(h)]
    river = River(elev, volumes=vol, waste=waste, silt=silt,
                  cross_section=cross_section, conductance=conductance,
                  sill_flow=sill_flow)
    header = {
        "tile_id": str(hdr.get("tile_id", "")),
        "board_hash": str(hdr.get("board_hash", "")),
        "shape": [h, w],
        "waste": sorted([y, x] for y, x in waste),
        "mantle": mantle,
    }
    return river, header


def save_state(state: dict[str, Any], path: str | Path) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, indent=1), encoding="utf-8")


def read_state(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        raise ValueError(f"state not found: {p} (run `load` first)")
    state = json.loads(p.read_text(encoding="utf-8"))
    if state.get("schema") != SCHEMA:
        raise ValueError(f"{p}: schema {state.get('schema')!r} != {SCHEMA!r}")
    return state


def river_from_state(state: dict[str, Any]) -> River:
    """river.v1 spec -> River with the RUN METERS restored (from_spec
    restarts them at zero by design; the CLI needs them cumulative)."""
    river = from_spec(state["river"])
    m = state["river"].get("meters", {})
    river.total_eroded = int(m.get("total_eroded", 0))
    river.total_deposited = int(m.get("total_deposited", 0))
    river.washed_out = int(m.get("washed_out", 0))
    river.drained = int(m.get("drained", 0))
    river.total_moved = int(m.get("total_moved", 0))
    return river


def _cell(x: int, y: int, state: dict[str, Any], what: str) -> tuple[int, int]:
    h, w = state["board"]["shape"]
    if not (0 <= x < w and 0 <= y < h):
        raise ValueError(f"{what} ({x}, {y}) outside the {h}x{w} board (x = column 0..{w - 1}, y = row 0..{h - 1})")
    return y, x


def gname(y: int, x: int) -> str:
    return f"g{y}x{x}"


# --------------------------------------------------------------- verbs ----
def cmd_load(args: argparse.Namespace) -> int:
    board = load_board_spec(args.board)
    river, header = build_river(
        board, args.mantle, args.sill, args.cross_section, args.conductance)
    state = {
        "schema": SCHEMA,
        "board_path": str(Path(args.board)),
        "board": header,
        "params": {"sill_flow": river.sill_flow,
                   "cross_section": river.cross_section,
                   "conductance": river.conductance},
        "baseline_elev": [list(r) for r in river.elev],   # pristine
        "digs": [],
        "pours": [],
        "silt_at_first_pour": None,
        "river": river.to_spec(),
    }
    save_state(state, args.state)
    h, w = header["shape"]
    lo = min(min(r) for r in river.elev)
    hi = max(max(r) for r in river.elev)
    print(f"[load] {header['tile_id'] or Path(args.board).stem} "
          f"{h}x{w} elev {lo}..{hi} waste "
          f"{','.join(gname(y, x) for y, x in header['waste'])}"
          + (f" hash {header['board_hash'][:16]}..." if header["board_hash"] else ""))
    print(f"[load] mantle {args.mantle} silt/cell on "
          f"{h * w - len(header['waste'])} land cells "
          f"(total {river.total_silt()}); state -> {args.state}")
    return 0


def cmd_dig(args: argparse.Namespace) -> int:
    state = read_state(args.state)
    river = river_from_state(state)
    y, x = _cell(args.x, args.y, state, "dig")
    if (y, x) in river.waste:
        raise ValueError(f"{gname(y, x)} is a waste outlet — the sea has no floor to a shovel")
    if args.depth < 1:
        raise ValueError(f"depth must be >= 1, got {args.depth}")
    before = river.elev[y][x]
    river.elev[y][x] -= args.depth          # the breach
    river.silt[y][x] += args.depth          # the spoil law: rock -> rubble
    river._mark_dirty(y, x)                 # noqa: SLF001 — the bed moved
    # spoil added after pouring is hand-placed material: the conservation
    # audit measures the WATER's ledger, so its expected total moves too.
    if state["silt_at_first_pour"] is not None:
        state["silt_at_first_pour"] += args.depth
    state["digs"].append({"x": args.x, "y": args.y, "depth": args.depth,
                          "before": before, "after": river.elev[y][x],
                          "tick": river.tick_count})
    state["river"] = river.to_spec()
    save_state(state, args.state)
    print(f"[dig] {gname(y, x)} elev {before} -> {river.elev[y][x]} "
          f"(-{args.depth}); spoil +{args.depth} silt on the cell; "
          f"{len(state['digs'])} dig(s) logged")
    return 0


def cmd_pour(args: argparse.Namespace) -> int:
    state = read_state(args.state)
    river = river_from_state(state)
    y, x = _cell(args.x, args.y, state, "pour")
    if args.rate < 1 or args.ticks < 1:
        raise ValueError("rate and ticks must be >= 1")
    if state["silt_at_first_pour"] is None:
        state["silt_at_first_pour"] = river.total_silt()
    for _ in range(args.ticks):
        river.add_water(y, x, args.rate)
        river.tick()
    state["pours"].append({"x": args.x, "y": args.y, "rate": args.rate,
                           "ticks": args.ticks, "until_tick": river.tick_count})
    state["river"] = river.to_spec()
    save_state(state, args.state)
    print(f"[pour] {gname(y, x)} +{args.rate}/tick x {args.ticks} ticks "
          f"(tick {river.tick_count}); drained {river.drained}; "
          f"eroded {river.total_eroded}; state -> {args.state}")
    return 0


def thalweg(river: River, y: int, x: int) -> list[tuple[int, int]]:
    """Max flow path: strictly-lowest-head walk over the carved bed (elev
    + standing volume) from (y, x); first-found wins ties. At a WET pit
    the walk crosses the lowest rim — fill-and-spill, the engine's own
    pooling law — so the route reads through lakes; a dry pit or a
    revisit ends it."""
    path = [(y, x)]
    seen = {(y, x)}
    while (y, x) not in river.waste:
        cur = river._head(y, x, river.vol[y][x])     # noqa: SLF001
        lower = rim = None
        for ny, nx in river._neighbors(y, x):        # noqa: SLF001
            if (ny, nx) in seen:
                continue
            h = river._head(ny, nx, river.vol[ny][nx])
            if rim is None or h < rim[0]:
                rim = (h, (ny, nx))
            if h < cur and (lower is None or h < lower[0]):
                lower = (h, (ny, nx))
        step = lower or (rim if river.vol[y][x] > 0 else None)
        if step is None:
            break
        path.append(step[1])
        seen.add(step[1])
        y, x = step[1]
    return path


def cmd_report(args: argparse.Namespace) -> int:
    state = read_state(args.state)
    river = river_from_state(state)
    baseline = state["baseline_elev"]
    h, w = state["board"]["shape"]
    lines: list[str] = []

    def out(s: str = "") -> None:
        lines.append(s)
        print(s)

    src = state["pours"][-1] if state["pours"] else None
    out(f"flood-report — {state['board']['tile_id'] or 'board'} "
        f"{h}x{w}, tick {river.tick_count}")
    out(f"  digs: {len(state['digs'])}"
        + ("" if state["digs"] else " (the mountain is untouched)")
        + "".join(f" | {gname(d['y'], d['x'])} {d['before']}->{d['after']}"
                  for d in state["digs"][:4])
        + (" ..." if len(state["digs"]) > 4 else ""))
    if src:
        out(f"  pour: {gname(src['y'], src['x'])} +{src['rate']}/tick "
            f"x {src['ticks']} ticks")
    wet = river.wet_cells()
    out(f"  wetted cells: {wet} ({wet * 100 // (h * w)}% of the board), "
        f"water standing {river.total_volume()} units, "
        f"drained to sea {river.drained}")
    if src:
        path = thalweg(river, src["y"], src["x"])
        end = path[-1]
        end_s = (f"reached the sea at {gname(end[0], end[1])}"
                 if end in river.waste else
                 f"ended in a pit at {gname(end[0], end[1])} "
                 f"(elev {river.elev[end[0]][end[1]]})")
        wet_on = sum(1 for cy, cx in path if river.vol[cy][cx] > 0)
        out(f"  max flow path (thalweg on the carved bed): {len(path)} "
            f"cells {gname(*path[0])} -> {end_s}; {wet_on} cells still wet")
        out("    " + " ".join(gname(*c) for c in path[:12]) + (" ..." if len(path) > 12 else ""))
    carved = sum(max(0, baseline[cy][cx] - river.elev[cy][cx])
                 for cy in range(h) for cx in range(w))
    raised = sum(max(0, river.elev[cy][cx] - baseline[cy][cx])
                 for cy in range(h) for cx in range(w))
    dug = sum(d["depth"] for d in state["digs"])
    out(f"  erosion: {river.total_eroded} units carved by water "
        f"(gross {carved} below baseline, gross {raised} raised, net "
        f"{carved - raised} lost = dug {dug} + water net "
        f"{river.total_eroded - river.total_deposited}) | "
        f"washed out {river.washed_out}")
    silt0 = state["silt_at_first_pour"]
    conserved = True if silt0 is None else river.total_silt() == silt0
    out(f"  silt: on board {river.total_silt()} "
        f"(conserved == at first pour: {conserved})")
    delta_silt = river.delta_silt()
    delta_raise = sum(max(0, river.elev[cy][cx] - baseline[cy][cx])
                      for cy, cx in river.waste)
    out(f"  delta: {delta_silt} silt parked at waste "
        f"{','.join(gname(cy, cx) for cy, cx in sorted(river.waste))}, "
        f"bed raised {delta_raise} — growth from zero baseline")
    e0 = sum(sum(r) for r in baseline)
    eok = e0 - river.total_elev() == dug + river.total_eroded - river.total_deposited
    out(f"  audit: silt {'CONSERVED' if conserved else 'BROKEN'}; elev accounting "
        f"{e0 - river.total_elev()} = {dug} dug + {river.total_eroded} carved - "
        f"{river.total_deposited} landed "
        f"{'OK' if eok else 'BROKEN'}")
    out("  trace ('~' wet, digits carve depth vs pristine, '^' raised bar):")
    for row in river.render(baseline).splitlines():
        out("    " + row)
    if args.trace:
        tp = Path(args.trace)
        tp.parent.mkdir(parents=True, exist_ok=True)
        tp.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"[flood-report] trace -> {tp}")
    return 0


# ------------------------------------------------------------------ cli ----
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="mountain_digflood",
        description="dig the breach, watch the flood (DFHack style, on the "
                    "St Helens board; the dig is the hand, the water obeys "
                    "the physics)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    st = str(DIGFLOOD_DIR / "state.json")

    p = sub.add_parser("load", help="board JSON -> digflood.v1 state")
    p.add_argument("--board", default=str(DEFAULT_BOARD),
                   help=f"water_graph.v1 board (default {DEFAULT_BOARD})")
    p.add_argument("--state", default=st)
    p.add_argument("--mantle", type=int, default=DEFAULT_MANTEL,
                   help=f"silt per land cell (default {DEFAULT_MANTEL})")
    p.add_argument("--sill", type=int, default=DEFAULT_SILL_FLOW,
                   help=f"erosion sill (default {DEFAULT_SILL_FLOW})")
    p.add_argument("--cross-section", type=int, default=DEFAULT_CROSS_SECTION)
    p.add_argument("--conductance", type=int, default=DEFAULT_CONDUCTANCE)
    p.set_defaults(fn=cmd_load)

    p = sub.add_parser("dig", help="the breach: lower one cell by K units")
    p.add_argument("x", type=int, help="column (node g{y}x{x})")
    p.add_argument("y", type=int, help="row")
    p.add_argument("-k", "--depth", type=int, default=DEFAULT_DEPTH,
                   help=f"elev units to remove (default {DEFAULT_DEPTH})")
    p.add_argument("--state", default=st)
    p.set_defaults(fn=cmd_dig)

    p = sub.add_parser("pour", help="N units/tick for T ticks at the source")
    p.add_argument("x", type=int, help="column")
    p.add_argument("y", type=int, help="row")
    p.add_argument("-n", "--rate", type=int, default=DEFAULT_RATE,
                   help=f"units per tick (default {DEFAULT_RATE})")
    p.add_argument("-t", "--ticks", type=int, default=DEFAULT_TICKS,
                   help=f"ticks to run (default {DEFAULT_TICKS})")
    p.add_argument("--state", default=st)
    p.set_defaults(fn=cmd_pour)

    p = sub.add_parser("flood-report", help="the after-T-ticks dossier")
    p.add_argument("--state", default=st)
    p.add_argument("--trace", default=None,
                   help="also write the report text here")
    p.set_defaults(fn=cmd_report)

    args = ap.parse_args(argv)
    try:
        return args.fn(args)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
