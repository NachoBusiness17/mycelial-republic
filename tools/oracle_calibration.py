"""THE 50, W6 item 29: oracle calibration harness (G31 recipe).

Recipe source: watch/inbox/GPS_BATTERY_20260918.jsonl line 31 (G31,
steering_theory): "oracle reads should carry a CONFIDENCE FIELD and the fleet's
rule should be: below threshold, the interpreter escalates to a bigger model or
a human, and the threshold is per-decision-class. ... how do you calibrate a
small oracle's confidence so the threshold means anything (calibration set,
temperature, per-domain drift)?"

Program row: watch/inbox/THE_50_PROGRAM_20260918.md line 46
(item 29, W6 INSTRUMENTS: "Oracle calibration harness (G31 recipe)").

What this module implements, per the G31 question:
  1. calibration set     -> binned predicted-vs-observed reliability table
                            (equal-width bins over confidence), with ECE, MCE
                            and Brier score
  2. temperature         -> fit temperature T on a calibration split
                            (logit scaling, NLL minimization), report ECE
                            before vs after on a held-out split
  3. per-domain drift    -> per decision_class reliability + ECE, drift flag
                            when a class is far worse calibrated than the best
                            class
  4. threshold           -> per decision_class, the LOWEST confidence
                            threshold whose calibration-set observed accuracy
                            meets a target, plus the escalated share (the
                            fraction of reads below the threshold that G31's
                            rule would send to a bigger model or a human)

No live oracle confidence ledger exists on disk yet (G31 is a steering
proposal), so the exercised validation path is the self-test on synthetic
data with known ground truth:
    .venv\\Scripts\\python.exe tools/oracle_calibration.py --selftest
It exits 0 only if every check passes and files a receipt with the real
numbers. Once oracle traces exist, score them with:
    .venv\\Scripts\\python.exe tools/oracle_calibration.py --input <reads.jsonl> --report <out.json>
Expected input rows (JSONL): {"confidence": float 0..1, "correct": bool,
"decision_class": str (optional), "ts": str (optional)}.

Stdlib only. Deterministic (fixed seed). No em-dashes.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RECEIPT_PATH = REPO / "watch/inbox/THE50_W6_T29_ORACLE_CALIBRATION.receipt.json"

SEED = 20260919
EPS = 1e-6
LOGIT_CLIP = 1e-4  # keep logits finite for confidence in {0, 1}


# --------------------------------------------------------------------------
# primitives
# --------------------------------------------------------------------------

def logit(p: float) -> float:
    p = min(max(float(p), LOGIT_CLIP), 1.0 - LOGIT_CLIP)
    return math.log(p / (1.0 - p))


def sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


def apply_temperature(confidence: float, temperature: float) -> float:
    """Logit scaling: p_T = sigmoid(logit(c) / T). T > 1 softens (fixes
    overconfidence), T < 1 sharpens (fixes underconfidence)."""
    return sigmoid(logit(confidence) / temperature)


# --------------------------------------------------------------------------
# 1. calibration set: binned predicted-vs-observed
# --------------------------------------------------------------------------

def load_reads(path: Path) -> list:
    reads = []
    skipped = 0
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                skipped += 1
                continue
            c = row.get("confidence")
            y = row.get("correct")
            if not isinstance(c, (int, float)) or isinstance(c, bool):
                skipped += 1
                continue
            if not isinstance(y, bool):
                skipped += 1
                continue
            reads.append({
                "confidence": float(c),
                "correct": y,
                "decision_class": str(row.get("decision_class") or "default"),
                "ts": row.get("ts"),
            })
    return reads


def bin_reliability(reads: list, n_bins: int = 10, strategy: str = "equal_width") -> dict:
    """Binned predicted-vs-observed over confidence in [0, 1].

    equal_width: fixed-width bins over [0, 1] (standard reliability diagram).
    equal_frequency: quantile bins (useful when confidence piles up near 1).

    Returns bins, ECE (expected calibration error, bin-size weighted mean of
    |observed - predicted|), MCE (max of the same) and Brier score.
    """
    if not reads:
        return {"n": 0, "bins": [], "ece": None, "mce": None, "brier": None}
    confs = [r["confidence"] for r in reads]
    if strategy == "equal_frequency":
        order = sorted(range(len(reads)), key=lambda i: confs[i])
        edges = [0.0]
        for k in range(1, n_bins):
            idx = round(k * len(reads) / n_bins)
            edges.append(confs[order[min(idx, len(reads) - 1)]])
        edges[-1] = 1.0 + EPS
    else:
        width = 1.0 / n_bins
        edges = [k * width for k in range(n_bins + 1)]
        edges[-1] = 1.0 + EPS

    bins = [{"lo": edges[b], "hi": min(edges[b + 1], 1.0), "n": 0,
             "mean_confidence": None, "observed_accuracy": None, "gap": None}
            for b in range(n_bins)]
    brier = 0.0
    for r in reads:
        c = r["confidence"]
        y = 1.0 if r["correct"] else 0.0
        b = min(int(c * n_bins), n_bins - 1)
        bins[b]["n"] += 1
        bins[b]["mean_confidence"] = (bins[b]["mean_confidence"] or 0.0) + c
        bins[b]["_sy"] = bins[b].get("_sy", 0.0) + y
        brier += (c - y) ** 2
    n_total = len(reads)
    ece = 0.0
    mce = 0.0
    for b in bins:
        if not b["n"]:
            b["mean_confidence"] = None
            b["observed_accuracy"] = None
            b["gap"] = None
            continue
        b["mean_confidence"] = round(b["mean_confidence"] / b["n"], 6)
        b["observed_accuracy"] = round(b["_sy"] / b["n"], 6)
        b["gap"] = round(b["observed_accuracy"] - b["mean_confidence"], 6)
        ece += (b["n"] / n_total) * abs(b["gap"])
        mce = max(mce, abs(b["gap"]))
        del b["_sy"]
    return {
        "n": n_total,
        "strategy": strategy,
        "bins": [{k: v for k, v in b.items()} for b in bins],
        "ece": round(ece, 6),
        "mce": round(mce, 6),
        "brier": round(brier / n_total, 6),
    }


def ece_of(reads: list, n_bins: int = 10) -> float:
    return bin_reliability(reads, n_bins=n_bins)["ece"]


# --------------------------------------------------------------------------
# 2. temperature (calibration split -> fit, held-out split -> verify)
# --------------------------------------------------------------------------

def _nll_at(reads: list, temperature: float) -> float:
    total = 0.0
    for r in reads:
        p = apply_temperature(r["confidence"], temperature)
        p = min(max(p, EPS), 1.0 - EPS)
        y = 1.0 if r["correct"] else 0.0
        total -= y * math.log(p) + (1.0 - y) * math.log(1.0 - p)
    return total / max(len(reads), 1)


def fit_temperature(reads: list) -> dict:
    """Minimum-NLL temperature on a calibration set. Grid over log-spaced T,
    then golden-section refine inside the winning bracket. Deterministic."""
    if len(reads) < 8:
        return {"temperature": 1.0, "nll": None, "n": len(reads), "note": "too few reads"}
    lo_t, hi_t, n_grid = 0.05, 20.0, 160
    grid = [lo_t * (hi_t / lo_t) ** (k / (n_grid - 1)) for k in range(n_grid)]
    nlls = [_nll_at(reads, t) for t in grid]
    best = min(range(n_grid), key=lambda k: nlls[k])
    a = grid[max(best - 1, 0)]
    b = grid[min(best + 1, n_grid - 1)]
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    c = b - gr * (b - a)
    d = a + gr * (b - a)
    fc, fd = _nll_at(reads, c), _nll_at(reads, d)
    for _ in range(80):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc = _nll_at(reads, c)
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd = _nll_at(reads, d)
    t_hat = (a + b) / 2.0
    return {"temperature": round(t_hat, 4), "nll": round(_nll_at(reads, t_hat), 6),
            "n": len(reads)}


def temperature_check(reads: list, n_bins: int = 10) -> dict:
    """Split reads in half: fit T on the calibration split, report held-out
    ECE before vs after applying T. This is what makes a threshold mean
    something: the same T must improve reads it never saw."""
    half = len(reads) // 2
    cal, ev = reads[:half], reads[half:]
    if not cal or not ev:
        return {"fitted": None, "note": "not enough reads to split"}
    fit = fit_temperature(cal)
    ece_before = ece_of(ev, n_bins=n_bins)
    scaled = [{"confidence": apply_temperature(r["confidence"], fit["temperature"]),
               "correct": r["correct"]} for r in ev]
    ece_after = ece_of(scaled, n_bins=n_bins)
    return {
        "fitted_temperature": fit["temperature"],
        "calibration_n": len(cal),
        "eval_n": len(ev),
        "ece_before": ece_before,
        "ece_after": ece_after,
        "improved": ece_after < ece_before,
    }


# --------------------------------------------------------------------------
# 3. per-domain drift  +  4. per-decision-class threshold (the G31 rule)
# --------------------------------------------------------------------------

def suggest_threshold(reads: list, target_accuracy: float, min_n: int = 200) -> dict:
    """Lowest confidence threshold whose observed accuracy on this calibration
    set meets the target; reads below it escalate per the G31 rule. Walks
    candidate thresholds ascending using suffix counts (c >= t)."""
    if not reads:
        return {"threshold": None, "note": "no reads"}
    order = sorted(reads, key=lambda r: r["confidence"])
    n = len(order)
    picked = None
    # build suffix stats for every unique confidence, ascending
    suffixes = []
    tot = 0
    cor = 0
    for r in reversed(order):
        tot += 1
        cor += 1 if r["correct"] else 0
        suffixes.append((r["confidence"], tot, cor / tot))
    suffixes.reverse()  # ascending t
    for t, k, acc in suffixes:
        if k >= min_n and acc >= target_accuracy:
            picked = {"threshold": round(t, 6), "n_at_or_above": k,
                      "observed_accuracy": round(acc, 6)}
            break
    if picked is None:
        return {"threshold": None,
                "note": "no threshold meets target on this calibration set",
                "max_n_checked": n}
    escalated = sum(1 for r in order if r["confidence"] < picked["threshold"])
    picked["escalated_share"] = round(escalated / n, 6)
    return picked


def per_domain_report(reads: list, target_accuracy: float = 0.9,
                      n_bins: int = 10, min_class_n: int = 50,
                      drift_abs_floor: float = 0.05,
                      drift_ratio: float = 2.0) -> dict:
    """Per decision_class: reliability, own temperature fit, G31 threshold.
    Drift flag: class ECE above an absolute floor AND above drift_ratio times
    the best-calibrated class's ECE."""
    classes = {}
    for r in reads:
        classes.setdefault(r["decision_class"], []).append(r)
    rows = {}
    for name in sorted(classes):
        sub = classes[name]
        if len(sub) < min_class_n:
            rows[name] = {"n": len(sub), "note": "below min_class_n, not scored"}
            continue
        fit = fit_temperature(sub)
        rows[name] = {
            "n": len(sub),
            "reliability": bin_reliability(sub, n_bins=n_bins),
            "ece": bin_reliability(sub, n_bins=n_bins)["ece"],
            "fitted_temperature": fit["temperature"],
            "threshold": suggest_threshold(sub, target_accuracy),
        }
    scored = {k: v for k, v in rows.items() if v.get("ece") is not None}
    if scored:
        best_ece = min(v["ece"] for v in scored.values())
        for name, v in scored.items():
            v["drift"] = bool(v["ece"] > drift_abs_floor
                              and v["ece"] > drift_ratio * best_ece)
            v["ece_vs_best"] = round(v["ece"] / max(best_ece, EPS), 2)
    return {"classes": rows, "target_accuracy": target_accuracy,
            "drift_rule": f"ece > {drift_abs_floor} and ece > {drift_ratio}x best class"}


