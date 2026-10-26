"""ITEM f-29: repo-wide silent-exception-handler census instrument.

Scans the ENTIRE readable working tree of the Mag Resource Harness repo for
Python files carrying silent exception handlers: any except-handler whose
body consists only of `pass` statements. A pass-only body can contain no
logging call, no re-raise, no handling of any kind, so "except: pass" and
"except Exception: pass without logging" are both exactly this shape.

Method: os.walk over the working tree (prunes .git, __pycache__, and any
directory holding pyvenv.cfg, i.e. virtualenvs), ast.parse per file, then a
context-tracking NodeVisitor over every ExceptHandler node. For every
pass-only handler the instrument records:
  - repo-relative file path
  - line number of the except clause (1-based, ast lineno)
  - the exception type EXACTLY AS WRITTEN in the source (BARE for a bare
    `except:`), via ast.get_source_segment
  - category: bare / broad (Exception, BaseException) / typed
  - whether the handler is a single-line `except ...: pass` form
  - the enclosing def/class/lambda chain (nearest three)
  - the first source line of the try body: the operation whose failure is
    being swallowed
  - git-tracked yes/no (git ls-files, subprocess spawned with
    creationflags CREATE_NO_WINDOW on win32 per repo law)
Also counts, for denominator context: every ExceptHandler node, ellipsis-only
handler bodies (`except X: ...`), and contextlib *.suppress(...) call sites.

Emits: _f29_scan.json (raw rows + aggregates, ascii-escaped),
silent-pass-census.md (full enumeration table, every hit), and a stdout
headline block. Markdown snippets are sanitized of em/en dashes; raw source
bytes survive in the JSON as \\uXXXX escapes. A leading UTF-8 BOM is stripped
before ast.parse because BOM-prefixed files are legal Python source and must
be censused, not misfiled as parse failures (line numbers unaffected).
"""

import ast
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
OUT_JSON = os.path.join(HERE, "_f29_scan.json")
OUT_MD = os.path.join(HERE, "silent-pass-census.md")

CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0
PRUNE_DIRS = {".git", "__pycache__"}
DASHES = {"\u2014": "--", "\u2013": "-", "\u2212": "-"}
OVERSIZE = 50 * 1024 * 1024

unreadable = []


def on_walk_error(err):
    unreadable.append(getattr(err, "filename", None) or str(err))


def sanitize(s):
    for k, v in DASHES.items():
        s = s.replace(k, v)
    return s


def one_line(s, cap=90):
    s = " ".join(s.split())
    if len(s) > cap:
        s = s[:cap].rstrip() + " ..."
    return s


class Scanner(ast.NodeVisitor):
    def __init__(self, src, rel, acc):
        self.src = src
        self.rel = rel
        self.acc = acc
        self.stack = []
        self.try_stack = []

    def _push(self, node, label):
        name = getattr(node, "name", "<lambda>")
        self.stack.append(label + " " + str(name))
        self.generic_visit(node)
        self.stack.pop()

    def visit_FunctionDef(self, node):
        self._push(node, "def")

    def visit_AsyncFunctionDef(self, node):
        self._push(node, "async def")

    def visit_ClassDef(self, node):
        self._push(node, "class")

    def visit_Lambda(self, node):
        self._push(node, "lambda")

    def visit_Try(self, node):
        self.try_stack.append(node)
        self.generic_visit(node)
        self.try_stack.pop()

    def visit_TryStar(self, node):
        self.visit_Try(node)

    def visit_ExceptHandler(self, node):
        acc = self.acc
        acc["handlers_total"] += 1
        body = node.body
        if body and all(isinstance(s, ast.Pass) for s in body):
            if node.type is None:
                exc_raw = "BARE except"
                cat = "bare"
            else:
                exc_raw = ast.get_source_segment(self.src, node.type)
                if exc_raw is None:
                    try:
                        exc_raw = ast.unparse(node.type)
                    except Exception:
                        exc_raw = "<unrenderable>"
                exc_raw = exc_raw.strip()
                cat = "broad" if exc_raw in ("Exception", "BaseException") else "typed"
            try_first = ""
            if self.try_stack:
                tn = self.try_stack[-1]
                if tn.body:
                    seg = ast.get_source_segment(self.src, tn.body[0]) or ""
                    try_first = one_line(seg)
            ctx = " / ".join(self.stack[-3:]) if self.stack else "<module>"
            inline = bool(body[0].lineno == node.lineno)
            acc["hits"].append({
                "file": self.rel,
                "line": node.lineno,
                "end_line": node.end_lineno if node.end_lineno else node.lineno,
                "exc_raw": exc_raw,
                "cat": cat,
                "inline": inline,
                "ctx": ctx,
                "try_first": try_first,
            })
            acc["cat"][cat] += 1
            acc["inline_count"] += 1 if inline else 0
            top = self.rel.split("/")[0] if "/" in self.rel else "."
            acc["inline_by_top"][top] = \
                acc["inline_by_top"].get(top, 0) + (1 if inline else 0)
            acc["cat_by_top"][top] = acc["cat_by_top"].get(
                top, {"bare": 0, "broad": 0, "typed": 0})
            acc["cat_by_top"][top][cat] += 1
        elif (len(body) == 1 and isinstance(body[0], ast.Expr)
              and isinstance(body[0].value, ast.Constant)
              and body[0].value.value is Ellipsis):
            acc["ellipsis_count"] += 1
        self.generic_visit(node)


