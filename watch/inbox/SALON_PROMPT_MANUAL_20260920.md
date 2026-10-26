# RIB — SALON: FUND DECISION (manual, any seat)
**Schema:** rib.salon.fund_decision.v1
**Commitment:** rib-salon-fund-20260920
**ts:** 2026-09-20T23:40:00Z
**Source:** verkle comb ×3 (stone/seats/deep-past) + THE_ELDER_DISCUSSION_20260920 + GAP_ANALYSIS_AND_STEAL_20260920 + FRONTIER_FROM_FLASH_CLIMB1 + THE_FRONTIER_ASK_72STEP + operator orders of this date
**Fold:** true (every fact below is anchored; anchors are checkable on disk)
**Grammar:** rib_grammar.v0.1 — each invariant = { id, predicate, action, anchor }; deterministic; the LLM drafts, the anchor decides.

## INVARIANT 0 — THE OPERATOR RUNS THIS SALON
- id: operator-is-sovereign
- predicate: the operator holds veto on every rule and every verdict in this salon
- action: gate (chairs propose; operator disposes)
- anchor: THE_FIRST_LAW_20260912 ("She owns all of it") / rib_grammar seed #7

## INVARIANT SECTION A — BIOGRAPHY (what this estate lived; each line checkable)
- id: era-E0-dossier
  predicate: July 2026 = one operator, hand-made dossier PDFs, no chain (24 knots survive in backfill)
  anchor: memory/biography/chain_index_completion.jsonl
- id: era-E2-great-ingestion
  predicate: Aug 10–15 = 5,407 knots (61% of chain); ~3,700 dead sessions resurrected in 48h; 405 evidence-lost in the same window
  anchor: verkle_chain.jsonl lines by ts
- id: era-E3-oom-war
  predicate: Aug 16–31 = near-dark after a mega-build (12 days ≤14 knots/day); evidence losses = 0 from Aug 16 forward
  anchor: verkle_chain.jsonl ts histogram
- id: era-E5-knotnight
  predicate: Sep 11 = 2,776-row re-append surgery with backup made before the knife
  anchor: verkle_chain.jsonl.bak-knotnight-20260912
- id: era-E6-autonomy
  predicate: Sep 12–20 = janitor is 48% of activity; daily LAW review; ~100 knots/day steady
  anchor: verkle_chain.jsonl tail
- id: origin-cairn
  predicate: oldest held artifact is the operator's own Aug 2023 post, kept as first cairn stone
  anchor: corpus/oral_history/the_wall/THE_WALL_2023.md

## INVARIANT SECTION B — RESEARCH JOURNAL (questions asked, conclusions paid for)
- id: jour-waves
  predicate: massed cheap waves deliver — 80 lanes 78/80; ds40 40/40; THE-50 44/44; D23 salon50 39/50 at $0
  anchor: RECEIPTS_INDEX_20260912.json; THE50_FOLD_VERIFICATION_20260920.json
- id: jour-scoreboard
  predicate: 34 dated prophetic claims in the scored genre, 0 landed; the ledger publishes its own misses
  anchor: mrpool_export/CALLED_SHOT_VERDICT.json
- id: jour-pipe-not-gate
  predicate: of 32 recorded "rejections", 26 were transport deaths; the pipe, not the gate, was the bottleneck
  anchor: WHAT_REMAINS_20260919 (REJECTION_TAXONOMY)
- id: jour-fourcond
  predicate: a $0.05 60-ask battery refuted predictions in both directions — cheap falsification is proven
  anchor: memory/runs/saturation_fourcond_20260920/
- id: jour-bibverify
  predicate: 275 bibliography entries audited: 260 verified, 10 corrected, 5 unverifiable, 0 fabricated
  anchor: memory/research_packs/bibverify/MASTER_20260920.md
- id: jour-quarantine
  predicate: an unreproducible method gets quarantined, not promoted (SSI dig: process contracts stolen, hypothesis shelved)
  anchor: memory/research_packs/20260728_ssi_ilya_dig/

