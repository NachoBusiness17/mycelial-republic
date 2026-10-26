# B2-188 receipt (2026-09-26)

## Verdict

LANDED. scripts/build_lane_game.py now ends every run with an ACROSS-RUNS transport tripwire: it counts the consecutive HTTP-404 tail of the persistent proposals.jsonl (the record the 3 cron runs each failed to read across their own boundaries), persists the streak in state.json, and fires once per streak at 8 consecutive 404s, naming the dead model, the last real success timestamp, and the successor pointer when a 404 body names one. Replayed against the disease shape (12 consecutive 404s), the alarm fires within 8 deaths, i.e. during the SECOND cron run instead of never.

## Evidence file:line quotes

- The disease: watch/inbox/union_fullsend_20260917/build_lane/proposals.jsonl rows at 2026-09-26T11:29:16-17Z (4), 11:36:10-11Z (4), 11:38:05-06Z (4), all `"model": "stealth/union-alpha", "ok": false, "error": "HTTP 404"`, last real success 2026-09-18; the in-run guard only ends a RUN ("two consecutive transport deaths end this RUN"), so each cron run saw 4 deaths and stayed silent.
- scripts/build_lane_game.py (post-edit): `TRANSPORT_TRIPWIRE_ALARM_N = 8`, `TRIPWIRE = OUT / "transport_tripwire.jsonl"`; `_successor_from_body` (regex pulls the successor model/URL a retirement body names in-band, e.g. "migrate to unbiased/pareto"); `_transport_tripwire(state)` (tail scan of last 64 rows, streak of ok:false rows whose error contains 404, streak persisted to state as transport_404_streak, last success as last_transport_success, alarm appended to transport_tripwire.jsonl + stderr, deduped by signature streak:newest-death-ts); wired in main's finally before the STATE write: `_transport_tripwire(state)  # B2-188`.
- tests/test_build_lane_tripwire.py: 4 pins, 4 passed: alarm at threshold with successor extraction ("migrate to unbiased/pareto" body yields successor unbiased/pareto); silent-below-threshold but streak counted; dedupe (same signature) plus re-alarm on a fresh streak after an intervening success; non-404-newest failure breaks the streak to 0.
- Live smoke: `.venv/Scripts/python.exe scripts/build_lane_game.py --census` still returns the B2-117 frozen census reconciled (denominator 41), so the edit did not disturb the read-only path. py_compile clean. Ratchet check --changed: NEW=0 PASS.
- Shared-file claim law honored: CLAIM zcode-sw-10-b2-188 scripts/build_lane_game.py 2026-09-26T20:28:50Z filed on QUEUE.md line 37 BEFORE the edit (the file was working-tree-modified by sibling lanes B2-55/B2-189/B2-117 whose edits are visible at lines 9, 187-203, 349-364); this lane rebased on those bytes and touched only the new block plus the one finally-line.

## Work done

1. Read the current script bytes after filing the CLAIM (two sibling lanes landed edits in the same hour; rebased on them, no overwrite).
2. Implemented the across-runs streak counter, threshold alarm, successor surfacing, and persistence; wired at run end.
3. Found and fixed a real defect in my first cut via the pins: dedupe keyed on streak LENGTH alone could not distinguish a fresh streak of the same length (a new 9-death streak after a recovery would stay silent forever); dedupe is now the (length, newest-death-ts) signature.
4. Corrected my own break-test ordering (the non-404 failure must be the NEWEST record to break the tail).
5. Verified the census path still reconciles and the ratchet is clean.

## Falsifier

The brief's falsifier shape: 12 consecutive transport-dead generations across runs with no alarm. Replay: append 8+ consecutive `HTTP 404` rows (any ts) to proposals.jsonl, run any code path that reaches the finally block (or call _transport_tripwire directly); the alarm must land in build_lane/transport_tripwire.jsonl naming model, streak, last_success, and successor. Inverse pins: a fresh streak with a newer newest-death-ts must re-alarm (test_dedupe...reset_on_success); a non-404 newest failure must silence it (test_non_404_failure_breaks_the_streak). The tripwire falsifies itself if proposals.jsonl stops being the append-only record (the tail scan trusts it) or if someone lowers TRANSPORT_TRIPWIRE_ALARM_N below the normal 2-death run-end shape and drowns the signal.

## Bibliography closed

- scripts/build_lane_game.py (CLAIM before edit; new block after FROZEN_COMMIT constants; finally wiring; B2-55 flip comment and B2-189 _file_retirement_flip read, unmodified)
- watch/inbox/union_fullsend_20260917/build_lane/proposals.jsonl (rows 95-111 region: the 12x404 evidence + 13:12Z pareto successes)
- watch/inbox/burn_wave_20260926/B2_31_poll_tripwire_20260926.md and B2_55_buildlane_flip_20260926.md (pointers; B2-55's flip already cured the dead primary, this lane adds the alarm that was missing)
- tests/test_build_lane_tripwire.py (4 pins); QUEUE.md CLAIM line 37 (to be retired CLAIMED with this receipt at landing)
