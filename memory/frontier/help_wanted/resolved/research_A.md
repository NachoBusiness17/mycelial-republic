# Resolved: stack row "research A" - PRUNE executed

- Date: 2026-09-26. Executor: gopher t13a (gala afterparty, HELP_WANTED brief 1).
- Verdict: PRUNE. The row was a smoke-test placeholder, not a research question. No rebind target exists; a BIND would have been fabricated.

## Provenance (why it is a placeholder)

- Pipe record `memory/runs/gpipes/p8bc0180ab9.json`: created 2026-08-09T05:13:14Z, goals `["research A","research B"]`, task_ids `["t-test","t-test"]` (literally a test id, duplicated), tags empty, provider deepseek, status "running". Both live entries show status "unknown" with exit_code null. 48 days stale with zero output: this is the smoke artifact that minted the label, not functionality.
- Stack row (pre-prune bytes, verified 2026-09-26): `memory/runs/gap_map/stack.json` line 4, `{"goal": "research A", "complexity": 2.0, "at": "2026-08-09T13:01:09.552389+00:00"}`. Raw check: `watch/inbox/gala_20260925/afterparty/lanes/t13a.check.txt` sections 1 to 2.

## Why not BIND

- Estate code, configs, and scripts contain zero references to the exact string `"research A"` (check section 4, grep exit 1).
- Candidate rebind targets `memory/runs/gap_swarm_experiment/design.json` + `probes.json` hold 5 fully named research questions (frontier coherence invariants, escalation policy, self-consistency failure modes, emergent vs stochastic convergence, cheap structure extraction). None mentions or is claimed by "research A" (check section 3, grep exit 1). Attaching the label to any of them would invent intent, violating the no-fabrication law.

## Prune executed

- `memory/runs/gap_map/stack.json`: research A item removed, complexity 12.0 -> 10.0 (its own 2.0 contribution), JSON revalidated: 4 items, complexity 10.0 (check sections 7 to 9).
- Byte check passes: stack.json no longer contains the exact string `"research A"` (check section 7, grep exit 1).
- `memory/runs/gpipes/p8bc0180ab9.json` is kept untouched as provenance; it also carries the research B smoke origin (separate brief 2, not pruned here).
- Verdict receipt: `watch/inbox/HELPWANTED_A_VERDICT_20260926.md`.

## What would reopen this

- A named estate research question claiming the literal label "research A" with a source path. None exists as of 2026-09-26.
