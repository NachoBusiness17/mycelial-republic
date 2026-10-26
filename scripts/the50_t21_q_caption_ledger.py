#!/usr/bin/env python
"""THE 50 / T21 (W5): Q caption ledger.

Reads watch/inbox/qdrop_export/qdrops.jsonl (6242 Q drops, harvested 2026-09-18
from https://qanon.pub/data/json/posts.json) and extracts DATED CLAIMS: one row
per (drop, sentence, date) where a specific calendar date is named in the text.

Output: watch/inbox/qdrop_export/q_caption_ledger.jsonl
Schema per row: {"id", "date", "claim", "confidence"}
  id         = qdrops.jsonl post "id" (join key back to the source corpus)
  date       = normalized ISO date "YYYY-MM-DD", or "YYYY-MM" for month-year
               precision claims (confidence reflects the coarser precision)
  claim      = the sentence (cleaned of HTML entities/tags, reply markers,
               URLs) that carries the date, max 320 chars
  confidence = extraction confidence 0..1, rubric below

Confidence rubric (mechanical, deterministic):
  0.95  ISO date in text (YYYY-MM-DD)
  0.90  explicit year + month name/day or numeric m/d/y (10/30/17, Oct 30,
        2017; year-first "2041 Dec 31" since B2-258, sweep below)
  0.75  month name + day, year inferred (year ladder below; dash-separated
        forms like "SEPT —-17" count here; the month word must be canonical
        and the sentence must not print a different year, both below)
  0.65  numeric m/d, no year, year inferred (excludes proportion reads:
        proper fraction followed by a plural-head noun phrase, below;
        and dash-pair unit/tally/reference reads, below)
  0.55  month-year only ("July 2018")
  0.50  Q cipher dotted m.d with both parts <= 12 ("11.3", "11.4"; m/d vs d/m
        ambiguous, conventional reading is month.day; corpus-audited
        2026-09-26: all 15 rows are genuine cipher markers, receipt
        watch/inbox/burn_wave_20260926/B2_243_bucket_audit_20260926.md)
  0.40  dotted token only valid as day.month ("13.4" -> 4th of ...)

Year ladder (when the text gives no year): the month-name paths (0.75)
resolve the year in three clauses, first match wins:
  clause 1  explicit year in the sentence: attached to the match it emits
            0.90; a standalone sentence year contradicting the inference
            drops the row (SENT_YEAR_RE guard, B2-243)
  clause 2  the sentence prints no year at all and the two sentences
            adjacent to it (same drop) print exactly one distinct
            standalone 19xx/20xx year: that year replaces the inference;
            the two adjacent sides printing different years abstains, and
            the adjacent year applies only when it yields a valid
            calendar date (else clause 3 stands). Cause: the 8 judgment-
            class rows of the B2-243 audit (byte audit of all 68 residual
            0.75 rows, watch/inbox/burn_wave_20260926/
            B2_243_bucket_audit_20260926.md) where nearest-year
            contradicted drop context; sweep (B2_257_ladder_probe.py,
            6,242 drops, receipt watch/inbox/burn_wave_20260926/
            B2_257_year_ladder_20260926.md): clause 2 fires on exactly
            one site, id 7643939 "the paper dated July 9" 2019-07-09 ->
            2016-07-09 (the next sentence prints "July 5, 2016"); the
            other 7 judgment rows stay on clause 3
  clause 3  nearest-year: candidate years {drop_year-1, drop_year,
            drop_year+1}; pick the one minimizing |candidate_date -
            drop_ts|, ties resolve to drop_year
The numeric (0.65) and dotted (0.50/0.40) no-year paths keep the bare
nearest-year clause 3.

Exclusions (documented, deliberate):
  - year-first year-MONTH-only ("2041 Dec", no day): no rule reads it, by
    measurement (B2-282, 2026-09-26 full-corpus sweep of 6,242 drops with the
    pattern (?<!\d)(19|20)\d{2}\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*
    plus the dash-join variant: exactly 2 candidate sites, BOTH false or
    subsumed; results watch/inbox/burn_wave_20260926/B2_282_yearmonth_sweep_results.json).
    Site 1842655 "Jan 20, 2017 June 20, 2018" only looks like "2017 June"
    across a line wrap; the June belongs to the following full date. Site
    7175228 "2041 Dec" is a prefix of "2041 Dec 31", which the B2-258
    YEAR_FIRST rule already extracts at 0.90 with the day. A year-MONTH-only
    row (month precision, no day) would mint "2017-06" on the first site and
    duplicate the second at lower precision, so the shape stays unwritten:
    any future classification banner quoting a year-month-only declassification
    date re-opens THIS note with a new sweep, not a silent rule.
  - bare "9/11" without a year (event reference, not a dated claim)
  - numeric m/d pairs that read as proportions: a proper fraction
    (numerator < denominator) immediately followed by a two-token noun
    phrase with a plural head ("7/10 plane crashes are targeted kills",
    drop 34917: seven of ten, not July 10). Kept to proper fractions and
    the two-token plural window so genuine dates ("10/30 across most
    major cities", "9/16") still extract; corpus-verified to fire on
    exactly one site across all 6,242 drops (2026-09-26 sweep,
    B2_68_guard_probe.py)
  - dash-separated numeric pairs that read as units, tallies, or
    reference numerals rather than month-day (2026-09-26 byte audit of
    the 31 residual 0.65 rows: watch/inbox/burn_wave_20260926/
    B2_219_misdate_classes_20260926.md). Seven mechanical predicates,
    dash separator only (every keeper row except "by 11-11" is
    slash-separated; the 2026-09-26 sweep B2_219_guard_probe.py rejects
    exactly the 15 audited misdate rows across 6,242 drops with 0 keeper
    hits):
      * pair touches a square bracket ("[D][1-6]", "[CLAS 1-9]",
        "10, [10-9]", "cross 1-9]") - Q drop/index references
      * pair fully parenthesized ("(6-3)" SC vote tally,
        "Operational_window(5-6)") - scores/tallies, not dates
      * "ages? " before the pair ("$60 (ages 8-9)" - age range,
        drop 7182803)
      * measure noun after the pair ("10-30 feet" - water depth,
        drop 7182803); frequency noun ("4-5 times" - posting rate,
        drop 251705, B2-242)
      * first number 1 ("ARTICLES 1-9", "establish 1-7",
        "ALLEGATIONS 1-9" - numbered-list references)
      * plural count noun before the pair ("Warning alerts 5-12" -
        alert-number range, drop 476806)
      * pair followed by another range ("5-3, 1-99" - coded reference
        pair, drop 7535766)
  - month-name tokens that are not month words: the 3-letter stem
    (mar, dec) swallowing a longer word, then a nearby number completing
    a fake date. Cause: 9 residual 0.75 rows dated non-dates on the
    month-name no-year path (2026-09-26 byte audit of all 68 rows:
    watch/inbox/burn_wave_20260926/B2_243_bucket_audit_20260926.md):
    id 147449624 "once 11.3 verifies as 1st marker" as 2018-03-01,
    id 158980 "Missing 10/15 marker" as 2018-03-10 and 2018-03-15,
    id 894571 "3rd Marine Aircraft Wing" as 2018-03-03, id 1784355
    "have 2 decide" as 2018-12-02, id 5705810 "[Marker 1 Complete]" as
    2019-03-01, id 7175228 "declassified 22" as 2019-12-22, id 7517929
    "GANG of 8 DECLAS" as 2019-12-08, id 9730975 "DECLAS 1-99" as
    2020-12-01. Canonical-month-word guard below; the 2026-09-26 sweep
    (B2_243_guard_probe.py) rejects exactly those 9 sites across 6,242
    drops, 0 on the explicit-year (0.90) path and 0 on MONTH_YEAR (0.55)
  - yearless month-day in a sentence that prints its own year: the
    no-year match is dropped when the sentence contains a standalone
    19xx/20xx year different from the inferred one (2 rows of the same
    audit: id 7039606 "on October 24 at Assouline ... on October 24,
    2013" held as 2019-10-24, correct 2013-10-24 already present at
    0.90; id 7175228 "2041 Dec 31" held as 2019-12-31). The guard still
    kills the inferred-year twin, so 2019-12-31 stays absent; the
    year-first month-word shape "YYYY Month D" extracts at 0.90 since
    B2-258 (2026-09-26 pre-edit sweep: fires on exactly that one site
    across 6,242 drops, receipt watch/inbox/burn_wave_20260926/
    B2_258_yearfirst_20260926.md; numeric dot/slash/dash year-first
    variants have zero corpus sites and ISO/NUM_Y already own the shapes)
  - year-only mentions ("2018") - too coarse
  - dates embedded in URLs (URLs stripped before matching)
  - dotted tokens followed/preceded by quantity words ("3.5 million",
    "$1.5", "1.5 yrs"; yr/yrs are units exactly like years). Unit words
    must stand alone: inside-word hits ("b-day", "today", "coming",
    "attack") are false exclusions, bounded per-alternative in B2-242
    (receipt watch/inbox/burn_wave_20260926/
    B2_242_quantity_bounds_20260926.md); mega/giga-style byte compounds
    ("22.7 megabytes") still count as units
  - dotted tokens that are figure or section numbers ("Figure 3.1",
    "Fig. 2", "Section 5.2"): a document label, not a calendar date
    (section labels joined the figure guard in B2-242)
  - weekday-only references ("Monday") - not calendar dates

Run: .venv/Scripts/python.exe scripts/the50_t21_q_caption_ledger.py
"""
import html
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "watch" / "inbox" / "qdrop_export" / "qdrops.jsonl"
OUT = ROOT / "watch" / "inbox" / "qdrop_export" / "q_caption_ledger.jsonl"

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}
MONTH_RE = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?"

