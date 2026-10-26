#!/usr/bin/env python3
"""freshness_gate.py - freshness-receipts gate (MICKEY17 V2 owed item, t11b; hash binding t37).

Master spec (corpus/steal/MASTER_MICKEY17_V2_20260924.md, row 8, lane agentcheck):
"Retries fix timeouts, not staleness. Staleness needs freshness evidence."

This gate checks one receipt markdown file for a fetch/source freshness stamp:
a dated line like `source-fetched: 2026-09-25`. Exit 0 when a stamp exists, its
date parses, and the date is at most --days old (default 14). Exit 2 otherwise.
Fail-closed by construction: no stamp, an unparseable date, a stale date, a
future-dated stamp (fabrication smell), or a missing file are all exit 2, never
a crash traceback and never a guess.

Optional source-hash binding (t37): a stamp line may carry a sha256 binding,
`source-fetched: 2026-09-25 sha256:<64 hex digits>`. Pass --source PATH to make
the binding load-bearing: when the cited file exists, the gate recomputes its
sha256 and exits 2 on any mismatch, so re-stamping old claims over changed
sources fails the gate. Binding rules:
  - no binding anywhere, no --source: exactly the t11b date-only behavior.
  - binding stamped, no --source: date rules apply; the binding is reported as
    stamped-but-unverified (the gate has nothing local to check against).
  - binding stamped, --source given: the cited file must exist and must hash
    equal (hex case-insensitive); missing file or mismatch is exit 2.
  - --source given, receipt binds nothing: exit 2, there is nothing to verify.
  - the newest stamp drops a sha256 binding an older stamp carried: exit 2
    (re-stamp smell) even without --source; appending a bare fresh stamp must
    not launder a bound claim.
  - a stamp line that says sha256 but carries a malformed binding (wrong
    length or non-hex digits) is not a stamp at all: exit 2, same rule an
    unparseable calendar date gets.

Accepted stamp labels (case-insensitive, colon optional space variants ok):
  source-fetched / source_fetched / fetched / observed-at / observed_at
Date format: YYYY-MM-DD, optionally followed by a time suffix (T…) as in
ISO timestamps, then optionally the sha256 binding. The most recent stamp in
the file is the evidence; older stamps are lineage, not the claim. On a date
tie a bound stamp beats a bare one.

Style: stands alone (tools/quote_gate.py from t11a is not on disk yet);
house conventions borrowed from tools/freshness_check.py (self-test, exit
codes stated in the docstring) and tools/workflow_gate.py (exit 2 is the
only hard block).

Usage: python tools/freshness_gate.py <receipt.md> [--days N] [--source PATH] [--self-test]
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

DEFAULT_MAX_AGE_DAYS = 14
# Tolerated clock skew for stamps slightly in the future (timezone drift).
FUTURE_TOLERANCE_DAYS = 1

# One regex does label + date + optional hash binding.
# Groups: 1=label, 2=YYYY, 3=MM, 4=DD, 5=sha256 hex (optional).
# A time suffix (T… or space HH:MM) may follow the date and is ignored by the
# gate; the sha256 binding, when present, comes after it. The trailing
# lookahead rejects a hex run longer than 64 digits instead of truncating it.
STAMP_RE = re.compile(
    r"(?i)\b(source[-_ ]fetched|fetched|observed[-_]at)\s*:\s*"
    r"(\d{4})-(\d{2})-(\d{2})(?:[T\s]\d{2}:\d{2}(?::\d{2})?Z?)?"
    r"(?:\s+sha256\s*:\s*([0-9a-fA-F]{64}))?(?![0-9a-fA-F])"
)


def find_stamp_bindings(text: str) -> list[tuple[date, str | None]]:
    """Return (date, sha256-hex-or-None) for every parseable stamp, in file order.

    A stamp line that clearly INTENDS a binding (it says sha256 after the
    date) but carries a malformed one (wrong length, non-hex) is not a stamp
    at all: fail-closed, the same rule an unparseable calendar date gets.
    """
    malformed_tail = re.compile(r"(?i)\bsha[-_ ]?256\b")
    bindings: list[tuple[date, str | None]] = []
    for m in STAMP_RE.finditer(text):
        try:
            stamp = date(int(m.group(2)), int(m.group(3)), int(m.group(4)))
        except ValueError:
            continue  # malformed calendar date (e.g. 2026-13-40): not a stamp
        line_end = text.find("\n", m.end())
        if line_end == -1:
            line_end = len(text)
        if malformed_tail.search(text[m.end():line_end]):
            continue  # intended binding is malformed: not evidence, never a guess
        hex_digest = m.group(5)
        bindings.append((stamp, hex_digest.lower() if hex_digest else None))
    return bindings


def find_stamps(text: str) -> list[date]:
    """Return every parseable stamp date in the text, in file order."""
    return [stamp for stamp, _ in find_stamp_bindings(text)]


def _evidence(bindings: list[tuple[date, str | None]]) -> tuple[date, str | None]:
    """Most recent stamp is the evidence; on a date tie a bound stamp wins."""
    best_date, best_hash = bindings[0]
    for stamp, bound in bindings[1:]:
        if stamp > best_date or (stamp == best_date and bound is not None):
            best_date, best_hash = stamp, bound
    return best_date, best_hash


def sha256_of_file(path: Path) -> str:
    """sha256 hex of the file's bytes; raises OSError when the file is unreadable."""
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def gate(
    text: str,
    today: date,
    max_age_days: int = DEFAULT_MAX_AGE_DAYS,
    source: Path | None = None,
) -> dict:
    """Gate one receipt's text. Returns a dict; ok=False means exit 2.

    New keys beside the t11b contract: hash (evidence binding hex or None) and
    hash_ok (True verified match, False verified mismatch, None not checked).
    """
    bindings = find_stamp_bindings(text)
    if not bindings:
        return {
            "ok": False,
            "reason": "no freshness stamp found (want a line like 'source-fetched: YYYY-MM-DD')",
            "stamp": None,
            "age_days": None,
            "hash": None,
            "hash_ok": None,
        }
    stamp, bound_hash = _evidence(bindings)
    if bound_hash is None and any(bound is not None for _, bound in bindings):
        return {
            "ok": False,
            "reason": "newest stamp drops a sha256 binding an older stamp carried; re-stamp smell",
            "stamp": stamp.isoformat(),
            "age_days": None,
            "hash": None,
            "hash_ok": None,
        }
    age_days = (today - stamp).days
    if age_days < -FUTURE_TOLERANCE_DAYS:
        return {
            "ok": False,
            "reason": f"stamp {stamp.isoformat()} is future-dated beyond {FUTURE_TOLERANCE_DAYS}d skew; fabrication smell",
            "stamp": stamp.isoformat(),
            "age_days": age_days,
            "hash": bound_hash,
            "hash_ok": None,
        }
    if age_days > max_age_days:
        return {
            "ok": False,
            "reason": f"stamp {stamp.isoformat()} is {age_days}d old; bar is {max_age_days}d",
            "stamp": stamp.isoformat(),
            "age_days": age_days,
            "hash": bound_hash,
            "hash_ok": None,
        }

    reason = f"stamp {stamp.isoformat()} is {age_days}d old; bar is {max_age_days}d"
    if source is not None and bound_hash is None:
        return {
            "ok": False,
            "reason": f"cited source {source} given but the receipt carries no sha256 binding to verify against it",
            "stamp": stamp.isoformat(),
            "age_days": age_days,
            "hash": None,
            "hash_ok": None,
        }
    hash_ok: bool | None = None
    if bound_hash is not None and source is not None:
        if not source.exists():
            return {
                "ok": False,
                "reason": f"bound source file not found: {source}",
                "stamp": stamp.isoformat(),
                "age_days": age_days,
                "hash": bound_hash,
                "hash_ok": None,
            }
        try:
            actual = sha256_of_file(source)
        except OSError as exc:
            return {
                "ok": False,
                "reason": f"bound source file unreadable: {exc}",
                "stamp": stamp.isoformat(),
                "age_days": age_days,
                "hash": bound_hash,
                "hash_ok": None,
            }
        if actual.lower() != bound_hash:
            return {
                "ok": False,
                "reason": (
                    f"source hash mismatch: receipt binds sha256:{bound_hash}, "
                    f"{source} hashes to sha256:{actual.lower()}"
                ),
                "stamp": stamp.isoformat(),
                "age_days": age_days,
                "hash": bound_hash,
                "hash_ok": False,
            }
        hash_ok = True
        reason += f"; sha256 binding verified against {source}"
    elif bound_hash is not None:
        reason += "; sha256 binding stamped but unverified (pass --source to enforce)"
    return {
        "ok": True,
        "reason": reason,
        "stamp": stamp.isoformat(),
        "age_days": age_days,
        "hash": bound_hash,
        "hash_ok": hash_ok,
    }


