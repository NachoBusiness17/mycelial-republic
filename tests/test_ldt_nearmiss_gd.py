"""ldt_nearmiss GDScript twin tests — Q18's FAIL answered (2026-10-01).

Q18 (watch/inbox/mountain_climb/FIFTY_QUESTIONS_ANSWERED.md row 18):
"imports of tests/test_ldt_nearmiss.py: numpy + tools.* python modules
only; no GDScript/godot references. FAIL: near-miss twins exercise the
python engine only; the GD twin V5 caught diverging is untouched."

This file closes that gap the honest way: the SCALAR kernel of the
near-miss scoring — the per-row margin/threshold rule around the argmax
(raw: argmax + max>=tau; strict/renorm: masked argmax, masked-max
confidence, renorm mass division with the 1e-12 clamp) — is ported to
roblox_to_godot/tests/ldt_nearmiss_runner.gd and compared verdict-for-
verdict across languages on a FROZEN corpus of boundary cases (exact-tau
confidences, first-max ties, mask flips, renorm clamps, float32-trap
values; handcrafted spine + seeded sweep, byte-pinned by sha256).

WHAT IS / IS NOT PORTED (the twin's honesty block, mirrored):
  PORTED      the scalar verdict rule of tools/ldt_lattice.py
              evaluate_lattice (:403-417) and tools/ldt_nearmiss.py _arm
              (:224 raw, :227-234 strict/renorm), first-max tie rule,
              float64, identical op order.
  NOT PORTED  the MLP forward pass (numpy float32 matmuls — probs are
              INPUTS, bit-transported); the numpy row vectorization (the
              rule is ported, not the vectorization); the featurizer and
              the Y10 propagator (feasible masks and labels are python-
              side inputs); fleet aggregates (soundness/coverage are
              tallies over row verdicts, not verdicts).

FLOAT LAW (Q14 flock lesson, applied): every float crosses the wire as
IEEE-754 double BITS in hex (little-endian pinned by hand both sides,
flock_parity_runner.gd's codec rule at 64 bits) — decimal JSON parses
differently per runtime and Godot's Vector paths are float32, so a
float32/float64 boundary disagreement on this corpus is a banked FINDING
with a root cause, never hidden. tau travels as bits; the only float
literals inside the GD twin are 1e-12 (the renorm clamp) and 0.0 — live
divergence axes on purpose (the corpus exercises both).

Family-integration OWED (not taken): tools/rule_parity.py is another
lane's active edit, so this twin is a standalone test file per the
ownership contract; folding it into the rule_parity `all` family table
(family "ldt_nearmiss") is named debt for when that lane lands.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import struct
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.ldt_lattice import evaluate_lattice  # noqa: E402
from tools.ldt_train import LABELS, LABEL_TO_IDX  # noqa: E402
from tools.ldt_nearmiss import _arm  # noqa: E402

GODOT = ROOT / "tools" / "godot" / "Godot_v4.3-stable_win64.exe"
GODOT_PROJECT = ROOT / "roblox_to_godot"
GD_RUNNER = "res://tests/ldt_nearmiss_runner.gd"
needs_godot = pytest.mark.skipif(not GODOT.exists(), reason="no godot binary")

TAU = 0.7                      # the V7 protocol pin
MODES = ("raw", "strict", "renorm")
GAIN = LABEL_TO_IDX["legal_gain"]
SCHEMA = "ldt_nearmiss_parity.v1"
# the frozen corpus's byte identity (handcrafted spine + seeded sweep)
CORPUS_SHA256 = "357c9f9f5df60f4e8d4a443bbbcbc3bfb7138097a16d2ae9ebcf8939fa6b63e3"
N_SWEEP = 60
SWEEP_SEED = 20261001

# the 7 feasible-set shapes the Y10 cascade can actually produce
# (cascade_chain levels: TOP, -verb, -verb-target, -verb-target-dry,
# plus the three illegal singletons)
CASCADE_SHAPES = ({0}, {1}, {2}, {3, 4}, {2, 3, 4}, {1, 2, 3, 4},
                  {0, 1, 2, 3, 4})


# ------------------------------------------------------------ float codec ----
# Little-endian pinned by hand (GD twin composes/decomposes PackedByteArray
# bytes itself); subnormals, +-0 and tau all ride exact bits.

def hx(x: float) -> str:
    return "0x%016x" % struct.unpack("<Q", struct.pack("<d", float(x)))[0]


def unhx(s: str) -> float:
    return struct.unpack("<d", struct.pack("<Q", int(s, 16)))[0]


def bits(x: float) -> int:
    return struct.unpack("<Q", struct.pack("<d", float(x)))[0]


# --------------------------------------------------------- scalar kernel ----
# The python mirror of the GD twin (and of the engine's own rule). Identical
# op order to roblox_to_godot/tests/ldt_nearmiss_runner.gd _verdict().

def scalar_verdict(probs: list[float], feasible: list[bool], tau: float,
                   mode: str) -> dict:
    """One row through the margin/threshold rule around the argmax."""
    if mode == "raw":
        best = 0
        for j in range(1, len(probs)):
            if probs[j] > probs[best]:
                best = j
        conf = probs[best]
        return {"pred": best, "answered": conf >= tau, "conf": conf,
                "pred_is_gain": best == GAIN}
    any_f = any(feasible)
    if not any_f:
        return {"pred": -1, "answered": False, "conf": 0.0,
                "pred_is_gain": False}
    best = -1
    for j in range(len(probs)):
        if feasible[j] and (best < 0 or probs[j] > probs[best]):
            best = j
    conf = probs[best]
    if mode == "renorm":
        mass = 0.0
        for j in range(len(probs)):
            mass += probs[j] if feasible[j] else 0.0
        conf = conf / max(mass, 1e-12) if mass > 0.0 else 0.0
    return {"pred": best, "answered": conf >= tau, "conf": conf,
            "pred_is_gain": best == GAIN}


# ------------------------------------------------------------- the corpus ----

def _hand_spine() -> list[dict]:
    """Boundary rows, hand-named. Values are exact doubles; nextafter
    neighbors of tau, float32 roundings of tau, exact ties, mask flips,
    renorm clamp arms, one empty-mask guard row."""
    below = float(np.nextafter(TAU, 0.0))          # tau - 1 ulp64
    above = float(np.nextafter(TAU, 2.0))          # tau + 1 ulp64
    f32_tau = float(np.float32(TAU))               # rounds BELOW tau in f64
    f32_up = float(np.nextafter(np.float32(TAU), np.float32(np.inf)))
    under8 = float(np.nextafter(0.8, 0.0))
    tie_up = float(np.nextafter(0.35, math.inf))   # f64-distinct, f32-equal
    allf = [True] * 5

    def row(rid, fam, probs, feas, y):
        return {"id": rid, "family": fam, "probs": [float(p) for p in probs],
                "feasible": [j in feas for j in range(5)], "y": y}

    return [
        # exact-tau boundary (>= is the law; both neighbors probed)
        row("tau_exact_allfeas", "tau_exact",
            [TAU, 0.1, 0.05, 0.05, 0.1], set(range(5)), 0),
        row("tau_below_1ulp", "tau_exact",
            [below, 0.1, 0.05, 0.05, 0.1], set(range(5)), 0),
        row("tau_above_1ulp", "tau_exact",
            [above, 0.1, 0.05, 0.05, 0.1], set(range(5)), 0),
        # float32 traps: a float32 engine rounds/moves these across tau
        row("tau_f32_rounds_below", "tau_exact",
            [f32_tau, 0.1, 0.05, 0.05, 0.1], set(range(5)), 0),
        row("tau_f32_nextabove", "tau_exact",
            [f32_up, 0.1, 0.05, 0.05, 0.1], set(range(5)), 0),
        row("tau_exact_strict_singleton", "tau_exact",
            [0.05, 0.05, TAU, 0.1, 0.1], {2}, 2),
        row("tau_exact_renorm_half_mass", "tau_exact",
            [0.2, 0.3, 0.0, 0.35, 0.15], {3, 4}, 4),
        # first-max ties (numpy argmax law: FIRST occurrence wins)
        row("tie_first_two", "argmax_tie",
            [0.4, 0.4, 0.1, 0.05, 0.05], set(range(5)), 1),
        row("tie_1_3", "argmax_tie",
            [0.1, 0.4, 0.05, 0.4, 0.05], set(range(5)), 3),
        row("tie_gain_split_raw_nogain", "argmax_tie",
            [0.05, 0.05, 0.05, 0.4, 0.4], set(range(5)), 4),
        row("tie_feasible_singleton_cure", "argmax_tie",
            [0.05, 0.05, 0.45, 0.05, 0.45], {2}, 2),
        row("tie_half_half_masked_gain", "argmax_tie",
            [0.05, 0.05, 0.05, 0.5, 0.5], {4}, 4),
        # mask flips: raw argmax infeasible -> projection moves the answer
        row("flip_fooled_gain_08", "mask_flip",
            [0.05, 0.05, 0.05, 0.05, 0.8], {2}, 2),
        row("flip_fooled_gain_1ulp_under", "mask_flip",
            [0.05, 0.05, 0.05, 0.05, under8], {2}, 2),
        row("flip_lowconf_gain", "mask_flip",
            [0.05, 0.05, 0.8, 0.05, 0.1], {3, 4}, 4),
        row("flip_control_mask_agrees", "mask_flip",
            [0.3, 0.0, 0.0, TAU, 0.0], {3}, 3),
        # renorm rescues: strict abstains, renorm divides across tau
        row("rescue_06_of_07", "renorm_rescue",
            [0.6, 0.2, 0.05, 0.05, 0.1], {0, 4}, 0),
        row("rescue_05_of_06", "renorm_rescue",
            [0.5, 0.2, 0.1, 0.1, 0.1], {0, 4}, 0),
        row("rescue_none_04_of_09", "renorm_rescue",
            [0.4, 0.3, 0.2, 0.1, 0.0], {0, 1, 2}, 0),
        # the renorm 1e-12 clamp and its mass>0 guard
        row("clamp_mass_1e_13", "renorm_clamp",
            [0.4, 0.3, 1e-13, 0.2, 0.1], {2}, 2),
        row("clamp_mass_zero", "renorm_clamp",
            [0.4, 0.3, 0.0, 0.2, 0.1], {2}, 2),
        row("clamp_mass_2e_12", "renorm_clamp",
            [0.4, 0.3, 2e-12, 0.2, 0.1], {2}, 2),
        row("clamp_subnormal_conf", "renorm_clamp",
            [0.4, 0.3, 0.2, 5e-324, 0.1], {3}, 3),
        # empty feasible set: the kernel's guard (never empty in real data)
        row("empty_mask_all_false", "empty_mask",
            [0.9, 0.05, 0.02, 0.02, 0.01], set(), 3),
        # float32 sum/order traps: values whose f32 rounding reorders the
        # argmax or the mass (f64 must agree; f32 would not)
        row("f32_sum_mass_trap", "f32_trap",
            [0.1, 0.2, 0.4, 0.15, 0.15], set(range(5)), 2),
        row("f32_argmax_order_trap", "f32_trap",
            [0.35, tie_up, 0.1, 0.1, 0.1], set(range(5)), 1),
        # cascade-shape controls (every real lattice F shape at least once)
        row("shape_singleton_verb", "lattice_shape",
            [0.6, 0.2, 0.1, 0.05, 0.05], {0}, 0),
        row("shape_singleton_target", "lattice_shape",
            [0.2, 0.6, 0.1, 0.05, 0.05], {1}, 1),
        row("shape_legal_pair_tie", "lattice_shape",
            [0.1, 0.1, 0.1, 0.35, 0.35], {3, 4}, 4),
        row("shape_top_minus_verb", "lattice_shape",
            [0.1, 0.55, 0.1, 0.1, 0.15], {1, 2, 3, 4}, 4),
        row("shape_top", "lattice_shape",
            [0.05, 0.05, 0.05, 0.05, 0.8], set(range(5)), 4),
        row("shape_minus_verb_target", "lattice_shape",
            [0.05, 0.05, 0.6, 0.2, 0.15], {2, 3, 4}, 2),
    ]


def _first_argmax(xs: list[float]) -> int:
    best = 0
    for j in range(1, len(xs)):
        if xs[j] > xs[best]:
            best = j
    return best


def _sweep(seed: int, n: int) -> list[dict]:
    """Seeded margin sweep: near-tau maxima, forced exact ties, cascade
    feasible shapes. One rng stream, no wall clock — byte-frozen."""
    rng = random.Random(seed)
    shapes = [s for s in CASCADE_SHAPES]
    rows: list[dict] = []
    for i in range(n):
        probs = [rng.random() for _ in range(5)]
        r = rng.random()
        if r < 0.40:  # exact tie at the top: duplicate max onto runner-up
            order = sorted(range(5), key=lambda j: (probs[j], -j))
            probs[order[-2]] = probs[order[-1]]
        elif r < 0.80:  # snap the (first) argmax to tau +- k ulp64
            k = rng.randint(0, 3)
            v = TAU
            for _ in range(k):
                v = float(np.nextafter(v, math.inf if rng.random() < 0.5
                                       else -math.inf))
            probs[_first_argmax(probs)] = v
        shape = shapes[rng.randrange(len(shapes))]
        rows.append({
            "id": f"sweep_{i:03d}", "family": "sweep", "probs": probs,
            "feasible": [j in shape for j in range(5)],
            "y": rng.choice(sorted(shape)),
        })
    return rows


def build_rows() -> list[dict]:
    return _hand_spine() + _sweep(SWEEP_SEED, N_SWEEP)


def build_corpus_doc(rows: list[dict] | None = None) -> dict:
    rows = build_rows() if rows is None else rows
    return {
        "schema": SCHEMA,
        "labels": list(LABELS),
        "tau_hex": hx(TAU),
        "rows": [{"id": r["id"], "family": r["family"],
                  "probs_hex": [hx(p) for p in r["probs"]],
                  "feasible": list(r["feasible"]), "y": r["y"]}
                 for r in rows],
    }


def corpus_bytes(doc: dict | None = None) -> bytes:
    doc = build_corpus_doc() if doc is None else doc
    return json.dumps(doc, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"


# ----------------------------------------------------- python-side engine ----
# The engine's own numpy expressions (verbatim shapes from
# tools/ldt_lattice.py evaluate_lattice :403-413 and the raw arm of
# tools/ldt_nearmiss.py _arm :224) evaluated per-row, for faithfulness.

def _engine_extraction(P: np.ndarray, feasibles: list[list[bool]], tau: float,
                       ) -> dict[str, list[tuple[int, bool, float]]]:
    mask = np.array(feasibles, dtype=bool)
    out: dict[str, list[tuple[int, bool, float]]] = {}
    parg, pmax = P.argmax(axis=1), P.max(axis=1)
    out["raw"] = [(int(parg[i]), bool(pmax[i] >= tau), float(pmax[i]))
                  for i in range(len(P))]
    neg = np.where(mask, P, -np.inf)
    pred = neg.argmax(axis=1)
    conf = neg.max(axis=1).astype(np.float64)
    empty = ~mask.any(axis=1)
    pred = np.where(empty, -1, pred)
    any_f = mask.any(axis=1)
    conf = np.where(any_f, conf, 0.0)
    out["strict"] = [(int(pred[i]), bool(conf[i] >= tau and not empty[i]),
                      float(conf[i])) for i in range(len(P))]
    mass = (P * mask).sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        conf_r = np.where(any_f & (mass > 0),
                          conf / np.maximum(mass, 1e-12), 0.0)
    out["renorm"] = [(int(pred[i]), bool(conf_r[i] >= tau and not empty[i]),
                      float(conf_r[i])) for i in range(len(P))]
    return out


def _random_rows(seed: int, n: int) -> list[dict]:
    return _sweep(seed, n)  # the sweep generator IS the margin sampler


# ---------------------------------------------------------------- compare ----

def compare(doc: dict, gd_rows: list[dict]) -> list[dict]:
    """Comparator: python scalar reference vs the GD twin's rows, all three
    modes, verdict fields + conf BITS. Returns the divergence list (empty =
    parity). The tamper-sensitivity test proves every field is load-bearing.
    """
    divs: list[dict] = []
    for crow, grow in zip(doc["rows"], gd_rows):
        probs = [unhx(h) for h in crow["probs_hex"]]
        feasible = list(crow["feasible"])
        if crow["id"] != grow.get("id"):
            divs.append({"id": crow["id"], "mode": "-",
                         "field": "row_id", "py": crow["id"],
                         "gd": grow.get("id")})
            continue
        for mode in MODES:
            want = scalar_verdict(probs, feasible, TAU, mode)
            got = grow.get(mode, {})
            checks = (("pred", want["pred"], got.get("pred")),
                      ("answered", want["answered"], got.get("answered")),
                      ("conf_bits", hx(want["conf"]), got.get("conf_hex")),
                      ("pred_is_gain", want["pred_is_gain"],
                       got.get("pred_is_gain")))
            for field, pv, gv in checks:
                if pv != gv:
                    divs.append({"id": crow["id"], "family": crow["family"],
                                 "mode": mode, "field": field,
                                 "py": pv, "gd": gv})
    return divs


def _run_godot(doc_path: Path, out_path: Path) -> None:
    cmd = [str(GODOT), "--headless", "--path", str(GODOT_PROJECT),
           "--script", GD_RUNNER, "--", str(doc_path.resolve()),
           str(out_path.resolve())]
    proc = subprocess.run(cmd, capture_output=True, text=True,
                          cwd=str(GODOT_PROJECT), timeout=120)
    if proc.returncode != 0:
        raise RuntimeError(f"godot runner exited {proc.returncode}\n"
                           f"stdout:\n{proc.stdout[-2000:]}\n"
                           f"stderr:\n{proc.stderr[-2000:]}")


# ================================================================= tests ====

def test_codec_roundtrip_boundary_doubles():
    """The hex-bits transport is lossless on the corpus's boundary alphabet
    (python side; the GD side's codec is proven by the tau echo + every
    conf_bits comparison through the real Godot process)."""
    vals = [TAU, float(np.nextafter(TAU, 0.0)), float(np.nextafter(TAU, 2.0)),
            float(np.float32(TAU)), 0.0, -0.0, 1e-12, 5e-324, 1e-300, 0.35,
            float(np.nextafter(0.35, math.inf)), 0.8, 1.0, 0.15]
    for v in vals:
        assert unhx(hx(v)) == v or bits(unhx(hx(v))) == bits(v)
        assert hx(unhx(hx(v))) == hx(v)
    assert bits(0.0) != bits(-0.0)          # sign survives the transport
    assert sys.byteorder == "little", \
        "transport is pinned little-endian by hand on both sides"


def test_corpus_frozen_deterministic_sha():
    """The corpus is FROZEN: same bytes every build, sha-pinned, spine laws
    present (exact-tau arms, first-max ties, mask flips, clamps, the empty
    guard). A sha change means the corpus moved — update the pin AND the
    receipt together, never silently."""
    doc_a, doc_b = build_corpus_doc(), build_corpus_doc()
    ba, bb = corpus_bytes(doc_a), corpus_bytes(doc_b)
    assert ba == bb
    sha = hashlib.sha256(ba).hexdigest()
    assert sha == CORPUS_SHA256, (
        f"corpus bytes moved: sha256 {sha} != pinned {CORPUS_SHA256} — "
        "update CORPUS_SHA256 and the receipt in the same commit")
    assert len(doc_a["rows"]) == 32 + N_SWEEP
    assert doc_a["tau_hex"] == hx(TAU)

    # spine laws (corpus rot guard)
    rows = {r["id"]: r for r in build_rows()}
    sv = {rid: {m: scalar_verdict(rows[rid]["probs"], rows[rid]["feasible"],
                                  TAU, m) for m in MODES}
          for rid in rows}
    assert sv["tau_exact_allfeas"]["raw"]["conf"] == TAU
    assert sv["tau_exact_allfeas"]["raw"]["answered"] is True
    assert sv["tau_below_1ulp"]["raw"]["answered"] is False
    assert sv["tau_above_1ulp"]["raw"]["answered"] is True
    assert sv["tau_f32_rounds_below"]["raw"]["answered"] is False  # f64 law
    # first-max tie rule
    assert sv["tie_first_two"]["raw"]["pred"] == 0
    assert sv["tie_1_3"]["raw"]["pred"] == 1
    assert sv["tie_gain_split_raw_nogain"]["raw"]["pred"] == 3
    # the near-miss row: 0.5/0.5 no_gain-vs-gain, feasible singleton {gain}
    nm = sv["tie_half_half_masked_gain"]
    assert nm["raw"]["pred"] == 3 and not nm["raw"]["answered"]
    assert nm["strict"]["pred"] == 4 and not nm["strict"]["answered"]
    assert nm["renorm"]["conf"] == 1.0 and nm["renorm"]["answered"]
    # the fooled twin: raw votes gain on an illegal singleton
    ff = sv["flip_fooled_gain_08"]
    assert ff["raw"]["pred_is_gain"] and ff["raw"]["answered"]
    assert ff["renorm"]["conf"] == 1.0 and ff["renorm"]["answered"]
    # clamp + empty guard
    assert sv["clamp_mass_2e_12"]["renorm"]["answered"] is True
    assert sv["clamp_mass_zero"]["renorm"]["conf"] == 0.0
    assert sv["empty_mask_all_false"]["strict"]["pred"] == -1
    # corpus-level near-miss dynamics actually present
    flips = sum(1 for rid in rows
                if sv[rid]["raw"]["pred"] != sv[rid]["strict"]["pred"])
    ties = sum(1 for rid in rows
               if rows[rid]["probs"].count(max(rows[rid]["probs"])) > 1)
    assert flips >= 6, f"corpus lost its mask-flip spine ({flips})"
    assert ties >= 20, f"corpus lost its tie spine ({ties})"


def test_scalar_reference_matches_engine_extraction_lines():
    """Instrument faithfulness 1: the scalar mirror computes BIT-IDENTICAL
    confidences to the engine's own numpy expressions on the whole corpus
    plus fresh random margin rows."""
    for rows in (build_rows(), _random_rows(777, 400)):
        P = np.array([r["probs"] for r in rows], dtype=np.float64)
        feas = [r["feasible"] for r in rows]
        eng = _engine_extraction(P, feas, TAU)
        for mode in MODES:
            for i, r in enumerate(rows):
                want = scalar_verdict(r["probs"], r["feasible"], TAU, mode)
                ep, ea, ec = eng[mode][i]
                assert want["pred"] == ep, (mode, r["id"])
                assert want["answered"] == ea, (mode, r["id"])
                assert bits(want["conf"]) == bits(ec), (
                    mode, r["id"], hx(want["conf"]), hx(ec))


def test_scalar_reference_matches_evaluate_lattice_aggregates():
    """Instrument faithfulness 2: the REAL engine (tools.ldt_lattice
    evaluate_lattice) tallies exactly what the scalar mirror answers, on
    the corpus and a fresh batch, both projection modes, several taus."""
    batches = [(build_rows(), "corpus")] + \
              [(_random_rows(seed, 250), f"rand{seed}")
               for seed in (101, 202, 303)]
    for rows, tag in batches:
        P = np.array([r["probs"] for r in rows], dtype=np.float64)
        feas_names = [frozenset(LABELS[j] for j in range(5)
                                if r["feasible"][j]) for r in rows]
        y = np.array([r["y"] for r in rows], dtype=np.int64)
        for tau in (0.5, TAU, 0.9):
            for mode in ("strict", "renorm"):
                lat = evaluate_lattice(P, feas_names, y, tau, mode=mode)
                ans = corr = 0
                infeas = 0
                for i, r in enumerate(rows):
                    v = scalar_verdict(r["probs"], r["feasible"], tau, mode)
                    ok = v["pred"] == y[i]
                    if v["answered"]:
                        ans += 1
                        corr += int(ok)
                        if LABELS[v["pred"]] not in feas_names[i]:
                            infeas += 1
                assert lat["answered"] == ans, (tag, mode, tau)
                assert lat["answered_correct"] == corr, (tag, mode, tau)
                assert lat["answered_wrong"] == ans - corr, (tag, mode, tau)
                assert lat["answered_infeasible"] == infeas == 0


def test_scalar_reference_matches_nearmiss_arm_aggregates():
    """Instrument faithfulness 3: the raw arm of tools.ldt_nearmiss._arm
    (the experiment's own scorer) tallies the scalar mirror — answered,
    forced accuracy, and fooled_into_gain on twin-shaped rows."""
    rows = build_rows()
    P = np.array([r["probs"] for r in rows], dtype=np.float64)
    feas_names = [frozenset(LABELS[j] for j in range(5)
                            if r["feasible"][j]) for r in rows]
    y = np.array([r["y"] for r in rows], dtype=np.int64)
    # twin shape = an illegal singleton feasible set (the near-miss twins)
    is_twin = np.array([len(f) == 1 and "illegal_" in next(iter(f))
                        for f in feas_names])
    family = np.array([r["family"] for r in rows])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)  # empty orig/twin slices
        arm = _arm("probe", P, feas_names, y, is_twin, family, TAU, "raw")
    ans = corr = fooled = 0
    correct: list[bool] = []
    for i, r in enumerate(rows):
        v = scalar_verdict(r["probs"], r["feasible"], TAU, "raw")
        ok = v["pred"] == y[i]
        correct.append(ok)
        if v["answered"]:
            ans += 1
            corr += int(ok)
        if is_twin[i] and v["pred"] == GAIN:
            fooled += 1
    assert arm["all"]["answered"] == ans
    assert arm["all"]["answered_correct"] == corr
    assert arm["all"]["forced_acc"] == float(np.mean(correct))
    assert arm["twin"]["fooled_into_gain"] == fooled
    assert fooled >= 3, "the corpus lost its fooled-into-gain near-miss rows"


@needs_godot
def test_gd_twin_parity_zero_divergences(tmp_path):
    """THE Q18 VERDICT: the GD twin answers the frozen boundary corpus
    verdict-for-verdict with the python scalar kernel — pred, answered and
    conf BITS across all three modes. Expected: 0 divergences. Any float32/
    float64 boundary disagreement is a banked FINDING (root cause below in
    the assertion rollup), never hidden."""
    doc = build_corpus_doc()
    doc_p = tmp_path / "corpus.json"
    doc_p.write_bytes(corpus_bytes(doc))
    out = tmp_path / "gd.jsonl"
    _run_godot(doc_p, out)
    gd_rows = [json.loads(x) for x in out.read_text().splitlines() if x.strip()]
    assert len(gd_rows) == len(doc["rows"])
    assert all(r["tau_echo_hex"] == doc["tau_hex"] for r in gd_rows), \
        "tau transport corrupted (endianness or codec drift)"
    divs = compare(doc, gd_rows)
    rollup: dict[str, int] = {}
    for d in divs:
        rollup[f"{d['mode']}.{d['field']}"] = \
            rollup.get(f"{d['mode']}.{d['field']}", 0) + 1
    assert divs == [], (
        f"GD twin diverged on {len(divs)} of "
        f"{len(doc['rows']) * 3} verdicts: {rollup}; first 5: {divs[:5]}")


@needs_godot
def test_gd_twin_self_parity_two_processes(tmp_path):
    """Determinism of the twin: two separate headless Godot processes on
    the same corpus produce byte-identical output."""
    doc = build_corpus_doc()
    doc_p = tmp_path / "corpus.json"
    doc_p.write_bytes(corpus_bytes(doc))
    out1, out2 = tmp_path / "gd1.jsonl", tmp_path / "gd2.jsonl"
    _run_godot(doc_p, out1)
    _run_godot(doc_p, out2)
    assert out1.read_bytes() == out2.read_bytes(), \
        "two godot processes disagreed with themselves"


def test_comparator_flags_tampered_verdicts():
    """Comparator sensitivity (the flock mutation law, cheap arm): a
    tampered pred / answered / conf bit / pred_is_gain on the GD side must
    flip the comparator red with the right field named."""
    doc = build_corpus_doc()
    rows = build_rows()
    good = []
    for r in rows:
        entry = {"id": r["id"]}
        for mode in MODES:
            v = scalar_verdict(r["probs"], r["feasible"], TAU, mode)
            entry[mode] = {"pred": v["pred"], "answered": v["answered"],
                           "conf_hex": hx(v["conf"]),
                           "pred_is_gain": v["pred_is_gain"]}
        good.append(entry)

    def tampered(field: str) -> list[dict]:
        out = [dict(e) for e in good]
        victim = dict(out[7])
        inner = dict(victim["strict"])
        if field == "pred":
            inner["pred"] = (inner["pred"] + 1) % 5
        elif field == "answered":
            inner["answered"] = not inner["answered"]
        elif field == "conf_bits":
            inner["conf_hex"] = "0x" + "0" * 15 + "1"
        elif field == "pred_is_gain":
            inner["pred_is_gain"] = not inner["pred_is_gain"]
        victim["strict"] = inner
        out[7] = victim
        return out

    for field in ("pred", "answered", "conf_bits", "pred_is_gain"):
        divs = compare(doc, tampered(field))
        assert divs and all(d["field"] == field and d["mode"] == "strict"
                            and d["id"] == doc["rows"][7]["id"]
                            for d in divs), (field, divs)
    # 1-bit conf tamper on a DIFFERENT mode too (raw conf = max prob)
    out = [dict(e) for e in good]
    out[3] = dict(out[3])
    out[3]["renorm"] = dict(out[3]["renorm"])
    out[3]["renorm"]["conf_hex"] = "0xdeadbeefdeadbeef"
    divs = compare(doc, out)
    assert divs and divs[0]["mode"] == "renorm" and \
        divs[0]["field"] == "conf_bits"
