"""s2-19 driver: alias-resolve monkeypatch object targets, collect setenv vars +
fixture producers, batch-resolve all unique targets via worker subprocesses
(CREATE_NO_WINDOW on win32), then git last-touch dates for test + real files."""
import ast, json, os, subprocess, sys, collections

REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
FLASH = os.path.join(REPO, "watch", "inbox", "burn_reset_20260927", "flash50")
SCAN = os.path.join(FLASH, "_s219_scan.json")
WORKER = os.path.join(FLASH, "_s219_worker.py")
OUT = os.path.join(FLASH, "_s219_verify.json")
CF = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0

d = json.load(open(SCAN, encoding="utf-8"))
records = d["records"]

# ---------- alias maps per file ----------
def alias_map(tree):
    am = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                bind = a.asname or a.name.split(".")[0]
                am[bind] = a.name if a.asname else a.name.split(".")[0]
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                for a in node.names:
                    bind = a.asname or a.name
                    am[bind] = node.module + "." + a.name
    return am

def local_names(tree):
    ln = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            ln.add(node.name)
            a = node.args
            for arg in list(a.args) + list(getattr(a, "kwonlyargs", [])):
                ln.add(arg.arg)
            if a.vararg:
                ln.add(a.vararg.arg)
            if a.kwarg:
                ln.add(a.kwarg.arg)
        elif isinstance(node, ast.ClassDef):
            ln.add(node.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                for n in ast.walk(t):
                    if isinstance(n, ast.Name):
                        ln.add(n.id)
        elif isinstance(node, (ast.For, ast.comprehension)):
            for n in ast.walk(node.target):
                if isinstance(n, ast.Name):
                    ln.add(n.id)
        elif isinstance(node, ast.With):
            for item in node.items:
                if item.optional_vars is not None:
                    for n in ast.walk(item.optional_vars):
                        if isinstance(n, ast.Name):
                            ln.add(n.id)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            ln.add(node.name)
    return ln

import tokenize
obj_resolved = {}     # rewritten qualified target -> sites
obj_local = []        # local-object stubbing sites
obj_unknown = []
patch_targets = {}
str_monkey = {}

for r in records:
    path = os.path.join(REPO, r["file"])
    src = tokenize.open(path).read()
    tree = ast.parse(src)
    am = alias_map(tree)
    ln = local_names(tree)
    for t in r["monkey_obj_targets"]:
        root, _, rest = t["target"].partition(".")
        site = {"file": r["file"], "line": t["line"], "raw": t["target"]}
        if root in am:
            qual = am[root] + (("." + rest) if rest else "")
            obj_resolved.setdefault(qual, []).append(site)
        elif root in ln:
            obj_local.append(site)
        else:
            # not aliased, not local: maybe direct module name (os, sys, urllib, mag...)
            obj_resolved.setdefault(t["target"], []).append(site)
    for pc in r["patch_calls"]:
        if pc["form"] == "string" and pc["target"]:
            patch_targets.setdefault(pc["target"], []).append(
                {"file": r["file"], "line": pc["line"], "kw": pc["kw"]})
    for t in r["monkey_string_targets"]:
        str_monkey.setdefault(t["target"], []).append({"file": r["file"], "line": t["line"]})

# ---------- env var names + fixture producers ----------
env_vars = collections.Counter()
fixture_produce = {}
for r in records:
    path = os.path.join(REPO, r["file"])
    src = tokenize.open(path).read()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "monkeypatch"
                and node.func.attr in ("setenv", "delenv")
                and node.args and isinstance(node.args[0], ast.Constant)):
            env_vars["%s:%s" % (node.func.attr, node.args[0].value)] += 1
    # fixture producers: first return/yield expr
    for fd in ast.walk(tree):
        if isinstance(fd, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for dec in fd.decorator_list:
                q = ast.unparse(dec).split("(")[0]
                if q in ("fixture", "pytest.fixture"):
                    expr = None
                    for n in ast.walk(fd):
                        if isinstance(n, ast.Yield) and n.value is not None:
                            expr = ast.unparse(n.value)
                            break
                        if isinstance(n, ast.Return) and n.value is not None:
                            expr = ast.unparse(n.value)
                            break
                    fixture_produce.setdefault(r["file"] + "::" + fd.name, {
                        "file": r["file"], "line": fd.lineno,
                        "produce": (expr or "?")[:110]})

# ---------- resolve all unique qualified targets in batches ----------
all_targets = set(patch_targets) | set(str_monkey) | set(obj_resolved)
targets = [{"id": i, "target": t} for i, t in enumerate(sorted(all_targets))]
print("unique qualified targets", len(targets),
      "| patch", len(patch_targets), "monkey_str", len(str_monkey),
      "monkey_obj_qualified", len(obj_resolved),
      "| local-object stub sites", len(obj_local))

CHUNK = 30
results = []
for i in range(0, len(targets), CHUNK):
    chunk = targets[i:i + CHUNK]
    cin = os.path.join(FLASH, "_s219_chunk_in.json")
    cout = os.path.join(FLASH, "_s219_chunk_out.json")
    with open(cin, "w", encoding="utf-8") as fh:
        json.dump(chunk, fh)
    if os.path.exists(cout):
        os.remove(cout)
    proc = subprocess.run(
        [os.path.join(REPO, ".venv", "Scripts", "python.exe"), WORKER, cin, cout],
        cwd=REPO, capture_output=True, text=True, timeout=420, creationflags=CF)
    if not os.path.exists(cout):
        print("BATCH FAIL at", i, proc.returncode, proc.stdout[-400:], proc.stderr[-600:])
        sys.exit(2)
    with open(cout, encoding="utf-8") as fh:
        results.extend(json.load(fh))
    print("batch", i // CHUNK + 1, "of", (len(targets) + CHUNK - 1) // CHUNK, "ok")

by_target = {x["target"]: x for x in results}

# ---------- git last-touch dates ----------
gl = subprocess.run(["git", "-C", REPO, "log", "--pretty=format:%cI", "--name-only"],
                    capture_output=True, text=True, timeout=600, creationflags=CF)
last_touch = {}
date = None
for line in gl.stdout.splitlines():
    line = line.strip()
    if not line:
        date = None
        continue
    if date is None:
        date = line
    else:
        last_touch.setdefault(line.replace("\\", "/"), date)

def lt(p):
    return last_touch.get(p)

# ---------- assemble verdict per target ----------
verdicts = []
for src, bucket in (("patch", patch_targets), ("monkey_str", str_monkey), ("monkey_obj", obj_resolved)):
  for t, sites in bucket.items():
    kind = src
    res = by_target.get(t)
    site_dates = [lt(s["file"]) for s in sites]
    site_date = max(x for x in site_dates if x) if any(site_dates) else None
    real_mod_file = None
    real_date = None
    real_newer = None
    in_repo = False
    if res:
        in_repo = bool(res.get("in_repo"))
        real_mod_file = res.get("module_file")
        if in_repo and real_mod_file:
            rel = os.path.relpath(real_mod_file, REPO).replace("\\", "/")
            real_mod_file = rel
            real_date = lt(rel)
            if real_date and site_date:
                real_newer = real_date > site_date
    verdicts.append({
        "target": t, "kind": kind, "sites": sites, "n_sites": len(sites),
        "status": res["status"] if res else "UNRESOLVED",
        "error": res.get("error") if res else None,
        "resolved_module": res.get("module") if res else None,
        "real_module_file": real_mod_file, "real_in_repo": in_repo,
        "real_kind": res.get("kind") if res else None,
        "real_sig": res.get("sig") if res else None,
        "site_last_commit": site_date, "real_module_last_commit": real_date,
        "real_module_changed_after_mock": real_newer,
    })

verdicts.sort(key=lambda v: (v["status"] != "ATTR_MISSING", v["status"] != "IMPORT_FAIL", v["target"]))

missing = [v for v in verdicts if v["status"] == "ATTR_MISSING"]
print("ATTR_MISSING", len(missing), "IMPORT_FAIL",
      sum(1 for v in verdicts if v["status"] == "IMPORT_FAIL"),
      "OK", sum(1 for v in verdicts if v["status"] == "OK"))
for v in missing:
    print("MISSING", v["target"], "<-", ["%s:%s" % (s["file"], s["line"]) for s in v["sites"][:3]])

out = {
    "unique_targets": len(verdicts),
    "verdicts": verdicts,
    "obj_local_stub_sites": obj_local,
    "env_vars": dict(env_vars),
    "fixture_produce": fixture_produce,
    "patch_targets_sites": patch_targets,
}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
print("wrote", OUT)
