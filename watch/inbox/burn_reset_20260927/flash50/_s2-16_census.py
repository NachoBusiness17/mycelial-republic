# s2-16 import census scanner v4 (FINAL classification). Read-only. No subprocess calls.
# Precedence: stdlib > repo-root-local (py-bearing top dir or root py stem)
#           > installed-distribution import name > archive-local (py-bearing name anywhere)
#           > unresolved.
# Banked from the session copy at C:/Users/foste/AppData/Local/Temp/s2_16_import_census_v4.py
# (byte-equivalent logic; run from repo root with .venv/Scripts/python.exe).
import ast
import json
import os
import re
import sys
from collections import Counter, defaultdict
from importlib import metadata

ROOT = os.path.abspath(os.getcwd())
OUT_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s2-16_data.json")

SKIP_DIR_NAMES = {"__pycache__", "node_modules", ".git", ".venv", "venv"}
CODE_EXTS = {".py", ".ps1", ".psm1", ".bat", ".cmd", ".sh"}
RUNTIME_TOPS = {".", "mag", "tools", "tests", "scripts", "dashboard", "dashboard-deploy"}

unreadable_dirs = []
py_files = []
code_text_files = []
top_dir_py_counts = Counter()

for dirpath, dirnames, filenames in os.walk(ROOT, onerror=lambda e: unreadable_dirs.append(e.filename)):
    rel = os.path.relpath(dirpath, ROOT)
    parts = [] if rel == "." else rel.split(os.sep)
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
    n_py_here = 0
    for fn in filenames:
        ext = os.path.splitext(fn)[1].lower()
        full = os.path.join(dirpath, fn)
        if ext == ".py":
            py_files.append(full)
            n_py_here += 1
        elif ext in CODE_EXTS:
            code_text_files.append(full)
    if parts:
        top_dir_py_counts[parts[0]] += n_py_here

# name universes
local_anywhere = set()   # py-bearing dir basenames anywhere (ancestors included) + py stems
local_root = set()       # top-level py-bearing dir basenames + root py stems
for dirpath, dirnames, filenames in os.walk(ROOT, onerror=lambda e: None):
    rel = os.path.relpath(dirpath, ROOT)
    parts = [] if rel == "." else rel.split(os.sep)
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
    has_py = any(fn.endswith(".py") for fn in filenames)
    if has_py and parts:
        for p in parts:
            local_anywhere.add(p)
        local_root.add(parts[0])
    for fn in filenames:
        if fn.endswith(".py"):
            local_anywhere.add(fn[:-3])
            if not parts:
                local_root.add(fn[:-3])

stdlib_names = set(sys.stdlib_module_names)

parse_errors = []
name_occ = defaultdict(int)
name_occ_rt = defaultdict(int)
name_fileset = defaultdict(set)
name_fileset_rt = defaultdict(set)
name_refs = defaultdict(list)
name_refs_rt = defaultdict(list)
name_dirs = defaultdict(Counter)
dyn_occ = Counter()
dyn_files = defaultdict(int)
rel_import_count = 0
static_import_stmts = 0
import_occurrences = 0

for full in py_files:
    rel = os.path.relpath(full, ROOT).replace("\\", "/")
    top = rel.split("/")[0] if "/" in rel else "."
    is_rt = top in RUNTIME_TOPS
    try:
        with open(full, "rb") as f:
            src = f.read()
    except OSError as e:
        parse_errors.append((rel, "read: %s" % e))
        continue
    try:
        tree = ast.parse(src, filename=rel)
    except (SyntaxError, ValueError) as e:
        parse_errors.append((rel, str(e).split(" (")[0]))
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            static_import_stmts += 1
            for alias in node.names:
                nm = alias.name.split(".")[0]
                import_occurrences += 1
                name_occ[nm] += 1
                name_dirs[nm][top] += 1
                name_fileset[nm].add(rel)
                if is_rt:
                    name_occ_rt[nm] += 1
                    name_fileset_rt[nm].add(rel)
                    if len(name_refs_rt[nm]) < 15:
                        name_refs_rt[nm].append("%s:%d" % (rel, node.lineno))
                if len(name_refs[nm]) < 15:
                    name_refs[nm].append("%s:%d" % (rel, node.lineno))
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                rel_import_count += 1
                continue
            if node.module:
                static_import_stmts += 1
                nm = node.module.split(".")[0]
                import_occurrences += 1
                name_occ[nm] += 1
                name_dirs[nm][top] += 1
                name_fileset[nm].add(rel)
                if is_rt:
                    name_occ_rt[nm] += 1
                    name_fileset_rt[nm].add(rel)
                    if len(name_refs_rt[nm]) < 15:
                        name_refs_rt[nm].append("%s:%d" % (rel, node.lineno))
                if len(name_refs[nm]) < 15:
                    name_refs[nm].append("%s:%d" % (rel, node.lineno))
        elif isinstance(node, ast.Call):
            fn = node.func
            is_dyn = (isinstance(fn, ast.Name) and fn.id == "__import__") or (
                isinstance(fn, ast.Attribute) and fn.attr in ("import_module", "__import__"))
            if not is_dyn or not node.args:
                continue
            a0 = node.args[0]
            if isinstance(a0, ast.Constant) and isinstance(a0.value, str):
                lit = a0.value.split(".")[0]
                dyn_occ[lit] += 1
                dyn_files[lit] += 1

