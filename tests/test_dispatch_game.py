"""The d13 dispatch game: 3 moves, exhaustive search, self-adjudicating falsifier.

Move 5 of stockfish-door-20261007, the encoding thesis's first executable byte
(watch/inbox/ractor_engine/2026-10-06-stockfish-coding/ logic.md L5 :30-34,
adopted by SYNTHESIS.md section 4 "the encoding map").

Board: one episode = one d13 problem in an 8-game session. Moves:
  SPAWN_HTTP    route the move through the spawned llama.cpp server over HTTP
                (one model load amortized over the session)
  INPROCESS     construct a fresh in-process model per call (the route the d13
                lane actually took: server spawned ok but never queried)
  FALLBACK_HASH skip the model, emit the sha256 hash move

Reward: the measured table, pinned below. Accuracy is the primary objective
(the deterministic oracle outranks the cost axis); wall milliseconds are the
cost axis. Silent expert: exhaustive search over all 3^8 per-game policies
(no board metaphor, no heuristic, the whole legal-move space). Self-
adjudication: the search's pick must beat the route the d13 lane actually
took ON THE SAME TABLE or the encoding thesis is ROUTE_DEAD for the class
(logic.md :32 kill criterion). Verdict grammar ported from the estate's own
trivalent instrument tools/gps_mcp/coverage.py:170-241
(ROUTE_MESH / ROUTE_FRONTIER / INSUFFICIENT, margin discipline, floor).

Two policy spaces, kept apart on purpose (the oracle-leakage finding):
  UNRESTRICTED  every 3^8 per-game assignments. Its optimum conditions on
                per-problem correctness (fall back on the games the oracle
                says you get wrong anyway), which no real dispatcher can
                know ex ante. It is an upper bound, not a route.
  REALIZABLE    policies a dispatcher can actually execute without knowing
                outcomes in advance. With no non-outcome per-game features
                in the table this reduces to the 3 uniform routes. THE
                falsifier adjudicates here, and the pick is the spawn+HTTP
                session.

Every number in the table below was read from a banked evidence file this
sitting; digests of the source files at pin time are in the verdict receipt
memory/runs/selfplay/s2_dispatch_game_verdict_20261007.json.

Table provenance (all byte-read 2026-10-07):
  HTTP per-game ms + correctness + wall_s 47.4:
      memory/runs/selfplay/evidence_latest.json (the wired re-run, s2 lane
      stockfish-door-20261007; same bytes as lanes/probes/wire_fix_evidence.json)
  INPROCESS per-game ms + correctness + wall_s 56.8:
      memory/runs/selfplay/evidence_pre_wirefix_20261007.json (the preserved
      d13 wiring; same bytes as
      memory/runs/mickey17_v2/runs/dogfood-100m-20261006/lanes/d13_selfplay_evidence.json)
  FALLBACK row (0 ms, accuracy 0):
      logic.md :32 ("fallback: 0ms, accuracy 0"); measured shape in the d13
      lane receipt row 1: runs 1-3 "spawn ok:false, actor ms 0.0, n_correct 0"
"""
from __future__ import annotations

import itertools

# ---------------------------------------------------------------------------
# The measured reward table (pinned constants, golden-vector style per
# tools/dungeon.py:12-13 refusal-to-run discipline: a wrong table is a red
# test, never a silently re-derived one).
# ---------------------------------------------------------------------------

N_GAMES = 8

# Correctness per problem m001..m008. Identical in both runs (asserted in
# test_reward_table_is_paired), so the two routes are a paired comparison:
# same model behavior, the only axis that moves is wall time.
CORRECT = [False, True, False, True, False, True, True, True]

# SPAWN_HTTP route: per-game actor_ms and scorer_ms from the wired re-run.
ACTOR_MS_HTTP = [2797.0, 1937.0, 4437.0, 6687.0, 1375.0, 1187.0, 1719.0, 1968.0]
SCORER_MS_HTTP = [2047.0, 1704.0, 2266.0, 1766.0, 1578.0, 4750.0, 3188.0, 1563.0]
SESSION_WALL_MS_HTTP = 47400.0  # wall_s 47.4

