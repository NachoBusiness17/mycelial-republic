"""prepush_verkle_hermeticity -- pytest-hermeticity tripwire for the verkle spine.

Cause (proven 2026-10-10, receipt
watch/inbox/mates_leave_protocol/receipts/receipt_20261010_archaeologist.md):
tests/test_merkle_cure_p4b_sized.py test_cross_arm_composition_leaf_domain_
untouched called a local helper that wrote through mag.verkle_knot WITHOUT
taking the file's estate fixture, so vk.CHAIN/vk.TIP stayed the LIVE
memory/biography/ paths and a pytest run overwrote the live provenance chain
with 3 fixture rows (byte-proven: fixture leaf hashes + legacy roots at chain
head). The one-test fix landed in the working tree 2026-10-10; this tool makes
the CLASS standing instead of per-test discipline (the B2-336 conftest
pattern, applied as a detector).

What it flags: a test function in tests/*.py that transitively (through
module-level helpers) reaches a WRITE on the mag.verkle_knot module surface
without protection. Writes are:
  (a) calls to the module's known writer functions (append_verkle_knot,
      _append_verkle_knot_unlocked, _rewrite_chain, _write_tip_atomic,
      repair_tip_if_consistent, consolidate_chain_one_leaf_per_session,
      _consolidate_chain_one_leaf_per_session_unlocked, _retire_knot,
      _sync_latest_knot, _update_topic_evolution), and
  (b) write-method calls on the module's live-path globals (BIO, KNOTS,
      CHAIN, TIP, LATEST, EVOLUTION, LOCK): p.write_text/write_bytes/open/
      unlink/replace/rename/mkdir/touch.
Protection is ANY of:
  - the test requests a fixture that (transitively, within the file)
    references the verkle module alias at all (the estate fixtures
    monkeypatch.setattr(vk, "CHAIN", ...) and aliases the trip),
  - the test body itself redirects: monkeypatch.setattr(...) referencing the
    alias, or a direct assignment to alias.PATH_GLOBAL.
Module-level (outside any function) writer shapes are always violations.

Honest limits (documented, not hidden): builtin open(vk.CHAIN, "w") shapes,
cross-module writers (mag/diary_node.py append_diary_to_verkle,
mag/chain_substrate.py writers, mag/ghost_auto.py KNOTS writes) and
subprocess-mediated writes are OUT of scope for v1; fixtures defined in
tests/conftest.py are not resolvable as protection (none redirects verkle
paths today); name-based call resolution assumes unique helper names per
file. This is a tripwire for the proven shape, not a proof of full
hermeticity.

CLI (exit 0 clean, 1 findings, 2 cannot-verify):
  tools/prepush_verkle_hermeticity.py                # scan tests/
  tools/prepush_verkle_hermeticity.py --files a b    # scan named files
  tools/prepush_verkle_hermeticity.py --selftest     # synthetic battery
Output contract (B2-338): green first line opens "VERKLE-HERMETICITY: ok";
findings open "VERKLE-HERMETICITY: WARN"; internal errors "VERKLE-HERMETICITY: ERROR".
"""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

MODULE_NAMES = {"verkle_knot"}
WRITER_FUNCS = frozenset({
    "append_verkle_knot",
    "_append_verkle_knot_unlocked",
    "_rewrite_chain",
    "_write_tip_atomic",
    "repair_tip_if_consistent",
    "consolidate_chain_one_leaf_per_session",
    "_consolidate_chain_one_leaf_per_session_unlocked",
    "_retire_knot",
    "_sync_latest_knot",
    "_update_topic_evolution",
})
PATH_GLOBALS = frozenset({"BIO", "KNOTS", "CHAIN", "TIP", "LATEST", "EVOLUTION", "LOCK"})
PATH_WRITE_METHODS = frozenset({
    "write_text", "write_bytes", "open", "unlink", "replace", "rename",
    "mkdir", "touch",
})


