#!/usr/bin/env python3
"""checkbox_receipt_gate.py - standing check for checked rows without receipts
(burn brief B2-316, 2026-09-26; turns the B2-251 audit into a gate).

The B2-251 audit proved a checked Open row mutes the dispatcher refill
denominator with no trace, and the audit sweep itself was hand-run. This gate
makes that sweep standing: every CHECKED row in the Open section of
watch/inbox/burn_wave_20260926/QUEUE.md must name at least one receipt path
that RESOLVES on disk. A checked row naming nothing resolvable is the B2-238
disease (unearned flip) and fails as NEW debt, naming the lane id.

Baseline (the B2-251-attached rows): a checked row carrying the
"(receipt attachment" marker is accepted as named baseline, and its attachment
path is also resolution-checked when present.

Usage: .venv/Scripts/python.exe tools/checkbox_receipt_gate.py [--queue PATH]
Exit 0 = every checked Open row carries a resolvable receipt (or named
baseline); 1 = NEW debt, offenders listed; 2 = cannot verify.
Falsifier: append a checked row with no resolvable receipt pointer and run
this gate; it must fail naming that row (before this gate, validate passed it
in silence).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"
ROW_RE = re.compile(r"^- \[x\] (B2-\d+) (.+)$")
PATH_RE = re.compile(r"[A-Za-z0-9_\-./\\]+\.(?:md|json|jsonl|py|txt)\b")
ATTACHMENT_MARKER = "(receipt attachment"
BASELINE_MARKERS = ("(receipt attachment",)


def checked_open_rows(text: str) -> list[tuple[str, str]]:
    """(id, text) for checked rows after the '## Open' heading.

    Only the '## Dispensed' and '## Open' headings toggle the section: the
    board carries annotation headings later in the file (a standing-law note,
    a restoration note) that do NOT end the Open section, so a naive
    any-'## '-heading parser would blind the gate to the whole tail.
    """
    out: list[tuple[str, str]] = []
    in_open = False
    for raw in text.splitlines():
        if raw.startswith("## "):
            h = raw.strip().lower()
            if h == "## open":
                in_open = True
            elif h == "## dispensed":
                in_open = False
            continue
        if not in_open:
            continue
        m = ROW_RE.match(raw.strip())
        if m:
            out.append((m.group(1), m.group(2)))
    return out


def resolvable_paths(text: str) -> list[str]:
    hits = []
    for tok in PATH_RE.findall(text):
        tok = tok.replace("\\", "/").lstrip("./")
        if tok.startswith("watch/") or tok.startswith("memory/"):
            cand = ROOT / tok
        else:
            cand = ROOT / "watch" / "inbox" / "burn_wave_20260926" / tok
            if not cand.is_file():
                cand = ROOT / tok
        if cand.is_file():
            hits.append(tok)
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", default=str(DEFAULT_QUEUE))
    a = ap.parse_args()
    q = Path(a.queue)
    if not q.is_file():
        print(f"cannot verify, queue missing: {q}")
        return 2
    rows = checked_open_rows(q.read_text(encoding="utf-8", errors="replace"))
    offenders: list[str] = []
    baseline = 0
    for rid, text in rows:
        if any(m in text for m in BASELINE_MARKERS):
            baseline += 1
            # baseline rows still owe a resolvable attachment path when named
            if not resolvable_paths(text) and ATTACHMENT_MARKER in text:
                offenders.append(f"{rid} (baseline-attached but no resolvable attachment path)")
            continue
        if not resolvable_paths(text):
            offenders.append(rid)
    print(f"CHECKBOX-RECEIPT-GATE: {len(rows)} checked Open rows, "
          f"{baseline} baseline-attached, {len(offenders)} offenders")
    for o in offenders:
        print(f"  NEW DEBT: {o}: checked Open row names no receipt path resolving on disk")
    if offenders:
        print("CHECKBOX-RECEIPT-GATE: FAIL (B2-238 disease: unearned flips mute the dispatcher)")
        return 1
    print("CHECKBOX-RECEIPT-GATE: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
