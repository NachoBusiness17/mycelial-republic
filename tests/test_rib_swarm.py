"""rib_swarm tests (GENOME-1 lane, 2026-10-01).

Spec: docs/ref/RIB_SWARM_SPEC.md section 7. Covers the law-row parser (lenient
parse + strict grade + round-trip), the rib ledger, the law-rows-only round-2
contract builder (run end-to-end in mock), cross-unit law convergence ranking,
the genetic operators (crossover clause provenance, mutate single-clause law,
bounds), the fitness formula (REAL dominance, cost floor), the offline genetic
cycle (one cycle must improve the population), and the no-em-dash contract law.
No real API fires anywhere in this file.
"""
from __future__ import annotations

import json
import random

import pytest

from tools import code_swarm as cs
from tools import model_garden as mg
from tools import rib_swarm as rs

GOOD = ("L1: spend cap unenforced\n"
        "CLAIM: spend accumulates without cap enforcement across the run\n"
        "STEAL: enforce the cap before every dispatch\n"
        "FALSIFIER: a run that stops itself at the cap\n"
        'SOURCE: tools/ocean_v2_pilot.py "COST_CAP=0.25"\n'
        "LEVERAGE: high")


@pytest.fixture
def estate(tmp_path, monkeypatch):
    """Synthetic mini-estate: every Path the module writes through is patched
    (the SWARM-1 lesson: patch every Path constant, not just GARDEN)."""
    monkeypatch.setattr(rs, "ROOT", tmp_path)
    monkeypatch.setattr(rs, "GARDEN", tmp_path / "watch" / "inbox" / "model_garden")
    monkeypatch.setattr(cs, "ROOT", tmp_path)
    monkeypatch.setattr(mg, "ROOT", tmp_path)
    monkeypatch.setattr(cs, "GARDEN", tmp_path / "watch" / "inbox" / "model_garden")
    monkeypatch.setattr(mg, "OUT_DIR", tmp_path / "watch" / "inbox" / "model_garden")
    monkeypatch.setattr(mg, "USAGE", tmp_path / "memory" / "runs" / "model_garden" / "usage.jsonl")
    (tmp_path / "mag").mkdir()
    for name in ("mag/lane_a.py", "mag/lane_b.py"):
        (tmp_path / name).write_text("import os\n" * 40, encoding="utf-8")
    return tmp_path


# --- law-row parser (spec section 1) ----------------------------------------

def test_parser_happy_path_grades_pass():
    rows = rs.parse_law_rows(GOOD)
    assert len(rows) == 1
    r = rows[0]
    assert r["law_id"] == "L1" and r["title"] == "spend cap unenforced"
    assert r["CLAIM"].startswith("spend accumulates")
    assert r["passes"] is True and r["shape_violations"] == 0
    assert all(r["checks"].values())


def test_parser_blank_lines_and_prose_tolerated():
    text = GOOD + "\n\nsome stray prose line\n\n" + GOOD.replace("L1:", "L2:")
    rows = rs.parse_law_rows(text)
    assert [r["law_id"] for r in rows] == ["L1", "L2"]
    assert rows[0]["shape_violations"] == 1  # graded, never fatal
    assert rows[1]["passes"] is True


def test_parser_missing_fields_fail_grade_not_parse():
    bad = GOOD.replace("FALSIFIER: a run that stops itself at the cap\n", "") \
              .replace("LEVERAGE: high", "LEVERAGE: critical")
    r = rs.parse_law_rows(bad)[0]
    assert r["checks"]["falsifier"] is False and r["checks"]["leverage"] is False
    assert r["passes"] is False  # an unfalsifiable law is an opinion


def test_parser_em_dash_fails_grade():
    r = rs.parse_law_rows(GOOD.replace("spend cap", "spend\u2014cap"))[0]
    assert r["checks"]["no_em_dash"] is False and r["passes"] is False


def test_parser_long_title_graded_not_gating():
    r = rs.parse_law_rows(GOOD.replace(
        "spend cap unenforced",
        "a very long rambling title that runs well past twelve words in total"))[0]
    assert r["checks"]["title_short"] is False and r["passes"] is True


