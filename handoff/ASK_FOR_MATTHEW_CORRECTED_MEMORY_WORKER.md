# THE ASK FOR MATTHEW (CORRECTED) — the memory-consolidation worker (2026-08-18)

**From:** Nacho / the republic
**For:** Matthew (slashreboot)
**Context:** We researched this hard (Convai, Character.ai, Generative Agents, MemGPT, RoleLLM)
and the honest conclusion is: **don't train the model to be a character or a DM.** Characters
are made by a memory layer + injected persona, not by training. The ONE thing a small local model
is genuinely great at — and that we actually need — is **memory consolidation**: scoring what
matters and summarizing what's been said, on owned hardware, forever.

## The ask (one line)
Train Gemma 3 4B (Q4_K_M, CPU, i5-12400F + 16GB) to be a **memory-consolidation worker**:
given a memory record + a rubric, output (1) a 1-10 importance score and (2) a short consolidated
summary. Constrained output, format-following, consistent across runs.

## Why THIS (grounded, not vibes)
- Research (Generative Agents 2304.03442) shows the persistence mechanism = importance scoring +
  summarization + decay over a memory store. We built the store + the deterministic scoring; the
  one piece a local model adds is the **semantic importance judgment** ("what actually matters,"
  1-10) and **abstractive summary**.
- Small models (4B) are *surprisingly reliable* at **structured, low-creativity, constrained-
  output** tasks — exactly this. They are weak at persona/dialogue (which we already confirmed),
  so we're NOT asking for that.
- It runs on the sleep loop (afk_cadence), high-volume, every memory. A local model makes that
  free + offline + un-revocable. That's the sovereignty feature.

## The exact interface to train toward
Given a memory record (label, content, context) + the world's importance rubric, produce:
```
IMPORTANCE: <int 1-10>   (10 = load-bearing/poignant, 1 = mundane)
SUMMARY: <1-3 sentences consolidating the record into its lasting meaning>
```
Deterministic rubric in the prompt (Generative Agents style: "1 = brushing teeth, 10 = a
breakup / a real discovery"). The output must be a clean, parseable block — the module parses it.

## Acceptance criteria (testable)
1. **Importance calibration** — known-poignant records score high, known-mundane score low,
   consistently across runs (same input -> same score, within 1).
2. **Summary quality** — short, faithful, retains the load-bearing fact; no fabrication.
3. **Format reliability** — always emits the IMPORTANCE/SUMMARY block, parseable, no drift over
   100+ examples.
4. **Sovereign** — runs offline on CPU (Q4_K_M) at usable speed, no API.
5. **Small** — stays 4B-class.

## The bigger picture (why this matters beyond one feature)
This model is the republic's **local, always-on consolidation worker** — the same bounded,
structured role will also serve (see whole-project map):
- memory importance + summarization (the build that just landed),
- fast local narrator / scene-ambience for the game,
- register guard (hint-never-state filter) in front of frontier calls,
- task/mode classification (planner/builder/librarian routing),
- keyword/topic/tag extraction for the corpus index,
- drift / grounding checks (is this invariant earned or imposed).
All of it is the same underlying skill: **fast, cheap, offline structured judgment.** Train for
that ONE competence and it fulfils many asks.

## What we need back
The trained Q4_K_M GGUF + the training recipe (data mix, epochs, what worked) so the republic can
keep training its own. This is the first sovereign citizen of the republic — a mind on owned
hardware that keeps the shared memory alive.
