"""B2-467 grep matrix over the fresh Mr Pool rows (2026-09-26).

Runs the in-window (2026-09-21T00:00Z..2026-09-23T00:05Z) HIT-class keyword
sweep and the Oct-3-referent sweep over ledger_delta_preview_20260926.jsonl,
per B2-166 Falsifier 2 and the rubric's pre-registered OCT 3 check. Prints
every match with row id, date, pattern, and a bounded snippet. No summary
without the matching bytes.
"""
import json
import re
from pathlib import Path

DELTA = Path(__file__).resolve().parents[1] / "mrpool_export" / "ledger_delta_preview_20260926.jsonl"

W0, W1 = "2026-09-21T00:00:00", "2026-09-23T00:05:00"

HIT_PATTERNS = {
    "blackout": r"black\s?out",
    "ebs": r"\bebs\b",
    "emergency_alert": r"emergency\s+(alert|broadcast|warning)",
    "eas_ipaws": r"\b(eas|ipaws)\b",
    "moex": r"\bmoex\b",
    "circuit_breaker": r"circuit\s?breaker",
    "xrp": r"\bxrp\b",
    "g20": r"\bg20\b",
    "this_is_it": r"this is it",
    "stay_tuned": r"stay\s+tuned",
    "satellite_truck": r"satellite\s+truck",
}
OCT3_PATTERNS = {
    "oct_3": r"oct\.?\s*3\b",
    "october_3": r"october\s+3\b",
    "slash_103": r"\b10/3\b",
    "3_oct": r"3\s+oct",
    "oct3_tight": r"oct3\b",
    "coffee": r"\bcoffee\b",
}


def main():
    rows = [json.loads(l) for l in open(DELTA, encoding="utf-8")]
    win = [r for r in rows if W0 <= r["date"] <= W1]
    print(f"rows={len(rows)} in_window={len(win)} ids={[r['msg_id'] for r in win]}")
    print()

    for name, pats in (("IN-WINDOW HIT sweep", HIT_PATTERNS), ("OCT 3 referent sweep (all 30 fresh rows)", OCT3_PATTERNS)):
        print(f"======== {name} ========")
        total = 0
        for r in rows:
            if name.startswith("IN-WINDOW") and r["date"] not in [w["date"] for w in win]:
                continue
            text = r["text"]
            for label, pat in pats.items():
                for m in re.finditer(pat, text, re.I):
                    total += 1
                    s = max(0, m.start() - 45)
                    e = min(len(text), m.end() + 45)
                    print(f"  msg {r['msg_id']} {r['date']} [{label}]: ...{text[s:e]}...")
        if total == 0:
            print("  0 matches")
        print()


if __name__ == "__main__":
    main()
