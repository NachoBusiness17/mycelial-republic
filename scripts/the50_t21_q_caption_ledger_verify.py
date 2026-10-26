#!/usr/bin/env python
"""THE 50 / T21 (W5): verifier for the Q caption ledger.

Checks watch/inbox/qdrop_export/q_caption_ledger.jsonl against its source
corpus watch/inbox/qdrop_export/qdrops.jsonl and the generator
scripts/the50_t21_q_caption_ledger.py:

  1. schema exact: every row has exactly the keys
     {id, date, claim, confidence} with correct types
  2. date well-formed: "YYYY-MM-DD" (valid calendar date) or "YYYY-MM"
  3. confidence drawn from the documented rubric values
  4. grounding: every row id exists in qdrops.jsonl
  5. traceability: every claim (whitespace-normalized) occurs inside its
     drop's cleaned text, truncated claims included
  6. reproducibility: for every drop, the extractor's current output is a
     superset of that drop's ledger rows (byte-equal date/claim/confidence)
  7. guard-class regression pin: the rows rejected by the landed guard
     families (B2-68 proportion, B2-220 dotted yrs/figure, B2-219 dash
     unit/tally/reference, B2-242 bounded QUANTITY + TIMES/SECTION,
     B2-243 canonical-month-word and sentence-year) stay absent, and the
     pinned keeper rows (16 B2-219, 3 B2-242 restored, 57 surviving
     0.75 B2-243) stay present byte-for-byte, so a QUANTITY/regex
     refactor cannot silently resurrect or re-kill them.
     SPEC (B2-275, 2026-09-26): every check7 FAIL print carries the pin
     maintenance law's required steps (re-audit every differing row
     against qdrops.jsonl bytes; re-derive the pin constants from that
     audit; name the audit in the landing receipt; never delete or
     weaken pins to get green), because the lane that trips check7 sees
     only the FAIL line, never this docstring; the PASS line stays
     byte-identical
  8. line-ending integrity (B2-239, 2026-09-26): the ledger's raw bytes
     hold zero CR bytes. CAUSE: the pre-B2-220 on-disk ledger was CRLF
     (291 CRLF lines, sha 2f3afda8976fe2...) while the generator writes
     LF (OUT.open newline="\n"), so B2-220's raw byte diff read as
     full-file churn (1,291c1,289) instead of its true two-row delta.
     Byte attribution (B2_239_line_endings_20260926.md): the CRLF state
     was content-identical to B2-68's post bytes (LF-normalized sha
     e1677ba76cf7... equal), the 291-row content survives in the git
     object store as dangling blob aba4dbbde7af67b986c9cbdc376e039f9
     fd13270, and no blob holds the CRLF form, i.e. the file was
     re-materialized by the smudge filter (core.autocrlf=true;
     .gitattributes guards only *.rbxlx/*.rbxm per B2-109), not edited
     by any repo script. FIX: fail while any CR byte is present, so an
     endings-only rewrite cannot masquerade as content drift (or hide
     real drift inside full-file churn)
  9. sealed baseline (W3A, 2026-09-29): the ledger must match the sealed
     row count + sha256 pinned in this file's SEALED_* constants. CAUSE:
     the gate-canary caption_ledger_verify family proved this gate DEAD
     on 2026-09-29 (receipt
     watch/inbox/mates_leave_protocol/W3A_CAPTION_GATE_FIX.md): deleting
     a ledger row left RESULT: PASS because every check above builds its
     denominator FROM the ledger rows it reads -- check1 counts the rows
     it parsed, checks 4/5/6 iterate ids still present, and check6's
     reproducibility direction only re-runs drops that still hold rows
     (the same blindness B2-306 documented for vanished cipher rows,
     generalized to ANY unpinned row). FIX: verify against an INDEPENDENT
     baseline -- the sealed count + sha of the ledger bytes, carried in
     this gate's own source (version-controlled and already watched by
     the prepush changed-path arm), never read back from the ledger it
     audits. A check9 FAIL is the audit trigger, not a bug to mute.

Run: .venv/Scripts/python.exe scripts/the50_t21_q_caption_ledger_verify.py
      [--ledger PATH]  # canary/manual drill: verify a tampered copy; the
                       # seal still applies, so any byte drift FAILs by design
Exits 0 on PASS, 1 on FAIL, printing one line per check.
"""
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from the50_t21_q_caption_ledger import SRC, OUT, extract  # noqa: E402

RUBRIC = {0.4, 0.5, 0.55, 0.65, 0.75, 0.9, 0.95}
KEYS = {"id", "date", "claim", "confidence"}

