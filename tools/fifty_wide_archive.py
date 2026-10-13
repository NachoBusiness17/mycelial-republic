#!/usr/bin/env python3
"""fifty_wide_archive.py - post-wave per-agent archive (a07 operator-owed item).

The disease (watch/inbox/burn_claims_50wide_20261003.md, D1 in
corpus/steal/MASTER_MICKEY17_V2.md section 7): the 2026-10-03 fifty-wide burn
wave lost 10 units and no per-agent artifact existed on disk to explain the
drop, because Task-agent outputs live only in session transcripts. The
fifty_wide_guard receipt filed per-agent retention as operator-owed
(watch/inbox/go_wave_20261004/fifty_wide_guard.md section 7); this tool makes
it mechanical: the coordinator runs it ONCE POST-WAVE and the bytes land.

Bar stated in numbers BEFORE reading anything:

  one archive run per wave writes every agent report to
  memory/runs/fifty_wide/<wave>/agents/<lane>.md and appends one manifest row
  {wave, lane, file, sha256, ts} per report; re-archiving bytes whose sha256
  already matches the lane's last manifest row is a full no-op (no rewrite,
  no row). Changed bytes for a lane rewrite the file and append a fresh row,
  so the manifest is an append-only history of what was believed when. The
  replay pair is the guard's dispatch_log.jsonl row (pre-flight) plus this
  agents dir (post-wave); either half alone cannot explain a count gap.

Fail-loud by construction: empty input, a lane with an empty report body,
duplicate lane labels, or content outside any labeled block is exit 1; a
missing or unreadable input file, or an unparseable existing manifest row, is
exit 2 (cannot verify), never a silent pass. The manifest is trusted for
idempotency only when every row parses; otherwise nothing is written.

Input formats (auto-detected; --format forces):
  - labeled blocks: a block starts at a line '=== <lane> ===' and runs to the
    next header; the trimmed body is that lane's report.
  - JSONL: one {"lane": ..., "report": ...} object per non-blank line.

Usage:
  .venv/Scripts/python.exe tools/fifty_wide_archive.py --wave <slug> \
      [--input <file, or stdin when omitted or ->] \
      [--format auto|blocks|jsonl] [--dir memory/runs/fifty_wide]

Prints 'ARCHIVED n/lane-count' on success (n = newly written; the rest are
unchanged sha matches, listed on the following lines).

Exit codes: 0 = archived (or every lane unchanged); 1 = FAIL (empty input,
bad labels, duplicate lanes, empty body); 2 = cannot verify (missing or
unreadable input, corrupt manifest, failed write).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIR = ESTATE_ROOT / "memory" / "runs" / "fifty_wide"

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_CANNOT_VERIFY = 2

_LANE_HEADER = re.compile(r"^\s*===\s*(.+?)\s*===\s*$")
_UNSAFE = re.compile(r"[^A-Za-z0-9._-]+")


def _moment() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sanitize_name(raw: str, what: str) -> str:
    """Reduce a wave slug or lane label to a safe single path component."""
    clean = _UNSAFE.sub("_", raw.strip()).strip("._")[:80]
    if not clean:
        raise ValueError(f"{what} {raw!r} sanitizes to an empty path component")
    return clean


def parse_blocks(text: str) -> list[tuple[str, str]]:
    """Split labeled text into (lane, report) pairs.

    A block starts at a '=== <lane> ===' header line; content before the first
    header and any empty body is a ValueError (an unattributable report is a
    failure, not a guess).
    """
    reports: list[tuple[str, str]] = []
    lane: str | None = None
    body: list[str] = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        m = _LANE_HEADER.match(raw)
        if m:
            if lane is not None:
                reports.append((lane, "\n".join(body).strip()))
            lane, body = m.group(1), []
        elif lane is not None:
            body.append(raw)
        elif raw.strip():
            raise ValueError(
                f"line {lineno} holds content before any '=== lane ===' header: "
                f"{raw.strip()[:80]!r}"
            )
    if lane is not None:
        reports.append((lane, "\n".join(body).strip()))
    for i, (ln, rep) in enumerate(reports, 1):
        if not rep:
            raise ValueError(f"lane {ln!r} (block {i}) has an empty report body")
    return reports


def parse_jsonl(text: str) -> list[tuple[str, str]]:
    """Parse one {"lane": ..., "report": ...} object per non-blank line."""
    reports: list[tuple[str, str]] = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except ValueError as e:
            raise ValueError(f"line {lineno} is not valid JSON: {type(e).__name__}: {e}")
        if not (isinstance(row, dict) and "lane" in row and "report" in row):
            raise ValueError(f'line {lineno} is not a {{"lane": ..., "report": ...}} object')
        reports.append((str(row["lane"]), str(row["report"])))
    for ln, rep in reports:
        if not rep.strip():
            raise ValueError(f"lane {ln!r} has an empty report body")
    return reports


def parse_reports(text: str, fmt: str) -> list[tuple[str, str]]:
    """Dispatch on --format; 'auto' picks JSONL when the first line is an object."""
    if fmt == "jsonl":
        return parse_jsonl(text)
    if fmt == "blocks":
        return parse_blocks(text)
    first = next((l for l in text.splitlines() if l.strip()), "")
    return parse_jsonl(text) if first.lstrip().startswith("{") else parse_blocks(text)


def load_lane_shas(manifest: Path) -> dict[str, str]:
    """Last banked sha256 per lane from the wave manifest.

    A missing manifest is a first run (empty dict); any unparseable or
    malformed row is a ValueError, surfaced as exit 2 so idempotency is never
    decided against a manifest we cannot read.
    """
    shas: dict[str, str] = {}
    if not manifest.is_file():
        return shas
    for lineno, raw in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except ValueError as e:
            raise ValueError(f"manifest line {lineno} is unparseable: {type(e).__name__}: {e}")
        if not (isinstance(row, dict) and "lane" in row and "sha256" in row):
            raise ValueError(f"manifest line {lineno} is not a lane/sha256 row")
        shas[str(row["lane"])] = str(row["sha256"])
    return shas


def archive(
    wave: str, reports: list[tuple[str, str]], base_dir: Path
) -> tuple[int, list[str], Path]:
    """Write changed reports, bank manifest rows. Returns (written, unchanged, wave_dir).

    Idempotency law: a lane whose report sha256 equals its last manifest row
    is skipped byte-for-byte (no rewrite, no row); changed bytes rewrite the
    file and append a fresh row.
    """
    wave_dir = base_dir / wave
    agents_dir = wave_dir / "agents"
    manifest = wave_dir / "manifest.jsonl"
    existing = load_lane_shas(manifest)
    written = 0
    unchanged: list[str] = []
    rows: list[dict] = []
    moment = _moment()
    for lane, report in reports:
        sha = hashlib.sha256(report.encode("utf-8")).hexdigest()
        if existing.get(lane) == sha:
            unchanged.append(lane)
            continue
        path = agents_dir / f"{lane}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(report.encode("utf-8"))
        try:
            rel = str(path.relative_to(ESTATE_ROOT)).replace("\\", "/")
        except ValueError:
            rel = str(path)
        rows.append({"wave": wave, "lane": lane, "file": rel, "sha256": sha, "ts": moment})
        written += 1
    if rows:
        manifest.parent.mkdir(parents=True, exist_ok=True)
        with manifest.open("a", encoding="utf-8", newline="\n") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return written, unchanged, wave_dir


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="fifty-wide post-wave per-agent archive")
    parser.add_argument("--wave", required=True,
                        help="wave slug; agents land under <dir>/<wave>/agents/")
    parser.add_argument("--input", default=None,
                        help="reports file (labeled blocks or JSONL); omitted or '-' reads stdin")
    parser.add_argument("--format", choices=("auto", "blocks", "jsonl"), default="auto",
                        help="input shape; auto detects JSONL vs labeled blocks")
    parser.add_argument("--dir", default=str(DEFAULT_DIR),
                        help=f"wave base dir (default {DEFAULT_DIR})")
    args = parser.parse_args(argv)

    try:
        wave = sanitize_name(args.wave, "wave slug")
    except ValueError as e:
        print(f"FIFTY-WIDE ARCHIVE: FAIL: {e}")
        return EXIT_FAIL

    if args.input in (None, "-"):
        text = sys.stdin.read()
        src = "<stdin>"
    else:
        path = Path(args.input)
        if not path.is_file():
            print(f"FIFTY-WIDE ARCHIVE: CANNOT-VERIFY: input file not found: {path}")
            return EXIT_CANNOT_VERIFY
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, ValueError) as e:
            print(f"FIFTY-WIDE ARCHIVE: CANNOT-VERIFY: input unreadable: {path}: {e}")
            return EXIT_CANNOT_VERIFY
        src = str(path)

    if not text.strip():
        print(f"FIFTY-WIDE ARCHIVE: FAIL: empty input ({src}): no agent reports found")
        return EXIT_FAIL

    try:
        reports = parse_reports(text, args.format)
    except ValueError as e:
        print(f"FIFTY-WIDE ARCHIVE: FAIL: {src}: {e}")
        return EXIT_FAIL

    raw_lanes = [ln for ln, _ in reports]
    dupes = sorted({ln for ln in raw_lanes if raw_lanes.count(ln) > 1})
    if dupes:
        print(f"FIFTY-WIDE ARCHIVE: FAIL: duplicate lane labels (merge into one block): {dupes}")
        return EXIT_FAIL

    try:
        renamed = [(sanitize_name(ln, "lane"), rep, ln) for ln, rep in reports]
    except ValueError as e:
        print(f"FIFTY-WIDE ARCHIVE: FAIL: {e}")
        return EXIT_FAIL
    seen: dict[str, str] = {}
    for clean, _rep, raw in renamed:
        prev = seen.get(clean)
        if prev is not None:
            print(f"FIFTY-WIDE ARCHIVE: FAIL: lanes {prev!r} and {raw!r} both sanitize to {clean!r}")
            return EXIT_FAIL
        seen[clean] = raw
    reports = [(clean, rep) for clean, rep, _raw in renamed]

    try:
        written, unchanged, _wave_dir = archive(wave, reports, Path(args.dir))
    except ValueError as e:
        print(f"FIFTY-WIDE ARCHIVE: CANNOT-VERIFY: {e}")
        return EXIT_CANNOT_VERIFY
    except OSError as e:
        print(f"FIFTY-WIDE ARCHIVE: CANNOT-VERIFY: archive write failed: {type(e).__name__}: {e}")
        return EXIT_CANNOT_VERIFY

    print(f"ARCHIVED {written}/{len(reports)}")
    for lane in unchanged:
        print(f"  unchanged (sha match): {lane}")
    return EXIT_PASS


if __name__ == "__main__":
    sys.exit(run())
