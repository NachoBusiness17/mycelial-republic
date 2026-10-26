"""B2-217 probe: verify the guard-bearing W40 stamp without writing repo bytes.

Read-only on real state; the W40 rehearsal runs against a throwaway ledger +
receipt copy in a temp dir (stamp is keyed on the passed date, not wall clock;
the real append-only ledger is never touched). Evidence law: bytes over talk.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import tools.drift_pairs_stamp as m  # noqa: E402
from tools.drift import drift_check  # noqa: E402

LEDGER = ROOT / "memory" / "runs" / "adv_arc_50" / "teleo_drift_stamps.jsonl"
RECEIPT = ROOT / "watch" / "inbox" / "THE50_W6_T26_DRIFT_STAMP.receipt.json"
BURNS = ROOT / "memory" / "burns" / "LEDGER.jsonl"

out: dict = {"probe": "B2_217_w40_verify", "when": "2026-09-26"}


def sha1(p: Path) -> str:
    return hashlib.sha1(p.read_bytes()).hexdigest()


# 1. integrity anchors before
out["sha_before"] = {"ledger": sha1(LEDGER), "receipt": sha1(RECEIPT)}

# 2. real ledger census
rows = [json.loads(l) for l in LEDGER.read_text(encoding="utf-8").splitlines() if l.strip()]
v2 = [r for r in rows if r.get("schema") == "teleo_drift_stamp.v2"]
w40 = [r for r in v2 if r.get("week_key") == "2026-W40"]
w39 = [r for r in v2 if r.get("week_key") == "2026-W39"]
out["ledger"] = {
    "total_rows": len(rows),
    "v2_rows": len(v2),
    "w40_rows": len(w40),
    "w39_rows": len(w39),
    "w39_rows_missing_guard_fields": [
        r.get("pair_id") for r in w39
        if not all(r.get(k) is not None for k in
                   ("referent_age_days", "referent_first_date", "referent_last_date", "verdict_guard"))
    ],
}
t6w39 = [r for r in w39 if r.get("pair_id") == "T6"]
out["w39_t6"] = {
    "verdict": t6w39[0]["verdict"].get("verdict"),
    "corr": t6w39[0]["verdict"].get("corr_dm_dr"),
    "stamped_at": t6w39[0].get("stamped_at"),
} if t6w39 else None

# 3. W40 rehearsal against a throwaway ledger + receipt (real files untouched)
tmp = Path(tempfile.mkdtemp(prefix="b2_217_"))
saved_ledger, saved_receipt = m.LEDGER, m.RECEIPT
try:
    m.LEDGER = tmp / "teleo_drift_stamps.jsonl"
    m.RECEIPT = tmp / "receipt.json"
    res = m.stamp(today=date(2026, 9, 28))  # W40 Monday rehearsal
    rehearsal = []
    guard_regressions = []
    required = ("referent_age_days", "referent_first_date", "referent_last_date", "verdict_guard")
    for r in res["results"]:
        v = r["verdict"]
        g = r.get("verdict_guard") or {}
        row = {
            "pair_id": r["pair_id"],
            "verdict": v.get("verdict"),
            "corr": v.get("corr_dm_dr"),
            "deltas": v.get("deltas_used"),
            "referent_age_days": r.get("referent_age_days"),
            "referent_first_date": r.get("referent_first_date"),
            "referent_last_date": r.get("referent_last_date"),
            "guard_threshold": g.get("threshold_days"),
            "guard_original": g.get("original_verdict"),
            "guard_downgraded": g.get("downgraded"),
        }
        missing = [k for k in required if r.get(k) is None]
        if missing:
            guard_regressions.append({"pair_id": r["pair_id"], "missing_fields": missing})
        if v.get("verdict") == "ALIGNED" and (r.get("referent_age_days") or 0) < 7:
            guard_regressions.append({"pair_id": r["pair_id"], "aligned_below_threshold": True})
        rehearsal.append(row)
    out["w40_rehearsal"] = {
        "note": ("throwaway-copy rehearsal at today=2026-09-28 (W40 Monday); the real "
                 "ledger holds zero W40 rows because 2026-09-26 is ISO W39 and the "
                 "stamp is keyed to the run date's ISO week"),
        "rows": rehearsal,
        "guard_regressions": guard_regressions,
        "appended": res["added"],
    }
    out["staleness_tripwire_in_rehearsal"] = res.get("staleness_tripwire")
finally:
    m.LEDGER, m.RECEIPT = saved_ledger, saved_receipt
    shutil.rmtree(tmp, ignore_errors=True)

# 4. live T6 probe on real bytes (the exact build+check path the W40 stamp uses)
built = m.PAIRS["T6"]["build"]()
t6 = drift_check(built["metric"], built["referent"], label="B2-217 live T6 probe")
out["live_t6"] = {
    "verdict": t6.get("verdict"),
    "corr": t6.get("corr_dm_dr"),
    "deltas_used": t6.get("deltas_used"),
    "window_start": built["span"][0].isoformat(),
    "window_end": built["span"][-1].isoformat(),
    "referent_first": built["referent_first"].isoformat() if built["referent_first"] else None,
    "referent_last": built["referent_last"].isoformat() if built["referent_last"] else None,
    "metric_total": sum(built["metric"]),
    "referent_total": sum(built["referent"]),
}

# 5. burn ledger census (the wave flooding T6's referent)
brows = [json.loads(l) for l in BURNS.read_text(encoding="utf-8").splitlines() if l.strip()]
days = Counter(r.get("ts", "")[:10] for r in brows if r.get("ts"))
out["burn_census"] = {"rows": len(brows), "distinct_days": dict(sorted(days.items()))}

# 6. integrity anchors after: prove no write
out["sha_after"] = {"ledger": sha1(LEDGER), "receipt": sha1(RECEIPT)}
out["unchanged"] = out["sha_before"] == out["sha_after"]

dest = Path(__file__).with_name("B2_217_verify_results.json")
dest.write_text(json.dumps(out, indent=1, ensure_ascii=True), encoding="utf-8")
print(json.dumps(out, indent=1, ensure_ascii=True))
print("results:", dest)
