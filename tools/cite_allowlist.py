"""cite_allowlist -- input-scoped citation gate (port wave P1, 2026-10-07).

The steal (watch/inbox/frontier_olm_2026-10-07/steal/evals-self-improvement
via reddit.md, find 2, r/LocalLLaMA thread 1uolb4y): citations must come from
an INPUT ALLOWLIST, and any cite outside it fails the run. The estate's two
existing gates verify against the whole repo, so a seat citing a sibling
lane's file it never read passes both today: tools/citation_lint.py accepts
any cite whose path exists, and mag/cite_gate.py LOCAL-VERIFIES any non-empty
path under ROOT. This gate adds the missing input scope. Given (a) a produced
document (receipt / card / lane output) and (b) the allowlist of source paths
the producing seat was GIVEN (the ask's finds JSON, research pack, context
pack contents), every directory-anchored path cite in the document must
resolve INTO the allowlist. It tightens, never replaces, the two existing
gates: run citation_lint + cite_gate as before, then this.

Verdicts, one finding per unique cited path (first doc line reported):
  CITE-OUTSIDE-ALLOWLIST  the path resolves on disk but is not in the
                          allowlist (the sibling-file-it-never-read class)
  PATH-MISSING            the path resolves nowhere, so membership in the
                          allowlist cannot even be tested
Remediation: mark the work OWED with a receipt, or actually read the file and
have it enter the input set at ask time. Bare filenames (no separator) are
mentions, not load-bearing cites (cite_gate's standing stance) and are not
scanned; URLs are out of scope for this lane.

One-line integration call for the fold / receipt verification paths:

    from tools.cite_allowlist import check_doc
    ok = check_doc(doc_path, allowlist_path)["ok"]  # True = clean

check_doc never mutates the document and raises OSError (caller maps to
cannot-verify) only when a path is unreadable; findings never depend on
network, env, or cwd.

Allowlist file: one repo path per line; blank lines and #comments ignored;
a trailing slash (or an entry that is an on-disk directory) makes the entry
a directory prefix covering every file under it. Comparison is separator-,
prefix- (ROOT/), and case-normalized, so win32 and repo-form cites match
one allowlist spelling.

Exit contract: 0 = clean, 1 = findings, 2 = cannot verify (bad args,
unreadable doc or allowlist). First-line law (B2-338 shape): green opens
"CITE-ALLOWLIST: ok", blocking "CITE-ALLOWLIST: FAIL", cannot-verify
"CITE-ALLOWLIST: ERROR"; never widen. The cite grammar mirrors
tools/citation_lint_io.py so both gates parse cites identically.

CLI:
  python tools/cite_allowlist.py check --doc <file> --allowlist <file> [--json]
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parent.parent
TOOL = "CITE-ALLOWLIST"

# Same grammar as tools/citation_lint_io.py (CITE_SUFFIXES + PATH_RE): a
# path-shaped token with optional drive/directories and a known file suffix.
# No space in the grammar, so prose words never anchor into the path.
CITE_SUFFIXES = (
    "py|md|txt|jsonl|json|ts|mjs|js|ps1|sh|cmd|bat|yaml|yml|toml|cfg|ini|csv|rst|gd|lua"
)
PATH_RE = re.compile(
    r"(?:[A-Za-z]:[\\/])?[\w\-.][\w\-.\\/]*?\.(?:%s)" % CITE_SUFFIXES
)

# Trailing prose punctuation stripped from a token; leading dots survive
# (path content, e.g. .agents/...).
_TRAIL = "\"'`),.;:"


def clean_token(raw: str) -> str:
    """Token as written: collapse escaped/win32 separators, strip prose tail."""
    p = raw.replace("\\\\", "\x00").replace("\\", "/").replace("\x00", "\\")
    return p.strip().rstrip(_TRAIL)


def normalize(clean: str) -> str:
    """Comparison form: ROOT/ prefix off, ./ off, forward seps, lowercase."""
    p = clean
    if p.lower().startswith("root/"):
        p = p[5:]
    while p.startswith("./"):
        p = p[2:]
    return p.lower()


def load_allowlist(path) -> list:
    """One path per line; #comments and blanks skipped; a trailing slash or an
    on-disk directory entry becomes a directory prefix (kept with trailing /)."""
    entries: list = []
    seen: set = set()
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            t = line.strip()
            if not t or t.startswith("#"):
                continue
            c = clean_token(t.rstrip(_TRAIL))
            if not c:
                continue
            n = normalize(c)
            if n in seen:
                continue
            seen.add(n)
            if c.endswith("/") or (ESTATE_ROOT / n).is_dir():
                c = c.rstrip("/") + "/"
            entries.append(c)
    return entries


def resolves(clean: str, doc_dir: Path) -> bool:
    """Does the cite land on disk? Repo-root-relative, doc-dir-relative, or
    absolute. Directories count (a dir cite is testable for membership)."""
    n = normalize(clean)
    cands = [ESTATE_ROOT / n, doc_dir / n]
    if re.match(r"^[A-Za-z]:/", n) or n.startswith("/"):
        cands.append(Path(clean.replace("\\", "/")))
    for c in cands:
        try:
            if c.is_file() or c.is_dir():
                return True
        except OSError:
            continue
    return False


def is_allowed(clean: str, entries: list) -> bool:
    """Membership: exact normalized match, or under an allowlisted directory."""
    n = normalize(clean)
    for e in entries:
        ne = normalize(e)
        if ne.endswith("/"):
            if n.startswith(ne):
                return True
        elif n == ne:
            return True
    return False


def nearest_allowed(clean: str, entries: list):
    """Nearest allowlist entry for a finding: exact-basename match first, then
    difflib close match; None when the allowlist offers no neighbor."""
    n = normalize(clean)
    base = n.rsplit("/", 1)[-1]
    stems = [(normalize(e).rstrip("/"), e) for e in entries]
    for stem, e in stems:
        if stem.rsplit("/", 1)[-1] == base:
            return e
    close = difflib.get_close_matches(n, [s for s, _ in stems], n=1, cutoff=0.6)
    if close:
        for stem, e in stems:
            if stem == close[0]:
                return e
    return None


def extract_cited_paths(text: str) -> list:
    """Directory-anchored path cites, deduped by normalized path, ordered by
    first doc line then path. Bare filenames are mentions and skipped."""
    found: dict = {}
    for lineno, line in enumerate(text.splitlines(), 1):
        for m in PATH_RE.finditer(line):
            c = clean_token(m.group(0))
            if "/" not in c and "\\" not in c:
                continue  # bare filename: a mention, not a load-bearing cite
            n = normalize(c)
            if n and n not in found:
                found[n] = {"cited": c, "doc_line": lineno}
    return sorted(found.values(), key=lambda r: (r["doc_line"], r["cited"]))


def check_doc(doc, allowlist) -> dict:
    """The gate. Returns one verdict row; ok is True iff zero findings.

    Integration (one line, fold / receipt verification paths):
        from tools.cite_allowlist import check_doc
        ok = check_doc(doc_path, allowlist_path)["ok"]
    """
    doc_p = Path(doc)
    text = doc_p.read_text(encoding="utf-8", errors="replace")
    entries = load_allowlist(allowlist)
    findings: list = []
    cites = extract_cited_paths(text)
    for c in cites:
        if not resolves(c["cited"], doc_p.parent):
            findings.append({"cited": c["cited"], "verdict": "PATH-MISSING",
                             "nearest": None, "doc_line": c["doc_line"]})
        elif not is_allowed(c["cited"], entries):
            findings.append({"cited": c["cited"], "verdict": "CITE-OUTSIDE-ALLOWLIST",
                             "nearest": nearest_allowed(c["cited"], entries),
                             "doc_line": c["doc_line"]})

    def _rel(p) -> str:
        try:
            return p.resolve().relative_to(ESTATE_ROOT).as_posix()
        except ValueError:
            return Path(p).as_posix()

    return {
        "tool": TOOL,
        "doc": _rel(doc_p),
        "allowlist": _rel(Path(allowlist)),
        "cites_checked": len(cites),
        "allowlist_entries": len(entries),
        "findings": findings,
        "ok": not findings,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="cite_allowlist",
                                 description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    chk = sub.add_parser("check", help="gate one document against one allowlist")
    chk.add_argument("--doc", required=True, help="the produced document to gate")
    chk.add_argument("--allowlist", required=True,
                     help="file with one allowed source path per line")
    chk.add_argument("--json", action="store_true", help="emit the verdict row as JSON")
    args = ap.parse_args(argv)

    try:
        row = check_doc(args.doc, args.allowlist)
    except OSError as exc:
        print(f"{TOOL}: ERROR cannot verify: {exc}")
        return 2

    if args.json:
        print(json.dumps(row, indent=2))
        return 0 if row["ok"] else 1

    if row["ok"]:
        print(f"{TOOL}: ok ({row['cites_checked']} cites checked, "
              f"{row['allowlist_entries']} allowlist entries)")
        return 0
    print(f"{TOOL}: FAIL ({len(row['findings'])} findings over "
          f"{row['cites_checked']} cites)")
    for f in row["findings"]:
        near = f"  nearest: {f['nearest']}" if f["nearest"] else ""
        print(f"  [!] {f['verdict']} {f['cited']} (doc line {f['doc_line']}){near}")
    print("  remediation: mark the work OWED with a receipt, or read the file "
          "into the ask's input set")
    return 1


if __name__ == "__main__":
    sys.exit(main())