def gate_file(
    path: Path,
    today: date,
    max_age_days: int = DEFAULT_MAX_AGE_DAYS,
    source: Path | None = None,
) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {"ok": False, "reason": f"receipt not found: {path}", "stamp": None, "age_days": None, "hash": None, "hash_ok": None}
    except UnicodeDecodeError as exc:
        return {"ok": False, "reason": f"receipt not decodable as utf-8: {exc}", "stamp": None, "age_days": None, "hash": None, "hash_ok": None}
    return gate(text, today, max_age_days, source=source)


def _self_test() -> int:
    today = date(2026, 9, 25)
    cases = [
        ("fresh stamp passes", "source-fetched: 2026-09-20\nclaim here", True),
        ("stale stamp fails", "source-fetched: 2026-09-01\nclaim here", False),
        ("missing stamp fails", "no stamp in this receipt", False),
    ]
    failed = 0

    def check(name: str, got: dict, want_ok: bool) -> None:
        nonlocal failed
        status = "PASS" if got["ok"] == want_ok else "FAIL"
        if got["ok"] != want_ok:
            failed += 1
        print(f"FRESHNESS-GATE self-test {status}: {name} -> ok={got['ok']} ({got['reason']})")

    for name, text, want_ok in cases:
        check(name, gate(text, today), want_ok)

    # Hash-binding cases need a real file to hash.
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        src = tmp_path / "source.txt"
        src.write_bytes(b"claim v1\n")
        good = hashlib.sha256(b"claim v1\n").hexdigest()
        bound = tmp_path / "bound.md"
        bound.write_text(f"source-fetched: 2026-09-20 sha256:{good}\n", encoding="utf-8")
        check("binding matches cited file passes", gate_file(bound, today, source=src), True)
        src.write_bytes(b"claim v2 changed\n")
        check("binding vs changed source fails", gate_file(bound, today, source=src), False)
        dropped = tmp_path / "dropped.md"
        dropped.write_text(
            "source-fetched: 2026-06-01 sha256:" + "a" * 64 + "\nsource-fetched: 2026-09-20\n",
            encoding="utf-8",
        )
        check("re-stamp dropping binding fails", gate_file(dropped, today), False)
    return 2 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Gate a receipt on a source-fetched freshness stamp.")
    parser.add_argument("receipt", nargs="?", help="path to the receipt markdown file")
    parser.add_argument("--days", type=int, default=DEFAULT_MAX_AGE_DAYS, help=f"max stamp age in days (default {DEFAULT_MAX_AGE_DAYS})")
    parser.add_argument("--source", default=None, help="path to the artifact the stamp's sha256 binding refers to")
    parser.add_argument("--self-test", action="store_true", help="run the built-in six-case self-test")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()
    if not args.receipt:
        parser.error("receipt path is required (or pass --self-test)")
        return 2

    source = Path(args.source) if args.source else None
    result = gate_file(Path(args.receipt), date.today(), args.days, source=source)
    label = "ok" if result["ok"] else "FAIL"
    print(f"FRESHNESS-GATE: {label} {args.receipt} ({result['reason']})")
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
