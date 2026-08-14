# RIB — The RIB Protocol: manufacturing memory states without execution
**Schema:** rib.rib_protocol_simulation.v1 · date 2026-08-10
**Operator's realization:** "the file structures we are going to run from terminal are really just
manufacturing memory states. if we can simulate them we don't even need them to run we just need to
know where to put their outputs." + "this could be automated via the rib protocol no?" — YES.

## The core insight
Every program/tool we run from a terminal is a **transform that manufactures a memory state**: it
reads known inputs (files/config/state), applies a deterministic transformation, and writes the
result to a known path. The **RIB is already the geometric map** of those paths and contracts. So a
deterministic memory-manufacturing program doesn't need to RUN — it needs its **output computed and
placed at the right location**. The RIB protocol automates this: contract registry + simulate +
place, instead of execute.

## What the RIB protocol is
A registry, seeded by the RIB, of every memory-manufacturing transform:
| Transform | Reads (inputs) | Writes (output) | Output location |
|---|---|---|---|
| state_quantizer | verkle chain | summary knot | `memory/ghost/quantum_state/summary_knots.jsonl` |
| solved_surface | pro_library + RIB + verkle_tip | solved list | `GET /api/v1/solved` |
| source_trace.sense | process snapshot | verdict | ghost trail |
| guard_registry.reconcile | probes | guard state | `memory/runs/guard_registry.json` |
| diary/story/bard | filed beads | narrative | `memory/diary_latest.md` / story |
| the flock pods | RIB file | steal knot | `memory/biography/knots/` + research_packs |

Each is a **pure-ish transform**: inputs → transform → output at a known path. The RIB already knows
these paths (that's what I've been reading all session).

## The protocol (automate it)
1. **Contract registry** — the RIB declares each transform's `{inputs, fn, output_path}` (one row per
   memory-manufacturing program). This IS the map of "where to put their outputs."
2. **Simulate / place** — for a deterministic transform, compute the output in-memory (call the `fn`
   directly as a function — no terminal, no subprocess) and **write it to the declared output_path**.
   The program "ran" — its memory state was manufactured and placed.
3. **No execution layer** — terminal/subprocess execution is replaced by "compute + place." The
   dispatcher reads the RIB contract, calls the transform, files the output. Everything routes
   through the memory substrate, not the shell.
4. **Fold** — each manufactured state is a knot; the lattice compounds.

## Why this is the RIB protocol specifically
The RIB is not a doc — it's the **executable contract map**. It already encodes:
- where every program stores its data (the paths I've been reading),
- the solved history (solved_surface),
- the surfaces-as-spec (each transform's contract).

So the RIB IS the registry. "Automating via the rib protocol" = turning the RIB's knowledge into a
dispatcher: **read the contract from the RIB, compute the output, place it.** The terminal layer
collapses because the RIB already knows where everything goes.

## The honest limits (what CAN'T be simulated)
- **External APIs / real model calls** (a frontier call, a provider) need execution — you can't
  simulate an API response without calling it. Those stay as real executions (the flock/fleet).
- **Non-deterministic or stateful external systems** (a live process, a remote) need a real run.
- Everything else — the deterministic memory-manufacturing transforms we've been running from
  terminal — becomes compute+place, $0, no shell.

## The shape
```
RIB contract registry (transform → inputs, fn, output_path)
        │  dispatcher
        ▼
   compute output (in-process fn) ──► place at output_path ──► fold as knot
   (no terminal, no subprocess for deterministic transforms)
```
This is the "do everything without the terminal" doctrine made structural: the RIB protocol simulates
the memory-manufacturing layer and places outputs, so the shell becomes optional and the memory
substrate is the only surface.

## Fold
This is the automation of "we just need to know where to put their outputs." Seed the RIB contract
registry (a `rib_dispatcher`) that reads the RIB, computes, and places — replacing the terminal
execution layer for deterministic transforms.
