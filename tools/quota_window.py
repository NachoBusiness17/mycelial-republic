"""quota_window - calculate the Gemini Pro 5-hour rolling windows.

The quota doctrine's calculator: each Pro account carries its own rolling
5-hour window; N accounts staggered tile the day instead of colliding.
Records a Pro-lane ask and reports headroom per account.

Usage:
  python tools/quota_window.py --account sf --record
  python tools/quota_window.py --account nacho --record --ask-class dossier
  python tools/quota_window.py --check            # headroom table, all accounts
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state" / "quota_windows.json"
WINDOW_HOURS = 5
DEFAULT_BUDGET = 12  # asks per account per rolling window before defer


def _load() -> dict:
    if STATE.is_file():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"accounts": {}}


def _save(d: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(d, indent=1) + "\n", encoding="utf-8")


def _iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _in_window(ts: str) -> bool:
    t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return datetime.now(timezone.utc) - t <= timedelta(hours=WINDOW_HOURS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--account", default="sf")
    ap.add_argument("--ask-class", default="general")
    ap.add_argument("--record", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--budget", type=int, default=DEFAULT_BUDGET)
    args = ap.parse_args()

    d = _load()
    acc = d["accounts"].setdefault(args.account, {"asks": []})

    if args.record:
        acc["asks"].append({"ts": _iso(), "class": args.ask_class})
        acc["asks"] = acc["asks"][-200:]
        _save(d)
        used = sum(1 for a in acc["asks"] if _in_window(a["ts"]))
        print(f"recorded {args.account} {args.ask_class}: {used} in window")
        return 0

    if args.check:
        print(f"{'account':8} {'in-window':>9} {'budget':>6}  verdict")
        for name, a in sorted(d["accounts"].items()):
            used = sum(1 for x in a.get("asks", []) if _in_window(x.get("ts", "")))
            verdict = "DEFER" if used >= args.budget else "OK"
            print(f"{name:8} {used:>9} {args.budget:>6}  {verdict}")
        return 0

    # default: record + report for one account
    used = sum(1 for x in acc.get("asks", []) if _in_window(x.get("ts", "")))
    verdict = "DEFER" if used >= args.budget else "OK"
    print(f"{args.account}: {used} in window, verdict {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
