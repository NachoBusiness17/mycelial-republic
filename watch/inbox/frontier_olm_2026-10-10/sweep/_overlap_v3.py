"""Final overlap scan v3 (2026-10-10): complete walk of watch/inbox + memory.

v2 crashed on a '\\\\.\\nul' mount artifact (ValueError in os.path.relpath).
v3 skips any path whose relpath raises, and scans the surviving candidate set:
the three read-and-possibly-clean items plus October alternates not yet read.
Catalog (all rows) and state/arxiv were fully grepped earlier this session and
are NOT rescanned here. Read-only; no subprocess spawns.
"""
import os

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
SCAN_DIRS = [os.path.join(ROOT, "watch", "inbox"), os.path.join(ROOT, "memory")]

TOKENS = [
    # read, possibly clean
    "2610.02766", "prefix-cache retention",
    "2610.11358", "rarecache",
    "2609.34432", "agent serving at production scale",
    # unread October alternates
    "2610.06479", "behavior-preserving kv",
    "2610.08378", "lachesis",
    "2609.34060", "kvcmas",
    "2610.03088",
    "2610.07643", "lore-kv",
    "2609.36938", "janus:",
    "2610.11784",
    "2610.12133", "attic-kv",
    "2610.07782",
]

low = {t.lower() for t in TOKENS}
hits = 0
files_scanned = 0
for d in SCAN_DIRS:
    for dirpath, dirs, files in os.walk(d):
        for fn in files:
            p = os.path.join(dirpath, fn)
            try:
                rel = os.path.relpath(p, ROOT)
            except ValueError:
                continue  # NUL-mount / cross-drive artifacts
            if not fn.lower().endswith((".md", ".txt", ".json", ".jsonl", ".html")):
                continue
            files_scanned += 1
            try:
                with open(p, encoding="utf-8", errors="replace") as f:
                    for ln, line in enumerate(f, 1):
                        ll = line.lower()
                        for t in low:
                            if t in ll:
                                print(f"HIT {t!r} -> {rel}:{ln}: {line.strip()[:140]}")
                                hits += 1
            except OSError:
                pass
print(f"V3_FILES_SCANNED {files_scanned}")
print(f"V3_FS_HITS {hits}")

print("=== frontier_olm sibling dirs ===")
wi = os.path.join(ROOT, "watch", "inbox")
for name in sorted(os.listdir(wi)):
    if name.startswith("frontier_olm"):
        print(" ", name)
