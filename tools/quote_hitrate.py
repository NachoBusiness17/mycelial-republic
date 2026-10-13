#!/usr/bin/env python3
"""quote_hitrate.py - standing verbatim-quote hit-rate over estate quote fields.

The BITF action line (memory/runs/mickey17_v2/lanes/citation-binding-tools.json,
steal 2, via corpus/steal/MASTER_MICKEY17_V2_20260924.md): sample evidence_quote
strings from judge outputs in watch/inbox, gate each against the cited file, and
publish the hit-rate as a standing number. This is that number.

Sources scanned (JSON + JSONL under the walk roots, default: watch/inbox and
memory/runs), each unit gated with tools/quote_gate.check_quote (raw byte match,
whitespace-normalized fallback, fail-closed):
  1. judge three-axis verdict rows: "evidence_quote" + a resolvable
     "cited_file" / "source_file" / "source_path" sibling
  2. quote-audit result units: "text" quote + repo-relative "dir"/"file" pair
  3. lane rows: "quote" + a "source" naming an existing local file
     (file:// prefix and trailing ":line" / "(annotation)" suffixes stripped)
Quote fields with no resolvable local source are counted as ungated, never
guessed at. Sample is capped (default 50).

Output: one QUOTE-HITRATE summary line plus per-miss lines on stdout, and one
JSON row {ts, sample, hits, misses, miss_paths} appended to
watch/inbox/quote_hitrate.jsonl. Fail-open honest: fewer than MIN_SAMPLE
gateable quotes prints the count and exits 0 with NO-SAMPLE; the record never
receives an invented or empty row. Misses are first-class data: exit 0 either
way, this is a measurement, not a gate.

Usage:
  python tools/quote_hitrate.py [ROOT ...] [--cap N] [--jsonl PATH] [--min-sample N]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from quote_gate import check_quote  # noqa: E402

DEFAULT_ROOTS = [ROOT / "watch" / "inbox", ROOT / "memory" / "runs"]
DEFAULT_JSONL = ROOT / "watch" / "inbox" / "quote_hitrate.jsonl"
DEFAULT_CAP = 50
DEFAULT_MIN_SAMPLE = 5
MAX_FILE_BYTES = 20 * 1024 * 1024

QUOTE_KEYS = ("evidence_quote", "quote", "text")
CITED_KEYS = ("cited_file", "source_file", "source_path")


def iter_json_values(path: Path):
    """Yield every parsed JSON value in a .json/.jsonl file; skip on parse or read failure."""
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    if path.suffix == ".jsonl":
        for line in text.splitlines():
            if not line.strip():
                continue
            try:
                yield json.loads(line)
            except ValueError:
                continue
        return
    try:
        yield json.loads(text)
    except ValueError:
        return


def walk_json(value, path: Path):
    """Yield every dict found anywhere inside one parsed JSON value."""
    if isinstance(value, dict):
        yield path, value
        for child in value.values():
            yield from walk_json(child, path)
    elif isinstance(value, list):
        for child in value:
            yield from walk_json(child, path)


def resolve_source(raw: str, roots: list[Path]) -> Path | None:
    """Resolve a cited-source string to an existing file, else None.

    Strips file:// prefixes, trailing "(annotation)" parentheticals and
    ":12" / ":12-20" / ":12,40" line suffixes; relative candidates are tried
    against each walk root.
    """
    if not raw or not isinstance(raw, str):
        return None
    s = raw.strip()
    if s.lower().startswith("file://"):
        s = s[len("file://"):]
    s = s.split(" (", 1)[0].strip()
    s = re.split(r":\d", s, maxsplit=1)[0]
    if not s:
        return None
    for base in roots:
        cand = Path(s)
        if not cand.is_absolute():
            cand = base / cand
        try:
            if cand.is_file():
                return cand
        except OSError:
            continue
    return None


def cited_path(obj: dict, roots: list[Path]) -> Path | None:
    for key in (*CITED_KEYS, "source"):
        if isinstance(obj.get(key), str):
            found = resolve_source(obj[key], roots)
            if found:
                return found
    if isinstance(obj.get("file"), str):
        pair = obj.get("dir", "")
        rel = f"{pair}/{obj['file']}" if pair else obj["file"]
        return resolve_source(rel, roots + [ROOT])
    return None


def collect_units(roots: list[Path], exclude: Path, cap: int) -> tuple[list[tuple[str, Path, str]], int]:
    """Return (units, ungated): units are (quote, source, label), capped; ungated
    counts quote fields with no resolvable local source."""
    units: list[tuple[str, Path, str]] = []
    ungated = 0
    files: list[Path] = []
    for base in roots:
        for pattern in ("*.json", "*.jsonl"):
            files.extend(base.rglob(pattern))
    for path in sorted(set(files)):
        if path.resolve() == exclude:
            continue
        for _, obj in walk_json_jsonl(path):
            quote = next((obj[k] for k in QUOTE_KEYS if isinstance(obj.get(k), str) and obj[k].strip()), None)
            if quote is None:
                continue
            src = cited_path(obj, roots)
            if src is None:
                ungated += 1
                continue
            label = f"{path.name} :: {obj.get('lane', obj.get('kind', obj.get('verdict_id', '?')))}"
            units.append((quote, src, label))
            if len(units) >= cap:
                return units, ungated
    return units, ungated


def walk_json_jsonl(path: Path):
    for value in iter_json_values(path):
        yield from walk_json(value, path)


def run(roots: list[Path], jsonl_path: Path, cap: int, min_sample: int) -> int:
    units, ungated = collect_units(roots, jsonl_path, cap)
    print(f"QUOTE-HITRATE scan: gateable={len(units)} ungated={ungated} cap={cap} roots={[str(r) for r in roots]}")
    if len(units) < min_sample:
        print(f"NO-SAMPLE verdict: only {len(units)} gateable quote field(s) found, need {min_sample}; no row filed")
        return 0
    hits, misses = 0, []
    for quote, src, label in units:
        try:
            source_bytes = src.read_bytes()
        except OSError:
            found = False
        else:
            found, _mode = check_quote(quote, source_bytes)
        if found:
            hits += 1
        else:
            misses.append({"label": label, "path": str(src)})
    rate = 100.0 * hits / len(units)
    print(f"QUOTE-HITRATE: {hits}/{len(units)} = {rate:.1f}% (misses={len(misses)}, capped={len(units) >= cap})")
    for m in misses:
        print(f"MISS: {m['path']} :: {m['label']}")
    row = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sample": len(units),
        "hits": hits,
        "misses": len(misses),
        "miss_paths": [m["path"] for m in misses],
    }
    try:
        jsonl_path.parent.mkdir(parents=True, exist_ok=True)
        with jsonl_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    except OSError as exc:
        print(f"QUOTE-HITRATE WARN: row not filed: {exc}")
    else:
        print(f"row filed: {jsonl_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Standing verbatim-quote hit-rate over judge/verdict quote fields (fail-open honest)."
    )
    parser.add_argument("roots", nargs="*", type=Path, help="walk roots (default: watch/inbox memory/runs)")
    parser.add_argument("--cap", type=int, default=DEFAULT_CAP, help="max quotes sampled (default 50)")
    parser.add_argument("--jsonl", type=Path, default=DEFAULT_JSONL, help="JSONL record to append the row to")
    parser.add_argument("--min-sample", type=int, default=DEFAULT_MIN_SAMPLE, help="NO-SAMPLE below this (default 5)")
    args = parser.parse_args(argv)
    roots = [r if r.is_absolute() else ROOT / r for r in args.roots] or DEFAULT_ROOTS
    jsonl = args.jsonl if args.jsonl.is_absolute() else ROOT / args.jsonl
    return run(roots, jsonl, args.cap, args.min_sample)


if __name__ == "__main__":
    sys.exit(main())
