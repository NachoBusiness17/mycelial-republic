import json, os, time, urllib.request

def hit(url, timeout=4):
    t0 = time.time()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            b = r.read(180)
        return round(time.time()-t0, 3), r.status, b[:80]
    except Exception as e:
        return round(time.time()-t0, 3), type(e).__name__, str(e)[:100]

print("GET /", hit("http://127.0.0.1:8765/"))
print("GET /table", hit("http://127.0.0.1:8765/table"))
print("GET /wave", hit("http://127.0.0.1:8765/wave"))
print("GET /api/v1/game", hit("http://127.0.0.1:8765/api/v1/game"))
print("GET view", hit("http://127.0.0.1:8765/api/v1/table/view", timeout=6))

print("---procs---")
for pid in os.listdir("/proc"):
    if not pid.isdigit():
        continue
    try:
        cmd = open(f"/proc/{pid}/cmdline", "rb").read().replace(b"\x00", b" ").decode("utf-8", "replace")
    except Exception:
        continue
    if "dashboard" in cmd or "mag_launch" in cmd:
        st = open(f"/proc/{pid}/status").read()
        rss = threads = state = "?"
        for line in st.splitlines():
            if line.startswith("VmRSS:"):
                rss = line
            if line.startswith("Threads:"):
                threads = line
            if line.startswith("State:"):
                state = line
        print(pid, state, rss, threads, cmd[:100])
