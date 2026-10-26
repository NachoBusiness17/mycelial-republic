---
name: flash-burn-width24-findings-20260927
description: 9/26-27 flash-lane burn width-24 experiment results — 407 briefs,
  400 landed, ~1.1B witnessed tokens, envelope ceiling is a function of window
  depth not a constant, 1302s surface when the window runs deep
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Flash-lane burn width-24 experiment completed 9/26-27. The envelope law is a
FUNCTION of window depth, not a constant. Key numbers: 816M witnessed agent
tokens across 191 agents, ~140 lanes landed of 167 dispensed, free-lane runner
added 2.6M through 8 alive lanes, measured peak 109M tok/h at width 10, and
the 97.3 pct cache hit rate is the cost engine.

**Width-24 experiment verdict:** clean at fresh-window (B2-25 confirmed 109M
tok/h zero surfaced 1302s), but surfaces the wall when the window runs deep
(eight surfaced 1302 deaths clustered 17:00-19:00Z). B2-98's tally caught 287
absorbed 1302s invisible to surfaced counts during "clean" waves — zero
surfaced ≠ zero occurred. Provider-error tally tool built.

**Structural findings:**
- Fold silently dropped watch/ paths (OUTSIDE_RE); 235 registers poisoned,
  all re-registered in 8 named batches
- Test census 1,341 was hand-copied from birth, never byte-backed; real count
  1,837 collected / 301 files
- 3 fabricated research answers caught and quarantined (UF-124/125/126)
- Q-drop #874 "gap" dissolved (misidentification, real number is #1104)
- Cerebras parked: never worked, community kill-pattern confirmed ($5 gone
  in 10 min to 3 days, no cache discount)
- Free-lane denominators: groq 1K RPM/200K TPD gpt-oss-120b is the fattest
  free lane; cerebras 402, nvidia 410, gemini 401, mistral zero-quota
- Discovery: window meters reset and refill; a point-in-time pct is not a
  budget; burn rate vs window depth is the real denominator

**Architecture proven:** 12-lane swarm × 25-brief slices + dispatcher refill
every 10 min at width 24 + free-lane runner = ~1.1B witnessed tokens in ~17h.
The 10-min refill cadence matters more than width (each gap cost real hours).

Related: [[width24-experiment-verdict-20260926]],
[[flash-burn-structural-findings-20260927]], [[envelope-probe-dispatch-law]],
[[cerebras-parked-20260926]].