def file_count(nm):
    return len(name_fileset[nm])

def canon(s):
    return re.sub(r"[-_.]+", "-", s).lower()

pkgs_dists = metadata.packages_distributions()
installed_import_names = set(pkgs_dists.keys())

classification = {}
for nm in name_occ:
    if nm in stdlib_names:
        classification[nm] = "stdlib"
    elif nm in local_root:
        classification[nm] = "local-root"
    elif nm in installed_import_names:
        classification[nm] = "third-party"
    elif nm in local_anywhere:
        classification[nm] = "local-archive"
    else:
        classification[nm] = "unresolved"

shadow_collisions = sorted([n for n in name_occ if n in local_root and n in installed_import_names])

external_like = {"third-party", "unresolved", "local-archive"}
external_names = sorted([n for n, c in classification.items() if c in external_like])
ext_info = {}
for nm in external_names:
    ext_info[nm] = {
        "cls": classification[nm],
        "occ": name_occ[nm],
        "occ_rt": name_occ_rt[nm],
        "files": file_count(nm),
        "files_rt": len(name_fileset_rt[nm]),
        "dists": pkgs_dists.get(nm, []),
        "dyn_occ": dyn_occ.get(nm, 0),
        "top_dirs": name_dirs[nm].most_common(12),
        "refs": name_refs[nm][:15],
        "refs_rt": name_refs_rt[nm][:15],
    }

stdlib_local_collisions = sorted([n for n in name_occ if n in stdlib_names and (n in local_root or n in local_anywhere)])

installed = {}
for d in metadata.distributions():
    try:
        nm = d.metadata["Name"]
    except Exception:
        nm = None
    if nm:
        installed[nm] = d.version

dist_words = defaultdict(set)
for n, v in installed.items():
    dist_words[canon(n)].add(n.lower())
    dist_words[canon(n)].add(canon(n))
for d in metadata.distributions():
    try:
        nm = d.metadata["Name"]
    except Exception:
        continue
    try:
        for ep in (d.entry_points or []):
            if ep.group in ("console_scripts", "gui_scripts"):
                dist_words[canon(nm)].add(ep.name.lower())
                mod = ep.value.split(":")[0].split(".")[0]
                if mod:
                    dist_words[canon(nm)].add(mod.lower())
    except Exception:
        pass
for imp, dlist in pkgs_dists.items():
    for dn in dlist:
        dist_words[canon(dn)].add(imp.lower())

req_re = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)")
dist_requires = {}
for n, v in installed.items():
    try:
        reqs = metadata.requires(n) or []
    except Exception:
        reqs = []
    deps = set()
    for r in reqs:
        m = req_re.match(r)
        if m:
            deps.add(canon(m.group(1)))
    dist_requires[canon(n)] = deps
reverse_deps = defaultdict(set)
for dn, deps in dist_requires.items():
    for dep in deps:
        reverse_deps[dep].add(dn)

req_lines = []
req_path = os.path.join(ROOT, "requirements.txt")
with open(req_path, "r", encoding="utf-8", errors="replace") as f:
    raw = f.read().splitlines()