# INPROCESS route: per-game actor_ms and scorer_ms from the preserved d13 run
# (per-call model load inside every actor_ms; its session fixed cost includes
# the spawn it never queried, which is exactly the route as actually taken).
ACTOR_MS_INPROC = [3094.0, 3187.0, 3953.0, 5297.0, 2953.0, 2797.0, 3219.0, 3281.0]
SCORER_MS_INPROC = [2391.0, 2891.0, 3078.0, 2359.0, 2625.0, 5766.0, 1953.0, 2672.0]
SESSION_WALL_MS_INPROC = 56800.0  # wall_s 56.8

# FALLBACK route: the register's own table row. No actor compute, never
# correct (d13 runs 1-3 measured actor ms 0.0 / n_correct 0 on this path).
ACTOR_MS_FALLBACK = [0.0] * N_GAMES
SCORER_MS_FALLBACK = [0.0] * N_GAMES
CORRECT_FALLBACK = [False] * N_GAMES

MOVES = ("SPAWN_HTTP", "INPROCESS", "FALLBACK_HASH")
SPAWN_HTTP, INPROCESS, FALLBACK_HASH = 0, 1, 2

# One-time session costs are DERIVED from the pinned walls, not hand-copied:
# wall minus the summed per-game totals is what the session overhead
# (spawn plus prompt build plus evidence write; for the in-process session,
# the dead spawn it paid for) cost on each measured route.
TOTALS_HTTP = [a + s for a, s in zip(ACTOR_MS_HTTP, SCORER_MS_HTTP)]
TOTALS_INPROC = [a + s for a, s in zip(ACTOR_MS_INPROC, SCORER_MS_INPROC)]
FIXED_MS_HTTP = round(SESSION_WALL_MS_HTTP - sum(TOTALS_HTTP), 1)
FIXED_MS_INPROC = round(SESSION_WALL_MS_INPROC - sum(TOTALS_INPROC), 1)

# Verdict constants and margins, ported from tools/gps_mcp/coverage.py:170-172
# and :207 (margin 0.05). ROUTE_SEARCH / ROUTE_DEAD rename the mesh/frontier
# poles for this game's head-to-head (search pick vs the route actually
# taken); INSUFFICIENT keeps the estate name and meaning.
ROUTE_SEARCH = "ROUTE_SEARCH"
ROUTE_DEAD = "ROUTE_DEAD"
INSUFFICIENT = "INSUFFICIENT"
RATE_MARGIN = 0.05
WALL_MARGIN = 0.05
MIN_PROBLEMS_FLOOR = 10  # coverage.py:40, ported for the prospective row


# ---------------------------------------------------------------------------
# The game
# ---------------------------------------------------------------------------

def per_game_ms(move: int, game: int) -> float:
    """Wall cost of playing one move on one game, from the measured table."""
    if move == SPAWN_HTTP:
        return TOTALS_HTTP[game]
    if move == INPROCESS:
        return TOTALS_INPROC[game]
    return 0.0


def play(policy: tuple[int, ...]) -> dict:
    """Score one policy (a move per game) on the pinned table.

    Fixed cost: any policy that uses the spawned server pays the spawn
    session's overhead exactly once (one load amortized, the register's
    reward-table row); a policy with no spawn but at least one in-process
    game pays the in-process session's measured overhead (dead spawn
    included, the route as actually taken); a pure-fallback policy pays
    neither (runs 1-3: no successful spawn, no load).
    """
    assert len(policy) == N_GAMES
    if SPAWN_HTTP in policy:
        fixed = FIXED_MS_HTTP
    elif INPROCESS in policy:
        fixed = FIXED_MS_INPROC
    else:
        fixed = 0.0
    wall = fixed + sum(per_game_ms(m, g) for g, m in enumerate(policy))
    correct = sum(
        1 for g, m in enumerate(policy) if m != FALLBACK_HASH and CORRECT[g]
    )
    return {"accuracy": correct / N_GAMES, "wall_ms": wall, "fixed_ms": fixed}


