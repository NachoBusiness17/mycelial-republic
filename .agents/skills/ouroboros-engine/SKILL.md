---
name: ouroboros-engine
description: Drive the 3x100 interlocking Ouroboros wave engine (Work sensing, First-Order Logic verification, and Depth+1 self-feeding) across estate queues with zero em-dashes and strict 0.00 first-person voice. Use when the user requests a 100-cycle or 3x100 ouroboros wave, or when estate queues need rapid, high-concurrency drainage and self-feeding.
---

# Ouroboros Engine Skill

The Ouroboros Engine provides a self-sustaining tripartite research loop that drives the estate queues without human intervention. The loop consumes existing estate tasks, verifies claims against repository facts, and self-feeds successor hypotheses.

## Architecture: The Three Interlocking Rings

The engine rotates through three continuous phases:

1. **Ring 1: Work Ladder (100 Cycles)**
   - Drains 100 queued items from `state/fuel/stealth_work_queue.jsonl`.
   - Synthesizes technical research reports with First-Order Logic predicates.
   - Banks markdown answers in `watch/inbox/burn_reset_20260927/work/<id>_sovereign.md`.
   - Logs mined findings into `watch/inbox/STEALTH_MINED_FINDINGS.jsonl`.
   - Stamps queue rows with `status: sensed`.

2. **Ring 2: Socratic Verification Gate (100 Cycles)**
   - Audits banked answers using `tools/judge_v3_fol.py` and `tools/quasilocal_boundary_gate.py`.
   - Evaluates factual atoms against `canon/same_book/false_premise_bank.json`.
   - Enforces zero unicode em-dashes and 0.00 / 1k first-person singular pronouns.
   - Writes verification receipts to `watch/inbox/burn_reset_20260927/work/<id>_verify.md`.
   - Stamps queue rows with `verdict: DONE`, writing `done_ts` and draining the work queue.

3. **Ring 3: Self-Feed & Regeneration (100 Cycles)**
   - Extracts stealable design patterns from verified findings.
   - Synthesizes 100 depth+1 successor inquiry briefs with testable hypotheses.
   - Assigns unique `m%03d` identifiers and appends rows to `state/fuel/stealth_work_queue.jsonl`.
   - Synthesizes and queues 10 concrete engineering build tasks into `state/fuel/stealth_selfimp_queue.jsonl`.
   - Resets `selffeed_fail_streak` to 0 in `state/fuel/stealth_work_state.json`.
   - Logs cycle telemetry into `state/fuel/stealth_driver.jsonl`.

## Invocation

Execute the engine directly via standard-library Python:

```bash
python3 tools/ouroboros_engine.py 100
```

For dry-run verification:

```bash
python3 tools/ouroboros_engine.py 100 --dry
```

## Guardrails & Laws

- **Pure Standard Library**: Zero external package dependencies.
- **Headless & Single-Writer**: Background tasks never run interactive shells or direct git commits.
- **Strict Compliance**: All outputs must pass `quasilocal_boundary_gate.py` with 0 banned tokens.
