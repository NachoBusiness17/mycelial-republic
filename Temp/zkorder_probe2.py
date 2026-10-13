import sqlite3, datetime

DB = "C:/Users/foste/.zcode/cli/db/db.sqlite"
conn = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
rows = list(conn.execute(
    "SELECT id, task_type, time_updated FROM session WHERE id LIKE '%7318df04%' "
    "OR id LIKE '%fce37d85%' OR id LIKE '%712a3b7b%' OR id LIKE '%fd5ec147%'"))
for sid, ttype, tu in rows:
    print(sid[:14], ttype, datetime.datetime.fromtimestamp(tu / 1000).strftime("%m-%d %H:%M"))
conn.close()
