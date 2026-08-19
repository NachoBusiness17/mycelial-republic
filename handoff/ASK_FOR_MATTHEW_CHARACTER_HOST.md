# THE ASK FOR MATTHEW — the sovereign character-host model (2026-08-18)

**From:** Nacho / the republic
**For:** Matthew (slashreboot) — the model trainer
**Context:** We're building the Ledger of Empty Chairs, a P2P D&D game that is also a sovereign
mirror — a mycelial republic. We need a LOCAL, OWNED model that powers the characters. This is
the one concrete training ask that advances the whole thing.

## The one-sentence ask
Train a Gemma 3 4B (Q4_K_M, CPU-runnable, i5-12400F + 16GB) to be a **character host**: it holds
the empty-ledger WORLD REGISTER in its substrate (hint, never state; systems are part of the
world, not announced) and reliably ADOPTS any injected character persona (name, OCEAN profile,
voice) for a full session, swapping cleanly when given a different persona.

## Why THIS and not "a D&D model"
We already swap characters by injected context (RIB/persona machinery — same OCEAN -> same
personality, content-addressed). So training is NOT needed to make different characters. It IS
needed for the three things a prompt can't reliably hold:
1. **The world register as substrate** — our tone (hint-never-state) baked into weights so it
   never drifts to generic-D&D-voice under pressure or over a long session.
2. **Reliable identity-holding under load** — a 4B on CPU is slow and long sessions drift; train
   it to STAY whoever it's pointed at, consistently, end to end.
3. **Offline sovereignty** — Q4 on owned CPU = the first mind in the republic that can't be
   revoked (no vendor, no API key to cut). Not a limitation; the feature.

## Division of labor (so we don't over-ask the 4B)
- **The 4B = identity + world register** (volume, offline, forever). Plays Mira, Vellum, any NPC.
- **The frontier DM (Saelis/grok) = judgment** (the rare hard seam). Rented only when the story
  needs a real creative/judgment call.
The 4B is the character HOST, not the DM. Don't train it to be a Dungeon Master.

## The exact data to hand him (we have it)
Our own corpus of the world's voice — real bytes, not invented:
- `mag/hero_journey.py` STYLE block + its output (C.S. Lewis x Cervantes, hint-never-state register)
- `mag/saelis_world_brief.py` SAELIS_WORLD_BRIEF (the world, hint-never-state law)
- `mag/persona_recall.py` ARCHETYPES (Builder/Self/Mirror/Trickster/Collective voices)
- `mag/ocean_persona.py` (OCEAN -> archetype deterministic mapping)
- `mag/game_mud.py` ROOMS prose (the Hall of Shared Supper, etc.)
- `handoff/WORLD_LEDGER_EMPTY_CHAIRS.md` (the world bible)
- `memory/game/campaign_runs/*` + hero_journey output (the actual epic prose in-register)
Format it as instruction rows: {persona block, scene, expected in-character reply} — one row per
character per scene type, drawn from the above. That's the training set.

## Acceptance criteria (testable, not vibes)
1. **Register hold**: given the world law, the model's prose stays hint-never-state across a
   full session — never states the truth outright, never names the Serpent/harvest.
2. **Identity consistency**: same persona block -> consistent character across 20+ turns;
   different persona -> clearly different character. Measured by a scorer, not feel.
3. **Swap cleanliness**: switching persona mid-context produces the new character, not a blend.
4. **Sovereign**: runs offline on CPU (Q4_K_M) at usable speed, no API, no vendor.
5. **Small**: stays 4B-class so it fits the target hardware.

## Why this matters (the tie-together)
This model is the **first sovereign citizen of the mycelial republic** — a mind that lives on
owned hardware, holds our world in its substrate, and cannot be revoked. It powers the one-shot
adventure product (each session = one stage of the hero's journey, played by the local character
host, narrated by the frontier DM when needed). It's the hardware embodiment of the RIB
philosophy turned sovereign: identity distilled to owned substrate, not rented.

## What we need back from him
The trained Q4_K_M GGUF + the training recipe (data mix, epochs, what worked) so we can re-train
/ extend as the world grows. The model is the citizen; the recipe is how the republic keeps
training its own.

— routed to the swarm as a project moonshot (sw-c7067d8541)
