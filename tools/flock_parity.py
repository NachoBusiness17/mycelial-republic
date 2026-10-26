"""flock_parity v0 — GDScript flock vs Python flock, measured (Q14, V2ASK3).

The estate's flock exists in FOUR implementations with no cross-check:
  dashboard/static/games/swarm.html (JS original) · roblox/src/shared/Flock.luau
  (Luau original) · roblox_to_godot/systems/flock.gd (the game's engine)
  · mag/flock_positive.py step_threat (the per-line Python port).
V2ASK3 (watch/inbox/frontier_asks/volley2/results/V2ASK3.md) ruled the first
pair: GDScript <-> Python — the hardest precision problem first (Godot
Vector2 is float32, Python is float64), both ends already proven by the
rule_parity.py water harness. Every other implementation pairs against the
Python reference later (JS, Luau) — N-1 harnesses, never N(N-1)/2.

THE COMPARISON LAW (V2ASK3: float boids are chaotic; two implementations
differing by one ulp at tick 0 diverge visibly within tens-to-hundreds of
ticks, so free-running trajectory compare is NOT the law):

  Teacher-forced single-step compare. Each tick both sides receive the SAME
  canonical input frame and produce ONE output; the next tick's input is the
  reference's (Python's) output quantized to float32 — never either side's
  own running state — so per-tick error cannot compound across ticks. A
  free-running lane is kept only as a flock-level smoke (centroid + spread).

  Tier D (discrete decisions) must match exactly: alive, caught, the flee
  flag, neighbour id sets. The one sanctioned exception is the threshold
  band: a decision whose |d^2 - R^2| <= 8*ulp32(R^2) (fatigue decisions:
  |f - TIRED| <= 8*ulp32(TIRED)) is excluded from the exact check and
  logged as `edge` — float32-vs-float64 distance math legitimately
  disagrees at the radius.

  Tier C (continuous state) must match within the NAMED EPSILON (floats,
  not integers):
      |a - b| <= K * ulp32(max(|a|, |b|)) + 2e-6
  K = 32 for pos/vel (TOLERANCE_EXCEPTIONS: every component passes through
  sin/cos wiggle + pow drag, and the school loop accumulates up to N-1
  float32 roundings per tick — V2ASK3's 16-ulp transcendental floor widened
  for the accumulation) and K = 4 for fatigue/satiation (pure float64
  arithmetic on both sides: GDScript Dictionary floats are 64-bit Variants;
  no transcendentals). ulp32(x) = one float32 unit-in-the-last-place at |x|
  (2^(e-150) normals, 2^-149 subnormal). 1e-6*dt absorbs near-zero
  cancellation.

  Constants guard (the Q15 link): frames carry constants_hash = sha256 over
  "NAME=<float32 bits>" lines of game_constants.gd's flock family. The
  GDScript runner recomputes it from its preload and exits 3 on mismatch —
  constant drift is a harness error, never a mysterious position diff.

Floats travel as float32 bit patterns in hex ("0x%08x") — decimal JSON
parses differently per runtime and corrupts integers above 2^53; the bits
are the only shared alphabet (both codecs hand-compose little-endian bytes,
proven lossless by the flockcodec echo through the real Godot process).

Verbs: gen · python · godot · compare · free · all (--quick/--full).
First-line contract (the B2-338 hook law, rule_parity's twin):
    FLOCK_PARITY: ok mode=...     (exit 0)
    FLOCK_PARITY: FAIL mode=...   (exit 1)
    FLOCK_PARITY: ERROR mode=...  (exit 2, instrument error)

Honest result either way: parity holds = the four-way drift fear is
measured dead for this pair; first divergence = the top flock engineering
item. The runner MEASURES, never patches — flock.gd and step_threat are
executed as-is, so any law drift lands in the diff.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
import struct
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag import flock_positive as fp  # noqa: E402  (the Python parity twin)

SCHEMA = "flockframe/1"
FREE_SCHEMA = "flockfree/1"
CODEC_SCHEMA = "flockcodec/1"
LATEST_SCHEMA = "flock_parity_latest.v1"
GODOT_EXE = ROOT / "tools" / "godot" / "Godot_v4.3-stable_win64.exe"
GODOT_PROJECT = ROOT / "roblox_to_godot"
GD_RUNNER = "res://tests/flock_parity_runner.gd"
DEFAULT_OUT = ROOT / "tools" / "flock_parity_out"
LATEST_NAME = "latest.json"
# the parity twins (digest-stamped into latest.json — a dirty tree can never
# hide behind a stale verdict artifact)
TWIN_PY = "mag/flock_positive.py"
TWIN_GD = "roblox_to_godot/systems/flock.gd"
GC_PATH = ROOT / "roblox_to_godot" / "systems" / "game_constants.gd"

# The single-sourced (Q15/R7/R4) flock family of game_constants.gd — the
# hash law's alphabet. Sorted; the GDScript runner's CONST_NAMES twin.
CONST_NAMES = (
    "CATCH_RADIUS", "COAST_TIME", "DRAG", "FATIGUE_DECAY", "FLEE_PUSH",
    "FLEE_RADIUS", "POOL_PREF_DIST", "POOL_PULL", "SCHOOL_RADIUS", "TIRED",
    "TRAIL_DROP", "TRAIL_RADIUS", "WIGGLE",
)

# ------------------------------------------------------------- the epsilon ----
TIER_K_CONT = 32   # ulp32 multiplier for pos/vel (module docstring names why)
TIER_K_ARITH = 4   # ulp32 multiplier for fatigue/satiation
# Flat absolute term (NOT V2ASK3's 1e-6*dt = 1.7e-8 at 60Hz): bring-up
# measured near-zero CANCELLATION twice — a vel component's own magnitude
# gives a tiny epsilon while the component is built from SCHOOL-scale
# float32 intermediates whose rounding residue rides through: the mirror
# pair carried ulp32(0.165-scale) ~5e-8 on a 2e-3 component, and a mid-
# school fish carried ulp32(5-scale) = 4.77e-7 EXACTLY on a near-zero
# component. TIER_ABS=2e-6 absorbs ~ulp32(SCHOOL-scale x COHESION_W sums)
# and stays ~2000x below the smallest real law divergence the harness must
# catch (the catch-tick move, 4.3e-3 px at wiggle speed; 7.5e-2 at flee).
TIER_ABS = 2e-6
TOLERANCE_EXCEPTIONS = {
    "pos": "K=32: sin/cos wiggle + pow drag feed every component, and the "
            "school loop adds up to N-1 float32 roundings per tick",
    "vel": "K=32: same transcendental + accumulation feed as pos",
    "fatigue": "K=4: float64 arithmetic on both sides (GDScript Dictionary "
               "floats are 64-bit Variants), no transcendentals",
    "satiation": "K=4: threat mode never touches it; arithmetic identity",
    "abs": "TIER_ABS=2e-6 flat (V2ASK3 1e-6*dt widened, bring-up-measured): "
           "cancellation residue scales with the school-loop's float32 "
           "intermediates (ulp32(5)=4.77e-7 observed), not the component's "
           "own magnitude",
}
EDGE_BAND_ULPS = 8  # |d^2 - R^2| <= 8*ulp32(R^2) -> `edge`, not a failure

PROFILES: dict[str, dict[str, int]] = {
    "quick": {"seed": 20260930, "n": 8, "ticks": 40},
    "full": {"seed": 20260930, "n": 24, "ticks": 90},
}
QUICK_WALL_BUDGET_S = 120.0


# ------------------------------------------------------------ float32 codec ----

def f32b(v: float) -> int:
    """float64 -> its float32 bit pattern as int (rounds to nearest)."""
    return struct.unpack("<I", struct.pack("<f", v))[0]


def b32f(bits: int) -> float:
    """float32 bit pattern -> float64 (exact widening)."""
    return struct.unpack("<f", struct.pack("<I", bits & 0xFFFFFFFF))[0]


def enc32(v: float) -> str:
    return f"0x{f32b(v):08x}"


def dec32(s: str) -> float:
    return b32f(int(s, 16))


def ulp32(x: float) -> float:
    """One float32 unit-in-the-last-place at |x| (the named epsilon unit)."""
    bits = f32b(abs(x))
    exp = (bits >> 23) & 0xFF
    if exp == 0xFF:
        return math.inf
    if exp == 0:
        return 2.0 ** -149                 # smallest subnormal
    return 2.0 ** (exp - 127 - 23)         # normal spacing


def band(R: float) -> float:
    """Threshold band half-width: 8*ulp32(R^2) (V2ASK3 Tier-D exception)."""
    return EDGE_BAND_ULPS * ulp32(R * R)


# --------------------------------------------------------- constants (Q15) ----

def parse_gc() -> dict[str, float]:
    """game_constants.gd's flock family, parsed (the Q15 single source)."""
    src = GC_PATH.read_text(encoding="utf-8")
    out: dict[str, float] = {}
    for name in CONST_NAMES:
        m = re.search(rf"^const {name} := ([0-9.eE+-]+)", src, re.M)
        if not m:
            raise ValueError(f"{name} missing from {GC_PATH}")
        out[name] = float(m.group(1))
    return out


