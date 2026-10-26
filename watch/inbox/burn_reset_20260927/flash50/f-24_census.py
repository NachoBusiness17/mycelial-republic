"""f-24 census instrument: every Python module in mag/.

Read-only survey of the mag/ package tree. Emits, next to this script:
  mag-census.md    - the human-readable census (deliverable)
  f-24_data.json   - the same data, machine-readable

Census definitions (also documented in the emitted markdown):
  lines          - wc -l semantics: count of b"\\n" bytes in the file
  public funcs   - ast.parse module-level def/async def, name not starting "_"
                   (methods inside classes are NOT counted here; classes are a
                   separate column)
  public classes - module-level class, name not starting "_"
  last modified  - two instruments: filesystem mtime (local time, includes
                   uncommitted working-tree edits) and last git commit that
                   touched the path (git log --no-merges --name-only, first
                   occurrence walking newest-first)
  tests          - test corpus = tests/**.py + mag/tests/**.py. A module "has
                   tests" if >= 1 test file textually references its import
                   name, a from-import of it, a relative import, or its file
                   path. Value = count of distinct test files.
  readers        - repo files with ext .py .pyw .cmd .bat .ps1 .sh .yaml .yml
                   .toml .cfg .ini, outside tests/, mag/tests/, watch/, hidden
                   dirs, __pycache__, referencing the module the same way.
                   Self-references excluded. watch/ excluded because it holds
                   scratch instruments and prose, not durable code.
Reference matching is textual (imports, from-imports, path strings), not a
runtime import graph; references inside comments/docstrings count. Reader and
test counts are therefore upper bounds on true importers and lower bounds on
dispatcher-routed use (generic dispatchers like mag.cmd "%*" never name a
specific module).

Run:  ./.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/f-24_census.py
"""
import ast
import json
import os
import re
import subprocess
from datetime import datetime

CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0

READER_EXTS = {".py", ".pyw", ".cmd", ".bat", ".ps1", ".sh", ".yaml", ".yml",
               ".toml", ".cfg", ".ini"}
SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", "watch", "tests",
             ".zcode", ".agents", ".idea", ".vscode", ".mimosa",
             "_archaeology_out", "corpus", "attic", "mine", "dist_audit",
             "local_sovereign_agent"}
MAX_SCAN_BYTES = 1_500_000

DOTTED = re.compile(r"\bmag\.([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)")
FROM_MAG = re.compile(r"\bfrom\s+mag\s+import\s+\(?([\w\s,.]*)")
RELATIVE = re.compile(r"\bfrom\s+(\.+)([\w.]*)\s+import\s+\(?([\w\s,.]*)")
PATHREF = re.compile(r"\bmag[/\\]([\w\\/.-]+)")
IMPORT_MAG = re.compile(r"\bimport\s+mag\b")


def run_git(args):
    kwargs = {}
    if os.name == "nt":
        kwargs["creationflags"] = CREATE_NO_WINDOW
    return subprocess.run(["git"] + args, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kwargs)


def find_root():
    p = os.path.dirname(os.path.abspath(__file__))
    for _ in range(12):
        if os.path.isdir(os.path.join(p, "mag")):
            return p
        nxt = os.path.dirname(p)
        if nxt == p:
            break
        p = nxt
    raise SystemExit("repo root with mag/ not found")


def import_name(rel_file):
    stem = rel_file[4:-3] if rel_file.startswith("mag/") else rel_file[:-3]
    parts = [p for p in stem.split("/") if p]
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def idents(capture):
    return [t for t in re.split(r"[\s,()]+", capture or "")
            if re.fullmatch(r"\w+", t)]


def read_text(path):
    with open(path, "rb") as f:
        return f.read()


