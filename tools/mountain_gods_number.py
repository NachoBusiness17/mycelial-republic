"""mountain_gods_number — God's Number for OUR mountain (W3 lane, 2026-09-29).

Seed (operator drop, Math_files): the cube's graph has ~4.3e19 states and
diameter 20 — God's Number. This tool computes the same artifact for the
Mountain water board (server/world.py build_mountain_graph over
mag/water_graph.WaterGraph): an exhaustive BFS over the reachable state
graph of the deterministic move set, reporting state count, diameter,
the farthest state, and the shortest solve length (start -> crown >= 4).

State (a flat tuple of small ints; layout owned by the Board):
    volumes of the tracked (non-waste) nodes, total steam, pipe open
    bits, siphon primed bits, sticky won bit.

Two collapses against the mission's literal "(volumes, open bits,
primed, won)" tuple, both argued here and pinned by tests:
  - waste volume dropped: engine law (WaterGraph._move) destroys water
    entering a `waste` node without crediting it, so v_waste == 0 is
    invariant on this board.
  - per-node steam collapsed to TOTAL steam: the board has exactly one
    cold node (crown, elev 14) and _condense_steam moves EVERY node's
    steam into the single max-elevation cold node; no other code reads
    steam. Placement is therefore irrelevant to every transition
    (tests/test_gods_number.py proves the quotient exact on the fixture:
    same reachable set, same per-state distances).

Edges (deterministic; server/world.py verbs minus the no-physics ones):
  - tick: the REAL WaterGraph.tick() runs on a scratch board restored
    from the state (volumes, steam parked on the first tracked node,
    opens, primed). Fidelity beats speed: the diameter is computed on
    the estate's own physics organ, not a re-implementation. The sticky
    `won` bit is MountainWorld-level (checked at tick end) and is folded
    in as won |= crown >= 4 after the tick.
  - boil at node: server validate law (volume >= 1, else DRY_POOL);
    volume -1, steam +1.
  - valve on pipe: toggle the open bit (p_bypass starts SHUT).
    join/tag touch roster/score only, never physics — excluded.

Engine corner kept AS IS: p_spring's deferral into the XOR junction is
read before p_bypass's direct commit in the same pipe pass, so a primed
open bypass can double-spend spring down to volume == -1 (floor proven
by cap arithmetic: both pipes carry min(1, v) from a read of v >= 1, so
at most v + 1 leaves a node holding v). The double-spend CONSERVES the
graph sum (the -1 backs a phantom +1 elsewhere: a sibling node can hold
w+1 units), and once spring is negative nothing ever refills it. God's
Number describes the engine we have, not the one we wish we had;
_bounds_check guards every invariant so an escape is a loud failure,
never a silent one.

Usage:
    .venv/Scripts/python.exe tools/mountain_gods_number.py               # mountain
    .venv/Scripts/python.exe tools/mountain_gods_number.py --board fixture
"""
from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass
from math import comb
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag.water_graph import WaterGraph  # noqa: E402
from server.world import build_mountain_graph  # noqa: E402

State = tuple[int, ...]
Move = str

# the mission's fit threshold: below this, exhaustive BFS is the method
BFS_FITS_UNDER = 5_000_000


def build_fixture_graph() -> WaterGraph:
    """Tiny 2-node board with a known hand-computed BFS (tests pin it):
    tank(2) drains 1/tick into a cold cup; boil routes via steam; one
    valve. Hand answer: 12 states, diameter 3."""
    g = WaterGraph()
    g.add_node("tank", elev=2, volume=2)
    g.add_node("cup", elev=0, kind="cold")
    g.add_pipe("p_tank", "tank", "cup", cap=1)
    return g


@dataclass
class Board:
    """A board plus the tuple layout of its states."""

    graph: WaterGraph
    vol_nodes: tuple[str, ...]                 # tracked volume nodes (non-waste)
    pipes: tuple[str, ...]                     # valve-able pipes, insertion order
    siphons: tuple[str, ...]                   # subset with siphon=True
    win_node: str | None                       # sticky-win node ("crown") or None
    win_volume: int
    total_water: int                           # frozen at construction

    @property
    def steam_idx(self) -> int:
        return len(self.vol_nodes)

    @property
    def open_base(self) -> int:
        return len(self.vol_nodes) + 1

    @property
    def primed_base(self) -> int:
        return self.open_base + len(self.pipes)

    @property
    def won_idx(self) -> int:
        return self.primed_base + len(self.siphons)

    @property
    def width(self) -> int:
        return self.won_idx + 1


