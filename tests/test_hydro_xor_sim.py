"""Tests for mag/hydro_xor_sim.py — the sim side of C18's falsifier section 4.5.

Three laws from the U3 wave-lane mission:
  1. determinism   — same inputs -> bit-identical outputs (noise off; and seeded noise
                     is itself deterministic).
  2. P-consistency — the sim satisfies its own P1-P8 report within the stated tolerances
                     (C18 Appendix B is the spec; p_report() is the measured analog).
  3. XOR truth     — (0,0)->0, (1,0)->1, (0,1)->1, (1,1)->0 under the pre-registered
                     read bands.

NOTE: these tests prove the SIM is self-consistent. They are NOT substrate evidence
(falsifier section 4.5); the water is graded against the same P1-P8 table.
"""
from __future__ import annotations

import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.hydro_xor_sim import SimParams, p_report, simulate, truth_table  # noqa: E402


# ------------------------------------------------------------------ 1. determinism

def test_same_inputs_bit_identical_outputs():
    a = simulate(1, 1)
    b = simulate(1, 1)
    assert asdict(a) == asdict(b)


def test_all_cases_bit_identical_across_truth_tables():
    t1 = truth_table()
    t2 = truth_table()
    for case in t1:
        assert asdict(t1[case]) == asdict(t2[case])


def test_seeded_noise_is_deterministic_per_seed():
    r1 = simulate(1, 1, noise_seed=7)
    r2 = simulate(1, 1, noise_seed=7)
    assert asdict(r1) == asdict(r2)


def test_noise_on_differs_from_noise_off_but_stays_in_band():
    quiet = simulate(1, 1)
    noisy = [simulate(1, 1, noise_seed=s) for s in range(20)]
    assert any(asdict(n) != asdict(quiet) for n in noisy), "seeded noise had no effect"
    for n in noisy:
        assert n.bit == "0", f"seed {n.case} broke the bit-0 band: {n.w_at_t_read}"
        assert abs(n.mass_residual_ml) <= 10.0, "noise broke mass balance"


def test_result_invariants_hold_everywhere():
    for case, r in truth_table().items():
        assert r.s_at_t_read >= 0.0
        assert r.w_at_t_read >= 0.0
        assert r.waste_ml >= 0.0
        assert r.max_w_ml <= SimParams().CREST_ML + 1.0  # crest clamp via prime
        assert len(r.w_series) == 151  # sampled every 1.0 s over [0, 150]
        if r.primed:
            assert r.min_crossing_ml is not None and r.min_crossing_ml >= SimParams().CREST_ML
            assert r.prime_time_s is not None and 0.0 < r.prime_time_s <= 90.0
        else:
            assert r.min_crossing_ml is None and r.prime_time_s is None


# ------------------------------------------------- 2. P-statement self-consistency

def test_p_report_all_hold():
    rep = p_report()
    assert rep["all_hold"] is True, {k: v["hold"] for k, v in rep.items() if k.startswith("P")}
    for key in ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"):
        assert rep[key]["hold"] is True, f"{key} failed: {rep[key]}"


def test_p1_unit_transfer_within_tolerance():
    rep = p_report()
    for case, gain in rep["P1"]["measured"].items():
        assert abs(gain - 100.0) <= 20.0, f"{case}: W gained {gain} mL"


def test_p5_margin_between_envelope_and_threshold():
    m = p_report()["P5"]["measured"]
    assert m["max_single_input_ml"] <= 130.0
    assert m["min_double_crossing_ml"] >= 140.0
    assert m["min_double_crossing_ml"] - m["max_single_input_ml"] >= 10.0


def test_p6_conservation_exact_in_noiseless_sim():
    m = p_report()["P6"]["measured"]
    assert m["s_monotonic_decreasing"] is True
    assert m["backflow_occurred"] is False
    assert m["max_abs_mass_residual_ml"] <= 1e-6  # float noise only, far inside 10 mL


def test_p8_drain_rate_ge_3_ml_s():
    m = p_report()["P8"]["measured"]["drain_rate_ml_s"]
    assert m is not None and m >= 3.0


def test_p7_skew_bits_match_skew_zero():
    tt = truth_table()
    for case in ((1, 0), (0, 1), (1, 1)):
        for skew in (5.0, -5.0):
            assert simulate(*case, skew_s=skew).bit == tt[case].bit


# ------------------------------------------------------------- 3. XOR truth table

def test_xor_truth_table_read_bands():
    tt = truth_table()
    assert tt[(0, 0)].bit == "0"
    assert tt[(1, 0)].bit == "1"
    assert tt[(0, 1)].bit == "1"
    assert tt[(1, 1)].bit == "0"


def test_single_inputs_never_prime():
    tt = truth_table()
    assert tt[(1, 0)].primed is False
    assert tt[(0, 1)].primed is False
    assert tt[(1, 1)].primed is True  # "or both valves siphon"
    assert tt[(0, 0)].primed is False


def test_double_input_primes_within_90s_and_dumps():
    r = truth_table()[(1, 1)]
    assert r.prime_time_s is not None and r.prime_time_s <= 90.0
    assert r.w_at_t_read <= 30.0
    assert r.waste_ml >= 100.0  # the marks actually went out the siphon


def test_custom_params_still_xor():
    p = SimParams(SIPHON_RATE_ML_S=18.0, INTAKE_BREAK_ML=4.0)
    tt = truth_table(p)
    assert [tt[c].bit for c in ((0, 0), (0, 1), (1, 0), (1, 1))] == ["0", "1", "1", "0"]
    assert p_report(p)["all_hold"] is True
