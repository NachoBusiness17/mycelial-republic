"""Stateless tests for mag.bare_numpy — our own minimal numerical core (deterministic, $0, zero deps)."""
from __future__ import annotations

import math

from mag.bare_numpy import BArray, amax, amin, apply, dot, from_list, magnitude, mean, normalize, ones, zeros


def test_construction_and_shape():
    a = from_list([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    assert a.shape() == (2, 3)
    z = zeros(2, 3)
    assert z.shape() == (2, 3) and amax(z) == 0.0 and amin(z) == 0.0
    o = ones(2)
    assert o.shape() == (2, 1) and amin(o) == 1.0


def test_elementwise():
    a = from_list([[1.0, 2.0], [3.0, 4.0]])
    b = from_list([[10.0, 20.0], [30.0, 40.0]])
    assert (a + b).to_list() == [[11.0, 22.0], [33.0, 44.0]]
    assert (b - a).to_list() == [[9.0, 18.0], [27.0, 36.0]]
    assert (a * 2).to_list() == [[2.0, 4.0], [6.0, 8.0]]
    assert (b / a).to_list() == [[10.0, 10.0], [10.0, 10.0]]


def test_reductions():
    a = from_list([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    assert mean(a) == 3.5
    assert amin(a) == 1.0
    assert amax(a) == 6.0


def test_normalize_range_0_1():
    a = from_list([[0.0, 5.0, 10.0]])
    n = normalize(a)
    assert n.to_list() == [[0.0, 0.5, 1.0]]


def test_dot():
    a = from_list([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    assert dot(a, [1.0, 1.0, 1.0]) == [6.0, 15.0]


def test_apply_and_magnitude():
    a = from_list([[1.0, 2.0]])
    assert apply(a, lambda x: x * x).to_list() == [[1.0, 4.0]]
    assert abs(magnitude(from_list([[3.0, 4.0]])) - 5.0) < 1e-9


def test_deterministic_same_input_same_output():
    a = from_list([[0.0, 2.0, 4.0]])
    assert normalize(a).to_list() == normalize(a).to_list()
    assert dot(a, [1.0, 1.0, 1.0]) == dot(a, [1.0, 1.0, 1.0])
