# STEAL — MCP as skill quantization: complex skills for dumb models (2026-09-04)

**Operator, verbatim:** "the whole point is to dogfood the mcp servers. there is something
here just like cache mining i can feel it. people are using this tech dumbly and we can
exploit it in novel ways… it's the whole kubernetes quantization and giving complex skills
to dumb agents. i literally want to give vision to 7b model."

## THE THESIS (one line)
Cache mining found compute in the prefix; this finds intelligence in the tools: **the MCP
server is the skill, quantized out of the weights.** A dumb model + honest tool outputs ≥
a smart model guessing — when the tool is the right transducer.

## THE THREE CONVERGENT FRAMES (all ours, all receipted)
1. **Quantization frame:** weights are the expensive place to store an ability; tools are
   the cheap, swappable place. MCP = capability factoring — move the skill out of the
   model, pay for it once per call, not per parameter.
2. **Kubernetes frame:** dumb agents + declarative structure. The model DECLARES intent
   (call, args); the server RECONCILES reality (the hard part). Same split as
   desired-state vs. control plane.
3. **Endowment frame (the orphan):** "senses for the blind, GPS for the stateless, hands
   for the tool-less" — the AX law measured it: the vision giant missed by 1,009px; the
   dumb walker reading the tree was exact. Structure beats pixels BECAUSE the structure
   is the skill the model doesn't have to synthesize.

## THE RECEIPTS ALREADY ON THE TABLE
- Eyes receipt (Aug 27): blind fails honestly; endowed passes — the endowment delta is
  measured, end-to-end, receipted.
- DUMB_AGENT_GPS A/B: 17 navigation primitives = GPS as a skill the stateless can call.
- AX-RESOLVE OVER PIXEL-GUESS (today): the strongest single data point — tool structure
  beat native vision at its own game.
- 4.6V-Flash-9B runs in the 68.7GB box (z.ai-org card) — a LOCAL native-vision baseline
  exists for the falsifier.
- AutoGLM (yesterday's steal): the vendor ships the brain but NOT the loop — the harness
  is where the skill lives. We own the harness.

## THE BUILD (launched this turn): VISION FOR A 7B, VIA MCP
Arms (same task set — the daytool/70-step ladder family):
- **A. blind 7B** — text-only, no eye (honest-failure baseline).
- **B. endowed 7B** — local 7B (mag-ollama) + ONE tool: `see(x)` → returns STRUCTURE
  (AX tree for UI, mag/vision description for images — the eye is an MCP-shaped tool,
  the model never sees pixels).
- **C. native vision** — vision-native model direct (4.6V-class or deepseek-vision).
Measure: task accuracy, steps-to-done, tokens, $ per arm. Falsifier: if B ≥ C at ≥10x
less cost, skill quantization is REAL and the whole MCP rack becomes a dumb-model
multiplier. If B ≈ A, the endowment needs smarter structure, not more tools.
Cost: ~$0 (local model + free vision lane).

## THE EXPLOIT LIST (if the falsifier holds)
1. **Dumb-model multipliers:** every lane agent drops to flash/local-tier + its whitelist.
   Judgment stays pooled; skills get served.
2. **Tool-output cache mining** (the literal analog): MCP outputs dedupe/cache across
   agents — the time-series fetch-cache pick attacks the same waste class the prefix
   cache does (92-97% re-feed measured).
3. **Skill lending library:** the manifest whitelists become a lending desk — a lane
   borrows a sense for one task, TTL, returned (three-gate adoption already lawed).
4. **The 7B fleet:** local small models as permanent staff (no per-token cost), skilled
   entirely by the rack. Rocinante runs a guild of 7Bs.

## TRI-STATE
Thesis: **Supported by convergent receipts** (AX, eyes, GPS), **Unproven as the unified
build** until the three-arm falsifier runs. Exploit list: **Unproven** (gated on the
falsifier). Cost claim ~$0: **Supported** (local + free lanes).

*Filed by the manager seat; the build gopher carries the falsifier. The guild teaches
dumb models to see — and charges nothing for the eyes.*
