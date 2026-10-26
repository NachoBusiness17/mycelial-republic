"""publish_recheck -- publish-time re-derivation of line cites (d16, 2026-10-06).

The R5 relay lesson as law: a line cite can be true at write and rotted
minutes later. Founding subject: the dawn report cited
memories/session/next-window-handoff.md for the XAI 403 console check at
line 69; the economics lens's append landed above it and moved the anchor
to line 80 (watch/inbox/DAWN_REPORT_20261006.md, communication amendment,
quoted anchor "XAI 403 console check"; cure banked in
watch/inbox/ouroboros_20261005/r5_land_truth.md section 4, quoted anchors
over line numbers). tools/citation_lint.py checks the cited file only as
it exists at lint time, so a rot AFTER the citing record was written is
invisible to it: the span still exists, is non-empty, the gate goes green
over a cite that no longer points at what the author claimed.

This tool closes that class at publish time: re-read every anchored cite
(path:start-end) in a prose record and compare the cited SOURCE's mtime
against the citing receipt's mtime (the record file's own mtime):

  source mtime <= record mtime   the source has not moved since the
                                 receipt was written, so the cited bytes
                                 cannot have moved. Clean, no finding.
  source mtime >  record mtime   the source moved after the receipt; the
                                 cite is re-derived by re-reading the span
                                 and token-matching it against the claim
                                 line (the same claim_tokens heuristic
                                 citation_lint's TOKEN-MISS uses, applied
                                 against the publish moment):

    ROTTED      blocking. The span mentions none of the claim's tokens,
                the source moved after the receipt, AND the span is not
                byte-identical to its pre-receipt commit (the newest
                commit of the source dated at or before the receipt's
                mtime): the bytes at the cite moved with the source (the
                handoff :69 class). Untracked sources carry no git
                history, so the token refutation stands alone there.
    ROT-STABLE  warn. Token refutation fired but the span is byte-
                identical to its pre-receipt commit: the cited bytes
                provably held across the receipt boundary and the token
                miss predates the receipt (citation_lint's static class).
    ROT-RECHECK warn. The source moved after the receipt and the span
                re-derivation held (still token-hits) or carries no
                testable tokens: re-read the lines before publishing.
    ROT-QUOTED  warn. A would-be ROTTED whose anchor sits inside
                quotation marks: an evidence mention of a rotted cite
                (the dawn report's own account of the handoff rot), not
                a live claim.

Known limits, stated honestly:
  - The receipt's mtime is the record's LAST write. A rot that moved a
    source between two amendments of the same record is invisible to the
    mtime comparison; citation_lint's static TOKEN-MISS warn stays the
    net for that case.
  - mtimes move on git checkout/stash operations; a false ROT-RECHECK
    warn there is noise, never a blocking ROTTED (blocking requires the
    span refutation AND no git proof the span held).
  - The git stability tier reads whole blobs; blobs over MAX_RECORD_BYTES
    are skipped (stability unknowable at gate cost, refutation stands).
  - Unresolved cite paths are citation_lint's class and are skipped here.

Scope: --files (explicit records) or --changed (changed prose records vs
HEAD, the same discovery as citation_lint). Exit contract: 0 = no
blocking findings, 1 = rotted cites, 2 = cannot verify. Output contract
(B2-338 first-line law): green opens "PUBLISH-RECHECK: ok", blocking
"PUBLISH-RECHECK: FAIL", cannot-verify "PUBLISH-RECHECK: ERROR"; never
widen. Baseline: --baseline PATH accepts a finding by fingerprint (the
accept-debt-by-NAME law); default configs/publish_recheck_baseline.json
when present.

CLI:
  python tools/publish_recheck.py check --files A.md B.md   (or --changed)
  python tools/publish_recheck.py --selftest
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from tools.citation_lint import claim_tokens
    from tools.citation_lint_io import (
        ANCHOR_RE,
        ESTATE_ROOT,
        FILE_SUFFIXES,
        Finding,
        HEADLESS,
        MAX_RECORD_BYTES,
        changed_records,
        load_baseline,
        read_lines,
        read_span,
        rel_path,
        resolve_path,
    )
except ImportError:  # script invocation: tools/ is sys.path[0]
    from citation_lint import claim_tokens
    from citation_lint_io import (
        ANCHOR_RE,
        ESTATE_ROOT,
        FILE_SUFFIXES,
        Finding,
        HEADLESS,
        MAX_RECORD_BYTES,
        changed_records,
        load_baseline,
        read_lines,
        read_span,
        rel_path,
        resolve_path,
    )

TOOL = "PUBLISH-RECHECK"
DEFAULT_BASELINE = ESTATE_ROOT / "configs" / "publish_recheck_baseline.json"
ROTTED_RULES = {"ROTTED"}
ROT_WARN_RULES = {"ROT-RECHECK", "ROT-QUOTED", "ROT-STABLE"}
QUOTE_CHARS = {'"', "'", "`"}

_PRE_SHA_CACHE: dict[tuple, str | None] = {}
_SPAN_AT_CACHE: dict[tuple, str | None] = {}


def _line_of(record_lines: list[str], match: re.Match) -> int:
    """1-based record line of a match offset (record_lines from splitlines)."""
    return match.string[: match.start(0)].count("\n") + 1


def _pre_receipt_sha(path_rel: str, rec_mtime: float) -> str | None:
    """Newest commit of path_rel dated at or before the receipt's mtime.

    None when the path has no such commit (untracked, outside the repo,
    created after the receipt) or git failed: stability is then
    unknowable and the token refutation stands.
    """
    when = datetime.fromtimestamp(rec_mtime, tz=timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S +0000"
    )
    key = (path_rel, when)
    if key in _PRE_SHA_CACHE:
        return _PRE_SHA_CACHE[key]
    sha: str | None = None
    try:
        # git log, not rev-list: rev-list rejects --before on this git build
        r = subprocess.run(
            ["git", "log", "-1", f"--before={when}", "--format=%H", "--", path_rel],
            cwd=str(ESTATE_ROOT), capture_output=True, timeout=30,
            creationflags=HEADLESS,
        )
        if r.returncode == 0 and r.stdout.strip():
            sha = r.stdout.decode("utf-8", "replace").strip()
    except (OSError, subprocess.TimeoutExpired):
        sha = None
    _PRE_SHA_CACHE[key] = sha
    return sha


def _span_at(path_rel: str, sha: str, start: int, end: int) -> str | None:
    """Lines start..end of path_rel at commit sha; None when unreadable.

    Blobs over MAX_RECORD_BYTES are skipped: whole-blob reads are gate
    cost the stability tier does not need to pay.
    """
    key = (path_rel, sha, start, end)
    if key in _SPAN_AT_CACHE:
        return _SPAN_AT_CACHE[key]
    span: str | None = None
    try:
        r = subprocess.run(
            ["git", "cat-file", "-s", f"{sha}:{path_rel}"],
            cwd=str(ESTATE_ROOT), capture_output=True, timeout=30,
            creationflags=HEADLESS,
        )
        if r.returncode == 0 and int(r.stdout.strip() or 0) <= MAX_RECORD_BYTES:
            b = subprocess.run(
                ["git", "show", f"{sha}:{path_rel}"],
                cwd=str(ESTATE_ROOT), capture_output=True, timeout=60,
                creationflags=HEADLESS,
            )
            if b.returncode == 0:
                lines = b.stdout.decode("utf-8", "replace").splitlines()
                if 0 < start <= len(lines):
                    span = "\n".join(lines[start - 1:end])
                else:
                    span = ""
    except (OSError, subprocess.TimeoutExpired, ValueError):
        span = None
    _SPAN_AT_CACHE[key] = span
    return span


def span_stable_across_receipt(
    resolved: Path, start: int, end: int, rec_mtime: float
) -> bool | None:
    """True when the span is byte-identical to its pre-receipt commit.

    False means the span differs from that commit (the bytes moved in the
    window the receipt sits in); None means unknowable (no pre-receipt
    commit, git failed, oversize blob). Sources outside the estate root
    resolve to no repo path and return None.
    """
    path_rel = rel_path(resolved)
    sha = _pre_receipt_sha(path_rel, rec_mtime)
    if sha is None:
        return None
    old = _span_at(path_rel, sha, start, end)
    if old is None:
        return None
    return old == (read_span(resolved, start, end) or "")


def check_anchor(
    match: re.Match, record: Path, record_lines: list[str]
) -> Finding | None:
    """Re-derive one anchored cite against the receipt's mtime.

    Unresolved paths and untouched sources return None: the first is
    citation_lint's class, the second cannot rot by definition.
    """
    path_raw = match.group("path")
    start = int(match.group("start"))
    end = int(match.group("end") or match.group("start"))
    resolved = resolve_path(path_raw, record)
    if resolved is None:
        return None
    try:
        rec_mtime = record.stat().st_mtime
        src_mtime = resolved.stat().st_mtime
    except OSError:
        return None
    if src_mtime <= rec_mtime:
        return None
    line_idx = _line_of(record_lines, match)
    claim = record_lines[line_idx - 1] if 0 < line_idx <= len(record_lines) else ""
    toks = claim_tokens(claim, path_raw, match.group("start"), match.group("end"))
    span = read_span(resolved, start, end) or ""
    span_norm = span.lower()
    span_commas = span_norm.replace(",", "")
    hit = next(
        (t for t in toks if t in span_norm or ("," in t and t.replace(",", "") in span_commas)),
        None,
    )
    quoted = match.start() > 0 and match.string[match.start() - 1] in QUOTE_CHARS
    if toks and hit is None:
        stable = None
        if not quoted:
            stable = span_stable_across_receipt(resolved, start, end, rec_mtime)
            if stable is True:
                return Finding(
                    "ROT-STABLE", rel_path(record), line_idx, path_raw,
                    f"cited lines {start}-{end} are byte-identical to the "
                    "pre-receipt commit; the token miss predates the receipt "
                    f"({', '.join(sorted(toks)[:6])}) and is citation_lint's "
                    "static class, not rot",
                )
        rule = "ROT-QUOTED" if quoted else "ROTTED"
        detail = (
            f"source moved after the receipt's mtime and cited lines {start}-{end} "
            f"mention none of the claim tokens ({', '.join(sorted(toks)[:6])}); "
            + (
                "the span also differs from its pre-receipt commit, so the bytes "
                "at the cite moved"
                if stable is False
                else "re-derive the cite before publish (the handoff :69 class)"
            )
        )
        return Finding(rule, rel_path(record), line_idx, path_raw, detail)
    detail = (
        f"source moved after the receipt's mtime; cited lines {start}-{end} "
        "re-derived and still carry the claim (or carry no testable tokens); "
        "re-read before publish"
    )
    return Finding("ROT-RECHECK", rel_path(record), line_idx, path_raw, detail)


def recheck_record(record: Path, record_lines: list[str]) -> tuple[int, list]:
    """Scan one record; returns (anchor count, findings)."""
    text = "\n".join(record_lines)
    anchors = 0
    findings: list = []
    for m in ANCHOR_RE.finditer(text):
        anchors += 1
        f = check_anchor(m, record, record_lines)
        if f is not None:
            findings.append(f)
    return anchors, findings


def cmd_check(records: list[Path], baseline_path: Path | None) -> int:
    baseline = load_baseline(baseline_path)
    all_findings: list = []
    total_records = 0
    total_anchors = 0
    for rec in records:
        lines = read_lines(rec)
        if lines is None:
            print(f"{TOOL}: ERROR record could not be read: {rec}")
            return 2
        total_records += 1
        anchors, findings = recheck_record(rec, lines)
        total_anchors += anchors
        all_findings.extend(findings)
    seen = set()
    deduped = []
    for f in all_findings:
        key = (f.rule, f.record, f.line, f.anchor)
        if key not in seen:
            seen.add(key)
            deduped.append(f)
    all_findings = [f for f in deduped if f.fingerprint() not in baseline]
    blocking = [f for f in all_findings if f.rule in ROTTED_RULES]
    warns = [f for f in all_findings if f.rule in ROT_WARN_RULES]
    if blocking:
        print(
            f"{TOOL}: FAIL records={total_records} anchors={total_anchors} "
            f"rotted={len(blocking)} warns={len(warns)}"
        )
        for f in blocking:
            print(f"  {f.render()}")
        for f in warns:
            print(f"  WARN {f.render()}")
        print(
            f"{TOOL}: re-derive the flagged cites (quoted-text anchor per the R5 "
            f"law) before publishing, or accept by name via --baseline"
        )
        return 1
    print(
        f"{TOOL}: ok records={total_records} anchors={total_anchors} "
        f"rotted=0 warns={len(warns)}"
    )
    for f in warns:
        print(f"  WARN {f.render()}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        prog="publish_recheck", description=__doc__.splitlines()[0]
    )
    sub = ap.add_subparsers(dest="cmd")
    ck = sub.add_parser("check", help="re-derive line cites against the receipt's mtime")
    scope = ck.add_mutually_exclusive_group(required=True)
    scope.add_argument("--changed", action="store_true", help="changed prose records vs HEAD")
    scope.add_argument("--files", nargs="+", help="explicit record paths")
    ck.add_argument("--baseline", default=None, help="baseline JSON (accept by name)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv[1:])

    if args.selftest:
        # the battery lives in tests/test_publish_recheck.py (fixtures are
        # test material; tests/ sits outside the ratchet's scan roots)
        try:
            import pytest
        except ImportError:
            print(f"{TOOL}: ERROR pytest unavailable, cannot run the battery")
            return 2
        return int(pytest.main([
            str(ESTATE_ROOT / "tests" / "test_publish_recheck.py"),
            "-q", "-p", "no:cacheprovider",
        ]))
    if args.cmd != "check":
        ap.print_help()
        return 2
    if args.baseline:
        baseline_path: Path | None = Path(args.baseline)
    else:
        baseline_path = DEFAULT_BASELINE if DEFAULT_BASELINE.is_file() else None
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
    return cmd_check(records, baseline_path)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
