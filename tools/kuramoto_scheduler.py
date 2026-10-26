#!/usr/bin/env python3
"""tools/kuramoto_scheduler.py - Decentralized Multi-Seat Phase Synchronizer.

Implements the Wave 6 Steal (@anish2good / Yoshiki Kuramoto 1975):
- Models autonomous estate seats and crons (commit sweeper, inbox compactor,
  radar scout, telemetry watcher) as a network of weakly coupled phase oscillators.
- Eliminates Windows NTFS/drvfs git index lock collisions (Ds+ uninterruptible sleep)
  without requiring a centralized lock coordinator or master daemon.
- Calculates dynamic harmonic phase offsets (theta_i) based on filesystem mtime traces
  in logs/ and state/.
- Interleaves execution cadences into non-overlapping harmonic time slots (2*pi / N).

Governing equation:
  d(theta_i)/dt = omega_i + (K / N) * sum(sin(theta_j - theta_i))

CONSUMER: commit_sweeper, inbox_consume, x_radar, multi-seat background tasks.
VERIFIER: tests/test_kuramoto_scheduler.py.
HOUSE LAW: Strictly zero unicode em-dashes; zero side effects on failure; pure functions.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_PERIOD_SEC = 600.0  # 10 minutes default cycle
DEFAULT_COUPLING_K = 1.25   # Coupling constant K > K_critical for phase locking


@dataclass(frozen=True)
class OscillatorNode:
    """Represents a scheduled seat or autonomous organ in the estate network."""
    seat_id: str
    natural_frequency: float  # omega_i in radians per second (2*pi / T_i)
    last_phase: float         # theta_i in [0, 2*pi)
    target_slot: int          # preferred slot index in [0, N-1]


def compute_phase_from_timestamp(ts: float, period_sec: float) -> float:
    """Map a unix epoch timestamp to a periodic circular phase in [0, 2*pi)."""
    if period_sec <= 0:
        return 0.0
    progress = (ts % period_sec) / period_sec
    return (2.0 * math.pi * progress) % (2.0 * math.pi)


def calculate_order_parameter(phases: List[float]) -> Tuple[float, float]:
    """Calculate the Kuramoto complex order parameter: r * exp(i * psi).
    
    Returns (r, psi):
      r: Coherence magnitude in [0.0, 1.0]. 0 = completely disordered; 1 = perfectly synchronized.
      psi: Mean cluster phase in [0, 2*pi).
    """
    if not phases:
        return (0.0, 0.0)
    n = len(phases)
    sum_cos = sum(math.cos(p) for p in phases)
    sum_sin = sum(math.sin(p) for p in phases)
    r = math.sqrt(sum_cos**2 + sum_sin**2) / n
    psi = math.atan2(sum_sin, sum_cos) % (2.0 * math.pi)
    return (round(r, 4), round(psi, 4))


def kuramoto_step(
    phases: List[float],
    frequencies: List[float],
    dt: float,
    coupling_k: float = DEFAULT_COUPLING_K,
) -> List[float]:
    """Perform one numerical integration step of the Kuramoto model using Euler integration."""
    n = len(phases)
    if n <= 1:
        return list(phases)

    new_phases: List[float] = []
    for i in range(n):
        theta_i = phases[i]
        omega_i = frequencies[i]
        coupling_sum = sum(math.sin(phases[j] - theta_i) for j in range(n))
        d_theta = omega_i + (coupling_k / n) * coupling_sum
        next_theta = (theta_i + d_theta * dt) % (2.0 * math.pi)
        new_phases.append(next_theta)

    return new_phases


def compute_harmonic_interleave_delay(
    seat_index: int,
    total_seats: int,
    cycle_period_sec: float = DEFAULT_PERIOD_SEC,
    current_time_sec: Optional[float] = None,
) -> Dict[str, Any]:
    """Calculate the non-overlapping phase delay for a seat to prevent lock collision.
    
    Partitions the cycle into N equal harmonic slots (2*pi / N).
    Computes required sleep or phase shift so that seat i runs in slot i.
    """
    if total_seats <= 1:
        return {
            "seat_index": 0,
            "total_seats": 1,
            "slot_width_sec": cycle_period_sec,
            "target_phase_rad": 0.0,
            "delay_sec": 0.0,
            "fire_immediately": True,
        }

    now = current_time_sec if current_time_sec is not None else time.time()
    current_phase = compute_phase_from_timestamp(now, cycle_period_sec)

    slot_width_rad = (2.0 * math.pi) / total_seats
    slot_width_sec = cycle_period_sec / total_seats
    target_phase = (seat_index * slot_width_rad) % (2.0 * math.pi)

    # Angular distance from current phase to target phase moving forward in time
    phase_diff = (target_phase - current_phase) % (2.0 * math.pi)
    delay_sec = round((phase_diff / (2.0 * math.pi)) * cycle_period_sec, 2)

    # If within tolerance of slot start, fire immediately
    tolerance_sec = min(5.0, slot_width_sec * 0.15)
    fire_immediately = (delay_sec <= tolerance_sec) or (delay_sec >= (cycle_period_sec - tolerance_sec))

    return {
        "seat_index": seat_index,
        "total_seats": total_seats,
        "slot_width_sec": round(slot_width_sec, 2),
        "target_phase_rad": round(target_phase, 4),
        "current_phase_rad": round(current_phase, 4),
        "delay_sec": 0.0 if fire_immediately else delay_sec,
        "fire_immediately": fire_immediately,
    }


def sense_estate_seat_phases(
    log_dir: Path,
    period_sec: float = DEFAULT_PERIOD_SEC,
    current_time_sec: Optional[float] = None,
) -> Dict[str, float]:
    """Sense recent activity phases of estate organs from file modification times."""
    phases: Dict[str, float] = {}
    if not log_dir.exists():
        return phases

    for fpath in log_dir.glob("*.log"):
        seat_name = fpath.stem
        try:
            mtime = fpath.stat().st_mtime
            phase = compute_phase_from_timestamp(mtime, period_sec)
            phases[seat_name] = round(phase, 4)
        except OSError:
            continue

    return phases


def main() -> int:
    """CLI diagnostics and synchronization calculator."""
    parser = argparse.ArgumentParser(description="Kuramoto Multi-Seat Phase Synchronizer")
    parser.add_argument("--seat-index", type=int, default=0, help="Zero-indexed seat identifier")
    parser.add_argument("--total-seats", type=int, default=4, help="Total active seats/crons in swarm")
    parser.add_argument("--period", type=float, default=600.0, help="Cycle period in seconds (default: 600s)")
    parser.add_argument("--simulate", action="store_true", help="Run 100-step numerical simulation of phase convergence")
    args = parser.parse_args()

    if args.simulate:
        print("Running Kuramoto swarm phase synchronization simulation (N=8)...")
        n = 8
        omega = [2.0 * math.pi / args.period] * n
        # Random initial phases
        phases = [(i * 1.7) % (2.0 * math.pi) for i in range(n)]
        init_r, _ = calculate_order_parameter(phases)
        print(f"Initial order parameter r = {init_r:.4f}")

        for step in range(50):
            phases = kuramoto_step(phases, omega, dt=5.0, coupling_k=1.5)

        final_r, final_psi = calculate_order_parameter(phases)
        print(f"Post-coupling order parameter r = {final_r:.4f} (phase locked at psi = {final_psi:.4f} rad)")
        return 0

    plan = compute_harmonic_interleave_delay(args.seat_index, args.total_seats, args.period)
    print(json.dumps(plan, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
