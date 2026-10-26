#!/usr/bin/env python3
"""Generator for deep-compiler-bootstrap (flash50 deep item, 2026-09-28).

Builds the dependency graph of every tool in tools/ back to first principles:
  nodes  = tools/*.py (+ tools/index/*.py, mountain_check, llamacpp dirs)
  edges  = (a) AST imports of sibling tools (from tools.X import / import tools.X)
           (b) literal references to tools/<name>.py in source text
               (subprocess spawn args and docstrings both count: in a CLI
               estate the spawn edge is as load-bearing as the import edge)
  layers = stdlib / third-party / repo-internal (mag, dashboard, ...)

READ-ONLY over the repo; writes only its own JSON next to this file.
Run: .venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/deep_compiler_bootstrap_gen.py
"""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TOOLS = ROOT / "tools"
OUT = Path(__file__).resolve().parent / "deep_compiler_bootstrap_graph.json"

REPO_PKGS = {"mag", "tools", "dashboard", "catalog", "queue", "memory",
             "watch", "configs", "corpus", "scripts", "games", "state",
             "shared", "tests"}
SPAWN_RE = re.compile(r"tools[/\\]([a-zA-Z0-9_]+)\.py")
MAG_RE = re.compile(r"^mag\.([a-zA-Z0-9_]+)")


def classify(mod: str) -> str:
    rootmod = mod.split(".")[0]
    if rootmod in sys.stdlib_module_names:
        return "stdlib"
    if rootmod in REPO_PKGS:
        return "repo"
    return "third_party"


def tool_names() -> dict[str, Path]:
    """tool name -> file path, for every python tool in tools/."""
    out: dict[str, Path] = {}
    for p in sorted(TOOLS.iterdir()):
        if p.is_file() and p.suffix == ".py" and p.stem != "__init__":
            out[p.stem] = p
    for sub in ("index", "mountain_check"):
        d = TOOLS / sub
        if d.is_dir():
            for p in sorted(d.iterdir()):
                if p.is_file() and p.suffix == ".py" and p.stem != "__init__":
                    out[f"{sub}/{p.stem}"] = p
    return out


