# F12 - first bulk feed of the living behavioral layer (2026-09-30)

Mission: read today's behavioral evidence (duel ledger, D6 ask-bank flip, AJ1
alt-judge, gopher burn, AA1 a1/a2 timeouts, D6 contamination, stealth findings)
and bank EVERY finding as a sourced observe() row. Target 20+ observations
across 5+ animals. Result: **+37 observations across 13 animals**, distill
regenerated, rib EVIDENCE footer created (the rib had none).

## Distill before/after (the receipt)

BEFORE (8 rows / 7 animal files, seed pass 2026-09-30T21:35Z):

```
- claude_opus_5_5: 2 obs [pricex1, transportx1] newest 2026-09-30 sources=2
- deepseek_v4_1_flash: 1 obs [railx1] newest 2026-09-30 sources=1
- grok_4_7: 1 obs [verdictx1] newest 2026-09-30 sources=1
- ling_3_0_flash_sante: 1 obs [envelopex1] newest 2026-09-30 sources=1
- nous_primes_lane: 1 obs [railx1] newest 2026-09-30 sources=1
- qwen3_7_flash: 1 obs [failurex1] newest 2026-09-30 sources=1
- zai_coding_plan: 1 obs [envelopex1] newest 2026-09-30 sources=1
```

AFTER (46 rows / 16 files at append time; a sibling lane's test_probe smoke
row appeared 23:47:17Z and was removed by its owner before the rib stamp, so
the footer and tree now read 15 animals / 45 rows + probe-independent):

```
- claude_opus_5_5: 5 obs [failurex1, pricex1, railx1, transportx2] sources=3
- deepseek_v4_1_flash: 3 obs [pricex1, railx1, verdictx1] sources=3
- fireworks_ember_1: 5 obs [failurex3, pricex1, verdictx1] sources=3
- google_gemini_3_8_flash: 3 obs [railx1, verdictx2] sources=2
- grok_4_7: 3 obs [pricex1, verdictx2] sources=2
- ling_3_0_flash_sante: 3 obs [envelopex2, railx1] sources=2
- meta_muse_glimmer_30b: 1 obs [envelopex1] sources=1
- nous_primes_lane: 1 obs [railx1] sources=1 (seed, untouched)
- qwen3_7_flash: 3 obs [failurex2, pricex1] sources=2
- qwen_qwen3_8_max_prime: 3 obs [pricex1, railx1, verdictx1] sources=2
- stealth_free_lanes: 1 obs [envelopex1] sources=1
- stealth_space_bunny_alpha: 3 obs [failurex2, verdictx1] sources=2
- x_ai_grok_4_3: 3 obs [failurex1, railx1, verdictx1] sources=2
- z_ai_glm_5_3_prime: 7 obs [failurex1, pricex1, railx1, verdictx4] sources=4
- zai_coding_plan: 1 obs [envelopex1] sources=1 (seed, untouched)
```

Every row cites its receipt (logs/duel/duels.jsonl row ids, D6/AJ1/AA1/gopher
receipts, STEALTH_MINED_FINDINGS.jsonl + STEALTH_TRIAGE_20260930.md). Stats were
computed from bytes, not read off prose: the qwen-glm 18-12-1 and cost/char
ranges come from a venv script over the 76 ledger rows; stealth per-model
finish/cached_tokens tallies over all 459 findings rows.

## What the new rows say (headline per animal)

- **opus-5.5** (+3): W4 16k all-reasoning empty; a1 1800s + a2 3600s
  whole-response timeouts ($0 metered, usage={}); 32k reasoning-eats-29476
  truncation. Whole-response is dead for 32k Opus.
- **glm-5.3-prime** (+7): 18-12-1 vs qwen3.8 at 1/3-1/4 cost; D6 hidden 3-0
  gemini; alt-judge 10/10 zero-flips (second-judge family EARNED); slot-A lean
  as judge (p=0.0547, arena not judge); judge quirks; AH10 2-0; price by shape.
- **qwen3.8-max-prime** (+3): loses the in-family head-to-head at ~3x cost;
  verbose (avg 8217 chars, 18 headers) without converting volume to wins.
- **gemini-3.8-flash** (+3): the D6 flip animal — plain-sight 3-0 sweep of glm
  is contamination-suspect; hidden draw 0-3 at 2-3x cost.
- **ember-1** (+5): starves below 512 max_tokens (2 empty probes at 16);
  rationale contradicts its own table (D6 r1/r3, three x4 rows); same-answers
  slot-swap verdict flip (retro n=1); coverage-over-fidelity bias (scored
  grok-4.7's off-task review 5/5); price truth.
- **grok-4.7** (+2): $0.2347-0.2661/fresh answer (dearest in ledger); the 9-0
  V1 sweep rode off-brief answers — contamination-suspect per D6.
- **grok-4.3** (+3, new file): 0-5 W8 surviving alt-judge; minimal-output mode
  (1295 chars / 0 headers on adv); schema type errors + fake sha256.
- **deepseek-v4.1-flash** (+2): 6-0 W8 sweep survives a judge family outside
  both opponents — cleanest tier signal; cheapest contender ($0.0005-0.0162).
- **qwen3.7-flash** (+2): fabrication concurred by two judge families (invented
  stats, nonexistent fallback_router.py/router.yaml/FAMILY_REGISTRY).
- **ling-3.0-flash-sante** (+2): cached_tokens=0 on ALL 110 openrouter rows
  (space-bunny rides 128-152 same lane) — cache economics unbankable; via-nous
  114/114 stop, terse honest answers, sensing-only.
- **space-bunny-alpha** (+3, new file): free-lane substance leader (6.7-8.0KB);
  owns ALL 9 finish=length rows in the file; ponytail dead-citation catch.
- **muse-glimmer-30b** (+1, new file): cached 0-210 volatile, generic, sensing-only.
- **stealth-free-lanes** (+1, new lane file): 459 rows, ZERO 429/empty under a
  69h+ FORCED loop — contradicts the rib "force -> 429 throttle" law (caveat in
  row: register may log successes only; check impfeed error path before amending).

## Incidents + fixes during the feed

- Slug fragmentation: my route-named observe() calls (e.g. "x-ai/grok-4.7")
  created parallel files for animals that already had seed slugs (grok_4_7).
  Fixed by merging rows BYTE-IDENTICAL into the canonical seed files and
  deleting the fragments — append-only preserved at the animal level, no row
  edited or lost (46 rows before and after the merge, counted).
- A sibling lane's test_probe smoke row (f4_flash_census.py) appeared at
  23:47:17Z and was removed by its owner before the rib stamp; the footer is
  byte-consistent with the tree as stamped.

## Rib application

Appended `## EVIDENCE (distilled 2026-09-30T23:47:51Z, F12 first bulk feed)` to
`memory/rib/RIB_MODEL_GATES_20261001.md` — the rib's first evidence footer (it
had none), per the tool's own contract (distill emits, orchestrator applies).

## Files owned / landed

- `memory/behavioral/animals/*.jsonl`: +37 rows this pass (16 files, 45 rows net)
- `memory/rib/RIB_MODEL_GATES_20261001.md`: +EVIDENCE footer
- `tools/animal_profiles.py`: used as-is (observe/distill API held; no change needed)
- This receipt.