def _alias_names(tree: ast.Module) -> set[str]:
    """Import aliases that bind mag.verkle_knot, plus directly imported
    writer function names."""
    aliases: set[str] = set()
    direct_writers: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name in ("mag.verkle_knot", "verkle_knot"):
                    aliases.add(a.asname or a.name.split(".")[-1])
        elif isinstance(node, ast.ImportFrom):
            if node.module in ("mag.verkle_knot", "verkle_knot"):
                for a in node.names:
                    if a.name in WRITER_FUNCS:
                        direct_writers.add(a.asname or a.name)
                    elif a.name in MODULE_NAMES:
                        aliases.add(a.asname or a.name)
            elif node.module == "mag" or node.module is None:
                for a in node.names:
                    if a.name in MODULE_NAMES:
                        aliases.add(a.asname or a.name)
    return aliases | direct_writers


def _refs_alias(node: ast.AST, aliases: set[str]) -> bool:
    """True if the subtree references any verkle module alias."""
    for n in ast.walk(node):
        if isinstance(n, ast.Name) and n.id in aliases:
            return True
        if isinstance(n, ast.Attribute):
            # mag.verkle_knot.X chains end in an Attribute whose value chain
            # bottoms out at Name("mag"); the attr name check covers
            # `import mag.verkle_knot` (no asname) usage.
            if n.attr in aliases | MODULE_NAMES:
                return True
    return False


def _writer_shapes(node: ast.AST, aliases: set[str], direct: set[str]) -> list[str]:
    """Return writer-shape names found in this statement/expr subtree."""
    found: list[str] = []
    for n in ast.walk(node):
        if not isinstance(n, ast.Call) or not isinstance(n.func, ast.Attribute):
            continue
        attr = n.func.attr
        base = n.func.value
        # (a) alias.writer(...)
        if attr in WRITER_FUNCS and _refs_alias(base, aliases):
            found.append(f"{attr}()")
        # (b) alias.PATH.write_xyz(...)
        if (
            attr in PATH_WRITE_METHODS
            and isinstance(base, ast.Attribute)
            and base.attr in PATH_GLOBALS
            and _refs_alias(base.value, aliases)
        ):
            found.append(f"{base.attr}.{attr}()")
    # directly imported writers called bare
    for n in ast.walk(node):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            if n.func.id in direct & WRITER_FUNCS:
                found.append(f"{n.func.id}()")
    return found


class _Module:
    def __init__(self) -> None:
        self.funcs: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = {}
        self.tests: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = {}
        self.fixtures: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = {}
        self.top_writer_shapes: list[str] = []
        self.alias: set[str] = set()
        self.direct: set[str] = set()
        self.calls: dict[str, set[str]] = {}


def _parse_module(tree: ast.Module) -> _Module:
    m = _Module()
    m.alias = _alias_names(tree)
    m.direct = {
        n.id for n in ast.walk(tree)
        if isinstance(n, ast.Name)
    } & WRITER_FUNCS if _imports_direct_writer(tree) else set()
    # fixture decorators
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            m.funcs[node.name] = node
            is_fixture = any(
                (isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute)
                 and d.func.attr == "fixture")
                or (isinstance(d, ast.Attribute) and d.attr == "fixture")
                or (isinstance(d, ast.Name) and d.id == "fixture")
                for d in node.decorator_list
            )
            if is_fixture:
                m.fixtures[node.name] = node
            if node.name.startswith("test_"):
                m.tests[node.name] = node
            else:
                shapes = _writer_shapes(node, m.alias, m.direct)
                if shapes:
                    # helper holding writer shapes: remember per name
                    m.calls.setdefault("__writers__", set()).add(node.name)
        elif not isinstance(node, (ast.Import, ast.ImportFrom,
                                   ast.FunctionDef, ast.AsyncFunctionDef,
                                   ast.ClassDef)):
            shapes = _writer_shapes(node, m.alias, m.direct)
            if shapes:
                m.top_writer_shapes.extend(shapes)
    # classes: collect methods as pseudo top-level by qualified name
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    qname = f"{node.name}.{sub.name}"
                    m.funcs[qname] = sub
                    if sub.name.startswith("test_"):
                        m.tests[qname] = sub
    # call graph (name-based, unique-name assumption documented)
    for name, fn in m.funcs.items():
        outs: set[str] = set()
        for n in ast.walk(fn):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
                outs.add(n.func.id)
                if n.func.id in m.funcs and n.func.id != name:
                    pass
        m.calls[name] = {c for c in outs if c in m.funcs and c != name}
    return m