def consts_hash(consts: dict[str, float] | None = None) -> str:
    """sha256 over 'NAME=<float32 bits hex>\\n' lines, name-sorted — the
    byte-identical text the GDScript runner hashes from its GC preload."""
    consts = consts if consts is not None else parse_gc()
    body = "".join(f"{n}={enc32(consts[n])}\n" for n in sorted(consts))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


# -------------------------------------------------------------- generation ----
# Sequences are SPECS: initial fish + a deterministic player law. The frame
# chain itself is built during the Python run (teacher forcing: tick t+1's
# input is Python's float32-quantized output at t, and hunt-law players read
# the live state), then shipped whole to the GDScript runner, which maps
# each frame independently — teacher forcing makes every tick a pure
# function of its input frame.

def _rand_fish(rng: random.Random, n: int, cx: float, cy: float,
               spread: float) -> list[dict[str, Any]]:
    """n fish jittered around (cx, cy), vel 0, fatigue/satiation 0, alive.
    Positions are kept >= 1.0 px apart: flock.gd's school loop compares
    Dictionary equality BY VALUE (`other == f`), so two full-state twins
    would be skipped in GDScript but counted in Python — twins are excluded
    by construction and the driver trips if one ever forms."""
    fish: list[dict[str, Any]] = []
    tries = 0
    while len(fish) < n and tries < n * 400:
        tries += 1
        pos = (cx + rng.uniform(-spread, spread), cy + rng.uniform(-spread, spread))
        if all(math.hypot(pos[0] - f["pos"][0], pos[1] - f["pos"][1]) > 1.0 for f in fish):
            fish.append({"id": len(fish), "pos": pos, "vel": (0.0, 0.0),
                         "fatigue": 0.0, "satiation": 0.0, "alive": True})
    if len(fish) < n:
        raise RuntimeError("could not place distinct fish (twin guard)")
    return fish


def _gen_free(rng: random.Random, seq_id: str, ticks: int) -> dict[str, Any]:
    n = rng.randint(4, 10)
    return {"id": seq_id, "family": "free_school", "ticks": ticks,
            "player_law": {"kind": "static", "pos": (2000.0, 2000.0)},
            "fish0": _rand_fish(rng, n, 300.0, 300.0, 60.0)}


def _gen_threat(rng: random.Random, seq_id: str, ticks: int) -> dict[str, Any]:
    """Sweeping cursor: sinusoid through the school so flee accrual, the
    fatigue ceiling, recovery (tire branch) and drag all fire."""
    n = rng.randint(4, 9)
    return {"id": seq_id, "family": "threat_sweep", "ticks": ticks,
            "player_law": {"kind": "sweep", "cx": 300.0, "cy": 300.0,
                           "ax": rng.uniform(80.0, 240.0),
                           "ay": rng.uniform(30.0, 160.0),
                           "w": rng.uniform(0.02, 0.09)},
            "fish0": _rand_fish(rng, n, 300.0, 300.0, 70.0)}


def _gen_catch(rng: random.Random, seq_id: str, ticks: int) -> dict[str, Any]:
    """Perfect hunter parked on fish 0: dist stays < CATCH_RADIUS while
    fatigue crosses TIRED — the catch window FIRES (probes the catch-tick
    law, where flock.gd moves the fish and the port returns early)."""
    return {"id": seq_id, "family": "catch_hunt", "ticks": ticks,
            "player_law": {"kind": "hunt", "target": 0, "off": (0.1, 0.05)},
            "fish0": _rand_fish(rng, rng.randint(3, 6), 300.0, 300.0, 40.0)}


