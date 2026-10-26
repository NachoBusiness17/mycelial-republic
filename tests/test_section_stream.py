"""section_stream tests — Z4 receipt (hydrology lane, 2026-09-29).

Port of roblox/src/shared/SectionStream.luau (103 lines, deterministic
streamed world-gen) to mag/section_stream.py. The Luau sells ONE property
and these tests buy it: with ``ordered=True`` the insertion order equals
rng draw order, so a world streamed section-by-section behind a walking
player is IDENTICAL to the eagerly built one — same seed, same mountain,
byte-exact rerun (the Ossuary SeedRng(20261031) claim). The test-side rng
mirrors roblox/src/shared/SeedRng.luau (xorshift32, wrap-exact) so the
proof rides the fleet's own seeded shape, satisfying the estate's no-RNG
law: no unseeded randomness anywhere, and the module under test has no rng
at all.

Coverage: same-seed determinism, streamed-ordered == eager, unordered mode
diverging (the load-bearing contrast), the ordered gate holding back a
section whose radius trips before its predecessors', per-poll budget caps,
inclusive radius boundary, pending()/return counts, and a small walked
world generating to completion.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.section_stream import SectionStream  # noqa: E402


class SeedRng:
    """xorshift32, replay-safe — mirror of roblox/src/shared/SeedRng.luau.
    Python ints are arbitrary precision, so the 32-bit wraparound that
    Luau's bit32 gives for free is explicit here via masks."""

    def __init__(self, seed: int) -> None:
        self.seed = seed % 2147483647
        if self.seed == 0:
            self.seed = 1  # xorshift32 must not start at zero

    def next(self) -> float:
        s = self.seed
        s = (s ^ ((s << 13) & 0xFFFFFFFF)) & 0xFFFFFFFF
        s ^= s >> 17
        s = (s ^ ((s << 5) & 0xFFFFFFFF)) & 0xFFFFFFFF
        self.seed = s
        return s / 4294967296

    def int(self, lo: int, hi: int) -> int:
        return lo + int(self.next() * (hi - lo + 1))

    def pick(self, options: Sequence[str]) -> str:
        return options[self.int(1, len(options)) - 1]


# --- world fixture: N sections on a grid, each closure draws a FIXED number
# --- of values from one shared rng (fixed per-section draw counts, the
# --- Ossuary shape: order of invocation fully determines every draw).


