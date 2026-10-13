"""B6 backfill: register INTAKE_* URLs into the canonical ledger via mag.link_library.

Stdlib only, fixed paths. Never touches LINKS.jsonl directly — all writes go
through mag.link_library.add_urls (which dedupes via canonical checks and
refuses localhost/private hosts via validate_host_safety).

Run: .venv\\Scripts\\python.exe artifacts\\backfill_links_20260916.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
INBOX = ROOT / "watch" / "inbox"
sys.path.insert(0, str(ROOT))

from mag.link_library import add_urls  # noqa: E402

URL_RE = re.compile(r"https?://\S+")
WRITER = "backfill-20260916"


def clean_url(raw: str) -> str:
    """Trim markdown/typographic trailing junk from a regex match."""
    url = raw.rstrip(".,;:!?'\"]>")
    while url.endswith(")") and url.count("(") < url.count(")"):
        url = url[:-1]
    return url


def main() -> int:
    files = sorted(INBOX.glob("INTAKE_*.md"))
    totals = {
        "files_scanned": 0,
        "urls_found": 0,
        "registered": 0,
        "duplicate": 0,
        "refused": 0,
    }
    per_file: list[dict] = []
    refused_detail: list[dict] = []

    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        raw_urls = [clean_url(m.group(0)) for m in URL_RE.finditer(text)]
        # de-dupe within file, keep order
        seen: set[str] = set()
        urls = [u for u in raw_urls if not (u in seen or seen.add(u))]
        stats = {"file": path.name, "urls_found": len(urls), "registered": 0,
                 "duplicate": 0, "refused": 0}
        for url in urls:
            try:
                entries = add_urls([url], note=f"backfill from {path.name}", writer=WRITER)
            except ValueError as exc:
                stats["refused"] += 1
                refused_detail.append({"file": path.name, "url": url, "reason": str(exc)})
                continue
            entry = entries[0]
            if entry["duplicate_of"]:
                stats["duplicate"] += 1
            else:
                stats["registered"] += 1
        totals["files_scanned"] += 1
        totals["urls_found"] += stats["urls_found"]
        totals["registered"] += stats["registered"]
        totals["duplicate"] += stats["duplicate"]
        totals["refused"] += stats["refused"]
        per_file.append(stats)
        print(f"{path.name}: found={stats['urls_found']} "
              f"registered={stats['registered']} duplicate={stats['duplicate']} "
              f"refused={stats['refused']}")

    summary = {"totals": totals, "per_file": per_file, "refused_detail": refused_detail}
    print("\nSUMMARY_JSON")
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
