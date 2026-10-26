# BURN rsi-harness — 2026-09-25

## Verdict
steal

## Evidence
- muratcan card (SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md section 4): "agents write evals (failing call traces → versioned scenario cards: persona/goal/expected tools/end state)" and "loop = simulate → judge & grade → cluster failures → propose (one fix + one new scenario per PR) → agent review → human gate at merge" and "Accept only if every scenario passes in both runtimes."
- memory/law/registry.json: LAW-4 ghost_self_improves (trigger ghost_cycle, action catalog_as_training, guardrail read_only); LAW-7/8/9 Ostrom set (graduated sanctions "narrow_only_no_grant", collective choice "consent_first_no_throne"). Enforced timestamps 2026-09-25 on LAW-3/4/7/8/9/10; LAW-1 and LAW-6 carry no last_enforced_ts.
- RRSI (Google Research, arXiv 2609.24972, 21 Sep 2026, via emergentmind): harness is the "optimization variable" with backbone frozen; leakage critic rejects diffs that "explicitly encode task names, entity names, task-specific values, answers"; candidates must clear a "noise-adjusted floor"; in-band candidates "must instead reduce cost or introduce previously unused structural mechanisms"; "If no candidate is admissible, the incumbent remains unchanged." Reusing a fixed evolve set "creates adaptive overfitting risk." The method has no human gate.
- Owed: preprints.org "Harness-Aware Evaluation of LLM Agents" returned HTTP 403, unfetched, unsynthesized.

## Steal or Vacuous
Steal, three items.
1. Cluster-failures-by-runtime as a standing organ between judge and propose. The drop already names it; registry laws act on runtime health but nothing clusters amendment failures by window. Register it as a lane, not a one-off hand taxonomy.
2. The registry registers laws (trigger/condition/action/guardrail) but holds no acceptance criterion for amendments to the law set itself. Muratcan's survivors rule is the missing shape: scenario cards minted from real failing traces, accept only if every scenario passes both runtimes, harness stays as was on a failed gate. RRSI shows why the criterion matters: the automated frontier runs gateless and compensates with leakage critics plus noise floors, so a human gate without a regression criterion is just a signature. Draft as LAW-11 amendment_gate wired to promote --apply.
3. Per-PR new scenario card is the anti adaptive-overfitting move. RRSI replays a fixed evolve set and pays in OOD risk; muratcan grows the set one scenario per fix. The fleet's evals-from-traces lane must mint, not replay.
Registry keeps what muratcan lacks: machine-readable runtime law with enforcement timestamps and an Ostrom governance loop (sanctions, consent, boundaries); muratcan has a merge gate, not governance.

## Falsifier
Pre-registered: LAW-11 amendment_gate passes only if, within 14 days of registration, scenario cards are filed from real failing traces and at least one promote --apply records a dual-runtime pass. The lane is falsified (LAW-11 dies) if zero cards are filed in that window, or any amendment lands without a dual-runtime pass record.

## Bibliography
1. watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md, section 4, repo, 2026-09-25
2. memory/law/registry.json, repo, read 2026-09-25
3. https://www.emergentmind.com/papers/2609.24972 (RRSI: Improving Agent Harness Evolution, Google Research, 21 Sep 2026), fetched 2026-09-25
4. https://www.emergentmind.com (homepage, source of the RRSI pointer), fetched 2026-09-25
