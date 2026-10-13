"""gods_number tests — the Mountain's diameter is a tested fact (W3, 2026-09-29).

Pins tools/mountain_gods_number.py three ways:
  - the 2-node fixture BFS equals a HAND-computed distance map (12
    states, diameter 3), so the BFS machinery is checked against
    arithmetic done on paper, not against itself;
  - collapsing per-node steam to TOTAL steam is an exact graph quotient
    (single cold node condenses everything; nothing else reads steam):
    a brute-force per-node-steam BFS projects onto the collapsed BFS
    with the same reachable set and the same per-state distances;
  - the golden Mountain numbers (339,840 states / diameter 25 / solve
    5) and the 5-move solve witness replay through the REAL server
    world (MountainWorld staged actions apply at tick start, then the
    physics condenses — winner in one tick).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from server.world import MountainWorld  # noqa: E402
from tools.mountain_gods_number import (  # noqa: E402
    bfs,
    board_from_graph,
    build_fixture_graph,
    initial_state,
    mountain_board,
    path_to,
    solve_distance,
)


# --------------------------------------------------------------- fixture ----

def test_fixture_bfs_matches_hand_computation():
    """Hand enumeration (2026-09-29, worked twice on paper):
    d0 (2,0,0,1); d1 (1,1,0,1),(1,0,1,1),(2,0,0,0);
    d2 (0,2,0,1),(0,1,1,1),(1,1,0,0),(0,0,2,1),(1,0,1,0);
    d3 (0,2,0,0),(0,1,1,0),(0,0,2,0).  State = (tank, cup, steam, open)."""
    board = board_from_graph(build_fixture_graph())
    start = initial_state(board)
    dist, parent = bfs(board, start)

    hand = {
        (2, 0, 0, 1): 0,
        (1, 1, 0, 1): 1, (1, 0, 1, 1): 1, (2, 0, 0, 0): 1,
        (0, 2, 0, 1): 2, (0, 1, 1, 1): 2, (1, 1, 0, 0): 2,
        (0, 0, 2, 1): 2, (1, 0, 1, 0): 2,
        (0, 2, 0, 0): 3, (0, 1, 1, 0): 3, (0, 0, 2, 0): 3,
    }
    got = {tuple(s[:3]) + (s[board.open_base],): d for s, d in dist.items()}
    assert got == hand, "fixture BFS disagrees with the hand computation"
    assert max(dist.values()) == 3
    # every depth-3 state has the valve SHUT: with it open the tank
    # drains in two ticks, so depth lives behind the closed valve.
    assert all(s[board.open_base] == 0 for s, d in dist.items() if d == 3)
    # parent chain reaches the farthest state in exactly 3 moves
    far = next(s for s, d in dist.items() if d == 3)
    assert len(path_to(parent, far)) == 3


def test_total_steam_is_a_sufficient_statistic():
    """Brute-force BFS over EXPLICIT per-node steam states (driven through
    the real engine) must project exactly onto the collapsed BFS: same
    reachable set, and collapsed distance == MIN distance over preimages
    (preimages of one quotient state can sit at different depths — steam
    at the tank is boil-reachable at d1, steam at the cup at d2 — but
    their forward evolution is identical, so the quotient preserves
    shortest-path lengths). This is the proof that parking all steam on
    one node loses no information on a board with a single cold node."""
    g = build_fixture_graph()

    def succ_explicit(s):  # s = (tank, cup, steam_tank, steam_cup, open)
        g.nodes["tank"].volume, g.nodes["cup"].volume = s[0], s[1]
        g.nodes["tank"].steam, g.nodes["cup"].steam = s[2], s[3]
        g.pipes["p_tank"].open = bool(s[4])
        g.tick()
        out = [(g.nodes["tank"].volume, g.nodes["cup"].volume,
                g.nodes["tank"].steam, g.nodes["cup"].steam, s[4])]
        if s[0] >= 1:
            out.append((s[0] - 1, s[1], s[2] + 1, s[3], s[4]))
        if s[1] >= 1:
            out.append((s[0], s[1] - 1, s[2], s[3] + 1, s[4]))
        out.append((s[0], s[1], s[2], s[3], 1 - s[4]))
        return out

    start = (2, 0, 0, 0, 1)
    dist = {start: 0}
    frontier = [start]
    while frontier:
        nxt = []
        for s in frontier:
            for t in succ_explicit(s):
                if t not in dist:
                    dist[t] = dist[s] + 1
                    nxt.append(t)
        frontier = nxt

    board = board_from_graph(build_fixture_graph())
    collapsed_dist, _ = bfs(board, initial_state(board))
    collapsed = {tuple(s[:3]) + (s[board.open_base],): d
                 for s, d in collapsed_dist.items()}
    preimages: dict[tuple, list[int]] = {}
    for (t, c, st_t, st_c, o), d in dist.items():
        preimages.setdefault((t, c, st_t + st_c, o), []).append(d)
    assert set(preimages) == set(collapsed), "quotient reachable set drifted"
    for q, depths in preimages.items():
        assert min(depths) == collapsed[q], (
            f"quotient distance must be the min over preimages: {q}")


# -------------------------------------------------------------- mountain ----

def test_mountain_witness_replays_on_server_world():
    """The BFS solve path (4 boils + 1 tick) through the REAL server
    semantics: staged boils apply at tick start, the physics condenses
    the steam onto the crown in the same tick, winner flips."""
    w = MountainWorld()
    try:
        w.register_session("s1", "tester")
        for _ in range(4):
            reply = w.stage("s1", "boil", "spring")
            assert reply["op"] == "ack", reply
        payload = w.tick()
        assert payload["nodes"]["crown"] == 4
        assert payload["winner"] is True
        assert w.verify_log(), "event log chain must stay intact"
    finally:
        w.close()


def test_mountain_gods_number_golden():
    """Byte-truth from the 2026-09-29 run (receipt W3M_GODS_NUMBER.md):
    339,840 reachable states, diameter 25, shortest solve 5. Also pins
    the engine invariants the bounds check guards."""
    board = mountain_board()
    start = initial_state(board)
    assert start[:5] == (6, 0, 0, 2, 0), "Mountain start board drifted"
    dist, _parent = bfs(board, start)

    assert len(dist) == 339_840
    assert max(dist.values()) == 25
    assert solve_distance(board, dist) == 5
    assert dist[start] == 0 and start[board.won_idx] == 0

    for s in dist:
        vols = s[: board.steam_idx]
        assert min(vols) >= -1, "double-spend floor is -1"
        assert sum(1 for v in vols if v < 0) <= 1, "only spring can go negative"
        assert sum(vols) + s[board.steam_idx] <= 8, "water is never created net"
        if s[board.vol_nodes.index("crown")] >= 4:
            assert s[board.won_idx] == 1, "crown>=4 implies sticky won"
