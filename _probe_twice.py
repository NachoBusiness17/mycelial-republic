import time, urllib.request, json

def hit():
    t0 = time.time()
    try:
        with urllib.request.urlopen("http://127.0.0.1:8765/api/v1/table/view", timeout=8) as r:
            body = r.read()
        j = json.loads(body)
        return round(time.time()-t0, 3), r.status, j.get("title"), j.get("room_id"), (j.get("scene") or {}).get("exits")
    except Exception as e:
        return round(time.time()-t0, 3), type(e).__name__, str(e)[:80], None, None

print("1", hit())
print("2", hit())
