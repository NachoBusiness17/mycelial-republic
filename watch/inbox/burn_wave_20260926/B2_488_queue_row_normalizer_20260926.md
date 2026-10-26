# B2-488 receipt (2026-09-26)

## Verdict

LANDED (both arms). tools/queue_row_census.py is the shared row-reading surface: a strict census, a tolerant census, a tripwire (check) that names every line a strict consumer is blind to, and a dated normalizer (normalize) that rewrites deviations to the canonical checkbox shape. The one live deviation found on today's compacted board was normalized in place (board sha f8b0a0b6c534353b to 46df9aa7bdd4e8ac) and the tripwire is green: strict 466 / tolerant 466 rows, deviations 0, undercount 0.

## Evidence file:line quotes

- The disease this closes (brief text): the Open section carried rows the strict census regex could not see, "the live form is a double space after the dash on the B2-369, B2-370 and B2-371 rows, present on the board at 18:58Z", and the B2-167 census "needed a second tolerant regex to catch them".
- Board state at this lane's normalize time (post the ~21:02Z compaction): zero double-space starts remained (the compaction removed those rows), but one deviation survived: QUEUE.md line 128 packed TWO checkbox rows onto one line - the landed "- [x] B2-77 ... Landed 2026-09-26 ..." note with the original "- [ ] B2-77 ..." brief text embedded after it - invisible to every strict consumer as a second row.
- The normalizer pass output: "normalized 1 line(s); board sha f8b0a0b6c534353b -> 46df9aa7bdd4e8ac; post-census deviations 0". The embedded original brief text was split onto its own indented line (a quote under the landing note, not a row start), so the strict census now sees exactly one row-start there.
- Post-normalize tripwire: "queue census: strict 466 / tolerant 466 rows; deviations 0; undercount 0", exit 0.
- tools/queue_row_census.py: STRICT_ROW = ^- \[[ x]\] B2-\d+<space>; TOLERANT_START accepts any dash/space damage; CHECKBOX_ROW_ANYWHERE additionally catches same-line embedded rows; check exits 1 naming line + shape (malformed-start / multi-row-line) and prints the strict-vs-tolerant undercount; normalize canonicalizes leading starts, splits genuine same-line rows, indents quoted landed-text rows, hard-capped restyling loop (5 iterations), sha before/after printed.

## Work done

1. Scanned the current board for deviations from the canonical shape (the brief's named double-space form plus the same-line embedded form this lane found on the compacted board).
2. Landed the shared parser/tripwire tool with check + normalize + --dry-run arms.
3. Found and fixed two of my own defects before the real pass: an unbounded restyling loop (hard-capped) and a dry-run census that counted embedded rows on not-yet-split elements (normalize now splits embedded newlines so the dry run's post-census is truthful).
4. Ran the dated normalizer pass on the board (1 line, sha-verified) and confirmed the tripwire green.

## Falsifier

The brief's falsifier: "a malformed row-start filed tomorrow changes the tolerant census but leaves every strict consumer blind with no surface naming it". Dead: the tripwire IS the naming surface, and it is one command (`python tools/queue_row_census.py check`, exit 1 with line numbers and shapes). Re-arm proof: any row filed with a damaged start or packed onto another row's line flips check to exit 1 until normalized. Standing honesty note: the tripwire only helps lanes that run it; the receipt recommends wiring check before any queue census claim, and the B2-167 census tool remains the strict-consumer example it protects. The normalize pass touched exactly 1 line (sha-pinned) so any claim that it erased board content is checkable against the before/after hashes.

## Bibliography closed

- tools/queue_row_census.py (new)
- watch/inbox/burn_wave_20260926/QUEUE.md (normalized line 128; sha before/after in the tool output)
- watch/inbox/burn_wave_20260926/B2_167_census.py (STRICT_ROW vs TOLERANT_ROW precedent, pointer from the brief)
- watch/inbox/burn_wave_20260926/B2_251_checkbox_audit_20260926.md (the audit lineage the brief rides)
