---
name: routine-carryover
description: "Use in Roster Swap Phase 6 to move only ON routines to the new bot copies."
---

# Routine carryover (Phase 6)
- Source: ROUTINE-STATUS.md. ON only. Keep the same name, schedule and verbatim prompt.
- A bot with "none" is N/A, which counts as PASS.
- Each new bot creates its own routine in its own chat. The user approves it there.
- [UNKNOWN] prompt: ask the old bot before deletion, else the user. Never invent. Until it's answered, that bot is BLOCKED for Phase 9.
- Fix references to retired bots or old paths.
- Mark each one done only after the new bot confirms.
- Avoid double runs: after the user's YES, pause the old bot's routine once the new one is confirmed.
Check: every ON routine is confirmed on its new bot. Stop: show the table, "Reply YES to continue."
Recovery: a failed create is retried in the new bot's chat. Rollback (after the user's YES): delete the new routine and resume the old one.

Optional template, off by default. Offer it only if the user asks to turn it on. Nightly memory cleanup (daily, keep old time):
"Nightly memory hygiene for <BOT>. Only if I have saved facts: back up their text to <backup folder>/<BOT>-<YYYY-MM-DD>.md, merge duplicates into one clean fact each, forget outdated versions. If unsure, keep it and mark it [UNKNOWN]. Touch only my own memory. Tell the user briefly only if something changed. Otherwise stay quiet."
