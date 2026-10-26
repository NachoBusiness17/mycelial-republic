#!/usr/bin/env python
# cross-librarian probe 2: inventory each candidate fleet surface dir (files + mtimes),
# plus check memory/frontier for a 2026-10-02 olm digest and ABLITERATUS mtime.
import os, time

ROOT = r"C:/Users/foste/Documents/projects/local_sovereign_agent"
INBOX = os.path.join(ROOT, "watch", "inbox")

DIRS = ["music", "salon_mine", "ractor_engine", "gap_analysis_20261001", "fillball",
        "model_garden", "48h_synth", "localfirst", "spiking_wide",
        "frontier_olm_2026-09-30", "frontier_olm_2026-10-01", "librarian_exp",
        "ractor50", os.path.join("gala_20260925")]

for d in DIRS:
    p = os.path.join(INBOX, d)
    print("=== " + d + " ===")
    if not os.path.isdir(p):
        print("  MISSING")
        continue
    for dirpath, dirnames, filenames in os.walk(p):
        rel = os.path.relpath(dirpath, p)
        if rel != ".":
            print("  [dir] " + rel.replace("\\", "/"))
        for fn in sorted(filenames):
            fp = os.path.join(dirpath, fn)
            try:
                st = os.stat(fp)
                sz = st.st_size
                mt = time.strftime("%m-%dT%H:%MZ", time.gmtime(st.st_mtime))
            except OSError:
                sz, mt = -1, "?"
            print("  %-52s %10d  %s" % ((rel.replace("\\", "/") + "/" if rel != "." else "") + fn, sz, mt))
    print()

print("=== memory/frontier (today's olm?) ===")
fr = os.path.join(ROOT, "memory", "frontier")
if os.path.isdir(fr):
    for dirpath, dirnames, filenames in os.walk(fr):
        for fn in sorted(filenames):
            fp = os.path.join(dirpath, fn)
            st = os.stat(fp)
            mt = time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(st.st_mtime))
            print("  %-60s %10d  %s" % (os.path.relpath(fp, ROOT).replace("\\", "/"), st.st_size, mt))

print()
print("=== drop receipt mtimes ===")
for fn in ["ABLITERATUS_DROP_20260929.md", "SPIKINGBRAIN_DROP_20261001.md", "STRATA_DROP_20261001.md",
           "DOUBLE_DROP_20261001.md", "x_intel_drop_20261001.md", "x_intel_deepgemm_20261001.md",
           "model_mating_paper_dig_20261001.md", "LOCALFIRST_MEMORY_LANDSCAPE_20261001.md"]:
    fp = os.path.join(INBOX, fn)
    if os.path.isfile(fp):
        st = os.stat(fp)
        print("  %-48s %10d  %s" % (fn, st.st_size, time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(st.st_mtime))))
    else:
        print("  %-48s MISSING" % fn)