def _gen_edge(rng: random.Random, seq_id: str, ticks: int) -> dict[str, Any]:
    """Threshold probes (V2ASK3 test-3 seam), PURE RADIAL (y=0.0): fish at
    FLEE_RADIUS exactly and +/- 1 ulp32 from a static player. The R4 refire
    moved these onto the axis — the first cut carried y=+/-0.05, and a
    0.05px cross-axis offset (~2.5e-3 on d^2) swamps the 1-ulp x reduction
    (~2e-6), so the `R - 1 ulp flees` paper truth was geometrically false
    (hypot(19.999998, 0.05) > 20) and the known-answer test failed on a
    correct engine. On the axis the ulp alone decides, both precisions
    agree, and no band is needed.
    Catch-window probes: id 3 at 1.0px (caught under any sane radius) and
    id 5 at CATCH_RADIUS - 0.1 = 3.4px, fatigue 0.8 — caught clean
    (3.4 < 3.5), ALIVE under a CATCH_RADIUS-0.5 mutant (3.4 >= 3.0), the
    seam that makes the constant-mutation suite catch a catch-radius
    retune that lands on one twin only (the Q15 falsifier). id 4 is the
    school-edge pair (Tier-D band coverage)."""
    R = parse_gc()["FLEE_RADIUS"]
    r_bit = f32b(R)
    fish = [
        {"id": 0, "pos": (R, 0.0), "vel": (0.0, 0.0), "fatigue": 0.0,
         "satiation": 0.0, "alive": True},                     # exactly R
        {"id": 1, "pos": (b32f(r_bit - 1), 0.0), "vel": (0.0, 0.0),
         "fatigue": 0.0, "satiation": 0.0, "alive": True},     # R - 1 ulp
        {"id": 2, "pos": (b32f(r_bit + 1), 0.0), "vel": (0.0, 0.0),
         "fatigue": 0.0, "satiation": 0.0, "alive": True},     # R + 1 ulp
        {"id": 3, "pos": (1.0, 0.0), "vel": (0.0, 0.0), "fatigue": 0.8,
         "satiation": 0.0, "alive": True},                     # catch window
        {"id": 4, "pos": (R + 20.0, 20.0), "vel": (0.0, 0.0), "fatigue": 0.0,
         "satiation": 0.0, "alive": True},                     # school edge
        {"id": 5, "pos": (parse_gc()["CATCH_RADIUS"] - 0.1, 0.0),
         "vel": (0.0, 0.0), "fatigue": 0.8,
         "satiation": 0.0, "alive": True},                     # catch seam
    ]
    return {"id": seq_id, "family": "threshold_edge", "ticks": min(ticks, 12),
            "player_law": {"kind": "static", "pos": (0.0, 0.0)},
            "fish0": fish}


def _gen_hand(rng: random.Random, seq_id: str, ticks: int) -> dict[str, Any]:
    """Known-answer frames (V2ASK3 test 3): a mirror-symmetric pair around
    x=300 with the player parked far — cohesion/separation/wiggle/drag must
    keep the mirror law (equal y-vel, opposite x-vel), asserted in tests."""
    return {"id": seq_id, "family": "hand_frames", "ticks": 3,
            "player_law": {"kind": "static", "pos": (2000.0, 0.0)},
            "fish0": [
                {"id": 0, "pos": (310.0, 300.0), "vel": (0.0, 0.0),
                 "fatigue": 0.0, "satiation": 0.0, "alive": True},
                {"id": 1, "pos": (290.0, 300.0), "vel": (0.0, 0.0),
                 "fatigue": 0.0, "satiation": 0.0, "alive": True},
            ]}


FAMILIES = ("free_school", "threat_sweep", "catch_hunt", "threshold_edge",
            "hand_frames")
_GEN = {"free_school": _gen_free, "threat_sweep": _gen_threat,
        "catch_hunt": _gen_catch, "threshold_edge": _gen_edge,
        "hand_frames": _gen_hand}


def generate(seed: int, n: int, ticks: int) -> dict[str, Any]:
    rng = random.Random(seed)
    sequences: list[dict[str, Any]] = []
    for i in range(n):
        fam = FAMILIES[i % len(FAMILIES)]
        sequences.append(_GEN[fam](rng, f"seq_{i:03d}", ticks))
    return {"schema": SCHEMA, "constants_hash": consts_hash(),
            "dt": enc32(1.0 / 60.0), "sequences": sequences}


# ----------------------------------------------------------- python engine ----

def _player_at(law: dict[str, Any], state: list[fp.Fish], t: int) -> tuple[float, float]:
    kind = law["kind"]
    if kind == "static":
        return law["pos"]
    if kind == "sweep":
        return (law["cx"] + law["ax"] * math.sin(law["w"] * t),
                law["cy"] + law["ay"] * math.sin(law["w"] * t * 1.7 + 1.0))
    if kind == "hunt":
        tgt = state[law["target"]]
        return (tgt.pos[0] + law["off"][0], tgt.pos[1] + law["off"][1])
    raise ValueError(f"unknown player law {kind}")


def _neighbors(state: list[fp.Fish], school_r: float) -> list[list[int]]:
    """Tier-D neighbour sets on the input state (flock.gd's school-loop
    membership: alive others with dist < SCHOOL_RADIUS; float64 here vs
    float32 in the runner — the compare band absorbs the difference)."""
    out = []
    for i, f in enumerate(state):
        ids = [j for j, o in enumerate(state)
               if j != i and o.alive
               and math.hypot(o.pos[0] - f.pos[0], o.pos[1] - f.pos[1]) < school_r]
        out.append(sorted(ids))
    return out


def _twin_check(state: list[fp.Fish]) -> None:
    """flock.gd compares Dictionary equality BY VALUE (`other == f`): two
    full-state twins would be skipped in GDScript but counted in Python.
    The generator excludes twins; this tripwire proves the invariant held."""
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            a, b = state[i], state[j]
            if (a.pos == b.pos and a.vel == b.vel and a.fatigue == b.fatigue
                    and a.satiation == b.satiation and a.alive == b.alive):
                raise RuntimeError(
                    f"value-twin fish {i},{j} formed — GDScript `other == f` "
                    f"would skip what Python counts (semantic divergence "
                    f"excluded by generator contract)")


def _encode_fish(f_id: int, s: fp.Fish) -> dict[str, Any]:
    return {"id": f_id, "pos": [enc32(s.pos[0]), enc32(s.pos[1])],
            "vel": [enc32(s.vel[0]), enc32(s.vel[1])],
            "fatigue": enc32(s.fatigue), "satiation": enc32(s.satiation),
            "alive": s.alive}


