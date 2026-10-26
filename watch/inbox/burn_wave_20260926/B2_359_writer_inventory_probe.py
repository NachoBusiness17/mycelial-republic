#!/usr/bin/env python3
"""B2-359 probe 1: inventory production-path writers and test-side risk.

Static half of the writer census. Two passes:

  pass A (writer inventory): every mag/*.py that names one of the four
  production trees (memory, logs, queue, watch) adjacent to a write-shaped
  call or path constant.

  pass B (test risk classes): every tests/*.py classified by the primitives
  that can reach production bytes without tmp/env injection:
    D  direct write primitive + production path string in the same file
    C  os.chdir / monkeypatch.chdir (relative-path writes land in prod)
    A  append-mode open anywhere (the falsifier class: jsonl appenders)
    W  imports a known mag writer module and calls it (needs side-sink
       isolation like the B2-80 helper to be provably clean)
  A file may hold several classes. Class membership is candidacy, not
  guilt: pass 2 (byte-still probes) decides.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROD_DIRS = ("memory", "logs", "queue", "watch")

WRITE_PRIM = re.compile(
    r"\.write_text\(|\.write_bytes\(|\.mkdir\(|os\.replace\(|os\.rename\(|"
    r"shutil\.(copy|copytree|move|rmtree)|\.touch\(|open\("
)
APPEND_OPEN = re.compile(r"open\([^)]*,\s*['\"][a*w]t?['\"]|open\([^)]*,\s*['\"]ab?['\"]")
PROD_PATH_STR = re.compile(
    r"[\"'](memory|logs|queue|watch)(/|\\\\|['\"])|[\"'](ROOT|BASE_DIR|ESTATE_ROOT)[\"']"
)
CHDIR = re.compile(r"os\.chdir\(|monkeypatch\.chdir\(|\.chdir\(")
# Known writer modules whose calls need side-sink isolation to be provably clean
WRITER_IMPORT = re.compile(
    r"from mag\.(temperature_stack|improve|training_events|state_snapshot|"
    r"agent_cli|orchestrator|lifecycle|shared_surface|index_events|board|"
    r"bio|attention|bonds)\s+import|import mag\.(temperature_stack|improve|"
    r"training_events|state_snapshot|agent_cli|orchestrator|lifecycle|"
    r"shared_surface)\b"
)
ROOT_CONST = re.compile(r"^ROOT\s*=|^[A-Z_]*ROOT[A-Z_]*\s*=|^BASE\s*=|^ESTATE_ROOT\s*=")


def scan_mag_writers():
    rows = []
    for py in sorted((ROOT / "mag").glob("*.py")):
        text = py.read_text(encoding="utf-8", errors="replace")
        hits = []
        for i, line in enumerate(text.splitlines(), 1):
            if any(f'"{d}"' in line or f"'{d}'" in line or f'"{d}/' in line or f"'{d}/" in line
                   for d in PROD_DIRS):
                if WRITE_PRIM.search(line) or re.search(r"=\s*ROOT|_PATH\s*[:=]|LOG\s*[:=]|_DIR\s*[:=]", line):
                    hits.append(i)
        if hits:
            rows.append({"file": str(py.relative_to(ROOT)), "lines": hits[:12], "n": len(hits)})
    return rows


def scan_tests():
    out = []
    for py in sorted((ROOT / "tests").glob("*.py")) + sorted((ROOT / "tests").glob("*_test.py")):
        text = py.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        cls = set()
        ev = {}
        has_root = any(ROOT_CONST.match(l) for l in lines)
        prod_lines = [i for i, l in enumerate(lines, 1)
                      if re.search(r"[\"'](memory|logs|queue|watch)[/\\]", l)]
        write_lines = [i for i, l in enumerate(lines, 1) if WRITE_PRIM.search(l)]
        if prod_lines and write_lines:
            cls.add("D")
            ev["D"] = {"prod": prod_lines[:8], "write": write_lines[:8]}
        if CHDIR.search(text):
            cls.add("C")
            ev["C"] = [i for i, l in enumerate(lines, 1) if CHDIR.search(l)][:8]
        if APPEND_OPEN.search(text):
            cls.add("A")
            ev["A"] = [i for i, l in enumerate(lines, 1) if APPEND_OPEN.search(l)][:8]
        if WRITER_IMPORT.search(text):
            cls.add("W")
            ev["W"] = [i for i, l in enumerate(lines, 1) if WRITER_IMPORT.search(l)][:8]
        if cls:
            out.append({"file": py.name, "classes": sorted(cls), "has_root_const": has_root,
                        "ev": ev})
    return out


def main():
    writers = scan_mag_writers()
    tests = scan_tests()
    report = {
        "writer_modules": writers,
        "writer_module_count": len(writers),
        "risk_files": tests,
        "risk_file_count": len(tests),
        "test_file_count": len(list((ROOT / "tests").glob("*.py")))
                          + len(list((ROOT / "tests").glob("*_test.py"))),
    }
    dest = Path(__file__).with_name("B2_359_static_census.json")
    dest.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"writer modules naming prod dirs: {len(writers)}")
    print(f"test files total: {report['test_file_count']}")
    print(f"test files with risk classes: {len(tests)}")
    by_cls = {}
    for t in tests:
        for c in t["classes"]:
            by_cls[c] = by_cls.get(c, 0) + 1
    print("by class:", json.dumps(by_cls))
    return 0


if __name__ == "__main__":
    sys.exit(main())
