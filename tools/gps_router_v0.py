"""GPS ROUTER v0 (classical) - lane ml3-router-classifier, run ml-moonshot-20261007.

Trains sklearn logistic regression + gradient boosting on the labeled corpus at
memory/corpus/ml/training/ (lane ml1-ledger-corpus) to predict success from
(node, animal, task_shape), following the GPS row contract in
tools/gps_mcp/ledger.py (verdict_log: ts, model_id, task_shape, verdict).

Rows unified from three ml1 tables, each keeping its byte origin:
- gps_verdicts 703 rows: node='ledger', animal=model_id, task_shape=task_shape,
  success=verdict_label, text='' (the ledger rows carry no text).
- gauntlet live pass/fail rows (pass_label notna, 12 rows): node=family,
  animal=model, task_shape=family, success=pass_label, text=note.
- usage rows (ok_label notna, 3038 rows): node=id prefix, animal=model,
  task_shape=derived from the id prefix (documented map below), success=ok_label,
  text=error (sparse: 8 of 3038 rows carry one).

Baselines on the SAME held-out split:
1. percolator_score (the named baseline): mag/percolator.py partition() lexicon
   (SIGNAL_HINTS vs THEATER_HINTS/NOISE_HINTS at mag/percolator.py:125-145,
   _classify at :198-210). Score = n_signal - n_theater - n_noise; predict
   success when score > 0; empty-text rows get the training prior. $0, hand-tuned.
2. ledger_capability (the incumbent production router): capability.pass_rate
   lookup per (model_id, task_shape), global mean as default. Hand-tuned mean,
   $0. Reported as context, the ask's named baseline is #1.

Models: LogisticRegression and GradientBoostingClassifier on one-hot
(node, animal, task_shape, source) with handle_unknown='ignore'.
Splits: primary = time-based (oldest 75% train, newest 25% test; corpus README
'Splits and cautions': train/test by ts to avoid leakage across chronological
drift), secondary = stratified random 75/25 seed 42.
Metrics: accuracy, balanced accuracy, ROC AUC on held-out.
Router: for each trained task_shape, rank animals by predicted P(success);
route table + fitted model + metrics land under watch/inbox/ml_moonshot_20261007/.

Driving-ladder law: classical first, $0; the MIRA-style generative critic is
deferred unless classical plateaus; the $0-vs-$ comparison is in the metrics
(paid per-call cost measured from the same usage rows the model trains on).

CLI: .venv/Scripts/python.exe tools/gps_router_v0.py [--corpus DIR] [--out DIR]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag.percolator import partition  # noqa: E402  (repo-root import after sys.path fix)

SCHEMA = "gps_router.v0"
SEED = 42

# usage id prefix -> task_shape (deterministic derivation from the id field;
# prefixes measured by value_counts on the 3038-row usage table at build).
USAGE_SHAPE_MAP = {
    "TAVERN": "tavern-turn", "T1W1": "tavern-turn", "T1W2": "tavern-turn",
    "T1W3": "tavern-turn", "dnd0": "dnd-session", "DND0": "dnd-session",
    "DUEL1": "duel", "DUEL2": "duel", "CAMP": "camp", "PROBE": "probe",
    "N1": "night", "N1R": "night", "A1": "descent-leg", "B1": "descent-leg",
    "B2": "descent-leg", "C1": "descent-leg", "D1": "descent-leg",
    "GALA": "gala", "H247": "hourly", "SUBSTANCE": "substance",
    "SEASON": "season", "THE": "other",
}
FEATURE_COLS = ["node", "animal", "task_shape", "source"]


def _usage_shape(uid: str) -> str:
    prefix = str(uid).split("_", 1)[0]
    if prefix in USAGE_SHAPE_MAP:
        return USAGE_SHAPE_MAP[prefix]
    head = "".join(ch for ch in prefix if ch.isalpha()).upper()
    return USAGE_SHAPE_MAP.get(head, "other")


def load_frame(corpus: Path) -> pd.DataFrame:
    """Unify ml1's gps_verdicts + gauntlet + usage tables into router rows."""
    rows: list[pd.DataFrame] = []

    v = pd.read_parquet(corpus / "gps_verdicts.parquet")
    rows.append(pd.DataFrame({
        "node": "ledger",
        "animal": v["model_id"].astype(str),
        "task_shape": v["task_shape"].astype(str),
        "source": "gps_verdicts",
        "success": v["verdict_label"].astype(int),
        "ts": v["ts"],
        "text": "",
        "cost_usd": np.nan,
    }))

    g = pd.read_parquet(corpus / "gauntlet.parquet")
    g = g[g["pass_label"].notna()].copy()
    rows.append(pd.DataFrame({
        "node": g["family"].astype(str),
        "animal": g["animal"].astype(str),
        "task_shape": g["family"].astype(str),
        "source": "gauntlet",
        "success": g["pass_label"].astype(int),
        "ts": g["ts"],
        "text": g["note"].fillna("").astype(str),
        "cost_usd": 0.0,  # free seats, per GAUNTLET_FREE_LANDED_20261006.md
    }))

    u = pd.read_parquet(corpus / "usage.parquet")
    u = u[u["ok_label"].notna()].copy()
    rows.append(pd.DataFrame({
        "node": u["id"].astype(str).str.split("_").str[0],
        "animal": u["model"].astype(str),
        "task_shape": u["id"].astype(str).map(_usage_shape),
        "source": "usage",
        "success": u["ok_label"].astype(int),
        "ts": u["ts"],
        "text": u["error"].fillna("").astype(str) if "error" in u else "",
        "cost_usd": u["cost_usd"].fillna(0.0).astype(float),
    }))

    df = pd.concat(rows, ignore_index=True)
    df["percolator_score"] = [
        (lambda p: p["n_signal"] - p["n_theater"] - p["n_noise"])(partition(t))
        for t in df["text"]
    ]
    return df


