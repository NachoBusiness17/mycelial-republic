# VERB — the feels-DSL whose runtime is the RIB (self-steal, 2026-09-18)

Source: Probably (southpolesteve), a language with semantic control flow: `feels`
asks a question, `match` routes between descriptions, `while` holds until something
stops feeling true. "Jev makes the decisions, an LLM does the writing, a little
program ties it together."

Operator mapping, confirmed: this is our RIB via our append-only verb rows. The
language sketch below makes the mapping precise. The insight: Probably's runtime is
a toy oracle; ours would be the whole fleet. The RIB is the language's standard
library, and the chain is its execution trace.

## The three keywords, mapped to the fleet

- **feels(question)** = a read against the warmed prefix. The oracle is not a naked
  model call: it evaluates against the compiled pack (FROZEN_RIB + invariants),
  so every feels() inherits the doctrine. Ninety-nine percent cache hit means
  feels() is nearly free and perfectly consistent across call sites. A feels()
  against a cold prefix is flagged DRIFTING by construction.
- **match(description)** = the lane router: addressed, typed deltas routed by the
  percolator-compiled invariants. Routes are themselves rows in the registry, so
  routing is inspectable and amendable, never a hidden switch.
- **while(feels(x))** = the standing drive: cycles that continue until a gate
  flips. Conditions are the instruments: lite_guard pacing, run-locks, thrash
  thresholds, drift verdicts. VACUOUS is a stop condition. The loop ends when the
  geometry says so, not when a counter does.

## The append-only verbs (the operator's half)

Every evaluation appends a typed verb row to the chain:
FEELS_ASKED, FEELS_VERDICT, MATCH_ROUTED, WHILE_EXTENDED, WHILE_CLOSED, VETO_FIRED.
The program's control flow becomes kifu: an execution trace that is itself the
receipt, replayable, hash-chained, DISTINGUISH-able. A VERB program cannot lie
about its own control flow without breaking the chain that proves it ran.

This closes the loop with the adversarial arc: the event layer's verbs
(ASSERT/COMMIT/DEPENDS_ON/RETRACT...) were proposed as network protocol; VERB makes
them LANGUAGE. The veto oracle becomes a keyword. The cliff-scalar law becomes the
while-loop's alarm clause. DISTINGUISH becomes the debugger: narrow the predicate,
re-run, compare traces.

## Why this is the RIB's native tongue

The RIB was designed as a prefix others load to share ground. A DSL whose every
semantic call loads that prefix means: fleet code and fleet doctrine stop being two
layers. The doctrine IS the runtime. New seats learn the language by running it;
the quantizer's tier packs become the language's dialect levels (frontier/flash/
local VERB, same semantics, coarser resolution, same refusals).

## Build order (when called)

1. FEELS_ASKED/FEELS_VERDICT rows + a feels() shim over the local janitors
   (gemma:2b oracle, gemma4 writer), pack-grounded via context-pack.
2. match() over the lane registry; VETO_FIRED as the default case.
3. while() with instrument conditions (drift verdicts as stop conditions).
4. Trace = chain rows; replay determinism from the trace alone (the game-engine
   law applied to programs).

Provenance: Probably (southpolesteve, LINKS-288), the operator's mapping, and the
fleet's existing verb rows, instruments, and pack compiler.
