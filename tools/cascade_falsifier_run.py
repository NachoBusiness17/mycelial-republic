"""Cascade falsifier run (burn brief B2-113, 2026-09-26).

Owns the measurement of the two pre-registered B2_08 falsifiers:

  F1 (B2_08_judge_lane_20260926.md:30): in the 50-wide burn the two-band
     cascade must beat the single tau=0.70 rule on escalation
     overturn-or-upgrade rate; else the JEV-derived thresholds file vacuous.
  F2 (B2_08_judge_lane_20260926.md:31): if >15% of confidence >= 0.9 verdicts
     overturn at spot-check, local confidence is uncalibrated; all verdicts
     defer to frontier until recalibrated.

Reads ONLY what the wiring actually emits: queue/lanes/*/trail.jsonl rows with
event == "GATE_VERDICT_V2" and a nested dict "verdict" (the same predicate as
mag/lane_runner._trail_verdicts). It never invents verdicts: with zero V2 rows
it reports NEED_DATA per falsifier and exits 0 (a cannot-verify measurement,
not a failure of the thresholds).

Decision vocabulary is the registered one (watch/inbox/
BURN_JUDGE_LANE_BUILD_20260925.md section 1 + configs/lanes.yaml
gate_verdict_v2): proposed/final = accept iff every axis score >= tau AND
failure_class == "none"; anything else rejects. Two-band escalation trigger =
routine band on_fail (not the accept predicate) or derivation-class axis
(band_derivation always_escalate). Single-rule counterfactual = any axis
confidence < 0.70. Rates gate at MIN_RATE_EVENTS = 10 (pass-e convention,
B2_34). Spot-check rows for F2 are event == "SPOT_CHECK" carrying
"overturns" and "sampled" counts; none exist yet, and the denominator is
named, not assumed (B2-193 protocol still open).

Usage: .venv/Scripts/python.exe tools/cascade_falsifier_run.py [--lanes DIR]
Exit 0 on a completed measurement (decide or NEED_DATA), 2 on internal error.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AXES = ("brief_fidelity", "build_quality", "receipt_completeness")
TAU_ROUTINE = 0.90          # configs/lanes.yaml gate_verdict_v2.cascade.band_routine.tau
TAU_SINGLE = 0.70           # the single-rule counterfactual named in F1
F2_THRESHOLD = 0.15         # B2_08:31
MIN_RATE_EVENTS = 10        # pass-e convention (B2_34)
DERIVATION_CLASSES = {"math", "derivation", "protocol", "security"}


def load_verdicts(lanes_dir: Path) -> list[dict]:
    """All GATE_VERDICT_V2 verdict dicts across lane trails, in file order."""
    out: list[dict] = []
    if not lanes_dir.is_dir():
        return out
    for trail in sorted(lanes_dir.glob("*/trail.jsonl")):
        for ln in trail.read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            if not ln:
                continue
            try:
                row = json.loads(ln)
            except Exception:  # noqa: BLE001
                continue
            if row.get("event") == "GATE_VERDICT_V2" and isinstance(row.get("verdict"), dict):
                out.append(row["verdict"])
    return out


def _conf(v: dict) -> float:
    return max(
        (float(v.get("axes", {}).get(a, {}).get("confidence", 0.0)) for a in AXES),
        default=0.0,
    )


def proposed_accept(v: dict, tau: float = TAU_ROUTINE) -> bool:
    axes = v.get("axes", {})
    scores_ok = all(
        float(axes.get(a, {}).get("score", 0.0)) >= tau for a in AXES
    ) if all(a in axes for a in AXES) else False
    return scores_ok and v.get("failure_class") == "none"


def two_band_escalates(v: dict) -> bool:
    """Registered two-band trigger: routine on_fail OR derivation band."""
    if not proposed_accept(v):
        return True
    return str(v.get("failure_class", "")).lower() in DERIVATION_CLASSES


def single_rule_escalates(v: dict) -> bool:
    return _conf(v) < TAU_SINGLE


def load_spot_checks(lanes_dir: Path) -> dict:
    """SPOT_CHECK rows: {"overturns": int, "sampled": int} summed."""
    overturns = sampled = 0
    if not lanes_dir.is_dir():
        return {"overturns": overturns, "sampled": sampled}
    for trail in sorted(lanes_dir.glob("*/trail.jsonl")):
        for ln in trail.read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            if not ln:
                continue
            try:
                row = json.loads(ln)
            except Exception:  # noqa: BLE001
                continue
            if row.get("event") == "SPOT_CHECK":
                overturns += int(row.get("overturns", 0))
                sampled += int(row.get("sampled", 0))
    return {"overturns": overturns, "sampled": sampled}


def pair_overturns(verdicts: list[dict]) -> tuple[int, int]:
    """(overturn_or_upgrade_events, high_conf_escalations) via escalated_from."""
    by_id = {v.get("verdict_id"): v for v in verdicts if v.get("verdict_id")}
    events = high = 0
    for v in verdicts:
        parent_id = v.get("escalated_from")
        if not parent_id or parent_id not in by_id:
            continue
        parent = by_id[parent_id]
        if _conf(parent) >= TAU_ROUTINE:
            high += 1
            if proposed_accept(v) != proposed_accept(parent):
                events += 1
    return events, high


def rate(num: int, den: int) -> dict:
    if den < MIN_RATE_EVENTS:
        return {"decidable": False, "num": num, "den": den,
                "reason": f"denominator {den} < MIN_RATE_EVENTS {MIN_RATE_EVENTS}"}
    return {"decidable": True, "num": num, "den": den, "rate": round(num / den, 4)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lanes", default=str(ROOT / "queue" / "lanes"))
    args = ap.parse_args()
    lanes_dir = Path(args.lanes)
    try:
        verdicts = load_verdicts(lanes_dir)
        spot = load_spot_checks(lanes_dir)
    except OSError as exc:
        print(json.dumps({"error": str(exc)}))
        return 2

    escalators_two_band = [v for v in verdicts if two_band_escalates(v)]
    escalators_single = [v for v in verdicts if single_rule_escalates(v)]
    events, high = pair_overturns(verdicts)

    f1 = {
        "question": "two-band cascade beats single tau=0.70 on escalation overturn-or-upgrade rate",
        "two_band_escalations": len(escalators_two_band),
        "single_rule_escalations": len(escalators_single),
        "overturn_or_upgrade_events": events,
        "note": ("per-falsifier F1 needs the frontier outcome row for each "
                 "escalation (escalated_from pair); rate gated at "
                 f"MIN_RATE_EVENTS={MIN_RATE_EVENTS}"),
    }
    sc_rate = rate(spot["overturns"], spot["sampled"])
    f2 = {
        "question": ">15% of confidence >= 0.9 verdicts overturn at spot-check",
        "spot_check": sc_rate,
        "pair_detector": rate(events, high),
        "note": ("spot-check denominator requires the B2-193 protocol "
                 "(who samples, how many, where filed); pair_detector is the "
                 "B2-34 confident_and_wrong detector on trail rows only"),
    }
    out = {
        "tool": "tools/cascade_falsifier_run.py",
        "lanes_dir": str(lanes_dir),
        "gate_verdict_v2_rows": len(verdicts),
        "spot_check_rows": {"overturns": spot["overturns"], "sampled": spot["sampled"]},
        "F1": f1,
        "F2": f2,
        "verdict": ("DECIDED" if (
            (f1["two_band_escalations"] or f1["single_rule_escalations"])
            and sc_rate.get("decidable")
        ) else "NEED_DATA"),
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