# W3A sealed baseline (2026-09-29), the canary DEAD-gate fix. These two
# constants are check9's INDEPENDENT denominator: derived from the ledger
# bytes at seal time and carried in this gate's own source file (version
# controlled, watched by the prepush changed-path arm), never read back
# from the ledger being audited. Sealed from
# watch/inbox/qdrop_export/q_caption_ledger.jsonl on 2026-09-29:
# 267 rows, 33,338 bytes, zero CR bytes.
# SEAL MAINTENANCE LAW (the B2-259 pin law applied to the whole file): a
# legitimate generator regen that changes the ledger re-derives both
# constants from the new bytes and names the byte audit in its landing
# receipt; deleting or weakening the seal to get green converts this gate
# back into the DEAD gate the canary filed (deleting a row used to leave
# RESULT: PASS -- receipt
# watch/inbox/mates_leave_protocol/W3A_CAPTION_GATE_FIX.md).
SEALED_ROW_COUNT = 267
SEALED_LEDGER_SHA256 = (
    "489d5af92c3d8ee945d5761f2e01ee66511e87e188e4ca1c6015f4e4cb826053")

# check7 guard-class regression pin (B2-244, 2026-09-26). Cause: three guard
# families landed in the generator (B2-68 proportion, B2-220 dotted yrs and
# figure labels, B2-219 dash unit/tally/reference) and nothing pinned their
# verdicts, so the next QUANTITY/regex refactor could silently resurrect the
# audited misdate rows. Every string below is copied verbatim from the
# pre-guard snapshots and the post-guard ledger; receipts in
# watch/inbox/burn_wave_20260926/ (B2_68_fraction_guard_20260926.md,
# B2_220_dotted_guards_20260926.md, B2_219_misdate_classes_20260926.md).
# PIN MAINTENANCE LAW (B2-259, 2026-09-26): a check7 FAIL the moment a
# generator lane lands is expected and legitimate when that lane's audit
# moved pinned rows; both precedents landed clean this way (B2-242's three
# restores tripped the keeper union and re-pinned with a per-row byte audit
# named in B2_242_quantity_bounds_20260926.md; B2-243's 11 rejections were
# initially untracked by this pin and were pinned by B2-256 from
# B2_243_bucket_audit_20260926.md). The law: when a generator lane lands
# and check7 fails, that lane re-audits every differing row against
# qdrops.jsonl bytes, re-derives the pin constants from that audit, and
# names the audit in its landing receipt; never delete or weaken pins to
# get green. Falsifier: any receipt that lands a generator change plus a
# check7 constants edit without a per-row byte audit converts this pin
# from evidence into decoration
# (watch/inbox/burn_wave_20260926/B2_259_pin_law_20260926.md).
# Rows the guards rejected, as exact (id, date, claim, confidence); each
# must stay absent exactly as the generator used to re-emit it.
GUARD_PINNED_ABSENT = {
    # B2-68 proportion guard: "7/10 plane crashes" reads seven-of-ten,
    # not July 10 (B2_68_ledger_before.jsonl)
    ("34917", "2017-07-10", "7/10 plane crashes are targeted kills.", 0.65),
    # B2-220 yrs guard: "1.5 yrs" is a duration, not January 5
    # (B2_220_ledger_before.jsonl)
    ("1416139", "2018-01-05", "Why has it taken 1.5 yrs?", 0.5),
    # B2-220 figure guard: "Figure 3.1" is a document figure label,
    # not March 1 (B2_220_ledger_before.jsonl)
    ("114", "2018-03-01",
     "Figure 3.1 - FBI Chain of Command for the Midyear Investigation", 0.5),
}
# Claim fragments that net the pinned rows even if a refactor changes the
# inferred year or confidence: a ledger claim carrying one of these is a
# resurrected guard-class row regardless of its date fields.
GUARD_PINNED_CLAIMS = ("7/10 plane crashes", "1.5 yrs", "Figure 3.1")
# B2-219 misdate classes: the 15 (id, date) rows the seven dash-pair
# guards rejected (byte audit: B2_219_misdate_classes_20260926.md); any
# ledger row with one of these pairs must stay absent.
B2_219_MISDATE_PAIRS = {
    ("173382", "2017-10-09"), ("173382", "2018-05-06"),
    ("476806", "2018-05-12"), ("893904", "2018-01-09"),
    ("5123210", "2019-06-03"), ("7182803", "2019-08-09"),
    ("7182803", "2019-10-30"), ("7355626", "2020-01-09"),
    ("7357987", "2020-01-06"), ("95", "2020-01-06"),
    ("7535766", "2020-05-03"), ("9081684", "2020-01-09"),
    ("9081684", "2020-01-07"), ("9105563", "2020-01-09"),
    ("9298758", "2020-01-09"),
}
# B2-219 keepers: the 16 genuine-date 0.65 rows that must stay present
# byte-for-byte, copied from the post-guard ledger (id 147012719 holds two
# rows on 2017-10-30). \u2013 escapes are U+2013 en dashes present in the
# source drop text.
B2_219_KEEPER_ROWS = {
    ("147012719", "2017-10-30",
     "Passport approved to be flagged effective 10/30 @ 12:01am.", 0.65),
    ("147012719", "2017-10-30",
     "Proof check: Locate a NG member and ask if activated for duty 10/30 "
     "across most major cities.", 0.65),
    ("121327", "2017-12-07", "12/7 \u2013 12/17.", 0.65),
    ("121327", "2017-12-17", "12/7 \u2013 12/17.", 0.65),
    ("121553", "2017-12-07", "What happened on 12/7?", 0.65),
    ("178973", "2017-12-21", "EO 12/21.", 0.65),
    ("594193", "2017-11-11", "Resolved by 11-11.", 0.65),
    ("914092", "2018-04-03", "\"WAR\" - Q, 4/3", 0.65),
    ("1181379", "2018-01-20", "POTUS win - 1/20.", 0.65),
    ("1702926", "2018-06-11", "6/11 ALMOST OVER", 0.65),
    ("1795201", "2018-06-27", "Moon = Full moon 6/27 (or 6/28)", 0.65),
    ("1795201", "2018-06-28", "Moon = Full moon 6/27 (or 6/28)", 0.65),
    ("1795201", "2018-06-29", "Missions = Space X launch 6/29", 0.65),
    ("2950871", "2018-09-16", "Article date: 9/16", 0.65),
    ("2950871", "2018-09-14", "post date 9/14", 0.65),
    ("5139710", "2018-09-26",
     "9/26 \u2013 Federal SW \u2013 IPhone/IPAD/Laptop", 0.65),
}
# B2-242 bounded-quantity guard classes (2026-09-26). Cause: bounding
# QUANTITY's unit alternatives restored 3 true-date rows the unanchored
# pattern had killed via inside-word hits (b-day, attack, coming), and
# moved 2 wrong-reason exclusions to the TIMES/SECTION guards (Posted
# 4-5 times; Section 5.2); the third wrong-reason site (22.7 megabytes)
# stays excluded through bytes? staying left-unanchored by design.
# Receipt: watch/inbox/burn_wave_20260926/B2_242_quantity_bounds_20260926.md.
# Restored rows must stay present byte-for-byte:
B2_242_KEEPER_ROWS = {
    ("1795201", "2018-06-28", "Stars = Musk b-day 6/28", 0.65),
    ("914092", "2018-04-03", "\"We are under attack\" - Q, 4/3", 0.65),
    ("10566765", "2020-11-03",
     "Now: voter intimidation in National and local elections "
     "[coming 11.3]?", 0.5),
}
# Migrated/still-excluded misdate rows must stay absent (pair pin, like
# B2_219_MISDATE_PAIRS):
B2_242_MISDATE_PAIRS = {
    ("251705", "2018-04-05"),   # "Posted 4-5 times today." = frequency range
    ("2264304", "2018-05-02"),  # "Section 5.2 CLAS [...]" = document label
    ("7643939", "2019-07-22"),  # "22.7 megabytes per second" = unit compound
}
# Claim fragments that net the B2-242 migrated rows even if a refactor
# changes the inferred date or confidence. "22.7" is load-bearing: the
# same drop holds a legitimate 0.90 row ("July 5, 2016, 1,976 megabytes",
# explicit-year path) that a bare "megabytes" fragment would wrongly net.
B2_242_PINNED_CLAIMS = ("Posted 4-5 times", "Section 5.2", "22.7 megabytes")

