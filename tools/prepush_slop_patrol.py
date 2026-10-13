#!/usr/bin/env python3
"""prepush_slop_patrol.py - deterministic AI-slop detector over prose (2026-10-07).

Spec: watch/inbox/NO_SLOP_STEAL_20261007.md (the steal of
petergyang/no-ai-slop, MIT, operator GO 2026-10-05 "Love it brother... lets
tighten up yes"). This tool is the REGEXABLE SUBSET of that skill's pattern
set; the skill (.agents/skills/no-slop/SKILL.md) stays the judgment layer for
everything that resists a word list (voice, cadence, robotic rhythm). No
model calls anywhere: every class below is a plain regex over bytes.

Finding classes (all WARN, all case-insensitive):
  BANNED-WORD     the operator's list in BANNED_WORDS below, word-boundary.
                  Fenced code blocks and inline backtick spans are exempt
                  (quoting a banned word as an example is the skill's own
                  sanctioned move).
  BINARY-CONTRAST the not-just-X-but-Y / it's-not-X-it's-Y (cross-sentence
                  form included) / the-question-isn't-X shapes.
  THROAT-CLEAR    the five openers in THROAT_CLEAR_RES below.
  COLON-REVEAL    noun-phrase colon lowercase dramatic reveal, approximated
                  by STRUCTURE and honestly heuristic: letters-only prefix
                  of 2+ words (a single-word label like "Spec:" is a
                  legitimate estate row, never a reveal), ": ", then a
                  lowercase clause of 8+ chars with a space, on a prose
                  line (never a heading, list item, table row, fence, or
                  URL). Expect noise; accept by fingerprint.
  FAKE-PROFOUND   the future-is-already-here and whole-thing kickers.

ALL classes are WARN: the tool exits 1 when fresh findings exist but the
githooks/pre-push block never propagates the exit (t40/B2-215 census-tripwire
precedent: no lockouts without operator). Zero baseline day one
(configs/prepush_slop_baseline.json, absent = zero accepted): accept a
finding by FINGERPRINT after triage, never mass-import (the accept-by-NAME
law; fingerprint = class + file + offending line text, so a line shift never
resurrects accepted debt and editing the line re-opens triage).

Scope: --changed (staged + unstaged .md/.txt/.rst vs HEAD, the
citation_lint discipline: untracked files are not push content and data
.jsonl/.json are the census patrol's class) or --files (explicit paths; a
.jsonl handed over explicitly is scanned by TITLE FIELD only, the LINKS
audit shape). One of the two is required; exit 2 = cannot verify.

Output contract (B2-338 first-line law): green opens "SLOP-PATROL: ok",
findings open "SLOP-PATROL: WARN", cannot-verify opens "SLOP-PATROL:
ERROR"; never widen. A "by class:" tail carries per-class counts so audits
can bank numbers without re-parsing rows.

CLI: check --changed | check --files A.md B.jsonl (see argparse help).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

TOOL = "SLOP-PATROL"
ESTATE_ROOT = Path(__file__).resolve().parent.parent
# main() re-resolves RELATIVE --baseline/--files against the repo root (the
# workflow_metadata tmp-root-test precedent).
DEFAULT_BASELINE = ESTATE_ROOT / "configs/prepush_slop_baseline.json"
PROSE_SUFFIXES = {".md", ".txt", ".rst"}
JSONL_SUFFIX = ".jsonl"
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0)

# --- pattern tables (compiled once; all matching is case-insensitive) ------

BANNED_WORDS = [
    "delve", "foster", "leverage", "utilize", "facilitate", "empower",
    "streamline", "robust", "cutting-edge", "paradigm shift", "game changer",
    "tapestry", "realm", "beacon", "multifaceted", "meticulous", "paramount",
    "transformative", "elevate", "embark", "supercharge", "ever-evolving",
    "this is huge", "this changes everything",
]

BANNED_WORD_RES = [
    (re.compile(rf"\b{re.escape(w)}\b", re.IGNORECASE), w) for w in BANNED_WORDS
]

BINARY_CONTRAST_RES = [
    # "not just X but Y" / "not just X, but Y", same sentence
    (re.compile(r"\bnot just\b[^.!?\n]{0,120}?\bbut\b", re.IGNORECASE),
     "not just X but Y"),
    # "it's not X, it's Y" AND the cross-sentence "It's not X. It's Y."
    # (the skill names that shape; window 80, line-local)
    (re.compile(
        r"\b(?:it|this)(?:'s| is) not\b[^#\n]{0,80}?\b(?:it|this)(?:'s| is)\b",
        re.IGNORECASE),
     "it's not X, it's Y"),
    # "the question isn't X" / "the question is not X"
    (re.compile(r"\bthe question (?:isn'?t|is not)\b", re.IGNORECASE),
     "the question isn't X"),
]

THROAT_CLEAR_RES = [
    (re.compile(r"here'?s the thing", re.IGNORECASE), "here's the thing"),
    (re.compile(r"let me be clear", re.IGNORECASE), "let me be clear"),
    (re.compile(r"the uncomfortable truth", re.IGNORECASE),
     "the uncomfortable truth"),
    (re.compile(r"what nobody tells you", re.IGNORECASE),
     "what nobody tells you"),
    (re.compile(r"the part everyone misses", re.IGNORECASE),
     "the part everyone misses"),
]

FAKE_PROFOUND_RES = [
    # cross-sentence-tolerant (the canonical kicker is "The future isn't
    # coming. It's already here."; window 20, line-local)
    (re.compile(
        r"the future (?:isn'?t|is not) coming[^#\n]{0,20}?already here",
        re.IGNORECASE),
     "the future isn't coming, it's already here"),
    # "That's it. That's the whole thing." / comma variant
    (re.compile(
        r"that'?s it[^#\n]{0,10}?that'?s the whole thing", re.IGNORECASE),
     "that's it, that's the whole thing"),
]

# COLON-REVEAL, structural approximation (documented heuristic above):
# letters-only phrase of 2+ words, ": ", lowercase clause 8+ chars with a
# space. Single-word prefixes (Spec:, Fix:, Note:) are estate label rows and
# are skipped; digits/backticks/paths in the prefix are skipped.
COLON_REVEAL_RE = re.compile(
    r"^(?P<pre>[A-Za-z][A-Za-z'\u2019 -]{1,59}): (?P<post>[a-z][^:\n]{7,})$"
)
REVEAL_SCHEME_RE = re.compile(r"^(?:https?|ftp)://")
MD_STRUCT_RE = re.compile(r"^\s*(?:[#>*+-]|\d+\.|\||```|~~~)")

BACKTICK_SPAN_RE = re.compile(r"`[^`\n]*`")


def normalize(text: str) -> str:
    """Curly apostrophes fold to straight so 'isn't' regexes match both."""
    return text.replace("\u2019", "'")


