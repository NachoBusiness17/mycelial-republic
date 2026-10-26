"""classical_law_feed - the v0.7 propagation bridge for the thought quantizer.

CLASSICAL MODELS ARE LAWS TOO (run ml-moonshot-20261007 lane ml7,
2026-10-07). ml3's trained GPS router and ml4's lane forecaster rode only
in their run archives, so no flash seat inherited the classical layer at
boot - the v0.2 fossil pattern one layer up: artifacts landed, consumers
never wired. This module turns each fitted model into quantizer pack rows
whose law text names the artifact path plus the feature importances /
regression coefficients, weighted 1.0 and pinned by the compiler
(tools/thought_quantizer.py compile_packs) to the head of the flash band -
inheritance is structural, not rank luck.

A missing artifact is a census fact (the feed info rides the compile
report verbatim), never a silent skip and never the vault's fail-loud
refuser: the artifacts are run-scoped, so archiving the run must not
brick later compiles.
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _rel_posix(path) -> str:
    """Repo-relative posix path, absolute when outside ROOT.

    Same shape as the driver-meter lane's helper (tools/stealth_driver.py)
    and the quantizer's own pre-extraction copy: display/receipt paths must
    not raise ValueError when the artifact lives outside the repo.
    """
    try:
        return Path(path).relative_to(ROOT).as_posix()
    except ValueError:
        return Path(path).as_posix()


# The classical-model artifacts the compile bridges into the packs. The law
# text of each row names the artifact path + the fitted weights, so a flash
# seat inherits the classical layer at boot and can walk the pointer to the
# bytes.
ML3_DIR = ROOT / "watch" / "inbox" / "ml_moonshot_20261007"
ML3_METRICS = ML3_DIR / "ml3_router_metrics.json"
ML3_MODEL = ML3_DIR / "ml3_router_model.joblib"
ML4_DIR = (ROOT / "memory" / "runs" / "mickey17_v2" / "runs"
           / "ml-moonshot-20261007" / "lanes")
# The report is a run-level artifact, not a lane-row file: tools/mickey17_v2_fold.py
# counts every lanes/*.json as a lane, and the report sitting there tripped the
# FIRED-BELOW-ARCHIVE gate (fired 8 < archive 9, 2026-10-07), so it lives in the
# run dir. Receipt: memory/runs/mickey17_v2/runs/ml-moonshot-20261007/ML4_LANE_FORECASTER_RECEIPT.md
ML4_REPORT = ML4_DIR.parent / "ml4_forecast_report.json"
ML4_CHECKPOINTS = ML4_DIR / "ml4_checkpoints.jsonl"
# ml4's feature contract, byte-named in ml4_build_lane_forecaster.py FEATS.
ML4_FEATURES = ["log_rows_so_far", "frac", "elapsed_sofar_min", "family_code",
                "log_run_lanes_started"]
CLASSICAL_TOP_K = 3


def _iso_date(p: Path) -> str:
    """Artifact mtime as a YYYY-MM-DD provenance stamp."""
    try:
        return datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat()[:10]
    except OSError:
        return ""


def compose_ml3_law(metrics: dict, importances, artifact_rel: str) -> str:
    """Law text for the ml3 router row: artifact path + feature importances.

    The evidence-gate clause transcribes the trainer's own routing law
    (tools/gps_router_v0.py route_table min_support=5): thin shapes route
    to nothing, ungated argmax routes every shape to the thinnest sample.
    """
    sp = metrics.get("splits", {}).get("time_75_25", {})
    gb = sp.get("gradient_boosting", {})
    base = sp.get("baseline_percolator", {})
    parts = [f"CLASSICAL LAW ml3-gps-router: route (animal x task_shape) by "
             f"the fitted model {artifact_rel}"]
    if importances:
        parts.append("top importances "
                     + ", ".join(f"{n} {v:.4f}" for n, v in importances))
    if gb:
        parts.append(f"GB acc {gb.get('accuracy')} AUC {gb.get('roc_auc')} "
                     f"on {metrics.get('n_rows')} rows")
    if base.get("roc_auc") is not None:
        parts.append(f"vs percolator baseline AUC {base.get('roc_auc')}")
    parts.append("route a shape only with 5+ training rows (evidence gate)")
    return "; ".join(parts) + "."


def compose_ml4_law(report: dict, coefs: dict, n_ckpt: int,
                    ckpt_rel: str) -> str:
    """Law text for the ml4 forecaster row: artifact path + coefficients."""
    models = report.get("models", {})
    ridge = models.get("ridge", {})
    parts = [f"CLASSICAL LAW ml4-lane-forecaster: lane remaining-rows "
             f"forecast by Ridge(alpha=1.0) refit on all {n_ckpt} checkpoints "
             f"of {ckpt_rel}",
             "standardized coefs "
             + ", ".join(f"{f} {coefs[f]:+.4f}" for f in ML4_FEATURES
                         if f in coefs)]
    if ridge.get("spearman") is not None:
        parts.append(
            f"leave-one-run-out spearman {ridge.get('spearman')} "
            f"(hgb {models.get('hgb', {}).get('spearman')}) vs mean baseline "
            f"{models.get('mean', {}).get('spearman')}")
    return "; ".join(parts) + "."


def ml4_ridge_coefficients(checkpoints_path: Path = ML4_CHECKPOINTS
                           ) -> tuple[dict[str, float], int] | None:
    """Refit ml4's Ridge head on the landed checkpoint table.

    Same contract as the lane's own trainer (ml4_build_lane_forecaster.py:
    FEATS, log1p features, per-family target encoding of log1p(remaining)
    with the global mean fallback, StandardScaler + Ridge(alpha=1.0)),
    refit on ALL rows for deployment coverage - the same full-data deploy
    refit the ml3 trainer performs before dumping its joblib. Closed-form
    ridge, deterministic. Returns (coefficients, n) or None when the
    checkpoint table is absent or empty.
    """
    if not checkpoints_path.is_file():
        return None
    rows = [json.loads(x) for x in
            checkpoints_path.read_text(encoding="utf-8").splitlines()
            if x.strip()]
    if not rows:
        return None

    def num(r: dict, k: str) -> float:
        try:
            v = float(r.get(k))
        except (TypeError, ValueError):
            return 0.0
        return v if math.isfinite(v) else 0.0

    log_rem = [math.log1p(max(num(r, "remaining"), 0.0)) for r in rows]
    global_code = sum(log_rem) / len(log_rem)
    fam: dict[str, list[float]] = {}
    for r, lv in zip(rows, log_rem):
        fam.setdefault(str(r.get("family")), []).append(lv)
    fam_code = {f: sum(v) / len(v) for f, v in fam.items()}

    import numpy as np
    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import StandardScaler
    X = np.array([[num(r, "rows_so_far"), num(r, "frac"),
                   num(r, "elapsed_sofar_min"),
                   fam_code.get(str(r.get("family")), global_code),
                   num(r, "run_lanes_started")] for r in rows], dtype=float)
    X[:, 0] = np.log1p(X[:, 0])
    X[:, 4] = np.log1p(X[:, 4])
    y = np.array([max(num(r, "remaining"), 0.0) for r in rows], dtype=float)
    sc = StandardScaler().fit(X)
    mdl = Ridge(alpha=1.0).fit(sc.transform(X), y)
    return ({f: float(c) for f, c in zip(ML4_FEATURES, mdl.coef_)}, len(rows))


def pin_classical_first(ranked: list[dict]) -> list[dict]:
    """The flash pin: classical-model rows head the ranked list.

    The flash tier is the consumer seam every seat boots
    (mag/context_pack._quantized_laws), so the classical layer must
    inherit into it structurally, never by rank luck - fresh percolator
    imperatives can fill the weight-1.0 tie. The L4 linker invariants
    hold: every kept row still lands in exactly one band; the pin only
    reorders the list before the bands are cut.
    """
    return ([r for r in ranked if r["shape"] == "classical-model"]
            + [r for r in ranked if r["shape"] != "classical-model"])


def ml3_router_row(metrics_path: Path = ML3_METRICS,
                   model_path: Path = ML3_MODEL) -> tuple[dict | None, str]:
    """ml3's deployed GPS router as a law row (artifact path + importances).

    Returns (row, status); row is None when the artifacts are absent or
    unreadable and status names which - the compile census reports it,
    never silent. A model artifact that fails to load degrades to
    metrics-only law, with the load failure named in the status.
    """
    if not metrics_path.is_file():
        return None, "absent"
    try:
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return None, f"error: {type(e).__name__}: {e}"[:120]
    importances: list[tuple[str, float]] = []
    status = "metrics-only (model artifact absent)"
    if model_path.is_file():
        try:
            import joblib
            pipe = joblib.load(model_path)
            names = pipe.named_steps["onehotencoder"].get_feature_names_out()
            vals = pipe.named_steps["gradientboostingclassifier"] \
                       .feature_importances_
            importances = sorted(((str(n), float(v))
                                  for n, v in zip(names, vals)),
                                 key=lambda p: -p[1])[:CLASSICAL_TOP_K]
            status = "ok"
        except Exception as e:  # noqa: BLE001  (artifact skew is a census fact)
            importances = []
            status = f"metrics-only (model load failed: {type(e).__name__})"
    return ({"text": compose_ml3_law(metrics, importances,
                                     _rel_posix(model_path)),
             "count": int(metrics.get("n_rows", 0)),
             "last_seen": _iso_date(metrics_path)}, status)


def live_classical_rows() -> tuple[dict[str, dict], dict]:
    """The classical feed: fitted run models as quantizer law rows.

    Sources are the ml-moonshot-20261007 artifacts named in the constants
    above. A missing or unreadable source is a census fact in the feed info
    (the report carries classical_feed verbatim), never a silent skip and
    never a compile refuser - the artifacts are run-scoped, so archiving
    the run must not brick later compiles. The flash pin in the compiler's
    compile_packs is what makes the inheritance structural.
    """
    rows: dict[str, dict] = {}
    info: dict = {"source": "ml-moonshot-20261007 classical artifacts"}
    r3, s3 = ml3_router_row()
    info["ml3"] = s3
    if r3:
        rows["bridge_ml3_router"] = r3
    fit = ml4_ridge_coefficients()
    if fit is None:
        info["ml4"] = "absent"
    else:
        coefs, n_ckpt = fit
        try:
            report = json.loads(ML4_REPORT.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            report = {}
        info["ml4"] = "ok" if report else \
            "coefficients-only (report unreadable)"
        rows["bridge_ml4_forecast"] = {
            "text": compose_ml4_law(report, coefs, n_ckpt,
                                    _rel_posix(ML4_CHECKPOINTS)),
            "count": n_ckpt,
            "last_seen": _iso_date(ML4_CHECKPOINTS)}
    return rows, info
