# B2-316 receipt: checkbox-receipt gate on the queue (2026-09-26)

## Verdict

LANDED as a standing check, wired beside mag.shared_surface validate per the brief's tools-checker arm. tools/checkbox_receipt_gate.py fails a checked Open row that names no receipt path resolving on disk (NEW debt, row named), accepts the B2-251-attached rows as the named baseline keyed on the "(receipt attachment" marker (71 rows accepted, attachment paths still resolution-checked), and is wired WARN-ONLY into githooks/pre-push so every push carries the trace. Falsifier executed live: a checked row with no resolvable receipt appended to a queue copy is NAMED and the gate exits 1 (before this gate, validate passed it in silence). The first live run also caught 3 real checked-no-receipt rows on today's board.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/QUEUE.md header (board law): "Self-feed law: every landed lane appends 1-3 new briefs here under Open, entered UNCHECKED; only the lane that lands a brief may flip its own checkbox, and the flip carries a pointer to the landing receipt."
- watch/inbox/burn_wave_20260926/B2_251_checkbox_audit_20260926.md (the audit this gate stands up; pointer named in the brief row).
- Falsifier transcript (this lane): queue copy + appended row "- [x] B2-999 Falsifier row: claims work landed but names no receipt anywhere on disk." -> "NEW DEBT: B2-999: checked Open row names no receipt path resolving on disk" -> "CHECKBOX-RECEIPT-GATE: FAIL" exit 1.
- First live run (2026-09-26 ~20:50Z): "388 checked Open rows, 71 baseline-attached, 3 offenders" -> NEW DEBT: B2-178, B2-475, B2-477 -> exit 1.
- githooks/pre-push (new block): "checkbox-receipt gate (B2-316, 2026-09-26, wired beside mag.shared_surface validate per the brief's tools-checker arm) ... WARN-ONLY at the hook (exit 1 prints the NEW DEBT names, never blocks): the gate's job here is trace on every push, the flip to blocking is an operator decision."

## Work done

1. Wrote tools/checkbox_receipt_gate.py (standalone CLI, --queue override, exit 0/1/2): parses checked rows in the Open section with section boundaries pinned to "## Dispensed"/"## Open" only (the board's later annotation headings, e.g. the standing-law note at line 399, do NOT end Open; the naive any-heading parser was blind to the whole tail and was fixed before results were accepted); resolution-checks receipt path tokens; baseline marker handling; offender list naming lane ids.
2. Wired it into githooks/pre-push as a WARN-ONLY block (trace on every push; blocking flip reserved as an operator decision, same convention as the census exit-1 flip), claim law honored (CLAIM SW-05 20:49:06Z, census and caption blocks untouched, bash -n clean). mag.shared_surface.py itself was left alone deliberately: another lane holds it mid-edit above the ratchet line cap.
3. Ran the falsifier (named B2-999, exit 1) and the live board (3 real offenders found, remediation classes named):
   - B2-178: receipt EXISTS on disk (B2_178_freelane_runner_20260926.md) but the row does not name it -> remediation is a pointer attachment by the landing lane, not a revert.
   - B2-475, B2-477: no receipt file under watch/inbox/burn_wave_20260926/ matches -> true B2-238 unearned-flip candidates for their owning lanes to complete or revert.
4. Limitation named honestly: the path matcher accepts any resolvable path token in the row, so a checked row citing an unrelated existing doc could false-pass; the 71-row baseline and the falsifier prove the intended behavior. Tightening to burn-dir-only receipts is a one-line change reserved for the gate's owner lane.

## Falsifier

The brief's falsifier, decided today: append a checked row with no resolvable receipt pointer -> the gate fails naming it (exit 1); today validate passed it in silence. The gate itself dies if: (a) a checked row with no receipt passes (widen falsifier to generated rows with pointer-only typos: a misspelled path must fail resolution and name the row); (b) a baseline-attached row with a dead attachment path passes (the gate checks attachment resolution and already names that class); (c) the pre-push wiring starts blocking (that flip is an operator decision, not landed here); (d) the section parser starts gating Dispensed rows or dropping the Open tail again (the annotation-heading case fixed this lane).

## Bibliography closed

All read this lane: watch/inbox/burn_wave_20260926/QUEUE.md (header laws, section structure, offender rows 432/749/751, claim line), B2_251_checkbox_audit_20260926.md + B2_251_queue_edit.py (pointer), mag/shared_surface.py (validate surface confirmed hot, left untouched), tools/checkbox_receipt_gate.py (written this lane), githooks/pre-push (gate block added, census and caption blocks untouched), QUEUE.md B2-316 row.
