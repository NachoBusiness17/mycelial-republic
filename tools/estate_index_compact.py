#!/usr/bin/env python3
"""Estate-index compaction check: measure what the .mimosa hook-state skip retires.

Curiosity register row 1, unit 1 (corpus/steal/MASTER_READ_ESTATE.md section 9,
landed 2026-10-05; carries r04#0's measured projection table, r04#1's skip-list
arithmetic, and D1's folded-in hardlink re-verify).

  --check (default): stream the index READ-ONLY, one line at a time, one pass,
      and print the measured profile:
        total rows, ext ".source" count, per-root counts (named root
        local_sovereign_agent\\.mimosa\\hook-state\\, the '_mimosa' sibling
        lane, other nested hook-state copies), and the retire percent if the
        named root were excluded (register truth 86.01%), if the two roots
        were excluded (89.29%), and if all hook-state subtrees were excluded
        (89.34%; 89.3378% exact, never 89.4%). Live refinement banked by this
        tool's first run (2026-10-05): hook-state subtrees also hold 4,072
        non-.source rows (named root +3,577, lane +120, other +375), so
        retiring every hook-state row retires 9,528,610 rows, 89.376%.
      Also prints the retention projection (what remains after the hook-state
      rows are retired) and a hardlink re-verify of both copies (os.stat
      st_ino/st_nlink plus best-effort "fsutil hardlink list") per D1, so
      dedup arithmetic never trusts a morning's link state.
  --apply: NOT landed in unit 1. The destructive rewrite of the 4.15 GB
      artifact is its own sitting (unit discipline; lane order 2026-10-05:
      never --apply, never delete history). Running it prints the register
      pointer and exits 3 without touching any file. Never deletes history.

Register truth the profile is compared against (r04 tier-2 census 2026-10-04,
MASTER_READ_ESTATE.md TS-07 + section 10 line "Skip-list arithmetic"):
10,661,260 rows; .source 9,524,538; 4,150,418,528 bytes; named-root .source
9,168,740 (96.27% of .source); '_mimosa' lane .source 350,503 (3.68%); other
nested .source 5,295 (0.06%); single-root retire 86.01%; named root + _mimosa
89.29%; all hook-state subtrees 89.34%.

Exit codes:
  0  clean streaming read, profile printed (drift vs register truth is printed
     as a finding, it is data, not a gate failure)
  1  malformed JSON rows encountered
  2  index file missing or unreadable
  3  --apply refused (not landed in unit 1)

Usage:
  .venv/Scripts/python.exe tools/estate_index_compact.py --check
  .venv/Scripts/python.exe tools/estate_index_compact.py --check --json
  .venv/Scripts/python.exe tools/estate_index_compact.py --check --index <path>
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "dashboard" / "data" / "ESTATE_INDEX.jsonl"
MIRROR = ROOT / "watch" / "ESTATE_INDEX" / "ESTATE_INDEX.jsonl"

HOOK_MARK = ".mimosa\\hook-state\\"
NAMED_ROOT_PREFIX = "local_sovereign_agent\\" + HOOK_MARK
LANE_PREFIX = HOOK_MARK  # rel paths starting here are the '_mimosa' sibling lane

REGISTER_TRUTH = {
    "rows": 10_661_260,
    "source": 9_524_538,
    "file_size_bytes": 4_150_418_528,  # the .jsonl file's own size on disk
    "named_root_source": 9_168_740,
    "mimosa_lane_source": 350_503,
    "other_nested_source": 5_295,
    "retire_single_root_pct": 86.01,   # register's published 2dp; live is 86.0005
    "retire_two_roots_pct": 89.29,
    "retire_source_pct": 89.34,        # register's 89.34 is the .source basis
}


def classify(raw_path: str) -> str | None:
    """Bucket a row path into the register's per-root classes, or None.

    Matches r04's census classes: named root, '_mimosa' sibling lane (rel path
    starting at .mimosa), and other nested .mimosa hook-state copies.
    """
    p = raw_path.replace("/", "\\").lower()
    if HOOK_MARK not in p:
        return None
    if p.startswith(NAMED_ROOT_PREFIX):
        return "named_root"
    if p.startswith(LANE_PREFIX):
        return "mimosa_lane"
    return "other_nested"


def stat_link_state(path: Path) -> dict:
    """os.stat hardlink identity for the D1 re-verify (never trusts a morning)."""
    st = path.stat()
    return {
        "size": st.st_size,
        "mtime_utc": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "dev": st.st_dev,
        "ino": st.st_ino,
        "nlink": st.st_nlink,
    }


def fsutil_hardlinks(path: Path) -> dict:
    """Best-effort 'fsutil hardlink list' (D1's own instrument). Never fatal."""
    try:
        r = subprocess.run(
            ["fsutil", "hardlink", "list", str(path)],
            capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"available": False, "reason": str(exc)[:120]}
    if r.returncode != 0:
        return {"available": False, "reason": (r.stderr or r.stdout).strip()[:120]}
    lines = [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]
    return {"available": True, "link_count": len(lines), "links": lines[:4]}


def check_index(index_path: Path) -> dict:
    """One read-only streaming pass over the index. Accumulates counters only."""
    if not index_path.is_file():
        return {"state": "missing", "index": str(index_path)}
    totals = {
        "file_size_bytes": index_path.stat().st_size,
        "rows": 0, "source": 0, "hookstate_rows": 0,
        "bad_rows": 0, "empty_lines": 0, "unclassified_source": 0,
        "sum_indexed_bytes": 0, "hookstate_bytes": 0,
    }
    per_root_rows = {"named_root": 0, "mimosa_lane": 0, "other_nested": 0}
    per_root_source = {"named_root": 0, "mimosa_lane": 0, "other_nested": 0}
    with index_path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.strip()
            if not s:
                totals["empty_lines"] += 1
                continue
            try:
                row = json.loads(s)
            except json.JSONDecodeError:
                totals["bad_rows"] += 1
                continue
            totals["rows"] += 1
            size = row.get("size", 0)
            if isinstance(size, (int, float)) and size > 0:
                totals["sum_indexed_bytes"] += int(size)
            cls = classify(str(row.get("path", "")))
            if cls is not None:
                totals["hookstate_rows"] += 1
                per_root_rows[cls] += 1
                if isinstance(size, (int, float)) and size > 0:
                    totals["hookstate_bytes"] += int(size)
            if row.get("ext") == ".source":
                totals["source"] += 1
                if cls is not None:
                    per_root_source[cls] += 1
                else:
                    totals["unclassified_source"] += 1
    out = {
        "state": "ok", "index": str(index_path),
        "per_root_rows": per_root_rows, "per_root_source": per_root_source,
        **totals,
    }
    if totals["rows"]:
        out["retire_single_root_pct"] = round(
            per_root_source["named_root"] / totals["rows"] * 100, 4)
        out["retire_two_roots_pct"] = round(
            (per_root_source["named_root"] + per_root_source["mimosa_lane"])
            / totals["rows"] * 100, 4)
        # The register's 89.34% is the .source basis; hook-state rows also
        # include non-.source files (live 2026-10-05: 4,072 of them), so
        # retire_all_hookstate_pct legitimately runs slightly higher.
        out["retire_source_pct"] = round(totals["source"] / totals["rows"] * 100, 4)
        out["retire_all_hookstate_pct"] = round(
            totals["hookstate_rows"] / totals["rows"] * 100, 4)
        out["retained_rows"] = totals["rows"] - totals["hookstate_rows"]
        out["retained_bytes"] = totals["sum_indexed_bytes"] - totals["hookstate_bytes"]
    out["link_state"] = {
        "index": stat_link_state(index_path),
        "mirror": stat_link_state(MIRROR) if MIRROR.is_file() else None,
        "fsutil_index": fsutil_hardlinks(index_path),
        "fsutil_mirror": fsutil_hardlinks(MIRROR) if MIRROR.is_file() else None,
    }
    ls = out["link_state"]
    if ls["mirror"] is not None:
        same = (ls["index"]["dev"] == ls["mirror"]["dev"]
                and ls["index"]["ino"] == ls["mirror"]["ino"])
        ls["verdict"] = ("HARDLINKED (one physical file)" if same
                         else "INDEPENDENT COPIES (two physical files)")
    else:
        ls["verdict"] = "mirror missing"
    return out


def drift_table(res: dict) -> list:
    """Compare the live profile against the r04 register truth (drift = finding)."""
    prs = res.get("per_root_source", {})
    rows = []
    for key in ("rows", "source", "file_size_bytes"):
        live = res.get(key)
        rows.append((key, live, REGISTER_TRUTH[key],
                     "MATCH" if live == REGISTER_TRUTH[key] else "DRIFT"))
    for key in ("named_root_source", "mimosa_lane_source", "other_nested_source"):
        live = prs.get(key[: -len("_source")])
        rows.append((key, live, REGISTER_TRUTH[key],
                     "MATCH" if live == REGISTER_TRUTH[key] else "DRIFT"))
    for key, tol in (("retire_single_root_pct", 0.01),
                     ("retire_two_roots_pct", 0.005),
                     ("retire_source_pct", 0.005)):
        live = res.get(key)
        if live is None:
            rows.append((key, None, REGISTER_TRUTH[key], "NO-DATA"))
            continue
        rows.append((key, live, REGISTER_TRUTH[key],
                     "MATCH" if abs(live - REGISTER_TRUTH[key]) <= tol else "DRIFT"))
    rows.append(("retire_all_hookstate_pct", res.get("retire_all_hookstate_pct"),
                 None, "INFO"))  # hook-state-rows basis; no register truth (see above)
    return rows


def print_profile(res: dict) -> None:
    idx = res["index"]
    print(f"ESTATE INDEX COMPACT --check: {idx}")
    print(f"  file: {res.get('file_size_bytes', 0):,} bytes on disk, "
          f"{res.get('rows', 0):,} rows parsed; source rows {res.get('source', 0):,}; "
          f"bad {res.get('bad_rows', 0):,}; empty lines {res.get('empty_lines', 0):,}")
    prr = res.get("per_root_rows", {})
    prs = res.get("per_root_source", {})
    print(f"  per-root rows (all exts): named_root {prr.get('named_root', 0):,}, "
          f"mimosa_lane {prr.get('mimosa_lane', 0):,}, "
          f"other_nested {prr.get('other_nested', 0):,}")
    print(f"  per-root .source:        named_root {prs.get('named_root', 0):,}, "
          f"mimosa_lane {prs.get('mimosa_lane', 0):,}, "
          f"other_nested {prs.get('other_nested', 0):,}")
    print(f"  unclassified .source rows: {res.get('unclassified_source', 0):,}")
    print(f"  retire if named root excluded:           "
          f"{res.get('retire_single_root_pct')} pct (register truth 86.01)")
    print(f"  retire if the two roots excluded:        "
          f"{res.get('retire_two_roots_pct')} pct (register truth 89.29)")
    print(f"  retire .source rows only:                "
          f"{res.get('retire_source_pct')} pct (register truth 89.34)")
    print(f"  retire all hook-state rows:              "
          f"{res.get('retire_all_hookstate_pct')} pct "
          f"(includes {res.get('hookstate_rows', 0) - res.get('source', 0):,} "
          f"non-.source hook-state rows)")
    print(f"  projection (sum of indexed sizes): retire "
          f"{res.get('hookstate_bytes', 0):,} bytes / "
          f"{res.get('hookstate_rows', 0):,} rows; retain "
          f"{res.get('retained_bytes', 0):,} bytes / {res.get('retained_rows', 0):,} rows")
    ls = res.get("link_state", {})
    print(f"  hardlink re-verify (D1): {ls.get('verdict')}")
    for name in ("fsutil_index", "fsutil_mirror"):
        f = ls.get(name, {})
        if f.get("available"):
            print(f"    {name}: fsutil hardlink list -> {f['link_count']} link(s)")
        else:
            print(f"    {name}: fsutil unavailable ({f.get('reason', 'n/a')})")
    print("  drift vs register truth (r04 2026-10-04 census):")
    for key, live, truth, verdict in drift_table(res):
        print(f"    {key:26s} live {live} truth {truth} {verdict}")
    print(
        f"PROFILE rows={res.get('rows', 0)} source={res.get('source', 0)} "
        f"named_root_source={prs.get('named_root', 0)} "
        f"mimosa_lane_source={prs.get('mimosa_lane', 0)} "
        f"other_nested_source={prs.get('other_nested', 0)} "
        f"hookstate_rows={res.get('hookstate_rows', 0)} "
        f"retire_single_root={res.get('retire_single_root_pct')} "
        f"retire_two_roots={res.get('retire_two_roots_pct')} "
        f"retire_source={res.get('retire_source_pct')} "
        f"file_size_bytes={res.get('file_size_bytes', 0)} "
        f"bad_rows={res.get('bad_rows', 0)}"
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", default=True,
                      help="measure only (default; never writes)")
    mode.add_argument("--apply", action="store_true",
                      help="NOT landed in unit 1; refuses without touching anything")
    ap.add_argument("--index", type=Path, default=DEFAULT_INDEX,
                    help="index file to stream (default: dashboard copy)")
    ap.add_argument("--json", action="store_true", help="print the result as JSON")
    args = ap.parse_args(argv)

    if args.apply:
        print("APPLY REFUSED (exit 3): the destructive rewrite of the 4.15 GB "
              "artifact is not landed in unit 1; unit discipline keeps it in its "
              "own sitting. Register: corpus/steal/MASTER_READ_ESTATE.md section 9 "
              "row 1. Nothing was touched, nothing deleted.")
        return 3

    index_path = args.index if args.index.is_absolute() else ROOT / args.index
    res = check_index(index_path)
    if args.json:
        print(json.dumps(res, indent=1))
    if res["state"] == "missing":
        print(f"CHECK ERROR: index missing at {res['index']}")
        return 2
    if not args.json:
        print_profile(res)
    if res.get("bad_rows", 0) > 0:
        print(f"CHECK: {res['bad_rows']} malformed rows; exit 1")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
