"""D24 triage probe — rebuild pure-dead module list from disk (no git).

Read-only except this file. Outputs JSON to stdout -> captured by caller.
Import graph via AST + conservative token fallback (grep -L style).
"""
import ast
import json
import os
import re
import sys
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
os.chdir(ROOT)

EXCLUDE_DIR_NAMES = {"__pycache__", ".venv", "node_modules", ".git", "memory",
                     "watch", "queue", "archive", ".mimosa", "mine", "biography_backup"}

def py_files_under(rel):
    out = []
    base = os.path.join(ROOT, rel)
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in ("__pycache__",)]
        for fn in filenames:
            if fn.endswith(".py"):
                out.append(os.path.join(dirpath, fn))
    return out

# ---- module inventory: mag package ----
mag_files = py_files_under("mag")          # includes mag/, mag/cli, mag/tests, mag/ontology_compiler
mod_by_name = {}                            # short name -> relpath (flat mag/ wins)
mod_dotted = {}                             # dotted (mag.x) -> relpath
for fp in mag_files:
    rel = os.path.relpath(fp, ROOT).replace("\\", "/")
    dotted = rel[:-3].replace("/", ".")
    short = dotted.split(".")[-1]
    mod_by_name.setdefault(short, rel)
    mod_dotted[dotted] = rel

# ---- code corpus to scan for references ----
corpus = list(mag_files)
for rel in ["scripts", "tests", "dashboard", "backend"]:
    corpus.extend(py_files_under(rel))
for fn in os.listdir(ROOT):
    if fn.endswith(".py"):
        corpus.append(os.path.join(ROOT, fn))

importers = {m: set() for m in mod_dotted}   # dotted -> set of importer relpaths
token_refs = {m: set() for m in mod_dotted}  # dotted -> set of files containing short name
edges = {m: set() for m in mod_dotted}       # dotted -> imported dotted names (for BFS)

for fp in corpus:
    rel = os.path.relpath(fp, ROOT).replace("\\", "/")
    try:
        src = open(fp, encoding="utf-8", errors="replace").read()
    except OSError:
        continue
    try:
        tree = ast.parse(src)
    except SyntaxError:
        tree = None
    if tree:
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    top = a.name.split(".")[0]
                    if a.name in mod_dotted:
                        importers[a.name].add(rel)
                    if top in mod_by_name and mod_by_name[top].split("/")[0] in ("mag",):
                        # bare `import x` where mag/x.py exists (dir-on-path style)
                        target = mod_by_name[top]
                        dotted_t = target[:-3].replace("/", ".")
                        importers[dotted_t].add(rel)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    if node.module in mod_dotted:
                        importers[node.module].add(rel)
                    parts = node.module.split(".")
                    top = parts[0]
                    if top == "mag" and len(parts) >= 2:
                        cand = ".".join(parts[:2])
                        if cand in mod_dotted:
                            importers[cand].add(rel)
                    elif top in mod_by_name:
                        dotted_t = mod_by_name[top][:-3].replace("/", ".")
                        importers[dotted_t].add(rel)
                    # `from mag import foo, bar`
                    if node.module == "mag":
                        for a in node.names:
                            if a.name in mod_by_name:
                                dotted_t = mod_by_name[a.name][:-3].replace("/", ".")
                                importers[dotted_t].add(rel)
    # token fallback: short name as word in any other file
    for name, relp in mod_by_name.items():
        if re.search(r"\b%s\b" % re.escape(name), src):
            dotted_t = relp[:-3].replace("/", ".")
            token_refs[dotted_t].add(rel)

def rel_note(r):
    return r

pure_dead, token_only, ast_alive = [], [], []
for dotted, relp in sorted(mod_dotted.items()):
    own = relp
    imp = {i for i in importers[dotted] if i != own}
    tok = {t for t in token_refs[dotted] if t != own}
    if imp:
        ast_alive.append(dotted)
    elif tok:
        token_only.append(dotted)
    else:
        pure_dead.append(dotted)

# ---- reachability from entrypoints ----
ENTRYPOINTS = ["main.py", "mag_launch.py", "dashboard/server.py", "backend/server.py",
               "dashboard/rest.py"]
