"""Tests for mag.lattice_distance — Legendre three-square lattice invariant.

Provenance: watch/INTAKE_LEGENDRE_LATTICE_20260904.md (sqrt(7) impossibility
tweet, hand-verified).  Excluded family in 0..64: 7, 15, 23, 28, 31, 39, 47,
55, 60, 63 — where 28 = 4^1*(8*0+7) and 60 = 4^1*(8*1+7).
"""
from __future__ import annotations

import math

import pytest

from mag.lattice_distance import (
    excluded_form,
    is_three_square,
    lattice_distance_ok,
    validate_voxel_coords,
)


def _brute_force_three_square(n: int) -> bool:
    """Direct enumeration: is n = x^2 + y^2 + z^2 for some x,y,z >= 0?"""
    lim = int(math.isqrt(n))
    sq = [i * i for i in range(lim + 1)]
    return any(x + y + z == n for x in sq for y in sq for z in sq)


def test_classification_0_to_64():
    """Every n in 0..64 classified correctly against brute-force enumeration."""
    for n in range(65):
        assert is_three_square(n) == _brute_force_three_square(n), f"n={n}"


def test_named_excluded_members():
    """7/15/23/28/31 excluded — the intake card's cursed distances."""
    for n in (7, 15, 23, 28, 31, 39, 47, 55, 60, 63):
        assert not is_three_square(n), f"{n} should be excluded (4^a(8b+7))"
        assert not lattice_distance_ok(n)


def test_fourteen_included():
    """14 = 1 + 4 + 9, so sqrt(14) lives on the lattice (intake card)."""
    assert is_three_square(14)
    assert lattice_distance_ok(14)
    assert excluded_form(14) is None


def test_excluded_form_decomposition():
    assert excluded_form(7) == (0, 0)
    assert excluded_form(28) == (1, 0)
    assert excluded_form(60) == (1, 1)
    assert excluded_form(112) == (2, 0)
    assert excluded_form(14) is None
    assert excluded_form(0) is None
    assert excluded_form(-7) is None


def test_edge_cases():
    assert is_three_square(0)  # 0 = 0 + 0 + 0
    assert lattice_distance_ok(0)
    assert is_three_square(1) and is_three_square(2) and is_three_square(3)
    assert not is_three_square(-1)
    assert not lattice_distance_ok(-1)
    assert not lattice_distance_ok(2.5)  # non-integer d2 never on-grid
    assert lattice_distance_ok(7.0) is False  # integral float accepted
    assert lattice_distance_ok(14.0) is True


def test_property_vs_brute_force_to_512():
    """Up to 512: theorem classification == enumeration, both directions."""
    lim = int(math.isqrt(512))
    sq = [i * i for i in range(lim + 1)]
    sums = {x + y + z for x in sq for y in sq for z in sq}
    for n in range(513):
        if n in (0, 1):  # 0/1 handled, brute force covers them anyway
            pass
        assert is_three_square(n) == (n in sums), f"n={n}"


def test_lattice_distance_known_values():
    assert lattice_distance_ok(4)   # distance 2 (dx=2,dy=0,dz=0)
    assert lattice_distance_ok(9)   # distance 3
    assert lattice_distance_ok(3)   # body diagonal sqrt(3)
    assert not lattice_distance_ok(7)   # the famous sqrt(7) — impossible
    assert not lattice_distance_ok(15)
    assert not lattice_distance_ok(23)
    assert not lattice_distance_ok(28)


def test_voxel_coords_clean_set():
    pts = [(0, 0, 0), (1, 1, 1), (2, 0, 0), (1, 2, 2)]
    result = validate_voxel_coords(pts)
    assert result["ok"] is True
    assert result["violations"] == []
    assert result["pairs_checked"] == 6


def test_voxel_coords_deliberate_violation_detected():
    # A "grid" that measures sqrt(7) between two supposed voxel centers:
    # the exact falsifier from the intake card — this space is NOT Z^3.
    pts = [(0, 0, 0), (1, 1, 1), (math.sqrt(7), 0, 0)]
    result = validate_voxel_coords(pts)
    assert result["ok"] is False
    assert len(result["violations"]) == 1
    v = result["violations"][0]
    assert v["d2"] == 7
    assert v["form"] == [0, 0]
    assert v["a"] == (0, 0, 0)


def test_voxel_coords_doubled_grid_still_clean():
    # A uniformly scaled integer grid (unit=2) keeps d2 = 4*(dx^2+dy^2+dz^2);
    # d2 = 4^1 * (non-excluded) passes the family check for non-(8b+7) cores.
    pts = [(0, 0, 0), (2, 2, 2)]  # d2 = 12 -> fine (12 not 4^a(8b+7))
    result = validate_voxel_coords(pts)
    assert result["ok"] is True


def test_voxel_coords_malformed_skipped():
    result = validate_voxel_coords([(0, 0, 0), (1, 1), "junk", (1, 1, 1)])
    assert result["ok"] is True
    assert result["pairs_checked"] == 1


def test_voxel_coords_empty():
    result = validate_voxel_coords([])
    assert result == {"ok": True, "violations": [], "pairs_checked": 0}
