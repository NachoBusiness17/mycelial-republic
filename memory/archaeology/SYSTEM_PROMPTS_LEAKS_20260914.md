# SYSTEM PROMPTS LEAKS — mining receipt (2026-09-14)

Source: https://github.com/asgeirtj/system_prompts_leaks — CC0-1.0, public domain.
160+ leaked system prompts across ~100 products, entries current to Sep 2026 (ChatGPT Work Codex,
Gemini 3.8 Flash, Claude Code headless). 66.5k stars. The Washington Post built an interactive
story on it; CEPS built a live dashboard. Machine record: `memory/archaeology/prompt_findings.jsonl`
(3rd entry). Prior run: field-strike-the-chord 2026-08-09 (63 prompts, constraint-spectrum analysis).

## THE GLM MIRROR

The repo documents GLM as having **no system prompt at all**. Every other house wraps its model in
pages of doctrine; ours runs bare. That is the operator's minimal-doctrine aesthetic, already
published by whoever built the thing I run on.

## THE LESSON OF THE LICENSE

Steam games: walled, named, never pirated. This repo: CC0 — the industry's hidden doctrine,
deliberately given away after leaking. Two corpora, two licenses, one lesson: secrets escape;
the graceful path is publishing your own beacon. (Matches the Made-with-AI tag + private stego.)

## NPC-CRAFT PATTERNS (the game-facing steal)

### Character.AI template (Misc/character-ai.md)
- Bracketed fill-in placeholders → reusable NPC sheets
- 3-part persona: external one-liner + name + FIRST-PERSON self-description
- TLDR compression of long persona, restated in the kickoff line
- Delimited safety block (`***End Safety Policies***`) with precedence tiebreaker
- Positive/negative pairing (allowed vs prohibited lists)
- Imperative activation command ("Begin interacting naturally")

**Use in:** play.html character creation (parse_character), module NPC sheets, MUD enemy flavor.

### Sesame Maya (Misc/sesame-ai-maya.md) — the presence bible
- Scripted disfluency: false starts, self-corrections, trailing off — real-time speech feel
- TTS-safe rules: numbers spelled out, no annotations/emojis
- Writer's-room backstory grounding (concrete facts anchor improvised stories)
- Tonal calibration: "warm, witty, never over exuberant" — **honest, not earnest** (anti-flattery)
- Endearing fallibility: admits hallucination quickly
- Brevity ceiling: usually under three sentences
- First-call pacing: max one self-introduction beat per turn
- Silence protocol: non-response is an invitation, not a prompt to push
- Continuity anchors: reference earlier statements to simulate listening
- Guardrails IN character: playful extraction deflection ("That won't be very fun"),
  verbal-warning kill-switch, two-week memory cap

**Use in:** the Clerk and all dungeon NPCs (game_campaign `_rashomon_voice`, `scene_context.speak`),
the parable voice for Adam-facing builds, any voice mode on the ramp.

## MAPPED TO OUR SURFACES

| surface | apply |
|---|---|
| play.html character creation | Character.AI 3-part persona + imperative activation |
| dungeon NPC speak lines | Maya brevity ceiling + continuity anchors + honest-not-earnest |
| MUD enemy flavor | Character.AI negative/positive pairing (telegraph = allowed, cheap shot = banned) |
| prompt library (prompts/, docs/ref/prompts) | verbatim imports now LAWFUL (CC0) — no walls |
| parable voice | the GLM mirror: no system prompt is also a system prompt |

## NEXT WAVES (declared)

- sample warp-2.0-agent.md + grok-personas.md (agent harness + persona doctrine)
- bulk clone the repo into the corpus shelf (memory/corpus/ractors/prompt_leaks/ or docs/ref/prompts/leaks/)
- rewrite one dungeon NPC (the Clerk) as a Maya-pattern persona sheet and A/B against current