# separator between month and day: whitespace or a dash run (unicode dashes
# included) - Q writes "SEPT —-17—–" with em-dash runs as date markers
DASH = r"[\s\u2010-\u2015\u2212-]+"
# month-first: "Oct 30, 2017" / "October 30" / "Nov. 5th" / "SEPT —-17"
MDY = re.compile(
    rf"\b{MONTH_RE}{DASH}(\d{{1,2}})(?:st|nd|rd|th)?(?:\s*,?\s*(\d{{4}}))?\b",
    re.IGNORECASE,
)
# day-first: "30 Oct 2017" / "5 November"
DMY = re.compile(
    rf"\b(\d{{1,2}})(?:st|nd|rd|th)?\s+{MONTH_RE}[a-z]*\.?(?:\s*,?\s*(\d{{4}}))?\b",
    re.IGNORECASE,
)
# year-first: "2041 Dec 31" (classification-banner quotes, document
# headers). MONTH_RE stays unwrapped so group 2 is the month stem and
# group 3 the day, same convention as DMY. Fix cause: id 7175228 quotes
# the banner "Declassify On: 20411231" then writes the date year-first;
# the B2-243 sentence-year guard correctly killed its inferred-year twin
# (2019-12-31) and no rule read "YYYY Month D", so the drop's one true
# date was lost entirely (byte audit:
# watch/inbox/burn_wave_20260926/B2_243_bucket_audit_20260926.md,
# sentence-year class). Evidence the window is tight: the 2026-09-26
# pre-edit sweep (watch/inbox/burn_wave_20260926/B2_258_yearfirst_
# probe.py) fires on exactly that one site across 6,242 drops and finds
# zero numeric year-first dot/slash/dash variant sites in the corpus
# (ISO and NUM_Y own those shapes); the canonical-month-word check
# applies unchanged, so the month token must still be a month word.
YEAR_FIRST = re.compile(
    rf"\b((?:19|20)\d{{2}}){DASH}{MONTH_RE}{DASH}(\d{{1,2}})(?:st|nd|rd|th)?\b",
    re.IGNORECASE,
)
# numeric slash/dash with year: 10/30/17, 10-30-2017, 2018/06/27
NUM_Y = re.compile(r"\b(\d{1,4})([/-])(\d{1,2})\2(\d{2,4})\b")
# numeric slash/dash without year: 10/30, 10-30
NUM_NOY = re.compile(r"\b(\d{1,2})[/-](\d{1,2})(?![\d/-])")
# ISO: 2018-06-27
ISO = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
# dotted with year: 10.30.17
DOT_Y = re.compile(r"\b(\d{1,2})\.(\d{1,2})\.(\d{2,4})\b")
# dotted without year (Q cipher): 11.3 / 11.4
DOT_NOY = re.compile(r"(?<![\d.])(\d{1,2})\.(\d{1,2})(?![\d.])")
# month-year only: "July 2018"
MONTH_YEAR = re.compile(
    rf"\b{MONTH_RE}[a-z]*\.?,?\s+(\d{{4}})\b", re.IGNORECASE
)
# B2-242: every letter-led unit alternative is boundary-bounded so the guard
# cannot fire inside another word. Fix cause: drop 1795201
# "Stars = Musk b-day 6/28" (ts 2018-06-18) produced no ledger row because
# THREE unanchored alternatives matched inside words in its window ("k" in
# Musk, the bare "b" of "b-day" via [kmgt]?i?b\b, "days?" in b-day) while the
# sibling sentence "Moon = Full moon 6/27 (or 6/28)" kept both dates; the same
# defect killed 914092 '"We are under attack" - Q, 4/3' ("k" in attack) and
# 10566765 "[coming 11.3]?" ("mins?" inside coming). Corpus-verified blast
# radius (B2_242_guard_probe.py, 2026-09-26, 6,242 drops): exactly 3 true
# dates restored, 2 wrong-reason exclusions migrated to properly-caused
# guards (TIMES/SECTION below), the 31 existing survivors untouched; zero
# new-only firings (the bounded language is a strict subset of the old).
# Digit-led spellings still fire ("5k", "32gb", "50%"). bytes? is
# deliberately left unanchored on the left: mega/giga-style compounds
# ("22.7 megabytes", drop 7643939) are real units and must keep excluding.
QUANTITY = re.compile(
    r"(\bmillion\b|\bbillion\b|\btrillion\b|\bpercent\b|%|(?<![a-z])k\b|"
    r"\bpts?\b|\bpoints?\b|\bamp\b|bytes?|"
    r"(?<![a-z])(?:[kmgt]?i?b)(?![a-z-])|(?<![a-z])hz\b|(?<![a-z])fps\b|"
    r"(?<![a-z])mph\b|\bhours?\b|\bhrs?\b|\bminutes?\b|\bmins?\b|"
    r"\bseconds?\b|\bsecs?\b|(?<![\w-])days?\b|\bweeks?\b|\bmonths?\b|"
    r"\byears?\b|\byrs?\b|\bdecades?\b)",
    re.IGNORECASE,
)
# yr/yrs are unit abbreviations exactly like years. Fix cause: drop 1416139
# "Why has it taken 1.5 yrs?" (ts 2018-05-15) was dated 2018-01-05 because
# QUANTITY knew "years" but not "yrs" (B2-220 receipt, DOT_NOY path).
# Corpus-verified blast radius: rejects exactly that one dotted site and
# zero of the 31 surviving NUM_NOY sites across 6,242 drops
# (B2_220_guard_probe.py, 2026-09-26); \byrs?\b boundaries keep words like
# "Syria" from firing the guard. Re-verified under the B2-242 bounded
# pattern: the yrs site still rejects, zero new exclusions on either path.
# figure labels immediately before a dotted token mark document figure
# numbers, not dates. Fix cause: drop 114 "Figure 3.1 - FBI Chain of
# Command for the Midyear Investigation" (ts 2018-08-03) was dated
# 2018-03-01 (B2-220 receipt). Corpus-verified: fires on exactly that one
# dotted site across 6,242 drops; the prefix-tail anchor (label ends where
# the token starts) keeps prose like "figure it out on 11.3" safe.
# B2-242 extension: section labels are the same document-label class.
# Fix cause: drop 2264304 "Section 5.2 CLAS [Office of President]"
# (ts 2018-07-24) was kept out of the ledger only by "secs?" firing inside
# "Section"; once QUANTITY was bounded the label guard must carry the
# exclusion or 5.2 resurrects as 2018-05-02. Evidence: B2_242_guard_probe.py
# fires SECTION on exactly that one site, 0 keeper hits.
FIGURE_RE = re.compile(r"\b(?:figures?|figs?|sections?)\.?\s*$", re.IGNORECASE)
# slash pairs that are English fractions far more often than dates
FRACTIONS = {(1, 2), (1, 3), (1, 4), (2, 3), (3, 4)}
# proportion read of a no-year numeric pair: proper fraction (numerator <
# denominator) directly quantifying a two-token noun phrase with a plural
# head. Cause of the guard: drop 34917 "7/10 plane crashes are targeted
# kills" misdated as 2017-07-10 (audit MICKEY17_WAVE2_QUALITY_20260925.md
# batch 4.1, 1/292 rows); FRACTIONS only covered (1,2)..(3,4). Evidence the
# window is tight: 2026-09-26 full-corpus sweep (B2_68_guard_probe.py)
# rejects exactly this one site across 6,242 drops.
PROPORTION_RE = re.compile(
    r"\s+(?:of\s+)?[A-Za-z][A-Za-z'-]*\s+[A-Za-z][A-Za-z'-]*s\b"
)
# dash-pair unit/tally/reference guards. Fix cause: 15 residual 0.65 rows
# dated non-dates on the numeric no-year path after the B2-68 proportion
# fix - id 7182803 "10-30 feet" as 2019-10-30 and "(ages 8-9)" as
# 2019-08-09, id 893904 "ARTICLES 1-9" as 2018-01-09, id 5123210 SC vote
# "(6-3)" as 2019-06-03, and 10 more (full 31-row byte audit:
# watch/inbox/burn_wave_20260926/B2_219_misdate_classes_20260926.md).
# Evidence the window is tight: 2026-09-26 full-corpus sweep
# (B2_219_guard_probe.py) rejects exactly those 15 rows across 6,242
# drops, 0 keeper hits; dash separator only, so the 16 keeper rows
# (15 slash-separated + "by 11-11") are untouched.
AGE_BEFORE_RE = re.compile(r"\bages?\s+$", re.IGNORECASE)
# measure/frequency noun after the pair. B2-242 extension: "times" is the
# frequency read. Fix cause: drop 251705 "Posted 4-5 times today."
# (ts 2018-01-06) was kept out of the ledger only by "days?" firing inside
# "today"; once QUANTITY was bounded the frequency noun must carry the
# exclusion or 4-5 resurrects as 2018-04-05. Evidence:
# B2_242_guard_probe.py fires TIMES on exactly that one site across 6,242
# drops, 0 keeper hits; dash separator only (inherited from the guard block).
MEASURE_AFTER_RE = re.compile(
    r"\s(?:feet|foot|inches|inch|meters|miles|acres|degrees|fathoms|times)\b",
    re.IGNORECASE,
)
# B2-263 ceiling note (2026-09-26): per-noun is the documented ceiling for
# this guard. Full-corpus audit (watch/inbox/burn_wave_20260926/
# B2_263_dash_noun_audit_20260926.md) swept every dash-pair followed by any
# word across 6,242 drops: 39 distinct followers, 9 measure/frequency-class
# sites, and ALL already yield zero extractor candidates because the
# QUANTITY near-window generically kills unit nouns; a generalized
# word-class follower fires only on those same already-dead sites (redundant)
# and has no class boundary without POS. Falsifier held: the generalized
# form rejects 0 of the 16 B2-219 keepers, 3 B2-242 restores, and "by 11-11".
COUNT_NP_BEFORE_RE = re.compile(r"\b\S+s\s+$", re.IGNORECASE)
RANGE_LIST_RE = re.compile(r"^\s*,\s*\d{1,3}\s*-\s*\d{1,3}\b")
# canonical month-word guard on the month-name paths. Fix cause: 9 residual
# 0.75 rows dated non-dates because a 3-letter month stem swallowed a longer
# word: id 147449624 "once 11.3 verifies as 1st marker" as 2018-03-01,
# id 158980 "Missing 10/15 marker" as 2018-03-10/15, id 894571 "3rd Marine
# Aircraft Wing" as 2018-03-03, id 1784355 "have 2 decide" as 2018-12-02,
# id 5705810 "[Marker 1 Complete]" as 2019-03-01, id 7175228 "declassified
# 22" as 2019-12-22, id 7517929 "GANG of 8 DECLAS" as 2019-12-08, id 9730975
# "DECLAS 1-99" as 2020-12-01 (byte audit of all 68 residual 0.75 rows:
# watch/inbox/burn_wave_20260926/B2_243_bucket_audit_20260926.md).
# Evidence the window is tight: 2026-09-26 full-corpus sweep
# (B2_243_guard_probe.py) rejects exactly those 9 sites across 6,242 drops,
# 0 on the explicit-year (0.90) path and 0 on MONTH_YEAR (0.55); "may" is
# canonical, so the modal verb is untouched by this check.
CANONICAL_MONTHS = {
    "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "sept",
    "oct", "nov", "dec",
    "january", "february", "march", "april", "june", "july", "august",
    "september", "october", "november", "december",
}
# sentence-year contradiction guard on the no-year month-name path. Fix
# cause: 2 residual 0.75 rows whose nearest-year inference contradicted a
# year printed in the same sentence: id 7039606 "on October 24 at Assouline
# ... on October 24, 2013" (the correct 2013-10-24 already held at 0.90; the
# yearless twin became 2019-10-24) and id 7175228 "2041 Dec 31" (year-first
# form, held as 2019-12-31; same B2-243 audit). Evidence: the B2_243_guard_
# probe.py sweep rejects exactly those 2 sites across 6,242 drops. Equal
# years keep the row ("2018 Jan 2" still extracts as 2018-01-02, 0.75);
# since B2-258 the year-first month-word shape re-extracts at 0.90
# (YEAR_FIRST above), so this guard only kills the inferred-year twin
# (7175228 keeps 2019-12-31 absent while 2041-12-31 lands).
SENT_YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")
# a no-year numeric pair must sit beside prose/brackets, not inside junk tokens
# like base64 filenames ("[J-Go_dX)-2-8")
LEAD_OK = re.compile(r"^$|[\s(\[>\"]")
TAIL_OK = re.compile(r"^$|[\s,.;:!?\])}\"'\-]")

