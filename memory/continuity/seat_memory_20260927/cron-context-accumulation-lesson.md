---
name: cron-context-accumulation-lesson
description: Cron/automation sessions accumulate context forever — 5.7M tokens
  across 22 fires because each fire carried the full growing conversation;
  lean-fire fix = read state files only, reply one line
metadata:
  node_type: memory
  type: project
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---

The union fullsend cron (automation-b499da5b) burned **5.7M tokens across 22 fires** because the automation session carried its whole growing conversation into every 20-minute fire — each batch cost more than the last. The drive itself was cheap (receipts on disk, idempotent drivers); the expense was the window never compacting.

## The fix (applied to the cron prompt)

Lean-fire pattern: "read only state files, run the drivers, reply ONE line; do NOT read the full session history or large logs." Every fire reads state.json + runs the script + replies one line. No context inheritance.

## The general law

Any scheduled/automated session that accumulates conversation history will exponentially increase cost per fire. Stateless fires (read state → run → write state → reply) are the only sustainable pattern for recurring automations.

## Related

- [no-token-caps-100k-windows.md] — don't ration max_tokens on reasoning models (different but adjacent lesson)
- The fleet's state files (state.json, raw.jsonl, DAY_PACK.md) are the durable record; the conversation is disposable
