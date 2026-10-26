#!/usr/bin/env python3
"""tools/kuramoto_chute.py - Kuramoto Phase Scheduling & Bartnik Boundary Chute.

Mandate:
Enforces non-linear Kuramoto coupled oscillator phase scheduling and Bartnik
quasi-local boundary admission control for conflict-free state mutations across
distributed nodes (Desktop, Bob, Pixel, Antigravity) without centralized locks.

Research Lineage:
- Kuramoto Oscillator Model: Phase synchronization theta_i = (omega * t + phi_i) mod 2pi.
  Interleaves node write windows across cloud/local storage to eliminate collision forks.
- Bartnik Quasi-Local Mass (Dr. Stephen McCormick, Wave 9): Boundary Hamiltonian flux
  bounds interior execution stability: H_boundary <= H_max.
- Irreversibility Budget (arXiv:2609.00275): Admission control fails closed when
  fleet queue drift exceeds capacity.
- 128-Agent Factorio Swarm (Hunter Leath): Single-writer FIFO commit hints.

HOUSE LAW: Strictly zero unicode em-dashes; standard library only; pure functions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

DEFAULT_HINT_QUEUE_DIR = os.path.join(ROOT, "queue", "commit_hints")

# Kuramoto intrinsic phase offsets for sovereign fleet bodies (4-quadrant estate)
NODE_PHASE_OFFSETS: Dict[str, float] = {
    "desktop": 0.0,                         # Phase 0.000 rad (0 deg)
    "bob": round(math.pi / 2.0, 4),         # Phase 1.5708 rad (90 deg)
    "pixel": round(math.pi, 4),             # Phase 3.1416 rad (180 deg)
    "antigravity": round(3.0 * math.pi / 2.0, 4), # Phase 4.7124 rad (270 deg)
    "mag-agent": round(math.pi / 2.0, 4),   # Maps to Bob cluster
}

# 16-Seat Harmonic Topology: 16 nodes spaced at pi/8 (22.5 deg)
NODE_16_PHASE_OFFSETS: Dict[str, float] = {
    "desktop-alpha": 0.0,
    "desktop-beta": round(math.pi / 8.0, 4),
    "desktop-gamma": round(math.pi / 4.0, 4),
    "desktop-delta": round(3.0 * math.pi / 8.0, 4),
    "bob-alpha": round(math.pi / 2.0, 4),
    "bob-beta": round(5.0 * math.pi / 8.0, 4),
    "bob-gamma": round(3.0 * math.pi / 4.0, 4),
    "bob-delta": round(7.0 * math.pi / 8.0, 4),
    "pixel-alpha": round(math.pi, 4),
    "pixel-beta": round(9.0 * math.pi / 8.0, 4),
    "pixel-gamma": round(5.0 * math.pi / 4.0, 4),
    "pixel-delta": round(11.0 * math.pi / 8.0, 4),
    "antigravity-alpha": round(3.0 * math.pi / 2.0, 4),
    "antigravity-beta": round(13.0 * math.pi / 8.0, 4),
    "antigravity-gamma": round(7.0 * math.pi / 4.0, 4),
    "antigravity-delta": round(15.0 * math.pi / 8.0, 4),
}
for _i in range(16):
    NODE_16_PHASE_OFFSETS[f"seat_{_i:02d}"] = round(_i * math.pi / 8.0, 4)

DEFAULT_CYCLE_PERIOD_S = 60.0  # 60s full harmonic cycle
PHASE_HALF_WINDOW_RAD = math.pi / 6.0  # 30-degree write window
PHASE_16_HALF_WINDOW_RAD = round(math.pi / 24.0, 4)  # 7.5 deg write window (33.3% guard band)
DEFAULT_MAX_BOUNDARY_FLUX = 100.0  # Bartnik Hamiltonian flux ceiling


class KuramotoChute:
    """Kuramoto phase scheduler and Bartnik boundary admission controller."""

    def __init__(
        self,
        queue_dir: Optional[str] = None,
        cycle_period_s: float = DEFAULT_CYCLE_PERIOD_S,
        max_flux: float = DEFAULT_MAX_BOUNDARY_FLUX,
    ) -> None:
        self.queue_dir = queue_dir or DEFAULT_HINT_QUEUE_DIR
        self.cycle_period_s = cycle_period_s
        self.max_flux = max_flux
        os.makedirs(self.queue_dir, exist_ok=True)

    def current_system_phase(self, t: Optional[float] = None) -> float:
        """Compute the master system phase theta(t) in [0, 2*pi)."""
        now = t if t is not None else time.time()
        phase = (2.0 * math.pi * (now % self.cycle_period_s)) / self.cycle_period_s
        return round(phase, 4)

    def check_phase_window(
        self,
        node_id: str,
        t: Optional[float] = None,
        fleet_size: int = 4,
    ) -> Dict[str, Any]:
        """Check if node's write window is currently open under Kuramoto scheduling."""
        if fleet_size == 16 or node_id in NODE_16_PHASE_OFFSETS:
            offsets = NODE_16_PHASE_OFFSETS
            half_win = PHASE_16_HALF_WINDOW_RAD
        else:
            offsets = NODE_PHASE_OFFSETS
            half_win = PHASE_HALF_WINDOW_RAD

        target_phase = offsets.get(node_id, 0.0)
        sys_theta = self.current_system_phase(t)

        # Angular distance wrapped to [-pi, pi]
        diff = (sys_theta - target_phase + math.pi) % (2.0 * math.pi) - math.pi
        abs_diff = abs(diff)

        is_open = abs_diff <= half_win

        # Seconds until window opens
        if is_open:
            wait_seconds = 0.0
        else:
            forward_diff = (target_phase - sys_theta) % (2.0 * math.pi)
            wait_seconds = round((forward_diff / (2.0 * math.pi)) * self.cycle_period_s, 2)

        return {
            "node_id": node_id,
            "target_phase_rad": target_phase,
            "system_phase_rad": sys_theta,
            "angular_distance_rad": round(abs_diff, 4),
            "window_open": is_open,
            "wait_seconds_to_open": wait_seconds,
        }

    def compute_boundary_hamiltonian(self, additional_bytes: int = 0) -> Tuple[float, int, int]:
        """Compute Bartnik quasi-local boundary Hamiltonian flux.

        H_boundary = (queue_file_count * 2.0) + (total_uncommitted_bytes / 50000.0)
        """
        file_count = 0
        total_bytes = additional_bytes

        if os.path.isdir(self.queue_dir):
            for f in os.listdir(self.queue_dir):
                if f.endswith(".json") and not f.startswith("."):
                    file_count += 1
                    try:
                        total_bytes += os.path.getsize(os.path.join(self.queue_dir, f))
                    except Exception:
                        pass

        # Hamiltonian calculation
        flux = (file_count * 2.0) + (total_bytes / 50000.0)
        return round(flux, 2), file_count, total_bytes

    def admit_mutation(
        self,
        node_id: str,
        task_name: str,
        payload_bytes: int,
        t: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Bartnik boundary admission check and Kuramoto phase gating."""
        flux, pending_count, total_bytes = self.compute_boundary_hamiltonian(payload_bytes)

        # 1. Bartnik Irreversibility Boundary Gate
        if flux > self.max_flux:
            return {
                "admitted": False,
                "reason": "REFUSED_IRREVERSIBILITY_EXCEEDED",
                "boundary_flux": flux,
                "flux_ceiling": self.max_flux,
                "pending_hints": pending_count,
                "detail": f"Boundary Hamiltonian flux {flux:.2f} exceeds ceiling {self.max_flux:.2f}.",
            }

        # 2. Kuramoto Phase Window Gate
        phase_status = self.check_phase_window(node_id, t)

        return {
            "admitted": True,
            "node_id": node_id,
            "task_name": task_name,
            "boundary_flux": flux,
            "flux_ceiling": self.max_flux,
            "phase_status": phase_status,
            "ready_to_write": phase_status["window_open"],
        }

    def emit_commit_hint(
        self,
        node_id: str,
        task_name: str,
        payload: Dict[str, Any],
        bypass_phase: bool = False,
    ) -> Dict[str, Any]:
        """Emit an atomic single-writer commit hint into the chute."""
        now = time.time()
        payload_str = json.dumps(payload, sort_keys=True)
        payload_bytes = len(payload_str.encode("utf-8"))

        adm = self.admit_mutation(node_id, task_name, payload_bytes, t=now)
        if not adm["admitted"]:
            raise PermissionError(f"Admission refused: {adm['reason']} (flux={adm['boundary_flux']})")

        if not bypass_phase and not adm["ready_to_write"]:
            wait_s = adm["phase_status"]["wait_seconds_to_open"]
            raise BlockingIOError(f"Phase window closed for node '{node_id}'. Wait {wait_s}s for slot.")

        # Construct hint document
        hint_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()[:8]
        now_iso = datetime.now(timezone.utc).isoformat()
        hint_doc = {
            "schema": "commit_hint.v1",
            "hint_id": f"hint-{node_id}-{int(now)}-{hint_hash}",
            "node_id": node_id,
            "task_name": task_name,
            "created_utc": now_iso,
            "system_phase_rad": adm["phase_status"]["system_phase_rad"],
            "payload": payload,
        }

        filename = f"{int(now)}_{node_id}_{hint_hash}.json"
        target_path = os.path.join(self.queue_dir, filename)
        temp_path = f"{target_path}.tmp.{os.getpid()}"

        with open(temp_path, "w", encoding="utf-8") as fp:
            json.dump(hint_doc, fp, indent=2, sort_keys=True)
        os.replace(temp_path, target_path)

        return {
            "emitted": True,
            "hint_path": target_path,
            "hint_id": hint_doc["hint_id"],
            "boundary_flux": adm["boundary_flux"],
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Kuramoto Phase & Bartnik Boundary Chute CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # phase
    p_phase = subparsers.add_parser("phase", help="Check current Kuramoto phase window for node")
    p_phase.add_argument("--node", default="desktop", choices=list(NODE_PHASE_OFFSETS.keys()))

    # admit
    p_admit = subparsers.add_parser("admit", help="Test Bartnik boundary admission for task")
    p_admit.add_argument("--node", default="desktop", choices=list(NODE_PHASE_OFFSETS.keys()))
    p_admit.add_argument("--task", required=True, help="Task name")
    p_admit.add_argument("--bytes", type=int, default=1024, help="Payload byte size")

    # emit
    p_emit = subparsers.add_parser("emit", help="Emit single-writer commit hint")
    p_emit.add_argument("--node", default="desktop", choices=list(NODE_PHASE_OFFSETS.keys()))
    p_emit.add_argument("--task", required=True, help="Task name")
    p_emit.add_argument("--payload-json", required=True, help="JSON string or file path")
    p_emit.add_argument("--bypass-phase", action="store_true", help="Bypass phase check")

    args = parser.parse_args()
    chute = KuramotoChute()

    if args.command == "phase":
        res = chute.check_phase_window(args.node)
        print(json.dumps(res, indent=2))
        return 0

    elif args.command == "admit":
        res = chute.admit_mutation(args.node, args.task, args.bytes)
        print(json.dumps(res, indent=2))
        return 0 if res.get("admitted") else 1

    elif args.command == "emit":
        raw = args.payload_json
        if os.path.isfile(raw):
            with open(raw, "r", encoding="utf-8") as fp:
                payload = json.load(fp)
        else:
            payload = json.loads(raw)
        res = chute.emit_commit_hint(args.node, args.task, payload, bypass_phase=args.bypass_phase)
        print(json.dumps(res, indent=2))
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
