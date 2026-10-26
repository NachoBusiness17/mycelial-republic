---
name: law-11-credits-over-failure
description: Operator granted standing permission (9/25) to burn Hermes/Nous
  paid credits instead of letting demanded work fail; registered as LAW-11
metadata:
  node_type: memory
  type: feedback
  originSessionId: sess_71c96bdc-4107-40e1-96f8-7211934ac587
---

Operator, 2026-09-25, during boot-lane planning: "you have my permission to burn hermes credits instead of failing." Registered in the estate as LAW-11 `credits_over_failure` in memory/law/registry.json (canon 87b8cf1750883595).

**Why:** Provider churn, 429 bursts, and dead free lanes kept killing demanded work mid-flight; the operator prefers spending the armed Hermes credits ($220) and the wired Nous key lanes over watching lanes die. Failure is the more expensive outcome.

**How to apply:** When a lane on demanded, in-flight work hits a failure a paid lane can absorb (rate limit, dead model, churned endpoint), escalate to Hermes/Nous and complete the work; log the rescue cost to provider usage. The boundary stands: this rescues work already asked for. It does not authorize buying answers to skip local/judgment work ([[hermes-100-spend-plan-20260917]] "buy meters not answers" still governs what Hermes is FOR). Related: [[lite-free-window-schedule]], [[sacred-cow-audit-sep20-20260918]].

**ARMED same night (09-25 boot lane):** nous added to configs/providers.yaml (openai_compat, base inference-api.nousresearch.com/v1, dual-key chain HERMES_API_KEY_1/2, models z-ai/glm-5.3-prime + qwen3.8-max-prime + fireworks/ember-1 — the 09-24 wiring had stopped at the free_tier registry, chat_provider still returned "unknown provider nous" until the yaml entry existed). mag/fuel_feed.py gained the last-resort rescue tier in _free_channel: free lanes → deepseek-burst → nous glm-5.3-prime max_tokens 4000 (thinking-burn gotcha: undersized caps return empty content), lane tag "nous-rescue" with law11_rescue flag, metered via _profile_record. Live armed-check returned "armed". Config seal re-registered by name (47 files) with the LAW-11 note. Rescue order is by design: cheap first, credits last.
