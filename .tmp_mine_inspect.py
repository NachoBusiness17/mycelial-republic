import json, io, sys, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
root = r"C:\Users\foste\Documents\projects\local_sovereign_agent"

for name in [".tmp_sweep_llama.json", ".tmp_sweep_candidates.json"]:
    p = root + "\\" + name
    try:
        with open(p, encoding="utf-8") as f:
            j = json.load(f)
    except Exception as e:
        print(name, "LOAD-FAIL", e); continue
    kids = j.get("data", {}).get("children") if isinstance(j, dict) else None
    if kids:
        print("==", name, "children:", len(kids))
        for c in kids[:60]:
            d = c.get("data", {})
            ts = d.get("created_utc", 0)
            dt = datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d") if ts else "?"
            print(f"{dt} | {d.get('score')} | {d.get('num_comments')} | {d.get('permalink','')} | {d.get('title','')[:110]}")
    else:
        # candidates file: unknown shape, print keys
        print("==", name, "shape:", type(j), (list(j.keys())[:10] if isinstance(j, dict) else len(j)))
        items = j if isinstance(j, list) else j.get("candidates", [])
        for it in items[:60]:
            if isinstance(it, dict):
                print(it.get("date","?"), "|", it.get("score",""), "|", str(it.get("url",""))[:90], "|", str(it.get("title",""))[:110])
