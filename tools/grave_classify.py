#!/usr/bin/env python3
"""grave_classify.py - one stable vocabulary for grave burial classifications.

Background (gala 2026-09-25, gravedigger lanes c1/c2/c3, receipt
t10.next_steal): the three lanes drifted across label vocabularies.
c1 used FOSSIL at the file level, c2 used DONE-ELSEWHERE / SUPERSEDED-BY /
STILL-RELEVANT, c3 used ABSORBED-BY / STILL-RELEVANT / FOSSIL. This tool is
the canonical label set plus a deterministic classifier so future burials
emit machine rows in one vocabulary.

Canonical labels (exactly five, enforced):
  FOSSIL          stale with forward content landed or overtaken; no living successor needed
  ABSORBED-BY     whole ground is carried forward inside a named successor artifact
  SUPERSEDED-BY   replaced by a later approach; the goal is carried by a named successor line
  DONE-ELSEWHERE  the work already landed outside this handoff
  STILL-RELEVANT  no absorbing successor verified; still owed or still executable

Usage:
  python tools/grave_classify.py <handoff_path> [--label LABEL] [--successor PATH] [--json]
  python tools/grave_classify.py --batch DIR [--pattern GLOB] [--json]

Decision order (deterministic, evidence-first, never fabricates):
  1. --label given: must be canonical, else exit 2 (unknown label).
  2. no --label: scan the file for a classification marker line
     (classification / verdict / disposition followed by a label token).
     One canonical label -> adopt it. Any unknown label token -> exit 2
     (this is exactly the drift this tool exists to catch). Several
     distinct canonical labels -> exit 3 (ambiguous).
  3. no marker, --successor given and found on disk -> SUPERSEDED-BY.
     Callers who mean "the successor carries the whole ground" pass
     --label ABSORBED-BY; absorbed-vs-superseded is a human call, the tool
     enforces the vocabulary, it does not invent the distinction.
  4. no marker, no successor -> STILL-RELEVANT with an
     unclassified-by-evidence note; age since last write is reported as
     data, never treated as a verdict.

Batch mode (t48, gala afterparty 2026-09-25): --batch DIR classifies every
handoff file directly inside DIR in one run. Files only (subdirectories are
skipped), sorted by name, names filtered through --pattern (glob, default
"*" = every file). Each file runs the same decision order above; a file
whose classification fails keeps its row in the table as ERROR(n) with the
error text as its justification line (negatives are first-class, the run
never aborts on the first failure). Batch classifies, it never writes:
handoff files are read, not touched. --label and --successor are
single-file options and are rejected alongside --batch (usage exit 2).

Exit codes: 0 = classified (batch: every file classified); otherwise the
worst per-file code in the batch. 1 = handoff missing, IO error, or
successor hint not found on disk; 2 = unknown label or usage error;
3 = ambiguous markers.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from datetime import date
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parent.parent

FOSSIL = "FOSSIL"
ABSORBED_BY = "ABSORBED-BY"
SUPERSEDED_BY = "SUPERSEDED-BY"
DONE_ELSEWHERE = "DONE-ELSEWHERE"
STILL_RELEVANT = "STILL-RELEVANT"

CANONICAL_LABELS = (
    FOSSIL,
    ABSORBED_BY,
    SUPERSEDED_BY,
    DONE_ELSEWHERE,
    STILL_RELEVANT,
)

#: marker lines look like "Verdict: **FOSSIL as of ..." or
#: '{"classification": "DONE-ELSEWHERE"}' (json) - optional brace, keyword,
#: separator, label. Fixes 2026-09-25: leading '{' allowance and formatting
#: strip came from byte evidence (c1 "Verdict: **FOSSIL", c2 json field).
MARKER_RE = re.compile(
    r"^\s*[{[]?\"?(classification|verdict|disposition)\"?\s*[:=]\s*(.+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)
LABEL_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z-]*")


class GraveClassifyError(Exception):
    """Classification failed; carries the process exit code."""

    def __init__(self, message: str, exit_code: int = 1):
        super().__init__(message)
        self.exit_code = exit_code


class UnknownLabelError(GraveClassifyError):
    """Label outside the canonical five."""

    def __init__(self, label: str):
        super().__init__(
            f"unknown grave label {label!r}; canonical set is "
            f"{', '.join(CANONICAL_LABELS)}",
            exit_code=2,
        )


def require_label(label: str) -> str:
    """Normalize and enforce the canonical label set. Raises UnknownLabelError."""
    normalized = (label or "").strip().upper()
    if normalized not in CANONICAL_LABELS:
        raise UnknownLabelError(label)
    return normalized


def scan_markers(text: str) -> list[tuple[int, str]]:
    """Return (line_number, raw_token_upper) for every marker line."""
    found: list[tuple[int, str]] = []
    for i, line in enumerate(text.splitlines(), start=1):
        m = MARKER_RE.match(line)
        if not m:
            continue
        token = LABEL_TOKEN_RE.match(m.group(2).lstrip("*`\"' "))
        if token:
            found.append((i, token.group(0).upper()))
    return found


def _resolve_successor(raw: str) -> Path | None:
    """Resolve a successor hint as given, then against the estate root."""
    candidate = Path(raw).expanduser()
    if candidate.exists():
        return candidate
    alt = ESTATE_ROOT / raw
    if alt.exists():
        return alt
    return None


def _justification(
    label: str, handoff: str, successor: str | None, successor_exists: bool | None,
    age_days: int | None, as_of: str,
) -> str:
    if label == FOSSIL:
        return (
            f"{handoff}: FOSSIL as of {as_of}; forward content landed or "
            "overtaken, no living successor required; receipt-only burial, "
            "the file stays on disk (deletions are operator-gated)."
        )
    if label == ABSORBED_BY:
        return (
            f"{handoff}: ABSORBED-BY {successor}; its whole ground is "
            f"carried forward there; successor verified on disk: "
            f"{successor_exists}; re-read before any operator gate."
        )
    if label == SUPERSEDED_BY:
        return (
            f"{handoff}: SUPERSEDED-BY {successor}; the goal is carried by a "
            f"later line, do not execute as written; successor verified on "
            f"disk: {successor_exists}; revival needs a fresh re-brief."
        )
    if label == DONE_ELSEWHERE:
        return (
            f"{handoff}: DONE-ELSEWHERE; the work landed outside this "
            "handoff; dead letter, revival needs a fresh re-brief against "
            "current doctrine."
        )
    # STILL_RELEVANT
    age_note = f"{age_days} days since last write" if age_days is not None else "age unknown"
    return (
        f"{handoff}: STILL-RELEVANT as of {as_of}; no absorbing successor "
        f"verified ({age_note}); re-read before acting, not buried by this row."
    )


def classify(
    handoff: str | Path,
    label: str | None = None,
    successor: str | None = None,
    as_of: str | None = None,
) -> dict:
    """Classify one handoff file. Raises GraveClassifyError on failure."""
    path = Path(handoff).expanduser()
    if not path.is_file():
        raise GraveClassifyError(f"handoff file not found: {path}", exit_code=1)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise GraveClassifyError(f"unreadable handoff {path}: {exc}", exit_code=1) from exc

    canonical_label: str
    source: str
    if label is not None:
        canonical_label = require_label(label)
        source = "explicit"
    else:
        markers = scan_markers(text)
        tokens = {tok for _, tok in markers}
        unknown = sorted(tok for tok in tokens if tok not in CANONICAL_LABELS)
        if unknown:
            raise GraveClassifyError(
                f"{path}: unknown grave label(s) {', '.join(unknown)} at "
                f"line(s) {sorted(ln for ln, tok in markers if tok in unknown)}; "
                "canonical set is " + ", ".join(CANONICAL_LABELS),
                exit_code=2,
            )
        if len(tokens) > 1:
            raise GraveClassifyError(
                f"{path}: ambiguous markers {', '.join(sorted(tokens))}; "
                "pass --label to disambiguate",
                exit_code=3,
            )
        if tokens:
            canonical_label = next(iter(tokens))
            source = "marker"
        else:
            # Decision-order step 3: successor hint on disk means SUPERSEDED-BY
            # (callers pass --label ABSORBED-BY to record absorption instead);
            # step 4: nothing at all means STILL_RELEVANT with the honest
            # unclassified-by-evidence note.
            if successor is not None:
                canonical_label = SUPERSEDED_BY
                source = "successor-hint"
            else:
                canonical_label = STILL_RELEVANT
                source = "default"

    resolved_successor: Path | None = None
    successor_exists: bool | None = None
    if successor is not None:
        resolved_successor = _resolve_successor(successor)
        if resolved_successor is None:
            raise GraveClassifyError(
                f"successor hint not found on disk: {successor} "
                "(never fabricate a successor)",
                exit_code=1,
            )
        successor_exists = True
    if canonical_label in (ABSORBED_BY, SUPERSEDED_BY) and resolved_successor is None:
        raise GraveClassifyError(
            f"label {canonical_label} requires --successor naming the "
            "carrying artifact on disk",
            exit_code=1,
        )

    mtime = path.stat().st_mtime
    age_days = max(0, (date.today() - date.fromtimestamp(mtime)).days)
    as_of = as_of or date.today().isoformat()
    successor_name = str(resolved_successor) if resolved_successor is not None else None
    justification = _justification(
        canonical_label, str(path), successor_name, successor_exists, age_days, as_of,
    )
    return {
        "handoff": str(path),
        "label": canonical_label,
        "source": source,
        "successor": successor_name,
        "successor_exists": successor_exists,
        "age_days": age_days,
        "as_of": as_of,
        "justification": justification,
    }


def classify_batch(
    directory: str | Path,
    pattern: str = "*",
    as_of: str | None = None,
) -> tuple[list[dict], int]:
    """Classify every handoff file directly inside a directory, in one run.

    Files only (subdirectories skipped), sorted by name, file names matched
    against ``pattern`` with fnmatch. Every file keeps a row: a classify()
    failure becomes an ERROR(n) row carrying the error text, so the table is
    complete and the run never aborts early. Returns (rows, worst) where
    worst is 0 when every file classified, else the max per-file exit code.
    """
    root = Path(directory).expanduser()
    if not root.is_dir():
        raise GraveClassifyError(f"batch directory not found: {root}", exit_code=1)
    rows: list[dict] = []
    worst = 0
    for path in sorted(root.iterdir(), key=lambda p: p.name):
        if not path.is_file() or not fnmatch.fnmatch(path.name, pattern):
            continue
        try:
            rows.append(classify(path, as_of=as_of))
        except GraveClassifyError as exc:
            worst = max(worst, exc.exit_code)
            rows.append(
                {
                    "handoff": str(path),
                    "label": f"ERROR({exc.exit_code})",
                    "source": "error",
                    "successor": None,
                    "successor_exists": None,
                    "age_days": None,
                    "as_of": as_of or date.today().isoformat(),
                    "error_code": exc.exit_code,
                    "error": str(exc),
                    "justification": str(exc),
                }
            )
    return rows, worst


def _print_batch_table(rows: list[dict]) -> None:
    """One summary table: file, label, justification line, then the tally."""
    fcol = max([len(r["handoff"]) for r in rows] + [len("file")])
    lcol = max([len(r["label"]) for r in rows] + [len("label")])
    print(f"{'file':<{fcol}}  {'label':<{lcol}}  justification")
    print(f"{'-' * fcol}  {'-' * lcol}  {'-' * len('justification')}")
    for row in rows:
        print(
            f"{row['handoff']:<{fcol}}  {row['label']:<{lcol}}  {row['justification']}"
        )
    classified = sum(1 for r in rows if r["source"] != "error")
    print(
        f"batch: {len(rows)} files, {classified} classified, "
        f"{len(rows) - classified} failed"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="grave_classify",
        description="Classify a handoff for grave burial in one stable vocabulary.",
    )
    parser.add_argument("handoff", nargs="?", default=None,
                        help="path to the handoff file to classify")
    parser.add_argument("--batch", default=None, metavar="DIR",
                        help="batch mode: classify every handoff file directly "
                             "inside DIR in one run; conflicts with <handoff>, "
                             "--label and --successor")
    parser.add_argument("--pattern", default="*", metavar="GLOB",
                        help="file-name glob for --batch (default: every file)")
    parser.add_argument("--label", default=None, choices=None,
                        help="force a label; must be in the canonical set")
    parser.add_argument("--successor", default=None,
                        help="path of the artifact that carries this handoff forward")
    parser.add_argument("--json", action="store_true", help="emit the machine row as JSON")
    args = parser.parse_args(argv)
    if args.batch is not None:
        if args.handoff is not None:
            parser.error("pass either <handoff_path> or --batch DIR, not both")
        if args.label is not None or args.successor is not None:
            parser.error(
                "--batch classifies by file evidence only; --label and "
                "--successor are single-file options"
            )
        try:
            rows, worst = classify_batch(args.batch, pattern=args.pattern)
        except GraveClassifyError as exc:
            print(f"grave_classify: {exc}", file=sys.stderr)
            return exc.exit_code
        if args.json:
            print(json.dumps(rows, sort_keys=True))
        else:
            _print_batch_table(rows)
        return worst
    if args.handoff is None:
        parser.error("pass a <handoff_path> or --batch DIR")
    try:
        if args.label is not None:
            require_label(args.label)  # unknown -> exit 2 before touching the file
        row = classify(args.handoff, label=args.label, successor=args.successor)
    except GraveClassifyError as exc:
        print(f"grave_classify: {exc}", file=sys.stderr)
        return exc.exit_code
    if args.json:
        print(json.dumps(row, sort_keys=True))
    else:
        print(row["label"])
        print(f"justification: {row['justification']}")
        evidence = f"source: {row['source']}; age_days: {row['age_days']}"
        if row["successor"] is not None:
            evidence += f"; successor: {row['successor']} (exists={row['successor_exists']})"
        print(f"evidence: {evidence}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
