#!/usr/bin/env python
# cross-librarian probe 1: enumerate fleet surfaces (watch/inbox) with last-48h activity,
# and locate the music program's receipts. Read-only listing, no content edits.
import os, json, time

ROOT = r"C:/Users/foste/Documents/projects/local_sovereign_agent"
INBOX = os.path.join(ROOT, "watch", "inbox")
CUTOFF = time.time() - 48 * 3600

entries = []
for name in sorted(os.listdir(INBOX)):
    p = os.path.join(INBOX, name)
    try:
        st = os.stat(p)
    except OSError:
        continue
    entries.append({"name": name, "is_dir": os.path.isdir(p),
                    "mtime": st.st_mtime, "mtime_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(st.st_mtime)),
                    "fresh48h": st.st_mtime >= CUTOFF})

fresh = [e for e in entries if e["fresh48h"]]
print("=== watch/inbox entries with mtime in last 48h (%d of %d) ===" % (len(fresh), len(entries)))
for e in sorted(fresh, key=lambda x: x["mtime"]):
    print(("DIR  " if e["is_dir"] else "FILE ") + e["mtime_iso"] + "  " + e["name"])

print()
print("=== name contains music (any age) ===")
for e in entries:
    if "music" in e["name"].lower():
        print(("DIR  " if e["is_dir"] else "FILE ") + e["mtime_iso"] + "  " + e["name"])

print()
print("=== grep music in watch/inbox *.md filenames' contents is expensive; instead list dirs for known fleet names ===")
for probe in ["gap", "fillball", "fill_ball", "salon", "ractor", "gala_20260925", "librarian_exp",
              "frontier_olm_2026-10-02", "frontier_olm", "ouroboros", "GAP_REGISTER"]:
    hits = [e["name"] for e in entries if probe.lower() in e["name"].lower()]
    if hits:
        print(probe + ": " + ", ".join(hits[:10]))
