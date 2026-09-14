from pathlib import Path
t = Path("main.py").read_text(encoding="utf-8")
idx = 0
n = 0
while n < 12:
    i = t.find("dashboard", idx)
    if i < 0:
        break
    line_start = t.rfind("\n", 0, i) + 1
    line = t[line_start:t.find("\n", i)]
    if "run(" in line or "server" in line.lower() or "import" in line:
        print(t.count("\n", 0, i)+1, line[:200])
    idx = i + 9
    n += 1
# also search run(
for needle in ["from dashboard.server import run", "dashboard.server.run", "server.run("]:
    print("N", needle, t.find(needle))
