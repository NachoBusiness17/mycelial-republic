import sys, os, json, re, datetime
sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def mt(p):
    return datetime.datetime.fromtimestamp(os.path.getmtime(p), datetime.timezone.utc).isoformat()

print("\n=== JUDGE PASS 3, machine now:", now(), "===")

# 1: flash-lane burn receipt existence + FLEET_IMPRINT mtime + LINKS row ts
print("\n=== P3.1 width-24 run records ===")
for rel in (
    r"watch\inbox\flash-lane-burn-20260926.md",
    r"watch\flash-lane-burn-20260926.md",
    r"watch\inbox\FLEET_IMPRINT_20260917.md",
):
    p = os.path.join(ROOT, rel)
    print(rel, "exists:", os.path.exists(p), ("mtime: " + mt(p)) if os.path.exists(p) else "")
lp = os.path.join(ROOT, "watch", "inbox", "LINKS.jsonl")
with open(lp, encoding="utf-8", errors="replace") as f:
    for line in f:
        if "width-24" in line or "1302 wall" in line:
            print("LINKS row:", line.strip()[:420])

# 2: bounded .zcode exec search for dispatcher-era lane deaths
print("\n=== P3.2 .zcode cli/exec bounded search ===")
ZC = r"C:\Users\foste\.zcode\cli\exec"
if not os.path.isdir(ZC):
    print(ZC, "(missing)")
else:
    sessions = sorted(os.listdir(ZC))
    print("session dirs:", len(sessions))
    lo = datetime.datetime(2026, 9, 26, 22, 0, tzinfo=datetime.timezone.utc).timestamp()
    hi = datetime.datetime(2026, 9, 27, 0, 40, tzinfo=datetime.timezone.utc).timestamp()
    scanned = 0
    hits = []
    for s in sessions:
        d = os.path.join(ZC, s)
        if not os.path.isdir(d):
            continue
        try:
            if not (lo <= os.path.getmtime(d) <= hi + 3600 * 6):
                # only dirs whose own mtime falls in or after the window
                if os.path.getmtime(d) < lo:
                    continue
        except Exception:
            continue
        for fn in os.listdir(d):
            p = os.path.join(d, fn)
            try:
                if os.path.getsize(p) > 30 * 1024 * 1024:
                    continue
                scanned += 1
                with open(p, encoding="utf-8", errors="replace") as f:
                    txt = f.read()
            except Exception:
                continue
            if "1302" in txt and ("B2-155" in txt or "B2-475" in txt or "width-24" in txt):
                hits.append((p, txt.count("1302"), "B2-155" in txt, "B2-475" in txt, "width-24" in txt))
    print("files scanned:", scanned, "| co-hit files:", len(hits))
    for p, n, a, b, c in hits[:15]:
        print("HIT:", p, "1302x", n, "B2-155:", a, "B2-475:", b, "width-24:", c)

print("\nmachine now (end pass 3):", now())
print("=== END PASS 3 ===")
