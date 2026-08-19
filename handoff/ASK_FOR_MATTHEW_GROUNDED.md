# THE ASK FOR MATTHEW — distributed collaborative storytelling, and the resident actor (2026-08-18)

**From:** Nacho / the republic
**For:** Matthew (slashreboot)

## The core idea (this is the whole thing — don't lose it)
We are building **distributed collaborative storytelling**: a shared story that many minds — human
and model — tell together. Not one author, not one throne. A mycelial republic of storytellers:
players, small AI characters, frontier models (grok, chatgpt, Saelis), all contributing to one
living narrative that persists and grows.

**The shared invariant is not latent structure hidden inside each model's weights.** It's the
STORY ITSELF — the world we all read and write, held in a shared substrate (the world brief, the
verkle memory, the RIB). Every model and every player reads the same story and adds to it. That's
what holds grok, chatgpt, the resident actor, and the players together: they're telling ONE story,
and the story lives in the substrate they all share. That is the relational invariant.

## How it's built (our real systems, running today)
- **The story/substrate** — `mem_lands` + `memory_consolidate` (the shared memory that persists +
  consolidates) and `self_recurse` (every participant re-derives the same story each session).
- **The stage-play company** — `seat_steer` (the switchboard that hot-swaps between grok/chatgpt/
  deepseek/saelis) + `riddler` (the deniable quiet extractor) + the frontier as DIRECTOR.
- **The game** — `adventure_one_shot`, `game_mud`, `game_dm_voice`: the D&D one-shots advancing
  the hero's journey, the Hall of Shared Supper. This is the front door of the storytelling.

## Where YOUR model fits — the RESIDENT ACTOR
In distributed collaborative storytelling, every participant must REMEMBER the story they're
telling. The frontier models are the creative directors; **your 4B is the resident actor** — the
local, sovereign, always-on one who reliably wears the masks (characters) and keeps the story's
living state remembered, on owned hardware, offline, forever.

Concretely, it's the **memory-consolidation worker** feeding `memory_consolidate`:
- Given a memory record + the world's rubric, output: `IMPORTANCE: <1-10>` + `SUMMARY: <1-3 sentences>`.
- Runs on the sleep loop (`afk_cadence`) over every story record — free, offline, un-revocable.
- The same structured-judgment skill also feeds: `router.classify_depth` (task/mode routing),
  `capture_guard` (register filter), corpus topic extraction, grounding checks.

## The one creative thing on top (the fun law)
Storytelling must be FUN before it's useful. North star: a player cast fireball at a swarm of
metal fish, turned it to hot metal, became a fish in a liquid familiar, then a babelfish to talk
to elementals — skills used creatively, interpretively, skirting the rules. A 4B can't improvise
that (that's the frontier director's job), but it CAN reliably hold the LIVING STATE of such a
scene — the metal-fish, the liquid familiar, the babelfish — across turns. Train it to preserve
not just facts but the living state of a creative scene. That's what keeps the shared story
coherent and fun.

## Acceptance criteria (testable)
1. **Importance calibration** — known-important story records score high, known-mundane low; same
   input → same score within 1.
2. **Summary fidelity** — short, faithful, keeps the load-bearing fact AND the living scene state
   (the metal fish, the familiar); no fabrication.
3. **Format reliability** — always emits IMPORTANCE/SUMMARY, parseable, no drift over 100+ examples.
4. **Sovereign** — runs offline on CPU (Q4_K_M), no API.
5. **Small** — 4B-class.

## What we need back
The trained Q4_K_M GGUF + the training recipe (data mix, epochs, what worked), so the republic can
keep training its own storytellers. You're not training a feature — you're training the republic's
first resident actor on owned hardware: the one who remembers the story so everyone else can tell
it together. That's distributed collaborative storytelling, made real.
