"""fold_v2_covariance.py — the covariance fold, applied to the fleet.

From "Reinforcement learning as nonequilibrium Monte Carlo" (Charles H. Martin,
2026-09-22 drop): the response coefficient is a covariance — the direction of
learning is computed from how scored fluctuations move together, not from
majority vote. fold v1 (quorum: keep what survives) becomes fold v2 (weight by
movement): per organ, the change in Gamma between the last two smith-chart
readings IS the fleet's learning direction — healing (Gamma falling), rotting
(Gamma rising), or flat.

Run:  .venv/Scripts/python.exe tools/fold_v2_covariance.py
Out:  watch/inbox/FOLD_V2_DIRECTIONS_<date>.json + .md
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "watch" / "inbox"


def load_readings():
    files = sorted(INBOX.glob("ESTATE_SMITH_CHART_*.json"))
    readings = []
    for f in files:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        ts = d.get("ts") or f.stem
        organs = d.get("organs") or d.get("gamma") or {}
        if isinstance(organs, dict):
            readings.append((ts, {k: float(v.get("gamma", v) if isinstance(v, dict) else v)
                                  for k, v in organs.items() if isinstance(v, (int, float, dict))}))
        elif isinstance(organs, list):
            readings.append((ts, {o.get("name"): float(o.get("gamma"))
                                  for o in organs if o.get("gamma") is not None}))
    return readings


def main() -> int:
    readings = load_readings()
    if len(readings) < 2:
        print("need >=2 smith chart readings for a direction fold; have", len(readings))
        return 1
    (ts0, g0), (ts1, g1) = readings[-2], readings[-1]
    organs = sorted(set(g0) | set(g1))
    rows = []
    for o in organs:
        a, b = g0.get(o), g1.get(o)
        if a is None or b is None:
            rows.append({"organ": o, "d_gamma": None, "direction": "DARK"})
            continue
        d = round(b - a, 3)
        direction = ("healing" if d < -0.02 else
                     "rotting" if d > 0.02 else "flat")
        rows.append({"organ": o, "gamma_prev": a, "gamma_now": b,
                     "d_gamma": d, "direction": direction})
    healing = [r for r in rows if r.get("direction") == "healing"]
    rotting = [r for r in rows if r.get("direction") == "rotting"]
    flat = [r for r in rows if r.get("direction") == "flat"]
    dark = [r for r in rows if r.get("direction") == "DARK"]

    out = {
        "schema": "fold_v2.directions.v1",
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "window": {"prev": ts0, "now": ts1},
        "method": "fold v2 covariance directions: d_gamma per organ between the last two meter readings (Martin 2026: response = covariance; a falling Gamma is the fleet healing, a rising one is rot)",
        "organs": rows,
        "summary": {
            "healing": [r["organ"] for r in healing],
            "rotting": [r["organ"] for r in rotting],
            "flat": [r["organ"] for r in flat],
            "dark": [r["organ"] for r in dark],
        },
    }
    outp = INBOX / ("FOLD_V2_DIRECTIONS_" + datetime.now(timezone.utc).strftime("%Y%m%d") + ".json")
    outp.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")

    md = ["# FOLD V2 — fleet learning directions (covariance fold)",
          "",
          f"Window: `{ts0}` → `{ts1}` · method: d-Γ per organ (Martin: response = covariance).",
          "",
          "## Healing (Γ falling = fixes landing)",
          "\n".join(f"- **{r['organ']}** {r.get('gamma_prev')} → {r.get('gamma_now')}" for r in healing) or "- (none)",
          "",
          "## Rotting (Γ rising = rot)",
          "\n".join(f"- **{r['organ']}** {r.get('gamma_prev')} → {r.get('gamma_now')}" for r in rotting) or "- (none)",
          "",
          "## Flat / dark",
          "\n".join(f"- {r['organ']} (flat)" for r in flat) or "- (none)",
          "\n".join(f"- {r['organ']} (DARK)" for r in dark),
          ""]
    outp.with_suffix(".md").write_text("\n".join(md), encoding="utf-8")
    print("fold v2 written:", outp.name)
    print("healing:", [r["organ"] for r in healing])
    print("rotting:", [r["organ"] for r in rotting])
    return 0


if __name__ == "__main__":
    sys.exit(main())
