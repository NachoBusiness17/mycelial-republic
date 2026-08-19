from pathlib import Path
t = Path(r"C:\Users\foste\terminals\583479.txt").read_text(encoding="utf-8", errors="replace")
for line in t.splitlines():
    if "trycloudflare" in line.lower() or "https://" in line and "cloudflare" in line.lower():
        print(line[:240])
print("--- header ---")
print("\n".join(t.splitlines()[:15]))
print("status", "exit" in t[-200:], t[-300:])
