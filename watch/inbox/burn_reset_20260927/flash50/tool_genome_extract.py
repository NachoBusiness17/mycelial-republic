"""TOOL GENOME PROJECT - extraction pass.

For every tracked tools/*.py in the estate:
  ancestry    = imports (stdlib / mag.* / sibling tools / third-party)
  descendants = code surfaces outside tools/ that invoke or import it
  immune      = tests/ files that reference it
  fossils     = receipt surfaces (watch/corpus/memory/docs/queue/state) mentioning it
  birth       = first git add date (git log --no-renames --diff-filter=A)
  death       = removal date for deleted tools (diff-filter=D) -> extinct lineages
Also: duplicate-byte .py groups (horizontal gene transfer candidates).

Run: .venv/Scripts/python.exe <this file>
Writes tool_genome_data.json next to itself.
"""
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import defaultdict

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
STDLIB = set(sys.stdlib_module_names)

def git(args):
    kw = {}
    if os.name == "nt":
        kw["creationflags"] = subprocess.CREATE_NO_WINDOW
    r = subprocess.run(["git"] + args, cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", **kw)
    return r.stdout

# ---------- inventory ----------
tracked = [l.strip() for l in git(["ls-files", "tools/"]).splitlines()
           if l.strip().endswith(".py")]
tools = {}  # name -> tracked path
for p in tracked:
    tools[os.path.basename(p)[:-3]] = p
names = set(tools)
print(f"inventory: {len(tracked)} tracked tools/*.py, {len(names)} distinct basenames")

# ---------- git birth / death ----------
def history(diff):
    out = git(["log", "--no-renames", "--diff-filter=" + diff, "--name-status",
               "--format=%x01%ad", "--date=short", "--reverse", "--", "tools/"])
    events, cur = {}, None
    for line in out.splitlines():
        if line.startswith("\x01"):
            cur = line.strip("\x01")
        elif line and cur:
            path = line.split("\t")[-1]
            events.setdefault(path, cur)
    return events

birth = history("A")
death = history("D")
print(f"git history: {len(birth)} ever-added paths, {len(death)} ever-removed paths")

# ---------- imports per tool ----------
def classify(mods, self_name):
    mag, sib, std, ext, other = set(), set(), set(), set(), set()
    for mod, level, alias_names in mods:
        cands = []
        if level and level > 0:
            base = mod.split(".")[0] if mod else ""
            cands.append(base)
            cands.extend(alias_names)
        elif mod:
            top = mod.split(".")[0]
            if top == "tools":
                rest = mod.split(".")
                if len(rest) > 1:
                    cands.append(rest[1])
                cands.extend(alias_names)
            elif top == "mag":
                mag.add(mod)
                for a in alias_names:
                    mag.add(mod + "." + a)
            elif top in STDLIB:
                std.add(top)
            else:
                other.add(top)
                for a in alias_names:
                    other.add(a)
        else:
            cands.extend(alias_names)
        for c in cands:
            c = c.strip()
            if c in names and c != self_name:
                sib.add(c)
    return sorted(mag), sorted(sib), sorted(std), sorted(ext), sorted(other)

GEN = {}
parse_fail = {}
for name, rel in sorted(tools.items()):
    full = os.path.join(ROOT, rel)
    try:
        src = open(full, encoding="utf-8", errors="replace").read()
    except OSError as e:
        parse_fail[name] = repr(e)
        continue
    loc = src.count("\n") + 1
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        parse_fail[name] = f"SyntaxError: {e}"
        mods = []
    else:
        mods = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    mods.append((a.name, 0, []))
            elif isinstance(node, ast.ImportFrom):
                mods.append((node.module or "", node.level or 0,
                             [a.name for a in node.names]))
    mag, sib, std, ext, other = classify(mods, name)
    GEN[name] = {
        "path": rel, "loc": loc,
        "birth": birth.get(rel), "death": death.get(rel),
        "imports_mag": mag, "imports_siblings": sib,
        "imports_stdlib": std, "imports_other": other,
        "callers": [], "test_files": [], "receipt_files": 0,
    }
print(f"parsed: {len(GEN)} ok, {len(parse_fail)} parse-failed")

# ---------- reference scan ----------
RE_TOOLPATH = re.compile(r"tools[/.]([A-Za-z_][A-Za-z0-9_]*)")
RE_FROMIMPORT = re.compile(r"from\s+tools\s+import\s+([\w\s,]+)")
RE_BAREPY = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\.py\b")

CODE_SURFACES = ["mag", "tests", "scripts", "dashboard", "githooks", "configs",
                 ".agents", "corpus"]
RECEIPT_SURFACES = ["watch", "memory", "docs", "queue", "state"]
ROOT_FILES = [f for f in os.listdir(ROOT)
              if os.path.isfile(os.path.join(ROOT, f))]
MAX_BYTES = 8_000_000
TEXT_EXT = {".py", ".md", ".json", ".jsonl", ".txt", ".ps1", ".cmd", ".bat",
            ".js", ".mjs", ".html", ".css", ".yml", ".yaml", ".csv", ".toml",
            ".cfg", ".ini", ".luau", ".sh", ".sql"}

hits = defaultdict(lambda: defaultdict(set))  # name -> kind -> {relpath}

def record(n, kind, rel):
    if n in names and rel != tools[n]:
        hits[n][kind].add(rel)

def rel_of(full):
    low = full.lower()
    if low.startswith(ROOT.lower() + os.sep):
        return full[len(ROOT) + 1:].replace("\\", "/")
    return full.replace("\\", "/")

def scan_file(full, rel):
    try:
        if os.path.getsize(full) > MAX_BYTES:
            return
        if os.path.splitext(full)[1].lower() not in TEXT_EXT:
            return
        with open(full, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        return
    norm = text.replace("\\", "/")
    strong = set()
    for m in RE_TOOLPATH.finditer(norm):
        strong.add(m.group(1))
    for m in RE_FROMIMPORT.finditer(norm):
        for tok in m.group(1).split(","):
            strong.add(tok.strip())
    if strong:
        for n in strong:
            record(n, "strong", rel)
    weak = set()
    for m in RE_BAREPY.finditer(norm):
        n = m.group(1)
        if n in names and n not in strong:
            weak.add(n)
    for n in weak:
        record(n, "bare", rel)

def walk_surface(surface, is_dir):
    if not is_dir:
        scan_file(os.path.join(ROOT, surface), surface.replace("\\", "/"))
        return
    base = os.path.join(ROOT, surface)
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames
                       if d not in ("__pycache__", ".git", "node_modules")]
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            scan_file(full, rel_of(full))

for s in CODE_SURFACES + RECEIPT_SURFACES:
    p = os.path.join(ROOT, s)
    if os.path.isdir(p):
        walk_surface(s, True)
    elif os.path.exists(p):
        walk_surface(s, False)
for f in ROOT_FILES:
    scan_file(os.path.join(ROOT, f), f.replace("\\", "/"))
print("reference scan done")

LIVE_CODE = ("mag/", "scripts/", "dashboard/", "githooks/", ".agents/")
FOSSIL = ("watch/", "memory/", "docs/", "queue/", "state/", "corpus/")
for name, g in GEN.items():
    h = hits[name]
    strong = h.get("strong", set())
    bare = h.get("bare", set())
    both = strong | bare
    root_hits = [r for r in both if "/" not in r]
    g["callers"] = sorted(r for r in both
                          if r.startswith(LIVE_CODE)
                          and not r.endswith("TOOLS.md"))
    g["callers_strong"] = sorted(r for r in strong
                                 if r.startswith(LIVE_CODE)
                                 and not r.endswith("TOOLS.md"))
    g["doc_files"] = sorted(r for r in root_hits if r.endswith("TOOLS.md"))
    g["registry_files"] = sorted(r for r in both if r.startswith("configs/"))
    g["test_files"] = sorted(r for r in both if r.startswith("tests/"))
    g["fossil_files"] = len([r for r in both if r.startswith(FOSSIL)])
    g["receipt_files"] = g["fossil_files"]

# ---------- duplicate-byte groups (horizontal gene transfer) ----------
allpy = [l.strip() for l in git(["ls-files", "*.py"]).splitlines() if l.strip()]
byhash = defaultdict(list)
for rel in allpy:
    try:
        data = open(os.path.join(ROOT, rel), "rb").read()
    except OSError:
        continue
    byhash[hashlib.sha256(data).hexdigest()].append(rel)
dups = {h: ps for h, ps in byhash.items()
        if len(ps) > 1 and any(p.startswith("tools/") for p in ps)}

# ---------- lineage graph ----------
children = defaultdict(set)   # tool -> tools that import it
for name, g in GEN.items():
    for s in g["imports_siblings"]:
        children[s].add(name)

def reach(n, seen=None):
    seen = set() if seen is None else seen
    for c in children.get(n, ()):
        if c not in seen:
            seen.add(c)
            reach(c, seen)
    return seen

def depth(n, memo=None):
    memo = {} if memo is None else memo
    if n in memo:
        return memo[n]
    kids = children.get(n, set())
    d = 0 if not kids else 1 + max(depth(k, memo) for k in kids)
    memo[n] = d
    return d

for name, g in GEN.items():
    g["import_children"] = sorted(children.get(name, ()))
    g["import_reach"] = len(reach(name))
    g["lineage_depth"] = depth(name)

out = {
    "census": {
        "tracked_tools_py": len(tracked),
        "distinct_basenames": len(names),
        "parse_failures": parse_fail,
        "ever_added": len(birth),
        "ever_removed": len(death),
    },
    "genomes": GEN,
    "removed_paths": {p: d for p, d in sorted(death.items(), key=lambda kv: kv[1])},
    "duplicate_byte_groups": {h: ps for h, ps in sorted(dups.items())},
}
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "tool_genome_data.json")
with open(dst, "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
print("wrote", dst)

# ---------- headline numbers ----------
live = {n: g for n, g in GEN.items() if not g["death"]}
callers_n = {n: len(g["callers"]) for n, g in GEN.items()}
callers_strong_n = {n: len(g["callers_strong"]) for n, g in GEN.items()}
tests_n = {n: len(g["test_files"]) for n, g in GEN.items()}
fossil_n = {n: g["fossil_files"] for n, g in GEN.items()}
print("")
print("== TOP 20 by live-code callers (any-tier) ==")
for n, c in sorted(callers_n.items(), key=lambda kv: -kv[1])[:20]:
    print(f"{c:4d} callers ({callers_strong_n[n]:3d} strong) "
          f"{tests_n[n]:3d} tests {fossil_n[n]:4d} fossils  {n}")
print("")
print("== TOP 15 by fossil files ==")
for n, c in sorted(fossil_n.items(), key=lambda kv: -kv[1])[:15]:
    print(f"{c:5d} fossils {callers_n[n]:3d} callers  {n}")
zero_caller = [n for n in live if callers_n[n] == 0]
zero_fossil = [n for n in live if fossil_n[n] == 0]
dead_end = [n for n in live if callers_n[n] == 0 and fossil_n[n] == 0
            and tests_n[n] == 0]
print(f"\nlive tools with ZERO live-code callers: {len(zero_caller)}")
print(f"live tools with ZERO fossil mentions: {len(zero_fossil)}")
print(f"live tools with NO callers, NO fossils, NO tests: {len(dead_end)}")
print("dead ends:", ", ".join(sorted(dead_end)))
notested = [n for n in live if tests_n[n] == 0]
testcov = sorted(n for n in live if tests_n[n] > 0)
print(f"\nzero-test live tools: {len(notested)}/{len(live)}")
print("immune-covered:", ", ".join(testcov))
print("")
print("== TOP 15 by import-descendants (who imports this tool) ==")
for n, k in sorted(children.items(), key=lambda kv: -len(kv[1]))[:15]:
    print(f"{len(k):4d} children  reach={len(reach(n)):3d}  {n}")
print("")
print("== OLDEST 15 surviving ==")
for n, g in sorted(live.items(), key=lambda kv: kv[1]["birth"] or "9999")[:15]:
    print(f"{g['birth']}  {n}")
print("")
print("== NEWEST 10 ==")
for n, g in sorted(live.items(), key=lambda kv: kv[1]["birth"] or "9999")[-10:]:
    print(f"{g['birth']}  {n}")
orphan = [n for n in live if callers_n[n] == 0 and tests_n[n] == 0
          and not children.get(n)]
print(f"\nfully orphan (no callers/tests/children): {len(orphan)}")
print("orphans:", ", ".join(sorted(orphan)))
print("")
print("== EXTINCT (removed from tools/) ==")
for p, d in out["removed_paths"].items():
    print(f"{d}  {p}")
print("")
print("== DUPLICATE-BYTE GROUPS ==")
for h, ps in dups.items():
    print(" | ".join(ps))