def mask_code_spans(text: str) -> str:
    """Blank inline backtick spans (same length) so code quoting is exempt."""
    return BACKTICK_SPAN_RE.sub(lambda m: " " * (m.end() - m.start()), text)


def scan_line_classes(norm: str) -> list[tuple[str, str]]:
    """(class, matched-text) hits for one already-normalized, code-masked
    prose line. Deterministic regexes only."""
    hits: list[tuple[str, str]] = []
    for rx, word in BANNED_WORD_RES:
        for m in rx.finditer(norm):
            hits.append(("BANNED-WORD", f"'{m.group(0)}' ({word})"))
    for rx, shape in BINARY_CONTRAST_RES:
        for m in rx.finditer(norm):
            hits.append(("BINARY-CONTRAST", f"{shape}: ...{m.group(0)}..."))
    for rx, phrase in THROAT_CLEAR_RES:
        for m in rx.finditer(norm):
            hits.append(("THROAT-CLEAR", f"{phrase}"))
    for rx, shape in FAKE_PROFOUND_RES:
        for m in rx.finditer(norm):
            hits.append(("FAKE-PROFOUND", f"{shape}: ...{m.group(0)}..."))
    return hits


def colon_reveal_hit(line: str) -> str | None:
    """The structural COLON-REVEAL approximation, or None. Exclusions (each
    a measured estate false-positive class): markdown structure, table
    pipes, URLs after the colon, single-word prefixes (label rows), reveals
    shorter than 8 chars or without a space (values, not clauses)."""
    if MD_STRUCT_RE.match(line):
        return None
    if "|" in line:
        return None
    m = COLON_REVEAL_RE.match(line)
    if m is None:
        return None
    pre, post = m.group("pre").strip(), m.group("post").rstrip()
    if " " not in pre:  # Spec:/Fix:/Note: label rows are not reveals
        return None
    if " " not in post or len(post) < 8:
        return None
    if REVEAL_SCHEME_RE.match(post):
        return None
    return f"colon reveal: {pre}: {post[:50]}"


