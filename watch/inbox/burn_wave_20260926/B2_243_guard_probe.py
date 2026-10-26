#!/usr/bin/env python
"""B2-243 probe: sweep all 6,242 drops with the proposed 0.75-path guards
BEFORE editing the generator.

Guards prototyped (month-name path, MDY/DMY):
  [MONTH] canonical-month-word check: the full alphabetic token holding the
    month stem must be a canonical month word (jan..dec, january..december,
    sept). Cause: 9 audited misdate rows where a 3-letter month stem swallowed
    a longer word ("1st marker", "10/15 marker", "3rd Marine", "decide 2",
    "Marker 1", "declassified 22", "8 DECLAS", "DECLAS 1-99"; byte audit
    watch/inbox/burn_wave_20260926/B2_243_bucket_audit_20260926.md).
  [YEAR] explicit-year contradiction check on the no-year path: if the
    sentence contains a standalone 19xx/20xx year different from the inferred
    year, reject. Cause: 2 audited misdate rows ("October 24 ... October 24,
    2013" held as 2019-10-24; "2041 Dec 31" held as 2019-12-31).

Expected PASS: [MONTH] fires on exactly the 9 audited sites (+ any disclosed
siblings on the 0.90/0.55 paths), [YEAR] fires on exactly the 2 audited
sites, keeper (surviving 0.75) hits = 57 sites matching the 57 audited
keeper rows, and 0 of the 15 dotted 0.5 rows are touched.

B2-257 amendment (2026-09-26, per the B2-259 maintenance law): the
generator's year ladder landed clause 2 (adjacent-sentence year) after
this probe was written, re-dating the judgment-class row id 7643939
2019-07-09 -> 2016-07-09 (re-audit in
watch/inbox/burn_wave_20260926/B2_257_year_ladder_20260926.md), so the
keeper-year computation below mirrors clause 2 to keep tracking the live
ledger's 0.75 multiset. [MONTH]/[YEAR] rejections are untouched by the
ladder (clause 2 applies only after the [YEAR] guard passes).
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# probe lives in watch/inbox/burn_wave_20260926/: parents[3] is the repo root
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import the50_t21_q_caption_ledger as gen  # noqa: E402  (pre-edit module for helpers)

SRC = ROOT / "watch" / "inbox" / "qdrop_export" / "qdrops.jsonl"
LEDGER = ROOT / "watch" / "inbox" / "qdrop_export" / "q_caption_ledger.jsonl"

CANONICAL_MONTHS = {
    "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "sept",
    "oct", "nov", "dec",
    "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december",
}
YEAR_IN_SENT_RE = re.compile(r"\b(?:19|20)\d{2}\b")

MONTH_RE = gen.MONTH_RE
DASH = gen.DASH
MDY = gen.MDY
DMY = gen.DMY
MONTH_YEAR = gen.MONTH_YEAR


def month_word(sent: str, stem_start: int) -> str:
    m = re.match(r"[A-Za-z]+", sent[stem_start:])
    return m.group(0).lower() if m else ""


def adj_year(prev_sent: str, next_sent: str):
    """B2-257 ladder clause 2: single distinct 19xx/20xx year across the
    two adjacent sentences, None when absent or contradictory."""
    years = set(gen.SENT_YEAR_RE.findall(prev_sent or "")) | set(
        gen.SENT_YEAR_RE.findall(next_sent or "")
    )
    return int(years.pop()) if len(years) == 1 else None


def main():
    month_rej, year_rej, keep = [], [], []
    with SRC.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            drop = json.loads(line)
            raw = drop.get("text") or ""
            if not raw.strip():
                continue
            try:
                ts = datetime.fromisoformat(drop["ts"])
            except (KeyError, ValueError):
                ts = None
            text = gen.clean_text(raw)
            sents = list(gen.sentences(text))
            for si, sent in enumerate(sents):
                prev_sent = sents[si - 1] if si else ""
                next_sent = sents[si + 1] if si + 1 < len(sents) else ""
                for m in MDY.finditer(sent):
                    word = month_word(sent, m.start(1))
                    if word not in CANONICAL_MONTHS:
                        month_rej.append(("MDY", str(drop.get("id")), word, m.group(0).strip(), sent[:110]))
                        continue
                    mo = gen.MONTHS[m.group(1).lower()[:3]] if m.group(1).lower()[:3] != "sept" else 9
                    d = int(m.group(2))
                    if m.group(3):
                        continue  # explicit-year path (0.90), untouched by guards
                    y = gen.infer_year(ts, mo, d) if ts else None
                    if not y:
                        continue
                    yr = YEAR_IN_SENT_RE.search(sent)
                    if yr and int(yr.group(0)) != y:
                        year_rej.append(("MDY", str(drop.get("id")), yr.group(0), m.group(0).strip(), sent[:110]))
                        continue
                    if not YEAR_IN_SENT_RE.search(sent):
                        ay = adj_year(prev_sent, next_sent)
                        if ay is not None and ay != y and gen.mk_date(ay, mo, d):
                            y = ay  # B2-257 ladder clause 2
                    keep.append(("MDY", str(drop.get("id")), f"{y:04d}-{mo:02d}-{d:02d}", sent[:110]))
                for m in DMY.finditer(sent):
                    word = month_word(sent, m.start(2))
                    if word not in CANONICAL_MONTHS:
                        month_rej.append(("DMY", str(drop.get("id")), word, m.group(0).strip(), sent[:110]))
                        continue
                    mo = gen.MONTHS[m.group(2).lower()[:3]] if m.group(2).lower()[:3] != "sept" else 9
                    d = int(m.group(1))
                    if m.group(3):
                        continue  # explicit-year path (0.90), untouched by guards
                    y = gen.infer_year(ts, mo, d) if ts else None
                    if not y:
                        continue
                    yr = YEAR_IN_SENT_RE.search(sent)
                    if yr and int(yr.group(0)) != y:
                        year_rej.append(("DMY", str(drop.get("id")), yr.group(0), m.group(0).strip(), sent[:110]))
                        continue
                    if not YEAR_IN_SENT_RE.search(sent):
                        ay = adj_year(prev_sent, next_sent)
                        if ay is not None and ay != y and gen.mk_date(ay, mo, d):
                            y = ay  # B2-257 ladder clause 2
                    keep.append(("DMY", str(drop.get("id")), f"{y:04d}-{mo:02d}-{d:02d}", sent[:110]))
                for m in MONTH_YEAR.finditer(sent):
                    word = month_word(sent, m.start(1))
                    if word not in CANONICAL_MONTHS:
                        month_rej.append(("MONTH_YEAR", str(drop.get("id")), word, m.group(0).strip(), sent[:110]))

    print(f"[MONTH] canonical rejections: {len(month_rej)}")
    for r in month_rej:
        print("   ", r[0], "id", r[1], "word:", r[2], "|", r[3], "|", r[4])
    print(f"[YEAR] year-contradiction rejections: {len(year_rej)}")
    for r in year_rej:
        print("   ", r[0], "id", r[1], "sent-year:", r[2], "|", r[3], "|", r[4])
    print(f"keeper surviving no-year month-name sites: {len(keep)}")

    # cross-check keepers against the ledger's non-rejected 0.75 rows
    rows = [json.loads(l) for l in LEDGER.open(encoding="utf-8") if l.strip()]
    audited_reject = {
        ("147449624", "2018-03-01"), ("158980", "2018-03-10"), ("158980", "2018-03-15"),
        ("894571", "2018-03-03"), ("1784355", "2018-12-02"), ("5705810", "2019-03-01"),
        ("7175228", "2019-12-22"), ("7517929", "2019-12-08"), ("9730975", "2020-12-01"),
        ("7039606", "2019-10-24"), ("7175228", "2019-12-31"),
    }
    rej_rows = [(r[1]) for r in month_rej + year_rej]
    target_reject_ids = {k[0] for k in audited_reject}
    extra_month_ids = {r[1] for r in month_rej} - target_reject_ids
    extra_year_ids = {r[1] for r in year_rej} - target_reject_ids
    # expected keeper multiset: ledger 0.75 rows minus the audited 11, keyed (id, date)
    from collections import Counter
    expect = Counter((r["id"], r["date"]) for r in rows
                     if r["confidence"] == 0.75 and (r["id"], r["date"]) not in audited_reject)
    got = Counter((r[1], r[2]) for r in keep)
    if (not extra_month_ids and not extra_year_ids
            and len(month_rej) == 9 and len(year_rej) == 2
            and {r[1] for r in month_rej + year_rej} == {k[0] for k in audited_reject}
            and expect == got):
        print("PROBE RESULT: PASS (9 MONTH + 2 YEAR = 11 rejections, exactly the audited misdate rows; 57 keeper sites match the surviving ledger 0.75 multiset)")
        return 0
    print("PROBE RESULT: REVIEW")
    print("  extra MONTH ids:", sorted(extra_month_ids))
    print("  extra YEAR ids:", sorted(extra_year_ids))
    print("  rejection counts: MONTH", len(month_rej), "YEAR", len(year_rej))
    print("  keeper multiset diff: missing", sorted((expect - got).items())[:10])
    print("  keeper multiset diff: extra", sorted((got - expect).items())[:10])
    return 1


if __name__ == "__main__":
    sys.exit(main())
