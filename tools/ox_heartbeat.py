"""ox_heartbeat — one-shot ox-alpha availability probe (Mag Estate lane A5, "ox heartbeat re-arm").

Cron-able wrapper around mag/ox_availability.py's OWN probe logic: runs ONE tiny heartbeat
(the module's _heartbeat(): pins account 1's OpenRouter key, pings ox-alpha via ox_seat.chat
with max_tokens=8 — a heartbeat, not real work) and appends ONE compact JSON row
{"ok": ..., "http": ..., "ts": ...} to memory/runs/ox_availability/heartbeats.jsonl
(the module's own LEDGER; dirs auto-created; append-only, one line per run).

Why _heartbeat(0) and not ping(account=1): the module's ping() folds its own full-schema row
to the ledger (ox_availability.py lines 103-105); calling it here would append TWO rows per
run. _heartbeat() is the probe itself, so this tool owns the append exactly once, in the
minimal {ok, http, ts} shape ask A5 specifies.

Always exits 0: a failed probe is still a successful heartbeat run (the row records the
failure); the scheduler must never see a crash from this tool.

TODO(alerting): if the last N rows of the ledger are all {"ok": false}, raise an operator
alert (N and channel TBD). Intentionally a comment only for now — per ask A5.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # project root; tools/ is its child
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag import ox_availability as ox_av  # noqa: E402  (module's own logic, own LEDGER)


def main() -> int:
    # ONE probe, the module's own logic (mag/ox_availability.py::_heartbeat, account 1).
    try:
        r = ox_av._heartbeat(0)
    except Exception as e:  # noqa: BLE001 — a crashed probe is still a recorded failure
        r = {"ok": False, "http": None, "error": str(e)[:160], "ts": ox_av._now()}

    row = {
        "ok": bool(r.get("ok")),
        "http": r.get("http"),
        "ts": r.get("ts") or ox_av._now(),
    }
    ledger = ox_av.LEDGER  # ROOT / "memory" / "runs" / "ox_availability" / "heartbeats.jsonl"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as f:  # append-only, same fold as the module
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps(row, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
