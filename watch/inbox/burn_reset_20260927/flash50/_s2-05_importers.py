# s2-05 import-graph pass 2: live-tree vs repo-wide importer counts.
# Live tree = importers under mag/, tools/, tests/, scripts/ or top-level .py.
import ast
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
SKIP_DIRS = {"node_modules", "__pycache__"}
LIVE_PREFIXES = ("mag/", "tools/", "tests/", "scripts/")


def walk_py_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT, onerror=lambda e: None):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".py"):
                out.append(os.path.join(dirpath, fn))
    return out


def read_text(path):
    with io.open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


def mod_name_for(mag_rel):
    parts = mag_rel.split("/")
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1][:-3]
    return ".".join(parts)


all_py = walk_py_files()
mag_py = [p for p in all_py if rel(p).startswith("mag/")]
mag_modules = {mod_name_for(rel(p)): rel(p) for p in mag_py}

importers_all = {}
importers_live = {}
stmt_live = {}
for p in all_py:
    r = rel(p)
    try:
        text = read_text(p)
    except OSError:
        continue
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        continue
    is_live = r.startswith(LIVE_PREFIXES) or "/" not in r
    cur_pkg = r.split("/")[:-1]
    touched = set()

    def touch(name):
        if name in mag_modules:
            touched.add(name)

    def touch_prefixes(dotted):
        comps = dotted.split(".")
        for i in range(1, len(comps) + 1):
            touch(".".join(comps[:i]))

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                touch_prefixes(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                base = node.module or ""
            else:
                idx = len(cur_pkg) - (node.level - 1)
                if idx < 0:
                    continue
                base = ".".join(cur_pkg[:idx])
                if node.module:
                    base = (base + "." + node.module) if base else node.module
            if base:
                touch_prefixes(base)
            for alias in node.names:
                if alias.name == "*":
                    continue
                full = (base + "." + alias.name) if base else alias.name
                touch(full)
        elif isinstance(node, ast.Call):
            fn = node.func
            fname = fn.attr if isinstance(fn, ast.Attribute) else (fn.id if isinstance(fn, ast.Name) else "")
            if fname in ("import_module", "__import__") and node.args:
                a0 = node.args[0]
                if isinstance(a0, ast.Constant) and isinstance(a0.value, str) and (a0.value == "mag" or a0.value.startswith("mag.")):
                    touch_prefixes(a0.value)
    for m in touched:
        importers_all.setdefault(m, set()).add(r)
        if is_live:
            importers_live.setdefault(m, set()).add(r)
            stmt_live[m] = stmt_live.get(m, 0) + 1

rows = []
for m, f in mag_modules.items():
    if f.endswith("/__init__.py"):
        continue
    rows.append({
        "module": m,
        "file": f,
        "live": len(importers_live.get(m, set())),
        "all": len(importers_all.get(m, set())),
        "touches_live": stmt_live.get(m, 0),
    })

most_live = sorted(rows, key=lambda x: (-x["live"], -x["touches_live"], x["module"]))[:15]
never_live = sorted([x for x in rows if x["live"] == 0 and x["all"] == 0], key=lambda x: x["module"])
never_live_but_archived = sorted([x for x in rows if x["live"] == 0 and x["all"] > 0], key=lambda x: x["module"])
print("repo_py_scanned:", len(all_py))
print("== MOST IMPORTED (live-tree importers) 15 ==")
for x in most_live:
    print(f"live={x['live']:4d} all={x['all']:4d} touches={x['touches_live']:4d} {x['module']}")
print("never_imported (live==0 AND all==0):", len(never_live))
print("imported ONLY by archived copies (live==0, all>0):", len(never_live_but_archived))
for x in never_live_but_archived[:30]:
    print("  arch-only:", x["module"], "all=", x["all"])
out = {
    "most_imported_live": most_live,
    "never_live_and_all": [x["module"] for x in never_live],
    "archived_only": [(x["module"], x["all"]) for x in never_live_but_archived],
}
with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s2-05_raw2.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
print("RAW2_JSON written")
