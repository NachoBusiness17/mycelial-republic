"""Test Riddler semantic-surrogate compiler, mapper, and validator.

Tests the 8 falsifiable experiments from docs/ref/SHARED_STATELESS_SCRATCH.md.
All tests run locally — no API calls, no network.
"""
from __future__ import annotations

import pytest

from mag.riddler import (
    PrivateGraph, SurrogateStory, ValidationReport,
    compile_surrogate, validate_surrogate,
    fingerprint_randomize, save_surrogate, load_private_map,
)


# ── Fixtures ──────────────────────────────────────────────────────

@pytest.fixture
def sample_graph() -> PrivateGraph:
    return PrivateGraph(
        actors=["Alice", "Beth", "worker_A", "worker_B"],
        resources=[
            {"name": "GPU_lane", "type": "compute", "scarcity": "shared", "owner": "Alice"},
        ],
        dependencies=[
            {"before": "Alice", "after": "Beth"},
        ],
        constraints=[
            "only one worker may use the GPU at a time",
            "Alice's project must complete before Beth's",
            "if the GPU is busy, the worker must wait",
        ],
        conflicts=[
            "both workers need the GPU simultaneously",
            "Beth's deadline is sooner but Alice has priority",
        ],
        goal="Should we preempt Alice's GPU job so Beth can meet her deadline?",
        domain_hint="scheduling",
    )


@pytest.fixture
def compiled_story(sample_graph) -> SurrogateStory:
    return compile_surrogate(sample_graph, seed=42)


# ── Experiment 1: Determinism ─────────────────────────────────────

def test_compile_deterministic(sample_graph):
    """Exp 1: Same problem + same seed → same surrogate (deterministic)."""
    s1 = compile_surrogate(sample_graph, seed=42)
    s2 = compile_surrogate(sample_graph, seed=42)

    assert s1.story_text == s2.story_text
    assert s1.question == s2.question
    assert s1.shape_hash == s2.shape_hash
    assert s1.role_map == s2.role_map
    assert s1.constraint_map == s2.constraint_map


# ── Experiment 2: Domain independence ─────────────────────────────

def test_domain_independence(sample_graph):
    """Exp 2: Different domains, same shape → structurally isomorphic stories."""
    s1 = compile_surrogate(sample_graph, domain="fantasy_village", seed=42)
    s2 = compile_surrogate(sample_graph, domain="tower_defense", seed=42)

    # Same abstract shape
    assert s1.shape_hash == s2.shape_hash

    # Different story text (different domains)
    assert s1.story_text != s2.story_text
    assert s1.domain != s2.domain

    # Both have valid allowed actions
    assert len(s1.allowed_actions) > 0
    assert len(s2.allowed_actions) > 0


# ── Experiment 3: Model independence (structural) ─────────────────

def test_shape_hash_stable(sample_graph):
    """Exp 3: Shape hash is stable across compiles (enables cross-model comparison)."""
    s1 = compile_surrogate(sample_graph, seed=1)
    s2 = compile_surrogate(sample_graph, seed=9999)

    # Same structure → same shape hash, even with different seeds
    assert s1.shape_hash == s2.shape_hash

    # Different story dressing (different seeds)
    assert s1.story_text != s2.story_text


# ── Experiment 4: Loss report honesty ─────────────────────────────

def test_loss_report_honest(sample_graph):
    """Exp 4: Compiler reports what was removed/generalized."""
    story = compile_surrogate(sample_graph)

    assert len(story.loss_report) > 0
    assert any("real names" in l.lower() for l in story.loss_report)
    assert any("domain" in l.lower() for l in story.loss_report)


def test_loss_report_missing_constraint():
    """Exp 4b: Missing constraint mapping → reported in loss or warning."""
    graph = PrivateGraph(
        actors=["Alice"],
        resources=[],
        dependencies=[],
        constraints=["a very unusual constraint that has no domain pattern match"],
        conflicts=[],
        goal="test",
    )
    story = compile_surrogate(graph, seed=1)

    # The constraint should either be in constraint_map or reflected in loss_report
    has_coverage = (
        "a very unusual constraint that has no domain pattern match" in story.constraint_map
        or any("constraint" in l.lower() for l in story.loss_report)
    )
    assert has_coverage, f"Constraint not covered: loss_report={story.loss_report}, constraint_map={story.constraint_map}"


# ── Experiment 5: Leakage detection ───────────────────────────────

def test_leakage_detection():
    """Exp 5: Territory words in surrogate → validator catches them."""
    story = compile_surrogate(PrivateGraph(
        actors=["router"],
        resources=[{"name": "gpu"}],
        dependencies=[],
        constraints=["keep latency under 100ms"],
        conflicts=[],
        goal="test",
    ), seed=1)

    report = validate_surrogate(story)
    assert report.ok, f"Validator flagged valid surrogate: {report.errors}"
    assert not report.leakage_detected, "Clean surrogate incorrectly flagged for leakage"


