"""tests for vram_hologram — 10 machines, different VRAM/compute, each a quantization of the shared
reality on a right-sized curve; and does the wave oscillate (yes — a standing wave).

RIB (frozen spec):
  quantization_curve() -> each machine's quantization fidelity as a function of VRAM/compute,
                          right-sized (saturates). More VRAM -> finer quantization.
  wave_oscillation()   -> DOES THE WAVE OSCILLATE? Yes — a standing wave (spine out + flesh in
                          superpose, oscillates in place, nodes at boundaries). Samples amplitude.
  right_size()         -> what a machine (or the pool) should hold (cheap everywhere, full only at
                          load-bearing).
  collective_reality() -> the pool: curve + oscillation + rightsize + shared-invariant dedupe.

Contract: grounded in vram_memory's VRAM-ceiling + standing-wave/fluid physics; deterministic + $0,
pure math; honest (never over-claims real VRAM telemetry it didn't measure).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import vram_hologram  # noqa: E402


def test_quantization_curve_right_sized():
    c = vram_hologram.quantization_curve()
    assert c["ok"] is True
    assert c["n_machines"] == 10
    # more VRAM -> higher fidelity (the curve is monotonic in the machine list)
    fidelities = [l["fidelity"] for l in sorted(c["levels"], key=lambda x: x["vram_gb"])]
    assert fidelities == sorted(fidelities)  # non-decreasing
    # fidelity saturates (the top machine is near 1.0, the bottom much lower)
    assert fidelities[-1] > fidelities[0]
    assert "quantization_bits" in c["levels"][0]


def test_wave_oscillates():
    o = vram_hologram.wave_oscillation(steps=8)
    assert o["ok"] is True
    assert o["oscillates"] is True  # yes, the wave oscillates
    assert "standing_wave" in o and "resonance" in o
    assert len(o["samples"]) == 8
    # amplitude breathes over time (some samples differ)
    amps = {s["amplitude"] for s in o["samples"]}
    assert len(amps) > 1


def test_right_size_holds_affordable_level():
    r = vram_hologram.right_size(target_vram=12)
    assert r["ok"] is True
    assert r["should_hold"]["vram_gb"] <= 12  # never holds more than it can afford
    assert r["pool_fidelity_sum"] > 0


def test_collective_reality_pool():
    c = vram_hologram.collective_reality()
    assert c["ok"] is True
    assert "curve" in c and "oscillation" in c and "rightsize" in c
    assert c["honesty"]
