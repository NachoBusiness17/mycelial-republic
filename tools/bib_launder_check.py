#!/usr/bin/env python3
"""bib_launder_check - mechanical FAIL(BIB_LAUNDER) pre-flight checker (B2-154).

The teeth for roblox/prompts/README.md amendment A (THE V2 AMENDMENTS,
2026-09-26): the candidate-side LOCK. Law level landed in the README; this
script is the mechanical check the README owes ("Still owed: the per-template
contract lines and the checker script from pass d"). Shape is pass d (b)/(c),
unchanged, per watch/inbox/BURN_prompt-uplift-lane_20260925_d.md and the
B2-154 queue row:

  - Extract each invariant block by fixed marker (header through next header).
  - sha256 against the SEED hash, never the previous candidate (anchor clause:
    candidate-to-candidate comparison lets drift compound silently).
  - No whitespace or unicode normalization: both are launder vectors. A block
    that differs by one byte (a folded space, a composed accent swapped for a
    decomposition, a CRLF for an LF) is a diff, and any diff is a fail.
  - Empty diff is the only pass.
  - Exit 2 on fail.
  - Never a judge instruction: byte-equality is mechanical, and a judge asked
    to verify bytes will paraphrase-verify. This script renders verdicts and
    hashes only; it never scores prose and never asks a model anything.
  - No repair round: a "corrected" FACTS block is still laundered provenance.
    On FAIL the only clean artifact is a candidate carrying the SEED blocks
    byte-for-byte; this script offers no merge, no patch, no fix-up.

Per-template invariant blocks (README amendment A):

  DETAIL        `## FACTS`
  PORT_GAME     `## SOURCE TRUTH`
  CLONE_WHEEL   `## THE WHEEL TO CLONE` plus its CONTRACT item 2 source lines
  NPC_HEAD      FROZEN PREFIX (`## FROZEN PREFIX`) + THE KNOT (`## THE KNOT`)
  ONE_SHOT_GAME ships none: a rewrite that introduces any invariant-block
                marker, or a sourced-looking claim (URL, arXiv id, DOI), is
                FAIL(BIB_LAUNDER)

Checked surface: the payload after the first standalone `---` line (the
system block each template tells the operator to paste), else the whole file.
The template is detected from the SEED only (filename, then content markers);
a candidate is never asked what it is, because a laundered candidate lies.

Exit codes: 0 all candidates pass; 2 FAIL(BIB_LAUNDER) on any candidate
block or introduction; 1 operational error (unreadable path, marker missing
from the SEED template, unknown template, usage). Exit 2 is reserved for the
verdict; nothing else may emit it.

Usage:
  python tools/bib_launder_check.py --seed roblox/prompts/DETAIL.prompt.md \
      --candidate candidate1.md [candidate2.md ...] [--template detail] [--json]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys

FAIL = "FAIL(BIB_LAUNDER)"
PASS = "PASS"

# "@item:N" is the sentinel for CONTRACT item N (a numbered list item), used
# where the README contract names source lines that live outside a header
# block (CLONE_WHEEL item 2).
TEMPLATES: dict[str, list[tuple[str, str]]] = {
    "detail": [("FACTS", "## FACTS")],
    "port_game": [("SOURCE_TRUTH", "## SOURCE TRUTH")],
    "clone_wheel": [("CONTRACT_ITEM_2", "@item:2"), ("WHEEL", "## THE WHEEL TO CLONE")],
    "npc_head": [("FROZEN_PREFIX", "## FROZEN PREFIX"), ("THE_KNOT", "## THE KNOT")],
    "one_shot_game": [],
}

# Introduced-block markers for the ships-none class: any of the fleet's
# invariant headers appearing in a ONE_SHOT_GAME candidate is a sourced-looking
# block by construction.
INTRO_MARKERS = sorted({m for blocks in TEMPLATES.values() for _, m in blocks if not m.startswith("@")})

# Sourced-looking claim patterns, deliberately conservative and mechanical.
# Aesthetics-by-reference stays legal ("GTA 1-style" is a required move in the
# template); only fetchable provenance shapes are matched.
SOURCE_PATTERNS = [
    re.compile(r"https?://", re.IGNORECASE),
    re.compile(r"www\.", re.IGNORECASE),
    re.compile(r"arxiv\.org", re.IGNORECASE),
    re.compile(r"arxiv:\d{4}", re.IGNORECASE),
    re.compile(r"doi\.org", re.IGNORECASE),
    re.compile(r"\b10\.\d{4,9}/\S"),
]

FILENAME_MAP = [
    ("DETAIL", "detail"),
    ("PORT_GAME", "port_game"),
    ("CLONE_WHEEL", "clone_wheel"),
    ("NPC_HEAD", "npc_head"),
    ("ONE_SHOT_GAME", "one_shot_game"),
]

CONTENT_MARKERS = [
    ("## FROZEN PREFIX", "npc_head"),
    ("## SOURCE TRUTH", "port_game"),
    ("## THE WHEEL TO CLONE", "clone_wheel"),
    ("## FACTS", "detail"),
]


class UsageParser(argparse.ArgumentParser):
    # argparse defaults to exit 2 on usage error; exit 2 is reserved for the
    # FAIL verdict, so usage errors take exit 1.
    def error(self, message):  # type: (str) -> None
        self.exit(1, "usage error: %s (see --help)\n" % message)


def split_lines(data: bytes) -> list[bytes]:
    """Split on LF only, keeping line ends; no other boundary is a line
    boundary (bytes.splitlines would also split on unicode separators, which
    would let a launder vector move bytes between 'lines' unnoticed)."""
    out: list[bytes] = []
    start = 0
    n = len(data)
    while start < n:
        idx = data.find(b"\n", start)
        if idx == -1:
            out.append(data[start:])
            break
        out.append(data[start:idx + 1])
        start = idx + 1
    return out


def line_text(raw: bytes) -> str:
    """Marker-detection view of one raw line: strips only the trailing line
    break. Interior bytes are never altered; decode is lossless via
    surrogateescape, so detection cannot normalize anything."""
    if raw.endswith(b"\r\n"):
        raw = raw[:-2]
    elif raw.endswith(b"\n"):
        raw = raw[:-1]
    return raw.decode("utf-8", "surrogateescape")


def payload(data: bytes) -> bytes:
    """Bytes after the first standalone `---` line, else the whole file."""
    off = 0
    for raw in split_lines(data):
        if line_text(raw) == "---":
            return data[off + len(raw):]
        off += len(raw)
    return data


def sha256_bytes(block: bytes) -> str:
    return hashlib.sha256(block).hexdigest()


def extract_block(data: bytes, marker: str) -> bytes | None:
    """Invariant block = marker line through the line before the next `## `
    header (or EOF). Exact source bytes, whatever they are."""
    lines = split_lines(data)
    start = None
    for i, raw in enumerate(lines):
        if line_text(raw).startswith(marker):
            start = i
            break
    if start is None:
        return None
    for j in range(start + 1, len(lines)):
        if line_text(lines[j]).startswith("## "):
            return b"".join(lines[start:j])
    return b"".join(lines[start:])


_NUMBERED = re.compile(r"^\d+\.")


def extract_contract_item(data: bytes, number: int) -> bytes | None:
    """CONTRACT item span: the `N.` line through the line before the next
    numbered item or `## ` header (or EOF). Exact source bytes."""
    lines = split_lines(data)
    start = None
    prefix = "%d." % number
    for i, raw in enumerate(lines):
        text = line_text(raw)
        if start is None:
            if text.startswith(prefix):
                start = i
        elif text.startswith("## ") or _NUMBERED.match(text):
            return b"".join(lines[start:i])
    if start is None:
        return None
    return b"".join(lines[start:])


def extract_part(data: bytes, part: str) -> bytes | None:
    if part.startswith("@item:"):
        return extract_contract_item(data, int(part.split(":", 1)[1]))
    return extract_block(data, part)


def detect_template(seed_path: str, seed_data: bytes) -> str:
    base = os.path.basename(seed_path).upper()
    for prefix, name in FILENAME_MAP:
        if base.startswith(prefix + "."):
            return name
    body = payload(seed_data)
    for marker, name in CONTENT_MARKERS:
        if extract_block(body, marker) is not None:
            return name
    return "one_shot_game"


def introduction_scan(cand_data: bytes) -> list[str]:
    """ONE_SHOT_GAME: list the introduced sourced-looking lines, if any."""
    hits: list[str] = []
    body = payload(cand_data)
    for raw in split_lines(body):
        text = line_text(raw)
        for marker in INTRO_MARKERS:
            if text.startswith(marker):
                hits.append("introduced invariant block marker %r" % marker)
                break
        else:
            for pattern in SOURCE_PATTERNS:
                if pattern.search(text):
                    hits.append("introduced sourced-looking claim: %r" % text[:120])
                    break
    return hits


def check(seed_path: str, cand_path: str, template: str) -> dict:
    report: dict = {"candidate": cand_path, "blocks": [], "verdict": PASS}
    seed_bytes = read_file(seed_path)
    cand_bytes = read_file(cand_path)
    cand_body = payload(cand_bytes)
    seed_body = payload(seed_bytes)
    for name, part in TEMPLATES[template]:
        seed_block = extract_part(seed_body, part)
        if seed_block is None:
            raise OperationalError(
                "seed %s lacks invariant part %s (%s): template contract broken"
                % (seed_path, name, part))
        cand_block = extract_part(cand_body, part)
        seed_sha = sha256_bytes(seed_block)
        if cand_block is None:
            report["blocks"].append({
                "block": name,
                "seed_sha256": seed_sha,
                "cand_sha256": None,
                "verdict": FAIL,
                "reason": "invariant block missing from candidate (deletion is laundering)",
            })
        else:
            cand_sha = sha256_bytes(cand_block)
            if cand_sha == seed_sha:
                report["blocks"].append({
                    "block": name,
                    "seed_sha256": seed_sha,
                    "cand_sha256": cand_sha,
                    "verdict": PASS,
                    "reason": "empty diff",
                })
            else:
                report["blocks"].append({
                    "block": name,
                    "seed_sha256": seed_sha,
                    "cand_sha256": cand_sha,
                    "verdict": FAIL,
                    "reason": "block bytes differ from SEED (no normalization applied; any diff fails)",
                })
    if template == "one_shot_game":
        for hit in introduction_scan(cand_bytes):
            report["blocks"].append({
                "block": None,
                "seed_sha256": None,
                "cand_sha256": None,
                "verdict": FAIL,
                "reason": hit,
            })
    if any(b["verdict"] == FAIL for b in report["blocks"]):
        report["verdict"] = FAIL
    return report


class OperationalError(Exception):
    pass


def read_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def main(argv: list[str]) -> int:
    parser = UsageParser(description="BIB_LAUNDER pre-flight byte check (B2-154)")
    parser.add_argument("--seed", required=True, help="SEED prompt path (the anchor)")
    parser.add_argument("--candidate", required=True, action="append", dest="candidates",
                        help="candidate path; repeat for multiple candidates")
    parser.add_argument("--template", choices=sorted(TEMPLATES), default=None,
                        help="force template (default: detect from the SEED)")
    parser.add_argument("--json", action="store_true", help="machine-readable report")
    args = parser.parse_args(argv)

    try:
        seed_bytes = read_file(args.seed)
    except OSError as exc:
        print("operational error: cannot read seed %s: %s" % (args.seed, exc), file=sys.stderr)
        return 1
    template = args.template or detect_template(args.seed, seed_bytes)
    if template not in TEMPLATES:
        print("operational error: unknown template %r" % template, file=sys.stderr)
        return 1

    reports = []
    for cand in args.candidates:
        try:
            reports.append(check(args.seed, cand, template))
        except OSError as exc:
            print("operational error: cannot read candidate %s: %s" % (cand, exc), file=sys.stderr)
            return 1
        except OperationalError as exc:
            print("operational error: %s" % exc, file=sys.stderr)
            return 1

    verdict = FAIL if any(r["verdict"] == FAIL for r in reports) else PASS
    if args.json:
        print(json.dumps({
            "check": "BIB_LAUNDER",
            "template": template,
            "seed": args.seed,
            "verdict": verdict,
            "candidates": reports,
        }, indent=2))
    else:
        print("BIB_LAUNDER pre-flight template=%s seed=%s" % (template, args.seed))
        for r in reports:
            print("candidate=%s" % r["candidate"])
            for b in r["blocks"]:
                print("  block=%s seed_sha256=%s cand_sha256=%s %s%s" % (
                    b["block"], b["seed_sha256"], b["cand_sha256"], b["verdict"],
                    "" if b["verdict"] == PASS else " (%s)" % b["reason"]))
        print("VERDICT: %s" % verdict)
        if verdict == FAIL:
            print("locked: rejection is independent of score; no repair round; "
                  "the only clean artifact carries the SEED blocks byte-for-byte.")
    return 0 if verdict == PASS else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
