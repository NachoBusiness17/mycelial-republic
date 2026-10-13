import sqlite3, datetime

DB = "C:/Users/foste/.zcode/cli/db/db.sqlite"
conn = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)

q = """
SELECT m.session_id, m.time_created, substr(json_extract(p.data,'$.text'),1,140)
FROM message m JOIN part p ON p.message_id = m.id
WHERE json_extract(m.data,'$.role') = 'user'
  AND (json_extract(p.data,'$.text') LIKE '%lens this%'
       OR json_extract(p.data,'$.text') LIKE '%coldest shared vertex%')
ORDER BY m.time_created DESC LIMIT 10
"""
for sid, t, txt in conn.execute(q):
    when = datetime.datetime.fromtimestamp(t / 1000).strftime("%m-%d %H:%M")
    print(when, sid[:14], repr(txt))

# card the candidate sessions zknot would see today
q2 = """
SELECT id, task_type, time_created, time_updated,
       (SELECT count(*) FROM message m2 WHERE m2.session_id = session.id
          AND json_extract(m2.data,'$.role')='user') AS user_msgs
FROM session
WHERE time_updated >= 1781000000000
ORDER BY time_updated DESC LIMIT 12
"""
print("=== recent sessions (id, task_type, created, updated, user_msgs)")
for sid, ttype, tc, tu, n in conn.execute(q2):
    print(sid[:14], ttype,
          datetime.datetime.fromtimestamp(tc / 1000).strftime("%m-%d %H:%M"),
          datetime.datetime.fromtimestamp(tu / 1000).strftime("%m-%d %H:%M"), n)
conn.close()
