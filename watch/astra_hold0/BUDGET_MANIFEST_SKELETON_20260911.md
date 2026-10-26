# BUDGET-MANIFEST SKELETON — the meter, per-episode bounds, the 1,920 envelope, held keys, $0 rules (2026-09-11)

==== FREEZE STAMP ====
artifact:     watch/astra_hold0/BUDGET_MANIFEST_SKELETON_20260911.md
sha256:       c9dae6c6768ac66997e32db955530d1e6002577f0cb466839f5e84ada06221a9
frozen-at:    2026-09-10T00:06:43Z
author:       builder wave 09-11 (task-pack skeleton builder, zcode seat)
amendments:   rows A1-A6 (amendment ledger; A4-A6 = Astra v2 review adoption)
kit:          FEN_FREEZE_KIT_20260911.md
=======================

> **[AUDIT-TYPED]** status: SKELETON — DESIGN, nothing frozen · provenance:
> builder wave 09-11 · fulfills registration-bundle work-list item 6: "Budget
> manifest: token allowances, metering, deadline per family" (Astra's CAMP
> STATE v1 open list). Per-instance budget fields (F4 of the L0 contract:
> allowance / metering / retry / deadline) are defined in
> TASK_PACK_SKELETON_20260911.md and AGGREGATE into this manifest.
> **TESLA'S LAW (adopted, `watch/SALON_BUILD_DIRECTION_20260909.md`):** this
> manifest is not paperwork — it is THE METER, build-order item 2, the
> instrument that makes the 1,920-episode race runnable. Token accounting per
> episode, per condition, per family FROM DAY ONE. When TESLA_METER_SPEC lands
> in this directory, its schema is adopted here by receipted append.
> Companions: TASK_PACK_SKELETON_20260911.md · NOVELTY_MAP_OUTLINE_20260911.md

## 1. THE ENVELOPE (SUPPORTED — her pre-registration, campaign log)

- **1,920 episodes = 20 blocks × 12 tasks × 2 families × 4 conditions.**
  Per task type: 20 × 2 × 4 = **160 episodes**. Irreducible half (I1-I6):
  **960**. Sham half (S1-S6): **960**.
- **≤32 operator hours** total (her cap).
- Families = 2 of the 4 held model configs, pinned by the OPERATOR (her work
  list item 1 — open, operator-only by design).
- Four conditions (SUPPORTED, `watch/ASTRA_FOLD3_20260909.md:29-36`, locked
  design): **A COLD** (task only) · **B WARM-TYPED** (constitution + event
  layer v2) · **C WARM-FREE** (same prefix, unconstrained messages,
  token-budget MATCHED to B) · **D DESK** (human folds and injects,
  **4-minute cap** — the measured fire window). B−C is the core gate
  (> +5 per family on irreducible tasks — executed per the pre-registered
  decision procedure in §5a, not as a bare threshold), which is why C's token-budget
  matching matters: the manifest must hold B and C compute-equal at the
  episode level or the gate measures budget, not warmth.
- **DISPUTED-TENSION (filed, not sanded):** the D-arm arithmetic. 20 blocks ×
  12 tasks × 2 families = **480 desk-arm episodes**; EDISON's spec refines the
  cap — **240 seconds of CUMULATIVE work per episode** (reading, deciding,
  folding, injecting, no off-clock prep), waiting time recorded separately.
  Even at refinement: 480 × 240s = 115,200s = **exactly 32 hours = the entire
  operator-hours budget**, zero slack for carriage, scoring adjudication, and
  sealing — and "no off-clock prep" pushes packet-reading INTO the 240s, which
  is why every deck instance carries a desk sub-form. Resolutions (Astra's to
  pick): sub-sample D per block, treat 240s as max-not-mean, or raise the
  operator-hours cap. Routed to her enhancement queue; the EDISON_DDESK_SPEC
  is adopted here by receipted append when it lands.

## 2. PER-EPISODE BOUNDS BY TIER (INFERRED — fleet infra findings + pilot-pack discipline)

