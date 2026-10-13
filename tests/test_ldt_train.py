"""ldt_train tests — Z13 smoke laws (Mickey17 W3 lane, 2026-09-29).

1. Smoke train: 1 epoch on ~100 generated samples, tiny net — predict
   shape (n, 5), proba rows sum to 1, weights round-trip through the npz.
2. Abstain algebra: threshold 0.0 answers everyone, so soundness must
   equal plain accuracy and coverage must be 1.0 (the evaluate() contract
   the Z13 receipt reports against).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.legality_dataset import generate  # noqa: E402
from tools.ldt_train import (Featurizer, LABELS, evaluate, forward,  # noqa: E402
                             load_npz, rows_xy, save_npz, train_model)


def _tiny_rows():
    train, val = generate(110, seed=5, val_frac=0.1)
    return train[:100], val[:12]


def test_smoke_train_predict_shape(tmp_path: Path) -> None:
    train_rows, val_rows = _tiny_rows()
    fe = Featurizer().fit(train_rows)
    Xtr, ytr = rows_xy(train_rows, fe)
    Xva, yva = rows_xy(val_rows, fe)

    params, losses = train_model(Xtr, ytr, hidden=[16, 8], epochs=1,
                                 lr=1e-3, batch=32, seed=13)
    assert len(losses) == 1 and np.isfinite(losses[0])
    assert params["W0"].shape == (fe.dim, 16)
    assert params["W2"].shape == (8, len(LABELS))

    probs, _ = forward(params, Xva)
    assert probs.shape == (len(val_rows), len(LABELS))
    np.testing.assert_allclose(probs.sum(axis=1), 1.0, atol=1e-5)
    assert set(np.unique(yva)) <= set(range(len(LABELS)))

    metrics = evaluate(params, Xva, yva, threshold=0.7)
    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert 0.0 <= metrics["coverage"] <= 1.0
    assert set(metrics["per_class"]) == set(LABELS)

    # npz round-trip: reload must reproduce identical probabilities
    out = tmp_path / "legality_smoke.npz"
    save_npz(out, params, fe, {"schema": "ldt_v0.npz", "seed": 13})
    params2, fe2, config = load_npz(out)
    assert fe2.dim == fe.dim and config["schema"] == "ldt_v0.npz"
    probs2, _ = forward(params2, fe2.transform(val_rows))
    np.testing.assert_allclose(probs2, probs, atol=1e-6)


def test_threshold_zero_soundness_equals_accuracy() -> None:
    train_rows, val_rows = _tiny_rows()
    fe = Featurizer().fit(train_rows)
    Xtr, ytr = rows_xy(train_rows, fe)
    Xva, yva = rows_xy(val_rows, fe)
    params, _ = train_model(Xtr, ytr, hidden=[16], epochs=2,
                            lr=1e-3, batch=32, seed=7)
    m = evaluate(params, Xva, yva, threshold=0.0)
    assert m["coverage"] == 1.0
    assert m["answered"] == len(yva)
    assert m["answered_correct"] + m["answered_wrong"] == len(yva)
    np.testing.assert_allclose(m["soundness"], m["accuracy"])
