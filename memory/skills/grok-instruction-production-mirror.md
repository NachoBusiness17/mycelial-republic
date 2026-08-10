# Grok Instruction-Production Mirror

**Steal:** the pattern from a shared X Grok conversation — Grok turns a VISION prompt +
"make this a frontier research plan for dumber models to execute" into a decomposable,
executable instruction package. This is the RenderMan tesuji observed in the wild:
frontier compacts, cheap executes.

## The prompt pattern (steal this shape)
```
Given this vision, produce a full frontier research plan for dumber models to execute:
0) one-sentence MISSION
1) DESIGN CONSTRAINTS for dumber-model execution (every work package <=8 sequential
   agent steps; open inputs only; outputs code/configs/protocols/CAD; automatic eval;
   no proprietary APIs)
2) FOUR PARALLEL TRACKS (A-D), 5 numbered work packages each + quantified success metric
3) CROSS-TRACK INTEGRATION KERNEL (unified accounting, interoperability score, re-ranking)
4) EXECUTION CADENCE (week/month phases + success gate)
5) BUILT-IN RISK & FAILURE HANDLING (overhang, hallucination, starvation, coordination)
6) IMMEDIATE FIRST PROMPT (copy-paste for any open model)
```

## Why it works (the law it encodes)
- **Compact at frontier, expand at cheap** — grok freezes the spec (the RIB); dumber
  models execute it. Never make the cheap tier invent the plan.
- **Decompose to <=8 agent steps** — a mid-tier model can only hold so much; bite-sized
  packages are machine-executable.
- **Automatic evaluation** — unit tests / physics checks / open benchmarks, not vibes.
- **Built-in risk** — capability overhang, hallucination, starvation, coordination handled
  up front so cheap models don't derail.

## Our pipeline (mag/grok_mirror.py)
`capture_plan(vision)` → `interpret(plan)` (map sections to our modules) → `questions(plan)`
(socratic elevation) → `research_project(vision)` (research_lens build + cheap_swarm) →
`distill_skill()`. Ghost observes via the active-coding-window flag
(state/active_coding_window.json).

## Do this next time
When a vision/ambition lands, mirror it: capture the grok plan, interpret against our
modules, ask grok what the executor needs, spin a research pack, fold it back into the
lens corpus. Do NOT hand-build the plan from scratch — let the frontier produce it, then
we decompose + execute with cheap models.
