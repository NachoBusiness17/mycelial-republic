#!/usr/bin/env python
"""B2-311 probe: whole-drop year context (clause 2b) swept over all drops
BEFORE any generator edit.

Clause 2b prototype (month-name no-year path, MDY/DMY only, fires ONLY where
the landed clause 2 adjacent-window did NOT fire): the single distinct
standalone 19xx/20xx year printed ANYWHERE in the same drop replaces the
nearest-year inference; abstain when the drop prints zero years or when
printed years disagree (2+ distinct); the year only applies when it yields a
valid date. Candidate of record: id 437 "on 21 July" held 2018-07-21 by
nearest-year while the drop's only printed year is "NOV 2017" (sentence 9).

Falsifier (QUEUE.md B2-311): the sweep must name every 0.75 row a
drop-scoped clause would move beyond id 437, and the 49 clean keepers plus
the 7 held judgment rows (the 8 B2-243 judgment pairs minus 7643939, which
the landed clause 2 already re-dated) must not move. Any move among them ->
the clause does not land (exit 1, probe-only evidence).

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_311_drop_year_probe.py
Exits 0 when the clause is safe to consider (moves are 437-only or none),
1 when keepers or held rows would move.
"""
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import the50_t21_q_caption_ledger as gen  # noqa: E402

SRC = ROOT / "watch" / "inbox" / "qdrop_export" / "qdrops.jsonl"
LEDGER = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "B2_257_ledger_before.jsonl"

# the 8 B2-243 judgment (id, date) pairs; 7643939 already re-dated by the
# landed clause 2 (B2-257), so the held set is the other 7
JUDGMENT_PAIRS = {
    ("9298758", "2020-01-05"),
    ("437", "2018-07-21"),
    ("5320727", "2019-02-06"),
    ("5320727", "2019-04-15"),
    ("7643939", "2019-07-09"),
    ("9158650", "2019-11-30"),
    ("60150", "2017-11-04"),
}
HELD = JUDGMENT_PAIRS - {("7643939", "2019-07-09")}
MOVED_BY_CLAUSE2 = {("7643939", "2016-07-09")}  # current landed state


def month_word(sent: str, stem_start: int) -> str:
    m = __import__("re").match(r"[A-Za-z]+", sent[stem_start:])
    return m.group(0).lower() if m else ""


def whole_drop_year(sents):
    """Clause 2b prototype: the single distinct standalone 19xx/20xx year
    anywhere in the drop; None on zero or 2+ distinct years."""
    years = set()
    for s in sents:
        years |= set(gen.SENT_YEAR_RE.findall(s or ""))
    if len(years) == 1:
        return int(years.pop())
    return None


def main() -> int:
    rows = [json.loads(l) for l in LEDGER.open(encoding="utf-8") if l.strip()]
    live_075 = Counter((r["id"], r["date"]) for r in rows if r["confidence"] == 0.75)

    # the clause-2 (adjacent) inference, re-derived, so 2b only fills its gaps
    import re

    def adjacent_year(sents, si):
        prev_sent = sents[si - 1] if si else ""
        next_sent = sents[si + 1] if si + 1 < len(sents) else ""
        years = set(gen.SENT_YEAR_RE.findall(prev_sent or "")) | set(
            gen.SENT_YEAR_RE.findall(next_sent or ""))
        return int(next(iter(years))) if len(years) == 1 else None

    clause3_multiset = Counter()
    sites = []  # (path, id, old_iso, new_iso, drop_year, n_sents, sent[:80])
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
            dy = whole_drop_year(sents)
            for si, sent in enumerate(sents):
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
                            continue  # clause 1 explicit-year path
                        y = gen.infer_year(ts, mo, d) if ts else None
                        if not y:
                            continue
                        yr = gen.SENT_YEAR_RE.search(sent)
                        if yr and int(yr.group(0)) != y:
                            continue  # B2-243 sentence-year contradiction
                        old = gen.mk_date(y, mo, d)
                        if old is None:
                            continue
                        clause3_multiset[(str(drop.get("id")), old.isoformat())] += 1
                        ay = adjacent_year(sents, si)
                        if ay is not None and ay != y and gen.mk_date(ay, mo, d):
                            continue  # landed clause 2 owns this site
                        if dy is None or dy == y:
                            continue  # clause 3 nearest-year stands
                        new = gen.mk_date(dy, mo, d)
                        if new is None:
                            continue  # valid-date guard
                        sites.append((path, str(drop.get("id")), old.isoformat(),
                                      new.isoformat(), dy, len(sents), sent[:80]))

    got = clause3_multiset
    print(f"clause-3 site multiset vs live ledger 0.75 multiset: "
          f"{'EQUAL' if got == live_075 else 'DIFF'}")

    print(f"\nclause-2b (whole-drop year) delta sites: {len(sites)}")
    for s in sites:
        print(f"   {s[0]} id {s[1]} {s[2]} -> {s[3]} (drop year {s[4]}, "
              f"drop has {s[5]} sentences): {s[6]}")

    beyond_437 = [s for s in sites if s[1] != "437"]
    print(f"\nmoves beyond id 437 (the falsifier must name these): {len(beyond_437)}")
    for s in beyond_437:
        print(f"   BEYOND-437 {s[0]} id {s[1]} {s[2]} -> {s[3]}")

    keepers_violated = [s for s in beyond_437
                        if (s[1], s[2]) not in HELD | MOVED_BY_CLAUSE2]
    held_violated = [s for s in beyond_437 if (s[1], s[2]) in HELD]
    print(f"\ninvariant violations: keepers moved {len(keepers_violated)}, "
          f"held judgment rows moved {len(held_violated)}")

    print("\ndisposition of the held 7 judgment (id, date) rows:")
    moved = {(s[1], s[2]): s[3] for s in sites}
    for pair in sorted(HELD):
        if pair in moved:
            label = ("2B MOVES (candidate of record, expected)"
                     if pair == ("437", "2018-07-21")
                     else "2B WOULD MOVE (invariant violation)")
            print(f"   {label}: {pair[0]} {pair[1]} -> {moved[pair]}")
        elif pair == ("437", "2018-07-21"):
            print(f"   2B CANDIDATE OF RECORD: {pair[0]} {pair[1]} -> "
                  f"{moved.get(pair)}" if pair in moved else
                  f"   2B CANDIDATE OF RECORD: {pair[0]} {pair[1]} -> NO MOVE")
        else:
            print(f"   HELD: {pair[0]} {pair[1]}")

    ok = got == live_075 and not keepers_violated and not held_violated
    verdict = ("PASS (clause 2b moves only 437 or nothing; 49 keepers + 7 held rows stand)"
               if ok else "FAIL (clause does not land)")
    print(f"\nPROBE RESULT: {verdict}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
