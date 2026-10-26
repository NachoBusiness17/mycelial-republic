# s2-05 follow-up stats: zero-public-def files, line distribution, subpackage split.
import ast
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
MAG = os.path.join(ROOT, "mag")

files = []
for dirpath, dirnames, filenames in os.walk(MAG, onerror=lambda e: None):
    dirnames[:] = [d for d in dirnames if d != "__pycache__"]
    for fn in filenames:
        if fn.endswith(".py"):
            files.append(os.path.join(dirpath, fn))

zero_pub = 0
zero_defs = 0
lines_list = []
top_level = 0
subdir = {}
for p in files:
    r = os.path.relpath(p, ROOT).replace("\\", "/")
    parts = r.split("/")
    key = parts[1] if len(parts) > 2 else "(top-level)"
    subdir[key] = subdir.get(key, 0) + 1
    if len(parts) == 2:
        top_level += 1
    try:
        text = io.open(p, "r", encoding="utf-8", errors="replace").read()
    except OSError:
        continue
    lines_list.append(len(text.splitlines()))
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        continue
    npub = 0
    ndef = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            ndef += 1
            if not node.name.startswith("_"):
                npub += 1
    if npub == 0:
        zero_pub += 1
    if ndef == 0:
        zero_defs += 1

lines_list.sort()
n = len(lines_list)


def pct(q):
    i = min(n - 1, int(q * n))
    return lines_list[i]


print("files:", n)
print("top_level_files:", top_level)
print("subdir_split:", subdir)
print("files_zero_public_defs:", zero_pub)
print("files_zero_defs_any:", zero_defs)
print("median_lines:", lines_list[n // 2])
print("p90_lines:", pct(0.90))
print("p99_lines:", pct(0.99))
print("avg_lines:", round(sum(lines_list) / n, 1))
print("min_lines:", lines_list[0])
print("empty_files(0 lines):", sum(1 for x in lines_list if x == 0))
