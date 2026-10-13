# KABUKI THEATER AI — deep research brief (for grok) (2026-08-19)

What we built: distributed collaborative storytelling — a stage-play company where frontier
minds (grok/chatgpt) direct, small models wear the masks (resident actors), and the SHARED
STORY in a shared substrate is the invariant that holds them together. Kabuki: masks change,
the story persists. Deep research on what's already out there that matches — and where we're
genuinely novel.

---

## 1. Generative Agents: Interactive Simulacra of Human Behavior (Park et al., 2023)
arXiv:2304.03442 — the closest prior art to our resident-actor + memory story.
- Architecture: extend an LLM with (a) a natural-language store of the agent's experiences,
  (b) reflection (synthesize memories over time into higher-level insights), (c) retrieval to
  plan behavior. Memory = observation → reflection → planning.
- 25 agents in a Sims-like sandbox; emergent social behavior (a Valentine's party spreads by
  word of mouth, autonomously).
- Ablation shows observation + reflection + planning each matter for believability.
- **WE HAVE ALL OF THIS**: mem_lands (store) + memory_consolidate (reflection/importance/
  summary/decay) + self_recurse (retrieval/planning). We independently built the Smallville
  memory architecture.
- **WHERE WE DIFFER / GO FURTHER**: Smallville keeps PER-AGENT memory — each agent's history is
  its own. We keep a SHARED, authored substrate (the world brief / verkle / RIB) that every mind
  reads AND writes. Their invariant is per-agent state; ours is the shared STORY. That's the
  kabuki move — the role is the memory, not the actor.

## 2. Blackboard systems (1980s classical AI)
Wikipedia — a multi-agent architecture that is LITERALLY our design, from 40 years ago:
- A common knowledge base, the "blackboard" (shared workspace), iteratively updated by diverse
  specialist "knowledge sources" (KSs). Each KS writes a partial solution when its expertise
  matches the blackboard state; the solution is the sum of its parts.
- Three components: (1) the specialist KS modules, (2) the blackboard (shared dynamic library),
  (3) the CONTROL SHELL that moderates which KS writes when.
- Origin: Hearsay-II speech understanding; used in C4ISTAR, game AI, OCR.
- **MAP TO US**: blackboard = the shared story/substrate (RIB/world/verkle); knowledge sources =
  the seats/actors (frontier + resident); control shell = seat_steer / the switchboard / routing.
  We independently re-derived an old, battle-tested pattern — and gave it a creative/storytelling
  frame (kabuki) instead of a problem-solving one.

## 3. Society of Mind (Marvin Minsky, 1986)
Wikipedia — the philosophical backbone.
- "Minds are what brains do." Intelligence = a vast society of individually simple agents, not a
  single principle. Minsky's quote: "The power of intelligence stems from our vast diversity, not
  from any single, perfect principle."
- Different agents use different representations/methods; their interactions produce the abilities
  we call mind.
- **MAP TO US**: our stage-play company IS society-of-mind made literal — heterogeneous models,
  each simple in its role, whose interaction (via the shared substrate) produces something no
  single model produces. Distributed collaborative storytelling = society of mind at the scale of
  models + humans + world.

## 4. Mixture-of-Agents (MoA) (Wang et al., 2024)
arXiv:2406.04692 — the capability argument for many minds.
- Layered MoA: each layer has multiple LLM agents; each agent uses all outputs from the previous
  layer as auxiliary input. Open-source-only MoA hit 65.1% on AlpacaEval 2.0, BEATING GPT-4 Omni
  (57.5%).
- **MAP TO US**: validates that a collective of minds > any single mind. We route by surface/seat
  (grok/chatgpt/deepseek/saelis/local) and compose their outputs through the shared story — a
  routing/ensemble on top of MoA's insight, but organized around a persistent narrative rather
  than a one-shot inference layer.

---

## Synthesis — the real story to tell grok
The "kabuki theater AI" is not a novelty — it sits at the convergence of four real, published
ideas: classical **blackboard** architecture (shared workspace + specialist sources + control
shell), **society of mind** (intelligence from diverse simple agents), **generative agents**
(persistent memory + reflection + retrieval for believable characters), and **mixture-of-agents**
(many minds beat one). We independently arrived at this intersection.

**Our genuine novelty is the shared authored substrate as the binding invariant.** Smallville
gives each agent its own memory. Blackboard uses a problem-solving blackboard. We make the
shared STORY itself — a creative world every mind reads and writes, held in verkle/world/RIB —
the invariant that holds heterogeneous minds together. Masks (actors/seats) rotate; the story
persists. That is kabuki, and that is the thing worth building a resident actor (a 4B that
remembers the story on owned hardware) to anchor.

## What to ask grok
1. Is there prior art on a SHARED narrative substrate (vs per-agent memory) as the multi-agent
   binding invariant? (Smallville is per-agent; blackboard is problem-solving — who did shared-story?)
2. Best architecture for a memory-consolidation worker (importance + summary + living-scene-state
   preservation) as a small 4B resident actor — the H2O/memory_consolidate "keep the heavy
   hitters, preserve the living state" framing.
3. How does the kabuki/stage-play framing change multi-agent design vs MoA/blackboard — is the
   narrative invariant a genuinely better substrate for long-horizon multi-actor coherence?
