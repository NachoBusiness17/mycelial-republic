#!/usr/bin/env python
"""B2-220 probe: sweep the full corpus for dotted-token (DOT_NOY) survivors
and measure what the two proposed guards would newly reject. Read-only;
prints every rejection with its sentence so the blast radius is
byte-verifiable before the edit.

Guards under test:
  1. QUANTITY gains \\byrs?\\b (yr/yrs unit abbreviation). Cause: id 1416139
     "Why has it taken 1.5 yrs?" dated as 2018-01-05. Measured on BOTH the
     DOT_NOY and NUM_NOY paths (QUANTITY is shared).
  2. FIGURE_RE prefix guard on the DOT_NOY path: the match must not sit
     directly after a figure label (Figure/Fig/Figs). Cause: id 114
     "Figure 3.1 - FBI Chain of Command" dated as 2018-03-01.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # probe lives 3 deep under repo root
sys.path.insert(0, str(ROOT / "scripts"))
from the50_t21_q_caption_ledger import (  # noqa: E402
    SRC, NUM_NOY, DOT_NOY, LEAD_OK, TAIL_OK, SKIP_MD, ORDINAL_RE, QUANTITY,
    FRACTIONS, PROPORTION_RE, clean_text,
)

QUANTITY_NEW = re.compile(
    r"(million|billion|trillion|percent|%|k\b|pts?|points?\b|amp|"
    r"bytes?|[kmgt]?i?b\b|hz\b|fps\b|mph\b|"
    r"hours?|hrs?|minutes?|mins?|seconds?|secs?|days?|weeks?|months?|years?|\byrs?\b|decades?)",
    re.IGNORECASE,
)
FIGURE_RE = re.compile(r"\b(?:figures?|figs?)\.?\s*$", re.IGNORECASE)


def main() -> int:
    dot_surv = dot_new_yrs = dot_new_fig = 0
    num_surv = num_new_yrs = 0
    with SRC.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            drop = json.loads(line)
            text = clean_text(drop.get("text") or "")
            for sent in sentences(text):

                # ---- DOT_NOY path, existing chain, then proposed guards ----
                for m in DOT_NOY.finditer(sent):
                    a, b = int(m.group(1)), int(m.group(2))
                    if not (LEAD_OK.match(sent[: m.start()][-1:] or "")
                            and TAIL_OK.match(sent[m.end(): m.end() + 1] or "")):
                        continue
                    near = sent[max(0, m.start() - 12): m.end() + 12]
                    if QUANTITY.search(near) or "$" in near:
                        continue
                    if not ((1 <= a <= 12 and 1 <= b <= 31)
                            or (1 <= a <= 31 and 1 <= b <= 12)):
                        continue
                    if (a, b) in SKIP_MD or (b, a) in SKIP_MD:
                        continue
                    dot_surv += 1
                    yrs_fires = (QUANTITY_NEW.search(near)
                                 and not QUANTITY.search(near))
                    fig_fires = bool(FIGURE_RE.search(sent[: m.start()]))
                    tag = []
                    if yrs_fires:
                        dot_new_yrs += 1
                        tag.append("YRS")
                    if fig_fires:
                        dot_new_fig += 1
                        tag.append("FIG")
                    if tag:
                        print(f"NEW-REJECT [{'+'.join(tag)}] id={drop['id']} "
                              f"token={m.group(0)!r} prefix={sent[max(0, m.start()-20):m.start()]!r} "
                              f"sent={sent[:100]!r}")
                    else:
                        print(f"KEEP id={drop['id']} token={m.group(0)!r} "
                              f"sent={sent[:100]!r}")

                # ---- NUM_NOY path: yrs-addition blast radius only ----
                for m in NUM_NOY.finditer(sent):
                    mo, d = int(m.group(1)), int(m.group(2))
                    if not (LEAD_OK.match(sent[: m.start()][-1:] or "")
                            and TAIL_OK.match(sent[m.end(): m.end() + 1] or "")):
                        continue
                    if not (1 <= mo <= 12 and 1 <= d <= 31):
                        continue
                    if (mo, d) in SKIP_MD or (mo, d) in FRACTIONS:
                        continue
                    if ORDINAL_RE.match(sent[m.end(): m.end() + 4]):
                        continue
                    if mo < d and PROPORTION_RE.match(sent[m.end():]):
                        continue
                    near = sent[max(0, m.start() - 12): m.end() + 12]
                    if QUANTITY.search(near):
                        continue
                    num_surv += 1
                    if QUANTITY_NEW.search(near):
                        num_new_yrs += 1
                        print(f"NEW-REJECT [NUM-YRS] id={drop['id']} "
                              f"token={m.group(0)!r} sent={sent[:100]!r}")

    print(f"DOT_NOY surviving existing guards: {dot_surv}")
    print(f"DOT_NOY new rejections: yrs={dot_new_yrs} fig={dot_new_fig} "
          f"total={dot_new_yrs + dot_new_fig}")
    print(f"NUM_NOY surviving existing guards: {num_surv}")
    print(f"NUM_NOY new rejections from yrs: {num_new_yrs}")
    return 0


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