def test_render_roundtrip_identity():
    rows = rs.parse_law_rows(GOOD + "\n\n" + GOOD.replace("L1:", "L9:"))
    back = rs.parse_law_rows(rs.render_law_rows(rows))
    assert [(r["law_id"], r["CLAIM"], r["LEVERAGE"]) for r in back] == \
           [(r["law_id"], r["CLAIM"], r["LEVERAGE"]) for r in rows]


def test_render_accepts_banked_ledger_rows():
    banked = [{"law_id": "L1", "title": "t", "claim": "c text here", "steal": "s",
               "falsifier": "f", "source": "tools/x.py", "leverage": "low"}]
    out = rs.render_law_rows(banked)
    assert "CLAIM: c text here" in out and "LEVERAGE: low" in out


# --- rib ledger (spec section 2) ---------------------------------------------

def test_bank_ledger_appends_across_rounds(estate):
    root = estate / "watch" / "inbox" / "model_garden" / "r0"
    rows1 = [{"schema": "rib_swarm.law_row.v1", "run": "r0", "round": 1, "unit": "U1",
              "mock": True, "law_id": "L1", "title": "t", "claim": "c", "steal": "s",
              "falsifier": "f", "source": "p", "leverage": "high", "passes": True,
              "reply_sha256": "x"}]
    rs.bank_ledger(root, rows1)
    rs.bank_ledger(root, [dict(rows1[0], law_id="L2", round=2)])
    lines = (root / "rib_ledger.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    first = json.loads(lines[0])
    assert first["mock"] is True and first["round"] == 1  # mock flag survives


# --- rib round: law rows only (spec section 3) -------------------------------

def test_rib_round_mock_end_to_end_law_rows_only(estate):
    out = rs.rib_round("ribT", ["mag/lane_a.py", "mag/lane_b.py"],
                       ["deepseek", "glm-flash"], mock=True,
                       concurrency=1, cap=0.5, seed=7)
    assert out["mock"] is True and out["ledger_rows"] > 0
    assert out["converged_laws"] > 0  # shaping lens converges across units
    led = [json.loads(l) for l in (estate / "watch" / "inbox" / "model_garden"
                                   / "ribT" / "rib_ledger.jsonl").read_text(encoding="utf-8").splitlines()]
    assert {r["round"] for r in led} == {1, 2}
    # round-2 contracts are built from ledger rows only: sibling CLAIM lines in,
    # raw carrier prose (headers, channel marks) physically absent
    for unit in ("U1", "U2"):
        meta = json.loads((estate / "watch" / "inbox" / "model_garden" / "ribT"
                           / "asks" / f"ribT-{unit}-r2-deepseek" / "ask.json")
                          .read_text(encoding="utf-8"))
        assert "SIBLING ROUND-1 LAWS" in meta["contract"]
        assert "CLAIM: spend accumulates without cap enforcement" in meta["contract"]
        assert "MOCK" not in meta["contract"] and "channel:" not in meta["contract"]
        for line in meta["contract"].splitlines():
            if line[:1] == "L" or ":" in line[:11]:
                assert rs.LAW_RE.match(line.strip()) or rs.FIELD_RE.match(line.strip()) or \
                    not line.strip().startswith(("L", "CLAIM", "STEAL", "FALSIFIER", "SOURCE", "LEVERAGE"))


def test_rib_round_real_mode_never_fires_in_test(estate):
    # real mode with a bogus key env must fail named, not silently pass
    staged = [{"unit": "U1", "target": "mag/lane_a.py", "family": "deepseek", "kind": "law",
               "n_lines": 0, "lens": "cost-leak",
               **rs.stage_ask("ribR", "ribR-U1-r1-deepseek", "deepseek", "contract")}]
    res = rs.fire("ribR", staged, mock=False, concurrency=1, cap=0.5, seed=7)
    assert res[0]["ok"] is False and "error" in res[0]  # no key in tmp estate


# --- convergence ranking (spec section 3) -------------------------------------

def _lrow(unit, law, title, claim, lev="medium"):
    return {"unit": unit, "law_id": law, "title": title, "claim": claim, "leverage": lev}


def test_converge_laws_cross_unit_agreement_and_ranking():
    rows = [
        _lrow("U1", "L1", "cap leak", "spend accumulates without cap enforcement", "low"),
        _lrow("U2", "L3", "cap bypass", "spend accumulates without cap guard rails", "medium"),
        _lrow("U3", "L2", "cap missing", "spend accumulates without cap enforcement rails", "low"),
        _lrow("U4", "L1", "noise", "totally unrelated deadbeef words here", "high"),
        _lrow("U4", "L2", "solo", "a single unit observation with unique tokens", "high"),
    ]
    out = rs.converge_laws(rows)
    top = out[0]
    assert top["status"] == "CONVERGED" and top["n_units"] == 3  # U1+U2+U3 cluster
    assert top["leverage"] == "medium"  # cluster takes its best leverage
    assert [c for c in out if c["status"] == "SINGLE" and "solo" in c["laws"][0]["title"]]
    # same-unit rows never cluster with each other
    u4 = [c for c in out if c["units"] == ["U4"]]
    assert all(c["status"] == "SINGLE" for c in u4)


def test_converge_laws_requires_two_shared_tokens():
    rows = [_lrow("U1", "L1", "a", "alpha bravo charlie delta"),
            _lrow("U2", "L1", "b", "alpha bravo echo foxtrot"),   # 2 shared: converges
            _lrow("U3", "L1", "c", "alpha golf hotel india")]     # 1 shared with U1: not
    out = rs.converge_laws(rows)
    conv = [c for c in out if c["status"] == "CONVERGED"]
    assert len(conv) == 1 and sorted(conv[0]["units"]) == ["U1", "U2"]
    singles = [c for c in out if c["status"] == "SINGLE"]
    assert any(c["units"] == ["U3"] for c in singles)


def test_converge_laws_containment_guard_blocks_weak_big_sig_sharing():
    # the live riblive1 bug: 2 shared tokens out of big signatures is domain
    # vocabulary, not agreement; the guard requires half the smaller sig
    rows = [_lrow("U1", "L1", "a", "alpha bravo charlie delta echo foxtrot"),
            _lrow("U2", "L1", "b", "alpha bravo golf hotel india juliet")]
    out = rs.converge_laws(rows)
    assert all(c["status"] == "SINGLE" for c in out)
    # but tight small signatures sharing half their vocab still converge
    tight = [_lrow("U1", "L1", "a", "alpha bravo charlie delta"),
             _lrow("U2", "L1", "b", "alpha bravo echo foxtrot")]
    assert rs.converge_laws(tight)[0]["status"] == "CONVERGED"


# --- genetic operators (spec section 4.4) --------------------------------------

def _g(gid, lens, target, md, probe):
    return {"id": gid, "gen": 0, "origin": "seed", "parents": [], "lens": lens,
            "target": target, "max_defects": md, "anchor_family": "deepseek",
            "probe_family": probe}


def test_crossover_clauses_come_from_parents_only_and_deterministic():
    a = _g("g0-0", "cost-leak", "mag/lane_a.py", 3, "glm-flash")
    b = _g("g0-1", "dead-code", "mag/lane_b.py", 5, "kimi")
    clauses = ("lens", "target", "max_defects", "probe_family")
    for seed in range(20):
        child = rs.crossover(a, b, random.Random(seed), seed)
        assert child["id"] not in (a["id"], b["id"]) and child["parents"] == ["g0-0", "g0-1"]
        for k in clauses:
            assert child[k] in (a[k], b[k])
        assert child["anchor_family"] == "deepseek"
    assert rs.crossover(a, b, random.Random(3), 0) == rs.crossover(a, b, random.Random(3), 0)


def test_mutate_perturbs_exactly_one_clause_with_bounds():
    g = _g("g0-0", "cost-leak", "mag/lane_a.py", 3, "glm-flash")
    clauses = ("lens", "target", "max_defects", "probe_family")
    for seed in range(50):
        m = rs.mutate(g, random.Random(seed), ["mag/lane_a.py", "mag/lane_b.py"],
                      ["deepseek", "glm-flash", "kimi"])
        diff = [k for k in clauses if m[k] != g[k]]
        assert len(diff) == 1, (seed, diff)
        assert m["parents"] == ["g0-0"] and m["origin"].endswith("+mutate")
        assert 2 <= m["max_defects"] <= 5
        if "lens" in diff:
            assert m["lens"] != "cost-leak"
    m2 = rs.mutate(g, random.Random(9), ["mag/lane_a.py"], ["deepseek", "glm-flash"])
    assert m2["target"] == g["target"]  # single-target pool: target not mutable


# --- fitness (spec section 4.3) -------------------------------------------------

def test_measure_fitness_real_dominance_and_formula(estate):
    pop = rs.seed_population(["mag/lane_a.py", "mag/lane_b.py"],
                             ["deepseek", "glm-flash", "kimi"], "deepseek", 8)
    measured = rs.measure("fitT", pop, mock=True, concurrency=1, cap=0.5, seed=7)
    by_lens = {g["lens"]: g for g in measured}
    assert by_lens["cost-leak"]["fitness"] > by_lens["wiring-organs"]["fitness"]
    assert by_lens["cost-leak"]["measured"]["real"] >= \
           by_lens["wiring-organs"]["measured"]["real"]
    for g in measured:  # formula law incl. the $0.01 cost floor (mock cost < floor)
        m = g["measured"]
        expect = (m["real"] + 0.25 * m["colocation"] + 0.05 * m["parse_rate"]) / 0.01
        assert abs(g["fitness"] - round(expect, 4)) < 0.01
        assert m["cost_usd"] <= 0.014  # synthetic: 2 asks, cheapest families


def test_zero_yield_genome_orders_by_parse_term(estate):
    # both zero-REAL genomes tie on yield; the parse term keeps fitness nonzero
    pop = [_g("z1", "wiring-organs", "mag/lane_a.py", 3, "glm-flash"),
           _g("z2", "error-swallow", "mag/lane_b.py", 2, "kimi")]
    measured = rs.measure("zT", pop, mock=True, concurrency=1, cap=0.5, seed=7)
    for g in measured:
        assert g["measured"]["real"] == 0 and g["fitness"] > 0  # parse term alive
        assert g["measured"]["parse_rate"] == 1.0


# --- the genetic cycle (spec section 4.5) ----------------------------------------

def test_mock_genetic_cycle_improves_population(estate):
    out = rs.genetic("genT", ["mag/lane_a.py", "mag/lane_b.py"],
                     ["deepseek", "glm-flash", "kimi"], "deepseek",
                     pop_size=8, gens=2, cap=0.5, seed=7, mock=True,
                     concurrency=1, stagnation=1)
    assert out["mock"] is True and out["exit"] in ("GENERATIONS", "STAGNANT")
    hist = out["generations"]
    assert len(hist) >= 2
    assert hist[1]["best"] >= hist[0]["best"]  # best never regresses (elites)
    assert hist[1]["mean"] > hist[0]["mean"]   # one cycle improved the population
    gdir = estate / "watch" / "inbox" / "model_garden" / "genT" / "genetic"
    gens = json.loads((gdir / "generations.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert gens["gen"] == 0
    genome_file = json.loads((gdir / "genomes_gen0.json").read_text(encoding="utf-8"))
    assert len(genome_file) == 8  # full population banked per generation


def test_mock_genetic_deterministic(estate):
    common = dict(targets=["mag/lane_a.py", "mag/lane_b.py"],
                  families=["deepseek", "glm-flash", "kimi"], anchor="deepseek",
                  pop_size=8, gens=2, cap=0.5, seed=11, mock=True,
                  concurrency=1, stagnation=1)
    a = rs.genetic("detA", **common)
    b = rs.genetic("detB", **common)
    assert a["generations"] == b["generations"]  # same seed, same trajectory


# --- no em-dash in any generated contract (spec section 4.2) ----------------------

def test_rendered_contracts_carry_no_em_dash(estate):
    text = (estate / "mag" / "lane_a.py").read_text(encoding="utf-8")
    g = _g("g0-0", "cost-leak", "mag/lane_a.py", 3, "glm-flash")
    assert rs.EM_DASH not in rs.render_genome_contract(g, text)
    assert rs.EM_DASH not in rs.ROUND1 and rs.EM_DASH not in rs.ROUND2
    assert rs.EM_DASH not in rs.GEN_CONTRACT
    # and the mock replies grade clean on the em-dash check
    reply = rs.mock_reply("defect", "cost-leak", "mag/lane_a.py", 40, random.Random(1))
    assert rs.EM_DASH not in reply
    graded = cs.parse_reply(reply, "mag/lane_a.py", 40)
    assert graded["checks"]["no_em_dash"] is True
