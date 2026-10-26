# operations-lens tape census probe (2026-10-10, read-only)
# Independent re-derivation of the interlocutor-tape volume the interaction
# thesis claims. Opens the harness session db mode=ro (the zknot law: no
# writes, no LLM). Same instrument class as tools/zknot.py:62.
import sqlite3, os, time

db = os.path.expanduser('~/.zcode/cli/db/db.sqlite')
uri = 'file:' + db.replace(chr(92), '/') + '?mode=ro'
con = sqlite3.connect(uri, uri=True)
cur = con.cursor()
cutoff = int((time.time() - 7 * 86400) * 1000)

base = ("select count(*), coalesce(sum(length(json_extract(p.data,'$.text'))),0) "
        "from message m join part p on p.message_id = m.id "
        "where json_extract(m.data,'$.role')='user' "
        "and json_extract(m.data,'$.semantics.origin')='real_user' "
        "and json_extract(p.data,'$.type')='text'")

print('all-time real_user text parts, chars:', cur.execute(base).fetchone())
print('7d real_user text parts, chars:',
      cur.execute(base + ' and m.time_created >= ' + str(cutoff)).fetchone())
vq = base + " and length(json_extract(p.data,'$.text')) < 500 and m.time_created >= " + str(cutoff)
print('7d voice-class (<500 chars):', cur.execute(vq).fetchone())

# assistant side of the dyad, all-time
aq = ("select count(*) from part p join message m on p.message_id = m.id "
      "where json_extract(m.data,'$.role')='assistant' "
      "and json_extract(p.data,'$.type')='text'")
print('all-time assistant text parts:', cur.execute(aq).fetchone())

# turn-taking shape: sessions with >= 10 real_user turns (dyad depth)
sq = ("select count(*) from (select m.session_id, count(*) c from message m "
      "where json_extract(m.data,'$.role')='user' "
      "and json_extract(m.data,'$.semantics.origin')='real_user' "
      "group by m.session_id having c >= 10)")
print('sessions with >=10 real_user turns:', cur.execute(sq).fetchone())
