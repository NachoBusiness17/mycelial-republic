#!/usr/bin/env python3
"""live_feed.py — the fleet's live nerve surface. $0, no model calls.

Operator ask (09-04 night, re-asked 09-05 with heat): a vision model over a live
feed of verbose code/window activity. This is the feed half: tails the ZCode
session db READ-ONLY and rewrites dashboard/static/live_feed.json every 30s so
/static/live.html can poll it. The VISION half rides steering passes — any seat
opens live.html (or reads the json) and looks; no cron'd model ticks
(heartbeat-throttle law: a watcher that wakes a premium model is the zombie-tick
disease). Loopback-only surface, one log line per refresh, secret-shaped strings
redacted from excerpts before they touch disk. Paths are pathlib constants
under the repo root (Mimosa-clean shape, same as salon_phone.py).
"""
import json, re, sqlite3, time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "dashboard" / "static" / "live_feed.json"
LOG = REPO / "watch" / "live_feed.log"
DB = Path.home() / ".zcode" / "cli" / "db" / "db.sqlite"
WINDOW_H = 12          # sessions updated within this many hours appear
SECRET = re.compile(r"(sk-[A-Za-z0-9]{6,}|Bearer\s+\S+|[A-Fa-f0-9]{32,}|xox[baprs]-\S+)")

for _p in (OUT, LOG):
    if REPO not in _p.resolve().parents:
        raise ValueError(f"write target escapes repo: {_p}")

def redact(s, n=160):
    s = SECRET.sub("[REDACTED]", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:n]

def snapshot():
    db = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=3)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("""
        SELECT id, title, time_updated FROM session
        WHERE time_updated > (? - 1000*3600*?)
        ORDER BY time_updated DESC""", (int(time.time()*1000), WINDOW_H))
    sessions = []
    for s in cur.fetchall():
        cur.execute("""
            SELECT p.data, p.time_created, m.data AS mdata
            FROM part p JOIN message m ON p.message_id = m.id
            WHERE p.session_id = ? ORDER BY p.time_created DESC LIMIT 4""", (s["id"],))
        actions = []
        for p in cur.fetchall():
            try:
                d = json.loads(p["data"])
                role = json.loads(p["mdata"]).get("role", "?")
            except Exception:
                continue
            dt = datetime.fromtimestamp(p["time_created"]/1000, tz=timezone.utc).strftime("%H:%M:%S")
            kind = d.get("type", "?")
            if kind == "text":
                excerpt = redact(d.get("text", ""))
            elif kind == "tool":
                tool = d.get("tool", "?")
                inp = d.get("state", {}).get("input", {})
                what = inp.get("file_path") or inp.get("description") or inp.get("command") or json.dumps(inp)
                excerpt = f"{tool}: {redact(str(what))}"
            elif kind == "reasoning":
                excerpt = redact(d.get("text", ""))
            else:
                excerpt = ""
            actions.append({"t": dt, "role": role, "kind": kind, "x": excerpt})
        sessions.append({
            "id": s["id"][:17], "title": (s["title"] or "?")[:60],
            "updated": datetime.fromtimestamp(s["time_updated"]/1000, tz=timezone.utc).strftime("%H:%M:%S"),
            "actions": actions,
        })
    db.close()
    return {"ts": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "note": "excerpt feed, secrets redacted, $0 — vision rides steering passes",
            "sessions": sessions}

def main():
    while True:
        try:
            data = snapshot()
            OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            with LOG.open("a", encoding="utf-8") as f:
                f.write(f"{data['ts']} sessions={len(data['sessions'])}\n")
        except Exception as exc:
            with LOG.open("a", encoding="utf-8") as f:
                f.write(f"{datetime.now(tz=timezone.utc).isoformat()} ERROR {type(exc).__name__}: {exc}\n")
        time.sleep(30)

if __name__ == "__main__":
    main()
