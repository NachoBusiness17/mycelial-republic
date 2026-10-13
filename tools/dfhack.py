"""DFHACK — the live colony overlay. Self-steal of the DFHack pattern.

The estate is a dwarf fortress: a colony of lanes, waves, seats and organs that
works in the dark. DFHack was the overlay that made the fortress watchable while
it ran. This is that, for us: one refreshing view over everything currently
running — waves, sessions, queue, meters, watch ledgers — plus the intervention
verbs the colony needs.

Usage:
  .venv/Scripts/python.exe tools/dfhack.py            # live overlay, 2s refresh (Ctrl+C to exit)
  .venv/Scripts/python.exe tools/dfhack.py --once     # single frame (for pipes/CI)
  .venv/Scripts/python.exe tools/dfhack.py --once --wide  # single frame, wider context

$0 · stdlib only · read-only by design — the overlay never touches the colony.
"""
import argparse
import http.client
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "watch" / "inbox"
CLEAR = "\033[2J\033[H" if sys.stdout.isatty() else ""


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def tail(path: Path, n: int = 6) -> list[str]:
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").strip().splitlines()
        return lines[-n:]
    except OSError:
        return []


def fullsend_state() -> list[str]:
    logs = sorted((ROOT / ".." / ".zcode" / "cli" / "exec").glob("*/call_*.log")) if False else []
    rows = []
    for f in sorted((INBOX / "fullsend_s2").glob("wave_*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            ok = sum(1 for r in d if r.get("status") == "ok" and r.get("chars", 0) > 200)
            rows.append(f"  wave file {f.name}: {ok}/{len(d)} substantial")
        except Exception:
            pass
    fin = INBOX / "fullsend_s2" / "FULLSEND_S2_final.json"
    if fin.exists():
        try:
            d = json.loads(fin.read_text(encoding="utf-8"))
            rows.append(f"  FINAL: {d['substantial']}/{d['lanes_run']} substantial ({d['ts'][:19]}Z)")
        except Exception:
            pass
    return rows or ["  (no fullsend receipts yet)"]


def serve_sessions() -> list[str]:
    try:
        conn = http.client.HTTPConnection("127.0.0.1", 4096, timeout=4)
        conn.request("GET", "/session")
        d = json.loads(conn.getresponse().read().decode("utf-8"))
        conn.close()
        rows = d if isinstance(d, list) else d.get("data", [])
        return [f"  {len(rows)} sessions alive · last: {(rows[-1].get('title') or '?')[:50] if rows else '-'}"]
    except Exception:
        return ["  serve :4096 down"]


def queue_state() -> list[str]:
    try:
        sys.path.insert(0, str(ROOT))
        from mag.orchestrator import list_queue

        q = list_queue(limit=500)
        c = {}
        for x in q:
            c[x.get("status")] = c.get(x.get("status"), 0) + 1
        return ["  " + " · ".join(f"{k}={v}" for k, v in sorted(c.items()))]
    except Exception as e:
        return ["  queue read failed: " + str(e)[:60]]


def meters_headline() -> list[str]:
    charts = sorted(INBOX.glob("ESTATE_SMITH_CHART_*.json"))
    if not charts:
        return ["  meters DARK (no smith chart)"]
    try:
        d = json.loads(charts[-1].read_text(encoding="utf-8"))
        organs = d.get("organs") or {}
        bar = d.get("bar", 0.5)
        np = d.get("no_prose_list") or d.get("no_prose") or []
        line = " · ".join(f"{k}={round(float((v or {}).get('gamma', 9)), 2)}" for k, v in list(organs.items())[:8])
        return [f"  Γ: {line}", f"  no-prose ({len(np)}): {', '.join(np) if np else 'none'}"]
    except Exception as e:
        return ["  meters read failed: " + str(e)[:60]]


def mimo_state() -> list[str]:
    rows = tail(INBOX / "mimo_watch.jsonl", 1)
    if not rows:
        return ["  mimo: no rows"]
    try:
        d = json.loads(rows[0])
        return [f"  mimo window: {d.get('hours_left')}h left · key {d.get('key')} · probe {d.get('probe')}"]
    except Exception:
        return ["  mimo: unreadable row"]


def frame() -> str:
    L = []
    L.append(f"╔═ DFHACK — the colony, live · {now()}Z " + "═" * 20)
    L.append("║ WAVES (fullsend S2)")
    L.extend("║" + r for r in fullsend_state())
    L.append("║ SERVE (opencode :4096)")
    L.extend("║" + r for r in serve_sessions())
    L.append("║ QUEUE (the drainer)")
    L.extend("║" + r for r in queue_state())
    L.append("║ METERS (smith chart)")
    L.extend("║" + r for r in meters_headline())
    L.append("║ WATCH (mimo window)")
    L.extend("║" + r for r in mimo_state())
    L.append("╚" + "═" * 60)
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--interval", type=float, default=2.0)
    a = ap.parse_args()
    if a.once:
        print(frame())
        return 0
    try:
        while True:
            sys.stdout.write(CLEAR + frame() + "\n")
            sys.stdout.flush()
            time.sleep(a.interval)
    except KeyboardInterrupt:
        print("\n[dfhack] overlay closed. the colony keeps working.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
