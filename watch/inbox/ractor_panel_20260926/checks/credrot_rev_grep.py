# credrot revision widened consumer grep, 2026-09-26. The survivor's rows 1-2
# zero-blast retirement claims rested on a py-only grep (mag/ tools/ scripts/
# main.py). This widens the surface to every repo text file (corpus/ pruned,
# HARD LAW) plus the bounded out-of-repo client-config roots, across all file
# types, for ANTHROPIC_API_KEY_2 and ZAI_API_KEY_3. Output prints path, line
# number, matched NAME, and a consumer/doc classification only. Line CONTENT is
# never printed (the .env line would carry a value). No corpus/ file is opened.
import os
import re

REPO = r"C:/Users/foste/Documents/projects/local_sovereign_agent"
TARGETS = ["ANTHROPIC_API_KEY_2", "ZAI_API_KEY_3"]
PRUNE_DIRS = {"corpus", ".git", ".venv", "node_modules", "__pycache__",
              ".pytest_cache", ".ruff_cache", ".mypy_cache", ".idea", ".vs"}
OUT_ROOTS = [
    r"C:/Users/foste/.codex",
    r"C:/Users/foste/.zcode",
    r"C:/Users/foste/.config",
    r"C:/Users/foste/.opencode",
    r"C:/Users/foste/.claude",
    r"C:/Users/foste/AppData/Roaming/Code/User",
    r"C:/Users/foste/AppData/Roaming/Cursor/User",
]
CONSUMER_EXT = {".py", ".ps1", ".psm1", ".cmd", ".bat", ".sh", ".bash", ".js",
                ".ts", ".jsx", ".tsx", ".mjs", ".cjs", ".yaml", ".yml",
                ".json", ".toml", ".ini", ".cfg", ".conf"}
RX = {t: re.compile(r"(?<![A-Za-z0-9_])" + t + r"(?![A-Za-z0-9_])") for t in TARGETS}


def textlike(path):
    try:
        size = os.path.getsize(path)
        if size > 10_000_000:
            return False
        with open(path, "rb") as f:
            head = f.read(8192)
        if b"\x00" in head:
            return False
        return True
    except OSError:
        return False


def scan(root, label):
    hits = 0
    consumer_hits = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in PRUNE_DIRS]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            if os.path.abspath(p) == os.path.join(REPO, ".env"):
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    for i, ln in enumerate(f, 1):
                        for t in TARGETS:
                            if RX[t].search(ln):
                                print("  [ENV-PRESENCE] root .env line %d declares %s (value not printed)" % (i, t))
                continue
            if not textlike(p):
                continue
            ext = os.path.splitext(fn)[1].lower()
            try:
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    for i, ln in enumerate(f, 1):
                        for t in TARGETS:
                            if RX[t].search(ln):
                                cls = "CONSUMER-SURFACE" if ext in CONSUMER_EXT else "doc-mention"
                                hits += 1
                                if cls == "CONSUMER-SURFACE":
                                    consumer_hits += 1
                                if hits <= 400:
                                    print("  %-16s %s:%d  (%s)" % (t, os.path.relpath(p, root), i, cls))
            except OSError:
                continue
    print("%s: total name-mention lines %d, of which consumer-class %d" % (label, hits, consumer_hits))
    return consumer_hits


print("=" * 78)
print("WIDENED CONSUMER GREP for ANTHROPIC_API_KEY_2 / ZAI_API_KEY_3")
print("consumer-class extensions:", sorted(CONSUMER_EXT))
print("pruned dirs:", sorted(PRUNE_DIRS))
print("-- repo walk (all text files, corpus/ pruned, HARD LAW held)")
c1 = scan(REPO, "REPO")
print("-- out-of-repo client-config roots (bounded list; existence reported)")
c2 = 0
for r in OUT_ROOTS:
    if os.path.isdir(r):
        print("  root searched:", r)
        c2 += scan(r, "  " + r)
    else:
        print("  root absent (not searched):", r)
print("=" * 78)
print("VERDICT: consumer-class hits outside root .env name declarations:", c1 + c2)
print("(0 = rows 1-2 retirement claim survives the widened grep this run;")
print(" any hit = the corresponding row demotes to a chassis R0-R3 rotation)")
print("No corpus/ file was opened; no line content was printed.")
