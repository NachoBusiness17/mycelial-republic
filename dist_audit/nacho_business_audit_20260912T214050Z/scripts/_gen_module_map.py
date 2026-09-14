"""_gen_module_map.py — surface every mag module with its REAL purpose + metadata.

Operator (2026-08-15): "look into what each does deeply and try to surface them inside of the live tools."
This reads each mag/*.py docstring (the real purpose), classifies it (family / refcount / schema), and emits
module_map_data.js for a browsable live Module Map. Real bytes — purpose comes from each module's own
docstring, never invented.

Schema: _gen_module_map.v1 · deterministic + $0 · read-only
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAG = ROOT / "mag"
OUT = ROOT / "module_map_data.js"

FAMILIES = [("roshomon", r"roshomon|witness|consensus"), ("flock", r"flock|boid|shader|renderman|field"),
            ("memweave", r"memweave|weave|distribut"), ("verkle", r"verkle|knot|chain|merkle|dirac"),
            ("rib", r"rib_|standing.?wave|rib\b"), ("gpu", r"gpu|vram|roc|quantiz|process_supervisor"),
            ("grok", r"grok|grokbot"), ("queue", r"queue|drain|worker|swarm"),
            ("gap", r"gap|frontier|moonshot|deep.?research|advisor|council"),
            ("game", r"game|mud|dnd|wow|dungeon|quest|npc|saelis|dm"), ("dash", r"dashboard|desk|seat|clawbot|ghost_"),
            ("memory", r"memory|mem|percolat|learn|biograph|knot|recall|weave|surrogate"),
            ("steal", r"steal|mine|harvest|corpus|research|scan|audit")]


def _family(name: str) -> str:
    n = name.lower()
    for f, pat in FAMILIES:
        if re.search(pat, n):
            return f
    return "misc"


def _purpose(text: str) -> str:
    """First docstring line(s) — the module's own statement of what it does."""
    m = re.search(r'"""(.*?)"""', text, re.S)
    if not m:
        return ""
    first = m.group(1).strip().splitlines()
    lines = [ln.strip().lstrip("#* ") for ln in first if ln.strip() and not ln.strip().startswith(("import", "from"))]
    if not lines:
        return ""
    return " ".join(lines[:3])[:180]


def _schema(text: str) -> str:
    m = re.search(r"Schema:\s*([\w.]+)", text)
    return m.group(1) if m else ""


def _module_names() -> set[str]:
    """The set of actual mag module stems — so the string-literal ref matcher only counts
    REAL modules, not common words / function args that happen to appear in quotes."""
    try:
        return {p.stem for p in MAG.glob("*.py") if not p.stem.startswith("_")}
    except OSError:
        return set()


_MODULE_NAMES = _module_names()


def _ref_index(ALL: str) -> "dict[str,int]":
    """Single pass over the whole code index; count every module reference once.

    SELF-STEAL correction (2026-08-15): the old regex only saw IDENTIFIER refs
    (mag.<name>, from mag import <name>, import <name>) and MISSED the string-literal
    dynamic dispatch that the whole cadence is built on:
        _import_run("auto_handoff", "run", None)   # name is a STRING, not an identifier
        orchestrator enqueue "[seat-steer]..." / _import_run("vscode_seat", ...)
    That made live, wired-in modules (auto_handoff, vscode_seat, shared_context, ...)
    show refs=0 -> falsely tagged 'orphan'. A broken lens — acting on it would have
    retired LIVE modules. Now we ALSO count quoted module-name strings.
    """
    from collections import Counter
    c: Counter = Counter()
    # 1) identifier refs: mag.<name>, from mag import <name>, import <name>, bare <name>( call
    for m in re.finditer(r"(?:mag\.([A-Za-z_]\w*))|(?:from\s+mag\s+import\s+([A-Za-z_]\w*))|(?:import\s+([A-Za-z_]\w*))|(?:import\s+mag\s+as\s+([A-Za-z_]\w*))", ALL):
        name = m.group(1) or m.group(2) or m.group(3) or m.group(4)
        if name:
            c[name] += 1
    # 2) string-literal dynamic dispatch: _import_run("name", ...), _import_run('name', ...),
    #    "mag.<name>", "<name>.py", and the mag module-name as a quoted atom in import helpers.
    for m in re.finditer(r'["\'](?:mag\.)?([a-z][a-z0-9_]{2,60})["\']', ALL):
        name = m.group(1)
        if name.endswith(".py"):
            name = name[:-3]
        # only count names that look like our modules (not common words/args)
        if name in _MODULE_NAMES:
            c[name] += 1
    return c


def main() -> None:
    # build one big code index for refcount (same as the notebook audit)
    code_dirs = ["mag", "scripts", "dashboard", "tools", "backend", "router", "configs", "deploy", "tests", "queue", "models"]
    parts = []
    for d in code_dirs:
        p = ROOT / d
        if p.is_dir():
            for f in p.rglob("*.py"):
                try:
                    parts.append(f.read_text(encoding="utf-8", errors="replace"))
                except OSError:
                    pass
    for f in ("main.py", "mag_launch.py", "config.py", "conftest.py"):
        try:
            parts.append((ROOT / f).read_text(encoding="utf-8", errors="replace"))
        except OSError:
            pass
    ALL = "\n".join(parts)
    REF = _ref_index(ALL)  # single-pass refcount map

    rows = []
    for p in sorted(MAG.glob("*.py")):
        name = p.stem
        if name.startswith("_"):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        refs = REF.get(name, 0)
        rows.append({
            "name": name,
            "purpose": _purpose(text),
            "schema": _schema(text),
            "family": _family(name),
            "refs": refs,
            "tier": "live" if refs > 2 else ("low" if refs > 0 else "orphan"),
        })

    js = "// AUTO-GENERATED from mag/*.py docstrings (real purposes). mag/_gen_module_map.py\n"
    js += "const MODULE_MAP = " + json.dumps(rows, ensure_ascii=False) + ";\n"
    OUT.write_text(js, encoding="utf-8")
    from collections import Counter
    print(f"wrote {OUT.name}: {len(rows)} modules; tiers " + dict(Counter(r['tier'] for r in rows)).__str__())


if __name__ == "__main__":
    main()