def _q32(v: Any) -> float:
    """Quantize to the float32 alphabet: hex strings decode, raw floats
    round through float32 (the spec's fish0 carries plain floats)."""
    if isinstance(v, str):
        return dec32(v)
    return dec32(enc32(float(v)))


def _decode_fish(raw: list[dict[str, Any]]) -> list[fp.Fish]:
    return [fp.Fish(pos=(_q32(f["pos"][0]), _q32(f["pos"][1])),
                    vel=(_q32(f["vel"][0]), _q32(f["vel"][1])),
                    fatigue=_q32(f["fatigue"]),
                    satiation=_q32(f["satiation"]), alive=bool(f["alive"]))
            for f in raw]


def run_teacher(doc: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """The Python reference run. Returns (frames_chain, output_rows).

    Teacher forcing: state is decoded from float32 bits each tick and the
    next input is the quantized output — Python's own float64 residue never
    compounds and both sides see byte-identical float32 inputs per tick.
    Stepping is fp.step_threat (the REAL twin, not a reimplementation) in
    index order over the live list, matching flock.gd's in-place pass where
    fish j < k read fish k's PRE-move pos and fish j > k read POST-move.
    """
    consts = parse_gc()
    dt = dec32(doc["dt"])
    frames_chain: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    for seq in doc["sequences"]:
        state = _decode_fish(seq["fish0"])
        for t in range(1, seq["ticks"] + 1):
            _twin_check(state)
            player = _player_at(seq["player_law"], state, t)
            # both sides consume the IDENTICAL float32 player bits: the
            # frame's hex IS the shared truth (float64 residue would skew
            # the flee branch by an un-banded ulp)
            player = (dec32(enc32(player[0])), dec32(enc32(player[1])))
            sim_time = dec32(enc32(t * dt))
            frame_fish = [_encode_fish(i, s) for i, s in enumerate(state)]
            frame = {"seq": seq["id"], "family": seq["family"], "tick": t,
                     "sim_time": enc32(sim_time),
                     "player": [enc32(player[0]), enc32(player[1])],
                     "fish": frame_fish}
            frames_chain.append(frame)
            neighbors = _neighbors(state, consts["SCHOOL_RADIUS"])
            fleeing_ctx = [
                s.alive and math.hypot(player[0] - s.pos[0], player[1] - s.pos[1])
                < consts["FLEE_RADIUS"] and s.fatigue < 1.0 for s in state]
            for s in state:
                if not s.alive:
                    continue
                fp.step_threat(s, state, player, dt, sim_time)
            fish_out = []
            for i, s in enumerate(state):
                in_alive = frame_fish[i]["alive"]
                fish_out.append({
                    "id": i, "alive": s.alive,
                    "caught": bool(in_alive) and not s.alive,
                    "fleeing": fleeing_ctx[i], "neighbors": neighbors[i],
                    "pos": [enc32(s.pos[0]), enc32(s.pos[1])],
                    "vel": [enc32(s.vel[0]), enc32(s.vel[1])],
                    "fatigue": enc32(s.fatigue),
                    "satiation": enc32(s.satiation)})
            rows.append({"seq": seq["id"], "family": seq["family"],
                         "tick": t, "fish": fish_out})
            # TEACHER FORCING, enforced on the state itself: the next tick's
            # python state is the float32-quantized output (fresh Fish from
            # the emitted bits), never the float64 residue — otherwise the
            # GDScript side (fed the frame) and this side see different
            # inputs (the hand_frames exactly-at-SCHOOL_RADIUS seam caught
            # exactly this during bring-up: float64 19.99998 vs float32
            # 20.0 flipped the neighbour verdict).
            state = _decode_fish(fish_out)
    return frames_chain, rows


# ------------------------------------------------------------- godot side ----

def _run_godot(doc_path: Path, out_path: Path) -> None:
    if not GODOT_EXE.exists():
        raise FileNotFoundError(f"godot binary missing: {GODOT_EXE}")
    doc_path, out_path = doc_path.resolve(), out_path.resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [str(GODOT_EXE), "--headless", "--path", str(GODOT_PROJECT),
           "--script", GD_RUNNER, "--", str(doc_path), str(out_path)]
    proc = subprocess.run(cmd, capture_output=True, text=True,
                          cwd=str(GODOT_PROJECT), timeout=600)
    if proc.returncode != 0:
        raise RuntimeError(f"godot runner exited {proc.returncode}\n"
                           f"stdout:\n{proc.stdout[-1500:]}\n"
                           f"stderr:\n{proc.stderr[-1500:]}")


# --------------------------------------------------------------- compare ----

def _tol(a: float, b: float, k: int, dt: float) -> tuple[bool, float, float]:
    m = max(abs(a), abs(b))
    eps = k * ulp32(m) + TIER_ABS
    return abs(a - b) <= eps, eps, abs(a - b)


def _d2(pa: tuple[float, float], pb: tuple[float, float]) -> float:
    return (pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2


def _frame_pos(f: dict[str, Any]) -> tuple[float, float]:
    return (dec32(f["pos"][0]), dec32(f["pos"][1]))


def compare(py_rows: list[dict[str, Any]], gd_rows: list[dict[str, Any]],
            dt: float,
            frames_chain: list[dict[str, Any]] | None = None
            ) -> dict[str, Any]:
    """Walk both sides in (seq, tick) order.

    Tier D (alive, caught, fleeing, neighbours): exact, with the V2ASK3
    threshold band — a mismatch inside 8*ulp32(R^2) of its radius decision
    (fatigue: 8*ulp32(TIRED)) counts as `edge`, never a failure.
    Tier C (pos, vel, fatigue, satiation): within K*ulp32 + 1e-6*dt, the
    named epsilon. first_divergence names seq/tick/fish/field with both
    values and the exceeded epsilon; the rollup counts EVERY divergence
    class across the full walk (not just the first)."""
    chain = {(fr["seq"], fr["tick"]): fr for fr in (frames_chain or [])}
    consts = parse_gc()
    py_by = {(r["seq"], r["tick"]): r for r in py_rows}
    gd_by = {(r["seq"], r["tick"]): r for r in gd_rows}
    order = [(r["seq"], r["tick"]) for r in py_rows]
    fam_of = {r["seq"]: r["family"] for r in py_rows}
    fam_stats: dict[str, dict[str, Any]] = {
        fam: {"sequences": 0, "diverged_seqs": 0, "first_tick": None,
              "max_dev": {}}
        for fam in sorted(set(fam_of.values()))}
    for s in dict.fromkeys(s_ for s_, _ in order):
        fam_stats[fam_of[s]]["sequences"] += 1

    report: dict[str, Any] = {
        "parity": True, "rows_py": len(py_rows), "rows_gd": len(gd_rows),
        "first_divergence": None, "per_family": fam_stats, "edges": 0,
        "edge_notes": [], "divergence_classes": {}, "diverged_seqs": [],
        "tolerance": {"k_cont": TIER_K_CONT, "k_arith": TIER_K_ARITH,
                      "abs": TIER_ABS, "edge_band_ulps": EDGE_BAND_ULPS,
                      "exceptions": TOLERANCE_EXCEPTIONS}}

    def fail(key: tuple[str, int], kind: str, detail: str) -> None:
        report["parity"] = False
        report["divergence_classes"][kind] = report["divergence_classes"].get(kind, 0) + 1
        fam = fam_of[key[0]]
        if key[0] not in report["diverged_seqs"]:
            report["diverged_seqs"].append(key[0])
            fam_stats[fam]["diverged_seqs"] += 1
        if fam_stats[fam]["first_tick"] is None or key[1] < fam_stats[fam]["first_tick"]:
            fam_stats[fam]["first_tick"] = key[1]
        if report["first_divergence"] is None:
            report["first_divergence"] = {"seq": key[0], "family": fam,
                                          "tick": key[1], "kind": kind,
                                          "detail": detail}

    def edge(key: tuple[str, int], what: str) -> None:
        report["edges"] += 1
        if len(report["edge_notes"]) < 40:
            report["edge_notes"].append(f"{key[0]} t{key[1]}: {what} (band)")

    def band_ctx(key: tuple[str, int], fid: int, what: str) -> bool:
        """Is this Tier-D mismatch inside the threshold band (edge)?"""
        fr = chain.get(key)
        if fr is None:
            return False
        f = fr["fish"][fid]
        player = (dec32(fr["player"][0]), dec32(fr["player"][1]))
        if what == "fleeing":
            d2 = _d2(_frame_pos(f), player)
            return abs(d2 - consts["FLEE_RADIUS"] ** 2) <= band(consts["FLEE_RADIUS"])
        if what in ("caught", "alive"):
            d2 = _d2(_frame_pos(f), player)
            near_catch = abs(d2 - consts["CATCH_RADIUS"] ** 2) <= band(consts["CATCH_RADIUS"])
            near_tired = abs(dec32(f["fatigue"]) - consts["TIRED"]) \
                <= EDGE_BAND_ULPS * ulp32(consts["TIRED"])
            return near_catch or near_tired
        if what == "neighbors":
            return any(abs(_d2(_frame_pos(f), _frame_pos(o))
                           - consts["SCHOOL_RADIUS"] ** 2)
                       <= band(consts["SCHOOL_RADIUS"])
                       for o in fr["fish"] if o["id"] != fid)
        return False

    for key in order:
        if key not in gd_by:
            fail(key, "missing_on_godot_side", "row absent in gd rows")
            break
        py, gd = py_by[key], gd_by[key]
        py_fish = {f["id"]: f for f in py["fish"]}
        gd_fish = {f["id"]: f for f in gd["fish"]}
        for fid in sorted(py_fish):
            a, b = py_fish[fid], gd_fish.get(fid)
            if b is None:
                fail(key, "fish_missing", f"fish {fid} absent in gd row")
                continue
            # ---- Tier D: discrete decisions, exact (band excepted) ----
            for dfield in ("alive", "caught", "fleeing"):
                if a[dfield] != b[dfield]:
                    if band_ctx(key, fid, dfield):
                        edge(key, f"fish {fid}.{dfield} py={a[dfield]} gd={b[dfield]}")
                    else:
                        fail(key, f"tier_d_{dfield}",
                             f"fish {fid}.{dfield}: py={a[dfield]} gd={b[dfield]}")
            if a["neighbors"] != b["neighbors"]:
                if band_ctx(key, fid, "neighbors"):
                    edge(key, f"fish {fid}.neighbors py={a['neighbors']} gd={b['neighbors']}")
                else:
                    fail(key, "tier_d_neighbors",
                         f"fish {fid}.neighbors: py={a['neighbors']} gd={b['neighbors']}")
            # ---- Tier C: continuous state, the named epsilon ----
            for field, k in (("pos", TIER_K_CONT), ("vel", TIER_K_CONT),
                             ("fatigue", TIER_K_ARITH), ("satiation", TIER_K_ARITH)):
                if field in ("pos", "vel"):
                    vals = [(dec32(a[field][c]), dec32(b[field][c])) for c in (0, 1)]
                else:
                    vals = [(dec32(a[field]), dec32(b[field]))]
                for vi, (va, vb) in enumerate(vals):
                    ok, eps, dev = _tol(va, vb, k, dt)
                    md = fam_stats[py["family"]]["max_dev"]
                    if dev > md.get(field, -1.0):
                        md[field] = dev
                    if not ok:
                        fail(key, f"tier_c_{field}",
                             f"fish {fid}.{field}{'' if field in ('fatigue','satiation') else f'[{vi}]'}"
                             f": py={va!r} gd={vb!r} |d|={dev:.3e} > eps={eps:.3e} "
                             f"({k}*ulp32({max(abs(va), abs(vb))!r})+{TIER_ABS})")
    if report["parity"]:
        extras = sorted(k for k in gd_by if k not in py_by)
        if extras:
            s, t = extras[0]
            fail((s, t), "extra_on_godot_side", "gd rows beyond py rows")
    return report


# ------------------------------------------------------------ free smoke ----

FREE_TICKS = 60
FREE_CENTROID_EPS_PX = 2.0   # loose: flock-level statistics only (V2ASK3)
FREE_SPREAD_RATIO = (0.5, 2.0)


def run_free_python(seed: int) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Free-run smoke (no teacher forcing): Python evolves its own state for
    FREE_TICKS from a seeded school; the same initial doc goes to Godot.
    Compare is centroid/spread only — chaos makes per-boid compare illegal
    on this lane by construction."""
    rng = random.Random(seed)
    fish0 = _rand_fish(rng, 8, 300.0, 300.0, 60.0)
    doc = {"schema": FREE_SCHEMA, "id": "free_smoke",
           "constants_hash": consts_hash(), "dt": enc32(1.0 / 60.0),
           "ticks": FREE_TICKS, "player": [enc32(2000.0), enc32(2000.0)],
           "fish0": [_encode_fish(f["id"], fp.Fish(pos=f["pos"])) for f in fish0]}
    state = _decode_fish(doc["fish0"])
    dt = dec32(doc["dt"])
    rows = []
    for t in range(1, FREE_TICKS + 1):
        sim_time = dec32(enc32(t * dt))
        for s in state:
            if not s.alive:
                continue
            fp.step_threat(s, state, (2000.0, 2000.0), dt, sim_time)
        # mimic GDScript's native float32 storage each tick so the loose
        # flock-level stats compare symmetric state precisions
        state = [fp.Fish(pos=(dec32(enc32(s.pos[0])), dec32(enc32(s.pos[1]))),
                         vel=(dec32(enc32(s.vel[0])), dec32(enc32(s.vel[1]))),
                         fatigue=dec32(enc32(s.fatigue)),
                         satiation=dec32(enc32(s.satiation)), alive=s.alive)
                 for s in state]
        rows.append({"seq": "free_smoke", "family": "free_smoke", "tick": t,
                     "fish": [{"id": i, "alive": s.alive,
                               "pos": [enc32(s.pos[0]), enc32(s.pos[1])]}
                              for i, s in enumerate(state)]})
    return doc, rows


def compare_free(py_rows: list[dict[str, Any]], gd_rows: list[dict[str, Any]]
                 ) -> dict[str, Any]:
    """Flock-level statistics at the LAST tick: centroid within
    FREE_CENTROID_EPS_PX, RMS-spread ratio within FREE_SPREAD_RATIO, alive
    counts equal at every tick."""
    py_by = {r["tick"]: r for r in py_rows}
    gd_by = {r["tick"]: r for r in gd_rows}
    out: dict[str, Any] = {"parity": True, "kind": "free_smoke",
                           "ticks": len(py_rows), "first_divergence": None}

    def stats(row: dict[str, Any]) -> tuple[tuple[float, float], float, int]:
        alive = [f for f in row["fish"] if f["alive"]]
        pts = [(_frame_pos(f)) for f in alive]
        n = len(alive)
        if n == 0:
            return (0.0, 0.0), 0.0, 0
        cx = sum(p[0] for p in pts) / n
        cy = sum(p[1] for p in pts) / n
        spread = math.sqrt(sum((p[0] - cx) ** 2 + (p[1] - cy) ** 2 for p in pts) / n)
        return (cx, cy), spread, n

    for t in sorted(py_by):
        if t not in gd_by:
            out["parity"] = False
            out["first_divergence"] = {"tick": t, "kind": "missing_tick"}
            break
        (pcx, pcy), ps, pn = stats(py_by[t])
        (gcx, gcy), gs, gn = stats(gd_by[t])
        if pn != gn:
            out["parity"] = False
            out["first_divergence"] = {"tick": t, "kind": "alive_count",
                                       "py": pn, "gd": gn}
            break
        if t == max(py_by):
            dc = math.hypot(pcx - gcx, pcy - gcy)
            ratio = (ps / gs) if gs > 1e-9 else (1.0 if ps < 1e-9 else math.inf)
            out["centroid_dist_px"] = round(dc, 4)
            out["spread_py"], out["spread_gd"] = round(ps, 3), round(gs, 3)
            out["spread_ratio"] = round(ratio, 4) if math.isfinite(ratio) else None
            if dc > FREE_CENTROID_EPS_PX:
                out["parity"] = False
                out["first_divergence"] = {
                    "tick": t, "kind": "centroid", "py": [pcx, pcy],
                    "gd": [gcx, gcy], "dist_px": round(dc, 4)}
            elif not (FREE_SPREAD_RATIO[0] <= ratio <= FREE_SPREAD_RATIO[1]):
                out["parity"] = False
                out["first_divergence"] = {"tick": t, "kind": "spread_ratio",
                                           "ratio": round(ratio, 4)}
    return out


# ------------------------------------------------------- codec corpus ----

def codec_corpus() -> list[str]:
    """float32 corner cases (V2ASK3 test 1): NaN (canonical quiet only —
    payloaded NaNs are not byte-stable through float64 widening on either
    runtime), +-0, subnormals, +-inf, max float32, min normal, and the
    flock's own constants."""
    specials = [
        0x7fc00000, 0xffc00000,              # quiet NaN, -NaN (canonical)
        0x00000000, 0x80000000,              # +0, -0
        0x00000001, 0x80000001,              # smallest subnormal, negative
        0x007fffff,                          # largest subnormal
        0x00800000, 0x80800000,              # min normal, negative
        0x7f7fffff, 0xff7fffff,              # max float32, negative
        0x7f800000, 0xff800000,              # +inf, -inf
        0x3fc00000,                          # 1.5
        0x42c80000, 0x43160000,              # 100.0, 150.0 (board scale)
        0x3dcccccd,                          # 0.1 (the V2ASK3 named case)
    ]
    hexes = [f"0x{b:08x}" for b in specials]
    hexes += [enc32(v) for v in parse_gc().values()]
    return hexes


# ------------------------------------------------------------------- io ----

def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(ln) for ln in
            Path(path).read_text(encoding="utf-8").splitlines() if ln.strip()]


def twin_digest() -> dict[str, Any]:
    out: dict[str, Any] = {}
    for label, rel in (("py", TWIN_PY), ("gd", TWIN_GD)):
        p = ROOT / rel
        out[label] = {"path": rel,
                      "sha256_12": hashlib.sha256(p.read_bytes()).hexdigest()[:12]
                      if p.exists() else "MISSING"}
    p = GC_PATH
    out["gc"] = {"path": "roblox_to_godot/systems/game_constants.gd",
                 "sha256_12": hashlib.sha256(p.read_bytes()).hexdigest()[:12]
                 if p.exists() else "MISSING",
                 "constants_hash": consts_hash()}
    return out


def _print_report(report: dict[str, Any]) -> None:
    print(f"flock parity: {report['parity']}  "
          f"(rows py={report['rows_py']} gd={report['rows_gd']}, "
          f"edges={report['edges']})")
    for fam, st in sorted(report["per_family"].items()):
        dev = " ".join(f"{k}={v:.2e}" for k, v in sorted(st["max_dev"].items()))
        print(f"  {fam}: {st['sequences']} seqs, diverged {st['diverged_seqs']}, "
              f"first divergent tick {st['first_tick']}  max_dev {dev}")
    fd = report["first_divergence"]
    if fd:
        print(f"FIRST DIVERGENCE: {fd['seq']} ({fd['family']}) tick {fd['tick']} "
              f"kind={fd['kind']}")
        print(f"  {fd['detail']}")


def _write_latest(out_dir: Path, mode: str, params: dict[str, int],
                  frames: int, wall: float, source: str,
                  report: dict[str, Any] | None, free: dict[str, Any] | None,
                  exit_code: int, error: str | None = None) -> Path:
    doc: dict[str, Any] = {
        "schema": LATEST_SCHEMA, "mode": mode, "seed": params["seed"],
        "n": params["n"], "ticks": params["ticks"], "total_frames": frames,
        "wall_seconds": round(wall, 2),
        "finished_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": source,
        "parity": report["parity"] if report is not None else None,
        "exit_code": exit_code,
        "first_divergence": (report or {}).get("first_divergence"),
        "per_family": (report or {}).get("per_family"),
        "divergence_classes": (report or {}).get("divergence_classes"),
        "edges": (report or {}).get("edges"),
        "free_smoke": free,
        "error": error,
        "twins": twin_digest(),
        "profiles": {k: dict(v) for k, v in PROFILES.items()},
        "godot_exe_present": GODOT_EXE.exists(),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / LATEST_NAME
    path.write_text(json.dumps(doc, indent=1, sort_keys=True), encoding="utf-8")
    return path


# --------------------------------------------------------------- verbs ----

def _gd_doc_from_chain(spec: dict[str, Any],
                       frames: list[dict[str, Any]]) -> dict[str, Any]:
    """Regroup the flat frames chain into the runner's per-sequence doc
    (order-preserving unique sequences; frames in tick order)."""
    by_seq: dict[str, dict[str, Any]] = {}
    seqs: list[dict[str, Any]] = []
    for fr in frames:
        if fr["seq"] not in by_seq:
            by_seq[fr["seq"]] = {"id": fr["seq"], "family": fr["family"],
                                 "frames": []}
            seqs.append(by_seq[fr["seq"]])
        by_seq[fr["seq"]]["frames"].append(
            {k: fr[k] for k in ("tick", "sim_time", "player", "fish")})
    return {"schema": SCHEMA, "constants_hash": spec["constants_hash"],
            "dt": spec["dt"], "sequences": seqs}


def cmd_gen(args: argparse.Namespace) -> int:
    doc = generate(args.seed, args.n, args.ticks)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, indent=1, sort_keys=True), encoding="utf-8")
    fams: dict[str, int] = {}
    for s in doc["sequences"]:
        fams[s["family"]] = fams.get(s["family"], 0) + 1
    print(f"gen: {len(doc['sequences'])} sequences ({fams}) -> {args.out}")
    return 0