URL_RE = re.compile(r"https?://\S+|www\.\S+")
# domain-like tokens (sources wrap '//' in <em> tags, splitting URLs in two)
DOMAIN_RE = re.compile(
    r"\b[a-z0-9][a-z0-9.-]*\.(com|net|org|gov|edu|mil|co|us|uk|io|info|biz|ru|ch|de|int|xyz|news|site|one|link|tv|me|to)\b\S*",
    re.IGNORECASE,
)
ORDINAL_RE = re.compile(r"\s?(st|nd|rd|th)\b", re.IGNORECASE)
REPLY_RE = re.compile(r"^(>{1,3}|\s)*\d{6,}\s*", re.MULTILINE)
TAG_RE = re.compile(r"</?[a-z]+>", re.IGNORECASE)

SKIP_MD = {(9, 11)}  # bare "9/11" without year = event reference


def clean_text(raw: str) -> str:
    t = html.unescape(raw)
    t = TAG_RE.sub("", t)  # tags first: sources wrap '//' in <em>, hiding URLs
    t = URL_RE.sub(" ", t)
    t = DOMAIN_RE.sub(" ", t)
    t = re.sub(r">>{1,3}\d+", " ", t)
    t = t.replace("\r", "\n")
    t = re.sub(r"[ \t]+", " ", t)
    return t.strip()