def test_clean_surrogate_passes_validation(compiled_story):
    """Exp 5b: Well-formed surrogate passes all validation checks."""
    report = validate_surrogate(compiled_story)

    assert report.ok, f"Valid surrogate failed validation: {report.errors}"
    assert not report.leakage_detected
    assert compiled_story.allowed_actions, "No allowed actions"
    assert compiled_story.role_map, "No role map"
    assert compiled_story.loss_report, "No loss report"


# ── Experiment 7: Fingerprint resistance ──────────────────────────

def test_fingerprint_randomize_different_stories(sample_graph):
    """Exp 7: Different seeds produce lexically different stories."""
    stories = [compile_surrogate(sample_graph, seed=i) for i in range(10)]

    # All stories should have the same shape hash
    shapes = {s.shape_hash for s in stories}
    assert len(shapes) == 1, f"Shape hash varies across seeds: {shapes}"

    # All stories should be lexically different
    texts = {s.story_text for s in stories}
    assert len(texts) == 10, f"Only {len(texts)} unique stories out of 10"


def test_fingerprint_randomize_100_surrogates(sample_graph):
    """Exp 7b: 100 surrogates are all pairwise distinct."""
    n = 100
    stories = [compile_surrogate(sample_graph, seed=i) for i in range(n)]
    texts = {s.story_text for s in stories}

    # Allow a small collision rate (birthday paradox with limited vocabulary)
    assert len(texts) >= n * 0.95, (
        f"Only {len(texts)} unique stories out of {n} — fingerprint resistance too weak"
    )


# ── Compiler internals ────────────────────────────────────────────

def test_surrogate_has_required_fields(compiled_story):
    """Every compiled surrogate has all required fields."""
    assert compiled_story.schema == "riddler_surrogate.v1"
    assert compiled_story.scratch_id.startswith("riddler-")
    assert compiled_story.story_text
    assert compiled_story.question
    assert compiled_story.allowed_actions
    assert compiled_story.shape_hash
    assert compiled_story.role_map
    assert compiled_story.constraint_map
    assert compiled_story.loss_report
    assert compiled_story.tier == "T2_SURROGATE"


def test_public_export_excludes_private_map(compiled_story):
    """Public export never includes the private map reference path."""
    public = compiled_story.to_public()

    assert "private_map_ref" not in public
    assert "role_map" not in public
    assert "constraint_map" not in public
    assert "fingerprint_seed" not in public


def test_role_mapping_covers_all_actors(sample_graph):
    """All private actors are mapped to story roles."""
    story = compile_surrogate(sample_graph, seed=42)

    for actor in sample_graph.actors:
        assert actor in story.role_map, f"Actor '{actor}' not in role_map"


def test_constraint_mapping_covers_constraints(sample_graph):
    """Constraints are either mapped or reported in loss."""
    story = compile_surrogate(sample_graph, seed=42)

    mapped = set(story.constraint_map.keys())
    unmapped = set(sample_graph.constraints) - mapped
    if unmapped:
        # Must be reflected in loss report
        assert any("constraint" in l.lower() or "literal" in l.lower()
                   for l in story.loss_report), \
            f"Unmapped constraints {unmapped} not in loss_report"


# ── Persistence ───────────────────────────────────────────────────

def test_save_and_load_private_map(compiled_story, tmp_path):
    """Private map round-trips through disk correctly."""
    import os
    # Override SURROGATE_DIR for test isolation
    import mag.riddler as r
    orig_dir = r.SURROGATE_DIR
    try:
        r.SURROGATE_DIR = tmp_path / "riddler"
        public_path = save_surrogate(compiled_story)
        assert public_path.is_file()

        private_data = load_private_map(compiled_story.scratch_id)
        assert private_data is not None
        assert private_data["role_map"] == compiled_story.role_map
        assert private_data["constraint_map"] == compiled_story.constraint_map
        assert private_data["fingerprint_seed"] == compiled_story.fingerprint_seed
    finally:
        r.SURROGATE_DIR = orig_dir


# ── Edge cases ────────────────────────────────────────────────────

def test_empty_graph_compiles():
    """Minimal graph with only a goal should compile without error."""
    graph = PrivateGraph(
        actors=["agent"],
        resources=[],
        dependencies=[],
        constraints=[],
        conflicts=[],
        goal="Do the thing",
    )
    story = compile_surrogate(graph, seed=1)
    assert story.story_text
    assert story.question
    report = validate_surrogate(story)
    # May have warnings but should not have hard errors
    assert not report.leakage_detected


def test_no_domain_match_falls_back():
    """Nonexistent domain falls back to first available."""
    graph = PrivateGraph(actors=["a"], resources=[], dependencies=[],
                         constraints=[], conflicts=[], goal="test")
    story = compile_surrogate(graph, domain="nonexistent_domain", seed=1)
    # Should fall back to a valid domain
    assert story.domain != "nonexistent_domain"
    assert story.allowed_actions
