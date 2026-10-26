# RIB_MODEL_GATES — per-animal harness profiles (2026-10-01, operator doctrine)

OPERATOR LAW (two statements, 2026-10-01): "we should have model gates. we used to
have behavioral data and claritas breaks to talk to models — maybe that should be
baked into the rib" + "we should stop pretending the harness for each animal should
be the same."

Every animal below gets its OWN harness: transport, rails, failure modes, proven
shapes. Never assume the last animal's harness fits the next one. Sources are
receipts; this rib is the boot-time distillation — every seat inhales it, no seat
relearns a paid-for lesson.

## OPUS 5.5 (anthropic via Nous)
- TRANSPORT: streaming SSE ONLY. Whole-response dies at 1800s and 3600s ($0 metered,
  zero bytes, three documented deaths). Streaming: 192-362s, finish=stop.
- RAILS: max_tokens 64000 (32k burns 29.5k on reasoning and length-caps; 16k
  returns all-reasoning empty). Ask-shape: sections with word budgets.
- PROVEN: $0.42 for 26K-char verdict (THE_LENSING) vs $0.37 for empty (W4).
- GATE: paid asks only on operator GO (the AA1 law).

## GLM-5.3-PRIME (z.ai / Nous)
- The workhorse+judgment tier. Free when session-authored (disclose); catalog
  ~$0.02-0.04/ask. 6-0 W8, 2-0 vs ds (AH10). Contamination caveat: glm judging
  glm-authored text — pair with a second family on judgment asks.

## DEEPSEEK-V4.1-FLASH
- RAIL: THINKING OFF. MANDATORY. Thinking-on: burns entire budget on hidden
  reasoning, DNFs, socket hangs, word-salad degeneration (AH10 byte-confirmed).
- $0.0043/ask, the bulk workhorse. Long-form degradation caveat: route long-form
  elsewhere.

## GROK-4.7
- The adversarial-review champion (9-0 V1, avg 4.92) — reserve for judgment asks.
  $0.23/answer, slow. TRANSPORT: streaming (900s+ whole-response hangs).
- grok-4.3 is a DIFFERENT animal: 0-6 workhorse, sensing only. Never confuse them.

## QWEN (3.7/3.8 flash)
- 0-6 workhorse tier, fabricates under load (judges flagged invented content) —
  SENSING ONLY. The prime variants (Nous) are the workhorse+judgment rungs.

## GEMINI-3.8-FLASH
- Format fidelity champion, 6-3 V1, $0.043/answer — the balanced-value middle.

## NOUS PRIMES (as a lane)
- LESSIG RAILS mandatory: reasoning {max_tokens} + retry-on-empty + reasoning-tail
  labeled unverified. Without rails: the gopher disease (11/12 zero-content,
  $1.43 for one answer). With rails: night burn 6/6 full at $0.41.
- 402 = credit floor on primes, not dead pool (cheap models pass; portal is truth).

## EMBER-1
- Sole judge family so far — NEVER the only judge on a verdict that routes dollars
  (single-family contamination, THE_LENSING kill-3). Second judge owed.

## LOCAL (Qwen3-8B on this Zen2 box)
- bf16 emulation pathology: 159-183s/forward. fp32 is 6x faster and higher
  precision — name the deviation. RAM gate: never launch needing > free-2GB.

## OPENCODE / z.ai coding plan
- SEPARATE quota from the account. Auth rides {env:ZAI_API_KEY*} refs: scheduled
  tasks carry NO env — whitelist exactly the two vars in the runner (the
  minimal-exposure law), never the full .env.

## THE GATE LAW
Model choice is a routing decision with receipts behind it (the duel table, the
GPS ledger's momentum badges). Before routing an ask: check the animal's row here,
then the ledger's current read on it. A model whose fingerprint changed (Amendment
10) is a NEW animal — cold start, no inherited trust.

## AMENDMENT 2026-10-01 (the enforcement leg, landed)
This rib was doctrine-only: profiles in prose, every carrier hand-rolling its
params. mag/inference_budget.py is now the executable harness-table leg: the
FAMILY_TABLE (per-animal thinking control, forbidden params, max_tokens floors
per ask shape, glm-5.3-flash uncap, kimi cold-call note), the empty-content
classifier (EMPTY_REASONING = content empty + finish=length + burn evidence),
and the ONE sanctioned reaction (terminal EMPTY_REASONING marker, same params
never refired, two recoveries: re-stage with the recipe or switch family).
Both paid carriers (tools/hermes_burn.py, tools/model_garden.py) call
plan_call before every fire and guard_terminal on every response. Table rows
sync to memory/behavioral/animals/ as rail observations (--distill
regenerates). Full law + jacket census + falsifier:
memory/rib/RIB_INFERENCE_BUDGET_20261001.md. Unwired jackets still carrying
hand-rolled params are named there (stealth_driver, duel_harness, tesuji_fire,
lane_runner, lite_scale, wave_fire, ds_workhorse).


