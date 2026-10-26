# B2-418 receipt: pin chain-marker placement between the two headers (2026-09-26)

## Verdict

LANDED, fixture-first with a live red-green cycle. The new falsifier fixture (a genuine 2-header chained stanza whose FINAL exception message embeds a newline plus the exact marker sentence at column 0) ran RED before the fix exactly as the brief predicted (chains=2 phantom second link, blocks=2, real=1) and GREEN after mag/improve.py crash_log_census tightened to between-headers placement: a marker line counts only when its line index is strictly between the first and last header line index of the stanza. Full file suite 18/18 passed, including every B2-383 quoted-shape test (mid-message, source echo, type prefix, own-line-without-second-header) - none regressed.

## Evidence file:line quotes

- Brief (QUEUE.md B2-418 row): "the B2-383 hardening counts a column-0 marker sentence in any stanza holding 2+ headers, but CPython prints the sentence BETWEEN the two sections, so a multi-line exception message inside the SECOND traceback of a genuine chained stanza could still land a quoted marker at column 0 and count a phantom second link; tighten to between-headers placement (marker line index strictly between the first and last header line index of the stanza) fixture-first".
- tests/test_improve_crash_scout.py:435 (red run, pre-fix): "assert census['chains'] == 1, census" -> "AssertionError: {'blocks': 2, 'entries': 1, 'test': 0, 'real': 1, ...} assert 2 == 1" (the phantom second link, live).
- mag/improve.py (post-fix, crash_log_census chains block): `lines = body.splitlines()` / `header_idx = [i for i, ln in enumerate(lines) if _CRASH_HEADER in ln]` / `lo, hi = header_idx[0], header_idx[-1]` / `chains += sum(1 for i in range(lo + 1, hi) if _CRASH_CHAIN_MARKER_RE.match(lines[i]))` with the B2-418 cause comment (the B2-383 column-0 rule alone let a 2-header stanza with a quoted tail marker report a phantom second link).
- tests/test_improve_crash_scout.py CHAIN_QUOTED_AT_END_OF_TWO_HEADER_STANZA (new fixture): 2 headers, one real column-0 join between them, then a RuntimeError message quoting the full marker sentence at column 0 plus a trailing operator note line.
- Post-fix run: "18 passed in 0.52s" (was 17 passed + 1 red-deselected state during the red cycle; 17 pre-existing tests stayed green through the change).

## Work done

1. Claimed mag/improve.py (QUEUE.md CLAIM SW-05 21:30:21Z; the file is working-tree-modified; the untracked test file needed no claim but is named in the claim reason).
2. Fixture-first: added CHAIN_QUOTED_AT_END_OF_TWO_HEADER_STANZA + test_quoted_marker_at_end_of_two_header_stanza_counts_one_join asserting blocks=2, entries=1, real=1, chains=1; watched it fail RED at chains=2 (insertion needed two repair passes after heredoc escaping mangled the string literals; final fixture is byte-clean and collection-verified).
3. Applied the between-headers rule in crash_log_census with the cause comment; re-ran the new test (green) and the whole file (18/18).
4. py_compile clean; ratchet check --changed names no hit for mag/improve.py or the test file (the NEW rows in scope belong to other lanes' tools files).

## Falsifier

The brief's falsifier, now a standing test: a 2-header stanza whose final exception message embeds a newline plus the exact marker sentence at column 0 must report chains=1 (the one real join), not 2. It reported 2 before the fix and 1 after; the fixture permanently pins it (any regression re-reddens tests/test_improve_crash_scout.py). The placement rule itself dies if: (a) a real join AFTER the last header exists in some CPython shape (there is none: the final chain sentence always precedes the section it introduces, and the last header is that section's first line); (b) a stanza where the join sits BEFORE the first header (impossible by construction: headers start each section); (c) an indented nested traceback (header not at column 0) breaks the header_idx search - covered because _CRASH_HEADER is matched by substring `in ln`, keeping nested-trace stanzas chain-eligible.

## Bibliography closed

All read this lane: mag/improve.py (_CRASH_STANZA_RE/_CRASH_MARKER_RE/_CRASH_HEADER/_CRASH_CHAIN_MARKERS constants 692-709, crash_log_census 710-800 pre + post), tests/test_improve_crash_scout.py (B2-383 fixtures 336-427, new fixture + test, 18 tests run), QUEUE.md B2-418 row + claim line, tools/violation_ratchet.py check --changed output, watch/inbox/burn_wave_20260926/B2_383_chain_quote_pin_20260926.md (prior falsifier, via queue pointer).
