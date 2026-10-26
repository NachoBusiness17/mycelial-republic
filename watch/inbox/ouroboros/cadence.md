# OUROBOROS STANDING WAVE: the weekly meta-analysis cadence

Class: SPEC (design, pre-registration) · Wave: gala ouroboros, division B,
lane standing-wave · Written 2026-10-02.

Operator order, verbatim: **"standing wave that shit. oroboros."**

This file turns the order into a cadence: one weekly run that eats the week's
workflow outputs and excretes next week's work orders. The snake's tail is the
week's receipts; the snake's head is next Monday's register. Every claim below
cites a path I read this sitting or a command I ran this sitting (see the lane
check file `watch/inbox/gala_20260925/ouroboros/lanes/standing-wave.check.txt`).

## 1. Why a wave and not another one-shot

- The recursion is already measured, not metaphor: `tools/ouroboros.py`
  (17,034 bytes on disk, verified by ls this sitting) produced
  `watch/inbox/last_mile_20260930/F14_OUROBOROS.md` (2026-09-30), whose verdict
  is GROWS: loop generations G=3, dimensionality D~4.3, receipt inflow 1,807
  in the last 7 filename-days, no fixed point at HEAD. One measurement on
  09-30 is a snapshot; F14_OUROBOROS.md:30 shows the loop state moved at every
  recent application. A snapshot per era is how the 1,341-test headline went
  stale for 12 days (B2-215 tripwire receipt, AGENTS.md census bullet). The
  wave makes the snapshot a cadence.
- The cadence layer that works is the proof of pattern. Verified this sitting
  with `Get-ScheduledTask` (raw output in the lane check file): EstateWalkDaily,
  MagImproveDaily, MagCensusPatrolDaily, MagFtsIndexDaily, MagGapSentinelDaily
  all EXIST and are State=Ready. `.agents/skills/frontier-mine/SKILL.md:31-32`
  carries the law that keeps them alive: "Same fossil-in-feed logic as every
  other organ: research intake that has no cadence dies silently."
- The gap the wave fills is named by the estate itself. The elder lens row
  banked at `queue/lanes/elder/inbox.jsonl` reads: "cadence layer has no
  liveness meter and no answerer-obligation." (grep count 1 this sitting;
  carried into `watch/inbox/ractor_engine/2026-10-01-dogfood-gaps/SYNTHESIS.md:82-84`).
  The weekly wave is the answerer-obligation: a standing hour where the
  cadence layer is asked what it produced and must answer on paper.

## 2. The flywheel law

**Every organ consumes and produces.** An organ that only produces is a firehose
(nobody drinks); an organ that only consumes is a tax (nobody is paid). The
standing fleet already obeys this pairwise (STANDING_WORKFLOWS_20261001.md:24-32:
daily mine -> per-burst gap-analysis -> fill-ball -> ractor-engine -> weekly
librarian), but no organ consumes the FLEET ITSELF on a schedule. F14 measured
that loop by hand once (receipts -> laws -> ribs -> boot -> agents -> receipts,
F14_OUROBOROS.md:13-25). The wave is that measurement plus a verdict plus work
orders, fired weekly instead of when someone remembers.

## 3. What each run CONSUMES (the period's outputs)

One cycle = one ISO week, Mon 00:00 through Sun 23:59 local. The run reads:

| input | surface | evidence this is real |
|---|---|---|
| daily mine digests | `watch/inbox/frontier_olm_<YYYY-MM-DD>/` (DIGEST.md, register.jsonl, percolator_candidates.jsonl, steal/) | member set named at SYNTHESIS.md:26-28; olm-mine fires 10:00 DAILY via cron automation-cac38363 (STANDING_WORKFLOWS_20261001.md:11; frontier-mine SKILL.md:30-32) |
| gap registers | `watch/inbox/gap_analysis_<slug>/GAP_REGISTER.md` | first register landed 2026-10-01, "the lane table for the NEXT 100M-token job" (GAP_REGISTER.md:5-6) |
| fill-ball fills | `watch/inbox/fillball/*.md` | 7 fill receipts on disk this sitting: citation-lint, corpus-fold-land, day1-digest, elder-salvage, errata, percolator-candidates, seed-seal |
| ractor chapters | `watch/inbox/ractor_engine/<slug>/SYNTHESIS.md` + `break-*.md` | two runs on disk this sitting: 2026-10-01-dogfood-gaps, 2026-10-02-dogfood-48h |
| daily-layer liveness logs | `logs/estate_walk_daily.log`, `logs/census_patrol.log`, `logs/fts_index.log` | the PATH LAW + alarm channel pattern at scripts/estate_walk_daily.ps1:1-11; log names carried in SYNTHESIS.md:181-189 |
| the loop itself | re-run `.venv/Scripts/python.exe tools/ouroboros.py --json` | the F14 instrument (F14_OUROBOROS.md:4-6) |

Nothing else. If a surface was dark all week, the run records the darkness as
a finding (a dead week is a result, not an error), per the tri-state claim law.

## 4. What each run PRODUCES

