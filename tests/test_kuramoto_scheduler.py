"""tests/test_kuramoto_scheduler.py - Verification for Kuramoto Multi-Seat Synchronizer."""
from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.kuramoto_scheduler import (
    calculate_order_parameter,
    compute_harmonic_interleave_delay,
    compute_phase_from_timestamp,
    kuramoto_step,
)


def test_phase_mapping():
    # 0 sec in 600s cycle -> 0 rad
    assert compute_phase_from_timestamp(0.0, 600.0) == 0.0
    # 300 sec in 600s cycle -> pi rad
    phase_half = compute_phase_from_timestamp(300.0, 600.0)
    assert math.isclose(phase_half, math.pi, rel_tol=1e-5)
    # 600 sec -> 0 rad (modulo)
    phase_full = compute_phase_from_timestamp(600.0, 600.0)
    assert math.isclose(phase_full, 0.0, abs_tol=1e-5)


def test_order_parameter():
    # Perfectly synchronized phases: r == 1.0
    synced = [1.2, 1.2, 1.2, 1.2]
    r_synced, psi = calculate_order_parameter(synced)
    assert math.isclose(r_synced, 1.0, abs_tol=1e-3)
    assert math.isclose(psi, 1.2, abs_tol=1e-3)

    # Disordered phases evenly distributed around circle: r ~ 0
    dispersed = [0.0, math.pi / 2, math.pi, 3 * math.pi / 2]
    r_disp, _ = calculate_order_parameter(dispersed)
    assert math.isclose(r_disp, 0.0, abs_tol=1e-3)


def test_kuramoto_convergence():
    n = 6
    omega = [0.1] * n
    # Start dispersed
    phases = [0.2, 1.5, 2.7, 3.9, 4.8, 5.9]
    init_r, _ = calculate_order_parameter(phases)
    assert init_r < 0.2

    # Integrate forward under strong coupling
    for _ in range(50):
        phases = kuramoto_step(phases, omega, dt=0.5, coupling_k=2.5)

    final_r, _ = calculate_order_parameter(phases)
    # Should have achieved strong phase locking
    assert final_r > init_r
    assert final_r > 0.85


def test_harmonic_interleaving_slots():
    total_seats = 4
    period = 600.0
    current_time = 0.0  # At cycle start (phase 0)

    delays = []
    for seat_i in range(total_seats):
        plan = compute_harmonic_interleave_delay(
            seat_index=seat_i,
            total_seats=total_seats,
            cycle_period_sec=period,
            current_time_sec=current_time,
        )
        delays.append(plan["delay_sec"])

    # Seat 0 fires immediately (delay 0)
    assert delays[0] == 0.0
    # Seat 1 fires at 150s
    assert math.isclose(delays[1], 150.0, abs_tol=1.0)
    # Seat 2 fires at 300s
    assert math.isclose(delays[2], 300.0, abs_tol=1.0)
    # Seat 3 fires at 450s
    assert math.isclose(delays[3], 450.0, abs_tol=1.0)


def test_em_dash_cleanliness():
    tool_file = os.path.join(ROOT, "tools", "kuramoto_scheduler.py")
    test_file = os.path.join(ROOT, "tests", "test_kuramoto_scheduler.py")
    for fpath in [tool_file, test_file]:
        content = open(fpath, "r", encoding="utf-8").read()
        assert "\u2014" not in content, f"Forbidden unicode em-dash found in {fpath}"


if __name__ == "__main__":
    test_phase_mapping()
    test_order_parameter()
    test_kuramoto_convergence()
    test_harmonic_interleaving_slots()
    test_em_dash_cleanliness()
    print("ALL TESTS PASSED in test_kuramoto_scheduler.py")