def percolator_baseline(df: pd.DataFrame, train_idx: np.ndarray,
                        test_idx: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Named baseline: percolator lexicon score, prior fallback on empty text.

    Rows with no text score 0 by construction, so the score cannot order them;
    those rows predict the training prior. Returns (pred, score) for AUC.
    """
    prior = float(df.iloc[train_idx]["success"].mean())
    te = df.iloc[test_idx]
    has_text = (te["text"].str.len() > 0).to_numpy()
    score = te["percolator_score"].to_numpy(dtype=float)
    pred = np.where(has_text, (score > 0).astype(int), int(prior >= 0.5))
    # rows without text get the prior as their constant score for AUC
    auc_score = np.where(has_text, score, prior)
    return pred, auc_score


def capability_baseline(corpus: Path, df: pd.DataFrame,
                        test_idx: np.ndarray) -> np.ndarray:
    """Incumbent production router: capability.pass_rate per (model, shape)."""
    cap = pd.read_parquet(corpus / "gps_capability.parquet")
    rates = {(r.model_id, r.task_shape): float(r.pass_rate)
             for r in cap.itertuples()}
    global_mean = float(cap["pass_rate"].mean())
    te = df.iloc[test_idx]
    return np.array([
        rates.get((r.animal, r.task_shape), global_mean) for r in te.itertuples()
    ])


def _metrics(y_true: pd.Series, pred: np.ndarray, score: np.ndarray) -> dict:
    out = {
        "n": int(len(y_true)),
        "pos_rate": round(float(y_true.mean()), 4),
        "accuracy": round(float(accuracy_score(y_true, pred)), 4),
        "balanced_accuracy": round(float(balanced_accuracy_score(y_true, pred)), 4),
    }
    if len(set(score)) > 1 and y_true.nunique() == 2:
        out["roc_auc"] = round(float(roc_auc_score(y_true, score)), 4)
    else:
        out["roc_auc"] = None
    return out


def make_models() -> dict:
    return {
        "logistic_regression": LogisticRegression(max_iter=2000, random_state=SEED),
        "gradient_boosting": GradientBoostingClassifier(
            n_estimators=200, max_depth=3, learning_rate=0.1, random_state=SEED),
    }


def evaluate(df: pd.DataFrame, corpus: Path, out: dict) -> dict:
    """Two splits x three model rows + two baselines, one dict of metrics."""
    X = df[FEATURE_COLS].astype(str)
    y = df["success"]
    results: dict = {}
    fitted: dict = {}

    splits = {}
    order = df["ts"].sort_values().index
    cut = int(len(order) * 0.75)
    splits["time_75_25"] = (order[:cut].to_numpy(), order[cut:].to_numpy())
    tr, te = train_test_split(df.index.to_numpy(), test_size=0.25,
                              random_state=SEED, stratify=y)
    splits["stratified_75_25"] = (tr, te)

    for split_name, (train_idx, test_idx) in splits.items():
        block: dict = {"n_train": int(len(train_idx)), "n_test": int(len(test_idx))}
        if y.iloc[test_idx].nunique() < 2:
            block["error"] = "held-out split carries one class only; AUC undefined"
            results[split_name] = block
            continue

        pred, score = percolator_baseline(df, train_idx, test_idx)
        block["baseline_percolator"] = _metrics(y.iloc[test_idx], pred, score)

        cap_pred_score = capability_baseline(corpus, df, test_idx)
        block["baseline_ledger_capability"] = _metrics(
            y.iloc[test_idx], (cap_pred_score >= 0.5).astype(int), cap_pred_score)

        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import OneHotEncoder
        for name, model in make_models().items():
            pipe = make_pipeline(
                OneHotEncoder(handle_unknown="ignore"),
                model,
            )
            pipe.fit(X.iloc[train_idx], y.iloc[train_idx])
            proba = pipe.predict_proba(X.iloc[test_idx])[:, 1]
            block[name] = _metrics(y.iloc[test_idx],
                                   (proba >= 0.5).astype(int), proba)
            fitted[(split_name, name)] = pipe
        results[split_name] = block

    out["splits"] = results
    return fitted


def route_table(df: pd.DataFrame, pipe, out_dir: Path,
                min_support: int = 5) -> list[dict]:
    """Rank animals by predicted P(success) per task_shape (the v0 router).

    Evidence gate: best_animal is chosen only among animals with at least
    min_support training rows for that task_shape; a model can extrapolate a
    perfect record from a handful of rows (grok-4.7 measures 9 rows ledger-wide
    at build), so ungated argmax routes everything to the thinnest sample.
    """
    shapes = sorted(df["task_shape"].unique())
    animals = sorted(df["animal"].unique())
    grid = pd.DataFrame(
        [(s, a) for s in shapes for a in animals],
        columns=["task_shape", "animal"],
    )
    grid["node"] = "route"
    grid["source"] = df["source"].mode().iat[0]
    grid["p_success"] = pipe.predict_proba(grid[FEATURE_COLS])[:, 1]
    counts = df.groupby(["task_shape", "animal"]).size()
    costs = df.groupby("animal")["cost_usd"].mean() if "cost_usd" in df else {}

    table = []
    for shape, grp in grid.groupby("task_shape"):
        ranked = grp.sort_values("p_success", ascending=False)
        supported = [r for r in ranked.itertuples()
                     if int(counts.get((shape, r.animal), 0)) >= min_support]
        pick = supported[0] if supported else None
        shape_rows = int(counts.loc[shape].sum()) if shape in counts.index.get_level_values(0) else 0
        table.append({
            "task_shape": shape,
            "n_train_rows": shape_rows,
            "best_animal": str(pick.animal) if pick else None,
            "p_success": round(float(pick.p_success), 4) if pick else None,
            "evidence_gated": pick is not None,
            "fallback_note": (None if pick else
                              f"no animal reaches {min_support} training rows "
                              "for this shape; do not route"),
            "ungated_best": str(ranked.iloc[0]["animal"]),
            "ranking": [
                {"animal": str(r.animal), "p_success": round(float(r.p_success), 4),
                 "n_train_rows": int(counts.get((shape, r.animal), 0)),
                 "mean_cost_usd_per_row": (
                     round(float(costs[r.animal]), 4) if r.animal in costs else None)}
                for r in ranked.itertuples()
            ],
        })
    (out_dir / "ml3_route_table.json").write_text(
        json.dumps(table, indent=2), encoding="utf-8")
    return table


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--corpus", type=Path,
                    default=ROOT / "memory" / "corpus" / "ml" / "training")
    ap.add_argument("--out", type=Path,
                    default=ROOT / "watch" / "inbox" / "ml_moonshot_20261007")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    df = load_frame(args.corpus)
    print(f"rows={len(df)} sources={df['source'].value_counts().to_dict()} "
          f"shapes={df['task_shape'].nunique()} animals={df['animal'].nunique()} "
          f"prior={df['success'].mean():.4f}")

    out: dict = {"schema": SCHEMA, "corpus": str(args.corpus),
                 "n_rows": int(len(df)),
                 "class_prior": round(float(df["success"].mean()), 4),
                 "source_counts": {k: int(v) for k, v
                                   in df["source"].value_counts().items()}}
    fitted = evaluate(df, args.corpus, out)

    # route table from the time-split gradient boosting (the leakage-cautious
    # primary per corpus README); refit on full data for deployment coverage.
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import OneHotEncoder
    deploy = make_pipeline(
        OneHotEncoder(handle_unknown="ignore"),
        GradientBoostingClassifier(n_estimators=200, max_depth=3,
                                   learning_rate=0.1, random_state=SEED),
    )
    deploy.fit(df[FEATURE_COLS], df["success"])
    out["route_table_head"] = [
        {"task_shape": t["task_shape"], "n_train_rows": t["n_train_rows"],
         "best_animal": t["best_animal"], "p_success": t["p_success"],
         "ungated_best": t["ungated_best"]}
        for t in route_table(df, deploy, args.out)
    ][:8]

    joblib.dump(deploy, args.out / "ml3_router_model.joblib")

    # $0-vs-$ block (driving-ladder law): the classical lane spends $0.00 of
    # paid API budget; the paid alternative is measured from the same corpus.
    paid = df.loc[(df["source"] == "usage") & (df["cost_usd"] > 0), "cost_usd"]
    per_animal = (
        df.loc[(df["source"] == "usage") & (df["cost_usd"] > 0)]
        .groupby("animal")["cost_usd"].agg(["mean", "count"]))
    out["cost_block"] = {
        "classical_lane_paid_cost_usd": 0.0,
        "n_paid_rows": int(len(paid)),
        "total_paid_spend_usd": round(float(paid.sum()), 4),
        "mean_cost_per_paid_row_usd": round(float(paid.mean()), 4),
        "mean_cost_per_paid_row_usd_by_animal": {
            str(k): {"mean_usd": round(float(v["mean"]), 6),
                     "n": int(v["count"])}
            for k, v in per_animal.iterrows()},
    }

    (args.out / "ml3_router_metrics.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out["splits"], indent=2))
    print(f"landed: {args.out / 'ml3_router_metrics.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
