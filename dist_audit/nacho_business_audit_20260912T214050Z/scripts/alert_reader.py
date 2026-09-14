"""alert_reader — the SEEN state for signature-pressure alarms (Build 3.5, item 1).

Chair 3's finding (2026-09-11 salon): the signature-pressure alarm had FIRED with
zero consumers — "alerted: true is the last word forever." This reader converts
FIRED -> SEEN: reads logs/failure_kb_alerts.jsonl, marks consumed rows in
state/failure_kb_alerts.read.json, and surfaces each unread alert as a behavioral
event + stdout line so doctor/morning-report/inbox surfaces pick it up.

Usage:
  python scripts/alert_reader.py            # consume + surface unread alerts
  python scripts/alert_reader.py --list     # show unread without consuming
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALERTS = ROOT / "logs" / "failure_kb_alerts.jsonl"
READ_STATE = ROOT / "state" / "failure_kb_alerts_read.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_rows() -> list[dict]:
    if not ALERTS.is_file():
        return []
    rows = []
    for ln in ALERTS.read_text(encoding="utf-8", errors="replace").splitlines():
        if ln.strip():
            try:
                rows.append(json.loads(ln))
            except Exception:
                continue
    return rows


def main() -> None:
    consume = "--list" not in sys.argv
    rows = load_rows()
    try:
        seen: dict[str, str] = json.loads(READ_STATE.read_text(encoding="utf-8"))
    except Exception:
        seen = {}
    # a row is identified by ts+sig (ts is unique per alert write)
    unread = [r for r in rows if f"{r.get('ts')}|{r.get('sig')}" not in seen]
    if not unread:
        print("alert_reader: 0 unread signature-pressure alerts")
        return
    for r in unread:
        key = f"{r.get('ts')}|{r.get('sig')}"
        print(f"ALERT SEEN: {r.get('sig')} x{r.get('count')} first-fired {r.get('ts')} — {r.get('sample', '')[:80]}")
        try:
            from mag.operator_inbox import log_behavioral_event

            log_behavioral_event(
                kind="signature_pressure_seen",
                detail=f"{r.get('sig')} x{r.get('count')} — {r.get('sample', '')[:120]}",
                tool=r.get("tool"),
                phase="ack_reaper",
            )
        except Exception:
            pass
        seen[key] = _now()
    if consume:
        READ_STATE.parent.mkdir(parents=True, exist_ok=True)
        READ_STATE.write_text(json.dumps(seen, indent=1), encoding="utf-8")
        print(f"alert_reader: {len(unread)} alert(s) marked SEEN at {_now()}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
