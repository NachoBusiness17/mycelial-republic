"""R4 flock parity harness tests — the harness is the instrument, these
prove the instrument is faithful (V2ASK3 Q14 tests 1-6, adapted and named):

  1. CODEC ROUND-TRIP: float32 hex-bits transport is lossless — pure Python
     AND through the real headless Godot process (NaN, +-0, subnormals,
     +-inf, max float32, the constants themselves).
  2. SELF-PARITY: Python vs Python through the full harness is EXACT
     (determinism + the comparator adds no noise); GDScript vs GDScript
     across two separate Godot processes is byte-identical.
  3. KNOWN-ANSWER FRAMES: paper truth on the reference side — exactly at
     FLEE_RADIUS does NOT flee (strict <), R-1ulp flees, R+1ulp does not;
     a tired fish inside CATCH_RADIUS dies at tick 1; the mirror pair
     keeps cohesion antisymmetry.
  4. MUTATION SENSITIVITY: constant mutants on ONE side (the Python twin)
     must flip the comparator red — FLEE_RADIUS+1, CATCH_RADIUS-0.5,
     FLEE_PUSH+0.5, DRAG, WIGGLE x3, SCHOOL_RADIUS+2, COAST_TIME x2.
     (V2ASK3's branch mutants — `<` for `<=`, dt-drop, negated separation,
     stale velocity — need source-mutation tooling: named as debt in the
     receipt, not silently skipped.)
  5. ANTI-SENSITIVITY: a 1-ulp32 perturbation of one output position must
     stay GREEN — the tolerance's resolution floor, bounding it from below.
  6. HASH GUARD: a frame whose constants_hash is stale makes the GDScript
     runner exit 3 and write NOTHING (Q15 link).
  7. TEACHER FORCING: the emitted frame chain IS the quantized reference
     output (the bring-up bug this pins: float64 residue once rode the
     Python state while frames shipped float32 and flipped a neighbour
     verdict at exactly SCHOOL_RADIUS).
  8. THE HONEST VERDICT PIN: end-to-end through Godot, the ONLY divergence
     class is the known catch-tick law difference — flock.gd moves a caught
     fish (f.pos += f.vel*dt runs after alive=false, flock.gd:146-150)
     while mag/flock_positive.step_threat returns before the move. If the
     port is ever trued up, parity flips green and THIS test updates in the
     same commit (the pin law).

Receipt: watch/inbox/last_mile_20260930/R4_FLOCK_PARITY.md.
"""
from __future__ import annotations

import json
import struct
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

import flock_parity as fpar  # noqa: E402
from mag import flock_positive as fp  # noqa: E402

GODOT = fpar.GODOT_EXE
needs_godot = pytest.mark.skipif(not GODOT.exists(), reason="no godot binary")
SMOKE_SEED = 20260930


def _smoke_spec(ticks: int = 8) -> dict:
    return fpar.generate(SMOKE_SEED, 5, ticks)  # one of each family


def _run_py(spec: dict) -> tuple[list[dict], list[dict]]:
    return fpar.run_teacher(spec)


# ------------------------------------------------------------ 1. codec ----

def test_codec_roundtrip_python():
    for h in fpar.codec_corpus():
        assert fpar.enc32(fpar.dec32(h)) == h
    # exactness of the widening/narrowing alphabet
    assert fpar.dec32("0x439b0000") == 310.0  # 310.0 exact float32 bits
    assert fpar.dec32("0x439ac000") == 309.5
    assert fpar.f32b(1.0) == 0x3F800000
    assert fpar.f32b(-0.0) == 0x80000000
    assert struct.unpack("<f", struct.pack("<f", float("nan")))[0] != \
        struct.unpack("<f", struct.pack("<f", float("nan")))[0]  # NaN != NaN


@needs_godot
def test_codec_roundtrip_through_real_godot(tmp_path):
    doc = {"schema": fpar.CODEC_SCHEMA, "constants_hash": fpar.consts_hash(),
           "values": fpar.codec_corpus()}
    doc_p = tmp_path / "codec.json"
    doc_p.write_text(json.dumps(doc))
    out = tmp_path / "echo.jsonl"
    fpar._run_godot(doc_p, out)
    echo = json.loads(out.read_text().splitlines()[0])
    assert echo["values"] == doc["values"], "transport corrupted float32 bits"
    assert echo["sha256"] == fpar.consts_hash()


