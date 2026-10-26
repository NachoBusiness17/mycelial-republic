"""B2-73 entropy-only pass over watch/inbox (closes the combined-run storage cap)."""
import json
import math
import os
import re

ENT = re.compile(r"[A-Za-z0-9+/_\-]{25,}")
SELF = ("B2_73_secret_scan.py", "B2_73_secret_scan_results.json",
        "B2_73_dump_census.py", "B2_73_entropy_watch.py",
        "B2_73_entropy_watch.json")


def shannon(s):
    c = {}
    for ch in s:
        c[ch] = c.get(ch, 0) + 1
    n = len(s)
    return -sum((v / n) * math.log2(v / n) for v in c.values())


out = []
total = 0
files = set()
for dirpath, dirnames, filenames in os.walk(os.path.join(".", "watch", "inbox")):
    dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", "__pycache__", ".venv")]
    for fn in filenames:
        if fn in SELF:
            continue
        p = os.path.join(dirpath, fn)
        try:
            if os.path.getsize(p) > 10 * 1024 * 1024:
                continue
            with open(p, "rb") as fh:
                raw = fh.read()
        except OSError:
            continue
        if b"\x00" in raw[:8192]:
            continue
        t = raw.decode("utf-8", errors="ignore")
        for i, line in enumerate(t.splitlines(), 1):
            if not line or len(line) > 4000:
                continue
            for m in ENT.finditer(line):
                tok = m.group()
                if len(tok) >= 25:
                    h = shannon(tok)
                    if h >= 4.3:
                        total += 1
                        files.add(p)
                        if len(out) < 5000:
                            out.append({"h": round(h, 2), "file": p.replace(os.sep, "/"),
                                        "line": i, "head": tok[:6], "len": len(tok)})
out.sort(key=lambda r: -r["h"])
print("watch/inbox entropy candidates:", total, "in", len(files), "files")
for r in out[:15]:
    print(" %.2f" % r["h"], r["file"] + ":" + str(r["line"]), r["head"], "len", r["len"])
with open("watch/inbox/burn_wave_20260926/B2_73_entropy_watch.json", "w") as fh:
    json.dump({"total": total, "files": len(files), "rows": out}, fh, indent=1)
