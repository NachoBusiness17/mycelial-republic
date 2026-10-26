---
name: next-window-handoff-spec-missing
description: RESOLVED 2026-09-15 — the fossil is fixed; memories/session/
  next-window-handoff.md now EXISTS (procedure + STATE section, update STATE
  only); warm windows follow it directly
metadata:
  node_type: memory
  type: reference
  originSessionId: sess_727c2fc5-be79-4f45-a7a4-229c471b2b9b
---

AGENTS.md's Clippy block tells every new window to "execute the frozen spec: `/memories/session/next-window-handoff.md`" — that file was a fossil (didn't exist) until 2026-09-15, when it was **written** as the real spec: a 5-step Procedure (load framework → warm briefs/CURRENT/context-pack → check inbox index events tail → one job → FILE before close), the Standing Laws (venv python, T0/T1 local, residual-on-disk, "launch N wide" = seed N lane tasks, journal transcription protocol), and a **STATE section** holding current facts (Discord bot live, checkpoint hashes, fifty-wide board, Sep-20 proof gate).

**How to apply:** new windows can now execute the spec directly. The maintenance rule is written into the file itself: **update the STATE section only, never the procedure.** When anything load-bearing changes (gate cleared, bot rotated, new checkpoint), edit that section so the next window starts warm. The warming recipe it encodes (briefs → CURRENT.md → context-pack → queue/todo.md) is what this session actually used and verified on 2026-09-15.
