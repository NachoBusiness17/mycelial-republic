#!/usr/bin/env python3
"""GATE V3 FALSIFIER — step 0 of the salon build order.
Question: do fleet events already carry discriminative signatures on EXISTING metadata?
If logistic regression on plain categorical fields predicts gate outcome (DONE vs THIN)
significantly above chance, the spectral premise is SUPPORTED and band-count EMERGES from
the coefficients. If AUC ~0.5, the premise fails cheaply — no gate v3 build.
No embeddings, no TF-IDF, no shaders, no dashboards (per the planning fold).
"""
import json, glob, os, collections, sys
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import roc_auc_score

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_rows():
    archives = sorted(glob.glob(os.path.join(ROOT, "dashboard", "data", "*.runaway-evidence-20260903")))
    path = archives[0] if archives else os.path.join(ROOT, "dashboard", "data", "ractor_board.jsonl")
    rows = []
    with open(path, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            try:
                r = json.loads(line)
                if r.get("status") in ("DONE", "THIN"):
                    rows.append(r)
            except Exception:
                continue
    print("data source:", os.path.basename(path), "labeled rows:", len(rows))
    return rows

def featurize(rows):
    organs = sorted({str(r.get("organ")) for r in rows})
    kinds = sorted({str(r.get("kind")) for r in rows})
    organ_idx = {o: i for i, o in enumerate(organs)}
    kind_idx = {k: i for i, k in enumerate(kinds)}
    X, y, meta = [], [], []
    for r in rows:
        ts = str(r.get("ts", ""))
        try:
            hour = int(ts[11:13])
        except (ValueError, IndexError):
            hour = 12
        detail = str(r.get("detail") or "")
        has_evidence = 1 if r.get("evidence") else 0
        X.append([organ_idx[str(r.get("organ"))], kind_idx[str(r.get("kind"))],
                  hour, len(detail), has_evidence])
        y.append(1 if r.get("status") == "DONE" else 0)
        meta.append((str(r.get("organ")), str(r.get("kind"))))
    return np.array(X), np.array(y), organs, kinds

def main():
    rows = load_rows()
    if len(rows) < 30:
        print("TOO FEW LABELED ROWS — falsifier cannot run honestly.")
        return 1
    X, y, organs, kinds = featurize(rows)
    print("label balance:", collections.Counter(y.tolist()))
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    clf = LogisticRegression(max_iter=2000, class_weight="balanced")
    clf.fit(Xtr, ytr)
    prob = clf.predict_proba(Xte)[:, 1]
    auc_hold = roc_auc_score(yte, prob)
    cv = cross_val_score(LogisticRegression(max_iter=2000, class_weight="balanced"),
                         X, y, cv=3, scoring="roc_auc")
    # block-wise 3-fold is weak with duplicated rows; report both + a shuffled-label floor
    rng = np.random.default_rng(7)
    floor_aucs = []
    for _ in range(5):
        ysh = rng.permutation(y)
        s = cross_val_score(LogisticRegression(max_iter=2000, class_weight="balanced"),
                            X, ysh, cv=3, scoring="roc_auc")
        floor_aucs.append(s.mean())
    print("\n=== GATE V3 FALSIFIER ===")
    print("holdout AUC: %.3f" % auc_hold)
    print("3-fold CV AUC: %.3f +/- %.3f" % (cv.mean(), cv.std()))
    print("shuffled-label floor: %.3f (mean of 5)" % float(np.mean(floor_aucs)))
    margin = cv.mean() - float(np.mean(floor_aucs))
    print("signal over floor: +%.3f" % margin)
    names = (["organ:" + o for o in organs] + ["kind:" + k for k in kinds]
             + ["hour", "detail_len", "has_evidence"])
    # coefficients: first two columns are categorical CODES (ordinal) — rerun one-hot
    # properly for honest band ranking
    enc_rows = [[str(r.get("organ")), str(r.get("kind")), str(r.get("ts"))[11:13],
                 len(str(r.get("detail") or "")), 1 if r.get("evidence") else 0] for r in rows]
    cats = OneHotEncoder(handle_unknown="ignore")
    cat_part = cats.fit_transform([[row[0], row[1]] for row in enc_rows]).toarray()
    num_part = np.array([[int(row[2]) if row[2].isdigit() else 12, row[3], row[4]]
                         for row in enc_rows], dtype=float)
    num_part[:, 1] = (num_part[:, 1] - num_part[:, 1].mean()) / (num_part[:, 1].std() + 1e-9)
    Xo = np.hstack([cat_part, num_part])
    clf2 = LogisticRegression(max_iter=2000, class_weight="balanced")
    clf2.fit(Xo, y)
    cv2 = cross_val_score(LogisticRegression(max_iter=2000, class_weight="balanced"),
                          Xo, y, cv=3, scoring="roc_auc")
    print("one-hot 3-fold CV AUC: %.3f +/- %.3f" % (cv2.mean(), cv2.std()))
    feat_names = list(cats.get_feature_names_out()) + ["hour", "detail_len(z)", "has_evidence"]
    ranked = sorted(zip(feat_names, clf2.coef_[0]), key=lambda t: -abs(t[1]))[:10]
    print("\nEMERGING BANDS (top |coefficients| — positive pushes DONE):")
    for name, coef in ranked:
        print("  %-28s %+.3f" % (name, coef))
    verdict = ("PASS" if cv2.mean() - 0.5 > 2 * (cv2.std() + 1e-9) and cv2.mean() > 0.60
               else "FAIL" if cv2.mean() < 0.55 else "WEAK — gather more data")
    print("\nVERDICT: %s (premise: fleet metadata discriminates gate outcomes)" % verdict)
    open(os.path.join(ROOT, "memory", "runs", "chord_test", "FALSIFIER_RESULT.md"), "w",
         encoding="utf-8").write(
         "holdout AUC %.3f\none-hot CV AUC %.3f +/- %.3f\nfloor %.3f\nverdict %s\nbands %s\n"
         % (auc_hold, cv2.mean(), cv2.std(), float(np.mean(floor_aucs)), verdict,
            str(ranked)))
    return 0

if __name__ == "__main__":
    sys.exit(main())
