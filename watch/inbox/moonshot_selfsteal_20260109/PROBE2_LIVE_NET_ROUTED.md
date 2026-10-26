# PROBE2: LIVE NET ROUTED (2026-10-08, moonshot build order, demand-side)

Mission: route the LIVE GSTD network through our ml3 route table. Read-only,
one curl, $0, no container, no ledger write. Executes the probe in 05_GSTD.md.

## 1. Live census (GET https://platform.gstdtoken.com/api/v1/nodes)

HTTP 200, 2120 bytes, moment per the API's freshest last_seen epoch
(2026-10-09 04:12Z platform clock; local evening 2026-10-08 EDT). count = 5.

| node | wallet (truncated) | v | capabilities | tasks | gstd | rep | last_seen |
|---|---|---|---|---|---|---|---|
| GSTD Bootstrap Pi | UQB03R2D...c8ve | 3.5.0 | llama3.2:3b (1 model) | 288 | 51.3876 | 37 | 2026-10-09 04:12Z, avg resp 34536 ms |
| gstd-desktop (OURS) | UQAcDaht...sjKg | 3.5.0 | 15 models (below) | 0 | 0.0001 | 25 | 2026-10-09 04:05Z, registered 04:03Z |
| LAPTOP-UTO92FB9-node | UQD0gCwC...U1KM | 3.4.0 | none | 0 | 4.7346 | 20 | 2026-10-06 09:25Z |
| unknown (Ubuntu 24.04.4) | (no wallet) | - | none | 0 | 0 | 0 | 2026-10-03 06:44Z |
| localhost-node | UQDTMU95...hAsH | 3.5.0 | qwen2.5:7b | 0 | 0.3444 | 25 | 2026-09-13, dark ~26d |

gstd-desktop caps match local `ollama list` byte-for-byte (15 models):
qwen2.5:7b-instruct-q8_0, gemma2:2b-instruct-q5_K_M, gemma:2b,
Ternary-Bonsai-2-27B-gguf PTQ1_0, athena-class:latest, qwen2.5:7b,
deepseek-r1:1.5b, qwen2.5vl:3b, qwen2.5-coder:7b, qwen-desk:latest,
qwen2.5:3b-instruct, gemma4-desk:latest, gemma4:latest, gemma4-hermes:latest,
nomic-embed-text:latest. (05_GSTD.md wrote "17-model garden"; byte truth
today is 15 - drift noted.) Net total: 16 models across 5 nodes; 15 of 16 on
OUR node. External net contributes 2 models (Pi llama3.2:3b + dark
localhost-node qwen2.5:7b), 1 reachable.

## 2. Our route table (watch/inbox/ml_moonshot_20261007/ml3_route_table.json)

25 shapes, 17-animal vocab, 15 evidence-gated (routable), 10 ungated
("no animal reaches 5 training rows for this shape; do not route").

## 3. The join (shape x who serves the gated best animal)

The live net serves exactly ONE of the 17 ranked animals exactly: qwen2.5:7b
(gstd-desktop live; localhost-node dark). Zero of the 15 gated best_animals
are served by any node, ours included.

| shape | rows | gated best animal | any live node serves it |
|---|---|---|---|
| adversarial-review | 68 | x-ai/grok-4.7 | no |
| arena-agreement-v1 | 461 | anthropic/claude-opus-5.5 | no |
| camp | 36 | anthropic/claude-haiku-4.5 | no |
| descent-leg | 66 | anthropic/claude-opus-5.5 | no |
| dnd-session | 905 | anthropic/claude-haiku-4.5 | no |
| duel | 97 | anthropic/claude-sonnet-5.5 | no |
| gala | 7 | z-ai/glm-5.3-prime | no |
| legality-water-graph-v1 | 100 | legality-propagator-v1 (estate tool) | no |
| night | 44 | anthropic/claude-fable-5.1 | no |
| night-judgment | 6 | z-ai/glm-5.3-prime | no |
| other | 25 | anthropic/claude-opus-5.5 | no |
| planning | 22 | z-ai/glm-5.3-prime | no |
| probe | 24 | anthropic/claude-haiku-4.5 | no |
| schema-design | 20 | z-ai/glm-5.3-prime | no |
| tavern-turn | 1824 | anthropic/claude-haiku-4.5 | no |

Ungated 10 (no routable animal for anyone): askbank-v1-safeguard, beat,
code-analysis, dice, grading, hourly, metagame, season, substance, world-tick.
Only local animal qwen2.5:7b: 1 row on dice, 1 on metagame, 0 elsewhere; never
a winner. Pi's llama3.2:3b is NOT the ranked 11b-vision variant (no family match).

## 4. Gaps

- Fat shapes: 15 of 15 gated shapes need API-tier animals (grok, claude, glm)
  or the estate legality-propagator-v1. The live net hosts none of them.
- Cheap lanes: 10 of 25 shapes unroutable by the evidence gate. The garden
  does NOT already cover them in table terms - 14 of its 15 models are outside
  the 17-animal vocab entirely (coder, vision, embed, r1, 27B bonsai, 32GB
  athena classes). Garden role is the $0 evidence farm to make these lanes
  routable, not current coverage.
- External net: excluding our node, the reachable market is one 3b model on a
  34.5s-response Pi. No node serves a fat shape; falsifier 5 stays frozen.

## 5. The argument (verdict)

CONFIRM on the fat half, REFINE on the cheap half. Byte truth: the live
network serves 0 of our 15 routable shapes (every best_animal is API-tier or
an estate tool) and exactly 1 of 17 ranked animals, and only because OUR
desktop went live minutes before this pull - pre-join that animal sat on a
node dark since 09-13. The garden does not yet cover the cheap lanes (they
are do-not-route shapes); what the live desktop node adds in served-shape
terms is: the net's only live ranked local animal, 15 of the net's 16 total
capabilities, and the only $0 surface where the 10 ungated shapes can earn
the 5-row evidence gate. Before any wallet moves, the desktop FULL node
remains the only join that makes this network useful to the estate - now
proven by network bytes: we are 1 of 2 nodes with capabilities and the other
runs a single 3b model. The Pi's 288 completed tasks prove demand exists for
thin local inference; the 15-model garden is supply-side capacity no other
node joined.

## 6. Next probe (falsifiable)

Submit one real routed task end-to-end when task traffic is wired: pick a
cheap shape, route it through tools/gps_router_v0.py to our own gstd-desktop,
then verify (a) a later /api/v1/nodes pull shows gstd-desktop tasks_completed
0 to 1 and gstd_earned moves, and (b) a gps_ledger row keyed on that external
settlement event. If tasks_completed stays 0 across N verified submissions,
the pool never dispatched to us - an earning-side gap, a different fix.
