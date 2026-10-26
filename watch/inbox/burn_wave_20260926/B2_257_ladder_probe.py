#!/usr/bin/env python
"""B2-257 probe: sweep all 6,242 drops with the proposed year ladder
BEFORE editing the generator.

Ladder prototyped (month-name no-year path, MDY/DMY only; the 0.65/0.50
nearest-year paths are out of scope per the brief):
  clause 1  explicit year in the sentence (already mechanical: the year
            attached to the match emits 0.90; a standalone year contradicting
            the inference is dropped by SENT_YEAR_RE, both landed by B2-243)
  clause 2  when the sentence itself prints no year at all: a single distinct
            standalone 19xx/20xx year found across the two sentences adjacent
            to the match's sentence (same drop) replaces the inference; both
            sides carrying different years abstains (nearest-year stands);
            the adjacent year only applies when it yields a valid date
  clause 3  nearest-year rule (landed behavior, unchanged)

Expected PASS: the clause-2 delta set is a subset of the 8 judgment-class
(id, date) rows of the B2-243 audit (receipt
watch/inbox/burn_wave_20260926/B2_243_bucket_audit_20260926.md Evidence,
judgment list), none of the other 49 audited 0.75 keeper rows move, and the
projected ledger diff is exactly len(deltas) pure modifications with zero
additions and zero deletions. The site multiset at clause-3 years must equal
the live ledger's 0.75 multiset (the B2-243 guard-probe precondition).

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_257_ladder_probe.py
Exits 0 on PASS, 1 on FAIL.
"""
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import the50_t21_q_caption_ledger as gen  # noqa: E402  (pre-edit module)

SRC = ROOT / "watch" / "inbox" / "qdrop_export" / "qdrops.jsonl"
BEFORE = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "B2_257_ledger_before.jsonl"

# the 8 judgment-class (id, date) rows held by the B2-243 audit (the
# 9298758 pair shares one (id, date))
JUDGMENT_PAIRS = {
    ("9298758", "2020-01-05"),
    ("437", "2018-07-21"),
    ("5320727", "2019-02-06"),
    ("5320727", "2019-04-15"),
    ("7643939", "2019-07-09"),
    ("9158650", "2019-11-30"),
    ("60150", "2017-11-04"),
}


def month_word(sent: str, stem_start: int) -> str:
    m = re.match(r"[A-Za-z]+", sent[stem_start:])
    return m.group(0).lower() if m else ""


def adjacent_year(prev_sent: str, next_sent: str):
    """Clause 2 prototype: single distinct 19xx/20xx year across the two
    adjacent sentences; None when absent or contradictory."""
    years = set(gen.SENT_YEAR_RE.findall(prev_sent or "")) | set(
        gen.SENT_YEAR_RE.findall(next_sent or "")
    )
    if len(years) == 1:
        return int(years.pop())
    return None


