"""tests for tools/gps_router_v0.py (lane ml3-router-classifier, ml-moonshot-20261007).

Runs the trainer end to end on a synthetic corpus built in tmp_path, so no
test touches the real ml1 corpus or the live gps_ledger.db3. The synthetic
frames carry the same columns the corpus README documents.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.gps_router_v0 import (  # noqa: E402
    FEATURE_COLS,
    _usage_shape,
    load_frame,
    make_models,
    percolator_baseline,
    route_table,
)


def _write_parquet(df: pd.DataFrame, path: Path) -> None:
    df.to_parquet(path, index=False)


@pytest.fixture()
def tiny_corpus(tmp_path: Path) -> Path:
    ts = pd.to_datetime(
        ["2026-10-01T00:00:00Z", "2026-10-01T01:00:00Z", "2026-10-01T02:00:00Z",
         "2026-10-02T00:00:00Z", "2026-10-02T01:00:00Z", "2026-10-03T00:00:00Z",
         "2026-10-03T01:00:00Z", "2026-10-03T02:00:00Z"])
    verdicts = pd.DataFrame({
        "ts": ts,
        "model_id": ["a-model"] * 6 + ["b-model"] * 2,
        "task_shape": ["grading"] * 6 + ["grading"] * 2,
        "verdict_label": [1, 1, 1, 1, 0, 1, 0, 0],
        "evidence_hash": "",
        "evidence_resolved": 0,
        "evidence_source": "",
        "evidence_bytes": None,
    })
    _write_parquet(verdicts, tmp_path / "gps_verdicts.parquet")

    capability = pd.DataFrame({
        "model_id": ["a-model", "b-model"],
        "task_shape": ["grading", "grading"],
        "pass_rate": [0.8, 0.0],
        "sample_size": [6, 2],
        "cost_usd_per_call": [0.01, 0.01],
        "last_measured": ["2026-10-03T02:00:00Z"] * 2,
        "updated_at": ["2026-10-03T02:00:00Z"] * 2,
    })
    _write_parquet(capability, tmp_path / "gps_capability.parquet")

    gauntlet = pd.DataFrame({
        "ts": ts[:2],
        "work_id": ["gauntlet:dice:v1", "gauntlet:dice:v2"],
        "family": ["dice", "dice"],
        "provider": ["free", "free"],
        "animal": ["free-seat-1", "free-seat-2"],
        "verdict": ["PASS", "FAIL"],
        "pass_label": [1.0, 0.0],
        "note": ["we built the mechanism", "the huge breaking amazing thing"],
        "onsets_made": [1, 0], "onsets_total": [1, 1], "onsets_frac": [1.0, 0.0],
        "overlap_1": [None, None], "overlap_2": [None, None],
        "overlap_3": [None, None], "corrected": [False, False],
        "superseded": [False, False],
        "expensive_ref": ["", ""], "source_line": [1, 2],
    })
    _write_parquet(gauntlet, tmp_path / "gauntlet.parquet")

    usage = pd.DataFrame({
        "ts": ts,
        "id": ["TAVERN_a", "TAVERN_b", "DUEL1_a", "DUEL1_b",
               "TAVERN_c", "DUEL1_c", "TAVERN_d", "DUEL1_d"],
        "model": ["paid-1"] * 8,
        "turn": [1] * 8,
        "prompt_tokens": [10] * 8, "completion_tokens": [10] * 8,
        "reasoning_tokens": [0] * 8, "total_tokens": [20] * 8,
        "cost_usd": [0.01] * 8,
        "ok": [True, True, True, False, True, False, True, False],
        "ok_label": [1, 1, 1, 0, 1, 0, 1, 0],
        "http_status": [None] * 8, "finish_reason": [None] * 8,
        "transport_error": [None] * 8, "refused": [None] * 8,
        "channel": [None] * 8,
        "error": [None] * 8,
    })
    _write_parquet(usage, tmp_path / "usage.parquet")
    return tmp_path


def test_load_frame_unifies_three_sources(tiny_corpus: Path) -> None:
    df = load_frame(tiny_corpus)
    assert len(df) == 8 + 2 + 8  # 8 verdicts + 2 gauntlet + 8 usage
    assert set(df["source"]) == {"gps_verdicts", "gauntlet", "usage"}
    assert set(FEATURE_COLS).issubset(df.columns)
    assert df["percolator_score"].between(-100, 100).all()


def test_usage_shape_map_is_deterministic() -> None:
    assert _usage_shape("TAVERN_abc") == "tavern-turn"
    assert _usage_shape("dnd0_run") == "dnd-session"
    assert _usage_shape("DUEL1_x") == "duel"
    assert _usage_shape("ZZZ_y") == "other"


def test_percolator_baseline_prior_on_textless_rows(tiny_corpus: Path) -> None:
    df = load_frame(tiny_corpus).sort_values("ts").reset_index(drop=True)
    train_idx = np.arange(0, 12)
    test_idx = np.arange(12, 16)
    pred, score = percolator_baseline(df, train_idx, test_idx)
    # usage rows carry no error text: they must fall back to the training prior
    assert (pred == 1).all()  # prior > 0.5 on this frame
    # the gauntlet theater-note row scores negative, a signal row positive
    gauntlet_scores = df.loc[df["source"] == "gauntlet", "percolator_score"]
    assert (gauntlet_scores.to_numpy() < [0, 100]).any()
    assert (gauntlet_scores.to_numpy() != 0).all()


def test_route_table_gates_thin_evidence(tiny_corpus: Path) -> None:
    df = load_frame(tiny_corpus)
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import OneHotEncoder
    pipe = make_pipeline(
        OneHotEncoder(handle_unknown="ignore"),
        make_models()["logistic_regression"],
    )
    pipe.fit(df[FEATURE_COLS], df["success"])
    out_dir = tiny_corpus / "out"
    out_dir.mkdir()
    table = route_table(df, pipe, out_dir, min_support=5)
    by_shape = {r["task_shape"]: r for r in table}

    # grading: 6 a-model rows + 2 b-model rows -> only a-model clears the gate
    grading = by_shape["grading"]
    assert grading["best_animal"] == "a-model"
    assert grading["ranking"][0]["n_train_rows"] == 6

    # every usage shape totals 4 rows: nothing clears min_support=5
    for shape in ("tavern-turn", "duel"):
        assert by_shape[shape]["best_animal"] is None
        assert "do not route" in by_shape[shape]["fallback_note"]

    # the route table lands as json
    assert json.loads((out_dir / "ml3_route_table.json").read_text(
        encoding="utf-8"))[0]["task_shape"] in by_shape


def test_end_to_end_metrics_beat_chance(tiny_corpus: Path) -> None:
    from tools.gps_router_v0 import evaluate
    df = load_frame(tiny_corpus)
    out: dict = {}
    fitted = evaluate(df, tiny_corpus, out)
    assert "time_75_25" in out["splits"] and "stratified_75_25" in out["splits"]
    for split in out["splits"].values():
        if "error" in split:
            continue
        assert split["gradient_boosting"]["roc_auc"] >= 0.5
        assert split["logistic_regression"]["roc_auc"] >= 0.5
        assert ("baseline_percolator" in split
                and "baseline_ledger_capability" in split)
    assert ("time_75_25", "gradient_boosting") in fitted


def test_models_are_deterministic(tiny_corpus: Path) -> None:
    df = load_frame(tiny_corpus)
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import OneHotEncoder

    def fit_once() -> np.ndarray:
        pipe = make_pipeline(
            OneHotEncoder(handle_unknown="ignore"), make_models()["gradient_boosting"])
        pipe.fit(df[FEATURE_COLS], df["success"])
        return pipe.predict_proba(df[FEATURE_COLS])[:, 1]

    assert np.allclose(fit_once(), fit_once())
