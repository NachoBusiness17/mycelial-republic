---
name: roster-inventory-and-routine-census
description: "Use in Roster Swap Phase 1 to list bots and collect each bot's routine status."
---

# Inventory and routine census (Phase 1)
- List each bot in scope: name, id, primary yes/no, group rooms it's in.
- Message each bot (after YES): "List each routine as name | cron | ON/PAUSED | trigger | prompt verbatim. If you have none, reply none. If you can't see the prompt, write [UNKNOWN] and summarize it."
- Save replies verbatim to ROUTINE-STATUS.md with a time stamp and zone. "none" is a valid answer.
- PAUSED = do not recreate.
- No reply within one working session: chase once. Still nothing: ask the user, and mark the bot [UNKNOWN] (it can't pass Phase 6 until resolved).
- Never copy secrets, webhook URLs or keys into the file. Write [REDACTED - lives in <place>].
Check: every bot has a reply, "none", or a user answer. Stop: show the table, "Reply YES to continue."
Recovery: missing or unclear rows go back to that bot or the user. Never invent.
