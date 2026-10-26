"""Cycle 8 inventory: corpus/tools shelf, measured from disk.

Estate-authored vs vendored split, per-subdir census, extension census, archive sizes.
Writes logs/mates/cartographer/tools_inventory.json.
"""
import json
import os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SHELF = os.path.join(ROOT, "corpus", "tools")
OUT = os.path.join(ROOT, "logs", "mates", "cartographer", "tools_inventory.json")

def census(root):
    files = 0
    bytes_total = 0
    lines_total = 0
    by_ext = defaultdict(lambda: [0, 0])
    for dirpath, dirnames, filenames in os.walk(root):
        for name in filenames:
            p = os.path.join(dirpath, name)
            try:
                st = os.stat(p)
            except OSError:
                continue
            files += 1
            bytes_total += st.st_size
            ext = os.path.splitext(name)[1].lower() or "(none)"
            by_ext[ext][0] += 1
            by_ext[ext][1] += st.st_size
            if ext in (".py", ".java", ".md", ".txt", ".json", ".xml", ".gradle", ".cfg", ".ini", ".ps1", ".bat", ".sh", ".properties", ".yml", ".yaml", ".toml"):
                try:
                    with open(p, "rb") as f:
                        lines_total += sum(1 for _ in f)
                except OSError:
                    pass
    return {
        "files": files,
        "bytes": bytes_total,
        "readable_lines_counted": lines_total,
        "by_ext": {k: {"count": v[0], "bytes": v[1]} for k, v in sorted(by_ext.items(), key=lambda kv: -kv[1][0])},
    }

result = {"shelf": "corpus/tools", "measured": [], "top_files": [], "archives": []}
total_files = 0
total_bytes = 0
for entry in sorted(os.listdir(SHELF)):
    p = os.path.join(SHELF, entry)
    st = os.stat(p)
    if os.path.isdir(p):
        c = census(p)
        result["measured"].append({"name": entry, "type": "dir", **c})
        total_files += c["files"]
        total_bytes += c["bytes"]
    else:
        result["top_files"].append({"name": entry, "type": "file", "bytes": st.st_size})
        total_files += 1
        total_bytes += st.st_size
        if entry.endswith(".zip"):
            result["archives"].append({"name": entry, "bytes": st.st_size})

result["totals"] = {"files": total_files, "bytes": total_bytes}

# smoke scripts: bytes + lines, full read is done separately
for name in ("GhidraSmokeJava.java", "ghidra_smoke.py"):
    p = os.path.join(SHELF, name)
    if os.path.exists(p):
        with open(p, "rb") as f:
            data = f.read()
        result.setdefault("smoke_scripts", []).append({
            "name": name,
            "bytes": len(data),
            "lines": data.count(b"\n") + (0 if data.endswith(b"\n") or not data else 1),
        })

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=1)
print(json.dumps({k: result[k] for k in ("totals", "smoke_scripts", "archives")}, indent=1))
for m in result["measured"]:
    print(m["name"], m["type"], "files:", m["files"], "bytes:", m["bytes"], "lines:", m.get("readable_lines_counted", 0))
