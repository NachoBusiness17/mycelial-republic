"""break-communication byte-check instrument (2026-10-10).

Read-only (db opens mode=ro). Verifies lens FINDING 2/3/4 numbers and
enumerates the schema the lens left as its own falsifier. Uses the estate's
own template instrument (tools/zknot_alarm.template_prefixes / is_template)
plus a raw docstring-rule variant. No writes outside stdout.
"""
import datetime as dt
import json
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT / "tools"))
from zknot_alarm import template_prefixes, is_template  # noqa: E402

now_ms = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)
D30 = 30 * 86400 * 1000
D7 = 7 * 86400 * 1000
print("moment_utc", dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"))

DB = Path.home() / ".zcode" / "cli" / "db" / "db.sqlite"
con = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
cur = con.cursor()

# schema: tables + columns (the lens's own falsifier leg)
tabs = [r[0] for r in cur.execute("select name from sqlite_master where type='table'")]
print("tables:", tabs)
for t in ("session", "message", "part"):
    if t in tabs:
        print(t, "columns:", [r[1] for r in cur.execute(f"PRAGMA table_info({t})")])

q = """
SELECT m.id, m.session_id, m.time_created,
 (SELECT group_concat(json_extract(p.data,'$.text'), char(10)) FROM part p
   WHERE p.message_id=m.id AND json_extract(p.data,'$.type')='text') AS txt
FROM message m
WHERE json_extract(m.data,'$.role')='user'
  AND coalesce(json_extract(m.data,'$.semantics.origin'),'real_user')='real_user'
  AND m.time_created >= ?
"""
rows = [(mid, sid, int(t), (txt or "")) for mid, sid, t, txt in cur.execute(q, (now_ms - D30,))
        if txt and txt.strip()]
print("raw30 (coalesce-origin, text-bearing):", len(rows))

# lens method: strict origin filter
n_strict = cur.execute(
    "select count(*) from message m where json_extract(m.data,'$.role')='user' "
    "and json_extract(m.data,'$.semantics.origin')='real_user' and m.time_created >= ? "
    "and exists (select 1 from part p where p.message_id=m.id "
    "and json_extract(p.data,'$.type')='text')", (now_ms - D30,)).fetchone()[0]
print("raw30 (strict origin, incl empty-text):", n_strict)

# templated drop, BOTH instruments
prompts = {}
for mid, sid, t, txt in rows:
    prompts.setdefault(sid, []).append({"t": t, "text": txt})
tmpl = template_prefixes(prompts)
drop_zk = sum(1 for mid, sid, t, txt in rows if is_template({"text": txt}, tmpl))
print("zknot_alarm instrument: bulk prefixes", len(tmpl), "dropped", drop_zk,
      "kept", len(rows) - drop_zk)

prefc = Counter(txt[:40] for mid, sid, t, txt in rows if len(txt) > 150)
bulk_raw = {p for p, c in prefc.items() if c >= 8}
drop_raw = sum(1 for mid, sid, t, txt in rows if len(txt) > 150 and txt[:40] in bulk_raw)
print("raw docstring rule (no ws-normalize): bulk prefixes", len(bulk_raw),
      "dropped", drop_raw, "kept", len(rows) - drop_raw)

kept = [(mid, sid, t, txt) for mid, sid, t, txt in rows if not is_template({"text": txt}, tmpl)]

# dispatch openers on kept
DIS = re.compile(r"^(LANE TASK|Tier-\d|Flash-lane)", re.I)
dis = [r for r in kept if DIS.match(r[3])]
print("dispatch-opener (^LANE TASK|^Tier-N|^Flash-lane) in kept:", len(dis))

# samples
print("sample1 'You are lane B2-64...':",
      sum(1 for r in rows if r[3].startswith("You are lane B2-64 of the 2026-09-26 flash-lane burn")))
print("sample2 'LANE: hermes-burn-economics (division B)':",
      sum(1 for r in rows if r[3].startswith("LANE: hermes-burn-economics (division B)")))

# first-line shape census (lens: 1766 lowercase / 518 url / 3696 capitalized)
def first_line(t):
    for ln in t.splitlines():
        ln = " ".join(ln.split())
        if ln:
            return ln
    return ""
shape = Counter()
for mid, sid, t, txt in kept:
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
print("first-line shape census (kept, zknot instrument):", dict(shape))

# FALSIFIER: message.data key census over the 30d user rows + session provenance
mids = [r[0] for r in rows]
msg_keys = Counter()
for i in range(0, len(mids), 500):
    chunk = mids[i:i + 500]
    for mid, data in cur.execute("select id, data from message where id in (%s)"
                                 % ",".join("?" * len(chunk)), chunk):
        try:
            for k in (json.loads(data or "{}") or {}).keys():
                msg_keys[k] += 1
        except Exception:
            msg_keys["<unparsable>"] += 1
print("message.data key census (30d user rows):", dict(msg_keys))

sids = list({r[1] for r in rows})
sess = {}
for i in range(0, len(sids), 500):
    chunk = sids[i:i + 500]
    for sid, ttype, parent, title in cur.execute(
            "select id, task_type, parent_id, title from session where id in (%s)"
            % ",".join("?" * len(chunk)), chunk):
        sess[sid] = (ttype, parent, title)
tt = Counter(v[0] for v in sess.values())
par = Counter("has_parent" if v[1] else "no_parent" for v in sess.values())
print("sessions holding 30d real_user msgs:", len(sess), "task_type:", dict(tt), dict(par))
n_child = sum(1 for r in rows if r[1] in sess and (sess[r[1]][0] in ("subagent_child", "workflow_child") or sess[r[1]][1]))
print("30d real_user msgs in child-type or parented sessions:", n_child)
lane_t = sum(1 for v in sess.values() if v[2] and re.search(r"lane|burn|division|flash|tier-\d", v[2], re.I))
print("sessions with lane/burn/division/flash/tier-shaped TITLE:", lane_t, "of", len(sess))
# kept-bucket messages living in lane-titled sessions (dispatch separation power)
lane_sids = {sid for sid, v in sess.items() if v[2] and re.search(r"lane|burn|division|flash|tier-\d", v[2], re.I)}
print("kept msgs in lane-titled sessions:", sum(1 for r in kept if r[1] in lane_sids))

# FINDING 4 falsifier: 7d meter-shape denominator
rows7 = [r for r in rows if r[2] >= now_ms - D7]
kept7 = [r for r in rows7 if not is_template({"text": r[3]}, tmpl)]
dis7 = [r for r in kept7 if DIS.match(r[3])]
oneoff7 = [r for r in kept7 if not DIS.match(r[3]) and re.match(
    r"^(You are |LANE:|TASK:|OPERATOR ORDER|DIVISION|Lane \d|B2-\d|WAVE |BURN )", r[3])]
print("7d raw:", len(rows7), "| 7d kept:", len(kept7),
      "| dispatch-opener:", len(dis7), "| oneoff-dispatch-shaped:", len(oneoff7))
for r in oneoff7[:5]:
    print("  oneoff:", repr(first_line(r[3])[:90]))

# FINDING 3: correction-keyword census on kept 30d (lens: 2862, method unspecified)
CORR = re.compile(r"\b(wrong|incorrect|no,|don't|do not|stop |not that|i said|correction|"
                  r"instead|actually,|you missed|you forgot|misread|mistake|again:|"
                  r"i asked|i told you|we already|already told|re-?ask)", re.I)
corr = sum(1 for r in kept if CORR.search(r[3]))
corr_human = sum(1 for r in kept if CORR.search(r[3]) and r[1] not in lane_sids)
print("correction-keyword hits kept30d (my list):", corr, "| excluding lane-titled sessions:", corr_human)
con.close()
