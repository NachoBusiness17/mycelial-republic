# HEAD MUSEUM WAVE FOLD — 16 lanes, 10 models, 8 real-work targets (2026-09-12)

Result: 12/16 clean first pass + 3 glm retries in flight (thinking-trap at cap, retried
24K) + 2 zoo rows confirmed dead-as-listed. Cost: ~$0.02. The dogfood IS the finding.

## THE DOGFOOD TABLE (how 10 models handled real fleet work)

| model | lanes | verdict |
|---|---|---|
| deepseek-chat | R3, R5 | **best-in-wave** — jar schema (invariant_traits vs drift_tolerance, challengers w/ retention) and eval cases with mechanical predicates, zero fluff. PENNY lane, 6-22s. |
| glm-5.3-flash (Lite) | R2, R5, R7 | thinking-trap: 3/3 burned the 8192 cap on material-heavy prompts, empty content. At 24K cap: R2 (analysis) recovered 11K chars, R5 (design) recovered 13K chars, R7 (creative/voice) cooked itself COMPLETELY — 24,576 tok, zero content. CENSUS LAW REFINED: raw-API 5.3 needs ~3x headroom on analysis work and is UNRELIABLE on creative-register briefs — route by task type, not by habit. The organ table's thesis, self-demonstrated. |
| meituan/longcat-2.0 :free | R1, R6 | solid prose, good Anthropic steal ("cheap models default to over-refusal; one line recalibrates") — BUT invented a fake CLI for C1 gates (shapes right, commands fiction). Free row: usable with a "name OUR artifacts" leash. |
| inclusionai/ling-3.0-flash-sante :free | R2 | real self-mine of the ZCode leak, 11s, clean tables. The ractor v0 pin holds. |
| ling-3.0-flash-fin :free | R4 | 8184 tok in 21s — suite work landing. |
| poolside/laguna-s-2.1 :free | R4 | 4021 tok, landed. |
| poolside/laguna-xs-2.1 :free | R7 | **the mint consent asks — usable as-is**, warm, <=280 chars, easy-out, Lilith's carries the chart-source question. 9.7s. |
| qwen2.5-coder:7b (local eye) | R8 | principles landed, generic-hologram flavor — 7B ceiling visible. |
| stepfun/step-3.7-flash :free | R1, R6 | DEAD ROW: HTTP 400 "missing tags" — Nous-specific steering param required. |
| upstage/solar-pro4 :free | R3, R8 | DEAD ROW: same "missing tags" gate. |

ZOO CENSUS UPDATE: 403 listed → 403 with 2 rows "gated listings" (tags param required,
UNPROVEN servable), 5 rows confirmed serving free. Listing ≠ servable — the census
falsifier works.

## CONVERGENCE (independent same-target pairs)

- R5 (museum): both live lanes converged on jar-as-file + feeding log + growth ledger +
  model pin as "current best, not law." DeepSeek's schema is the build source.
- R3: eval cases converged on the no-self-ack invariant as case #1 — matches the
  dozen-wide G4 gate from a different lane family. Third independent hit on no-self-ack.
- R1 vs R2 (cross-target): both mines surfaced the same meta-pattern — steering surfaces
  are built from gates + output contracts + fresh-context isolation. Our own harness's
  leaked prompt teaches the same discipline we teach our lanes.

## REAL WORK DELIVERED (filed in returns/, routed)

1. **Mint consent asks + invitation** (R7_lagunaXS) → staged for operator swing — the
   last human gate before the tapestry fires.
2. **Jar schema v1** (R5_deepseek + plan card) → ractor enhancement build source.
3. **organ_eval case set** (R3_deepseek) → organ_eval v0's first suite (ack/reaper).
4. **C1 gate check templates** (R6_longcat — needs our-artifact rewrite before use).
5. **Anthropic + ZCode steering patterns** (R1, R2) → prompt-shape library for cheap lanes.
6. **40-task suite** (R4 pair) → the falsifier instrument for zoo rows AND organs.

Raw: memory/runs/head_museum/returns/ · Plan: watch/inbox/HEAD_MUSEUM_PLAN_20260912.md