def scan_text(text: str, rel: str, start_line: int = 1,
              is_markdown: bool = True) -> list[dict]:
    """Findings for one prose text. Fenced regions are exempt in markdown."""
    findings: list[dict] = []
    in_fence = False
    line_no = start_line - 1
    for raw in text.split("\n"):
        line_no += 1
        stripped = raw.rstrip("\r")
        fence_head = stripped.lstrip()[:3]
        if is_markdown and (fence_head.startswith("```")
                            or fence_head.startswith("~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        norm = mask_code_spans(normalize(stripped))
        for name, detail in scan_line_classes(norm):
            findings.append({
                "name": name, "file": rel, "line": line_no,
                "detail": detail, "line_text": stripped.strip(),
            })
        reveal = colon_reveal_hit(stripped.strip())
        if reveal is not None:
            findings.append({
                "name": "COLON-REVEAL", "file": rel, "line": line_no,
                "detail": reveal, "line_text": stripped.strip(),
            })
    return findings


def scan_jsonl_titles(text: str, rel: str) -> tuple[list[dict], int]:
    """(findings, malformed-row count) for the title field of every parseable
    JSONL row (the LINKS audit shape; every other field is data, not prose).
    Malformed rows are counted and named in the head line, never fatal (the
    seal-patrol law)."""
    findings: list[dict] = []
    line_no = 0
    bad = 0
    for raw in text.split("\n"):
        line_no += 1
        line = raw.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except ValueError:
            bad += 1
            continue
        if not isinstance(row, dict):
            bad += 1
            continue
        title = row.get("title")
        if not isinstance(title, str) or not title.strip():
            continue
        for name, detail in scan_line_classes(mask_code_spans(normalize(title))):
            findings.append({
                "name": name, "file": rel, "line": line_no,
                "detail": detail, "line_text": title.strip(),
            })
        # titles are one-liners: the structural reveal needs the whole string
        reveal = colon_reveal_hit(title.strip())
        if reveal is not None:
            findings.append({
                "name": "COLON-REVEAL", "file": rel, "line": line_no,
                "detail": reveal, "line_text": title.strip(),
            })
    return findings, bad


def fingerprint(finding: dict) -> str:
    """Accept-by-NAME identity: class + file + offending line text (line
    numbers excluded so a shift never resurrects debt)."""
    raw = f"{finding['name']}|{finding['file']}|{finding['line_text']}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def scan_file(path: Path, rel: str) -> tuple[list[dict], int]:
    """(findings, malformed-jsonl-rows) for one file."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == JSONL_SUFFIX:
        return scan_jsonl_titles(text, rel)
    return scan_text(text, rel, is_markdown=path.suffix.lower() == ".md"), 0


def changed_records() -> list[Path] | None:
    """Changed prose records vs HEAD (staged + unstaged, the push content;
    citation_lint discipline: no untracked, no data .jsonl)."""
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
        if Path(rel).suffix.lower() not in PROSE_SUFFIXES:
            continue
        p = ESTATE_ROOT / rel
        if p.is_file():
            out.append(p)
    return sorted(set(out))


def load_baseline(path: Path) -> dict:
    if not path.is_file():
        return {"accepted": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"accepted": {}}
    return data if isinstance(data, dict) and "accepted" in data else {"accepted": {}}


def run(files: list[Path], root: Path, baseline_path: Path) -> int:
    accepted = load_baseline(baseline_path).get("accepted", {})
    findings: list[dict] = []
    unreadable: list[str] = []
    bad_rows = 0
    for path in files:
        rel = path.relative_to(root).as_posix() if path.is_relative_to(root) \
            else path.as_posix()
        try:
            rows, bad = scan_file(path, rel)
        except OSError:
            unreadable.append(rel)
            continue
        findings.extend(rows)
        bad_rows += bad
    fresh = [f for f in findings if fingerprint(f) not in accepted]
    classes = ["BANNED-WORD", "BINARY-CONTRAST", "THROAT-CLEAR",
               "COLON-REVEAL", "FAKE-PROFOUND"]
    counts = {c: sum(1 for f in findings if f["name"] == c) for c in classes}
    by_class = " ".join(f"{c}={counts[c]}" for c in classes)
    head = (f"scanned {len(files)} file(s), {len(findings)} finding(s) "
            f"({len(findings) - len(fresh)} accepted by fingerprint)")
    if bad_rows:
        head += f", {bad_rows} malformed jsonl row(s) skipped"
    if unreadable:
        print(f"{TOOL}: ERROR unreadable file(s): {', '.join(unreadable)}")
        return 2
    if not findings or not fresh:
        print(f"{TOOL}: ok - {head}; by class: {by_class}")
        for f in findings:
            print(f"  accepted [{fingerprint(f)}]: {f['name']} "
                  f"{f['file']}:{f['line']} {f['detail']}")
        return 0
    print(f"{TOOL}: WARN - {head}; by class: {by_class}")
    for f in findings:
        if fingerprint(f) in accepted:
            print(f"  accepted [{fingerprint(f)}]: {f['name']} "
                  f"{f['file']}:{f['line']} {f['detail']}")
    for f in fresh:
        print(f"  {f['name']} {f['file']}:{f['line']}: {f['detail']} "
              f"| {f['line_text'][:80]} [fp {fingerprint(f)}]")
    print("  fix: cut the slop per .agents/skills/no-slop/SKILL.md (state Y "
          "directly, drop the setup, end on the concrete point), or accept "
          f"THIS finding by fingerprint into {baseline_path.as_posix()}")
    return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="prepush_slop_patrol",
        description="deterministic AI-slop detector over prose records "
                    "(WARN-only pre-push shape)")
    sub = ap.add_subparsers(dest="cmd")
    ck = sub.add_parser("check", help="scan prose for slop patterns")
    scope = ck.add_mutually_exclusive_group(required=True)
    scope.add_argument("--changed", action="store_true",
                       help="changed prose records vs HEAD (.md/.txt/.rst)")
    scope.add_argument("--files", nargs="+",
                       help="explicit paths (.md/.txt/.rst scanned whole; "
                            ".jsonl scanned by title field)")
    ck.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE,
                    help="accept-by-fingerprint baseline (default: configs/"
                         "prepush_slop_baseline.json; absent = zero)")
    ck.add_argument("--root", type=Path, default=ESTATE_ROOT,
                    help="repo root for relative path resolution")
    args = ap.parse_args(argv)
    if args.cmd != "check":
        ap.print_help()
        return 2
    root = args.root.resolve()
    baseline = args.baseline
    if not baseline.is_absolute():
        baseline = root / baseline
    if args.changed:
        records = changed_records()
        if records is None:
            print(f"{TOOL}: ERROR git failed, refusing to guess the changed set")
            return 2
    else:
        records = []
        for f in args.files:
            p = Path(f)
            if not p.is_absolute():
                p = root / f
            if p.suffix.lower() not in PROSE_SUFFIXES | {JSONL_SUFFIX}:
                print(f"{TOOL}: ERROR not a prose or jsonl suffix: {f}")
                return 2
            if not p.is_file():
                print(f"{TOOL}: ERROR file not found: {f}")
                return 2
            records.append(p)
    return run(records, root, baseline)


if __name__ == "__main__":
    sys.exit(main())
