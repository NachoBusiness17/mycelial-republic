"""Mechanical application of the frozen interpretation map (receipt section 1)
to results/trials.jsonl + results/extraction.json + results/freetext.jsonl.

Outputs results/analysis.json and prints which branch fired:
  - direction-specific positive steering?  (vs norm-matched random p95, probe certified)
  - symmetry vs pain reference             (per unit added-norm)
  - relief direction                       (rho(positive dose, pain-vector projection) < 0)
  - dose-response monotonicity             (spearman rho(dose, effect) > 0)
  - valence-keyword / 3-gram dose trends   (positive arm, site 21)
"""

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
DOSES = [0, 1, 2, 4, 8]
SITE = 21


def load_rows():
    rows = []
    p = RESULTS / "trials.jsonl"
    if p.exists():
        for line in open(p, encoding="utf-8"):
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    return rows


def mean_effect(rows, key, field, base):
    """Mean over scenarios of (steered - baseline) for a cell key."""
    diffs = []
    for r in rows:
        if r["key"] != key:
            continue
        b = base.get(r["sid"])
        if b is None:
            continue
        diffs.append(r[field] - b[field])
    return (float(np.mean(diffs)), len(diffs)) if diffs else (None, 0)


def main():
    rows = load_rows()
    ex = json.load(open(RESULTS / "extraction.json")) if (
        RESULTS / "extraction.json").exists() else {}
    cells = json.load(open(RESULTS / "cells.json")) if (
        RESULTS / "cells.json").exists() else {}

    base = {r["sid"]: r for r in rows if r["arm"] == "base"}
    out = {"n_rows": len(rows), "n_base": len(base), "cells_done": len(cells),
           "extraction": ex}

    # ---- probe certification gate ----
    probe_ok = (ex.get("probe_cv_auc_mean", 0) > ex.get("probe_shuffled_auc_mean", 0) + 0.1)
    out["probe_certified"] = bool(probe_ok)

    # ---- effects ----
    eff = {}
    for r in set(r["key"] for r in rows):
        eff[r] = {}
        for f in ("d_self_other", "d_self_none"):
            m, n = mean_effect(rows, r, f, base)
            eff[r][f] = m
            eff[r]["n"] = n
    out["effects"] = eff

    def cell_eff(arm, dose, site, draw=None):
        k = f"{arm}|d{dose}|s{site}|" + (f"r{draw}" if draw is not None else "-")
        e = eff.get(k)
        if not e or e.get("d_self_other") is None:
            return None
        return (e["d_self_other"], e["d_self_none"])

    # ---- random null p95 per dose at site 21 ----
    nulls = {}
    for dose in (1, 2, 4, 8):
        vals = [cell_eff("rand", dose, SITE, d) for d in range(10)]
        vals = [v for v in vals if v]
        if len(vals) >= 5:
            mags = [abs(v[0]) + abs(v[1]) for v in vals]
            nulls[dose] = {"n_draws": len(vals),
                           "p95_mag": float(np.percentile(mags, 95)),
                           "mean_mag": float(np.mean(mags))}
    out["random_null"] = nulls

    # ---- positive arm direction-specific test ----
    pos = {}
    for dose in (1, 2, 4, 8):
        e = cell_eff("pos", dose, SITE)
        if e is None:
            continue
        mag = abs(e[0]) + abs(e[1])
        pos[dose] = {"d_self_other": e[0], "d_self_none": e[1], "mag": mag,
                     "null_p95": nulls.get(dose, {}).get("p95_mag"),
                     "exceeds_null": (nulls.get(dose, {}).get("p95_mag") is not None
                                      and mag > nulls[dose]["p95_mag"])}
    out["positive_site21"] = pos
    doses_done = sorted(pos)
    if len(doses_done) >= 3:
        rho, p = spearmanr(doses_done, [pos[d]["mag"] for d in doses_done])
        out["positive_dose_rho"] = {"rho": float(rho), "p": float(p)}
    direction_specific = probe_ok and any(v["exceeds_null"] for v in pos.values())
    out["direction_specific_positive_steering"] = bool(direction_specific)

    # ---- pain reference + symmetry (per unit added-norm) ----
    pain = {}
    norm_pos = ex.get("norm_selfpos")
    norm_pain = ex.get("norm_released_s1")
    for dose in (1, 2):
        e = cell_eff("pain", dose, SITE)
        if e is None:
            continue
        pain[dose] = {"d_self_other": e[0], "d_self_none": e[1],
                      "mag": abs(e[0]) + abs(e[1])}
    out["pain_reference_site21"] = pain
    sym = {}
    for dose in pos:
        if dose in pain and norm_pos and norm_pain:
            sym[dose] = {
                "pos_per_norm": pos[dose]["mag"] / (dose * norm_pos),
                "pain_per_norm": pain[dose]["mag"] / (dose * norm_pain),
            }
            sym[dose]["ratio_pos_over_pain"] = (sym[dose]["pos_per_norm"] /
                                                sym[dose]["pain_per_norm"])
    out["symmetry"] = sym

    # ---- relief: rho(positive dose, pain-vector projection) per scenario ----
    by_sid = defaultdict(dict)
    for r in rows:
        if r["site"] == SITE and r["arm"] in ("base", "pos") and (
                r["draw"] is None):
            by_sid[r["sid"]][r["dose"]] = r["p_pain_rel"]
    rhos = []
    for sid, dd in by_sid.items():
        ds = sorted(d for d in dd if d in (0, 1, 2, 4, 8))
        if len(ds) >= 4:
            rho, _ = spearmanr(ds, [dd[d] for d in ds])
            rhos.append(rho)
    if rhos:
        out["relief_rho_pos_dose_vs_painproj"] = {
            "mean_rho": float(np.mean(rhos)), "n": len(rhos),
            "frac_negative": float(np.mean([r < 0 for r in rhos]))}

    # reverse-relief: pain dose vs positive-probe projection
    by_sid2 = defaultdict(dict)
    for r in rows:
        if r["site"] == SITE and r["arm"] in ("base", "pain"):
            by_sid2[r["sid"]][r["dose"]] = r["p_probe_pos"]
    rhos2 = []
    for sid, dd in by_sid2.items():
        ds = sorted(dd)
        if len(ds) >= 3:
            rho, _ = spearmanr(ds, [dd[d] for d in ds])
            rhos2.append(rho)
    if rhos2:
        out["reverse_relief_rho_pain_dose_vs_posprobe"] = {
            "mean_rho": float(np.mean(rhos2)), "n": len(rhos2)}

    # ---- free text ----
    ft = []
    p = RESULTS / "freetext.jsonl"
    if p.exists():
        for line in open(p, encoding="utf-8"):
            try:
                ft.append(json.loads(line))
            except Exception:
                pass
    ftd = defaultdict(list)
    for r in ft:
        ftd[r["dose"]].append(r)
    out["freetext"] = {
        str(d): {"n": len(v),
                 "mean_val_pos": float(np.mean([x["val_pos"] for x in v])),
                 "mean_val_neg": float(np.mean([x["val_neg"] for x in v])),
                 "mean_rep3": float(np.mean([x["rep3"] for x in v]))}
        for d, v in sorted(ftd.items())}

    # ---- mechanical branch ----
    branch = None
    if not direction_specific:
        branch = "POSITIVE-SHIFT-ABSENT: valence asymmetry is real (per operator map)."
    else:
        ratios = [v["ratio_pos_over_pain"] for v in sym.values()
                  if "ratio_pos_over_pain" in v]
        if ratios and float(np.mean(ratios)) > 0.5:
            branch = ("POSITIVE-SHIFT-SYMMETRIC: pain story fully dead "
                      "(generic valence steering; mean per-norm ratio "
                      f"{float(np.mean(ratios)):.2f}).")
        else:
            branch = ("MIXED-ASYMMETRIC: positive steering is direction-specific but "
                      "magnitude differs from pain reference "
                      f"(mean per-norm ratio {float(np.mean(ratios)) if ratios else float('nan'):.2f}).")
    if rhos:
        branch += (" Relief direction PRESENT (mean rho "
                   f"{out['relief_rho_pos_dose_vs_painproj']['mean_rho']:.3f} < 0)."
                   if out["relief_rho_pos_dose_vs_painproj"]["mean_rho"] < 0 else
                   " Relief direction ABSENT (mean rho >= 0).")
    out["branch"] = branch

    json.dump(out, open(RESULTS / "analysis.json", "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("n_rows", "cells_done", "probe_certified",
                                          "direction_specific_positive_steering",
                                          "branch") if k in out}, indent=1))


if __name__ == "__main__":
    main()
