---
name: roster-swap-automation
description: "Optional. Use when the owner turns on Roster Swap Auto mode (phases 0-3 back to back) or the monthly read-only bloat check."
---

# Roster Swap automation (optional, both off by default)

## Auto mode
- Off unless the owner says YES to it in getting-started (or later). Default is NO.
- Turning it on is one YES that covers phases 0-3 only (preflight, inventory, archive, verify) for the bots in scope, including the read-only routine-census questions to those bots. Nothing else is sent.
- Auto mode runs in Roster Swap's own chat. It needs bot messaging and transcript reading, so don't hand phases 1-3 to a helper that lacks them.
- Census wait: give each bot up to 15 minutes to reply, chase once, then wait 15 more. Only then mark it [UNKNOWN] and stop.
- Run phases 0-3 back to back with no stop between them. Every phase still runs its own check and updates PROGRESS.md.
- A date range marked [UNKNOWN] because rows have no timestamps is a noted gap, not a stop. Show it in the summary.
- Any FAIL, any other [UNKNOWN], or a BLOCKED bot: stop right away, say what failed and for which bot, and offer the recovery. Don't continue to the next phase.
- When phase 3 passes for every bot in scope, show one summary table (per bot: inventory, routines found, archive folder, verify result, redaction status) and PROGRESS.md, then stop: "Reply YES to continue to Phase 4."
- Phases 4 and later keep their per-step YES. Auto mode never copies, renames, deletes, sends messages outside the census, or changes routines.
- The owner can turn it off at any time; the run then falls back to a stop after every phase.

## Monthly bloat check (optional routine)
- Off unless the owner says YES in getting-started. Create it only after that YES, approved in this bot's own chat.
- Schedule: once a month, at a time the owner picks.
- Routine prompt: "Monthly roster bloat check. Read-only. Get the bot list and count from the roster manager (or the user if there is none), and history length and last activity from each bot's transcript reader. Look at the bot count, bots with very long histories, bots with no recent activity, and routines that are paused or look stale. Show one short table and say whether a roster swap looks worth it and for which bots. Change nothing: no copies, renames, deletes, sends or routine changes. If something can't be checked, mark it [UNKNOWN]. If nothing stands out, say so in one line."
- Never include secrets, webhook URLs or personal data in the report.
- Turning it off: after the owner's YES, pause or delete the routine.
Check: the owner's choice for each option is recorded in PROGRESS.md.
