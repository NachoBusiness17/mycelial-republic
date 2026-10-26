# wo12_paths.md - lane B (wo12-paths) receipt, mickey17_v2 GO item 7 sibling sweep

Filed 2026-10-04 by wo12-paths (lane B), finishing the finding lane 7
(queue-truth-a14) recorded in watch/inbox/go_wave_20261004/queue_truth.md:
"8 sibling WO-12 todo lines still cite queue/Q-0xx.md paths that do not
exist". Method per lane 7: test the cited path, find the real file, fix in
place with an inline fix receipt (cause + evidence). Strike pattern from
watch/inbox/NIGHT_CLOSE_20261002.md move 2 was read and kept ready but was
not needed: every dead citation's target file exists.

## Enumeration (job step 1)

Every todo line citing a queue/Q-0xx.md path was enumerated with
`grep -n "queue/Q-0" queue/todo.md`. 24 lines carry the citation shape
`Q-0xx (queue/Q-0xx.md)` with a repo-root queue/ path:

Q-003 (todo line 33), Q-007 (:104), Q-008 (:126), Q-010 (:129), Q-011
(:130), Q-020 (:146), Q-021 (:147), Q-022 (:148), Q-023 (:149), Q-026
(:152), Q-027 (:153), Q-031 (:162), Q-033 (:195), Q-034 (:196), Q-036
(:198), Q-037 (:203), Q-039 (:218), Q-040 (:223), Q-041 (:224), Q-042
(:225), Q-043 (:245). That is 21 lines, not the 8 lane 7's receipt named
(it named Q-003, Q-007, Q-020, Q-021, Q-022, Q-023, Q-026, Q-027); the
other 13 sit in the same WO-12 close notes elsewhere in the file and are
the same rot class, so they were swept too.

Each was existence-tested before the edit with the loop below. All 21 old
paths are dead: `ls queue/` shows zero Q-*.md files at repo-root queue/
(PITCHES_NEXT.md, STANDING_RAILS.md, queue_index.jsonl, todo.md, and
subdirs only). Pre-existing correct cites left untouched: Q-002 (line 32),
Q-005 (:98) and Q-025 (:151) already fixed by lane 7, Q-024 (:150), Q-028
(:154), all carrying the full burn_reset path already.

## Real location (job step 2)

`find . -name "Q-0*.md" -not -path "./.git/*"` returns exactly one
directory repo-wide: watch/inbox/burn_reset_20260927/queue/ (39 Q-0*.md
files). queue/queue_index.jsonl agrees: its close_receipt fields point at
watch/inbox/burn_reset_20260927/queue/Q-0xx.md (checked Q-003 and Q-021
rows directly). Per-target loop (pre-edit):

    for id in 003 007 008 010 011 020 021 022 023 026 027 031 033 034 036 037 039 040 041 042 043; do
      old="queue/Q-$id.md"; new="watch/inbox/burn_reset_20260927/queue/Q-$id.md"
      if [ -e "$old" ]; then o="OLD-EXISTS"; else o="old-dead"; fi
      if [ -e "$new" ]; then n="NEW-OK($(stat -c%s "$new")B)"; else n="new-MISSING"; fi
      echo "Q-$id: $o -> $n"
    done

Output: 21 lines, every one `old-dead -> NEW-OK(n B)`, sizes 3057B to
9303B. Zero strikes needed and zero struck: all 21 targets exist.

## Fixes applied

21 single-string edits to queue/todo.md, one per line, each replacing
`Q-0xx (queue/Q-0xx.md)` with
`Q-0xx (watch/inbox/burn_reset_20260927/queue/Q-0xx.md; path fixed
2026-10-04 wo12-paths, the cited queue/Q-0xx.md never existed)`, mirroring
lane 7's inline fix-receipt shape on lines 98 and 151. Original claim text
on every line is otherwise untouched. No git commit (queue/todo.md is
git-ignored by design, .gitignore:51; the file is the live shared surface).

## Proof (job step 3), commands + output

1. No dead-shaped citations remain:

    grep -oP '(?<!burn_reset_20260927/)\(queue/Q-[0-9]+\.md\)' queue/todo.md

   Output: empty, exit 1 (zero matches).

2. Every paren-cited Q path exists on disk (the verification loop; note
   `tr -d '\r'` is load-bearing, the file is CRLF and a bare while-read
   over grep -o output tests "path\r" and fails every line):

    grep -oP 'Q-[0-9]+ \([^)]*\.md[^)]*\)' queue/todo.md \
      | grep -oP '\(\K[^;)]+\.md' | tr -d '\r' | sort -u \
      | while read p; do if [ -e "$p" ]; then echo "OK   $p"; else echo "DEAD $p"; fi; done

   Output: 24 lines, every one OK: Q-002, Q-003, Q-005, Q-007, Q-008,
   Q-010, Q-011, Q-020, Q-021, Q-022, Q-023, Q-025, Q-026, Q-027, Q-031,
   Q-033, Q-034, Q-036, Q-037, Q-039, Q-040, Q-041, Q-042, Q-043, all under
   watch/inbox/burn_reset_20260927/queue/. Q-024 and Q-028 are cited in
   prose (after a +, not the Q-id paren shape) and were proven by the
   sibling loop over all full burn_reset paths
   (`grep -oP 'watch/inbox/burn_reset_20260927/queue/Q-[0-9]+\.md'
   queue/todo.md | sort -u | tr -d '\r' | while read p; ...`): 26/26 OK.

3. Fix marker count: `grep -c "path fixed 2026-10-04 wo12-paths"
   queue/todo.md` = 21.

4. Integrity: file still uniform CRLF (`grep -c $'\r$' queue/todo.md` = 279
   = `wc -l < queue/todo.md`); zero em/en-dash bytes in the added segments
   (`grep -oP 'path fixed 2026-10-04[^)]*' queue/todo.md | grep -cP
   '[\x{2013}\x{2014}]'` = 0); no double-path mangling (`grep -c
   'burn_reset_20260927/watch' queue/todo.md` = 0, `grep -c 'queue/watch'
   queue/todo.md` = 0).

## Files touched

- queue/todo.md (21 lines: the 21 citation fixes above)
- watch/inbox/go_wave_20261004/wo12_paths.md (this receipt)

## Blockers

None. One observation for the record: the "8 sibling lines" figure from
lane 7's receipt undercounts; the true dead-citation count was 21 and all
21 are now fixed. The whole class traces to the 2026-09-29 queue-closes
WO-12 sweep writing repo-root queue/Q-0xx.md paths while the burn_reset
wave of 2026-09-28 had filed the receipts under
watch/inbox/burn_reset_20260927/queue/ (root cause named in lane 7's
receipt and in the Q-005/Q-025 close_notes).

Filed by wo12-paths, 2026-10-04. $0 metered. No em-dash bytes.
