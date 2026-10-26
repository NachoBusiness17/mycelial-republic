# ACCURACY - dogfood the 48h window (2026-09-30T20:00Z to 2026-10-02T11:00Z)

Lens: accuracy, falsifier-hunter. Filed 2026-10-02 ~10:55Z. Read FIRST and
going beyond: watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md (this file
does not re-derive its findings; it sweeps the same claim classes wider
across all six commits and re-tests the OWED list against the CURRENT tree).
Every check below was run this sitting; commands named per the
instrument-and-moment grammar. No em-dash bytes.

## What byte-checks TRUE on the current tree (ran, not trusted)

- Night-close money core re-derived independently: heredoc python over
  memory/runs/hermes_burn/usage.jsonl, window ts >= 2026-10-01T21:31:24Z,
  re-sums to exactly 43 rows and $5.5208 (matches NIGHT_CLOSE_20261002.md
  receipt; the synthesis's triple-verification now quadruple).
- TICKET_LEDGER row two: watch/inbox/hermes_burn/TICKET_LEDGER.md tail reads
  "issued 65 / run 48 / parked 17", redemption 73.8 pct. Byte-true.
- pidfile guard: scripts/descent_driver.sh:10-23, second instance exit 3,
  stale-pid reclaim, trap cleanup. Byte-true.
- Patrol tasks DIRECT on the live scheduler (MSYS_NO_PATHCONV=1 schtasks
  /Query /V): MagCensusPatrolDaily -> powershell -File
  scripts/census_patrol_daily.ps1; MagFtsIndexDaily -> fts_index_daily.ps1;
  MagImproveDaily -> improve_daily.ps1; MagLeaveProtocolDaily -> direct
  .venv python tools/leave_dispatcher.py. Zero wscript/VBS actions. The
  e3c7d341c MOVE 2 claim is byte-true on schtasks, not just on the receipt.
- citation_lint wired at pre-push: githooks/pre-push:24-25 runs
  tools/citation_lint.py check --changed with exit 1. Byte-true.
- seed_seal: .venv/Scripts/python.exe -m pytest tests/test_seed_seal.py -q
  -> 14 passed in 0.62s (this sitting). The forge-drill claim holds live.
- percolator --candidates: mag/percolator.py:23-25 and :67-68, with the
  zero-ingestion rationale inline. Byte-true.
- corpus-fold 6 entries: six CORPUS_FOLD_*_20261001.md files on disk
  (corpus/steal/, Oct 2 00:07-00:11 NTFS). Byte-true.
- census: fresh run this sitting, .venv/Scripts/python.exe -m pytest
  --collect-only -q -p no:cacheprovider tests at 2026-10-02T10:50:18Z ->
  4147 tests collected in 9.44s. The 10:08Z carrier claim (census_refresh_
  20261002.md:13) holds at a second moment, same count.
- librarian primaries spot-check: corpus/papers_reference_nonredistributable/
  law_dynamo-2007-sosp.pdf and law_lamport-1998-part-time-parliament.pdf
  both exist on disk. Sampled, not census (61 not re-counted).
- garden dollar claims: SWARM_1.md:27-28 "279 clusters total, 50 REAL";
  PREMIUM_AUTOPSY.md:15 "$0.69"; RIB_SWARM_1.md:34 "gen0 best 102.5 ...
  gen1 best 205.0" (that row's cost reads $0.0455, the commit's $0.075 not
  re-derived); SALON1_RACTOR.md:40-87 the S1-Lx law set. Nous $47.54 is
  byte-backed at its probe moment: model_garden/deepseek_api_probe/
  probe_receipts.jsonl:2, P1_balance 200, ts 2026-10-02T00:27:53Z.
- engine topic-undefined fix HELD: the saved ractor-engine workflow now
  declares "arg topic (string, required)" and gate digest 5253afd2d68d
  (amended past the commit's 912a34520349, consistent with the 10-02
  metadata repair), and this very run rode a fully-formed topic.

## The findings (submitted to the swarm)

F1 kpi.jsonl still growing, unrotated. logs/kpi.jsonl read 752,846,276
bytes this sitting (mtime 10:42Z) vs the synthesis's 748,222,017 (~06:55Z):
+4,624,259 bytes in under 4 hours. Writer unchanged (mag/records.py:138
write_kpi; sed this sitting), zero rotation code. Falsifier: a rotation
receipt in watch/inbox, a size drop, or rotation logic at the writer. Move:
one sitting, rotate at writer + last-consumed-offset meter (~30 min; this is
synthesis move 5, still unexecuted).

F2 the awareness layer is still dark: 4 of the synthesis's 8 moves are
unpaid on the tree. NIGHT_CLOSE_20261002.md mtime Oct 2 01:14 EDT = its
creation moment (05:14Z), never edited (move 3 unpaid); scripts/
invisible_runner.vbs mtime Sep 30 10:59 with zero audit code and no audit
jsonl anywhere (move 6 unpaid), and the 23:32 EDT launch is named by zero
receipts (grep across watch/inbox + scripts hit only unrelated
bearableguy_export data); the commit-queue law of 2093ca518 has zero rows in
queue/todo.md, TICKET_LEDGER.md, memory/law/registry.json (move 7 unpaid);
queue/todo.md itself is mtime Sep 29 06:53, and state/CURRENT.md says
updated 2026-09-30T11:56:08Z with "latest result" = last_mile_20260930: the
estate's live-truth pointer predates the entire six-commit window. Falsifier:
any of those files showing post-07:31Z edits paying the moves. Move: one
sitting pays moves 3+6+7 plus a CURRENT.md refresh (~60 min).

