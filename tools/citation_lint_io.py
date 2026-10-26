"""citation_lint_io -- base layer for the citation lint (a05-r2, 2026-10-01).

Finding/LintResult types, the shared cite-path grammar, path resolution,
streamed source reads, the changed-record discovery, and the accept-by-name
baseline loader. Split from tools/citation_lint.py for the ratchet's
400-line cap; the seams are the real layers: this module knows nothing
about anchors or numbers beyond the grammar.

Spec: watch/inbox/ractor50/accuracy.md incident 5 + GAP_REGISTER rank 3.
Receipt: watch/inbox/fillball/citation-lint.md
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

TOOL = "CITATION-LINT"
ESTATE_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASELINE = ESTATE_ROOT / "configs" / "citation_lint_baseline.json"
# Records read whole; anything bigger is a data file, not a prose record.
MAX_RECORD_BYTES = 64 * 1024 * 1024
# Named sources bigger than this are data surfaces (the live estate carries a
# 2.5GB dashboard/data/ESTATE_INDEX.jsonl and a 356MB training/events.jsonl);
# containment against them is unverifiable at push-gate cost, so a number
# cannot be called phantom while one of its sources is oversize.
MAX_SOURCE_BYTES = 256 * 1024 * 1024
# Sources up to this size are read once into the per-run text cache.
CACHE_SOURCE_BYTES = 16 * 1024 * 1024
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0

# Prose record surfaces the --changed scan reads: doctrine, receipts, run
# stories. Data surfaces (.jsonl catalogs, .json indexes) are the census
# patrol's class (B2-216): their rows are structured size+path pairs, not
# consumed prose claims, and whole-row lines make token pairing meaningless.
# Explicit --files runs accept the wider set for targeted lane work.
RECORD_SUFFIXES = {".md", ".txt", ".rst"}
FILE_SUFFIXES = {".md", ".txt", ".rst", ".jsonl", ".json"}
# Phantom-number sources are RECORDS (digests, receipts, ledgers): the class
# the register names is "its named source has zero '191' hits", where the
# source is a compiled payload document. Code paths co-sentential with a
# number serve anchor roles, not attribution roles, and never contain prose
# totals; pairing against them manufactured thousands of false fires on
# number-dense fold docs.
RECORD_SOURCE_SUFFIXES = {".md", ".txt", ".rst", ".jsonl", ".json"}

BLOCKING_RULES = {"PATH-MISSING", "LINE-OOB", "EMPTY-SPAN", "PHANTOM-NUMBER"}
# Warn-only classes (never block without --enforce-tokens):
#   TOKEN-MISS: the spec clause (b) token match is heuristic.
#   SHORTHAND-UNRESOLVED: a bare-basename anchor (no directory separator)
#   that resolves nowhere deterministically; the a05 lane verified cites like
#   "SKILL.md:26-29" and "ladder-02.md:73" clean by sibling context, which no
#   static resolver can see. Pathed cites that fail to resolve stay blocking
#   (the f-25 wrong-path class).
#   UNRESOLVED-SOURCE: a notable number whose sentence names ONLY record
#   sources that resolve nowhere (ouroboros R3 move 5, 2026-10-05: the 900M
#   probe line passed exit 0, so the founding 191.8M class survived one
#   dead-path citation; warn tier because unresolved is unverifiable, not
#   proven phantom).
WARN_RULES = {"TOKEN-MISS", "SHORTHAND-UNRESOLVED", "RECORD-UNREADABLE",
              "UNRESOLVED-SOURCE"}

# Code/doctrine files a citation may point at (anchor existence targets and
# the path-token grammar). Anything else after the colon is not an anchor.
CITE_SUFFIXES = (
    "py|md|txt|jsonl|json|ts|mjs|js|ps1|sh|cmd|bat|yaml|yml|toml|cfg|ini|csv|rst|gd|lua"
)

# Path grammar carries NO space: "SEE FILE x.md:12" must anchor on x.md, not
# on the prose word before it. The leading class includes "." so dotfiles
# anchor (.gitignore:198); digits-only suffix guards keep prose ellipses out.
ANCHOR_RE = re.compile(
    r"(?P<path>(?:[A-Za-z]:[\\/])?[\w\-.][\w\-.\\/]*?\.(?:%s)):(?P<start>\d{1,5})(?:-(?P<end>\d{1,5}))?"
    % CITE_SUFFIXES
)
PATH_RE = re.compile(
    r"(?:[A-Za-z]:[\\/])?[\w\-.][\w\-.\\/]*?\.(?:%s)" % CITE_SUFFIXES
)


def rel_path(record: Path) -> str:
    """Record path relative to the estate root when inside it, else as-given."""
    try:
        return record.resolve().relative_to(ESTATE_ROOT).as_posix()
    except ValueError:
        return record.as_posix()

_RESOLVE_CACHE: dict[tuple, object] = {}
_CONTAINS_CACHE: dict[tuple, bool] = {}
_SOURCE_TEXT_CACHE: dict[str, str | None] = {}


@dataclass
class Finding:
    rule: str
    record: str
    line: int
    anchor: str
    detail: str

    @property
    def blocking(self) -> bool:
        return self.rule in BLOCKING_RULES

    @property
    def is_warn(self) -> bool:
        return self.rule in WARN_RULES

    def fingerprint(self) -> str:
        raw = f"{self.rule}|{self.record}|{self.anchor}|{self.detail[:80]}"
        return hashlib.sha1(raw.encode("utf-8", "replace")).hexdigest()[:16]

    def render(self) -> str:
        # Detail names line spans in prose form ("lines N-M"), never the
        # colon-digit anchor form, so saved gate output does not re-arm the
        # lint when the output itself lands in a scanned record.
        return f"{self.record}:{self.line} {self.rule} {self.anchor} {self.detail}"


@dataclass
class LintResult:
    records: int = 0
    anchors: int = 0
    numbers: int = 0
    findings: list = field(default_factory=list)
    warns: list = field(default_factory=list)

    @property
    def blocking(self) -> list:
        return [f for f in self.findings if f.blocking]


def norm_seps(path: str) -> str:
    """Normalize a cited path: collapse JSONL backslash escapes and win seps.

    Trailing punctuation only (a prose comma or close-quote after the path);
    leading dots are path content (.agents/...) and must survive.
    """
    p = path.replace("\\\\", "\x00").replace("\\", "/").replace("\x00", "\\")
    return p.strip().rstrip("\"'`),.;")


_LSFILES_CACHE: dict[str, list[str]] = {}


def _git_ls_files(pattern: str) -> list[str]:
    """git ls-files (tracked + untracked) for a basename glob, cached per run."""
    if pattern not in _LSFILES_CACHE:
        out: list[str] = []
        for extra in ([], ["--others", "--exclude-standard"]):
            try:
                r = subprocess.run(
                    ["git", "ls-files", *extra, "--", pattern],
                    cwd=str(ESTATE_ROOT), capture_output=True, text=True,
                    timeout=30, creationflags=HEADLESS,
                )
                # git failure leaves the pattern unresolved, never blocking:
                # ambiguous resolution is the warn class, not a gate error
                if r.returncode == 0:
                    out.extend(r.stdout.splitlines())
            except (OSError, subprocess.TimeoutExpired) as exc:
                print(f"{TOOL}: WARN ls-files unavailable for {pattern}: {exc}")
        _LSFILES_CACHE[pattern] = sorted(set(out))
    return _LSFILES_CACHE[pattern]


def resolve_path(raw: str, record: Path) -> Path | None:
    """Resolve a cited path as-given, repo-root relative, or beside the record.

    Fallback for unresolved paths: a single basename hit in the git index
    (tracked + untracked). Window-relative cite forms like
    "flash50/ladder-02.md" (the a05 lane's verified form, real file under
    watch/inbox/burn_reset_20260927/) resolve this way; zero or multiple
    hits stay unresolved (ambiguous is not deterministic, so it never blocks).
    Results cached per (raw path, record dir): jsonl records repeat the same
    cite strings across hundreds of rows.
    """
    cache_key = (raw, str(record.parent))
    if cache_key in _RESOLVE_CACHE:
        return _RESOLVE_CACHE[cache_key]
    p = norm_seps(raw)
    cands = []
    if Path(p).is_absolute() or (len(p) > 1 and p[1] == ":"):
        cands.append(Path(p))
    else:
        cands.append(ESTATE_ROOT / p)
        cands.append(record.parent / p)
        try:
            rel_parent = record.parent.resolve().relative_to(ESTATE_ROOT)
        except ValueError:
            rel_parent = None
        if rel_parent is not None:
            for anc in list(rel_parent.parents)[:-1]:
                cands.append(ESTATE_ROOT / anc / p)
    for c in cands:
        try:
            if c.is_file():
                _RESOLVE_CACHE[cache_key] = c
                return c
        except OSError:
            continue
    base = p.rsplit("/", 1)[-1]
    resolved: Path | None = None
    if base:
        hits = _git_ls_files(f"*{base}")
        if len(hits) == 1:
            cand = ESTATE_ROOT / hits[0]
            try:
                resolved = cand if cand.is_file() else None
            except OSError as exc:
                # an unreadable index hit is unresolved, never a gate error
                print(f"{TOOL}: WARN index hit unreadable {cand}: {exc}")
                resolved = None
    _RESOLVE_CACHE[cache_key] = resolved
    return resolved


def read_lines(path: Path) -> list[str] | None:
    """Read a record whole; None when unreadable or oversize.

    Named SOURCES are never read whole (see MAX_SOURCE_BYTES): sources use
    file_line_count / read_span / file_contains, all streaming.
    """
    try:
        if path.stat().st_size > MAX_RECORD_BYTES:
            return None
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    return text.splitlines()


def file_line_count(path: Path) -> int | None:
    try:
        with open(path, "rb") as fh:
            count = 0
            last = b""
            while True:
                chunk = fh.read(4 * 1024 * 1024)
                if not chunk:
                    break
                count += chunk.count(b"\n")
                last = chunk[-1:]
            if last not in (b"", b"\n"):
                count += 1
            return count
    except OSError:
        return None


def read_span(path: Path, start: int, end: int) -> str | None:
    """Stream lines start..end (1-based, inclusive) without loading the file."""
    try:
        out = []
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for i, line in enumerate(fh, 1):
                if i >= start:
                    out.append(line.rstrip("\r\n"))
                if i >= end:
                    break
        return "\n".join(out)
    except OSError:
        return None


def _source_text(path: Path) -> str | None:
    """One read per source per run; None when unreadable."""
    key = str(path)
    if key not in _SOURCE_TEXT_CACHE:
        try:
            _SOURCE_TEXT_CACHE[key] = path.read_text(
                encoding="utf-8", errors="replace"
            )
        except OSError:
            _SOURCE_TEXT_CACHE[key] = None
    return _SOURCE_TEXT_CACHE[key]


def file_contains(path: Path, forms: list[str]) -> bool | None:
    """Case-insensitive containment with carry-safe chunking for big files.

    Returns None when the source is oversize (containment unverifiable at
    gate cost); the caller must then NOT call a number phantom. Sources up
    to CACHE_SOURCE_BYTES are read once into the per-run text cache.
    """
    try:
        size = path.stat().st_size
        if size > MAX_SOURCE_BYTES:
            return None
    except OSError:
        return False
    key = (str(path), tuple(forms))
    if key in _CONTAINS_CACHE:
        return _CONTAINS_CACHE[key]
    try:
        if size <= CACHE_SOURCE_BYTES:
            text = _source_text(path)
            if text is None:
                return False
            low = text.lower()
            found = any(f in low for f in forms) or any(
                f.replace(",", "") in low.replace(",", "") for f in forms
            )
            _CONTAINS_CACHE[key] = found
            return found
        carry = ""
        max_len = max(len(f) for f in forms)
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            while True:
                chunk = fh.read(4 * 1024 * 1024)
                if not chunk:
                    _CONTAINS_CACHE[key] = False
                    return False
                hay = (carry + chunk).lower()
                if any(f in hay for f in forms):
                    _CONTAINS_CACHE[key] = True
                    return True
                carry = hay[-(max_len - 1):] if max_len > 1 else ""
    except OSError:
        return False


def changed_records() -> list[Path] | None:
    """Changed prose records vs HEAD (staged + unstaged, the push content).

    The ratchet also scans untracked files (catch half-done work); this gate
    does NOT: untracked files are not push content, and concurrent lanes
    keep untracked work surfaces on this one tree (measured at landing:
    two sibling rebuild_live*.txt logs carried 3,711 of 3,805 fires). A
    staged-new receipt IS covered: `git diff HEAD` includes staged adds.
    Saved instrument output (*.check.txt, *.extract.txt) is evidence cited
    BY records, not an authored record making claims, and is skipped.
    """
    try:
        diff = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=str(ESTATE_ROOT), capture_output=True, text=True, timeout=60,
            creationflags=HEADLESS,
        )
        if diff.returncode != 0:
            return None
    except (OSError, subprocess.TimeoutExpired):
        return None
    out = []
    for line in diff.stdout.splitlines():
        rel = line.strip().replace("\\", "/")
        if Path(rel).suffix.lower() not in RECORD_SUFFIXES:
            continue
        if rel.endswith(".check.txt") or rel.endswith(".extract.txt"):
            continue
        out.append(ESTATE_ROOT / rel)
    return sorted(set(out))


def load_baseline(path: Path | None) -> dict:
    if path is None or not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data.get("accepted", {}) if isinstance(data, dict) else {}
