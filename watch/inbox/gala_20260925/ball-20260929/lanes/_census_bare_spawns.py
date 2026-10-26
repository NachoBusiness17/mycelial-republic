"""One-shot census helper for the bare-spawn-descent lane (2026-09-29).

Replicates tests/test_headless_law.py _scan() exactly (same rules, same
top-level globs) but also records line numbers so the descent can be done
site by site. Not a substitute for the ratchet; the ratchet test itself is
the finish-line check.
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SPAWN_NAMES = ("subprocess.run", "subprocess.Popen",
               "subprocess.check_call", "subprocess.check_output",
               "subprocess.getoutput", "subprocess.getstatusoutput")


def _spawn_call(node):
    f = node.func
    if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) \
            and f.value.id == "subprocess":
        return f"subprocess.{f.attr}"
    return None


def main() -> int:
    sites: list[dict] = []
    for d in ("tools", "tests"):
        for p in sorted((ROOT / d).glob("*.py")):
            try:
                tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
            except SyntaxError:
                continue
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                name = _spawn_call(node)
                if name in SPAWN_NAMES and not any(k.arg == "creationflags" for k in node.keywords):
                    sites.append({"file": rel, "line": node.lineno, "call": name})
    per_file: dict[str, int] = {}
    for s in sites:
        per_file[s["file"]] = per_file.get(s["file"], 0) + 1
    out = {"total": len(sites), "per_file": per_file, "sites": sites}
    print(json.dumps(out, indent=1))
    tests_total = sum(v for k, v in per_file.items() if k.startswith("tests/"))
    tools_total = sum(v for k, v in per_file.items() if k.startswith("tools/"))
    print(f"SUMMARY total={len(sites)} tests={tests_total} tools={tools_total}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