def cmd_python(args: argparse.Namespace) -> int:
    spec = json.loads(args.inp.read_text(encoding="utf-8"))
    frames, rows = run_teacher(spec)
    _write_jsonl(args.frames_out, frames)
    _write_jsonl(args.out, rows)
    print(f"python: {len(rows)} tick rows (frames chain: {args.frames_out}) "
          f"-> {args.out}")
    return 0


def cmd_godot(args: argparse.Namespace) -> int:
    frames = _load_jsonl(args.frames)
    spec = json.loads(args.inp.read_text(encoding="utf-8"))
    doc = _gd_doc_from_chain(spec, frames)
    args.doc_out.parent.mkdir(parents=True, exist_ok=True)
    args.doc_out.write_text(json.dumps(doc, indent=1, sort_keys=True),
                            encoding="utf-8")
    _run_godot(args.doc_out, args.out)
    n = len(_load_jsonl(args.out))
    print(f"godot: {n} tick rows -> {args.out}")
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    spec = json.loads(args.inp.read_text(encoding="utf-8"))
    frames = _load_jsonl(args.frames) if args.frames else []
    report = compare(_load_jsonl(args.py), _load_jsonl(args.gd),
                     dec32(spec["dt"]), frames)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=1, sort_keys=True),
                        encoding="utf-8")
    _print_report(report)
    return 0 if report["parity"] else 1


