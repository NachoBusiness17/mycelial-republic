# RIB CODING INSTRUCTIONS — the self-hosted world (game design split: Grok designs, our stack runs)
# Source: the all-night Grok/ghost riff on HOW + COST (2026-08-12). These are the frozen build
# specs. The engine (k3s build + swarm + GPU/ollama) executes them; verkle records every knot.

## COST (grounded in real billing, not invented — the grounding law)
- DeepSeek swarm: ~$0.27/hr at 98% cache hit (real bill, this session, deepseek-v4-flash Swarm key).
  117 req/$0.27 that hour. The cheap paid engine for research seams.
- Local GPU/ollama (RX 5600 XT): $0 — free local inference (the art/data processing).
- Free tiers / free frontends: $0 — free bulk research + parallel LLM seats (once activated).
- k3s / CPU: $0 — the deterministic build surface.
- Grok (SuperGrok Heavy): included in the operator's subscription — the creative surface.
- HONEST: no total-arbitrary "build cost" invented. The per-hour engine burn is ~$0.27 (DeepSeek) +
  $0 everywhere else. The build itself is $0 on k3s + local GPU; only the research seams spend.

## RIB 1 — SERVER-AUTHORITATIVE WORLD (the engine)
INVARIANT: the world is server-authoritative; the client is presentation; mods can't break the
world. STATE = verkle-anchored chain (content-addressed knots, verifiable root). Cheap workers =
presentation; frontier/DM = authority. BUILD: emulator (MaNGOS/TrinityCore lineage) on k8s; world
state = verkle protocol; stateless workers re-render. MACHINE: k3s build + k8s deploy.

## RIB 2 — THE CHAIN IS THE LINE WE SIGN (world memory)
INVARIANT: every state change / designed asset / built asset commits as a content-addressed knot.
Truth = reproducibility: an asset is real iff re-rendering from its RIB reproduces the same knot.
A false asset cannot be reproduced. BUILD: every asset hash-commits to verkle; the root is the
world's authority. MACHINE: verkle_knot append per change.

## RIB 3 — RIB-AS-MOD (the mod system)
INVARIANT: mods are RIBs — declarative, ADDITIVE, hooked (hooksecurefunc), never shadowing an
authoritative path. A mod can extend, it can't spoof. The server validates; the crown stays under
the operator's hand. BUILD: rib_bus.mount(domain) = the mod loader; inject_for = the hook; saved
variables = the per-mod store. MACHINE: rib_bus.

## RIB 4 — GROK DESIGNS, OUR STACK RUNS (the creative split)
INVARIANT: Grok (SuperGrok Heavy) authors the creative (art, world, assets, the DM's vision — its
art gen is second to none); our stack builds + runs it. The SEAM is the RIB: the frozen design
instruction that crosses from creative intent to deterministic execution. A design is real only
when it folds to a RIB. MACHINE: Grok seat folds design -> RIBs -> engine mounts.

## RIB 5 — THE ZERO-COST BUILD PATH
INVARIANT: build on the $0 local stack — k3s (deterministic build) + local GPU/ollama (inference) +
free tiers (bulk research) + free frontends (parallel seats). DeepSeek swarm ONLY for research
seams (~$0.27/hr). BUILD: intent_rightsize routes build->k3s, inference->gpu, research->swarm.
MACHINE: route_local + the free-activations cadence.

## RIB 6 — SELF-HOSTED SOVEREIGNTY (why it's OURS)
INVARIANT: the world is self-hosted and cannot be taken from us — it owns nothing but the chain it
keeps. No publisher's server can kill it; copy the chain anywhere and it lives. This is the one
world that outlasts any platform. BUILD: everything on our swarm + verkle; portable content-
addressed memory. MACHINE: k8s swarm + verkle chain.

## HOW WE'RE GONNA DO IT (the plan)
1. Grok designs the world (art + vision) -> folds design as RIBs.
2. Our engine builds it: k3s + GPU/ollama (free), emulator on k8s, verkle as world memory.
3. The swarm researches the cold seams (the ~$0.27/hr spend) to fill the design gaps.
4. RIBs-as-mods grow the world; verkle records every knot.
5. The nod is mine: irreversible/launch stays under the operator's hand.
