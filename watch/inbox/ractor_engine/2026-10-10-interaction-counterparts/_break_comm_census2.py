"""break-communication follow-up (2026-10-10): the session-separated human tape.

Applies zknot's own session filter (parent_id IS NULL AND task_type NOT IN
child types) to the 30d/7d kept buckets, then dispatch shapes within it.
Read-only, mode=ro.
"""
import datetime as dt
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT / "tools"))
from zknot_alarm import template_prefixes, is_template  # noqa: E402

now_ms = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)
D30, D7 = 30 * 86400 * 1000, 7 * 86400 * 1000
print("moment_utc", dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"))
DB = Path.home() / ".zcode" / "cli" / "db" / "db.sqlite"
con = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)

q = """
SELECT m.id, m.session_id, m.time_created,
 (SELECT group_concat(json_extract(p.data,'$.text'), char(10)) FROM part p
   WHERE p.message_id=m.id AND json_extract(p.data,'$.type')='text') AS txt
FROM message m JOIN session s ON s.id = m.session_id
WHERE json_extract(m.data,'$.role')='user'
  AND coalesce(json_extract(m.data,'$.semantics.origin'),'real_user')='real_user'
  AND m.time_created >= ?
  AND s.parent_id IS NULL AND s.task_type NOT IN ('subagent_child','workflow_child')
"""
rows = [(mid, sid, int(t), (txt or "")) for mid, sid, t, txt in con.execute(q, (now_ms - D30,))
        if txt and txt.strip()]
print("30d real_user in TOP-LEVEL non-child sessions (raw):", len(rows))
prompts = {}
for mid, sid, t, txt in rows:
    prompts.setdefault(sid, []).append({"t": t, "text": txt})
tmpl = template_prefixes(prompts)
kept = [r for r in rows if not is_template({"text": r[3]}, tmpl)]
print("30d kept after template drop:", len(kept), "| bulk prefixes:", len(tmpl))

DIS = re.compile(r"^(LANE TASK|LANE:|Tier-\d|Flash-lane|You are |TASK:|OPERATOR ORDER|"
                 r"DIVISION|Lane \d|B2-\d|WAVE |BURN )", re.I)
dis = [r for r in kept if DIS.match(r[3])]
print("dispatch-shaped in top-level kept (blocklist union):", len(dis))
print("=> deterministic human-tape ceiling 30d:", len(kept) - len(dis),
      "| naive raw 30d was ~14.0k, so overstatement factor ~%.1fx"
      % (14009.0 / max(1, len(kept) - len(dis))))

# 7d meter denominator audit (LATEST.md:3 says 448 human prompts last 7d)
rows7 = [r for r in rows if r[2] >= now_ms - D7]
kept7 = [r for r in rows7 if not is_template({"text": r[3]}, tmpl)]
dis7 = [r for r in kept7 if DIS.match(r[3])]
# zknot qualifying sessions need >=5 prompts
per_sess = Counter(r[1] for r in kept7)
qual = {sid for sid, c in per_sess.items() if c >= 5}
kept7q = [r for r in kept7 if r[1] in qual]
dis7q = [r for r in kept7q if DIS.match(r[3])]
print("7d top-level kept:", len(kept7), "| in >=5-prompt sessions (zknot qualifier):", len(kept7q),
      "| dispatch-shaped among those:", len(dis7q))
print("=> meter-denominator comparable figures: raw7 all-sessions 4421 / top-level kept",
      len(kept7), "/ zknot-qualifier", len(kept7q))
for r in kept7q[:0]:
    pass
sample_dis = [r[3].splitlines()[0][:70] for r in dis7q[:6]]
print("dispatch samples inside the qualifier bucket:", sample_dis)

# shape census of the separated human tape (30d, kept, minus dispatch)
def first_line(t):
    for ln in t.splitlines():
        ln = " ".join(ln.split())
        if ln:
            return ln
    return ""
shape = Counter()
for mid, sid, t, txt in kept:
    if DIS.match(txt):
        continue
    fl = first_line(txt)
    if not fl:
        shape["empty"] += 1
    elif re.match(r"https?://|www\.", fl):
        shape["url"] += 1
    elif fl[0].islower():
        shape["lowercase"] += 1
    elif fl[0].isupper():
        shape["capitalized"] += 1
    else:
        shape["other"] += 1
print("shape census of separated human tape 30d:", dict(shape))
con.close()
