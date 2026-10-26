"""zoo_census.py - census the dashboard/static zoo (one row per page, regenerable).

Extracts per page: title, first self-description (comment or hud/h1 line), bytes,
git birth date, git last-touch date. Writes dashboard/static/zoo_census.jsonl and
prints a compact table. The ancestry map (watch/inbox/ZOO_ANCESTRY_MAP_*.md) is
hand-authored but byte-grounded in this census; rerun before editing the map.

Usage: .venv/Scripts/python.exe tools/zoo_census.py [--root dashboard/static]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TAG_RE = re.compile(r"<[^>]+>")
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
COMMENT_RE = re.compile(r"<!--(.*?)-->", re.S)
HUD_RE = re.compile(r'id="hud"[^>]*>(.*?)</div>', re.S | re.I)
HEAD_RE = re.compile(r"<h[123][^>]*>(.*?)</h[123]>", re.S | re.I)


def _clean(text: str) -> str:
    text = TAG_RE.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


def describe(text: str) -> str:
    for pattern in (COMMENT_RE, HUD_RE, HEAD_RE):
        match = pattern.search(text)
        if match:
            desc = _clean(match.group(1))
            if len(desc) >= 12:
                return desc[:220]
    return ""


def git_dates(path: Path, root: Path) -> tuple[str, str]:
    rel = path.relative_to(root.parent).as_posix()
    try:
        birth = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%as", "--", rel],
            cwd=root.parent, capture_output=True, text=True, timeout=20,
        ).stdout.strip().splitlines()
        last = subprocess.run(
            ["git", "log", "-1", "--format=%as", "--", rel],
            cwd=root.parent, capture_output=True, text=True, timeout=20,
        ).stdout.strip()
        return (birth[-1] if birth else "untracked", last or "untracked")
    except Exception as exc:  # git missing or repo oddity: census must not die
        return (f"error:{exc.__class__.__name__}", "error")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="dashboard/static")
    args = parser.parse_args()
    root = Path(args.root)
    if not root.is_dir():
        print(f"no such root: {root}")
        return 2

    rows = []
    for path in sorted(root.glob("*.html")):
        text = path.read_text(encoding="utf-8", errors="replace")
        title_match = TITLE_RE.search(text)
        birth, last = git_dates(path, root)
        rows.append(
            {
                "file": path.name,
                "title": _clean(title_match.group(1))[:120] if title_match else "",
                "desc": describe(text),
                "bytes": path.stat().st_size,
                "mtime": datetime.fromtimestamp(
                    path.stat().st_mtime, tz=timezone.utc
                ).strftime("%Y-%m-%d"),
                "birth": birth,
                "last_touch": last,
            }
        )

    out = root / "zoo_census.jsonl"
    with out.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True) + "\n")

    print(f"census: {len(rows)} pages -> {out}")
    for row in rows:
        t = row["title"] or "(no title)"
        d = row["desc"]
        print(f"{row['file']} | {row['bytes']:>7}b | born {row['birth']} | {t} | {d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
