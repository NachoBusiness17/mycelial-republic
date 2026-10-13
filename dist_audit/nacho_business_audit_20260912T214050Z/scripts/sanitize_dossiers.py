"""Janitor: sanitize biography dossier .md files.

Strips API keys and <system-reminder> sludge from memory/biography/*.md
and writes clean copies to memory/biography/clean/.

Run: .venv\\Scripts\\python.exe scripts\\sanitize_dossiers.py [--dry]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC_DIR = REPO / "memory" / "biography"
DST_DIR = SRC_DIR / "clean"

KEY_PATTERNS = [
    re.compile(r"xai-[A-Za-z0-9]{16,}"),
    re.compile(r"sk-ant-[A-Za-z0-9_-]{16,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"gsk_[A-Za-z0-9]{16,}"),
    re.compile(r"AIza[A-Za-z0-9_-]{16,}"),
    re.compile(r"hf_[A-Za-z0-9]{16,}"),
    re.compile(r"ghp_[A-Za-z0-9]{16,}"),
    re.compile(r"gho_[A-Za-z0-9]{16,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{16,}"),
    re.compile(r"glpat-[A-Za-z0-9_-]{12,}"),
    re.compile(r"dop_v1_[a-f0-9]{32,}"),
    re.compile(r"eyJ[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"),
]
KEY_TOKEN = "[REDACTED-KEY]"

# whole bullet that is pure reminder sludge: "- <system-reminder> ..."
BULLET_RE = re.compile(r"^\s*-\s*<system-reminder>.*$")
# quoted sludge inside prose: “<system-reminder> … ” (ellipsis + close quote)
QUOTE_RE = re.compile(r"<system-reminder>.*?\u2026\u201d", re.DOTALL)
# any leftover reminder fragment up to end of line
TAIL_RE = re.compile(r"<system-reminder>.*$")


def redact_keys(text: str) -> tuple[str, int]:
    n = 0
    for pat in KEY_PATTERNS:
        text, k = pat.subn(KEY_TOKEN, text)
        n += k
    return text, n


def sanitize_line(line: str) -> str | None:
    """Return cleaned line, or None if the line should be dropped."""
    if BULLET_RE.match(line):
        return None
    # inline quoted sludge -> placeholder
    line = QUOTE_RE.sub("[system notification]\u201d", line)
    # trailing fragment (unclosed reminder) -> cut
    if "<system-reminder>" in line:
        line = TAIL_RE.sub("[system notification]", line)
    return line


def sanitize_file(src: Path, dst: Path, dry: bool) -> dict:
    raw = src.read_text(encoding="utf-8")
    kept, dropped = [], 0
    for line in raw.splitlines():
        cleaned = sanitize_line(line)
        if cleaned is None:
            dropped += 1
        else:
            kept.append(cleaned)
    body = "\n".join(kept)
    if raw.endswith("\n"):
        body += "\n"
    body, keys = redact_keys(body)
    if not dry:
        dst.write_text(body, encoding="utf-8")
    return {"file": src.name, "dropped": dropped, "redactions": keys,
            "changed": body != raw}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    if not SRC_DIR.is_dir():
        print(f"missing {SRC_DIR}", file=sys.stderr)
        return 1
    if not args.dry:
        DST_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(p for p in SRC_DIR.glob("*.md") if p.is_file())
    total_dropped = total_keys = total_changed = 0
    for src in files:
        dst = DST_DIR / src.name
        r = sanitize_file(src, dst, args.dry)
        total_dropped += r["dropped"]
        total_keys += r["redactions"]
        total_changed += 1 if r["changed"] else 0
        print(f"{r['file']}: dropped={r['dropped']} keys={r['redactions']} "
              f"changed={r['changed']}")
    print(f"--- {len(files)} files · {total_changed} changed · "
          f"{total_dropped} sludge lines dropped · {total_keys} keys redacted"
          + (" · DRY" if args.dry else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