def main():
    acc = {
        "hits": [],
        "handlers_total": 0,
        "ellipsis_count": 0,
        "suppress_sites": 0,
        "inline_count": 0,
        "inline_by_top": {},
        "cat_by_top": {},
        "cat": {"bare": 0, "broad": 0, "typed": 0},
    }
    files_seen = 0
    parsed_ok = 0
    parse_errors = []
    by_file = {}
    by_top = {}
    venv_trees = []
    py_in_venv = 0
    started = datetime.now(timezone.utc)

    def count_venv_py(vroot):
        nonlocal py_in_venv
        for _dp, _dns, fns in os.walk(vroot, onerror=on_walk_error):
            py_in_venv += sum(1 for fn in fns if fn.endswith(".py"))

    for dirpath, dirnames, filenames in os.walk(ROOT, onerror=on_walk_error):
        keep = []
        for d in dirnames:
            if d in PRUNE_DIRS:
                continue
            if os.path.exists(os.path.join(dirpath, d, "pyvenv.cfg")):
                vd = os.path.relpath(os.path.join(dirpath, d), ROOT)
                venv_trees.append(vd.replace("\\", "/"))
                count_venv_py(os.path.join(dirpath, d))
                continue
            keep.append(d)
        dirnames[:] = keep
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            files_seen += 1
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT).replace("\\", "/")
            try:
                if os.path.getsize(full) > OVERSIZE:
                    parse_errors.append([rel, "OversizeSkip: >50MB"])
                    continue
                with open(full, "rb") as f:
                    raw = f.read()
                src = raw.decode("utf-8", errors="replace")
                # A leading UTF-8 BOM is legal in real Python source but
                # ast.parse on the decoded string rejects it; strip it so
                # BOM-prefixed files are censused instead of misfiled as
                # parse failures. Line numbers are unaffected (same line).
                if src.startswith("\ufeff"):
                    src = src.lstrip("\ufeff")
                tree = ast.parse(src)
            except SyntaxError as e:
                parse_errors.append([rel, "SyntaxError: " + str(e)[:120]])
                continue
            except (OSError, ValueError, MemoryError, RecursionError) as e:
                parse_errors.append([rel, type(e).__name__ + ": " + str(e)[:120]])
                continue
            parsed_ok += 1
            sc = Scanner(src, rel, acc)
            sc.visit(tree)
            for node in ast.walk(tree):
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                        and node.func.attr == "suppress"):
                    acc["suppress_sites"] += 1

    hits = acc["hits"]
    for h in hits:
        rel = h["file"]
        by_file[rel] = by_file.get(rel, 0) + 1
        top = rel.split("/")[0] if "/" in rel else "."
        by_top[top] = by_top.get(top, 0) + 1

    gr = subprocess.run(
        ["git", "-C", ROOT, "ls-files", "-z", "--", "*.py"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        creationflags=CREATE_NO_WINDOW,
    )
    tracked = set()
    if gr.returncode == 0:
        for b in gr.stdout.split(b"\0"):
            if b:
                tracked.add(b.decode("utf-8", errors="replace").replace("\\", "/"))
    for h in hits:
        h["tracked"] = h["file"] in tracked

    hits.sort(key=lambda h: (h["file"], h["line"]))
    files_with_hits = sorted(by_file)
    tracked_hits = sum(1 for h in hits if h["tracked"])
    unreadable_unique = sorted(set(unreadable))

    meta = {
        "item": "f-29",
        "generated_utc": started.isoformat(timespec="seconds"),
        "python": sys.version.split()[0],
        "root": ROOT,
        "definition": "except-handler whose body is only pass statements",
        "files_seen": files_seen,
        "parsed_ok": parsed_ok,
        "parse_errors": len(parse_errors),
        "handlers_total": acc["handlers_total"],
        "hits_total": len(hits),
        "hits_tracked": tracked_hits,
        "hits_untracked": len(hits) - tracked_hits,
        "cat": acc["cat"],
        "inline_count": acc["inline_count"],
        "multiline_count": len(hits) - acc["inline_count"],
        "ellipsis_bodies": acc["ellipsis_count"],
        "suppress_sites": acc["suppress_sites"],
        "files_with_hits": len(files_with_hits),
        "venv_trees_pruned": sorted(venv_trees),
        "py_in_venv_excluded": py_in_venv,
        "unreadable_paths": len(unreadable_unique),
        "by_file": by_file,
        "by_top": by_top,
        "inline_by_top": acc["inline_by_top"],
        "cat_by_top": acc["cat_by_top"],
        "parse_error_rows": parse_errors,
        "hits": hits,
    }

    with open(OUT_JSON, "w", encoding="ascii", errors="backslashreplace") as f:
        json.dump(meta, f, ensure_ascii=True, indent=1, sort_keys=True)

    # ---- markdown emit ----
    L = []
    A = L.append
    A("# Silent exception handler census (f-29)")
    A("")
    A("Generated %s UTC by `_f29_silent_pass_scan.py` (Python %s ast walk)." %
      (started.strftime("%Y-%m-%d %H:%M"), sys.version.split()[0]))
    A("")
    A("## Definition")
    A("")
    A("A hit is any `except` handler whose body consists only of `pass`")
    A("statements: `except: pass`, `except Exception: pass`,")
    A("`except SomeError: pass`, single-line or multi-line. A pass-only body")
    A("contains no logging call, no re-raise, no handling of any kind, so")
    A("every hit is by construction a handler without logging. Comments after")
    A("`pass` do not change the shape (comments are not statements).")
    A("")
    A("## Scope and denominators")
    A("")
    A("- Root walked: repo working tree `%s`" % ROOT.replace("\\", "/"))
    A("- Files seen (.py): %d" % files_seen)
    A("- Parsed OK (ast): %d" % parsed_ok)
    A("- Parse failures (recorded, not silently dropped): %d" % len(parse_errors))
    A("- Virtualenv trees pruned: %d (%s), holding %d .py files excluded as third-party"
      % (len(venv_trees), ", ".join(sorted(venv_trees)) if venv_trees else "none", py_in_venv))
    A("- Unreadable paths (PermissionError on walk): %d unique; their contents are"
      % len(unreadable_unique))
    A("  NOT in any denominator. These are pytest scratch dirs and transient lock")
    A("  files held by concurrent lanes; the readable-tree numbers above are the")
    A("  census of record.")
    A("")
    A("## Findings")
    A("")
    A("- Silent (pass-only) except handlers: **%d**" % len(hits))
    A("- Files carrying at least one: %d of %d parsed" % (len(files_with_hits), parsed_ok))
    A("- Total except handlers in scanned code: %d (silent = %.1f%%)" %
      (acc["handlers_total"], 100.0 * len(hits) / acc["handlers_total"] if acc["handlers_total"] else 0.0))
    A("- Git-tracked hits: %d; untracked (scratch/backup trees): %d" %
      (tracked_hits, len(hits) - tracked_hits))
    A("- bare `except:` (swallows everything incl. KeyboardInterrupt/SystemExit): %d" % acc["cat"]["bare"])
    A("- `except Exception:` / `except BaseException:` (broad): %d" % acc["cat"]["broad"])
    A("- typed specific exceptions: %d" % acc["cat"]["typed"])
    A("- single-line `except ...: pass` form: %d; multi-line form: %d" %
      (acc["inline_count"], len(hits) - acc["inline_count"]))
    A("")
    A("Adjacent shapes counted for context (NOT hits): ellipsis-only bodies")
    A("`except X: ...` = %d; `*.suppress(...)` call sites = %d." %
      (acc["ellipsis_count"], acc["suppress_sites"]))
    A("")
    A("## Breakdown by top-level directory")
    A("")
    A("| dir | silent handlers | bare | broad | typed |")
    A("|---|---|---|---|---|")
    for top in sorted(by_top, key=lambda k: -by_top[k]):
        cb = acc["cat_by_top"].get(top, {"bare": 0, "broad": 0, "typed": 0})
        A("| %s | %d | %d | %d | %d |" % (top, by_top[top], cb["bare"], cb["broad"], cb["typed"]))
    A("| TOTAL | %d | %d | %d | %d |" % (len(hits), acc["cat"]["bare"],
                                         acc["cat"]["broad"], acc["cat"]["typed"]))
    A("")
    A("## Full enumeration: every silent handler")
    A("")
    A("Columns: line (except clause, 1-based), except clause as written (what it")
    A("swallows), first line of the try body (the operation whose failure dies),")
    A("enclosing def/class chain, form. Files sorted by path; rows by line.")
    A("")
    for rel in files_with_hits:
        rows = [h for h in hits if h["file"] == rel]
        tflag = "tracked" if rows[0]["tracked"] else "UNTRACKED"
        A("### %s (%d, %s)" % (rel, len(rows), tflag))
        A("")
        A("| line | except clause | try body first line | context | form |")
        A("|---|---|---|---|---|")
        for h in rows:
            exc = sanitize(h["exc_raw"]).replace("|", "\\|")
            tf = sanitize(h["try_first"]).replace("|", "\\|")
            ctx = sanitize(h["ctx"]).replace("|", "\\|")
            A("| %d | `%s` | %s | %s | %s |" %
              (h["line"], exc, tf if tf else "(none)", ctx,
               "single-line" if h["inline"] else "multi-line"))
        A("")
    A("## Parse failures (%d)" % len(parse_errors))
    A("")
    A("Files seen but not ast-parseable; their except handlers (if any) are NOT")
    A("counted and that gap is explicit rather than silent:")
    A("")
    for rel, err in parse_errors[:200]:
        A("- %s: %s" % (rel, sanitize(err)))
    if len(parse_errors) > 200:
        A("- ... plus %d more in `_f29_scan.json`" % (len(parse_errors) - 200))
    A("")
    A("Raw rows + aggregates: `_f29_scan.json` (same directory).")
    A("")

    text = "\n".join(L)
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    print("=== f-29 headline ===")
    print("python:", sys.version.split()[0])
    print("files_seen:", files_seen)
    print("parsed_ok:", parsed_ok)
    print("parse_errors:", len(parse_errors))
    print("handlers_total:", acc["handlers_total"])
    print("silent_hits:", len(hits))
    print("files_with_hits:", len(files_with_hits))
    print("tracked_hits:", tracked_hits, "untracked_hits:", len(hits) - tracked_hits)
    print("cat:", acc["cat"])
    print("inline:", acc["inline_count"], "multiline:", len(hits) - acc["inline_count"])
    print("ellipsis_bodies:", acc["ellipsis_count"], "suppress_sites:", acc["suppress_sites"])
    print("venv_trees:", sorted(venv_trees), "py_in_venv:", py_in_venv)
    print("unreadable_unique:", len(unreadable_unique))
    print("by_top:", json.dumps(by_top, sort_keys=True))
    print("inline_by_top:", json.dumps(acc["inline_by_top"], sort_keys=True))
    print("md_bytes:", len(text.encode("utf-8")))
    print("unreadable sample:", unreadable_unique[:10])


if __name__ == "__main__":
    main()
