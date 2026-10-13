import time, urllib.request, json
t0=time.time()
with urllib.request.urlopen("http://127.0.0.1:8765/api/v1/table/view", timeout=8) as r:
    body=r.read()
print("sec", round(time.time()-t0,3), "len", len(body), "status", r.status)
j=json.loads(body)
print("title", j.get("title"), "room", j.get("room_id"), "skin", j.get("skin"), "cid", j.get("campaign_id"))
print("exits", (j.get("scene") or {}).get("exits"))
print("grid_text:")
print(j.get("grid_text") or "")
