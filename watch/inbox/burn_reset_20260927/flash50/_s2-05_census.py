# s2-05 mag/ deep census sweep. Pure file IO + ast, no subprocess.
# Instrument: .venv/Scripts/python.exe on this script. Every number in
# mag-deep-census.md comes from this run's stdout.
import ast
import io
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
SKIP_DIRS = {"node_modules", "__pycache__"}
TEXT_EXT = {".py", ".cmd", ".bat", ".ps1", ".md", ".yaml", ".yml", ".json", ".toml", ".cfg", ".ini", ".txt", ".sh", ".example", ".html", ".psm1"}


def walk_py_files():
    """All .py files in the repo, pruning dot-dirs, node_modules, __pycache__."""
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


def rel(repo_path):
    return os.path.relpath(repo_path, ROOT).replace("\\", "/")


def mod_name_for(mag_rel):
    """mag/foo/bar.py -> mag.foo.bar ; mag/foo/__init__.py -> mag.foo ; mag/__init__.py -> mag"""
    parts = mag_rel.split("/")
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1][:-3]
    return ".".join(parts)


def analyze():
    all_py = walk_py_files()
    mag_py = [p for p in all_py if rel(p).startswith("mag/")]

    # ---- pass 1: per-file stats for mag/ ----
    files = {}
    parse_fail = []
    total_lines = 0
    total_bytes = 0
    total_defs = 0
    total_public_defs = 0
    total_toplevel_public = 0
    total_public_methods = 0
    mag_modules = {}   # dotted name -> rel path
    is_init = {}       # dotted name -> bool

    for p in mag_py:
        r = rel(p)
        try:
            text = read_text(p)
        except OSError:
            continue
        nlines = len(text.splitlines())
        nbytes = os.path.getsize(p)
        ndef = 0
        npub = 0
        ntop = 0
        nmethod_pub = 0
        tree = None
        try:
            tree = ast.parse(text)
        except (SyntaxError, ValueError) as e:
            parse_fail.append({"file": r, "error": str(e)})
        if tree is not None:
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    ndef += 1
                    if not node.name.startswith("_"):
                        npub += 1
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
                    ntop += 1
            # public methods = public defs inside ClassDef
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for sub in node.body:
                        if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)) and not sub.name.startswith("_"):
                            nmethod_pub += 1
        m = mod_name_for(r)
        mag_modules[m] = r
        is_init[m] = r.endswith("/__init__.py")
        files[r] = {
            "module": m,
            "lines": nlines,
            "bytes": nbytes,
            "defs_all": ndef,
            "defs_public": npub,
            "toplevel_public": ntop,
            "public_methods": nmethod_pub,
            "is_init": r.endswith("/__init__.py"),
        }
        total_lines += nlines
        total_bytes += nbytes
        total_defs += ndef
        total_public_defs += npub
        total_toplevel_public += ntop
        total_public_methods += nmethod_pub

    # subpackages: dirs under mag/ (at any depth) holding an __init__.py
    subpkgs = set()
    for r, d in files.items():
        if d["is_init"]:
            subpkgs.add(r.rsplit("/", 1)[0])

    # ---- pass 2: import graph over every repo .py ----
    importers = {}     # mag module -> set(importer rel path)
    stmt_count = {}    # mag module -> number of import touches
    importers_mag = {} # mag module -> set(importer rel path restricted to mag/)
    dyn_strings = set()   # 'mag...' strings from import_module/__import__
    for p in all_py:
        r = rel(p)
        try:
            text = read_text(p)
        except OSError:
            continue
        try:
            tree = ast.parse(text)
        except (SyntaxError, ValueError):
            # regex fallback for the import lines only
            for mobj in re.finditer(r"^\s*(?:from\s+([\w.]+)\s+)?import\s+([\w.,\s()]+?)(?:#.*)?$", text, re.M):
                pass
            for s in re.findall(r"import_module\(\s*[\"']([^\"']+)[\"']", text):
                if s.startswith("mag."):
                    dyn_strings.add(s)
            continue
        in_mag = r.startswith("mag/")
        parts = r.split("/")
        pkg_parts = parts[:-1]
        if parts[-1] == "__init__.py":
            cur_pkg = pkg_parts  # package's own dir IS its package
        else:
            cur_pkg = pkg_parts

        touched = set()

        def touch(name):
            if name in mag_modules:
                touched.add(name)

        def touch_prefixes(dotted):
            # import mag.a.b also executes mag and mag.a
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
                    # relative: trim (level-1) components off current package
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
                fname = ""
                if isinstance(fn, ast.Attribute):
                    fname = fn.attr
                elif isinstance(fn, ast.Name):
                    fname = fn.id
                if fname in ("import_module", "__import__") and node.args:
                    a0 = node.args[0]
                    if isinstance(a0, ast.Constant) and isinstance(a0.value, str):
                        if a0.value == "mag" or a0.value.startswith("mag."):
                            dyn_strings.add(a0.value)
                            touch_prefixes(a0.value)
        for m in touched:
            importers.setdefault(m, set()).add(r)
            stmt_count[m] = stmt_count.get(m, 0) + 1
            if in_mag:
                importers_mag.setdefault(m, set()).add(r)

    # ---- entry-point scan over text files (non-.py too) ----
    ep_modules = set()
    ep_examples = {}
    ep_re = re.compile(r"-m\s+mag\.([A-Za-z_][A-Za-z0-9_.]*)")
    for dirpath, dirnames, filenames in os.walk(ROOT, onerror=lambda e: None):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in SKIP_DIRS]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in TEXT_EXT or fn.endswith(".py") and False:
                continue
            p = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(p) > 2_000_000:
                    continue
                text = read_text(p)
            except OSError:
                continue
            for mobj in ep_re.finditer(text):
                name = mobj.group(1)
                ep_modules.add(name)
                ep_examples.setdefault(name, rel(p))
    for s in dyn_strings:
        ep_modules.add(s[len("mag."):] if s.startswith("mag.") else s)

    # ---- assemble ----
    rows = []
    for r, d in files.items():
        m = d["module"]
        imps = importers.get(m, set())
        rows.append({
            "file": r,
            "module": m,
            "is_init": d["is_init"],
            "lines": d["lines"],
            "bytes": d["bytes"],
            "defs_public": d["defs_public"],
            "toplevel_public": d["toplevel_public"],
            "importers_repo": len(imps),
            "importers_mag": len(importers_mag.get(m, set())),
            "stmt_touches": stmt_count.get(m, 0),
        })

    non_init = [x for x in rows if not x["is_init"]]
    init_rows = [x for x in rows if x["is_init"]]

    largest = sorted(rows, key=lambda x: (-x["lines"], x["file"]))[:15]
    most_imported = sorted(non_init, key=lambda x: (-x["importers_repo"], -x["stmt_touches"], x["module"]))[:15]
    most_imported_mag = sorted(non_init, key=lambda x: (-x["importers_mag"], -x["stmt_touches"], x["module"]))[:15]

    never = [x for x in non_init if x["importers_repo"] == 0]
    never.sort(key=lambda x: (-x["lines"], x["file"]))
    never_flagged = []
    for x in never:
        leaf = x["module"].split(".")[-1]
        ep = leaf in ep_modules or x["module"] in ep_modules or x["module"] in dyn_strings
        x2 = dict(x)
        x2["entrypoint_hit"] = ep
        never_flagged.append(x2)

    out = {
        "instrument": ".venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/_s2-05_census.py",
        "moment_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "root": ROOT,
        "repo_py_files_scanned": len(all_py),
        "mag": {
            "py_files": len(mag_py),
            "bytes": total_bytes,
            "non_init_modules": len(non_init),
            "init_files": len(init_rows),
            "subpackages": sorted(subpkgs),
            "subpackage_count": len(subpkgs),
            "parse_failures": parse_fail,
            "total_lines": total_lines,
            "defs_all_incl_private": total_defs,
            "defs_public_all_incl_methods": total_public_defs,
            "toplevel_public_defs": total_toplevel_public,
            "public_methods": total_public_methods,
            "public_nonmethod_defs": total_public_defs - total_public_methods,
        },
        "largest": largest,
        "most_imported_repo": most_imported,
        "most_imported_mag": most_imported_mag,
        "never_imported_count": len(never),
        "never_imported_top": never_flagged[:20],
        "never_init_count": len([x for x in init_rows if x["importers_repo"] == 0]),
        "entrypoint_modules": sorted(ep_modules),
        "entrypoint_examples": ep_examples,
        "dynamic_import_strings": sorted(dyn_strings),
        "zero_metered_note": "",
    }
    return out


