# probe: size the operator tape in the zknot source db (read-only)
# moonshot-2 2026-10-10; counts real_user messages + correction-shaped subset
import json
import re
import sqlite3
from pathlib import Path

db = Path.home() / ".zcode" / "cli" / "db" / "db.sqlite"
con = sqlite3.connect("file:" + str(db).replace("\\", "/") + "?mode=ro", uri=True)
cur = con.cursor()

total = cur.execute("select count(*) from message").fetchone()[0]
corr_re = re.compile(
    r"(you keep|stop doing|that'?s bullshit|you'?re wrong|i already told|we discussed|"
    r"you forgot|don'?t make|why aren'?t|why can'?t we|quit it|no\.|ugh|i don'?t believe)",
    re.I,
)
n_real = 0
n_corr = 0
first = None
last = None
rows = cur.execute(
    "select session_id, time_created, data from message "
    "where json_extract(data,'$.semantics.origin')='real_user' order by time_created"
).fetchall()
for sid, tc, data in rows:
    try:
        d = json.loads(data)
    except Exception:
        continue
    n_real += 1
    c = d.get("content")
    txt = ""
    if isinstance(c, list):
        txt = " ".join(p.get("text", "") for p in c if isinstance(p, dict))
    elif isinstance(c, str):
        txt = c
    if corr_re.search(txt):
        n_corr += 1
    if first is None:
        first = tc
    last = tc
print("total messages:", total)
print("real_user messages:", n_real)
print("correction-shaped (regex hit):", n_corr)
print("span:", first, "->", last)