def _imports_direct_writer(tree: ast.Module) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module in (
                "mag.verkle_knot", "verkle_knot"):
            if any(a.name in WRITER_FUNCS for a in node.names):
                return True
    return False


def _protecting_fixtures(mod: _Module) -> set[str]:
    """Fixtures whose body references the alias, transitively closed over
    fixture-depends-on-fixture params."""
    protecting: set[str] = set()
    changed = True
    while changed:
        changed = False
        for name, fn in mod.fixtures.items():
            if name in protecting:
                continue
            touches = _refs_alias(fn, mod.alias)
            feeds = any(
                a.arg in protecting for a in fn.args.args
            )
            if touches or feeds:
                protecting.add(name)
                changed = True
    return protecting


def _test_reaches_writer(mod: _Module, test_name: str,
                         writer_helpers: set[str]) -> bool:
    seen: set[str] = {test_name}
    stack = [test_name]
    fn = mod.funcs.get(test_name)
    if fn is None:
        return False
    if _writer_shapes(fn, mod.alias, mod.direct):
        return True
    while stack:
        cur = stack.pop()
        for callee in mod.calls.get(cur, ()):
            if callee in seen:
                continue
            seen.add(callee)
            if callee in writer_helpers or callee in WRITER_FUNCS:
                return True
            callee_fn = mod.funcs.get(callee)
            if callee_fn is not None and _writer_shapes(callee_fn, mod.alias, mod.direct):
                return True
            stack.append(callee)
    return False


def _test_protected(mod: _Module, fn, protecting: set[str]) -> bool:
    if any(a.arg in protecting for a in fn.args.args):
        return True
    # body-level redirect: monkeypatch.setattr(... alias ...) or alias.PATH = ...
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) \
                and n.func.attr == "setattr":
            if _refs_alias(n, mod.alias):
                return True
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Attribute) and t.attr in PATH_GLOBALS \
                        and _refs_alias(t.value, mod.alias):
                    return True
    return False