if __name__ == "__main__":
    res = analyze()
    outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s2-05_raw.json")
    with io.open(outpath, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res["mag"], indent=1))
    print("repo_py_files_scanned:", res["repo_py_files_scanned"])
    print("moment_utc:", res["moment_utc"])
    print("== LARGEST 15 ==")
    for x in res["largest"]:
        print(f"{x['lines']:6d}L {x['bytes']:9d}B pub={x['defs_public']:3d} {x['file']}")
    print("== MOST IMPORTED (repo-wide importers) 15 ==")
    for x in res["most_imported_repo"]:
        print(f"repo={x['importers_repo']:4d} mag={x['importers_mag']:4d} touches={x['stmt_touches']:4d} {x['module']}")
    print("== MOST IMPORTED (mag-only importers) 15 ==")
    for x in res["most_imported_mag"]:
        print(f"mag={x['importers_mag']:4d} repo={x['importers_repo']:4d} touches={x['stmt_touches']:4d} {x['module']}")
    print("== NEVER IMPORTED (non-init, repo-wide) count:", res["never_imported_count"], "==")
    for x in res["never_imported_top"]:
        print(f"{x['lines']:6d}L ep={str(x['entrypoint_hit']):5s} {x['module']}  ({x['file']})")
    print("never_imported_init_files:", res["never_init_count"])
    print("entrypoint -m mag.* modules:", len(res["entrypoint_modules"]))
    print("dynamic import strings:", res["dynamic_import_strings"][:40])
    print("RAW_JSON:", outpath)