def cmd_free(args: argparse.Namespace) -> int:
    doc, py_rows = run_free_python(args.seed)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    free_doc = args.out_dir / "free_doc.json"
    free_doc.write_text(json.dumps(doc, indent=1, sort_keys=True),
                        encoding="utf-8")
    _write_jsonl(args.out_dir / "free_python.jsonl", py_rows)
    _run_godot(free_doc, args.out_dir / "free_godot.jsonl")
    rep = compare_free(py_rows, _load_jsonl(args.out_dir / "free_godot.jsonl"))
    (args.out_dir / "free_report.json").write_text(
        json.dumps(rep, indent=1, sort_keys=True), encoding="utf-8")
    print(f"free smoke: {rep['parity']} {json.dumps({k: v for k, v in rep.items() if k not in ('parity', 'kind')})}")
    return 0 if rep["parity"] else 1


def cmd_codec(args: argparse.Namespace) -> int:
    """Codec round-trip through the REAL Godot process (V2ASK3 test 1)."""
    args.out_dir.mkdir(parents=True, exist_ok=True)
    doc = {"schema": CODEC_SCHEMA, "constants_hash": consts_hash(),
           "values": codec_corpus()}
    doc_p = args.out_dir / "codec_doc.json"
    doc_p.write_text(json.dumps(doc, indent=1, sort_keys=True), encoding="utf-8")
    _run_godot(doc_p, args.out_dir / "codec_echo.jsonl")
    echo = _load_jsonl(args.out_dir / "codec_echo.jsonl")[0]
    assert echo["schema"] == CODEC_SCHEMA
    assert echo["sha256"] == consts_hash(), "gd runner computed a different constants hash"
    bad = [(a, b) for a, b in zip(doc["values"], echo["values"]) if a != b]
    if bad:
        print(f"codec: FAIL {len(bad)}/{len(doc['values'])} values mutated "
              f"through the godot transport: {bad[:5]}")
        return 1
    print(f"codec: ok {len(doc['values'])} float32 values round-tripped "
          f"bit-identical through the godot process")
    return 0


