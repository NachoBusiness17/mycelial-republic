from pathlib import Path
h = Path("dashboard/static/wave.html").read_text(encoding="utf-8")
for i,line in enumerate(h.splitlines(),1):
    if any(x in line for x in ("function send", "sendLine", "talk.addEventListener", "form", "async function ptt", "function boot", "setInterval", "finally")):
        print(f"{i}:{line.rstrip()[:140]}")
