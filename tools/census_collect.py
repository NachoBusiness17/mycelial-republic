#!/usr/bin/env python3
"""census_collect.py - the --collect deep-check collectors (B2-365 split).

Owns the byte-gatherers for the census deep check, moved here verbatim from
tools/census_drift_patrol.py (2026-09-26) so the patrol file sits under the
ratchet 400-line bar with headroom for the next fix (the B2-248 split
precedent: self-contained block, sibling module, patrol keeps the CLI).

  COLLECT_TAIL_RE     the pytest --collect-only -q summary-tail grammar
  parse_collect_tail  collected total from the summary tail
  parse_collect_files the item-bearing file set from node-id lines
  collect_report      the subprocess gatherer (items + unique files)
  CollectError        cannot-verify condition; census_drift_patrol.run()
                      maps it to exit 2 exactly as it maps its own PatrolError

This module imports nothing from census_drift_patrol (no circular edge); the
patrol side reaches these names through thin delegating defs that lazy-import
here with the script directory on sys.path, the same context rule the
B2-248 self-test delegation documents. Behavior is byte-frozen at the split:
the pre-split patrol file sha256 head is ffe096be (the B2-469 pin).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# The pytest --collect-only -q summary tail: "N tests collected in T.TTs"
# ("tests?" because pytest prints the singular for a single item).
COLLECT_TAIL_RE = re.compile(r"(\d[\d,]*)\s+tests?\s+collected\s+in\s+\d")


class CollectError(Exception):
    """Cannot-verify condition for the deep check; exit 2 upstream."""


def parse_collect_tail(stdout: str) -> int | None:
    """The collected total from a `pytest --collect-only -q` stdout tail.

    Takes the LAST match, which is the summary line, not any earlier prose.
    """
    matches = COLLECT_TAIL_RE.findall(stdout)
    return int(matches[-1].replace(",", "")) if matches else None


def parse_collect_files(stdout: str) -> set[str]:
    """The item-bearing file set from a `pytest --collect-only -q` stdout.

    Item lines are node ids ("tests/x.py::test_y"), the only "::" lines with
    a path separator; disk candidates minus this set is the B2-247 gap.
    """
    files: set[str] = set()
    for line in stdout.splitlines():
        s = line.strip()
        if "::" in s and "/" in s:
            files.add(s.split("::", 1)[0])
    return files


def collect_report(root: Path, timeout: int = 600) -> dict:
    """Byte gatherer for the deep check: collected items AND unique files.

    Runs with the interpreter executing this tool (house law: the venv
    python), so an invocation on a pytest-less interpreter fails closed as a
    cannot-verify exit rather than silently skipping the check. Cacheprovider
    stays off so the check writes nothing into the estate. --rootdir is
    pinned to root so node ids stay root-relative even when an ancestor
    carries a pytest.ini (the repo conftest puts tmp_path inside the repo),
    which is what parse_collect_files diffing assumes.
    """
    out = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider",
         "--rootdir", str(root)],
        cwd=root, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=timeout,
    )
    if out.returncode != 0:
        tail = (out.stderr or out.stdout).strip()[-200:]
        raise CollectError(f"pytest --collect-only exited {out.returncode}: {tail}")
    items = parse_collect_tail(out.stdout)
    if items is None:
        raise CollectError("pytest --collect-only output has no parsable 'N tests collected' tail")
    return {"items": items, "files": parse_collect_files(out.stdout)}