def board_from_graph(g: WaterGraph, win_node: str | None = None,
                     win_volume: int = 0) -> Board:
    # total_water is frozen here: the graph is a scratch board the BFS
    # mutates tick by tick, so a live sum would drift mid-run (caught by
    # _bounds_check firing on a phantom bound of 5, 2026-09-29).
    return Board(
        graph=g,
        vol_nodes=tuple(n for n, node in g.nodes.items() if node.kind != "waste"),
        pipes=tuple(g.pipes),
        siphons=tuple(p for p in g.pipes if g.pipes[p].siphon),
        win_node=win_node,
        win_volume=win_volume,
        total_water=sum(n.volume for n in g.nodes.values()),
    )


def mountain_board() -> Board:
    return board_from_graph(build_mountain_graph(), win_node="crown", win_volume=4)


def fixture_board() -> Board:
    return board_from_graph(build_fixture_graph())


def initial_state(board: Board) -> State:
    s = [0] * board.width
    for i, name in enumerate(board.vol_nodes):
        s[i] = board.graph.nodes[name].volume
    for j, p in enumerate(board.pipes):
        s[board.open_base + j] = 1 if board.graph.pipes[p].open else 0
    for k, p in enumerate(board.siphons):
        s[board.primed_base + k] = 1 if board.graph.pipes[p].primed else 0
    return tuple(s)


# --------------------------------------------------------------- engine ----

def _restore(board: Board, s: State) -> None:
    g = board.graph
    for i, name in enumerate(board.vol_nodes):
        g.nodes[name].volume = s[i]
    for node in g.nodes.values():
        if node.kind == "waste":
            node.volume = 0          # invariant: waste is never credited
        node.steam = 0
    # park all steam on the first tracked node: placement is irrelevant
    # (single cold node condenses everything; nothing else reads steam)
    g.nodes[board.vol_nodes[0]].steam = s[board.steam_idx]
    for j, p in enumerate(board.pipes):
        g.pipes[p].open = bool(s[board.open_base + j])
    for k, p in enumerate(board.siphons):
        g.pipes[p].primed = bool(s[board.primed_base + k])


def _state_of(board: Board, won: int) -> State:
    g = board.graph
    s = [0] * board.width
    for i, name in enumerate(board.vol_nodes):
        s[i] = g.nodes[name].volume
    s[board.steam_idx] = sum(n.steam for n in g.nodes.values())
    for j, p in enumerate(board.pipes):
        s[board.open_base + j] = 1 if g.pipes[p].open else 0
    for k, p in enumerate(board.siphons):
        s[board.primed_base + k] = 1 if g.pipes[p].primed else 0
    s[board.won_idx] = won
    return tuple(s)


def _bounds_check(board: Board, s: State) -> None:
    """True invariants of the engine on this board, each proven from the
    tick code (receipt: two loud catches during the 2026-09-29 run):
      - only spring has BOTH a deferring outflow (p_spring into the XOR)
        and a direct-commit outflow (p_bypass), so only it can be
        double-spent, and only down to -1 (both pipes carry min(1, v)
        read at v >= 1; nothing ever refills spring);
      - the double-spend CONSERVES the graph sum (spring 1 -> -1 while
        terrace and gate1 each gain 1), so one sibling node can legally
        hold w+1 units backed by the -1 — a per-node cap of w is too
        tight (first catch fired on hollow=9, spring=-1);
      - sum(volumes) + steam never exceeds the initial total (destroyed
        to waste / starve-spill only decreases it).
    """
    w = board.total_water
    vols = s[: board.steam_idx]
    negs = sum(1 for v in vols if v < 0)
    if min(vols) < -1 or negs > 1:
        raise RuntimeError(f"volume below the -1 double-spend floor: {s}")
    if s[board.steam_idx] < 0 or s[board.steam_idx] > w:
        raise RuntimeError(f"steam out of [0, {w}]: {s}")
    if max(vols) > w + 1:
        raise RuntimeError(f"volume above the w+1 phantom-unit ceiling: {s}")
    if sum(vols) + s[board.steam_idx] > w:
        raise RuntimeError(f"water created from nothing: {s}")


def tick_state(board: Board, s: State) -> State:
    """One physics tick on the real engine; the only mutator of volumes,
    primed bits, and (via condensation) the won bit."""
    _restore(board, s)
    board.graph.tick()
    won = s[board.won_idx]
    if (board.win_node is not None
            and board.graph.nodes[board.win_node].volume >= board.win_volume):
        won = 1
    t = _state_of(board, won)
    _bounds_check(board, t)
    return t


def successors(board: Board, s: State) -> list[tuple[Move, State]]:
    """All edges from s: one tick + one boil per wet node + one valve per
    pipe. Deterministic order; self-loops (tick on a dead board) are fine,
    BFS dedups."""
    out: list[tuple[Move, State]] = [("tick", tick_state(board, s))]
    for i, name in enumerate(board.vol_nodes):
        if s[i] >= 1:                # server validate: volume <= 0 -> DRY_POOL
            t = list(s)
            t[i] -= 1
            t[board.steam_idx] += 1
            out.append((f"boil {name}", tuple(t)))
    for j, pname in enumerate(board.pipes):
        t = list(s)
        t[board.open_base + j] ^= 1
        out.append((f"valve {pname}", tuple(t)))
    return out


