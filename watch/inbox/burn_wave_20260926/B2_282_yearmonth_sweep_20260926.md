# B2-282 sweep the year-first year-month shape 2026-09-26

## Verdict

LANDED as the non-rule arm. The full-corpus sweep ran over all 6,242 drops with the brief's pattern plus the dash-join variant: exactly 2 candidate "YYYY Month" sites, BOTH false or subsumed, so NO rule is written; the decision is documented as an Exclusions note in scripts/the50_t21_q_caption_ledger.py (the owning spec doc, landed before any code, and here no code follows at all) naming the sweep, both sites, and the re-open condition. The falsifier's two dead-ends are both addressed: a claimed zero would have been falsifiable by the recorded sites (they are named and classified, not hidden), and no rule exists whose probe could fire on a non-year-first sentence.

## Evidence file:line quotes

- Sweep results (watch/inbox/burn_wave_20260926/B2_282_yearmonth_sweep_results.json): pattern (?<!\d)(19|20)\d{2}\s+(jan|feb|...|dec)[a-z]*\b over 6,242 drops -> site 1842655 match "2017\nJune" (context: ">>1842592 Jan 20, 2017 June 20, 2018 Exactly 17 months...") and site 7175228 match "2041 Dec" (context: "Declassify On: 20411231   2041 Dec 31  This has been declassified..."). Dash-join variant total: 3.
- Site classification: 1842655's "2017 June" is a line-wrap artifact (the June belongs to "June 20, 2018"; a year-MONTH rule would mint false "2017-06"); 7175228's "2041 Dec" is a prefix of "2041 Dec 31", already extracted at 0.90 with the day by the B2-258 YEAR_FIRST rule (scripts/the50_t21_q_caption_ledger.py documents this; ledger verifier confirms span includes 2041-12-31).
- scripts/the50_t21_q_caption_ledger.py Exclusions section (post-edit): the year-first year-MONTH-only non-rule note with the pattern, both sites, and the re-open condition; py_compile clean; module imports clean.

## Work done

1. Read the B2-258 pre-edit sweep (probe + receipt) and the MONTH_YEAR/YEAR_FIRST state in the generator; confirmed the B2-258 pre-edit sweep covered "YYYY Month D" (with day) but not the year-MONTH-only form.
2. Ran the brief's pattern plus the dash-join variant across all 6,242 drops, joined sites to qdrops.jsonl ids, classified both sites (false-positive line wrap; subsumed prefix).
3. Landed the non-rule Exclusions note in the generator's Exclusions section (spec-first; zero code change), naming the sweep, both sites, the would-be false rows, and the re-open condition.
4. Verified no regression: py_compile clean, module import clean, caption ledger verifier RESULT: PASS (267 rows, 163 drops, span 1993-06 .. 2041-12-31, all 7 checks including guard pins).

## Falsifier

Dies if: (a) a future sweep finds a TRUE standalone year-MONTH site (a classification banner quoting only "YYYY Month" with no day elsewhere in the sentence) while the Exclusions note still says the shape is unwritten (re-open the note with a new sweep, then a 0.55-precision rule would need the probe-then-edit discipline); (b) the note's cited sweep results file diverges from the recorded pattern (rerun); (c) the ledger verifier stops passing with this note present (the note must stay documentation-only).

## Bibliography closed

Read whole: scripts/the50_t21_q_caption_ledger.py (Exclusions section, MONTH_YEAR, canonical-month guard, YEAR_FIRST doc), watch/inbox/burn_wave_20260926/B2_258_yearfirst_probe.py, watch/inbox/qdrop_export/qdrops.jsonl (6,242 rows swept). Bytes: sweep results JSON on file; verifier PASS observed live. Nothing synthesized.