def resolve_params(mode: str, seed: int | None, n: int | None,
                   ticks: int | None) -> dict[str, int]:
    prof = PROFILES[mode]
    return {"seed": seed if seed is not None else prof["seed"],
            "n": n if n is not None else prof["n"],
            "ticks": ticks if ticks is not None else prof["ticks"]}


def cmd_all(args: argparse.Namespace) -> int:
    mode = args.mode
    params = resolve_params(mode, args.seed, args.n, args.ticks)
    d = args.out_dir
    inp = d / f"{mode}_inputs.json"
    frames_p, py_p, gd_doc, gd_p = (d / f"{mode}_frames.jsonl",
                                    d / f"{mode}_python.jsonl",
                                    d / f"{mode}_gd_doc.json",
                                    d / f"{mode}_godot.jsonl")
    rep_p = d / f"{mode}_report.json"
    t0 = time.monotonic()
    free: dict[str, Any] | None = None
    try:
        spec = generate(params["seed"], params["n"], params["ticks"])
        inp.write_text(json.dumps(spec, indent=1, sort_keys=True), encoding="utf-8")
        frames, rows = run_teacher(spec)
        _write_jsonl(frames_p, frames)
        _write_jsonl(py_p, rows)
        doc = _gd_doc_from_chain(spec, frames)
        gd_doc.write_text(json.dumps(doc, indent=1, sort_keys=True), encoding="utf-8")
        _run_godot(gd_doc, gd_p)
        report = compare(rows, _load_jsonl(gd_p), dec32(spec["dt"]), frames)
        rep_p.write_text(json.dumps(report, indent=1, sort_keys=True),
                         encoding="utf-8")
        # free smoke rides along (failures reported, not fatal to the line)
        fd, py_rows_f = run_free_python(params["seed"])
        free_doc = d / "free_doc.json"
        free_doc.write_text(json.dumps(fd, indent=1, sort_keys=True), encoding="utf-8")
        _run_godot(free_doc, d / "free_godot.jsonl")
        free = compare_free(py_rows_f, _load_jsonl(d / "free_godot.jsonl"))
        (d / "free_report.json").write_text(
            json.dumps(free, indent=1, sort_keys=True), encoding="utf-8")
    except Exception as exc:  # instrument error: honest artifact + exit 2
        wall = time.monotonic() - t0
        err = f"{type(exc).__name__}: {str(exc)[:300]}"
        print(f"FLOCK_PARITY: ERROR mode={mode} {err}")
        _write_latest(d, mode, params, None, wall, args.source, None, None, 2,
                      error=err)
        return 2
    wall = time.monotonic() - t0
    exit_code = 0 if report["parity"] else 1
    if report["parity"]:
        print(f"FLOCK_PARITY: ok mode={mode} rows_py={report['rows_py']}")
    else:
        fdv = report["first_divergence"]
        print(f"FLOCK_PARITY: FAIL mode={mode} first={fdv['seq']} "
              f"family={fdv['family']} tick={fdv['tick']} kind={fdv['kind']}")
    latest = _write_latest(d, mode, params, len(frames), wall, args.source,
                           report, free, exit_code)
    print(f"artifacts in {d} (standing verdict: {latest})")
    _print_report(report)
    if free is not None:
        print(f"free smoke: {free['parity']} "
              + json.dumps({k: v for k, v in free.items()
                            if k not in ("parity", "kind")}))
    if mode == "quick" and wall > QUICK_WALL_BUDGET_S:
        print(f"WARN: quick run took {wall:.1f}s (budget {QUICK_WALL_BUDGET_S:.0f}s)")
    return exit_code


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("gen", help="generate seeded sequence specs")
    g.add_argument("--seed", type=int, default=20260930)
    g.add_argument("--n", type=int, default=24)
    g.add_argument("--ticks", type=int, default=90)
    g.add_argument("--out", type=Path, default=DEFAULT_OUT / "flock_inputs.json")
    g.set_defaults(func=cmd_gen)

    q = sub.add_parser("python", help="teacher-forced reference run (flock_positive)")
    q.add_argument("--in", dest="inp", type=Path, required=True)
    q.add_argument("--out", type=Path, default=DEFAULT_OUT / "flock_python.jsonl")
    q.add_argument("--frames-out", dest="frames_out", type=Path,
                   default=DEFAULT_OUT / "flock_frames.jsonl")
    q.set_defaults(func=cmd_python)

    r = sub.add_parser("godot", help="run the GDScript side (headless godot)")
    r.add_argument("--in", dest="inp", type=Path, required=True,
                   help="the sequence spec (for constants_hash + dt)")
    r.add_argument("--frames", type=Path, required=True,
                   help="the python-emitted frames chain")
    r.add_argument("--doc-out", dest="doc_out", type=Path,
                   default=DEFAULT_OUT / "flock_gd_doc.json")
    r.add_argument("--out", type=Path, default=DEFAULT_OUT / "flock_godot.jsonl")
    r.set_defaults(func=cmd_godot)

    c = sub.add_parser("compare", help="Tier-D/Tier-C diff with the band law")
    c.add_argument("--py", type=Path, required=True)
    c.add_argument("--gd", type=Path, required=True)
    c.add_argument("--in", dest="inp", type=Path, required=True)
    c.add_argument("--frames", type=Path, default=None,
                   help="frames chain (enables the edge band)")
    c.add_argument("--out", type=Path, default=DEFAULT_OUT / "flock_report.json")
    c.set_defaults(func=cmd_compare)

    f = sub.add_parser("free", help="free-run flock-level smoke (60 ticks)")
    f.add_argument("--seed", type=int, default=20260930)
    f.add_argument("--out-dir", dest="out_dir", type=Path, default=DEFAULT_OUT)
    f.set_defaults(func=cmd_free)

    k = sub.add_parser("codec", help="float32 codec round-trip through godot")
    k.add_argument("--out-dir", dest="out_dir", type=Path, default=DEFAULT_OUT)
    k.set_defaults(func=cmd_codec)

    a = sub.add_parser("all", help="gen + python + godot + compare + free")
    mode_g = a.add_mutually_exclusive_group()
    mode_g.add_argument("--quick", action="store_const", dest="mode", const="quick",
                        help=f"pre-push profile: {PROFILES['quick']}")
    mode_g.add_argument("--full", action="store_const", dest="mode", const="full",
                        help=f"depth profile: {PROFILES['full']} (the default)")
    a.set_defaults(mode="full")
    a.add_argument("--seed", type=int, default=None)
    a.add_argument("--n", type=int, default=None)
    a.add_argument("--ticks", type=int, default=None)
    a.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    a.add_argument("--source", default="manual")
    a.set_defaults(func=cmd_all)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
