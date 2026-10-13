"""Q15 guard tests — game_constants.gd is the single source, and the drift
it killed stays dead (R4 2026-09-30, V2ASK3 Q15; completing R7's landing:
the guard this file's consumers cite existed only as a claim until now).

Laws under test (receipt watch/inbox/last_mile_20260930/R4_FLOCK_PARITY.md):
  - VALUE PIN: the flock family holds the V6/Z14 tuning (FLEE_RADIUS 20 —
    the drift was flock.gd 20 vs fish_brain.gd/mountain_units 14).
  - LITERAL LINT: no .gd file outside game_constants.gd declares a raw
    numeric literal for a registered name — a retune can never land on one
    twin only (V2ASK3 falsifier: re-adding `const FLEE_RADIUS := 14.0` to
    fish_brain.gd must fail this suite).
  - ALIAS PIN: flock.gd and fish_brain.gd read GC.*, not local truth.
  - PYTHON TWINS: mag/flock_positive.py and tools/mountain_units.py parse
    equal to GC (mountain_units rode the stale 14 until the R4 true-up).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

GC = ROOT / "roblox_to_godot" / "systems" / "game_constants.gd"
FLOCK_GD = ROOT / "roblox_to_godot" / "systems" / "flock.gd"
BRAIN_GD = ROOT / "roblox_to_godot" / "systems" / "fish_brain.gd"
GODOT_TREE = ROOT / "roblox_to_godot"

# the registered flock family (tools/flock_parity.py CONST_NAMES twin)
REGISTERED = (
    "FLEE_RADIUS", "CATCH_RADIUS", "SCHOOL_RADIUS", "TRAIL_RADIUS", "TIRED",
    "TRAIL_DROP", "FLEE_PUSH", "WIGGLE", "FATIGUE_DECAY", "DRAG",
    "COAST_TIME", "POOL_PREF_DIST", "POOL_PULL",
)
PINNED_VALUES = {
    "FLEE_RADIUS": 20.0,   # Z14/V6: 14 -> 20 (the drift this file killed)
    "CATCH_RADIUS": 3.5,
    "SCHOOL_RADIUS": 20.0,
    "TRAIL_RADIUS": 38.0,
    "TIRED": 0.7,
    "TRAIL_DROP": 0.5,
    "FLEE_PUSH": 6.0,      # Z14/V6: 2.5 -> 6.0
    "WIGGLE": 0.05,
    "FATIGUE_DECAY": 0.4,
    "DRAG": 0.985,
    "COAST_TIME": 0.8,
    "POOL_PREF_DIST": 30.0,
    "POOL_PULL": 22.0,
}


def _parse_gc() -> dict[str, float]:
    src = GC.read_text(encoding="utf-8")
    out = {}
    for name in REGISTERED:
        m = re.search(rf"^const {name} := ([0-9.eE+-]+)", src, re.M)
        assert m, f"{name} missing from game_constants.gd"
        out[name] = float(m.group(1))
    return out


# --------------------------------------------------------------- value pin ----

def test_gc_values_pinned():
    got = _parse_gc()
    assert got == PINNED_VALUES, f"retune landed without updating the pin: {got}"


def test_gc_flee_radius_is_20_not_the_stale_14():
    # the drift law: flock.gd's 20 is canonical (Z14 terminal-speed math);
    # fish_brain.gd + mountain_units rode 14 until R7/R4 trued them up.
    assert _parse_gc()["FLEE_RADIUS"] == 20.0


# ------------------------------------------------------------ literal lint ----

def test_no_raw_literal_consts_outside_gc():
    offenders = []
    for gd in GODOT_TREE.rglob("*.gd"):
        if gd.name == "game_constants.gd":
            continue
        for i, line in enumerate(gd.read_text(encoding="utf-8").splitlines(), 1):
            for name in REGISTERED:
                if re.match(rf"^\s*const\s+{name}\s*:?=\s*-?\d", line):
                    offenders.append(f"{gd.relative_to(ROOT)}:{i}: {line.strip()}")
    assert not offenders, (
        "raw literal for a registered constant outside game_constants.gd — "
        "the V6 drift failure mode; alias GC instead:\n  " + "\n  ".join(offenders))


# ------------------------------------------------------------- alias pins ----

def test_flock_gd_aliases_gc():
    src = FLOCK_GD.read_text(encoding="utf-8")
    for name in ("FLEE_RADIUS", "CATCH_RADIUS", "SCHOOL_RADIUS", "TRAIL_RADIUS",
                 "FATIGUE_DECAY", "DRAG", "COAST_TIME", "FLEE_PUSH", "WIGGLE",
                 "TIRED", "TRAIL_DROP"):
        # (?=\s|$): alias lines carry inline receipt comments after the value
        assert re.search(rf"^const {name} := GC\.{name}(?=\s|$)", src, re.M), \
            f"flock.gd lost its GC alias for {name}"


def test_fish_brain_gd_aliases_gc():
    src = BRAIN_GD.read_text(encoding="utf-8")
    for name in ("FLEE_RADIUS", "CATCH_RADIUS", "SCHOOL_RADIUS", "TRAIL_RADIUS",
                 "TIRED", "POOL_PREF_DIST"):
        assert re.search(rf"^const {name} := GC\.{name}(?=\s|$)", src, re.M), \
            f"fish_brain.gd lost its GC alias for {name}"


# ---------------------------------------------------------- python twins ----

def test_flock_positive_python_twin_matches_gc():
    src = (ROOT / "mag" / "flock_positive.py").read_text(encoding="utf-8")
    name_map = {"POOL_PREF_DIST": "FOOD_PREF_DIST", "POOL_PULL": "FOOD_PULL"}
    # flock_positive mirrors only the steering law: no trail (visual only);
    # TIRED is inlined as a literal in its catch line (named-TIRED debt,
    # LM9's file) — pinned by parsing that literal below, so a GC.TIRED
    # retune that misses the Python twin still fails this suite
    skip = {"TRAIL_DROP", "TRAIL_RADIUS", "TIRED"}
    for gc_name in REGISTERED:
        if gc_name in skip:
            continue
        py_name = name_map.get(gc_name, gc_name)
        m = re.search(rf"^{py_name} = ([0-9.eE+-]+)", src, re.M)
        assert m, f"{py_name} missing from mag/flock_positive.py"
        assert float(m.group(1)) == PINNED_VALUES[gc_name], (
            f"python twin drift: {py_name}={m.group(1)} vs GC.{gc_name}="
            f"{PINNED_VALUES[gc_name]}")


def test_flock_positive_inline_tired_literal_pinned():
    """step_threat's catch line carries TIRED as an inline literal (not a
    named constant — LM9's file, outside R4 ownership): parse it and pin it
    to GC.TIRED, so the skip above is guarded, not silent."""
    src = (ROOT / "mag" / "flock_positive.py").read_text(encoding="utf-8")
    m = re.search(r"if dist < CATCH_RADIUS and f\.fatigue > ([0-9.]+)", src)
    assert m, "step_threat catch line moved — update this pin"
    assert float(m.group(1)) == PINNED_VALUES["TIRED"], (
        f"inline TIRED drift: step_threat catches above {m.group(1)} but "
        f"GC.TIRED={PINNED_VALUES['TIRED']} — true the literal up (Q15)")


def test_mountain_units_flee_radius_trued_to_gc():
    src = (ROOT / "tools" / "mountain_units.py").read_text(encoding="utf-8")
    m = re.search(r"^FLEE_RADIUS, SCHOOL_RADIUS, TRAIL_RADIUS = "
                  r"([0-9.]+), ([0-9.]+), ([0-9.]+)", src, re.M)
    assert m, "mountain_units constants line moved — update this pin"
    flee, school, trail = (float(m.group(i)) for i in (1, 2, 3))
    assert flee == 20.0, (
        f"mountain_units FLEE_RADIUS={flee} — the stale fish_brain-14 mirror; "
        f"GC.FLEE_RADIUS is 20.0 (R4 true-up, V6_FISH_FLEE.md handoff closed)")
    assert school == 20.0 and trail == 38.0


# ------------------------------------------------------- hash stability ----

def test_flock_parity_consts_hash_matches_gc():
    """The Q14 frame guard's alphabet: tools/flock_parity.py's hash is a
    pure function of the pinned GC values (a retune changes the hash, the
    runner then refuses stale frames with exit 3 — drift becomes a harness
    error, never a mysterious position diff)."""
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import flock_parity as fpar
    finally:
        sys.path.pop(0)
    consts = _parse_gc()
    assert fpar.consts_hash(consts) == fpar.consts_hash()  # pure function of GC
    h = fpar.consts_hash()
    assert re.fullmatch(r"[0-9a-f]{64}", h), h
    # independent re-derivation: same canonical text, same digest
    body = "".join(f"{n}={fpar.enc32(consts[n])}\n" for n in sorted(consts))
    import hashlib
    assert hashlib.sha256(body.encode()).hexdigest() == h
