from pathlib import Path
# tunnel tail
tp = Path(r"C:\Users\foste\terminals\583479.txt")
if tp.exists():
    t = tp.read_text(encoding="utf-8", errors="replace")
    print("TUNNEL len", len(t), "trycloudflare", "trycloudflare.com" in t)
    print(t[-800:])
else:
    print("no tunnel log")
print("==== STT ====")
import urllib.request, json
# stt endpoint on LAN http
req = urllib.request.Request("http://192.168.86.35:8765/api/v1/voice/stt", data=b'{"data":"","filename":"x.webm"}', headers={"Content-Type":"application/json"}, method="POST")
try:
    r = urllib.request.urlopen(req, timeout=8)
    print("stt", r.status, r.read()[:200])
except Exception as e:
    print("stt", type(e).__name__, str(e)[:250])
h = urllib.request.urlopen("http://192.168.86.35:8765/wave", timeout=5).read().decode("utf-8","replace")
print("wave ptt", 'id="ptt"' in h, "getUserMedia" in h, "capture" in h)
print("voice html", urllib.request.urlopen("http://192.168.86.35:8765/voice", timeout=5).status)
