#!/usr/bin/env python3
"""bib_launder_check.py: byte-compare invariant blocks between a seed prompt
and an uplifted candidate.

Spec source: watch/inbox/BURN_prompt-uplift-lane_20260925_d.md (patch (b)/(c))
and the LOCK half of roblox/prompts/README.md V2 amendment A. The invariant
block is delimited by a fixed marker header and runs through the line before
the next markdown header (or EOF). Blocks are extracted as raw bytes: no
whitespace or unicode normalization, because both are launder vectors. Each
block's sha256 in the candidate is compared against the SEED hash, never
against a previous candidate (anchor clause).

Exit codes:
  0  MATCH: every invariant block in the candidate is byte-identical to the
     seed's (and at least one invariant block exists).
  2  FAIL(BIB_LAUNDER): a block differs, or a block present in the seed is
     missing from the candidate. Prints the first divergent line.
  3  NO_INVARIANT_BLOCK: the seed carries none of the known markers (for
     example ONE_SHOT_GAME ships none by design). Nothing to compare.

Stdlib only. Usage:
  python bib_launder_check.py SEED_FILE UPLIFTED_FILE [--marker "## FACTS"] ...
"""
import argparse
import hashlib
import re
import sys

# The roblox/prompts convention (README.md V2 amendment A, LOCK half):
# per-template invariant markers. Auto-detected from the seed in this order.
KNOWN_MARKERS = [
    "## FACTS",              # DETAIL.prompt.md
    "## SOURCE TRUTH",       # PORT_GAME.prompt.md
    "## THE WHEEL TO CLONE", # CLONE_WHEEL.prompt.md
    "## FROZEN PREFIX",      # NPC_HEAD.prompt.md (block 1 of 2)
    "## THE KNOT",           # NPC_HEAD.prompt.md (block 2 of 2)
]

HEADER_RE = re.compile(rb"^#{1,6} ")


def line_offsets(data: bytes):
    """Start offset of every line in data (bytes, newlines preserved)."""
    offs = [0]
    pos = 0
    while True:
        nl = data.find(b"\n", pos)
        if nl == -1:
            break
        offs.append(nl + 1)
        pos = nl + 1
    return offs


def is_header(line: bytes) -> bool:
    return bool(HEADER_RE.match(line))


def extract_block(data: bytes, marker: bytes):
    """Return (start, end) byte span of the marker's block, or None.

    Block starts at the first line that is a header beginning with the
    marker text, and ends just before the next header line (any level) or
    EOF. Byte-exact: the span includes the original line endings.
    """
    for start in line_offsets(data):
        line = data[start:].split(b"\n", 1)[0]
        if is_header(line) and line.startswith(marker):
            for off in line_offsets(data):
                if off <= start:
                    continue
                hline = data[off:].split(b"\n", 1)[0]
                if is_header(hline):
                    return (start, off)
            return (start, len(data))
    return None


def first_divergence(seed_block: bytes, cand_block: bytes):
    """First differing line pair as decoded text, or None if identical."""
    s_lines = seed_block.splitlines(keepends=True)
    c_lines = cand_block.splitlines(keepends=True)
    for i in range(max(len(s_lines), len(c_lines))):
        s = s_lines[i] if i < len(s_lines) else None
        c = c_lines[i] if i < len(c_lines) else None
        if s != c:
            fmt = lambda b: (
                b.decode("utf-8", "replace").rstrip("\r\n")
                if b is not None else "<line absent>"
            )
            return (i + 1, fmt(s), fmt(c))
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("seed")
    ap.add_argument("uplifted")
    ap.add_argument("--marker", action="append", default=None,
                    help="marker header (repeatable); default: auto-detect "
                         "known roblox/prompts markers present in the seed")
    args = ap.parse_args()

    with open(args.seed, "rb") as f:
        seed = f.read()
    with open(args.uplifted, "rb") as f:
        cand = f.read()

    markers = args.marker
    if markers is None:
        markers = [m for m in KNOWN_MARKERS if extract_block(seed, m.encode())]
    if not markers:
        print("NO_INVARIANT_BLOCK: seed carries no known invariant marker; "
              "nothing to byte-compare")
        return 3

    failed = False
    for marker in markers:
        mb = marker.encode()
        s_span = extract_block(seed, mb)
        c_span = extract_block(cand, mb)
        if s_span is None:
            print("NO_INVARIANT_BLOCK: marker %r absent from seed" % marker)
            return 3
        if c_span is None:
            print("FAIL(BIB_LAUNDER): marker %r block present in seed but "
                  "missing from uplifted (launder by deletion)" % marker)
            failed = True
            continue
        s_block = seed[s_span[0]:s_span[1]]
        c_block = cand[c_span[0]:c_span[1]]
        s_hash = hashlib.sha256(s_block).hexdigest()
        c_hash = hashlib.sha256(c_block).hexdigest()
        print("marker %s" % marker)
        print("  seed sha256     %s" % s_hash)
        print("  uplifted sha256 %s" % c_hash)
        if s_hash != c_hash:
            div = first_divergence(s_block, c_block)
            if div:
                print("  first divergent line (block line %d):" % div[0])
                print("    seed:     %s" % div[1])
                print("    uplifted: %s" % div[2])
            else:
                print("  span boundaries differ but line content identical "
                      "(boundary shift); treating as FAIL: byte span is the "
                      "unit of invariance")
            print("FAIL(BIB_LAUNDER): %s block altered" % marker)
            failed = True
        else:
            print("  MATCH")

    if failed:
        print("VERDICT: FAIL(BIB_LAUNDER)")
        return 2
    print("VERDICT: MATCH (all invariant blocks byte-identical to seed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