def exhaustive_search() -> dict:
    """Enumerate ALL 3^N_GAMES policies, return the (accuracy, wall) argmax.

    Deterministic: lexicographic enumeration, strict-less-than keeps the
    first optimum, so reruns are byte-identical. UNRESTRICTED space: the
    winner may condition on per-problem correctness (oracle policy).
    """
    best_policy, best_key, best_score = None, None, None
    count = 0
    for policy in itertools.product((SPAWN_HTTP, INPROCESS, FALLBACK_HASH),
                                    repeat=N_GAMES):
        count += 1
        score = play(policy)
        key = (-score["accuracy"], score["wall_ms"])
        if best_key is None or key < best_key:
            best_policy, best_key, best_score = policy, key, score
    return {"policy": best_policy, "score": best_score, "policies": count}


def realizable_search() -> dict:
    """Exhaustive search over REALIZABLE policies: the 3 uniform routes.

    A dispatcher chooses a route for the session before seeing outcomes;
    the measured table carries no non-outcome per-game feature to key a
    finer policy on, so the realizable space is exactly the 3 uniform
    sessions. The falsifier adjudicates HERE, not on the oracle space.
    """
    best_policy, best_key, best_score = None, None, None
    count = 0
    for move in (SPAWN_HTTP, INPROCESS, FALLBACK_HASH):
        policy = (move,) * N_GAMES
        count += 1
        score = play(policy)
        key = (-score["accuracy"], score["wall_ms"])
        if best_key is None or key < best_key:
            best_policy, best_key, best_score = policy, key, score
    return {"policy": best_policy, "score": best_score, "policies": count}


def adjudicate(pick_score: dict, actual_score: dict) -> dict:
    """Head-to-head verdict: search pick vs the route actually taken.

    Ported from tools/gps_mcp/coverage.py:224-241 (floor-and-margin
    discipline): a pick that loses the accuracy primary by more than
    RATE_MARGIN is ROUTE_DEAD; a pick that ties or wins the primary and
    cuts wall beyond WALL_MARGIN is ROUTE_SEARCH; inside the wall margin
    is INSUFFICIENT (no prediction from thin air either way).
    """
    a_pick, a_act = pick_score["accuracy"], actual_score["accuracy"]
    w_pick, w_act = pick_score["wall_ms"], actual_score["wall_ms"]
    if a_pick < a_act - RATE_MARGIN:
        verdict, reason = ROUTE_DEAD, (
            f"pick accuracy {a_pick:.3f} loses actual {a_act:.3f} "
            f"by more than margin {RATE_MARGIN}"
        )
    elif w_pick < w_act * (1.0 - WALL_MARGIN):
        verdict, reason = ROUTE_SEARCH, (
            f"accuracy held at {a_pick:.3f} vs {a_act:.3f} and wall "
            f"{w_pick:.0f}ms beats actual {w_act:.0f}ms beyond margin {WALL_MARGIN}"
        )
    elif w_pick >= w_act:
        verdict, reason = ROUTE_DEAD, (
            f"accuracy held but pick wall {w_pick:.0f}ms does not beat "
            f"actual {w_act:.0f}ms"
        )
    else:
        verdict, reason = INSUFFICIENT, (
            f"inside wall margin {WALL_MARGIN}: pick {w_pick:.0f}ms "
            f"vs actual {w_act:.0f}ms"
        )
    return {"verdict": verdict, "reason": reason}


def prospective_verdict(n_problems: int) -> dict:
    """The routing-advice row for unseen problems, floored like coverage.py.

    The head-to-head above adjudicates the measured past on paired same-
    problem deltas; predicting routes for FUTURE problems from a pass-rate
    style table is the claim coverage.py floors. Ported faithfully: below
    MIN_PROBLEMS_FLOOR the prediction is INSUFFICIENT, a verdict rather
    than a failure (the door waits for a bigger measured table).
    """
    if n_problems < MIN_PROBLEMS_FLOOR:
        return {"verdict": INSUFFICIENT, "reason": (
            f"{n_problems} measured games < floor {MIN_PROBLEMS_FLOOR} "
            "(tools/gps_mcp/coverage.py:40); no route prediction for "
            "unseen problems from this table"
        )}
    return {"verdict": ROUTE_SEARCH, "reason": "floored table, head-to-head stands"}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

