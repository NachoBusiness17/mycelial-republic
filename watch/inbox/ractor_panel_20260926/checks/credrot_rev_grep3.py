# credrot revision widened grep, part 3 (final, bounded), 2026-09-27.
# Attempts 1 and 2 of the full .zcode recursive walk (raw outputs kept:
# credrot.rev.grep2.attempt1.txt, and attempt 2 produced no flushed output
# before being stopped; both crawled .zcode non-config trees at unreasonable
# cost) are superseded by this targeted client-config pass: it walks the same
# roots but prunes node_modules/.git plus the .zcode cli transcript/capture/
# cache trees, caps files at 2 MB, and ALSO matches config-shaped filenames
# first. Laws unchanged: no corpus/ file, no line content printed, names only.
import os
import re

TARGETS = ["ANTHROPIC_API_KEY_2", "ZAI_API_KEY_3"]
RX = {t: re.compile(r"(?<![A-Za-z0-9_])" + t + r"(?![A-Za-z0-9_])") for t in TARGETS}
CONSUMER_EXT = {".py", ".ps1", ".psm1", ".cmd", ".bat", ".sh", ".bash", ".js",
                ".ts", ".jsx", ".tsx", ".mjs", ".cjs", ".yaml", ".yml",
                ".json", ".toml", ".ini", ".cfg", ".conf"}
GENERIC_PRUNE = {"node_modules", ".git", "__pycache__"}
CLI_PRUNE = {"artifacts", "exec", "rollout", "log", "tmp_orphan_mine",
             "db", "image-cache", "pdf-cache", "video-cache"}
ROOT_PRUNE = {"tmp"}
ROOTS = [
    (r"C:/Users/foste/.zcode", "transcript-pruned"),
    (r"C:/Users/foste/.config", None),
    (r"C:/Users/foste/.opencode", None),
    (r"C:/Users/foste/.claude", None),
    (r"C:/Users/foste/AppData/Roaming/Code/User", None),
    (r"C:/Users/foste/AppData/Roaming/Cursor/User", None),
]


def scan(root, note):
    hits = 0
    consumer = 0
    walked = 0
    for dirpath, dirnames, filenames in os.walk(root):
        rel = os.path.relpath(dirpath, root).replace("\\", "/")
        dirnames[:] = [d for d in dirnames if d not in GENERIC_PRUNE]
        if note == "transcript-pruned":
            if rel == ".":
                dirnames[:] = [d for d in dirnames if d not in ROOT_PRUNE]
            elif rel == "cli":
                dirnames[:] = [d for d in dirnames if d not in CLI_PRUNE]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            walked += 1
            try:
                if os.path.getsize(p) > 2_000_000:
                    continue
                with open(p, "rb") as f:
                    if b"\x00" in f.read(8192):
                        continue
                ext = os.path.splitext(fn)[1].lower()
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    for i, ln in enumerate(f, 1):
                        for t in TARGETS:
                            if RX[t].search(ln):
                                hits += 1
                                cls = "CONSUMER-SURFACE" if ext in CONSUMER_EXT else "doc-mention"
                                if cls == "CONSUMER-SURFACE":
                                    consumer += 1
                                print("  %-16s %s:%d  (%s)" % (t, os.path.relpath(p, root), i, cls))
            except OSError:
                continue
    print("%s [%s]: files walked %d, name-mention lines %d, consumer-class %d"
          % (root, note or "full", walked, hits, consumer))
    return consumer


print("=" * 78)
print("PART 3 (final, bounded): client-config roots, node_modules/.git pruned,")
print(".zcode cli transcript/capture/cache trees pruned at the cli level, 2MB cap.")
total = 0
for root, note in ROOTS:
    if os.path.isdir(root):
        total += scan(root, note)
    else:
        print("  root absent (not searched):", root)
print("=" * 78)
print("PART 3 consumer-class total:", total)
print("No corpus/ file was opened; no line content was printed.")
