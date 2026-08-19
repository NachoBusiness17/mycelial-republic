import json, time, urllib.request, urllib.error

def post(url, obj, timeout=10):
    t0 = time.time()
    req = urllib.request.Request(url, data=json.dumps(obj).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            b = r.read()
        return round(time.time()-t0, 3), r.status, json.loads(b)
    except urllib.error.HTTPError as e:
        return round(time.time()-t0, 3), e.code, e.read()[:300]
    except Exception as e:
        return round(time.time()-t0, 3), type(e).__name__, str(e)[:160]

def get(url, timeout=8):
    t0 = time.time()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            b = r.read()
        return round(time.time()-t0, 3), r.status, json.loads(b) if b.startswith(b"{") else b[:80]
    except Exception as e:
        return round(time.time()-t0, 3), type(e).__name__, str(e)[:160]

print("WAVE", get("http://127.0.0.1:8765/api/v1/wave"))
sec, st, j = post("http://127.0.0.1:8765/api/v1/voice/turn", {
    "text": "look", "session_id": "wave-debug", "channel": "table", "conversation": True
})
ans = j.get("answer") if isinstance(j, dict) else j
print("LOOK", sec, st, (ans or "")[:220], "route", (j.get("route") if isinstance(j, dict) else None))