for i, ln in enumerate(raw, 1):
    s = ln.split("#")[0].strip()
    if not s:
        continue
    m = re.match(r"^([A-Za-z0-9][A-Za-z0-9._-]*)\s*(.*)$", s)
    if m:
        req_lines.append({"line": i, "raw": ln.strip(), "name": m.group(1), "spec": m.group(2).strip(), "canon": canon(m.group(1))})

imp_names_for_dist = defaultdict(set)
for imp, dlist in pkgs_dists.items():
    for dn in dlist:
        imp_names_for_dist[canon(dn)].add(imp)

m_mod = Counter()
m_files = defaultdict(set)
m_re = re.compile(r"(?:py(?:thon)?(?:\d+(?:\.\d+)?)?|\.venv[/\\]Scripts[/\\]python(?:\.exe)?)\b[^&|;<>]{0,120}?-m\s+([A-Za-z_][\w.]*)", re.IGNORECASE)
for full in code_text_files:
    rel = os.path.relpath(full, ROOT).replace("\\", "/")
    try:
        with open(full, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()
    except OSError:
        continue
    for line in txt.splitlines():
        for m in m_re.finditer(line):
            mod = m.group(1).split(".")[0]
            m_mod[mod] += 1
            if len(m_files[mod]) < 15:
                m_files[mod].add(rel)

result = {
    "root": ROOT,
    "py_files_total": len(py_files),
    "code_text_files": len(code_text_files),
    "unreadable_dirs": sorted(unreadable_dirs),
    "unreadable_dir_count": len(unreadable_dirs),
    "top_dir_py_counts": dict(top_dir_py_counts),
    "parse_error_count": len(parse_errors),
    "parse_errors": parse_errors,
    "static_import_stmts": static_import_stmts,
    "import_occurrences": import_occurrences,
    "relative_imports": rel_import_count,
    "distinct_names": len(name_occ),
    "class_counts": {k: sum(1 for c in classification.values() if c == k) for k in ("stdlib", "local-root", "third-party", "local-archive", "unresolved")},
    "stdlib_local_collisions": stdlib_local_collisions,
    "shadow_collisions": shadow_collisions,
    "stdlib_names_used": sorted([n for n, c in classification.items() if c == "stdlib"]),
    "local_root_used": sorted([(n, name_occ[n], name_occ_rt[n], file_count(n)) for n, c in classification.items() if c == "local-root"], key=lambda t: -t[1]),
    "external": ext_info,
    "installed_count": len(installed),
    "installed": {n: v for n, v in sorted(installed.items())},
    "requirements": req_lines,
    "imp_names_for_dist": {k: sorted(v) for k, v in imp_names_for_dist.items()},
    "module_invocations": m_mod.most_common(),
    "module_invocation_files": {k: sorted(v) for k, v in m_files.items()},
    "dynamic_literal_imports": dyn_occ.most_common(),
    "dist_words": {k: sorted(v) for k, v in dist_words.items()},
    "reverse_deps": {k: sorted(v) for k, v in reverse_deps.items() if v},
}

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=1, default=list)

tp = [n for n, c in classification.items() if c == "third-party"]
unres = [n for n, c in classification.items() if c == "unresolved"]
larch = [n for n, c in classification.items() if c == "local-archive"]
print("PY FILES:", len(py_files))
print("UNREADABLE DIRS:", len(unreadable_dirs))
print("PARSE ERRORS:", len(parse_errors))
print("STATIC IMPORT STMTS:", static_import_stmts)
print("IMPORT OCCURRENCES:", import_occurrences)
print("RELATIVE IMPORTS:", rel_import_count)
print("CLASS COUNTS:", result["class_counts"])
print("SHADOW COLLISIONS (root-local AND installed):", shadow_collisions)
print("STDLIB LOCAL COLLISIONS:", stdlib_local_collisions)
print("THIRD-PARTY WITH RUNTIME OCC:", sorted([n for n in tp if ext_info[n]["occ_rt"] > 0]))
print("UNRESOLVED WITH RUNTIME OCC:", sorted([n for n in unres if ext_info[n]["occ_rt"] > 0]))
print("LOCAL-ARCHIVE WITH RUNTIME OCC:", sorted([n for n in larch if ext_info[n]["occ_rt"] > 0]))
print("WROTE:", OUT_JSON)