def main() -> int:
    before_rows = [
        json.loads(l) for l in BEFORE.open(encoding="utf-8") if l.strip()
    ]
    before_075 = Counter(
        (r["id"], r["date"]) for r in before_rows if r["confidence"] == 0.75
    )

    sites = []  # (path, id, old_iso, new_iso, side, adj_year, sent[:90])
    raw = []  # clause-3 site multiset (path, id, old_iso)
    with SRC.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            drop = json.loads(line)
            if not (drop.get("text") or "").strip():
                continue
            try:
                ts = datetime.fromisoformat(drop["ts"])
            except (KeyError, ValueError):
                ts = None
            text = gen.clean_text(drop["text"])
            sents = list(gen.sentences(text))
            for si, sent in enumerate(sents):
                prev_sent = sents[si - 1] if si else ""
                next_sent = sents[si + 1] if si + 1 < len(sents) else ""
                for path, regex, gmo, gday in (
                    ("MDY", gen.MDY, 1, 2),
                    ("DMY", gen.DMY, 2, 1),
                ):
                    for m in regex.finditer(sent):
                        if month_word(sent, m.start(gmo)) not in gen.CANONICAL_MONTHS:
                            continue
                        stem = m.group(gmo).lower()[:3]
                        mo = 9 if stem == "sept" else gen.MONTHS[stem]
                        d = int(m.group(gday))
                        if (mo, d) in gen.SKIP_MD and not m.group(3):
                            continue
                        if m.group(3):
                            continue  # clause 1 explicit-year path (0.90)
                        y = gen.infer_year(ts, mo, d) if ts else None
                        if not y:
                            continue
                        yr = gen.SENT_YEAR_RE.search(sent)
                        if yr and int(yr.group(0)) != y:
                            continue  # B2-243 sentence-year contradiction
                        old = gen.mk_date(y, mo, d)
                        if old is None:
                            continue
                        raw.append((path, str(drop.get("id")), old.isoformat()))
                        ay = adjacent_year(prev_sent, next_sent)
                        if ay is None or ay == y or gen.mk_date(ay, mo, d) is None:
                            continue  # clause 3 nearest-year stands
                        new = gen.mk_date(ay, mo, d)
                        side = (
                            "prev" if gen.SENT_YEAR_RE.search(prev_sent or "") else ""
                        ) + ("next" if gen.SENT_YEAR_RE.search(next_sent or "") else "")
                        sites.append((
                            path, str(drop.get("id")), old.isoformat(),
                            new.isoformat(), side, ay, sent[:90],
                        ))

    got = Counter((r[1], r[2]) for r in raw)
    print(f"clause-3 site multiset vs live ledger 0.75 multiset: "
          f"{'EQUAL' if got == before_075 else 'DIFF'}")
    if got != before_075:
        print("  missing:", sorted((before_075 - got).items())[:8])
        print("  extra:", sorted((got - before_075).items())[:8])

    print(f"\nclause-2 delta sites: {len(sites)}")
    for s in sites:
        print(f"   {s[0]} id {s[1]} {s[2]} -> {s[3]} (adj year {s[5]}, "
              f"side {s[4] or 'both-equal'}): {s[6]}")

    non_judgment = [s for s in sites if (s[1], s[2]) not in JUDGMENT_PAIRS]
    print(f"\ndeltas outside the 8 judgment rows: {len(non_judgment)}")
    for s in non_judgment:
        print(f"   VIOLATION {s[0]} id {s[1]} {s[2]} -> {s[3]}")

    # judgment disposition table: which of the 8 the ladder re-dates
    print("\ndisposition of the 8 judgment (id, date) rows:")
    moved = {(s[1], s[2]): s[3] for s in sites}
    for pair in sorted(JUDGMENT_PAIRS):
        if pair in moved:
            print(f"   RE-DATED clause 2: {pair[0]} {pair[1]} -> {moved[pair]}")
        else:
            print(f"   HELD clause 3:     {pair[0]} {pair[1]}")

    # projected ledger: pure modifications only
    delta_map = {(s[1], s[2]): s[3] for s in sites}
    projected, modifications = [], 0
    for r in before_rows:
        key = (r["id"], r["date"])
        if r["confidence"] == 0.75 and key in delta_map:
            modifications += 1
            projected.append({**r, "date": delta_map[key]})
        else:
            projected.append(r)
    before_m = Counter((r["id"], r["date"], r["claim"], r["confidence"])
                       for r in before_rows)
    proj_m = Counter((r["id"], r["date"], r["claim"], r["confidence"])
                     for r in projected)
    # a pure modification is one removal + one addition at full-tuple
    # granularity: the removed tuples must be exactly the deltas' old rows
    # and the added tuples exactly their new rows, counts equal, and the
    # row count unchanged
    removed_m = before_m - proj_m
    added_m = proj_m - before_m
    want_removed = Counter()
    want_added = Counter()
    for r in before_rows:
        key = (r["id"], r["date"])
        if r["confidence"] == 0.75 and key in delta_map:
            want_removed[(r["id"], r["date"], r["claim"], r["confidence"])] += 1
            want_added[(r["id"], delta_map[key], r["claim"], r["confidence"])] += 1
    exact = removed_m == want_removed and added_m == want_added
    print(f"\nprojected ledger: {len(before_rows)} -> {len(projected)} rows, "
          f"modifications {modifications}, removed tuples {sum(removed_m.values())}, "
          f"added tuples {sum(added_m.values())}, exact-delta-diff {exact}")

    ok = (got == before_075 and not non_judgment and exact
          and len(projected) == len(before_rows)
          and modifications == len(sites))
    print(f"\nPROBE RESULT: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
