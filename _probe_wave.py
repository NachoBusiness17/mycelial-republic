import json, time, urllib.request, urllib.error

def hit(url, data=None, timeout=8):
    t0 = time.time()
    try:
        req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
        if data:
            req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
        return round(time.time()-t0, 3), r.status, body[:500]
    except urllib.error.HTTPError as e:
        return round(time.time()-t0, 3), e.code, e.read()[:400]
    except Exception as e:
        return round(time.time()-t0, 3), type(e).__name__, str(e)[:160]

print("TABLE", hit("http://127.0.0.1:8765/table"))
print("WAVEHTML", hit("http://127.0.0.1:8765/wave"))
print("WAVEAPI", hit("http://127.0.0.1:8765/api/v1/wave?session_id=wave-debug"))
print("GAME", hit("http://127.0.0.1:8765/api/v1/game", json.dumps({"action":"status"}).encode()))
print("LOOK", hit("http://127.0.0.1:8765/api/v1/voice/turn", json.dumps({
    "text":"look","session_id":"wave-debug","channel":"table","conversation":True
}).encode(), timeout=12))