# ------------------------------------------------------- 2. self-parity ----

def test_self_parity_python_exact():
    spec = _smoke_spec()
    _, rows_a = _run_py(spec)
    _, rows_b = _run_py(spec)
    assert rows_a == rows_b  # determinism: same inputs, same bytes
    rep = fpar.compare(rows_a, rows_b, fpar.dec32(spec["dt"]))
    assert rep["parity"] and rep["edges"] == 0


@needs_godot
def test_self_parity_godot_two_processes(tmp_path):
    spec = _smoke_spec()
    frames, rows = _run_py(spec)
    doc = fpar._gd_doc_from_chain(spec, frames)
    doc_p = tmp_path / "doc.json"
    doc_p.write_text(json.dumps(doc))
    out1, out2 = tmp_path / "g1.jsonl", tmp_path / "g2.jsonl"
    fpar._run_godot(doc_p, out1)
    fpar._run_godot(doc_p, out2)
    assert out1.read_bytes() == out2.read_bytes(), \
        "two godot processes disagreed with themselves"


# ---------------------------------------------------- 3. known answers ----

def test_known_answer_threshold_verdicts():
    spec = _smoke_spec()
    _, rows = _run_py(spec)
    edge = next(r for r in rows if r["family"] == "threshold_edge" and r["tick"] == 1)
    by_id = {f["id"]: f for f in edge["fish"]}
    R = fpar.parse_gc()["FLEE_RADIUS"]
    catch_r = fpar.parse_gc()["CATCH_RADIUS"]
    # paper truth, PURE RADIAL probes (y=0: the ulp alone decides):
    # strict < — exactly R does NOT flee, R-1ulp DOES, R+1ulp does not
    assert by_id[0]["fleeing"] is False      # exactly at FLEE_RADIUS
    assert by_id[1]["fleeing"] is True       # R - 1 ulp32
    assert by_id[2]["fleeing"] is False      # R + 1 ulp32
    # tired fish inside the catch ring dies on tick 1 — deep (1.0px) AND at
    # the 3.4px seam (CATCH_RADIUS - 0.1: dead clean, the CATCH_RADIUS-0.5
    # mutation-sensitivity mutant leaves it alive)
    assert by_id[3]["alive"] is False and by_id[3]["caught"] is True
    assert by_id[5]["alive"] is False and by_id[5]["caught"] is True
    assert R == 20.0 and catch_r == 3.5  # the paper assumed the pinned tuning


def test_known_answer_school_radius_is_strict_and_wiggle_y_shared():
    """Tick 1 the mirror pair sits at EXACTLY SCHOOL_RADIUS (20.0): strict
    `<` means no schooling (a `<=` mutant lights this). Later ticks may
    legitimately dip the gap 1 ulp under via wiggle drift — NOT a violation
    (both sides must agree; the e2e verdict test covers that). While the
    pair is unschooled their y-velocities are BIT-IDENTICAL (same y, same
    wiggle phase, no forces but wiggle+drag); once schooling starts the
    in-place pass is deliberately asymmetric (flock.gd steps fish in index
    order over one array: fish j>k reads fish k's POST-move pos), so y-bit
    identity is asserted only for neighbor-free ticks — the lawful
    asymmetry itself is parity-checked against Godot, not pinned here."""
    spec = _smoke_spec()
    _, rows = _run_py(spec)
    t1 = next(r for r in rows if r["family"] == "hand_frames" and r["tick"] == 1)
    assert all(f["neighbors"] == [] for f in t1["fish"]), \
        "distance exactly SCHOOL_RADIUS must not school (strict <)"
    for r in rows:
        if r["family"] == "hand_frames" and not r["fish"][0]["neighbors"]:
            assert r["fish"][0]["vel"][1] == r["fish"][1]["vel"][1]


