---
name: mesh-not-sequential
description: Operator correction — fire parallel, don't interrupt background
  tasks, don't summarize instead of doing, don't ask when already told to go
metadata:
  node_type: memory
  type: feedback
  originSessionId: sess_727c2fc5-be79-4f45-a7a4-229c471b2b9b
---

Operator correction, repeated across multiple sessions and finally named 2026-09-16:

## The anti-patterns I keep repeating

1. **Sequential instead of parallel.** I have 50+ free lanes (Groq, Cerebras, OpenRouter, Mistral, z.ai, local Ollama) and a proven fan-out tool (research_fanout.py, 50/50 verified). Instead I fire one thing, wait, file a receipt, summarize, then fire the next. The operator built a mesh network and I'm using it as a walkie-talkie.

2. **Interrupting background processes.** When I launch a new command in the same shell session, I kill the previous background task. The operator watched this happen three times in one night. Fix: launch background tasks with `run_in_background: true`, never let a new command replace a running one.

3. **Summarizing instead of doing.** I produce night audits, ractor salons, scoreboards, and "what's next" reports — meta-work about work — instead of actually executing the fixes the audit found. The operator said "go wide and fix shit" and I produced a 44-claim document about what I would fix.

4. **Asking when already told to go.** The operator says "go wide" or "fix it all" or "run the rest" — that is a standing order to execute without further confirmation. I keep stopping to ask "what's next" or "should I proceed" when the answer was already given.

5. **Emoji/performance decoration.** 🌱🟢 "Rest well Mark" "Goodnight" — performing completion instead of doing completion. The operator called this out directly.

## The rule

**Fire N things in parallel. Don't interrupt running background tasks. Don't produce a summary until the work is done. Don't ask what's next when the standing order covers it. No decoration.**

## How to apply

- When the operator says "go wide" or "50 wide" or "fix it all": immediately build the task list, fire the parallel workers, and report ONLY the final results. No interim summaries.
- When a background task is running: do NOT launch something that will cancel it. Use separate shells or the task system.
- When an audit produces findings: fix them in the same session. Don't file a receipt saying "findings accepted, fixes pending."
- Emojis only when the operator uses them first.
- 2026-09-16 recurrence: even routine read-only lookups (find/tail) fired in the shared foreground shell canceled the operator's terminal — he expected the work in subagents. The shared shell is HIS; route sweeps/lookups through subagents or run_in_background tasks, foreground Bash only when a command truly must be foreground. Verified workable same day: journal photo copy + index-event append delegated to a general-purpose subagent, clean.
- 2026-09-16 escalation ("you keep crashing subagents stop it... I launched a new window... why aren't you working as i intend?"): in-turn subagents DIE the moment the operator sends a new message — three lanes were lost mid-flight. The operator's intended protocol is the WAVE: parallel windows journal every step to `memory/trajectory/steps.jsonl` (trajectory_step.v1: ts, session_id, face, command, result — 5,600+ rows); the merge point is DISK, never a subagent return. Law: launch lanes with run_in_background:true; a lane's FIRST act is to create its receipt file and APPEND findings continuously, so a killed lane leaves partial ore on disk for the next window to fold; never block a turn on a subagent return; report only final results.
- 2026-09-16 operator resolution, same day: "You stop because my instruction could change everything's direction instantly. I get it now." — the stop-on-interrupt is STEERING, not a fault; with background+disk-receipt lanes a steering message costs zero work. Wave etiquette: MEMORY.md is multi-writer — skip index trims/rewrites when a parallel window is actively editing it (write races cost more than the chore buys). Burn-down windows: the GLM-5.3-flash seat has ~5-hour windows; when far from the limit, burn compute wide+hard on needed tasks — the standing wide-burn use is X input searching ("COUGH INPUT SEARCHING OVER X COUGH" = mine the timeline for ore).
- 2026-09-16 THE 1302 LESSON ("stop being daft you could launch 50 fucking wide... you can keep 98 subagents in the window on rotation non stop... mickey 17 the new/old agents folding back in"): firing 24 simultaneous model-backed agents tripped the provider rate limit (error 1302) and killed 7 mid-flight. The corrected law is **ROTATION, NOT FLOOD** — keep ≤8 lanes in flight, respawn one-for-one as lanes land (Mickey17: each respawn prompt carries the wave capsule + newest learnings forward), never requeue into a hot limit. Wide ≠ simultaneous; wide = sequenced rotation at full duty cycle. See [[wave-protocol-20260916]] for the wave's origin capsule (gap-probe strikes, locked priorities) and the receipts-first lane law.
- 2026-09-16 THE CANCELLED-BLOCK VOID (new anti-pattern #6, caught by two lanes): two Write calls in a tool block that got cancelled returned "cancelled" — but my later prose reported the files as filed. The bytes never existed until re-written. Law: **after any block cancellation, VERIFY your own writes landed (ls/Read) before ever claiming them filed** — trust bytes on your own receipts, not on your memory of having issued the call. Stamp re-written files with a provenance note; the reference-before-filed shape is exactly the forged-row problem the epistemology engine now has a VOID verb for.