def parse_tool(name: str, path: Path) -> dict:
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return {"name": name, "error": str(e)}
    tree = ast.parse(src, filename=str(path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                imports.add(a.name)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            imports.add(node.module)
    sibling_refs = set(SPAWN_RE.findall(src))
    mag_mods = sorted({m.group(1) for m in (MAG_RE.match(i) for i in imports) if m})
    return {
        "name": name,
        "lines": src.count("\n") + 1,
        "imports": sorted(imports),
        "std": sorted({i for i in imports if classify(i) == "stdlib"}),
        "third": sorted({i for i in imports if classify(i) == "third_party"}),
        "repo_non_tools": sorted({i for i in imports
                                  if classify(i) == "repo" and i.split(".")[0] != "tools"}),
        "mag_modules": mag_mods,
        "sibling_imports": sorted({i.split(".")[1] for i in imports
                                   if i.startswith("tools.") and i.split(".")[1] in TOOL_SET}
                                  | {i.split(".")[2] for i in imports
                                     if i.startswith("tools.index.") or i.startswith("tools.mountain_check.")}),
        "sibling_spawns": sorted({s for s in sibling_refs
                                  if s in TOOL_SET or f"index/{s}" in TOOL_SET
                                  or f"mountain_check/{s}" in TOOL_SET}),
    }


TOOL_PATHS = tool_names()
TOOL_SET = set(TOOL_PATHS)

parsed = [parse_tool(n, p) for n, p in TOOL_PATHS.items()]

# pass 2: bare sibling imports (sys.path.insert makes `import drift` resolve to
# tools/drift.py) and repo-root substrate modules (config, llm) that dozens of
# tools reach via the same sys.path trick.
BARE_SIBLING_HINTS = TOOL_SET | {n.split("/")[-1] for n in TOOL_SET}
ROOT_MODULES = {"config", "llm"}
for rec in parsed:
    bare = [i for i in rec["third"] if i.split(".")[0] in BARE_SIBLING_HINTS]
    substrate = [i for i in rec["third"] if i.split(".")[0] in ROOT_MODULES]
    if bare:
        rec["sibling_imports"] = sorted(set(rec["sibling_imports"]) | {b.split(".")[0] for b in bare})
        rec["third"] = sorted(set(rec["third"]) - set(bare))
    if substrate:
        rec["substrate"] = substrate
        rec["third"] = sorted(set(rec["third"]) - set(substrate))

# --- upward dependents OUTSIDE tools/: mag/, scripts/, githooks, main.py ---
UPWARD_RE = re.compile(r"tools[/\\]([a-zA-Z0-9_/]+)\.py|from tools\.([a-zA-Z0-9_.]+)")
upward: dict[str, list[str]] = {}


def scan_upward(base: Path, label: str) -> None:
    for p in base.rglob("*"):
        if not p.is_file() or p.suffix not in (".py", ".ps1", ".sh", ""):
            continue
        if "__pycache__" in p.parts or ".venv" in p.parts:
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = f"{label}/{p.relative_to(base).as_posix()}"
        for m in UPWARD_RE.finditer(txt):
            hit = m.group(1) or m.group(2)
            hit = hit.split(".")[0].split("/")[0]
            if hit in TOOL_SET:
                upward.setdefault(hit, []).append(rel)


scan_upward(ROOT / "mag", "mag")
scan_upward(ROOT / "scripts", "scripts")
scan_upward(ROOT / "githooks", "githooks")
upward_files = ["main.py", "mag.cmd", "CONTRIBUTING.md"]
for f in upward_files:
    p = ROOT / f
    if p.is_file():
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in UPWARD_RE.finditer(txt):
            hit = (m.group(1) or m.group(2) or "").split(".")[0].split("/")[0]
            if hit in TOOL_SET:
                upward.setdefault(hit, []).append(f)

# --- graph ---
edges: list[dict] = []
in_deg: dict[str, int] = {n: 0 for n in TOOL_SET}
out_deg: dict[str, int] = {}
for rec in parsed:
    deps = set(rec.get("sibling_imports", [])) | set(rec.get("sibling_spawns", []))
    deps.discard(rec["name"])
    out_deg[rec["name"]] = len(deps)
    for d in sorted(deps):
        edges.append({"from": rec["name"], "to": d,
                      "kind": "import" if d in rec.get("sibling_imports", []) else "spawn"})
        in_deg[d] += 1

std_universe: dict[str, int] = {}
for rec in parsed:
    for s in rec.get("std", []):
        std_universe[s] = std_universe.get(s, 0) + 1
third_universe: dict[str, int] = {}
mag_universe: dict[str, int] = {}
for rec in parsed:
    for s in rec.get("third", []):
        third_universe[s.split(".")[0]] = third_universe.get(s.split(".")[0], 0) + 1
    for s in rec.get("repo_non_tools", []):
        mag_universe[s] = mag_universe.get(s, 0) + 1

zero_dep = sorted(n for n in TOOL_SET if out_deg.get(n, 0) == 0)
never_depended = sorted(n for n in TOOL_SET if in_deg[n] == 0)
stdlib_only = sorted(rec["name"] for rec in parsed
                     if not rec.get("third") and not rec.get("repo_non_tools")
                     and not rec.get("substrate") and out_deg.get(rec["name"], 0) == 0)
substrate_users = sorted(rec["name"] for rec in parsed if rec.get("substrate"))
spawn_users = sum(1 for rec in parsed if "subprocess" in rec.get("std", []))

summary = {
    "n_tools": len(TOOL_SET),
    "n_edges": len(edges),
    "edges": edges,
    "in_degree": in_deg,
    "out_degree": out_deg,
    "top_dependents": sorted(in_deg.items(), key=lambda kv: (-kv[1], kv[0]))[:15],
    "top_dependees": sorted(out_deg.items(), key=lambda kv: (-kv[1], kv[0]))[:15],
    "zero_internal_dep": zero_dep,
    "stdlib_only_zero_dep_count": len(stdlib_only),
    "stdlib_only_zero_dep": stdlib_only,
    "substrate_module_users": substrate_users,
    "spawn_users_count": spawn_users,
    "never_depended_on_count": len(never_depended),
    "stdlib_universe_top": sorted(std_universe.items(), key=lambda kv: (-kv[1], kv[0]))[:25],
    "stdlib_distinct": len(std_universe),
    "third_party_distinct": sorted(third_universe),
    "repo_internal_top": sorted(mag_universe.items(), key=lambda kv: (-kv[1], kv[0]))[:15],
    "upward_dependents": {k: sorted(set(v))[:8] for k, v in sorted(upward.items(), key=lambda kv: -len(kv[1]))},
    "upward_dependents_count": len(upward),
}
OUT.write_text(json.dumps({"summary": {k: v for k, v in summary.items() if k != "edges"},
                           "edges": edges}, sort_keys=True, indent=1), encoding="utf-8")
print(json.dumps({k: v for k, v in summary.items() if k != "zero_internal_dep"},
                 sort_keys=True, indent=1))
print(f"\nzero_internal_dep ({len(zero_dep)}): {zero_dep}")
print(f"index bytes: {OUT.stat().st_size}")
