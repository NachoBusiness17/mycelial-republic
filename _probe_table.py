import time, urllib.request
t0 = time.time()
try:
    req = urllib.request.Request("http://127.0.0.1:8765/api/v1/table/view")
    with urllib.request.urlopen(req, timeout=8) as r:
        body = r.read()
    print("status", r.status, "len", len(body), "sec", round(time.time()-t0, 3))
    print(body[:300].decode("utf-8", "replace"))
except Exception as e:
    print("ERR", type(e).__name__, e, "sec", round(time.time()-t0, 3))