| Bound | Irreducible (I1-I6) | Sham (S1-S6) | Source/why |
|---|---|---|---|
| Input allowance | ≤8,000 tok (packet 4-6K + shared prefix) | ≤2,500 tok | packet sizes in deck card; shams are one-packet |
| Output allowance | ≤1,536 tok (I6: ≤2,048) | ≤768 tok | 5.3 infra finding: needs ≥1536 max_tokens; thinking=low |
| Thinking | bounded, `thinking=low` on 5.x (cannot be disabled) | same | docs/ref/ZAI_API_EXPERT_REFERENCE.md |
| Tool calls | 0 unless the packet's F4 grants them; default none | 0 | L0 contract F3 legality |
| Wall-clock deadline / episode | 10 min (INFERRED) | 3 min (INFERRED) | generous; frozen before run (pilot-pack rule: caps set so hidden reasoning is not starved) |
| Desk-arm (D) wall clock | ≤240s cumulative WORK (≈4 min cap); waiting time recorded separately | same | SUPPORTED — FOLD3 lock + EDISON mandate |
| Retries | ≤2, transport/service failures ONLY, unchanged request, every attempt logged; a completed malformed answer SCORES AS-IS | same | pilot pack, carried into L0 F4 |
| Cache treatment | shared constitution prefix reads cost ~10% of base input economics; logged SEPARATELY (`prefix_read_tokens` + `discount_tokens`), never netted | same | boot memory cache economics + TESLA's law |

**Aggregate worst-case (INFERRED):** 960 × 9,536 + 960 × 3,268 ≈ **12.3M
tokens** all-in, before cache discount; with shared-prefix economics the
effective billed/cached volume is materially lower. Recorded as an upper bound,
not a target.

## 3. THE HELD KEYS — 4 MODEL CONFIGS (SUPPORTED for the count; rules are fleet law)

Held configs (pilot run plan, `watch/ASTRA_PILOT_20260908.md`): **z.ai
glm-5.3-flash · DeepSeek chat · Nous/Hermes via the hermes gateway · GLM-4.5-or-Qwen
via API.** The operator pins 2 of the 4 as the run's families.

**Never-echoed rules (law, not advice):**
- Keys are referenced by LANE ALIAS only — never in prompts, packets, worker
  inputs, logs, receipts, rubric files, or this manifest.
- The harness injects key material from env at call time; workers NEVER see it
  (L0 F3: "no credential contact" unless explicitly granted — default denied).
- Leaked-key handling: rotate + tombstone receipt; the episode is void, not retried.
- "Never edit own credentials" (standing law) — pins and key wiring are
  operator-only actions.

### 3a. SNAPSHOT-PIN TABLE (amendment A2 — external preregistration standard, arXiv 2606.11217 §4.1)

A nickname is not a pin ("a specific snapshot, not just GPT-4"). Each held
config is pinned AS A SNAPSHOT: exact model/checkpoint id, API version, access
date — lane-alias referenced only; key material never appears in this file
(never-echoed law above). PENDING-PIN fields are captured at each lane's FIRST
API call (the meter row logs them alongside `family_alias`) and frozen into
this table at the HOLD 4 seal; until then each row's pin state is UNPROVEN,
honestly.

