#!/usr/bin/env python3
r"""estate_cleanup.py — known-junk enumerator and guarded cleaner.

The estate has junk that has been flagged repeatedly but never cleaned.
Provenance (the triage lane's receipts):
  - root-level `nul` (Windows reserved name; path-resolution hazard called out
    by watch/inbox/SECRET_GATE_BUILD_20260927.md and audit_20260926/LANE4B)
  - `UsersfosteAppData*` root files (path-bug dumps: tools wrote to a literal
    "C:UsersfosteAppData..." string instead of %TEMP%)
  - `_s218_*` root files (rogue endpoint build debris — "unaccounted build
    debris — scan before they merge", work/lib-belady-1966_hermes.md)
  - `braid_test.out`, `sweep_llama*.json`, `stealth-tools.check.txt`
    (one-shot scratch outputs, superseded by their receipts)
  - `tmp_gopher/` (2.8MB vendored llama.cpp/amdgpu dig staging, classified
    "scratch or vendored ... none is estate debt" by flash50/todo-census.md)

Contract: DEFAULT IS DRY-RUN. `--apply` is the only path that deletes, and it
deletes exactly the enumerated set, then re-enumerates and exits 1 if anything
survived (fail-loud: no silent partial success). The reserved-name `nul` file
cannot be removed by os.remove (Win32 resolves `dir\nul` to the NUL device),
so it is deleted via the device-path syntax `cmd /c del \\.\C:\path\nul`.

Existence checks for `nul` go through scandir, never os.path.exists: on
Windows `C:\dir\nul` resolves to the NUL device even after the literal file is
gone, so os.path.exists is always True there and would mask both the file and
its removal (root cause of the SECRET_GATE false positives).

Usage:
  python tools/estate_cleanup.py                 # dry-run report (default)
  python tools/estate_cleanup.py --apply         # actually delete
  python tools/estate_cleanup.py --root <dir>    # scan another tree
  python tools/estate_cleanup.py --json          # machine-readable report
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Win32 DOS reserved device names (bare, no extension) that can shadow real
# files: a directory entry literally named one of these needs device-path I/O.
RESERVED_NAMES = frozenset(
    {"con", "prn", "aux", "nul", "com1", "com2", "com3", "com4", "lpt1", "lpt2", "lpt3"}
)


@dataclass
class JunkSpec:
    """One known-junk category: what matches at repo ROOT and why it is junk."""

    category: str  # stable key used by tests and receipts
    pattern: str   # fnmatch pattern over root-level entry names
    kind: str      # "file" | "dir" | "any"
    why: str       # provenance, for the report


# The junk list from the triage lane's receipts (see module docstring).
JUNK_SPECS: tuple[JunkSpec, ...] = (
    JunkSpec(
        category="nul-reserved",
        pattern="nul",
        kind="any",
        why="Windows reserved-name file at root; breaks naive path handling "
        "(SECRET_GATE_BUILD_20260927, audit_20260926/LANE4B)",
    ),
    JunkSpec(
        category="path-bug-dumps",
        pattern="UsersfosteAppData*",
        kind="any",
        why="path-bug dumps: literal 'C:UsersfosteAppData...' temp-path writes",
    ),
    JunkSpec(
        category="s218-build-debris",
        pattern="_s218_*",
        kind="any",
        why="rogue endpoint-map build debris, superseded by the banked s2-18 receipt",
    ),
    JunkSpec(
        category="braid-scratch",
        pattern="braid_test.out",
        kind="any",
        why="one-shot test output, superseded by its receipt",
    ),
    JunkSpec(
        category="sweep-llama-scratch",
        pattern="sweep_llama*.json",
        kind="any",
        why="one-shot sweep outputs, superseded by their receipts",
    ),
    JunkSpec(
        category="tmp-gopher-dig",
        pattern="tmp_gopher",
        kind="dir",
        why="vendored llama.cpp/amdgpu dig staging, classified scratch by todo-census",
    ),
    JunkSpec(
        category="stealth-check-scratch",
        pattern="stealth-tools.check.txt",
        kind="any",
        why="one-shot gate check output, superseded by its receipt",
    ),
)


@dataclass
class JunkItem:
    """One enumerable junk path under root, with its byte cost."""

    category: str
    path: str        # relative to root, posix separators
    kind: str        # "file" | "dir"
    bytes: int       # st_size sum (recursive for dirs)
    file_count: int  # number of files inside (1 for plain files)
    delete_action: str  # "plain" | "win32_reserved"
    why: str


def _is_reserved(name: str) -> bool:
    stem = name.split(".")[0].lower()
    return os.name == "nt" and stem in RESERVED_NAMES


def entry_exists(root: Path, name: str) -> bool:
    """Directory-entry truth. For reserved names (e.g. `nul`) os.path.exists
    resolves to the DOS device and lies; scandir reads the real directory."""
    try:
        with os.scandir(root) as it:
            return any(e.name == name for e in it)
    except OSError:
        return False


def _tree_cost(path: Path) -> tuple[int, int]:
    """(bytes, file_count) for a directory tree, no symlink following."""
    total = 0
    files = 0
    for dirpath, _dirnames, filenames in os.walk(path, followlinks=False):
        for fname in filenames:
            fpath = Path(dirpath) / fname
            try:
                total += fpath.stat().st_size
                files += 1
            except OSError:
                # Unreadable member still counts as a file at 0 reclaimable
                # bytes; --apply's re-enumeration will surface it as a survivor.
                files += 1
    return total, files


def enumerate_junk(root: Path) -> list[JunkItem]:
    """Enumerate every root-level match of every JUNK_SPECS entry.

    Single scandir pass (directory-entry truth, required for the reserved
    `nul` file); globs match entry names with fnmatch.
    """
    with os.scandir(root) as it:
        entries = [(e.name, e) for e in it]
    found: list[JunkItem] = []
    for spec in JUNK_SPECS:
        for name, entry in entries:
            if not fnmatch.fnmatchcase(name, spec.pattern):
                continue
            is_dir = entry.is_dir(follow_symlinks=False)
            if spec.kind == "dir" and not is_dir:
                continue
            if spec.kind == "file" and is_dir:
                continue
            if is_dir:
                nbytes, files = _tree_cost(Path(entry.path))
                kind = "dir"
            else:
                st = entry.stat(follow_symlinks=False)
                nbytes, files, kind = st.st_size, 1, "file"
            found.append(
                JunkItem(
                    category=spec.category,
                    path=name,
                    kind=kind,
                    bytes=nbytes,
                    file_count=files,
                    delete_action="win32_reserved" if _is_reserved(name) else "plain",
                    why=spec.why,
                )
            )
    found.sort(key=lambda j: (j.category, j.path))
    return found


def _delete_reserved(root: Path, name: str) -> None:
    """Delete a literal reserved-name file with `del \\\\.\\<drive>:\\path\\nul`.

    os.remove on `root/nul` opens the NUL device (or fails); the Win32 device
    path `\\\\.\\C:\\...` bypasses DOS-name resolution and addresses the file.
    Absolute backslash path is required by the device syntax.
    """
    device_path = "\\\\.\\" + str((root / name).resolve()).replace("/", "\\")
    result = subprocess.run(
        ["cmd", "/c", "del", "/f", "/a", device_path],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or entry_exists(root, name):
        raise OSError(
            f"reserved-name delete failed (rc={result.returncode}): "
            f"{device_path} stderr={result.stderr.strip()!r}"
        )


def apply_removals(root: Path, items: list[JunkItem]) -> list[str]:
    """Delete exactly the given items. Returns the relative paths removed."""
    removed: list[str] = []
    for item in items:
        target = root / item.path
        if item.delete_action == "win32_reserved":
            _delete_reserved(root, item.path)  # verifies via scandir itself
        elif item.kind == "dir":
            shutil.rmtree(target)  # raises on partial removal
        else:
            target.unlink()  # raises if it cannot remove
        removed.append(item.path)
    return removed


def _fmt_bytes(n: int) -> str:
    mb = n / (1024 * 1024)
    return f"{n:,} B ({mb:.2f} MiB)" if mb >= 1 else f"{n:,} B"


def build_report(root: Path, items: list[JunkItem], applied: bool) -> str:
    lines = [
        "estate_cleanup — known-junk report",
        f"root: {root}",
        f"mode: {'APPLIED (files deleted)' if applied else 'DRY-RUN (nothing touched)'}",
        "",
        f"{'category':<24} {'kind':<5} {'bytes':>12} {'files':>6}  path",
        "-" * 100,
    ]
    for item in items:
        lines.append(
            f"{item.category:<24} {item.kind:<5} {item.bytes:>12,} {item.file_count:>6}  {item.path}"
        )
    total = sum(i.bytes for i in items)
    files = sum(i.file_count for i in items)
    lines.append("-" * 100)
    lines.append(f"TOTAL RECLAIMABLE: {_fmt_bytes(total)} across {files} files, {len(items)} paths")
    if not applied:
        lines.append("dry-run: rerun with --apply to delete the set above")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=str(REPO_ROOT), help="tree to scan (default: repo root)")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="actually delete the enumerated junk (default is dry-run report only)",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON instead of the text report")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"error: root is not a directory: {root}", file=sys.stderr)
        return 2

    items = enumerate_junk(root)
    removed: list[str] = []
    if args.apply:
        removed = apply_removals(root, items)

    if args.json:
        payload = {
            "root": str(root),
            "applied": args.apply,
            "total_bytes": sum(i.bytes for i in items),
            "total_files": sum(i.file_count for i in items),
            "items": [asdict(i) for i in items],
            "removed": removed,
        }
        print(json.dumps(payload, indent=2))
    else:
        print(build_report(root, items, applied=args.apply))

    if args.apply:
        # Fail-loud post-check: everything enumerated must be gone.
        survivors = [i.path for i in enumerate_junk(root)]
        if survivors:
            print(f"error: junk survived --apply: {survivors}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
