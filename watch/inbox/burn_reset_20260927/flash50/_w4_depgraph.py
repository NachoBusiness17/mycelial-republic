"""w4-24 instrument: estate dependency graph, cycles, deepest chain, kernel.

Pure ast + os.walk. No subprocess. Output: JSON to _w4_depgraph_out.json + text digest to stdout.
"""
import ast
import json
import os
import sys
from collections import defaultdict

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
STDLIB = set(sys.stdlib_module_names)

def module_key(path):
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    key = rel[:-3] if rel.endswith(".py") else rel
    if key.endswith("/__init__"):
        key = key[:-9]
    return key.replace("/", ".")

def parse_imports(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            tree = ast.parse(f.read(), filename=path)
    except SyntaxError as e:
        return None, str(e)
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                mods.add(a.name.split(".")[0] if not a.name.startswith(("mag", "tools")) else a.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                # relative import within package
                mods.add("__rel__")
                continue
            if node.module:
                base = node.module
                mods.add(base)
    return mods, None

def resolve(modname, importing_key):
    """Map an import string to a repo module key if it resolves to a repo file, else None."""
    if not modname:
        return None
    parts = modname.split(".")
    # exact file or package
    cands = []
    cur = parts[:]
    while cur:
        rel = "/".join(cur)
        for ext in (".py", "/__init__.py"):
            p = os.path.join(ROOT, rel + ext)
            if os.path.isfile(p):
                cands.append(module_key(p))
                break
        cur.pop()
    return cands[0] if cands else None

def collect(subdir):
    out = {}
    for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, subdir)):
        dirnames[:] = [d for d in dirnames if d not in ("__pycache__", "node_modules", ".git")]
        for fn in filenames:
            if fn.endswith(".py"):
                p = os.path.join(dirpath, fn)
                out[module_key(p)] = p
    return out

tools = collect("tools")
mag = collect("mag")
allkeys = {**tools, **mag}

edges = {}          # key -> set(internal dep keys)
edge_locs = {}      # (src,dst) -> (file, line)
syntax_errs = {}
stdlib_use = defaultdict(set)
thirdparty_use = defaultdict(set)
unresolved = defaultdict(set)

for key, path in sorted(allkeys.items()):
    mods, err = parse_imports(path)
    if err:
        syntax_errs[key] = err
        edges[key] = set()
        continue
    deps = set()
    for m in mods:
        if m == "__rel__":
            continue
        top = m.split(".")[0]
        if top in ("mag", "tools"):
            r = resolve(m, key)
            if r and r != key:
                deps.add(r)
                edge_locs[(key, r)] = (path, None)
            elif r is None:
                unresolved[key].add(m)
        elif top in STDLIB:
            stdlib_use[top].add(key)
        else:
            thirdparty_use[top].add(key)
    edges[key] = deps

# Tarjan SCC
index_counter = [0]
stack, lowlink, index, on_stack = [], {}, {}, {}
sccs = []

def strongconnect(v):
    index[v] = index_counter[0]
    lowlink[v] = index_counter[0]
    index_counter[0] += 1
    stack.append(v); on_stack[v] = True
    for w in sorted(edges.get(v, ())):
        if w not in index:
            strongconnect(w)
            lowlink[v] = min(lowlink[v], lowlink[w])
        elif on_stack.get(w):
            lowlink[v] = min(lowlink[v], index[w])
    if lowlink[v] == index[v]:
        comp = []
        while True:
            w = stack.pop(); on_stack[w] = False
            comp.append(w)
            if w == v:
                break
        sccs.append(comp)

sys.setrecursionlimit(100000)
for v in sorted(edges):
    if v not in index:
        strongconnect(v)

cycles = [c for c in sccs if len(c) > 1]
self_loops = sorted([(k, d) for k, ds in edges.items() for d in ds if d == k])

# condensation DAG + longest path (node count)
scc_id = {}
for i, c in enumerate(sccs):
    for n in c:
        scc_id[n] = i
cond_edges = defaultdict(set)
for u, ds in edges.items():
    for v in ds:
        if scc_id[u] != scc_id[v]:
            cond_edges[scc_id[u]].add(scc_id[v])

