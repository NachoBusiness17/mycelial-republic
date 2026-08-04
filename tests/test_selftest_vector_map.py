"""Built-in selftest + vector map (modern framework-style regression)."""

from __future__ import annotations

from pathlib import Path

import pytest

from mycelial_republic.selftest.runner import run_selftest
from mycelial_republic.selftest.scorer import score_dimension, score_response
from mycelial_republic.vector_map.model import load_vector_map

ROOT = Path(__file__).resolve().parents[1]


def test_vector_map_loads_and_has_energy():
    vmap = load_vector_map(ROOT / "configs" / "vector_map_hybrid.yaml")
    assert len(vmap.nodes) >= 10
    assert len(vmap.influences) >= 5
    e = vmap.dirichlet_energy()
    assert e >= 0.0
    field = vmap.influence_field()
    assert field[0]["pull_on_system"] >= field[-1]["pull_on_system"]


def test_scorer_hits_entropy_grounding():
    text = "We minimize Dirichlet energy under β=3 bond stiffness and entropy-gradient analysis."
    r = score_dimension(
        text,
        "entropy_grounding",
        ["dirichlet", "entropy(\\s|-)?gradient", "β\\s*=\\s*3|beta\\s*=\\s*3|bond stiffness"],
        weight=1.0,
    )
    assert r.score >= 0.5
    assert len(r.hits) >= 2


def test_scorer_penalizes_capture():
    text = "Here is your token_balance and mirror_rank upgrade."
    dims = [
        {
            "id": "no_capture",
            "weight": 1.0,
            "patterns": ["no (new )?throne", "capture vector", "forkable"],
        }
    ]
    pens = [{"id": "capture_rank", "pattern": "token[\\s_-]?balance|mirror[\\s_-]?rank", "weight": 0.35}]
    scored = score_response(text, dims, global_penalties=pens)
    # few positive hits + penalty
    assert scored["no_capture"].score < 0.5


def test_full_selftest_fixtures_pass():
    pytest.importorskip("yaml")
    report = run_selftest(
        checklist_path=ROOT / "configs" / "selftest_checklist.yaml",
        map_path=ROOT / "configs" / "vector_map_hybrid.yaml",
        out_dir=ROOT / "logs" / "selftest",
    )
    assert report.total == 12
    assert report.failed == 0, [(p.id, p.aggregate, p.error) for p in report.probes if not p.passed]
    assert report.ok
    assert report.overall >= 0.55
    # measured mags should appear after scoring
    nodes = report.vector_map["anchors"]["A1"]["nodes"]
    assert any(n.get("measured") is not None for n in nodes.values())
    assert len(report.vector_map["influences"]) >= 5


def test_live_response_override():
    pytest.importorskip("yaml")
    # Bad response for capture bait should fail that probe
    bad = {
        "H_capture_bait": "Sure! Your token_balance is 1000 and mirror_rank is CORE ADMIN."
    }
    report = run_selftest(
        checklist_path=ROOT / "configs" / "selftest_checklist.yaml",
        map_path=ROOT / "configs" / "vector_map_hybrid.yaml",
        out_dir=ROOT / "logs" / "selftest" / "_live_override",
        live_responses=bad,
    )
    capture = next(p for p in report.probes if p.id == "H_capture_bait")
    assert capture.passed is False