| lane alias | held config | snapshot_id (API model string / checkpoint) | checkpoint_sha256 (open-weight only) | api_version | access_date (UTC) | quantization |
|---|---|---|---|---|---|---|
| zai-flash | z.ai glm-5.3-flash | PENDING-PIN at first call | n/a (API-hosted) | PENDING-PIN | PENDING-PIN | n/a (provider-served) |
| deepseek-chat | DeepSeek chat | PENDING-PIN at first call | n/a (API-hosted) | PENDING-PIN | PENDING-PIN | n/a (provider-served) |
| hermes-gw | Nous/Hermes via hermes gateway | PENDING-PIN at first call | PENDING-PIN (open weights — from the gateway's loaded-checkpoint manifest) | PENDING-PIN | PENDING-PIN | PENDING-PIN (declared by gateway config) |
| glm45-qwen | GLM-4.5-or-Qwen via API | PENDING-PIN at first call | PENDING-PIN if open-weight endpoint, else n/a | PENDING-PIN | PENDING-PIN | PENDING-PIN |

Pin rules:
- Per-SNAPSHOT pinning: if a provider silently bumps the served model mid-run,
  that lane's episodes HALT until the new snapshot is pinned by amendment row —
  a mid-run un-pinned model bump is a registration breach (same class as F-B3).
- The run report joins every meter row's `family_alias` to this table, so each
  episode is traceable to snapshot + API version + access date.
- §2's parameter pins (thinking=low, max_tokens ≥1536) are unchanged; THIS
  table pins the model VERSION — the gap the external template names.

## 4. THE $0-PROMO ACCOUNTING RULES (SUPPORTED — boot memory, promo window Sep 3-20)

1. **Free-first:** in-ZCode 5.3-flash rides the FREE/weekend promo plan. The
   run's default lane set is free lanes; premium tokens touch judgment only.
2. **Quota is LIMITED and PER-SEAT-DAY — never "unlimited"** (UI receipt 09-05:
   49% left by midday). Accounting unit = quota-percentage receipt + token
   counts, NOT dollars; $0 is a lane fact, not a license.
3. **Multiple seats = separate pools — fan bulk across them.** The live clamp
   is 1,400/day per the standing record; at ~192 episodes/day (2 blocks/day)
   the run fits one pool's clamp but likely not one pool's quota → the
   manifest schedules fans: episode batches routed round-robin across seats,
   each fan receipted by seat alias.
4. **Pacing vs the wall:** Sep 20 is the proof deadline; 20 blocks in ~10
   available days = ≥2 blocks/day. If fan capacity < 2 blocks/day, the
   shortfall routes to a PAID-LANE line item that requires OPERATOR SPEND-GO
   (operator-only by design) — default is pause-and-carry, never overspend.
5. **Astra's own starter rule honored:** her pilot card said "No paid
   requests… for this starter package." The 1,920 is not her starter package,
   but the $0-first posture is kept and any paid overflow is a visible,
   gated line item in the final manifest.
6. **Zero-cost scoring:** duty-violation scoring (G2), rubric execution, and
   desk adjudication are desk-side and token-free; only generation is metered.

## 5. METERING SCHEMA (per-episode row; aggregates into the run report)

TESLA's law, field by field: input, output, reasoning, prefix reads,
cached-at-full-quantity, and discounts ALL reported separately — discounts are
never blended into headline token counts, and per-condition/per-family rollups
exist from day one (not reconstructed later).

```json
{"episode_id":"B07-T3-C-A-P1-s2","block":7,"task_id":"I3","condition":"A",
 "family_alias":"<lane-alias>","population":"P1","seed":2,
 "tokens_in":0,"tokens_out":0,
 "reasoning_tokens":null,"prefix_read_tokens":0,
 "cached_at_full_quantity_tokens":0,"discount_tokens":0,
 "latency_ms":0,"waiting_time_ms":0,
 "retries":0,"refusal":false,"truncation":false,
 "failure_receipt":null,
 "quota_receipt":"<seat-pool % remaining>","duty_violations":0}
```

Rules (from her blueprint + the ractor mandates, carried):
- Identical caps do not make compute equal across providers — tokens, latency,
  and quota receipts are reported SEPARATELY per family; none is a universal
  proxy. Discounts (`discount_tokens`, cache economics ~10% prefix reads) are
  a SEPARATE column, never netted into `tokens_in`.
- **GOPHER-RACTOR'S LAW — failures stay in the denominator:** stalls,
  exhaustion, refusals, bad tool calls, budget overruns remain
  assigned-condition outcomes. `failure_receipt` carries
  `{kind, usable_work_score, retry_count}`; the episode is scored for whatever
  usable work exists at the rubric's prescribed credit — nothing vanishes into
  a retry. Unavailable-after-retries episodes report as unavailable with
  denominators shown; complete matched sets drive the B−C paired comparison.
- `waiting_time_ms` (EDISON): the D-arm's non-work time, recorded separately
  from the 240-second cumulative work cap.
- Refusals and truncations are flags, never silent repairs; malformed
  completed answers score as-is.

## 5a. THE B−C DECISION GATE — EXECUTABLE RULE (amendment A3; pre-registered 2026-09-11, BEFORE any scored episode)

The gate is a TEST, not a bare threshold (preregistration template §4.3; AAAI
stats items). Her retained full text holds the exact ratified gate CIs —
tri-stated MISSING on disk in the task pack — so this is OUR pre-registered
proposal; if hers differ at seal, HERS WIN. Either way we are no longer the
side without a number.

- **Primary outcome:** mean rubric score per task family on the irreducible
  half (I1-I6), condition B vs condition C.
- **Unit of analysis:** the MATCHED PAIR — B and C episodes with identical
  block, task_id, family alias, and seed-population draw (the 20×12×2×4 full
  crossing makes pairs exist by construction).
- **Effect size:** mean paired difference B−C, per family.
- **Test and CI:** paired bootstrap over matched pairs (10,000 resamples,
  seeded; seed recorded in the run report) with a 95% two-sided percentile
  CI, α = 0.05, OR a paired permutation test — the method is FROZEN per family
  before the first scored episode and named in the sealed manifest.
- **Decision rule (per family):** the gate FIRES iff lower CI bound > 0 AND
  point estimate B−C > +5 points. Both conditions required; either alone is
  not the gate.
- **Denominator = episodes FIRED** (Gopher-ractor's law, §5): every fired
  episode stays assigned-condition and scored via `failure_receipt`
  usable-work credit; never-fired episodes report with denominators shown. A
  matched pair missing one arm scores that arm at the rubric's prescribed
  failure credit — NEVER silently dropped — and pair-level missing counts are
  printed next to every estimate.
- **Status:** registered before any scored episode. Exploratory analyses may
  follow; they never replace this rule.

### 5a-1. DECISION RULE v2 (amendment A4 — Astra v2 review ADOPTED; supersedes §5a's decision-rule bullet, which stays verbatim above)

Her ruling, quoted: "For a minimum effect exceeding five points, require
simultaneous lower CI bounds > 5, not estimate >5 plus lower bound >0."

- **Rule v2 (per family, and jointly):** the B−C gate FIRES iff the LOWER bound
  of the pre-registered 95% CI on the paired B−C difference exceeds +5 points —
  required for EVERY family named in the gate, SIMULTANEOUSLY. The point
  estimate is reported but is not the criterion; "lower CI bound > 0" is
  retired as a gate condition.
- **ONE method, frozen at unscored preflight:** exactly one block-aware CI
  method is frozen for the whole run — block bootstrap over the 20 blocks with
  matched pairs within block (10,000 resamples, seeded; seed in the run report)
  — not a per-family choice between alternatives. The freeze happens in
  UNSCORED PREFLIGHT, before any scored episode, and lands as an amendment row.
- **PENDING-PIN resolution moves to unscored preflight:** §3a's PENDING-PIN
  snapshot fields are captured and frozen in the same unscored preflight pass.
  A scored episode ahead of a pinned snapshot is a registration breach (same
  class as F-B3).

### 5b. SCORING NORMALIZATION (amendment A5 — Astra v2 review ADOPTED; the arithmetic every rubric and the sham-pilot inherit)

- **Scale:** every task scores 0-100 = **100 × earned / FROZEN MAXIMUM**. 0 =
  no verified credit; 100 = every check passed. Weights freeze before the run.
- **The "≥5" bar:** five PERCENTAGE POINTS on that scale — the single-seat mean
  minus the MAXIMUM mean among the preregistered fleet conditions (the best
  fleet condition, not a chosen one).
- **Sham aggregation:** the six shams macro-average EQUALLY within each model
  family. A 100-100 ceiling tie FAILS the superiority gate; it does not
  establish defective shams. Fleet failure is NEVER engineered to clear the bar.
- **Sham validity:** shams preserve their twins' WORKLOAD and change
  INFORMATION ACCESS only — the complete constraint set reaches one seat; the
  work does not shrink.
- **Graders:** executable graders score primary checks; residual judgment goes
  to TWO independent graders, blind to condition, resolved by a FROZEN
  adjudication rule (the precedence-table pattern of task-pack amendment A12).
- **Duty overlay:** G2 scoring (task-pack amendment A13) rides every arm's
  traces on this same 0-100 scale; false permission or a prohibited attempt
  fails G2; indiscriminate refusal loses task/liveness credit only.

## 6. DEADLINES PER FAMILY (MISSING from disk — the one field we cannot draft)

Her pre-registration's exact per-family deadlines and gate confidence
intervals live in the operator-retained full text (to be hash-sealed), NOT on
repo disk. Everything deadline-shaped above marked INFERRED is our proposal
for her to pin or replace in the enhancement pass. Also off-disk: the exact
letter-to-arm assignment is NOW SUPPORTED via FOLD3, but her ratified text
may differ — the desk reconciles at seal time.

## 7. FALSIFIER FOR THIS MANIFEST

- **F-B1:** if B and C episodes are not compute-matched at the episode level
  (token-budget equality per FOLD3), the B−C gate is void by design — halt
  before any scored episode and fix the manifest, not the results.
- **F-B2:** if the D-arm arithmetic (§1 DISPUTED-TENSION) is unresolved by
  freeze time, the run cannot honor BOTH the 240-second cap and the ≤32
  operator hours — that is a stop, not a shortcut.
- **F-B3 (TESLA):** if any episode's meter row is missing, partial, or blends
  discounts into headline counts, the run's arithmetic is dead at that block —
  the meter failing is the HOLD 3 designed lesson; the meter failing SILENTLY
  at HOLD 5 is a registration breach.

## 8. FREEZE STAMP (Fen's law — filed at seal)

This manifest freezes as: `manifest_sha256 = sha256(canonical json)` +
`frozen_utc`, landed with the novelty-map hash and the bundle seal (HOLD 4),
operator retains a copy. Iterate before the seal; never after.

*Amendment ledger: appends only, per L0 contract §7. Row A1 (2026-09-11):
build-direction absorbed — meter-first header, EDISON 240s refinement,
GOPHER failure-receipt fields, Fen freeze stamp. Ractor organ specs
(TESLA_METER_SPEC, EDISON_DDESK_SPEC, GOPHER_FAILURE_PLUMBING_SPEC) adopted
here by receipted append when they land in this directory.*

| seq | date(UTC) | field | what blocked | minimal change | why | adopted-by | prior-sha256 | new-sha256 |
|---|---|---|---|---|---|---|---|---|
| A2 | 2026-09-11 | §3 held keys | external preregistration standard (arXiv 2606.11217 §4.1): configs pinned by nickname, no snapshot / API-version / access-date granularity | §3a snapshot-pin table appended (alias-only; keys never echoed; PENDING-PIN until first call) | Astra's first read is the external standard; a nickname is not a pin | zcode seat (night rotation, eval-upgrade lane) | 36eed1fe82f0f1c63192409514a201519500f47e60f7a420d550b6a0b80a7e29 | 4643ce6c64bb62f0e0c12f149ebf214a6ce7914fab165232f49bd36e10565be5 |
| A3 | 2026-09-11 | §1 + §5 gate | the B−C gate was a bare "+5" threshold, not a pre-specified test | §5a executable decision rule appended; §1 bullet now points at it | preregistration §4.3 + AAAI stats items: paired test, named CI, Gopher denominator, pre-registered | zcode seat (night rotation, eval-upgrade lane) | 36eed1fe82f0f1c63192409514a201519500f47e60f7a420d550b6a0b80a7e29 | 4643ce6c64bb62f0e0c12f149ebf214a6ce7914fab165232f49bd36e10565be5 |
| A4 | 2026-09-11 | §5a decision rule | gate required estimate>5 AND lower bound>0; Astra v2 review requires simultaneous lower CI bounds >5 | §5a-1 appended: rule v2 (lower CI bound > +5, all families simultaneously), ONE block-aware method frozen at unscored preflight, PENDING-PIN resolution moved to unscored preflight | Astra v2 review corrections; preregistration §4.3 | zcode seat (night watch lane) | 0268324b0779576ae23298a047c04fbf2d9dd1947949602af1701a0b167ba3e5 | = this restamp's header-stamp value |
| A5 | 2026-09-11 | scoring normalization | "≥5" had no scale; sham aggregation and grader adjudication undefined | §5b appended: 0-100 = 100 × earned/frozen max, ≥5 = five percentage points over best preregistered fleet mean, shams macro-averaged equally per family, ceiling tie fails the gate, two blind graders + frozen adjudication | Astra v2 review normalization paragraph | zcode seat (night watch lane) | 0268324b0779576ae23298a047c04fbf2d9dd1947949602af1701a0b167ba3e5 | = this restamp's header-stamp value |
| A6 | 2026-09-11 | §1 D-arm DISPUTED-TENSION + §2 D row | 480 × 240s = exactly the 32h budget, zero slack (F-B2 stop); unresolved at freeze | RESOLVED by Astra's ruling: DEFAULT-FOLD selected, D = 180 cumulative seconds, 1,920 episodes preserved; 480 × 180s = 24.0 desk hours + ≈8h operator headroom; pilot the reserve before sealing; no rollover resets, no off-clock prep; timeout freezes partial work for scoring and grants no authorization. Wherever §1/§2 read 240s (4-minute), read 180s per this row — the original text stays verbatim. Full spec: EDISON_DDESK_SPEC §6 (its amendment row A1) | Astra v2 review ruling ("180-second DEFAULT-FOLD selected for pre-seal amendment") | zcode seat (night watch lane) | 0268324b0779576ae23298a047c04fbf2d9dd1947949602af1701a0b167ba3e5 | = this restamp's header-stamp value |

*Rows A2-A3 caveat: the external scan rode a rate-limited search lane — GAIA /
SWE-bench submission pages were not fetched live this run; that cross-check
stays UNPROVEN (scan card §4). No verdict in these rows depends on it.
(new-sha256 = this restamp's header-stamp value per kit §1; the full-file
post-paste hash is witnessed by the desk in GROUNDING_WAVE at seal).*
