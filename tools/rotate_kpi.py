"""rotate_kpi.py - archive old rows of logs/kpi.jsonl to a dated gzip, then truncate (2026-10-03).

Why: logs/kpi.jsonl (writer mag/records.py:138 write_kpi, append at :166) has no
rotation and passed 790 MB. The only code reader found (rg, 2026-10-03) is
synthesis_agent.py:181 `_last_jsonl(KPI_JSONL)`, which wants the LAST row only;
mag/biography/kpi.json already holds the latest row in full. So the live file
only needs a recent window.

Self-steal: shape from scripts/backup_chain.py (dated archive name, idempotent,
a no-write status path) and the receipt trail in
watch/inbox/burn_reset_20260927/flash50/large-file-census.md section 7.
No rotation helper existed in tools/ or scripts/ (rg rotat|gzip, 2026-10-03).

Safety:
- DEFAULT IS DRY RUN. Nothing is written unless --apply is passed.
- Snapshot boundary = last newline at start; rows appended by the writer while
  this runs are preserved (they are re-read and written back after the kept window).
- Archive = every snapshot row except the newest --keep rows, written to
  <archive-dir>/kpi_<first-date>_<last-date>_<stamp>.jsonl.gz.
- Verify before truncating: gzip row count == archived row count AND
  archived + kept == snapshot rows AND sha256 of archived bytes matches.
  Any mismatch aborts with the live file untouched.
- Never deletes the archive; never touches mag/biography/kpi.json.

CLI:
  .venv\\Scripts\\python.exe tools\\rotate_kpi.py                 # dry run (default)
  .venv\\Scripts\\python.exe tools\\rotate_kpi.py --keep 2000      # dry run, other window
  .venv\\Scripts\\python.exe tools\\rotate_kpi.py --apply          # real run (operator)
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import sys
import zlib
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KPI = ROOT / "logs" / "kpi.jsonl"
ARCHIVE_DIR = ROOT / "attic" / "kpi"
CHUNK = 8 * 1024 * 1024


def _snapshot_end(path: Path) -> int:
    """Byte offset just past the last newline (a half-written tail row is excluded)."""
    size = path.stat().st_size
    with path.open("rb") as f:
        pos = size
        while pos > 0:
            step = min(65536, pos)
            pos -= step
            f.seek(pos)
            buf = f.read(step)
            i = buf.rfind(b"\n")
            if i >= 0:
                return pos + i + 1
    return 0


def _row_ts(line: bytes) -> str:
    try:
        return str(json.loads(line).get("ts") or "")[:10]
    except Exception:  # noqa: BLE001
        return ""


def scan(path: Path, end: int, keep: int) -> dict:
    """One streaming pass: total rows, byte offset where the kept window starts."""
    rows = 0
    offsets: deque[int] = deque(maxlen=keep + 1)
    first_line = b""
    pos = 0
    with path.open("rb") as f:
        while pos < end:
            line = f.readline()
            if not line:
                break
            if pos + len(line) > end:
                break
            if rows == 0:
                first_line = line
            offsets.append(pos)
            rows += 1
            pos += len(line)
    # offsets holds the starts of the last keep+1 rows; the kept window starts at offsets[1]
    cut = offsets[1] if rows > keep else 0
    last_old = b""
    if cut:
        with path.open("rb") as f:
            back = min(cut, 1 << 20)
            f.seek(cut - back)
            tail = f.read(back).rstrip(b"\n")
            last_old = tail[tail.rfind(b"\n") + 1:]
    return {
        "rows": rows,
        "archive_rows": max(rows - keep, 0),
        "keep_rows": min(rows, keep),
        "cut": cut,
        "end": end,
        "first_date": _row_ts(first_line),
        "last_old_date": _row_ts(last_old) if last_old else "",
    }


def estimate_ratio(path: Path, cut: int, sample: int = 32 * 1024 * 1024) -> float:
    n = min(cut, sample)
    if n <= 0:
        return 0.0
    with path.open("rb") as f:
        data = f.read(n)
    return len(zlib.compress(data, 6)) / max(len(data), 1)


def archive_and_verify(path: Path, cut: int, expect_rows: int, dest: Path) -> dict:
    h_src = hashlib.sha256()
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    left = cut
    with path.open("rb") as src, gzip.open(tmp, "wb", compresslevel=6) as gz:
        while left > 0:
            buf = src.read(min(CHUNK, left))
            if not buf:
                break
            h_src.update(buf)
            gz.write(buf)
            left -= len(buf)
    if left != 0:
        raise RuntimeError(f"short read: {left} bytes not copied")
    h_gz = hashlib.sha256()
    gz_rows = 0
    with gzip.open(tmp, "rb") as gz:
        while True:
            buf = gz.read(CHUNK)
            if not buf:
                break
            h_gz.update(buf)
            gz_rows += buf.count(b"\n")
    if gz_rows != expect_rows or h_gz.hexdigest() != h_src.hexdigest():
        raise RuntimeError(f"verify FAILED: gz_rows={gz_rows} expect={expect_rows} "
                           f"sha_match={h_gz.hexdigest() == h_src.hexdigest()}")
    os.replace(tmp, dest)
    return {"gz_rows": gz_rows, "sha256": h_src.hexdigest(), "gz_bytes": dest.stat().st_size}


def truncate_keep(path: Path, cut: int) -> int:
    """Rewrite the live file in place as bytes[cut:] (kept window + anything appended meanwhile)."""
    with path.open("r+b") as f:
        f.seek(cut)
        rest = f.read()  # kept window (~MBs) + concurrent appends
        f.seek(0)
        f.write(rest)
        f.truncate()
        f.flush()
        os.fsync(f.fileno())
    return len(rest)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--path", default=str(KPI))
    ap.add_argument("--keep", type=int, default=1000, help="newest rows left in the live file")
    ap.add_argument("--archive-dir", default=str(ARCHIVE_DIR))
    ap.add_argument("--apply", action="store_true", help="real run; default is dry run")
    a = ap.parse_args(argv)
    a.keep = max(1, a.keep)
    path = Path(a.path)
    if not path.is_file():
        print(json.dumps({"ok": False, "error": f"missing {path}"}))
        return 2
    size = path.stat().st_size
    end = _snapshot_end(path)
    s = scan(path, end, a.keep)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    name = f"kpi_{s['first_date'] or 'start'}_{s['last_old_date'] or 'end'}_{stamp}.jsonl.gz"
    dest = Path(a.archive_dir) / name
    ratio = estimate_ratio(path, s["cut"])
    plan = {
        "mode": "apply" if a.apply else "dry-run",
        "path": str(path), "size_bytes": size, "snapshot_end": end,
        "rows_total": s["rows"], "rows_to_archive": s["archive_rows"], "rows_kept": s["keep_rows"],
        "archive_bytes_raw": s["cut"], "live_bytes_after": end - s["cut"],
        "est_gzip_bytes": int(s["cut"] * ratio), "est_gzip_ratio": round(ratio, 4),
        "archive_path": str(dest), "first_row_date": s["first_date"],
        "last_archived_row_date": s["last_old_date"],
    }
    if not a.apply or s["archive_rows"] == 0:
        plan["ok"] = True
        plan["note"] = "dry run: nothing written" if not a.apply else "nothing to archive"
        print(json.dumps(plan, indent=2))
        return 0
    v = archive_and_verify(path, s["cut"], s["archive_rows"], dest)
    plan.update(v)
    plan["live_bytes_written"] = truncate_keep(path, s["cut"])
    plan["ok"] = True
    print(json.dumps(plan, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
