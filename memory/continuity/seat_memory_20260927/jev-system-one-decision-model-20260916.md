---
name: jev-system-one-decision-model-20260916
description: Jev (TypeSafe AI) — non-autoregressive "System One" decision model;
  schema-native parallel per-field scoring with probabilities; tri-state verdict
  + three fleet steals (tri-state forms map 1:1, capture-cap fix, weighted fold)
metadata:
  node_type: memory
  type: reference
  originSessionId: sess_f8f2909b-0ac5-4763-abba-fbd8ba748f54
---

2026-09-16, operator dropped the "How Jev works" explainer (filed durably at
watch/inbox/ore_20260916/JEV_HOW_WORKS_20260916.jpg; LINKS rows 173–174).

**What it is:** TypeSafe AI's decision model (announced by Diogo Almeida). NOT autoregressive:
it only emits schema-constrained structured output. Prefill context+schema once into a KV
cache, then score EVERY field in parallel — one forward pass per field, softmax restricted to
that field's legal values, calibrated probabilities free (HIGH p=0.99, true p=1.00). No runtime
masking layer needed. "Uncertainty-native": stops where uncertainty enters. Hosted API,
early-access waitlist, not open weights.

**Tri-state:** mechanism REAL (constrained decoding is established engineering; HN skeptics
right that LLMs+structured outputs overlap); "new class of model" framing OVERSOLD; the
uncertainty-native design is the genuinely novel, unproven-at-scale part.

**Three fleet steals:** (1) the Astra tri-state forms map 1:1 — enum verdicts
(Supported/Disputed/Unproven) + confidence per claim, per field; a Jev-class API replaces
hand-rolled confidence calibration with the decoder's own. (2) The capture-cap fix — ask for
per-field small outputs instead of 4,000-char prose; prefill-once = the context tax paid once
(deliberate-ask literalized). (3) Competence-weighted fold — p=0.99 vs p=0.55 verdicts get
different weights in the salon desk (the salon-50 witnesses' own proposal).

Related: [[provider-chat-capture-cap]], [[astra-repair-lane-20260915]],
[[salon-50-and-basecamp-20260916]].

**UPDATE 2026-09-18 (daily scout):** Jev resurfaced via Latent Space —
claimed >100x faster and >200x cheaper than small frontier LLMs on
classification/routing/scoring. Operational action filed with the scout row:
benchmark Jev against lane_runner gate_drop heuristics on 100 real inbox
drops; if verdicts hold, wire it as the routing organ behind the switchboard
(the tri-state-forms 1:1 steal becomes a live integration, not just a note).
