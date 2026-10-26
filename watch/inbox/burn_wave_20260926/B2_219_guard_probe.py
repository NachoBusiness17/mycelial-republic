#!/usr/bin/env python
"""B2-219 probe: sweep the full corpus for NUM_NOY candidates the proposed
unit/tally guards would newly reject. Read-only; prints every rejection with
its sentence so the guards' blast radius is byte-verifiable before the edit.

Guards under test (all dash-separator only; slash pairs are untouched):
  BRACKET_REF   pair touches a square bracket (lead "[" or tail "]")
                - "[D][1-6]", "[CLAS 1-9]", "[10-9]", "cross 1-9]"
  PAREN_TALLY   pair fully parenthesized (lead "(" and tail ")")
                - "(6-3)" SC vote tally, "(5-6)" operational window
  AGE_RANGE     "ages? " immediately before the pair - "(ages 8-9)"
  MEASURE_AFTER unit noun right after the pair - "10-30 feet"
  TALLY_ONE     first number is 1 - "ARTICLES 1-9", "establish 1-7",
                "ALLEGATIONS 1-9" (numbered-list reference reads)
  COUNT_NP_BEFORE plural count noun immediately before - "alerts 5-12"
  RANGE_LIST    pair followed by ", N-M" - "5-3, 1-99"

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_219_guard_probe.py
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # probe lives 3 deep under repo root
sys.path.insert(0, str(ROOT / "scripts"))
from the50_t21_q_caption_ledger import (  # noqa: E402
    SRC, NUM_NOY, LEAD_OK, TAIL_OK, SKIP_MD, ORDINAL_RE, QUANTITY, FRACTIONS,
    PROPORTION_RE, clean_text, mk_date, infer_year,
)

MEASURE_AFTER_RE = re.compile(
    r"\s(?:feet|foot|inches|inch|meters|miles|acres|degrees|fathoms)\b",
    re.IGNORECASE,
)
AGE_BEFORE_RE = re.compile(r"\bages?\s+$", re.IGNORECASE)
COUNT_NP_BEFORE_RE = re.compile(r"\b\S+s\s+$", re.IGNORECASE)
RANGE_LIST_RE = re.compile(r"^\s*,\s*\d{1,3}\s*-\s*\d{1,3}\b")

# the 15 (id, iso-date) rows the 2026-09-26 byte audit classified as misdates
TARGETS = {
    ("173382", "2017-10-09"), ("173382", "2018-05-06"),
    ("476806", "2018-05-12"), ("893904", "2018-01-09"),
    ("5123210", "2019-06-03"), ("7182803", "2019-08-09"),
    ("7182803", "2019-10-30"), ("7355626", "2020-01-09"),
    ("7357987", "2020-01-06"), ("95", "2020-01-06"),
    ("7535766", "2020-05-03"), ("9081684", "2020-01-09"),
    ("9081684", "2020-01-07"), ("9105563", "2020-01-09"),
    ("9298758", "2020-01-09"),
}
# the 16 genuine-date rows that must survive every new guard
KEEPERS = {
    ("147012719", "2017-10-30"), ("121327", "2017-12-07"),
    ("121327", "2017-12-17"), ("121553", "2017-12-07"),
    ("178973", "2017-12-21"), ("594193", "2017-11-11"),
    ("914092", "2018-04-03"), ("1181379", "2018-01-20"),
    ("1702926", "2018-06-11"), ("1795201", "2018-06-27"),
    ("1795201", "2018-06-28"), ("1795201", "2018-06-29"),
    ("2950871", "2018-09-16"), ("2950871", "2018-09-14"),
    ("5139710", "2018-09-26"),
}


def new_guard(mo, d, lead, tail, before, after):
    if lead == "[" or tail == "]":
        return "BRACKET_REF"
    if lead == "(" and tail == ")":
        return "PAREN_TALLY"
    if AGE_BEFORE_RE.search(before):
        return "AGE_RANGE"
    if MEASURE_AFTER_RE.match(after):
        return "MEASURE_AFTER"
    if mo == 1:
        return "TALLY_ONE"
    if COUNT_NP_BEFORE_RE.search(before):
        return "COUNT_NP_BEFORE"
    if RANGE_LIST_RE.match(after):
        return "RANGE_LIST"
    return None


def main() -> int:
    rejected = {}   # (id, iso) -> (guard, sentence)
    surviving = 0
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
                    near = sent[max(0, m.start() - 12): m.end() + 12]
                    if QUANTITY.search(near):
                        continue
                    dt = mk_date(infer_year(ts, mo, d), mo, d) if ts else None
                    if dt is None:
                        continue
                    surviving += 1
                    sep = re.search(r"[/-]", m.group(0)).group(0)
                    if sep != "-":
                        continue
                    guard = new_guard(
                        mo, d,
                        sent[: m.start()][-1:] or "",
                        sent[m.end(): m.end() + 1] or "",
                        sent[: m.start()],
                        sent[m.end():],
                    )
                    if guard:
                        key = (did, dt.isoformat())
                        if key not in rejected:
                            rejected[key] = (guard, sent[:110])
                            print(f"REJECT {guard} id={did} {dt.isoformat()} "
                                  f"pair={mo}-{d} sent={sent[:110]!r}")
    hits = set(rejected)
    keeper_hits = sorted(hits & KEEPERS)
    missed = sorted(TARGETS - hits)
    print(f"NUM_NOY surviving existing guards: {surviving}")
    print(f"new-guard rejections (distinct id+date): {len(hits)}")
    print(f"keeper rows newly rejected: {keeper_hits or 'NONE'}")
    print(f"target rows not fired on: {missed or 'NONE'}")
    ok = not keeper_hits and not missed and hits == TARGETS
    print("PROBE RESULT:", "PASS" if ok else "FAIL")
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
