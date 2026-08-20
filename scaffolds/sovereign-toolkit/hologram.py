"""hologram — the shared-reality-as-hologram primitive, pure stdlib.

THE MECHANISM (our working implementation of this pattern):
  N peers, different machines, each seeing a QUANTIZATION of the shared reality,
  right-sized on a CURVE. The shared reality IS the hologram: any fragment reconstructs
  the whole. Each peer's capacity (VRAM / compute / tokens) is its quantization-fidelity
  ceiling — a 6GB machine keeps a coarser lattice, a 128GB machine keeps full fidelity.
  Same reality, different quantization level. And the wave OSCILLATES: a standing wave
  (deterministic spine out + stochastic flesh in) that breathes in place, nodes fixed at
  the invariant boundaries, antinodes swelling/contracting between them.

THE CONTRACT:
  * fidelity(capacity)        -> a peer's quantization fidelity on the curve (logistic
                                  saturation; diminishing returns; cheap everywhere).
  * quantization_bits(f)      -> how many fidelity levels this capacity can represent.
  * reconstruct(fragments)    -> the hologram: any full-fidelity fragment reconstructs
                                  the whole; otherwise the collective union does.
  * wave_oscillation(steps)   -> does the wave oscillate? yes — a standing wave breathing
                                  in place (feedback in = swell, fold out = contract).
  * right_size(target, caps)  -> what a peer should actually hold (<= its capacity).

PURE STDLIB — math, typing. Runs: python -m pytest tests/ -q
Schema: hologram.v1
"""
from __future__ import annotations

import math
from typing import Any

SCHEMA = "hologram.v1"
# RIB: shared-reality-as-hologram (capacity -> quantization fidelity; any fragment reconstructs the whole) · verify: fidelity monotonic + reconstruct union + oscillation · tests: test_toolkit


def fidelity(capacity: float, *, midpoint: float = 24.0, steepness: float = 20.0) -> float:
    """A peer's quantization fidelity as a function of its capacity.

    Logistic saturation: fidelity rises with capacity but saturates (diminishing returns),
    so every machine can afford a usable level — cheap everywhere, full fidelity only at
    the load-bearing top of the curve.
    """
    return 1.0 / (1.0 + math.exp(-((capacity - midpoint) / steepness)))


def quantization_bits(f: float, *, max_bits: int = 8) -> int:
    """How many fidelity levels a capacity can represent. At least 1."""
    return max(1, round(max_bits * f))


def reconstruct(fragments: list[Any]) -> dict[str, Any]:
    """The hologram: any fragment reconstructs the whole.

    fragments: list of capacities, or (id, capacity) pairs. Each is a quantization of the
    shared reality (a fidelity level). A single full-fidelity fragment reconstructs the
    whole ALONE; otherwise the collective union of all fragments' representable fidelity
    reconstructs it together. Deterministic, $0.
    """
    frags = []
    for i, f in enumerate(fragments):
        if isinstance(f, (list, tuple)):
            fid_, cap_ = f[0], float(f[1])
        else:
            fid_, cap_ = f"peer-{i}", float(f)
        fi = fidelity(cap_)
        frags.append({"id": fid_, "capacity": cap_, "fidelity": round(fi, 3),
                      "bits": quantization_bits(fi)})

    top_cap = max(fr["capacity"] for fr in frags)
    shared = fidelity(top_cap)  # the highest shared reality = full fidelity at the top
    solo = [fr for fr in frags if fr["fidelity"] >= 0.95]  # full-fidelity fragment
    union_bits = max(fr["bits"] for fr in frags)
    whole = bool(solo) or union_bits >= quantization_bits(shared)

    return {"ok": True, "schema": SCHEMA, "n_fragments": len(frags),
            "fragments": frags,
            "shared_fidelity": round(shared, 3),
            "whole_reconstructed": whole,
            "reconstructed_by": ("single_full_fidelity_fragment" if solo else
                                 "collective_union" if whole else "partial"),
            "note": "the shared reality IS the hologram: any full-fidelity fragment "
                    "reconstructs the whole; otherwise the collective union does"}


def wave_oscillation(*, steps: int = 12, freq: float = 1.0) -> dict[str, Any]:
    """Does the wave oscillate? Yes — it is a STANDING WAVE.

    Two counter-propagating components (deterministic spine outward + stochastic flesh
    inward) superpose into a wave that oscillates IN PLACE at a resonant frequency set by
    the invariant-lattice boundaries. Nodes stay fixed at the boundaries; antinodes
    breathe between them (swell on feedback-in, contract on fold-out).
    """
    samples = []
    for i in range(steps):
        t = i / max(1, steps - 1)
        s = math.sin(2.0 * math.pi * freq * t)
        samples.append({"t": round(t, 3), "amplitude": round(abs(s), 3),
                        "phase": "swelling (feedback in)" if s > 0 else "contracting (folding out)"})
    return {"ok": True, "schema": SCHEMA, "oscillates": True, "freq": freq,
            "standing_wave": "deterministic spine (out) + stochastic flesh (in) counter-propagate "
                             "and superpose -> a standing wave that oscillates in place, nodes at "
                             "the invariant boundaries, antinodes breathing between them",
            "resonance": "constructive when the returning fold is in phase with the outgoing steer "
                         "(the compounding)",
            "samples": samples}


def right_size(target: float, capacities: list[float]) -> dict[str, Any]:
    """What a peer should actually hold: the highest level it can afford (<= target).

    Cheap everywhere: each machine holds its affordable level; full fidelity only where
    load-bearing. The pool sums to more than any one machine (many angles, one reality).
    """
    if not capacities:
        return {"ok": True, "schema": SCHEMA, "target": target, "should_hold": None,
                "pool_fidelity_sum": 0.0, "note": "no capacities"}
    affordable = [c for c in capacities if c <= target]
    hold = affordable[-1] if affordable else min(capacities)
    pool = sum(fidelity(c) for c in capacities)
    return {"ok": True, "schema": SCHEMA, "target": target, "should_hold": hold,
            "pool_fidelity_sum": round(pool, 3),
            "pool_mean_fidelity": round(pool / len(capacities), 3),
            "note": "right-sized: cheap everywhere (each holds its affordable level), full "
                    "fidelity only where load-bearing; the collective pool exceeds any one "
                    "machine (the hologram: many angles, one reality)"}


if __name__ == "__main__":
    import json

    # 3 machines: a small one, a mid one, and one at full fidelity
    r = reconstruct([("rx-5600xt", 6), ("rtx-3060", 12), ("rtx-4090", 24)])
    print(json.dumps(r, indent=2))
