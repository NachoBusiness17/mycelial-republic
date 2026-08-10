# AUDIT + SOCRATIC LOOP — STEAL (2026-08-09)

Steal research for the "first dogfood full-blast code audit + socratic proof-first loop."
Both steals done (standing directive): SELF-STEAL (our own machinery) + EXTERNAL STEAL (steal_protocol forest).

## SELF-STEAL — what we already have (don't rebuild)
- `audit.py` is the ROUTER LOG + CURRENT.md sync — NOT a code audit. Do not confuse.
- `mag/gap_analysis.py` — deterministic "where we're NOT using our systems / pretending": CADENCE gaps (MAG_*_EVERY defined but trail stale), MODULE gaps (mag/*.py defined but never imported), PRETENDING (defined but not enforced). CLI `python -m mag.gap_analysis`; wired MAG_GAP_EVERY.
- `mag/scrum.py` — proof-first Socratic sprint loop + backlog (memory/scrum/backlog.json, items S1-S6+): advance() runs item's LOW-COST proof → verify → fold; escalate only on failure; grok only frontier.
- `mag/verkle_audit.py`, `mag/ponytail_audit.py`, `mag/loop_audit.py`, `mag/build_audit.py`, `mag/caveman_audit.py` — audit modules.
- `mag/framework_map.compile_report` — seam checks (import/compile/manifest) over the framework map.
- `mag/doctor` — health + system-tracking check (13 systems importable + store on disk + non-empty).
- `mag/socratic.py` — prompt workshop (not codebase socratic). `mag/socratic_tree.py` — query verkle tree before asking operator.

## EXTERNAL STEAL — top mechanisms to adapt (source: mine/raw/steal_protocol, mostly ollama-agent-harness + bmas + conductor)
1. **bmas tiered-cadence health loop** (`arvarik/bmas/daemon/src/monitoring/health_loop.py`) — cadence scales with check cost: cheap probe high-frequency, expensive deep check low-frequency, typed pub/sub events. ADAPT: audit has a cheap liveness tier (governor ticking, DB reachable) + slow deep tier (compile/import/seam walk).
2. **harness buildGate / doneStateVerifier** (`.../src/core/buildGate.ts:90-200`, `doneStateVerifier.ts:64-130`) — per module: `py_compile` → `import <name>` smoke → `pytest`, cheapest-first, STOP AT FIRST FAILURE; typed `pass|fail|warn|skip`; **timeout→warn (never fail)**; run only changed files on fast tier. THE canonical audit walk.
3. **harness jobSafety audit + curator staleness** (`.../src/automation/jobSafety.ts:47-78`, `curator/curator.ts`) — classify every capability as proven-active vs dormant-never-invoked against a usage ledger, with a reason + counts; gate auto-disable behind caps + kill switch. ADAPT: cross-ref capability registry against invocation ledger → dormant/wired-vs-unwired.
4. **harness verification panel** (`.../src/verification/panel.ts:60-130`) — weighted per-axis signals; **lowest axis is the honest headline** (never average 28 with 87 into 58); **signals abstain rather than fabricate**; throwing signal abstains. ADAPT: health score = weighted signals per axis, headline = lowest, abstain not fake.
5. **harness surgical critic** (`.../src/verification/critic.ts:20-90`) — rank failing signals by weight×(target−score), fix top-N only, list passing as "do-not-touch". ADAPT: after failed audit, repair top-N only, preserve passing.
6. **harness goldenTraces** (`.../src/eval/goldenTraces.ts`) — capture golden baseline (expectedOutput/tools/files) of a fix, diff future runs by weighted similarity, classify drift. ADAPT: every fix persists a golden signature; later runs diff → regression hardened.
7. **harness readinessGate ladder** (`.../src/core/readinessGate.ts:50-170`) — Execution Readiness Score ≥0.80 execute / 0.60-0.79 dry-run-verify / <0.60 escalate-to-model. Cheap-first ladder.
8. **harness continuation law** (`.../src/core/continuation.ts:76-131`) — hard errors never auto-continue; meta-budget caps retries so a sick loop can't spin. ADAPT: bound the audit (no unbounded self-escalation).
9. **harness promotionGate** (`.../src/learning/promotionGate.ts:180-250`) — a learned fix graduates only after N clean eval runs on a frozen dataset + zero safety violations (safety = multiplicative gate). ADAPT: promote learned patterns only under evidence + safety.
10. **harness autonomyPrompt drift-gate** (`.../src/learning/autonomyPrompt.ts:50-95`) — reflective self-modification applies only under a hash-validated approval marker, else revert to baseline on drift.
11. **conductor validator** (`microsoft/conductor/src/conductor/engine/validator.py`) — second-voice grader with forced output schema; **fail-open** so a flaky grader never blocks a valid module.
12. **conductor dialog_evaluator** (`.../dialog_evaluator.py`) — ask the operator only after a cheap gate fails, ONE concrete question with full context (matches our routing doctrine: interrupt only for a hard blocker, one line).
13. **operator-input-contracts** (our prior art `memory/steal/operator-input-contracts.md`) — approval gate times out → proceeds autonomously; loop never blocks on operator.

## SYNTHESIS — the combined cheap restful automated audit+socratic loop
1. Audit = a CADENCE job, two tiers: cheap liveness high-freq, deep compile/import/seam low-freq (bmas).
2. Deep tier = per-module `py_compile → import smoke → pytest`, stop-first, timeout→warn, typed pass/fail/warn/skip (buildGate/doneStateVerifier).
3. Score through the PANEL: weighted per-axis, lowest axis = headline, abstain not fake (panel).
4. Cross-ref usage ledger → dormant/wired-vs-unwired (jobSafety/curator + our gap_analysis).
5. Feed failures into a SURGICAL critic: top-N only, preserve passing (critic).
6. Proof ladder: deterministic cheap → dry-run verify → escalate only on low readiness (readinessGate).
7. Every fix = a regression GOLDEN (goldenTraces); promote only under evidence+safety (promotionGate); bound retries (continuation); ask operator only on a gated hard blocker, one question, timeout→autonomous (operator-input-contracts).
8. Fold each fix/breakthrough through ghost → testing-improvement + puppeteering lessons (mag.breakthrough_loop).

Net: prove on the cheapest tier, abstain rather than fabricate, surface the honest lowest signal, surgically fix top-N, turn each fix into a regression golden, promote only under evidence, never block on the operator, bounded self-healing.
