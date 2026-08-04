"""List and read scaffold files under scaffolds/."""

from __future__ import annotations

import sys
from pathlib import Path


def scaffolds_root() -> Path:
    # src/mycelial_republic/scaffolds/catalog.py → project/scaffolds
    here = Path(__file__).resolve()
    # package may be installed editable; prefer project root relative to package
    candidates = [
        here.parents[3] / "scaffolds",  # .../mycelial-republic/scaffolds
        Path.cwd() / "scaffolds",
    ]
    for c in candidates:
        if c.is_dir():
            return c
    return candidates[0]


def list_scaffolds(sub: str = "") -> list[Path]:
    root = scaffolds_root() / sub if sub else scaffolds_root()
    if not root.is_dir():
        return []
    files: list[Path] = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if p.suffix.lower() in {".md", ".txt", ".yml", ".yaml", ".json", ".jsonl", ".py"}:
            # skip huge training dumps in default list unless under training and small
            if p.suffix == ".jsonl" and p.stat().st_size > 100_000:
                continue
            if "chat-" in p.name.lower() and p.stat().st_size > 50_000:
                continue
            files.append(p)
    return files


def read_scaffold(rel: str) -> str:
    path = scaffolds_root() / rel
    if not path.is_file():
        # allow absolute
        path = Path(rel)
    if not path.is_file():
        raise FileNotFoundError(rel)
    return path.read_text(encoding="utf-8", errors="replace")


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(prog="mycelial_republic.scaffolds")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="List scaffold files")
    p_show = sub.add_parser("show", help="Print a scaffold by relative path")
    p_show.add_argument("path")
    p_show.add_argument("--max-chars", type=int, default=0)
    args = ap.parse_args(argv)

    if args.cmd == "list":
        root = scaffolds_root()
        print(f"root: {root}")
        for p in list_scaffolds():
            rel = p.relative_to(root)
            print(f"{p.stat().st_size:8d}  {rel.as_posix()}")
        return 0
    if args.cmd == "show":
        text = read_scaffold(args.path)
        if args.max_chars and len(text) > args.max_chars:
            print(text[: args.max_chars])
            print(f"\n... [{len(text) - args.max_chars} more chars]")
        else:
            print(text)
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
