from pathlib import Path
h = Path("dashboard/static/wave.html").read_text(encoding="utf-8")
print("len", len(h))
for needle in ["id=\"talk\"", "submit", "finally", "inflight", "voice/turn", "function send", "ptt"]:
    print("HAS", needle, h.find(needle))
print("==== LAST 2200 ====")
print(h[-2200:])
print("==== REFRESH CHUNK ====")
i = h.find("let inflight")
print(h[i:i+1800] if i>=0 else "no inflight")
