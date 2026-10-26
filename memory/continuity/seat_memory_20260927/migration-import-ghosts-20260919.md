---
name: migration-import-ghosts-20260919
description: The 51 "code archaeologist" chats flooding the new ZCode desktop
  are Sep-3 claude-code imports replayed at first boot, NOT a live spawner
metadata:
  node_type: memory
  type: project
  originSessionId: sess_833dd189-7e2d-4705-b3dd-059d5e40c78d
---

2026-09-19 migration audit: the ZCode desktop first-boot (08:42) imported 65
claude-import-*.json files from `.claude/projects/` into
`C:\Users\foste\.zcode\v2\sessions\8af8c49a6c1b\`; 51 were the old Sep-3
Claude-Code churn sessions ("You are a code archaeologist...") and two were old
lane probes ("Reply with exactly CLAUDE-ZAI-PONG", "LANE_OK"). The UI stamps
imports as created today, so it looked like a runaway session spawner. Verified
in db.sqlite: zero archaeologist sessions created since 09-03.

**Why:** two agents burned ~1.4M tokens hunting a spawner that did not exist;
the "fresh timestamps" were an import artifact.

**How to apply:** on any "mass-spawned chats" alarm after a client migration,
check the migrator's import dir and the session DB creation times BEFORE hunting
processes. Originals live in `.claude/projects/`; imported copies are safe to
delete in the UI. See [[openclaw-retired-20260919]] and
[[cron-session-bloat-zod-death]].
