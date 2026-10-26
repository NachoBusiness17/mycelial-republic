# B2-68 caption ledger fraction guard, 2026-09-26

## Verdict

LANDED. scripts/the50_t21_q_caption_ledger.py now rejects proportion reads on the numeric m/d path: a proper fraction (numerator < denominator) immediately followed by a two-token noun phrase with a plural head is excluded, not dated. The id 34917 misdate ("7/10 plane crashes" as 2017-07-10) is gone; the regenerated ledger holds 291 rows (was 292), a byte diff shows exactly one removed line, all other rows identical, and the module verifier passes 6/6. A mechanical rescan of all 291 rows through the same guard predicate finds 0 remaining guard-class misdates.

## Evidence

- qdrops.jsonl:307, id 34917, ts 2017-12-05: `"text": "RED RED 9/11. \nFunds raised vs distributed?\nOversight?\n7/10 plane crashes are targeted kills.\n..."` - the pair has no year, so infer_year picked 2017 (nearest to the drop), emitting 2017-07-10 at confidence 0.65.
- q_caption_ledger.jsonl (pre-edit) line 13: `{"id": "34917", "date": "2017-07-10", "claim": "7/10 plane crashes are targeted kills.", "confidence": 0.65}` - the defect named by MICKEY17_WAVE2_QUALITY_20260925.md:131 ("1/292 rows" audit batch 4.1).
- Guard design verified against all 32 rows the 0.65 path produced: keeper dates survive because they sit behind date markers ("effective 10/30", "on 12/7", "by 11-11", "Article date: 9/16"), inside brackets ("[CLAS 1-9]"), or are followed by non-plural tokens within the two-token window ("10/30 across most" stops at "most"; "6/11 ALMOST OVER"; "10-30 feet").
- Blast radius: B2_68_guard_probe.py sweep over all 6,242 drops prints `NUM_NOY surviving existing guards: 55` and `new guard rejections: 1`, the rejection being id 34917 only.
- Post-edit diff `13d12` (one line) and `grep -c "34917\|plane crashes"` on the new ledger = 0; ledger sha256 e1677ba76cf7f97e226736cdbafd7b90b34232868c3d0bbc5ed9b86f0450cbf0 (pre-edit 21c866c7216871f9530b875153fcbf12742c76d31058f2a569f2bd19e2314e93).

## Work done

Read the generator and verifier in full; enumerated all 32 confidence-0.65 rows; prototyped the guard and swept the whole corpus before editing (probe fires exactly once). Spec first: docstring rubric line 0.65 and the Exclusions list updated before the code. Then added PROPORTION_RE with a fix comment carrying cause + evidence, applied in the NUM_NOY loop after the ORDINAL_RE check. Regen: 292 to 291 rows, 0.65 bucket 32 to 31, drops-with-claims 180 to 179. Verifier: check1 schema 291/291, check2 dates 291/291, check3 rubric PASS, check4 grounding 179 ids 0 orphans, check5 traceability 291/291, check6 reproducibility 179 drops re-run, RESULT PASS. Post-regen predicate scan: 0 guard-class rows. No tests reference this module (pytest -k "caption or the50" collects 0), so the module verifier is the gate; full 12-minute pytest not run, change is in scripts/ outside the mag/+tools/ ratchet scope. Full pytest claim: not run, not needed for a scripts/ artifact with its own verifier.

## Falsifier

Any one kills the verdict: (a) any ledger row whose claim matches `^\s*\d{1,2}/\d{1,2}` with numerator < denominator followed by a two-token plural-head NP (the guard predicate) - rescan must print 0; (b) any of the 31 surviving 0.65 rows changed or removed versus the pre-edit file (diff must stay exactly `13d12`); (c) verifier exiting nonzero or row count not 291; (d) drop 34917 reappearing with any date row; (e) a genuine Q date mention corpus-wide that the new guard rejects (sweep must print rejections = 1).

## Bibliography closed

scripts/the50_t21_q_caption_ledger.py (docstring rubric line 22-23, Exclusions entry lines 36-42, FRACTIONS/PROPORTION_RE block, guard applied at line 254, NUM_NOY loop); scripts/the50_t21_q_caption_ledger_verify.py (6 checks, RESULT PASS); qdrops.jsonl:307; q_caption_ledger.jsonl pre line 13 / post sha e1677ba7...; MICKEY17_WAVE2_QUALITY_20260925.md:131,149; B2_68_guard_probe.py; B2_68_ledger_before.jsonl. No external sources. Queue self-feed: B2-219, B2-220 (drafted B2-217/B2-218; both numbers were taken by a concurrent lane before landing, renumbered highest+1 per house convention).
