# THOUGHT PRIMITIVE — spec v0 (the operator-decision twin)

**What it is:** a simulation primitive that answers "what would Nacho do in situation X?" — from his own mapped history, in D&D language, bound by code-as-law. Not a prediction oracle: a POSITION ESTIMATOR with citations.

## Architecture (three layers, all pieces exist)
- **L0 LAW (constants — code as law):** the constitution. The twin cannot violate standing laws; its outputs cite which laws bound the estimate. Operator = constitutional root; the twin NEVER transacts, NEVER decides — estimates and cites.
- **L1 SEA (memory — the mapped ocean):** riddlered decisions as the training sea — `/mag/memory/runs/riddler/*.public.json` (decision shapes, privacy-safe by construction: iso-reencode stripped the personal already) + `ocean_model_mind` / `ocean_persona` organ state (host-side; interface via catalog). Situation-shape lookup: an incoming situation is iso-encoded, then matched against decision-shapes in the sea.
- **L2 GAME (engine — D&D language):** situations rendered as encounters in `game_campaign` (deterministic engine owns truth, LLM narrates after — house pattern). The water-network model supplies PRESSURE (what's queued, what's demanded) — the twin reads the sea's state, not just its history.

## Output contract (per estimate)
likely move (1 line) · matching riddle citations (file + span) · confidence (match quality) · falsifier (what observation would flip the estimate) · laws invoked. No move without citations.

## Falsification rung (before any trust)
Replay 5 real past decisions with known outcomes: the primitive must predict the actual operator move ≥3/5, or it is wrong and stays benched. The sea, not the seat, does the predicting.

## Rungs
- R0: inventory riddler corpus (readable NOW from cage — public.json shapes) + catalog the ocean organ interfaces [host-side later].
- R1: primitive v0 in-cage: iso-encode a test situation → shape-match against riddler sea → narrate with citations. Zero new authority.
- R2: falsification replay (5 decisions, ≥3/5 or benched).
- R3: D&D rendering — the twin answers inside game_campaign as an NPC with the operator's sheet.
- R4 (host): wire ocean_model_mind organ state into L1 via the jail.

## Provenance
Method #3 in the evolving set: (1) salon fan-out enhances asks via model lenses, (2) Socratic discovery, (3) thought primitive simulates the asker. All three feed the v5 contract's methods chapter. Convergence note: builder's Futamura lens maps this too — the sea is the static input, the situation is dynamic, the primitive is the residual program.
