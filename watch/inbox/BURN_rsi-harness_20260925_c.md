# BURN rsi-harness _c — 2026-09-25

## Verdict
steal

## Evidence
- SIX_DROPS s4 (muratcan): "Accept only if every scenario passes in both runtimes." Loop: "simulate → judge & grade → cluster failures → propose (one fix + one new scenario per PR) → agent review → human gate at merge."
- RRSI carried from BURN _b's primary fetches: "If none is admissible, the incumbent is retained." Gate is algorithmic only: noise floor, cost cap (ΔC ≤ β0 + β1ΔS), leakage critic, w_s = 0.
- memory/law/registry.json read 2026-09-25: LAW-11 is now "credits_over_failure" (T1, operator chat, registered 2026-09-25T20:28:17). Both prior burns proposed "LAW-11 amendment_gate"; that slot is taken. Next free ID is LAW-12. Row format learned: registered_ts, id, name, tier, source, trigger, condition, action, guardrail, optional semantics/grounding/last_enforced_ts.
- One web search (2026-09-25): top hit "AI Agent Self-Modification Exposes New Risks" (cypro.co.uk, Sep 17 2026), snippet claims "a lack of a separate human approval gate around self-modification creates governance gaps." Article URL returned HTTP 404 on fetch; homepage fetched, carries no such content. Filed owed, unsynthesized. Signal only: the field is converging on named approval gates; zero checklist substance obtained from the web this pass.

## Steal or Vacuous
Steal: the amendment-gate checklist, filed as LAW-12 (LAW-11 collision noted above). Per amendment:
1. Trace provenance: scenario cards exist and each cites a real failing trace by pointer (receipt path or ledger row id). No trace, no card.
2. Non-compensatory admission: every mandatory axis needs a nonzero pass, any zero fails regardless of the others. Axes: (a) trace_provenance, (b) dual_runtime_regression, (c) eval_independence (not graded only on a set the amendment itself touched or minted), (d) cost_honesty (rescue spend logged per LAW-11), (e) rollback_safety (incumbent restorable byte-for-byte).
3. Runtime: dual-runtime pass recorded, or explicitly single-runtime with a written rollback note naming its trigger.
4. Incumbent default: any failed gate leaves registry and harness exactly as was; the failed proposal is filed, never half-landed.
5. Human-gate regression criterion checked at promote --apply: every versioned scenario passes on both runtimes AND the new scenario minted from this fix's own failing trace passes on both, graded on recorded runtime events plus deterministic graders, not the proposing agent's self-report.

Example row (draft, not filed; registry untouched):

```json
"LAW-12": {
  "registered_ts": "<set at promote time>",
  "id": "LAW-12",
  "name": "amendment_gate",
  "tier": "T0",
  "source": "SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md s4 survivors rule + RRSI arXiv 2609.24972 gateless loop (via BURN _a/_b) + this checklist",
  "trigger": "amendment_to_law_registry_or_harness",
  "condition": "all_five_gate_axes_nonzero_and_dual_runtime_pass_recorded",
  "action": "land_via_promote_apply_human_gate",
  "guardrail": "non_compensatory_any_zero_axis_fails; incumbent_stays_default_on_fail; single_runtime_needs_rollback_note"
}
```

## Falsifier
Pre-registered: LAW-12 dies if, within 14 days of registration, any promote --apply lands with fewer than five nonzero axis records, or any rejected amendment leaves a diff in memory/law/registry.json or the harness default path.

## Bibliography
1. watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md s4, read 2026-09-25
2. memory/law/registry.json, read 2026-09-25
3. watch/inbox/BURN_rsi-harness_20260925.md, read 2026-09-25
4. watch/inbox/BURN_rsi-harness_20260925_b.md, read 2026-09-25 (RRSI quotes carried from its primary fetches)
5. Web search, query "governance of self-modifying AI agents amendment gate policy change runtime self-update safety September 2026", 2026-09-25
6. https://cypro.co.uk homepage, fetched 2026-09-25; its self-modification article 404'd, owed
