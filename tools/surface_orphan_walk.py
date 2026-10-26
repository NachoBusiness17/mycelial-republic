"""Surface orphan walk: full-depth orphan check for the shared inbox.

G1 lane i07-orphan-walk (parent gene G0 g04-contract-widening, 2026-10-18;
design watch/inbox/ORG_SYSTEM_V2_20261018.md Organ 4). Read-only: it walks
watch/inbox to its full depth, joins every disk file against the INDEX.json
active-items set by REPO-RELATIVE PATH, and reports the orphans (files on
disk no INDEX item claims). It writes nothing.

Defect being fixed (mag/shared_surface.py:275-280): the inline orphan check
scans INBOX.iterdir() top level only and builds the indexed set from
Path(item.path).name BASENAMES, so (a) every subdir file is invisible to it
(22,371 of 23,990 surface files at the 2026-10-18 census) and (b) a
top-level file is false-cleared as "indexed" whenever some subdir item
happens to share its basename. This tool kills basename matching entirely:
relative path is the identity. INDEX item paths are normalized through the
SAME prefix-strip ladder used at mag/shared_surface.py:298-303
("/board/inbox/", "/app/inbox/", "inbox/", first match only, backslashes
folded to forward slashes first).

Output contract (B2-338 first-line law, receipt
watch/inbox/burn_wave_20260926/B2_338_case_fix_20260926.md): a completed run
opens stdout with exactly::

    surface_orphan_walk: ok (<n> orphans)

Orphans are WARNING-class (the unindexed backlog is ~19k files; hard-failing
every run would train operators to dismiss the channel, the exact disease
B2-338 cured), so the walk exits 0 with counts even when orphans exist.
Malformed input is the only failure: exit 2, first line
"surface_orphan_walk: malformed input - <reason>". Malformed means the INDEX
file is missing/unreadable/not-JSON/not-an-object/items-not-a-list/an item
that is not an object or carries no usable path, or the inbox directory
itself is missing.

--json prints one pure JSON document (machine consumers parse stdout
directly; the B2-338 headline rides inside as "headline"). Text mode
carries the headline as the literal first line. --limit bounds the sample
of orphan paths LISTED (the count always reports the full total) so the
backlog can be sampled without dumping ~19k lines.

Exit codes: 0 walk completed (orphan warnings reported inline); 2 malformed
input. This tool never writes: the backfill/register sweep that cures the
orphans it names is the fold's own add-verb work (g04 sequencing step 2-3),
a separate operator-gated verb.

Consumer Law (genome risk gate 4): consumer is the surface patrol family -
this verb is the WARN-first rollout phase; wiring it into mag.shared_surface
inspect_surface and flipping WARN to ERROR is the operator call named in
g04 step 5. Verifier is tests/test_surface_orphan_walk.py plus the live-run
receipt banked in memory/runs/genetic_burn/20261018/G1/lanes/i07-orphan-walk.md.
Falsifier (ORG_SYSTEM_V2 F4 family): if a month after landing a file can
still appear in a watch/inbox subdir and never show up in any patrol
output, the walk is a cow and this receipt is the lesson.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Mirror of mag/shared_surface.py:128. These sit at the inbox top level by
# design (discovery pointers, not payload) and are never orphans.
CONTROL_FILES = frozenset({"INDEX.json", "INDEX.md", "SHARED_SURFACE_CONTRACT.json"})

SCHEMA = "surface_orphan_walk.v1"
DEFAULT_LIMIT = 50


class MalformedInput(Exception):
    """Structural break in the walk's inputs; exit 2 per the output contract."""


def strip_inbox_prefix(raw: str) -> str:
    """Normalize an INDEX item path to an inbox-relative path.

    Same ladder as mag/shared_surface.py:298-303: fold backslashes to
    forward slashes, then strip the first matching accepted prefix. No
    basename fallback: the relative path IS the identity.
    """
    raw = raw.replace("\\", "/")
    for pref in ("/board/inbox/", "/app/inbox/", "inbox/"):
        if raw.startswith(pref):
            return raw[len(pref):]
    return raw


def load_indexed_paths(index_path: Path) -> set[str]:
    """Load INDEX.json and return the indexed inbox-relative path set.

    Raises MalformedInput on any structural break (see module docstring).
    """
    try:
        text = index_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise MalformedInput(f"INDEX missing: {index_path}") from None
    except OSError as exc:
        raise MalformedInput(f"INDEX unreadable: {exc}") from None
    except UnicodeDecodeError as exc:
        raise MalformedInput(f"INDEX not valid UTF-8: {exc}") from None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise MalformedInput(f"INDEX not valid JSON: {exc}") from None
    if not isinstance(payload, dict):
        raise MalformedInput("INDEX root is not a JSON object")
    items = payload.get("items")
    if not isinstance(items, list):
        raise MalformedInput("INDEX 'items' is not a list")
    indexed: set[str] = set()
    for pos, item in enumerate(items):
        if not isinstance(item, dict):
            raise MalformedInput(f"INDEX items[{pos}] is not an object")
        path = item.get("path")
        if not isinstance(path, str) or not path.strip():
            raise MalformedInput(f"INDEX items[{pos}] has no usable 'path'")
        indexed.add(strip_inbox_prefix(path))
    return indexed


