# break-operations voice-class audit (2026-10-10, read-only)
# Attacks F1's falsifier (real_user mislabeling) and calibrates the probe's
# pass bar: applies the SAME regexes zknot_alarm.py:49-50 uses (SELF_STEAL_RE,
# FORGOT_RE) to the db 7d voice-class population, then samples texts.
# Same instrument class as _tape_census.py: sqlite mode=ro, no writes, no LLM.
import sqlite3, os, re, time, json

db = os.path.expanduser('~/.zcode/cli/db/db.sqlite')
uri = 'file:' + db.replace(chr(92), '/') + '?mode=ro'
con = sqlite3.connect(uri, uri=True)
cur = con.cursor()
cutoff = int((time.time() - 7 * 86400) * 1000)

SELF_STEAL_RE = re.compile(r"self[\s_-]*ste[a]?l", re.I)
FORGOT_RE = re.compile(r"\bforg[oe]t|already have|\bremember\b", re.I)

q = ("select m.session_id, json_extract(p.data,'$.text') t, m.time_created "
     "from message m join part p on p.message_id = m.id "
     "where json_extract(m.data,'$.role')='user' "
     "and json_extract(m.data,'$.semantics.origin')='real_user' "
     "and json_extract(p.data,'$.type')='text' "
     "and length(json_extract(p.data,'$.text')) < 500 "
     "and m.time_created >= ? order by m.time_created desc")
rows = cur.execute(q, (cutoff,)).fetchall()
texts = [r[1] or '' for r in rows]
ss = sum(1 for t in texts if SELF_STEAL_RE.search(t))
fg = sum(1 for t in texts if FORGOT_RE.search(t))
n = len(texts)
rate = round(1000 * (ss + fg) / n) if n else 0
print('7d voice-class turns:', n)
print('self-steal matches:', ss, 'forgot matches:', fg,
      '-> rate per 1000:', rate, '(published meter: 98 per 1000 of 448 zknot-population)')

# session mix: how many of these turns come from sessions zknot cards cover
# (zknot.py drops child sessions + under-5-prompt mains)?
sess = {}
for s, t, tc in rows:
    sess.setdefault(s, []).append(tc)
print('distinct sessions holding 7d voice-class turns:', len(sess))
big = sorted(sess.items(), key=lambda kv: -len(kv[1]))[:5]
for s, ts in big:
    print('  session', s[:22], 'turns', len(ts))

# sample the 10 newest texts (first 90 chars, escapes kept) for the
# humanity audit the lens's falsifier named
print('--- newest 10 samples (90 chars) ---')
for s, t, tc in rows[:10]:
    print(' ', json.dumps((t or '')[:90]))