def scan_source(source: str, filename: str = "<string>") -> list[str]:
    """Return finding lines for one test module's source."""
    findings: list[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return [f"ERROR {filename}: unparseable ({e.msg})"]
    mod = _parse_module(tree)
    if not mod.alias and not mod.direct:
        return findings  # file never touches verkle_knot: out of scope
    if mod.top_writer_shapes:
        findings.append(
            f"VIOLATION {filename}: module-level writer shape "
            f"{', '.join(sorted(set(mod.top_writer_shapes)))} can never be fixture-protected")
    protecting = _protecting_fixtures(mod)
    writer_helpers = mod.calls.get("__writers__", set())
    for tname, fn in sorted(mod.tests.items()):
        if not _test_reaches_writer(mod, tname, writer_helpers):
            continue
        if not _test_protected(mod, fn, protecting):
            findings.append(
                f"VIOLATION {filename}:{fn.lineno}: {tname} reaches a "
                f"verkle_knot writer with no redirecting fixture "
                f"(estate-style) in its parameter closure")
    return findings


def scan_path(p: Path) -> list[str]:
    try:
        # utf-8-sig, not utf-8: 2026-10-20 archaeologist cycle 10. A test file
        # with a leading UTF-8 BOM (tests/test_grokbot_seats.py) parses fine
        # under the import system (PEP 263 strips it) but ast.parse chokes on
        # the leading U+FEFF kept by a plain utf-8 decode, which error-exited
        # the whole scan (exit 2, "cannot verify") and blinded the tripwire.
        return scan_source(p.read_text(encoding="utf-8-sig"), str(p).replace("\\", "/"))
    except (OSError, UnicodeDecodeError) as e:
        return [f"ERROR {p}: unreadable ({e})"]


def scan_tree(tests_dir: Path) -> list[str]:
    findings: list[str] = []
    for p in sorted(tests_dir.rglob("test_*.py")):
        findings.extend(scan_path(p))
    return findings


def selftest() -> int:
    ok = True

    def check(name: str, source: str, want_violations: int) -> None:
        nonlocal ok
        f = scan_source(source, f"selftest/{name}.py")
        got = len([x for x in f if x.startswith("VIOLATION")])
        flag = "PASS" if got == want_violations else "FAIL"
        if got != want_violations:
            ok = False
        print(f"{flag} {name}: violations={got} want={want_violations}"
              + ("" if got == want_violations else f" :: {f}"))

    fixture = (
        "import pytest\n"
        "from mag import verkle_knot as vk\n"
        "@pytest.fixture\n"
        "def estate(tmp_path, monkeypatch):\n"
        "    monkeypatch.setattr(vk, 'CHAIN', tmp_path / 'c.jsonl')\n"
        "    monkeypatch.setattr(vk, 'TIP', tmp_path / 't.json')\n"
    )
    helper = (
        "def _hand_chain():\n"
        "    vk._write_tip_atomic({})\n"
        "    vk.CHAIN.write_bytes(b'x')\n"
    )
    # 1: the historic clobber shape: helper writes, test takes no fixture
    check("violating_no_fixture",
          "from mag import verkle_knot as vk\n" + helper +
          "def test_cross_arm():\n    _hand_chain()\n", 1)
    # 2: the cure shape: same helper, test takes the estate fixture
    check("protected_by_estate",
          "import pytest\nfrom mag import verkle_knot as vk\n" +
          "@pytest.fixture\ndef estate(tmp_path, monkeypatch):\n"
          "    monkeypatch.setattr(vk, 'CHAIN', tmp_path / 'c.jsonl')\n" +
          helper +
          "def test_cross_arm(estate):\n    _hand_chain()\n", 0)
    # 3: body-level redirect protects
    check("protected_by_body_setattr",
          "import pytest\nfrom mag import verkle_knot as vk\n"
          "def test_direct(tmp_path, monkeypatch):\n"
          "    monkeypatch.setattr(vk, 'CHAIN', tmp_path / 'c.jsonl')\n"
          "    vk.CHAIN.write_bytes(b'x')\n", 0)
    # 4: module-level writer shape always violates
    check("module_level_writer",
          "from mag import verkle_knot as vk\n"
          "vk.CHAIN.write_bytes(b'x')\n"
          "def test_any():\n    pass\n", 1)
    # 5: reads only: clean
    check("read_only_clean",
          "from mag import verkle_knot as vk\n"
          "def test_read():\n    return vk.CHAIN.exists()\n", 0)
    # 6: fixture depends on protecting fixture (transitive)
    check("protected_transitive_fixture",
          "import pytest\nfrom mag import verkle_knot as vk\n" +
          "@pytest.fixture\ndef estate(tmp_path, monkeypatch):\n"
          "    monkeypatch.setattr(vk, 'CHAIN', tmp_path / 'c.jsonl')\n"
          "@pytest.fixture\ndef rib_estate(estate):\n"
          "    return estate\n" +
          helper +
          "def test_rib(rib_estate):\n    _hand_chain()\n", 0)
    print("SELFTEST " + ("PASS" if ok else "FAILED"))
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="verkle pytest-hermeticity tripwire")
    ap.add_argument("--files", nargs="*", help="scan these files instead of tests/")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.files:
        findings: list[str] = []
        for f in a.files:
            findings.extend(scan_path(Path(f)))
    else:
        root = Path(__file__).resolve().parents[1]
        tdir = root / "tests"
        if not tdir.is_dir():
            print("VERKLE-HERMETICITY: ERROR no tests/ dir")
            return 2
        findings = scan_tree(tdir)
    if [f for f in findings if f.startswith("ERROR")]:
        for f in findings:
            print(f"VERKLE-HERMETICITY: {f}")
        print("VERKLE-HERMETICITY: ERROR (cannot verify)")
        return 2
    if findings:
        for f in findings:
            print(f"VERKLE-HERMETICITY: {f}")
        print(f"VERKLE-HERMETICITY: WARN ({len(findings)} finding(s))")
        return 1
    print("VERKLE-HERMETICITY: ok (no unprotected verkle_knot writer reach in tests)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