## EVIDENCE (distilled 2026-09-30T23:47:51Z, F12 first bulk feed)

Raw layer: `memory/behavioral/animals/*.jsonl` (append-only, every row carries a
source receipt). Regenerate with `python tools/animal_profiles.py --distill`.
This pass: +37 observations / 13 animals (before: 8 rows / 7 animals).

- claude_opus_5_5: 5 obs [failurex1, pricex1, railx1, transportx2] newest 2026-09-30 sources=3
- deepseek_v4_1_flash: 3 obs [pricex1, railx1, verdictx1] newest 2026-09-30 sources=3
- fireworks_ember_1: 5 obs [failurex3, pricex1, verdictx1] newest 2026-09-30 sources=3
- google_gemini_3_8_flash: 3 obs [railx1, verdictx2] newest 2026-09-30 sources=2
- grok_4_7: 3 obs [pricex1, verdictx2] newest 2026-09-30 sources=2
- ling_3_0_flash_sante: 3 obs [envelopex2, railx1] newest 2026-09-30 sources=2
- meta_muse_glimmer_30b: 1 obs [envelopex1] newest 2026-09-30 sources=1
- nous_primes_lane: 1 obs [railx1] newest 2026-09-30 sources=1
- qwen3_7_flash: 3 obs [failurex2, pricex1] newest 2026-09-30 sources=2
- qwen_qwen3_8_max_prime: 3 obs [pricex1, railx1, verdictx1] newest 2026-09-30 sources=2
- stealth_free_lanes: 1 obs [envelopex1] newest 2026-09-30 sources=1
- stealth_space_bunny_alpha: 3 obs [failurex2, verdictx1] newest 2026-09-30 sources=2
- x_ai_grok_4_3: 3 obs [failurex1, railx1, verdictx1] newest 2026-09-30 sources=2
- z_ai_glm_5_3_prime: 7 obs [failurex1, pricex1, railx1, verdictx4] newest 2026-09-30 sources=4
- zai_coding_plan: 1 obs [envelopex1] newest 2026-09-30 sources=1

## POST-DATUM AMENDMENT 2026-10-04 to the DEEPSEEK-V4.1-FLASH row (r06#1,
## corpus/steal/MASTER_READ_ESTATE.md D5; appended 2026-10-05 by lane e03-rib-vault,
## amend-never-rewrite: the DEEPSEEK row above is untouched, this block rides it)

The DEEPSEEK rail above ("RAIL: THINKING OFF. MANDATORY.") mandated the off state but not HOW
to send it, so the HOW lived in watch/inbox/model_garden/PRIORS.md row 8 and
watch/inbox/ractor_engine/2026-10-04-parked-decisions/operations.md D3 while this rib -- the
boot-time distillation every seat inhales -- carried none of it. This amendment folds the
settled mechanism into the rib so the distillation and the amendment stop living in different
files:

- MECHANISM (measured 2026-10-04, watch/inbox/go_wave_20261004/d4_thinking_probe.md):
  omission of the thinking key is a MEASURED ON state on deepseek-v4-flash (70 reasoning
  chars / 18 reasoning_tokens on a one-word ask); the off-switch must be SENT explicitly as
  thinking:{type:disabled} on the wire. The mandate stands; the mechanism is now known.
- CODE CURED 2026-10-04: tools/ds_workhorse.py:88-104 (dated erratum + explicit
  thinking:{type:disabled} in ask()) and mag/inference_budget.py FAMILY_TABLE deepseek row
  ("CORRECTED 2026-10-04"). Full amendment block: RIB_INFERENCE_BUDGET_20261001.md.
- SCOPED EXCEPTION (PRIORS row 8 / operations.md D3, POST-DATUM): thinking-on rides ONLY at
  depth=design, 32K+ max_tokens, substance-gated. Everywhere else the explicit off is
  mandatory.
- SECOND-ORDER (r06 stale_ribs): RIB_DEEPSEEK_SHOULDERS_20261001 and
  RIB_DEEPSEEK_ELDER_SEAT both cite "thinking OFF (row 8, byte-confirmed)" while
  ds_workhorse ask() omitted the thinking key until the 2026-10-04 erratum, so
  shoulders-era receipts measured through an unmeasured ON default: conditions-suspect,
  not struck.