# B2-243 canonical-month-word + sentence-year guard classes (2026-09-26).
# Cause: the two guard families B2-243 landed in the generator
# (CANONICAL_MONTHS + month_word() on the MDY/DMY loops, SENT_YEAR_RE on
# both no-year branches) pinned nothing of their own, so a month-word or
# nearest-year refactor could silently resurrect the 11 audited misdate
# rows (self-feed B2-256; byte audit of all 68 residual 0.75 rows:
# watch/inbox/burn_wave_20260926/B2_243_bucket_audit_20260926.md).
# Any fire here means a guard verdict changed: re-audit the differing
# rows against qdrops.jsonl bytes and name that audit in the landing
# receipt before touching these constants.
# Rows the guards rejected, as exact (id, date); each must stay absent:
B2_243_MISDATE_PAIRS = {
    ("147449624", "2018-03-01"),  # "1st marker": mar stem inside "marker"
    ("158980", "2018-03-10"),     # "Missing 10 marker": post number, not a date
    ("158980", "2018-03-15"),     # "Missing 15 marker": post number, not a date
    ("894571", "2018-03-03"),     # "3rd Marine Aircraft Wing": unit designation
    ("1784355", "2018-12-02"),    # "have 2 decide": dec stem inside "decide"
    ("5705810", "2019-03-01"),    # "[Marker 1 Complete]": red-marker series
    ("7175228", "2019-12-22"),    # "declassified 22": dec stem inside the word
    ("7175228", "2019-12-31"),    # "2041 Dec 31": year-first banner quote
    ("7517929", "2019-12-08"),    # "GANG of 8 DECLAS": dec stem inside DECLAS
    ("9730975", "2020-12-01"),    # "[DECLAS 1-99 material]": not a date
    ("7039606", "2019-10-24"),    # same sentence prints "October 24, 2013"
}
# Claim fragments that net the pinned rows even if a refactor changes the
# inferred date or confidence. Narrowed from the bare audit words where
# the bare fragment occurs inside surviving claims: "DECLAS" appears in
# two legitimate keepers (ids 5477046, 9298758) and "decide" inside
# "decides" (id 7003276), so those rows net only through the narrowed
# strings below (same practice as B2-242: "megabytes" -> "22.7 megabytes").
# B2-258 pin maintenance (2026-09-26, per the B2-259 law): "2041 Dec 31"
# left the bare net because the sentence legitimately survives at 0.90 via
# the new year-first rule (drop 7175228, re-audited against qdrops.jsonl
# bytes: "Declassify On: 20411231" banner plus "2041 Dec 31"; landing
# receipt watch/inbox/burn_wave_20260926/B2_258_yearfirst_20260926.md).
# It moved to the scoped net below so a 0.65/0.75-band resurrection still
# fires while the 0.90 keeper row survives.
B2_243_PINNED_CLAIMS = (
    "3rd Marine", "Missing 10 marker", "Missing 15 marker",
    "have 2 decide", "Marker 1 Complete",
    "declassified 22 years", "8 DECLAS", "DECLAS 1-99",
)
# Pinned sentences legitimately surviving at another confidence, so a
# bare fragment net would kill a true row: id 147449624 "1st marker" is
# the same sentence as the kept 0.50 dotted cipher row (2017-11-03), and
# id 7039606's sentence is kept at 0.90 via the explicit year
# (2013-10-24). These nets fire only inside the guard-class confidence
# band (the month-name no-year path emits 0.75; explicit year emits 0.90):
B2_243_SCOPED_CLAIMS = (
    ("1st marker", 0.65, 0.75),         # spares the 0.50 cipher row
    ("Martine Assouline", 0.75, 0.75),  # spares the 0.90 explicit-year row
    # B2-258: the sentence survives at 0.90 via the year-first rule
    # ("2041 Dec 31" -> 2041-12-31); the band still nets the killed
    # 0.75 nearest-year twin (2019-12-31) or any 0.65 resurrection
    ("2041 Dec 31", 0.65, 0.75),
)

