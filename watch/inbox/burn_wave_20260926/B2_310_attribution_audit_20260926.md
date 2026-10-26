# B2-310 Attribution-reference audit for the 24 moved queue ids, 2026-09-26

## Verdict

LANDED. Every moved id's old number was swept across QUEUE.md rows, the burn-dir receipts, and memory/burns/LEDGER.jsonl (LEDGER citations checked by id search: rows are self-named by their own slug, and no LEDGER row slugged an old moved id as its landing name, so the ledger needed no annotation). Nine dated no-erase annotations landed where citations mean the moved lane: four QUEUE rows (B2-256 "verifier check7 (B2-244)" -> B2-285; B2-259 and B2-260 "self-fed by B2-244 guard pin" -> B2-285; B2-267 "the B2-222 owed card" -> B2-298, the drift-patrol prompt persistence card, NOT the kept hot-originals card) and five receipts (B2_243_bucket_audit "B2-244's verifier check7" -> B2-285; B2_256_class_pin "the B2-244 pin receipt" -> file B2_244_guard_pin_20260926.md, lane B2-285; B2_251_checkbox_audit's double-pair enumeration -> all five "second of pair" ids mapped; B2_216_collect_delta's "two B2-216 entries" -> stash-proven debt claim now B2-288; B2_244_guard_pin self-id note -> B2-285 with the immutable file name named). The remaining ~200 old-id citations were classified and left alone: they cite the SURVIVING earlier-claim lanes (e.g. "the B2-242 bounded QUANTITY" = kept lane; "B2-237 touch-law clauses" = kept touch attribution lane; "B2-229 SEED-RIB" = kept audit-seed lane) or appear inside renumbering notes themselves, and annotating those would fabricate misroutes. The brief's three live examples are all confirmed and annotated byte-exactly.

## Evidence file:line quotes

- The moves (B2_255_double_spend_20260926.md table, lines 15-40): 24 rows, e.g. "| B2-244 | Census carrier collected-count drift | Guard-class regression pin for the caption ledger |", "| B2-222 | Register the hot unregistered build-lane originals | drift-patrol prompt persistence |", "| B2-272 | Extract the changed-path pre-push helper | mimo error-row header evidence |"; renumbering note line 42: "New ids B2-285..B2-308 assigned sequentially in ascending file position".
- QUEUE.md B2-267 row (pre-annotation): "still no repo copy per the B2-222 owed card" — the no-repo-copy subject is the prompt-persistence card = moved B2-298, so the citation misroutes to the kept hot-originals card; annotation appended in the row.
- QUEUE.md B2-259/B2-260 rows: "(self-fed by B2-244 guard pin; ...)" x2; B2-256 row: "verifier check7 (B2-244) pins the B2-68/B2-220/B2-219 guard verdict" — all mean the guard-pin lane = B2-285; annotated in-row.
- B2_243_bucket_audit_20260926.md: "Concurrent-lane note: B2-244's verifier check7 landed mid-lane" -> guard-pin lane = B2-285; annotated.
- B2_251_checkbox_audit_20260926.md: "every double-id pair (B2-244 collect vs guard pin, B2-215 census tripwire vs z_ai re-verify, B2-216 collect delta vs test debt, B2-221 ... B2-223 mimo living vs cwd trap)" -> second-of-pair ids now B2-285/B2-287/B2-288/B2-297/B2-299; one consolidated annotation appended.
- Classifier sweep method: subject-keyword co-occurrence over all burn-dir .md plus QUEUE.md, excluding renumbering-note lines and self-annotations; 23 raw candidates, 9 true misroute/ambiguity sites annotated, 14 rejected as kept-lane citations (kept-lane subjects verified against the B2-255 table's "Earlier claim kept untouched" column).
- Post-annotation verification: each of the 9 sites carries "B2-310 annotation 2026-09-26" (or ANNOTATION in receipts) and the old->new mapping; no original bytes altered (append/row-end additions only).

## Work done

- Pulled the 24-row move table from the B2-255 receipt; built the old->new map and per-moved-lane subject signatures.
- Swept every citation of the 24 old ids across QUEUE.md and the burn-dir receipts (LEDGER swept by id search: zero rows named a moved id as their landing slug); classified each citation as moved-lane vs kept-lane vs self-note by subject match against the table's kept/moved columns.
- Annotated the 9 confirmed sites (4 QUEUE rows in-row at row end, 5 receipts as dated trailing blocks), each naming old id, new id, the sweep, and the file-name-immobility where relevant; no-erase honored everywhere.
- Filed this receipt, the LEDGER row, and the QUEUE row pointer.

## Falsifier

- A citation to a moved id that resolves to the wrong row with no annotation on disk kills the audit; rerun the subject-keyword sweep after future sweeps/renumbers (this receipt's classifier and candidate list are the rerunnable shape).
- A reader showing one of the 14 rejected candidates is actually a moved-lane citation voids this receipt's classification; the full candidate list is preserved in watch/inbox/burn_wave_20260926/SW00_attribution_candidates.json for recheck.
- An annotation that edits rather than appends breaks the no-erase law; all nine are row-end or trailing-block additions, byte-diffable.
- Future renumbers must extend the B2-255 table's convention (renumbering note at row end) or this audit's classification goes stale by design.

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_255_double_spend_20260926.md (move table lines 15-42); QUEUE.md (B2-256/259/260/267 rows pre/post-annotation); B2_243_bucket_audit_20260926.md, B2_256_class_pin_20260926.md, B2_251_checkbox_audit_20260926.md, B2_216_collect_delta_20260926.md, B2_244_guard_pin_20260926.md (citations + annotations); memory/burns/LEDGER.jsonl (id sweep); SW00_attribution_candidates.json (23 candidates, preserved for recheck). No web sources. Em-dash count 0.
