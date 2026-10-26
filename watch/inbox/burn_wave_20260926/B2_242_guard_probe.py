#!/usr/bin/env python
"""B2-242 probe: sweep the full corpus for NUM_NOY and DOT_NOY candidates that
survive every non-QUANTITY guard but are killed by the QUANTITY window check,
and classify every QUANTITY hit inside the near window as WHOLE-WORD (standalone
unit: legit exclusion) or INSIDE-WORD (substring of another token: false
exclusion). Read-only; prints every affected candidate with its sentence so the
proposed bounded pattern's blast radius is byte-verifiable before the edit.

Cause under test: QUANTITY's unit alternatives are unanchored, so the guard
fires inside words - id 1795201 "Stars = Musk b-day 6/28" lost its 2018-06-28
row because THREE alternatives hit inside words ("k" in Musk, the bare "b" of
"b-day" via [kmgt]?i?b\\b, and "days?" in b-day), while the sibling sentence
"Moon = Full moon 6/27 (or 6/28)" kept both dates. Same defect shape on id
914092 ("k" in attack killed the '"We are under attack" - Q, 4/3' signature
date) and id 10566765 ("mins?" matched "min" inside coming, killing the
"[coming 11.3]?" election marker).

Proposed pattern (QUANTITY_NEW below): per-alternative boundaries. Letter-led
units require no letter/hyphen compound contact; digit-led unit spellings keep
firing after digits ("5k", "32gb", "50%"). bytes? stays unanchored on the left
BY DESIGN: mega/giga-style compounds ("22.7 megabytes") are real units, so the
suffix must keep firing (id 7643939 stays excluded through it).

Two-sided consequence (the guard families over-fire AND under-fire): bounding
would resurrect three candidates that were excluded for the wrong reason.
They move to properly-caused guards, mirrored here:
  TIMES    MEASURE_AFTER gains "times": id 251705 "Posted 4-5 times today."
           is a frequency range, not April 5 (the kill came from "days?" in
           "today").
  SECTION  FIGURE_RE gains "sections?": id 2264304 "Section 5.2 CLAS" is a
           document section reference, not May 2 (the kill came from "secs?"
           in "Section" - same class as B2-220's "Figure 3.1").

PASS requires: restores == exactly the 3 named true dates; new-guard firings ==
exactly the 2 named misdates; zero new-only firings (new pattern is a subset of
old); the 31 existing survivors untouched.

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_242_guard_probe.py
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # probe lives 3 deep under repo root
sys.path.insert(0, str(ROOT / "scripts"))
from the50_t21_q_caption_ledger import (  # noqa: E402
    SRC, NUM_NOY, DOT_NOY, LEAD_OK, TAIL_OK, SKIP_MD, ORDINAL_RE, QUANTITY,
    FRACTIONS, PROPORTION_RE, FIGURE_RE, AGE_BEFORE_RE, MEASURE_AFTER_RE,
    COUNT_NP_BEFORE_RE, RANGE_LIST_RE, clean_text, mk_date, infer_year,
)

# proposed: letter-led units are standalone words (no letter/hyphen compound
# contact); digit-led unit spellings still fire after digits. bytes? keeps its
# left side open for mega-/giga- compounds (real units).
QUANTITY_NEW = re.compile(
    r"(\bmillion\b|\bbillion\b|\btrillion\b|\bpercent\b|%|(?<![a-z])k\b|"
    r"\bpts?\b|\bpoints?\b|\bamp\b|bytes?|"
    r"(?<![a-z])(?:[kmgt]?i?b)(?![a-z-])|(?<![a-z])hz\b|(?<![a-z])fps\b|"
    r"(?<![a-z])mph\b|\bhours?\b|\bhrs?\b|\bminutes?\b|\bmins?\b|"
    r"\bseconds?\b|\bsecs?\b|(?<![\w-])days?\b|\bweeks?\b|\bmonths?\b|"
    r"\byears?\b|\byrs?\b|\bdecades?\b)",
    re.IGNORECASE,
)
# mirrored: SECTION joins the document-label guard (B2-220 Figure class)
FIGURE_RE_NEW = re.compile(r"\b(?:figures?|figs?|sections?)\.?\s*$", re.IGNORECASE)
# mirrored: TIMES joins the measure-noun guard (B2-219 dash family)
MEASURE_AFTER_RE_NEW = re.compile(
    r"\s(?:feet|foot|inches|inch|meters|miles|acres|degrees|fathoms|times)\b",
    re.IGNORECASE,
)

ADJ = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-")

# the 3 true-date rows the bounded guard must restore (id, iso-date)
RESTORE_TARGETS = {
    ("1795201", "2018-06-28"),  # "Stars = Musk b-day 6/28"
    ("914092", "2018-04-03"),   # '"We are under attack" - Q, 4/3'
    ("10566765", "2020-11-03"), # "[coming 11.3]?" election marker
}
# the 2 misdate rows that must migrate to the new guards, not resurrect
NEW_GUARD_TARGETS = {
    ("251705", "2018-04-05"): "TIMES",    # "Posted 4-5 times today."
    ("2264304", "2018-05-02"): "SECTION", # "Section 5.2 CLAS [...]"
}


def hit_class(near: str, m: re.Match):
    """INSIDE if a letter or hyphen touches either edge of the hit."""
    before = near[m.start() - 1] if m.start() > 0 else ""
    after = near[m.end()] if m.end() < len(near) else ""
    kind = "INSIDE" if (before in ADJ or after in ADJ) else "WHOLE"
    return kind, (before or "^"), (after or "$")


def main() -> int:
    restored = {}       # (id, iso) -> (path, near, hits)
    guard_fired = {}    # (id, iso) -> guard name
    survivors = 0
    restored_rows = {}  # ledger key -> conf
    with SRC.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            drop = json.loads(line)
            did = str(drop.get("id"))
            try:
                ts = datetime.fromisoformat(drop["ts"])
            except (KeyError, ValueError):
                ts = None
            text = clean_text(drop.get("text") or "")
            for sent in sentences(text):

                # ---- NUM_NOY path, identical to the module loop ----
                for m in NUM_NOY.finditer(sent):
                    mo, d = int(m.group(1)), int(m.group(2))
                    if not (LEAD_OK.match(sent[: m.start()][-1:] or "")
                            and TAIL_OK.match(sent[m.end(): m.end() + 1] or "")):
                        continue
                    if not (1 <= mo <= 12 and 1 <= d <= 31) or (mo, d) in SKIP_MD:
                        continue
                    if (mo, d) in FRACTIONS:
                        continue
                    if ORDINAL_RE.match(sent[m.end(): m.end() + 4]):
                        continue
                    if mo < d and PROPORTION_RE.match(sent[m.end():]):
                        continue
                    if re.search(r"[/-]", m.group(0)).group(0) == "-":
                        lead = sent[: m.start()][-1:] or ""
                        tail = sent[m.end(): m.end() + 1] or ""
                        if lead == "[" or tail == "]":
                            continue
                        if lead == "(" and tail == ")":
                            continue
                        if AGE_BEFORE_RE.search(sent[: m.start()]):
                            continue
                        if MEASURE_AFTER_RE.match(sent[m.end():]):
                            continue
                        if mo == 1:
                            continue
                        if COUNT_NP_BEFORE_RE.search(sent[: m.start()]):
                            continue
                        if RANGE_LIST_RE.match(sent[m.end():]):
                            continue
                    near = sent[max(0, m.start() - 12): m.end() + 12]
                    dt = mk_date(infer_year(ts, mo, d), mo, d) if ts else None
                    if dt is None:
                        continue
                    old = QUANTITY.search(near)
                    new = QUANTITY_NEW.search(near)
                    if old and not new:
                        guard = "TIMES" if (
                            re.search(r"[/-]", m.group(0)).group(0) == "-"
                            and MEASURE_AFTER_RE_NEW.match(sent[m.end():])
                        ) else None
                        if guard:
                            print(f"NEW-GUARD [{guard}] id={did} "
                                  f"{dt.isoformat()} near={near!r} "
                                  f"sent={sent[:100]!r}")
                            guard_fired[(did, dt.isoformat())] = guard
                        else:
                            hits = [f"{hit_class(near, h)[0]}:{h.group(0)!r}"
                                    for h in QUANTITY.finditer(near)]
                            print(f"RESTORE [NUM_NOY] id={did} {dt.isoformat()} "
                                  f"pair={mo}/{d} near={near!r} hits={hits} "
                                  f"sent={sent[:100]!r}")
                            restored[(did, dt.isoformat())] = ("NUM_NOY", near, hits)
                            restored_rows[(did, dt.isoformat(), sent[:120])] = 0.65
                        continue
                    if not old and not new:
                        if MEASURE_AFTER_RE_NEW.match(sent[m.end():]) \
                                and re.search(r"[/-]", m.group(0)).group(0) == "-":
                            print(f"BUG GUARD-ONLY [NUM_NOY] id={did} near={near!r}")
                            return 1
                        survivors += 1
                        continue
                    # old and new both fire: stays excluded, cause may migrate
                    if not new:
                        pass
                    still = [f"{hit_class(near, h)[0]}:{h.group(0)!r}"
                             for h in QUANTITY_NEW.finditer(near)]
                    g2 = None
                    if re.search(r"[/-]", m.group(0)).group(0) == "-" \
                            and MEASURE_AFTER_RE_NEW.match(sent[m.end():]) \
                            and not MEASURE_AFTER_RE.match(sent[m.end():]):
                        g2 = "TIMES"
                    if g2:
                        print(f"NEW-GUARD [{g2}] id={did} {dt.isoformat()} "
                              f"near={near!r} still={still} sent={sent[:100]!r}")
                        guard_fired[(did, dt.isoformat())] = g2

                # ---- DOT_NOY path, identical to the module loop ----
                for m in DOT_NOY.finditer(sent):
                    a, b = int(m.group(1)), int(m.group(2))
                    if not (LEAD_OK.match(sent[: m.start()][-1:] or "")
                            and TAIL_OK.match(sent[m.end(): m.end() + 1] or "")):
                        continue
                    near = sent[max(0, m.start() - 12): m.end() + 12]
                    if "$" in near:
                        continue
                    if FIGURE_RE.search(sent[: m.start()]):
                        continue
                    if 1 <= a <= 12 and 1 <= b <= 31:
                        mo, d, conf = a, b, 0.50
                    elif 1 <= a <= 31 and 1 <= b <= 12:
                        mo, d, conf = b, a, 0.40
                    else:
                        continue
                    if (mo, d) in SKIP_MD:
                        continue
                    dt = mk_date(infer_year(ts, mo, d), mo, d) if ts else None
                    if dt is None:
                        continue
                    old = QUANTITY.search(near)
                    new = QUANTITY_NEW.search(near)
                    if old and not new:
                        if FIGURE_RE_NEW.search(sent[: m.start()]) \
                                and not FIGURE_RE.search(sent[: m.start()]):
                            print(f"NEW-GUARD [SECTION] id={did} {dt.isoformat()} "
                                  f"token={m.group(0)!r} near={near!r} "
                                  f"sent={sent[:100]!r}")
                            guard_fired[(did, dt.isoformat())] = "SECTION"
                        else:
                            hits = [f"{hit_class(near, h)[0]}:{h.group(0)!r}"
                                    for h in QUANTITY.finditer(near)]
                            print(f"RESTORE [DOT_NOY] id={did} {dt.isoformat()} "
                                  f"token={m.group(0)!r} near={near!r} hits={hits} "
                                  f"sent={sent[:100]!r}")
                            restored[(did, dt.isoformat())] = ("DOT_NOY", near, hits)
                            restored_rows[(did, dt.isoformat(), sent[:120])] = conf
                        continue
                    if not old and not new:
                        if FIGURE_RE_NEW.search(sent[: m.start()]) \
                                and not FIGURE_RE.search(sent[: m.start()]):
                            print(f"BUG GUARD-ONLY [DOT_NOY] id={did} near={near!r}")
                            return 1
                        survivors += 1

    print(f"unchanged survivors (no guard difference): {survivors}")
    print(f"RESTORED candidates: {len(restored)} "
          f"(distinct ledger rows: {len(restored_rows)})")
    for (did, iso, claim), conf in sorted(restored_rows.items()):
        print(f"  ROW id={did} {iso} conf={conf} claim={claim[:100]!r}")
    for (did, iso), guard in sorted(guard_fired.items()):
        print(f"  GUARD {guard} id={did} {iso}")
    got_r = set(restored)
    got_g = {k: v for k, v in guard_fired.items()}
    ok = (got_r == RESTORE_TARGETS and got_g == NEW_GUARD_TARGETS
          and survivors == 31)
    print("PROBE RESULT:", "PASS" if ok else
          f"FAIL (restores={sorted(got_r)} guards={got_g} survivors={survivors})")
    return 0 if ok else 1


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
