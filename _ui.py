from pathlib import Path
h = Path("dashboard/static/wave.html").read_text(encoding="utf-8")
# css + structure
print(h[:2200])
print("==== BODY ====")
i = h.find("<body")
print(h[i:i+1800])
