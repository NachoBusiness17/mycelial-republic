"""Recompute every caption-ledger have-row sha256 against disk bytes.

B2-409 (2026-09-26). Invariant: every have-row of
watch/inbox/CAPTION_LEDGER_20260926.jsonl carries a sha256 (backfilled from
disk bytes by B2-89), and the file bytes must still hash to it. The B2-12
builder re-verified only REGISTER-supplied shas at build time, so a hashed
file drifting after the build was invisible to every existing check; this
script is the named drift detector and is wired into the builder as a
post-write gate (next to the B2-421 caption_via gate).

Rows without a path (metadata-only) are counted, not failed. A path that is
missing on disk or a sha mismatch is a named FAIL (path + row sha + actual,
first 20 shown). Relative paths resolve under the export root
(watch/inbox/mrpool_export; 497/497 of the first 500 rows verified there at
land time); absolute paths are used as-is.

Usage:
  python tools/caption_ledger_sha_check.py [--ledger PATH] [--root PATH] [--limit N]
Exit 0 = every checked sha matches. Exit 1 = any mismatch/missing/bad row.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = ROOT / "watch" / "inbox" / "CAPTION_LEDGER_20260926.jsonl"
DEFAULT_ROOT = ROOT / "watch" / "inbox" / "mrpool_export"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT,
                    help="base dir for ledger-relative paths")
    ap.add_argument("--limit", type=int, default=0,
                    help="check only the first N rows (0 = all); scratch-run arm")
    args = ap.parse_args(argv)

    rows_checked = 0
    rows_meta = 0
    mismatches: list[str] = []
    missing: list[str] = []
    bad_rows: list[str] = []
    with args.ledger.open(encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if args.limit and rows_checked + rows_meta >= args.limit:
                break
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except Exception as exc:
                bad_rows.append(f"line {n}: unparseable ({exc})")
                continue
            path = row.get("path")
            sha = row.get("sha256")
            if not path:
                rows_meta += 1
                if sha:
                    bad_rows.append(f"line {n}: sha256 without path ({path!r})")
                continue
            if not sha:
                # have-row without a sha: not the B2-89 post-backfill state
                bad_rows.append(f"line {n}: have-row {path} missing sha256")
                continue
            rows_checked += 1
            p = Path(path)
            if not p.is_absolute():
                p = args.root / path
            if not p.is_file():
                missing.append(f"line {n}: {path} (registered sha {str(sha)[:12]}...)")
                continue
            actual = sha256_file(p)
            if actual.lower() != str(sha).lower():
                mismatches.append(
                    f"line {n}: {path} DRIFT ledger={str(sha)[:16]}... disk={actual[:16]}...")
            if len(mismatches) >= 20 or len(missing) >= 20 or len(bad_rows) >= 20:
                break

    ok = not (mismatches or missing or bad_rows)
    print(f"caption-ledger sha check: {rows_checked} have-rows hashed, "
          f"{rows_meta} metadata-only, mismatches {len(mismatches)}, "
          f"missing {len(missing)}, bad rows {len(bad_rows)}: "
          f"{'PASS' if ok else 'FAIL'}")
    for m in (mismatches + missing + bad_rows)[:20]:
        print("  " + m)
    if mismatches:
        print("DRIFT LAW: a hashed file changed after the ledger carried its "
              "sha; re-audit the file (B2-89 provenance) and re-register the "
              "row with a named byte audit before touching these constants.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
