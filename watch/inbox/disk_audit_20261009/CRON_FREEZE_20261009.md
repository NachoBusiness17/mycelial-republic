# CRON FREEZE 2026-10-09 - two ZCode burn automations paused, recipes banked verbatim

Found during the operator's "am I bugging / am I being steered" integrity check
(same window as the disk audit). The 10-08 shutdown order disabled the three
schtasks churn tasks (MagFreeLaneFleet / MagHermesBurn247 / MagGauntletFree30,
verified Disabled) but two ZCode session automations kept firing through the
freeze. Both paused now; recipes below are the verbatim restoration path.

## 1. Flash-lane burn dispatcher - automation-160c358a-a801-4a5e-a76d-42c612adb24f

- Schedule: */10 * * * * (every 10 minutes). runCount 1781. Status: was ENABLED, firing no-ops.
- Why zombie: its own step 1 says "If local time is 12:00 or later on 2026-09-27: write CLOSE
  file and reply 'burn window closed, receipt filed'. Do not dispatch." That date passed 12
  days ago; every fire since is a no-op session (reads QUEUE.md + STATE, replies one line).
  ~144 sessions/day of pure exhaust, through the AV fight and the disk storm.
- Disposition: DELETE FAILED from this seat ("not found in the current workspace" - it is
  owned by another session). STILL FIRING every 10 min as a no-op as of 2026-10-09 ~01:30Z.
  Kill path: the operator's Automations page, or the owning session window. Risk class:
  exhaust-only (each fire reads 3 files and replies one line; ~144 tiny sessions/day).

## 2. 24x7 free burn churn - automation-87ef6bc0-ca6c-4190-a539-be96e1243e91

- Schedule: 0 * * * * (hourly). runCount 308. Status: was ENABLED, last fired 2026-10-08 ~23:20Z (through the freeze).
- Why paused: each fire dispatches 3 background agents at "target 1M+ tokens" of reading -
  this is a primary engine of the exact exec-log exhaust the storm audit is auditing, and
  it kept running during the freeze the operator ordered ("shut everything down and
  reboot"; churn disabled for the AV fight). Pausing aligns with the newer, more specific
  operator order; the standing "burn the free lanes 24/7" order (2026-10-05) resumes the
  moment the operator says GO after the retention law lands.
- Disposition: DELETED 2026-10-09 (this window). Restore verbatim from this session's
  CronList output; re-enable only on operator GO post-retention.

## Left armed deliberately (dailies, per the close doc)

Hermes intel 09:15, OLM mine 10:00, free-resource scout 09:00, wave tide 06:15,
drift patrol 08:00 - all daily cadence, all the "dailies left armed" class.

## The honest finding class

This is the second time a shutdown order reached schtasks but not ZCode-side
automations (the first: the AV-fight reboot sequence). The freeze surface has
two registries; any future "shut everything down" must sweep BOTH. Candidate
law for the wave-2 law pack: a freeze/patrol row that enumerates CronList +
schtasks together.
