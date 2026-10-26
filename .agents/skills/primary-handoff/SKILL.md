---
name: primary-handoff
description: "Use in Roster Swap Phase 7 to move the primary-bot role to a fresh copy."
---

# Primary handoff (Phase 7)
1. Find out which bot is primary (ask the user, or check the setting). If it's unclear, stop and ask. If the primary isn't in scope, mark Phase 7 N/A.
2. Old primary writes HANDOFF-<date>.md: Done today / Routines to recreate (ON only, per bot) / Its own routines (schedule, prompt location, next run) / Webhooks (location only, never values) / Next task / Open items / Archive path.
3. New primary reads it and, after the user's YES (approved in the new primary's chat), recreates its own routines (time-sensitive ones first), then asks the user to set it as primary.
4. Check: the new primary answers as primary and its routines are confirmed. Stop: "Reply YES to continue."
5. Old primary answers follow-up questions until deleted.
Rollback: the user sets the old primary back, and after the user's YES the new copy's routines are paused.