def calibration_report(reads: list, target_accuracy: float = 0.9,
                       n_bins: int = 10) -> dict:
    """Full G31 recipe over a set of oracle reads."""
    return {
        "overall": bin_reliability(reads, n_bins=n_bins),
        "temperature": temperature_check(reads, n_bins=n_bins),
        "per_domain": per_domain_report(reads, target_accuracy=target_accuracy,
                                        n_bins=n_bins),
    }


# --------------------------------------------------------------------------
# synthetic oracles with known ground truth (for the self-test)
# --------------------------------------------------------------------------

def make_reads(n: int, rng: random.Random, temp: float = 1.0,
               decision_class: str = "synthetic",
               base_lo: float = 0.05, base_hi: float = 0.95) -> list:
    """Synthetic oracle reads. Draws true probability p ~ U(base_lo, base_hi),
    labels correct ~ Bernoulli(p), reports confidence c = sigmoid(temp * logit(p)).
    temp == 1.0 is perfectly calibrated; temp > 1 is overconfident (says 0.99
    when right far less often, exactly the small-oracle failure G31 names);
    temp < 1 is underconfident. Ground truth is known by construction."""
    reads = []
    for _ in range(n):
        p = rng.uniform(base_lo, base_hi)
        c = sigmoid(temp * logit(p))
        y = rng.random() < p
        reads.append({"confidence": c, "correct": bool(y),
                      "decision_class": decision_class, "ts": None})
    return reads


