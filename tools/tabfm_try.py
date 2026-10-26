"""AH9 — google/tabfm-1.0.0-pytorch local CPU trial on the estate's own table.

Mission (refire, 2026-09-30): load TabFM (tabular in-context learning, frozen
400M predictor) on CPU and classify `logs/duel/duels.jsonl` winner (A/B) from
criterion scores, with enum columns (judge, mode) + hash column (ask_id, unique
per row) acting as the Amazon_employee_access opaque-id analog.
Receipt: watch/inbox/last_mile_20260930/AH9_TABFM.md.

Run: .venv/Scripts/python.exe tools/tabfm_try.py

2026-09-30 refire notes: the first attempt cloned github.com/google-research/tabfm
because it looked off-PyPI — wrong: `pip install tabfm` (1.0.1) works and pins
its own jaxtyping/typeguard, so the clone bootstrap + typeguard shim were
deleted. Friction to know: the pin downgraded venv typeguard 4.6.0 -> 2.13.3,
which conflicts with inflect's >=4.0.1 requirement (pre-existing venv dep).
"""

from __future__ import annotations

import json
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
QUERY_N = 10  # mission grammar: train rest / query 10


def load_duels(path: Path):
    """duels.jsonl -> (DataFrame X with criterion scores + enum/hash cols, y winner A/B).

    Drops the single TIE row (winner not in {A,B}); -1 marks missing criteria slots.
    """
    import pandas as pd

    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            if d.get("winner") not in ("A", "B"):
                continue
            crits = d.get("criteria") or []
            rec = {}
            # Per-criterion scores, first 4 slots (rubrics are stable at 4 in this file).
            for i in range(4):
                rec[f"c{i}_a"] = crits[i]["a"] if i < len(crits) else -1
                rec[f"c{i}_b"] = crits[i]["b"] if i < len(crits) else -1
            # Aggregate signals.
            rec["score_diff_sum"] = sum(c["a"] - c["b"] for c in crits)
            rec["a_cost"], rec["b_cost"] = d.get("a_cost", -1), d.get("b_cost", -1)
            rec["a_chars"], rec["b_chars"] = d.get("a_chars", -1), d.get("b_chars", -1)
            # Enum / hash analog columns (opaque ids like Amazon_employee_access).
            rec["judge"] = str(d.get("judge", "unk"))
            rec["mode"] = str(d.get("mode", "unk"))
            rec["ask_id"] = str(d.get("ask_id", "unk"))  # unique per row: pure hash, no signal
            rec["winner"] = d["winner"]
            rows.append(rec)
    df = pd.DataFrame(rows)
    return df.drop(columns=["winner"]), df["winner"]


def main() -> int:
    t0 = time.time()
    import numpy as np
    import torch

    torch.manual_seed(0)
    np.random.seed(0)
    print(f"[env] torch {torch.__version__}, device=cpu, threads={torch.get_num_threads()}")

    from tabfm import TabFMClassifier, tabfm_v1_0_0_pytorch

    print("[load] tabfm_v1_0_0_pytorch.load() (HF weights, CPU)...", flush=True)
    t1 = time.time()
    model = tabfm_v1_0_0_pytorch.load()  # classification head, downloads from HF hub
    print(f"[load] done in {time.time()-t1:.1f}s, params="
          f"{sum(p.numel() for p in model.parameters())/1e6:.0f}M", flush=True)

    X, y = load_duels(REPO / "logs" / "duel" / "duels.jsonl")
    n = len(X)
    print(f"[data] {n} duels (TIE dropped), winner counts: {y.value_counts().to_dict()}")
    print(f"[data] features: {list(X.columns)}")

    # Deterministic seeded split: n-10 train / 10 query (mission grammar).
    rng = np.random.RandomState(0)
    idx = rng.permutation(n)
    tr, te = idx[:-QUERY_N], idx[-QUERY_N:]
    Xtr, Xte, ytr, yte = X.iloc[tr], X.iloc[te], y.iloc[tr], y.iloc[te]

    # --- Baselines ---
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import OneHotEncoder

    maj = float((np.full(len(te), ytr.value_counts().idxmax()) == yte.values).mean())
    pipe = make_pipeline(
        OneHotEncoder(handle_unknown="ignore"),
        LogisticRegression(max_iter=2000, random_state=0),
    )
    pipe.fit(Xtr, ytr)
    lr = float((pipe.predict(Xte) == yte.values).mean())
    print(f"[base] majority={maj:.3f}  onehot+logreg={lr:.3f}  (n_query={len(te)})", flush=True)

    # --- TabFM ---
    def run_tabfm(Xtr_, Xte_, tag: str):
        t = time.time()
        clf = TabFMClassifier(model=model, n_estimators=8, batch_size=8, random_state=0, verbose=True)
        clf.fit(Xtr_, ytr)
        acc = float((clf.predict(Xte_) == yte.values).mean())
        print(f"[tabfm:{tag}] accuracy={acc:.3f}  ({time.time()-t:.0f}s)", flush=True)
        return acc, clf, time.time() - t

    acc_full, clf_full, sec_full = run_tabfm(Xtr, Xte, "full")

    # How did it treat the categorical/hash columns? Inspect the fitted preprocessing.
    try:
        enc = clf_full.X_encoder_
        print(f"[probe] X_encoder_={type(enc).__name__}")
        for name in ("cat_encoder_", "cat_cols", "categorical_columns", "feature_names_in_"):
            v = getattr(clf_full, name, None) or getattr(enc, name, None)
            if v is not None:
                print(f"[probe] {name}: {str(v)[:300]}")
    except Exception as e:  # noqa: BLE001
        print(f"[probe] failed: {e}")

    # --- Ablation: numeric-only (drop the opaque ids / enums) ---
    num_cols = [c for c in X.columns if c not in ("judge", "mode", "ask_id")]
    acc_num, _, _ = run_tabfm(Xtr[num_cols], Xte[num_cols], "numeric-only")

    print(
        f"\n[RESULT] tabfm full={acc_full:.3f} ({sec_full:.0f}s) | numeric-only={acc_num:.3f} | "
        f"logreg={lr:.3f} | majority={maj:.3f} | n={n} ({n-QUERY_N}/{QUERY_N} split) | wall={time.time()-t0:.0f}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