memo = {}
def longest_from(c):
    if c in memo:
        return memo[c]
    best = 0; nxt = None
    for w in sorted(cond_edges.get(c, ())):
        l, n2 = longest_from(w)
        if 1 + l > best:
            best = 1 + l; nxt = w
    memo[c] = (best, nxt)
    return memo[c]

best_len, best_start = -1, None
for c in cond_edges:
    l, _ = longest_from(c)
    if l > best_len:
        best_len, best_start = l, c

def chain_from(c):
    out = [c]
    while True:
        nxt = memo[c][1]
        if nxt is None:
            break
        out.append(nxt)
        c = nxt
    return out

cond_chain = chain_from(best_start) if best_start is not None else []
deepest_chain = [sccs[c][0] for c in cond_chain]

# deepest FILE-level chain by expanding each scc node to its longest internal member chain (approx: report scc members)
# also compute deepest simple chain ignoring cycles via DFS memo on acyclic approximation:
depth = {}
def depth_of(k, seen=()):
    if k in depth:
        return depth[k]
    if k in seen:
        return 0
    d = 0
    for w in edges.get(k, ()):
        if w != k:
            d = max(d, 1 + depth_of(w, seen + (k,)))
    depth[k] = d
    return d

# NOTE: with cycles this memoized version is unsound; compute depth only over DAG of unique edges with cycle guard, per-node without memo reuse across cycle paths is too slow.
# Instead: depth on condensation is the honest measure. Keep depth_of only for acyclic subgraph (tools->tools->mag->leaf).
# Compute "kernel" stats:
fanin = defaultdict(int)
for u, ds in edges.items():
    for v in ds:
        fanin[v] += 1

tools_only_edges = {k: {d for d in ds if d in tools} for k, ds in edges.items() if k in tools}
tool_imports_tool = {k: sorted(v) for k, v in tools_only_edges.items() if v}

mag_fanin_top = sorted(((fanin[m], m) for m in mag), reverse=True)[:30]
tools_fanin_top = sorted(((fanin[t], t) for t in tools), reverse=True)[:25]

zero_dep_tools = sorted(t for t in tools if not (edges[t] - set()))
zero_dep_mag = sorted(m for m in mag if not (edges[m] - set()))
stdlib_only_tools = sorted(t for t in tools if not edges[t])

out = {
    "root": ROOT,
    "counts": {"tools_py": len(tools), "mag_py": len(mag), "syntax_errors": len(syntax_errs)},
    "syntax_errors": syntax_errs,
    "cycles": [sorted(c) for c in sorted(cycles, key=len, reverse=True)],
    "self_loops": self_loops,
    "deepest_chain_condensation": deepest_chain,
    "deepest_chain_len_edges": len(deepest_chain) - 1 if deepest_chain else 0,
    "tool_imports_tool": tool_imports_tool,
    "mag_fanin_top": mag_fanin_top,
    "tools_fanin_top": tools_fanin_top,
    "zero_dep_tools": zero_dep_tools,
    "zero_dep_mag_count": len(zero_dep_mag),
    "zero_dep_mag_top": [m for m in zero_dep_mag if fanin[m] >= 5][:60],
    "stdlib_top": sorted(((len(v), k) for k, v in stdlib_use.items()), reverse=True)[:25],
    "thirdparty_top": sorted(((len(v), k) for k, v in thirdparty_use.items()), reverse=True)[:25],
    "unresolved_mag_imports_count": sum(1 for v in unresolved.values() if v),
}
opath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_w4_depgraph_out.json")
with open(opath, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print("root:", ROOT)
print("counts:", out["counts"])
print("cycles:", len(cycles), "self_loops:", len(self_loops))
for c in cycles[:12]:
    print("  CYCLE(len%d):" % len(c), " <- ".join(sorted(c)))
print("deepest condensation chain (%d edges):" % out["deepest_chain_len_edges"])
print("  " + " <- ".join(deepest_chain))
print("tool->tool importers:", len(tool_imports_tool))
for k, v in sorted(tool_imports_tool.items()):
    print("  %s -> %s" % (k, ",".join(v)))
print("mag fanin top10:", mag_fanin_top[:10])
print("tools fanin top10:", tools_fanin_top[:10])
print("zero-dep tools:", len(zero_dep_tools), zero_dep_tools[:20])
print("stdlib top10:", out["stdlib_top"][:10])
print("3p top10:", out["thirdparty_top"][:10])
print("wrote", opath)
