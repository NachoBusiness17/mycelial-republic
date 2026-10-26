#!/usr/bin/env python
"""B2-258 probe: sweep all 6,242 drops with the proposed year-first rule
BEFORE editing the generator.

Rule prototyped (new 0.90 path, YEAR_FIRST):
  a standalone 19xx/20xx year, then whitespace/dash, then a canonical
  month word, then whitespace/dash, then a day number. Cause: the
  sentence-year guard (B2-243) correctly kills the inferred-year twin of
  id 7175228 "2041 Dec 31" (the drop quotes the classification banner
  "Declassify On: 20411231"), and no rule reads the year-first shape
  "YYYY Month D" at all, so the drop's one true date (2041-12-31) is
  lost entirely (byte audit:
  watch/inbox/burn_wave_20260926/B2_243_bucket_audit_20260926.md,
  sentence-year class; landing brief B2-258).

Sweeps, in order:
  [DOT/SLASH/DASH] numeric year-first variants "YYYY.MM.D", "YYYY/M/D",
    "YYYY-M-D" across all sentences, checked against the current module's
    output: ISO (0.95) covers YYYY-MM-DD, NUM_Y (0.90) covers the slash
    and dash forms, DOT_Y does NOT match a 4-digit leading year. The sweep
    reports every corpus site and whether the current module already
    extracts it; any unhandled site would widen this lane's rule and must
    be disclosed before the edit.
  [YEAR_FIRST] the month-word rule above across all sentences. Expected:
    exactly one site, id 7175228 "2041 Dec 31" -> 2041-12-31 at 0.90.
  [TARGET] the current (pre-edit) module yields NO row for the target
    sentence: MDY/DMY match "Dec 31" yearless, infer 2019 from the drop
    ts, and SENT_YEAR_RE kills the row because the sentence prints 2041.

Expected PASS: [YEAR_FIRST] fires on exactly id 7175228, [DOT/SLASH/DASH]
finds zero corpus sites (or all sites already extracted at >= 0.90), and
the target sentence currently yields zero rows.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# probe lives in watch/inbox/burn_wave_20260926/: parents[3] is the repo root
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import the50_t21_q_caption_ledger as gen  # noqa: E402  (pre-edit module)

SRC = ROOT / "watch" / "inbox" / "qdrop_export" / "qdrops.jsonl"

DASH = gen.DASH
MONTH_RE = gen.MONTH_RE
CANONICAL_MONTHS = gen.CANONICAL_MONTHS
SENT_YEAR_RE = gen.SENT_YEAR_RE

# proposed year-first month-word rule (the candidate this probe vets);
# MONTH_RE stays unwrapped so group 2 is the month stem and group 3 the day,
# same convention as the generator's DMY
YEAR_FIRST = re.compile(
    rf"\b((?:19|20)\d{{2}}){DASH}{MONTH_RE}{DASH}(\d{{1,2}})(?:st|nd|rd|th)?\b",
    re.IGNORECASE,
)
# numeric year-first variants: dot/slash/dash, both parts numeric
NUM_YEAR_FIRST = re.compile(r"(?<!\d)(?:19|20)\d{2}\s*[./-]\s*\d{1,2}\s*[./-]\s*\d{1,2}(?!\d)")


def month_word(sent: str, stem_start: int) -> str:
    m = re.match(r"[A-Za-z]+", sent[stem_start:])
    return m.group(0).lower() if m else ""


def main():
    yearfirst, variants, target_rows = [], [], []
    with SRC.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            drop = json.loads(line)
            raw = drop.get("text") or ""
            if not raw.strip():
                continue
            text = gen.clean_text(raw)
            for sent in gen.sentences(text):
                # [DOT/SLASH/DASH] first, per the brief: numeric year-first
                for m in NUM_YEAR_FIRST.finditer(sent):
                    tok = m.group(0)
                    parts = [p.strip() for p in re.split(r"\s*[./-]\s*", tok)]
                    cur = [(d, c) for d, _, c in gen.extract(drop)]
                    y, a, b = int(parts[0]), int(parts[1]), int(parts[2])
                    cands = set()
                    for mo, dd in ((a, b), (b, a)):
                        try:
                            datetime(y, mo, dd)
                            cands.add(f"{y:04d}-{mo:02d}-{dd:02d}")
                        except ValueError:
                            pass
                    handled = any(d in cands and c >= 0.9 for d, c in cur)
                    variants.append((str(drop.get("id")), tok, sorted(cur),
                                     sorted(cands), handled, sent[:90]))
                # [YEAR_FIRST] proposed month-word rule
                for m in YEAR_FIRST.finditer(sent):
                    if month_word(sent, m.start(2)) not in CANONICAL_MONTHS:
                        continue
                    y, mo_stem, d = int(m.group(1)), m.group(2).lower()[:3], int(m.group(3))
                    mo = 9 if mo_stem == "sept" else gen.MONTHS[mo_stem]
                    try:
                        datetime(y, mo, d)
                    except ValueError:
                        continue  # not a real calendar date
                    yearfirst.append((str(drop.get("id")), f"{y:04d}-{mo:02d}-{d:02d}", sent[:110]))
                # [TARGET] current-module rows for the target sentence
                if str(drop.get("id")) == "7175228" and "2041 Dec 31" in sent:
                    rows = [(d, c) for d, _, c in gen.extract(drop)]
                    target_rows.append((sent[:80], rows))

    print(f"[DOT/SLASH/DASH] numeric year-first variant sites: {len(variants)}")
    for v in variants:
        print("   ", v)
    print(f"[YEAR_FIRST] proposed-rule sites: {len(yearfirst)}")
    for r in yearfirst:
        print("   ", r)
    print(f"[TARGET] current rows for the '2041 Dec 31' sentence: {target_rows}")

    # Phase-aware PASS: the rule fires on exactly id 7175228 in both phases.
    #   pre-edit:  the target sentence yields no row (SENT_YEAR_RE kills it)
    #   post-edit: the target sentence yields exactly (2041-12-31, 0.9)
    # so the instrument stays rerunnable after the landing (the B2-243 probe
    # practice: rerun post-landing as a regression pin).
    has_rule = hasattr(gen, "YEAR_FIRST")
    target_ok = False
    phase = "post-edit" if has_rule else "pre-edit"
    if has_rule:
        target_ok = (
            len(target_rows) == 1
            and target_rows[0][1] == [("2041-12-31", 0.9)]
        )
    else:
        target_ok = (
            len(target_rows) == 1
            and all(not rows for _, rows in target_rows)
        )
    ok = (
        len(yearfirst) == 1
        and yearfirst[0][0] == "7175228"
        and yearfirst[0][1] == "2041-12-31"
        and target_ok
        and len(variants) == 0
    )
    if ok:
        print(f"PROBE RESULT: PASS ({phase}: 1 YEAR_FIRST site = id 7175228 "
              "-> 2041-12-31; 0 numeric year-first dot/slash/dash sites in "
              f"the corpus; target sentence rows: {target_rows[0][1]})")
        return 0
    print("PROBE RESULT: REVIEW")
    return 1


if __name__ == "__main__":
    sys.exit(main())
