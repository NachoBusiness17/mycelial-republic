import urllib.request, json
h = urllib.request.urlopen("http://192.168.86.35:8765/wave", timeout=5).read().decode("utf-8", "replace")
boot = h.find("boot();")
print("stray", "} finally { inflight" in h[boot:boot+90])
print("sendLine", "function sendLine" in h)
print("submit", "talk.addEventListener" in h and "submit" in h)
sc = h.split("<script>", 1)[1]
print("braces", sc.count("{"), sc.count("}"))
req = urllib.request.Request(
    "http://192.168.86.35:8765/api/v1/voice/turn",
    data=json.dumps({"text": "look", "channel": "table", "conversation": True}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)
try:
    r = urllib.request.urlopen(req, timeout=15)
    print("turn", r.status, r.read()[:200])
except Exception as e:
    print("turn FAIL", type(e).__name__, str(e)[:200])