def sentences(text: str):
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        for part in re.split(r"(?<=[.!?])\s+", line):
            part = part.strip()
            if 8 <= len(part):
                yield part


def mk_date(y: int, m: int, d: int):
    try:
        return datetime(y, m, d).date()
    except ValueError:
        return None


def infer_year(drop_ts: datetime, m: int, d: int) -> int:
    best, best_gap = drop_ts.year, None
    for y in (drop_ts.year - 1, drop_ts.year, drop_ts.year + 1):
        cand = mk_date(y, m, d)
        if cand is None:
            continue
        gap = abs((cand - drop_ts.date()).days)
        if best_gap is None or gap < best_gap:
            best, best_gap = y, gap
    return best


def month_word(sent: str, stem_start: int) -> str:
    """Full alphabetic token holding the month stem ("marker" for mar)."""
    m = re.match(r"[A-Za-z]+", sent[stem_start:])
    return m.group(0).lower() if m else ""


def adjacent_year(prev_sent: str, next_sent: str):
    """Clause 2 of the year ladder (docstring "Year ladder"): the single
    distinct standalone 19xx/20xx year printed across the two sentences
    adjacent to the match's sentence, or None when absent or contradictory
    (both sides carry years and they differ). Fix cause: 8 judgment-class
    0.75 rows where nearest-year contradicted drop context (B2-243 audit,
    watch/inbox/burn_wave_20260926/B2_243_bucket_audit_20260926.md); bytes
    alone re-date exactly one, id 7643939 "the paper dated July 9" held
    2019-07-09 while the next sentence prints "July 5, 2016". Evidence the
    window is tight: the pre-edit sweep (B2_257_ladder_probe.py, 6,242
    drops) fires clause 2 on exactly that one site and moves none of the
    other 56 surviving 0.75 rows. Applied only when the sentence itself
    prints no year (the SENT_YEAR_RE guard owns sentences that do)."""
    years = set(SENT_YEAR_RE.findall(prev_sent or "")) | set(
        SENT_YEAR_RE.findall(next_sent or "")
    )
    if len(years) == 1:
        return int(years.pop())
    return None


