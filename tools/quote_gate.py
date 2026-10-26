#!/usr/bin/env python3
"""quote_gate.py - verbatim-quote gate over a cited source file.

The Mickey17 V2 cheapest-3-gates row (corpus/steal/MASTER_MICKEY17_V2_20260924.md
item 3): LLMs emit verbatim quotes correctly only 47% of the time (BITF
self-test, 29/62 quotes found), so every judge quote is gated against the file
it claims to come from before it can count as evidence. Fixed-string semantics
(grep -F): the whole quote must appear byte-for-byte; a whitespace-normalized
fallback absorbs line-wrap and CRLF drift, nothing else. A miss means the
source does not contain the quote: exit 2 is the first-class negative, not an
error, and every error path (missing file, unreadable file, empty quote)
raises into the same fail-closed verdict instead of a traceback.

Usage:
  python tools/quote_gate.py "QUOTE" path/to/source.ext

Exit codes: 0 = quote found (raw or whitespace-normalized), 2 = not found
(miss, missing source, unreadable source, or empty quote).
Stdout is exactly one verdict line, safe to tee into a receipt.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def check_quote(quote: str, source_bytes: bytes) -> tuple[bool, str]:
    """Return (found, mode); mode is "raw" or "whitespace-normalized"."""
    if not quote:
        return False, "empty-quote"
    if quote.encode("utf-8") in source_bytes:  # grep -F: byte-for-byte substring
        return True, "raw"
    q_norm = re.sub(r"\s+", " ", quote).strip()
    if q_norm and q_norm in re.sub(r"\s+", " ", source_bytes.decode("utf-8", errors="replace")):
        return True, "whitespace-normalized"
    return False, "miss"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Gate a verbatim quote against its cited source file (fail-closed)."
    )
    parser.add_argument("quote", help="the quote the judge claims is verbatim")
    parser.add_argument("source", type=Path, help="file the quote claims to come from")
    args = parser.parse_args(argv)
    if not args.quote.strip():
        print("QUOTE-GATE FAIL: empty quote, nothing to verify")
        return 2
    if not args.source.is_file():
        print(f"QUOTE-GATE FAIL: source file not found: {args.source}")
        return 2
    try:
        source_bytes = args.source.read_bytes()
    except OSError as exc:
        print(f"QUOTE-GATE FAIL: source unreadable: {exc}")
        return 2
    found, mode = check_quote(args.quote, source_bytes)
    if found:
        print(f"QUOTE-GATE PASS: quote found in {args.source} ({mode})")
        return 0
    print(f"QUOTE-GATE FAIL: quote not found in {args.source} (raw and whitespace-normalized both missed)")
    return 2


if __name__ == "__main__":
    sys.exit(main())
