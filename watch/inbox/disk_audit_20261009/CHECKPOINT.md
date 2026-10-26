# CHECKPOINT - disk-storm audit verdict + cleanup GO menu - 2026-10-09

One page. Everything below is byte-backed; every number's source is named.
Your GO executes Phase 1-5 of the runbook; nothing deletes before it.

## THE VERDICT

- WHAT HAPPENED: the burn era (09-21 onward) wrote tool-call stdout with no
  cap and no expiry. Storm peak 61GiB/day (10-04); 309.12GiB total in 11,079
  files. Sources: evidence_pack/digest.md, internal/TIMELINE_AND_ESTATE_LAW.md
- WHAT THE DATA WAS: junk and normal logs - nothing precious. Top-8 giants
  (64.16GiB, 20.8%) are identical full-disk `find` dumps + one runaway FINDSTR
  loop. Sources: giant-file heads, internal/ATTRIBUTION.md
- WHO WROTE IT: 82.8% (255.9GiB) maps to 30 named burns, zero unmapped; top 3
  spore-sharing ractor 34.9 / external-steal ractor 24.8 / OLM mine day-4 23.6
  GiB. Interactive seats innocent. Source: internal/ATTRIBUTION.md
- IS ANYTHING AT RISK IF WE DELETE: no. Durable work landed in watch/inbox
  receipts, physically separate - verified by sampling. One bookkeeping flag:
  dwfrun-c13997d8 (5.95GiB) left no receipt dir; its name survives only in
  sibling receipts. Source: internal/ATTRIBUTION.md
- YOUR 36H CLAIM: retracted by you, confirmed by curve - ~2-week ramp, not 36
  hours. The felt size was right; the clock was not. Source: digest.md curve,
  OPERATOR_CORRECTION_GROWTH_CLAIMS.md
- TWO ZOMBIES FOUND: hourly 24/7 free-burn kept firing 3x1M-token agents
  through your freeze (deleted, recipe banked, restore on your GO post-law);
  the every-10-min flash dispatcher no-ops since 09-27 and I cannot delete it
  from this seat - YOUR 10-SECOND KILL: Automations page, "Flash-lane burn
  dispatcher". Source: CRON_FREEZE_20261009.md

## THE GO MENU (runbook: runbook/CLEAN_RUNBOOK.md)

| Phase | What | Yield | Who |
|---|---|---|---|
| P0 | AV exclusions + fixed 40GB pagefile + docker vhdx compact | ~114GB | YOU (admin) |
| P1 | giant-junk pass (>1GiB find/FINDSTR signature, content-gated, dry-run first) | ~100GiB | seat |
| P2 | retention purge (mtime 7d+) | 81.2GiB today, ~300 with daily retention | seat |
| P3 | HF purge (4 models, re-download manifest banked first) | ~58.2GB | seat |
| P4 | re-enable 3 schtasks (fleet/hermes247/gauntlet); hourly churn restore stays separate | 0 | seat |
| P5 | smith BEFORE/AFTER strip + df | the receipt | seat |

Total ~353GB class -> free space 480-520GB. One decision owed in P0: the close
doc said "five seats" but named four AV roots; the fifth (AppData\Local\Temp)
is your call.

## THE NEVER-AGAIN (law pack, lands after your GO - preview)

The standing-wave budget (your coinage - the stolen 5-hour window):
1. PER-CALL STDOUT CAP - the #1 external steal; Claude Code / OpenHands /
   Docker all converge on the same shape; kills the monster class at source.
2. RETENTION CONTRACT on the smith daily - Gemini CLI's knob shape
   (enabled/maxAge/maxCount/minRetention) under a journald-style budget.
3. BURN ORDERS CARRY GB/DAY - intended vs actual, smith deltas adjudicate.
4. FREEZE SWEEPS BOTH REGISTRIES - schtasks + session crons, one receipted pass.
5. LAYOUT LAW - dated workspaces, mandatory receipt dirs (the c13997d8 cure),
   lifecycle classes, index-first moves with redirect stubs. Spec in flight.

## THE REAL TAIL RISK (higher than any purge)

The durable estate (ribs, receipts, memory) has no off-box copy: github holds
the curated public face only, the backup remote is the same C:. The 5TB cloud
offload (banked 09-30 plan) is the highest-value unexecuted item.

## RECEIPT INDEX

WAVE_PLAN.md / harvest_exec_forest.py / evidence_pack/ (digest + json +
samples) / internal/TIMELINE_AND_ESTATE_LAW.md / internal/ATTRIBUTION.md /
external/PRIOR_ART_CARDS.md / runbook/CLEAN_RUNBOOK.md / LESSONS.md (11
lessons incl. your standing-wave coinage) / CRON_FREEZE_20261009.md /
OPERATOR_CORRECTION_GROWTH_CLAIMS.md. Pending: ORGANIZATION_SPEC.md (Lane G),
law pack (Lane D, post-GO build).
