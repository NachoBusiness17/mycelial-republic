"""ghost_pylance — Ghost's execution surface, distilled to a forkable pure-stdlib tool.

THE MECHANISM (our working implementation of this pattern):
  Ghost does its work through a DETERMINISTIC tool surface — never a blind terminal spawn.
  The core organ is GHOSTLANCE: Pylance-style code intelligence built on the stdlib `ast`
  module ($0, no deps). It GROUNDS the agent against the ACTUAL bytes of its code so it can
  VERIFY and CORRECT its work instead of trusting a stochastic recall. This is the
  anti-hallucination execution-side tool: the agent reasons, then checks itself against bytes.

MEMTOOLS (the ghost's code-intelligence organs):
  * diagnose(source)     -> AST diagnostics: syntax errors, undefined names, unused imports.
  * symbols(source)      -> document symbol map (defs/classes/assigns with line numbers).
  * imports(source)      -> dependency audit of one module (imported names vs used).
  * self_check(paths)    -> syntax-check every module: "N/N modules syntax-clean".

The grounding contract: a real typo is caught; an annotation-only reference (like `Any`,
`Path`) is treated as KNOWN (Pylance resolves those) so we don't raise false positives.

PURE STDLIB — ast, builtins, pathlib, json. Runs: python -m pytest tests/ -q
Schema: ghost_pylance.v1
"""
from __future__ import annotations

import ast
import builtins
from pathlib import Path
from typing import Any

SCHEMA = "ghost_pylance.v1"
_BUILTINS = set(dir(builtins))


# ---------------------------------------------------------------- helpers
def _defined_names(tree: ast.AST) -> set[str]:
    """All names bound in the module: defs, classes, assigns, imports, args."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    names.add(t.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
        elif isinstance(node, ast.Import):
            for a in node.names:
                names.add((a.asname or a.name).split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                names.add(a.asname or a.name)
        elif isinstance(node, ast.arg):
            names.add(node.arg)
    return names


def _used_names(tree: ast.AST) -> set[str]:
    """Names read (Load context) anywhere in the module."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            names.add(node.id)
    return names


def _annotation_names(tree: ast.AST) -> set[str]:
    """Name-references inside type annotations — treated as KNOWN (kills false positives)."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            _collect_ann(node.args, names)
            if node.returns is not None:
                _collect_ann(node.returns, names)
        elif isinstance(node, ast.AnnAssign) and node.annotation is not None:
            _collect_ann(node.annotation, names)
    return names


def _collect_ann(node: ast.AST, out: set[str]) -> None:
    for n in ast.walk(node):
        if isinstance(n, ast.Name):
            out.add(n.id)


def _imported_names(tree: ast.AST) -> dict[str, list[int]]:
    """Map of imported names -> line numbers (for unused-import detection)."""
    out: dict[str, list[int]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                out.setdefault((a.asname or a.name).split(".")[0], []).append(node.lineno)
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                if a.name != "*":
                    out.setdefault(a.asname or a.name, []).append(node.lineno)
    return out


# ---------------------------------------------------------------- memtools
def diagnose(source: str) -> dict[str, Any]:
    """AST diagnostics: syntax errors, undefined names, unused imports.

    Undefined = used - (defined | builtins | annotation-known). Returns a deterministic,
    grounded verdict an agent can act on without trusting its own recall.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return {"ok": False, "schema": SCHEMA, "syntax_error": {
            "line": e.lineno, "col": e.offset, "msg": e.msg, "text": (e.text or "").strip(),
        }, "undefined": [], "unused_imports": []}

    defined = _defined_names(tree)
    used = _used_names(tree)
    ann = _annotation_names(tree)

    undefined = sorted(
        n for n in used
        if n not in defined and n not in _BUILTINS and n not in ann
    )

    imported = _imported_names(tree)
    # an import is UNUSED if its name is never READ (Load) and never referenced in an
    # annotation — NOT merely because it was "defined" (the import itself defines it).
    used_reads = _used_names(tree) | ann
    unused_imports = sorted(
        {"name": name, "line": lines[0]}
        for name, lines in imported.items()
        if name not in used_reads and name not in _BUILTINS
    )

    return {"ok": True, "schema": SCHEMA, "syntax_error": None,
            "undefined": undefined, "unused_imports": unused_imports,
            "n_defined": len(defined), "n_used": len(used)}


def symbols(source: str) -> list[dict[str, Any]]:
    """Document symbol map: every def/class/assignment with its line + kind."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    out = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.append({"name": node.name, "line": node.lineno, "kind": "function"})
        elif isinstance(node, ast.ClassDef):
            out.append({"name": node.name, "line": node.lineno, "kind": "class"})
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    out.append({"name": t.id, "line": node.lineno, "kind": "assign"})
    out.sort(key=lambda x: x["line"])
    return out


def imports(source: str) -> dict[str, Any]:
    """Dependency audit of one module: what it imports and whether each is used."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {"ok": False, "schema": SCHEMA, "imports": []}
    imported = _imported_names(tree)
    used_in_body = _used_names(tree) | _defined_names(tree)
    return {"ok": True, "schema": SCHEMA, "imports": [
        {"name": name, "line": lines[0], "used": name in used_in_body}
        for name, lines in imported.items()
    ]}


def self_check(paths: list[str]) -> dict[str, Any]:
    """Syntax-check every module path: 'N/N modules syntax-clean'."""
    total, clean = 0, 0
    failures = []
    for p in paths:
        path = Path(p)
        if not path.is_file():
            continue
        total += 1
        try:
            compile(path.read_text(encoding="utf-8", errors="replace"), str(path), "exec")
            clean += 1
        except SyntaxError as e:
            failures.append({"path": str(path), "line": e.lineno, "msg": e.msg})
    return {"ok": clean == total, "schema": SCHEMA, "total": total, "clean": clean,
            "failures": failures}


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "self_check":
        print(self_check(sys.argv[2:] or ["."]))
    else:
        src = (
            "import os\n"
            "def greet(name):\n"
            "    return 'hi ' + name\n"
            "print(greet('world') + missing)\n"
        )
        print(diagnose(src))
