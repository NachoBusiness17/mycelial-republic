"""s2-24 decorator census scanner (AST only).

Scans every .py file under mag/ and tools/, extracts every decorator
expression, resolves where each decorator is defined (builtin / stdlib /
third-party / in-repo), counts decorated functions (methods included) and
classes, checks docstrings and docs-tree mentions for in-repo decorators,
and writes:

  _s2_24_decorators.json  raw aggregates (receipt)
  decorator-census.md     the census

Reads source bytes only; the only subprocesses are three `git` reads
(rev-parse x2, ls-files) and each carries creationflags CREATE_NO_WINDOW
on win32 per the harness law.
"""
import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
OUT_DIR = ROOT / "watch" / "inbox" / "burn_reset_20260927" / "flash50"
TARGETS = ("mag", "tools")

BUILTIN_DEC = {"property", "staticmethod", "classmethod"}
BUILTIN_PROP_ATTRS = {"setter", "getter", "deleter"}

KIND_LABEL = {
    "inrepo": "custom",
    "builtin": "builtin",
    "stdlib": "stdlib",
    "thirdparty": "third-party",
    "module-as-decorator": "module-object",
    "unresolved-star-import": "unresolved (star import)",
    "unresolved": "unresolved",
    "expr": "raw expression",
}
PRIORITY = ["inrepo", "builtin", "stdlib", "thirdparty", "module-as-decorator",
            "unresolved-star-import", "unresolved", "expr"]

STD_DESC = {
    "property": "builtin: computed attribute getter",
    "property.setter": "builtin: defines the setter of a @property attribute",
    "property.getter": "builtin: re-binds the getter of an existing @property",
    "property.deleter": "builtin: defines the deleter of a @property attribute",
    "staticmethod": "builtin: method that receives no implicit self/cls",
    "classmethod": "builtin: method that receives cls instead of self",
    "functools.lru_cache": "stdlib: memoizes function results in an LRU cache",
    "functools.cache": "stdlib: lru_cache variant without a size limit",
    "functools.cached_property": "stdlib: computes an attribute once per instance, then caches it",
    "functools.wraps": "stdlib: copies __name__/__doc__/__module__ onto wrapper functions inside decorator bodies",
    "functools.singledispatch": "stdlib: dispatches calls on the type of the first argument",
    "functools.total_ordering": "stdlib: fills in the remaining comparison methods from __eq__ plus one ordering",
    "functools.singledispatchmethod": "stdlib: singledispatch on a method's second argument",
    "dataclasses.dataclass": "stdlib: generates __init__/__repr__/__eq__ from class annotations",
    "abc.abstractmethod": "stdlib: marks a method that concrete subclasses must override",
    "contextlib.contextmanager": "stdlib: turns a generator function into a with-statement factory",
    "contextlib.asynccontextmanager": "stdlib: async version of contextmanager",
    "typing.overload": "stdlib: declares alternate call signatures for type checkers",
    "enum.unique": "stdlib: raises when an enum defines a duplicated value",
}