# B2-281 keeper pin (2026-09-26, per the B2-259 maintenance law). CAUSE: the
# landed 0.90 year-first row (7175228, 2041-12-31, "2041 Dec 31", 0.9) was
# protected only by the scoped-claim spare above, which nets the killed twin
# class (0.65-0.75) but never requires the 0.90 row itself; check6 proves
# ledger-equals-extractor, so a refactor that deletes the YEAR_FIRST loop and
# regenerates would silently vanish the row from BOTH sides and stay
# verifier-green (the demonstrated gap). EVIDENCE: ledger post sha
# 72884939492b3a05 row `{"id": "7175228", "date": "2041-12-31",
# "claim": "2041 Dec 31", "confidence": 0.9}` (q_caption_ledger.jsonl:191);
# re-audited against qdrops.jsonl bytes, this pin copies it byte-for-byte.
# FIX: the exact tuple joined into the check7 keeper union, so a regen that
# loses the row fails check7 on the missing keeper instead of passing.
B2_281_YEARFIRST_KEEPER = {
    ("7175228", "2041-12-31", "2041 Dec 31", 0.9),
}
# B2-306 cipher keepers: all 16 confidence-0.5 rows of the live ledger
# (the Q cipher m.d markers of the B2-243 bucket audit plus the B2-242
# 16th restoration), extracted verbatim from
# watch/inbox/qdrop_export/q_caption_ledger.jsonl on 2026-09-26 so a
# QUANTITY/DOT_NOY/FIGURE refactor cannot silently re-kill a cipher row
# (check6's reproducibility direction only compares drops still holding
# rows, so a vanished 0.5 row is invisible to it). (id, date) collision
# check the B2-256 way: exactly one pair collides, ("1393554",
# "2018-11-11") twice, distinct claims, both held as full tuples so the
# collision is preserved, not collapsed. Receipt:
# watch/inbox/burn_wave_20260926/B2_306_cipher_pin_20260926.md. A
# legitimate NEW 0.5 row a later audited lane adds must extend this set
# with its own named byte audit per the B2-259 pin maintenance law (the
# pin fails on the extra row by design; that is the audit trigger).
B2_306_CIPHER_KEEPER_ROWS = {
    ("10566765", "2020-11-03",
     "Now: voter intimidation in National and local elections [coming "
     "11.3]?", 0.5),
    ("110", "2020-11-03", "Kevin Clinesmith [KC][11.3]", 0.5),
    ("1393554", "2018-11-11", "What must happen pre 11.11?", 0.5),
    ("1393554", "2018-11-11", "11.11 provided as strategic marker.", 0.5),
    ("147434025", "2017-11-03", "11.3 - Podesta indicted", 0.5),
    ("147434025", "2017-11-06", "11.6 - Huma indicted", 0.5),
    ("147449624", "2017-11-03",
     "Save & spread (once 11.3 verifies as 1st marker).", 0.5),
    ("147567888", "2017-11-03",
     "On POTUS\u2019 order, we have initiated certain fail-safes that shall "
     "safeguard the public from the primary fallout which is slated to "
     "occur 11.3 upon the arrest announcement of Mr.", 0.5),
    ("147567888", "2017-11-04", "Podesta (actionable 11.4).", 0.5),
    ("1769691", "2018-11-03", "11.3 - Podesta indicted", 0.5),
    ("1769691", "2018-11-06", "11.6 - Huma indicted", 0.5),
    ("1769812", "2018-11-03", "11.3 = when HUBER made a SEALED indictment", 0.5),
    ("1769812", "2018-11-06", "11.6 = when HUBER made a SEALED indictment", 0.5),
    ("3714939", "2018-11-11", "POTUS meeting PUTIN on 11.11", 0.5),
    ("64", "2018-04-21",
     "James Baker - FIRED [reported today - resigned [false]] / removed "
     "Jan/FIRED 4.21", 0.5),
    ("9749096", "2020-11-03", "[D] + China = 11.3", 0.5),
}
# B2-243 keepers: the 57 surviving 0.75 rows (49 clean keepers plus the
# 8 documented judgment-class rows) that must stay present byte-for-byte,
# extracted from the live ledger during the B2-256 byte audit. The
# \u2013 \u2014 \u2019 \u201c \u2026 escapes are the unicode characters
# present in the source drop text.
B2_243_KEEPER_ROWS = {
    ("10134839", "2020-11-03",
     "[Ready when needed] Activate 4-year BLM narrative 4x power"
     " [use as division + [2020] C19 infect rates to justify clo"
     "se-limit until Nov 3].", 0.75),
    ("10630891", "2020-09-14",
     "SEPT 14-18, 21-25 [track & follow events]", 0.75),
    ("10716779", "2020-09-21", "SEPT 21-25 [track & follow events]", 0.75),
    ("10870492", "2020-11-03",
     "MATHEMATICAL PROBABILITY OF C19 EVENT AS SOLUTION TO ABOVE"
     " _PERFECTLY TIMED 'WINDOW OF OPPORTUNITY' START RE: IMPACT"
     " NOV 3 P_ELECTION ADV [D]?", 0.75),
    ("12984", "2017-12-29",
     "28-29 December (itw on 28, excerpts and Luke Roziak tweet "
     "on 29)", 0.75),
    ("12984", "2018-01-02", "Passport system shutdown on Jan 2", 0.75),
    ("12984", "2018-01-04",
     "RR shutdown on Jan 4 for power outage (need sauce but shou"
     "ld be accurate)", 0.75),
    ("13061", "2018-01-02",
     "Im curious if POTUS tweet from Jan 2nd plays a part.", 0.75),
    ("158096", "2017-12-04", "Dec 4, 19:38:51", 0.75),
    ("158096", "2017-12-04", "Dec 4, 19:50:10", 0.75),
    ("158096", "2017-12-04", "Dec 4, 20:01:17", 0.75),
    ("158096", "2017-12-19", "Dec 19, 17:50:59", 0.75),
    ("1699199", "2018-06-11",
     "At around 9.10pm on Monday (June 11), his motorcade was se"
     "en leaving the St Regis Hotel in the Tanglin area where hi"
     "s delegation is being housed at, before driving past the R"
     "affles City area towards Marina Bay.", 0.75),
    ("2342603", "2018-06-10", "Also from June 10\u2026", 0.75),
    ("235", "2018-09-17", "SEPT \u2014-17\u2014\u2013 [week of]", 0.75),
    ("2381818", "2018-07-31", ", , , More Iran protests - July 31", 0.75),
    ("245", "2018-09-17", "SEPT \u2014\u201317\u2014\u2013", 0.75),
    ("259", "2018-09-10", "SEPT 10 DROP re: MEMES NON_NSA ABILITY", 0.75),
    ("259", "2018-09-13", "SEPT 13 & 14 [2] ARTICLES DROP re: FB MEMES", 0.75),
    ("259", "2018-09-16",
     "SEPT 16 [2] ARTICLES DROPPED/HIGHLIGHTED [EXAMPLES]", 0.75),
    ("259", "2018-09-18",
     "SEPT 18 [WIRED] RESPONDS [1] ARTICLE re: MEMES & Q", 0.75),
    ("2906216", "2018-03-22", "[March 22]", 0.75),
    ("318", "2018-11-06", "Are you registered to vote on Nov 6th?", 0.75),
    ("328", "2018-11-06",
     "Did the delay and smear tactics used by D's re: Justice K "
     "help R's re: public support / endorsement re: confirmation"
     " & NOV 6 E?", 0.75),
    ("359", "2018-10-04",
     ">Coleman\u2019s notes from October 4 contained the following en"
     "try:", 0.75),
    ("359", "2018-10-04",
     ">We showed Coleman\u2019s notes from October 4 to Comey.", 0.75),
    ("359", "2018-10-04",
     "[Meeting between Comey and Coleman on October 4]", 0.75),
    ("367", "2018-11-06",
     "Data provided to D party 'affiliate' to [target] voters fo"
     "r Nov 6 election?", 0.75),
    ("378", "2018-11-07",
     "Cannot point to any particular candidate or party prior to"
     " Nov 7?", 0.75),
    ("437", "2018-07-21",
     "\u201cThe appointment itself, on 21 July, triggered a shake-up "
     "at the Trump White House.", 0.75),
    ("5187870", "2019-02-15", "feb 15th", 0.75),
    ("5320727", "2019-02-06",
     "Just another coincidence we dropped [LL] was offered a SC "
     "seat on Feb 6th and backed up by POTUS on April 15th.", 0.75),
    ("5320727", "2019-04-15",
     "Just another coincidence we dropped [LL] was offered a SC "
     "seat on Feb 6th and backed up by POTUS on April 15th.", 0.75),
    ("5477046", "2018-09-17",
     "POTUS already ordered the DECLAS (per Q-proof Sep 17).", 0.75),
    ("5705892", "2019-03-15", "On March 15th?", 0.75),
    ("60150", "2017-11-04", "Tues Nov 4th,", 0.75),
    ("7516458", "2019-12-02",
     "Anons determine significance of 1:29 from [Dec 2] drop?", 0.75),
    # B2-257 pin maintenance (2026-09-26, per the B2-259 law): this
    # judgment-class row re-dated 2019-07-09 -> 2016-07-09 by ladder
    # clause 2 (adjacent-sentence year); re-audited against qdrops.jsonl
    # bytes: the drop's next sentence prints "July 5, 2016" and the
    # pre-edit sweep (B2_257_ladder_probe.py, 6,242 drops) fired clause 2
    # on exactly this one site, receipt
    # watch/inbox/burn_wave_20260926/B2_257_year_ladder_20260926.md
    ("7643939", "2016-07-09",
     "orensicator\u2019s first decisive findings, made public in the "
     "paper dated July 9, concerned the volume of the supposedly"
     " hacked material and what is called the transfer rate\u2014the "
     "time a remote hack would require.", 0.75),
    ("8725298", "2020-01-15", "Why did [Pelosi] hold until Jan 15th?", 0.75),
    ("8954923", "2019-12-16",
     "SWC drop [Dec 16] to closure - coincidence?", 0.75),
    ("8954923", "2020-02-14",
     "Soros invest [Feb 14] Blizzard - coincidence?", 0.75),
    ("9000629", "2020-01-15", "[Jan 15] First COVID-19 U.S.", 0.75),
    ("9000629", "2020-01-15",
     "[Jan 15] [D] Impeachment Articles transfer to Senate?", 0.75),
    ("9091582", "2020-01-24",
     "CNY extend Jan 24 - Feb 9 (avg): 16 days", 0.75),
    ("9091582", "2020-02-09",
     "CNY extend Jan 24 - Feb 9 (avg): 16 days", 0.75),
    ("9105563", "2020-01-15",
     "Why did [Pelosi] then hold impeachment article(s) until Ja"
     "n 15?", 0.75),
    ("9158650", "2019-11-30", "Nov 30 'unmask' needed justification?", 0.75),
    ("9298758", "2020-01-05",
     "Critical thinking _what did [Susan Rice] DECLAS [Jan 5] WH"
     " meeting reveal?", 0.75),
    ("9298758", "2020-01-05",
     "What was really discussed during [Jan 5] meeting?", 0.75),
    ("9298758", "2020-01-15", "COINCIDENCE JAN 15", 0.75),
    ("9791774", "2020-05-08",
     "It is a spiritual battle, which I spoke about in my recent"
     " Appeal which was published on May 8.In society, Mr.", 0.75),
    ("9811683", "2020-06-01",
     "What % [of total] of BLM donations between June 1 - July 1"
     " went to the Biden campaign for president?", 0.75),
    ("9811683", "2020-07-01",
     "What % [of total] of BLM donations between June 1 - July 1"
     " went to the Biden campaign for president?", 0.75),
    ("9812912", "2020-06-01",
     "What % [of total] of BLM donations between June 1 - July 1"
     " went to Biden for president?", 0.75),
    ("9812912", "2020-06-01",
     "What % [of total] of BLM donations between June 1 - July 1"
     " went to [D] party affiliated networks?", 0.75),
    ("9812912", "2020-07-01",
     "What % [of total] of BLM donations between June 1 - July 1"
     " went to Biden for president?", 0.75),
    ("9812912", "2020-07-01",
     "What % [of total] of BLM donations between June 1 - July 1"
     " went to [D] party affiliated networks?", 0.75),
}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def main(ledger: Path | None = None) -> int:
    # --ledger drill arm: audit a copy (canary/manual); the seal below still
    # applies to whatever bytes arrive, so a tampered copy FAILs by design.
    out_path = ledger if ledger is not None else OUT
    if not SRC.exists():
        print(f"FAIL missing source: {SRC}")
        return 1
    rows = []
    bad_json = 0
    with out_path.open(encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                bad_json += 1
                print(f"FAIL line {ln}: not JSON")

    # 1 schema exact
    bad_schema = [
        (i, r) for i, r in enumerate(rows)
        if set(r) != KEYS
        or not isinstance(r["id"], str) or not r["id"].isdigit()
        or not isinstance(r["date"], str)
        or not isinstance(r["claim"], str) or not 0 < len(r["claim"]) <= 320
        or not isinstance(r["confidence"], (int, float))
    ]
    print(f"check1 schema-exact rows: {len(rows) - len(bad_schema)}/{len(rows)}"
          + (f" FAIL {bad_schema[:3]}" if bad_schema else " PASS"))

    # 2 date well-formed
    bad_date = []
    for r in rows:
        d = r["date"]
        try:
            if len(d) == 10:
                date.fromisoformat(d)
            elif len(d) == 7:
                y, m = int(d[:4]), int(d[5:7])
                if not (1900 <= y <= 2100 and 1 <= m <= 12):
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            bad_date.append(d)
    print(f"check2 date well-formed: {len(rows) - len(bad_date)}/{len(rows)}"
          + (f" FAIL {bad_date[:3]}" if bad_date else " PASS"))

    # 3 confidence rubric
    bad_conf = sorted({r["confidence"] for r in rows} - RUBRIC)
    print(f"check3 confidence in rubric: "
          f"{'PASS' if not bad_conf else 'FAIL ' + str(bad_conf)}")

    # corpus index
    drops = {}
    with SRC.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            drops[str(d["id"])] = d

    # 4 grounding
    orphans = sorted({r["id"] for r in rows} - set(drops))
    print(f"check4 ids ground to corpus: {len(set(r['id'] for r in rows))} "
          f"distinct ids, orphans: {'PASS none' if not orphans else orphans[:3]}")

    # 5 traceability (claim inside drop text, whitespace-normalized)
    import html as _html
    from the50_t21_q_caption_ledger import clean_text
    untraceable = []
    for r in rows:
        text = norm(clean_text(_html.unescape(drops[r["id"]]["text"] or "")))
        if norm(r["claim"]) not in text:
            untraceable.append(r["id"])
    print(f"check5 claims trace to drop text: {len(rows) - len(untraceable)}"
          f"/{len(rows)}" + (f" FAIL {untraceable[:3]}" if untraceable else " PASS"))

    # 6 reproducibility (extractor output superset of ledger rows per drop)
    by_id = {}
    for r in rows:
        by_id.setdefault(r["id"], []).append((r["date"], r["claim"], r["confidence"]))
    missing, checked_drops = [], 0
    for rid, want in by_id.items():
        got = {(dt, cl, cf) for dt, cl, cf in extract(drops[rid])}
        checked_drops += 1
        for w in want:
            if w not in got:
                missing.append((rid, w))
    print(f"check6 extractor reproduces ledger: {checked_drops} drops re-run, "
          f"missing rows: {'PASS none' if not missing else missing[:3]}")

    # 7 guard-class regression pin (B2-244, extended B2-242 and B2-243):
    # rejected rows stay absent, pinned keeper rows stay byte-for-byte
    resurgent = [
        r for r in rows
        if (r["id"], r["date"], r["claim"], r["confidence"])
        in GUARD_PINNED_ABSENT
        or (r["id"], r["date"]) in B2_219_MISDATE_PAIRS
        or any(sig in r["claim"] for sig in GUARD_PINNED_CLAIMS)
        or (r["id"], r["date"]) in B2_242_MISDATE_PAIRS
        or any(sig in r["claim"] for sig in B2_242_PINNED_CLAIMS)
        or (r["id"], r["date"]) in B2_243_MISDATE_PAIRS
        or any(sig in r["claim"] for sig in B2_243_PINNED_CLAIMS)
        or any(sig in r["claim"] and lo <= r["confidence"] <= hi
               for sig, lo, hi in B2_243_SCOPED_CLAIMS)
    ]
    keeper_pairs = {(k[0], k[1]) for k in B2_219_KEEPER_ROWS} | {
        (k[0], k[1]) for k in B2_242_KEEPER_ROWS
    } | {(k[0], k[1]) for k in B2_243_KEEPER_ROWS} | {
        (k[0], k[1]) for k in B2_281_YEARFIRST_KEEPER
    } | {(k[0], k[1]) for k in B2_306_CIPHER_KEEPER_ROWS}
    keeper_want = sorted(
        B2_219_KEEPER_ROWS | B2_242_KEEPER_ROWS | B2_243_KEEPER_ROWS
        | B2_281_YEARFIRST_KEEPER | B2_306_CIPHER_KEEPER_ROWS
    )
    keeper_now = sorted(
        (r["id"], r["date"], r["claim"], r["confidence"]) for r in rows
        if (r["id"], r["date"]) in keeper_pairs
    )
    keepers_ok = keeper_now == keeper_want
    keeper_want_set = set(keeper_want)
    pin_msg = (f"resurgent {len(resurgent)}, keepers byte-equal "
               f"{sum(t in keeper_want_set for t in keeper_now)}"
               f"/{len(keeper_want)}")
    if not resurgent and keepers_ok:
        print(f"check7 guard pin (B2-68/B2-220/B2-219/B2-242/B2-243): "
              f"{pin_msg} PASS")
    else:
        extra = [t for t in keeper_now if t not in keeper_want][:2]
        gone = [t for t in keeper_want if t not in keeper_now][:2]
        # B2-275 (spec in the docstring check 7 entry): the FAIL line is the
        # only surface the tripping lane sees, so it carries the pin
        # maintenance law's required steps verbatim (B2-259). The PASS line
        # above stays byte-identical.
        print(f"check7 guard pin (B2-68/B2-220/B2-219/B2-242/B2-243): "
              f"{pin_msg} FAIL "
              f"resurgent={resurgent[:3]} extra={extra} gone={gone}")
        print("PIN MAINTENANCE LAW (B2-259) required steps on every check7 "
              "FAIL: re-audit every differing row against qdrops.jsonl "
              "bytes; re-derive the pin constants from that audit; name the "
              "audit in the landing receipt; never delete or weaken pins to "
              "get green (watch/inbox/burn_wave_20260926/"
              "B2_259_pin_law_20260926.md)")

    # 8 line-ending integrity (B2-239, 2026-09-26). CAUSE: the pre-B2-220
    # on-disk ledger was CRLF (291 CRLF lines, sha 2f3afda8976fe2...) while
    # the generator writes LF (OUT.open newline="\n" in HEAD and working
    # tree), so B2-220's raw byte diff read as full-file churn (1,291c1,289)
    # instead of its true two-row delta. Byte attribution in
    # watch/inbox/burn_wave_20260926/B2_239_line_endings_20260926.md: the
    # CRLF state was content-identical to B2-68's post bytes (LF-normalized
    # sha e1677ba76cf7... equal), the 291-row content survives as dangling
    # blob aba4dbbde7af67b986c9cbdc376e039f9fd13270, and no blob holds the
    # CRLF form: the file was re-materialized by git's smudge filter
    # (core.autocrlf=true; .gitattributes guards only *.rbxlx/*.rbxm per
    # B2-109), not edited by any repo script. FIX: fail while any CR byte is
    # present so an endings-only rewrite cannot masquerade as content drift
    # (or hide real drift inside full-file churn).
    raw_bytes = out_path.read_bytes()
    cr_count = raw_bytes.count(b"\r")
    lf_only = ("PASS" if cr_count == 0 else
               f"FAIL {cr_count} CR bytes (CRLF smudge or default-newline "
               f"rewrite; renormalize to LF via the generator before any "
               f"content edit)")
    print(f"check8 ledger bytes LF-only: {lf_only}")

    # 9 sealed baseline (W3A, 2026-09-29). CAUSE: the gate-canary
    # caption_ledger_verify family proved this gate DEAD on 2026-09-29:
    # deleting a ledger row left RESULT: PASS because every check above
    # builds its denominator FROM the ledger rows it reads (check1 counts
    # the parsed rows; checks 4/5/6 only visit ids still present; check6
    # re-runs drops that still hold rows). EVIDENCE IT IS FIXED: a copy of
    # the live ledger minus its last row must FAIL here on count + sha
    # (tests/test_pin_law_fail_output.py::test_canary_row_deletion_fails_
    # seal replays the exact canary plant). FIX: count and hash the ledger
    # bytes against the SEALED_* constants pinned in this source file --
    # an independent baseline, not the ledger it audits.
    ledger_sha = hashlib.sha256(raw_bytes).hexdigest()
    seal_problems = []
    if len(rows) != SEALED_ROW_COUNT:
        seal_problems.append(f"row count {len(rows)} != sealed "
                             f"{SEALED_ROW_COUNT}")
    if ledger_sha != SEALED_LEDGER_SHA256:
        seal_problems.append(f"sha256 {ledger_sha[:16]}... != sealed "
                             f"{SEALED_LEDGER_SHA256[:16]}...")
    if seal_problems:
        print(f"check9 sealed baseline (W3A): FAIL " + "; ".join(seal_problems))
        print("SEAL MAINTENANCE LAW (W3A): a FAIL here means the ledger "
              "bytes drifted from the seal (deletion, addition, or edit); "
              "re-derive SEALED_ROW_COUNT/SEALED_LEDGER_SHA256 from the "
              "new bytes only after a byte audit named in the landing "
              "receipt; never delete or weaken the seal to get green "
              "(watch/inbox/mates_leave_protocol/W3A_CAPTION_GATE_FIX.md)")
    else:
        print(f"check9 sealed baseline (W3A): rows {len(rows)} + sha256 "
              f"match seal PASS")

    ok = not (bad_json or bad_schema or bad_date or bad_conf or orphans
              or untraceable or missing or resurgent or not keepers_ok
              or cr_count or seal_problems)
    print(f"RESULT: {'PASS' if ok else 'FAIL'} - {len(rows)} rows, "
          f"{len(by_id)} drops, "
          f"span {min((r['date'] for r in rows), default='-')} .. "
          f"{max((r['date'] for r in rows), default='-')}")
    return 0 if ok else 1


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(
        description="Q caption ledger verifier (9 checks; check9 seals the "
                    "ledger bytes against the SEALED_* constants in this "
                    "file, so a tampered --ledger copy FAILs by design)")
    ap.add_argument("--ledger", type=Path, default=None,
                    help="verify this ledger file instead of the live OUT "
                         "(canary/manual drill on a copy)")
    sys.exit(main(ledger=ap.parse_args().ledger))
