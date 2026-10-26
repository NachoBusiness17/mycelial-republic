---
name: webhook-swap
description: "Optional. Use in Roster Swap Phase 8 when a local watcher posts to a bot webhook."
---

# Webhook swap (Phase 8, optional)
- No local watcher or webhook: mark Phase 8 N/A with the reason, and move on.
- New bot creates a webhook routine. The URL and key stay in the routine panel.
- Never print, paste, log or echo the URL or key. The user copies them into the watcher config, or confirms a local agent already holds them.
- With a file bus: post a signed job (see signed-bus-job). Swap the URL and key, reload the watcher, one test post. Each PC step needs the user's YES.
- Check: the test post wakes the new bot. Until then, warn that local returns won't reach it.
- Recovery: if the test fails, after the user's YES put the old URL and key back in the watcher (a PC step; the old bot is still live until Phase 9), then retry.
Stop: show the result, "Reply YES to continue."