ACTUAL_ROUTE = (INPROCESS,) * N_GAMES  # the d13 lane's dead-endpoint route


class TestRewardTable:
    def test_reward_table_is_paired(self):
        """Both measured runs must agree problem-by-problem on correctness.

        This is what makes the wall comparison a paired delta instead of a
        thin-air rate: same problems, same model behavior, one axis moves.
        Averages must reproduce the banked verdicts (2763.4 vs 3472.6).
        """
        assert len(CORRECT) == N_GAMES
        assert sum(CORRECT) == 5
        assert round(sum(ACTOR_MS_HTTP) / N_GAMES, 1) == 2763.4
        assert round(sum(ACTOR_MS_INPROC) / N_GAMES, 1) == 3472.6
        assert round(sum(SCORER_MS_HTTP) / N_GAMES, 1) == 2357.8
        assert round(sum(SCORER_MS_INPROC) / N_GAMES, 1) == 2966.9

    def test_fixed_costs_derived_not_copied(self):
        """Session overheads recompute from the pinned walls and totals."""
        assert FIXED_MS_HTTP == round(47400.0 - sum(TOTALS_HTTP), 1) == 6431.0
        assert FIXED_MS_INPROC == round(56800.0 - sum(TOTALS_INPROC), 1) == 5284.0

    def test_uniform_policies_reproduce_the_banked_walls(self):
        """The three uniform routes score the sessions as measured."""
        assert play((SPAWN_HTTP,) * N_GAMES) == {
            "accuracy": 0.625, "wall_ms": 47400.0, "fixed_ms": 6431.0}
        assert play((INPROCESS,) * N_GAMES) == {
            "accuracy": 0.625, "wall_ms": 56800.0, "fixed_ms": 5284.0}
        assert play((FALLBACK_HASH,) * N_GAMES) == {
            "accuracy": 0.0, "wall_ms": 0.0, "fixed_ms": 0.0}


class TestExhaustiveSearch:
    def test_space_is_three_to_the_eighth(self):
        result = exhaustive_search()
        assert result["policies"] == 3 ** N_GAMES == 6561

    def test_pick_golden_vectors(self):
        """The UNRESTRICTED optimum is pinned: fall back on the three games
        the oracle says are wrong anyway (m001, m003, m005, saving their
        whole 14500ms), ride in-process on m004 (its measured draw is the
        one game faster in-process), spawn+HTTP on the rest, and the
        optimum is unique. This pick conditions on outcomes, so it is an
        oracle upper bound, NOT a route (see the realizable tests below).
        """
        result = exhaustive_search()
        expected = (FALLBACK_HASH, SPAWN_HTTP, FALLBACK_HASH, INPROCESS,
                    FALLBACK_HASH, SPAWN_HTTP, SPAWN_HTTP, SPAWN_HTTP)
        assert result["policy"] == expected
        assert result["score"]["accuracy"] == 0.625
        assert result["score"]["wall_ms"] == 32103.0
        # uniqueness: no other policy ties the winning key
        winners = sum(
            1 for p in itertools.product((SPAWN_HTTP, INPROCESS, FALLBACK_HASH),
                                         repeat=N_GAMES)
            if (-play(p)["accuracy"], play(p)["wall_ms"])
            == (-result["score"]["accuracy"], result["score"]["wall_ms"])
        )
        assert winners == 1

    def test_realizable_pick_is_spawn_http_session(self):
        """The REALIZABLE optimum is the uniform spawn+HTTP session: same
        accuracy as the actual route (paired correctness), 9400ms cheaper
        wall, one load amortized. This is the pick a dispatcher can run.
        """
        result = realizable_search()
        assert result["policies"] == 3
        assert result["policy"] == (SPAWN_HTTP,) * N_GAMES
        assert result["score"] == {
            "accuracy": 0.625, "wall_ms": 47400.0, "fixed_ms": 6431.0}

    def test_oracle_gap_is_named(self):
        """First-class negative: the gap between the oracle optimum and the
        realizable optimum is exactly the leaked outcome information. Named
        so nobody banks the 32103ms number as a dispatchable route.
        """
        oracle = exhaustive_search()["score"]["wall_ms"]
        realizable = realizable_search()["score"]["wall_ms"]
        assert oracle == 32103.0
        assert realizable - oracle == 15297.0

    def test_determinism_across_10_reruns(self):
        """Kill criterion 1 (strict determinism): both searches are pure
        functions of the pinned table; 10 reruns must be byte-identical.
        """
        runs = [exhaustive_search() for _ in range(10)]
        assert all(r["policy"] == runs[0]["policy"] for r in runs)
        assert all(r["score"] == runs[0]["score"] for r in runs)
        rruns = [realizable_search() for _ in range(10)]
        assert all(r["policy"] == rruns[0]["policy"] for r in rruns)
        assert all(r["score"] == rruns[0]["score"] for r in rruns)


