# B2-311 Whole-drop year context clause

## Verdict

PROBE LANDED, CLAUSE REJECTED AS SCOPED (the brief's falsifier branch). The drop-scoped clause 2b (single distinct standalone 19xx/20xx year anywhere in the same drop, abstain on disagreement or zero years, valid-date guard, firing only where the landed adjacent-window clause 2 does not) was probed over the full corpus BEFORE any generator edit and FAILS the invariant: it would move 3 sites, and 2 of them are clean 0.75 keeper rows beyond id 437 - id 13061 2018-01-02 -> 2017-01-02 (a 3-sentence drop printing 2017 once) and id 2381818 2018-07-31 -> 2012-07-31 (a 70-sentence drop whose single printed year 2012 sits far from the claim, the weakest possible grounding, exactly the over-reach the falsifier was built to catch). The 7 held judgment rows do not move; id 437 moves exactly as predicted (2018-07-21 -> 2017-07-21 on the drop's "NOV 2017", sentence 9). Per the falsifier ("the 49 clean keepers plus the 7 held judgment rows must not move, else the clause does not land"), clause 2b does NOT land: scripts/the50_t21_q_caption_ledger.py is byte-untouched, id 437 stays 2018-07-21, and the generator's spec (docstring "Year ladder") is therefore never contradicted by behavior.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/B2_311_probe_results.txt (full sweep output, this lane): "clause-3 site multiset vs live ledger 0.75 multiset: EQUAL" (guard precondition), "clause-2b (whole-drop year) delta sites: 3", the three sites quoted, "moves beyond id 437 ...: 2", "invariant violations: keepers moved 2, held judgment rows moved 0", "PROBE RESULT: FAIL (clause does not land)".
- The three sites: `DMY id 437 2018-07-21 -> 2017-07-21 (drop year 2017, drop has 35 sentences)` over the claim sentence "The appointment itself, on 21 July, triggered a shake-up at the Trump White Hou[se]"; `MDY id 13061 2018-01-02 -> 2017-01-02 (drop year 2017, drop has 3 sentences)`; `MDY id 2381818 2018-07-31 -> 2012-07-31 (drop year 2012, drop has 70 sentences)`.
- Probe script: watch/inbox/burn_wave_20260926/B2_311_drop_year_probe.py (clause 2b prototype: whole_drop_year collects gen.SENT_YEAR_RE across ALL drop sentences, abstains on 0 or 2+ distinct, valid-date guard via gen.mk_date; fires only where the re-derived clause 2 adjacent-window did not fire).
- The byte facts the brief asserted, confirmed: id 437's claim sentence sits 15 sentences from the drop's only printed year "NOV 2017" (sentence 9 of 35), and "1,976"-style comma numbers do not match the year pattern (SENT_YEAR_RE), both unchanged from the B2-257 evidence.
- scripts/the50_t21_q_caption_ledger.py: UNTOUCHED by this lane (the rejection arm; sha unchanged, behavior unchanged, id 437 remains 2018-07-21 in the live ledger).

## Work done

1. Read the B2-257 receipt, the generator's ladder implementation (adjacent_year, SENT_YEAR_RE guard, infer_year), and the landed clause-2 semantics.
2. Wrote the clause 2b prototype as a standalone probe reusing the generator's own helpers (clean_text, sentences, SENT_YEAR_RE, MDY/DMY, CANONICAL_MONTHS, SKIP_MD) so the sweep measures the real pipeline, plus the clause-2 precedence re-derivation.
3. Ran the full-corpus sweep: multiset guard EQUAL, exactly 3 delta sites, named both beyond-437 moves, invariant verdict FAIL (2 keeper rows move).
4. Took the falsifier's prescribed branch: the clause does not land; the generator and ledger stay byte-identical; the probe + full output are filed as the decision evidence.
5. Filed this receipt, LEDGER row, QUEUE row.

## Falsifier

The brief's falsifier, executed to its letter: "the sweep must name every 0.75 row a drop-scoped clause would move beyond id 437 and the 49 clean keepers plus the 7 held judgment rows must not move, else the clause does not land." The sweep names them (13061 and 2381818, both keepers), keepers move, so the clause does not land. The landing IS the probe evidence plus the refusal to edit. Reproduction: run B2_311_drop_year_probe.py; PASS would require the delta set to be 437-only or empty. A future landing must either narrow the clause (e.g., whole-drop year only when the drop is short: the 3-sentence 13061 case still moves, so shortness does not save it; distance-bounded year windows are the only surviving shape, a design question for another brief) or re-audit 13061/2381818 by hand.

## Bibliography closed

- watch/inbox/burn_wave_20260926/B2_257_year_ladder_20260926.md (the landed ladder this probes)
- watch/inbox/burn_wave_20260926/B2_257_ladder_probe.py (template; sweep shape reused)
- watch/inbox/burn_wave_20260926/B2_257_ledger_before.jsonl (the merged ledger snapshot used as the live 0.75 multiset; post-B2-258 live ledger state verified equal via the multiset guard)
- scripts/the50_t21_q_caption_ledger.py (helpers; byte-untouched)
- watch/inbox/qdrop_export/qdrops.jsonl (6,242 drops swept)
- watch/inbox/burn_wave_20260926/B2_311_drop_year_probe.py + B2_311_probe_results.txt (evidence, this lane)
- watch/inbox/burn_wave_20260926/B2_243_bucket_audit_20260926.md (the 8 judgment pairs)
- Nothing owed beyond the named design question for any future narrowing brief.
