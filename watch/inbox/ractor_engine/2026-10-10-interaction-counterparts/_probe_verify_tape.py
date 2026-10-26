# probe (accuracy lens): adjudicate the tape census contradiction between the
# economics.md char-level claims and moonshot-2.md "content unmeasured" claim.
# Read-only against the zknot source db. Banks counts + char stats for real_user
# text via BOTH candidate shapes: message.data content field AND the part table.
import json
import sqlite3
import statistics
from pathlib import Path

db = Path.home() / ".zcode" / "cli" / "db" / "db.sqlite"
con = sqlite3.connect("file:" + str(db).replace("\\", "/") + "?mode=ro", uri=True)
cur = con.cursor()

print("db size MB:", round(db.stat().st_size / 1048576, 1))
tables = [r[0] for r in cur.execute("select name from sqlite_master where type='table'").fetchall()]
print("tables:", tables)
print("message count:", cur.execute("select count(*) from message").fetchone()[0])
print("real_user messages:", cur.execute(
    "select count(*) from message where json_extract(data,'$.semantics.origin')='real_user'"
).fetchone()[0])
print("message columns:", [d[1] for d in cur.execute("pragma table_info(message)").fetchall()])
print("part columns:", [d[1] for d in cur.execute("pragma table_info(part)").fetchall()])

# shape A: text inside message.data content (the moonshot guess that returned 0)
rows = cur.execute(
    "select time_created, data from message "
    "where json_extract(data,'$.semantics.origin')='real_user' order by time_created"
).fetchall()

def text_from_data(d):
    try:
        obj = json.loads(d)
    except Exception:
        return None
    c = obj.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        t = " ".join(p.get("text", "") for p in c if isinstance(p, dict))
        return t or None
    return None

shapeA = [(tc, t) for tc, d in rows if (t := text_from_data(d))]
print("shape A (message.data content) texts:", len(shapeA))

# shape B: the part table keyed by message
cols = [d[1] for d in cur.execute("pragma table_info(part)").fetchall()]
msg_key = "message_id" if "message_id" in cols else ("sessionId" if False else None)
print("part rows:", cur.execute("select count(*) from part").fetchone()[0])
# sample one part row to learn the shape
sample = cur.execute("select * from part limit 1").fetchone()
if sample:
    print("part sample (truncated 400):", str(sample)[:400])

SEVEN_D_MS = 7 * 24 * 3600 * 1000
last_ms = rows[-1][0] if rows else 0
cutoff = last_ms - SEVEN_D_MS

def report(name, pairs):
    if not pairs:
        print(name, ": NO TEXTS MEASURED")
        return
    chars = [len(t) for _, t in pairs]
    last7 = [(tc, t) for tc, t in pairs if tc >= cutoff]
    c7 = [len(t) for _, t in last7]
    voice7 = [len(t) for _, t in last7 if len(t) < 500]
    print(name, "texts:", len(pairs), "total chars:", sum(chars))
    if c7:
        print(name, "last7d: turns", len(c7), "chars", sum(c7),
              "median", int(statistics.median(c7)), "p90", int(sorted(c7)[int(0.9 * len(c7))]),
              "max", max(c7), "voice(<500c) turns", len(voice7), "voice chars", sum(voice7))

report("shapeA", shapeA)
con.close()