def norm_yy(y: int, drop_year: int) -> int:
    return y if y > 99 else (2000 + y if y <= 49 else 1900 + y)


def extract(drop: dict):
    """Yield (date_str, claim, confidence) tuples for one drop."""
    raw = drop.get("text") or ""
    if not raw.strip():
        return
    try:
        ts = datetime.fromisoformat(drop["ts"])
    except (KeyError, ValueError):
        ts = None
    text = clean_text(raw)
    sents = list(sentences(text))
    for si, sent in enumerate(sents):
        prev_sent = sents[si - 1] if si else ""
        next_sent = sents[si + 1] if si + 1 < len(sents) else ""
        seen = set()
        hits = []  # (sortkey, date_str, conf)

        for m in ISO.finditer(sent):
            y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
            dt = mk_date(y, mo, d)
            if dt:
                hits.append((m.start(), dt.isoformat(), 0.95))

        for m in MDY.finditer(sent):
            if month_word(sent, m.start(1)) not in CANONICAL_MONTHS:
                continue  # "Marker 1", "decide 2": month stem inside a longer word
            mo = MONTHS[m.group(1).lower()[:3]] if m.group(1).lower()[:3] != "sept" else 9
            d = int(m.group(2))
            if (mo, d) in SKIP_MD and not m.group(3):
                continue
            if m.group(3):
                dt = mk_date(int(m.group(3)), mo, d)
                conf = 0.90
            else:
                y = infer_year(ts, mo, d) if ts else None
                if y and (yr := SENT_YEAR_RE.search(sent)) and int(yr.group(0)) != y:
                    continue  # sentence prints its own year; do not infer a different one
                if y and not SENT_YEAR_RE.search(sent):
                    ay = adjacent_year(prev_sent, next_sent)
                    if ay is not None and ay != y and mk_date(ay, mo, d):
                        y = ay  # ladder clause 2: adjacent-sentence year
                dt = mk_date(y, mo, d) if y else None
                conf = 0.75
            if dt:
                hits.append((m.start(), dt.isoformat(), conf))

        for m in DMY.finditer(sent):
            if month_word(sent, m.start(2)) not in CANONICAL_MONTHS:
                continue  # "1st marker", "3rd Marine": month stem inside a longer word
            mo = MONTHS[m.group(2).lower()[:3]] if m.group(2).lower()[:3] != "sept" else 9
            d = int(m.group(1))
            if (mo, d) in SKIP_MD and not m.group(3):
                continue
            if m.group(3):
                dt = mk_date(int(m.group(3)), mo, d)
                conf = 0.90
            else:
                y = infer_year(ts, mo, d) if ts else None
                if y and (yr := SENT_YEAR_RE.search(sent)) and int(yr.group(0)) != y:
                    continue  # sentence prints its own year; do not infer a different one
                if y and not SENT_YEAR_RE.search(sent):
                    ay = adjacent_year(prev_sent, next_sent)
                    if ay is not None and ay != y and mk_date(ay, mo, d):
                        y = ay  # ladder clause 2: adjacent-sentence year
                dt = mk_date(y, mo, d) if y else None
                conf = 0.75
            if dt:
                hits.append((m.start(), dt.isoformat(), conf))

        for m in YEAR_FIRST.finditer(sent):
            if month_word(sent, m.start(2)) not in CANONICAL_MONTHS:
                continue  # year + non-month word: not a date
            y = int(m.group(1))
            mo = MONTHS[m.group(2).lower()[:3]] if m.group(2).lower()[:3] != "sept" else 9
            d = int(m.group(3))
            dt = mk_date(y, mo, d)
            if dt:
                hits.append((m.start(), dt.isoformat(), 0.90))  # explicit year

        for m in NUM_Y.finditer(sent):
            a, b, c = int(m.group(1)), int(m.group(3)), int(m.group(4))
            y = norm_yy(c, ts.year if ts else 2018)
            if m.group(1).startswith(("19", "20")):  # ymd: 2018/06/27
                dt = mk_date(a, b, c)
                mo, d = b, c
            else:  # mdy
                mo, d = a, b
                dt = mk_date(y, a, b)
            if dt and not (mo, d) in SKIP_MD:
                hits.append((m.start(), dt.isoformat(), 0.90))

        for m in DOT_Y.finditer(sent):
            a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
            y = norm_yy(c, ts.year if ts else 2018)
            dt = mk_date(y, a, b)
            if dt:
                hits.append((m.start(), dt.isoformat(), 0.90))

        for m in NUM_NOY.finditer(sent):
            mo, d = int(m.group(1)), int(m.group(2))
            if not (LEAD_OK.match(sent[: m.start()][-1:] or "")
                    and TAIL_OK.match(sent[m.end(): m.end() + 1] or "")):
                continue
            if not (1 <= mo <= 12 and 1 <= d <= 31) or (mo, d) in SKIP_MD:
                continue
            if (mo, d) in FRACTIONS:
                continue
            if ORDINAL_RE.match(sent[m.end(): m.end() + 4]):  # "1/10th" ratios
                continue
            if mo < d and PROPORTION_RE.match(sent[m.end():]):
                continue  # "7/10 plane crashes" = proportion, not July 10
            if re.search(r"[/-]", m.group(0)).group(0) == "-":
                # dash pairs read as units/tallies/references more often
                # than dates; predicates + receipts in the guard block
                # above (B2-219, 15 rows)
                lead = sent[: m.start()][-1:] or ""
                tail = sent[m.end(): m.end() + 1] or ""
                if lead == "[" or tail == "]":
                    continue  # "[D][1-6]", "[CLAS 1-9]" drop references
                if lead == "(" and tail == ")":
                    continue  # "(6-3)" vote tally, "(5-6)" window
                if AGE_BEFORE_RE.search(sent[: m.start()]):
                    continue  # "(ages 8-9)" age range
                if MEASURE_AFTER_RE.match(sent[m.end():]):
                    continue  # "10-30 feet" measure range
                if mo == 1:
                    continue  # "ARTICLES 1-9" numbered-list reference
                if COUNT_NP_BEFORE_RE.search(sent[: m.start()]):
                    continue  # "alerts 5-12" alert-number range
                if RANGE_LIST_RE.match(sent[m.end():]):
                    continue  # "5-3, 1-99" coded range pair
            near = sent[max(0, m.start() - 12): m.end() + 12]
            if QUANTITY.search(near):
                continue
            y = infer_year(ts, mo, d) if ts else None
            dt = mk_date(y, mo, d) if y else None
            if dt:
                hits.append((m.start(), dt.isoformat(), 0.65))

        for m in DOT_NOY.finditer(sent):
            a, b = int(m.group(1)), int(m.group(2))
            if not (LEAD_OK.match(sent[: m.start()][-1:] or "")
                    and TAIL_OK.match(sent[m.end(): m.end() + 1] or "")):
                continue
            near = sent[max(0, m.start() - 12): m.end() + 12]
            if QUANTITY.search(near) or "$" in near:
                continue
            if FIGURE_RE.search(sent[: m.start()]):
                continue  # "Figure 3.1" = document figure number, not March 1
            if 1 <= a <= 12 and 1 <= b <= 31:
                mo, d, conf = a, b, 0.50
            elif 1 <= a <= 31 and 1 <= b <= 12:
                mo, d, conf = b, a, 0.40  # day-first reading
            else:
                continue
            if (mo, d) in SKIP_MD:
                continue
            y = infer_year(ts, mo, d) if ts else None
            dt = mk_date(y, mo, d) if y else None
            if dt:
                hits.append((m.start(), dt.isoformat(), conf))

        for m in MONTH_YEAR.finditer(sent):
            mo = MONTHS[m.group(1).lower()[:3]] if m.group(1).lower()[:3] != "sept" else 9
            y = int(m.group(2))
            if 1900 <= y <= 2030:
                hits.append((m.start(), f"{y:04d}-{mo:02d}", 0.55))

        # keep highest-confidence hit per normalized date in this sentence
        best = {}
        for _, date_str, conf in hits:
            if date_str not in best or conf > best[date_str]:
                best[date_str] = conf
        for date_str, conf in sorted(best.items()):
            key = (drop.get("id"), date_str, sent[:120])
            if key in seen:
                continue
            seen.add(key)
            claim = sent[:320].strip()
            yield date_str, claim, conf


def main():
    if not SRC.exists():
        print(f"MISSING SOURCE: {SRC}", file=sys.stderr)
        return 1
    rows, drops_seen, drops_with, skips = [], 0, 0, {"null_or_empty_text": 0}
    with SRC.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            drop = json.loads(line)
            drops_seen += 1
            got = list(extract(drop))
            if not got:
                if not (drop.get("text") or "").strip():
                    skips["null_or_empty_text"] += 1
                continue
            drops_with += 1
            for date_str, claim, conf in got:
                rows.append({
                    "id": str(drop.get("id")),
                    "date": date_str,
                    "claim": claim,
                    "confidence": conf,
                })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    dates = sorted(r["date"] for r in rows if len(r["date"]) == 10)
    hist = {}
    for r in rows:
        hist[r["confidence"]] = hist.get(r["confidence"], 0) + 1
    print(f"drops read: {drops_seen}")
    print(f"drops with >=1 dated claim: {drops_with}")
    print(f"skips: {skips}")
    print(f"ledger rows: {len(rows)}")
    print(f"full-date span: {dates[0]} .. {dates[-1]}" if dates else "no full dates")
    print(f"confidence histogram: {dict(sorted(hist.items()))}")
    print(f"wrote: {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
