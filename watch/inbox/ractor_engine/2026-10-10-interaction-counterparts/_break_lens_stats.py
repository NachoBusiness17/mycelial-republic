"""break-economics supplement: db size + 7d turn-length stats (raw vs human voice)."""
import datetime as dt
import json
import sqlite3
import statistics
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT / "tools"))
from zknot_alarm import template_prefixes, is_template

DB = Path.home() / ".zcode" / "cli" / "db" / "db.sqlite"
now_ms = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)
WK = 7 * 86400 * 1000
out = {"now_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
       "db_bytes": DB.stat().st_size, "db_gib": round(DB.stat().st_size / 1024 ** 3, 2)}

conn = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
msgs = []
for sid, t, is_child, txt in conn.execute("""
SELECT m.session_id, m.time_created, CASE WHEN s.parent_id IS NULL THEN 0 ELSE 1 END,
  (SELECT group_concat(json_extract(p.data,'$.text'), char(10)) FROM part p
    WHERE p.message_id=m.id AND json_extract(p.data,'$.type')='text') AS txt
FROM message m JOIN session s ON s.id=m.session_id
WHERE json_extract(m.data,'$.role')='user'
  AND coalesce(json_extract(m.data,'$.semantics.origin'),'real_user')='real_user'
  AND m.time_created >= ?""", (now_ms - 40 * 86400 * 1000,)):
    if txt and txt.strip():
        msgs.append({"t": int(t), "child": is_child, "text": txt})
prompts = {}
for m in msgs:
    prompts.setdefault(m["sid"] if "sid" in m else "", []).append(m)
# rebuild sid key properly (query returns sid first)
conn.close()
conn = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
msgs = []
for sid, t, is_child, txt in conn.execute("""
SELECT m.session_id, m.time_created, CASE WHEN s.parent_id IS NULL THEN 0 ELSE 1 END,
  (SELECT group_concat(json_extract(p.data,'$.text'), char(10)) FROM part p
    WHERE p.message_id=m.id AND json_extract(p.data,'$.type')='text') AS txt
FROM message m JOIN session s ON s.id=m.session_id
WHERE json_extract(m.data,'$.role')='user'
  AND coalesce(json_extract(m.data,'$.semantics.origin'),'real_user')='real_user'
  AND m.time_created >= ?""", (now_ms - 40 * 86400 * 1000,)):
    if txt and txt.strip():
        msgs.append({"sid": sid, "t": int(t), "child": is_child, "text": txt})
conn.close()
pr = {}
for m in msgs:
    pr.setdefault(m["sid"], []).append({"t": m["t"], "text": m["text"]})
tmpl = template_prefixes(pr)


def pctl(vals, p):
    vals = sorted(vals)
    if not vals:
        return None
    k = max(0, min(len(vals) - 1, int(round(p / 100.0 * (len(vals) - 1)))))
    return vals[k]


def lens_stats(label, ms):
    L = [len(m["text"]) for m in ms]
    out[label] = {"n": len(L), "median": statistics.median(L) if L else None,
                  "p90": pctl(L, 90), "max": max(L) if L else None}


w7 = [m for m in msgs if m["t"] >= now_ms - WK]
lens_stats("raw_7d_all", w7)
lens_stats("nontmpl_toplevel_7d", [m for m in w7 if not m["child"] and not is_template(m, tmpl)])
lens_stats("voice_lt500_nontmpl_toplevel_7d", [m for m in w7 if not m["child"] and len(m["text"]) < 500
                                               and not is_template(m, tmpl)])
print(json.dumps(out, indent=1))
