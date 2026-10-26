#!/usr/bin/env python3
"""break-communication hostile probe (ouroboros R3): independent adjudication
of the seal-patrol drift set. Imports the patrol's own parse/patrol core,
then for each drifted file checks: full-ledger latest row (any depth), row
count, CRLF/LF-normalized sha variants, git tracked/committed state, mtime.
Any subprocess spawn carries CREATE_NO_WINDOW (win32 law).
"""
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from tools.prepush_seal_patrol import DEFAULT_LEDGER, ESTATE_ROOT, parse_ledger, patrol, resolve_sealed_path  # noqa: E402

CREATE_NO_WINDOW = 0x08000000


def git_out(args: list[str], cwd: Path) -> str:
    try:
        p = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True,
                           text=True, timeout=30, creationflags=CREATE_NO_WINDOW)
        return (p.stdout or "").strip()
    except Exception as e:
        return f"ERR {e}"


def main() -> int:
    root = ESTATE_ROOT
    rows, malformed = parse_ledger(DEFAULT_LEDGER)
    res = patrol(root, rows, 1000)
    drifted = [p for p, _, _ in res["drifted"]]
    print(f"drift set at --rows 1000, moment {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}: {len(drifted)} files")

    # full-ledger latest row per drifted path (no window)
    latest_full: dict[Path, dict] = {}
    for r in rows:
        rp = resolve_sealed_path(root, str(r["file"]))
        if rp is None:
            continue
        latest_full[rp] = r
    now = time.time()
    for path in sorted(drifted):
        rel = path.relative_to(root).as_posix()
        full = latest_full.get(path)
        sealed = str(full["sha256"]).lower() if full else "NO-ROW"
        ts = full.get("ts", "?") if full else "?"
        n_rows = sum(1 for r in rows if resolve_sealed_path(root, str(r["file"])) == path)
        raw = path.read_bytes()
        variants = {
            "raw": __import__("hashlib").sha256(raw).hexdigest(),
            "crlf->lf": __import__("hashlib").sha256(raw.replace(b"\r\n", b"\n")).hexdigest(),
            "lf->crlf": __import__("hashlib").sha256(raw.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")).hexdigest(),
        }
        variant_hit = [k for k, v in variants.items() if v == sealed]
        st = git_out(["status", "--porcelain", "--", rel], root)
        log = git_out(["log", "-n", "1", "--format=%h %ad", "--date=short", "--", rel], root)
        age_min = round((now - path.stat().st_mtime) / 60, 1)
        print(f"\n== {rel}")
        print(f"  full-ledger latest seal: ts={ts} rows_total={n_rows} sealed={sealed[:12]}")
        print(f"  full-ledger latest still drifts: {variants['raw'] != sealed}")
        print(f"  line-ending variant match: {variant_hit or 'NONE'}")
        print(f"  mtime age: {age_min} min")
        print(f"  git status: {st or 'CLEAN/UNTRACKED-ABSENT'}")
        print(f"  git last commit: {log or 'NEVER COMMITTED'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
