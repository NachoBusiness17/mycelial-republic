# BURN: world-models-multi-agent — 2026-09-25

## Verdict

steal

## Evidence

Odyssey homepage (fetched live 2026-09-25) still headlines Agora-1: participants human or AI sharing and interacting inside one real-time world simulation, multiplayer research preview. Agora-2 lives only at /introducing-agora-2 (the homepage lags the drop; the /agora path 404s).

From "Introducing Agora-2" (odyssey.systems): "Agora-2 maintains an explicit shared state that accounts for multiple participants' actions and their effects on one another." Persistence mechanism: "Because entity properties are retained in this state independently of any particular view, they remain available when an entity is out of frame, and do not have to be reconstructed from that participant's visual history when it reappears." Arbitration is single-authority: "The world server then combines the simulation model's predictions to update the shared state, which gives every participant's rendering model the same account of everything that's happening, all in real time." Anti-drift is trained in: "we frequently remove visual history so the rendering model has to rely on the supplied state to depict the simulation."

daily.dev (2026-09-24): "most agent failures in robotics, self-driving, and cyber defense aren't caused by the environment. They're caused by other agents." A quoted observer calls it "a gym for AI agents that happens to be playable." Community split 45% mixed; open questions named: latency, state synchronization, cost at scale.

## Steal or Vacuous

Steal, and it confirms NPC = SEAT as shipped architecture, not metaphor. Agora-2's split maps one-to-one onto fleet canon: explicit shared state retained independent of any view = CANVAS anchors (the anchor is the durable artifact; the view is derived); the world server combining predictions into one shared account = the switchboard/effect broker (one authority arbitrates actor claims; no actor writes shared state directly); per-participant rendering conditioned on that shared state = every actor, human or agent, is a seat rendering the same lane mesh from its own position. Humans and agents enter as identical participants at one interface, which is the NPC = SEAT thesis proven in production.

Sharpest single steal: they train by deleting visual history and forcing reliance on supplied state. That is our warm-boot law (state over scrollback) proven necessary in a shipped world model. Canon phrasing to adopt: drift control is "state over history," enforced at the seat, never accumulated context.

Gap that stays open: long-horizon persistence beyond out-of-frame retention is a stated goal ("extended it in Agora-2 to support more complex interactions over longer periods"), not a measured result. The technical report holding the drift and serving detail is referenced but was not resolvable in fetch; filed owed.

## Falsifier

none proposed

## Bibliography

- watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md, section 6 (drop @odysseyml 2103146841378586820)
- https://odyssey.systems (homepage, fetched 2026-09-25)
- https://odyssey.systems/introducing-agora-2 (fetched 2026-09-25)
- https://daily.dev/posts/odyssey-s-agora-2-puts-20-agents-in-one-shared-world-at-once-3m6xbnplm (2026-09-24)
- Owed: Odyssey Agora-2 technical report (announcement says "Our technical report describes the architecture, training, and serving system in more detail"; link not extractable from the fetched page, guessed path 404'd)
