# credrot revision widened grep, part 2, 2026-09-26. Part 1
# (checks/credrot.rev.grep.txt) completed the REPO walk (533 mention lines,
# 77 consumer-class) and C:/Users/foste/.codex (8 / 0) before being stopped
# inside .zcode/cli/artifacts, a session-TRANSCRIPT tree whose only observed
# hits were this panel's own tool-result JSONs quoting the candidate packets.
# This part finishes the client-CONFIG surface: .zcode with transcript trees
# (cli/artifacts, cli/exec) pruned, plus the remaining bounded roots. Same
# laws: no corpus/ file, no line content printed, names only.
import os
import re

TARGETS = ["ANTHROPIC_API_KEY_2", "ZAI_API_KEY_3"]
RX = {t: re.compile(r"(?<![A-Za-z0-9_])" + t + r"(?![A-Za-z0-9_])") for t in TARGETS}
CONSUMER_EXT = {".py", ".ps1", ".psm1", ".cmd", ".bat", ".sh", ".bash", ".js",
                ".ts", ".jsx", ".tsx", ".mjs", ".cjs", ".yaml", ".yml",
                ".json", ".toml", ".ini", ".cfg", ".conf"}
# .zcode/cli prune set (attempt 1 walked into cli/artifacts because the prune
# fired one level too late; it fires at rel == "cli" now): session/capture
# trees (artifacts, exec, rollout, log, tmp_orphan_mine) and binary caches
# (db, image-cache, pdf-cache, video-cache) leave; config files, agents/,
# plugins/, memories/ stay. At the .zcode root, tmp/ is pruned.
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


def textlike(path):
    try:
        if os.path.getsize(path) > 10_000_000:
            return False
        with open(path, "rb") as f:
            return b"\x00" not in f.read(8192)
    except OSError:
        return False


def scan(root, note):
    hits = 0
    consumer = 0
    for dirpath, dirnames, filenames in os.walk(root):
        rel = os.path.relpath(dirpath, root).replace("\\", "/")
        if note == "transcript-pruned":
            if rel == ".":
                dirnames[:] = [d for d in dirnames if d not in ROOT_PRUNE]
            elif rel == "cli":
                dirnames[:] = [d for d in dirnames if d not in CLI_PRUNE]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            if not textlike(p):
                continue
            ext = os.path.splitext(fn)[1].lower()
            try:
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    for i, ln in enumerate(f, 1):
                        for t in TARGETS:
                            if RX[t].search(ln):
                                hits += 1
                                cls = "CONSUMER-SURFACE" if ext in CONSUMER_EXT else "doc-mention"
                                if cls == "CONSUMER-SURFACE":
                                    consumer += 1
                                if hits <= 200:
                                    print("  %-16s %s:%d  (%s)" % (t, os.path.relpath(p, root), i, cls))
            except OSError:
                continue
    print("%s [%s]: total name-mention lines %d, of which consumer-class %d" % (root, note or "full", hits, consumer))
    return consumer


print("=" * 78)
print("PART 2 (attempt 2): client-config roots, transcript/capture trees pruned")
print("at the cli level. Part 1 already covered REPO and .codex; attempt 1 of")
print("this part (credrot.rev.grep2.attempt1.txt) stopped inside cli/artifacts.")
print("cli-level prune set:", sorted(CLI_PRUNE))
total = 0
for root, note in ROOTS:
    if os.path.isdir(root):
        total += scan(root, note)
    else:
        print("  root absent (not searched):", root)
print("=" * 78)
print("PART 2 consumer-class total:", total)
print("Excluded by design: .zcode cli transcript/capture/cache trees named in")
print("CLI_PRUNE (2043 session dirs live under cli/artifacts alone; part 1 and")
print("attempt 1 both observed their only hits quoting this panel's artifacts).")
print("No corpus/ file was opened; no line content was printed.")
