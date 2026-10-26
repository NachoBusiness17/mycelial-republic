"""path_lint — detect workspace-path strays (self-gap pass 3 law: absence-claims
need searcher's root; agents that lose their root write to the sandbox default
workspace instead of the repo).

Checks:
  1. repo files CONTAINING the stray prefix (evidence a stray was referenced/homed late)
  2. live strays: files sitting in the default workspace dirs that mention the repo
     (orphans awaiting mv home)
  3. receipts the scan itself (rows, not claims)

Run:  python -u tools/path_lint.py
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ROOT  # noqa: E402

STRAY_PREFIX = "C:/Users/foste/.zcode/workspace/default"
STRAY_PREFIXES = [STRAY_PREFIX, STRAY_PREFIX.replace("/", "\\")]
# dirs a lost agent most likely wrote into
STRAY_ROOTS = [Path(STRAY_PREFIX), Path(STRAY_PREFIX) / "memory"]
SKIP_PARTS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".py", ".txt", ".yaml", ".yml", ".toml", ".log", ".cfg"}


def main() -> None:
    repo_hits, live_strays = [], []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_PARTS]
        for fn in filenames:
            p = Path(dirpath) / fn
            if p.suffix.lower() not in TEXT_SUFFIXES or p.stat().st_size > 2_000_000:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if any(pref in text for pref in STRAY_PREFIXES):
                repo_hits.append(p.relative_to(ROOT).as_posix())

    for root in STRAY_ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if p.stat().st_size > 5_000_000:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            marker = str(ROOT).replace("\\", "/").lower()
            if marker in text.replace("\\", "/").lower():
                live_strays.append(p.as_posix())

    print(f"[repo references to stray prefix] {len(repo_hits)}")
    for h in repo_hits[:25]:
        print("  ", h)
    print(f"[live strays in default workspace mentioning the repo] {len(live_strays)}")
    for s in live_strays[:25]:
        print("  ", s)
    receipt = ROOT / "memory" / "runs" / f"path_lint_{datetime.now(timezone.utc).strftime('%Y%m%d')}.json"
    receipt.write_text(__import__("json").dumps(
        {"utc": datetime.now(timezone.utc).isoformat(),
         "repo_reference_count": len(repo_hits), "repo_references": repo_hits,
         "live_stray_count": len(live_strays), "live_strays": live_strays},
        indent=1), encoding="utf-8")
    print(f"[receipt] {receipt}")


if __name__ == "__main__":
    main()
