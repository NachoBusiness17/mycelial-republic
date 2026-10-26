# B2-486 automate the queue double-claim census 2026-09-26

## Verdict

LANDED and biting. tools/queue_dupes_check.py is the promoted census (strict plus tolerant row-start ids, exit 1 on any id claimed by two or more briefs, WARN on malformed row-start forms the strict regex misses, exit 2 when the board cannot be read, --json optional, read-only), and it rides the tools/refold_gate.py payload beside the restore-guard audit with the same fail-closed mapping (2->2 cannot-verify, 1->1 doubles, warnings never fail). Falsifier fired live both directions: appending a second Open row under B2-137 flipped the gate to rc=1 naming the double in one run; removing it returned rc=0. The promotion was immediately justified: the live board carried 20 verbatim duplicate rows minted by tonight's concurrent whole-file restores (the B2-343 disease at board scale: ids 160, 161, 163, 194, 195, 196, 202, 203, 214, 215, 216, 221, 222, 223, 229, 237, 238, 242, 243, 244, every one a byte-identical row pair, zero divergent), deduped keeping one row each, gate green at 444 rows / 444 distinct ids / 0 doubles.

## Evidence file:line quotes

- Live gate runs (2026-09-26): doubled-board probe "QUEUE-DUPES: FAIL, 21 id(s) claimed by 2+ briefs: [137, 160, ...]" rc=1; post-probe-removal and post-dedupe "QUEUE-DUPES: ok, 442 rows, 442 distinct ids, 0 doubles" rc=0 (444 at first green, 442 after two later probe-row removals; the board is a moving target under concurrent restores, the check is deterministic per snapshot).
- tools/queue_dupes_check.py: STRICT_ROW + TOLERANT_ROW regexes (the census's two forms), dupes exit 1, malformed WARN list, board default watch/inbox/burn_wave_20260926/QUEUE.md.
- tools/refold_gate.py (this lane's arm, after the B2-343 restore-guard block): subprocess queue_dupes_check.py --root root; return 2 if 2, else 1 on doubles; WARN/ok lines print into the payload.
- watch/inbox/burn_wave_20260926/B2_167_census.py: the hand-run original (read whole; its strict/tolerant/dupe logic is the promoted spec; the original stays in place untouched).

## Work done

1. Authored tools/queue_dupes_check.py promoting the census (same regexes, gate exit semantics, --json, --board/--root).
2. Claim law: tools/refold_gate.py is untracked (B2-343 lane), CLAIM B2-486 (21:09:55Z) before the edit; the arm inserts after the restore-guard block, nothing else touched.
3. First live run found the board itself double-spent: 20 verbatim duplicate rows from concurrent board restores; audited all 20 pairs byte-identical (zero divergent doubles), deduped keeping the first row of each, gate green. No divergent (two-different-briefs) double exists, so no renumber was owed.
4. Falsifier executed live in both directions (append double -> rc 1 naming it; remove -> rc 0).
5. Note: a refold_gate run during this lane showed 4 failing pins in tests/test_index_fold_host.py from ANOTHER lane's in-flight fold work (uncommitted mjs edits); those pre-date this arm and are not this lane's red.

## Falsifier

Dies if: (a) a second Open row under an existing id leaves tools/queue_dupes_check.py green (rerun the probe); (b) a divergent double (two different briefs on one id) is auto-deduped as if verbatim (the tool reports ids only; healing divergent doubles must go through the B2-167 renumber law, never this tool's keep-first drop-rest shortcut, which this lane applied only to byte-identical pairs); (c) the refold_gate arm stops invoking the census (payload rot).

## Bibliography closed

Read whole: watch/inbox/burn_wave_20260926/B2_167_census.py, tools/refold_gate.py (restore-guard arm pattern), the live board bytes at three snapshots. Commands: queue_dupes_check on healthy/doubled/healed boards, refold_gate with the arm live. Nothing synthesized.
