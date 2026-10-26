#!/usr/bin/env python
"""B2-68 probe: sweep the full corpus for NUM_NOY candidates the proposed
proportion guard would newly reject. Read-only; prints every rejection with
its sentence so the guard's blast radius is byte-verifiable before the edit.

Guard under test (proper-fraction + plural-head NP within 2 tokens):
  PROPORTION_RE = r"\\s+(?:of\\s+)?[A-Za-z][A-Za-z'-]*\\s+[A-Za-z][A-Za-z'-]*s\\b"
applied to the sentence tail starting at the match end, only when
numerator < denominator (proper fraction reading).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # probe lives 3 deep under repo root
sys.path.insert(0, str(ROOT / "scripts"))
from the50_t21_q_caption_ledger import (  # noqa: E402
    SRC, NUM_NOY, LEAD_OK, TAIL_OK, SKIP_MD, ORDINAL_RE, QUANTITY, clean_text,
)

PROPORTION_RE = re.compile(
    r"\s+(?:of\s+)?[A-Za-z][A-Za-z'-]*\s+[A-Za-z][A-Za-z'-]*s\b"
)


def main() -> int:
    fired = kept = 0
    with SRC.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            drop = json_load(line)
            text = clean_text(drop.get("text") or "")
            for sent in sentences(text):
                for m in NUM_NOY.finditer(sent):
                    mo, d = int(m.group(1)), int(m.group(2))
                    if not (1 <= mo <= 12 and 1 <= d <= 31):
                        continue
                    if not (LEAD_OK.match(sent[: m.start()][-1:] or "")
                            and TAIL_OK.match(sent[m.end(): m.end() + 1] or "")):
                        continue
                    if (mo, d) in SKIP_MD:
                        continue
                    if ORDINAL_RE.match(sent[m.end(): m.end() + 4]):
                        continue
                    near = sent[max(0, m.start() - 12): m.end() + 12]
                    if QUANTITY.search(near):
                        continue
                    kept += 1
                    if mo < d and PROPORTION_RE.match(sent[m.end():]):
                        fired += 1
                        print(f"FIRE id={drop['id']} mo={mo} d={d} "
                              f"tail={sent[m.end():m.end()+40]!r} "
                              f"sent={sent[:100]!r}")
    print(f"NUM_NOY surviving existing guards: {kept}")
    print(f"new guard rejections: {fired}")
    return 0


import json  # noqa: E402


def json_load(s):
    return json.loads(s)


def sentences(text):
    for ln in text.split("\n"):
        ln = ln.strip()
        if not ln:
            continue
        for part in re.split(r"(?<=[.!?])\s+", ln):
            part = part.strip()
            if 8 <= len(part):
                yield part


if __name__ == "__main__":
    sys.exit(main())
