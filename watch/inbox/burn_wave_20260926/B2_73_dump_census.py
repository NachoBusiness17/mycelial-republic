"""B2-73 dump census: distinct exposed credential values per class, corpus only.

Byte-faithful read (utf-8 errors=replace), file-based so no shell quoting
can mangle the patterns. Values are printed masked: first 8 chars only.
Output: per-class distinct count, occurrence count, file count.
"""
import collections
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CORPUS = os.path.join(ROOT, "corpus")
WATCH = os.path.join(ROOT, "watch", "inbox")

PATS = {
    "XAI": re.compile(r"XAI_API_KEY=(xai-[A-Za-z0-9]{16})"),
    "DEEPSEEK": re.compile(r"DEEPSEEK_API_KEY=(sk-[a-f0-9]{16})"),
    "VASTAI": re.compile(r"VASTAI_API_KEY=([0-9a-f]{16})"),
    "OPENROUTER": re.compile(r"OPENROUTER_API_KEY(?:_2)?=(sk-or-v1-[a-f0-9]{16})"),
    "OPENAI": re.compile(r"OPENAI_API_KEY=(sk-proj-[A-Za-z0-9_\-]{16})"),
    "ANTHROPIC": re.compile(r"ANTHROPIC_API_KEY=(sk-ant-[A-Za-z0-9_\-]{16})"),
    "GROQ": re.compile(r"GROQ_API_KEY(?:_2)?=(gsk_[A-Za-z0-9]{16})"),
    "OPENCODE": re.compile(r"OPENCODE2?=(sk-[A-Za-z0-9_\-]{16})"),
    "XBEARER": re.compile(r"X_BearerToken=([A-Za-z0-9_\-]{16})"),
    "ZAI": re.compile(r"ZAI_API_KEY(?:_Pro|_Lite|_2|_3)?=([A-Za-z0-9]{16})"),
}

vals = {c: collections.Counter() for c in PATS}
val_files = {c: collections.defaultdict(set) for c in PATS}
walked = 0
for base in (CORPUS, WATCH):
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", "__pycache__", ".venv")]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            walked += 1
            try:
                if os.path.getsize(p) > 20 * 1024 * 1024:
                    continue
                with open(p, "rb") as fh:
                    t = fh.read().decode("utf-8", errors="replace")
            except OSError:
                continue
            for cls, rx in PATS.items():
                for m in rx.finditer(t):
                    v = m.group(1)[:8]
                    vals[cls][v] += 1
                    val_files[cls][v].add(os.path.relpath(p, ROOT).replace("\\", "/"))

print("walked", walked)
total_files = set()
for cls in PATS:
    rows = vals[cls].most_common()
    nf = len(set().union(*val_files[cls].values())) if val_files[cls] else 0
    total_files.update(f for vs in val_files[cls].values() for f in vs)
    print(cls, "distinct:", len(rows), "files:", nf,
          "occurrences:", [(v, n) for v, n in rows])
print("distinct files carrying any dump-shaped value:", len(total_files))
sys.exit(0)