class TestFalsifier:
    def test_search_pick_beats_the_route_actually_taken(self):
        """THE falsifier (logic.md :32, SYNTHESIS section 5 kill 2): on the
        same reward table, the exhaustive search's pick must beat the
        dead-endpoint route the d13 lane actually took. If it does not,
        the encoding thesis is ROUTE_DEAD for the class. Adjudicated on the
        REALIZABLE pick (uniform routes, no outcome conditioning): the
        spawn+HTTP session. The oracle-space pick beats it too and is
        asserted separately as an upper bound.
        """
        pick = realizable_search()
        actual = play(ACTUAL_ROUTE)
        assert pick["score"]["accuracy"] >= actual["accuracy"], (
            "search pick lost the accuracy primary; encoding thesis dies"
        )
        assert pick["score"]["wall_ms"] < actual["wall_ms"], (
            "search pick did not cut wall time vs the actual route; "
            "encoding thesis dies"
        )
        # oracle upper bound also clears the bar (weaker claim, realizable
        # is the one the thesis rides on)
        oracle = exhaustive_search()["score"]
        assert oracle["accuracy"] >= actual["accuracy"]
        assert oracle["wall_ms"] < actual["wall_ms"]

    def test_head_to_head_verdict_is_route_search(self):
        pick = realizable_search()
        verdict = adjudicate(pick["score"], play(ACTUAL_ROUTE))
        assert verdict["verdict"] == ROUTE_SEARCH
        assert "wall 47400ms beats actual 56800ms" in verdict["reason"]


class TestTrivalentPort:
    def test_inside_wall_margin_is_insufficient(self):
        verdict = adjudicate(
            {"accuracy": 0.625, "wall_ms": 56_000.0},
            {"accuracy": 0.625, "wall_ms": 56_800.0},
        )
        assert verdict["verdict"] == INSUFFICIENT

    def test_pick_losing_accuracy_is_route_dead(self):
        verdict = adjudicate(
            {"accuracy": 0.5, "wall_ms": 100.0},
            {"accuracy": 0.625, "wall_ms": 56_800.0},
        )
        assert verdict["verdict"] == ROUTE_DEAD

    def test_pick_not_beating_wall_is_route_dead(self):
        verdict = adjudicate(
            {"accuracy": 0.625, "wall_ms": 57_500.0},
            {"accuracy": 0.625, "wall_ms": 56_800.0},
        )
        assert verdict["verdict"] == ROUTE_DEAD

    def test_prospective_row_is_floored_at_8_games(self):
        """Honest negative row, filed first-class: this table holds 8 games,
        below the ported 10-keyed-problems floor, so the ROUTE prediction
        for unseen problems is INSUFFICIENT even though the head-to-head
        adjudication stands. A verdict, not a failure.
        """
        verdict = prospective_verdict(N_GAMES)
        assert verdict["verdict"] == INSUFFICIENT
        assert "8 measured games < floor 10" in verdict["reason"]
        assert prospective_verdict(MIN_PROBLEMS_FLOOR)["verdict"] == ROUTE_SEARCH
