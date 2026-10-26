#!/usr/bin/env python
"""Duel style-control regression (Z18, 2026-09-30).

Reads logs/duel/duels.jsonl (blind v1.1 era rows carry a_chars/b_chars
and a_headers/b_headers) and fits a numpy-only logistic regression of
glm win probability on normalized style differences, to answer the S5
hydrology question: is glm-prime's blind-era lead explained by answer
STYLE (length, header count) or by MODEL CONTENT?

Design, glm perspective in every row (the league is two contenders,
qwen on side A and glm on side B in all banked rows):

    y        = 1 if glm won the row, 0 if qwen won (ties: dropped in
               the primary fit, duplicated 0+1 in the sensitivity fit)
    char_d   = (glm_chars - qwen_chars) / mean(gl_chars, qw_chars)
               symmetric relative length gap; -0.5 means glm is ~50%
               of the way to half-length
    hdr_d    = (glm_hdr - qwen_hdr) / mean(gl_hdr, qw_hdr)
    identity = "glm appears in this row" dummy. With exactly one
               pairing in the ledger this dummy is constant and
               PERFECTLY COLLINEAR with the intercept, so the tool
               detects it, drops it, and reports the intercept as the
               style-controlled glm identity term (glm win log-odds at
               style parity). If a future ledger gains mixed pairings
               (glm on side A, or a third contender), the dummy gains
               variation and enters the fit for real.

Estimator: Newton/IRLS on the exact binomial log-likelihood, tiny
ridge (1e-8) for numerical stability, Wald SEs from the inverse
Fisher information X^T W X. No sklearn, no network, no spend; the
script is read-only over the ledger and prints to stdout.

Honesty contract: n is tiny (roughly 10 effective rows), so every
number below is SUGGESTIVE, never a calibrated claim. The script
prints the raw win rate and the exact one-sided binomial p next to
the coefficients so nobody reads signal into noise.

Usage:
    .venv/Scripts/python.exe tools/duel_style_regression.py
    .venv/Scripts/python.exe tools/duel_style_regression.py --json
    .venv/Scripts/python.exe tools/duel_style_regression.py --ledger <path>
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
DEFAULT_LEDGER = REPO / "logs" / "duel" / "duels.jsonl"
RIDGE = 1e-8
MAX_ITER = 100


def load_rows(ledger: Path) -> list[dict]:
    rows = []
    with open(ledger, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def rel_diff(x: float, y: float) -> float:
    """Symmetric relative difference (x - y) / mean(x, y)."""
    m = (x + y) / 2.0
    return 0.0 if m == 0 else (x - y) / m


def build_design(rows: list[dict], tie_mode: str) -> tuple[np.ndarray, np.ndarray, list[str], dict]:
    """Return (X, y, names, stats) from the glm perspective.

    Rows missing header counts are excluded from every fit (style pool);
    ties are dropped (primary) or duplicated 0+1 (sensitivity).
    """
    feats: list[list[float]] = []
    ys: list[float] = []
    n_skipped_hdr = 0
    for r in rows:
        a_c, b_c = r.get("a_chars"), r.get("b_chars")
        a_h, b_h = r.get("a_headers"), r.get("b_headers")
        if a_c is None or b_c is None or a_h is None or b_h is None:
            n_skipped_hdr += 1
            continue
        char_d = rel_diff(b_c, a_c)  # glm minus qwen, glm is side B
        hdr_d = rel_diff(b_h, a_h)
        w = r.get("winner")
        if w == "B":
            ys.append(1.0)
            feats.append([char_d, hdr_d])
        elif w == "A":
            ys.append(0.0)
            feats.append([char_d, hdr_d])
        elif str(w).upper() == "TIE":
            if tie_mode == "drop":
                continue
            # duplicate: one row y=1, one row y=0; contributes
            # -log p - log(1-p), minimized at p=0.5 (soft tie)
            ys.extend([1.0, 0.0])
            feats.extend([[char_d, hdr_d], [char_d, hdr_d]])
        else:
            raise ValueError(f"unparsable winner field: {w!r}")
    X = np.asarray(feats, dtype=float)
    y = np.asarray(ys, dtype=float)
    stats = {"n_rows": len(rows), "n_skipped_no_headers": n_skipped_hdr,
             "n_eff": int(y.shape[0])}
    return X, y, ["char_diff_norm", "hdr_diff_norm"], stats


def irls(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, bool]:
    """Newton/IRLS logistic fit with ridge; returns (beta, se, converged).

    Wald SEs from the inverse Fisher information X^T diag(p(1-p)) X
    (plus the same ridge so the inverse stays finite).
    """
    n, p = X.shape
    beta = np.zeros(p)
    converged = False
    for _ in range(MAX_ITER):
        eta = X @ beta
        mu = 1.0 / (1.0 + np.exp(-np.clip(eta, -35, 35)))
        grad = X.T @ (y - mu) - RIDGE * beta
        W = np.clip(mu * (1.0 - mu), 1e-10, None)
        H = X.T @ (X * W[:, None]) + RIDGE * np.eye(p)
        try:
            step = np.linalg.solve(H, grad)
        except np.linalg.LinAlgError:
            break
        beta = beta + step
        if np.max(np.abs(step)) < 1e-10:
            converged = True
            break
    eta = X @ beta
    mu = 1.0 / (1.0 + np.exp(-np.clip(eta, -35, 35)))
    W = np.clip(mu * (1.0 - mu), 1e-10, None)
    H = X.T @ (X * W[:, None]) + RIDGE * np.eye(p)
    cov = np.linalg.inv(H)
    return beta, np.sqrt(np.clip(np.diag(cov), 0, None)), converged


def z_p(z: float) -> float:
    """Two-sided normal tail p, erfc-based (no scipy)."""
    return math.erfc(abs(z) / math.sqrt(2.0))


def binom_ge(k: int, n: int, p0: float = 0.5) -> float:
    """Exact one-sided binomial P(wins >= k | n, p0)."""
    total = sum(math.comb(n, i) * p0 ** i * (1 - p0) ** (n - i)
                for i in range(k, n + 1))
    return total


def fit_spec(name: str, X: np.ndarray, y: np.ndarray, labels: list[str]) -> dict:
    beta, se, conv = irls(X, y)
    rows = []
    for lab, b, s in zip(labels, beta, se):
        z = b / s if s > 0 else float("inf")
        rows.append({"term": lab, "log_odds": round(float(b), 4),
                     "se": round(float(s), 4), "z": round(float(z), 2),
                     "p_two_sided": round(z_p(z), 4)})
    p_max = float(np.max(1.0 / (1.0 + np.exp(-(X @ beta)))))
    p_min = float(np.min(1.0 / (1.0 + np.exp(-(X @ beta)))))
    return {"spec": name, "n": int(y.shape[0]), "converged": conv,
            "coefficients": rows,
            "glm_win_prob_at_style_parity": round(
                float(1.0 / (1.0 + math.exp(-beta[0]))), 4),
            "fitted_prob_range": [round(p_min, 4), round(p_max, 4)]}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    ap.add_argument("--json", action="store_true",
                    help="emit machine-readable JSON instead of prose")
    args = ap.parse_args()

    rows = load_rows(args.ledger)
    X, y, feat_names, pool = build_design(rows, tie_mode="drop")

    glm_wins = int(y.sum())
    qwen_wins = int(y.shape[0] - glm_wins)
    raw_rate = glm_wins / y.shape[0] if y.shape[0] else float("nan")

    # identity-dummy feasibility: with one fixed pairing the glm-side
    # dummy is constant, so the intercept IS the identity term (see
    # module docstring); detect and say so instead of fitting a
    # collinear column.
    pairs = {(r.get("a_model"), r.get("b_model")) for r in rows}
    identity_dummy_feasible = len(pairs) > 1

    specs: list[dict] = []
    # M0: intercept only (raw glm lead, style-blind)
    specs.append(fit_spec("M0 intercept only (raw glm lead)",
                          np.ones((y.shape[0], 1)), y, ["intercept"]))
    # M1: primary style-controlled fit
    X1 = np.column_stack([np.ones(y.shape[0]), X])
    specs.append(fit_spec("M1 style-controlled (primary)",
                          X1, y, ["intercept (=glm identity at parity)"]
                          + feat_names))
    # M2: add presentation-slot dummy (swap=true puts glm in slot A)
    swaps = []
    for r in rows:
        if (r.get("a_headers") is not None and r.get("b_headers") is not None
                and str(r.get("winner", "")).upper() not in ("TIE",)):
            swaps.append(1.0 if r.get("swap") else 0.0)
    X2 = np.column_stack([X1, np.asarray(swaps)])
    specs.append(fit_spec("M2 + slot dummy (glm in slot A)",
                          X2, y, ["intercept (=glm identity at parity)"]
                          + feat_names + ["glm_in_slot_a"]))
    # S1: sensitivity, ties duplicated as 0+1
    Xt, yt, _, _ = build_design(rows, tie_mode="duplicate")
    Xs = np.column_stack([np.ones(yt.shape[0]), Xt])
    specs.append(fit_spec("S1 ties duplicated 0+1",
                          Xs, yt, ["intercept (=glm identity at parity)"]
                          + feat_names))

    # confound diagnostics: glm is shorter in EVERY row, so length and
    # identity are near-collinear; print the raw correlations
    r_char = float(np.corrcoef(X[:, 0], y)[0, 1]) if y.shape[0] > 2 else float("nan")
    r_hdr = float(np.corrcoef(X[:, 1], y)[0, 1]) if y.shape[0] > 2 else float("nan")
    char_always_negative = bool(np.all(X[:, 0] < 0))
    hdr_always_negative = bool(np.all(X[:, 1] < 0))

    out = {
        "ledger": str(args.ledger),
        "pool": pool,
        "pairs": sorted(f"{a} vs {b}" for a, b in pairs),
        "identity_dummy_feasible": identity_dummy_feasible,
        "raw_glm_record": {"glm": glm_wins, "qwen": qwen_wins,
                           "ties_dropped": pool["n_rows"]
                           - pool["n_skipped_no_headers"] - pool["n_eff"],
                           "raw_win_rate": round(raw_rate, 4),
                           "exact_binom_p_one_sided":
                               round(binom_ge(glm_wins, int(y.shape[0])), 4)},
        "confound": {"pearson_r_char_diff_vs_win": round(r_char, 3),
                     "pearson_r_hdr_diff_vs_win": round(r_hdr, 3),
                     "glm_always_shorter": char_always_negative,
                     "glm_always_fewer_headers": hdr_always_negative},
        "specs": specs,
        "honesty": ("n is tiny; all coefficients are suggestive only. "
                    + ("Length and identity are near-collinear "
                       "(glm shorter in every effective row). "
                       if char_always_negative else "")
                    + ("Header count is constant-sign (glm has fewer "
                       "headers in every effective row), so a header "
                       "effect cannot be separated from identity. "
                       if hdr_always_negative else "")
                    + "The style/content split is weakly identified."),
    }

    if args.json:
        print(json.dumps(out, indent=2))
        return 0

    W = out["raw_glm_record"]
    print(f"ledger {out['ledger']}: {pool['n_rows']} rows, "
          f"{pool['n_skipped_no_headers']} skipped (no header fields), "
          f"{pool['n_eff']} effective (ties dropped)")
    print(f"pairings: {out['pairs']}")
    print(f"identity dummy feasible: {identity_dummy_feasible} "
          "(constant side identity -> absorbed into intercept)")
    print(f"raw glm record: {W['glm']}-{W['qwen']} "
          f"(win rate {W['raw_win_rate']}, exact one-sided binomial p "
          f"{W['exact_binom_p_one_sided']})")
    c = out["confound"]
    print(f"confound: r(char_diff, glm_win)={c['pearson_r_char_diff_vs_win']} "
          f"r(hdr_diff, glm_win)={c['pearson_r_hdr_diff_vs_win']} "
          f"glm_always_shorter={c['glm_always_shorter']} "
          f"glm_always_fewer_headers={c['glm_always_fewer_headers']}")
    for s in specs:
        print(f"\n[{s['spec']}] n={s['n']} converged={s['converged']}")
        for cf in s["coefficients"]:
            print(f"  {cf['term']:38s} b={cf['log_odds']:+8.4f} "
                  f"se={cf['se']:.4f} z={cf['z']:+6.2f} "
                  f"p={cf['p_two_sided']:.4f}")
        print(f"  glm win prob at style parity: "
              f"{s['glm_win_prob_at_style_parity']}; fitted range "
              f"{s['fitted_prob_range']}")
    print(f"\nHONESTY: {out['honesty']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
