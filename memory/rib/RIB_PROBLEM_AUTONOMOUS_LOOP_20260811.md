# RIB — the problem: turn on the autonomous loop (2026-08-11)
Schema: rib_grammar.v0.1 · invariant { id, predicate, action, anchor } · deterministic

## The problem (id: autonomous-loop-running)
We want the system to run FULL-AUTOMATION: the queue drains, the swarm executes the work, without the
operator present. Right now it's ARMED but NOT RUNNING.

## Our understanding (grounded, not guessed)
- The drainer is a SUPERVISED loop: `process_supervisor` supervises
  `from mag.governor_autorun import autorun_loop; autorun_loop(5.0)`.
- `.env` MAG_DRAINER=1 + MAG_DRAINER_FORCE=1 only GATES it (autorun_allowed = enabled AND not
  operator_active, with FORCE overriding operator_active). It does NOT start the process.
- Evidence: governor_autorun_trail.jsonl last wrote 2026-08-06 -> the drainer is NOT running.
- To actually run it, the SUPERVISOR (process_supervisor.start_all / start_loop) must be launched,
  which spawns the drain loop. That is the real "turn on the loop."

## Invariants (the laws we keep violating)
- id: use-ghost-tools-in-process
  predicate: ghost work runs via in-process mem-tool functions, NOT `python -m` CLI / terminal
  action: default to ghost tools; the CLI/terminal prompts the operator
  anchor: training-use-mem-tools-not-cli / training-ghost-tools-by-default
- id: don't-prompt-standing-autonomy
  predicate: when the operator grants autonomy ("just do it", full-automation handoff), execute
  end-to-end with ZERO approval pings; only interrupt for a genuine hard blocker
  action: run the full-automation handoff (dinner-run pattern: keep shipping, skip blockers)
  anchor: routing.md / autonomous standing permission
- id: honest-state-not-claim
  predicate: report grounded truth (armed vs running, evidence from artifacts) — never overclaim
  action: state whether the loop is actually executing, backed by the trail/queue evidence
  anchor: grounding-and-origin / window-bug truth
- id: execution-over-accumulation
  predicate: land work, fold the win, then dispatch more; don't build a backlog that sits
  action: the loop must actually drain; verify via artifacts, not handoff files
  anchor: cadence-rightsize

## The clean start
1. Start the SUPERVISOR (the real launch — via ghost's in-process path / the proper launch tool,
   NOT `python -m` terminal CLI).
2. Verify the drain loop writes a NEW trail entry (grounded proof it's alive).
3. Let the queue drain; watch via artifacts, narrated as DM.
