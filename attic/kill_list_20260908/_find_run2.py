from pathlib import Path
t = Path("main.py").read_text(encoding="utf-8")
i = t.find("from dashboard.server import run as run_dashboard")
print(t[i:i+1200])
