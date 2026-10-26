"""w4-24 instrument v2: import-time vs lazy graph, root-module resolution, honest cycles.

Pure ast + os. No subprocess.
"""
import ast
import json
import os
import sys
from collections import defaultdict

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
STDLIB = set(sys.stdlib_module_names)
FOCUS_ROOTS = ("mag", "tools")  # report detail for these

_file_cache = {}
_repo_files = {}  # dotted key -> abs path
for _sub in ("mag", "tools", "models", "harness"):
    for _dp, _dn, _fn in os.walk(os.path.join(ROOT, _sub)):
        _dn[:] = [d for d in _dn if d not in ("__pycache__",)]
        for _f in _fn:
            if _f.endswith(".py"):
                _rel = os.path.relpath(os.path.join(_dp, _f), ROOT).replace("\\", "/")
                _k = _rel[:-3]
                if _k.endswith("/__init__"):
                    _k = _k[:-9]
                _repo_files[_k.replace("/", ".")] = os.path.join(_dp, _f)
# root-level single-file modules
for _f in os.listdir(ROOT):
    if _f.endswith(".py"):
        _repo_files[_f[:-3]] = os.path.join(ROOT, _f)

REPO_KEYS = set(_repo_files)

def parse(path):
    if path in _file_cache:
        return _file_cache[path]
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            tree = ast.parse(f.read(), filename=path)
        err = None
    except SyntaxError as e:
        tree = None
        err = str(e)
    _file_cache[path] = (tree, err)
    return tree, err

def imports_of(path):
    """Return (module_level set, lazy set) of import strings."""
    tree, err = parse(path)
    if tree is None:
        return set(), set()
    top, lazy = set(), set()

    def visit(node, is_top):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                visit(child, False)
                continue
            if isinstance(child, ast.ClassDef):
                visit(child, is_top)  # class body executes at import time
                continue
            if isinstance(child, ast.Import):
                for a in child.names:
                    (top if is_top else lazy).add(a.name)
            elif isinstance(child, ast.ImportFrom):
                if child.level:
                    (top if is_top else lazy).add("__rel__")
                    continue
                if child.module:
                    (top if is_top else lazy).add(child.module)
            else:
                visit(child, is_top)

    visit(tree, True)
    return top, lazy

def resolve_import(modstr):
    """Longest repo-internal module the import string binds to; 'pkg' for bare package hub."""
    parts = modstr.split(".")
    for i in range(len(parts), 0, -1):
        cand = ".".join(parts[:i])
        if cand in REPO_KEYS:
            return cand
    return None

def from_aliases(modstr, names):
    """For 'from mag import x, y' return resolved repo modules for alias names."""
    out = set()
    for a in names:
        r = resolve_import(modstr + "." + a.name)
        if r and r != modstr:
            out.add(r)
    return out

def scan(trees):
    edges = {}
    for key, path in sorted(trees.items()):
        t, l = imports_of(path)
        deps = set()
        for m in t | l:
            if m == "__rel__":
                continue
            r = resolve_import(m)
            if r and r != key:
                deps.add(r)
        # refine from-imports
        tree, _ = parse(path)
        if tree:
            def walk2(node, is_top):
                for ch in ast.iter_child_nodes(node):
                    if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                        walk2(ch, False); continue
                    if isinstance(ch, ast.ClassDef):
                        walk2(ch, is_top); continue
                    if isinstance(ch, ast.ImportFrom) and not ch.level and ch.module:
                        base = resolve_import(ch.module)
                        if base:
                            for a in ch.names:
                                r = resolve_import(ch.module + "." + a.name)
                                if r and r != key and r != base:
                                    deps.add(r)
                    else:
                        walk2(ch, is_top)
            walk2(tree, True)
        edges[key] = deps
    return edges