reach = set()
frontier = [e for e in ENTRYPOINTS if os.path.exists(os.path.join(ROOT, e))]
seen_files = set(frontier)
while frontier:
    fp = frontier.pop()
    rel = os.path.relpath(fp, ROOT).replace("\\", "/")
    try:
        tree = ast.parse(open(fp, encoding="utf-8", errors="replace").read())
    except Exception:
        continue
    for node in ast.walk(tree):
        targets = []
        if isinstance(node, ast.Import):
            targets = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            targets = [node.module]
            if node.module == "mag":
                targets += [a.name for a in node.names]
        for t in targets:
            cands = []
            if t in mod_dotted:
                cands.append(t)
            top = t.split(".")[0]
            if top in mod_by_name:
                cands.append(mod_by_name[top][:-3].replace("/", "."))
            if t == "mag" or t.startswith("mag."):
                parts = t.split(".")
                if len(parts) >= 2 and ".".join(parts[:2]) in mod_dotted:
                    cands.append(".".join(parts[:2]))
            for c in cands:
                if c not in reach:
                    reach.add(c)
                    nf = os.path.join(ROOT, mod_dotted[c].replace("/", os.sep))
                    if nf not in seen_files:
                        seen_files.add(nf)
                        frontier.append(nf)

core_unreachable = [d for d in mod_dotted if d not in reach and d not in pure_dead]

# ---- tests ----
test_files = []
for fp in py_files_under("tests") + py_files_under("mag/tests"):
    rel = os.path.relpath(fp, ROOT).replace("\\", "/")
    test_files.append(rel)

def test_target(rel):
    b = os.path.basename(rel)[:-3]
    b = re.sub(r"^test_", "", b)
    b = re.sub(r"_test$", "", b)
    return b

orphaned_tests = []
for tf in test_files:
    tgt = test_target(tf)
    dotted = mod_by_name.get(tgt)
    if dotted:
        dd = dotted[:-3].replace("/", ".")
        if dd in pure_dead:
            orphaned_tests.append((tf, dd))

tested_modules = set()
tests_text = []
for tf in test_files:
    try:
        tests_text.append(open(os.path.join(ROOT, tf), encoding="utf-8", errors="replace").read())
    except OSError:
        pass
tests_blob = "\n".join(tests_text)
for name, relp in mod_by_name.items():
    if re.search(r"\b%s\b" % re.escape(name), tests_blob):
        tested_modules.add(relp[:-3].replace("/", "."))

# ---- mtimes (git forbidden -> mtime proxy) ----
def mtime_date(dotted):
    fp = os.path.join(ROOT, mod_dotted[dotted].replace("/", os.sep))
    return datetime.fromtimestamp(os.path.getmtime(fp)).strftime("%Y-%m-%d")

zero_importer_giants = []
for dotted in pure_dead + token_only:
    fp = os.path.join(ROOT, mod_dotted[dotted].replace("/", os.sep))
    try:
        n = len(open(fp, encoding="utf-8", errors="replace").read().splitlines())
    except OSError:
        n = 0
    if n >= 150:
        zero_importer_giants.append((dotted, n))

out = {
    "generated": datetime.now().isoformat(timespec="seconds"),
    "module_total": len(mod_dotted),
    "ast_alive": len(ast_alive),
    "token_only": len(token_only),
    "pure_dead_count": len(pure_dead),
    "core_reachable": len(reach & set(mod_dotted)),
    "core_unreachable_alive": len(core_unreachable),
    "tested_modules": len(tested_modules),
    "coverage_pct": round(100.0 * len(tested_modules) / len(mod_dotted), 1),
    "test_files": len(test_files),
    "orphaned_tests": orphaned_tests,
    "pure_dead": pure_dead,
    "token_only": token_only,
    "zero_importer_giants": sorted(zero_importer_giants, key=lambda x: -x[1])[:30],
    "pure_dead_mtime": {d: mtime_date(d) for d in pure_dead[:200]},
    "token_only_mtime": {d: mtime_date(d) for d in token_only[:200]},
    "core_unreachable_sample": core_unreachable[:40],
}
json.dump(out, open(os.path.join(ROOT, "watch/inbox/wave_20260916/d24_triage_probe_out.json"), "w", encoding="utf-8"), indent=1)
print("total", out["module_total"], "| ast_alive", out["ast_alive"], "| token_only",
      out["token_only"], "| pure_dead", out["pure_dead_count"], "| core_reach",
      out["core_reachable"], "| tested", out["tested_modules"], f"({out['coverage_pct']}%)",
      "| test_files", out["test_files"], "| orphaned_tests", len(orphaned_tests))
