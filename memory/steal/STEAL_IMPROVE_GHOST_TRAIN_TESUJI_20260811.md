# STEAL — IMPROVE !steal !ghost !training !tesuji (measure + stateless + self-heal + falsify) (2026-08-11)

Operator: "how can we improve the !steal !ghost !training !tesuji features?" -> "steal".
Thesis: turn the four "features" into stateless, MEASURED, self-correcting loop steps. Cross-cutting
invariant: every feature becomes (read real state -> pure transform -> fold/verify) and is FALSIFIABLE.

## SELF-STEAL (what we already own, reuse it)
- Self-heal ghost daemon: mag/sentinel.py (always-on watcher), mag/process_supervisor.py
  (LOOP_DEFS crashLoopBackOff), mag/guard_registry.py (single_controller). Wire sentinel to RESTART the
  crashed ghost cycle loop, not just report. (ghost cycle crashed 2026-08-10T22:42 — live gap.)
- Measured tesuji: mag/dogfood_audit.py (real probe results), mag/cost_enforcer.py (real billing),
  logs/failure_kb.jsonl (FKB signatures w/ counts), mag/orchestrator task died-rates. The $147 cache
  "tesuji" was WRONG (billing ~$31.15 / ~98% hit) -> measure-before-optimize is the standing lesson.
- Verified training: mag/training_rightsize.py + memory/pile/training_rows.jsonl + the auto-capture
  (no !train). Turn each captured correction into a checkable change, not just a note.
- Stateless steal: mag/steal_pack.py + mag/stateless_research.py + mag/verkle_knot.py (content-addressed
  fold, amend-in-place stable sessions). Already the substrate for the embedded-steal design.

## EXTERNAL-STEAL (adapt the contract, not the DNA)
- Self-healing: Kubernetes liveness/readiness probe + restartPolicy/crashLoopBackOff (we stole it once —
  apply it to GHOST itself, not just mag workloads). Supervisor pattern (systemd/launchd auto-restart).
- Measured tesuji: SRE error-budget / SLO alerting — only act on MEASURED budget burn, never vibes.
  Impact-effort scoring on real data (billing, dogfood, died-rates); surface ONE highest-leverage move.
- Verified training: regression/golden-test harness — every training capture becomes a deterministic
  regression check (CI gate) so the cause cannot silently recur. RLHF-style: reward on REAL outcomes.
- Stateless steal: Git/event-store CAS dedupe + event sourcing — adapt invariant, dedupe by content
  address, replayable.

## ADAPTATION (the concrete roadmap, folded)
1. steal_step(source, signal)->invariant_knot pure function; wire into autorun fill/drain (stateless
   embedded steal). Adoption check: every steal doc links to its consuming path.
2. ghost: sentinel restarts the cycle loop; nudge/route explainable; inbox watch loop always-on.
3. training: capture -> regression check (prove the cause can't recur); dedupe repeated corrections.
4. tesuji: detector scores ONE highest-leverage move on REAL data (billing/dogfood/died-rates);
   falsify before spending (cheap A/B or oracle).

## Falsifiability guard (honesty)
- Any tesuji/steal that would spend or grow complexity must cite the MEASURED number it acts on.
  Never chase an unverified number (cache-router lesson). Fold as case-law so it compounds.
