#!/usr/bin/env python3
"""receipt_xref_gate.py - dead-citation gate for watch/inbox receipts (W2, 2026-09-29).

The disease this meters (MICKEY17 wave ledger RETURN 14,
watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md): receipts cite repo paths in
backticks and nothing verifies those citations resolve on disk. One dead
citation poisons every downstream dispatch that trusts the receipt (a lane
loads the cited path, finds nothing, and re-derives from scratch or silently
skips the step). skills_lint already owned the path-existence regex but
pointed it only at SKILL.md; this gate self-steals that regex and points it
at receipts.

Bar in numbers BEFORE reading anything:

  every backticked repo-relative path (docs/|watch/|mag/|tools/|configs/|
  corpus/|memory/|state/|scripts/|tests/|server/ prefixed, the skills_lint
  allowlist plus server/ for the world lane) cited in a scanned receipt must
  exist on disk; every trivially parseable LINKS-N citation must name a row
  of watch/inbox/LINKS.jsonl (1-based). Richer citation shapes (prose
  references, unbackticked paths, LINKS row titles) stay out of scope: a
  gate that guesses citations fails closed on noise.

Fail-closed where the instrument is blind: a receipt that cannot be read, a
requested receipt that does not exist, --changed with file args, or a git
failure is exit 2, never a pass. Dead citations themselves are WARN-only by
default (exit 0, the census-patrol t40 precedent: no lockouts without
operator); --strict flips them to exit 1 (the same flip convention as the
freshness TODO-FLIP-TO-ENFORCE arm).

Output contract (githooks case-arm convention, B2-338): a green run's FIRST
line opens with the exact lowercase prefix "RECEIPT-XREF: ok"; red runs keep
the uppercase token DEAD-CITATIONS / CANNOT-VERIFY so a hook case arm can
route them to the WARN tail. All printed text passes through mask(): runs
that look like keys, tokens, or long hex/base64 blobs are replaced with
[REDACTED] before printing, because receipts sometimes quote environment
scraps and a citation gate must never become a leak surface.

Usage:
  .venv/Scripts/python.exe tools/receipt_xref_gate.py FILE [FILE...]   WARN-only
  .venv/Scripts/python.exe tools/receipt_xref_gate.py --changed        git diff vs HEAD, .md under watch/
  .venv/Scripts/python.exe tools/receipt_xref_gate.py --summary FILE.. dead-citation counts per receipt
  .venv/Scripts/python.exe tools/receipt_xref_gate.py --strict ...     exit 1 on any dead citation
  --root PATH (census_drift_patrol convention) pins the repo root, which
  keeps the CLI exit codes testable against a synthetic mini-estate.

Exit codes: 0 = no dead citations (or dead citations in WARN-only mode);
1 = dead citations under --strict; 2 = cannot verify.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LINKS_LEDGER_RELPATH = "watch/inbox/LINKS.jsonl"

# Self-steal: tools/skills_lint.py:61 path-existence regex, plus server/
# (skills_lint was written before the world lane landed).
PATH_RE = re.compile(
    r"`((?:docs|watch|mag|tools|configs|corpus|memory|state|scripts|tests|server)/[^`\s]+)`"
)
# House citation form `mag/x.py:245-306` names the FILE plus a line anchor;
# the anchor is not part of the path. Resolving the anchor literally was the
# W2 first-run defect: 12 of 21 raw hits were live files flagged dead. The
# gate strips a trailing :line[,line[-line]] anchor and resolves the base.
ANCHOR_RE = re.compile(r":\d+(?:[-,]\d+)*$")
# Trivially parseable LINKS-row citation: LINKS-N names the Nth (1-based) row
# of watch/inbox/LINKS.jsonl.
LINKS_RE = re.compile(r"\bLINKS-(\d+)\b")

SECRET_RE = re.compile(
    r"(sk-[A-Za-z0-9_-]{8,}"
    r"|ghp_[A-Za-z0-9]{16,}"
    r"|xox[baprs]-[A-Za-z0-9-]{10,}"
    r"|AKIA[0-9A-Z]{16}"
    r"|Bearer\s+[A-Za-z0-9._-]{8,}"
    r"|[A-Fa-f0-9]{40,}"
    r"|[A-Za-z0-9+/=]{60,}"
    r"|(?:api[_-]?key|apikey|token|secret|password)['\"]?\s*[:=]\s*['\"]?[^\s'\"]+)",
    re.IGNORECASE,
)


def mask(text: str) -> str:
    """Redact secret-looking runs before anything is printed."""
    return SECRET_RE.sub("[REDACTED]", text)


def extract_paths(text: str) -> list[str]:
    return sorted(set(PATH_RE.findall(text)))


def extract_links_rows(text: str) -> list[int]:
    return sorted({int(n) for n in LINKS_RE.findall(text)})


def links_row_count(repo: Path) -> int:
    """Row count of the LINKS ledger, or -1 when the ledger itself is missing."""
    ledger = repo / LINKS_LEDGER_RELPATH
    if not ledger.is_file():
        return -1
    with ledger.open(encoding="utf-8", errors="replace") as fh:
        return sum(1 for _ in fh)


def scan_receipt(md: Path, repo: Path = REPO) -> list[str]:
    """Dead-citation rows for one receipt (raw; the runner masks at print).

    An unreadable receipt yields one CANNOT-VERIFY row instead of a pass.
    """
    try:
        text = md.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [f"CANNOT-VERIFY unreadable receipt: {exc}"]
    dead: list[str] = []
    for p in extract_paths(text):
        base = ANCHOR_RE.sub("", p)
        if not (repo / base).exists():
            dead.append(f"DEAD-CITATION path `{p}` resolves to nothing on disk")
    rows = links_row_count(repo)
    for n in extract_links_rows(text):
        if rows < 0:
            dead.append(f"DEAD-CITATION LINKS-{n}: ledger {LINKS_LEDGER_RELPATH} missing")
        elif n < 1 or n > rows:
            dead.append(f"DEAD-CITATION LINKS-{n}: ledger has {rows} rows")
    return dead


def changed_receipts(repo: Path) -> list[Path]:
    """Receipts (`.md` under watch/) changed vs HEAD, per git diff --name-only."""
    proc = subprocess.run(
        ["git", "-C", str(repo), "diff", "--name-only", "HEAD", "--", "watch/"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git diff failed: {mask(proc.stderr.strip())}")
    out: list[Path] = []
    for line in proc.stdout.splitlines():
        name = line.strip()
        if name.endswith(".md") and (repo / name).is_file():
            out.append(repo / name)
    return out


def parse_args(argv: list[str]) -> tuple[dict | None, str | None]:
    """Split argv into options/files. Returns (opts, error_line); error wins."""
    opts: dict = {"strict": False, "summary": False, "changed": False, "root": None, "files": []}
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--root":
            i += 1
            if i >= len(argv):
                return None, "RECEIPT-XREF: CANNOT-VERIFY --root needs a PATH value"
            opts["root"] = argv[i]
        elif arg == "--strict":
            opts["strict"] = True
        elif arg == "--summary":
            opts["summary"] = True
        elif arg == "--changed":
            opts["changed"] = True
        elif arg.startswith("--"):
            return None, f"RECEIPT-XREF: CANNOT-VERIFY unknown flag {arg}"
        else:
            opts["files"].append(arg)
        i += 1
    return opts, None


def run(argv: list[str] | None = None, repo: Path = REPO) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    opts, err = parse_args(argv)
    if err is not None:
        print(err)
        return 2
    if opts["root"]:
        repo = Path(opts["root"]).resolve()
    strict, summary, changed = opts["strict"], opts["summary"], opts["changed"]
    file_args: list[str] = opts["files"]

    if changed and file_args:
        print("RECEIPT-XREF: CANNOT-VERIFY --changed takes no file arguments")
        return 2
    if changed:
        try:
            receipts = changed_receipts(repo)
        except RuntimeError as exc:
            print(f"RECEIPT-XREF: CANNOT-VERIFY {exc}")
            return 2
    else:
        receipts = [Path(a) for a in file_args]
        missing = [str(r) for r in receipts if not r.is_file()]
        if missing:
            print(
                "RECEIPT-XREF: CANNOT-VERIFY receipt(s) not found: "
                + ", ".join(mask(m) for m in missing)
            )
            return 2
        if not receipts:
            print("RECEIPT-XREF: CANNOT-VERIFY no receipts given (pass files or --changed)")
            return 2

    dead_by_receipt: list[tuple[Path, list[str]]] = [(r, scan_receipt(r, repo)) for r in receipts]
    total_dead = sum(len(rows) for _, rows in dead_by_receipt)

    if total_dead == 0:
        print(f"RECEIPT-XREF: ok ({len(receipts)} receipt(s) scanned, 0 dead citations)")
        if summary:
            for r, _ in dead_by_receipt:
                print(f"  {mask(str(r))}: dead=0")
        return 0

    arm = "STRICT" if strict else "WARN-ONLY"
    print(f"RECEIPT-XREF: DEAD-CITATIONS ({arm}) {total_dead} dead citation(s) found")
    for r, rows in dead_by_receipt:
        if summary:
            print(f"  {mask(str(r))}: dead={len(rows)}")
        else:
            for row in rows:
                print(f"  {mask(str(r))}: {mask(row)}")
    if strict:
        print("exit 1 (--strict): fix the citation or restore the file it names")
        return 1
    return 0


def main() -> None:
    sys.exit(run())


if __name__ == "__main__":
    main()
