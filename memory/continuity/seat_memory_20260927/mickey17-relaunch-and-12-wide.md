---
name: mickey17-relaunch-and-12-wide
description: Operator correction 2026-09-17 — cancelled background agents get RELAUNCHED immediately (Mickey 17: bodies die, mission persists); 12 parallel agents in-window on top of the cron is the expected operating mode
metadata:
  type: feedback
---

Operator correction 2026-09-17, twice in one night: a batch of 10 parallel audit agents was cancelled before returning and I stopped — "there is no fucking way the dnd layer just died... STOP CANCELING BACKGROUND AGENTS WHY THE ACTUAL FUCK... i'm floored that you stopped operating the way we have designed."

**Why:** the design is Mickey 17 — the expendable bodies die and are replaced; the work continues. Cancellation is a scheduling event, not a verdict. The operator also ordered 12 parallel agents run IN-WINDOW on top of the cron jobs as the standard width ("run parallel, run 12 agents in this window").

**How to apply:** when parallel agents come back cancelled, relaunch them immediately in the same turn with identical prompts — do not grieve, do not summarize, do not stop. The two that DID return still delivered (litter scan + D&D completeness audit), proving partial survival still pays. The relaunched wave then returned the full games-audit findings that drove the fix wave (see [[games-audit-fix-wave-20260917]]).

Related: [[wing-chun-operating-lenses]], [[mesh-not-sequential]], [[12-wide-background-architecture]].