# ------------------------------------------------------------------ BFS ----

def bfs(board: Board, start: State) -> tuple[dict[State, int], dict[State, tuple[State, Move] | None]]:
    """Exhaustive breadth-first search from start. Returns (dist, parent);
    parent[start] is None, else (previous state, move label)."""
    dist: dict[State, int] = {start: 0}
    parent: dict[State, tuple[State, Move] | None] = {start: None}
    frontier = [start]
    while frontier:
        nxt: list[State] = []
        for s in frontier:
            d = dist[s] + 1
            for move, t in successors(board, s):
                if t not in dist:
                    dist[t] = d
                    parent[t] = (s, move)
                    nxt.append(t)
        frontier = nxt
    return dist, parent


def path_to(parent: dict[State, tuple[State, Move] | None], goal: State) -> list[Move]:
    moves: list[Move] = []
    s = goal
    while parent[s] is not None:
        prev, move = parent[s]
        moves.append(move)
        s = prev
    moves.reverse()
    return moves


# -------------------------------------------------------------- report ----

def describe_state(board: Board, s: State) -> str:
    vols = ", ".join(f"{n}={s[i]}" for i, n in enumerate(board.vol_nodes))
    opens = ", ".join(p for j, p in enumerate(board.pipes) if s[board.open_base + j]) or "-"
    shuts = ", ".join(p for j, p in enumerate(board.pipes) if not s[board.open_base + j]) or "-"
    prim = ", ".join(p for k, p in enumerate(board.siphons) if s[board.primed_base + k]) or "-"
    lost = board.total_water - (sum(s[: board.steam_idx + 1]))
    return (f"volumes[{vols}] steam={s[board.steam_idx]} open[{opens}] "
            f"shut[{shuts}] siphon_primed[{prim}] won={s[board.won_idx]} "
            f"water_lost_to_waste={lost}")


def estimate_upper_bound(board: Board) -> int:
    """Combinatorial upper bound on reachable states, printed BEFORE the
    run so the method call (BFS fits / does not fit) is on the record."""
    w = board.total_water
    buckets = len(board.vol_nodes) + 1          # volumes + one shared steam bucket
    combos = comb(w + buckets, buckets)         # nonneg ints summing <= w
    if any(board.graph.nodes[p.dst].kind in ("xor", "sill")
           for p in board.graph.pipes.values()):
        # a gated junction defers a read that a later direct pipe from
        # the same source can spend again: one bucket may sit at -1
        combos += comb(w + 1 + buckets, buckets)
    return combos * (2 ** len(board.pipes)) * (2 ** len(board.siphons)) * 2


def solve_distance(board: Board, dist: dict[State, int]) -> int | None:
    if board.win_node is None:
        return None
    won_dists = [d for s, d in dist.items() if s[board.won_idx]]
    return min(won_dists) if won_dists else None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="God's Number for the Mountain water board")
    ap.add_argument("--board", choices=("mountain", "fixture"), default="mountain")
    args = ap.parse_args(argv)

    board = mountain_board() if args.board == "mountain" else fixture_board()
    est = estimate_upper_bound(board)
    print(f"[estimate] {args.board}: combinatorial upper bound {est:,} states "
          f"(threshold {BFS_FITS_UNDER:,}) -> exhaustive BFS "
          f"{'FITS' if est < BFS_FITS_UNDER else 'DOES NOT FIT'}")

    start = initial_state(board)
    print(f"[start]    {describe_state(board, start)}")

    t0 = time.perf_counter()
    dist, parent = bfs(board, start)
    elapsed = time.perf_counter() - t0

    diameter = max(dist.values())
    farthest = [s for s, d in dist.items() if d == diameter]
    print(f"[bfs]      states={len(dist):,} diameter={diameter} elapsed={elapsed:.1f}s")

    print(f"[farthest] {len(farthest)} state(s) at depth {diameter}:")
    for s in farthest[:5]:
        print(f"           {describe_state(board, s)}")
    witness = path_to(parent, farthest[0])
    print(f"[path]     to first farthest ({len(witness)} moves): {'; '.join(witness)}")

    solve = solve_distance(board, dist)
    if solve is not None:
        goal = min((s for s in dist if s[board.won_idx]), key=lambda s: dist[s])
        print(f"[solve]    shortest start->won (crown>={board.win_volume}) = {solve} moves")
        print(f"[path]     to win: {'; '.join(path_to(parent, goal))}")
    print(f"[end]      THE NUMBER (diameter of the {args.board} state graph) = {diameter}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
