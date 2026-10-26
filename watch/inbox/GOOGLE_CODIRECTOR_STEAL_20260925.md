# GOOGLE CODIRECTOR STEAL — 2026-09-25

**Drop:** @GoogleResearch 2103208899650437286 (2026-09-24) → research.google/blog/coherent-long-form-video-generation
**Authors:** Yale Song, Yiwen Song (Google). Suite: AI video co-director + CANVAS + A²RD + VQQA.
**Papers:** arxiv.org/abs/2604.24842 (COLM 2026) · 2604.13452 (EMNLP 2026) · 2605.06924 · 2603.12310
**Verdict:** LIVE STEAL. This is the fleet loop (brief → pack → lanes → judge → receipt) built by Google for video, with the one piece we lack formalized: a **factored reward** fed back to the chooser.

## Their architecture (one paragraph)

An orchestrator runs a multi-armed bandit over a factored creative configuration (creative strategy / narrative mode / aesthetic archetype) and injects the sampled config into sub-agent system prompts. A pre-production agent builds a storyboard; production sub-agents (keyframe, video, audio) execute it; an MLLM judge grades the compiled cut and returns a **reward factored along the same three dimensions**, so the bandit updates each arm separately over optimization loops. They name the failure mode of linear pipelines — semantic drift, cascading failures, content collapse — as **a credit assignment problem**. Numbers: GenAD-Bench 81.4 peak quality, gains on ViStoryBench/HardContinuityBench/VBench-Long, a demonstrated ten-minute film (A²RD).

## The four steals, landed in fleet canon

1. **Factored reward → the judge lanes.** Our judges currently return scalar ok/fail (41-row rejection taxonomy proved the symptom: 39/41 failures were infrastructure, 2 merit — one scalar cannot tell the chooser which axis broke). Adopt their shape: judge returns per-axis verdicts aligned to the dimensions the governor actually controls (brief fidelity / build quality / receipt completeness), and the lane/tier chooser updates per axis. Content collapse in our build lanes is the same credit assignment problem they named.

2. **VQQA Global Selection → the drift instrument, vendor-confirmed.** VQQA scores every refined candidate against the **original prompt**, never against the previous candidate — that is exactly `tools/drift.py` corr(ΔM,ΔR) and the metric-referent law, applied to prompts. New operating rule for `roblox/prompts/` and any iterated prompt: an amendment may only be accepted if it still scores against the original ask. Amendment chains that drift are rejected even when each step "improved" on the last.

3. **CANVAS → Librarian / context-pack bonds.** Their persistent memory stores structured entity state (characters, locations, objects) and retrieves **visual anchors** per shot to hold identity across segments. Fleet equivalent: structured entity rows + anchors retrieved into the pack per window, instead of prose summaries. Bonds are already the right shape; the steal is per-segment anchor retrieval, not whole-context recall.

4. **A²RD loop → next-window handoff.** Autoregressive segment generation with a retrieve-synthesize-refine-update loop that adaptively switches between **extrapolation** (advance the plot) and **interpolation** (anchor to existing entities). `memories/session/next-window-handoff.md` already does this implicitly; make it explicit: each window opens by deciding extrapolate-vs-interpolate against the receipts.

## Constitution note

Their MLLM judge grades output, holds no authority over the production agents' identity or behavior — consistent with amendment A3 (second model never judges). Judge stays a meter, not a government. The bandit, like our effect broker, is the only thing its reward can move.

## Pre-registered falsifier

Wire factored three-axis verdicts into the build lane for the next 50-wide burn. **Falsifier:** factored rewards reduce repeat infra-class failures vs the scalar-verdict baseline (39/41 pattern). If infra-class repeat rate does not drop, the steal is vacuous for us and gets filed as such.

## Filed

- LINKS-326 in `memory/corpus/LINKS.jsonl`
- This file is the landing. No promotion claimed; intake only.
