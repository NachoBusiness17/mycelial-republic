"""GPS embedding-lane tests (2026-10-06 order: EmbeddingGemma 2 trial).

Model-free invariants (wilson/mcnemar/knn_vote/split) always run. The
model-dependent tests (determinism round-trip, sidecar idempotence)
skip cleanly when the pull is absent so the fleet suite stays green on
seats without models/embeddinggemma-2-onnx.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.gps_mcp.gps_embed import (  # noqa: E402
    DEFAULT_MODEL_DIR,
    FP32_ONNX,
    build_sidecar,
    load_sidecar_vectors,
)
from tools.gps_mcp.gps_embed_stats import (  # noqa: E402
    knn_vote,
    mcnemar_exact_p,
    stratified_holdout,
    wilson_ci,
)

MODEL_PRESENT = (DEFAULT_MODEL_DIR / FP32_ONNX).exists() and (
    DEFAULT_MODEL_DIR / "onnx" / "model.onnx_data"
).exists()
needs_model = pytest.mark.skipif(
    not MODEL_PRESENT, reason="EmbeddingGemma 2 ONNX pull absent (models/ is gitignored)"
)


# -- model-free invariants ---------------------------------------------------


def test_wilson_ci_bounds_and_point():
    lo, hi = wilson_ci(210, 210)
    assert lo == pytest.approx(0.9817, abs=0.01) and hi == 1.0
    lo, hi = wilson_ci(0, 10)
    assert lo == 0.0 and hi < 0.35


def test_mcnemar_exact_p_symmetric_and_degenerate():
    # 2 discordant pairs split 2-0: two-sided exact p = 0.5.
    assert mcnemar_exact_p(2, 0) == pytest.approx(0.5)
    # Perfectly balanced discordants: p = 1.0.
    assert mcnemar_exact_p(3, 3) == pytest.approx(1.0)
    # No discordants: nothing to test.
    assert mcnemar_exact_p(0, 0) == 1.0


def _norm(v: np.ndarray) -> np.ndarray:
    return v / np.linalg.norm(v)


def test_knn_vote_majority_and_tie_nearest():
    # Three candidate shapes; two share winner M1, self-match says M2.
    cand = {
        "self": _norm(np.array([1.0, 0.0, 0.0], dtype=np.float32)),
        "near": _norm(np.array([0.95, 0.05, 0.0], dtype=np.float32)),
        "far": _norm(np.array([0.0, 1.0, 0.0], dtype=np.float32)),
    }
    labels = {"self": "M2", "near": "M1", "far": "M1"}
    query = cand["self"]
    pick, detail = knn_vote(query, cand, labels, k=3)
    # Majority (2x M1) outranks the exact self-match: the filed rule.
    assert pick == "M1"
    assert detail[0]["cosine"] == pytest.approx(1.0)
    # 1-1-1 tie falls to the nearest neighbor's label.
    tie_labels = {"self": "M2", "near": "M1", "far": "M3"}
    pick, _ = knn_vote(query, cand, tie_labels, k=3)
    assert pick == "M2"
    # Empty candidate space routes nowhere.
    assert knn_vote(query, {}, {}, k=3)[0] is None


def test_stratified_holdout_shape_integrity_and_determinism():
    rows = []
    for i in range(40):
        shape = "alpha" if i % 4 == 0 else ("beta" if i % 4 == 1 else "gamma")
        rows.append({"rowid_key": i, "task_shape": shape, "verdict": i % 2,
                     "model_id": "m", "ts": "t"})
    train1, held1 = stratified_holdout(rows, 0.3, seed=20261006)
    train2, held2 = stratified_holdout(rows, 0.3, seed=20261006)
    assert [r["rowid_key"] for r in held1] == [r["rowid_key"] for r in held2]
    assert len(train1) + len(held1) == 40
    held_ids = {r["rowid_key"] for r in held1}
    train_ids = {r["rowid_key"] for r in train1}
    assert not held_ids & train_ids
    # Every shape keeps at least one train row (a train-empty shape
    # would decide the A/B race by construction, not evidence).
    for shape in ("alpha", "beta", "gamma"):
        assert any(r["task_shape"] == shape for r in train1)
    # ~30% per shape (round), n>=2 shapes hold some rows out.
    assert 0 < sum(1 for r in held1 if r["task_shape"] == "alpha") <= 3


# -- model-dependent (skip without the pull) ----------------------------------


@needs_model
def test_embedding_round_trip_determinism():
    """Same input twice = same vector, in-session AND across a fresh
    session load (the order's determinism falsifier)."""
    from tools.gps_mcp.gps_embed import EmbeddingGemma2ONNX

    emb = EmbeddingGemma2ONNX()
    v1 = emb.embed(["route determinism probe"])
    v2 = emb.embed(["route determinism probe"])
    assert v1.shape == (1, 768)
    assert np.array_equal(v1, v2), "same-session re-embed must be bit-identical"
    fresh = EmbeddingGemma2ONNX()
    v3 = fresh.embed(["route determinism probe"])
    assert np.array_equal(v1, v3), "fresh-session re-embed must be bit-identical"
    # Output contract: L2-normalized rows.
    assert np.allclose(np.linalg.norm(v1, axis=1), 1.0, atol=1e-5)


@needs_model
def test_padding_mask_invariance():
    """Batching must not move a vector: a short text embedded alone vs
    padded next to a longer text must agree (attention_mask correctness
    for the batched sidecar build)."""
    from tools.gps_mcp.gps_embed import EmbeddingGemma2ONNX

    emb = EmbeddingGemma2ONNX()
    short = "grading"
    alone = emb.embed([short])[0]
    batched = emb.embed([short, "a considerably longer task shape description "
                                "that forces padding on the shorter row"])[0]
    assert np.allclose(alone, batched, atol=1e-4)


@needs_model
def test_sidecar_build_idempotence(tmp_path):
    """Building the sidecar twice must not grow it and must not move a
    stored vector (ledger-embed idempotence)."""
    sidecar = tmp_path / "vectors.db3"
    first = build_sidecar(sidecar_db=sidecar)
    assert first["shapes_embedded"] == 10
    second = build_sidecar(sidecar_db=sidecar)
    assert second["groups_written"] == first["groups_written"]
    vecs1 = load_sidecar_vectors(sidecar)
    # Rebuild and re-read: same keys, bit-identical vectors.
    build_sidecar(sidecar_db=sidecar)
    vecs2 = load_sidecar_vectors(sidecar)
    assert set(vecs1) == set(vecs2) and len(vecs1) == 10
    for shape, vec in vecs1.items():
        assert np.array_equal(vec, vecs2[shape]), f"vector drifted for {shape}"
    con = sqlite3.connect(sidecar)
    try:
        n_vectors = con.execute("SELECT COUNT(*) FROM vectors").fetchone()[0]
        n_shapes = con.execute("SELECT COUNT(*) FROM shape_vectors").fetchone()[0]
    finally:
        con.close()
    assert n_shapes == 10 and n_vectors == first["groups_written"]
