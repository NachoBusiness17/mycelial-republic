#!/usr/bin/env python3
# prior_art: tools/precommit_secret_check.py, tools/citation_lint.py -- both gate
#   staged content at commit time, but neither asks whether the file should exist.
"""prior_art_check -- bind prior-art at file creation, not at regret.

From the 2026-10-24 ractor fold: the estate writes laws ("DO NOT re-derive -
execute", 2026-08-27) and then re-derives anyway, because a law is a statement and
nothing sits between a statement and an effect. This is the mechanism.

Rule: a NEW file under tools/ must carry a header line

    prior_art: tools/cockpit.py, tools/lens_packet.py -- <why neither serves>

with at least two paths that exist in the estate. Modified files are not checked;
only additions, because that is the moment the question is live.

    python tools/prior_art_check.py                 # check staged additions
    python tools/prior_art_check.py --warn          # advisory (never blocks)
    python tools/prior_art_check.py --paths a.py b.py
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERN = re.compile(r"^\s*(?:#|//|\"\"\"|''')?\s*prior_art:\s*(.+)$", re.MULTILINE)
MIN_PATHS = 2


def staged_additions(root: Path) -> list[str]:
    try:
        out = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
                             cwd=str(root), capture_output=True, text=True, timeout=60).stdout
    except Exception:  # noqa: BLE001
        return []
    return [p.strip() for p in out.splitlines() if p.strip().startswith("tools/")]


def extract_paths(line: str) -> list[str]:
    head = line.split("--", 1)[0]
    parts = re.split(r"[,\s]+", head.strip())
    return [p.strip().strip("`'\"") for p in parts if "/" in p or p.endswith(".py")]


def check(path: Path, root: Path) -> tuple[bool, str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return False, f"unreadable: {exc}"
    m = PATTERN.search(text)
    if not m:
        return False, "no prior_art: header"
    refs = [p for p in extract_paths(m.group(1)) if (root / p).exists()]
    if len(refs) < MIN_PATHS:
        return False, (f"prior_art names {len(refs)} existing path(s), needs {MIN_PATHS}: "
                       f"{m.group(1)[:80]}")
    return True, f"{len(refs)} paths: {', '.join(refs[:3])}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--warn", action="store_true")
    ap.add_argument("--paths", nargs="*", default=None)
    ap.add_argument("--root", default=None)
    args = ap.parse_args(argv)
    root = Path(args.root).resolve() if args.root else ROOT
    paths = args.paths if args.paths is not None else staged_additions(root)
    if not paths:
        print("prior_art_check: no new tools/ files staged")
        return 0
    bad = []
    for rel in paths:
        ok, detail = check(root / rel, root)
        if not ok:
            bad.append((rel, detail))
    if not bad:
        print(f"prior_art_check: PASS - {len(paths)} new file(s) declare prior art")
        return 0
    for rel, detail in bad:
        print(f"prior_art_check: {'WARN' if args.warn else 'REFUSED'} - {rel}: {detail}")
    print("  add a header line:  # prior_art: tools/x.py, tools/y.py -- why neither serves")
    return 0 if args.warn else 1


if __name__ == "__main__":
    sys.exit(main())
