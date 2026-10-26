"""W4-02: retrodictive Brier demonstration for the sovereign mirror.

The three operator corrections of the 09-27/28 night (verbatim at
memory/rib/RIB_DRIVING_LADDER_20260928.md:3-5) are treated as three
resolved binary forecast events:

  Event = "the operator endorses the pre-correction seat policy"
          (P1: free lanes usable as work; P2: run-first over
           remember-first; P3: re-deriving rib-held doctrine is fine).
  The pre-correction seat acted at implicit confidence ~1.0 (it ran the
  policy as if it were law). y = 0 for all three (operator corrected).

The implicit-confidence parameter is an ASSUMPTION, swept below.
Coin-flip baseline: constant p=0.5 scores 0.25 expected Brier.
Rail effect: once a corrected preference compiles to a gate, that
decision class leaves the statistical set; its future Brier
contribution is 0 by construction (checked, not forecast).

Stdlib only. No em-dashes.
"""
import json
import math

# --- 1. retrodictive Brier on the three corrections -------------------
terms = {}
for conf in (0.90, 0.95, 1.00):
    t = [(0.0 - conf) ** 2] * 3
    terms[f"conf={conf:.2f}"] = {"per_event": [round(x, 4) for x in t],
                                 "mean_brier": round(sum(t) / 3, 4)}
base = {"constant_p0.5_baseline": 0.25,
        "perfect_forecaster": 0.0,
        "always_wrong_at_conf": 1.0}

# sample sd of the conf=0.95 terms (illustrative only, n=3)
t95 = [(0.0 - 0.95) ** 2] * 3
mean95 = sum(t95) / 3
var95 = sum((x - mean95) ** 2 for x in t95) / 3  # population var, n=3
sd95 = math.sqrt(var95)

# --- 2. power: N needed for a 95% CI half-width of 0.05 ---------------
# Brier-term sd ranges 0.0-1.0; typical near sd=0.4 (p near 0.8 resolved
# against you) to 0.5. Use 0.4 and 0.5 as stated assumptions.
power = {}
for sd in (0.4, 0.5):
    n = (1.96 * sd / 0.05) ** 2
    power[f"sd={sd}"] = {"n_for_pm0.05": round(n), "halfwidth_at_n8": round(1.96 * sd / math.sqrt(8), 3),
                         "halfwidth_at_n100": round(1.96 * sd / math.sqrt(100), 3)}

# --- 3. live denominator drift check (B2-216 instance) ----------------
import subprocess
import sys

def count_lines(path):
    with open(path, "rb") as fh:
        return sum(1 for _ in fh)

dl = count_lines("memory/decisions_log.jsonl")
be = count_lines("logs/behavioral_events.jsonl")
drift = {"decisions_log_this_session": dl, "decisions_log_w3_lane": 213259,
         "delta_rows_between_moments": dl - 213259,
         "behavioral_events_this_session": be, "behavioral_events_w3_lane": 215576,
         "delta_rows_between_moments_be": be - 215576}

out = {"correction_events_brier": terms, "baselines": base,
       "sd_of_terms_conf095": round(sd95, 4), "power": power,
       "denominator_drift": drift}
print(json.dumps(out, indent=1))

from pathlib import Path as _P
_out_path = _P(__file__).resolve().parent / "_w4_02_brier_out.json"
with _out_path.open("w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