def make_world(
    seed: int,
    n: int,
    spacing: float,
    radius: float,
    ordered: bool,
    budget: float | None = None,
) -> Tuple[SectionStream, List[Tuple[int, int, str]]]:
    rng = SeedRng(seed)
    log: List[Tuple[int, int, str]] = []
    stream = SectionStream(radius=radius, budget=budget, ordered=ordered)
    for i in range(n):
        center = (spacing * (i % 5), 0.0, spacing * (i // 5))

        def build(i: int = i, rng: SeedRng = rng, log: List[Tuple[int, int, str]] = log) -> None:
            log.append((i, rng.int(0, 999), rng.pick(["corridor", "sentinel", "lever"])))

        stream.add(center, build)
    return stream, log


def walk(stream: SectionStream, stops: List[Tuple[float, float, float]], max_cycles: int = 50) -> int:
    """Poll once per walker stop, cycling the stop list until drained; a
    full cycle with zero builds aborts (the ordered gate can hold back
    progress at any single stop, but never across a whole covering tour)."""
    total = 0
    for _cycle in range(max_cycles):
        if not stream.pending():
            break
        progress = total
        for stop in stops:
            total += stream.poll([stop])
        if total == progress:
            break  # covering tour built nothing: would spin forever
    return total


def grid_stops(spacing: float) -> List[Tuple[float, float, float]]:
    """Walker stops AT each section center, row-major = insertion order."""
    return [(spacing * (i % 5), 0.0, spacing * (i // 5)) for i in range(25)]


def test_same_seed_identical_stream() -> None:
    """Determinism: two independent streams, same seed + same walk -> identical."""
    a, log_a = make_world(20261031, 25, 4.0, 6.0, ordered=True, budget=3)
    b, log_b = make_world(20261031, 25, 4.0, 6.0, ordered=True, budget=3)
    walk(a, grid_stops(4.0))
    walk(b, grid_stops(4.0))
    assert a.pending() == 0 and b.pending() == 0
    assert log_a == log_b
    assert len(log_a) == 25  # every section drew exactly once


def test_ordered_streamed_equals_eager() -> None:
    """The Ossuary law: streamed-ordered draws == eager draws, exactly."""
    streamed, log = make_world(20261031, 25, 4.0, 6.0, ordered=True, budget=4)
    # walker starts at the FAR corner: later sections' radii trip first, the
    # ordered gate must still force insertion-order builds
    walk(streamed, list(reversed(grid_stops(4.0))))
    eager_rng = SeedRng(20261031)
    eager = [
        (i, eager_rng.int(0, 999), eager_rng.pick(["corridor", "sentinel", "lever"]))
        for i in range(25)
    ]
    assert log == eager


def test_unordered_diverges_from_eager() -> None:
    """Contrast: ordered=False lets a far-first walker break rng order."""
    unordered, log = make_world(20261031, 25, 4.0, 6.0, ordered=False, budget=4)
    walk(unordered, list(reversed(grid_stops(4.0))))
    eager_rng = SeedRng(20261031)
    eager = [
        (i, eager_rng.int(0, 999), eager_rng.pick(["corridor", "sentinel", "lever"]))
        for i in range(25)
    ]
    assert log != eager  # section ids not in insertion order
    assert sorted(first for first, _, _ in log) == list(range(25))  # ...but all 25 built once


def test_ordered_gate_holds_back_early_radius_trip() -> None:
    """A section whose own radius trips first waits for its predecessors."""
    stream, _ = make_world(20261031, 25, 4.0, 6.0, ordered=True)
    far_corner = grid_stops(4.0)[-1]  # in radius of late sections only
    assert stream.poll([far_corner]) == 0  # gated: sections 0.. not built
    assert stream.pending() == 25
    built = walk(stream, grid_stops(4.0))
    assert built == 25 and stream.pending() == 0


def test_budget_caps_builds_per_poll() -> None:
    """budget builds per poll, never more; repeated polls drain the rest."""
    stream, _ = make_world(20261031, 25, 4.0, 400.0, ordered=False, budget=2)
    for _ in range(12):  # 25 sections, 2 per poll: 12 full polls...
        assert stream.poll([(0.0, 0.0, 0.0)]) == 2
    assert stream.pending() == 1
    assert stream.poll([(0.0, 0.0, 0.0)]) == 1  # ...then the odd tail
    assert stream.poll([(0.0, 0.0, 0.0)]) == 0  # nothing left
    assert stream.pending() == 0


def test_default_budget_unlimited_one_poll() -> None:
    stream, log = make_world(20261031, 10, 4.0, 400.0, ordered=False)
    assert stream.poll([(0.0, 0.0, 0.0)]) == 10  # math.inf default
    assert len(log) == 10


def test_radius_boundary_inclusive() -> None:
    """Luau `<=`: distance == radius builds; a hair beyond does not."""
    stream, _ = make_world(1, 1, 4.0, 10.0, ordered=False)
    assert stream.pending() == 1
    assert stream.poll([(10.0, 0.0, 0.0)]) == 1  # |d| == 10 exactly
    stream2, _ = make_world(1, 1, 4.0, 10.0, ordered=False)
    assert stream2.poll([(0.0, 6.0, 8.0)]) == 1  # 3-4-5 doubled, still == 10
    stream3, _ = make_world(1, 1, 4.0, 10.0, ordered=False)
    assert stream3.poll([(10.000001, 0.0, 0.0)]) == 0  # just over
    assert stream3.pending() == 1


def test_poll_positions_iterable_is_snapshotted() -> None:
    """The Luau re-iterates its positions table per section; the port must
    too, so a one-shot generator must behave like a list (Z4 fix note)."""
    stream, log = make_world(1, 5, 4.0, 400.0, ordered=False)
    positions = iter([(0.0, 0.0, 0.0), (16.0, 0.0, 0.0)])
    assert stream.poll(positions) == 5
    assert len(log) == 5


def test_small_world_generates_on_a_walk() -> None:
    """5x5 world, proximity radius 5 (overlapping neighbors), walker sweeps
    row-major; ordered mode must build in EXACT insertion order."""
    stream, log = make_world(20261031, 25, 4.0, 5.0, ordered=True, budget=3)
    built = walk(stream, grid_stops(4.0))
    assert built == 25
    assert stream.pending() == 0
    assert [entry[0] for entry in log] == list(range(25))  # strict insertion order
    # every build closure ran exactly once (done flags agree with the log)
    assert all(sec.done for sec in stream._sections)


def test_pending_and_add_after_poll() -> None:
    stream, _ = make_world(1, 3, 4.0, 400.0, ordered=False)
    assert stream.pending() == 3
    assert stream.poll([(0.0, 0.0, 0.0)]) == 3
    assert stream.pending() == 0
    stream.add((100.0, 0.0, 0.0), lambda: None)  # table.insert equivalence
    assert stream.pending() == 1
    assert stream.poll([(100.0, 0.0, 0.0)]) == 1
