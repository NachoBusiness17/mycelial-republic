---
name: zcode-shadow-steal-20260918
description: zcode correspondence+trajectory stolen local-only — operator voice
  does NOT survive in .zcode/cli (attrition measured); 1,161-task corpus filed;
  export law proposed
metadata:
  node_type: memory
  type: project
  originSessionId: sess_c424b80a-5f44-4511-bcdb-8dcec10fdce9
---

Shadow steal of the zcode store, 2026-09-18, ran LOCAL-ONLY (chat history is
T0/T1 private — nothing to remote lanes).

**Why:** the operator asked for all correspondence + trajectory; the measured
truth is the correspondence's operator half has ~total attrition in
`.zcode/cli` — model-io rollouts strip request messages, so only the
assistant side (3 rollouts), the work's shadow (1,161 subagent task
descriptions across 36 sessions), and exec/telemetry logs survive.

**How to apply:**
- Corpus: `memory/corpus/zcode_history/` (sessions.jsonl, agent_tasks.jsonl,
  correspondence_*); digest + 7-room taxonomy:
  `watch/inbox/ZCODE_SHADOW_STEAL_20260918.md`.
- Task clusters: research 81 / infra 76 / doctrine 75 / salons 86 / games 61 /
  verkle 21 / astra 20 / x-play 20 / parables 12 / unnamed 709 (61% — the
  fleet's real mass is plumbing too plain to name).
- Attrition fix: propose an export law — every window copies transcripts to
  `watch/inbox/` (the inbox-first rule); `export-log-stage/` sits EMPTY, the
  pipeline was staged and never wired.
- Loading protocol that worked: trajectory milestone row (trajectory_step.v1),
  rib_chat structure-only digest on z_ai3 (FROZEN_RIB prefix cache-mined,
  private text stays in the tail/none), mag.state_snapshot dedups repeat
  captures.
- Task descriptions are the real session memory — when recovering a vanished
  zcode window, read `cli/agents/<sess>/agent_*/metadata.json` descriptions
  FIRST ([[zcode-session-recovery-path]]).
Related: [[corpus-map-salon-20260918]], [[the-librarian-fleet-imprint-20260917]]
