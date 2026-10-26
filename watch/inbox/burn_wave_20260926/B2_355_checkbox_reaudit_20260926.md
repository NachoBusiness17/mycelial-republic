# B2-355 checked-Open-row receipt re-audit, second pass 2026-09-26

## Verdict

Landed, CLEAN PASS this sweep: every one of the 169 checked Open rows carries at least one watch/inbox receipt .md pointer that RESOLVES to a file on disk (earned 169 / ghost 0). The B2-337/B2-338 ghost shape from the first-pass audit has not recurred in the current generation. The B2-343-class damage this lane DID catch live was the opposite op - whole-file board RESTORES erasing landed rows and earned flips (this lane's own flips were erased twice and re-applied from the durable LEDGER; a 20-row verbatim duplicate band from the same restores was caught by the new B2-486 census gate and deduped). No flipping writer could be named for THIS pass because there are no unearned flips in the scanned generation to attribute; the erase-side attribution is carried in the re-applied rows' annotations and in the B2-486 receipt.

## Evidence file:line quotes

- Sweep method (this lane, read-only): scanned the "## Open" section of watch/inbox/burn_wave_20260926/QUEUE.md; for every line matching ^- [x] (B2-\d+) extracted each watch/inbox/... .md pointer and tested existence on disk.
- Result bytes: checked Open rows 169; earned (resolvable receipt) 169; ghost (no resolvable receipt) 0. The B2-251 sweep shape (resolvable landing receipt or bust, flip unearned to [ ]) had nothing to flip.
- Disease recurrence captured live this evening (related, restore-side): this lane re-applied 6 fully-erased landed rows and 5 erased landing notes from durable records (annotations on the re-filed rows name it), and tools/queue_dupes_check.py measured 20 verbatim duplicate rows across ids 160..244 (B2_486_queue_dupes_gate_20260926.md), all deduped.

## Work done

1. Re-ran the B2-251 sweep shape over the whole Open section (169 checked rows) with a resolvable-receipt existence test per row.
2. Zero unearned flips found: nothing to flip to [ ], no no-erase annotation owed this pass.
3. Named the evening's actual board disease (concurrent whole-file restores erasing rows/flips and minting verbatim duplicate rows), with the live measurements and the durable-record re-application already landed this lane (B2-486 receipt + the re-applied rows' annotations).
4. Writer attribution attempt: the index events log carries no flip-writer events for this generation because no unearned flip exists to attribute; the erase events are outside the events log's surface (whole-file restores bypass it, which is exactly the B2-343 restore-guard finding this wave landed).

## Falsifier

Dies if: (a) a checked Open row with no resolvable landing receipt survives this sweep (rerun the census; any future ghost is immediately attributable by diffing generations); (b) the board's restore disease erases this receipt's own row again without the durable LEDGER row preserving the verdict (the LEDGER row and this file are the durable copy).

## Bibliography closed

Read whole: watch/inbox/burn_wave_20260926/QUEUE.md Open section (169 checked rows scanned), watch/inbox/burn_wave_20260926/B2_251_checkbox_audit_20260926.md shape (pointer from the brief), watch/inbox/burn_wave_20260926/B2_238_checkbox_law_20260926.md shape, watch/inbox/burn_wave_20260926/B2_337_ghost_resolve_20260926.md disease-recurrence pointer. Bytes: per-row existence tests executed live this pass. Nothing synthesized.
