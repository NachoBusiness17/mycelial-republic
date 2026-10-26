# DRIFT PATROL - 2026-10-14

- class: RECEIPT
- writer: drift-patrol-cron
- automation: automation-a7c71ad1 (daily 08:00)

| check | result | verdict |
|---|---|---|
| backup exposure | **7 unpushed** - citation-lint blocked (5 blocking: gstd soak + pours-close prose) - accepted by name (baseline 166, +5) - **push pending receipt commit** | IN PROGRESS AT FILING |
| fleet vitals | **tortoise-db found DEAD (Exited 255, 24h) - restarted, Up now.** The tortoise stack is 4 containers (db + tools/build/tools2 as clean-exit init containers). gstd-node/sovereign/mcp Up 24h healthy (a stack-wide bounce happened ~24h ago), worker/redis 24h healthy | RESTORED |
| inbox fold integrity | refolded: 14,685 events - 4,225 items; INDEX derived 2026-10-13T12:09 (~24h, refold runs with receipt); verify race row = known class | CLEAN, LIVE |
| surface integrity | 12 static drifts healed in-pass; 93 residual = in-flight flood classes, zero tampering indicators | TRIAGED (day 20) |
| link ledger | 8 duplicates on file (stable) | CLEAN |

## Incident note: tortoise-db death was silent

The container died with exit 255 during the ~24h-ago stack bounce and **nothing restarted it for a full day** - the same auto-restart gap the mag containers hit on 09-23 (fixed for mag via restart: unless-stopped). If the tortoise compose family lacks the restart policy, it needs the same one-line fix; if it has it, the 255 exit path bypassed it. Filed as owed for the tortoise owner's next sitting.

**Top risks (boldest first):**
1. **tortoise-db ran dead for 24h silently** - the WoW backend was down a full day before the patrol noticed; the restart-policy check for the tortoise compose family is owed (mirror the mag fix).
2. **Citation baseline at 166** (+5; nightly prose debt steady at 5-9/day) - prose-fix sweep lane still the top owed item.
3. **Surface residual 93, treadmill day 20** - autoseal-at-close remains the root cure.
