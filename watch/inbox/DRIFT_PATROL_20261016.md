# DRIFT PATROL - 2026-10-16

- class: RECEIPT
- writer: drift-patrol-cron
- automation: automation-a7c71ad1 (daily 08:00)

| check | result | verdict |
|---|---|---|
| backup exposure | **30 unpushed** - citation-lint blocked (1 blocking, down from 4 - the night prose is converging on lint-clean) - accepted by name (baseline 171, +1) - re-sealed - **push pending receipt commit** | IN PROGRESS AT FILING |
| fleet vitals | six mag-family containers bounced ~11h ago, all healthy; **tortoise-db found DEAD AGAIN (Exited 255, 11h) - restarted. This is the second 255 death on a ~daily cadence.** | RESTARTED - PATTERN ESCALATED |
| inbox fold integrity | refolded: 14,780 events - 4,255 items; INDEX derived 2026-10-15T12:08 (~24h, refold runs with receipt); verify race row = known class | CLEAN, LIVE |
| surface integrity | 7 static drifts healed in-pass; 92 residual = in-flight flood classes, zero tampering indicators | TRIAGED (day 22) |
| link ledger | 8 duplicates on file (stable) | CLEAN |

## ESCALATION: tortoise-db exit-255 death is now a confirmed daily pattern

Second 255 exit in three days (10-13 restart, dead again by 10-14, restarted, dead again by this patrol). The kill correlates with the mag-family stack bounces (~11-24h cadence): every bounce restarts the mag containers (restart: unless-stopped) but tortoise-db has **no restart policy**, so each bounce kills it without reviving it. The cure is one line in the tortoise compose family (`restart: unless-stopped`) plus identifying what fires the daily bounce. Until then this patrol restarts it every morning - which works, but means the WoW backend is dark for up to 24h at a stretch, daily.

## Overnight: light - rib boot regen (handoff rib mounted first), handoff addendum (gate unblocked by relocation, lanes 1-4 landed, **impersonation refused** - the seat refused an impersonation attempt and recorded it), mem_echo header fix (was hardcoded to watch/inbox).

**Top risks (boldest first):**
1. **tortoise-db daily 255 death cycle** - restart policy + bounce-source identification owed NOW; the daily dark window is a data-availability risk for the WoW backend.
2. **Citation baseline at 171** - volume converged (1/night, down from 70) - the writers ARE adopting lint-clean prose; the acceptance valve is winning.
3. **Treadmill day 22, residual 92** - autoseal-at-close (day 24 owed) remains the root cure.