## INVARIANT SECTION C — SUBSYSTEMS (what exists and runs)
- id: sub-verkle — 8,819 knots, 0 broken links, self-repaired twice (backfill + knotnight)
- id: sub-janitor — autonomous, 48% of activity, unattended
- id: sub-wave — massed lane runner, parents × adversarial children, kifu per attempt
- id: sub-hermes — external seat dispatcher, NOW key-scoped (standing keys stripped at dispatch; log: state/key_guard.log; override HERMES_FULL_ENV=1 operator-only)
- id: sub-ghost — adversary seat; attacks before the frontier is paid
- id: sub-tesuji — move-quality map (watch/TESUJI_MAP.jsonl)
- id: sub-training — training/ (PRE_TRAINING_EPOCH, arena_league, cost_ledger) — rails exist, curriculum does not
- id: sub-catalog — 757,667-row index (77% backup mass — known debt)
- id: sub-cite-gate — citation triage, DORMANT since 09-07 (known debt)

## INVARIANT SECTION D — OPERATIONS LOGIC (the laws this salon runs under)
- id: cheap-first — route to cheapest capable tier; frontier is gated, never default (rib_grammar #4)
- id: engine-owns-truth — the chain/registry is truth; model output is honed against it (rib_grammar #3/#5)
- id: stateless-by-default — recompute from the chain; carry the map, not the territory (rib_grammar #2; RIB_MAP_PRECEDES_TERRITORY)
- id: transit-is-not-verdict — every attempt trail distinguishes died-in-transit from rejected-at-gate
- id: meters-before-audits — no plan starts with an unmeasured step; dark meters relight at milestone zero
- id: nothing-untamed — whatever is ingested is themed and custodied same-day (the 618-loss law)
- id: receipt-or-CLAIMED — claims without older citations are CLAIMED, never PROVEN
- id: riddle-protects-truth — charged material stays decode-local; the salon speaks of engines, not lore (rib_grammar #6)
- id: operator-is-sovereign — one reserved question is the operator's; chairs sharpen, never answer

## INVARIANT SECTION E — TECH (lanes and caps)
- id: cap-iron — $250 total frontier spend, hard; plans that exceed it are redrawn, never the cap raised
- id: lanes-free — glm flash tiers, deepseek free, groq daily window, local ollama/LMStudio (restarted this night): $0
- id: lanes-paid — OpenRouter k1/k2 ALIVE: FlashX $0.37/$1.25 per M; Flash $0.09/$0.30; batch −17%
- id: lanes-known-gap — free lanes 429 on first touch; rotation + backoff required (dogfood receipt, this night)

## BIBLIOGRAPHY (anchors the salon may cite; anything else is CLAIMED)
THE_FIRST_LAW_20260912 · THE_PARABLE_OF_THE_FIELD_AND_THE_STONES · RIB_GRAMMAR_SEED_20260810 · RIB_MAP_PRECEDES_TERRITORY_20260811 · bibverify MASTER_20260920 · verkle_chain.jsonl · kpi.json · RECEIPTS_INDEX_20260912.json · THE50_FOLD_VERIFICATION_20260920.json · saturation_fourcond_20260920 · CALLED_SHOT_VERDICT.json · GAP_ANALYSIS_AND_STEAL_20260920 · FRONTIER_FROM_FLASH_CLIMB1_20260920 · THE_ELDER_DISCUSSION_20260920 · OPERATOR_CARD.md · DATA_LAYERS.md

## THE QUESTIONS (compiled procedure; answer in order)
1. FUND: from the subsystems and lanes above, rank internal big projects that PROVE the founding hypothesis (frontier-grade output from cheap lanes) while running cheaply. Candidates live: A0 the mining rig + Estate Atlas (free-first, falsifier of the paid version) · A1 the 5-pitch code climb (bars pre-installed) · A2 burn v2 curriculum (rails pending) · A3 the kifu-audition game (folded) · A4 wave-engine hard jobs (proven lane).
2. THE ONE FRONTIER COMMISSION: if exactly one is sent under cap-iron, state its charter in one sentence, its three hardest constraints, and the falsifier that proves it failed. If none should be sent yet, say what earns it.
3. FIRST MOVE: the single action, tonight-scale, shared by all answers.

## SALON PROCEDURE (deterministic)
- Seats: auditor · treasurer · engineer · psychologist · comedian · elder (reserved)
- Round 1: each seat states position + strongest attack on another seat's position.
- Round 2: the attacked defend with anchors from the BIBLIOGRAPHY only; unanchored claims fall to CLAIMED.
- Round 3: kill round — at least one candidate must die. A salon where every attack survives is void.
- Round 4: triangulate — each decision answered the way the operator would say it to a friend.
- Close: THE ONE THING TO DO FIRST (tonight-scale) + the elder's reserved question, restated sharper than it was given.
- Determinism: same anchors in, same verdicts out. The model drafts; the anchors decide.