def tarjan(edges):
    idx = [0]; stack = []; low = {}; ind = {}; on = {}; sccs = []
    def sc(v):
        ind[v] = low[v] = idx[0]; idx[0] += 1
        stack.append(v); on[v] = True
        for w in sorted(edges.get(v, ())):
            if w not in ind:
                sc(w); low[v] = min(low[v], low[w])
            elif on.get(w):
                low[v] = min(low[v], ind[w])
        if low[v] == ind[v]:
            c = []
            while True:
                w = stack.pop(); on[w] = False; c.append(w)
                if w == v: break
            sccs.append(c)
    sys.setrecursionlimit(200000)
    for v in sorted(edges):
        if v not in ind:
            sc(v)
    return sccs

allkeys = dict(_repo_files)
# scan only mag/ tools/ models/ harness/ + root .py (skip _alpha junk? no, scan all; they are part of estate)
E_top = scan(allkeys)

sccs_top = tarjan(E_top)
cycles_top = sorted([sorted(c) for c in sccs_top if len(c) > 1], key=len, reverse=True)

# import-time only graph
E_import = {}
for key, path in sorted(allkeys.items()):
    t, _ = imports_of(path)
    deps = set()
    tree, _ = parse(path)
    if tree:
        def walk3(node):
            for ch in ast.iter_child_nodes(node):
                if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                    continue
                if isinstance(ch, ast.Import):
                    for a in ch.names:
                        r = resolve_import(a.name)
                        if r and r != key: deps.add(r)
                elif isinstance(ch, ast.ImportFrom) and not ch.level and ch.module:
                    base = resolve_import(ch.module)
                    if base and base != key: deps.add(base)
                    if base:
                        for a in ch.names:
                            r = resolve_import(ch.module + "." + a.name)
                            if r and r != key: deps.add(r)
                else:
                    walk3(ch)
        walk3(tree)
    E_import[key] = deps

sccs_imp = tarjan(E_import)
cycles_imp = sorted([sorted(c) for c in sccs_imp if len(c) > 1], key=len, reverse=True)

def condense_longest(edges, sccs):
    sid = {}
    for i, c in enumerate(sccs):
        for n in c: sid[n] = i
    ce = defaultdict(set)
    for u, ds in edges.items():
        for v in ds:
            if sid[u] != sid[v]: ce[sid[u]].add(sid[v])
    memo = {}
    def lf(c):
        if c in memo: return memo[c]
        best, nxt = 0, None
        for w in sorted(ce.get(c, ())):
            l, _ = lf(w)
            if 1 + l > best: best, nxt = 1 + l, w
        memo[c] = (best, nxt); return memo[c]
    bl, bs = -1, None
    for c in ce:
        l, _ = lf(c)
        if l > bl: bl, bs = l, c
    chain = []
    c = bs
    while c is not None:
        chain.append(c); c = memo[c][1]
    nodes = [sccs[c][0] for c in chain]
    return bl, nodes

bl_imp, chain_imp = condense_longest(E_import, sccs_imp)
bl_all, chain_all = condense_longest(E_top, sccs_top)

fanin = defaultdict(int)
for u, ds in E_import.items():
    for v in ds: fanin[v] += 1

mag_tools = {k: v for k, v in E_import.items() if k.startswith(("mag.", "mag", "tools.", "tools"))}
fanin_mt = sorted(((fanin[m], m) for m in mag_tools), reverse=True)[:20]

# gate closure
gates = ["tools.workflow_gate", "tools.violation_ratchet", "tools.config_seal",
         "tools.census_drift_patrol", "tools.freshness_check", "tools.freshness_gate",
         "tools.secret_gate", "tools.ledger_lock", "tools.checkbox_receipt_gate",
         "tools.fossil_check"]
closure = {}
for g in gates:
    if g not in E_import: continue
    seen, stack = set(), [g]
    while stack:
        n = stack.pop()
        for d in E_import.get(n, ()):
            if d not in seen:
                seen.add(d); stack.append(d)
    closure[g] = sorted(seen)

