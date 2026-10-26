# attention-channel: attention feedback contract + eviction-order repair, banked 2026-09-29

Lane: gala wave5-repair, division B, attention-channel. Owed: (1) mag/feedback.py normalizes
casts to good/bad while mag/attention_ranker.py:17 accepts only useful/wallpaper/pin/mute/acted,
so every cast through the flagship pipe was silently rejected while the pipe reported success;
(2) mag/biography.py:526 prepends and beheads memory/attention.md at 40K chars while the patrol
(scripts/census_patrol_daily.ps1 Add-Content :79/:109/:150/:170) and mag/improve.py:535 append
at the bottom, which is the eviction zone of a prepend ring, so real patrol alerts were
destroyed (the 2026-09-26 COLLECT-DRIFT and 2026-09-28 fleet-task-doctor alerts, w4-09);
(3) watch/attention_count_day.txt frozen at "2026-08-07 48" for 52 days. All findings in this
receipt were read or run this session; the source cards are
watch/inbox/burn_reset_20260927/flash50/w4-37.md, w4-09.md, w4-03.md.

## Code changes (all run against by tests, see checks)

1. mag/act.py: new shared attention surface contract. ATTENTION_ALERT_SENTINEL
   ("<!-- attention:alerts-preserved-below -->") marks a preserved alert tail;
   evict_for_prepend(prev, note, cap) prepends newest-first, evicts whole records at
   "\n---\n" boundaries (the old prev[:cap] slice ended mid-identifier: the live file's last
   line ended inside "mag-agent-orc-t27c4ffccad.m" before the repair), and never touches or
   slices the alert tail below the sentinel; the tail is seeded on first write so
   bottom-appenders (patrol, improve) survive every later flood. bump_attention_count() is the
   shared daily meter, format kept "YYYY-MM-DD N" because mag/daemon.py:_attention_over_cap
   (:166-176, not this lane's file) reads it; a stale day or garbage restarts at 0 instead of
   freezing. _do_attention rewritten onto both helpers; over-cap still files the alert and
   suppresses only the push (the good accident, now a contract). act.py:87-131.
2. mag/biography.py: the inline ping block in summarize_session extracted to module-level
   ping_session_record() (biography.py:347-389), routed through evict_for_prepend, each block
   now carries a "- ts:" line (the old template had no timestamp, w4-09 defect 2), and the
   flood meters itself via bump_attention_count (emission parity: the unmetered writer was the
   only survivor, w4-37 law A1/A3). Dedup policy unchanged: ping only on first write, force,
   or incomplete.
3. mag/feedback.py: ONE vocabulary everywhere, the ranker's ALLOWED_SIGNALS
   {useful, wallpaper, pin, mute, acted}; thumbs spellings (good/bad/up/down/positive/negative/
   thumbs-up/thumbs-down) are aliases mapped before the cast (good* -> useful, bad* ->
   wallpaper). A cast the ranker rejects now makes capture return ok False and the CLI exit 1
   (the old pipe recorded ranking: False and returned success: boolean-cosmetic, w4-37 T2).
   Pipe ledger and training row carry the canonical signal. mag.feedback has zero in-tree
   callers (git grep) so the semantics change breaks nothing; dashboard/rest.py:871-874 speaks
   to record_feedback directly.
4. mag/attention_ranker.py: UNCHANGED. It is the canonical side of the unified vocabulary;
   the drift fix lives on the caller side per w4-37 A2.

## Runtime repairs (live surfaces, this session)

- watch/attention_count_day.txt: "2026-08-07 48" -> "2026-09-29 0"; within the hour real
  production biographer pings metered through the new path and it reads "2026-09-29 2".
  The counter is live because the flood now pays the meter.
- memory/attention.md: compacted 40,317 bytes / 124 identical "Session record ready" template
  blocks to a 442-byte seed (header + sentinel). The blocks were zero-entropy pointers; the
  narratives they point at live in memory/biography/derived + memory/biography/index.jsonl
  (one live row per session, biography.py _upsert_index_row). No information lost. Since the
  compaction, 12 real production pings landed through the new contract and the file is 4,839
  bytes, newest-first, whole-block, with a clean preserved zone.

## Tests (the finish line)

- tests/test_attention_feedback_contract.py (7 tests): a cast through flagship mag.feedback is
  accepted by the ranker vocabulary (ledger row signal in ALLOWED_SIGNALS, _feedback() maps
  it); bad lands as wallpaper and reprices a soft item by the ranker's -8 tax through the real
  build_ranked_attention; all thumbs aliases map; native signals pass through (mute forces P5/0
  on a soft item); pipe ledger + training row carry the canonical signal; simulated ranker
  rejection makes capture ok False and main() exit 1; unknown signal rejected loudly.
- tests/test_attention_eviction_order.py (9 tests): patrol-style and improve-style
  bottom-appends survive a 200-ping / ~66KB flood through the 40K cap via the real
  biography.ping_session_record; a second patrol alert joins the first and both survive;
  no headless half-record at any eviction boundary; the new note is never evicted even when
  the cap is smaller than it; the preserved tail is never sliced even past cap; amend dedup
  unchanged; every ping stamps a ts and meters the counter in the daemon-readable shape;
  counter rotates on stale day and garbage; over-cap attention is filed but the push is
  suppressed.
- Full run: 20 passed including the pre-existing tests/test_attention_ranker.py regression
  suite. Adjacent suites touching the edited modules (test_silentpass_batch2,
  test_improve_provider_probe, test_chat_source_agent_workday): 24 passed. Raw output:
  watch/inbox/gala_20260925/wave5-repair/lanes/attention-channel.check.txt

## Violation ratchet (ask step 3)

`.venv/Scripts/python.exe tools/violation_ratchet.py check --changed` exited 1. The four NEW
violations name files this lane never touched (mag/corpus_gap_research.py:663,
mag/corpus_selfsteal.py:476, mag/link_library.py:421, tools/fossil_check.py:73) plus two
GROWTH claims (tools/secret_gate_scan.py, tools/stealth_driver.py): sibling lanes' uncommitted
work in a shared working tree with ~100 modified files. Zero NEW rows name this lane's files
(mag/act.py, mag/biography.py, mag/feedback.py, both new tests); the ratchet's contract is
that only NEW violations fail, so this lane's changes pass the gate and the exit 1 belongs to
other lanes. Recorded honestly rather than suppressed; each sibling owes its own
baseline-update by name.

## Finding reported, not fixed (another lane's file)

During this lane's regression run, six [priority][probe-alarm] lines with pytest-tmp snapshot
refs landed in the LIVE preserved zone. Source:
tests/test_improve_provider_probe.py:132 (test_due_run_probes_once_env_hygiene_snapshot_and_row),
:181 (test_prior_env_value_preserved_and_restored), :192 (test_second_call_after_stamp_is_noop)
run the full probe flow WITHOUT monkeypatching improve.ATTENTION_PATH, unlike the alarm tests
at :225/:241/:252 which do. This is the w4-09 section-1 "test suite writes into the operator's
attention surface" disease, reproduced live. mag/improve.py and its tests are not this lane's
to edit; the six pytest-artifact lines were removed from the live preserved zone and the leak
is left to the improve lane or the operator. Note the structural win: under the old behead
these lines would have been silently destroyed; under the contract they persisted long enough
to be seen and audited.

## Honest limits

- The eviction contract preserves the alert tail but does not yet bound its growth: alerts
  accumulate below the sentinel unbounded. Patrol alerts are rare by construction (non-ok
  verdicts only), so this is deferred, named here, not hidden.
- The counter now meters records and pushes into one number; only the push is capped. Per-class
  operator-seconds budgets (w4-37 A1) remain unimplemented design.
- The live feedback ledger (memory/attention_feedback.jsonl) still has zero real casts; the
  pipe now works and is exit-code-visible, but no operator gesture has settled a trade yet.
- No AGENTS.md or doctrine file was edited by this lane (not owed, not owned).
- em/en dash scan of the five touched code/test files: 0 introduced by this lane's diff
  (verified against git diff; remaining em dashes in act.py x1, biography.py x11, feedback.py x2
  sit on pre-existing lines this lane did not author). Receipt and lane JSON: clean.

## Checks (exact commands, raw output in the check file)

1. pytest tests/test_attention_feedback_contract.py tests/test_attention_eviction_order.py
   tests/test_attention_ranker.py -v -> 20 passed
2. pytest tests/test_silentpass_batch2.py tests/test_improve_provider_probe.py
   tests/test_chat_source_agent_workday.py -q -> 24 passed
3. tools/violation_ratchet.py check --changed -> exit 1, all NEW rows name sibling-lane files
4. python -m mag.feedback meh some-item --source attention-channel-lane -> exit 1, loud
   vocabulary error, zero file writes
5. em/en dash + non-ascii scan of touched files -> no dash introduced by this diff
6. live surfaces: counter "2026-09-29 2"; attention.md 4,839 bytes, sentinel present,
   preserved zone clean of pytest artifacts
