# B2-263 dash-pair noun-class corpus audit (2026-09-26)

## Verdict

LANDED. Per-noun is the ceiling, and the audit proves it rather than asserts
it. The corpus sweep found every dash-pair followed by any word across all
6,242 drops: 39 distinct follower words, of which 9 sites carry genuine
measure/frequency/duration nouns beyond the guarded list (2-4 years x4,
1-2 minutes, 2-4 days, 1-3 jumps, 1-99 events, 9-11 pages). Running the real
extractor on all 9: ZERO candidates. The misdate risk these sites pose is
already neutralized by the QUANTITY near-window (+-12 chars) which
generically kills unit nouns on the dash path; MEASURE_AFTER_RE's per-noun
list exists only for the frequency class QUANTITY deliberately misses
("times"). A generalized word-class follower guard was built and tested per
the brief's falsifier: it rejects 0 of the 16 B2-219 keepers, 0 of the
3 B2-242 restores, and 0 of "by 11-11" - but every site it would newly fire
on is already dead through QUANTITY, so generalization adds no rejection
while widening the false-fire surface (a regex has no noun/verb boundary).
Decision documented at the guard site (comment-only) and in this receipt; no
guard bytes changed.

## Evidence file:line quotes

- Corpus census (this lane, full 6,242-drop sweep): 39 distinct follower
  words after dash pairs; top counts: q x5, years x4, https x3, full x2,
  then 1 each for pages, protocols, minutes, times, feet, days, jumps,
  events, december, defcon, and 24 others. The measure/frequency-class
  beyond the guarded nouns: years(4), pages, minutes, days, jumps, events.
- The 9 real sites with drop ids and context (this lane, from
  watch/inbox/qdrop_export/qdrops.jsonl bytes): id 2803535 / 175 / 264
  "wait 2-4 years [take a gamble]"; id 6961951 "audited every 1-2 years by
  an independent agency"; id 4618020 "2.2 million attempted access within
  1-2 minutes. Site crashed."; id 10597597 "2-4 days. They will deploy a
  'centralized' picture frame"; id 7355626 "C_A HUMINT domestic placement
  [1-3 jumps primary target]"; id 10134839 "+ CLAS 1-99 events."; id
  148287184 "classified 9-11 pages being released?".
- Extractor ground truth (this lane, running
  scripts/the50_t21_q_caption_ledger.py extract() on those drops): 8 of 9
  return no rows; id 10134839's single candidate ('2020-11-03', ..., 0.75)
  traces to "justify close-limit until Nov 3]" with "[2020]" in the same
  sentence, a true month-name date unrelated to "CLAS 1-99 events".
- Why zero: scripts/the50_t21_q_caption_ledger.py NUM_NOY loop, after the
  seven predicates: "near = sent[max(0, m.start() - 12): m.end() + 12]; if
  QUANTITY.search(near): continue" with QUANTITY covering
  "hours?|minutes?|mins?|seconds?|secs?|days?|weeks?|months?|years?|yrs?|decades?"
  (QUANTITY block, lines 212-218).
- Falsifier run (this lane): the generalized follower
  r"\\s[A-Za-z][A-Za-z'-]*\\b" over the 16 keeper claims (B2_219 receipt
  line 10 list), the 3 restore claims (B2_242 receipt line 5 list), and
  "Resolved by 11-11.": total violations 0. Only two keeper claims contain
  dash pairs at all ("12/7 - 12/17", "Resolved by 11-11.") and neither has a
  word following the pair in guard scope; the other 14 keepers and all 3
  restores are slash/dot forms outside the dash-scoped guard.
- The generalization's redundancy, measured on the audit sites: MEASURE
  fires False on all 6 duration sites (years/minutes/days/jumps/pages/events),
  GENERAL fires True on all of them - but the extractor already emits zero
  candidates there via QUANTITY, so the new fires are all redundant.

## Work done

1. Swept all 6,242 drops for dash-pair + following word; censused the
   vocabulary (39 distinct).
2. Pulled drop bytes for the 9 measure-class sites; ran the module's real
   extract() on each: zero candidates, with the single candidate traced and
   exonerated.
3. Built the generalized word-class guard and ran the brief's falsifier
   against the 16 keepers + 3 restores + "by 11-11": zero violations.
4. Documented the ceiling decision at the guard site in
   scripts/the50_t21_q_caption_ledger.py (comment-only; claim filed first
   per the shared-file law; ast.parse verified; zero guard bytes touched).
5. Filed this receipt; LEDGER row; QUEUE pointer; INDEX registration.

## Falsifier

This audit is inverted if any of the following holds: (a) a future corpus
regen shows a 0.65-or-lower row dated from one of the 9 audited sites (the
"already neutralized" finding was wrong; the noun class must then be
reopened); (b) a new drop exhibits a measure/frequency noun follower that
QUANTITY does not cover AND the seven predicates miss, and it misdates (then
per-noun gained a member, or the class reopened if a stable family emerges);
(c) rerunning the falsifier script's generalized guard rejects any of the 16
keepers, 3 restores, or "by 11-11" (my scope analysis misread the guard
geometry).

## Bibliography closed

watch/inbox/qdrop_export/qdrops.jsonl (6,242 drops swept; site bytes read);
scripts/the50_t21_q_caption_ledger.py (guard block, QUANTITY block, NUM_NOY
loop read; comment-only edit landed); watch/inbox/burn_wave_20260926/B2_219_misdate_classes_20260926.md
(keeper list, line 10); watch/inbox/burn_wave_20260926/B2_242_quantity_bounds_20260926.md
(restore list line 5, times rationale line 11); extract() run locally, no
network calls.
