# probe (accuracy lens) shape B: real_user text via part-table join.
# Adjudicates economics.md claims: 18,991 turns / 51.65M chars all-time;
# 7d 4,402 turns / 16.8M chars / median 2,584 / p90 4,673 / max 345,016;
# voice-class (<500 chars) 539 turns in 7d. Read-only.
import json
import sqlite3
import statistics
from pathlib import Path

db = Path.home() / ".zcode" / "cli" / "db" / "db.sqlite"
con = sqlite3.connect("file:" + str(db).replace("\\", "/") + "?mode=ro", uri=True)
cur = con.cursor()

rows = cur.execute(
    "select p.time_created, p.data from part p join message m on p.message_id = m.id "
    "where json_extract(m.data,'$.semantics.origin')='real_user' "
    "and json_extract(p.data,'$.type')='text' order by p.time_created"
).fetchall()
print("real_user text parts:", len(rows))

texts = []
for tc, d in rows:
    try:
        obj = json.loads(d)
    except Exception:
        continue
    t = obj.get("text")
    if isinstance(t, str):
        texts.append((tc, t))
print("parsed texts:", len(texts))

chars = [len(t) for _, t in texts]
print("all-time turns:", len(texts), "total chars:", sum(chars),
      "approx tokens chars/4:", round(sum(chars) / 4))

last_ms = texts[-1][0]
print("span:", texts[0][0], "->", last_ms)
SEVEN_D_MS = 7 * 24 * 3600 * 1000
for label, cutoff in (("last7d", last_ms - SEVEN_D_MS),):
    t7 = [(tc, t) for tc, t in texts if tc >= cutoff]
    c7 = sorted(len(t) for _, t in t7)
    voice7 = [len(t) for _, t in t7 if len(t) < 500]
    print(label, "turns:", len(t7), "chars:", sum(c7),
          "median:", int(statistics.median(c7)) if c7 else None,
          "p90:", c7[int(0.9 * len(c7))] if c7 else None,
          "max:", max(c7) if c7 else None,
          "voice(<500c):", len(voice7), "voice chars:", sum(voice7),
          "voice approx tokens:", round(sum(voice7) / 4))

# assistant side (for the dyad claim: ~104,809 text parts, ~9.6M tokens)
arows = cur.execute(
    "select count(*) from part p join message m on p.message_id = m.id "
    "where json_extract(m.data,'$.semantics.origin')='assistant' "
    "and json_extract(p.data,'$.type')='text'"
).fetchone()[0]
achars = cur.execute(
    "select sum(length(json_extract(p.data,'$.text'))) from part p join message m on p.message_id = m.id "
    "where json_extract(m.data,'$.semantics.origin')='assistant' "
    "and json_extract(p.data,'$.type')='text'"
).fetchone()[0]
print("assistant text parts:", arows, "assistant chars:", achars,
      "approx tokens chars/4:", round((achars or 0) / 4))
con.close()