out = {
    "repo_files_total": len(allkeys),
    "cycles_importtime": cycles_imp,
    "cycles_all": [c for c in cycles_top if len(c) < 200],
    "cycles_all_big_len": [len(c) for c in cycles_top if len(c) >= 200],
    "deepest_importtime_edges": bl_imp,
    "deepest_importtime_chain": chain_imp,
    "deepest_all_edges": bl_all,
    "deepest_all_chain": chain_all,
    "fanin_mag_tools_top": fanin_mt,
    "fanin_config": fanin.get("config", 0),
    "fanin_mag_init": fanin.get("mag", 0),
    "gate_closures": closure,
}
opath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_w4_depgraph2_out.json")
with open(opath, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)

print("repo files scanned:", len(allkeys))
print("IMPORT-TIME cycles:", len(cycles_imp))
for c in cycles_imp: print("  CYCLE:", " <- ".join(c))
print("ALL-imports cycles (small):", len([c for c in cycles_top if len(c) < 200]))
for c in [c for c in cycles_top if len(c) < 200]: print("  CYCLE:", " <- ".join(c))
print("big SCC lens:", out["cycles_all_big_len"])
print("deepest import-time chain, %d edges:" % bl_imp)
print("  " + " <- ".join(chain_imp))
print("deepest all-imports chain, %d edges:" % bl_all)
print("  " + " <- ".join(chain_all))
print("fanin top (mag/tools):", fanin_mt[:12])
print("config fanin:", fanin.get("config"), " mag hub fanin:", fanin.get("mag"))
for g, c in closure.items():
    print("closure", g, "->", c if c else "[]  (PURE STDLIB)")

# --- v3 extras: big SCC members, third-party roots, lazy-vs-top counts ---
big = [c for c in sccs_top if len(c) >= 200]
if big:
    members = sorted(big[0])
    tools_in = [m for m in members if m.startswith("tools")]
    print("BIG SCC len", len(members), "tools members:", tools_in)
    out["big_scc_len"] = len(members)
    out["big_scc_tools"] = tools_in
    out["big_scc_roots"] = sorted({m.split(".")[0] for m in members})

third_roots = defaultdict(int)
for key, path in sorted(allkeys.items()):
    t, _ = imports_of(path)
    for m in t:
        r = resolve_import(m)
        if r:
            continue
        top = m.split(".")[0]
        if top not in STDLIB and top != "__rel__":
            third_roots[top] += 1
print("third-party roots (top-level importers):", sorted(third_roots.items(), key=lambda x: -x[1])[:25])
out["thirdparty_roots"] = dict(sorted(third_roots.items(), key=lambda x: -x[1]))

lazy_mag = 0; top_mag = 0
for key, path in sorted(allkeys.items()):
    t, l = imports_of(path)
    tm = any(m == "mag" or m.startswith("mag.") for m in t)
    lm = any(m == "mag" or m.startswith("mag.") for m in l)
    if lm and not tm: lazy_mag += 1
    if tm: top_mag += 1
print("files importing mag top-level:", top_mag, " lazy-only:", lazy_mag)
out["mag_import_top_files"] = top_mag
out["mag_import_lazy_only_files"] = lazy_mag

import os as _os
print("watch/__init__.py exists:", _os.path.isfile(_os.path.join(ROOT, "watch", "__init__.py")))
print("llm module:", _os.path.isfile(_os.path.join(ROOT, "llm.py")) or _os.path.isdir(_os.path.join(ROOT, "llm")))

# zero-repo-dep tools at import time, and which of those spawn subprocess
zd = sorted(k for k in E_import if k.startswith("tools.") and not E_import[k])
spawners = []
for k in zd:
    with open(allkeys[k], "r", encoding="utf-8", errors="replace") as f:
        src = f.read()
    if "subprocess" in src:
        spawners.append(k)
print("import-time zero-dep tools:", len(zd), "of", sum(1 for k in E_import if k.startswith("tools.")))
print("of those, subprocess users:", len(spawners))
out["zero_dep_tools_importtime"] = zd
out["zero_dep_tools_spawners"] = spawners

with open(opath, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print("wrote", opath)