Four artifacts, deterministic names under `watch/inbox/ouroboros/<YYYY-MM-DD>/`
(YYYY-MM-DD = the Sunday fire date):

1. **The cross-dogfood chapters**: a ractor-engine run, slug
   `ouroboros_<YYYY-MM-DD>`, where each lens audits a DIFFERENT workflow's week
   (the operations lens reads fill-ball's fills, the accuracy lens reads the
   gap register's claims, the economics lens reads the mine's digests, and so
   on), landing SYNTHESIS.md + break-*.md under
   `watch/inbox/ractor_engine/ouroboros_<slug>/`. "Chapter" is the house noun:
   SYNTHESIS.md:3 names its own file a "GAP_REGISTER dogfood chapter". Cross
   means no lens audits its own workflow's output.
2. **The Hermes verdict** (the ask's "Hermès verdict"): `VERDICT.md`, written by
   ONE funded-tier judgment dispatch over the chapters (the primes or grok-4.7
   per the DRIVING LADDER, memory/rib/RIB_DRIVING_LADDER_20260928.md; sensing
   stays free-lane). The verdict answers exactly four questions: what did the
   week prove, what died, what was fabricated or hand-copied, and what should
   next week's register rank first. Usage banked per turn in
   `memory/runs/hermes_burn/usage.jsonl` (descent protocol leg 8, AGENTS.md).
3. **The fill-ball orders**: next week's register, AMENDED not rewritten
   (GAP_REGISTER.md:13-15 amendment law), carrying the status / checked-at /
   checked-by columns SYNTHESIS.md:197-200 prescribes, plus the one-sitting
   fill list handed to fill-ball as `{register, slug}` args
   (STANDING_WORKFLOWS_20261001.md:13). This closes the disease the synthesis
   named: "The register works as a work-order and fails as a ledger, and the
   failure is the finding." (SYNTHESIS.md:48-49).
4. **The measure receipt**: `measure.json`, the raw `tools/ouroboros.py --json`
   snapshot for the week (loop graph edges, G, D). F14's numbers (G=3,
   D~4.3 on 2026-09-30) are the baseline the weekly numbers diff against.

## 5. How the tail feeds the head

The flywheel edge, stated as law:

**Week N's fills are week N+1's audited work.** Concretely, three hops:

```
week N fill-ball lands fills  ->  ouroboros-weekly N lists each fill receipt
as a named input of gap-analysis N+1  ->  a fill that survives the audit gets
its status column set (fixed, receipt-cited); a fill that does not survive
RE-ENTERS the register with the audit's evidence; it never silently stays
"closed".
```

This is the same shape F14 measured at corpus scale (bridge receipts both cited
by and citing AGENTS.md, F14_OUROBOROS.md:35) brought down to a weekly gear.
It also answers the SYNTHESIS finding that fixed-never-recorded is the
register's dominant failure mode (SYNTHESIS.md:76-79): the status column only
exists if something is OBLIGED to write it weekly, and the wave is that
obligation with a clock.

**Falsifier (this wave can die honestly):** a cycle that fires and produces no
amended register, no VERDICT.md, no fill orders, and no measure.json is spend
theater. Fix the consumption leg before refiring; if two consecutive cycles
produce nothing consumed downstream (no gap-analysis N+1 names the fill
receipts), kill the cron and demote the wave back to a per-burst manual step.

## 6. Registration proposal (cron day/time)

- **Name:** `ouroboros-weekly` (saved, gate-checked workflow, fired by name;
  reruns are amendments, per the workflow-gate law in AGENTS.md; gate rows for
  the fleet's precedent live in memory/workflows/REGISTRY.jsonl, e.g.
  frontier-olm-mine PASS 2026-09-30T01:18:10Z digest 2487787e949f).
- **When:** **Sundays 11:30 local (America/New_York; 15:30Z during EDT)**.
  Rationale: the last daily mine of the week has landed (10:00 fire,
  STANDING_WORKFLOWS_20261001.md:11), the morning wave is clear (08:00 improve
  and leave, 08:30 census, 09:00 FTS, 09:15 EstateWalk tapestry, 09:45 Estate
  Ratchet per SYNTHESIS.md:182-186), and the verdict is in hand before Monday's
  first lane opens. Sunday is the quietest lane day, so the meta-run's
  children do not collide with burst traffic.
- **How:** the same surface as olm-mine: a zcode cron automation holding the
  saved workflow, NOT a VBS-wrapped Task Scheduler entry. The wrapper is a
  proven S1: scripts/invisible_runner.vbs quote-wraps through cmd /c and four
  cadence tasks burned red through it (SYNTHESIS.md:108-121, twelve tasks
  non-zero that night); the EstateWalkDaily direct-execution + absolute-path
  pattern is the registration shape that survived (scripts/estate_walk_daily.ps1:5-11).
  A future Windows task, if ever wanted, copies that pattern.
- **Width:** modest fan-out (8-15 lanes, one per workflow audited plus
  synthesis), max_concurrency 3 or less per the fan-out width law
  (AGENTS.md: workflow children get maxAttempts 0 and die on first 429/1302).