def walk_inbox_files(inbox_path: Path) -> list[str]:
    """Return every file under the inbox as a sorted forward-slash rel path.

    Full depth (rglob), unlike mag/shared_surface.py:277 which stops at the
    top level. Raises MalformedInput when the inbox directory is missing.
    """
    if not inbox_path.is_dir():
        raise MalformedInput(f"inbox directory missing: {inbox_path}")
    return sorted(
        p.relative_to(inbox_path).as_posix()
        for p in inbox_path.rglob("*")
        if p.is_file()
    )


def find_orphans(inbox_path: Path, index_path: Path) -> dict:
    """Run the walk and return the full report dict (no rendering).

    Input order check: the inbox first (it is the primary surface), then
    the INDEX, so a missing surface is never masked by an index error.
    """
    disk = walk_inbox_files(inbox_path)
    indexed = load_indexed_paths(index_path)
    disk_set = set(disk)
    control_skipped = sorted(disk_set & CONTROL_FILES)
    scanned = disk_set - CONTROL_FILES
    orphans = sorted(scanned - indexed)
    return {
        "schema": SCHEMA,
        "inbox": inbox_path.as_posix(),
        "index": index_path.as_posix(),
        "disk_files": len(disk),
        "indexed_items": len(indexed),
        "control_files_skipped": control_skipped,
        "orphans_total": len(orphans),
        "orphans": orphans,
    }


def render_text(report: dict, limit: int) -> str:
    """Human output; first line is the B2-338 headline."""
    total = report["orphans_total"]
    lines = [f"surface_orphan_walk: ok ({total} orphans)"]
    lines.append(
        f"  scanned: {report['disk_files']} disk files, "
        f"{report['indexed_items']} indexed items, "
        f"{len(report['control_files_skipped'])} control files skipped"
    )
    if total:
        orphans = report["orphans"]
        lines.append(f"  orphan sample ({min(limit, total)} of {total}, sorted):")
        lines.extend(f"    {path}" for path in orphans[:limit])
        if total > limit:
            lines.append(f"    ... and {total - limit} more (raise --limit for more)")
    return "\n".join(lines)


def render_json(report: dict, limit: int) -> str:
    """One pure JSON document; bounded payload (sample, never the full list)."""
    doc = {
        "schema": report["schema"],
        "ok": True,
        "headline": f"surface_orphan_walk: ok ({report['orphans_total']} orphans)",
        "inbox": report["inbox"],
        "index": report["index"],
        "disk_files": report["disk_files"],
        "indexed_items": report["indexed_items"],
        "control_files_skipped": report["control_files_skipped"],
        "orphans_total": report["orphans_total"],
        "limit": limit,
        "orphans_sample": report["orphans"][:limit],
    }
    return json.dumps(doc, indent=2, sort_keys=True)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="surface_orphan_walk",
        description="Full-depth orphan walk of the shared inbox (read-only).",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="emit one pure JSON document instead of text lines",
    )
    parser.add_argument(
        "--limit", type=int, default=DEFAULT_LIMIT,
        help=f"max orphan paths listed in the sample (default {DEFAULT_LIMIT})",
    )
    parser.add_argument(
        "--inbox", type=Path, default=ROOT / "watch" / "inbox",
        help="inbox directory override (default <repo>/watch/inbox)",
    )
    parser.add_argument(
        "--index", type=Path, default=None,
        help="INDEX.json override (default <inbox>/INDEX.json)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry; returns the process exit code (0 ok/warnings, 2 malformed)."""
    args = build_arg_parser().parse_args(argv)
    if args.limit < 0:
        print("surface_orphan_walk: malformed input - --limit must be >= 0")
        return 2
    index_path = args.index if args.index is not None else args.inbox / "INDEX.json"
    try:
        report = find_orphans(args.inbox, index_path)
    except MalformedInput as exc:
        reason = str(exc)
        if args.json:
            print(json.dumps({
                "schema": SCHEMA,
                "ok": False,
                "headline": "surface_orphan_walk: malformed input",
                "error": reason,
            }, indent=2, sort_keys=True))
        else:
            print(f"surface_orphan_walk: malformed input - {reason}")
        return 2
    if args.json:
        print(render_json(report, args.limit))
    else:
        print(render_text(report, args.limit))
    return 0


if __name__ == "__main__":
    sys.exit(main())