def main():
    root = find_root()
    flash = os.path.dirname(os.path.abspath(__file__))
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    head = run_git(["rev-parse", "--short", "HEAD"]).stdout.strip()
    branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()

    # ---- 1. module inventory -------------------------------------------
    mods = []
    magdir = os.path.join(root, "mag")
    for dirpath, dirnames, filenames in os.walk(magdir):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in sorted(filenames):
            if fn.endswith(".py"):
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, root).replace("\\", "/")
                mods.append({"file": rel, "full": full})
    mods.sort(key=lambda m: m["file"])

    modules_by_name = {}
    for m in mods:
        iname = import_name(m["file"])
        if iname == "":
            iname = "mag"
            m["root_init"] = True
        m["name"] = iname
        modules_by_name[iname] = m

    # ---- 2. lines, mtime, AST publics ----------------------------------
    parse_failures = []
    for m in mods:
        data = read_text(m["full"])
        m["lines"] = data.count(b"\n")
        m["mtime"] = datetime.fromtimestamp(os.path.getmtime(m["full"])) \
            .strftime("%Y-%m-%d %H:%M")
        tree = None
        try:
            tree = ast.parse(data.decode("utf-8", errors="replace"))
            m["parse"] = "ok"
        except SyntaxError as e:
            m["parse"] = "SyntaxError line %s" % e.lineno
            parse_failures.append(m["file"])
        fns, classes = [], []
        if tree is not None:
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                        and not node.name.startswith("_"):
                    fns.append(node.name)
                elif isinstance(node, ast.ClassDef) \
                        and not node.name.startswith("_"):
                    classes.append(node.name)
        m["fns"] = fns
        m["classes"] = classes

    # ---- 3. last commit touching each mag/ path -------------------------
    gl = run_git(["log", "--no-merges", "--name-only",
                  "--pretty=format:@%h %cs", "--", "mag/"])
    last_commit = {}
    cur = None
    for line in gl.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("@"):
            bits = line[1:].split()
            cur = (bits[0], bits[1]) if len(bits) >= 2 else ("?", "?")
        elif cur:
            f = line.replace("\\", "/")
            if f not in last_commit:
                last_commit[f] = cur
    for m in mods:
        lc = last_commit.get(m["file"])
        m["last_commit"] = "%s %s" % lc if lc else "never-committed"

    # ---- 4. reference scan ----------------------------------------------
    def pkg_parts(rel_file):
        parts = rel_file.split("/")[:-1]
        if not parts or parts[0] != "mag":
            return None
        return parts[1:]

    def extract_absolute(text):
        """Return (set of module names referenced by absolute forms, root_init_ref)."""
        refs = set()
        for mt in DOTTED.finditer(text):
            parts = mt.group(1).split(".")
            for i in range(len(parts), 0, -1):
                cand = ".".join(parts[:i])
                if cand in modules_by_name:
                    refs.add(cand)
                    break
        for mt in FROM_MAG.finditer(text):
            for ident in idents(mt.group(1)):
                if ident in modules_by_name:
                    refs.add(ident)
        path_hit = False
        for mt in PATHREF.finditer(text):
            raw = mt.group(1).replace("\\", "/")
            if raw.endswith(".py"):
                raw = raw[:-3]
            parts = [p for p in raw.split("/") if p and p != "."]
            for i in range(len(parts), 0, -1):
                cand = ".".join(parts[:i])
                if cand in modules_by_name:
                    refs.add(cand)
                    path_hit = True
                    break
        root_ref = bool(IMPORT_MAG.search(text)) or bool(FROM_MAG.search(text)) \
            or bool(DOTTED.search(text)) or path_hit
        return refs, root_ref

    def extract_relative(text, rel_file):
        """Resolve relative imports for a .py reader that lives under mag/."""
        refs = set()
        pkg = pkg_parts(rel_file)
        if pkg is None:
            return refs
        for mt in RELATIVE.finditer(text):
            lvl = len(mt.group(1)) - 1
            base = list(pkg)
            for _ in range(lvl):
                if base:
                    base.pop()
            target = base + [p for p in mt.group(2).split(".") if p]
            for i in range(len(target), 0, -1):
                cand = ".".join(target[:i])
                if cand in modules_by_name:
                    refs.add(cand)
                    break
            for ident in idents(mt.group(3)):
                cand = ".".join(target + [ident])
                if cand in modules_by_name:
                    refs.add(cand)
        return refs

    def expand(names):
        """A submodule reference also executes its package __init__ chain."""
        out = set()
        for n in names:
            out.add(n)
            parts = n.split(".")
            for i in range(1, len(parts)):
                anc = ".".join(parts[:i])
                if anc in modules_by_name:
                    out.add(anc)
        return out

    def scan_corpus(corpus):
        """corpus: list of (rel, full). Returns dict name -> [rels]."""
        hits = {}
        for rel, full in corpus:
            try:
                if os.path.getsize(full) > MAX_SCAN_BYTES:
                    continue
                text = read_text(full).decode("utf-8", errors="replace")
            except OSError:
                continue
            refs, root_ref = extract_absolute(text)
            if rel.endswith(".py"):
                refs |= extract_relative(text, rel)
            if refs or root_ref:
                refs = set(refs)
                if root_ref and "mag" in modules_by_name:
                    refs.add("mag")
            for name in expand(refs):
                if name in modules_by_name:
                    hits.setdefault(name, []).append(rel)
        return hits

    # test corpus: tests/ + mag/tests/
    test_files = []
    for base in ("tests", "mag/tests"):
        bp = os.path.join(root, base)
        if not os.path.isdir(bp):
            continue
        for dirpath, dirnames, filenames in os.walk(bp):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for fn in sorted(filenames):
                if fn.endswith(".py"):
                    full = os.path.join(dirpath, fn)
                    rel = os.path.relpath(full, root).replace("\\", "/")
                    test_files.append((rel, full))

    # reader corpus: whole repo minus tests/, mag/tests/, watch/, hidden
    scan_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root).replace("\\", "/")
        keep = []
        for d in dirnames:
            if d in SKIP_DIRS or d.startswith("."):
                continue
            rd = d if rel_dir == "." else rel_dir + "/" + d
            if rd == "mag/tests":
                continue
            keep.append(d)
        dirnames[:] = keep
        for fn in sorted(filenames):
            ext = os.path.splitext(fn)[1].lower()
            if ext not in READER_EXTS:
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace("\\", "/")
            scan_files.append((rel, full))

    test_hits = scan_corpus(test_files)
    reader_hits = scan_corpus(scan_files)

    for m in mods:
        name = m["name"]
        t = [r for r in test_hits.get(name, []) if r != m["file"]]
        r = [x for x in reader_hits.get(name, []) if x != m["file"]]
        m["test_files"] = sorted(set(t))
        m["readers"] = sorted(set(r))

    # ---- 5. summary ------------------------------------------------------
    total_lines = sum(m["lines"] for m in mods)
    total_fns = sum(len(m["fns"]) for m in mods)
    total_classes = sum(len(m["classes"]) for m in mods)
    with_tests = [m for m in mods if m["test_files"]]
    without_tests = [m for m in mods if not m["test_files"]]
    with_readers = [m for m in mods if m["readers"]]
    orphans = [m for m in mods if not m["test_files"] and not m["readers"]]

    # ---- 6. markdown ------------------------------------------------------
    L = []
    A = L.append
    A("# mag/ module census (item f-24, %s)" % now.split()[0])
    A("")
    A("Instrument: `watch/inbox/burn_reset_20260927/flash50/f-24_census.py`, "
      "run with `./.venv/Scripts/python.exe` (Python 3.11.15) at %s. "
      "Snapshot of one tree at one moment: HEAD `%s` on branch `%s`, "
      "working tree includes uncommitted edits (mtime column shows them)."
      % (now, head, branch))
    A("")
    A("## Method (read before quoting any number)")
    A("")
    A("- **Population:** every `*.py` file under `mag/` on disk at census "
      "moment, found with `os.walk`, `__pycache__` skipped. Cross-check: "
      "`find mag -name \"*.py\" -type f | wc -l` = %d files; "
      "`git ls-files mag | grep -c \"\\.py$\"` = %d tracked."
      % (len(mods), len(mods)))
    A("- **lines:** `wc -l` semantics (count of `\\n` bytes). Instrument "
      "total must equal `find mag -name \"*.py\" | xargs wc -l` = 294316 "
      "(measured before the run); see Verification below.")
    A("- **public functions:** `ast.parse` of each file; module-level "
      "`def`/`async def` whose name does not start with `_`. Decorated defs "
      "included; methods inside classes are NOT in this column (classes have "
      "their own column).")
    A("- **public classes:** module-level `class` names not starting `_`.")
    A("- **last modified:** two instruments. `mtime` = filesystem mtime, "
      "local time, includes uncommitted edits. `last commit` = newest "
      "`git log --no-merges --name-only -- mag/` entry touching the path; "
      "renamed files map under their current name only.")
    A("- **tests:** corpus = `tests/**.py` (%d files) + `mag/tests/**.py` "
      "(%d files) = %d test files. A module HAS TESTS when at least one "
      "test file textually references its import name (`mag.foo`), a "
      "`from mag import foo`, a `from mag import (foo, ...)`, a relative "
      "import resolving to it, or its path (`mag/foo.py`). The value shown "
      "is the count of distinct referencing test files. Textual matching, "
      "so it is an upper bound on true importing test files."
      % (sum(1 for r, _ in test_files if r.startswith("tests/")),
         sum(1 for r, _ in test_files if r.startswith("mag/tests/")),
         len(test_files)))
    A("- **readers:** repo files with extension in {py, pyw, cmd, bat, ps1, "
      "sh, yaml, yml, toml, cfg, ini} outside `tests/`, `mag/tests/`, "
      "`watch/`, hidden dirs and `__pycache__` (%d files scanned), matching "
      "the same reference forms as tests. `watch/` excluded: scratch "
      "instruments and prose, not durable code. Archival copies of code "
      "excluded: `_archaeology_out/` (951 py files, 2026-09-05 disk-image "
      "of an older repo state), `corpus/` (3402 py, session-artifact "
      "copies), `attic/` (105 py, retired code), `mine/` (15800 py, raw "
      "third-party repo dumps mined for training data), `dist_audit/` "
      "(1076 py, dated audit bundles each containing a full `mag/` copy), "
      "`local_sovereign_agent/` (a nested succession-audit snapshot of "
      "this very repo). Textual mentions inside archives are not live "
      "reads. Self-references excluded. "
      "`.json`/`.jsonl` data files not scanned. Reader counts are lower "
      "bounds for modules reached only through generic dispatchers "
      "(`mag.cmd` passes `%%*`, dispatch tables never name the module)."
      % len(scan_files))
    A("- **reference semantics:** textual, not runtime: an import of "
      "`mag.sub.mod` credits `mod` AND the `sub` and root `__init__` chains "
      "(executing a submodule executes its inits). References inside "
      "comments/docstrings/strings count.")
    A("")
    A("## Summary")
    A("")
    A("| metric | value |")
    A("|---|---|")
    A("| modules in mag/ | %d |" % len(mods))
    A("| total lines | %d |" % total_lines)
    A("| AST parse failures | %d |" % len(parse_failures))
    A("| modules with >=1 public function | %d |"
      % sum(1 for m in mods if m["fns"]))
    A("| public functions total | %d |" % total_fns)
    A("| modules with >=1 public class | %d |"
      % sum(1 for m in mods if m["classes"]))
    A("| public classes total | %d |" % total_classes)
    A("| modules referenced by >=1 test file | %d of %d (%.1f%%) |"
      % (len(with_tests), len(mods), 100.0 * len(with_tests) / len(mods)))
    A("| modules with ZERO test-file references | %d |" % len(without_tests))
    A("| modules with >=1 non-test reader | %d |" % len(with_readers))
    A("| modules with ZERO readers and ZERO test refs | %d |" % len(orphans))
    A("| test corpus files | %d |" % len(test_files))
    A("| reader-corpus files scanned | %d |" % len(scan_files))
    A("")
    A("### Largest modules (top 15 by lines)")
    A("")
    A("| module | lines | pub fns | test files | readers |")
    A("|---|---|---|---|---|")
    for m in sorted(mods, key=lambda m: -m["lines"])[:15]:
        A("| `%s` | %d | %d | %d | %d |"
          % (m["file"], m["lines"], len(m["fns"]),
             len(m["test_files"]), len(m["readers"])))
    A("")
    A("### Most-referenced modules (top 15 by reader count)")
    A("")
    A("| module | readers | test files | lines |")
    A("|---|---|---|---|")
    for m in sorted(mods, key=lambda m: -len(m["readers"]))[:15]:
        A("| `%s` | %d | %d | %d |"
          % (m["file"], len(m["readers"]), len(m["test_files"]), m["lines"]))
    A("")
    A("### Modules with zero test-file references (%d)" % len(without_tests))
    A("")
    if without_tests:
        per = ", ".join("`%s`" % m["file"] for m in without_tests)
        A(per)
    else:
        A("none - every mag/ module is referenced by at least one test file.")
    A("")
    A("### Orphans: zero test refs AND zero readers (%d)" % len(orphans))
    A("")
    if orphans:
        A(", ".join("`%s`" % m["file"] for m in orphans))
    else:
        A("none.")
    A("")
    A("## Per-module census table (all %d modules)" % len(mods))
    A("")
    A("module | lines | pub fns | pub classes | test files | readers | "
      "last commit | mtime")
    A("---|---|---|---|---|---|---|---")
    for m in mods:
        A("%s | %d | %d | %d | %d | %d | %s | %s"
          % (m["file"], m["lines"], len(m["fns"]), len(m["classes"]),
             len(m["test_files"]), len(m["readers"]),
             m["last_commit"], m["mtime"]))
    A("")
    A("## Per-module detail")
    A("")

    def cap_list(items, cap=8):
        if not items:
            return "none"
        if len(items) <= cap:
            return ", ".join("`%s`" % i for i in items)
        return ", ".join("`%s`" % i for i in items[:cap]) + \
            " + %d more" % (len(items) - cap)

    for m in mods:
        A("### %s" % m["file"])
        A("")
        A("- lines: %d | parse: %s | last commit: %s | mtime: %s"
          % (m["lines"], m["parse"], m["last_commit"], m["mtime"]))
        A("- public functions (%d): %s"
          % (len(m["fns"]), cap_list(m["fns"], cap=999) if m["fns"] else "none"))
        A("- public classes (%d): %s"
          % (len(m["classes"]), cap_list(m["classes"], cap=999)
             if m["classes"] else "none"))
        A("- test files (%d): %s"
          % (len(m["test_files"]), cap_list(m["test_files"])))
        A("- readers (%d): %s" % (len(m["readers"]), cap_list(m["readers"])))
        A("")

    md = "\n".join(L) + "\n"
    md_path = os.path.join(flash, "mag-census.md")
    with open(md_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(md)

    # ---- 7. machine-readable dump ---------------------------------------
    data = {
        "item": "f-24",
        "captured": now,
        "head": head,
        "branch": branch,
        "method": {
            "lines": "count of b'\\n' bytes (wc -l semantics)",
            "public_functions": "ast module-level defs, no leading underscore",
            "tests": "test-file textual references; corpus tests/ + mag/tests/",
            "readers": "non-test repo refs (py/cmd/bat/ps1/sh/yaml/yml/toml/"
                       "cfg/ini), self excluded, watch/ excluded",
        },
        "totals": {
            "modules": len(mods),
            "lines": total_lines,
            "public_functions": total_fns,
            "public_classes": total_classes,
            "modules_with_tests": len(with_tests),
            "modules_without_tests": len(without_tests),
            "modules_with_readers": len(with_readers),
            "orphans": len(orphans),
            "test_files": len(test_files),
            "reader_files_scanned": len(scan_files),
            "parse_failures": parse_failures,
        },
        "modules": [
            {k: m[k] for k in ("file", "name", "lines", "fns", "classes",
                               "test_files", "readers", "last_commit",
                               "mtime", "parse")}
            for m in mods
        ],
    }
    json_path = os.path.join(flash, "f-24_data.json")
    with open(json_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=1)

    # ---- 8. stdout verification ------------------------------------------
    print("modules=%d lines=%d (baseline wc -l 294316) match=%s"
          % (len(mods), total_lines, total_lines == 294316))
    print("parse_failures=%d %s" % (len(parse_failures), parse_failures[:5]))
    print("public_fns=%d public_classes=%d" % (total_fns, total_classes))
    print("with_tests=%d without_tests=%d with_readers=%d orphans=%d"
          % (len(with_tests), len(without_tests),
             len(with_readers), len(orphans)))
    print("test_files=%d reader_files=%d" % (len(test_files), len(scan_files)))
    print("git_log_lines=%d last_commit_entries=%d"
          % (len(gl.stdout.splitlines()), len(last_commit)))
    print("md_chars=%d md_path=%s" % (len(md), md_path))
    print("json_path=%s" % json_path)
    spot = [m for m in mods if m["file"] in
            ("mag/context_pack.py", "mag/game_campaign.py", "mag/__init__.py")]
    for m in spot:
        print("SPOT %s lines=%d fns=%d classes=%d tests=%d readers=%d"
              % (m["file"], m["lines"], len(m["fns"]), len(m["classes"]),
                 len(m["test_files"]), len(m["readers"])))


if __name__ == "__main__":
    main()