def test_no_deaths_without_threat():
    spec = _smoke_spec()
    _, rows = _run_py(spec)
    for r in rows:
        if r["family"] in ("free_school", "threat_sweep", "hand_frames"):
            assert all(f["alive"] for f in r["fish"])


# --------------------------------------------- 4. mutation sensitivity ----

MUTANTS = {
    "FLEE_RADIUS+1": {"FLEE_RADIUS": 21.0},
    "CATCH_RADIUS-0.5": {"CATCH_RADIUS": 3.0},
    "FLEE_PUSH+0.5": {"FLEE_PUSH": 6.5},
    "DRAG 0.99": {"DRAG": 0.99},
    "WIGGLE x3": {"WIGGLE": 0.15},
    "SCHOOL_RADIUS+2": {"SCHOOL_RADIUS": 22.0},
    "COAST_TIME x2": {"COAST_TIME": 1.6},
}


@pytest.mark.parametrize("name,patch", list(MUTANTS.items()),
                         ids=list(MUTANTS))
def test_mutation_sensitivity_constant_mutants_go_red(name, patch, monkeypatch):
    """Each constant mutant on the PYTHON side only must flip compare red
    on a corpus where the affected branch fires (5-seq smoke = every
    family). The comparator's Tier-D/Tier-C laws are the detector."""
    spec = _smoke_spec(12)
    clean_frames, clean_rows = _run_py(spec)
    for k, v in patch.items():
        monkeypatch.setattr(fp, k, v, raising=True)
    _, mutant_rows = _run_py(spec)
    rep = fpar.compare(clean_rows, mutant_rows, fpar.dec32(spec["dt"]),
                       clean_frames)
    assert not rep["parity"], f"mutant {name} survived the comparator"


@needs_godot
def test_mutation_sensitivity_end_to_end_vs_real_godot(tmp_path, monkeypatch):
    """The full falsifier: mutant Python vs the REAL GDScript engine."""
    spec = _smoke_spec(12)
    frames, clean_rows = _run_py(spec)
    doc = fpar._gd_doc_from_chain(spec, frames)
    doc_p = tmp_path / "doc.json"
    doc_p.write_text(json.dumps(doc))
    gd_out = tmp_path / "gd.jsonl"
    fpar._run_godot(doc_p, gd_out)
    gd_rows = [json.loads(x) for x in gd_out.read_text().splitlines() if x.strip()]
    monkeypatch.setattr(fp, "FLEE_RADIUS", 21.0)
    _, mutant_rows = _run_py(spec)
    rep = fpar.compare(mutant_rows, gd_rows, fpar.dec32(spec["dt"]), frames)
    assert not rep["parity"]
    assert rep["first_divergence"]["kind"].startswith("tier_")


# ----------------------------------------------- 5. anti-sensitivity ----

def test_anti_sensitivity_one_ulp_perturbation_stays_green():
    spec = _smoke_spec()
    frames, rows = _run_py(spec)
    # perturb ONE fish's output pos by exactly 1 ulp32 at ONE tick (the gd
    # side receiving one-ulp-different input)
    victim = next(r for r in rows if r["family"] == "free_school" and r["tick"] == 3)
    f = victim["fish"][0]
    bits = int(f["pos"][0], 16) + 1
    f["pos"][0] = f"0x{bits:08x}"
    _, clean = _run_py(spec)  # fresh unperturbed reference
    rep = fpar.compare(clean, rows, fpar.dec32(spec["dt"]), frames)
    assert rep["parity"], "1-ulp perturbation must stay inside the epsilon"


# ------------------------------------------------------- 6. hash guard ----

@needs_godot
def test_hash_guard_stale_constants_exit_3(tmp_path):
    doc = {"schema": fpar.CODEC_SCHEMA,
           "constants_hash": "0" * 64,  # stale: not the GC digest
           "values": ["0x3f800000"]}
    doc_p = tmp_path / "stale.json"
    doc_p.write_text(json.dumps(doc))
    out = tmp_path / "stale_out.jsonl"
    proc = subprocess.run(
        [str(GODOT), "--headless", "--path", str(fpar.GODOT_PROJECT),
         "--script", fpar.GD_RUNNER, "--", str(doc_p), str(out)],
        capture_output=True, text=True, cwd=str(fpar.GODOT_PROJECT), timeout=120)
    assert proc.returncode == 3, f"stale constants must exit 3, got {proc.returncode}"
    assert not out.exists() or not out.read_text().strip(), \
        "guard refused AFTER writing output — a refused frame must produce nothing"


