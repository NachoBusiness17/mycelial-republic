# RIB_RIB_PROBLEM_AUTONOMOUS_LOOP_20260811 - translated by babelfish v1.0.0 (2026-10-10)

**Minted:** 2026-10-10 (caller-supplied; the module reads no clocks).
**Source bytes:** 2,534 | sha256 `cea962550eb071d2981cfe4406e3675c8f04fef486bdba0920bf701793533988`
**Named roles found:** none detected
**Dominant terms:** loop (6), predicate (5), action (5), anchor (5), ghost (5), process (4), drain (4), tools (4)

## THE LAW AS THEY STATE IT (verbatim, their voice)

> Schema: rib_grammar.v0.1 · invariant { id, predicate, action, anchor } · deterministic
> We want the system to run FULL-AUTOMATION: the queue drains, the swarm executes the work, without the
> operator present. Right now it's ARMED but NOT RUNNING.
> - The drainer is a SUPERVISED loop: `process_supervisor` supervises
> `from mag.governor_autorun import autorun_loop; autorun_loop(5.0)`.
> operator_active, with FORCE overriding operator_active). It does NOT start the process.

## THE INVARIANT TRANSLATION (each row names its check; status UNVERIFIED until run)

| their claim | invariant form | the check |
|---|---|---|
| - `.env` MAG_DRAINER=1 + MAG_DRAINER_FORCE=1 only GATES it (autorun_allowed = enabled AND not | MAG_DRAINER = RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |
| - Evidence: governor_autorun_trail.jsonl last wrote 2026-08-06 -> the drainer is NOT running. | jsonl last wrote 2026-08-06 - > RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |

## INSTRUMENT ROWS (measurable with a named instrument)

| claim | instrument |
|---|---|
| predicate: report grounded truth (armed vs running, evidence from artifacts) — never overclaim | sample N instances per the universal's domain and count exceptions |

## REGISTER (the unmappable remainder - kept verbatim, never struck)

The babel fish preserves what it cannot translate. Register is the
seed, not the defect.

- - To actually run it, the SUPERVISOR (process_supervisor.start_all / start_loop) must be launched,
- which spawns the drain loop. That is the real "turn on the loop."
- - id: use-ghost-tools-in-process
- predicate: ghost work runs via in-process mem-tool functions, NOT `python -m` CLI / terminal
- action: default to ghost tools; the CLI/terminal prompts the operator
- anchor: training-use-mem-tools-not-cli / training-ghost-tools-by-default
- - id: don't-prompt-standing-autonomy
- predicate: when the operator grants autonomy ("just do it", full-automation handoff), execute
- end-to-end with ZERO approval pings; only interrupt for a genuine hard blocker
- action: run the full-automation handoff (dinner-run pattern: keep shipping, skip blockers)
- anchor: routing.md / autonomous standing permission
- - id: honest-state-not-claim
- action: state whether the loop is actually executing, backed by the trail/queue evidence
- anchor: grounding-and-origin / window-bug truth
- - id: execution-over-accumulation
- predicate: land work, fold the win, then dispatch more; don't build a backlog that sits
- action: the loop must actually drain; verify via artifacts, not handoff files
- anchor: cadence-rightsize
- 1. Start the SUPERVISOR (the real launch — via ghost's in-process path / the proper launch tool,
- NOT `python -m` terminal CLI).

## FALSIFIERS

- For each invariant row: run its named check against primary bytes;
  a mismatch kills the row, not the corpus.
- For the translation itself: a second pass over the same bytes must
  produce a byte-identical rib (determinism law).
- Class-deafness: an estate-authored doc must yield nonzero invariant
  rows and a woo corpus must yield nonzero REGISTER rows (spec falsifier).

## LINEAGE

- Translated by babelfish v1.0.0 (2026-10-10); spec watch/inbox/babelfish_20261010/SPEC.md
- Operator thesis: book-to-skill == closed-corpus-to-self-improving-system,
  in the direction you set, despite the platform's best wishes (2026-10-10).
