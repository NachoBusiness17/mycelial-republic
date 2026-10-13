"""NIGHTLY METERS WRAPPER — runs the fleet meters and seals what it writes.

Dogfood wiring, 2026-09-22 (watch/inbox/DOGFOOD_OPERATING_ENVIRONMENT_20260922.md):
the meters go default across the mesh, but the md-record autoseal hook only covers
tool-call writes — files written by meters executed from a shell must append their
own register events or the audit flips to TEETH-MARKS. Found live that night: two
meter runs left 3 unsealed files. This wrapper is the cron-ready unit: it runs the
meters, then registers every output it produced.

Usage (repo root): .venv/Scripts/python.exe tools/meters_nightly.py
Schedule: one line in the estate's daily task (e.g. MagImproveDaily) — $0.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = ROOT / ".venv" / "Scripts" / "python.exe"
INBOX = ROOT / "watch" / "inbox"
INDEX = INBOX / "index_events.jsonl"

JOBS = [
    ("tools/estate_smith_chart.py", ["--no-plot"], "smith chart nightly reading (meters_nightly)"),
    ("tools/curvature_scan.py", [], "curvature nightly reading (meters_nightly)"),
    ("tools/lattice_build.py", [], "estate lattice rebuild — the warm map stays fresh (meters_nightly)"),
]


def register(path: Path, purpose: str) -> None:
    sha = hashlib.sha256(path.read_bytes()).hexdigest().upper()
    now = datetime.now(timezone.utc)
    line = json.dumps(
        {
            "seq": int(now.timestamp() * 1e6),
            "ts": now.isoformat(timespec="seconds"),
            "op": "register",
            "file": "/board/inbox/" + path.name,
            "sha256": sha,
            "class": "RECEIPT",
            "purpose": purpose,
        },
        ensure_ascii=False,
    )
    with INDEX.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def main() -> int:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    sealed: list[str] = []
    for script, extra, purpose in JOBS:
        try:
            r = subprocess.run(
                [str(PY), str(ROOT / script), *extra],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                timeout=900,
            )
        except subprocess.TimeoutExpired:
            print(f"[meters] {script}: TIMEOUT")
            return 1
        if r.returncode != 0:
            print(f"[meters] {script}: FAIL {(r.stderr or r.stdout or '')[-300:]}")
            return 1
        print(f"[meters] {script}: ok")
        targets = ("ESTATE_SMITH_CHART_",) if "smith" in purpose else ("CATHEDRAL_CURVATURE_SCAN_",)
        for name in targets:
            for p in INBOX.glob(name + stamp + ".*"):
                register(p, purpose)
                sealed.append(p.name)
    print(f"[meters] sealed {len(sealed)}: {', '.join(sealed)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
