"""B2-64 close: append LEDGER row + 3 self-feed briefs to QUEUE.md (max+1 at run time)."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
LEDGER = ROOT / "memory" / "burns" / "LEDGER.jsonl"
QUEUE = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"

ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

row = {
    "ts": ts,
    "slug": "B2-64-drift-dashboard",
    "verdict": "LANDED",
    "landing": "watch/inbox/burn_wave_20260926/B2_64_drift_dashboard_20260926.md",
    "one_line": (
        "Drift board T1-T6: spec filed first (docs/DRIFT_BOARD_SPEC.md) then "
        "tools/drift_dashboard.py renders "
        "dashboard/static/drift_board.html on the lab UI /static/ handler (zero "
        "server.py changes, LAW-060 fleetbar injects server-side); per pair: verdict "
        "history over weeks, current corr, live recomputed referent age, DRIFTING-days "
        "streak with start date; 4/6 DRIFTING, T1/T3 streak 7d, board caught a live "
        "referent event mid-lane (B2-65 revival appended 3 gates + 3 milestones "
        "13:35Z, T4/T5 ref age 51d/47d flipped to 0d); undated v1 rows displayed but "
        "never counted in day math; ratchet NEW except-pass debt fixed not registered "
        "(sig 59b703f590d8c52a); FRAGILE-ALIGNED styled per the concurrent aging "
        "guard; 5 new tests pass, full suite numbers in receipt"
    ),
}
with LEDGER.open("a", encoding="utf-8") as f:
    f.write(json.dumps(row, ensure_ascii=True) + "\n")
print("ledger row appended:", row["ts"])

text = QUEUE.read_text(encoding="utf-8")
nums = [int(n) for n in re.findall(r"B2-(\d+)", text)]
base = max(nums) + 1
briefs = [
    "- [ ] B2-{a} W40 drift stamp + board refresh: when the ISO week flips to W40 "
    "run tools/drift_pairs_stamp.py then tools/drift_dashboard.py --check, read the "
    "board row for T6 and decide B2-05's pre-registered falsifier (burn ledger rows "
    "on 3+ distinct days while T6 corr stays under 0.5 demotes the "
    "receipts-as-referent design); pointers docs/DRIFT_BOARD_SPEC.md section 5 + "
    "watch/inbox/burn_wave_20260926/B2_05_drift_pairs_20260926.md Falsifier.",

    "- [ ] B2-{b} Streak and staleness tripwire: the board computes DRIFTING-day "
    "streaks and live referent ages but nothing fires on them (T4's referent sat 51d "
    "stale with no alarm until the B2-65 revival: gates.jsonl was 16 rows ending "
    "2026-08-06 before the 13:35Z appends); add a --alarm mode to "
    "tools/drift_dashboard.py that files an inbox row when a streak crosses 14d or a "
    "referent age crosses 30d; pointers tools/drift_dashboard.py drifting_days + "
    "watch/inbox/burn_wave_20260926/B2_31_poll_tripwire_20260926.md.",

    "- [ ] B2-{c} Aging-guard board test: docs/DRIFT_BOARD_SPEC.md section 3 now "
    "defines FRAGILE-ALIGNED semantics (breaks a DRIFTING streak, never extends one, "
    "amber-green not gray) but no unit test exercises a W40 FRAGILE-ALIGNED stamp "
    "row through history_cell/drifting_days/_verdict_color; add the test with a "
    "synthetic v2 row so the B2-218 vocabulary-sweep falsifier is decidable for the "
    "board; pointers docs/DRIFT_BOARD_SPEC.md + tools/drift_pairs_stamp.py "
    "_apply_aging_guard.",
]
lines = [b.format(a=base, b=base + 1, c=base + 2) for b in briefs]

marker = "\n## Standing law note"
idx = text.find(marker)
if idx == -1:
    raise SystemExit("Open-section boundary not found; not appending")
new_text = text[:idx] + "\n" + "\n".join(lines) + "\n" + text[idx:]
QUEUE.write_text(new_text, encoding="utf-8")

check = QUEUE.read_text(encoding="utf-8")
for tag in (base, base + 1, base + 2):
    n = len(re.findall(rf"B2-{tag}\b", check))
    print(f"B2-{tag}: {n} occurrence(s) after append")
print("briefs appended:", base, base + 1, base + 2)
