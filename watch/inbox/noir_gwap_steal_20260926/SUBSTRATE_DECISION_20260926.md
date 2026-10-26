# SUBSTRATE DECISION + NOIR GWAP DESIGN SPEC

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 · **Class:** RECEIPT / decision + spec
**Authority:** operator order "do all of that" (2026-09-26) delegating the substrate pick; box inventory run live this pass (Docker 29.6.2 RUNNING, WSL2 present, GPU = AMD RX 5600 XT 8GB no NVIDIA, Ollama alive, Steam present with 12 titles and NONE of the relevant games installed).

## The decision

**Staged build, session-based first:**

- **Phase 1: Teardown, round-based 6v6 heist prototype.** $30 on Steam (not installed; purchase is the operator's). Fastest time-to-fun: destruction native, official Lua modding, mplib (MIT) game-mode skeleton, server-authoritative scripts. Session-based rounds only: no persistent world (no dedicated servers, host-local persistence, no NPC AI API: player cops in v1, hand-rolled AI cops in v2).
- **Phase 2: FiveM QBCore noir persistent city.** Requires GTA V copies per player + Element Club sub ($15-50/mo) + hosting ($40-80/mo). Commission an ORIGINAL Miami-noir map (never VC ports). This is the persistent-world stage, sanctioned and de-risked by L07.
- **Phase 3: UE5 native (the sovereign Arena).** Per-building pre-fractured Chaos + event replication, Embark-style. Long-run substrate, doubles as the v6-brief experimental arena. Start only after Phase 1 proves the game design.

Rationale in one line: the design hypothesis (does adversarial cop/robber play generate verifiable useful artifacts?) is testable cheapest in Phase 1; Phases 2-3 scale the proven loop.

## The design spec (v1, applies to every phase)

**Roles:** Robber (plans and executes heists, authors private intent record), Cop (patrol, responds, authors incident report), Witness (NPC or player holding hidden info, answers templated clue prompts). Optional third adversarial role per KissKissBan: the Blocker, who briefly bans the obvious answers (see mechanics).

**Core loop (the GWAP payload):**
1. Robber commits a heist; intent record sealed server-side (what/where/how in free text + structured fields).
2. Cop discovers the scene; interviews witnesses (Peekaboom/Verbosity inversion: templated clues, hidden info).
3. Cop files an incident report independently of the intent record.
4. Match engine scores intent-vs-report agreement (semantic + structured). High agreement = verified label of the incident: THIS IS THE ARTIFACT. Auto-payouts to both sides on agreement; disagreement triggers the Challenge process (human or LLM judge panel = the V3 verifier).
5. Blocker mechanic (anti-match-early): the N most common words for a scene are tabooed per round (KissKissBan, Ho et al. HCOMP '09), forcing rarer, more descriptive, more verifiable reports. This is the one literature-proven fix for the low-effort equilibrium.

**Anti-cheat = the agreement itself:** independent authorship + match is ESP output-agreement; collusion degrades into detectable copy patterns (timestamps + edit distance), and the Blocker makes pre-agreed common answers worthless.

**Session shape (The Precinct lesson):** 20-40 minute shifts; procedural callout generator fills slack; 6v6 or asymmetric 2 cops + 4 robbers per round in Phase 1.

**Period immersion (Mafia II lesson):** cars, radio, weather first. Phase 1 vintage car pack + period radio streams; the illustrated-poster look via the print-shader stack (halftone + Kuwahara + palette quantization, repos verified in REPORT_noir_shaders.md).

**Shader-channel doctrine (the necrodancer-audio analog):**
| Diegetic layer | Encodes |
|---|---|
| Rain intensity | drift/alert level (world state) |
| Neon flicker | lane/round health |
| Wanted posters on walls | live match queue / open warrants |
| Diner/bar window light | player seat activity |
| Halftone dot size | event volume that minute |
| Palette quantization shift | round phase (Downwell lesson: palette IS the HUD) |
| One master uniform (Superhot lesson) | the round clock, driving every stylized pass |

**GWAP payload schema (what the game produces for the fleet):** every matched incident = a verified trace record `{scene_id, intent_struct, report_struct, agreement_score, blocker_taboo_list, witness_clue_chain, verdict}`. These are labeled adversarial-interaction corpora: the externally useful byproduct, exactly the v6 brief's verified-trace-to-artifact shape. Consumers: LLM training pairs (intent/report alignment), evaluation scenarios, the U1-style analysis. Storage: JSONL append-only, one file per session, landed on the shared inbox.

## Purchases/signups this decision needs from the operator (nothing else blocks)

1. Teardown ($30 Steam) for Phase 1.
2. GTA V Legacy copies + Element Club + hosting when Phase 2 starts.
3. dash.llm7.io + SiliconFlow console + chutes.ai signups if the cheap provider lanes are wanted (llm7 note: catalog now has ZERO free SKUs across 64 models; it is a cheap paid marketplace, DeepSeek-V4-Flash at $0.02/$0.04 per 1M).

## Hardware facts this decision respects

RX 5600 XT 8GB (no NVIDIA): fine for Phase 1 mod dev and Ollama lanes; NOT sufficient for local LTX-Video Hopper renders (CUDA-centric) or UE5 Lumen-heavy work at speed. Hopper pipeline and Phase 3 want an NVIDIA 24GB-class card or a cloud render lane.
