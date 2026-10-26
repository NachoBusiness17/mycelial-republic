import json, io, sys, glob, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
root = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
for p in sorted(glob.glob(root + r"\.tmp_sweep_deep\sub_*.json")):
    try:
        with open(p, encoding="utf-8") as f: s = json.load(f)
    except Exception as e:
        print(p, "ERR", e); continue
    if isinstance(s, list): s = s[0] if s else {}
    ts = s.get("created_utc", 0)
    print(time.strftime("%Y-%m-%d", time.gmtime(ts)), f"score={s.get('score')}", f"c={s.get('num_comments')}",
          f"[{s.get('subreddit')}]", (s.get("title") or "")[:95])
print("---- comment file row counts ----")
for p in sorted(glob.glob(root + r"\.tmp_sweep_deep\com_*.json")):
    try:
        with open(p, encoding="utf-8") as f: rows = json.load(f)
        n = len(rows) if isinstance(rows, list) else -1
        last = max((r.get("created_utc",0) for r in rows), default=0) if isinstance(rows,list) else 0
        print(p.split("\\")[-1], "rows:", n, "newest comment:", time.strftime("%Y-%m-%d", time.gmtime(last)))
    except Exception as e:
        print(p, "ERR", e)
