"""citation_lint -- byte-check citations and numbers in changed records (a05-r2).

Spec chain: watch/inbox/ractor50/accuracy.md incident 5 ("Instrument upgrade:
a citation linter runs at filing time ... every file:line citation in a
doctrine/receipt under corpus/steal/ must satisfy (a) the path exists, (b) the
line range is non-empty and mentions a token from the claim") and
watch/inbox/gap_analysis_20261001/GAP_REGISTER.md rank 3 + fill spec 3 ("Build
tools/citation_lint.py exactly to the accuracy.md spec ..., wire one line into
githooks/pre-push after the ratchet, run it once over ractor50's 12
spot-checked cites to prove it catches the 2 known drifts
(mag/mcp_server.py:338-340, mag/biography.py:526)"). Founding fixture: the
191.8M phantom (STORY.md:240 stated 191.8M tokens; its named source
watch/inbox/frontier_olm_20260928/DIGEST.md carries zero "191" hits). The
errata that struck the clause landed 2026-10-01, so the founding paragraph
lives verbatim in tests/test_citation_lint.py, never read live from STORY.md.

Finding classes and certainty:
  PATH-MISSING     anchored cite path:NN whose path does not resolve.
                   Deterministic (f-25's wrong-path class).
  LINE-OOB         anchored cite whose end line is past the file's last line.
                   Deterministic.
  EMPTY-SPAN       cited line range is all whitespace. Deterministic.
  PHANTOM-NUMBER   a notable quantity appears in NONE of its sentence's
                   named record sources (the 191.8M class). Deterministic
                   against the named bytes; engine in citation_lint_numbers.
  UNRESOLVED-SOURCE  a notable quantity whose sentence names only record
                   sources that resolve nowhere (R3 move 5: the 900M probe
                   passed exit 0; the 191.8M class survives one dead-path
                   citation). WARN; engine in citation_lint_numbers.
  TOKEN-MISS       the cited span mentions none of the claim line's tokens.
                   Heuristic: WARN by default, blocking via --enforce-tokens.
  SHORTHAND-UNRESOLVED  bare-basename anchor with no deterministic hit. Warn.

Scope: --changed (staged + unstaged prose records vs HEAD; the same
discipline as tools/violation_ratchet.py, minus untracked files, which are
not push content and include sibling lanes' work surfaces on this shared
tree) or --files (explicit list, wider suffix set). One is required; with
neither the tool cannot know the scope and exits 2 (cannot verify).

Exit contract: 0 = no blocking findings, 1 = blocking findings,
2 = cannot verify (git broke, bad args, unreadable record). Output contract
(B2-338 first-line law): green opens "CITATION-LINT: ok", blocking
"CITATION-LINT: FAIL", cannot-verify "CITATION-LINT: ERROR"; never widen.

Baseline: --baseline PATH (default configs/citation_lint_baseline.json when
present) accepts a finding by fingerprint, the accept-debt-by-NAME law.
Modules: citation_lint_io (types/grammar/resolution/reads) and
citation_lint_numbers (the phantom engine).

CLI:
  python tools/citation_lint.py check --changed
  python tools/citation_lint.py check --files A.md B.md [--enforce-tokens]
  python tools/citation_lint.py --selftest   # runs the pytest battery
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

try:
    from tools.citation_lint_io import (
        ANCHOR_RE,
        DEFAULT_BASELINE,
        ESTATE_ROOT,
        FILE_SUFFIXES,
        Finding,
        LintResult,
        RECORD_SUFFIXES,
        TOOL,
        WARN_RULES,
        changed_records,
        file_line_count,
        load_baseline,
        norm_seps,
        read_lines,
        read_span,
        rel_path,
        resolve_path,
    )
except ImportError:  # script invocation: tools/ is sys.path[0]
    from citation_lint_io import (
        ANCHOR_RE,
        DEFAULT_BASELINE,
        ESTATE_ROOT,
        FILE_SUFFIXES,
        Finding,
        LintResult,
        RECORD_SUFFIXES,
        TOOL,
        WARN_RULES,
        changed_records,
        file_line_count,
        load_baseline,
        norm_seps,
        read_lines,
        read_span,
        rel_path,
        resolve_path,
    )

try:
    from tools.citation_lint_numbers import check_phantom_numbers
except ImportError:  # script invocation: tools/ is sys.path[0]
    from citation_lint_numbers import check_phantom_numbers

WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")
# Tokens too generic to certify a claim-span match (kept minimal and honest).
STOPWORDS = {
    "this", "that", "with", "from", "have", "been", "were", "their", "which",
    "there", "these", "those", "still", "only", "must", "line", "file", "code",
    "cites", "cited", "cite", "also", "into", "over", "than", "then", "when",
    "what", "where", "says", "said", "same", "both", "each", "more", "most",
    "some", "such", "they", "them", "upon", "about", "after", "before",
    "under", "while",
}


def claim_tokens(claim_line: str, path: str, start: str, end: str | None) -> set[str]:
    """Tokens from the claim line that may certify the cited span.

    Word tokens are >=4 chars, lowercased, minus stopwords and minus anything
    that is a substring of the cited path itself (path words cannot vouch for
    their own span). Number tokens are comma-stripped digits minus the anchor
    line numbers. One hit anywhere in the span satisfies spec clause (b).
    """
    toks: set[str] = set()
    for w in WORD_RE.findall(claim_line):
        wl = w.lower()
        if wl in STOPWORDS or wl in path.lower():
            continue
        toks.add(wl)
    num_re = re.compile(r"\d[\d,]*(?:\.\d+)?")
    for n in num_re.findall(claim_line):
        num = n.replace(",", "").strip()
        if not num:
            continue
        if num == start or num == (end or "") or num in norm_seps(path):
            continue
        toks.add(num)
    return toks


def _line_of(record_lines: list[str], match: re.Match) -> int:
    """1-based record line of a match offset (record_lines from splitlines)."""
    return match.string[: match.start(0)].count("\n") + 1


def check_anchor(match: re.Match, record: Path, record_lines: list[str]) -> Finding | None:
    """Spec clauses (a) path exists, (b) line range non-empty + claim token."""
    path_raw = match.group("path")
    start = int(match.group("start"))
    end = int(match.group("end") or match.group("start"))
    resolved = resolve_path(path_raw, record)
    if resolved is None:
        pathed = ("/" in path_raw or "\\" in path_raw or ":" in path_raw[:-2])
        rule = "PATH-MISSING" if pathed else "SHORTHAND-UNRESOLVED"
        reason = (
            "cited path does not resolve on disk" if pathed
            else "bare-basename anchor resolves nowhere deterministically"
        )
        return Finding(rule, rel_path(record), _line_of(record_lines, match), path_raw, reason)
    total = file_line_count(resolved)
    if total is None:
        return Finding(
            "PATH-MISSING", rel_path(record), _line_of(record_lines, match),
            path_raw, "cited path exists but is unreadable",
        )
    if start > total or end > total:
        return Finding(
            "LINE-OOB", rel_path(record), _line_of(record_lines, match),
            path_raw,
            f"cited lines {start}-{end} run past the file's last line {total}",
        )
    span = read_span(resolved, start, end) or ""
    if not span.strip():
        return Finding(
            "EMPTY-SPAN", rel_path(record), _line_of(record_lines, match),
            path_raw, f"cited lines {start}-{end} are blank (line range empty)",
        )
    line_idx = _line_of(record_lines, match)
    claim = record_lines[line_idx - 1] if 0 < line_idx <= len(record_lines) else ""
    toks = claim_tokens(claim, path_raw, match.group("start"), match.group("end"))
    if toks:
        span_norm = span.lower()
        span_commas = span_norm.replace(",", "")
        hit = next(
            (t for t in toks if t in span_norm or ("," in t and t.replace(",", "") in span_commas)),
            None,
        )
        if hit is None:
            return Finding(
                "TOKEN-MISS", rel_path(record), line_idx,
                path_raw,
                f"cited lines {start}-{end} mention none of the claim tokens "
                f"({', '.join(sorted(toks)[:6])})",
            )
    return None


def lint_record(record: Path, result: LintResult, root: Path) -> None:
    """Scan one record: every anchored cite, then the phantom-number engine."""
    record_lines = read_lines(record)
    if record_lines is None:
        result.findings.append(
            Finding("RECORD-UNREADABLE", rel_path(record), 1, "-", "record could not be read")
        )
        return
    result.records += 1
    text = "\n".join(record_lines)
    for m in ANCHOR_RE.finditer(text):
        result.anchors += 1
        f = check_anchor(m, record, record_lines)
        if f is not None:
            result.findings.append(f)
    check_phantom_numbers(record, record_lines, result)


def run(records: list[Path], enforce_tokens: bool, baseline: dict) -> LintResult:
    result = LintResult()
    for rec in records:
        lint_record(rec, result, ESTATE_ROOT)
    # dedupe: one finding per (rule, record, line, anchor)
    seen = set()
    deduped = []
    for f in result.findings:
        key = (f.rule, f.record, f.line, f.anchor)
        if key not in seen:
            seen.add(key)
            deduped.append(f)
    result.findings = deduped
    # baseline accepts a finding by fingerprint, the ratchet's law
    result.findings = [f for f in result.findings if f.fingerprint() not in baseline]
    result.warns = [f for f in result.findings if f.is_warn]
    if not enforce_tokens:
        # warn classes are heuristic: WARN by default, blocking under the flag
        result.findings = [f for f in result.findings if not f.is_warn]
    return result


def cmd_check(records: list[Path], enforce_tokens: bool, baseline_path: Path | None) -> int:
    baseline = load_baseline(baseline_path)
    result = run(records, enforce_tokens, baseline)
    blocking = result.blocking
    if blocking:
        print(
            f"{TOOL}: FAIL records={result.records} anchors={result.anchors} "
            f"numbers-checked={result.numbers} blocking={len(blocking)} "
            f"warns={len(result.warns)} enforce-tokens={enforce_tokens}"
        )
        for f in blocking:
            print(f"  {f.render()}")
        for f in result.warns:
            print(f"  WARN {f.render()}")
        print(
            f"{TOOL}: fix the citation or downgrade the claim before landing "
            f"(accuracy.md incident 5), or accept by name via --baseline"
        )
        return 1
    print(
        f"{TOOL}: ok records={result.records} anchors={result.anchors} "
        f"numbers-checked={result.numbers} blocking=0 "
        f"warns={len(result.warns)} enforce-tokens={enforce_tokens}"
    )
    for f in result.warns:
        print(f"  WARN {f.render()}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="citation_lint", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd")
    ck = sub.add_parser("check", help="lint records for phantom citations")
    scope = ck.add_mutually_exclusive_group(required=True)
    scope.add_argument("--changed", action="store_true", help="changed prose records vs HEAD")
    scope.add_argument("--files", nargs="+", help="explicit record paths")
    ck.add_argument(
        "--enforce-tokens", action="store_true",
        help="TOKEN-MISS blocks (heuristic class; default is WARN)",
    )
    ck.add_argument("--baseline", default=None, help="baseline JSON (accept by name)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv[1:])

    if args.selftest:
        # the battery lives in tests/test_citation_lint.py (fixtures are test
        # material; tests/ sits outside the ratchet's scan roots). Run it
        # in-process: a nested pytest subprocess lost its output and exit
        # code through two capture layers on landing hardware. The env guard
        # stops the inner battery test from re-running the battery.
        import os

        try:
            import pytest
        except ImportError:
            print(f"{TOOL}: ERROR pytest unavailable, cannot run the battery")
            return 2
        os.environ["CITATION_LINT_SELFTEST"] = "1"
        try:
            rc = pytest.main([
                str(ESTATE_ROOT / "tests" / "test_citation_lint.py"),
                "-q", "-p", "no:cacheprovider",
            ])
        finally:
            os.environ.pop("CITATION_LINT_SELFTEST", None)
        return int(rc)
    if args.cmd != "check":
        ap.print_help()
        return 2
    baseline_path = Path(args.baseline) if args.baseline else (
        DEFAULT_BASELINE if DEFAULT_BASELINE.is_file() else None
    )
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
                p = (ESTATE_ROOT / f).resolve()
            if p.suffix.lower() not in FILE_SUFFIXES:
                print(f"{TOOL}: ERROR not a record suffix: {f}")
                return 2
            if not p.is_file():
                print(f"{TOOL}: ERROR record not found: {f}")
                return 2
            records.append(p)
    return cmd_check(records, args.enforce_tokens, baseline_path)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