def ascii_clean(s, limit=140):
    if not s:
        return ""
    s = s.replace("\u2014", "-").replace("\u2013", "-").replace("\u2015", "-")
    s = s.replace("\u2018", "'").replace("\u2019", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    out = s.encode("ascii", "replace").decode("ascii")
    out = " ".join(out.split())
    return out[:limit]


def dec_name(node):
    """Dotted name of a decorator expression, or None if it is not a
    Name/Attribute/Call-of-Name chain."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dec_name(node.value)
        if base is None:
            return None
        return base + "." + node.attr
    if isinstance(node, ast.Call):
        return dec_name(node.func)
    return None


def module_of(rel):
    name = rel[:-3].split("/")
    if name[-1] == "__init__":
        name = name[:-1]
    return ".".join(name)


def main():
    # ---- git context (subprocess with CREATE_NO_WINDOW on win32)
    gflags = {"capture_output": True, "text": True, "cwd": str(ROOT)}
    if os.name == "nt":
        gflags["creationflags"] = 0x08000000  # CREATE_NO_WINDOW
    head = ""
    branch = ""
    tracked = set()
    try:
        head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], **gflags).stdout.strip()
        branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], **gflags).stdout.strip()
        tracked = set(subprocess.run(["git", "ls-files", "--", "mag", "tools"], **gflags).stdout.splitlines())
    except OSError as e:
        print("git unavailable:", e)

    # ---- file discovery
    all_files = []
    per_target = {}
    dist = {}
    for t in TARGETS:
        ps = [p for p in sorted((ROOT / t).rglob("*.py")) if p.is_file()]
        per_target[t] = len(ps)
        for p in ps:
            rel = p.relative_to(ROOT).as_posix()
            all_files.append(rel)
            parts = rel.split("/")
            key = parts[0] if len(parts) == 1 else parts[0] + "/" + parts[1]
            dist[key] = dist.get(key, 0) + 1
    untracked = [r for r in all_files if r not in tracked]

    # ---- pass 1: parse + collect decorators, imports, aliases, defs
    parse_fail = []
    fileinfo = {}          # rel -> {nm, mods, aliases, star}
    module_to_file = {}    # module string -> rel
    defs = {}              # (rel, name) -> [ {lineno, kind, doc_head} ]
    uses = {}              # dotted name -> aggregate
    has_dec_files = set()
    occ_ast = 0
    occ_regex = 0
    total_funcs = 0
    total_classes = 0
    n_ok = 0

    for rel in all_files:
        p = ROOT / rel
        try:
            src = p.read_bytes()
        except OSError as e:
            parse_fail.append((rel, "read error: %s" % e))
            continue
        try:
            tree = ast.parse(src, filename=rel)
        except SyntaxError as e:
            parse_fail.append((rel, "SyntaxError: %s" % e))
            continue
        n_ok += 1
        module_to_file[module_of(rel)] = rel
        for line in src.splitlines():
            if line.strip().startswith(b"@"):
                occ_regex += 1

        info = {"nm": {}, "mods": set(), "aliases": {}, "star": False}
        fileinfo[rel] = info
        nm, mods, aliases = info["nm"], info["mods"], info["aliases"]

        for stmt in tree.body:
            if (isinstance(stmt, ast.Assign) and len(stmt.targets) == 1
                    and isinstance(stmt.targets[0], ast.Name)):
                v = stmt.value
                dotted = None
                if isinstance(v, (ast.Name, ast.Attribute)):
                    dotted = dec_name(v)
                elif isinstance(v, ast.Call):
                    dotted = dec_name(v.func)
                if dotted:
                    aliases[stmt.targets[0].id] = dotted

        def add_use(owner, dnode, kind, in_class):
            nonlocal occ_ast
            occ_ast += 1
            has_dec_files.add(rel)
            name = dec_name(dnode)
            key = name if name else "<expr>"
            is_call = isinstance(dnode, ast.Call)
            u = uses.get(key)
            if u is None:
                u = uses[key] = {"funcs": 0, "methods": 0, "classes": 0,
                                 "files": set(), "calls": 0, "bare": 0,
                                 "count": 0, "examples": []}
            u["count"] += 1
            if kind == "class":
                u["classes"] += 1
            else:
                u["funcs"] += 1
                if in_class:
                    u["methods"] += 1
            u["files"].add(rel)
            if is_call:
                u["calls"] += 1
            else:
                u["bare"] += 1
            if len(u["examples"]) < 3:
                u["examples"].append([rel, owner.lineno])

        def reg_def(node, kind):
            if (rel, node.name) not in defs:
                defs[(rel, node.name)] = [{
                    "lineno": node.lineno,
                    "kind": kind,
                    "doc_head": ascii_clean(ast.get_docstring(node) or ""),
                }]

        def visit(node, in_class):
            nonlocal total_funcs, total_classes
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.Import):
                    for a in child.names:
                        mods.add(a.name)
                        if a.asname:
                            nm[a.asname] = a.name
                    continue
                if isinstance(child, ast.ImportFrom):
                    lvl = child.level or 0
                    base = ""
                    if lvl:
                        pkg = rel.split("/")[:-1]
                        cut = len(pkg) - (lvl - 1)
                        if cut > 0:
                            base = ".".join(pkg[:cut])
                    mod = child.module or ""
                    full = base + "." + mod if (base and mod) else (base or mod)
                    for a in child.names:
                        if a.name == "*":
                            info["star"] = True
                            continue
                        nm[a.asname or a.name] = (full + "." + a.name) if full else a.name
                    if full:
                        mods.add(full)
                    continue
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    total_funcs += 1
                    reg_def(child, "def")
                    for d in child.decorator_list:
                        add_use(child, d, "func", in_class)
                    visit(child, in_class)
                    continue
                if isinstance(child, ast.ClassDef):
                    total_classes += 1
                    reg_def(child, "class")
                    for d in child.decorator_list:
                        add_use(child, d, "class", in_class)
                    visit(child, True)
                    continue
                visit(child, in_class)

        visit(tree, False)

    # ---- pass 2: resolve each decorator name per using-file
    def resolve(rel, dotted):
        im = fileinfo[rel]
        parts = dotted.split(".")
        hops = 0
        while parts[0] in im["aliases"] and hops < 5:
            tail = parts[1:]
            dotted = im["aliases"][parts[0]] + ("." + ".".join(tail) if tail else "")
            parts = dotted.split(".")
            hops += 1
        if dotted in BUILTIN_DEC:
            return "builtin", "builtins"
        if len(parts) == 2 and parts[0] == "property" and parts[1] in BUILTIN_PROP_ATTRS:
            return "builtin", "builtins"
        target = None
        if parts[0] in im["nm"]:
            target = im["nm"][parts[0]] + ("." + ".".join(parts[1:]) if len(parts) > 1 else "")
        else:
            best = ""
            for m in im["mods"]:
                if (dotted == m or dotted.startswith(m + ".")) and len(m) > len(best):
                    best = m
            if best:
                target = dotted
        if target is None:
            rec = defs.get((rel, parts[-1]))
            if rec:
                return "inrepo", "%s:%d" % (rel, rec[0]["lineno"])
            return ("unresolved-star-import" if im["star"] else "unresolved"), ""
        tp = target.split(".")
        best_cut = 0
        for cut in range(len(tp), 0, -1):
            if ".".join(tp[:cut]) in module_to_file:
                best_cut = cut
                break
        if best_cut:
            if best_cut == len(tp):
                return "module-as-decorator", target
            f2 = module_to_file[".".join(tp[:best_cut])]
            attr = tp[best_cut]
            rec = defs.get((f2, attr))
            site = "%s:%s" % (f2, rec[0]["lineno"] if rec else "?")
            return "inrepo", site
        top = tp[0]
        if top in getattr(sys, "stdlib_module_names", ()):
            return "stdlib", target
        return "thirdparty", target

    rows = []
    for key, u in uses.items():
        if key == "<expr>":
            kind, origins = "expr", []
        else:
            kinds = {}
            origins = []
            for f in sorted(u["files"]):
                k, o = resolve(f, key)
                kinds[k] = kinds.get(k, 0) + 1
                if o and o not in origins:
                    origins.append(o)
            kind = next((k for k in PRIORITY if k in kinds), "unresolved")
        rows.append({
            "name": key,
            "kind": kind,
            "kinds_seen": {k: v for k, v in sorted(kinds.items())} if key != "<expr>" else {},
            "origins": origins,
            "funcs": u["funcs"],
            "methods": u["methods"],
            "classes": u["classes"],
            "files": sorted(u["files"]),
            "count": u["count"],
            "calls": u["calls"],
            "bare": u["bare"],
            "examples": u["examples"],
        })
    rows.sort(key=lambda r: (-r["funcs"], r["name"]))

    # ---- docs-tree mention scan for in-repo decorators
    doc_files = []
    skipped_docs = []
    for p in sorted((ROOT / "docs").rglob("*")):
        if p.is_file() and p.suffix.lower() in (".md", ".txt", ".rst"):
            doc_files.append(p)
    doc_files += [p for p in sorted(ROOT.glob("*.md")) if p.is_file()]
    doc_corpus = []
    doc_bytes_total = 0
    for p in doc_files:
        try:
            if p.stat().st_size > 5 * 1024 * 1024:
                skipped_docs.append(p.relative_to(ROOT).as_posix())
                continue
            data = p.read_bytes()
            doc_corpus.append((p.relative_to(ROOT).as_posix(), data))
            doc_bytes_total += len(data)
        except OSError:
            skipped_docs.append(p.relative_to(ROOT).as_posix())

    custom_names = []
    for r in rows:
        if r["kind"] == "inrepo":
            n = r["name"].split(".")[-1]
            if n not in custom_names:
                custom_names.append(n)
    name_hits = {n: {"files": 0, "example": ""} for n in custom_names}
    if custom_names:
        alt = re.compile(rb"\b(" + b"|".join(re.escape(n.encode()) for n in custom_names) + rb")\b")
        for relstr, data in doc_corpus:
            seen_here = set(alt.findall(data))
            for raw in seen_here:
                n = raw.decode()
                name_hits[n]["files"] += 1
                if not name_hits[n]["example"]:
                    name_hits[n]["example"] = relstr

    for r in rows:
        r["doc_head"] = ""
        r["docs_files"] = 0
        r["docs_example"] = ""
        r["docstring"] = False
        if r["kind"] == "inrepo":
            n = r["name"].split(".")[-1]
            recs = []
            for o in r["origins"]:
                path, _, ln = o.rpartition(":")
                rec = defs.get((path, n))
                if rec:
                    recs.append(rec[0])
            r["docstring"] = bool(recs and any(x["doc_head"] for x in recs))
            r["doc_head"] = next((x["doc_head"] for x in recs if x["doc_head"]), "")
            hit = name_hits.get(n, {"files": 0, "example": ""})
            r["docs_files"] = hit["files"]
            r["docs_example"] = hit["example"]

    # ---- totals
    decorated_funcs = sum(r["funcs"] for r in rows)
    decorated_methods = sum(r["methods"] for r in rows)
    decorated_classes = sum(r["classes"] for r in rows)
    unique_names = len([r for r in rows if r["name"] != "<expr>"])
    expr_rows = len([r for r in rows if r["name"] == "<expr>"])
    n_calls = sum(r["calls"] for r in rows)
    n_bare = sum(r["bare"] for r in rows)
    kind_count = {}
    for r in rows:
        kind_count[r["kind"]] = kind_count.get(r["kind"], 0) + 1

    # ---- markdown
    L = []
    A = L.append
    A("# s2-24: decorator census - mag/ + tools/")
    A("")
    A("Date: 2026-09-28. Snapshot: branch `%s`, HEAD `%s` (read at scan time)."
      % (branch or "unknown", head or "unknown"))
    A("")
    A("Scope: every decorator expression on every function, method, and class in")
    A("every .py file under `mag/` and `tools/` (recursive), extracted with")
    A("Python `ast` from source bytes. All numbers below come from the scanner")
    A("run recorded in the Receipt section.")
    A("")
    A("## Method")
    A("")
    A("- interpreter: `.venv/Scripts/python.exe` (%s)" % (sys.version.split()[0]))
    A("- scanner: `watch/inbox/burn_reset_20260927/flash50/_s2_24_scan.py`")
    A("  (AST walk, bytes in, no shell spawn except three `git` reads with")
    A("  CREATE_NO_WINDOW on win32)")
    A("- run command: `.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/_s2_24_scan.py`")
    A("- files found: mag %d + tools %d = %d .py; parsed OK %d; parse failures %d"
      % (per_target["mag"], per_target["tools"], len(all_files), n_ok, len(parse_fail)))
    A("- untracked .py in scope (git ls-files): %d%s"
      % (len(untracked), ": " + ", ".join(untracked[:8]) if untracked else ""))
    A("- decorator expressions collected by ast: %d" % occ_ast)
    A("- independent recount: physical lines whose stripped form starts with `@`: %d"
      % occ_regex)
    A("  (difference %d; explained in Limits)" % (occ_regex - occ_ast))
    A("- docs corpus scanned for custom-decorator mentions: %d files, %d bytes"
      % (len(doc_corpus), doc_bytes_total))
    A("")
    A("## Totals")
    A("")
    A("- unique decorator names: %d%s" % (unique_names, " (+%d raw-expression row)" % expr_rows if expr_rows else ""))
    A("- decorated functions incl. methods (decorator-to-def rows, a def with N decorators counts N times): %d (of which methods: %d)"
      % (decorated_funcs, decorated_methods))
    A("- decorated classes (same counting rule): %d" % decorated_classes)
    A("- total defs in scope: %d functions + %d classes" % (total_funcs, total_classes))
    A("- files containing at least one decorator: %d of %d parsed"
      % (len(has_dec_files), n_ok))
    A("- call form vs bare form: %d `@x(...)` / %d bare `@x`" % (n_calls, n_bare))
    A("- rows by kind: " + ", ".join("%s %d" % (KIND_LABEL.get(k, k), v) for k, v in sorted(kind_count.items(), key=lambda kv: -kv[1])))
    A("")
    A("Tree shape (files per second-level dir, top 12): " +
      ", ".join("%s %d" % kv for kv in sorted(dist.items(), key=lambda kv: -kv[1])[:12]))
    A("")
    A("## Table: every unique decorator name (sorted by function uses)")
    A("")
    A("| decorator | kind | origin / def site | funcs | methods | classes | files | call-form |")
    A("|---|---|---|---:|---:|---:|---:|---:|")
    for r in rows:
        if len(r["origins"]) > 2:
            origin = "; ".join(r["origins"][:2]) + " (+%d more)" % (len(r["origins"]) - 2)
        else:
            origin = "; ".join(r["origins"])
        A("| `@%s` | %s | %s | %d | %d | %d | %d | %d |"
          % (r["name"], KIND_LABEL.get(r["kind"], r["kind"]), origin,
             r["funcs"], r["methods"], r["classes"], len(r["files"]), r["calls"]))
    A("")

    # ---- stdlib / third-party grouped summary
    A("## Stdlib and third-party decorators (what they do)")
    A("")
    A("Standard-library semantics are Python semantics; one line each. Unknown")
    A("origins are left to their own module docs rather than guessed.")
    A("")
    A("| decorator | origin module | funcs | what it does |")
    A("|---|---|---:|---|")
    for r in rows:
        if r["kind"] in ("builtin", "stdlib", "thirdparty"):
            origin = r["origins"][0] if r["origins"] else "?"
            mod = origin.split(".")[0] if origin != "builtins" else "builtins"
            desc = STD_DESC.get(r["name"])
            if desc is None:
                desc = "semantics: see %s docs (not restated here)" % origin
            A("| `@%s` | %s | %d | %s |" % (r["name"], origin, r["funcs"], desc))
    A("")

    # ---- custom decorators
    customs = [r for r in rows if r["kind"] == "inrepo"]
    doc_n = len([r for r in customs if r["docstring"] and r["docs_files"] > 0])
    ds_only = len([r for r in customs if r["docstring"] and r["docs_files"] == 0])
    undoc = len([r for r in customs if not r["docstring"] and r["docs_files"] == 0])
    A("## Custom decorators (defined inside mag/ or tools/)")
    A("")
    A("Custom decorator names: %d. Documentation rubric: **documented** = has a "
      "docstring at the definition AND >=1 mention of its name in `docs/` or a "
      "root `*.md`; **docstring-only** = docstring, no doc-tree mention; "
      "**undocumented** = neither. Mixed rows (one of the two signals) state "
      "their exact evidence in the block. Result: %d documented / %d "
      "docstring-only / %d undocumented."
      % (len(customs), doc_n, ds_only, undoc))
    A("")
    for r in customs:
        n = r["name"].split(".")[-1]
        A("### `@%s`" % r["name"])
        A("")
        A("- def site(s): %s" % ("; ".join(r["origins"]) if r["origins"] else "?"))
        kind_txt = ""
        for o in r["origins"]:
            path, _, ln = o.rpartition(":")
            rec = defs.get((path, n))
            if rec:
                kind_txt = "class" if rec[0]["kind"] == "class" else "function"
                break
        if kind_txt:
            A("- decorator is a %s" % kind_txt)
        A("- docstring at def: %s%s" % ("yes" if r["docstring"] else "no",
                                       (": \"%s\"" % r["doc_head"]) if r["doc_head"] else ""))
        A("- doc-tree mentions: %d file(s)%s" % (
            r["docs_files"],
            ("; example: %s" % r["docs_example"]) if r["docs_example"] else ""))
        A("- uses: %d function(s) (%d methods), %d class(es), across %d file(s); count %d (%d call-form)"
          % (r["funcs"], r["methods"], r["classes"], len(r["files"]), r["count"], r["calls"]))
        A("- first use sites: %s" % ", ".join("%s:%d" % (e[0], e[1]) for e in r["examples"]))
        if r["docstring"] and r["docs_files"] > 0:
            verdict = "documented (docstring + doc-tree mention)"
        elif r["docstring"]:
            verdict = "docstring-only (no doc-tree mention)"
        elif r["docs_files"] > 0:
            verdict = "doc-tree mention only (no docstring at def)"
        else:
            verdict = "undocumented"
        A("- verdict: %s" % verdict)
        A("")

    # ---- unresolved
    unres = [r for r in rows if r["kind"] in ("unresolved", "unresolved-star-import", "module-as-decorator", "expr")]
    A("## Unresolved or special rows")
    A("")
    if unres:
        for r in unres:
            A("- `@%s` (%s): %d use(s) in %d file(s); first: %s:%d"
              % (r["name"], r["kind"], r["count"], len(r["files"]),
                 r["examples"][0][0], r["examples"][0][1]))
    else:
        A("- none: every decorator name resolved to builtin, stdlib, third-party,")
        A("  or an in-repo definition site.")
    A("")

    # ---- limits
    A("## Limits")
    A("")
    A("- Static ast scan: decorators attached dynamically (getattr, a decorator")
    A("  registry dict, decorator lib apply(), manual wrapper assignment) do not")
    A("  appear; only syntactic `@` applications count.")
    A("- Names bound by `from x import *` cannot be resolved; files with star")
    A("  imports: %d." % len([rel for rel, im in fileinfo.items() if im["star"]]))
    A("- The regex recount counts any physical line starting with `@` including")
    A("  ones inside string literals or comments and multi-line decorator-call")
    A("  arg lines never start with @; the ast count is the census number, the")
    A("  regex number is a second instrument for the same tree.")
    A("- A def with several decorators contributes one row-hit per decorator,")
    A("  so per-kind sums exceed distinct decorated defs; distinct-decorator")
    A("  def counts are not separately reported (row sums are the ask's unit:")
    A("  how many functions use each decorator).")
    A("- docs mention check is name-based (`\\bname\\b`) over docs/ + root *.md:")
    A("  short generic names can match prose (overcount); example file given")
    A("  per custom decorator so a human can spot-check.")
    A("- Aliases (module-level `name = decorator` assignments) resolved up to")
    A("  5 hops; deeper alias chains would show as unresolved.")
    A("- Class decorators are reported in their own column; the ask's headline")
    A("  unit is functions, which for this census includes methods (methods")
    A("  also broken out).")
    A("- parse failures: %s" % ("; ".join("%s (%s)" % pf for pf in parse_fail) if parse_fail else "none"))
    if skipped_docs:
        A("- doc files skipped over 5MB: %s" % ", ".join(skipped_docs))
    A("")
    A("## Receipt")
    A("")
    A("- instrument: `watch/inbox/burn_reset_20260927/flash50/_s2_24_scan.py`")
    A("- raw aggregates: `watch/inbox/burn_reset_20260927/flash50/_s2_24_decorators.json`")
    A("- twins: `decorator-census.md` and `s2-24.md` in the same directory,")
    A("  byte-identical (hash recorded in the commit message)")
    A("")

    md = "\n".join(L) + "\n"
    out_md = OUT_DIR / "decorator-census.md"
    out_md.write_text(md, encoding="utf-8", newline="\n")

    # ---- JSON receipt
    def jsonable(r):
        return {k: v for k, v in r.items()}
    payload = {
        "date": "2026-09-28",
        "branch": branch,
        "head": head,
        "targets": per_target,
        "files_total": len(all_files),
        "files_parsed_ok": n_ok,
        "parse_failures": parse_fail,
        "untracked_py": untracked,
        "occurrences_ast": occ_ast,
        "occurrences_regex_lines": occ_regex,
        "unique_decorator_names": unique_names,
        "expr_rows": expr_rows,
        "decorated_funcs_rows_sum": decorated_funcs,
        "decorated_methods_rows_sum": decorated_methods,
        "decorated_classes_rows_sum": decorated_classes,
        "total_funcs": total_funcs,
        "total_classes": total_classes,
        "files_with_decorator": len(has_dec_files),
        "call_form": n_calls,
        "bare_form": n_bare,
        "kind_counts": kind_count,
        "docs_corpus_files": len(doc_corpus),
        "docs_corpus_bytes": doc_bytes_total,
        "custom_counts": {"documented": doc_n, "docstring_only": ds_only,
                          "undocumented": undoc, "total": len(customs)},
        "rows": [jsonable(r) for r in rows],
    }
    (OUT_DIR / "_s2_24_decorators.json").write_text(
        json.dumps(payload, indent=1, sort_keys=False), encoding="utf-8", newline="\n")

    # ---- stdout summary
    print("HEAD", head, "branch", branch)
    print("files", per_target, "ok", n_ok, "fail", len(parse_fail), "untracked", len(untracked))
    print("occ_ast", occ_ast, "occ_regex", occ_regex)
    print("unique_names", unique_names, "expr_rows", expr_rows)
    print("funcs_rows", decorated_funcs, "methods", decorated_methods,
          "classes", decorated_classes, "total_funcs", total_funcs, "total_classes", total_classes)
    print("files_with_dec", len(has_dec_files), "/", n_ok)
    print("call", n_calls, "bare", n_bare)
    print("kinds", kind_count)
    print("customs", len(customs), "documented", doc_n, "docstring_only", ds_only,
          "undocumented", undoc)
    print("md_chars", len(md.encode("utf-8")))
    print("top10:")
    for r in rows[:10]:
        print("  @%s funcs=%d files=%d kind=%s" % (r["name"], r["funcs"], len(r["files"]), r["kind"]))
    print("customs:")
    for r in customs:
        print("  @%s funcs=%d docs_files=%d docstring=%s origins=%s"
              % (r["name"], r["funcs"], r["docs_files"], r["docstring"],
                 ";".join(r["origins"][:3])))


if __name__ == "__main__":
    main()
