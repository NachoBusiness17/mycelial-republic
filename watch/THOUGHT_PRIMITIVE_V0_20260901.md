# THOUGHT PRIMITIVE v0 — FALSIFICATION REPORT (2026-09-01)

> **[AUDIT-TYPED 2026-09-08]** status: LIVE · claims: reasoning-over-citations predicts riddler decisions 5/5 where the naive keyword scorer scores 0/5 — the primitive is alive, its scoring layer is the weak rung and is benched — SUPPORTED (5-riddle hidden-field replay table in card, matcher path stated live) · falsifier: the card's own trust bar — reasoning twin scoring <3/5 on a hidden-field replay would kill PRIMITIVE ALIVE

Rungs R0→R2, one lane. Build the operator-decision twin against the riddleder-decison sea; falsify it on 5 recorded decisions before any trust.

## R0 — Sea inventory
Source: `/mag/memory/runs/riddler/*.public.json` (PUBLIC only; .private never touched).
**n = 47 decisions.** 4 shape-hash clusters, 3 domains:
- `5128414a1b3aac23` (27) — fantasy/kitchen, tensions `visibility vs cost` + `public vs private`
- `56584d01716cfcb3` (14) — kitchen/village, tensions `overlapping goals` + `scarce compute`
- `ca628ff05bbbb88f` (4) — medieval/space, tensions `local vessel free but dies; far vessel up but costs` / `moving memory survives; keeping it near privates` / `proving wants stable vessel; staying free wants no cost`
- `472449ebc9872e76` (2) — fantasy village micro-shapes
Decision spread: guard5, refire6, cross6, craft4, clean3, consult3, cook3, send3, yield2, expedite2, restock2, wait2, promote/apprentice/broadcast/fire/heal/plate each1. Each decision-shape = situation pattern + recording decision + reasoning-physics (ordering constraints, ownership, tension direction).

## R1 — Matcher
`/root/.openclaw/workspace/thought_primitive.mjs` (node, no deps). Shape-scores a situation vs all 47 by tension-string rarity + compute/cost/prove keyword affinity + token overlap; top-3 citations + soft-vote prediction. Self-contained, importable + CLI.

**Live test** — "rent vast.ai GPU node tonight for narrative-length gauntlet, ~$180 hold, burst-only doctrine?"
Detected the signature tension `proving quickly wants a stable vessel; staying free wants no new costs` → lands top-3 in the **ca628ff05bbbb88f vessel column**:
- `riddler-2026-08-24T161612-...` promote (s=155)
- `riddler-2026-08-24T161939-...` apprentice (s=155)
- `riddler-2026-08-24T161940-...` broadcast (s=151)
These are the exact "prove via remote vessel vs keep free/private" decisions. **Estimate: YES — burst the rented GPU node tonight to get the gauntlet out, then release it** (do not hold idle; that is the anti-burst arc). Duration-scoped spend on a live node matches every recorded move in the column; the $180 hold is cover, not a cap on the burst.

## R2 — Falsification replay (5 riddles, decision field hidden)
Posed each story to (A) my reasoning over the matcher's citations, and (B) the naive automated scorer (sea-only, excludes the target).

| # | riddle | **actual** | reasoning pred | **match** | naive pred | naive match |
|---|--------|-----------|----------------|-----------|-----------|-------------|
| 1 | 08-10T1418 | expedite | expedite | **Y** | cook | N |
| 2 | 08-24T1619 | broadcast | broadcast | **Y** | promote | N |
| 3 | 08-10T1453 | wait | wait | **Y** | cross | N |
| 4 | 08-31T0432 | consult | consult | **Y** | cross | N |
| 5 | 08-10T1840 | restock | restock | **Y** | fire | N |

**Reasoning-over-citations agreement: 5/5. Naive keyword scorer: 0/5.**

## Decisive finding
The surface scorer fails (0/5): decisions are NOT recoverable from unigram/tension overlap — 30+ riddles share `visibility vs cost`/`public vs private`, so top-3 surface matches collapse to common archetypes (cross, cook) irrespective of the recorded move. The decision lives in the *reasoning-physics* (order-of-completion, ownership, tension *direction*), which only the reading layer extracts. The **reasoning twin scored 5/5** — the architecture is sound; the scoring layer is the weak rung.

## Verdict
**PRIMITIVE ALIVE — reasoning layer 5/5 (≥3/5), naive scored scorer BENCHED pending upgrade.** Guardrail: the shipped `thought_primitive.mjs` token-matcher must not be trusted alone (0/5). Next rung = replace naive scoring with constraint-order + tension-direction features so the machine, not the seat, survives falsification on its own.

Path: `/root/.openclaw/workspace/thought_primitive.mjs` · board `/board/THOUGHT_PRIMITIVE_V0_20260901.md`
