---
name: bo-cube-selector-20260916
description: Run-ready Bayesian Optimization config for cube stage-2 dose ladder
  — twin-differenced objective, EI, multi-fidelity proxy, config hashed into a
  registration row before first dose
metadata:
  node_type: memory
  type: project
  originSessionId: sess_f8f2909b-0ac5-4763-abba-fbd8ba748f54
---

2026-09-16, N3 lane (receipt: watch/inbox/moonshot_20260916/receipts/N3_BO_FOR_CUBE.md) turned the Bayesian Optimization primer the operator dropped (probnstat thread) into a run-ready experiment selector for cube stage-2.

**Config (CUBE-BO v1):** f(x) = z-scored evoked response of live block minus concurrent dead twin, over C17's stage-2 features. x = 6-d GP input (λ 400–740 nm, PPFD 20–400, field 0–10 V/cm, pulse duty 0–0.4 as dose dims; moisture/salt as context covariates), d_eff = 4, model fits REALIZED doses never setpoints. Kernel Matérn 5/2 + ARD. Acquisition: EI with ξ = 0.01·range (over GP-UCB — Bull 2011 regret guarantees with data-estimated hyperparameters vs UCB's sub-Gaussian/RKHS assumptions a growing block can't honor). Prior: 5-point maximin LHS. Cap: 25 expensive trials (~14 wk at 3-cup batch arms) targeting a top-ε basin.

**Multi-fidelity:** 1-day electrical proxy co-kriged against the 14-day read (Kennedy-O'Hagan / Forrester); self-test demotes the proxy to veto-only if ρ̂ < 0.7 from the 5 dual-read anchors. Non-stationarity: sliding window W=15, twin-differencing, 2σ drift re-anchor trigger.

**Integration law:** the BO config itself is hashed into a kind:"registration" row before the first BO-selected dose — the optimizer operates inside C17's registration discipline, not beside it. Laptop = planner; ESP32+ADS1115 = actuator-logger; $0 added to C17's BOM.

All 12 citations byte-verified via arXiv API/Crossref. Related: [[design-myco-memory-20260916]], conducted block K12 spec.
