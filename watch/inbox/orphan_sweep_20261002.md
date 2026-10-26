# ORPHAN SWEEP 20261002 (librarian A-division, HOLD-BOTH-DIRECTIONS)

Sweep moment: 2026-10-02 ~14:15Z. Instrument: python claim-check over index_events.jsonl
(8,890 events parsed, 3,082 distinct paths), INDEX.json (2,779 path strings), git ls-files
watch/ (18,819 tracked). Inventory only: nothing registered, nothing deleted.

## HEADLINE

12 strict orphans (untracked by git AND unclaimed by both indexes AND uncited by any
receipt): 8 descent-driver run artifacts in memory/runs/hermes_burn plus 4 files in
watch/inbox. Plus 2 near-orphans (index-blind, git-committed only) and 1,513 git-committed
index-blind files (not orphans by definition; a coverage gap, not lost work).

## SURFACE 1: watch/inbox (top + hermes_burn + model_garden + ractor_engine)

2,932 files (find counts: 1,339 top, 85 hermes_burn, 1,449 model_garden, 59 ractor_engine).
Claim basis distribution (python exact-or-basename check):
- exact-index 1,418 | basename-index-only 1 (model_garden/BATTERY.md; a different
  BATTERY.md elsewhere carries the claim) | git-only 1,513 | NONE 0.
- git-only split: hermes_burn 79/85, model_garden 1,433/1,449, top 1/1,339
  (NIGHT_CLOSE_20261002.md), ractor_engine 0.

Strict orphans found by `git status --porcelain` (7 untracked entries) + per-name greps:

| Path | Bytes | mtime (EDT) | Claimed by | Class |
|---|---|---|---|---|
| gala_20260925/ouroboros/PRIME_JUDGMENT_20261002.STUB1.md | 806 | 10-02 09:11 | none (events=0 INDEX=0 git=0) | REGISTERABLE (cost row already banked in usage.jsonl id GALA_OUROBOROS_PRIME_JUDGMENT_20261002, grep=1) |
| gala_20260925/ouroboros/lanes/fleet_citations.json | 423,167 | 10-02 09:28 | none (0/0/0) | REGISTERABLE (siblings registered: cross-librarian.json events=4, holdings-of-fleet.md events=10) |
| handoff/ZCODE_HANDOFF_README_20261002.md | 5,255 | 10-02 09:07 | none | REGISTERABLE |
| handoff/ZCODE_HANDOFF_session-full_20261002-0900_1ea31bae.zip | 758,590 | 10-02 09:07 | none | REGISTERABLE (758KB binary; fold seat decides commit vs pointer) |

Claimed-but-untracked (no action needed, listed for the fold): cross-librarian.json,
verify_score_table_fps.py, holdings-of-fleet.md, monitor_lane_selfsteal_20261002.md
(registered nonce 2280, index_events tail).

## SURFACE 2: memory/runs/hermes_burn (driver outputs)

23 files, ALL git-untracked (git ls-files grep "hermes_burn/<name>" = 0 for all 23).
Receipt citation via `grep -rilF <basename> watch/inbox --include="*.md"` (trusted
instrument; an earlier glob-form loop returned all-zeros and was contradicted by a deep
grep, so it was discarded). 15 cited (usage.jsonl 168 cites incl AGENTS.md + descent rib;
driver.log 20; driver.beat 11; deepgemm_results 6; lens1_sherpa 4; ds_baseline_results 4;
socratic_results 3; socratic2_results 2; xmodel_cross.* 1 each; judge2_* 1 each;
deepgemm_items 2; ds_baseline_prompt 1). 8 UNCITED = orphans:

| Path | Bytes | mtime (UTC) | Class |
|---|---|---|---|
| assemble_results.jsonl | 9,632 | 10-01T13:54Z | REGISTERABLE (a results file, not just an input batch) |
| assemble_items.jsonl | 1,528 | 10-01T13:54Z | REGISTERABLE |
| assemble_prompt.md | 329 | 10-01T13:54Z | REGISTERABLE |
| socratic_items.jsonl | 1,726 | 10-01T13:26Z | REGISTERABLE |
| socratic_prompt.md | 535 | 10-01T13:26Z | REGISTERABLE |
| ds_baseline_items.jsonl | 1,440 | 10-01T13:09Z | REGISTERABLE |
| socratic2_items.jsonl | 1,230 | 10-01T16:48Z | REGISTERABLE |
| lens1_sherpa_items.jsonl | 5,296 | 10-01T21:30Z | REGISTERABLE |

