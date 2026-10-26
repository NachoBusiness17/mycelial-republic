---
name: max-concurrency-law-20260926
description: OPERATOR LAW 9/26 — maintain max concurrency usefully from now on: 5 gated workflows x 10 children ran clean (50-wide), first rate limit = HOLD not cut, dogfood tools every wave, fold a self-improvement per wave, overflow to free lanes (offpeak + Hermes LAW-11), seat token-maxed on useful work
metadata:
  type: feedback
---

2026-09-26 operator law after watching the 50-wide game-dig shape run: "we now know what max concurrency looks like. this is what i want to maintain from now on usefully. dogfooding our tools and always self improving. burning our free lanes when we hit max and just keeping the window on flash 5.3 token maxed on useful work."

**Why:** the measured envelope superseded the old 3-cap conservatism: 5 concurrent gated workflows at max_concurrency 10 each (50 workflow children) plus hourly cron plus offpeak ran clean for hours; first rate-limit contact at that shape was a hold signal (children retry internally, nothing lost), not a width cut.

**How to apply:** every window keeps lanes at max concurrency on demanded work; dogfood fleet tools every wave (workflow gate, drift, graders, checkers, probes); fold one self-improvement per wave into the manifest; on account cap, overflow to free lanes (offpeak queue, Hermes/Nous credits per LAW-11 — the $180 dual-burn driver pattern: watch/inbox/hermes_dual_burn_20260926.py); keep the seat token-maxed on useful work, never idle-waiting. Receipt: watch/inbox/ENVELOPE_50W_HIT_20260926.md; law line in AGENTS.md next to the fan-out width law. First subject: the five game-dig veins (dwfrun ccae8926/b176df98/04a2c303/25f23d23/0b24d2b1). Related: [[burn-program-24x7-20260925]], [[workflow-gate-law-20260925]], [[law-11-credits-over-failure]].
