# ZERO-CONTEXT DELEGATION

Decisions only exist if they **compile to a file a zero-context executor can check and
run**. The swarm that builds from your output cannot read your mind — only your files.
Assume competence, assume zero context, assume one chance.

## 1. Decisions compile: the RIB file

Every invariant is a four-field tuple, deterministic, compilable:

| field | rule |
|---|---|
| `id` | content-addressed name (hash of canonical form) |
| `predicate` | the CHECKABLE condition asserted — deterministic, same-input-same-output |
| `action` | the enforcement when the predicate fails: guard / hook / route / gate — or explicitly `NONE` if pure doctrine |
| `anchor` | pointer at a REAL file the invariant binds to |

Target path: `memory/rib/RIB_<name>_<date>.md`. The RIB precedes the flock: these files
are not your diary — they are the instructions the cheap swarm executes. A decision that
never became a RIB never happened. The grammar stays deterministic: the LLM may help
draft, never execute, the invariant.

## 2. Specs are written for a stranger with one chance

**What you left vague, the swarm builds vague** — vagueness propagates 1:1 into what
gets built. Write every spec as if the reader never met the author, because it didn't.

## 3. Solutions ship as replayable solve-packets

Per module/job, four sections:

| section | bar |
|---|---|
| SOLUTION PATH | reproducible by a stranger: same inputs, same states, no judgment calls mid-path |
| VALIDATION | the mechanic by engine function or JSON field; what breaks if built wrong |
| TEST ORACLE | input tape + expected state hash-points |
| GAPS FILLED | stubs specified, not described |

## The pre-registered bars (fail these, the delegation failed)

- [ ] every solution path REPLAYS (no mid-path judgment calls)
- [ ] every invariant compiles (predicate checkable, action executable or NONE, anchor real)
- [ ] no new engine invented inside the delegated window
- [ ] nothing described that is not specified

## Receipt

- watch/inbox/ASTRA_HOUR_BRIEF.md:19-34 (estate) — RIB grammar reference :19, solve-packet
  contract :23, "what you left vague" :25, bars :27-31, cathedral clause :33-34 — read this session.
- memory/rib/RIB_GRAMMAR_SEED_20260810.md:1-9, :47-51 (estate) — the four-field grammar +
  the no-stochastic-translation compiler note — read this session.
