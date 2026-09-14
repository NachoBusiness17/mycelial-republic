# RANKING LAW — do 8 outrank 1? (octant 2026-08-31)

## 1. Verdict by tier

- **T0: No.** 8 never beat 1; they only spread it. Mechanical work has one right answer that doesn't improve by vote — 8 arms just multiply cost. Receipt: moiche rightsizing law ("T0 → all-local ollama, never pay a remote for scut"). Calibration: receipted.
- **T1: Yes.** 8 voting arms beat 1 arm on classification/verify. Receipts: socratic_relay A/B/C/D — B must name A's error, D exists as kill-shot because solo answers miss; our relay is built on that observed failure. MoA prior (Wang et al. 2024, arXiv:2406.04692, Meta): aggregated weak open-source agents beat GPT-4-single on AlpacaEval 2.0. Mechanism is error decorrelation, not headcount. Calibration: high-confidence.
- **T2: No — collapse.** Verdict/arbitration/merge → ≤3 arms + 1 judge, dissent preserved. Receipt: moiche 32×32 rung + rightsizing law ("consensus exists to capture dissent, not to add headcount"). Calibration: receipted.

## 2. Monarch pattern (1 driver + 32 deepseek gophers)

Beats the council on **sequential depth with one coherent context**: multi-step deploys, refactor chains — any task where step 3 depends on what step 2 revealed. 32 shallow lanes can't hold a narrative; each re-earns context it can't share. The driver spends one unbroken world-model (RIB-fed: 900-tok spine ≈ 7× session multiplier, freescale §2); gophers do T0 deref/fetch/scut at $0 and hand back receipts. Monarch loses when sub-judgments are independent and parallelizable — then council breadth wins.

## 3. Council pattern (grok+kimi+glm+qwen+gemma+deepseek as T2 judges)

Questions deserving a council: **arbitration between conflicting verdicts, kill-criteria, doctrine changes, and the 8→16→32 growth gates.** Receipts: Five Tests must pass before 32×32 (CODEX merge); freescale growth rule needs ≥2 independent votes per vertex before 16. A council is for decisions expensive to *reverse*, not expensive to *compute*. Calibration: reasoned — design matches our gate law; no council outcome receipts yet.

## 4. THE RANKING LAW (three sentences)

1. Arms rank below a single capable arm at T0 and T2, and outrank it at T1, where independent votes decorrelate error.
2. The crossover is **error independence + cheap verification**: if a task decomposes into independently checkable sub-judgments, N weak arms + judge beat 1 strong arm (MoA 2024); if errors are correlated or the task needs one unbroken context, 1 strong arm + verifier wins.
3. Assign by tier, not ambition: T0 = 1 spread wide, T1 = 8 votes + 1 cache judge, T2 = ≤3 arms + 1 judge; sequential depth gets a monarch with gophers, irreversible calls get a council.

## Self-attack

Weakest claim: "8 beat 1 at T1" inherits MoA's benchmark condition — open-ended drafts. On a single binary call with one unambiguous answer, a strong arm can match the vote at 1/8 the tokens. The law should read "8 beat 1 where answers disagree," not "always."

## GOPHERS

- GOPHER: verify MoA 2024 citation (AlpacaEval 2.0, weak-agents-beat-GPT-4-single) | pointer: arXiv:2406.04692 | output: /board/octant_20260831/rows/ranking-g1.row.md
- GOPHER: did socratic relay B/D actually catch a solo-arm error in the demo? | pointer: /board/socratic_relay_*.md + /room outcomes | output: rows/ranking-g2.row.md