F3 the guard landed on the launcher, not the drain, and the estate already
knew. tools/hermes_burn.py (the queue drainer any seat can hand-fire) has
zero claim lock (its only "claim" hit is prompt prose at :156);
tools/ds_workhorse.py zero; the other sleep-loop shell scripts
(astra_convo_loop.sh, vast_ollama_bootstrap.sh) zero pidfile; and the
single-instance doctrine has existed since commit 47d3907e3 (2026-08-25) in
mag/autodrain.py:6 "SINGLE INSTANCE (pid lock) - two loops = double cadence
+ CPU hog (the known failure)" - descent_driver shipped five weeks later
without copying it, burned ~$1.16, and the fix guarded only the launcher.
The T1W2 19:17-19:18Z double-fire cause remains unattributed (grep: zero
receipts), and it predates the twins, so the launcher guard cannot be
assumed to cover it. Falsifier: a claim lock inside the drain tools, or a
receipt attributing the 19:17 double-fire to a launcher-only path. Move:
move the lock into the drain (queue-level claim on (id,turn) or a mutex in
hermes_burn.py, copying autodrain's pattern), ~45 min.

F4 "inference_budget 42 tests" fails the collection instrument. Ran
pytest --collect-only -q on tests/test_inference_budget.py -> 19 tests
collected; paired with tests/test_code_swarm.py -> 28 collected. The file
has no working-tree drift (git diff HEAD empty; landed in 0c9d72a06), so 19
is what the tree holds. The 42 is repeated downstream in
watch/inbox/census_refresh_20261002.md:26 and the AGENTS.md Tests bullet
without its instrument named - the exact B2-216 disease the census laws
exist to kill. Falsifier: a receipt naming the instrument that counted 42
(a pytest -q "42 passed" at its moment, or a case-table count), or
collection at the commit moment reading 42. Move: one sitting, re-count
with a named instrument and correct the two downstream repeats (or name
the 42's source), ~15 min.

F5 what the window cost and what survives (REVISION 1 after the hostile
pass killed one sub-claim; both ledgers re-summed this sitting). usage.jsonl's
first row is 2026-10-01T13:11:41Z: the ledger is blind for the window's
first ~17 hours (the GAP ANALYSIS day and LIBRARIAN morning are unpriced by
this instrument; the garden ledger starts later still, 22:10:27Z). Whole
hermes ledger: 236 rows, $37.7591, 4,368,123 prompt+completion tokens
(python sum, this sitting); last row 21:53:52Z, so the drain has been idle
since and the kill held. WITHDRAWN on steering: my original claim that the
night close's 5,547,496 tokens was "an instrument-mix the receipt does not
name" is false - NIGHT_CLOSE_20261002.md:50 says "usage ledgers" plural and
:52-54 names both files, and my re-sum of exactly those two ledgers'
night windows reproduces every digit: hermes night 43 rows $5.5208
(551,163/295,153/235,478) + garden night 725 rows $3.4746
(2,964,706/906,875/594,121) = 768 rows $8.9954, 5,547,496 tokens with
prompt 3,515,869 / completion 1,202,028 / reasoning 829,599, matching :55-56
exactly. The attack hit a claim the receipt never made. Standing addition
from the same re-derivation: the commit message's "Ledger ~$42 of 145"
re-sums to $41.2337 (hermes whole $37.7591 + garden whole $3.4746), so the
tilde is honest rounding, byte-backed. The bought set survives
byte-true at this moment (seed_seal 14 green, percolator flag, corpus-fold
6, citation_lint at pre-push, patrols DIRECT, census 4,147 twice, founding
primaries on disk, engine topic required) - the window bought durable
instruments; its cost instrument has a 17-hour blind head and the
workflow-side tokens (63.1M + 37.6M + 54.0M + 68.7M per the ask's
ListWorkflowRuns) were not verifiable here (see blind spots).

## OWED (named, never asserted)

- LINKS 250->257 (3c83da5b0): the metric's family is digest link rows
  (FLEET_IMPRINT_20260917.md:1397-1399 numbers LINKS rows), but no live
  counter reading 257 was found; DIGEST.md grep empty. Not verified.
- code_swarm "$0.22" and salon "$0.058" line items: receipts exist, the
  two exact dollar strings were not re-derived this sitting.
- rib_swarm commit cost "$0.075" vs the receipt row's "$0.0455"
  (RIB_SWARM_1.md:34): unresolved, likely a two-run sum; not asserted.

## Blind spots (honest)

- ListWorkflowRuns is unavailable in this session (tool error
  "workflow_introspection_unavailable"): the four workflow token counts are
  ask-given, not verified here.
- WMI process-birth readings and the USN journal were not run (transient /
  admin instruments); the 06:11:22Z WMI reading stands as of its moment.
- The 61 primaries were sampled (2 of 61 byte-checked on disk), not
  censused; the 975-artifact inventory was not re-counted.
- FTS (09:00 EDT) and census (08:30 EDT) direct-task fires are post-window
  today: the DIRECT re-registration is verified on schtasks, but the first
  scheduled fire's exit-0 log line is not yet testable.
- The 110-file uncommitted working tree means tree readings may differ from
  HEAD; where it mattered (test_inference_budget.py) the tree matches HEAD.
- Nous "live balance $47.54" is probe-true at 00:27:53Z and stale after the
  night's later spend; the live balance now was not re-probed (paid call).

Filed by lens-accuracy, ractor run 2026-10-02-dogfood-48h.