- **First cycle:** cycle zero already happened by hand; it is the receipts in
  section 7. The first scheduled cycle is the next Sunday after the operator
  approves the saved workflow (the one-time SaveWorkflow approval is the
  harness contract, AGENTS.md workflow-gate section).
- **Cost:** one funded-tier judgment turn per cycle (the Hermes verdict) plus
  local/free lenses; expected order $0.2-2.0 per cycle based on the burn
  ledger's per-turn rows (usage.jsonl rows cited in
  watch/inbox/ractor_engine/2026-10-01-dogfood-gaps/break-economics.md:44 ran
  $0.0458-$0.1571). If a cycle's chapters need more than one premium turn,
  the checkpoint-climb law applies: one landed deliverable per turn.

## 7. First-cycle receipt references (cycle zero, all on disk)

- `watch/inbox/last_mile_20260930/F14_OUROBOROS.md`: the recursion measured
  2026-09-30; G=3, D~4.3, verdict GROWS; the narrow waist named honestly
  (receipts -> laws absorbed only 15 of 3,070 receipts, :21; laws -> ribs 2/44, :22).
- `watch/inbox/STANDING_WORKFLOWS_20261001.md`: the fleet card and the standing
  loop this wave rides (lines 24-32); "What is NOT standing yet" (:40-45) is
  the standing order this spec partially fills.
- `watch/inbox/gap_analysis_20261001/GAP_REGISTER.md`: the first register
  (written 2026-10-01 by lane a15-rollup, 8 sibling lanes merged, :1-15).
- `watch/inbox/fillball/`: the 7 fill receipts of fill-ball 1001, the first
  tail the head will eat (card line 13: 7/7 closed same-night).
- `watch/inbox/ractor_engine/2026-10-01-dogfood-gaps/SYNTHESIS.md`: the
  closure-recording thesis, the wrapper kill, the register's missing status
  columns; the wave's product 3 is that move, scheduled.
- `watch/inbox/ractor_engine/2026-10-02-dogfood-48h/`: the 48h dogfood
  chapters (SYNTHESIS.md + break-*.md on disk; the RACTOR DOGFOOD commit
  e3c7d341c in git log).
- `queue/lanes/elder/inbox.jsonl`: the elder row that names the hole
  ("no liveness meter and no answerer-obligation").
- `scripts/estate_walk_daily.ps1:1-11`: the registration pattern (absolute
  paths, loud alarm channel, receipt-bearing header).
- `tools/ouroboros.py`: the measuring instrument (17,034 bytes, ls this sitting).

## 8. The consumption chain, end to end (text diagram)

```
DAILY CADENCE LAYER (armed, Ready per Get-ScheduledTask 2026-10-02)
  08:00 MagImproveDaily + MagLeaveProtocolDaily
  08:30 MagCensusPatrolDaily          (logs/census_patrol.log)
  09:00 MagFtsIndexDaily              (logs/fts_index.log)
  09:15 EstateWalkDaily               (bakes the tapestry, scripts/estate_walk_daily.ps1)
  10:00 olm-mine                      (zcode cron automation-cac38363)
        |
        v
PER BURST (unchanged, STANDING_WORKFLOWS_20261001.md:28-29)
  gap-analysis -> fill-ball -> ractor-engine
        |
        v  accumulates all week
WEEK N OUTPUTS  =  THE TAIL
  frontier_olm_<day>/  gap_analysis_<slug>/  fillball/*.md
  ractor_engine/<slug>/  librarian/salon/wide-dig/drop-dig receipts
        |
        v
SUNDAY 11:30  OUROBOROS-WEEKLY  =  THE WAVE  (PROPOSAL)
  consumes: the tail (section 3) + fresh tools/ouroboros.py measure
  produces: cross-dogfood chapters + Hermes VERDICT.md
            + amended register + fill-ball orders + measure.json
            (watch/inbox/ouroboros/<YYYY-MM-DD>/)
        |
        v
WEEK N+1  =  THE HEAD
  gap-analysis N+1 consumes week N's fill receipts as named inputs
  fill-ball N+1 lands the new register's top one-sittings
  ractor-engine rides whatever stays ambiguous
  ... and those fills are week N+2's audited work: the snake eats forward
```

## 9. Laws the wave carries in every ask

Never fabricate (unverified is OWED, never asserted) · no em-dash anywhere ·
cite path:line or URL · byte-check before banking · hostile second pass before
speaking · receipt or it didn't happen · tri-state claims (ran / read / owed) ·
the measure is named (instrument + moment) before two counts are compared
(census law B2-216).

## 10. What this spec does NOT do (honest edges)

- It registers nothing by itself. The cron automation is created when the
  operator approves the saved `ouroboros-weekly` workflow; this file is the
  design the approval is for.
- It does not replace per-burst gap-analysis; it audits the auditors weekly.
- It does not widen the fan-out width envelope; Sunday 11:30 was chosen partly
  so the standing envelope never sees it (AGENTS.md max-concurrency law).
- The Hermes verdict is one funded turn by design; if the chapters outgrow one
  turn, the verdict gets climbed, not skipped (descent protocol legs 3-4).