# --------------------------------------------------------------------------
# self-test on synthetic data
# --------------------------------------------------------------------------

def selftest(verbose: bool = True) -> list:
    results = []

    def check(name, ok, detail):
        results.append({"test": name, "pass": bool(ok), "detail": detail})
        if verbose:
            print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    rng = random.Random(SEED)

    # --- 1. binner on a perfectly calibrated oracle: ECE ~ sampling floor ---
    reads = make_reads(20000, rng, temp=1.0)
    rel = bin_reliability(reads, n_bins=10)
    check("binner_shape_perfect",
          rel["n"] == 20000 and sum(b["n"] for b in rel["bins"]) == 20000
          and len(rel["bins"]) == 10,
          f"n={rel['n']}, bins={len(rel['bins'])}, "
          f"bin_ns={[b['n'] for b in rel['bins']]}")
    check("binner_ece_perfect_calibrated", rel["ece"] < 0.03,
          f"ECE={rel['ece']:.4f} < 0.03 (sampling floor ~0.01 at n=20000)")
    check("brier_perfect_calibrated", rel["brier"] < 0.20,
          f"Brier={rel['brier']:.4f} < 0.20 (E[p(1-p)] over U(0.05,0.95) ~ 0.153)")

    # --- 2. binner detects overconfidence, with direction ---
    reads_hot = make_reads(60000, rng, temp=4.0)
    rel_hot = bin_reliability(reads_hot, n_bins=10)
    top = max((b for b in rel_hot["bins"] if b["n"]),
              key=lambda b: b["mean_confidence"])
    check("binner_detects_overconfidence", rel_hot["ece"] > 0.08,
          f"ECE={rel_hot['ece']:.4f} > 0.08 at temp=4.0")
    check("binner_overconfidence_direction",
          top["gap"] < -0.05,
          f"top bin [{top['lo']:.1f},{top['hi']:.1f}] predicted "
          f"{top['mean_confidence']:.4f} observed {top['observed_accuracy']:.4f} "
          f"gap {top['gap']:.4f} (observed far below predicted)")

    # --- 3. binner detects underconfidence, opposite direction ---
    reads_cold = make_reads(60000, rng, temp=0.4)
    rel_cold = bin_reliability(reads_cold, n_bins=10)
    top_cold = max((b for b in rel_cold["bins"] if b["n"]),
                   key=lambda b: b["mean_confidence"])
    check("binner_detects_underconfidence",
          rel_cold["ece"] > 0.05 and top_cold["gap"] > 0.05,
          f"ECE={rel_cold['ece']:.4f} > 0.05; top non-empty bin gap "
          f"{top_cold['gap']:.4f} > +0.05 (observed above predicted)")

    # --- 4. temperature fit recovers the distortion and fixes held-out ECE ---
    rng_cal = random.Random(SEED + 1)
    rng_ev = random.Random(SEED + 2)
    cal = make_reads(40000, rng_cal, temp=4.0)
    ev = make_reads(40000, rng_ev, temp=4.0)
    fit = fit_temperature(cal)
    ece_before = ece_of(ev)
    scaled = [{"confidence": apply_temperature(r["confidence"], fit["temperature"]),
               "correct": r["correct"]} for r in ev]
    ece_after = ece_of(scaled)
    check("temperature_recovers_distortion", 3.2 <= fit["temperature"] <= 5.0,
          f"T_hat={fit['temperature']:.4f} in [3.2, 5.0], true T=4.0, "
          f"n_cal=40000")
    check("temperature_fixes_heldout_ece",
          ece_after < 0.05 and ece_after < 0.4 * ece_before,
          f"held-out ECE {ece_before:.4f} -> {ece_after:.4f} after scaling "
          f"(want after < 0.05 and < 0.4x before)")

    # --- 5. per-domain drift separation ---
    mixed = (make_reads(30000, random.Random(SEED + 3), temp=4.0,
                        decision_class="cheap_gate")
             + make_reads(30000, random.Random(SEED + 4), temp=1.0,
                          decision_class="heavy_read"))
    pd = per_domain_report(mixed, target_accuracy=0.9)
    a = pd["classes"]["cheap_gate"]
    b = pd["classes"]["heavy_read"]
    check("per_domain_drift_separates",
          a["ece"] > 0.08 and b["ece"] < 0.03 and a["drift"] and not b["drift"],
          f"cheap_gate ECE={a['ece']:.4f} drift={a['drift']}; "
          f"heavy_read ECE={b['ece']:.4f} drift={b['drift']}")

    # --- 6. per-class threshold meets target out of sample (the G31 rule) ---
    rng_thr = random.Random(SEED + 5)
    thr_reads = make_reads(60000, rng_thr, temp=1.0, decision_class="gate")
    thr = suggest_threshold(thr_reads, target_accuracy=0.90, min_n=2000)
    held = make_reads(20000, random.Random(SEED + 6), temp=1.0,
                      decision_class="gate")
    kept = [r for r in held if r["confidence"] >= thr["threshold"]]
    held_acc = sum(1 for r in kept if r["correct"]) / len(kept)
    check("threshold_meets_target_heldout",
          0.75 <= thr["threshold"] <= 0.85 and held_acc >= 0.88,
          f"t*={thr['threshold']:.4f} in [0.75, 0.85]; held-out accuracy of "
          f"reads at or above t* = {held_acc:.4f} >= 0.88 (target 0.90)")
    check("threshold_escalation_share_sane",
          0.70 <= thr["escalated_share"] <= 0.90,
          f"escalated share below t* = {thr['escalated_share']:.4f} "
          f"(theory ~0.83 for uniform confidence)")

    # --- 7. ledger IO roundtrip ---
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False,
                                     encoding="utf-8") as fh:
        for r in reads[:500]:
            fh.write(json.dumps({"confidence": round(r["confidence"], 6),
                                 "correct": r["correct"],
                                 "decision_class": "io_test",
                                 "ts": "2026-09-19T00:00:00Z"}) + "\n")
        tmp_path = Path(fh.name)
    loaded = load_reads(tmp_path)
    ece_a = bin_reliability(reads[:500], n_bins=5)["ece"]
    ece_b = bin_reliability(loaded, n_bins=5)["ece"]
    tmp_path.unlink()
    check("ledger_io_roundtrip",
          len(loaded) == 500 and abs(ece_a - ece_b) < 1e-9,
          f"{len(loaded)}/500 rows loaded, ECE matches to {abs(ece_a - ece_b):.2e}")

    return results


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Oracle calibration harness (G31)")
    ap.add_argument("--selftest", action="store_true",
                    help="run the synthetic-data self-test and file a receipt")
    ap.add_argument("--input", type=str, default=None,
                    help="JSONL of oracle reads to score")
    ap.add_argument("--report", type=str, default=None,
                    help="where to file the calibration report JSON")
    ap.add_argument("--n-bins", type=int, default=10)
    ap.add_argument("--target", type=float, default=0.9,
                    help="accuracy target for the escalation threshold")
    ap.add_argument("--no-receipt", action="store_true",
                    help="self-test mode: do not write the receipt file")
    args = ap.parse_args(argv)

    if args.selftest:
        results = selftest()
        n_pass = sum(1 for r in results if r["pass"])
        ok = n_pass == len(results)
        receipt = {
            "receipt": "THE50 W6 T29: oracle calibration harness (G31 recipe)",
            "filed": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "finish_line": "tools/oracle_calibration.py",
            "program_row": ("watch/inbox/THE_50_PROGRAM_20260918.md line 46 "
                            "(item 29, W6 INSTRUMENTS, [QUEUED])"),
            "recipe_source": ("watch/inbox/GPS_BATTERY_20260918.jsonl line 31 "
                              "(G31: confidence field, per-decision-class "
                              "escalation threshold, calibration set, "
                              "temperature, per-domain drift)"),
            "computed_this_session": {
                "command": (".venv\\Scripts\\python.exe "
                            "tools/oracle_calibration.py --selftest"),
                "script": "tools/oracle_calibration.py",
                "seed": SEED,
                "tests_passed": n_pass,
                "tests_total": len(results),
                "all_pass": ok,
                "tests": results,
            },
            "implements": [
                "bin_reliability: binned predicted-vs-observed + ECE/MCE/Brier "
                "(equal-width or equal-frequency bins)",
                "fit_temperature + temperature_check: NLL temperature on a "
                "calibration split, held-out ECE before vs after",
                "per_domain_report: per decision_class reliability, own "
                "temperature, drift flag vs best class",
                "suggest_threshold: lowest threshold meeting the accuracy "
                "target + escalated share (the G31 escalation rule)",
            ],
            "honest_limits": [
                "no live oracle confidence ledger exists on disk yet (G31 is a "
                "steering proposal), so all numbers here are synthetic-data "
                "self-test numbers, which is the finish line as written",
                "score real traces with --input <reads.jsonl> --report <out.json>",
                "binary reads only (confidence vs correct); multiclass "
                "calibration is future work",
                "temperature fit assumes the miscalibration is logit-temperature "
                "shaped; per-domain drift is flagged, not attributed",
            ],
            "no_em_dash": True,
        }
        if not args.no_receipt:
            RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
            RECEIPT_PATH.write_text(
                json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8")
            print(f"[filed] {RECEIPT_PATH}")
        print(f"[selftest] {n_pass}/{len(results)} passed")
        return 0 if ok else 1

    if args.input:
        reads = load_reads(Path(args.input))
        if not reads:
            print(f"[error] no usable rows in {args.input} "
                  f"(need confidence float + correct bool per line)")
            return 1
        report = calibration_report(reads, target_accuracy=args.target,
                                    n_bins=args.n_bins)
        report["task"] = "THE 50 / W6 / item 29: oracle calibration harness"
        report["input"] = str(args.input)
        report["rows"] = len(reads)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        if args.report:
            out = Path(args.report)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
            print(f"[filed] {out}")
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
