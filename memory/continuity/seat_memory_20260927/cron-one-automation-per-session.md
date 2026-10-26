---
name: cron-one-automation-per-session
description: ZCode CronCreate limit — a session that already belongs to a scheduled
  task CANNOT create a second one; fold new duties into the existing automation
  via CronUpdate instead (conditional steps make the fold clean)
metadata:
  node_type: memory
  type: reference
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---

2026-09-17: attempting a second CronCreate (a queue-tender alongside the existing every-20-min union fullsend drive) failed with "Cannot create a scheduled task inside a session that already belongs to a scheduled task." CronUpdate on the existing automation works fine.

**How to apply:** when a session already owns an automation and needs an additional scheduled duty, don't spawn a sibling — extend the existing automation's prompt via CronUpdate with a conditional step (e.g., "if remaining < 12, first append items, then run the batch"). Conditionals keep the merged automation cheap on fires where the extra duty doesn't trigger. Keep the title synchronized with the merged behavior. If the duties genuinely need different cadences, the extra automation must be created from a different (non-scheduled) session.
