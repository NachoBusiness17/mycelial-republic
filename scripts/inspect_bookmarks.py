"""Inspect browser Bookmarks JSON for high-signal folders/URLs."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def walk(node: dict, path: str = "", out: list | None = None) -> list:
    if out is None:
        out = []
    name = node.get("name", "")
    t = node.get("type")
    p = f"{path}/{name}" if path else name
    if t == "url":
        out.append(
            {
                "name": name,
                "url": node.get("url", ""),
                "path": path,
                "date_added": node.get("date_added"),
            }
        )
    for c in node.get("children") or []:
        walk(c, p, out)
    return out


def main() -> None:
    sources = {
        "chrome": Path.home()
        / "AppData/Local/Google/Chrome/User Data/Default/Bookmarks",
        "edge": Path.home()
        / "AppData/Local/Microsoft/Edge/User Data/Default/Bookmarks",
    }
    keys = (
        "x.com",
        "twitter.com",
        "threadreader",
        "nacho",
        "zenodo",
        "github.com",
        "academia",
        "slashreboot",
        "arxiv",
    )
    for label, path in sources.items():
        if not path.is_file():
            print(label, "missing")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        all_b: list = []
        for k, v in (data.get("roots") or {}).items():
            if isinstance(v, dict):
                walk(v, k, all_b)
        print(f"=== {label}: {len(all_b)} bookmarks ===")
        folders = Counter(b["path"] for b in all_b)
        for f, n in folders.most_common(40):
            print(f"  [{n:3d}] {f}")
        hit = [
            b
            for b in all_b
            if any(x in (b["url"] or "").lower() for x in keys)
            or any(x in (b["name"] or "").lower() for x in keys)
        ]
        print(f"  high-signal-ish urls: {len(hit)}")
        for b in hit[:60]:
            print(
                f"    {b['path'][:60]} | {b['name'][:50]} | {(b['url'] or '')[:100]}"
            )


if __name__ == "__main__":
    main()