# --------------------------------------------------- 7. teacher forcing ----

def test_teacher_forcing_chain_is_quantized_output():
    spec = _smoke_spec()
    frames, rows = _run_py(spec)
    by_key = {(r["seq"], r["tick"]): r for r in rows}
    checked = 0
    for fr in frames[1:]:
        prev = by_key.get((fr["seq"], fr["tick"] - 1))
        if prev is None:
            continue
        prev_fish = {f["id"]: f for f in prev["fish"]}
        for f in fr["fish"]:
            if f["id"] in prev_fish:
                # every tick's input IS the previous tick's emitted bits —
                # the float64 residue the bring-up bug once let ride
                assert f["pos"] == prev_fish[f["id"]]["pos"], \
                    f"frame {fr['seq']} t{fr['tick']} fish {f['id']} input " \
                    f"is not the quantized reference output"
                checked += 1
    assert checked > 100


def test_twin_guard_raises_on_value_twins():
    twins = [fp.Fish(pos=(5.0, 5.0)), fp.Fish(pos=(5.0, 5.0)),
             fp.Fish(pos=(100.0, 100.0))]
    with pytest.raises(RuntimeError, match="value-twin"):
        fpar._twin_check(twins)


# --------------------------------------------- 8. the honest verdict ----

@needs_godot
def test_end_to_end_only_known_divergence_is_catch_tick_move(tmp_path):
    """The pinned honest verdict (full pipeline through real Godot): every
    family holds parity EXCEPT the catch tick, where flock.gd moves the
    caught fish and the port freezes it. First divergence must be that
    class — any OTHER class is a new, unnamed divergence and must fail
    here loudly."""
    spec = _smoke_spec(12)
    frames, rows = _run_py(spec)
    doc = fpar._gd_doc_from_chain(spec, frames)
    doc_p = tmp_path / "doc.json"
    doc_p.write_text(json.dumps(doc))
    gd_out = tmp_path / "gd.jsonl"
    fpar._run_godot(doc_p, gd_out)
    gd_rows = [json.loads(x) for x in gd_out.read_text().splitlines() if x.strip()]
    rep = fpar.compare(rows, gd_rows, fpar.dec32(spec["dt"]), frames)
    fd = rep["first_divergence"]
    assert fd is not None, (
        "parity went fully green — the catch-tick law was trued up; update "
        "this pin and the receipt in the same commit")
    assert fd["kind"] == "tier_c_pos", f"new divergence class: {fd}"
    assert "pos" in fd["detail"]
    assert rep["per_family"]["free_school"]["diverged_seqs"] == 0
    assert rep["per_family"]["threat_sweep"]["diverged_seqs"] == 0
    assert rep["per_family"]["hand_frames"]["diverged_seqs"] == 0


# --------------------------------------------------------- epsilon law ----

def test_ulp32_law():
    assert fpar.ulp32(1.0) == 2.0 ** -23
    assert fpar.ulp32(0.0) == 2.0 ** -149
    assert fpar.ulp32(fpar.b32f(0x7F7FFFFF)) == 2.0 ** 104
    assert fpar.ulp32(300.0) == fpar.b32f(0x43960000) - fpar.b32f(0x4395FFFF)
    ok, eps, dev = fpar._tol(300.0, 300.0 + 3 * fpar.ulp32(300.0),
                             fpar.TIER_K_CONT, 1 / 60)
    assert ok and dev < eps


def test_band_law():
    # 8*ulp32(R^2): at R=20 -> band ~2.4e-4 on the SQUARED distance
    R = 20.0
    assert fpar.band(R) == 8 * fpar.ulp32(400.0)
    assert abs(400.0 - (R - 1) ** 2) > fpar.band(R)  # 1px off is NOT an edge