## SURFACE 3: watch/ top-level, scout, arc_seeds

- watch/scout: 38 files, 38 git-tracked (find vs git ls-files). No orphans.
- watch/arc_seeds: 5/5 tracked. No orphans.
- Newer than 2026-10-01T00:00Z, unclaimed by index events (grep "watch/<name>" = 0) and
  untracked (git=0): room.jsonl 4.9MB, grok_feed.jsonl 9.0MB, summarized_sessions.json
  47KB, heartbeat.json, active_session.json, attention_count_day.txt, mag.pid. All live
  runtime state, regenerated continuously: JUNK (cache class per shared-surface doctrine;
  grok_feed/room content-harvest coverage is OWED below).
- Claimed by git among the recent: PROSE_CENSUS_20261001/02.md, DAY_LEDGER_2026-10-01.md,
  LIBRARIAN_REPORT.md, HUNGER_LEDGER.md, monitor_lane.state. monitor_lane.state is state
  but tracked; leave to fold seat.

## SURFACE 4: git untracked durability

7 untracked entries, all mtime 2026-10-02 09:07-09:28 EDT (under 24h, so the 24h rule
flags none). 4 are index-claimed; the 3 unclaimed are the strict orphans already listed
(stub, fleet_citations.json, handoff/ dir).

## PRIOR FINDING RECHECK: POSITION_CHANNEL_RESULT.md

Status NOW: index_events.jsonl grep=0, INDEX.json grep=0, git ls-files=1 (committed),
mtime 2026-10-02 02:09 EDT, 13,416 bytes. The single-shot post-close creation is STILL
unregistered in both indexes; the git commit is its only claim. Near-orphan,
REGISTERABLE (one register op closes it).

## COUNTS BY CLASSIFICATION

REGISTERABLE 14 (12 strict + POSITION_CHANNEL_RESULT.md + NIGHT_CLOSE_20261002.md)
JUNK 7 (live runtime state files)
DUPLICATE 0 pure (the PRIME stub's cost row is duplicated into usage.jsonl; noted in row)
Index-blind-but-committed 1,513 (coverage gap, not orphans)

## TOP 10 REGISTERABLES AND THEIR LEDGER

1. memory/runs/hermes_burn/assemble_results.jsonl -> hermes_burn run close receipt (new watch/inbox/hermes_burn/ run-register row or TICKET_LEDGER.md widening; TICKET_LEDGER row zero names "wider waves" as owed)
2. memory/runs/hermes_burn/assemble_items.jsonl -> same
3. memory/runs/hermes_burn/assemble_prompt.md -> same
4. memory/runs/hermes_burn/socratic_items.jsonl -> same
5. memory/runs/hermes_burn/socratic_prompt.md -> same
6. memory/runs/hermes_burn/ds_baseline_items.jsonl -> same
7. memory/runs/hermes_burn/socratic2_items.jsonl -> same
8. memory/runs/hermes_burn/lens1_sherpa_items.jsonl -> same
9. watch/inbox/gala_20260925/ouroboros/lanes/fleet_citations.json -> index_events register (md-record-seal autoseal path, same as its two siblings)
10. watch/inbox/handoff/ package (README + zip) -> index_events register + explicit git-add-or-pointer decision by fold seat

## OWED (could not check)

- grok_feed.jsonl (9.0MB) and room.jsonl (4.9MB): JUNK class is provisional; did not
  verify whether their content is harvested into durable receipts.
- handoff zip not opened (binary); README contents unverified.
- Basename-match first pass: a claim hit may come from a same-named file elsewhere;
  exact-path was verified for git (exact rel paths) and for 1,418 exact-index files, but
  the 1,513 git-only class was not per-file receipt-audited.
- model_garden 1,433 git-only files carry only the collective git claim; no per-file
  receipt sweep (out of the 40-recent cap by design).
- Roots outside the mission bound not swept: memory/ minus runs/hermes_burn, corpus/,
  configs/, state/, queue/.
- INDEX.json derivations say 2,580 active items vs 2,932 surface files; delta (superseded
  or parked items) not reconciled.
