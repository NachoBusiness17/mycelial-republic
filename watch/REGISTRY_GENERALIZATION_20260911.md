# REGISTRY GENERALIZATION — "can we do this everywhere? should we?" (2026-09-11 night)

**THE POINT:** The librarian pattern — claim → provenance legend → status →
pull+hash+excerpt → auditor → consult-at-build — already exists in six places
across the fleet. It generalizes to everything, but NOT as more registers: the
same auditor, one shared schema, and registration gated by cost-of-ignorance.
The frontier review's stop-building law applies to registries too.

## Where the pattern already lives (self-steal)

| surface | the pattern's presence |
|---|---|
| verkle chain | the ancestor: knots with parent hashes = provenance chains |
| GROUNDING_WAVE | claim-level tri-state rows, hash-witnessed, second-writer rule |
| BIBLIOGRAPHY_MAP + librarian | today's build: papers, provenance legend, retrieval plans, dust audit |
| kvos_block | artifacts content-addressed, hash-chained per file |
| invariant surface | extracted lines, every one with a source pointer |
| watch cards | tri-state claims with falsifiers |

## Where it's missing (the dust, inventoried)

1. **Claims without witnesses.** Cards say SUPPORTED; the witnesses (hashes,
   pull receipts) live somewhere else or nowhere. Frontiers review: "I have
   your assertion, not the witnesses."
2. **Falsifiers without a ledger.** Pre-registered falsifiers scattered across
   cards; no single register with state (armed / fired / passed / failed /
   expired). A forgotten falsifier is a law that can't fail.
3. **Datasets without schemas.** cachewise traces, kpi.jsonl, estate index —
   no register of (schema, hash, rights, last-used).
4. **Decisions without status.** Operator GO/no-go rulings scattered in CONVO;
   no register saying active / superseded / expired.
5. **Model pins.** Post-abliteration, trusted-weights hashes need a register
   (lane integrity).
6. **The tool tree.** 950 files, no provenance registry — but stop-building
   says FREEZE FIRST, then register incrementally as tools are touched.

## The design: one schema, one auditor, many tables

Every register is a markdown table with the same six columns:
`id | claim/artifact | provenance ([V]/[M]/[S]/†) | status | last_verified |
consulted_by`. One auditor (librarian.py, generalized) walks ALL registries
with the same checks it already runs: UNREGISTERED (referenced but not
registered), DUST (registered but never consulted), NO-STATUS, ARCHIVE. One
pump: the daily dogfood pass runs the audit; the morning report carries the
deltas. One consult surface: the MCP gateway gains `registry.lookup` so seats
query registers as tools.

## Should we? The gating rule

Register a surface when its dust costs something measurable:
- NOW (already half-built, high value): claims-witness registry (invariant
  surface feeds it), falsifier ledger, dataset register, decision register,
  model-pin register.
- LATER (after the freeze): full tool-tree provenance — register a tool when
  the librarian or a build touches it, not before.
- NEVER as busywork: a register that cannot fail an audit is decoration; if a
  surface's dust costs nothing, it stays unregistered.

## Leveraging what we have
- librarian.py generalizes from one map to the registry directory (same code,
  more tables).
- invariant_surface feeds the claims register (extraction = registration).
- The MCP gateway consult endpoint makes registers load-bearing for every seat.
- The morning report is the pump's output: registry deltas next to burn deltas.
